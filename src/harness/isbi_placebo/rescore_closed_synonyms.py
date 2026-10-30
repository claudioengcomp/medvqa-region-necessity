"""E7 (19/09/2026): re-scores ALREADY GENERATED predictions accepting two polarity synonyms in the
CLOSED-ENDED questions, with no new inference and without touching `answer_matches` (the ruler shared by
all models stays identical).

Rule, deliberately minimal and closed:
  - applies only when the gold is "yes" or "no" (closed-ended question);
  - "negative" counts as "no" and "positive" counts as "yes";
  - nothing else is accepted: "possibly", finding names ("infiltration"), sentences, all remain wrong.

Reason (recorded in §36 of the plan): MedVLThinker answers "negative" in 47 % of the HEAL closed-ended questions,
21/57 in one of the Kvasir closed-ended questions and 29/355 in SLAKE; exact matching counts all of that as error,
which mixes "does not know" with "said the same thing in another word". The fine-tuned models never produce
these tokens (they learned the yes/no vocabulary), so the rule only affects the zero-shot runs.

Monotonic by construction: an already-correct prediction is literally "yes"/"no", never in the map, so
no hit turns into an error. Reversible: the original files remain in the git history.

    python -m harness.isbi_placebo.rescore_closed_synonyms --input results/isbi_placebo/X.json [--dry-run]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

CLOSED_GOLDS = ("yes", "no")
SYNONYMS = {"negative": "no", "positive": "yes"}


def apply_synonyms(predictions: list[dict]) -> tuple[list[dict], dict]:
    """Returns (updated predictions, summary). Does not change `predicted`: only recomputes `correct`,
    and annotates `closed_synonym` on the item that changed, so the file says what was accepted."""
    updated, n_flipped, by_token = [], 0, {}
    for p in predictions:
        pred = str(p["predicted"]).strip().lower()
        gold = str(p["gold"]).strip().lower()
        if not p["correct"] and gold in CLOSED_GOLDS and SYNONYMS.get(pred) == gold:
            n_flipped += 1
            by_token[pred] = by_token.get(pred, 0) + 1
            updated.append({**p, "correct": True, "closed_synonym": f"{pred}->{gold}"})
        else:
            updated.append(p)
    return updated, {"n_flipped": n_flipped, "by_token": by_token}


def rescore_file(path: str, dry_run: bool = False) -> dict:
    record = json.loads(Path(path).read_text())
    preds = record.get("predictions")
    if preds is None:
        return {"file": path, "skipped": "sem predictions"}
    n = len(preds)
    before = sum(1 for p in preds if p["correct"])
    updated, summary = apply_synonyms(preds)
    after = sum(1 for p in updated if p["correct"])
    if after < before:
        raise AssertionError(f"{path}: rescore diminuiu acertos ({before} -> {after}) — impossivel por construcao")
    out = {"file": path, "n": n, "n_correct_before": before, "n_correct_after": after,
           "accuracy_before": before / n if n else 0.0, "accuracy_after": after / n if n else 0.0,
           "delta_pp": 100 * (after - before) / n if n else 0.0, **summary}
    if not dry_run and summary["n_flipped"]:
        record["predictions"] = updated
        record["n_correct"] = after
        record["accuracy"] = after / n if n else 0.0
        record["closed_synonyms_e7"] = {"synonyms": SYNONYMS, "n_flipped": summary["n_flipped"]}
        Path(path).write_text(json.dumps(record, indent=1) + "\n")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    for path in a.input:
        print(json.dumps(rescore_file(path, a.dry_run), ensure_ascii=False))


if __name__ == "__main__":
    main()
