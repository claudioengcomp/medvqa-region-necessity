"""Filters a condition arrow to a list of qids (JSON with key "qids").

Intended use: fill ablation (F-mean/F-blur) over the 300 stratified questions
(docs/isbi/placebo/fill_ablation_subset_kvasir.json). Keeps the image bytes
intact; only removes rows with no listed qid and, in the kept rows, the
unlisted questions. Writes the sha256 of the generated file.

    python -m harness.isbi_placebo.subset_arrow --arrow data/isbi_placebo/vqa_kvasir_placebo_T_mean.arrow         --qids docs/isbi/placebo/fill_ablation_subset_kvasir.json --output data/isbi_placebo/vqa_kvasir_placebo_T_mean_fill300.arrow
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

from harness.interventions.arrow_io import read_arrow, write_arrow


def subset_arrow(arrow: str, qids_json: str, output: str) -> dict:
    keep = set(json.loads(Path(qids_json).read_text())["qids"])
    df = read_arrow(arrow)
    rows, found = [], set()
    for row in df.itertuples(index=False):
        idx = [i for i, q in enumerate(row.question_id) if q in keep]
        if not idx:
            continue
        found.update(row.question_id[i] for i in idx)
        rows.append({"image": row.image, "questions": [row.questions[i] for i in idx], "answers": [row.answers[i] for i in idx],
                     "answer_labels": [row.answer_labels[i] for i in idx], "answer_scores": [row.answer_scores[i] for i in idx],
                     "image_id": row.image_id, "question_id": [row.question_id[i] for i in idx],
                     "answer_type": [row.answer_type[i] for i in idx], "split": row.split})
    write_arrow(pd.DataFrame(rows), output)
    sha = hashlib.sha256(Path(output).read_bytes()).hexdigest()
    return {"source": arrow, "qids_json": qids_json, "output": output, "n_rows": len(rows), "n_questions": len(found),
            "qids_missing": sorted(keep - found), "sha256": sha}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arrow", required=True); ap.add_argument("--qids", required=True); ap.add_argument("--output", required=True)
    a = ap.parse_args(argv)
    print(json.dumps(subset_arrow(a.arrow, a.qids, a.output), indent=1))


if __name__ == "__main__":
    main()
