"""HEAL-MedVQA masks (VinDr part): `mask_rle` is a flat list of (start, length) pairs
with 0-based indexing over the image vector in COLUMN-MAJOR (Fortran) order, with `mask_h` x `mask_w` =
native size of the DICOM. Validated on 15/09/2026 on one test image (identifier omitted)
("Left upper lung" falls on the patient's left side, L marker, rows 465-1095 of 3032).
"""
from __future__ import annotations

import numpy as np


def decode_rle(rle, h: int, w: int) -> np.ndarray:
    """(start, length)* in column-major order -> boolean mask (h, w)."""
    rle = np.asarray(rle, dtype=np.int64)
    if rle.size % 2:
        raise ValueError("RLE com numero impar de elementos")
    flat = np.zeros(h * w, dtype=bool)
    for s, l in zip(rle[0::2], rle[1::2]):
        if s < 0 or s + l > h * w:
            raise ValueError(f"RLE fora da imagem: inicio {s}, comprimento {l}, h*w {h * w}")
        flat[s:s + l] = True
    return flat.reshape((w, h)).T


def encode_rle(mask: np.ndarray) -> list[int]:
    """Inverse of decode_rle (for tests and for writing derived masks)."""
    flat = np.asarray(mask, bool).T.reshape(-1)
    out: list[int] = []
    pad = np.concatenate([[0], flat.astype(np.int8), [0]])
    d = np.diff(pad)
    starts = np.nonzero(d == 1)[0]; ends = np.nonzero(d == -1)[0]
    for s, e in zip(starts, ends):
        out += [int(s), int(e - s)]
    return out


def resize_mask(mask: np.ndarray, out_h: int, out_w: int) -> np.ndarray:
    """Nearest neighbour (binary mask) to the PNG resolution."""
    from PIL import Image
    im = Image.fromarray(np.asarray(mask, np.uint8) * 255)
    return np.asarray(im.resize((out_w, out_h), Image.NEAREST)) > 127
