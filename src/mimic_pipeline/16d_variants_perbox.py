"""simulates variants of the per-box rule on the units that failed (analysis only; does not write the inventory)."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json, zipfile, collections, sys
from pathlib import Path
import numpy as np
from scipy import ndimage
sys.path.insert(0, os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic/scripts"); import importlib; M = importlib.import_module("16_inventory_mimic")
from harness.isbi_placebo.heal.thorax_atlas import atlas_for_shape
V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic"); RAW = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/raw/chest-imagenome/1.0.0"); DER = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/derived/mimic_png")
inv = json.load(open(V7 / "results/inventory_mimic_test.json")); Q = inv["questions"]; emap = json.load(open(V7 / "analysis/entity_map.json"))["entity_map"]
z = zipfile.ZipFile(RAW / "silver_dataset/scene_graph.zip"); sg = {Path(n).name.replace("_SceneGraph.json", ""): n for n in z.namelist() if n.endswith("_SceneGraph.json")}
pm = json.load(open(DER / "png_manifest_test.json"))["items"]; atlas = np.load(V7 / "data/thorax_atlas_mimic_256.npy")
ZONES = ["apical zone", "upper lung zone", "mid lung zone", "lower lung zone"]
def cands_ext(r, tr):
    p = r.split(); side = p[0] if p[0] in ("right", "left") else None; base = M.box_candidates(r, tr)
    if r.endswith("hilar structures"): return base + [f"{side} {z}" for z in ("upper lung zone", "mid lung zone", "apical zone")]
    if r.endswith("costophrenic angle"): return base + [f"{side} {z}" for z in ("apical zone", "upper lung zone", "mid lung zone")]
    if r.endswith("apical zone"): return base + [f"{side} upper lung zone", f"{side} costophrenic angle"]
    if r.endswith("lung zone"): return base + [f"{side} apical zone", f"{side} hilar structures"]
    return base
def place(q, boxes, masks, attr_yes, target, fov, H, W, cand_fn, area, vflip):
    forb = ndimage.binary_dilation(target, iterations=5); used = set(); taken = np.zeros_like(target); methods = []
    def ok(b):
        x1, y1, x2, y2 = b
        if x1 < 0 or y1 < 0 or x2 > W or y2 > H or x2 <= x1 or y2 <= y1: return None
        m = np.zeros((H, W), bool); m[y1:y2, x1:x2] = True
        if (m & forb).any() or (m & taken).any() or (m & fov).sum() / m.sum() < 0.8: return None
        return m
    for r in q["target_regions"]:
        tb = boxes[r]; ta = (tb[2]-tb[0])*(tb[3]-tb[1]); ch = None
        for c in cand_fn(r, q["target_regions"]):
            if c in used or c in q["target_regions"] or c in attr_yes or c not in boxes: continue
            cb = boxes[c]; ratio = (cb[2]-cb[0])*(cb[3]-cb[1])/ta
            if not (area[0] <= ratio <= area[1]): continue
            m = ok(cb)
            if m is not None: ch = f"anatomy:{c}"; used.add(c); taken |= m; break
        if ch is None:
            m = ok([W-tb[2], tb[1], W-tb[0], tb[3]])
            if m is not None: ch = "hflip"; taken |= m
        if ch is None and vflip:
            m = ok([tb[0], H-tb[3], tb[2], H-tb[1]])
            if m is not None: ch = "vflip"; taken |= m
        if ch is None: return None
        methods.append(ch)
    return methods
VARS = {"v2 (atual)": (M.box_candidates, (0.8, 1.25), False), "A: candidatas ampliadas": (cands_ext, (0.8, 1.25), False),
        "B: A + area 0,5-2,0": (cands_ext, (0.5, 2.0), False), "C: B + vflip por caixa": (cands_ext, (0.5, 2.0), True), "D: v2 + area 0,5-2,0": (M.box_candidates, (0.5, 2.0), False)}
fail = [q for q in Q if q["exclusion_reason"] == "sem placebo por caixa"]; cache = {}
rec = {k: collections.Counter() for k in VARS}; meth = {k: collections.Counter() for k in VARS}
for q in fail:
    d = q["image_id"]; it = pm[d]; H, W = it["png_h"], it["png_w"]
    if d not in cache:
        g = json.loads(z.read(sg[d])); agg = M.aggregate_last(g); boxes = {}; masks = {}
        for n, o in {o["bbox_name"]: o for o in g["objects"]}.items():
            m, b = M.box_mask(o, it, H, W)
            if m.any(): boxes[n] = b; masks[n] = m
        cache[d] = (boxes, masks, agg, atlas_for_shape(atlas, H, W))
    boxes, masks, agg, fov = cache[d]; attrs = emap.get(q["entity"], {}).get("attrs", []); attr_yes = {b for (b, k), c in agg.items() if c == "yes" and k in attrs}
    target = np.any([masks[r] for r in q["target_regions"]], axis=0)
    for k, (cf, ar, vf) in VARS.items():
        ms = place(q, boxes, masks, attr_yes, target, fov, H, W, cf, ar, vf)
        if ms: rec[k][q["question_class"]] += 1; meth[k]["+".join(sorted(set(x.split(":")[0] for x in ms)))] += 1
base = inv["summary"]["evaluable_by_class"]
print("falhas atuais por classe:", dict(collections.Counter(q["question_class"] for q in fail)))
for k in VARS:
    print(f"\n{k}: recupera {sum(rec[k].values())} perguntas -> avaliáveis por classe: " + ", ".join(f"{c} {base.get(c,0)}+{rec[k][c]}={base.get(c,0)+rec[k][c]}" for c in ("closed_yes","closed_no","closed_no_sham","open")) + f" | métodos: {dict(meth[k].most_common(6))}")
