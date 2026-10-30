"""E5 (15/09/2026, D4): HEAL's own table, separate from P3 and from the SLAKE one. Reads only
necessity_*_HEAL_seed*.json.

Table 1 (per class): Δ_nec [CI] under {black, blur 10 %, region mean color} for closed_yes and
closed_no (both depend on the region: the question names the target anatomy), E3 verdict per class and
headroom Acc(C0) − M0 per class. Table 2 (per anatomy, 8 groups): Δ_nec under black [CI] and headroom per
anatomy (aorta and heart have M0 ≈ 87 %, almost no headroom). Per-family summary as in P3.
HEAL has no pure negative control (every closed-ended question names an anatomy): recorded.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FILLS = [("black", "preto"), ("blur10", "blur 10 %"), ("regmean", "cor média região")]
GROUPS = [("closed_yes", "fechada-sim", True), ("closed_no", "fechada-não", True)]
ANATOMIES = ["Aorta", "Heart", "Left upper lung", "Left middle lung", "Left lower lung", "Right upper lung", "Right middle lung", "Right lower lung"]
FAMILY = {"QWEN2VL": "Qwen2-VL", "SMOLVLM": "SmolVLM2", "M3AE": "M3AE"}
_RE = re.compile(r"^necessity_(?P<key>(?P<model>[A-Z0-9]+)(?:_(?P<peft>[A-Z0-9]+))?_HEAL_seed(?P<seed>\d))\.json$")


def _cell(s: dict, fill: str, dependent: bool = True) -> dict | None:
    k = "delta_nec" if fill == "black" else f"delta_nec_{fill}"
    if k not in s or f"{k}_ci" not in s:
        return None
    lo, hi = s[f"{k}_ci"]
    return {"n": s.get("n"), "delta": s[k], "ci": [lo, hi], "mark": (lo > 0) if dependent else (lo > 0 or hi < 0)}


def _components(s: dict) -> dict | None:
    """Components under black (request of 15/09/2026): Acc(C0), Acc(T), Acc(P), Acc(S) with paired CI, Acc(C0) − Acc(P) [CI]
    (= vdd["P"]) and Acc(S)/Acc(C0) [CI]."""
    acc = s.get("acc") or {}
    if not all(k in acc for k in ("C0", "T", "P", "S")):
        return None
    ci = s.get("acc_ci") or {}
    return {"n": s.get("n"), "acc": {k: acc[k] for k in ("C0", "T", "P", "S")}, "acc_ci": {k: ci.get(k) for k in ("C0", "T", "P", "S")},
            "c0_minus_p": (s.get("vdd") or {}).get("P"), "c0_minus_p_ci": (s.get("vdd_ci") or {}).get("P"),
            "sufficiency": s.get("sufficiency"), "sufficiency_ci": s.get("sufficiency_ci")}


def _ceiling(s: dict) -> dict | None:
    if "ceiling" not in s:
        return None
    return {"acc_c0": s.get("acc", {}).get("C0"), "acc_m0": s.get("acc_m0"), "ceiling": s["ceiling"], "no_margin": bool(s.get("no_margin"))}


def collect(results_dir: str) -> dict:
    rows, fam = {}, {}
    for path in sorted(Path(results_dir).glob("necessity_*_HEAL_seed*.json")):
        m = _RE.match(path.name)
        if not m:
            continue
        nec = json.loads(path.read_text()); key = m["key"]
        cfg = m["model"] + (f"_{m['peft']}" if m["peft"] else "")
        row = {"config": cfg, "family": FAMILY.get(m["model"], m["model"]), "seed": int(m["seed"]), "cells": {}, "e3": {}, "ceiling": {}, "anatomy": {}}
        for gkey, _, dependent in GROUPS:
            s = nec.get("by_class", {}).get(gkey, {})
            row["cells"][gkey] = {f: _cell(s, f, dependent) for f, _ in FILLS}
            row["ceiling"][gkey] = _ceiling(s)
            row["e3"][gkey] = (s.get("e3") or {}).get("necessary")
        for a in ANATOMIES:
            s = nec.get("by_anatomy", {}).get(a, {})
            row["anatomy"][a] = {"black": _cell(s, "black"), "ceiling": _ceiling(s), "components": _components(s)}
        rows[key] = row
        deps = [g for g, _, _ in GROUPS]
        f = fam.setdefault(row["family"], {"n_seeds": 0, "n_evaluable": {g: 0 for g in deps}, "n_pass_e3": {g: 0 for g in deps},
                                           "n_no_margin": {g: 0 for g in deps}, "checkpoints": []})
        f["n_seeds"] += 1; f["checkpoints"].append(key)
        for g in deps:
            if row["e3"].get(g) is not None:
                f["n_evaluable"][g] += 1; f["n_pass_e3"][g] += int(bool(row["e3"][g]))
            c = row["ceiling"].get(g)
            if c and c["no_margin"]:
                f["n_no_margin"][g] += 1
    return {"fills": [f for f, _ in FILLS], "groups": [g for g, _, _ in GROUPS], "anatomies": ANATOMIES, "rows": rows, "families": fam}


def _fmt(c: dict | None) -> str:
    if not c:
        return "—"
    lo, hi = c["ci"]; m = "**" if c["mark"] else ""
    return f"{m}{100 * c['delta']:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}]{m}"


def _fmt_ceiling(c: dict | None) -> str:
    if not c:
        return "—"
    return f"{100 * c['ceiling']:+.1f}" + (" (sem margem)" if c["no_margin"] else "")


def _fmt_acc(v, ci) -> str:
    if v is None:
        return "—"
    return f"{100 * v:.1f} [{100 * ci[0]:.1f}, {100 * ci[1]:.1f}]" if ci else f"{100 * v:.1f}"


def _fmt_pp(v, ci) -> str:
    if v is None:
        return "—"
    return f"{100 * v:+.1f} [{100 * ci[0]:+.1f}, {100 * ci[1]:+.1f}]" if ci else f"{100 * v:+.1f}"


def _fmt_ratio(v, ci) -> str:
    if v is None:
        return "—"
    return f"{v:.2f} [{ci[0]:.2f}, {ci[1]:.2f}]" if ci else f"{v:.2f}"


def render(out: dict) -> str:
    e3s = lambda v: "—" if v is None else ("sim" if v else "não")
    L = ["# Tabela do HEAL — células × preenchimento × classe e anatomia (separada do P3 e do SLAKE)", "",
         "Δ_nec = Acc(P) − Acc(T) em pp, IC 95 % bootstrap pareado, perguntas fechadas avaliáveis do teste do HEAL (unidade = imagem × "
         "anatomia; exclusões da E4). **Negrito** = IC exclui zero para cima. Preto, blur 10 % da largura e cor média da própria região "
         "(E5/D4; sem blur 4 %, dose e anel). \"—\" = condição ainda não rodada. E3 = preto E (blur 10 % ou cor média). Teto = Acc(C0) − M0 "
         "(TF-IDF+LR só com a pergunta, treino fechado do HEAL) por grupo, em pp; \"sem margem\" = teto ≤ 0. O HEAL não tem controle "
         "negativo puro: toda pergunta fechada nomeia a anatomia alvo.", "",
         "## Por classe", ""]
    hdr = ("| checkpoint | " + " | ".join(f"{glab} · {flab}" for _, glab, _ in GROUPS for _, flab in FILLS)
           + " | E3 sim | E3 não | " + " | ".join(f"teto {glab}" for _, glab, _ in GROUPS) + " |")
    L += [hdr, "|---|" + "---|" * (len(GROUPS) * len(FILLS)) + "---|---|" + "---:|" * len(GROUPS)]
    for key, r in out["rows"].items():
        L.append(f"| {key} | " + " | ".join(_fmt(r["cells"][g].get(f)) for g, _, _ in GROUPS for f, _ in FILLS)
                 + f" | {e3s(r['e3'].get('closed_yes'))} | {e3s(r['e3'].get('closed_no'))} | "
                 + " | ".join(_fmt_ceiling(r["ceiling"].get(g)) for g, _, _ in GROUPS) + " |")
    L += ["", "## Por anatomia (Δ_nec sob preto [IC] · teto)", "",
          "| checkpoint | " + " | ".join(out["anatomies"]) + " |", "|---|" + "---|" * len(out["anatomies"])]
    for key, r in out["rows"].items():
        L.append(f"| {key} | " + " | ".join(f"{_fmt(r['anatomy'][a]['black'])} · {_fmt_ceiling(r['anatomy'][a]['ceiling'])}" for a in out["anatomies"]) + " |")
    L += ["", "## Por anatomia × seed: componentes em preto (Acc com IC 95 % pareado; Δ_nec inalterado ao lado)", "",
          "| checkpoint | anatomia | n | Acc(C0) | Acc(T) | Acc(P) | Acc(S) | Acc(C0) − Acc(P) | Acc(S)/Acc(C0) | Δ_nec |",
          "|---|---|---:|---|---|---|---|---|---|---|"]
    for key, r in out["rows"].items():
        for a in out["anatomies"]:
            comp = r["anatomy"][a].get("components")
            if not comp:
                continue
            L.append(f"| {key} | {a} | {comp['n']} | " + " | ".join(_fmt_acc(comp["acc"][k], comp["acc_ci"].get(k)) for k in ("C0", "T", "P", "S"))
                     + f" | {_fmt_pp(comp['c0_minus_p'], comp['c0_minus_p_ci'])} | {_fmt_ratio(comp['sufficiency'], comp['sufficiency_ci'])} | {_fmt(r['anatomy'][a]['black'])} |")
    L += ["", "## Resumo por família (critério E3 e margem sobre o M0)", "",
          "| família | seeds | fechada-sim: passam / avaliáveis | fechada-não: passam / avaliáveis | sem margem (sim / não) |", "|---|---:|---:|---:|---:|"]
    for fam, f in out["families"].items():
        L.append(f"| {fam} | {f['n_seeds']} | {f['n_pass_e3']['closed_yes']} / {f['n_evaluable']['closed_yes']} | "
                 f"{f['n_pass_e3']['closed_no']} / {f['n_evaluable']['closed_no']} | {f['n_no_margin']['closed_yes']} / {f['n_no_margin']['closed_no']} |")
    L += ["", "Avaliáveis = seeds com ao menos um preenchimento plausível rodado (E3). MedVLThinker (500, sem ajuste fino) fica fora desta tabela."]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results-dir", default="results/isbi_placebo"); ap.add_argument("--docs-dir", default="docs/isbi/placebo")
    a = ap.parse_args(argv)
    out = collect(a.results_dir)
    Path(a.results_dir, "heal_table.json").write_text(json.dumps(out, indent=1) + "\n")
    md = render(out); Path(a.docs_dir, "heal_table.md").write_text(md); print(md)


if __name__ == "__main__":
    main()
