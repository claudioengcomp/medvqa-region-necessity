"""v7_mimic/scripts/17_make_mimic_conditions.py -- 2026-10-11 -- arrows of the image conditions of the occlusion experiment on the MIMIC test set (CPU only).

Functional copy of harness/isbi_placebo/heal/make_heal_conditions.py (@2b7e731), which cannot be called without editing because it reads
the HEAL RLE masks (annotation parquet). Differences (recorded in patches/make_conditions_vs_heal.md):
  * masks = Chest ImaGenome boxes scaled to the PNG (inventory: units[].all_boxes_png), union of the target regions;
  * control occlusion (`placebo`): anatomy:<region> -> box of the region; other methods -> conditions.apply_placement (identical to HEAL);
  * evaluable classes closed_yes, closed_no and open in the main conditions (HEAL: closed-ended only); closed_no_sham in SHAM_* arrows;
  * extra conditions requested by the authors: C1 (gray 384x384 RGB 128), S_blur10, S_regmean, doses T1.5/P1.5/T2/P2 (black),
    with the dose control occlusion by masks.place_placebos_by_factor (pre-registered rule of the Kvasir benchmark; FOV = MIMIC thoracic atlas);
  * blur10 computed once per image (same formula as conditions.fill_region: sigma = 10% of the width, gaussian_filter per channel).
Reuses without editing: conditions.fill_region/encode_png/apply_placement, masks.dilate_to_area/place_placebos_by_factor,
arrow_io.write_arrow, thorax_atlas.atlas_for_shape.
Usage: python 17_make_mimic_conditions.py --group main1|blur|regmean|dose|sham --workers 8
"""
from __future__ import annotations
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import argparse, hashlib, io, json, sys, time, socket
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np, pandas as pd
from PIL import Image
from scipy import ndimage
PLACEBO = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-placebo"; sys.path.insert(0, PLACEBO)
from harness.interventions.arrow_io import write_arrow  # noqa: E402
from harness.isbi_placebo.conditions import fill_region, encode_png, apply_placement  # noqa: E402
from harness.isbi_placebo.masks import dilate_to_area, place_placebos_by_factor  # noqa: E402
from harness.isbi_placebo.heal.thorax_atlas import atlas_for_shape  # noqa: E402

V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic"); DER = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/derived/mimic_png")
OUT = V7 / "data/conditions"; QC = V7 / "qc/conditions"; SEED = 20260913
GROUPS = {"main1": ["C0", "C1", "T", "P", "S"], "blur": ["T_blur10", "P_blur10", "S_blur10"], "regmean": ["T_regmean", "P_regmean", "S_regmean"],
          "dose": ["T1.5", "P1.5", "T2", "P2"], "sham": ["C0", "SHAM_black", "SHAM_blur10"]}
MAIN_CLASSES = {"closed_yes", "closed_no", "open"}
VOCAB = json.load(open(V7 / "data/answer_vocab.json"))
ATLAS = np.load(V7 / "data/thorax_atlas_mimic_256.npy")
GRAY384 = None


def gray384():
    b = io.BytesIO(); Image.new("RGB", (384, 384), (128, 128, 128)).save(b, format="PNG"); return b.getvalue()


def box(b, H, W):
    m = np.zeros((H, W), bool); x1, y1, x2, y2 = b; m[y1:y2, x1:x2] = True; return m


def blur_fill(img, blurred, region):
    out = img.copy(); out[region] = blurred[region]; return out


def do_unit(job):
    u, qs, conds = job
    png = (DER / "test" / u["png"]).read_bytes()
    gray = np.asarray(Image.open(io.BytesIO(png)).convert("L"), np.uint8); rgb = np.stack([gray] * 3, -1); H, W = gray.shape
    t = np.any([box(u["all_boxes_png"][r], H, W) for r in u["target_regions"]], axis=0)
    m = u["placebo_method"]
    if u.get("placebo_scheme") == "per_box":   # v2: union of the control-occlusion boxes (one per target box)
        p = np.any([box(b, H, W) for b in u["placebo_boxes_png"]], axis=0)
    else:
        p = box(u["all_boxes_png"][m.split(":", 1)[1]], H, W) if m.startswith("anatomy:") else apply_placement(t, m)
    blurred = None
    if any("blur10" in c for c in conds):
        sig = 10 / 100.0 * W
        bl = np.clip(np.round(ndimage.gaussian_filter(gray.astype(np.float32), sig)), 0, 255).astype(np.uint8); blurred = np.stack([bl] * 3, -1)
    dose = {}
    if any(c[1:] in ("1.5", "2") for c in conds):
        fov = atlas_for_shape(ATLAS, H, W)
        if u.get("placebo_scheme") == "per_box":
            # v2: dilated target in place; each control-occlusion box dilated IN PLACE (dilate_to_area), valid if it does not touch the target
            # dilated (+5 px), >= 80% inside the atlas per box, no overlap between boxes, and dilated target <= 40% of the FOV
            meth, why, pmasks = {}, {}, {}
            for f in (1.5, 2.0):
                k = f"{f:g}"; grown = dilate_to_area(t, f)
                if (grown & fov).sum() / max(fov.sum(), 1) > 0.4: meth[k], why[k] = None, "area_gt_max"; continue
                forb = ndimage.binary_dilation(grown, iterations=5); acc = np.zeros_like(t); okk = True
                for b in u["placebo_boxes_png"]:
                    g = dilate_to_area(box(b, H, W), f)
                    if (g & forb).any() or (g & acc).any() or (g & fov).sum() / g.sum() < 0.8: okk = False; break
                    acc |= g
                if okk: meth[k], why[k], pmasks[k] = "per_box_dilated_in_place", None, acc
                else: meth[k], why[k] = None, "no_valid_placement"
            dose = {"methods": meth, "reasons": why, "fov": fov, "pmasks": pmasks}
        else:
            meth, why = place_placebos_by_factor(t, fov, seed=SEED)
            dose = {"methods": meth, "reasons": why, "fov": fov}
    imgs, info = {}, {}
    for c in conds:
        if c == "C0": imgs[c] = png
        elif c == "C1": imgs[c] = None  # filled in the main process (same bytes)
        elif c in ("T", "SHAM_black"): imgs[c] = encode_png(fill_region(rgb, t, "black"))
        elif c == "P": imgs[c] = encode_png(fill_region(rgb, p, "black"))
        elif c == "S": imgs[c] = encode_png(fill_region(rgb, ~t, "black"))
        elif c in ("T_blur10", "SHAM_blur10"): imgs[c] = encode_png(blur_fill(rgb, blurred, t))
        elif c == "P_blur10": imgs[c] = encode_png(blur_fill(rgb, blurred, p))
        elif c == "S_blur10": imgs[c] = encode_png(blur_fill(rgb, blurred, ~t))
        elif c in ("T_regmean", "P_regmean", "S_regmean"):
            reg = {"T": t, "P": p, "S": ~t}[c[0]]; imgs[c] = encode_png(fill_region(rgb, reg, "regmean"))
        elif c[0] in "TP" and c[1:] in ("1.5", "2"):
            k = c[1:]; f = float(k); grown = dilate_to_area(t, f)
            if c[0] == "T":
                imgs[c] = encode_png(fill_region(rgb, grown, "black")) if dose["methods"][k] else None
            elif dose["methods"][k] is None:
                imgs[c] = None
            elif dose["methods"][k] == "per_box_dilated_in_place":
                imgs[c] = encode_png(fill_region(rgb, dose["pmasks"][k], "black"))
            else:
                imgs[c] = encode_png(fill_region(rgb, apply_placement(grown, dose["methods"][k]), "black"))
            info[c] = {"method": dose["methods"][k], "reason": dose["reasons"][k], "grown_area_frac": float(grown.mean())}
        else:
            raise ValueError(c)
    base = {"questions": [q["question"] for q in qs], "answers": [[q["answer"]] for q in qs], "answer_labels": [[VOCAB[q["answer"]]] for q in qs],
            "answer_scores": [[1.0] for _ in qs], "image_id": f"mimic/{u['image_id']}#{'+'.join(u['target_regions'])}", "question_id": [q["qid"] for q in qs],
            "answer_type": [1 if q["question_class"] == "open" else 0 for q in qs], "split": "test"}
    rec = {"image_id": u["image_id"], "target_regions": u["target_regions"], "qids": base["question_id"], "placebo_method": m, "placebo_rule": u.get("placebo_rule"), "placebo_scheme": u.get("placebo_scheme"),
           "placebo_boxes_png": u.get("placebo_boxes_png"), "n_target_boxes": len(u["target_regions"]), "classes": sorted({q["question_class"] for q in qs}),
           "target_area_frac": float(t.mean()), "placebo_area_frac": float(p.mean()), "overlap_frac": float((t & p).sum() / max(t.sum(), 1)),
           "png_sha256": hashlib.sha256(png).hexdigest(), "png_hw": [H, W], "dose": info}
    return base, imgs, rec


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--group", required=True, choices=list(GROUPS)); ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--n-examples", type=int, default=12)
    a = ap.parse_args(); conds = GROUPS[a.group]
    inv = json.load(open(V7 / "results/inventory_mimic_test.json")); Q = {q["qid"]: q for q in inv["questions"]}
    jobs = []
    for u in inv["units"]:
        qs = [Q[i] for i in u["qids"] if Q[i]["evaluable"]]
        qs = [q for q in qs if (q["question_class"] == "closed_no_sham") == (a.group == "sham")]
        if qs: jobs.append((u, qs, conds))
    tag = "sham" if a.group == "sham" else "placebo"
    rows = {c: [] for c in conds}; recs = []; c1 = gray384(); t0 = time.time()
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for n, (base, imgs, rec) in enumerate(ex.map(do_unit, jobs, chunksize=4), 1):
            for c in conds:
                b = c1 if c == "C1" else imgs[c]
                if b is not None: rows[c].append({"image": b, **base})
            recs.append(rec)
            if n % 200 == 0: print(f"{n}/{len(jobs)} {time.time()-t0:.0f}s", flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    manp = OUT / f"manifest_mimic_{tag}.json"
    man = json.load(open(manp)) if manp.is_file() else {"dataset": "mimic_diffvqa_single_image_test", "inventory": str(V7 / "results/inventory_mimic_test.json"),
                                                         "inventory_sha256": hashlib.sha256((V7 / "results/inventory_mimic_test.json").read_bytes()).hexdigest(), "seed": SEED, "version": "v2 (2026-10-12): placebo por caixa (inventario v2)", "conditions": {}, "units_by_group": {}}
    man["inventory_sha256_now"] = hashlib.sha256((V7 / "results/inventory_mimic_test.json").read_bytes()).hexdigest()
    rng = np.random.default_rng(SEED)
    for c in conds:
        f = OUT / f"vqa_mimic_{tag}_{c}.arrow"; df = pd.DataFrame(rows[c]); write_arrow(df, str(f))
        sha = hashlib.sha256(f.read_bytes()).hexdigest()
        man["conditions"][c] = {"file": str(f), "sha256": sha, "bytes": f.stat().st_size, "n_units": len(df), "n_questions": int(sum(len(x) for x in df.question_id)),
                                "n_by_answer_type": {"closed": int(sum(x.count(0) for x in df.answer_type)), "open": int(sum(x.count(1) for x in df.answer_type))}}
        d = QC / f"{tag}_{c}"; d.mkdir(parents=True, exist_ok=True)
        for i in sorted(rng.choice(len(df), size=min(a.n_examples, len(df)), replace=False)):
            (d / f"{df.image_id.iloc[i].replace('mimic/', '').replace('#', '__').replace(' ', '_')}.png").write_bytes(df.image.iloc[i])
    man["units_by_group"][a.group] = {"n_units": len(recs), "units": recs}
    man["provenance_" + a.group] = {"script": "v7_mimic/scripts/17_make_mimic_conditions.py", "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "host": socket.gethostname(), "seconds": round(time.time() - t0)}
    manp.write_text(json.dumps(man, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({c: {k: v for k, v in man["conditions"][c].items() if k != "file"} for c in conds}, indent=1))


if __name__ == "__main__":
    main()
