"""v7_mimic/scripts/13_bbox_qc.py -- scales the ImaGenome boxes to the PNG (long side 1024) via the `scale` factor of the png_manifest;
20 inspection PNGs in v7_mimic/qc/ (kept on the lab server) + numeric checks (side, center, intensity, crop)."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json, zipfile, random
from pathlib import Path
import numpy as np, pandas as pd
from PIL import Image, ImageDraw
RAW = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/raw/chest-imagenome/1.0.0"); V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic")
DER = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/derived/mimic_png"); QC = V7 / "qc/bbox_scale"; QC.mkdir(parents=True, exist_ok=True)
z = zipfile.ZipFile(RAW / "silver_dataset/scene_graph.zip"); sg = {Path(n).name.replace("_SceneGraph.json", ""): n for n in z.namelist() if n.endswith("_SceneGraph.json")}
pm = json.load(open(DER / "png_manifest_test.json"))["items"]
SHOW = ["right lung", "left lung", "cardiac silhouette", "right lower lung zone", "left upper lung zone", "mediastinum", "abdomen", "trachea"]
COL = {"right lung": (255, 0, 0), "left lung": (0, 0, 255), "cardiac silhouette": (0, 200, 0), "right lower lung zone": (255, 160, 0), "left upper lung zone": (0, 200, 255), "mediastinum": (255, 0, 255), "abdomen": (160, 160, 0), "trachea": (255, 255, 255)}


def box_png(o, it):
    """original box -> PNG: scaling + clipping to [0,W]x[0,H] of the PNG."""
    s = it["scale"]; W, H = it["png_w"], it["png_h"]
    x1, y1, x2, y2 = (max(0, min(W, round(o["original_x1"] * s))), max(0, min(H, round(o["original_y1"] * s))),
                      max(0, min(W, round(o["original_x2"] * s))), max(0, min(H, round(o["original_y2"] * s))))
    full = (o["original_x2"] - o["original_x1"]) * (o["original_y2"] - o["original_y1"]) * s * s
    kept = max(0, x2 - x1) * max(0, y2 - y1)
    return (x1, y1, x2, y2), (kept / full if full > 0 else 0.0)


rng = random.Random(20260913); ids = sorted(pm); rng.shuffle(ids); ids = ids[:20]
checks = []
for d in ids:
    it = pm[d]; g = json.loads(z.read(sg[d])); ob = {o["bbox_name"]: o for o in g["objects"]}
    im = Image.open(DER / "test" / it["png"]).convert("RGB"); arr = np.asarray(im.convert("L"), float); dr = ImageDraw.Draw(im)
    W, H = im.size; assert (W, H) == (it["png_w"], it["png_h"])
    rec = {"dicom_id": d, "native_hw": [it["native_h"], it["native_w"]], "png_wh": [W, H], "scale": it["scale"], "boxes": {}}
    for name in SHOW:
        if name not in ob: continue
        (x1, y1, x2, y2), kept = box_png(ob[name], it)
        if x2 > x1 and y2 > y1:
            dr.rectangle([x1, y1, x2, y2], outline=COL[name], width=3); dr.text((x1 + 3, y1 + 3), name, fill=COL[name])
            rec["boxes"][name] = {"png_xyxy": [x1, y1, x2, y2], "kept_frac": round(kept, 3), "mean_intensity": round(float(arr[y1:y2, x1:x2].mean()), 1), "area_frac": round((x2 - x1) * (y2 - y1) / (W * H), 4)}
    b = rec["boxes"]
    rec["checks"] = {"right_lung_in_left_half": b.get("right lung", {}).get("png_xyxy", [W])[0] < W / 2 and (b["right lung"]["png_xyxy"][0] + b["right lung"]["png_xyxy"][2]) / 2 < W / 2 if "right lung" in b else None,
                     "left_lung_in_right_half": (b["left lung"]["png_xyxy"][0] + b["left lung"]["png_xyxy"][2]) / 2 > W / 2 if "left lung" in b else None,
                     "heart_center_x_frac": round((b["cardiac silhouette"]["png_xyxy"][0] + b["cardiac silhouette"]["png_xyxy"][2]) / 2 / W, 3) if "cardiac silhouette" in b else None,
                     "lungs_darker_than_heart": (b["right lung"]["mean_intensity"] + b["left lung"]["mean_intensity"]) / 2 < b["cardiac silhouette"]["mean_intensity"] if all(k in b for k in ("right lung", "left lung", "cardiac silhouette")) else None,
                     "lungs_darker_than_mediastinum": (b["right lung"]["mean_intensity"] + b["left lung"]["mean_intensity"]) / 2 < b["mediastinum"]["mean_intensity"] if all(k in b for k in ("right lung", "left lung", "mediastinum")) else None,
                     "abdomen_below_lungs": b["abdomen"]["png_xyxy"][1] >= min(b["right lung"]["png_xyxy"][1], b["left lung"]["png_xyxy"][1]) if all(k in b for k in ("abdomen", "right lung", "left lung")) else None}
    im.save(QC / f"{d}.png"); checks.append(rec)
summ = {k: sum(1 for r in checks if r["checks"].get(k) is True) for k in ("right_lung_in_left_half", "left_lung_in_right_half", "lungs_darker_than_heart", "lungs_darker_than_mediastinum", "abdomen_below_lungs")}
summ["n"] = len(checks); summ["heart_center_x_frac_range"] = [min(r["checks"]["heart_center_x_frac"] for r in checks if r["checks"]["heart_center_x_frac"] is not None), max(r["checks"]["heart_center_x_frac"] for r in checks if r["checks"]["heart_center_x_frac"] is not None)]
summ["kept_frac_min_by_box"] = {n: min(r["boxes"][n]["kept_frac"] for r in checks if n in r["boxes"]) for n in SHOW}
summ["area_frac_median_by_box"] = {n: float(np.median([r["boxes"][n]["area_frac"] for r in checks if n in r["boxes"]])) for n in SHOW}
json.dump({"summary": summ, "images": checks, "qc_dir": str(QC)}, open(V7 / "analysis/bbox_qc.json", "w"), indent=1)
print(json.dumps(summ, indent=1))
