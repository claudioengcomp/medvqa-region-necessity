"""Question-only floor (M0, no-image baseline) of the HEAL arm (plan §10.3): TF-IDF over the question text + logistic
regression, trained on the CLOSED-ENDED questions of the official VinDr training set of HEAL (yes/no answer),
evaluated on the closed-ended questions of the test set (inventory). Same three fixed decisions as the Kvasir M0: word
TF-IDF (1-2-grams), LR with C=1, no image; aggregation per class (closed_yes/closed_no), per
template (question text) and per anatomy. Output in the m0_by_type format (by_class/by_template
.evaluable), for compute_necessity --m0.

    python -m harness.isbi_placebo.heal.m0_heal --train data/isbi_placebo/heal/heal_annotations_train.parquet         --inventory results/isbi_placebo/inventory_heal_test.json --out results/isbi_placebo/m0_by_type_heal.json
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

from harness.isbi_placebo.heal.inventory_heal import normalize_answer


def _acc(rows):
    n = len(rows); c = sum(rows)
    return {"n": n, "n_correct": int(c), "accuracy": c / n if n else None}


def train_and_eval(train_parquet: str, inventory: str, seed: int = 0) -> dict:
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    tr = pd.read_parquet(train_parquet, columns=["question", "answer", "question_type", "anatomy"])
    tr = tr[tr.question_type.isin(["closed_yes", "closed_no"])]
    y_tr = [normalize_answer(a, t) for a, t in zip(tr.answer, tr.question_type)]
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, lowercase=True)
    X_tr = vec.fit_transform(tr.question)
    clf = LogisticRegression(C=1.0, max_iter=2000, random_state=seed).fit(X_tr, y_tr)
    inv = json.loads(Path(inventory).read_text())
    ev = [q for q in inv["questions"] if q["evaluable"]]
    pred = clf.predict(vec.transform([q["question"] for q in ev]))
    correct = [int(p == q["answer"]) for p, q in zip(pred, ev)]
    by_c, by_t, by_a = collections.defaultdict(list), collections.defaultdict(list), collections.defaultdict(list)
    for q, c in zip(ev, correct):
        by_c[q["question_class"]].append(c); by_t[q["question"]].append(c); by_a[q["anatomy"]].append(c)
    prior = collections.Counter(y_tr)
    return {"model": "M0_TFIDF_LR", "dataset": "HEAL", "train_rows": int(len(tr)), "train_prior": {k: v / len(tr) for k, v in prior.items()},
            "n_test": len(ev), "overall": _acc(correct),
            "by_class": {"evaluable": {k: _acc(v) for k, v in sorted(by_c.items())}, "full": {k: _acc(v) for k, v in sorted(by_c.items())}},
            "by_template": {"evaluable": {k: _acc(v) for k, v in by_t.items()}, "full": {k: _acc(v) for k, v in by_t.items()}},
            "by_anatomy": {k: _acc(v) for k, v in sorted(by_a.items())},
            "predictions": {str(q["qid"]): p for q, p in zip(ev, pred)}}


def render(out: dict) -> str:
    o = out["overall"]
    L = [f"# M0 só-pergunta do HEAL (TF-IDF + LR, treino fechado n = {out['train_rows']})", "",
         f"Acurácia global no teste fechado: {o['accuracy']:.4f} ({o['n_correct']}/{o['n']}). Prior do treino: "
         + ", ".join(f"{k} {100 * v:.1f} %" for k, v in out["train_prior"].items()) + ".", "",
         "| classe | n | M0 |", "|---|---:|---:|"]
    L += [f"| {k} | {v['n']} | {v['accuracy']:.3f} |" for k, v in out["by_class"]["evaluable"].items()]
    L += ["", "| anatomia | n | M0 |", "|---|---:|---:|"] + [f"| {k} | {v['n']} | {v['accuracy']:.3f} |" for k, v in out["by_anatomy"].items()]
    L += ["", f"Templates distintos no teste: {len(out['by_template']['evaluable'])} (o texto contém anatomia e doença; o piso é a média por classe)."]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--train", required=True); ap.add_argument("--inventory", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--out-md", default=None)
    a = ap.parse_args(argv)
    out = train_and_eval(a.train, a.inventory)
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n")
    md = render(out)
    if a.out_md:
        Path(a.out_md).write_text(md)
    print(md)


if __name__ == "__main__":
    main()
