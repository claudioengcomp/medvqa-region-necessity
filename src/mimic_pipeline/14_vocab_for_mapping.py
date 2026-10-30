"""inputs for the mapping: ImaGenome attributes (test+val), Diff-VQA entities and <loc>, cross-check against the gold."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json, re, collections
from pathlib import Path
import pandas as pd
RAW = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/raw/chest-imagenome/1.0.0"); V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic")
cov = json.load(open(V7 / "analysis/imagenome_coverage.json"))
print("=== atributos do ImaGenome nos scene graphs de test+val (categoria|contexto|label : n)")
ac = cov["attribute_counts_testval"]
labels = collections.defaultdict(lambda: collections.Counter())
for k, v in ac.items():
    cat, ctx, lab = k.split("|"); labels[(cat, lab)][ctx] += v
for (cat, lab), c in sorted(labels.items(), key=lambda kv: -sum(kv[1].values())):
    print(f"{cat:20s} {lab:45s} yes={c.get('yes',0):6d} no={c.get('no',0):6d}")
print("\n=== entidades do Diff-VQA (entities.json)")
ent = json.load(open(V7 / "analysis/entities.json"))["entities"]
for e, n in ent.items(): print(f"{n:7d}  {e!r}")
print("\n=== <loc> nos templates de presence com localizacao (itens test+val+train)")
pool = pd.read_parquet(V7 / "data/pool_single_image_all_splits.parquet", columns=["question", "template_id", "template", "split", "answer"])
locq = pool[pool.template.str.contains("<loc>")]
loc = locq.question.str.extract(r" in the (.+?)(?: area)?\?$")[0]
print(loc.value_counts().head(60).to_string())
print("distinct locs:", loc.nunique(), "rows:", len(locq))
items = pd.concat([pd.read_parquet(V7 / f"data/items_{s}.parquet", columns=["question", "template_id", "split", "answer"]) for s in ("test", "val", "train")])
li = items[items.template_id.isin(["T02", "T03"])]
print("\n<loc> no subconjunto (test):"); print(li[li.split == "test"].question.str.extract(r" in the (.+?)(?: area)?\?$")[0].value_counts().to_string())
print("\n=== gold x Diff-VQA")
gold_attr = pd.read_csv(RAW / "gold_dataset/gold_object_attribute_with_coordinates.txt", sep="\t")
gold_attr["dicom_id"] = gold_attr.image_id.str.replace(".dcm", "", regex=False)
poolall = pd.read_parquet(V7 / "data/pool_single_image_all_splits.parquet", columns=["dicom_id", "split", "question_type", "template_id", "answer"])
q = pd.read_csv(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/raw/medical-diff-vqa/1.0.1/mimic_pair_questions.csv", usecols=["study_id", "question_type", "question", "answer"])
m = pd.read_csv(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/raw/medical-diff-vqa/1.0.1/mimic_all.csv", usecols=["study_id", "dicom_id"])
gd = set(gold_attr.dicom_id)
print("gold attr images:", len(gd), "| em mimic_all (dicom):", len(gd & set(m.dicom_id)), "| no nosso pool elegivel:", len(gd & set(poolall.dicom_id)), "| no teste:", len(gd & set(poolall[poolall.split=='test'].dicom_id)))
qm = q.merge(m, on="study_id"); qg = qm[qm.dicom_id.isin(gd) & (qm.question_type == "presence")]
print("perguntas presence do Diff-VQA em imagens gold:", len(qg), "| imagens:", qg.dicom_id.nunique())
print("gold: colunas", list(gold_attr.columns)); print("gold relation values:", gold_attr.relation.value_counts().to_dict(), "| context:", gold_attr.context.value_counts().to_dict())
print("gold label_name top:", gold_attr.label_name.value_counts().head(40).to_dict())
print("gold bbox names:", sorted(gold_attr.bbox.unique()))
