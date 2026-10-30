"""v7_mimic/scripts/18_validate_conditions.py -- validates each condition arrow on CPU with load_condition_dataset
(+ med_vlm normalizer) and checks qids/answers against the inventory and against C0. Output: logs/validate_conditions.json."""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import json, os, sys, hashlib, time
os.environ["CUDA_VISIBLE_DEVICES"] = ""
sys.path.insert(0, os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-placebo")
from pathlib import Path
from harness.circle_data_bridge import load_condition_dataset
from harness.interventions.arrow_io import read_arrow
from med_vlm.data.normalizer import build_normalizer
V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic")
inv = json.load(open(V7 / "results/inventory_mimic_test.json")); Q = {q["qid"]: q for q in inv["questions"]}
norm = build_normalizer(image_key="image", question_key="question", answers_key="answers", id_key="id", preprocessor=None)
out = {"date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "arrows": {}}
for tag in ("placebo", "sham"):
    man = json.load(open(V7 / f"data/conditions/manifest_mimic_{tag}.json"))
    c0 = read_arrow(man["conditions"]["C0"]["file"]); c0_q = {q for l in c0.question_id for q in l}
    for c, m in man["conditions"].items():
        p = Path(m["file"]); sha = hashlib.sha256(p.read_bytes()).hexdigest()
        df = read_arrow(str(p)); ds = load_condition_dataset(str(p))
        qids = [q for l in df.question_id for q in l]
        ans_ok = all(Q[q]["answer"] == a[0] for l, al in zip(df.question_id, df.answers) for q, a in zip(l, al))
        ev_ok = all(Q[q]["evaluable"] for q in qids)
        cls = sorted({Q[q]["question_class"] for q in qids})
        batch = [norm(ds[i]) for i in range(min(8, len(ds)))]
        out["arrows"][f"{tag}_{c}"] = {"sha256_matches_manifest": sha == m["sha256"], "n_rows": len(df), "n_questions": len(qids), "ds_len": len(ds),
                                       "qids_unique": len(set(qids)) == len(qids), "qids_subset_of_C0": set(qids) <= c0_q, "n_missing_vs_C0": len(c0_q - set(qids)),
                                       "answers_match_inventory": ans_ok, "all_evaluable": ev_ok, "classes": cls,
                                       "batch8_ok": len(batch) == min(8, len(ds)) and all(set(b) == {"image", "question", "answers", "id"} for b in batch),
                                       "example_image_size": list(ds[0]["image"].size)}
        r = out["arrows"][f"{tag}_{c}"]; print(f"{tag}_{c}", {k: r[k] for k in ("sha256_matches_manifest", "n_rows", "n_questions", "qids_subset_of_C0", "n_missing_vs_C0", "answers_match_inventory", "all_evaluable", "classes", "batch8_ok", "example_image_size")}, flush=True)
(V7 / "logs/validate_conditions.json").write_text(json.dumps(out, indent=1) + "\n")
