"""Extracts the domain field (procedure) of Kvasir from the already built
evaluation arrow -- analogous to SLAKE's `location`, but Kvasir does not
have this field ready in the raw data. Finding of 26/08/2026: the question
"What type of procedure is the image taken from?" answers
colonoscopy/gastroscopy for 1,756/4,058 images of the test split (43%) --
cross-validated against the existing pathology_label (polyp/ulcerative
colitis should be colonoscopy; oesophagitis/barretts should be
gastroscopy): of 682 images with both signals, only 2 inconsistent
(99.7% agreement).

Used by C6 (harness/interventions/make_c6_organ_modality_swap.py) as
`--bucket-membership`, one bucket per procedure -- same role that
build_slake_pathology_labels.build_slake_bucket_membership plays for SLAKE.

Usage:
    python -m harness.prepro.build_kvasir_domain_membership         --input data/finetune_arrows/vqa_kvasir_test.arrow         --output-colonoscopy results/kvasir_bucket_colonoscopy.json         --output-gastroscopy results/kvasir_bucket_gastroscopy.json
"""
from __future__ import annotations

import argparse
import json

_PROCEDURE_QUESTION = "what type of procedure is the image taken from?"


def _first_answer(answer) -> str:
    """Normalizes an answer value (may come as a string, list, or
    numpy array from pandas/arrow) to its first item, as a string."""
    if hasattr(answer, "__len__") and not isinstance(answer, str):
        answer = answer[0]
    return str(answer).strip().lower()


def extract_domain_membership(rows: list[dict]) -> dict[str, str]:
    """rows: list of {"image_id":..., "questions": [...], "answers": [...]}
    (one row per image, in the evaluation arrow format). Returns
    {image_id: procedure} only for the images that actually have this
    question answered -- most do not (56.7% of the test split,
    see the module docstring)."""
    membership: dict[str, str] = {}
    for row in rows:
        for q, a in zip(row["questions"], row["answers"]):
            if q.strip().lower() == _PROCEDURE_QUESTION:
                membership[row["image_id"]] = _first_answer(a)
                break
    return membership


def split_by_procedure(membership: dict[str, str]) -> tuple[list[str], list[str]]:
    """Splits {image_id: procedure} into two lists (colonoscopy,
    gastroscopy) -- values outside this pair (not observed in
    practice, see the module's finding) are ignored, not raised as errors."""
    colonoscopy = [img for img, proc in membership.items() if proc == "colonoscopy"]
    gastroscopy = [img for img, proc in membership.items() if proc == "gastroscopy"]
    return colonoscopy, gastroscopy


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-colonoscopy", required=True)
    parser.add_argument("--output-gastroscopy", required=True)
    return parser.parse_args()


if __name__ == "__main__":
    from harness.interventions.arrow_io import read_arrow

    args = _parse_args()
    df = read_arrow(args.input)
    rows = [{"image_id": r["image_id"], "questions": r["questions"], "answers": r["answers"]}
            for _, r in df.iterrows()]

    membership = extract_domain_membership(rows)
    colonoscopy, gastroscopy = split_by_procedure(membership)

    with open(args.output_colonoscopy, "w", encoding="utf-8") as fp:
        json.dump(colonoscopy, fp, indent=2, ensure_ascii=False)
    with open(args.output_gastroscopy, "w", encoding="utf-8") as fp:
        json.dump(gastroscopy, fp, indent=2, ensure_ascii=False)

    print(f"{len(colonoscopy)} imagens colonoscopy -> {args.output_colonoscopy}")
    print(f"{len(gastroscopy)} imagens gastroscopy -> {args.output_gastroscopy}")
    print(f"{len(membership)} imagens com procedimento identificado, de {len(rows)} no arrow "
          f"({100 * len(membership) / len(rows):.1f}%)")
