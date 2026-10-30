"""E5/D5 (15/09/2026, approved by the authors): 500 evaluable closed-ended HEAL questions for MedVLThinker
("no fine-tuning" contrast), stratified by anatomy x class (closed_yes / closed_no), proportional
allocation with largest-remainder rounding, seed 20260913 (the same as Kvasir). Same format as
`medvlthinker_subset_kvasir.json`. Then: `subset_arrow` over the C0/T/P/S arrows -> `*_mvt500.arrow`.

    python -m harness.isbi_placebo.heal.medvlthinker_subset_heal         --inventory results/isbi_placebo/inventory_heal_test.json --n 500 --seed 20260913         --output docs/isbi/placebo/medvlthinker_subset_heal.json
"""
from __future__ import annotations

import argparse
import collections
import json
import random
from pathlib import Path


def stratified_sample(questions: list[dict], n_total: int, seed: int) -> dict:
    strata: dict[tuple[str, str], list[int]] = collections.defaultdict(list)
    for q in questions:
        if q.get("evaluable"):
            strata[(q["anatomy"], q["question_class"])].append(int(q["qid"]))
    total = sum(len(v) for v in strata.values())
    if total < n_total:
        raise ValueError(f"so {total} perguntas avaliaveis para {n_total} pedidas")
    keys = sorted(strata)
    raw = {k: n_total * len(strata[k]) / total for k in keys}
    alloc = {k: int(raw[k]) for k in keys}
    for k in sorted(keys, key=lambda k: -(raw[k] - alloc[k]))[: n_total - sum(alloc.values())]:
        alloc[k] += 1
    rng = random.Random(seed)
    qids: list[int] = []
    for k in keys:
        pool = sorted(strata[k]); rng.shuffle(pool)
        qids.extend(pool[: alloc[k]])
    return {"n_total_requested": n_total, "n": len(qids), "seed": seed, "stratified_by": "anatomy x question_class",
            "per_stratum": {f"{a} | {c}": alloc[(a, c)] for a, c in keys},
            "per_anatomy": {a: sum(v for (aa, _), v in alloc.items() if aa == a) for a in sorted({a for a, _ in keys})},
            "per_class": {c: sum(v for (_, cc), v in alloc.items() if cc == c) for c in sorted({c for _, c in keys})},
            "qids": sorted(qids)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inventory", required=True); ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--seed", type=int, default=20260913); ap.add_argument("--output", required=True)
    a = ap.parse_args(argv)
    inv = json.loads(Path(a.inventory).read_text())
    out = {"inventory": a.inventory, **stratified_sample(inv["questions"], a.n, a.seed)}
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    Path(a.output).write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "qids"}, indent=1))


if __name__ == "__main__":
    main()
