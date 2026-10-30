"""Diagnostic of "Is there a green/black box artefact?" (analysis request of 14/09/2026, item 3).

Δ_nec negative and significant in both seeds: the control occlusion makes the model say "yes"
where C0 said "no". Without changing anything: (a) distribution of the answers under C0, T and P;
(b) for the items that turn "yes" only under P, geometry of the control occlusion (rectangularity =
area / bounding box, minimum distance to the FOV border, fraction outside the FOV,
centroid position, placement family: mirror, rotation, translation);
(c) the same geometry for those that did not turn. Reads the geometry from
results/isbi_placebo/placebo_geometry_<dataset>.json (computed once where the
masks are). Automatic one-sentence conclusion comparing medians; no
amendment proposal.
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

import numpy as np

from med_vlm.metrics.process_text import normalize_text

Q_GREENBOX = "Is there a green/black box artefact?"
_FIELDS = ("rectangularity", "min_dist_to_fov_border_px", "frac_outside_fov", "area_px")


def _dist(values: list[float]) -> dict:
    a = np.asarray(values, float)
    if a.size == 0:
        return {"n": 0}
    return {"n": int(a.size), "median": float(np.median(a)), "q1": float(np.quantile(a, .25)), "q3": float(np.quantile(a, .75)),
            "min": float(a.min()), "max": float(a.max())}


def _group(units: list[dict]) -> dict:
    geo = {f: _dist([u["placebo"][f] for u in units]) for f in _FIELDS}
    geo["centroid_x_frac"] = _dist([u["placebo"]["centroid"][1] / u["width"] for u in units])
    geo["centroid_y_frac"] = _dist([u["placebo"]["centroid"][0] / u["height"] for u in units])
    return {"n": len(units), "families": dict(collections.Counter(u["placement_family"] for u in units)), "geometry": geo,
            "image_ids": [u["image_id"] for u in units]}


def diag_greenbox(inventory: str, geometry: str, preds: dict[str, str]) -> dict:
    inv = [q for q in json.loads(Path(inventory).read_text())["questions"] if q["evaluable"] and q["question"] == Q_GREENBOX]
    geo = {u["image_id"]: u for u in json.loads(Path(geometry).read_text())["units"]}
    loaded = {c: {r["qid"]: r for r in json.loads(Path(p).read_text())["predictions"]} for c, p in preds.items()}
    qs = [q for q in inv if all(q["qid"] in d for d in loaded.values()) and q["image_id"] in geo]
    answers = {c: dict(collections.Counter(normalize_text(d[q["qid"]]["predicted"]) for q in qs)) for c, d in loaded.items()}
    def is_yes(c, q):
        return normalize_text(loaded[c][q["qid"]]["predicted"]) == "yes"
    flipped = [q for q in qs if is_yes("P", q) and not is_yes("C0", q) and not is_yes("T", q)]
    not_flipped = [q for q in qs if q not in flipped]
    out = {"template": Q_GREENBOX, "n": len(qs), "predictions": preds, "geometry_file": geometry, "answers": answers,
           "acc": {c: sum(bool(d[q["qid"]]["correct"]) for q in qs) / len(qs) if qs else None for c, d in loaded.items()},
           "flipped_yes_only_under_P": _group([geo[q["image_id"]] for q in flipped]),
           "not_flipped": _group([geo[q["image_id"]] for q in not_flipped])}
    f, nf = out["flipped_yes_only_under_P"]["geometry"], out["not_flipped"]["geometry"]
    if out["flipped_yes_only_under_P"]["n"] and out["not_flipped"]["n"]:
        out["conclusion"] = (
            f"Nos {out['flipped_yes_only_under_P']['n']} itens que viram \"yes\" só sob P, o placebo tem retangularidade mediana "
            f"{f['rectangularity']['median']:.2f} (contra {nf['rectangularity']['median']:.2f} nos {out['not_flipped']['n']} que não viraram), "
            f"distância mediana à borda do FOV {f['min_dist_to_fov_border_px']['median']:.0f} px (contra {nf['min_dist_to_fov_border_px']['median']:.0f}), "
            f"centroide em x = {f['centroid_x_frac']['median']:.2f} da largura (contra {nf['centroid_x_frac']['median']:.2f}) e famílias "
            + ", ".join(f"{k}={v}" for k, v in out["flipped_yes_only_under_P"]["families"].items()) + ".")
    else:
        out["conclusion"] = "Sem itens em um dos grupos; nada a comparar."
    return out


def render(out: dict) -> str:
    L = [f"# Diagnóstico — {out['template']} ({Path(out['predictions']['P']).stem})", "",
         f"n = {out['n']}; acurácia: " + ", ".join(f"{c} {100 * a:.1f} %" for c, a in out["acc"].items()) + ".", "",
         "## (a) Respostas sob cada condição", "", "| condição | " + " | ".join(sorted({k for a in out["answers"].values() for k in a})) + " |"]
    keys = sorted({k for a in out["answers"].values() for k in a})
    L.append("|---|" + "---:|" * len(keys))
    L += [f"| {c} | " + " | ".join(str(a.get(k, 0)) for k in keys) + " |" for c, a in out["answers"].items()]
    L += ["", "## (b) e (c) Geometria do placebo: viraram \"yes\" só sob P × não viraram", "",
          "| medida | viraram (n=%d) mediana [Q1, Q3] | não viraram (n=%d) mediana [Q1, Q3] |" % (out["flipped_yes_only_under_P"]["n"], out["not_flipped"]["n"]),
          "|---|---|---|"]
    labels = {"rectangularity": "retangularidade (área / caixa)", "min_dist_to_fov_border_px": "distância mín. à borda do FOV (px)",
              "frac_outside_fov": "fração fora do FOV", "area_px": "área (px)", "centroid_x_frac": "centroide x (fração da largura)",
              "centroid_y_frac": "centroide y (fração da altura)"}
    f, nf = out["flipped_yes_only_under_P"]["geometry"], out["not_flipped"]["geometry"]
    def cell(d):
        return f"{d['median']:.2f} [{d['q1']:.2f}, {d['q3']:.2f}]" if d.get("n") else "—"
    L += [f"| {labels[k]} | {cell(f[k])} | {cell(nf[k])} |" for k in labels]
    L += ["", "| família de colocação | viraram | não viraram |", "|---|---:|---:|"]
    fam = sorted(set(out["flipped_yes_only_under_P"]["families"]) | set(out["not_flipped"]["families"]))
    L += [f"| {k} | {out['flipped_yes_only_under_P']['families'].get(k, 0)} | {out['not_flipped']['families'].get(k, 0)} |" for k in fam]
    L += ["", "**Conclusão.** " + out["conclusion"]]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inventory", required=True); ap.add_argument("--geometry", required=True); ap.add_argument("--pred", action="append", required=True)
    ap.add_argument("--output-json", required=True); ap.add_argument("--output-md")
    a = ap.parse_args(argv)
    out = diag_greenbox(a.inventory, a.geometry, dict(kv.split("=", 1) for kv in a.pred))
    Path(a.output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(a.output_json).write_text(json.dumps(out, indent=1) + "\n")
    md = render(out)
    if a.output_md:
        Path(a.output_md).write_text(md)
    print(md)


if __name__ == "__main__":
    main()
