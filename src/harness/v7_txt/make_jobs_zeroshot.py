"""P3.2 (2026-10-09): zero-shot C0 and TXT jobs (no image, same rule as P1.0, without telling the model) for MEDVLTHINKER (cache),
LLAVA_MED, QWEN25VL on the three full test sets (Kvasir 10 779, SLAKE 1 061, HEAL 1 446 evaluable). HuatuoGPT-Vision-7B
is not native to transformers (LlavaQwen2ForCausalLM): left out of the list (deviation reported). System prompt only for MedVLThinker
(the one registered in spec_registry). E7 rescoring of the closed-ended questions applied afterwards by rescore_e7.py."""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import json, os
R = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_zeroshot"
ARROWS = {"MIMIC": (os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic/data/vqa_mimic_test.arrow", "e68d155a615f7ecd"), "KVASIR": (os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-p0/data/finetune_arrows/vqa_kvasir_test_clean.arrow", "ff5c25692c1b4632"),
          "SLAKE": (os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/M3AE/data/finetune_arrows/vqa_slack_test.arrow", "fe94d9a08770ab65"),
          "HEAL": (os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-placebo/data/finetune_arrows/vqa_heal_test.arrow", "a106ad849f50ddd9")}
# 13/10 (authors): MedVLThinker under peak-based accounting; reservation = largest peak measured over 10 runs (16 602 MiB), rounded to 16 640 MiB.
MODELS = {"MEDVLTHINKER": ("UCSC-VLAA/MedVLThinker-7B-RL_PMC", 16640, "system prompt registrado (spec_registry._MEDVLTHINKER_SYSTEM_PROMPT), max_new_tokens 512"),
          "LLAVA_MED": ("chaoyinshe/llava-med-v1.5-mistral-7b-hf", 20 * 1024, "sem system prompt; dtype auto; template [INST] <image>\\n{q} [/INST]"),
          "QWEN25VL": ("Qwen/Qwen2.5-VL-7B-Instruct", 20 * 1024, "sem system prompt alem do default do template (You are a helpful assistant.)"),
          "MEDGEMMA": ("google/medgemma-1.5-4b-it", 14 * 1024, "sem system prompt; template de chat do Gemma 3; modelo do cache = medgemma-1.5-4b-it (nao o medgemma-4b-it do plano)")}
jobs = []
INS = "Answer with a single word or a short phrase."
INS_MODE = {"LLAVA_MED": "prefix", "QWEN25VL": "system", "MEDGEMMA": "system"}   # MedVLThinker: registered system prompt, without the instruction
import sys
ORDER = sys.argv[1].split(",") if len(sys.argv) > 1 else ["MEDVLTHINKER", "LLAVA_MED", "QWEN25VL", "MEDGEMMA"]
BENCHES = sys.argv[2].split(",") if len(sys.argv) > 2 else ["SLAKE", "HEAL", "KVASIR"]
OUTFILE = sys.argv[3] if len(sys.argv) > 3 else R + "/logs/jobs_zeroshot.json"
SUFFIX = sys.argv[4] if len(sys.argv) > 4 else ""   # e.g. _instr (MedVLThinker with the short instruction appended to the registered system prompt)
if SUFFIX == "_instr": INS_MODE = dict(INS_MODE, MEDVLTHINKER="system_append")   # authors' order (10/10): MedVLThinker, LLaVA-Med, Qwen2.5-VL; MedGemma once in the cache
for m in ORDER:
    for bench in BENCHES:
        for cond in ("C0", "TXT"):
            hf, res, note = MODELS[m]
            name = "%s_ZEROSHOT_%s_%s%s" % (m, bench, cond, SUFFIX); out = "%s/results/%s.json" % (R, name); arrow, sha = ARROWS[bench]
            cmd = ["-m", "harness.extract_predictions_circle", "--model", m, "--peft", "ZEROSHOT", "--dataset", bench, "--condition", cond, "--condition-arrow", arrow, "--batch-size", "4", "--progress-checkpoint", "%s/results/.progress/%s.jsonl" % (R, name), "--output", out] + (["--no-image"] if cond == "TXT" else []) + (["--instruction", INS, "--instruction-mode", INS_MODE[m]] if m in INS_MODE else [])
            jobs.append({"name": name, "env": "circle", "reserve_mib": res, "output": out, "log": "%s/logs/%s.log" % (R, name), "cmd": cmd, "skip_order": True,
                         "meta": {"line": "%s_ZEROSHOT_%s" % (m, bench), "condition": cond, "base_model": hf, "adapter_dir": None, "input_arrow": arrow, "input_arrow_sha256_expected_prefix": sha, "prompting": note + ((" | instrucao: '%s' (%s)" % (INS, INS_MODE[m])) if m in INS_MODE else ""), "dtype": "auto (LLaVA-Med) / bf16 (Qwen2.5-VL, MedVLThinker) -- med_vlm/models/loader.py",
                                  "inference": "harness.extract_predictions_circle --peft ZEROSHOT" + (" --no-image (braco so-texto, sem aviso ao modelo)" if cond == "TXT" else ""), "rescoring": "answer_matches do harness; E7 (negative->no, positive->yes nas fechadas) aplicada depois por rescore_e7.py"}})
os.makedirs(R + "/results/.progress", exist_ok=True); os.makedirs(R + "/logs", exist_ok=True)
json.dump(jobs, open(OUTFILE, "w"), indent=1); print(len(jobs), "jobs ->", OUTFILE)
