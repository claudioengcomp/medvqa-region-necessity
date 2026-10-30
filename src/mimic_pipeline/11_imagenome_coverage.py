"""v7_mimic/scripts/11_imagenome_coverage.py -- 2026-10-11 -- coverage of the subset's dicom_ids in scene_graph.zip (silver)
and in the gold; sample of one scene graph; likely reasons for the missing ones (ViewPosition, ImaGenome split, report)."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json, zipfile, collections, time, socket
from pathlib import Path
import pandas as pd
RAW = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/raw/chest-imagenome/1.0.0"); V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic")
z = zipfile.ZipFile(RAW / "silver_dataset/scene_graph.zip")
names = z.namelist()
sg = {Path(n).name.replace("_SceneGraph.json", ""): n for n in names if n.endswith("_SceneGraph.json")}
out = {"zip_entries": len(names), "scene_graphs": len(sg), "name_example": names[1] if len(names) > 1 else names[0],
       "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "host": socket.gethostname()}
splits = pd.concat([pd.read_csv(RAW / f"silver_dataset/splits/{s}.csv").assign(ig_split=s) for s in ("train", "valid", "test")])
ig_split = dict(zip(splits.dicom_id, splits.ig_split))
gold_img = set(x.replace(".dcm", "") for x in pd.read_csv(RAW / "gold_dataset/gold_bbox_coordinate_annotations_1000images.csv").image_id.unique())
gold_attr = pd.read_csv(RAW / "gold_dataset/gold_object_attribute_with_coordinates.txt", sep="\t")
gold_attr_img = set(x.replace(".dcm", "") for x in gold_attr.image_id.unique())
out["gold_bbox_images"] = len(gold_img); out["gold_attr_images"] = len(gold_attr_img)
cov = {}
for s in ("test", "val", "train"):
    it = pd.read_parquet(V7 / f"data/items_{s}.parquet", columns=["dicom_id", "ViewPosition", "study_id", "subject_id"]).drop_duplicates("dicom_id")
    have = it.dicom_id.isin(sg)
    miss = it[~have]
    cov[s] = {"n_images": len(it), "with_scene_graph": int(have.sum()), "frac": float(have.mean()),
              "missing": [{"dicom_id": r.dicom_id, "ViewPosition": r.ViewPosition, "imagenome_split": ig_split.get(r.dicom_id, "not in splits")} for r in miss.itertuples()][:200],
              "missing_reason_counts": dict(collections.Counter(("in_imagenome_splits:" + ig_split[d]) if d in ig_split else "not_in_imagenome_splits" for d in miss.dicom_id)),
              "in_gold_bbox": int(it.dicom_id.isin(gold_img).sum()), "in_gold_attr": int(it.dicom_id.isin(gold_attr_img).sum()),
              "imagenome_split_of_ours": dict(collections.Counter(ig_split.get(d, "none") for d in it.dicom_id))}
out["coverage"] = cov
# sample: first test dicom with a scene graph
it = pd.read_parquet(V7 / "data/items_test.parquet", columns=["dicom_id"]).drop_duplicates()
d0 = next(d for d in it.dicom_id if d in sg)
g = json.loads(z.read(sg[d0]))
out["sample"] = {"dicom_id": d0, "top_keys": list(g.keys()), "n_objects": len(g["objects"]), "n_attributes": len(g["attributes"]), "n_relationships": len(g["relationships"]),
                 "object_example": g["objects"][0], "bbox_names": sorted(o["bbox_name"] for o in g["objects"]),
                 "attribute_example": {k: v for k, v in g["attributes"][0].items() if k not in ("phrases",)} if g["attributes"] else None,
                 "attributes_bbox_names": sorted(a["bbox_name"] for a in g["attributes"])}
# dicom -> original dimension relation: compares max original_x2 with Rows/Columns from the MIMIC metadata
meta = pd.read_csv(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/raw/mimic-cxr-jpg/2.1.0/mimic-cxr-2.0.0-metadata.csv.gz", usecols=["dicom_id", "Rows", "Columns"]).set_index("dicom_id")
out["sample"]["mimic_rows_cols"] = [int(meta.loc[d0, "Rows"]), int(meta.loc[d0, "Columns"])]
out["sample"]["max_original_xy"] = [max(o["original_x2"] for o in g["objects"]), max(o["original_y2"] for o in g["objects"])]
# attribute vocabulary in the scene graphs of our test+val (counts of (category|context|label) and bbox_names)
attr_counter = collections.Counter(); bbox_counter = collections.Counter(); n_read = 0
for s in ("test", "val"):
    for d in pd.read_parquet(V7 / f"data/items_{s}.parquet", columns=["dicom_id"]).dicom_id.unique():
        if d not in sg: continue
        g = json.loads(z.read(sg[d])); n_read += 1
        for o in g["objects"]: bbox_counter[o["bbox_name"]] += 1
        for a in g["attributes"]:
            for lst in a["attributes"]:
                for x in lst: attr_counter[x] += 1
out["testval_scene_graphs_read"] = n_read
out["bbox_name_counts_testval"] = dict(bbox_counter.most_common())
out["attribute_counts_testval"] = dict(attr_counter.most_common())
json.dump(out, open(V7 / "analysis/imagenome_coverage.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: out[k] for k in ("zip_entries", "scene_graphs", "name_example", "gold_bbox_images", "gold_attr_images")}))
for s in cov: print(s, {k: v for k, v in cov[s].items() if k != "missing"})
print("sample:", json.dumps({k: v for k, v in out["sample"].items() if k not in ("object_example", "attribute_example")}, ensure_ascii=False)[:1500])
print("object_example:", json.dumps(out["sample"]["object_example"]))
print("attribute_example:", json.dumps(out["sample"]["attribute_example"], ensure_ascii=False)[:1200])
print("bbox_names (n distinct):", len(bbox_counter)); print("attributes (n distinct):", len(attr_counter))
