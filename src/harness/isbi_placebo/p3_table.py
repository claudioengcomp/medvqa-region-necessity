"""Item 4 (14/09, authors): table of gate P3. 15 Kvasir runs x fills {black, blur 10 %, region mean color}
x {polyp, instrument, pure negative ("Is there text?")}: Δ_nec [CI], cell marked (**) when the CI excludes
zero (upward in the dependent types, either side in the negative). Summary per family (Qwen, SmolVLM2, M3AE):
how many seeds pass criterion E3 (black AND blur 10 % or region mean color) on polyp and on instrument.
Blur 4 % goes in the fill-sensitivity figure, not here. Reads only necessity_<ckpt>.json.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FILLS = [("black", "preto"), ("blur10", "blur 10 %"), ("regmean", "cor média região")]
GROUPS = [("dependent_polyp", "pólipo", "class"), ("dependent_instrument", "instrumento", "class"), ("Is there text?", "negativo puro (texto)", "template")]
FAMILY = {"QWEN2VL": "Qwen2-VL", "SMOLVLM": "SmolVLM2", "M3AE": "M3AE"}
_RE = re.compile(r"^necessity_(?P<key>(?P<model>[A-Z0-9]+)(?:_(?P<peft>[A-Z0-9]+))?_KVASIR_seed(?P<seed>\d))\.json$")


def _cell(s: dict, fill: str, dependent: bool) -> dict | None:
    k = "delta_nec" if fill == "black" else f"delta_nec_{fill}"
    if k not in s:
        return None
    lo, hi = s[f"{k}_ci"]
    return {"n": s["n"], "delta": s[k], "ci": [lo, hi], "mark": (lo > 0) if dependent else (lo > 0 or hi < 0)}


def collect(results_dir: str) -> dict:
    rows, fam = {}, {}
    for path in sorted(Path(results_dir).glob("necessity_*_KVASIR_seed*.json")):
        m = _RE.match(path.name)
        if not m:
            continue
        nec = json.loads(path.read_text()); key = m["key"]
        cfg = m["model"] + (f"_{m['peft']}" if m["peft"] else "")
        row = {"config": cfg, "family": FAMILY.get(m["model"], m["model"]), "seed": int(m["seed"]), "cells": {}, "e3": {}}
        for gkey, _, kind in GROUPS:
            s = (nec["by_class"] if kind == "class" else nec["by_template"]).get(gkey, {})
            dependent = kind == "class"
            row["cells"][gkey] = {f: _cell(s, f, dependent) for f, _ in FILLS}
            if dependent:
                e3 = s.get("e3") or {}
                row["e3"][gkey] = e3.get("necessary")
        rows[key] = row
        f = fam.setdefault(row["family"], {"n_seeds": 0, "n_evaluable": {g: 0 for g, _, k in GROUPS if k == "class"},
                                           "n_pass_e3": {g: 0 for g, _, k in GROUPS if k == "class"}, "checkpoints": []})
        f["n_seeds"] += 1; f["checkpoints"].append(key)
        for g, _, k in GROUPS:
            if k == "class" and row["e3"].get(g) is not None:
                f["n_evaluable"][g] += 1; f["n_pass_e3"][g] += int(bool(row["e3"][g]))
    return {"fills": [f for f, _ in FILLS], "groups": [g for g, _, _ in GROUPS], "rows": rows, "families": fam}


def _fmt(c: dict | None) -> str:
    if not c:
        return "—"
    lo, hi = c["ci"]; m = "**" if c["mark"] else ""
    return f"{m}{100 * c['delta']:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}]{m}"


def render(out: dict) -> str:
    L = ["# Tabela do P3 — Kvasir, 15 linhas × preenchimento × grupo", "",
         "Δ_nec = Acc(P) − Acc(T) em pp, IC 95 % bootstrap pareado. **Negrito** = IC exclui zero (para cima em pólipo e "
         "instrumento; qualquer lado no negativo puro). Preto, blur 10 % da largura e cor média da própria região; blur 4 % fica "
         "na figura de sensibilidade. \"—\" = condição ainda não rodada para a célula. E3 = preto E (blur 10 % ou cor média).", ""]
    hdr = "| checkpoint | " + " | ".join(f"{glab} · {flab}" for _, glab, _ in GROUPS for _, flab in FILLS) + " | E3 pólipo | E3 instr. |"
    sep = "|---|" + "---|" * (len(GROUPS) * len(FILLS)) + "---|---|"
    L += [hdr, sep]
    e3s = lambda v: "—" if v is None else ("sim" if v else "não")
    for key, r in out["rows"].items():
        L.append(f"| {key} | " + " | ".join(_fmt(r["cells"][g].get(f)) for g, _, _ in GROUPS for f, _ in FILLS)
                 + f" | {e3s(r['e3'].get('dependent_polyp'))} | {e3s(r['e3'].get('dependent_instrument'))} |")
    L += ["", "## Resumo por família (critério E3)", "", "| família | seeds | pólipo: passam / avaliáveis | instrumento: passam / avaliáveis |", "|---|---:|---:|---:|"]
    for fam, f in out["families"].items():
        L.append(f"| {fam} | {f['n_seeds']} | {f['n_pass_e3']['dependent_polyp']} / {f['n_evaluable']['dependent_polyp']} | "
                 f"{f['n_pass_e3']['dependent_instrument']} / {f['n_evaluable']['dependent_instrument']} |")
    L += ["", "Avaliáveis = seeds com ao menos um preenchimento plausível rodado no conjunto inteiro (E3)."]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results-dir", default="results/isbi_placebo"); ap.add_argument("--docs-dir", default="docs/isbi/placebo")
    a = ap.parse_args(argv)
    out = collect(a.results_dir)
    Path(a.results_dir, "p3_table.json").write_text(json.dumps(out, indent=1) + "\n")
    md = render(out); Path(a.docs_dir, "p3_table.md").write_text(md); print(md)


if __name__ == "__main__":
    main()
