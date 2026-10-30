"""v7_mimic/scripts/07_manifest.py -- sha256/size/provenance of everything generated in v7_mimic (excluding data/raw)."""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import hashlib, json, os, socket, time
from pathlib import Path
ROOT = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic")
SKIP = {"manifest.json"}
items = {}
for p in sorted(ROOT.rglob("*")):
    if p.is_file() and p.name not in SKIP and "tmp" not in p.parts and "models" not in p.parts:
        rel = str(p.relative_to(ROOT))
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        items[rel] = {"sha256": h.hexdigest(), "bytes": p.stat().st_size, "mtime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(p.stat().st_mtime))}
man = {"root": str(ROOT), "host": socket.gethostname(), "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "sources": {"medical-diff-vqa": "https://physionet.org/files/medical-diff-vqa/1.0.1/", "mimic-cxr-jpg": "https://physionet.org/files/mimic-cxr-jpg/2.1.0/",
                   "medgemma": "google/medgemma-1.5-4b-it @91850547d9f0b2fdd21aa7c5f4f3d1a8a52c243b"},
       "reused_code": "doutorado/med-vqa-icdip-placebo @2b7e731 (harness/isbi_placebo/heal/*, harness/interventions/arrow_io.py, harness/circle_data_bridge.py)",
       "n_files": len(items), "files": items}
(ROOT / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
print(len(items), "files")
