"""Pure mask functions for the ISBI 2027 paper (positional control occlusion).

Implements the rules of §2 of plan v2 (docs/isbi/placebo/plano-execucao-isbi-v2-placebo.md):

- control occlusion (`placebo` in the code) = same shape and area as the target, at another position in the same image;
  order of attempts: horizontal mirror, vertical mirror, 180-degree rotation,
  then up to `n_random` random translations with a fixed seed;
- a control occlusion is valid if entirely inside the frame, with no overlap with the target
  dilated by `margin_px` (5 px) and with >= `min_fov_frac` (80 %) of its pixels
  inside the endoscopic field of view (FOV);
- morphological dilation of the target to 1.5x and 2x the area (dose);
- classification of the 18 Kvasir questions, fixed in §1 of the plan.

Everything here operates on boolean arrays at the original image resolution; the
mask is never resized separately from the image (plan §2, rule 4).
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage

# §1 of plan v2: pre-registered class per template (target = polyp, unless noted).
KVASIR_QUESTION_CLASS: dict[str, str] = {
    "How many polyps are in the image?": "dependent_polyp",
    "What is the size of the polyp?": "dependent_polyp",
    "What type of polyp is present?": "dependent_polyp",
    "Where in the image is the abnormality?": "dependent_polyp",
    "What color is the abnormality? If more than one separate with ;": "dependent_polyp",
    "Are there any abnormalities in the image? Check all that are present.": "dependent_polyp",
    "Does this image contain any finding?": "dependent_polyp",
    "How many findings are present?": "dependent_polyp",
    "Have all polyps been removed?": "dependent_polyp_secondary",
    "How many instrumnets are in the image?": "dependent_instrument",
    "Where in the image is the instrument?": "dependent_instrument",
    "Are there any instruments in the image? Check all that are present.": "dependent_instrument",
    "Is there text?": "negative_control",
    "Is there a green/black box artefact?": "negative_control",
    "What type of procedure is the image taken from?": "negative_control",
    "Where in the image is the anatomical landmark?": "excluded",
    "Are there any anatomical landmarks in the image? Check all that are present.": "excluded",
    "What color is the anatomical landmark? If more than one separate with ;": "excluded",
}


def _norm(q: str) -> str:
    return " ".join(q.split()).rstrip(".").lower()


_NORMALIZED_CLASS = {_norm(k): v for k, v in KVASIR_QUESTION_CLASS.items()}


def classify_kvasir_question(question: str) -> str:
    """Pre-registered class of the question; KeyError if the template is not one of the 18."""
    key = _norm(question)
    if key not in _NORMALIZED_CLASS:
        raise KeyError(f"template desconhecido: {question!r}")
    return _NORMALIZED_CLASS[key]


def binarize_mask(arr: np.ndarray, threshold: int = 127) -> np.ndarray:
    """Boolean mask from gray, RGB or RGBA (alpha channel ignored).

    Threshold at 127 because the Kvasir-SEG masks are JPEG and carry compression
    noise (values 0-5 in the background, ~250 on the target)."""
    a = np.asarray(arr)
    if a.ndim == 3:
        a = a[..., :3].max(axis=-1)
    return a > threshold


def fov_mask(rgb: np.ndarray, threshold: int = 20, opening: int = 0) -> np.ndarray:
    """Field of view: largest connected component of the non-black pixels, with holes
    filled. Isolated bright pixels outside the disc are not included.

    `opening` > 0 applies a morphological opening (3x3, `opening` iterations) before
    choosing the component: removes thin lines (the CT table in SLAKE) that, connected
    to the body, would make the hole filling swallow the background between body and table.
    In Kvasir it stays 0 (plan rule); in SLAKE, 4 (authors' decision, 14/09/2026)."""
    bright = np.asarray(rgb)[..., :3].max(axis=-1) > threshold
    if opening > 0:
        bright = ndimage.binary_opening(bright, iterations=opening)
    bright = ndimage.binary_closing(bright, iterations=2)
    labels, n = ndimage.label(bright)
    if n == 0:
        return np.zeros(bright.shape, bool)
    sizes = ndimage.sum(bright, labels, index=np.arange(1, n + 1))
    largest = labels == (int(np.argmax(sizes)) + 1)
    return ndimage.binary_fill_holes(largest)


def dilate_to_area(mask: np.ndarray, factor: float) -> np.ndarray:
    """Dilates iteratively (3x3) until the area reaches `factor` times the original."""
    mask = np.asarray(mask, bool)
    if factor <= 1.0 or not mask.any():
        return mask.copy()
    target = factor * mask.sum()
    out = mask.copy()
    while out.sum() < target:
        grown = ndimage.binary_dilation(out)
        if grown.sum() == out.sum():  # whole frame; nothing left to grow into
            break
        out = grown
    return out


DOSE_FACTORS = (1.5, 2.0)


def place_placebos_by_factor(target: np.ndarray, fov: np.ndarray, seed: int, n_random: int = 50,
                             margin_px: int = 5, min_fov_frac: float = 0.8, max_area_frac: float = 0.4,
                             factors=DOSE_FACTORS) -> tuple[dict[str, str | None], dict[str, str | None]]:
    """Dose (authors' decision, 14/09/2026): the dilated target stays in place and the control occlusion is
    RE-PLACED for the dilated shape, with the same search order and the same seed.
    Returns ({factor: method|None}, {factor: reason|None}); keys "1.5" and "2"."""
    methods, reasons = {}, {}
    for f in factors:
        key = f"{f:g}"
        grown = dilate_to_area(target, f)
        if area_fraction(grown, fov) > max_area_frac:
            methods[key], reasons[key] = None, "area_gt_max"
            continue
        placebo, how = place_placebo(grown, fov, seed=seed, n_random=n_random, margin_px=margin_px,
                                     min_fov_frac=min_fov_frac)
        methods[key], reasons[key] = (how, None) if placebo is not None else (None, how)
    return methods, reasons


def area_fraction(mask: np.ndarray, fov: np.ndarray) -> float:
    """Fraction of the FOV occupied by the mask."""
    fov_px = int(np.asarray(fov, bool).sum())
    return float((np.asarray(mask, bool) & fov).sum() / fov_px) if fov_px else float("nan")


def _translate(mask: np.ndarray, dy: int, dx: int) -> np.ndarray:
    """Shift the mask without wrap-around (pixels that would leave the frame are lost)."""
    h, w = mask.shape
    out = np.zeros_like(mask)
    ys, xs = np.nonzero(mask)
    ys, xs = ys + dy, xs + dx
    keep = (ys >= 0) & (ys < h) & (xs >= 0) & (xs < w)
    out[ys[keep], xs[keep]] = True
    return out


def _is_valid(candidate: np.ndarray, forbidden: np.ndarray, fov: np.ndarray,
              n_target: int, min_fov_frac: float) -> bool:
    n = int(candidate.sum())
    if n != n_target:            # lost pixels: left the frame
        return False
    if (candidate & forbidden).any():
        return False
    return (candidate & fov).sum() / n >= min_fov_frac


def place_placebo(target: np.ndarray, fov: np.ndarray, seed: int, n_random: int = 50,
                  margin_px: int = 5, min_fov_frac: float = 0.8):
    """Place a copy of the target elsewhere in the image (plan §2, rules 1-2).

    Returns (placebo_mask, method) or (None, "no_valid_placement").
    Methods, in the order tried: "hflip", "vflip", "rot180", "translate:<dy>,<dx>"."""
    target = np.asarray(target, bool)
    fov = np.asarray(fov, bool)
    n_target = int(target.sum())
    if n_target == 0:
        return None, "empty_target"
    forbidden = ndimage.binary_dilation(target, iterations=margin_px)
    fixed = (("hflip", target[:, ::-1]), ("vflip", target[::-1, :]), ("rot180", target[::-1, ::-1]))
    for how, cand in fixed:
        if _is_valid(cand, forbidden, fov, n_target, min_fov_frac):
            return cand.copy(), how
    ys, xs = np.nonzero(target)
    h, w = target.shape
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    rng = np.random.default_rng(seed)
    for _ in range(n_random):
        dy = int(rng.integers(-y0, h - 1 - y1 + 1))   # keeps the box inside the frame
        dx = int(rng.integers(-x0, w - 1 - x1 + 1))
        cand = _translate(target, dy, dx)
        if _is_valid(cand, forbidden, fov, n_target, min_fov_frac):
            return cand, f"translate:{dy},{dx}"
    return None, "no_valid_placement"
