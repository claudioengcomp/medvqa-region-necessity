"""P2.3 (2026-10-09): jobs of the SLAKE occluder-test (`sham`) battery: 15 published runs (M3AE_SCRATCH s0-2; Qwen LoRA/DoRA s0-2; SmolVLM LoRA/DoRA s0-2)
x SHAM_DIS_black, SHAM_DIS_blur10. PEFT via extract_predictions_circle; M3AE via m3ae_infer_v7 (own data_root per condition, label size 222)."""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import json, os
R = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_sham"; P0 = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-p0"; M3 = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/M3AE"
CONDS = ["SHAM_DIS_black", "SHAM_DIS_blur10"]
M3CK = {0: M3 + "/checkpoints/task_finetune_vqa_slack-seed0-from_downloaded_pretrained_m3ae.ckpt_dummy/0_6b4ewgo6/checkpoints/epoch=11-step=1847.ckpt",
        1: M3 + "/checkpoints/task_finetune_vqa_slack-seed1-from_downloaded_pretrained_m3ae.ckpt_dummy/1_7x3rodoc/checkpoints/epoch=11-step=1847.ckpt",
        2: M3 + "/checkpoints/task_finetune_vqa_slack-seed2-from_downloaded_pretrained_m3ae.ckpt_dummy/0_xfxythgm/checkpoints/epoch=12-step=2001.ckpt"}
man = json.load(open(R + "/data/manifest_slake_sham.json")); lines = []
for s in range(3): lines.append(("M3AE_SCRATCH_SLAKE_seed%d" % s, "m3ae", M3CK[s], None))
for fam, FAM in (("qwen2vl", "QWEN2VL"), ("smolvlm2", "SMOLVLM")):
    for pe in ("lora", "dora"):
        for s in range(3): lines.append(("%s_%s_SLAKE_seed%d" % (FAM, pe.upper(), s), "peft", "%s/outputs/models/%s_%s_slake%s" % (P0, fam, pe, "" if s == 0 else "_seed%d" % s), FAM))
jobs = []
for cond in CONDS:
    arrow = "%s/data/vqa_slake_sham_%s.arrow" % (R, cond); sha = man["conditions"][cond]["sha256"]
    root = "%s/data/m3ae_root_slake/%s" % (R, cond); os.makedirs(root, exist_ok=True)
    for sp, src in (("test", arrow), ("train", M3 + "/data/finetune_arrows/vqa_slack_train.arrow"), ("val", M3 + "/data/finetune_arrows/vqa_slack_val.arrow")):
        dst = "%s/vqa_slack_%s.arrow" % (root, sp)
        if not os.path.islink(dst): os.symlink(src, dst)
    for line, eng, adp, FAM in lines:
        name = "%s_%s" % (line, cond); out = "%s/results/%s.json" % (R, name); log = "%s/logs/%s.log" % (R, name)
        if eng == "peft":
            assert os.path.isfile(adp + "/adapter_model.safetensors"), adp
            jobs.append({"name": name, "env": "circle", "reserve_mib": 6 * 1024, "output": out, "log": log, "skip_order": True, "cmd": ["-m", "harness.extract_predictions_circle", "--model", FAM, "--peft", line.split("_")[1], "--dataset", "SLAKE", "--condition", cond, "--condition-arrow", arrow, "--adapter-dir", adp, "--batch-size", "4", "--progress-checkpoint", "%s/results/.progress/%s.jsonl" % (R, name), "--output", out],
                         "meta": {"line": line, "group": "published", "condition": cond, "adapter_dir": adp, "base_model": {"QWEN2VL": "Qwen/Qwen2-VL-2B-Instruct", "SMOLVLM": "HuggingFaceTB/SmolVLM2-2.2B-Instruct"}[FAM], "input_arrow": arrow, "input_arrow_sha256_expected": sha, "inventory": R + "/inventory_slake_sham.json", "inference": "harness.extract_predictions_circle (mesmo harness e rescoring das baterias do placebo)"}})
        else:
            assert os.path.isfile(adp), adp
            jobs.append({"name": name, "env": "lapa", "reserve_mib": 8 * 1024, "output": out, "log": log, "skip_order": True, "cwd": os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/worktree_m3ae",
                         "cmd": [os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/worktree/harness/v7_txt/m3ae_infer_v7.py", "--name", name, "--checkpoint", adp, "--data-root", root + "/", "--dataset-key", "vqa_slack", "--vqa-label-size", "222", "--dataset", "SLAKE", "--condition", cond, "--output", out, "--arrow-sha256", sha, "--model-label", "M3AE_SCRATCH", "--extra", "inventory=" + R + "/inventory_slake_sham.json"]})
json.dump(jobs, open(R + "/logs/jobs_slake_sham.json", "w"), indent=1); print(len(jobs), "jobs")
