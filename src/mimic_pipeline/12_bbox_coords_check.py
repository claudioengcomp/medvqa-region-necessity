"""v7_mimic/scripts/12_bbox_coords_check.py -- coordinate system of the ImaGenome 'original_*' boxes vs native dimensions
of the MIMIC-CXR-JPG JPG (png_manifest_*.json: native_h, native_w, scale)."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json, zipfile, collections
from pathlib import Path
import pandas as pd, numpy as np
RAW = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/raw/chest-imagenome/1.0.0"); V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic")
DER = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/derived/mimic_png")
z = zipfile.ZipFile(RAW / "silver_dataset/scene_graph.zip"); sg = {Path(n).name.replace("_SceneGraph.json", ""): n for n in z.namelist() if n.endswith("_SceneGraph.json")}
meta = pd.read_csv(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/raw/mimic-cxr-jpg/2.1.0/mimic-cxr-2.0.0-metadata.csv.gz", usecols=["dicom_id", "Rows", "Columns"]).set_index("dicom_id")
res = collections.Counter(); rows = []
for s in ("test", "val"):
    pm = json.load(open(DER / f"png_manifest_{s}.json"))["items"]
    for d, it in pm.items():
        g = json.loads(z.read(sg[d])); H, W = it["native_h"], it["native_w"]
        mx = max(o["original_x2"] for o in g["objects"]); my = max(o["original_y2"] for o in g["objects"])
        mnx = min(o["original_x1"] for o in g["objects"]); mny = min(o["original_y1"] for o in g["objects"])
        res["n"] += 1
        res["meta_rows_eq_native_h"] += int(meta.loc[d, "Rows"] == H); res["meta_cols_eq_native_w"] += int(meta.loc[d, "Columns"] == W)
        res["x2_within_W"] += int(mx <= W); res["y2_within_H"] += int(my <= H)
        res["x2_within_H_(swapped)"] += int(mx <= H); res["y2_within_W_(swapped)"] += int(my <= W)
        res["neg_coords"] += int(mnx < 0 or mny < 0)
        # image side: the patient's right lung must be in the LEFT half of the image (smaller x)
        ob = {o["bbox_name"]: o for o in g["objects"]}
        if "right lung" in ob and "left lung" in ob:
            res["right_lung_left_of_left_lung"] += int(ob["right lung"]["original_x1"] < ob["left lung"]["original_x1"]); res["both_lungs"] += 1
        rows.append({"dicom_id": d, "split": s, "H": H, "W": W, "max_x2": mx, "max_y2": my, "rows_meta": int(meta.loc[d, "Rows"]), "cols_meta": int(meta.loc[d, "Columns"]),
                     "frac_x": mx / W, "frac_y": my / H})
df = pd.DataFrame(rows); df.to_csv(V7 / "analysis/bbox_coords_check.csv", index=False)
print(dict(res))
print("frac_x (max_x2/W) quantis:", df.frac_x.quantile([0, .01, .5, .99, 1]).round(3).to_dict())
print("frac_y (max_y2/H) quantis:", df.frac_y.quantile([0, .01, .5, .99, 1]).round(3).to_dict())
print("exemplos fora de W/H:", df[(df.max_x2 > df.W) | (df.max_y2 > df.H)].head(8).to_dict("records"))
