"""Geometry of the target and control occlusions (`placebo` in the code) per unit, for the diagnostics (item 3).

Runs where the masks are (lab server), reads the manifest and the inventory, rebuilds the target and the
control occlusion exactly as the generator does, and writes one small JSON per dataset: per unit, placement
method, area, rectangularity (area / area of the bounding box), centroid, box, minimum distance to the FOV
border and fraction outside the FOV, for target and control. Does not touch arrows or results.

Usage (lab server):
    python -m harness.isbi_placebo.placebo_geometry --dataset kvasir         --arrow .../vqa_kvasir_test_clean.arrow --manifest results/isbi_placebo/manifest_kvasir.json         --map data/isbi_placebo/kvasir_vqa_to_seg_instrument_map.json --seg-dir ... --instrument-dir ...         --output results/isbi_placebo/placebo_geometry_kvasir.json
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

from harness.interventions.arrow_io import read_arrow
from harness.isbi_placebo.conditions import apply_placement
from harness.isbi_placebo.inventory_kvasir import load_target_mask
from harness.isbi_placebo.inventory_slake import entity_regions, fov_for_modality, read_legend
from harness.isbi_placebo.masks import fov_mask


def mask_geometry(mask: np.ndarray, fov: np.ndarray) -> dict:
    mask = np.asarray(mask, bool); fov = np.asarray(fov, bool)
    ys, xs = np.nonzero(mask)
    area = int(mask.sum())
    if area == 0:
        return {"area_px": 0}
    y0, y1, x0, x1 = int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max())
    bbox_area = (y1 - y0 + 1) * (x1 - x0 + 1)
    # distance from each FOV pixel to the FOV border (0 outside the FOV)
    dist = ndimage.distance_transform_edt(fov)
    return {"area_px": area, "rectangularity": area / bbox_area, "bbox": [y0, x0, y1, x1],
            "centroid": [float(ys.mean()), float(xs.mean())],
            "min_dist_to_fov_border_px": float(dist[mask].min()),
            "frac_outside_fov": float((mask & ~fov).sum() / area)}


def build(dataset: str, arrow: str, manifest: str, inventory: str, src: dict) -> dict:
    man = json.loads(Path(manifest).read_text())
    df = read_arrow(arrow)
    units = []
    if dataset == "kvasir":
        mapping = json.loads(Path(src["map"]).read_text())
        fov_opening = json.loads(Path(inventory).read_text())["params"].get("fov_opening", 0)
    else:
        legend = read_legend(os.path.join(src["slake_root"], "mask.txt"))
        inv_imgs = {i["image_id"]: i for i in json.loads(Path(inventory).read_text())["images"]}
    for u in man["units"]:
        row = df.iloc[u["row"]]
        img = np.array(Image.open(io.BytesIO(row.image)).convert("RGB"))
        if dataset == "kvasir":
            target, _ = load_target_mask(u["image_id"], mapping, src["seg_dir"], src["instrument_dir"])
            fov = fov_mask(img, opening=fov_opening)
        else:
            regions = entity_regions(os.path.join(src["slake_root"], "imgs", u["image_id"]), legend)
            target = np.logical_or.reduce([regions[n]["mask"] for n in u["target_key"].split("+")])
            fov = fov_for_modality(img, inv_imgs[u["image_id"]]["modality"])
        placebo = apply_placement(target, u["placebo_method"])
        units.append({"image_id": u["image_id"], "target_key": u["target_key"], "qids": u["qids"],
                      "placebo_method": u["placebo_method"], "placement_family": u["placebo_method"].split(":")[0],
                      "height": int(img.shape[0]), "width": int(img.shape[1]), "fov_frac": float(fov.mean()),
                      "target": mask_geometry(target, fov), "placebo": mask_geometry(placebo, fov)})
    return {"dataset": dataset, "manifest": manifest, "source_sha256": man["source_sha256"], "units": units}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dataset", choices=["kvasir", "slake"], required=True)
    ap.add_argument("--arrow", required=True); ap.add_argument("--manifest", required=True); ap.add_argument("--inventory", required=True)
    ap.add_argument("--map"); ap.add_argument("--seg-dir"); ap.add_argument("--instrument-dir"); ap.add_argument("--slake-root")
    ap.add_argument("--output", required=True)
    a = ap.parse_args(argv)
    src = {"map": a.map, "seg_dir": a.seg_dir, "instrument_dir": a.instrument_dir} if a.dataset == "kvasir" else {"slake_root": a.slake_root}
    out = build(a.dataset, a.arrow, a.manifest, a.inventory, src)
    Path(a.output).write_text(json.dumps(out, indent=1) + "\n")
    print(f"{len(out['units'])} unidades -> {a.output}")


if __name__ == "__main__":
    main()
