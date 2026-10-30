"""Figure 1 of the ISBI 2027 paper -- the three regimes, one panel per benchmark (Kvasir | HEAL | SLAKE), same x scale.

Reads ONLY `necessity_<cell>.json` (Kvasir, HEAL), `slake_closed_<cell>.json` (SLAKE, E8) and the `collect` functions of the
tables (E3 counts for the regime label). Each row = checkpoint x class, grouped by family and, within
it, by class. Grey band from 0 to the headroom Acc(C0) − M0; if headroom <= 0, red hatching from the headroom to 0 (and a
red tick at 0 when the headroom is exactly 0). Hollow marker = Δ_nec under black with 95 % CI; filled = under
blur 10 % of the width. Plan, Task 5. Output: docs/isbi/paper/figs/fig1_regimes.{pdf,png}.

    $HOME/Documents/doutorado/rescoring/.venv312/bin/python -m harness.isbi_placebo.fig1_regimes
"""
from __future__ import annotations
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable

import json
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

from harness.isbi_placebo import heal_table, p3_table, slake_table  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
RES = REPO / "results/isbi_placebo"
OUT = REPO / "docs/isbi/paper/figs"
COPY_TO = Path.home() / "Documents/doutorado/isbi/paper/figs"
plt.rcParams.update({"font.size": 7.5, "font.family": "serif", "pdf.fonttype": 42})

FAM_ORDER = ["M3AE", "QWEN2VL", "SMOLVLM"]
FAM_LABEL = {"M3AE": "M3AE", "QWEN2VL": "Qwen2-VL", "SMOLVLM": "SmolVLM2"}
DARK, LIGHT, RED, GREY = "#08306b", "#6baed6", "#d62728", "#d9d9d9"
XMIN, XMAX = -15, 45


def _rows(cells: list[str], prefix: str, classes: list[tuple[str, str]]) -> list[dict | None]:
    """Rows from bottom to top: family -> class -> cell; `None` = gap between families."""
    rows: list[dict | None] = []
    for fam in FAM_ORDER:
        ks = [k for k in cells if k.split("_")[0] == fam]
        if rows:
            rows.append(None)
        for ci_, (cls, lab) in enumerate(classes):
            for k in ks:
                s = json.loads((RES / f"{prefix}_{k}.json").read_text())["by_class"][cls]
                rows.append({"family": fam, "cls": cls, "label": lab, "colour": DARK if ci_ == 0 else LIGHT, "cell": k,
                             "black": (s["delta_nec"], s["delta_nec_ci"]), "blur10": (s.get("delta_nec_blur10"), s.get("delta_nec_blur10_ci")),
                             "ceiling": s.get("ceiling")})
    return rows


def _panel(ax, rows: list[dict | None], title: str, regime: str) -> None:
    y = 0
    fam_span: dict[str, list[int]] = {}
    for r in rows:
        if r is None:
            y += 1
            continue
        fam_span.setdefault(r["family"], [y, y])[1] = y
        c = r["ceiling"]
        if c is not None:
            if c > 0:
                ax.barh(y, 100 * c, left=0, height=0.9, color=GREY, lw=0, zorder=0)
            else:
                ax.barh(y, 100 * c, left=0, height=0.9, facecolor="none", edgecolor=RED, hatch="//////", lw=0, zorder=0)
                ax.plot([0, 0], [y - 0.45, y + 0.45], color=RED, lw=1.2, zorder=1)
        for key, dy, mfc in (("black", +0.2, "white"), ("blur10", -0.2, r["colour"])):
            d, ci = r[key]
            if d is None:
                continue
            lo, hi = 100 * ci[0], 100 * ci[1]
            ax.plot([max(lo, XMIN), min(hi, XMAX)], [y + dy, y + dy], color=r["colour"], lw=0.6, zorder=2, solid_capstyle="butt")
            if hi > XMAX:
                ax.annotate("", xy=(XMAX, y + dy), xytext=(XMAX - 2.5, y + dy), arrowprops=dict(arrowstyle="->", color=r["colour"], lw=0.6), zorder=3)
            ax.plot(min(100 * d, XMAX - 0.5), y + dy, marker="o", ms=2.4, mfc=mfc, mec=r["colour"], mew=0.7, ls="none", zorder=4)
        y += 1
    ax.axvline(0, color="k", lw=1.0, zorder=1)
    ax.set_xlim(XMIN, XMAX)
    ax.set_ylim(-0.7, y + 2.6)   # 2.6 rows of slack for the regime label
    ax.set_yticks([])
    for fam, (a, b) in fam_span.items():
        ax.text(XMIN + 0.8, (a + b) / 2, FAM_LABEL[fam], rotation=90, ha="left", va="center", fontsize=6.5, color="0.25")
    ax.set_title(title, fontsize=8, pad=2, loc="left")
    ax.text(0.99, 0.985, regime, transform=ax.transAxes, ha="right", va="top", fontsize=7, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="0.7", lw=0.5))
    ax.tick_params(axis="x", labelsize=7, length=2, pad=1)
    ax.spines[["top", "right"]].set_visible(False)


def main() -> None:
    p3 = p3_table.collect(str(RES)); he = heal_table.collect(str(RES)); sc = slake_table.collect(str(RES), prefix="slake_closed")
    kv_cells, he_cells, sl_cells = sorted(p3["rows"]), sorted(he["rows"]), sorted(sc["rows"])
    kv_yes = sum(all(p3["rows"][k]["e3"].get(c) for c in ("dependent_polyp", "dependent_instrument")) for k in kv_cells)
    he_yes = sum(any(he["rows"][k]["e3"].get(c) for c in ("closed_yes", "closed_no")) for k in he_cells)
    sl_yes = sum(bool(sc["rows"][k]["e3"].get("dependent_disease")) for k in sl_cells)
    sl_nomargin = sum(1 for k in sl_cells if (sc["rows"][k]["ceiling"].get("dependent_disease") or {}).get("no_margin"))
    panels = [
        (_rows(kv_cells, "necessity", [("dependent_polyp", "polyp"), ("dependent_instrument", "instrument†")]), "Kvasir-VQA-x1", f"A. necessity ({kv_yes}/{len(kv_cells)})"),
        (_rows(he_cells, "necessity", [("closed_yes", "closed, answer yes"), ("closed_no", "closed, answer no")]), "HEAL-MedVQA", f"B. no necessity ({he_yes}/{len(he_cells)})"),
        (_rows(sl_cells, "slake_closed", [("dependent_disease", "disease"), ("dependent_organ", "organ")]), "SLAKE, closed questions", f"C. no usable headroom ({sl_yes}/{len(sl_cells)})"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.7), sharex=True, gridspec_kw=dict(wspace=0.08, left=0.012, right=0.995, top=0.84, bottom=0.17))
    for ax, (rows, title, regime) in zip(axes, panels):
        _panel(ax, rows, title, regime)
    fig.text(0.5, 0.045, "$\\Delta_{\\mathrm{nec}}$ = Acc(P) − Acc(T), percentage points (95 % CI)", ha="center", va="bottom", fontsize=7.5)
    handles = [Line2D([], [], marker="o", mfc="white", mec="k", mew=0.7, ms=3, ls="none", label="hollow: solid black fill"),
               Line2D([], [], marker="o", mfc="k", mec="k", ms=3, ls="none", label="filled: Gaussian blur, σ = 10 % of width"),
               Patch(fc=GREY, label="grey band: headroom Acc(C0) − M0"),
               Patch(fc="none", ec=RED, hatch="//////", label="red: no headroom (Acc(C0) ≤ M0)"),
               Patch(fc=DARK, label="dark: polyp / answer yes / disease"), Patch(fc=LIGHT, label="light: instrument / answer no / organ")]
    fig.legend(handles=handles, loc="upper center", ncol=3, frameon=False, fontsize=6.5, handlelength=1.4, columnspacing=1.2, bbox_to_anchor=(0.5, 1.0), handletextpad=0.5)
    fig.text(0.995, 0.0, "† every evaluable instrument question carries an instrument: the question-only floor is 0 there and the band equals Acc(C0)", ha="right", va="bottom", fontsize=5.8, color="0.3")
    OUT.mkdir(parents=True, exist_ok=True)
    for ext, kw in (("pdf", {}), ("png", {"dpi": 300})):
        fig.savefig(OUT / f"fig1_regimes.{ext}", bbox_inches="tight", pad_inches=0.02, **kw)
    COPY_TO.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        shutil.copy2(OUT / f"fig1_regimes.{ext}", COPY_TO / f"fig1_regimes.{ext}")
    print(f"{OUT}/fig1_regimes.pdf  rows: {[sum(r is not None for r in p[0]) for p in panels]}  labels: {[p[2] for p in panels]}  (SLAKE: headroom <= 0 in {sl_nomargin}/{len(sl_cells)})")


if __name__ == "__main__":
    main()
