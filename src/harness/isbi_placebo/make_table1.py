"""Table 1 of the ISBI 2027 paper -- the auditable table: benchmark x family, with the "regime" column.

Reads the same JSON files as the numbers sheet (`necessity_<cell>.json`, `slake_closed_<cell>.json`, `negative_by_template.json`) and
the `collect` functions of the tables (E3 counts). Per family: mean ± sd over the seeds (LoRA and DoRA together in the
family; M3AE on SLAKE = the 3 seeds trained from scratch, the public checkpoint goes in the note). Kvasir in two sub-rows
(polyp, instrument); HEAL = closed-yes; SLAKE = disease on the closed-ended questions (E8). Regime labels v2 (01/10/2026): A necessity /
B no necessity / C no usable headroom, in the order of the Figure 1 panels. Output: docs/isbi/paper/tables/table1_regimes.tex.
Layout adjustments go in the copy at ~/Documents/doutorado/isbi/paper/tables/, never here.

    python -m harness.isbi_placebo.make_table1
"""
from __future__ import annotations

import json
import shutil
import statistics
from pathlib import Path

from harness.isbi_placebo import heal_table, p3_table, slake_table

REPO = Path(__file__).resolve().parents[2]
RES = REPO / "results/isbi_placebo"
OUT = REPO / "docs/isbi/paper/tables/table1_regimes.tex"
COPY_TO = Path.home() / "Documents/doutorado/isbi/paper/tables/table1_regimes.tex"
FAM = [("M3AE", "M3AE"), ("QWEN2VL", "Qwen2-VL"), ("SMOLVLM", "SmolVLM2")]


def _msd(xs, scale=100.0, nd=1, sign=False) -> str:
    m = round(statistics.mean(xs) * scale, nd) + 0.0   # + 0.0 evita "-0.0"
    s = statistics.pstdev(xs) * scale if len(xs) > 1 else 0.0
    return (f"{m:+.{nd}f}" if sign else f"{m:.{nd}f}") + f" $\\pm$ {s:.{nd}f}"


def _cells(prefix: str, keys: list[str]) -> dict[str, dict]:
    return {k: json.loads((RES / f"{prefix}_{k}.json").read_text())["by_class"] for k in keys}


def _row(regime: str, name: str, cells: dict[str, dict], cls: str, e3: tuple[int, int], dagger: bool = False) -> str:
    ss = [c[cls] for c in cells.values()]
    acc = _msd([s["acc"]["C0"] for s in ss]); m0 = f"{100 * ss[0]['acc_m0']:.1f}"
    hr = _msd([s["ceiling"] for s in ss], sign=True)
    if statistics.mean(s["ceiling"] for s in ss) <= 0:
        hr = f"\\textcolor{{red}}{{{hr}}}"
    suf = _msd([s["sufficiency"] for s in ss], scale=1, nd=2)
    db = _msd([s["delta_nec"] for s in ss], sign=True); dbl = _msd([s["delta_nec_blur10"] for s in ss], sign=True)
    return f"{regime} & {name}{'$^{\\dagger}$' if dagger else ''} & {acc} & {m0}{'$^{\\dagger}$' if dagger else ''} & {hr} & {suf} & {db} & {dbl} & {e3[0]}/{e3[1]} \\\\"


def build() -> str:
    p3 = p3_table.collect(str(RES)); he = heal_table.collect(str(RES)); sc = slake_table.collect(str(RES), prefix="slake_closed")
    neg = json.loads((RES / "negative_by_template.json").read_text())["rows"]
    txt = [neg[k]["text"][f] for k in neg for f in ("black", "blur", "blur10") if neg[k]["text"].get(f)]
    n_txt_ok, n_txt = sum(c["within_zero"] for c in txt), len(txt)
    L = ["% Gerado por harness/isbi_placebo/make_table1.py a partir de results/isbi_placebo/*.json — nao editar os numeros a mao.",
         "% Rotulos de regime v2 (01/10/2026, candidato): A necessity / B no necessity / C no usable headroom, na ordem dos paineis da Figura 1.",
         "% Requer \\usepackage{booktabs}, \\usepackage{xcolor} (\\textcolor{red}) e \\usepackage{graphicx} (\\resizebox) no preambulo.",
         "\\begin{table*}[!t]", "\\centering", "\\scriptsize", "\\setlength{\\tabcolsep}{4pt}",
         "\\caption{Three regimes of the same occlusion test. Per benchmark and model family (mean $\\pm$ sd over seeds; LoRA and DoRA pooled for the "
         "generative families), on the class subset of evaluable questions: intact accuracy Acc(C0), question-only floor M0 on the same subset, "
         "headroom Acc(C0) $-$ M0, sufficiency Acc(S)/Acc(C0), $\\Delta_{\\mathrm{nec}}$ = Acc(P) $-$ Acc(T) under the solid black fill and under "
         "Gaussian blur ($\\sigma$ = 10\\,\\% of the image width), and the number of checkpoints meeting criterion E3 (95\\,\\% CI of "
         "$\\Delta_{\\mathrm{nec}}$ above zero under black and under a plausible fill). Kvasir-VQA-x1: polyp and instrument; HEAL-MedVQA: closed "
         "questions with answer yes; SLAKE: disease questions, closed subset.}",
         "\\label{tab:regimes}",
         "\\resizebox{\\textwidth}{!}{%", "\\begin{tabular}{@{}llrrrrrrr@{}}", "\\toprule",
         "Regime & Benchmark $\\cdot$ family & Acc(C0) \\% & M0 \\% & Headroom pp & Acc(S)/Acc(C0) & $\\Delta_{\\mathrm{nec}}$ black & $\\Delta_{\\mathrm{nec}}$ blur 10\\,\\% & E3 yes/total \\\\",
         "\\midrule"]
    kv = sorted(p3["rows"]); hc = sorted(he["rows"]); sl = [k for k in sorted(sc["rows"]) if not k.startswith("M3AE_SLAKE_")]
    for fam, lab in FAM:
        ks = [k for k in kv if k.startswith(fam + "_")]; cells = _cells("necessity", ks)
        e3p = (p3["families"][lab]["n_pass_e3"]["dependent_polyp"], p3["families"][lab]["n_evaluable"]["dependent_polyp"])
        e3i = (p3["families"][lab]["n_pass_e3"]["dependent_instrument"], p3["families"][lab]["n_evaluable"]["dependent_instrument"])
        L.append(_row("A necessity", f"Kvasir $\\cdot$ {lab} $\\cdot$ polyp", cells, "dependent_polyp", e3p))
        L.append(_row("", f"\\quad instrument", cells, "dependent_instrument", e3i, dagger=True))
    L.append("\\midrule")
    for fam, lab in FAM:
        ks = [k for k in hc if k.startswith(fam + "_")]; cells = _cells("necessity", ks)
        e3 = (he["families"][lab]["n_pass_e3"]["closed_yes"], he["families"][lab]["n_evaluable"]["closed_yes"])
        L.append(_row("B no necessity", f"HEAL $\\cdot$ {lab} $\\cdot$ answer yes", cells, "closed_yes", e3))
    L.append("\\midrule")
    for fam, lab in FAM:
        ks = [k for k in sl if k.startswith(fam + "_")]; cells = _cells("slake_closed", ks)
        e3 = (sum(bool(sc["rows"][k]["e3"].get("dependent_disease")) for k in ks), sum(sc["rows"][k]["e3"].get("dependent_disease") is not None for k in ks))
        L.append(_row("C no usable headroom", f"SLAKE $\\cdot$ {lab} $\\cdot$ disease (closed)", cells, "dependent_disease", e3))
    pub = json.loads((RES / "slake_closed_M3AE_SLAKE_seed0.json").read_text())["by_class"]["dependent_disease"]
    L += ["\\bottomrule", "\\end{tabular}}", "\\par\\vspace{2pt}\\raggedright\\scriptsize",
          f"Negative control (Kvasir, ``Is there text?''): {n_txt_ok} of {n_txt} cells with CI including zero. "
          "$^{\\dagger}$ Every evaluable instrument question carries an instrument, so the question-only floor is 0 on this subset and the headroom equals Acc(C0). "
          "Headroom $\\le 0$ in red. SLAKE M3AE rows: the three checkpoints trained from scratch; the authors' public checkpoint gives "
          f"Acc(C0) {100 * pub['acc']['C0']:.1f}, headroom {100 * pub['ceiling']:+.1f} pp, $\\Delta_{{\\mathrm{{nec}}}}$ {100 * pub['delta_nec']:+.1f} on the same subset.",
          "\\end{table*}"]
    return "\n".join(L) + "\n"


def main() -> None:
    tex = build()
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(tex)
    COPY_TO.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(OUT, COPY_TO)
    print(tex)


if __name__ == "__main__":
    main()
