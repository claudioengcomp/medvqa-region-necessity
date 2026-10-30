"""Build the side .json of SLAKE pathology labels, in the same format used
for Kvasir (harness/prepro/prepare_kvasir_arrow.py) — {image_id: label}, so
that the restricted swap script (make_c5_matched_pathology_swap.py) can
consume it without knowing which dataset it came from.

Unlike Kvasir, SLAKE already ships `content_type` in the raw JSON (nothing
needs to be decomposed) — it only has to be filtered and aggregated.

Default bucket: X-Ray + Lung. The number that matters in practice is not
the dataset total (130 images across train+test+validate) — it is how many
remain **restricted to the test split**, since C5 can only swap images
that are actually in the evaluated set. Restricted to test.json and to
English-only questions: 20 images. Other buckets are available via
--modality/--location, with the caveat that CT+Abdomen and MRI+Brain* have
a smaller and more imbalanced N.

**SLAKE is not an EN/ZH parallel corpus for content_type=='Abnormality'.**
Inspecting `test.json` directly: 61 test-split images have their pathology
question ONLY in Chinese, with no English equivalent. Since the label is
used purely internally (C5 pairing eligibility — it is never shown to the
model, which still sees only the English questions already present in the
arrow), it is safe to translate that vocabulary and include those images.
The vocabulary was confirmed to be small and closed (29 unique Chinese
answers across the whole test.json) — translated by hand below
(`_ZH_TO_EN`), in the same spirit as the pre-existing `_TYPO_FIXES` on the
English side. Measured effect: X-Ray/Lung goes from 20 to 47 eligible
images (2.35x) when restricted to test; MRI/Brain_Tissue becomes a viable
second bucket (9 -> 22). The exclusion of trivial/non-pathological answers
covers both languages, so `q_lang` is not used as a filter.

image_id in the arrow follows the pattern
"data/finetune_data/slack//imgs/<img_name>" (note the double slash — it is
not a typo introduced here). Confirmed two ways at run time: (1) by
reading the `image_id` column of the real arrow; (2) by reading the source
of `prepro_vqa_slack()` in the `zhjohnchan/M3AE` repository (pinned commit
`14da377255280eed547e451f368cf71a43f3ca1c`,
`prepro/prepro_finetuning_data.py`):
`data_root = "data/finetune_data/slack/"`, `image_root = f"{data_root}/imgs"`
(this is where the double slash comes from — data_root already ends in
"/"), and `img_path = os.path.join(image_root, sample["img_name"])`. Since
that literal is fixed in M3AE's own code, it is stable across runs and
does not need to be reconfirmed.

Usage:
    python -m harness.prepro.build_slake_pathology_labels \
        --slake-dir ~/Downloads/Slake1.0 \
        --modality X-Ray --location Lung \
        --output data/finetune_arrows/vqa_slack_test_pathology_labels.json
"""
from __future__ import annotations

import argparse
import json

_TRIVIAL_ANSWERS = {"yes", "no", "none"}

# The real image_id prefix in the SLAKE arrow — see the module docstring
# for the full confirmation (real arrow + prepro_vqa_slack() source).
SLAKE_IMAGE_ID_PREFIX = "data/finetune_data/slack//imgs/"

# Found by running against the real SLAKE data: typos confirmed to be
# present in the original dataset.
_TYPO_FIXES = {
    "noudle": "nodule",
    "cardiomegal": "cardiomegaly",
    "cardiomega": "cardiomegaly",
}

# From the same survey: these answers show up on content_type=='Abnormality'
# questions but are organ names or ambiguous answers rather than
# pathologies — "lung" on its own appeared in 33 of the 130 images in the
# X-Ray/Lung bucket, and is clearly not a specific finding.
_NON_PATHOLOGY_ANSWERS = {"lung", "heart", "both"}

# Chinese equivalents of _TRIVIAL_ANSWERS/_NON_PATHOLOGY_ANSWERS above —
# same exclusion semantics. Confirmed by fully enumerating the
# Chinese-only answers across ALL THREE splits (train+test+validate, which
# is what the script actually processes, see __main__ below).
_ZH_TRIVIAL_ANSWERS = {
    "是", "否", "有", "没有", "可以", "不可以", "是的", "不是", "健康", "不正常", "存在", "无",
    "不包含", "不存在", "无异常", "正常", "都是",
}
_ZH_NON_PATHOLOGY_ANSWERS = {"肺", "心脏", "肝脏", "肺脏"}

# A small, closed vocabulary (complete enumeration over the 3 splits) —
# each entry translates to the SAME canonical category name already used
# on the English side, so that pairing stays consistent across the two
# languages. Entries containing a comma are composite answers from the
# original SLAKE data (the same question admits more than one finding) —
# the order written here does not matter, since normalize_answer()
# canonicalizes by alphabetical sorting before returning (see
# _canonicalize_compound_order below).
_ZH_TO_EN = {
    "心脏肥大": "cardiomegaly",
    "气胸": "pneumothorax",
    "肺不张": "atelectasis",
    "肺炎": "pneumonia",
    "肺结节": "nodule",
    "肺肿块": "mass",
    "胸腔积液": "effusion",
    "积液": "effusion",
    "肺浸润": "pulmonary infiltration",
    "肝癌": "liver cancer",
    "肾癌": "kidney cancer",
    "肺癌": "lung cancer",
    "脑积水": "hydrocephalus",
    "脑水肿": "brain edema",
    # The wording "brain enhancing/non-enhancing tumor" (rather than
    # "enhancing brain tumor") was chosen to match SLAKE's own native
    # English phrasing for the same bucket (MRI/Brain_Tissue) -- confirmed
    # by inspecting the dataset's real EN answers. The order of terms in
    # composite answers does not matter here -- see the sort-based
    # canonicalization in normalize_answer() below, which covers both
    # languages (SLAKE's English side itself contains the same answer in
    # more than one order, e.g. "Brain Edema, Brain Enhancing Tumor" and
    # "Brain Enhancing Tumor, Brain Edema, Brain Non-enhancing Tumor").
    "脑水肿,增强型脑肿瘤": "brain edema, brain enhancing tumor",
    "脑水肿,增强型脑肿瘤,非增强型脑肿瘤": "brain edema, brain enhancing tumor, brain non-enhancing tumor",
    "脑水肿,非增强型脑肿瘤": "brain edema, brain non-enhancing tumor",
    "脑肿瘤,脑水肿": "brain tumor, brain edema",
    "脑水肿,脑肿瘤": "brain edema, brain tumor",
    "脑水肿,脑瘤": "brain edema, brain tumor",
    "脑瘤,脑水肿": "brain tumor, brain edema",
    "脑积水,脑瘤": "hydrocephalus, brain tumor",
    "增强型脑瘤,脑水肿,非增强型脑瘤": "brain enhancing tumor, brain edema, brain non-enhancing tumor",
    "增强型脑肿瘤,非增强型脑肿瘤,脑水肿": "brain enhancing tumor, brain non-enhancing tumor, brain edema",
    "心脏肥大,气胸": "cardiomegaly, pneumothorax",
    "心脏肥大,肺浸润,积液": "cardiomegaly, pulmonary infiltration, effusion",
    "肝癌,肾癌": "liver cancer, kidney cancer",
    "肺不张,积液": "atelectasis, effusion",
    "肺不张,肺肿块": "atelectasis, mass",
    "肺肿块,肺不张": "mass, atelectasis",
    "肺结节,气胸": "nodule, pneumothorax",
}


def normalize_answer(answer: str) -> str | None:
    """Normalize a SLAKE pathology answer: fix known typos, translate the
    small Chinese-only vocabulary (see _ZH_TO_EN above), and return None if
    the answer is not a real pathology (a bare organ name, an ambiguous
    answer, or a trivial answer in either language) — a signal to drop the
    row, not a valid category."""
    normalized = answer.strip().lower()
    # Comma spacing is inconsistent in the original SLAKE composite answers
    # ("心脏肥大, 气胸" and "心脏肥大,气胸" both occur) -- normalize to ","
    # with no space before matching against _ZH_TO_EN, otherwise the two
    # would accidentally become different dictionary entries. This does not
    # affect English (it never matches any dict here, and _TYPO_FIXES
    # contains no comma).
    normalized = normalized.replace(", ", ",")
    # Chinese check first -- .lower() is a no-op for these characters, so
    # the comparison works the same over the text normalized above.
    if normalized in _ZH_TRIVIAL_ANSWERS or normalized in _ZH_NON_PATHOLOGY_ANSWERS:
        return None
    if normalized in _ZH_TO_EN:
        return _canonicalize_compound_order(_ZH_TO_EN[normalized])
    if normalized in _NON_PATHOLOGY_ANSWERS:
        return None
    return _canonicalize_compound_order(_TYPO_FIXES.get(normalized, normalized))


def _canonicalize_compound_order(label: str) -> str:
    """Composite answers (more than one finding in the same answer, e.g.
    'Brain Edema, Brain Enhancing Tumor') appear in more than one order in
    the original SLAKE data -- confirmed in both languages, so it is not an
    artifact of the Chinese translation above (the English side itself has
    'Brain Edema, Brain Enhancing Tumor, Brain Non-enhancing Tumor' AND
    'Brain Enhancing Tumor, Brain Edema, Brain Non-enhancing Tumor' for
    different images). Without canonicalization the same clinical category
    fragments into distinct categories by accident of ordering -- so the
    terms are sorted (after splitting on commas) to collapse them into a
    single key. A single-term answer passes through untouched (nothing to
    sort)."""
    parts = [p.strip() for p in label.split(",")]
    if len(parts) <= 1:
        return label
    return ", ".join(sorted(parts))


def canonical_label_per_image(records: list[dict]) -> dict[str, str]:
    """records: list of already filtered questions (content_type=='Abnormality',
    modality/location already restricted, trivial/non-pathological answers
    already excluded and normalized). Groups by img_name and picks the
    alphabetically smallest answer when there is more than one
    (deterministic and documented as such — it is not a clinical judgement
    about which one is 'the' correct answer)."""
    by_img: dict[str, list[str]] = {}
    for r in records:
        by_img.setdefault(r["img_name"], []).append(r["answer"])
    return {img: sorted(answers)[0] for img, answers in by_img.items()}


def build_slake_labels(records: list[dict], modality: str, location: str) -> dict[str, str]:
    filtered = []
    for r in records:
        # q_lang is not used as a filter -- SLAKE is not EN/ZH
        # parallel for content_type=='Abnormality' (see the module
        # docstring); normalize_answer() already knows how to exclude or
        # translate Chinese answers.
        if not (r.get("content_type") == "Abnormality"
                and r.get("modality") == modality
                and r.get("location") == location):
            continue
        answer = r["answer"].strip().lower()
        if answer in _TRIVIAL_ANSWERS:
            continue
        normalized = normalize_answer(answer)
        if normalized is None:
            continue
        filtered.append({"img_name": r["img_name"], "answer": normalized})

    canonical = canonical_label_per_image(filtered)
    return {f"{SLAKE_IMAGE_ID_PREFIX}{img_name}": label for img_name, label in canonical.items()}


def build_slake_bucket_membership(records: list[dict], modality: str, location: str) -> list[str]:
    """All images (any content_type, not just 'Abnormality') belonging to
    the modality+location bucket -- unlike build_slake_labels(), which
    returns only those with an eligible pathology answer (a smaller
    subset). Used by C6
    (harness/interventions/make_c6_organ_modality_swap.py) to know which
    images of the same domain exist in total, including those without a
    pathology label -- those become candidates for unrestricted pairing.
    First-occurrence order, without duplicates (each image appears in
    several questions in the raw JSON)."""
    seen: list[str] = []
    seen_set: set[str] = set()
    for r in records:
        if r.get("modality") == modality and r.get("location") == location:
            img_name = r["img_name"]
            if img_name not in seen_set:
                seen_set.add(img_name)
                seen.append(img_name)
    return [f"{SLAKE_IMAGE_ID_PREFIX}{img_name}" for img_name in seen]


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slake-dir", required=True)
    parser.add_argument("--modality", default="X-Ray")
    parser.add_argument("--location", default="Lung")
    parser.add_argument("--output", required=True)
    parser.add_argument("--membership-output", default=None,
                         help="If given, also writes the list of ALL images in the bucket "
                              "(any content_type, not only those with an eligible pathology label) "
                              "-- used by C6 (make_c6_organ_modality_swap.py) to find the "
                              "free pairing pool.")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    all_records = []
    for split in ("train", "test", "validate"):
        with open(f"{args.slake_dir}/{split}.json", "r", encoding="utf-8") as fp:
            all_records.extend(json.load(fp))

    labels = build_slake_labels(all_records, modality=args.modality, location=args.location)
    with open(args.output, "w", encoding="utf-8") as fp:
        json.dump(labels, fp, indent=2, ensure_ascii=False)
    print(f"{len(labels)} pathology labels ({args.modality}/{args.location}) -> {args.output}")

    if args.membership_output:
        membership = build_slake_bucket_membership(all_records, modality=args.modality, location=args.location)
        with open(args.membership_output, "w", encoding="utf-8") as fp:
            json.dump(membership, fp, indent=2, ensure_ascii=False)
        print(f"{len(membership)} images in the bucket ({args.modality}/{args.location}, "
              f"any content_type) -> {args.membership_output}")
