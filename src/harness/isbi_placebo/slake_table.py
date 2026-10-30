"""Authors' decision (15/09): SLAKE gets its own table, separate from P3 (Kvasir by definition, because the gate
was Kvasir). Same columns as p3_table -- Δ_nec [CI] under {black, blur 10 %, region mean color} -- per group
and per seed (three seeds in the fine-tuned cells and in the from-scratch M3AE; one in the checkpoint released
by the M3AE authors), plus the headroom Acc(C0) - M0 per group. Nothing merged with Kvasir.

"Per template" axis in SLAKE: the questions are free-form (145 distinct question texts across 388 evaluable, n from 1 to
8 per text), so the analogue of the Kvasir templates is the pre-registered class (disease-dependent,
organ-dependent, negative control = modality/plane); the breakdown per question text goes in the
necessity_<ckpt>_SLAKE_<seed>.md. Reads only necessity_*_SLAKE_seed*.json.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FILLS = [("black", "preto"), ("blur10", "blur 10 %"), ("regmean", "cor média região")]
GROUPS = [("dependent_disease", "doença", True), ("dependent_organ", "órgão", True), ("negative_control", "negativo (mod./plano)", False)]
FAMILY = {"QWEN2VL": "Qwen2-VL", "SMOLVLM": "SmolVLM2", "M3AE": "M3AE"}
_RE_FMT = r"^%s_(?P<key>(?P<model>[A-Z0-9]+)(?:_(?P<peft>[A-Z0-9]+))?_SLAKE_seed(?P<seed>\d))\.json$"
_RE = re.compile(_RE_FMT % "necessity")


def _cell(s: dict, fill: str, dependent: bool) -> dict | None:
    k = "delta_nec" if fill == "black" else f"delta_nec_{fill}"
    if k not in s or f"{k}_ci" not in s:
        return None
    lo, hi = s[f"{k}_ci"]
    return {"n": s.get("n"), "delta": s[k], "ci": [lo, hi], "mark": (lo > 0) if dependent else (lo > 0 or hi < 0)}


def _ceiling(s: dict) -> dict | None:
    if "ceiling" not in s:
        return None
    return {"acc_c0": s.get("acc", {}).get("C0"), "acc_m0": s.get("acc_m0"), "ceiling": s["ceiling"], "no_margin": bool(s.get("no_margin"))}


def collect(results_dir: str, prefix: str = "necessity") -> dict:
    """`prefix` = "necessity" (388 evaluable) or "slake_closed" (E8: evaluable closed-ended); same JSON format."""
    rows, fam = {}, {}
    rx = re.compile(_RE_FMT % prefix)
    for path in sorted(Path(results_dir).glob(f"{prefix}_*_SLAKE_seed*.json")):
        m = rx.match(path.name)
        if not m:
            continue
        nec = json.loads(path.read_text()); key = m["key"]
        cfg = m["model"] + (f"_{m['peft']}" if m["peft"] else "")
        row = {"config": cfg, "family": FAMILY.get(m["model"], m["model"]), "seed": int(m["seed"]), "cells": {}, "e3": {}, "ceiling": {}}
        for gkey, _, dependent in GROUPS:
            s = nec.get("by_class", {}).get(gkey, {})
            row["cells"][gkey] = {f: _cell(s, f, dependent) for f, _ in FILLS}
            row["ceiling"][gkey] = _ceiling(s)
            if dependent:
                row["e3"][gkey] = (s.get("e3") or {}).get("necessary")
        rows[key] = row
        deps = [g for g, _, d in GROUPS if d]
        f = fam.setdefault(row["family"], {"n_seeds": 0, "n_evaluable": {g: 0 for g in deps}, "n_pass_e3": {g: 0 for g in deps},
                                           "n_no_margin": {g: 0 for g, _, _ in GROUPS}, "checkpoints": []})
        f["n_seeds"] += 1; f["checkpoints"].append(key)
        for g in deps:
            if row["e3"].get(g) is not None:
                f["n_evaluable"][g] += 1; f["n_pass_e3"][g] += int(bool(row["e3"][g]))
        for g, _, _ in GROUPS:
            c = row["ceiling"].get(g)
            if c and c["no_margin"]:
                f["n_no_margin"][g] += 1
    return {"fills": [f for f, _ in FILLS], "groups": [g for g, _, _ in GROUPS], "rows": rows, "families": fam}


def _fmt(c: dict | None) -> str:
    if not c:
        return "—"
    lo, hi = c["ci"]; m = "**" if c["mark"] else ""
    return f"{m}{100 * c['delta']:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}]{m}"


def _fmt_ceiling(c: dict | None) -> str:
    if not c:
        return "—"
    return f"{100 * c['ceiling']:+.1f}" + (" (sem margem)" if c["no_margin"] else "")


def render(out: dict, title: str | None = None, intro: str | None = None) -> str:
    L = [title or "# Tabela do SLAKE — células × preenchimento × classe (secundário; separado do P3)", "",
         intro or "Δ_nec = Acc(P) − Acc(T) em pp, IC 95 % bootstrap pareado, 388 perguntas avaliáveis (doença 198, órgão 68, negativo 142). "
         "**Negrito** = IC exclui zero (para cima em doença e órgão; qualquer lado no controle negativo). Preto, blur 10 % da largura e "
         "cor média da própria região (E3 do SLAKE, como ordenado; sem blur 4 % e sem anel, por decisão de 15/09). \"—\" = condição ainda "
         "não rodada para a célula. E3 = preto E (blur 10 % ou cor média). Teto = Acc(C0) − M0 (M0 = TF-IDF+LR só com a pergunta) por "
         "classe, em pp; \"sem margem\" = teto ≤ 0, nΔ_nec indefinido.", "",
         "Eixo por classe: as perguntas do SLAKE são livres (145 enunciados distintos), então a classe pré-registrada faz o papel dos "
         "templates do Kvasir; o desdobramento por enunciado está em cada `necessity_<ckpt>_SLAKE_<seed>.md`. Três seeds nas células "
         "fine-tuned e no M3AE do zero (`M3AE_SCRATCH`); o checkpoint dos autores (`M3AE_SLAKE_seed0`) tem uma seed.", ""]
    hdr = ("| checkpoint | " + " | ".join(f"{glab} · {flab}" for _, glab, _ in GROUPS for _, flab in FILLS)
           + " | E3 doença | E3 órgão | " + " | ".join(f"teto {glab}" for _, glab, _ in GROUPS) + " |")
    sep = "|---|" + "---|" * (len(GROUPS) * len(FILLS)) + "---|---|" + "---:|" * len(GROUPS)
    L += [hdr, sep]
    e3s = lambda v: "—" if v is None else ("sim" if v else "não")
    for key, r in out["rows"].items():
        L.append(f"| {key} | " + " | ".join(_fmt(r["cells"][g].get(f)) for g, _, _ in GROUPS for f, _ in FILLS)
                 + f" | {e3s(r['e3'].get('dependent_disease'))} | {e3s(r['e3'].get('dependent_organ'))} | "
                 + " | ".join(_fmt_ceiling(r["ceiling"].get(g)) for g, _, _ in GROUPS) + " |")
    L += ["", "## Resumo por família (critério E3 e margem sobre o M0)", "",
          "| família | seeds | doença: passam / avaliáveis | órgão: passam / avaliáveis | sem margem (doença / órgão / negativo) |", "|---|---:|---:|---:|---:|"]
    for fam, f in out["families"].items():
        nm = f["n_no_margin"]
        L.append(f"| {fam} | {f['n_seeds']} | {f['n_pass_e3']['dependent_disease']} / {f['n_evaluable']['dependent_disease']} | "
                 f"{f['n_pass_e3']['dependent_organ']} / {f['n_evaluable']['dependent_organ']} | "
                 f"{nm['dependent_disease']} / {nm['dependent_organ']} / {nm['negative_control']} |")
    L += ["", "Avaliáveis = seeds com ao menos um preenchimento plausível rodado (E3). Seeds do M3AE = do zero (3) + autores (1), contadas juntas na família."]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results-dir", default="results/isbi_placebo"); ap.add_argument("--docs-dir", default="docs/isbi/placebo")
    a = ap.parse_args(argv)
    out = collect(a.results_dir)
    Path(a.results_dir, "slake_table.json").write_text(json.dumps(out, indent=1) + "\n")
    md = render(out); Path(a.docs_dir, "slake_table.md").write_text(md); print(md)


if __name__ == "__main__":
    main()
