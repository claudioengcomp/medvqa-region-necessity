"""Construction of the paper's conditions (plan v2 §2), at the original resolution.

    C0     intact, with the ORIGINAL BYTES of the arrow (same evaluable questions; same
           session as T/P/S); reproduces the reference cache with 0 % disagreement
    T      target filled (necessity)
    P      control occlusion (`placebo` in the code) filled: same shape and area, different position (artifact control)
    S      everything outside the target filled (sufficiency)
    T1.5, P1.5, T2, P2   target/control occlusion dilated to 1.5x and 2x the area (dose)
    S2     sufficiency with the target dilated 2x (context margin)
    T_mean, P_mean, T_blur, P_blur   T and P filled with the image mean
           and with strong Gaussian blur (robustness to the fill type)
    T_blur1/3/10, P_blur1/3/10, T_regmean, P_regmean, T_ringmean, P_ringmean
           sigma ablation (1/3/10 % of the width), mean color of the region itself and mean
           color of the surroundings (15 px ring), E3 of the pre-registration

The control occlusion is NOT drawn here: it comes from the method recorded in the inventory (F1),
rebuilt by `apply_placement`.

Encoding (amendment of 14/09/2026 to pre-registration §3.1): the conditions are
written as PNG, lossless, from the decoded pixels of the original JPEG,
so that outside the occluded region the pixel is IDENTICAL to what the model sees in C0.
Measured reason: JPEG re-encoding (PIL, default quality, PSNR 58 dB) changed
2.36 % of the C0 predictions (50/2,121) without any visible change, precisely in the
color, position and size templates; with the original bytes C0 reproduces the reference
cache with 0 %. The C4_OCC_75 positive control remains JPEG re-encoded;
that +0.19 pp difference is negligible next to the drop it measures.
"""
from __future__ import annotations

import io
import re

import numpy as np
from PIL import Image
from scipy import ndimage

from harness.isbi_placebo.masks import dilate_to_area

CONDITIONS = ["C0", "T", "P", "S", "T1.5", "P1.5", "T2", "P2", "S2", "T_mean", "P_mean", "T_blur", "P_blur",
              # sigma ablation (execution, 14/09/2026): blur with sigma = 1, 3 and 10 % of the image WIDTH, and mean color
              # of the region itself (limit of blur as sigma -> infinity: removes the shape, keeps the color)
              "T_blur1", "P_blur1", "T_blur3", "P_blur3", "T_blur10", "P_blur10", "T_regmean", "P_regmean",
              # E3 (14/09/2026): mean color of the SURROUNDINGS (15 px ring around the mask): "context suffices" vs "the blob suffices"
              "T_ringmean", "P_ringmean"]
SIGMA_ABLATION = ["T_blur1", "P_blur1", "T_blur3", "P_blur3", "T_blur10", "P_blur10", "T_regmean", "P_regmean",
                  "T_ringmean", "P_ringmean"]
RING_PX = 15
_SPEC = re.compile(r"^(?P<kind>[TPS])(?P<factor>1\.5|2)?(?:_(?P<fill>mean|blur|blur1|blur3|blur10|regmean|ringmean))?$")


def apply_placement(target: np.ndarray, method: str) -> np.ndarray:
    """Rebuild the control occlusion from the method recorded in the inventory."""
    t = np.asarray(target, bool)
    if method == "hflip":
        return t[:, ::-1].copy()
    if method == "vflip":
        return t[::-1, :].copy()
    if method == "rot180":
        return t[::-1, ::-1].copy()
    m = re.match(r"^translate:(-?\d+),(-?\d+)$", method)
    if m:
        dy, dx = int(m.group(1)), int(m.group(2))
        h, w = t.shape
        out = np.zeros_like(t)
        ys, xs = np.nonzero(t)
        ys, xs = ys + dy, xs + dx
        keep = (ys >= 0) & (ys < h) & (xs >= 0) & (xs < w)
        out[ys[keep], xs[keep]] = True
        return out
    raise ValueError(f"metodo de placebo desconhecido: {method!r}")


def fill_region(img: np.ndarray, region: np.ndarray, fill: str, blur_sigma: float = 25.0) -> np.ndarray:
    """Copy of `img` with `region` filled: black, whole-image mean or Gaussian blur."""
    img = np.asarray(img, np.uint8)
    region = np.asarray(region, bool)
    out = img.copy()
    if fill == "black":
        out[region] = 0
    elif fill == "mean":
        out[region] = np.round(img.reshape(-1, img.shape[-1]).mean(axis=0)).astype(np.uint8)
    elif fill == "regmean":  # mean colour of the region itself: removes the shape, keeps the local colour
        out[region] = np.round(img[region].reshape(-1, img.shape[-1]).mean(axis=0)).astype(np.uint8)
    elif fill == "ringmean":  # mean color of the surroundings (ring of RING_PX around the region): removes shape AND color of the region
        ring = ndimage.binary_dilation(region, iterations=RING_PX) & ~region
        if not ring.any():  # region fills the whole image: no surroundings; falls back to the image mean color
            ring = np.ones_like(region)
        out[region] = np.round(img[ring].reshape(-1, img.shape[-1]).mean(axis=0)).astype(np.uint8)
    elif fill.startswith("blur"):
        sigma = blur_sigma if fill == "blur" else float(fill[4:]) / 100.0 * img.shape[1]   # blurN = N % of the width
        blurred = np.stack([ndimage.gaussian_filter(img[..., c].astype(np.float32), sigma)
                            for c in range(img.shape[-1])], axis=-1)
        out[region] = np.clip(np.round(blurred[region]), 0, 255).astype(np.uint8)
    else:
        raise ValueError(f"preenchimento desconhecido: {fill!r}")
    return out


def make_condition_image(img: np.ndarray, target: np.ndarray, placebo: np.ndarray | None, cond: str,
                         blur_sigma: float = 25.0,
                         placebo_by_factor: dict[float, np.ndarray] | None = None) -> tuple[np.ndarray, dict]:
    """Image of condition `cond` and a dictionary describing what was done.

    Dose (authors' decision, 14/09/2026): the dilated target stays in place; the control occlusion
    of P1.5/P2 comes RE-PLACED from `placebo_by_factor[factor]` (inventory). Without this
    argument, falls back to the old behaviour (dilating the control occlusion in place), which only
    exists for tests and for the `overlaps_target` flag.

    info: region_px (filled pixels; in S, everything outside the target), factor, fill,
    overlaps_target (P* only: does the control occlusion touch the dilated target?)."""
    if cond == "C0":  # intact; the generator uses the original bytes, not this image
        img = np.asarray(img, np.uint8)
        return img.copy(), {"condition": cond, "factor": 1.0, "fill": None, "overlaps_target": None, "region_px": 0}
    m = _SPEC.match(cond)
    if not m or cond not in CONDITIONS:
        raise ValueError(f"condicao desconhecida: {cond!r}")
    kind, factor, fill = m.group("kind"), float(m.group("factor") or 1.0), m.group("fill") or "black"
    target = np.asarray(target, bool)
    grown_target = dilate_to_area(target, factor)
    info = {"condition": cond, "factor": factor, "fill": fill, "overlaps_target": None}
    if kind == "T":
        region = grown_target
    elif kind == "S":
        region = ~grown_target
    else:
        if placebo_by_factor is not None and factor in placebo_by_factor:
            region = np.asarray(placebo_by_factor[factor], bool)
        elif placebo is None:
            raise ValueError("condicao P exige placebo")
        else:
            region = dilate_to_area(np.asarray(placebo, bool), factor)
        info["overlaps_target"] = bool((region & grown_target).any())
    info["region_px"] = int(region.sum())
    return fill_region(img, region, fill, blur_sigma), info


def encode_png(img: np.ndarray) -> bytes:
    """Lossless PNG of the already-decoded pixels: outside the occluded region, identical to C0."""
    buf = io.BytesIO()
    Image.fromarray(np.asarray(img, np.uint8)).save(buf, format="PNG", optimize=False)
    return buf.getvalue()
