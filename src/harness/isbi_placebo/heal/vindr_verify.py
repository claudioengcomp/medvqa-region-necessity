"""Step 5 of the selective download: verifies by sha256 the VinDr-CXR DICOMs downloaded
against SHA256SUMS.txt (filtered to the ids in the list), lists missing and corrupted files
for re-download and writes/updates the manifest data/isbi_placebo/heal/vindr_manifest.json
(id, VinDr split, HEAL split, bytes, sha256, verified).

Never reads credentials or transfers data: operates only on local files.

    python -m harness.isbi_placebo.heal.vindr_verify --base <vindr-cxr/1.0.0 root>         --list <base>/ids_heal_test.txt --heal-items data/isbi_placebo/heal/heal_items.parquet         --manifest data/isbi_placebo/heal/vindr_manifest.json --redo <base>/ids_redo.txt
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for blk in iter(lambda: fp.read(chunk), b""):
            h.update(blk)
    return h.hexdigest()


def read_sums(path: str) -> dict[str, str]:
    out = {}
    for line in Path(path).read_text().splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            out[parts[1].strip()] = parts[0].strip()
    return out


def read_list(path: str) -> list[str]:
    return [l.strip() for l in Path(path).read_text().splitlines() if l.strip()]


def heal_split_map(heal_items: str | None) -> dict[str, str]:
    if not heal_items:
        return {}
    import pandas as pd
    df = pd.read_parquet(heal_items, columns=["image_id", "heal_split"]).drop_duplicates("image_id")
    return dict(zip(df["image_id"], df["heal_split"]))


def verify(base: str, rel_paths: list[str], sums: dict[str, str], heal_splits: dict[str, str],
           manifest: dict | None = None) -> tuple[dict, list[str], list[str]]:
    """Returns (updated manifest, missing, corrupted). Entries already verified in the
    manifest with the same size in bytes are kept without recomputing the hash."""
    items = dict(manifest["items"]) if manifest else {}
    missing, corrupt = [], []
    for rel in rel_paths:
        split, fname = rel.split("/", 1)
        image_id = fname[: -len(".dicom")] if fname.endswith(".dicom") else fname
        expected = sums.get(rel)
        p = Path(base, rel)
        prev = items.get(image_id)
        if not p.is_file():
            missing.append(rel)
            items[image_id] = {"id": image_id, "vindr_split": split, "heal_split": heal_splits.get(image_id),
                               "bytes": None, "sha256": None, "sha256_expected": expected, "verified": False, "status": "missing"}
            continue
        nbytes = p.stat().st_size
        if prev and prev.get("verified") and prev.get("bytes") == nbytes and prev.get("sha256_expected") == expected:
            continue
        digest = sha256_file(p)
        ok = expected is not None and digest == expected
        if not ok:
            corrupt.append(rel)
        items[image_id] = {"id": image_id, "vindr_split": split, "heal_split": heal_splits.get(image_id),
                           "bytes": nbytes, "sha256": digest, "sha256_expected": expected, "verified": ok,
                           "status": "ok" if ok else ("no_reference" if expected is None else "corrupt")}
    out = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "base": str(base),
           "n_items": len(items), "n_verified": sum(1 for v in items.values() if v["verified"]),
           "n_missing": sum(1 for v in items.values() if v["status"] == "missing"),
           "n_corrupt": sum(1 for v in items.values() if v["status"] == "corrupt"),
           "n_no_reference": sum(1 for v in items.values() if v["status"] == "no_reference"),
           "bytes_verified": sum(v["bytes"] or 0 for v in items.values() if v["verified"]),
           "items": dict(sorted(items.items()))}
    return out, missing, corrupt


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", required=True); ap.add_argument("--list", required=True, action="append")
    ap.add_argument("--sums", default=None, help="padrao: <base>/SHA256SUMS.txt")
    ap.add_argument("--heal-items", default=None); ap.add_argument("--manifest", required=True)
    ap.add_argument("--redo", default=None, help="lista (faltantes + corrompidos) para redownload")
    ap.add_argument("--delete-corrupt", action="store_true", help="apaga os arquivos corrompidos para o redownload")
    a = ap.parse_args(argv)
    sums = read_sums(a.sums or os.path.join(a.base, "SHA256SUMS.txt"))
    rel = []
    for l in a.list:
        rel += read_list(l)
    prev = json.loads(Path(a.manifest).read_text()) if Path(a.manifest).is_file() else None
    man, missing, corrupt = verify(a.base, rel, sums, heal_split_map(a.heal_items), prev)
    Path(a.manifest).parent.mkdir(parents=True, exist_ok=True)
    Path(a.manifest).write_text(json.dumps(man, indent=1) + "\n")
    if a.delete_corrupt:
        for r in corrupt:
            Path(a.base, r).unlink(missing_ok=True)
    if a.redo:
        Path(a.redo).write_text("".join(f"{r}\n" for r in missing + corrupt))
    summary = {k: v for k, v in man.items() if k != "items"}
    summary.update({"listed": len(rel), "missing_now": len(missing), "corrupt_now": len(corrupt)})
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
