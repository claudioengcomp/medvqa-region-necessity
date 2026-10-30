"""Question-only M0 for the ALIGNED HEAL (2026-10-10, authors' request): same classifier as harness/isbi_placebo/heal/m0_heal.py
(TF-IDF 1-2-grams, min_df 1, lowercase; LogisticRegression C=1, max_iter 2000, random_state 0) and the same training set
(the 7 641 closed-ended yes/no questions of the HEAL VinDr training split). The parquet heal_annotations_train.parquet is no longer on disk
nor on the Drive; the same 7 641 rows (question, normalized answer) are read from the train + validation arrows
(vqa_heal_train.arrow + vqa_heal_val.arrow = split D2 of the same annotations; count and prior checked against the published
m0_by_type_heal.json: 7 641 rows, prior no 0.5112 / yes 0.4888). Predicts exactly the 1 446 evaluable qids of the
current inventory; output in the format of the _C0.json files + aggregates + provenance."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import collections, hashlib, json, platform, time
from harness.interventions.arrow_io import read_arrow
from harness.results_schema import validate_results_dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import sklearn
P = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-placebo"; ARR = [f"{P}/data/finetune_arrows/vqa_heal_train.arrow", f"{P}/data/finetune_arrows/vqa_heal_val.arrow"]
INV = f"{P}/results/isbi_placebo/inventory_heal_test.json"; PUB = f"{P}/results/isbi_placebo/m0_by_type_heal.json"; OUT = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/results/M0_question_only_HEAL_aligned.json"
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""): h.update(b)
    return h.hexdigest()
qs, ys = [], []
for a in ARR:
    df = read_arrow(a)
    for _, r in df.iterrows():
        for q, ans in zip(r["questions"], r["answers"]):
            g = str(list(ans)[0]).strip().lower()
            if g in ("yes", "no"): qs.append(q); ys.append(g)
pub = json.load(open(PUB)); prior = collections.Counter(ys); assert len(qs) == pub["train_rows"], (len(qs), pub["train_rows"])
vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, lowercase=True); X = vec.fit_transform(qs); clf = LogisticRegression(C=1.0, max_iter=2000, random_state=0).fit(X, ys)
inv = json.load(open(INV)); ev = [q for q in inv["questions"] if q["evaluable"]]; pred = clf.predict(vec.transform([q["question"] for q in ev]))
preds = [{"qid": int(q["qid"]), "predicted": str(p), "gold": q["answer"], "correct": bool(p == q["answer"])} for q, p in zip(ev, pred)]
byc = collections.defaultdict(list); bya = collections.defaultdict(list)
for q, p in zip(ev, preds): byc[q["question_class"]].append(p["correct"]); bya[q["anatomy"]].append(p["correct"])
agg = lambda v: {"n": len(v), "n_correct": int(sum(v)), "accuracy": sum(v) / len(v)}
rec = {"model": "M0_question_only", "dataset": "HEAL", "condition": "C0", "accuracy": sum(p["correct"] for p in preds) / len(preds), "n": len(preds), "n_correct": sum(p["correct"] for p in preds), "predictions": preds,
       "aggregates": {"train_rows": len(qs), "train_prior": {k: v / len(qs) for k, v in prior.items()}, "by_class": {k: agg(v) for k, v in sorted(byc.items())}, "by_anatomy": {k: agg(v) for k, v in sorted(bya.items())}, "published_1512": {"train_rows": pub["train_rows"], "train_prior": pub["train_prior"], "by_class": pub["by_class"]["evaluable"]}},
       "provenance": {"recipe": "igual a harness.isbi_placebo.heal.m0_heal.train_and_eval (TF-IDF 1-2-gramas + LogisticRegression C=1, random_state 0)", "train_source": ARR, "train_source_sha256": [sha(a) for a in ARR], "train_rows": len(qs), "note": "parquet heal_annotations_train.parquet ausente do disco e do Drive; as mesmas 7641 fechadas lidas dos arrows train+val (split D2 das mesmas anotacoes); predicao nos 1446 qids avaliaveis do inventario atual",
                      "inventory": INV, "inventory_sha256": sha(INV), "sklearn": sklearn.__version__, "python": platform.python_version(), "host": platform.node(), "stamped": time.strftime("%Y-%m-%d %H:%M:%S")}}
validate_results_dict(rec); json.dump(rec, open(OUT, "w"), indent=1)
print("train rows", len(qs), "prior", rec["aggregates"]["train_prior"], "| n", rec["n"], "acc %.4f" % rec["accuracy"], {k: round(v["accuracy"], 4) for k, v in rec["aggregates"]["by_class"].items()}, "| publicado 1512:", {k: round(v["accuracy"], 4) for k, v in pub["by_class"]["evaluable"].items()})
