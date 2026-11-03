"""Compares two harness prediction files item by item.

Reads the `correct` field already stored (scoring rule of `rescore_predictions.py`); does not
recompute anything. Serves to tell whether a re-inference reproduces a cache --
for example the original C0 cell re-run in a new environment (F0, step 9 of the ISBI
protocol). Reading reference: 0 % per-item disagreement
in the same environment, 2.7-5.9 % across environments.

Usage:
    python -m harness.isbi_placebo.compare_prediction_files         --ref results/QWEN2VL_LORA_KVASIR_seed0_C0.json         --new results/isbi_placebo/QWEN2VL_LORA_KVASIR_seed0_C0_ws3repro.json         --output results/isbi_placebo/compare_C0_seed0_ws3repro.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def _load(path: Path) -> dict[int, dict]:
    data = json.loads(Path(path).read_text())
    rows = {}
    for p in data["predictions"]:
        qid = p["qid"]
        if qid in rows:
            raise ValueError(f"{path}: qid {qid} repetido")
        rows[qid] = p
    return rows


def compare_predictions(ref_path: Path, new_path: Path, qids=None) -> dict:
    """`qids`: if given, restricts the comparison to these qids (e.g. only the evaluable ones)."""
    ref = _load(ref_path)
    new = _load(new_path)
    common = sorted(set(ref) & set(new) & (set(qids) if qids is not None else set(ref)))
    if not common:
        raise ValueError("nenhum qid em comum entre os dois arquivos")
    n_disagree_pred = n_disagree_correct = wrong_to_right = right_to_wrong = 0
    ref_correct = new_correct = 0
    for q in common:
        a, b = ref[q], new[q]
        if a["gold"] != b["gold"]:
            raise ValueError(f"qid {q}: gold difere entre os arquivos ({a['gold']!r} vs {b['gold']!r})")
        if a["predicted"] != b["predicted"]:
            n_disagree_pred += 1
        ca, cb = bool(a["correct"]), bool(b["correct"])
        ref_correct += ca
        new_correct += cb
        if ca != cb:
            n_disagree_correct += 1
            if cb:
                wrong_to_right += 1
            else:
                right_to_wrong += 1
    n = len(common)
    acc_ref, acc_new = ref_correct / n, new_correct / n
    return {
        "n_common": n,
        "only_ref": len(set(ref) - set(new)),
        "only_new": len(set(new) - set(ref)),
        "n_disagree_pred": n_disagree_pred,
        "disagree_pred_rate": n_disagree_pred / n,
        "n_disagree_correct": n_disagree_correct,
        "flips_wrong_to_right": wrong_to_right,
        "flips_right_to_wrong": right_to_wrong,
        "acc_ref": acc_ref,
        "acc_new": acc_new,
        "delta_pp": (acc_new - acc_ref) * 100,
    }


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", required=True, help="arquivo de referencia (cache do P0)")
    ap.add_argument("--new", required=True, help="arquivo novo (re-inferencia)")
    ap.add_argument("--output", help="onde gravar o relatorio JSON")
    args = ap.parse_args(argv)
    out = compare_predictions(Path(args.ref), Path(args.new))
    out = {"ref": str(args.ref), "new": str(args.new), **out}
    print(json.dumps(out, indent=2))
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
