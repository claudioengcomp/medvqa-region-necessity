"""Item 1 (15/09/2026, authors): coverage reconciliation. For the 15 Kvasir runs, the state
of each fill on disk (results/isbi_placebo/<ckpt>_<cond>.json): black (T, P), blur 4 %
(T_blur, P_blur), blur 10 % (T_blur10, P_blur10), region mean color (T_regmean, P_regmean) on the
whole set, and 15 px ring (T/P_ringmean_fill300, 300 stratified). A run counts
as "E3 evaluable" when it has T and P under black AND under blur 10 % or mean color.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CONFIGS = ["QWEN2VL_LORA", "QWEN2VL_DORA", "SMOLVLM_LORA", "SMOLVLM_DORA", "M3AE"]
FILLS = [("black", "preto", "T", "P", ""), ("blur", "blur 4 %", "T_blur", "P_blur", ""), ("blur10", "blur 10 %", "T_blur10", "P_blur10", ""),
         ("regmean", "cor média região", "T_regmean", "P_regmean", ""), ("ringmean", "anel 15 px (300)", "T_ringmean", "P_ringmean", "_fill300")]


def collect(results_dir: str) -> dict:
    rows = {}
    for cfg in CONFIGS:
        for seed in (0, 1, 2):
            key = f"{cfg}_KVASIR_seed{seed}"
            st = {}
            for fill, _, t, p, suf in FILLS:
                ht = Path(results_dir, f"{key}_{t}{suf}.json").is_file(); hp = Path(results_dir, f"{key}_{p}{suf}.json").is_file()
                st[fill] = {"T": ht, "P": hp, "pair": ht and hp}
            st["C0"] = Path(results_dir, f"{key}_C0.json").is_file()
            e3_ready = st["black"]["pair"] and (st["blur10"]["pair"] or st["regmean"]["pair"])
            rows[key] = {"config": cfg, "seed": seed, "fills": st, "e3_evaluable": e3_ready}
    n = {f: sum(r["fills"][f]["pair"] for r in rows.values()) for f, *_ in FILLS}
    return {"rows": rows, "n_pairs_by_fill": n, "n_e3_evaluable": sum(r["e3_evaluable"] for r in rows.values()), "n_lines": len(rows)}


def _mark(c: dict) -> str:
    return "✓" if c["pair"] else ("T" if c["T"] else ("P" if c["P"] else "—"))


def render(out: dict) -> str:
    L = ["# Cobertura das 15 linhas do Kvasir por preenchimento (o que existe em disco)", "",
         "✓ = T e P presentes; T ou P = só um dos dois; — = nenhum. Anel: 300 estratificadas; demais: 2.121. "
         "E3 avaliável = preto ✓ e (blur 10 % ✓ ou cor média ✓).", "",
         "| linha | C0 | " + " | ".join(lab for _, lab, *_ in FILLS) + " | E3 avaliável |", "|---|---|" + "---|" * len(FILLS) + "---|"]
    for key, r in out["rows"].items():
        L.append(f"| {key} | {'✓' if r['fills']['C0'] else '—'} | " + " | ".join(_mark(r["fills"][f]) for f, *_ in FILLS) + f" | {'sim' if r['e3_evaluable'] else 'não'} |")
    L += ["", "| preenchimento | linhas com T e P |", "|---|---:|"] + [f"| {lab} | {out['n_pairs_by_fill'][f]} / {out['n_lines']} |" for f, lab, *_ in FILLS]
    L += ["", f"**Linhas E3 avaliáveis: {out['n_e3_evaluable']} / {out['n_lines']}.**"]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results-dir", default="results/isbi_placebo"); ap.add_argument("--docs-dir", default="docs/isbi/placebo")
    a = ap.parse_args(argv)
    out = collect(a.results_dir)
    Path(a.results_dir, "e3_coverage.json").write_text(json.dumps(out, indent=1) + "\n")
    md = render(out); Path(a.docs_dir, "e3_coverage.md").write_text(md); print(md)


if __name__ == "__main__":
    main()
