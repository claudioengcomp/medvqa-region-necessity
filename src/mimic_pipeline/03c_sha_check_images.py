"""v7_mimic/scripts/03c_sha_check_images.py -- sha256 of each JPG in the subset against SHA256SUMS.txt of MIMIC-CXR-JPG 2.1.0.
Usage: python 03c_sha_check_images.py <list> <tag>  -> logs/sha_check_images_<tag>.json (+ list of missing/errored files to redo)."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import hashlib, json, sys, time, socket
from pathlib import Path
RAW = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/raw/mimic-cxr-jpg/2.1.0"); V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic")
lst, tag = sys.argv[1], sys.argv[2]
want = [l.strip() for l in open(lst) if l.strip()]; ws = set(want); exp = {}
with open(RAW / "SHA256SUMS.txt") as f:
    for line in f:
        h, _, p = line.rstrip("\n").partition(" "); p = p.strip()
        if p in ws: exp[p] = h
missing_file, mismatch, ok, total_bytes = [], [], 0, 0
for p in want:
    fp = RAW / p
    if not fp.is_file(): missing_file.append(p); continue
    b = fp.read_bytes(); total_bytes += len(b)
    if hashlib.sha256(b).hexdigest() == exp.get(p): ok += 1
    else: mismatch.append(p)
res = {"tag": tag, "list": lst, "n": len(want), "with_expected_sha": len(exp), "ok": ok, "n_missing_file": len(missing_file), "n_mismatch": len(mismatch),
       "missing_file": missing_file[:20], "mismatch": mismatch[:20], "total_bytes_ok_files": total_bytes, "mean_bytes": round(total_bytes / max(1, len(want) - len(missing_file))),
       "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "host": socket.gethostname(), "script": "v7_mimic/scripts/03c_sha_check_images.py"}
(V7 / f"logs/sha_check_images_{tag}.json").write_text(json.dumps(res, indent=1) + "\n")
(V7 / f"logs/redo_{tag}.txt").write_text("\n".join(missing_file + mismatch) + ("\n" if (missing_file or mismatch) else ""))
print(json.dumps({k: res[k] for k in ("n", "ok", "n_missing_file", "n_mismatch", "mean_bytes")}))
