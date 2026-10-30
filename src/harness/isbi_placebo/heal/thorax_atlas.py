"""Thoracic atlas of the HEAL arm (E4, 15/09/2026). The two definitions suggested in E4 are not
computable on most images (876 of the 1,192 images with a fallback control occlusion have ONE annotated
anatomy; only 44 have both lungs). Registered definition: **population atlas** = union of all
anatomy masks of the HEAL test set (lungs, heart, aorta) in normalized coordinates
(256 x 256), keeping the pixels annotated in >= 2 % of the masks, with holes filled; covers
~49 % of the frame (lungs + mediastinum). Rescaled to each image by nearest neighbour and
used as the FOV of the placer (>= 80 % of the control occlusion inside it). Reproducible from the annotations.

    python -m harness.isbi_placebo.heal.thorax_atlas --annotations data/isbi_placebo/heal/heal_annotations_test.parquet         --out data/isbi_placebo/heal/thorax_atlas_256.npy --png docs/isbi/placebo/figs/thorax_atlas_heal.png
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

from harness.isbi_placebo.heal.heal_rle import decode_rle

N = 256
MIN_FREQ = 0.02


def build_atlas(annotations: str, n: int = N, min_freq: float = MIN_FREQ) -> tuple[np.ndarray, dict]:
    import pandas as pd
    df = pd.read_parquet(annotations, columns=["image_id", "anatomy", "mask_rle", "mask_h", "mask_w"])
    seen = set(); acc = np.zeros((n, n), np.float64); count = 0
    for r in df.itertuples(index=False):
        key = (r.image_id, r.anatomy)
        if key in seen:
            continue
        seen.add(key)
        m = decode_rle(r.mask_rle, int(r.mask_h), int(r.mask_w))
        ms = np.asarray(Image.fromarray(m.astype(np.uint8) * 255).resize((n, n), Image.NEAREST)) > 127
        acc += ms; count += 1
    freq = acc / max(count, 1)
    atlas = ndimage.binary_fill_holes(freq >= min_freq)
    return atlas, {"n_masks": count, "n": n, "min_freq": min_freq, "atlas_area_frac": float(atlas.mean())}


def atlas_for_shape(atlas: np.ndarray, h: int, w: int) -> np.ndarray:
    return np.asarray(Image.fromarray(atlas.astype(np.uint8) * 255).resize((w, h), Image.NEAREST)) > 127


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--annotations", required=True); ap.add_argument("--out", required=True); ap.add_argument("--png", default=None)
    ap.add_argument("--min-freq", type=float, default=MIN_FREQ)
    a = ap.parse_args(argv)
    atlas, info = build_atlas(a.annotations, min_freq=a.min_freq)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True); np.save(a.out, atlas)
    Path(a.out).with_suffix(".json").write_text(json.dumps(info, indent=1) + "\n")
    if a.png:
        Path(a.png).parent.mkdir(parents=True, exist_ok=True); Image.fromarray(atlas.astype(np.uint8) * 255).save(a.png)
    print(json.dumps(info))


if __name__ == "__main__":
    main()
