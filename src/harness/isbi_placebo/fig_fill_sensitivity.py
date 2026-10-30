"""Fill sensitivity figure (authors' request, 14/09/2026).

Δ_nec under black (x) versus Δ_nec under blur (y), one point per template x
configuration (every necessity_<cfg>_KVASIR_seed<N>.json that has both
measures), marker per class, with the diagonal y = x. Templates below the
diagonal are the ones blur "erases": either black measures shock or blur retains
low-frequency information -- the sigma ablation separates the two readings.
IEEE single-column width (8.6 cm), font >= 7 pt.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from harness.isbi_placebo.fig_quadrants import CLASS_STYLE, SHORT  # noqa: E402

matplotlib.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "font.size": 7, "axes.labelsize": 7, "axes.titlesize": 7,
                            "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7})
_RE = re.compile(r"^necessity_(?P<cfg>[A-Z0-9]+(?:_[A-Z0-9]+)?)_KVASIR_seed(?P<seed>\d)\.json$")


def collect_points(results_dir: str, inventory: str) -> list[dict]:
    cls_of = {q["question"]: q["question_class"] for q in json.loads(Path(inventory).read_text())["questions"]}
    pts = []
    for p in sorted(Path(results_dir).glob("necessity_*_KVASIR_seed*.json")):
        m = _RE.match(p.name)
        if not m:
            continue
        nec = json.loads(p.read_text())
        for q, s in nec.get("by_template", {}).items():
            if "delta_nec" in s and "delta_nec_blur" in s:
                pts.append({"checkpoint": f"{m['cfg']}_KVASIR_seed{m['seed']}", "config": m["cfg"], "seed": int(m["seed"]), "question": q,
                            "question_class": cls_of.get(q, "?"), "black": s["delta_nec"], "black_ci": s["delta_nec_ci"],
                            "blur": s["delta_nec_blur"], "blur_ci": s["delta_nec_blur_ci"], "below_diagonal": s["delta_nec_blur"] < s["delta_nec"]})
    return pts


def make_figure(results_dir: str, inventory: str, out_stem: str) -> list[str]:
    pts = collect_points(results_dir, inventory)
    fig, ax = plt.subplots(figsize=(8.6 / 2.54, 8.0 / 2.54))
    seen = set()
    for pt in pts:
        mk, col, lab = CLASS_STYLE.get(pt["question_class"], ("o", "k", pt["question_class"]))
        alpha = 0.9 if pt["config"].startswith("QWEN2VL_LORA") else 0.55
        ax.scatter(100 * pt["black"], 100 * pt["blur"], marker=mk, s=14, color=col, alpha=alpha, linewidths=0,
                   label=None if lab in seen else lab, zorder=3)
        seen.add(lab)
    lo = min([100 * p["black"] for p in pts] + [100 * p["blur"] for p in pts] + [-12]); hi = max([100 * p["black"] for p in pts] + [100 * p["blur"] for p in pts] + [50])
    ax.plot([lo, hi], [lo, hi], ls="--", lw=0.7, color="0.5", zorder=1)
    ax.axhline(0, lw=0.5, color="0.7"); ax.axvline(0, lw=0.5, color="0.7")
    ax.set_xlabel("Δ_nec com preenchimento preto (pp)"); ax.set_ylabel("Δ_nec com blur (pp)")
    ax.set_title("(c) sensibilidade ao preenchimento (template × config × seed)", loc="left")
    ax.text(hi - 1, lo + 1, "abaixo da diagonal:\no blur \"apaga\" o efeito", ha="right", va="bottom", fontsize=7, color="0.5", style="italic")
    ax.legend(frameon=False, loc="upper left")
    fig.subplots_adjust(left=0.16, right=0.98, top=0.92, bottom=0.14)
    Path(out_stem).parent.mkdir(parents=True, exist_ok=True)
    paths = [f"{out_stem}.png", f"{out_stem}.pdf"]
    fig.savefig(paths[0], dpi=300); fig.savefig(paths[1]); plt.close(fig)
    return paths


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results-dir", default="results/isbi_placebo"); ap.add_argument("--inventory", default="results/isbi_placebo/inventory_kvasir_test_clean.json")
    ap.add_argument("--out-stem", default="docs/isbi/placebo/figs/fig_fill_sensitivity_kvasir")
    a = ap.parse_args(argv)
    print(make_figure(a.results_dir, a.inventory, a.out_stem))


if __name__ == "__main__":
    main()
