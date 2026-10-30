"""Round 15 (22/10/2026, CPU): final rule with blur 4 % instead of blur 10 %: Delta black > 0, Delta blur4 > 0, image gain > 0 and raw drop > 0
under black and under blur 4 % (all by the lower bound of the per-image 95 % CI; engine.block, 2 000 replicates, seed 20260913, replicates fixed
per benchmark). Blur 4 % = T_blur/P_blur (Kvasir: the 15 runs of 01/10 in results/isbi_placebo; the others in v7_txt/extra_runs/blur4_r10/results).
Items aligned as in round 10 (main conditions of the run and the two blur 4 % conditions). HEAL QWEN2VL_DORA_HEAL_seed2 excluded (retrained adapter).
Zero-shot: only if T_blur/P_blur predictions exist. Output: analysis/rodada15.json."""
import glob, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
import engine as E, analise_bases as AB
T0 = time.time(); NV2 = f"{OUT}/analysis/necessity_v2"; TASK = BLUR4_DIRS
TCL = {"KVASIR": ["dependent_polyp", "dependent_instrument", "negative_control"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no"]}
EXCL = {("HEAL", "QWEN2VL_DORA_HEAL_seed2")}
def lo(bk, k): c = (bk or {}).get(k); return c[0] if c else None
def b4file(line, c):
    for p in [f"{d}/{line}_{c}.json" for d in DIRS["KVASIR"] + DIRS["HEAL"] + DIRS["MIMIC"] + TASK + ZS_DIRS]:
        if os.path.exists(p): return p
    return None
OUTJ = {"script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "regra": "regra final com blur 4 %: Delta preto, Delta blur 4 %, image gain, queda bruta sob preto e queda bruta sob blur 4 %, todos com IC > 0", "por_linha": {}, "contagens": {}, "zero_shot_sem_predicoes": []}
for b in BASES:
    inv = json.load(open(INV[b])); IMG = {int(q["qid"]): q["image_id"] for q in inv["questions"]}; Bb = E.Base(IMG); G, extra, _ = AB.classes(b, inv)
    recs = [(L["line"], False) for L in lines(b)] + [(f"{m}_ZEROSHOT_{b}", True) for m in ZS]
    for ln, zs in recs:
        pt, pp_ = b4file(ln, "T_blur"), b4file(ln, "P_blur")
        if not (pt and pp_):
            if zs: OUTJ["zero_shot_sem_predicoes"].append(f"{b}|{ln}")
            continue
        r = json.load(open(f"{NV2}/{ln}_{b}.json")); C = {c: E.load_correct(p) for c, p in r["files"].items() if c in E.CORE}; C4 = {"C0": C["C0"], "T": E.load_correct(pt), "P": E.load_correct(pp_)}
        rec = {"zero_shot": zs, "fora": (b, ln) in EXCL, "classes": {}}
        for c in TCL[b]:
            qs = [q for q in G[c] if all(q in C[k] for k in E.CORE) and q in C4["T"] and q in C4["P"]]; b4 = E.block(Bb, qs, C4); bk = r["by_class"][c]
            t = {"L0_preto": (lo(bk, "custo_alvo_preto_ci_by_image") or 0) > 0, "L1_preto": (lo(bk, "delta_preto_ci_by_image") or 0) > 0, "ganho": (lo(bk, "headroom_ci_by_image") or 0) > 0,
                 "delta_blur4": (lo(b4, "delta_preto_ci_by_image") or 0) > 0, "L0_blur4": (lo(b4, "custo_alvo_preto_ci_by_image") or 0) > 0}
            rec["classes"][c] = {"testes": t, "declarado_final_blur4": all(t.values()), "declarado_s14": t["L1_preto"] and t["delta_blur4"] and t["ganho"] and t["L0_preto"],
                                 "queda_bruta_blur4": b4["custo_alvo_preto"], "queda_bruta_blur4_ci": b4["custo_alvo_preto_ci_by_image"], "n_blur4": b4["n"]}
        OUTJ["por_linha"][f"{b}|{ln}"] = rec
    for c in TCL[b]:
        for kind in ("afinados", "zero_shot"):
            xs = [(k, v["classes"][c]) for k, v in OUTJ["por_linha"].items() if k.startswith(b + "|") and v["zero_shot"] == (kind == "zero_shot") and not v["fora"]]
            if not xs: continue
            OUTJ["contagens"][f"{b}|{c}|{kind}"] = {"runs": len(xs), "declarados_final_blur4": sum(x["declarado_final_blur4"] for _, x in xs), "declarados_s14": sum(x["declarado_s14"] for _, x in xs),
                                                    "saem_so_pela_queda_bruta_blur4": [{"linha": k.split("|")[1], "queda_bruta_blur4": x["queda_bruta_blur4"], "ic": x["queda_bruta_blur4_ci"]} for k, x in xs if x["declarado_s14"] and not x["declarado_final_blur4"]]}
s14 = json.load(open(f"{OUT}/analysis/blur4_r10.json"))["contagens"]
OUTJ["confere_s14"] = {k: [OUTJ["contagens"][k.replace("|27_runs", "|afinados")]["declarados_s14"], v["L3_blur4_e_L0"]] for k, v in s14.items() if k.endswith("|27_runs")}
OUTJ["t"] = time.strftime("%Y-%m-%d %H:%M:%S"); OUTJ["segundos"] = round(time.time() - T0)
json.dump(OUTJ, open(f"{OUT}/analysis/rodada15.json", "w"), indent=1)
print("confere S14 (agora, rodada 10):", OUTJ["confere_s14"]); print("zero-shot sem predicoes blur 4 %:", OUTJ["zero_shot_sem_predicoes"])
for k, v in OUTJ["contagens"].items(): print(k, v["runs"], v["declarados_final_blur4"], v["declarados_s14"], v["saem_so_pela_queda_bruta_blur4"])
