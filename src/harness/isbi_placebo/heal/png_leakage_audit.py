"""PIXEL-level train x test leakage audit (plan §10.2): hash of the PNG downscaled to
64x64 (grayscale) for each image; exact duplicates across splits are leakage. Reads only the PNG
manifests (sha256 of the file) and the PNGs.

    python -m harness.isbi_placebo.heal.png_leakage_audit --train-dir <png/train> --test-dir <png/test> --out data/isbi_placebo/heal/png_leakage_audit.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def small_hash(path: Path, size: int = 64) -> str:
    from PIL import Image
    im = Image.open(path).convert("L").resize((size, size), Image.BILINEAR)
    return hashlib.md5(im.tobytes()).hexdigest()


def hashes(d: str) -> dict[str, str]:
    return {p.stem: small_hash(p) for p in sorted(Path(d).glob("*.png"))}


def audit(train_dir: str, test_dir: str) -> dict:
    tr, te = hashes(train_dir), hashes(test_dir)
    inv_tr = {}
    for k, v in tr.items():
        inv_tr.setdefault(v, []).append(k)
    cross = {k: inv_tr[v] for k, v in te.items() if v in inv_tr}
    dup_tr = [ks for ks in inv_tr.values() if len(ks) > 1]
    return {"n_train": len(tr), "n_test": len(te), "test_ids_with_train_duplicate": cross, "n_cross": len(cross),
            "train_internal_duplicates": dup_tr, "verdict": "sem vazamento em nivel de pixel (64x64)" if not cross else "VAZAMENTO"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--train-dir", required=True); ap.add_argument("--test-dir", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    out = audit(a.train_dir, a.test_dir); Path(a.out).write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k not in ("test_ids_with_train_duplicate", "train_internal_duplicates")}, indent=1))


if __name__ == "__main__":
    main()
