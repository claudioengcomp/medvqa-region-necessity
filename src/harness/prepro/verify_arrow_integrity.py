"""Checks the sha256 of M3AE arrows against a manifest of known
checksums BEFORE running real inference -- explicit request of the
authors after the seed 2 finding (`kill -9` left
`vqa_nih_pa_test.arrow` temporarily with the validation content; the
`.orig_backup` saved the day that time, but "if the backup did not exist you
would have found this out with the test arrow swapped, silently").

Detects silent file corruption/swap -- does not REPLACE
`swap_test_arrow`/`relabel_arrow_with_vocab` (which already take care of
correct label/vocabulary); checks that the BYTES of the file are the same
as those recorded as canonical the last time someone confirmed
it was right.

Usage:
    python -m harness.prepro.verify_arrow_integrity         --manifest data/isbi/nih_test_arrow_checksums.json         --arrow-dir $LAB_ROOT/doutorado/M3AE/data/finetune_arrows
"""
from __future__ import annotations
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable

import argparse
import hashlib
import json
import os


def sha256_of_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_arrows(manifest: dict[str, str], arrow_dir: str) -> dict[str, dict]:
    """`manifest`: {file_name: expected_sha256}. Returns
    {file_name: {"ok": bool, "expected": str, "actual": str|None,
    "error": str|None}} -- NEVER raises on its own (the caller
    decides what to do with a mismatch), but clearly marks missing
    file vs. different hash, which are distinct findings."""
    result = {}
    for filename, expected_sha256 in manifest.items():
        path = os.path.join(arrow_dir, filename)
        if not os.path.isfile(path):
            result[filename] = {"ok": False, "expected": expected_sha256, "actual": None,
                                 "error": f"arquivo não existe: {path}"}
            continue
        actual = sha256_of_file(path)
        result[filename] = {"ok": actual == expected_sha256, "expected": expected_sha256,
                             "actual": actual, "error": None}
    return result


def load_manifest_checksums(manifest_path: str) -> dict[str, str]:
    """Reads the manifest file ({"comment": ..., "checksums": {file:
    sha256}}) and returns only the `checksums` dict -- separated from the
    `comment` key so that `verify_arrows` never tries to treat the comment as
    a file name."""
    with open(manifest_path, encoding="utf-8") as fp:
        manifest_doc = json.load(fp)
    return manifest_doc["checksums"]


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--arrow-dir", required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    manifest = load_manifest_checksums(args.manifest)

    results = verify_arrows(manifest, args.arrow_dir)
    any_failed = False
    for filename, r in results.items():
        if r["ok"]:
            print(f"OK   {filename}")
        else:
            any_failed = True
            if r["error"]:
                print(f"FAIL {filename}: {r['error']}")
            else:
                print(f"FAIL {filename}: esperado {r['expected']}, achado {r['actual']}")

    if any_failed:
        raise SystemExit(
            "integridade dos arrows FALHOU -- não prosseguir pro Portão 1 sem investigar "
            "(ver docs/isbi/fase_a3_treino.md pro contexto do achado que motivou esta checagem)"
        )
    print(f"\n{len(results)} arrow(s) conferidos, todos batem com o manifesto.")
