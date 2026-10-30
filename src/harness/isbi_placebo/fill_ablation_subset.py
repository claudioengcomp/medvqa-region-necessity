"""Subset for the fill ablation (F-mean, F-blur): 300 Kvasir questions,
STRATIFIED by template (proportional allocation, largest-remainder rounding,
minimum 1 per template with an evaluable item), drawn with a fixed seed.

Execution detail fixed on 14/09/2026, before any inference with
F-mean/F-blur: the plan only said "subset of 300 questions"; the
stratification guarantees that the artefact box and the polyp count are in
the subset. Recorded in pre-registration §3.7 as a detail, not as an amendment.

Usage:
    python -m harness.isbi_placebo.fill_ablation_subset         --inventory results/isbi_placebo/inventory_kvasir_test_clean.json         --n 300 --seed 20260913 --output results/isbi_placebo/fill_ablation_subset_kvasir.json
"""
from __future__ import annotations

import argparse
import collections
import json
import random
from pathlib import Path


def build_subset(inventory: str, n_total: int = 300, seed: int = 20260913) -> dict:
    qs = [q for q in json.loads(Path(inventory).read_text())["questions"] if q["evaluable"]]
    by_t = collections.defaultdict(list)
    for q in qs:
        by_t[q["question"]].append(q["qid"])
    n_all = len(qs)
    raw = {t: n_total * len(v) / n_all for t, v in by_t.items()}
    alloc = {t: max(1, int(raw[t])) for t in by_t}
    rest = n_total - sum(alloc.values())
    for t in sorted(by_t, key=lambda t: raw[t] - int(raw[t]), reverse=True)[:max(rest, 0)]:
        alloc[t] += 1
    while sum(alloc.values()) > n_total:  # only happens if the minimum of 1 exceeds the total
        t = max(alloc, key=alloc.get); alloc[t] -= 1
    rng = random.Random(seed)
    qids = []
    for t in sorted(by_t):
        qids += sorted(rng.sample(sorted(by_t[t]), min(alloc[t], len(by_t[t]))))
    return {"inventory": inventory, "n_total_requested": n_total, "n": len(qids), "seed": seed, "stratified_by": "template",
            "per_template": {t: alloc[t] for t in sorted(by_t)}, "qids": sorted(qids)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inventory", required=True); ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--seed", type=int, default=20260913); ap.add_argument("--output", required=True)
    a = ap.parse_args(argv)
    out = build_subset(a.inventory, a.n, a.seed)
    Path(a.output).write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({"n": out["n"], "per_template": out["per_template"]}, indent=1))


if __name__ == "__main__":
    main()
