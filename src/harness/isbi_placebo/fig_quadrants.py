"""Central figure, draft (analysis request of 14/09/2026, item 6).

Panel (a): scatter of Δ_nec (x, pp, with horizontal CI bars) against
sufficiency Acc(S)/Acc(C0) (y) per Kvasir template, one marker per class,
dashed lines at x = 0 and y = 0.5; templates without headroom (headroom <= 0) in grey
and without bar. Panel (b): paired bars per class of the drop under T, P and
C4_OCC_75, with CI. Pure Matplotlib, vector fonts (Type 42), IEEE single-column
width (8.6 cm). E3: a template whose Δ_nec excludes zero only under black (field
`e3.solid_only` of the necessity file) gets a hollow marker in the class color and a "†" in the legend.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# Minimum 7 pt font at IEEE column width (8.6 cm); the two stacked panels
# take half a page, the figure budget of the whole paper (authors, 14/09/2026).
matplotlib.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "font.size": 7, "axes.labelsize": 7, "axes.titlesize": 7,
                            "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7, "font.family": "sans-serif"})
CLASS_STYLE = {"dependent_polyp": ("o", "#1f77b4", "pólipo"), "dependent_instrument": ("s", "#d62728", "instrumento"),
               "negative_control": ("^", "#2ca02c", "controle negativo"), "dependent_polyp_secondary": ("D", "#9467bd", "secundária")}
# Two-letter codes on the markers; the legend table beside them translates. "Have all polyps been removed?"
# is marked as secondary: a cover example, never a main result (authors, 14/09/2026).
CODES = {"How many polyps are in the image?": ("NP", "n pólipos"), "What is the size of the polyp?": ("TM", "tam. pólipo"),
         "What type of polyp is present?": ("TP", "tipo pólipo"), "Where in the image is the abnormality?": ("PA", "pos. anorm."),
         "What color is the abnormality? If more than one separate with ;": ("CR", "cor anorm."),
         "Are there any abnormalities in the image? Check all that are present.": ("HA", "há anorm."),
         "How many findings are present?": ("NA", "n achados"), "Have all polyps been removed?": ("RM", "removidos (sec.)"),
         "How many instrumnets are in the image?": ("NI", "n instrum."), "Where in the image is the instrument?": ("PI", "pos. instrum."),
         "Are there any instruments in the image? Check all that are present.": ("HI", "há instrum."),
         "Is there text?": ("TX", "texto"), "Is there a green/black box artefact?": ("CX", "caixa artef."),
         "What type of procedure is the image taken from?": ("PR", "procedimento")}
SHORT = {q: v[0] for q, v in CODES.items()}


def make_figure(necessity: str, inventory: str, out_stem: str) -> list[str]:
    nec = json.loads(Path(necessity).read_text())
    cls_of = {q["question"]: q["question_class"] for q in json.loads(Path(inventory).read_text())["questions"]}
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.6 / 2.54, 12.5 / 2.54), gridspec_kw={"height_ratios": [1.3, 1]})
    seen = set()
    used_codes = []
    any_solid_only = False
    for q, s in nec["by_template"].items():
        if "delta_nec" not in s or s.get("sufficiency") is None:
            continue
        cls = cls_of.get(q, "negative_control"); mk, col, lab = CLASS_STYLE.get(cls, ("o", "k", cls))
        x, y = 100 * s["delta_nec"], s["sufficiency"]
        solid_only = bool((s.get("e3") or {}).get("solid_only"))   # E3: passes only under black -> hollow marker, class colour
        if s.get("no_margin"):
            ax1.scatter(x, y, marker=mk, s=16, facecolor="none", edgecolor="0.6", linewidths=0.8, zorder=3)
        elif solid_only:
            lo, hi = s["delta_nec_ci"]
            ax1.errorbar(x, y, xerr=[[x - 100 * lo], [100 * hi - x]], fmt=mk, ms=4, mfc="white", mec=col, color=col, ecolor=col,
                         elinewidth=0.7, capsize=1.5, ls="none", label=None if lab in seen else lab, zorder=4)
            seen.add(lab)
        else:
            lo, hi = s["delta_nec_ci"]
            ax1.errorbar(x, y, xerr=[[x - 100 * lo], [100 * hi - x]], fmt=mk, ms=4, color=col, ecolor=col, elinewidth=0.7, capsize=1.5,
                         label=None if lab in seen else lab, zorder=4)
            seen.add(lab)
        code = SHORT.get(q, q[:2].upper())
        used_codes.append((code, CODES.get(q, (code, q))[1] + (" *" if s.get("no_margin") else "") + (" †" if solid_only else "")))
        any_solid_only |= solid_only
        ax1.annotate(code, (x, y), fontsize=7, xytext=(3, 3), textcoords="offset points", color="0.2")
    ax1.axvline(0, ls="--", lw=0.7, color="0.5"); ax1.axhline(0.5, ls="--", lw=0.7, color="0.5")
    xmin, xmax = ax1.get_xlim(); ymin, ymax = ax1.get_ylim()
    ax1.set_xlim(min(xmin, -12), max(xmax, 52)); ax1.set_ylim(min(ymin, 0.1), max(ymax, 1.12))
    xmin, xmax = ax1.get_xlim(); ymin, ymax = ax1.get_ylim()
    qlab = dict(fontsize=7, color="0.62", ha="center", va="center", style="italic", zorder=1)
    ax1.text(xmax - 1, ymax - 0.025, "necessária e suficiente", **{**qlab, "ha": "right"})
    ax1.text(xmax - 1, ymin + 0.025, "necessária, não suficiente", **{**qlab, "ha": "right"})
    ax1.text((xmin + 0) / 2, (0.5 + ymax) / 2, "não\nnecessária", **qlab)
    ax1.set_xlabel("Δ_nec = Acc(P) − Acc(T) (pp)"); ax1.set_ylabel("suficiência Acc(S)/Acc(C0)")
    ax1.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.20), ncol=2, handletextpad=0.3, columnspacing=1.0, borderaxespad=0)
    ax1.set_title("(a) por template; * sem margem sobre o M0" + ("; † só sob preto" if any_solid_only else ""), loc="left")
    # legend table of the codes, to the right of panel (a)
    table = "\n".join(f"{c} {name}" for c, name in sorted(set(used_codes)))
    ax1.text(1.03, 1.0, table, transform=ax1.transAxes, fontsize=7, va="top", ha="left", family="monospace", color="0.2", linespacing=1.12)
    conds = [c for c in ("T", "P", "C4_OCC_75") if c in nec["predictions"]]
    classes = [c for c in ("dependent_polyp", "dependent_instrument", "negative_control") if c in nec["by_class"] and "vdd" in nec["by_class"][c]]
    w = 0.8 / max(len(conds), 1)
    for i, c in enumerate(conds):
        xs = [j + (i - (len(conds) - 1) / 2) * w for j in range(len(classes))]
        ys = [100 * nec["by_class"][k]["vdd"][c] for k in classes]
        err = [[100 * (nec["by_class"][k]["vdd"][c] - nec["by_class"][k]["vdd_ci"][c][0]) for k in classes],
               [100 * (nec["by_class"][k]["vdd_ci"][c][1] - nec["by_class"][k]["vdd"][c]) for k in classes]]
        ax2.bar(xs, ys, width=w * 0.95, yerr=err, capsize=1.5, error_kw={"elinewidth": 0.7},
                label={"T": "T (alvo)", "P": "P (placebo)", "C4_OCC_75": "oclusão central 75 %, não específica"}[c],
                color={"T": "#d62728", "P": "#1f77b4", "C4_OCC_75": "0.55"}[c])
    ax2.axhline(0, lw=0.7, color="0.3")
    ax2.set_xticks(range(len(classes)))
    short = {"dependent_polyp": "pólipo", "dependent_instrument": "instrumento", "negative_control": "controle\nnegativo"}
    ax2.set_xticklabels([f"{short.get(k, CLASS_STYLE[k][2])}\n(n = {nec['by_class'][k]['n']})" for k in classes])
    ax2.set_ylabel("queda Acc(C0) − Acc(cond) (pp)"); ax2.legend(frameon=False, loc="upper left")
    ax2.set_title("(b) por classe, com IC 95 %", loc="left")
    fig.subplots_adjust(left=0.15, right=0.67, top=0.96, bottom=0.12, hspace=0.62)
    Path(out_stem).parent.mkdir(parents=True, exist_ok=True)
    paths = [f"{out_stem}.png", f"{out_stem}.pdf"]
    fig.savefig(paths[0], dpi=300); fig.savefig(paths[1]); plt.close(fig)
    return paths


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--necessity", required=True); ap.add_argument("--inventory", required=True); ap.add_argument("--out-stem", required=True)
    a = ap.parse_args(argv)
    print(make_figure(a.necessity, a.inventory, a.out_stem))


if __name__ == "__main__":
    main()
