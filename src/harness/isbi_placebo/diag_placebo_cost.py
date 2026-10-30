"""EXPLORATORY (item 4, 15/09/2026, authors; recorded without interpretation). Per Kvasir run, only
on the instrument questions: Acc(P) under black versus Acc(P) under blur 10 % (same questions),
paired difference with bootstrap CI and McNemar. Question: does the black control occlusion cost accuracy on
instruments in the VLMs and not in M3AE? Reads the prediction files _P.json and _P_blur10.json.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from harness.stats.compute_ldv import bootstrap_paired_diff_ci, mcnemar_test

_RE = re.compile(r"^(?P<key>[A-Z0-9]+(?:_[A-Z0-9]+)?_KVASIR_seed\d)_P\.json$")


def _preds(p: Path) -> dict:
    return {r["qid"]: bool(r["correct"]) for r in json.loads(p.read_text())["predictions"]}


def collect(results_dir: str, inventory: str, n_boot: int = 10000, seed: int = 42, cls: str = "dependent_instrument",
            other: str = "P_blur10") -> dict:
    inv = json.loads(Path(inventory).read_text())["questions"]
    qids_cls = [q["qid"] for q in inv if q["evaluable"] and q["question_class"] == cls]
    rows = {}
    for p in sorted(Path(results_dir).glob("*_KVASIR_seed?_P.json")):
        m = _RE.match(p.name)
        if not m:
            continue
        key = m["key"]; q = Path(results_dir, f"{key}_{other}.json")
        if not q.is_file():
            rows[key] = {"status": "pendente"}; continue
        a, b = _preds(p), _preds(q)
        qids = [i for i in qids_cls if i in a and i in b]
        ca, cb = [a[i] for i in qids], [b[i] for i in qids]
        n = len(qids); acc_a, acc_b = sum(ca) / n, sum(cb) / n
        lo, hi = bootstrap_paired_diff_ci(ca, cb, n_boot=n_boot, seed=seed)
        rows[key] = {"status": "ok", "n": n, "acc_P_black": acc_a, f"acc_{other}": acc_b, "diff_black_minus_other": acc_a - acc_b,
                     "diff_ci": [lo, hi], "mcnemar": mcnemar_test(ca, cb)}
    return {"class": cls, "other": other, "rows": rows, "n_boot": n_boot}


def render(out: dict) -> str:
    L = [f"# EXPLORATÓRIO — Acc(P) sob preto × Acc(P) sob blur 10 %, perguntas de {out['class']} (Kvasir)", "",
         "Registro sem interpretação. Mesmas perguntas nas duas condições; diferença = Acc(P preto) − Acc(P blur 10 %), "
         f"IC 95 % bootstrap pareado ({out['n_boot']}), McNemar. Negativo = o placebo preto custa acurácia em relação ao placebo com blur 10 %.", "",
         "| linha | n | Acc(P) preto | Acc(P) blur 10 % | diferença (pp) | IC 95 % | McNemar p |", "|---|---:|---:|---:|---:|---|---:|"]
    for key, r in out["rows"].items():
        if r.get("status") != "ok":
            L.append(f"| {key} | — | — | — | pendente | | |"); continue
        lo, hi = r["diff_ci"]
        L.append(f"| {key} | {r['n']} | {100 * r['acc_P_black']:.1f} | {100 * r['acc_P_blur10']:.1f} | {100 * r['diff_black_minus_other']:+.1f} | "
                 f"[{100 * lo:+.1f}, {100 * hi:+.1f}] | {r['mcnemar']['p_value']:.3g} |")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results-dir", default="results/isbi_placebo"); ap.add_argument("--docs-dir", default="docs/isbi/placebo")
    ap.add_argument("--inventory", default="results/isbi_placebo/inventory_kvasir_test_clean.json")
    ap.add_argument("--n-boot", type=int, default=10000); ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args(argv)
    out = collect(a.results_dir, a.inventory, a.n_boot, a.seed)
    Path(a.results_dir, "diag_placebo_cost.json").write_text(json.dumps(out, indent=1) + "\n")
    md = render(out); Path(a.docs_dir, "diag_placebo_cost.md").write_text(md); print(md)


if __name__ == "__main__":
    main()
