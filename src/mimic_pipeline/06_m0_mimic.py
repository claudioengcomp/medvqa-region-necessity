"""v7_mimic/scripts/06_m0_mimic.py -- 2026-10-10 -- gpu-server-a (CPU only)

Question-only (no-image) baseline M0 for the single-image MIMIC/Diff-VQA, as in harness/isbi_placebo/heal/m0_heal.py (placebo
repo @2b7e731): word TF-IDF (1-2-grams, min_df=1, lowercase) + LogisticRegression(C=1, max_iter=2000),
no image, trained on the CLOSED-ENDED (yes/no) questions and evaluated on all test questions (closed-ended by the
prediction; for the open-ended ones the yes/no prediction never matches, and the baseline is also reported as the majority answer
per template in the train split, "prior"). Aggregation by type, by template_id and by answer_type; 95% CI by bootstrap
PER IMAGE (dicom_id), 2,000 replicates, seed 20260913.

  python 06_m0_mimic.py --train <parquet with question,answer,template_id,question_type,answer_type>       --test data/items_test.parquet --tag subset --out results/M0_question_only_MIMIC_subset.json
"""
from __future__ import annotations
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import argparse, collections, json, socket, time
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 20260913
B = 2000


def _acc(c):
    n = len(c); k = int(sum(c))
    return {"n": n, "n_correct": k, "accuracy": k / n if n else None}


def boot_ci(correct: np.ndarray, groups: np.ndarray, b=B, seed=SEED):
    """95% CI by image bootstrap (groups): resamples images with replacement, sums hits/items."""
    uniq, inv = np.unique(groups, return_inverse=True)
    n_img = len(uniq)
    sum_c = np.bincount(inv, weights=correct, minlength=n_img)
    cnt = np.bincount(inv, minlength=n_img).astype(float)
    rng = np.random.default_rng(seed)
    accs = np.empty(b)
    for i in range(b):
        idx = rng.integers(0, n_img, n_img)
        accs[i] = sum_c[idx].sum() / cnt[idx].sum()
    return {"ci95_low": float(np.percentile(accs, 2.5)), "ci95_high": float(np.percentile(accs, 97.5)), "n_images": int(n_img), "B": b, "seed": seed}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", required=True); ap.add_argument("--test", required=True)
    ap.add_argument("--tag", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    tr = pd.read_parquet(a.train); te = pd.read_parquet(a.test)
    trc = tr[tr.answer_type == "closed"]
    assert set(trc.answer) <= {"yes", "no"}, set(trc.answer)
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, lowercase=True)
    X = vec.fit_transform(trc.question)
    clf = LogisticRegression(C=1.0, max_iter=2000, random_state=0).fit(X, trc.answer)
    pred = clf.predict(vec.transform(te.question))
    correct = (pred == te.answer.values).astype(int)
    # prior: majority answer per template in the TRAIN split (all questions, closed-ended and open-ended)
    maj = tr.groupby("template_id").answer.agg(lambda s: s.value_counts().idxmax()).to_dict()
    glob = tr.answer.value_counts().idxmax()
    prior_pred = np.array([maj.get(t, glob) for t in te.template_id])
    prior_correct = (prior_pred == te.answer.values).astype(int)
    groups = te.dicom_id.values
    def agg(mask_col):
        out = {}
        for k, g in te.groupby(mask_col, sort=True):
            idx = g.index.values
            c = correct[te.index.get_indexer(idx)]; pc = prior_correct[te.index.get_indexer(idx)]
            out[str(k)] = {"m0": {**_acc(c), **boot_ci(c, groups[te.index.get_indexer(idx)])},
                           "prior_majority": {**_acc(pc), **boot_ci(pc, groups[te.index.get_indexer(idx)])},
                           "n_images": int(g.dicom_id.nunique())}
        return out
    closed = te.answer_type.values == "closed"
    res = {"model": "M0_TFIDF_LR", "dataset": f"MIMIC-Diff-VQA single-image ({a.tag})", "train_file": a.train, "test_file": a.test,
           "train_rows_closed": int(len(trc)), "train_prior_closed": {k: float(v) for k, v in (trc.answer.value_counts() / len(trc)).items()},
           "n_test": int(len(te)), "n_test_images": int(te.dicom_id.nunique()),
           "overall_closed": {**_acc(correct[closed]), **boot_ci(correct[closed], groups[closed])},
           "overall_all_m0": {**_acc(correct), **boot_ci(correct, groups)},
           "overall_all_prior": {**_acc(prior_correct), **boot_ci(prior_correct, groups)},
           "by_answer_type": agg("answer_type"), "by_question_type": agg("question_type"), "by_template": agg("template_id"),
           "template_text": tr.drop_duplicates("template_id").set_index("template_id").template.to_dict() if "template" in tr.columns else {},
           "predictions": {str(q): p for q, p in zip(te.qid, pred)}, "prior_predictions": {str(q): p for q, p in zip(te.qid, prior_pred)},
           "provenance": {"script": "v7_mimic/scripts/06_m0_mimic.py", "like": "harness/isbi_placebo/heal/m0_heal.py @2b7e731", "seed_bootstrap": SEED, "B": B,
                          "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "host": socket.gethostname()}}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({k: res[k] for k in ("train_rows_closed", "train_prior_closed", "n_test", "overall_closed", "overall_all_m0", "overall_all_prior")}, indent=1))


if __name__ == "__main__":
    main()
