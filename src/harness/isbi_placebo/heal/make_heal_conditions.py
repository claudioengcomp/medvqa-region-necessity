"""Condition arrows of the HEAL arm (VinDr test set of HEAL-MedVQA): C0 (PNG from the DICOM, long side 1024,
lossless), T (mask of the target anatomy in black), P (control occlusion from the inventory: another anatomy of the same
image, mirror, or Kvasir placer), S (everything outside the target in black). Unit = (image,
anatomy); the closed-ended questions of that anatomy share the condition image. Masks come from the
RLE (native), placed at native resolution and downscaled to the PNG by nearest neighbour. Manifest with the sha256
of each arrow and of the source PNGs; HTML gallery (10 units + 50 control occlusions) for review.

    python -m harness.isbi_placebo.heal.make_heal_conditions --inventory results/isbi_placebo/inventory_heal_test.json         --annotations data/isbi_placebo/heal/heal_annotations_test.parquet --png-dir <png/test>         --png-manifest data/isbi_placebo/heal/png_manifest_test.json --out-dir data/isbi_placebo         --manifest results/isbi_placebo/manifest_heal.json --gallery docs/isbi/placebo/gallery_heal.html --seed 20260913
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from harness.interventions.arrow_io import write_arrow
from harness.isbi_placebo.conditions import apply_placement, encode_png, fill_region
from harness.isbi_placebo.heal.heal_rle import decode_rle, resize_mask
from harness.isbi_placebo.make_placebo_conditions import _gallery_html

CONDITIONS = ["C0", "T", "P", "S"]
E3_FILLS = ("blur10", "regmean")             # E5/D4 (15/09/2026): T/P_blur10 and T/P_regmean; no blur 4 %, dose or ring
E3_CONDITIONS = [f"{k}_{f}" for f in E3_FILLS for k in ("T", "P")]
ANSWER_LABEL = {"no": 0, "yes": 1}


def _thumb(img: np.ndarray, target=None, placebo=None, size: int = 220) -> str:
    rgb = np.asarray(img, np.uint8).copy()
    if target is not None:
        rgb[target, 0] = np.clip(rgb[target, 0].astype(int) + 140, 0, 255)
    if placebo is not None:
        rgb[placebo, 2] = np.clip(rgb[placebo, 2].astype(int) + 140, 0, 255)
    im = Image.fromarray(rgb); im.thumbnail((size, size)); buf = io.BytesIO(); im.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


PTYPES = ["anatomy", "hflip", "translate", "rot180", "vflip"]
AGROUPS = ["pulmões", "coração", "aorta"]


def _ptype(method: str) -> str:
    return method.split(":")[0]


def _agroup(anatomy: str) -> str:
    a = anatomy.lower()
    return "aorta" if "aorta" in a else ("coração" if "heart" in a else "pulmões")


def _stratified(cells: dict, n: int) -> list:
    """n items split among the cells (type x group) proportionally, with at least 1 per non-empty cell."""
    keys = sorted(cells); total = sum(len(v) for v in cells.values())
    quota = {k: max(1, round(n * len(cells[k]) / total)) for k in keys}
    while sum(quota.values()) > n:
        k = max(keys, key=lambda k: quota[k]); quota[k] -= 1
    out = []
    for k in keys:
        out += cells[k][:quota[k]]
    return out


def _distribution_html(units: list[dict]) -> str:
    import collections
    by = collections.Counter((_ptype(u["placebo_method"]), _agroup(u["anatomy"])) for u in units)
    byq = collections.Counter((_ptype(u["placebo_method"]), _agroup(u["anatomy"])) for u in units for _ in u["qids"])
    h = ["<h2>Distribuição final dos placebos: unidades (perguntas), por tipo de posição × grupo anatômico</h2>",
         "<table border='1'><tr><th>tipo</th>" + "".join(f"<th>{g}</th>" for g in AGROUPS) + "<th>total</th></tr>"]
    for t in PTYPES:
        row = [f"{by[(t, g)]} ({byq[(t, g)]})" for g in AGROUPS]
        h.append(f"<tr><td>{t}</td>" + "".join(f"<td>{c}</td>" for c in row) + f"<td>{sum(by[(t, g)] for g in AGROUPS)} ({sum(byq[(t, g)] for g in AGROUPS)})</td></tr>")
    h.append("<tr><td><b>total</b></td>" + "".join(f"<td>{sum(by[(t, g)] for t in PTYPES)} ({sum(byq[(t, g)] for t in PTYPES)})</td>" for g in AGROUPS)
             + f"<td>{len(units)} ({sum(len(u['qids']) for u in units)})</td></tr></table>")
    return "\n".join(h)


def placebo_mask(target_native: np.ndarray, method: str, other_masks: dict[str, np.ndarray]) -> np.ndarray:
    if method.startswith("anatomy:"):
        return other_masks[method.split(":", 1)[1]]
    return apply_placement(target_native, method)


def generate(inventory: str, annotations: str, png_dir: str, png_manifest: str, out_dir: str, manifest_out: str,
             gallery: str | None, seed: int, conditions: list[str] = CONDITIONS, gallery_n: int = 10, review_n: int = 50) -> dict:
    inv = json.loads(Path(inventory).read_text())
    pm = json.loads(Path(png_manifest).read_text())["items"]
    ann = pd.read_parquet(annotations, columns=["image_id", "anatomy", "mask_rle", "mask_h", "mask_w"])
    rle = {(r.image_id, r.anatomy): (r.mask_rle, int(r.mask_h), int(r.mask_w)) for r in ann.itertuples(index=False)}
    qs = {q["qid"]: q for q in inv["questions"]}
    rows = {c: [] for c in conditions}
    units_out, gallery_items, review_items = [], [], []
    rng = random.Random(seed)
    for u in inv["units"]:
        ev = [qs[q] for q in u["qids"] if qs[q]["evaluable"]]
        if not ev:
            continue
        p = Path(png_dir, f"{u['image_id']}.png")
        png_bytes = p.read_bytes()
        gray = np.asarray(Image.open(io.BytesIO(png_bytes)).convert("L"), np.uint8)
        rgb = np.stack([gray] * 3, axis=-1)
        H, W = gray.shape
        native = {a: decode_rle(*rle[(u["image_id"], a)]) for a in u["anatomies"]}
        by_anatomy: dict[str, list[dict]] = {}
        for q in ev:
            by_anatomy.setdefault(q["anatomy"], []).append(q)
        for anatomy, qlist in by_anatomy.items():
            t_nat = native[anatomy]
            method = qlist[0]["placebo"]["method"]
            p_nat = placebo_mask(t_nat, method, {a: m for a, m in native.items() if a != anatomy})
            t, pl = resize_mask(t_nat, H, W), resize_mask(p_nat, H, W)
            qids = [q["qid"] for q in qlist]
            base = {"questions": [q["question"] for q in qlist], "answers": [[q["answer"]] for q in qlist],
                    "answer_labels": [[ANSWER_LABEL[q["answer"]]] for q in qlist], "answer_scores": [[1.0] for _ in qlist],
                    "image_id": f"heal/{u['image_id']}#{anatomy}", "question_id": qids, "answer_type": [0] * len(qlist), "split": "test"}
            imgs = {}
            for c in conditions:
                if c == "C0":
                    imgs[c] = png_bytes
                elif c == "T":
                    imgs[c] = encode_png(fill_region(rgb, t, "black"))
                elif c == "P":
                    imgs[c] = encode_png(fill_region(rgb, pl, "black"))
                elif c == "S":
                    imgs[c] = encode_png(fill_region(rgb, ~t, "black"))
                elif c[:2] in ("T_", "P_") and c[2:] in E3_FILLS:   # E5/D4: T/P under blur 10 % of the width or region mean color
                    imgs[c] = encode_png(fill_region(rgb, t if c[0] == "T" else pl, c[2:]))
                else:
                    raise ValueError(c)
                rows[c].append({"image": imgs[c], **base})
            units_out.append({"image_id": u["image_id"], "anatomy": anatomy, "qids": qids, "placebo_method": method,
                              "target_area_frac": float(t.mean()), "placebo_area_frac": float(pl.mean()),
                              "overlap_frac": float((t & pl).sum() / max(t.sum(), 1)), "png_sha256": hashlib.sha256(png_bytes).hexdigest(),
                              "png_hw": [H, W]})
            if len(gallery_items) < gallery_n and sum(1 for g in gallery_items if _ptype(g["placebo_method"]) == _ptype(method)) < max(2, gallery_n // len(PTYPES)):
                dec = lambda b: np.asarray(Image.open(io.BytesIO(b)).convert("RGB"))
                gallery_items.append({"image_id": u["image_id"], "target_key": anatomy, "placebo_method": method, "qids": qids,
                                      "questions": [q["question"] for q in qlist],
                                      "panels": [("original", _thumb(rgb)), ("alvo+placebo", _thumb(rgb, t, pl))]
                                      + [(c, _thumb(dec(imgs[c]))) for c in conditions if c != "C0"]})
            review_items.append({"image_id": u["image_id"], "target_key": anatomy, "placebo_method": method, "_t": t, "_p": pl, "_rgb": rgb})
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    man = {"dataset": "heal_vindr_test", "inventory": inventory, "png_manifest": png_manifest, "seed": seed,
           "encoding": {"C0": "PNG do DICOM (lado maior 1024)", "others": "PNG lossless"}, "n_units": len(units_out),
           "n_questions": sum(len(u["qids"]) for u in units_out), "conditions": {}, "checksums": {}, "units": units_out}
    for c in conditions:
        f = f"vqa_heal_placebo_{c}.arrow"; path = Path(out_dir, f)
        write_arrow(pd.DataFrame(rows[c]), str(path))
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        man["conditions"][c] = {"file": f, "sha256": sha, "bytes": path.stat().st_size, "n_units": len(rows[c])}
        man["checksums"][f] = sha
    Path(manifest_out).parent.mkdir(parents=True, exist_ok=True)
    if Path(manifest_out).exists():   # partial round (e.g. only the E3 fills): merge with the conditions already recorded
        old = json.loads(Path(manifest_out).read_text())
        if old.get("n_units") == man["n_units"] and old.get("seed") == seed:
            man["conditions"] = {**old.get("conditions", {}), **man["conditions"]}
            man["checksums"] = {**old.get("checksums", {}), **man["checksums"]}
    Path(manifest_out).write_text(json.dumps(man, indent=1) + "\n")
    if gallery:
        # E4 (15/09/2026): review of control occlusions STRATIFIED by placement type x anatomical group, with the final distribution
        rng.shuffle(review_items)
        cells: dict[tuple[str, str], list] = {}
        for r in review_items:
            cells.setdefault((_ptype(r["placebo_method"]), _agroup(r["target_key"])), []).append(r)
        picked = _stratified(cells, review_n)
        review = [{"image_id": r["image_id"], "target_key": f"{r['target_key']} [{_agroup(r['target_key'])}]", "placebo_method": r["placebo_method"],
                   "src": _thumb(r["_rgb"], r["_t"], r["_p"], 260)} for r in picked]
        dist = _distribution_html(units_out)
        html = _gallery_html("HEAL (VinDr, teste)", gallery_items, review).replace("<h2>Amostra de unidades", dist + "<h2>Amostra de unidades", 1)
        Path(gallery).parent.mkdir(parents=True, exist_ok=True)
        Path(gallery).write_text(html)
    return {k: v for k, v in man.items() if k != "units"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inventory", required=True); ap.add_argument("--annotations", required=True)
    ap.add_argument("--png-dir", required=True); ap.add_argument("--png-manifest", required=True)
    ap.add_argument("--out-dir", required=True); ap.add_argument("--manifest", required=True); ap.add_argument("--gallery", default=None)
    ap.add_argument("--conditions", default=",".join(CONDITIONS)); ap.add_argument("--seed", type=int, default=20260913)
    a = ap.parse_args(argv)
    out = generate(a.inventory, a.annotations, a.png_dir, a.png_manifest, a.out_dir, a.manifest, a.gallery, a.seed, a.conditions.split(","))
    print(json.dumps({k: v for k, v in out.items() if k in ("n_units", "n_questions", "conditions")}, indent=1))


if __name__ == "__main__":
    main()
