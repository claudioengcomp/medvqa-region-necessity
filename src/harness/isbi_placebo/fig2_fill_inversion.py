"""Figure 2 (optional) of the ISBI 2027 paper -- sign inversion under solid fill (claim C4).

x = fill (black, region mean color, blur 4 %, blur 10 %); y = Δ_nec in pp. Two series over the 15
Kvasir cells: the template "Is there a green/black box artefact?" (negative control; drops to −6…−13 under
black and goes to ≈ 0 under blur) and the instrument class (dependent; positive in all). Reads only
`necessity_<cell>.json` (`by_template` and `by_class`). Plan, Task 7; does not go into main.tex until Task 17.
Output: docs/isbi/paper/figs/fig2_fill_inversion.{pdf,png} (column width).

    $HOME/Documents/doutorado/rescoring/.venv312/bin/python -m harness.isbi_placebo.fig2_fill_inversion
"""
from __future__ import annotations
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable

import json
import shutil
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from harness.isbi_placebo import p3_table  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
RES = REPO / "results/isbi_placebo"
OUT = REPO / "docs/isbi/paper/figs"
COPY_TO = Path.home() / "Documents/doutorado/isbi/paper/figs"
plt.rcParams.update({"font.size": 7.5, "font.family": "serif", "pdf.fonttype": 42})
BOX = "Is there a green/black box artefact?"
FILLS = [("black", "solid black"), ("regmean", "region mean"), ("blur", "blur 4 %"), ("blur10", "blur 10 %")]
SERIES = [("by_template", BOX, "artefact-box template (negative control)", "#d62728", "s"),
          ("by_class", "dependent_instrument", "instrument class (dependent)", "#08306b", "o")]


def _delta(s: dict, fill: str):
    k = "delta_nec" if fill == "black" else f"delta_nec_{fill}"
    return s.get(k)


def main() -> None:
    cells = sorted(p3_table.collect(str(RES))["rows"])
    nec = {k: json.loads((RES / f"necessity_{k}.json").read_text()) for k in cells}
    fig, ax = plt.subplots(figsize=(3.3, 1.8))
    rng = np.random.default_rng(0)
    x = np.arange(len(FILLS))
    for si, (group, key, label, colour, marker) in enumerate(SERIES):
        vals = [[100 * _delta(nec[k][group][key], f) for k in cells if _delta(nec[k][group][key], f) is not None] for f, _ in FILLS]
        med = [statistics.median(v) for v in vals]
        q1 = [float(np.percentile(v, 25)) for v in vals]; q3 = [float(np.percentile(v, 75)) for v in vals]
        off = -0.12 if si == 0 else 0.12
        ax.fill_between(x + off, q1, q3, color=colour, alpha=0.15, lw=0)
        for xi, v in zip(x + off, vals):
            ax.plot(xi + rng.uniform(-0.05, 0.05, len(v)), v, marker=marker, ms=2, mfc=colour, mec="none", ls="none", alpha=0.45, zorder=2)
        ax.plot(x + off, med, marker=marker, ms=4, color=colour, lw=1.0, mec="k", mew=0.4, label=label, zorder=3)
    ax.axhline(0, color="k", lw=0.8, zorder=1)
    ax.set_xticks(x); ax.set_xticklabels([l for _, l in FILLS], fontsize=7)
    ax.set_ylabel("$\\Delta_{\\mathrm{nec}}$ (pp)", fontsize=7.5)
    ax.set_xlabel("fill of the occluded region", fontsize=7.5)
    ax.tick_params(axis="both", labelsize=7, length=2, pad=1)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper left", fontsize=6, frameon=False, handlelength=1.2)
    ax.text(0.99, 0.02, f"15 Kvasir checkpoints; median, IQR band", transform=ax.transAxes, ha="right", va="bottom", fontsize=5.8, color="0.3")
    OUT.mkdir(parents=True, exist_ok=True)
    for ext, kw in (("pdf", {}), ("png", {"dpi": 300})):
        fig.savefig(OUT / f"fig2_fill_inversion.{ext}", bbox_inches="tight", pad_inches=0.02, **kw)
    COPY_TO.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        shutil.copy2(OUT / f"fig2_fill_inversion.{ext}", COPY_TO / f"fig2_fill_inversion.{ext}")
    print(f"{OUT}/fig2_fill_inversion.pdf; cells {len(cells)}")


if __name__ == "__main__":
    main()
