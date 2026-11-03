"""Job list of the Qwen2.5-VL-7B battery (27/10/2026), with parity to the 2B runs. Blocks: A 18 DoRA trainings with image; B 9 DoRA no-image
trainings; C the occlusion conditions of the paper on the 12 runs per benchmark (LoRA and DoRA; black, blur 10 %, blur 4 %; target and control) + C0 where
the analysis reads it; D occluder on images without the target (Kvasir 8 conditions, Medical-Diff-VQA 2); E no-image predictions of the DoRA runs.
Full-test C0 of the LoRA runs (Kvasir: reference of Delta-Yes; HEAL and Medical-Diff-VQA: C0 of the analysis) and LoRA no-image predictions: from the
earlier LoRA 7B battery (read-only). Order: measurement (DoRA no-image training of HEAL s0, then one LoRA inference of HEAL), trainings (longest first),
inferences. High initial reservations (rule: measure before lowering). Writes jobs_q25_artigo1.json and the estimates."""
import hashlib, json, os
W = os.environ.get("LAB_ROOT", "LAB_ROOT") + ""; T = f"{W}/v7_txt/extra_runs/q25_artigo1"; Q = f"{W}/v7_txt/extra_runs/qwen25vl7b"; TMP = f"{W}/tmp/v7/q25_artigo1"
PLC = f"{W}/doutorado/med-vqa-icdip-placebo/data"; ISB = f"{PLC}/isbi_placebo"; B4 = f"{W}/v7_txt/extra_runs/blur4_r10/data"; MC = f"{W}/v7_mimic/data/conditions"
ENVX = {k: f"{TMP}/{v}" for k, v in (("TMPDIR", "tmp"), ("TRITON_CACHE_DIR", "triton"), ("TORCHINDUCTOR_CACHE_DIR", "inductor"), ("MPLCONFIGDIR", "matplotlib"), ("XDG_CACHE_HOME", "xdg_cache"),
                                     ("WANDB_CONFIG_DIR", "wandb_config"), ("WANDB_CACHE_DIR", "wandb_cache"), ("WANDB_DATA_DIR", "wandb_data"), ("TORCH_HOME", "torch_home"), ("CUDA_CACHE_PATH", "cuda_cache"))}
for v in ENVX.values(): os.makedirs(v, exist_ok=True)
ENVX["HF_HOME"] = f"{W}/cache/huggingface"; ENVX["HF_DATASETS_CACHE"] = f"{W}/cache/huggingface/datasets"   # never the home partition, always the NVMe volume
for d in ("models", "results", "results/.progress", "results_c0full", "results_c0full/.progress", "logs/sched", "ckpt_int"): os.makedirs(f"{T}/{d}", exist_ok=True)
SHA = {}
def sha(p):
    if p not in SHA: SHA[p] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return SHA[p]
ARR = {"KVASIR": {"C0": (f"{ISB}/vqa_kvasir_placebo_C0.arrow", "607a90e01a88"), "T": (f"{ISB}/vqa_kvasir_placebo_T.arrow", "593f49031982"), "P": (f"{ISB}/vqa_kvasir_placebo_P.arrow", "6e059b79f659"),
                  "T_blur10": (f"{ISB}/vqa_kvasir_placebo_T_blur10.arrow", "54157e7a7ce1"), "P_blur10": (f"{ISB}/vqa_kvasir_placebo_P_blur10.arrow", "b1d2f64a5c69"),
                  "T_blur": (f"{ISB}/vqa_kvasir_placebo_T_blur.arrow", "9b4514dea764"), "P_blur": (f"{ISB}/vqa_kvasir_placebo_P_blur.arrow", "b230c1128786")},
       "HEAL": {"T": (f"{ISB}/vqa_heal_placebo_T.arrow", "a39b15f95e3b"), "P": (f"{ISB}/vqa_heal_placebo_P.arrow", "2f0659246f5c"), "T_blur10": (f"{ISB}/vqa_heal_placebo_T_blur10.arrow", "dd766d08f202"),
                "P_blur10": (f"{ISB}/vqa_heal_placebo_P_blur10.arrow", "9edacf283d8c"), "T_blur": (f"{B4}/vqa_heal_placebo_T_blur.arrow", "0f18c817c5aa"), "P_blur": (f"{B4}/vqa_heal_placebo_P_blur.arrow", "db45000d54fe")},
       "MIMIC": {"T": (f"{MC}/vqa_mimic_placebo_T.arrow", "3ac4979fc01a"), "P": (f"{MC}/vqa_mimic_placebo_P.arrow", "5bb06aa2b27a"), "T_blur10": (f"{MC}/vqa_mimic_placebo_T_blur10.arrow", "92db06c236d3"),
                 "P_blur10": (f"{MC}/vqa_mimic_placebo_P_blur10.arrow", "78540dac2cc6"), "T_blur": (f"{B4}/vqa_mimic_placebo_T_blur.arrow", "f5abf72e4d0b"), "P_blur": (f"{B4}/vqa_mimic_placebo_P_blur.arrow", "eba3399b8350"),
                 "SHAM_black": (f"{MC}/vqa_mimic_sham_SHAM_black.arrow", None), "SHAM_blur10": (f"{MC}/vqa_mimic_sham_SHAM_blur10.arrow", None)}}
for c in ("SHAM_ART_black", "SHAM_ART_blur10", "SHAM_POL_Q1_black", "SHAM_POL_Q1_blur10", "SHAM_POL_Q3_black", "SHAM_POL_Q3_blur10", "SHAM_INS_black", "SHAM_INS_blur10"): ARR["KVASIR"][c] = (f"{W}/v7_sham/data/vqa_kvasir_sham_{c}.arrow", None)
TEST = {"KVASIR": (f"{W}/doutorado/med-vqa-icdip-p0/data/finetune_arrows/vqa_kvasir_test_clean.arrow", None), "HEAL": (f"{PLC}/finetune_arrows/vqa_heal_test.arrow", "a106ad849f50"), "MIMIC": (f"{W}/v7_mimic/data/vqa_mimic_test.arrow", "e68d155a615f")}
NQ = {"KVASIR": 2121, "HEAL": 1446, "MIMIC": 1594, "SHAM_ART": 532, "SHAM_POL_Q1": 1196, "SHAM_POL_Q3": 1199, "SHAM_INS": 1411, "MIMIC_SHAM": 391, "TEST_KVASIR": 10779, "TEST_HEAL": 1446, "TEST_MIMIC": 3000}
for b, d in list(ARR.items()) + [("TEST", TEST)]:
    for c, (p, h) in d.items():
        assert os.path.exists(p), p
        if h: assert sha(p).startswith(h), (p, sha(p))
# estimates (GPU hours): DoRA training = 1.3 x the measured LoRA 7B (HEAL/MIMIC with image ~6.1 h; no-image ~1.6-1.7 h; Kvasir with image ~17 h and no-image
# ~4.2 h estimated from the step rate of the running training); prediction: 0.187 s per question (batch 4, measured) + 1.5 min of loading; no-image 0.15 s/question
# 28/10 (measurement): DoRA no-image HEAL s0 1.45 h, peak 17 036 MiB; DoRA fine-tuned Kvasir s0 1 680 steps/h (~17 h), peak 21 564 MiB -> DoRA ~ measured LoRA
EST_TR = {("KVASIR", "img"): 17.0, ("HEAL", "img"): 6.3, ("MIMIC", "img"): 6.5, ("KVASIR", "txt"): 5.5, ("HEAL", "txt"): 1.5, ("MIMIC", "txt"): 1.8}
def est_pred(n, txt=False): return round((n * (0.15 if txt else 0.187) + 90) / 3600, 3)
J = []
def train(b, enc):   # enc: "", "vt", "txt"
    k = (f"{enc}_" if enc else "") + b.lower(); run = f"qwen25vl_dora_{k}"
    for s in range(3):
        J.append({"name": f"train_{run}_seed{s}", "kind": "train", "env": "circle", "reserve_mib": 19456 if enc == "txt" else 24576,
                  "output": f"{T}/logs/{run}_seed{s}_train.json", "log": f"{T}/logs/sched/{run}_seed{s}.train.log", "skip_order": True,
                  "cmd": [f"{T}/scripts/train_dora_q25.py", f"{T}/configs/qwen25vl_dora_{k}.yaml", str(s), run, f"{T}/logs/{run}_seed{s}_train.json"],
                  "meta": {"bloco": "B" if enc == "txt" else "A", "rodada": "rodada 21 (Qwen2.5-VL-7B DoRA)", "est_h": round(EST_TR[(b, "txt" if enc == "txt" else "img")], 1)}, "env_extra": ENVX})
def pred(b, pe, enc, s, c, arrow, n, bloco, outdir="results", txt=False):
    lab = f"{pe}{'_' + enc if enc else ''}"; line = f"QWEN25VL_{lab}_{b}_seed{s}"; nm = f"{line}_{c}" + ("_full" if outdir == "results_c0full" else "")
    if pe == "LORA":
        ad = f"{Q}/models/qwen25vl_lora{'_vt' if enc == 'VT' else ''}_{b.lower()}_seed{s}"; dep = {"requires": [f"{ad}/adapter_model.safetensors", f"{Q}/logs/qwen25vl_lora{'_vt' if enc == 'VT' else ''}_{b.lower()}_seed{s}.json"]}
    else:
        r = f"qwen25vl_dora_{({'VT': 'vt_', 'TXT': 'txt_'}.get(enc, ''))}{b.lower()}"; ad = f"{T}/models/{r}_seed{s}"; dep = {"after": f"train_{r}_seed{s}"}
    out = f"{T}/{outdir}/{line}_{c}.json"
    cmd = ["-m", "harness.extract_predictions_circle", "--model", "QWEN25VL", "--peft", lab, "--dataset", b, "--condition", c, "--condition-arrow", arrow, "--adapter-dir", ad] + (["--no-image"] if txt else []) + \
          ["--batch-size", "4", "--progress-checkpoint", f"{T}/{outdir}/.progress/{line}_{c}.jsonl", "--output", out]
    J.append({"name": f"predict_{nm}", "kind": "predict", "env": "circle", "reserve_mib": 22528 if pe == "DORA" else 20480, "output": out, "log": f"{T}/logs/sched/{nm}.predict.log", "skip_order": True,
              "line": line, "condition": c, **dep, "cmd": cmd, "env_extra": ENVX,
              "meta": {"bloco": bloco, "line": line, "condition": c, "base_model": "Qwen/Qwen2.5-VL-7B-Instruct (snapshot cc594898)", "adapter_dir": ad, "input_arrow": arrow, "input_arrow_sha256": sha(arrow),
                       "n_perguntas": n, "est_h": est_pred(n, txt), "rodada": "rodada 21"}})
# measurement: DoRA no-image training of HEAL s0 first
train("HEAL", "txt"); J.insert(0, J.pop(0)); med = J[:1]; J.clear(); J.extend(med)
for b in ("KVASIR", "MIMIC", "HEAL"):
    for enc in ("vt", ""): train(b, enc)
for b in ("KVASIR", "MIMIC", "HEAL"): train(b, "txt")
J = [j for k, j in enumerate(J) if not (k > 0 and j["name"] == med[0]["name"])]   # no duplicate of the measurement job
pred("HEAL", "LORA", "", 0, "T", ARR["HEAL"]["T"][0], NQ["HEAL"], "C")   # measurement of the inference (LoRA adapter already available)
for b in ("HEAL", "MIMIC", "KVASIR"):
    for s in range(3):
        for pe in ("LORA", "DORA"):
            for enc in ("", "VT"):
                for c, (p, _) in ARR[b].items():
                    if c.startswith("SHAM"): continue
                    if (b, pe, enc, s, c) == ("HEAL", "LORA", "", 0, "T"): continue
                    pred(b, pe, enc, s, c, p, NQ[b], "C")
                if pe == "DORA":
                    if b == "KVASIR": pred(b, pe, enc, s, "C0", TEST[b][0], NQ["TEST_KVASIR"], "E", outdir="results_c0full")
                    else: pred(b, pe, enc, s, "C0", TEST[b][0], NQ[f"TEST_{b}"], "E")
                for c, (p, _) in ARR[b].items():
                    if c.startswith("SHAM"): pred(b, pe, enc, s, c, p, NQ["MIMIC_SHAM"] if b == "MIMIC" else NQ[c.rsplit("_", 1)[0]], "D")
    for s in range(3): pred(b, "DORA", "TXT", s, "TXT", TEST[b][0], NQ[f"TEST_{b}"], "E", txt=True)
names = [j["name"] for j in J]; assert len(names) == len(set(names))
json.dump(J, open(f"{T}/jobs_q25_artigo1.json", "w"), indent=1)
import collections
tot = collections.defaultdict(lambda: [0, 0.0])
for j in J: k = (j["meta"]["bloco"], j["kind"]); tot[k][0] += 1; tot[k][1] += j["meta"]["est_h"]
for k in sorted(tot): print(k, tot[k][0], "jobs", round(tot[k][1], 1), "h de GPU")
print("total", len(J), "jobs", round(sum(v[1] for v in tot.values()), 1), "h de GPU")
