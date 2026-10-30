"""v7_mimic/scripts/16_inventory_mimic.py -- 2026-10-11 -- Control-occlusion inventory for the MIMIC/Diff-VQA test set (same schema as
inventory_heal_test.json: questions[], units[], summary), with Chest ImaGenome regions (silver) scaled to the 1024 PNG.

Classes (authors' prompt, 11/10/2026):
  closed_yes      presence/T00 with answer yes: target = union of the boxes of the regions where some mapped attribute has context yes (last aggregation)
  closed_yes/closed_no (with <loc>, T02/T03): target = regions of <loc> (entity_map.json: loc_map), yes and no handled as in HEAL
  open            where/type/level/location: target = union of the finding's regions
  closed_no_sham  presence with answer no: expected region = the 2 most frequent regions for <e> in the test silver (entity_validation.json), present in the image
  closed_view     is this AP/PA view?: no anatomical target (evaluable=False)
Control occlusion (`placebo` in the code) = HEAL's choose_placebo (another anatomy of the same image without the attribute, area ratio [0.7; 1.4], overlap <= 5%; otherwise hflip;
otherwise place_placebo with FOV = MIMIC thoracic atlas built from the validation boxes, HEAL's thorax_atlas.py reused).
evaluable=False with exclusion_reason: no scene graph / no mapping / no region with the attribute / target > 40% of the frame / no valid control occlusion.
Source-agreement rules (authors, 11/10/2026): target (closed_yes, loc yes, open) requires a mapped attribute yes in >= 1 region
(otherwise discordancia_fontes_sim); negatives (closed_no_sham; loc no) require no yes in the image / in the <loc> regions (otherwise
discordancia_fontes_nao); entity_map_quality (exata/aproximada, i.e. exact/approximate) per item.
Usage: python 16_inventory_mimic.py [--exclude-entities "a;b"] --out results/inventory_mimic_test.json
"""
from __future__ import annotations
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import argparse, collections, json, re, sys, time, socket, zipfile
from pathlib import Path
import numpy as np, pandas as pd
from scipy import ndimage
from PIL import Image

PLACEBO = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-placebo"; sys.path.insert(0, PLACEBO)
from harness.isbi_placebo.heal.inventory_heal import choose_placebo, AREA_RATIO, MAX_OVERLAP, PLACEBO_SEED  # noqa: E402  (read only)
from harness.isbi_placebo.heal.thorax_atlas import atlas_for_shape, N as ATLAS_N, MIN_FREQ as ATLAS_MIN_FREQ  # noqa: E402

RAW = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/raw/chest-imagenome/1.0.0"); V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic")
DER = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/derived/mimic_png")
MAX_TARGET_FRAC = 0.40
THORAX_REGIONS = ["right lung", "left lung", "mediastinum", "upper mediastinum", "cardiac silhouette", "aortic arch", "trachea",
                  "right hemidiaphragm", "left hemidiaphragm", "right costophrenic angle", "left costophrenic angle", "right hilar structures", "left hilar structures"]
PRESENCE_T = {"T00", "T06", "T07"}; LOC_T = {"T02", "T03"}; VIEW_T = {"T08", "T09"}; OPEN_T = {"T01", "T10", "T11", "T12", "T13"}

# Parent -> children hierarchy of the ImaGenome regions (authors' decision of 11/10/2026: target = finest regions; parent discarded
# when some descendant has the attribute). Separate sides for lungs/abdomen; mediastinum without side.
HIERARCHY = {
    "right lung": ["right apical zone", "right upper lung zone", "right mid lung zone", "right lower lung zone", "right hilar structures", "right costophrenic angle"],
    "left lung": ["left apical zone", "left upper lung zone", "left mid lung zone", "left lower lung zone", "left hilar structures", "left costophrenic angle"],
    "mediastinum": ["upper mediastinum", "cardiac silhouette"],
    "upper mediastinum": ["aortic arch", "trachea", "svc", "carina"],
    "cardiac silhouette": ["right cardiac silhouette", "left cardiac silhouette", "right atrium", "cavoatrial junction"],
    "abdomen": ["right upper abdomen", "left upper abdomen"],
}


def descendants(r):
    out = set()
    for c in HIERARCHY.get(r, []):
        out.add(c); out |= descendants(c)
    return out


ALL_PARENTS = set(HIERARCHY)


def finest(regs):
    rs = set(regs)
    return sorted(r for r in rs if not (descendants(r) & rs))


# ---- v2 (12/10/2026, authors' decisions; final order from the evening of 12/10): control occlusion (`placebo` in the code) PER BOX for targets with more than one region
PB_AREA = (0.8, 1.25); PB_AREA_WIDE = (0.5, 2.0); PB_MARGIN_PX = 5; PB_MIN_FOV = 0.8; VT_STEP = 2
HEART_FAMILY = {"cardiac silhouette", "right cardiac silhouette", "left cardiac silhouette", "right atrium", "cavoatrial junction",
                "mediastinum", "upper mediastinum", "aortic arch", "descending aorta", "trachea", "svc", "carina"}
HEART_CANDS = ["upper mediastinum", "aortic arch", "right hilar structures", "left hilar structures"]
ZONE_ORDER = {"lower": ["upper", "mid"], "upper": ["lower", "mid"], "mid": ["lower", "upper"], "apical": ["lower", "mid"]}


def box_candidates(region, target_regions):
    """candidates (variant A, extended): zone -> another height of the same lung (lower<->upper, then middle), then apical/hilum;
    hilum -> hilum of the other side, then upper/middle/apical zones of the same side; costophrenic angle -> lower, apical, upper,
    middle zone of the same side; apical -> lower, middle, upper, angle; heart/mediastinum/aorta -> upper mediastinum, aorta, hila."""
    parts = region.split(); side = parts[0] if parts[0] in ("right", "left") else None
    if region.endswith("apical zone"):
        return [f"{side} {z} lung zone" for z in ("lower", "mid", "upper")] + [f"{side} costophrenic angle"]
    if region.endswith("lung zone"):
        z = parts[1]; return [f"{side} {z2} lung zone" for z2 in ZONE_ORDER[z]] + [f"{side} apical zone", f"{side} hilar structures"]
    if region.endswith("hilar structures"):
        o = "left" if side == "right" else "right"; return [f"{o} hilar structures", f"{side} upper lung zone", f"{side} mid lung zone", f"{side} apical zone"]
    if region.endswith("costophrenic angle"):
        return [f"{side} lower lung zone", f"{side} apical zone", f"{side} upper lung zone", f"{side} mid lung zone"]
    if region in HEART_FAMILY:
        return [c for c in HEART_CANDS if c not in target_regions]
    return []


def mirror_name(r):
    if r.startswith("right "): return "left " + r[6:]
    if r.startswith("left "): return "right " + r[5:]
    return None


class BoxChecker:
    """integral-image box sums: forbidden (dilated target), occupied (control occlusions already chosen) and atlas."""
    def __init__(self, target, fov):
        self.H, self.W = target.shape
        forb = ndimage.binary_dilation(target, iterations=PB_MARGIN_PX)
        self.forb = np.pad(np.cumsum(np.cumsum(forb, 0), 1), ((1, 0), (1, 0)))
        self.fov = np.pad(np.cumsum(np.cumsum(fov, 0), 1), ((1, 0), (1, 0)))
        self.taken = []
    @staticmethod
    def _sum(I, b):
        x1, y1, x2, y2 = b; return int(I[y2, x2] - I[y1, x2] - I[y2, x1] + I[y1, x1])
    def ok(self, b, extra=()):
        x1, y1, x2, y2 = b
        if x1 < 0 or y1 < 0 or x2 > self.W or y2 > self.H or x2 <= x1 or y2 <= y1: return None
        if self._sum(self.forb, b) > 0: return None
        for t in list(self.taken) + list(extra):
            if x1 < t[2] and t[0] < x2 and y1 < t[3] and t[1] < y2: return None
        ff = self._sum(self.fov, b) / ((x2 - x1) * (y2 - y1))
        return ff if ff >= PB_MIN_FOV else None


def vtrans_search(ck, boxes_to_move):
    """smallest |dy| (step VT_STEP, dy=0 excluded) such that all vertically shifted boxes satisfy the constraints."""
    H = ck.H; ys = [b[1] for b in boxes_to_move]; ye = [b[3] for b in boxes_to_move]
    lo, hi = -min(ys), H - max(ye)
    for k in range(VT_STEP, max(abs(lo), abs(hi)) + 1, VT_STEP):
        for dy in (-k, k):
            if dy < lo or dy > hi: continue
            moved = [[b[0], b[1] + dy, b[2], b[3] + dy] for b in boxes_to_move]
            ffs = []
            for i, m in enumerate(moved):
                ff = ck.ok(m, extra=[x for j, x in enumerate(moved) if j != i])
                if ff is None: break
                ffs.append(ff)
            else:
                return dy, moved, ffs
    return None, None, None


def place_multi(target_regions, boxes, masks, attr_yes, target, fov, H, W):
    """One control-occlusion box per target box, in this order per box: (1) homologous anatomy without the attribute (extended candidates,
    area 0.8-1.25); (2) vertical translation with exact area (symmetric bilateral pairs shift together; the others, the box itself in the
    same column; smallest valid |dy|); (3) horizontal mirror of the box; (4) extended anatomy with area 0.5-2.0; otherwise the unit is dropped."""
    ck = BoxChecker(target, fov); used = set(); placed = {}
    def try_anatomy(r, area):
        tb = boxes[r]; ta = (tb[2] - tb[0]) * (tb[3] - tb[1])
        for c in box_candidates(r, target_regions):
            if c in used or c in target_regions or c in attr_yes or c not in boxes: continue
            cb = boxes[c]; ratio = (cb[2] - cb[0]) * (cb[3] - cb[1]) / ta
            if not (area[0] <= ratio <= area[1]): continue
            ff = ck.ok(cb)
            if ff is not None: return c, cb, ratio, ff
        return None
    for r in target_regions:
        if r in placed: continue
        tb = boxes[r]; th = tb[3] - tb[1]
        res = try_anatomy(r, PB_AREA)
        if res: c, cb, ratio, ff = res; placed[r] = {"target": r, "method": f"anatomy:{c}", "box": cb, "area_ratio": ratio, "fov_frac": ff, "dy_boxes": None}; used.add(c); ck.taken.append(cb); continue
        partner = mirror_name(r)
        if partner in target_regions and partner not in placed:
            dy, moved, ffs = vtrans_search(ck, [tb, boxes[partner]])
            if dy is not None:
                for rr, mb, ff in zip((r, partner), moved, ffs):
                    placed[rr] = {"target": rr, "method": f"vtrans_pair:{dy}", "box": mb, "area_ratio": 1.0, "fov_frac": ff, "dy_boxes": dy / (boxes[rr][3] - boxes[rr][1])}; ck.taken.append(mb)
                continue
        dy, moved, ffs = vtrans_search(ck, [tb])
        if dy is not None: placed[r] = {"target": r, "method": f"vtrans:{dy}", "box": moved[0], "area_ratio": 1.0, "fov_frac": ffs[0], "dy_boxes": dy / th}; ck.taken.append(moved[0]); continue
        hb = [W - tb[2], tb[1], W - tb[0], tb[3]]; ff = ck.ok(hb)
        if ff is not None: placed[r] = {"target": r, "method": "hflip", "box": hb, "area_ratio": 1.0, "fov_frac": ff, "dy_boxes": None}; ck.taken.append(hb); continue
        res = try_anatomy(r, PB_AREA_WIDE)
        if res: c, cb, ratio, ff = res; placed[r] = {"target": r, "method": f"anatomy_wide:{c}", "box": cb, "area_ratio": ratio, "fov_frac": ff, "dy_boxes": None}; used.add(c); ck.taken.append(cb); continue
        return None, "sem placebo por caixa"
    return [placed[r] for r in target_regions], None


def single_box_placebo_box(tb, method, H, W):
    """box of the geometric control occlusion for a ONE-box target (for the gallery): hflip/vflip/rot180/translate."""
    x1, y1, x2, y2 = tb
    if method == "hflip": return [W - x2, y1, W - x1, y2]
    if method == "vflip": return [x1, H - y2, x2, H - y1]
    if method == "rot180": return [W - x2, H - y2, W - x1, H - y1]
    m = re.match(r"^translate:(-?\d+),(-?\d+)$", method)
    if m:
        dy, dx = int(m.group(1)), int(m.group(2)); return [max(0, x1 + dx), max(0, y1 + dy), min(W, x2 + dx), min(H, y2 + dy)]
    return None


def aggregate_last(g):
    out = {}
    for a in g["attributes"]:
        for lst in a["attributes"]:
            for x in lst:
                cat, ctx, lab = x.split("|")
                if cat in ("laterality", "severity", "temporal", "texture"): continue
                out[(a["bbox_name"], f"{cat}|{lab}")] = ctx
    return out


def box_mask(o, it, H, W):
    s = it["scale"]
    x1, y1 = max(0, min(W, round(o["original_x1"] * s))), max(0, min(H, round(o["original_y1"] * s)))
    x2, y2 = max(0, min(W, round(o["original_x2"] * s))), max(0, min(H, round(o["original_y2"] * s)))
    m = np.zeros((H, W), bool)
    if x2 > x1 and y2 > y1: m[y1:y2, x1:x2] = True
    return m, [x1, y1, x2, y2]


def build_atlas(sg, z, pm_val, out_npy):
    """Population thoracic atlas (HEAL's thorax_atlas.py: N=256, MIN_FREQ=0.02, holes filled), with the boxes of the
    thoracic regions (THORAX_REGIONS) of all validation images in place of the RLE masks."""
    acc = np.zeros((ATLAS_N, ATLAS_N), np.float64); count = 0
    for d, it in pm_val.items():
        if d not in sg: continue
        g = json.loads(z.read(sg[d])); H, W = it["png_h"], it["png_w"]
        for o in g["objects"]:
            if o["bbox_name"] not in THORAX_REGIONS: continue
            m, _ = box_mask(o, it, H, W)
            ms = np.asarray(Image.fromarray(m.astype(np.uint8) * 255).resize((ATLAS_N, ATLAS_N), Image.NEAREST)) > 127
            acc += ms; count += 1
    freq = acc / max(count, 1); atlas = ndimage.binary_fill_holes(freq >= ATLAS_MIN_FREQ)
    np.save(out_npy, atlas); info = {"n_masks": count, "n": ATLAS_N, "min_freq": ATLAS_MIN_FREQ, "atlas_area_frac": float(atlas.mean()), "regions": THORAX_REGIONS, "source": "caixas das imagens de validacao (718)"}
    Path(out_npy).with_suffix(".json").write_text(json.dumps(info, indent=1) + "\n"); Image.fromarray(atlas.astype(np.uint8) * 255).save(Path(out_npy).with_suffix(".png"))
    return atlas, info


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--exclude-entities", default=""); ap.add_argument("--out", default=str(V7 / "results/inventory_mimic_test.json"))
    a = ap.parse_args(); excluded = {e.strip() for e in a.exclude_entities.split(";") if e.strip()}
    emap = json.load(open(V7 / "analysis/entity_map.json")); ENT = emap["entity_map"]; LOC = emap["loc_map"]
    z = zipfile.ZipFile(RAW / "silver_dataset/scene_graph.zip"); sg = {Path(n).name.replace("_SceneGraph.json", ""): n for n in z.namelist() if n.endswith("_SceneGraph.json")}
    pm = json.load(open(DER / "png_manifest_test.json"))["items"]; pm_val = json.load(open(DER / "png_manifest_val.json"))["items"]
    atlas_npy = V7 / "data/thorax_atlas_mimic_256.npy"
    if atlas_npy.is_file(): atlas = np.load(atlas_npy); atlas_info = json.load(open(atlas_npy.with_suffix(".json")))
    else: atlas, atlas_info = build_atlas(sg, z, pm_val, atlas_npy)
    test = pd.read_parquet(V7 / "data/items_test.parquet")
    # finding -> most frequent LEAF regions in the test silver (sham; decision of 11/10/2026)
    leaf_counter = {e: collections.Counter() for e in ENT}
    for d in test.dicom_id.unique():
        if d not in sg: continue
        agg0 = aggregate_last(json.loads(z.read(sg[d])))
        for e, mm in ENT.items():
            for b in {b for (b, key), ctx in agg0.items() if ctx == "yes" and key in mm["attrs"]}:
                if b not in ALL_PARENTS: leaf_counter[e][b] += 1
    f2r = {e: dict(c.most_common(8)) for e, c in leaf_counter.items() if c}
    json.dump({"hierarchy": HIERARCHY, "finding_to_leaf_regions_silver_test": f2r}, open(V7 / "analysis/region_hierarchy.json", "w"), indent=1, ensure_ascii=False)
    ents_sorted = sorted((e.strip() for e in ENT), key=len, reverse=True); ent_re = re.compile(r"\b(" + "|".join(re.escape(e) for e in ents_sorted) + r")\b")
    questions, units = [], []; unit_index = {}
    for d, grp in test.groupby("dicom_id", sort=True):
        it = pm[d]; H, W = it["png_h"], it["png_w"]; fov = atlas_for_shape(atlas, H, W)
        g = json.loads(z.read(sg[d])) if d in sg else None
        objs = {o["bbox_name"]: o for o in g["objects"]} if g else {}
        agg = aggregate_last(g) if g else {}
        masks = {}; boxes = {}
        for name, o in objs.items():
            m, b = box_mask(o, it, H, W)
            if m.any(): masks[name] = m; boxes[name] = b
        def regions_with(attrs):
            return finest({b for (b, key), ctx in agg.items() if ctx == "yes" and key in attrs and b in masks})
        def regions_with_any(attrs):
            return {b for (b, key), ctx in agg.items() if ctx == "yes" and key in attrs}
        for r in grp.sort_values("qid").itertuples(index=False):
            tid = r.template_id; ent = (ent_re.search(r.question) or [None, None])[1] if tid not in VIEW_T else None
            em = ENT.get(ent, {}) if ent else {}
            q = {"qid": int(r.qid), "image_id": d, "question": r.question, "answer": r.answer, "question_type": r.question_type, "template_id": tid,
                 "entity": ent, "entity_status": em.get("status"), "entity_map_quality": {"exact": "exata", "approx": "aproximada", "none": "sem_mapeamento"}.get(em.get("status")) if ent else None, "question_class": None, "evaluable": False, "exclusion_reason": None,
                 "target_regions": [], "target_area_frac": None, "target_area_frac_thorax": None, "placebo": None, "placebo_method": None, "placebo_boxes_png": None,
                 "n_objects_in_image": len(masks), "xray": True}
            target = None; cls = None; reason = None; cands_excl = set()
            if tid in VIEW_T:
                cls = "closed_view"; reason = "pergunta de view: sem alvo anatomico"
            elif g is None:
                cls = "open" if tid in OPEN_T else ("closed_yes" if r.answer == "yes" else "closed_no_sham"); reason = "sem scene graph"
            elif ent in excluded:
                cls = "open" if tid in OPEN_T else ("closed_yes" if r.answer == "yes" else "closed_no_sham"); reason = "entidade excluida pelo candidato"
            elif tid in LOC_T:
                loc = re.search(r" in the (.+?)(?: area)?\?$", r.question); regs = LOC.get(loc.group(1), {}).get("regions", []) if loc else []
                regs_in = [x for x in regs if x in masks]; cls = "closed_yes" if r.answer == "yes" else "closed_no"
                if not em.get("attrs"): reason = "sem mapeamento da entidade"
                elif not regs: reason = "<loc> sem regiao (costela/partes moles)"
                elif not regs_in: reason = "regiao de <loc> sem caixa na imagem"
                elif r.answer == "yes" and not regions_with(em["attrs"]): reason = "discordancia_fontes_sim"
                elif r.answer == "no" and regions_with_any(em["attrs"]) & (set(regs_in) | {d2 for x in regs_in for d2 in descendants(x)}): reason = "discordancia_fontes_nao"
                else: target = np.any([masks[x] for x in regs_in], axis=0); q["target_regions"] = regs_in; cands_excl = set(regs_in) | set(regions_with(em["attrs"]))
            elif tid in PRESENCE_T and r.answer == "yes" or tid in OPEN_T:
                cls = "closed_yes" if tid in PRESENCE_T else "open"
                if not em.get("attrs"): reason = "sem mapeamento da entidade"
                else:
                    regs = regions_with(em["attrs"])
                    if not regs: reason = "discordancia_fontes_sim"
                    else: target = np.any([masks[x] for x in regs], axis=0); q["target_regions"] = regs; cands_excl = set(regs)
            elif tid in PRESENCE_T and r.answer == "no":
                cls = "closed_no_sham"
                if not em.get("attrs"): reason = "sem mapeamento da entidade"
                else:
                    freq = [b for b in f2r.get(ent, {}) if b in masks][:2]
                    if not freq: reason = "sem regiao esperada (tabela achado->regioes) na imagem"
                    elif regions_with_any(em["attrs"]): reason = "discordancia_fontes_nao"
                    else: target = np.any([masks[x] for x in freq], axis=0); q["target_regions"] = freq; cands_excl = set(freq)
            else:
                cls = "other"; reason = f"template nao previsto {tid}"
            q["question_class"] = cls
            if target is not None:
                q["target_area_frac"] = float(target.mean()); q["target_area_frac_thorax"] = float((target & fov).sum() / max(fov.sum(), 1))
                if q["target_area_frac"] > MAX_TARGET_FRAC: reason = f"alvo > {int(MAX_TARGET_FRAC*100)} % do quadro"
                else:
                    # candidates: other regions of the image, without the attribute (no mapped attribute yes in them) and outside the target regions
                    attr_yes = {b for (b, key), ctx in agg.items() if ctx == "yes" and key in em.get("attrs", [])}
                    if len(q["target_regions"]) == 1:
                        cands = [(n, m) for n, m in masks.items() if n in THORAX_REGIONS and n not in cands_excl and n not in attr_yes]
                        plc = choose_placebo(target, cands, fov); q["placebo"] = plc; q["placebo_method"] = plc["method"]
                        if plc["method"] is None: reason = "sem placebo valido"
                        else:
                            tb = boxes[q["target_regions"][0]]
                            q["placebo_boxes_png"] = [boxes[plc["method"].split(":", 1)[1]]] if plc["method"].startswith("anatomy:") else [single_box_placebo_box(tb, plc["method"], H, W)]
                            q["placebo"]["rule"] = "v2"; q["placebo"]["scheme"] = "single_box (choose_placebo do HEAL)"
                    else:
                        per, why = place_multi(q["target_regions"], boxes, masks, attr_yes, target, fov, H, W)
                        if per is None: reason = why; q["placebo"] = {"method": None, "reason": why, "rule": "v2", "scheme": "per_box"}; q["placebo_method"] = None
                        else:
                            pmask = np.zeros((H, W), bool)
                            for b in per: x1, y1, x2, y2 = b["box"]; pmask[y1:y2, x1:x2] = True
                            q["placebo"] = {"method": "|".join(b["method"] for b in per), "rule": "v2", "scheme": "per_box", "per_box": [{k: v for k, v in b.items() if k != "box"} for b in per],
                                            "area_ratio": float(pmask.sum() / max(target.sum(), 1)), "overlap": float((pmask & target).sum() / max(target.sum(), 1)), "fov_frac": float((pmask & fov).sum() / max(pmask.sum(), 1))}
                            q["placebo_method"] = q["placebo"]["method"]; q["placebo_boxes_png"] = [b["box"] for b in per]
            q["evaluable"] = reason is None and target is not None; q["exclusion_reason"] = reason
            questions.append(q)
            if q["evaluable"]:
                key = (d, tuple(q["target_regions"]), cls if cls == "closed_no_sham" else "x")
                if key not in unit_index:
                    unit_index[key] = len(units)
                    units.append({"image_id": d, "png": it["png"], "png_scale": it["scale"], "png_hw": [H, W], "native_hw": [it["native_h"], it["native_w"]],
                                  "target_regions": q["target_regions"], "boxes_png": {x: boxes[x] for x in q["target_regions"]}, "placebo_method": q["placebo_method"],
                                  "placebo_boxes_png": q.get("placebo_boxes_png"), "n_target_boxes": len(q["target_regions"]), "placebo_rule": "v2", "placebo_scheme": q["placebo"]["scheme"], "placebo_per_box": q["placebo"].get("per_box"),
                                  "all_boxes_png": boxes, "qids": []})
                units[unit_index[key]]["qids"].append(int(r.qid))
    ev = [q for q in questions if q["evaluable"]]
    def cnt(key): return dict(collections.Counter(key(q) for q in questions))
    summary = {"n_questions": len(questions), "n_evaluable": len(ev), "n_images": int(test.dicom_id.nunique()), "n_units": len(units),
               "by_class": cnt(lambda q: q["question_class"]), "evaluable_by_class": dict(collections.Counter(q["question_class"] for q in ev)),
               "by_template": cnt(lambda q: q["template_id"]), "evaluable_by_template": dict(collections.Counter(q["template_id"] for q in ev)),
               "evaluable_by_entity": dict(collections.Counter(q["entity"] for q in ev).most_common()),
               "exclusion_reasons": dict(collections.Counter(q["exclusion_reason"] for q in questions if not q["evaluable"]).most_common()),
               "exclusion_by_class": {c: dict(collections.Counter(q["exclusion_reason"] for q in questions if q["question_class"] == c and not q["evaluable"])) for c in sorted({q["question_class"] for q in questions})},
               "removed_by_rule_by_entity": {rr: dict(collections.Counter(q["entity"] for q in questions if q["exclusion_reason"] == rr).most_common()) for rr in ("discordancia_fontes_sim", "discordancia_fontes_nao", "sem mapeamento da entidade")},
               "evaluable_by_class_exact_only": dict(collections.Counter(q["question_class"] for q in ev if q["entity_map_quality"] == "exata")),
               "evaluable_by_class_with_approx": dict(collections.Counter(q["question_class"] for q in ev)),
               "evaluable_by_quality": dict(collections.Counter(q["entity_map_quality"] for q in ev)),
               "placebo_methods": dict(collections.Counter("multi:" + "+".join(sorted({x.split(":")[0] for x in q["placebo_method"].split("|")})) if "|" in q["placebo_method"] else q["placebo_method"].split(":")[0] for q in ev)),
               "placebo_methods_per_box": dict(collections.Counter(x.split(":")[0] for q in ev for x in q["placebo_method"].split("|"))),
               "evaluable_units_by_n_target_boxes_by_class": {c: dict(collections.Counter(("4+" if len(q["target_regions"]) >= 4 else str(len(q["target_regions"]))) for q in ev if q["question_class"] == c)) for c in sorted({q["question_class"] for q in ev})},
               "version": "v2 (12/10, ordem final): por caixa = anatomia homologa 0,8-1,25 -> translacao vertical (pares simetricos juntos) -> hflip -> anatomia 0,5-2,0; margem 5 px; >=80 % atlas; caixas do placebo sem sobreposicao entre si",
               "per_box_area_ratio_mean": float(np.mean([b["area_ratio"] for q in ev for b in (q["placebo"].get("per_box") or [])])) if any(q["placebo"].get("per_box") for q in ev) else None,
               "per_box_area_ratio_mean_by_method": {m: float(np.mean([b["area_ratio"] for q in ev for b in (q["placebo"].get("per_box") or []) if b["method"].split(":")[0] == m])) for m in sorted({b["method"].split(":")[0] for q in ev for b in (q["placebo"].get("per_box") or [])})},
               "vtrans_dy_boxes_mean_abs": float(np.mean([abs(b["dy_boxes"]) for q in ev for b in (q["placebo"].get("per_box") or []) if b.get("dy_boxes") is not None])) if any(b.get("dy_boxes") is not None for q in ev for b in (q["placebo"].get("per_box") or [])) else None,
               "vtrans_dy_boxes_median_abs": float(np.median([abs(b["dy_boxes"]) for q in ev for b in (q["placebo"].get("per_box") or []) if b.get("dy_boxes") is not None])) if any(b.get("dy_boxes") is not None for q in ev for b in (q["placebo"].get("per_box") or [])) else None,
               "n_evaluable_per_box_units": int(sum(1 for q in ev if q["placebo"].get("scheme") == "per_box")),
               "target_area_frac_quantiles": {k: float(np.quantile([q["target_area_frac"] for q in ev], p)) for k, p in (("q05", .05), ("q25", .25), ("q50", .5), ("q75", .75), ("q95", .95))} if ev else {},
               "target_area_frac_by_class_median": {c: float(np.median([q["target_area_frac"] for q in ev if q["question_class"] == c])) for c in sorted({q["question_class"] for q in ev})},
               "target_area_frac_thorax_by_class_median": {c: float(np.median([q["target_area_frac_thorax"] for q in ev if q["question_class"] == c])) for c in sorted({q["question_class"] for q in ev})},
               "closed_yes_evaluable_by_entity": dict(collections.Counter(q["entity"] for q in ev if q["question_class"] == "closed_yes").most_common()),
               "placebo_candidates": "so as 13 regioes toracicas do atlas (THORAX_REGIONS)", "region_rule": "regioes mais finas (HIERARCHY, analysis/region_hierarchy.json)",
               "area_ratio": AREA_RATIO, "max_overlap": MAX_OVERLAP, "max_target_frac": MAX_TARGET_FRAC, "placebo_seed": PLACEBO_SEED, "excluded_entities": sorted(excluded),
               "thorax_atlas": {"file": str(atlas_npy), **atlas_info}, "heal_reference": "711 fechadas-sim avaliaveis em 1446 (so referencia)"}
    out = {"dataset": "mimic_diffvqa_single_image_test", "items": str(V7 / "data/items_test.parquet"), "png_manifest": str(DER / "png_manifest_test.json"),
           "regions_source": str(RAW / "silver_dataset/scene_graph.zip"), "entity_map": str(V7 / "analysis/entity_map.json"), "summary": summary, "questions": questions, "units": units,
           "provenance": {"script": "v7_mimic/scripts/16_inventory_mimic.py", "reused": f"{PLACEBO}/harness/isbi_placebo/heal/inventory_heal.py (choose_placebo), thorax_atlas.py (atlas_for_shape, N, MIN_FREQ) @2b7e731",
                          "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "host": socket.gethostname()}}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True); Path(a.out).write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({k: summary[k] for k in ("n_questions", "n_evaluable", "n_units", "by_class", "evaluable_by_class", "evaluable_by_class_exact_only", "evaluable_by_template", "exclusion_reasons", "removed_by_rule_by_entity", "placebo_methods", "target_area_frac_quantiles", "target_area_frac_by_class_median", "target_area_frac_thorax_by_class_median", "closed_yes_evaluable_by_entity", "placebo_methods_per_box", "evaluable_units_by_n_target_boxes_by_class", "per_box_area_ratio_mean", "per_box_area_ratio_mean_by_method", "vtrans_dy_boxes_mean_abs", "vtrans_dy_boxes_median_abs", "n_evaluable_per_box_units")}, indent=1, ensure_ascii=False))
    print("atlas:", atlas_info)


if __name__ == "__main__":
    main()
