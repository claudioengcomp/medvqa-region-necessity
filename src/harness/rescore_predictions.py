"""Re-scores an already generated results file, without running inference
again -- applies `answer_matches` (the fix of 25/08/2026, commit `d8ba4a0`,
which treats "x ray" == "xray" == "x-ray") over the `predicted`/`gold` pairs
already saved per item. Monotonic and safe: it can only raise or keep
`accuracy`, never lower it (`answer_matches` is a superset of `==`).

Finding 27/08/2026: most of the project's results (M0, M3AE,
M3AE_SCRATCH, QWEN2VL_LORA/DORA, SMOLVLM_LORA/DORA -- ~120 files) were
generated BEFORE the fix (24-25/08, before 25/08 19:15 UTC) and were never
re-scored. Only MedVLThinker was born correct (generated after the fix).

`predicted`/`gold` already come normalized (extract_answer + normalize_text
already applied at the time of the original extraction) -- rescore only reapplies the
comparison criterion, it does not reprocess any raw text.

Usage:
    python -m harness.rescore_predictions --input results/QWEN2VL_LORA_SLAKE_C0.json
    # overwrites the file, prints the accuracy delta.
"""
from __future__ import annotations

import argparse
import json

from med_vlm.metrics.process_text import answer_matches


def rescore_predictions(predictions: list[dict]) -> tuple[list[dict], int]:
    """Recomputes `correct` for each item using `answer_matches` over the
    stored `predicted`/`gold`. Returns (updated predictions,
    number that changed from False->True) -- never True->False, by
    construction of `answer_matches` (superset of `==`)."""
    updated = []
    n_flipped = 0
    for p in predictions:
        new_correct = answer_matches(p["predicted"], [p["gold"]])
        if new_correct and not p["correct"]:
            n_flipped += 1
        assert not (p["correct"] and not new_correct), (
            f"rescore diminuiu accuracy no qid={p.get('qid')} -- não deveria ser possível, "
            f"answer_matches é superconjunto de =="
        )
        updated.append({**p, "correct": new_correct})
    return updated, n_flipped


def rescore_file(path: str) -> dict:
    """Reloads, re-scores and overwrites `path`. Returns a summary
    {path, accuracy_before, accuracy_after, n_flipped} for reporting."""
    with open(path, "r", encoding="utf-8") as fp:
        record = json.load(fp)

    accuracy_before = record["accuracy"]
    updated_predictions, n_flipped = rescore_predictions(record["predictions"])

    n = len(updated_predictions)
    n_correct = sum(1 for p in updated_predictions if p["correct"])
    record["predictions"] = updated_predictions
    record["n_correct"] = n_correct
    record["accuracy"] = (n_correct / n) if n else 0.0

    with open(path, "w", encoding="utf-8") as fp:
        json.dump(record, fp, indent=2, ensure_ascii=False)

    return {
        "path": path,
        "accuracy_before": accuracy_before,
        "accuracy_after": record["accuracy"],
        "n_flipped": n_flipped,
    }


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    summary = rescore_file(args.input)
    delta = summary["accuracy_after"] - summary["accuracy_before"]
    print(f"{summary['path']}: {summary['accuracy_before']:.4f} -> {summary['accuracy_after']:.4f} "
          f"(+{delta:.4f}, {summary['n_flipped']} itens corrigidos)")
