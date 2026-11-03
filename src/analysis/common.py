"""Paths, run list and file lookup shared by the analysis scripts (the single configuration point of the pipeline).

Every location comes from a YAML file: config/paths.yaml at the repository root by default, or the file named by the
environment variable MRN_CONFIG. Relative paths are resolved from the current working directory, so run the scripts from
the repository root. Variable names are kept from the original research code (W, PLC, ISBI, P0, V7T, V7S, V7Z, V7M, V5Q,
V5S, V6) so that the scripts work unchanged; the README glossary maps the internal names to the paper's terms.
Environment overrides: MRN_OUT (output root), MRN_HOST (host name recorded in the JSON outputs; default "not recorded")."""
import hashlib, json, os, re, functools
import yaml
CFG_PATH = os.environ.get("MRN_CONFIG", "config/paths.yaml")
CFG = yaml.safe_load(open(CFG_PATH))
OUT = os.environ.get("MRN_OUT") or CFG["out"]
HOST = os.environ.get("MRN_HOST", "not recorded")
CODE_ROOT = CFG.get("code_root", "src")                       # importable root: med_vlm/, harness/
SCRIPTS = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))   # this directory (analysis scripts)
LAB = CFG.get("lab_root", "local/lab")                         # root of the original lab layout (credentialed data; not distributed)
LAB_INPUTS = CFG.get("lab_inputs", f"{LAB}/v7_artigo1/inputs")   # credentialed inputs (HEAL annotations parquet, Kvasir-VQA-x1 parquet copy)
W = LAB; PLC = f"{W}/doutorado/med-vqa-icdip-placebo"; ISBI = f"{PLC}/results/isbi_placebo"; P0 = f"{W}/doutorado/med-vqa-icdip-p0"
V7T = f"{W}/v7_txt"; V7S = f"{W}/v7_sham"; V7Z = f"{W}/v7_zeroshot"; V7M = f"{W}/v7_mimic"
V5Q = f"{W}/v5_qwen_vt"; V5S = f"{W}/v5_smolvlm_ft"; V6 = f"{W}/v6_tower_heal"
_KV = CFG["kvasir"]; KV_META = _KV["meta"]; KV_OCC_META = _KV["occluder_meta"]
KV_FULL = list(_KV["full_test_predictions"])                  # intact-image predictions on the full test set (occluder test reference)
_HEAL = CFG.get("heal", {}); _MIMIC = CFG.get("mimic", {})
HEAL_META = _HEAL.get("meta", ISBI); MIMIC_META = _MIMIC.get("meta", f"{V7M}/results")
BLUR4_META = CFG["blur4_meta"]; PREV_SHEETS = CFG.get("previous_sheets", "results/previous_sheets")
ZS_DIRS = list(CFG.get("zero_shot_predictions", [])) + [f"{V7Z}/results"]
NOIMG_DIRS = list(CFG.get("no_image_predictions", [])) + [f"{V7T}/results", f"{V7M}/results"]
NOIMG_DORA_DIRS = list(CFG.get("no_image_dora_predictions", [])) + list(CFG.get("lab_no_image_dora_predictions", []))
M3AE_NOIMG_DIRS = list(CFG.get("m3ae_no_image_predictions", [])) + list(CFG.get("lab_m3ae_no_image_predictions", []))
BLUR4_DIRS = list(CFG.get("blur4_predictions", [])) + list(CFG.get("lab_blur4_predictions", []))
LAB_BLUR4_ARROWS = CFG.get("lab_blur4_arrows", f"{LAB}/blur4_arrows")   # fixed-scale blur arrows of the credentialed benchmarks (lab only)
BASES = ["KVASIR", "HEAL", "MIMIC"]
INV = {"KVASIR": f"{KV_META}/inventory_kvasir_test_clean.json", "HEAL": f"{HEAL_META}/inventory_heal_test.json", "MIMIC": f"{MIMIC_META}/inventory_mimic_test.json"}
M0 = {"KVASIR": f"{KV_META}/M0_question_only_KVASIR_C0.json", "HEAL": _HEAL.get("question_only", f"{V7T}/results/M0_question_only_HEAL_aligned.json")}   # MIMIC: composite floor (txt_floors.mimic_floors)
# search directories per benchmark (order = priority; the first existing file wins)
DIRS = {"KVASIR": list(_KV["predictions"]) + [ISBI, f"{V5Q}/results_placebo", f"{V5S}/results_placebo", f"{V5Q}/results", f"{V5S}/results", f"{P0}/results", f"{V7T}/results", f"{V7S}/results"],
        "HEAL": list(_HEAL.get("predictions", [])) + [ISBI, f"{V6}/results_placebo", f"{V6}/results", f"{V7T}/results", f"{V7S}/results"],
        "MIMIC": list(_MIMIC.get("predictions", [])) + [f"{V7M}/results"]}
# Qwen2.5-VL-7B family: 12 more runs per benchmark (LoRA and DoRA, frozen and fine-tuned vision encoder, three seeds), enabled by default;
# A1_FAMILIAS_EXTRA="" restores the 27 runs. Their Kvasir-VQA-x1 predictions are in the same results/predictions/kvasir sub-directories as the
# 2B runs; for the credentialed benchmarks the extra search directories come from the configuration (qwen25vl_7b_predictions,
# lab_qwen25vl_7b_predictions). A1_TESTE_ALIAS=1 is a test switch only: the 7B runs read the files of the corresponding 2B run.
Q7B = list(CFG.get("qwen25vl_7b_predictions", [])) + list(CFG.get("lab_qwen25vl_7b_predictions", []))
FAM_EXTRA = [x for x in os.environ.get("A1_FAMILIAS_EXTRA", "QWEN25VL").split(",") if x]; ALIAS_TESTE = os.environ.get("A1_TESTE_ALIAS") == "1"
if "QWEN25VL" in FAM_EXTRA:
    for _b in DIRS: DIRS[_b] = DIRS[_b] + Q7B
    KV_FULL = KV_FULL + Q7B; NOIMG_DIRS = NOIMG_DIRS + Q7B; NOIMG_DORA_DIRS = NOIMG_DORA_DIRS + Q7B; BLUR4_DIRS = BLUR4_DIRS + Q7B
COND_MAIN = ["C0", "T", "P", "S", "T_blur10", "P_blur10", "S_blur10", "T_regmean", "P_regmean", "S_regmean"]
COND_DOSE = ["T1.5", "P1.5", "T2", "P2"]
COND_OTHER = ["C1"]
SHAM = {"KVASIR": ["C0_cross", "SHAM_ART_black", "SHAM_ART_blur10", "SHAM_POL_Q1_black", "SHAM_POL_Q1_blur10", "SHAM_POL_Q3_black", "SHAM_POL_Q3_blur10", "SHAM_INS_black", "SHAM_INS_blur10"],
        "HEAL": [], "MIMIC": ["SHAM_black", "SHAM_blur10"]}   # HEAL: occluder on negatives = T/P (and _blur10) on the closed_no questions
def first_existing(dirs, name):
    """First existing <dir>/<name> over a list of directories; the first candidate when none exists (so callers report it)."""
    cands = [f"{d}/{name}" for d in dirs]
    return next((p for p in cands if os.path.exists(p)), cands[0])
def lines(base):
    """27 runs (line, family, method, encoder group, seed, origin), plus the 12 Qwen2.5-VL-7B runs when the family is enabled."""
    L = []
    for s in range(3):
        for pe in ("LORA", "DORA"):
            q = f"QWEN2VL_{pe}_{base}_seed{s}" if not (base == "MIMIC" and pe == "LORA") else f"QWEN2VL_LORA_FROZEN_MIMIC_seed{s}"
            L.append(dict(line=q, family="Qwen2-VL-2B", fam="QWEN2VL", method=pe, encoder="congelado", seed=s, pack="15 de 01/10" if base != "MIMIC" else "15 (MIMIC, 11-13/10)"))
            L.append(dict(line=f"SMOLVLM_{pe}_{base}_seed{s}", family="SmolVLM2-2.2B", fam="SMOLVLM", method=pe, encoder="afinado", seed=s, pack="15 de 01/10" if base != "MIMIC" else "15 (MIMIC, 11-13/10)"))
            L.append(dict(line=f"QWEN2VL_{pe}_VT_{base}_seed{s}", family="Qwen2-VL-2B", fam="QWEN2VL", method=pe, encoder="afinado", seed=s, pack="12 de encoder invertido"))
            L.append(dict(line=f"SMOLVLM_{pe}_FT_{base}_seed{s}", family="SmolVLM2-2.2B", fam="SMOLVLM", method=pe, encoder="congelado", seed=s, pack="12 de encoder invertido"))
        L.append(dict(line=f"M3AE_{base}_seed{s}", family="M3AE", fam="M3AE", method="ajuste completo", encoder="ajuste completo", seed=s, pack="15 de 01/10" if base != "MIMIC" else "15 (MIMIC, 11-13/10)"))
    if "QWEN25VL" in FAM_EXTRA:   # only with the family enabled; without it, the usual 27 runs
        for s in range(3):
            for pe in ("LORA", "DORA"):
                L.append(dict(line=f"QWEN25VL_{pe}_{base}_seed{s}", family="Qwen2.5-VL-7B", fam="QWEN25VL", method=pe, encoder="congelado", seed=s, pack="7B (rodadas 21-22)"))
                L.append(dict(line=f"QWEN25VL_{pe}_VT_{base}_seed{s}", family="Qwen2.5-VL-7B", fam="QWEN25VL", method=pe, encoder="afinado", seed=s, pack="7B (rodadas 21-22)"))
    return L
def alias_teste(line):   # test switch only (A1_TESTE_ALIAS=1): 7B run -> corresponding 2B run
    if not (ALIAS_TESTE and line.startswith("QWEN25VL_")): return line
    q = line.replace("QWEN25VL_", "QWEN2VL_")
    return q.replace("QWEN2VL_LORA_MIMIC_", "QWEN2VL_LORA_FROZEN_MIMIC_")
def txt_line(base, fam, s):
    return (f"M3AE_TXT_{base}_seed{s}" if fam == "M3AE" else f"{fam}_LORA_TXT_{base}_seed{s}")
def txt_file(base, fam, s):
    if fam == "QWEN25VL" and ALIAS_TESTE: return txt_file(base, "QWEN2VL", s)
    p = first_existing(NOIMG_DIRS, f"{txt_line(base, fam, s)}_TXT.json")
    return p if os.path.exists(p) else None
DOSE_ALIAS = {"QWEN2VL_DORA_HEAL_seed2": "QWEN2VL_DORA_HEAL_seed2_retrain20261003"}   # dose and C1 conditions of this run come from the 2026-10-03 retraining
def find(base, line, cond):
    names = [alias_teste(line)]
    if cond in COND_DOSE + COND_OTHER and line in DOSE_ALIAS: names = [DOSE_ALIAS[line]]
    for d in DIRS[base]:
        for n in names:
            p = f"{d}/{n}_{cond}.json"
            if os.path.exists(p): return p
    return None
@functools.lru_cache(maxsize=None)
def sha(p):
    if p is None or not os.path.exists(p): return None
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""): h.update(b)
    return h.hexdigest()
def zs_file(m, base, c):
    return first_existing(ZS_DIRS, f"{m}_ZEROSHOT_{base}_{c}" + ("_instr" if m == "MEDVLTHINKER" else "") + ".json")
ZS = ["MEDGEMMA", "QWEN25VL", "LLAVA_MED", "MEDVLTHINKER"]
