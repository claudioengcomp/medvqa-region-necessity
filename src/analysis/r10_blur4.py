"""Round 10, item C5 (CPU, after the GPU step): blur 4 % on the three benchmarks. Delta blur4 = Acc(P_blur) - Acc(T_blur) per run and class, per-image
95 % CI (engine.block, 2 000 replicates, seed 20260913, replicates fixed per benchmark); items aligned to the main conditions of the run and to the
two blur 4 % conditions. Final criterion with blur 4 %: L1 (Delta black) and Delta blur4 with CI > 0 and image gain with CI > 0 (L3_blur4), and also
with the raw drop (L3_blur4 and L0); next to them, the same with blur 10 %. Predictions: the 15 Kvasir runs of 01/10 in results/isbi_placebo; the
others in v7_txt/extra_runs/blur4_r10/results. QWEN2VL_DORA_HEAL_seed2: blur 4 % from the adapter retrained on 03/10 (the original no longer exists)
-- outside the counts (26 runs), values reported separately. Output: analysis/blur4_r10.json."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
import engine as E, analise_bases as AB
T0 = time.time(); NV2 = f"{OUT}/analysis/necessity_v2"; TASK = BLUR4_DIRS
CL = {"KVASIR": ["dependent_polyp", "dependent_instrument", "negative_control"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no"]}
EXCL = {("HEAL", "QWEN2VL_DORA_HEAL_seed2")}
def lo(bk, k): c = (bk or {}).get(k); return c[0] if c else None
def b4file(b, line, c):
    for p in [f"{d}/{line}_{c}.json" for d in DIRS[b] + TASK]:
        if os.path.exists(p): return p
    return None
OUTJ = {"script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "engine_sha256": sha(f"{OUT}/scripts/engine.py"), "por_linha": {}, "contagens": {}, "faltando": []}
for b in BASES:
    inv = json.load(open(INV[b])); IMG = {int(q["qid"]): q["image_id"] for q in inv["questions"]}; Bb = E.Base(IMG); G, extra, _ = AB.classes(b, inv)
    for L in lines(b):
        r = json.load(open(f"{NV2}/{L['line']}_{b}.json")); pt, pp_ = b4file(b, L["line"], "T_blur"), b4file(b, L["line"], "P_blur")
        if not (pt and pp_): OUTJ["faltando"].append(f"{b}|{L['line']}"); continue
        C = {c: E.load_correct(p) for c, p in r["files"].items() if c in E.CORE}; C4 = {"C0": C["C0"], "T": E.load_correct(pt), "P": E.load_correct(pp_)}
        rec = {"pack": L["pack"], "fora_das_contagens": (b, L["line"]) in EXCL, "arquivos": {"T_blur": pt, "P_blur": pp_}, "sha256": {"T_blur": sha(pt), "P_blur": sha(pp_)}}
        for c in CL[b]:
            qs = [q for q in G[c] if all(q in C[k] for k in E.CORE if k in C) and q in C4["T"] and q in C4["P"]]; b4 = E.block(Bb, qs, C4); bk = r["by_class"][c]
            L0 = (lo(bk, "custo_alvo_preto_ci_by_image") or 0) > 0; L1 = (lo(bk, "delta_preto_ci_by_image") or 0) > 0; gain = (lo(bk, "headroom_ci_by_image") or 0) > 0
            b10 = (lo(bk, "delta_blur10_ci_by_image") or 0) > 0; b4ok = (lo(b4, "delta_preto_ci_by_image") or 0) > 0
            rec[c] = {"n_blur4": b4["n"], "n_classe": bk["n"], "delta_blur4": b4["delta_preto"], "delta_blur4_ci": b4["delta_preto_ci_by_image"], "delta_blur10": bk.get("delta_blur10"),
                      "L3_blur10": L1 and b10 and gain, "L3_blur10_e_L0": L1 and b10 and gain and L0, "L3_blur4": L1 and b4ok and gain, "L3_blur4_e_L0": L1 and b4ok and gain and L0, "L2_blur4": L1 and b4ok, "L2_blur10": L1 and b10}
        OUTJ["por_linha"][f"{b}|{L['line']}"] = rec
    for c in CL[b]:
        for nome, sel in (("27_runs", lambda k, v: True), ("15_runs_01_10", lambda k, v: v["pack"].startswith("15 de")), ("12_runs_invertidos", lambda k, v: v["pack"].startswith("12 de"))):
            xs = [v[c] for k, v in OUTJ["por_linha"].items() if k.startswith(b + "|") and not v["fora_das_contagens"] and sel(k, v)]
            if not xs: continue
            OUTJ["contagens"][f"{b}|{c}|{nome}"] = {"runs": len(xs), **{k: sum(x[k] for x in xs) for k in ("L2_blur4", "L2_blur10", "L3_blur4", "L3_blur10", "L3_blur4_e_L0", "L3_blur10_e_L0")},
                                                   "delta_blur4_min": min(x["delta_blur4"] for x in xs), "delta_blur4_max": max(x["delta_blur4"] for x in xs), "n_blur4": sorted({x["n_blur4"] for x in xs}), "n_classe": sorted({x["n_classe"] for x in xs})}
r8 = json.load(open(f"{OUT}/analysis/rodada8.json"))["item5"]["contagens"]
OUTJ["confere_rodada8_kvasir_15"] = {c: {"rodada8": [r8[c]["L3_blur4"], r8[c]["L3_blur10"]], "agora": [OUTJ["contagens"][f"KVASIR|{c}|15_runs_01_10"]["L3_blur4"], OUTJ["contagens"][f"KVASIR|{c}|15_runs_01_10"]["L3_blur10"]]} for c in CL["KVASIR"]}
OUTJ["t"] = time.strftime("%Y-%m-%d %H:%M:%S"); OUTJ["segundos"] = round(time.time() - T0)
json.dump(OUTJ, open(f"{OUT}/analysis/blur4_r10.json", "w"), indent=1)
print("faltando", OUTJ["faltando"]); print("confere r8", OUTJ["confere_rodada8_kvasir_15"])
for k, v in OUTJ["contagens"].items(): print(k, v)
for k, v in OUTJ["por_linha"].items():
    if v["fora_das_contagens"]: print("FORA", k, {c: (v[c]["delta_blur4"], v[c]["delta_blur4_ci"], v[c]["L3_blur4"]) for c in CL[k.split("|")[0]]})
