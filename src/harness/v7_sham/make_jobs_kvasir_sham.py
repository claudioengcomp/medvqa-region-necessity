"""P2.2 (2026-10-09): job list of the Kvasir occluder-test (`sham`) battery: 15 published runs (M3AE s0-2; Qwen LoRA/DoRA s0-2;
SmolVLM LoRA/DoRA s0-2) x 8 sham conditions + C0_cross; then (if a GPU is available) the 12 VT/FT. PEFT: same harness
(extract_predictions_circle) and rescoring as in the control-occlusion batteries; M3AE: m3ae_infer_v7 with its own data_root per condition."""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import json, os, sys
R = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_sham"; P0 = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-p0"; M3 = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/M3AE"
CONDS = ["SHAM_ART_black", "SHAM_ART_blur10", "SHAM_POL_Q1_black", "SHAM_POL_Q1_blur10", "SHAM_POL_Q3_black", "SHAM_POL_Q3_blur10", "SHAM_INS_black", "SHAM_INS_blur10", "C0_cross"]
M3CK = {0: M3 + "/checkpoints/task_finetune_vqa_kvasir-seed0-from_downloaded_pretrained_m3ae.ckpt_dummy/1_u2zxbyuv/checkpoints/epoch=11-step=7175.ckpt",
        1: M3 + "/checkpoints/task_finetune_vqa_kvasir-seed1-from_downloaded_pretrained_m3ae.ckpt_dummy/0_u7xbsvdm/checkpoints/epoch=7-step=4783.ckpt",
        2: M3 + "/checkpoints/task_finetune_vqa_kvasir-seed2-from_downloaded_pretrained_m3ae.ckpt_dummy/0_w33cyvbi/checkpoints/epoch=7-step=4783.ckpt"}
man = json.load(open(R + "/data/manifest_kvasir_sham.json")); group = sys.argv[1] if len(sys.argv) > 1 else "published"
lines = []
if group == "published":
    for s in range(3): lines.append(("M3AE_KVASIR_seed%d" % s, "m3ae", M3CK[s], None))
    for fam, FAM in (("qwen2vl", "QWEN2VL"), ("smolvlm2", "SMOLVLM")):
        for pe in ("lora", "dora"):
            for s in range(3): lines.append(("%s_%s_KVASIR_seed%d" % (FAM, pe.upper(), s), "peft", "%s/outputs/models/%s_%s_kvasir_seed%d" % (P0, fam, pe, s), FAM))
else:
    for pe in ("lora", "dora"):
        for s in range(3): lines.append(("QWEN2VL_%s_VT_KVASIR_seed%d" % (pe.upper(), s), "peft", os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v5_qwen_vt/models/qwen2vl_%s_vt_kvasir_seed%d" % (pe, s), "QWEN2VL"))
    for pe in ("lora", "dora"):
        for s in range(3): lines.append(("SMOLVLM_%s_FT_KVASIR_seed%d" % (pe.upper(), s), "peft", os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v5_smolvlm_ft/models/smolvlm2_%s_ft_kvasir_seed%d" % (pe, s), "SMOLVLM"))
jobs = []
for cond in CONDS:   # condition on the outer loop: all runs of one condition before the next
    arrow = "%s/data/vqa_kvasir_sham_%s.arrow" % (R, cond); sha = man["conditions"][cond]["sha256"]
    for line, eng, adp, FAM in lines:
        name = "%s_%s" % (line, cond); out = "%s/results/%s.json" % (R, name); log = "%s/logs/%s.log" % (R, name)
        if eng == "peft":
            assert os.path.isfile(adp + "/adapter_model.safetensors"), adp
            pe = "LORA_VT" if "_VT_" in line else "DORA_VT" if "_DORA_VT" in line else line.split("_")[1] + ("_FT" if "_FT_" in line else "")
            jobs.append({"name": name, "env": "circle", "reserve_mib": 6 * 1024, "output": out, "log": log, "cmd": ["-m", "harness.extract_predictions_circle", "--model", FAM, "--peft", pe, "--dataset", "KVASIR", "--condition", cond, "--condition-arrow", arrow, "--adapter-dir", adp, "--batch-size", "4", "--progress-checkpoint", "%s/results/.progress/%s.jsonl" % (R, name), "--output", out],
                         "meta": {"line": line, "group": group, "condition": cond, "adapter_dir": adp, "base_model": {"QWEN2VL": "Qwen/Qwen2-VL-2B-Instruct", "SMOLVLM": "HuggingFaceTB/SmolVLM2-2.2B-Instruct"}[FAM], "input_arrow": arrow, "input_arrow_sha256_expected": sha, "inventory": R + "/inventory_kvasir_sham.json", "inference": "harness.extract_predictions_circle (mesmo harness e rescoring das baterias do placebo)"}})
        else:
            root = "%s/data/m3ae_root/%s/" % (R, cond)
            jobs.append({"name": name, "env": "lapa", "reserve_mib": 8 * 1024, "output": out, "log": log, "cwd": os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/worktree_m3ae",
                         "cmd": [os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/worktree/harness/v7_txt/m3ae_infer_v7.py", "--name", name, "--checkpoint", adp, "--data-root", root, "--dataset-key", "vqa_kvasir", "--vqa-label-size", "500", "--dataset", "KVASIR", "--condition", cond, "--output", out, "--arrow-sha256", sha, "--extra", "inventory=" + R + "/inventory_kvasir_sham.json"]})
os.makedirs(R + "/results/.progress", exist_ok=True)
for cond in CONDS:
    root = "%s/data/m3ae_root/%s" % (R, cond); os.makedirs(root, exist_ok=True)
    for s, src in (("test", "%s/data/vqa_kvasir_sham_%s.arrow" % (R, cond)), ("train", M3 + "/data/finetune_arrows/vqa_kvasir_train.arrow"), ("val", M3 + "/data/finetune_arrows/vqa_kvasir_val.arrow")):
        dst = "%s/vqa_kvasir_%s.arrow" % (root, s)
        if not os.path.islink(dst): os.symlink(src, dst)
out = "%s/logs/jobs_kvasir_sham_%s.json" % (R, group); json.dump(jobs, open(out, "w"), indent=1); print(len(jobs), "jobs ->", out)
