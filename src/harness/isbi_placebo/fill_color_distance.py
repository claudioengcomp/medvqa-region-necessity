"""EXPLORATORY (item 5, 14/09/2026, authors; not in the main table). For each
fill, mean color distance between the filled region (T_<fill>) and the original
region (C0), per item, aggregated per fill: ΔE (CIE76, Lab) and L2 in RGB. The region
of each image is the set of pixels the black fill changes (T != C0). One
plot: x = color distance of the fill, y = Δ_nec (300-item ablation, per class),
one point per fill × family.

    python -m harness.isbi_placebo.fill_color_distance --arrow-dir data/isbi_placebo         --results-dir results/isbi_placebo --docs-dir docs/isbi/placebo
"""
from __future__ import annotations

import argparse
import io
import json
from pathlib import Path

import numpy as np
from PIL import Image

FILL_ARROWS = {"black": "T", "mean": "T_mean", "blur": "T_blur", "blur1pct": "T_blur1_fill300", "blur3pct": "T_blur3_fill300",
               "blur10pct": "T_blur10", "regmean": "T_regmean", "ringmean": "T_ringmean_fill300"}
LABELS = {"black": "preto", "mean": "média imagem", "blur": "blur 4 %", "blur1pct": "blur 1 %", "blur3pct": "blur 3 %",
          "blur10pct": "blur 10 %", "regmean": "cor média região", "ringmean": "anel 15 px"}
FAMILY = {"QWEN2VL": "Qwen2-VL", "SMOLVLM": "SmolVLM2", "M3AE": "M3AE"}


def rgb_to_lab(rgb: np.ndarray) -> np.ndarray:
    """sRGB uint8 (N,3) -> CIE Lab (N,3), D65, CIE76."""
    c = rgb.astype(np.float64) / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16.0 / 116.0)
    return np.stack([116.0 * f[:, 1] - 16.0, 500.0 * (f[:, 0] - f[:, 1]), 200.0 * (f[:, 1] - f[:, 2])], axis=1)


def _decode(b: bytes) -> np.ndarray:
    return np.asarray(Image.open(io.BytesIO(b)).convert("RGB"), np.uint8)


def color_distances(arrow_dir: str, image_ids: set[str] | None = None) -> dict:
    from harness.interventions.arrow_io import read_arrow
    c0 = read_arrow(str(Path(arrow_dir, "vqa_kvasir_placebo_C0.arrow")))
    black = read_arrow(str(Path(arrow_dir, "vqa_kvasir_placebo_T.arrow")))
    c0_by = dict(zip(c0.image_id, c0.image)); bk_by = dict(zip(black.image_id, black.image))
    ids = [i for i in bk_by if i in c0_by and (image_ids is None or i in image_ids)]
    regions, orig = {}, {}
    for i in ids:
        a, b = _decode(c0_by[i]), _decode(bk_by[i])
        reg = np.any(a != b, axis=-1)
        if reg.sum() == 0:
            continue
        regions[i] = reg; orig[i] = a
    out = {"n_images_reference": len(regions), "fills": {}}
    for fill, cond in FILL_ARROWS.items():
        p = Path(arrow_dir, f"vqa_kvasir_placebo_{cond}.arrow")
        if not p.is_file():
            out["fills"][fill] = {"status": "pendente", "arrow": p.name}; continue
        df = read_arrow(str(p)); by = dict(zip(df.image_id, df.image))
        de, l2, n = [], [], 0
        for i, reg in regions.items():
            if i not in by:
                continue
            img = _decode(by[i])
            if img.shape != orig[i].shape:
                continue
            a = orig[i][reg].reshape(-1, 3); b = img[reg].reshape(-1, 3)
            de.append(float(np.linalg.norm(rgb_to_lab(a) - rgb_to_lab(b), axis=1).mean()))
            l2.append(float(np.linalg.norm(a.astype(np.float64) - b.astype(np.float64), axis=1).mean())); n += 1
        out["fills"][fill] = {"status": "ok", "arrow": p.name, "n_images": n, "delta_e_mean": float(np.mean(de)) if de else None,
                              "delta_e_median": float(np.median(de)) if de else None, "l2_rgb_mean": float(np.mean(l2)) if l2 else None}
    return out


def _delta_nec_by_family(results_dir: str) -> dict:
    """Δ_nec per fill × family, from the 300-item ablation (fill_ablation_<ckpt>.json, seed 0 of each family)."""
    out = {}
    for p in sorted(Path(results_dir).glob("fill_ablation_*_KVASIR_seed0.json")):
        fa = json.loads(p.read_text()); model = p.stem.replace("fill_ablation_", "").split("_")[0]
        fam = FAMILY.get(model, model)
        out[fam] = {f: {cls: {"delta": d["by_class"][cls]["delta_nec"], "ci": d["by_class"][cls]["delta_nec_ci"], "n": d["by_class"][cls]["n"]}
                        for cls in ("dependent_polyp", "dependent_instrument") if cls in d["by_class"]}
                    for f, d in fa["fills"].items() if d.get("status") == "ok"}
    return out


def make_figure(dist: dict, dnec: dict, out_stem: str) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "font.size": 7})
    fig, axes = plt.subplots(1, 2, figsize=(17.2 / 2.54, 6.5 / 2.54), sharex=True)
    markers = {"Qwen2-VL": "o", "SmolVLM2": "s", "M3AE": "^"}
    for ax, (cls, title) in zip(axes, [("dependent_polyp", "pólipo (n = 133)"), ("dependent_instrument", "instrumento (n = 45)")]):
        for fam, fills in dnec.items():
            xs, ys, lo, hi, labs = [], [], [], [], []
            for f, v in fills.items():
                d = dist["fills"].get(f)
                if not d or d.get("status") != "ok" or cls not in v:
                    continue
                xs.append(d["delta_e_mean"]); ys.append(100 * v[cls]["delta"]); lo.append(100 * (v[cls]["delta"] - v[cls]["ci"][0]))
                hi.append(100 * (v[cls]["ci"][1] - v[cls]["delta"])); labs.append(LABELS.get(f, f))
            if xs:
                ax.errorbar(xs, ys, yerr=[lo, hi], fmt=markers.get(fam, "o"), ms=4, capsize=1.5, elinewidth=0.6, label=fam, ls="none")
                for x, y, l in zip(xs, ys, labs):
                    ax.annotate(l, (x, y), fontsize=5.5, xytext=(2, 2), textcoords="offset points", color="0.3")
        ax.axhline(0, ls="--", lw=0.6, color="0.5"); ax.set_title(title, loc="left"); ax.set_xlabel("ΔE médio (CIE76) região preenchida × original")
    axes[0].set_ylabel("Δ_nec (pp), 300 estratificadas"); axes[0].legend(frameon=False)
    fig.suptitle("EXPLORATÓRIO — distância de cor do preenchimento × necessidade", fontsize=7, x=0.01, ha="left")
    fig.tight_layout()
    Path(out_stem).parent.mkdir(parents=True, exist_ok=True)
    paths = [f"{out_stem}.png", f"{out_stem}.pdf"]; fig.savefig(paths[0], dpi=300); fig.savefig(paths[1]); plt.close(fig)
    return paths


def render(dist: dict, dnec: dict) -> str:
    L = ["# EXPLORATÓRIO — distância de cor do preenchimento × Δ_nec", "",
         "Não entra na tabela principal. Região = pixels alterados pelo preenchimento preto; ΔE = CIE76 em Lab, média por item, "
         f"agregada por preenchimento ({dist['n_images_reference']} imagens de referência). Δ_nec da ablação de 300 (seed 0 de cada família).", "",
         "| preenchimento | n imagens | ΔE médio | ΔE mediano | L2 RGB médio |", "|---|---:|---:|---:|---:|"]
    for f, d in dist["fills"].items():
        if d.get("status") != "ok":
            L.append(f"| {LABELS.get(f, f)} | pendente ({d['arrow']}) | | | |"); continue
        L.append(f"| {LABELS.get(f, f)} | {d['n_images']} | {d['delta_e_mean']:.1f} | {d['delta_e_median']:.1f} | {d['l2_rgb_mean']:.1f} |")
    L += ["", "| família | preenchimento | Δ_nec pólipo | Δ_nec instrumento |", "|---|---|---:|---:|"]
    for fam, fills in dnec.items():
        for f, v in fills.items():
            g = lambda c: f"{100 * v[c]['delta']:+.1f} [{100 * v[c]['ci'][0]:+.1f}, {100 * v[c]['ci'][1]:+.1f}]" if c in v else "—"
            L.append(f"| {fam} | {LABELS.get(f, f)} | {g('dependent_polyp')} | {g('dependent_instrument')} |")
    L += ["", "Figura: `figs/fig_fill_color_distance.{png,pdf}` (x = ΔE, y = Δ_nec, um ponto por preenchimento × família)."]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arrow-dir", default="data/isbi_placebo"); ap.add_argument("--results-dir", default="results/isbi_placebo")
    ap.add_argument("--docs-dir", default="docs/isbi/placebo")
    ap.add_argument("--reference-arrow", default="vqa_kvasir_placebo_T_ringmean_fill300.arrow",
                    help="arrow das 300 estratificadas cujas imagens definem o conjunto de referencia (comparavel entre preenchimentos)")
    a = ap.parse_args(argv)
    ids = None
    ref = Path(a.arrow_dir, a.reference_arrow)
    if ref.is_file():
        from harness.interventions.arrow_io import read_arrow
        ids = set(read_arrow(str(ref)).image_id)
    dist = color_distances(a.arrow_dir, ids)
    dnec = _delta_nec_by_family(a.results_dir)
    Path(a.results_dir, "fill_color_distance.json").write_text(json.dumps({"distances": dist, "delta_nec": dnec}, indent=1) + "\n")
    make_figure(dist, dnec, str(Path(a.docs_dir, "figs", "fig_fill_color_distance")))
    md = render(dist, dnec); Path(a.docs_dir, "fill_color_distance.md").write_text(md); print(md)


if __name__ == "__main__":
    main()
