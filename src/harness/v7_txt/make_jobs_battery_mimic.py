"""v7_mimic block B (2026-10-11): jobs for the MIMIC control-occlusion/occluder-test batteries for infer_scheduler_v7.
27 image runs (15 published + 12 fine-tuned-encoder (tower) runs; the text-only ones are left out: C1 and T/P/S do not apply). Conditions, in the authors' order:
C1 -> T, P, S -> T/P/S_blur10 -> T/P/S_regmean -> SHAM_black, SHAM_blur10 -> T1.5, P1.5, T2, P2. List order = condition-major
(published before tower within each condition), skip_order; each job requires the run's C0 (`requires`). control-occlusion C0 and occluder-test C0 = the same
test images (PNG 1024): reused from the run's full C0 by qid; invariance check by actually running them on
QWEN2VL_LORA_FROZEN_MIMIC_seed0 (first jobs). sha of each arrow checked here against the condition manifests and again in the provenance stamp."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json, hashlib, re
R = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic"; H = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/worktree/harness/v7_txt"; WM = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/worktree_m3ae"
SHA = json.load(open(R + "/logs/battery_arrows_sha_check.json")); assert all(v["ok"] for v in SHA.values()) and len(SHA) == 18
ARW = {}
for k, v in SHA.items():
    g, c = k.split("_", 1); ARW[(g, c)] = v
ORDER = [("placebo", "C1")] + [("placebo", c) for c in ("T", "P", "S")] + [("placebo", c + "_blur10") for c in ("T", "P", "S")] + [("placebo", c + "_regmean") for c in ("T", "P", "S")] + [("sham", "SHAM_black"), ("sham", "SHAM_blur10")] + [("placebo", c) for c in ("T1.5", "P1.5", "T2", "P2")]
PUB = [("QWEN2VL_LORA_FROZEN", "QWEN2VL", "LORA_FROZEN", "qwen2vl_lora_mimic", 6144), ("QWEN2VL_DORA", "QWEN2VL", "DORA", "qwen2vl_dora_mimic", 6144), ("SMOLVLM_LORA", "SMOLVLM", "LORA", "smolvlm2_lora_mimic", 7168), ("SMOLVLM_DORA", "SMOLVLM", "DORA", "smolvlm2_dora_mimic", 7168), ("M3AE", None, None, None, 8192)]
TOW = [("QWEN2VL_LORA_VT", "QWEN2VL", "LORA_VT", "qwen2vl_lora_vt_mimic", 6144), ("QWEN2VL_DORA_VT", "QWEN2VL", "DORA_VT", "qwen2vl_dora_vt_mimic", 6144), ("SMOLVLM_LORA_FT", "SMOLVLM", "LORA_FT", "smolvlm2_lora_ft_mimic", 7168), ("SMOLVLM_DORA_FT", "SMOLVLM", "DORA_FT", "smolvlm2_dora_ft_mimic", 7168)]
LINES = [(f"{p}_MIMIC_seed{s}", m, pe, (f"{R}/models/{a}_seed{s}" if a else None), res, s, grp) for grp, L in (("publicada", PUB), ("torre", TOW)) for s in (0, 1, 2) for (p, m, pe, a, res) in L]
FAM = [x[0] for x in PUB + TOW]; LINES.sort(key=lambda x: (x[6] != "publicada", FAM.index(x[0].rsplit("_MIMIC_", 1)[0]), x[5]))   # published ones first; family in PUB/TOW order; seed
def job(line, model, peft, adir, res, seed, grp, g, c, cname=None):
    cname = cname or c; a = ARW[(g, c)]; out = f"{R}/results/{line}_{cname}.json"; prog = f"{R}/results/.progress/{line}_{cname}.jsonl"; logf = f"{R}/logs/battery/{line}_{cname}.log"
    base = {"name": f"{line}_{cname}", "reserve_mib": res, "output": out, "log": logf, "skip_order": True, "requires": [f"{R}/results/{line}_C0.json"], "group": grp, "condition": cname, "line": line}
    if model is None:   # M3AE: its own data_root per condition (links); the wrapper locates the best checkpoint
        return {**base, "env": "lapa", "cwd": WM, "cmd": [H + "/m3ae_mimic_cond.py", str(seed), cname, a["path"], a["sha256"], out]}
    return {**base, "env": "circle", "cmd": ["-m", "harness.extract_predictions_circle", "--model", model, "--peft", peft, "--dataset", "MIMIC", "--condition", ("C0" if cname.endswith("_check") else cname), "--condition-arrow", a["path"], "--adapter-dir", adir, "--batch-size", "4", "--progress-checkpoint", prog, "--output", out],
            "meta": {"line": line, "condition": cname, "conjunto": g, "base_model": {"QWEN2VL": "Qwen/Qwen2-VL-2B-Instruct", "SMOLVLM": "HuggingFaceTB/SmolVLM2-2.2B-Instruct"}[model], "adapter_dir": adir, "input_arrow": a["path"], "input_arrow_sha256_expected": a["sha256"],
                     "inference": "harness.extract_predictions_circle (mesmo da C0)", "rescoring": "answer_matches do harness (mesmo da C0)"}}
jobs = []
chk = LINES[0]; assert chk[0] == "QWEN2VL_LORA_FROZEN_MIMIC_seed0", chk
jobs.append(job(*chk, "placebo", "C0", "placeboC0_check")); jobs.append(job(*chk, "sham", "C0", "shamC0_check"))
for g, c in ORDER:
    for L in LINES: jobs.append(job(*L, g, c))
json.dump(jobs, open(R + "/logs/jobs_battery_mimic.json", "w"), indent=1)
print(len(jobs), "jobs;", len(LINES), "linhas;", len(ORDER), "condicoes; primeiras:", [j["name"] for j in jobs[:4]])
