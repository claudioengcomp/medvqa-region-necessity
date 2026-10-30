"""v7_mimic (2026-10-13, authors): M3AE arrows with the image replaced by the constant gray 384x384 RGB(128,128,128) of
harness/interventions/make_c1_blank_images.py (the same as C1 and as the text-only M3AE of Kvasir, SLAKE and HEAL; tmp/v7/make_gray_arrows.py),
for MIMIC train, validation and test. Sources (read-only): v7_mimic/data/vqa_mimic_{train,val,test}.arrow.
Output: v7_mimic/m3ae_arrows_gray/vqa_mimic_{split}_gray.arrow + data_root/vqa_mimic_{split}.arrow (links) + manifest_gray_arrows.json.
No MIMIC pixel enters the gray arrows; the questions and answers do (credentialed data: they stay on gpu1)."""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import hashlib, json, os, socket, sys, time
sys.path.insert(0, os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/worktree")
from harness.interventions.make_c1_blank_images import blank_out_images, DEFAULT_SIZE, DEFAULT_FILL_COLOR
from harness.interventions.arrow_io import read_arrow, count_questions
SRC = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic/data"; OUT = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic/m3ae_arrows_gray"
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""): h.update(b)
    return h.hexdigest()
os.makedirs(OUT + "/data_root", exist_ok=False)
man = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "host": socket.gethostname(), "script": __file__, "script_sha256": sha(__file__), "gray": {"size": DEFAULT_SIZE, "rgb": DEFAULT_FILL_COLOR, "encoder": "harness.interventions.make_c1_blank_images.blank_out_images (JPEG)"}, "files": {}}
for split in ("train", "val", "test"):
    s = f"{SRC}/vqa_mimic_{split}.arrow"; o = f"{OUT}/vqa_mimic_{split}_gray.arrow"
    t0 = time.time(); blank_out_images(s, o)
    src_df = read_arrow(s); df = read_arrow(o)
    assert len(df) == len(src_df) and count_questions(df) == count_questions(src_df), (split, len(df), len(src_df))
    os.symlink(f"../vqa_mimic_{split}_gray.arrow", f"{OUT}/data_root/vqa_mimic_{split}.arrow")
    man["files"][os.path.basename(o)] = {"source": s, "source_sha256": sha(s), "sha256": sha(o), "bytes": os.path.getsize(o), "rows": len(df), "questions": count_questions(df), "seconds": round(time.time() - t0, 1)}
    print(split, man["files"][os.path.basename(o)], flush=True)
json.dump(man, open(f"{OUT}/manifest_gray_arrows.json", "w"), indent=1)
print("FIM")
