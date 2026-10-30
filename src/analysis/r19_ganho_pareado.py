"""Round 19 (22/10/2026, CPU): image gain with the no-image baseline of the SAME adapter type (authors' decision): LoRA runs -> LoRA baseline
(the current one); DoRA runs -> DoRA baseline of round 17 (same family, seed and benchmark); M3AE -> grey-image baseline (the current one).
G = A_int - A_text, per-image 95 % CI and one-sided bootstrap p (fraction of the 2 000 replicates <= 0), engine.block and the same replicates fixed
per benchmark. Nothing else changes. Recomputes, with the current G (LoRA for all) and the paired G side by side: Table 1 (criteria i-v), Table 2
(mean (SD) image gain and Declared per group), Holm IUT (round 16), blur 4 % under the final rule (round 15), ranges and text counts, the
Medical-Diff-VQA cascade. Output: analysis/rodada19.json."""
import collections, json, os, statistics, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
import engine as E, analise_bases as AB
T0 = time.time(); NV2 = f"{OUT}/analysis/necessity_v2"; TKD = NOIMG_DORA_DIRS
TCL = {"KVASIR": ["dependent_polyp", "dependent_instrument", "negative_control"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no"]}
def lo(c): return c[0] if c else None
def base_txt(b, L):
    if L["method"] == "DORA": return first_existing(TKD, f"{L['fam']}_DORA_TXT_{b}_seed{L['seed']}_TXT.json"), "DoRA (rodada 17)"
    return txt_file(b, L["fam"], L["seed"]), ("imagem cinza" if L["fam"] == "M3AE" else "LoRA")
R14 = json.load(open(f"{OUT}/analysis/rodada14.json"))["por_linha"]; R15 = json.load(open(f"{OUT}/analysis/rodada15.json"))["por_linha"]
POR = {}
for b in BASES:
    inv = json.load(open(INV[b])); IMG = {int(q["qid"]): q["image_id"] for q in inv["questions"]}; Bb = E.Base(IMG); G, extra, _ = AB.classes(b, inv)
    for L in lines(b):
        r = json.load(open(f"{NV2}/{L['line']}_{b}.json")); C = {c: E.load_correct(p) for c, p in r["files"].items() if c in E.CORE}; core = [c for c in E.CORE if c in C]
        tf, tipo = base_txt(b, L); TX = E.load_correct(tf)
        rec = {"metodo": L["method"], "familia": L["family"], "encoder": L["encoder"], "grupo": f"{L['family']}, encoder {L['encoder']}", "semente": L["seed"], "baseline": tf, "baseline_sha256": sha(tf), "baseline_tipo": tipo, "classes": {}}
        for c in G:
            qs = [q for q in G[c] if all(q in C[k] for k in core)]
            if not qs: continue
            bk = E.block(Bb, qs, C, TX); q2 = [q for q in qs if q in TX]
            reps = Bb.reps(q2, np.array([C["C0"][q] for q in q2], float) - np.array([TX[q] for q in q2], float))
            old = r["by_class"][c]
            rec["classes"][c] = {"n": bk["n"], "G": bk["headroom"], "G_ci": bk["headroom_ci_by_image"], "p_G": float(np.mean(reps <= 0)), "acc_txt": bk["acc_txt"],
                                 "G_atual": old.get("headroom"), "G_atual_ci": old.get("headroom_ci_by_image"),
                                 "L0p": (lo(old.get("custo_alvo_preto_ci_by_image")) or 0) > 0, "L0b": (lo(old.get("custo_alvo_blur10_ci_by_image")) or 0) > 0,
                                 "L1": (lo(old.get("delta_preto_ci_by_image")) or 0) > 0, "L2b": (lo(old.get("delta_blur10_ci_by_image")) or 0) > 0}
            if L["method"] != "DORA": assert rec["classes"][c]["G"] == old.get("headroom") and rec["classes"][c]["G_ci"] == old.get("headroom_ci_by_image"), (b, L["line"], c)
        POR[f"{b}|{L['line']}"] = rec
    print(b, round(time.time() - T0), "s", flush=True)
def crit(x, gkey):
    g = (lo(x[gkey + "_ci"]) or 0) > 0; i = x["L0p"]; ii = x["L1"]; iii = ii and x["L2b"]; iv = iii and g; v = iv and x["L0p"] and x["L0b"]
    return {"i": i, "ii": ii, "iii": iii, "iv": iv, "v": v, "ganho": g}
T1 = {}
for b in BASES:
    for c in TCL[b]:
        xs = [v["classes"][c] for k, v in POR.items() if k.startswith(b + "|")]
        T1[f"{b}|{c}"] = {s: {k: sum(crit(x, "G_atual" if s == "atual" else "G")[k] for x in xs) for k in ("i", "ii", "iii", "iv", "v", "ganho")} for s in ("atual", "pareado")}
def msd(v): return {"media": statistics.mean(v), "dp": statistics.stdev(v) if len(v) > 1 else None, "n": len(v)}
T2 = {}
for b, c in (("KVASIR", "dependent_polyp"), ("KVASIR", "dependent_instrument"), ("HEAL", "closed_yes"), ("MIMIC", "closed_yes")):
    gg = collections.OrderedDict()
    for k, v in POR.items():
        if not k.startswith(b + "|"): continue
        x = v["classes"][c]; y = gg.setdefault(v["grupo"], {"G_atual": [], "G": [], "dec_atual": 0, "dec": 0, "sig_atual": 0, "sig": 0, "runs": 0})
        y["G_atual"].append(x["G_atual"]); y["G"].append(x["G"]); y["runs"] += 1
        ca, cn = crit(x, "G_atual"), crit(x, "G"); y["dec_atual"] += ca["v"]; y["dec"] += cn["v"]; y["sig_atual"] += ca["ganho"]; y["sig"] += cn["ganho"]
    T2[f"{b}|{c}"] = {g: {"G_atual": msd(y["G_atual"]), "G": msd(y["G"]), "declared_atual": f"{y['dec_atual']}/{y['sig_atual']}/{y['runs']}", "declared": f"{y['dec']}/{y['sig']}/{y['runs']}"} for g, y in gg.items()}
def holm_adj(p):
    k = sorted(p, key=lambda x: p[x]); m = len(k); out = {}; run = 0.0
    for i, key in enumerate(k): run = max(run, min(1.0, (m - i) * p[key])); out[key] = run
    return out
HI = {}
for key, v in POR.items():
    b = key.split("|")[0]; p14 = R14[key]["classes"]
    for s in ("atual", "pareado"):
        piut = {c: max(p14[c]["p"]["L1_preto"], p14[c]["p"]["L2_blur10"], p14[c]["p"]["L0_preto"], p14[c]["p"]["L0_blur10"], p14[c]["p"]["ganho"] if s == "atual" else v["classes"][c]["p_G"]) for c in TCL[b]}
        for c, a in holm_adj(piut).items(): HI.setdefault(f"{b}|{c}", {}).setdefault(s, 0); HI[f"{b}|{c}"][s] += int(a < 0.025)
B4 = {}
for key, v in R15.items():
    if v["zero_shot"] or v["fora"]: continue
    b = key.split("|")[0]
    for c, x in v["classes"].items():
        t = x["testes"]; gn = (lo(POR[key]["classes"][c]["G_ci"]) or 0) > 0
        y = B4.setdefault(f"{b}|{c}", {"runs": 0, "atual": 0, "pareado": 0}); y["runs"] += 1; y["atual"] += x["declarado_final_blur4"]
        y["pareado"] += t["L1_preto"] and t["delta_blur4"] and gn and t["L0_preto"] and t["L0_blur4"]
TX_ = {}
for b in BASES:
    for c in TCL[b]:
        xs = [v["classes"][c] for k, v in POR.items() if k.startswith(b + "|")]
        TX_[f"{b}|{c}"] = {s: {"min": min(x[g] for x in xs), "max": max(x[g] for x in xs), "significativos": sum((lo(x[g + "_ci"]) or 0) > 0 for x in xs)} for s, g in (("atual", "G_atual"), ("pareado", "G"))}
CASC = {}
for s, g in (("atual", "G_atual"), ("pareado", "G")):
    xs = [(k, v["classes"]["closed_yes"]) for k, v in POR.items() if k.startswith("MIMIC|")]
    ii = [(k, x) for k, x in xs if x["L1"]]; iii = [(k, x) for k, x in ii if x["L2b"]]; iv = [(k, x) for k, x in iii if (lo(x[g + "_ci"]) or 0) > 0]; v_ = [(k, x) for k, x in iv if x["L0p"] and x["L0b"]]
    CASC[s] = {"ii": len(ii), "iii": len(iii), "iv": len(iv), "v": len(v_), "tirados_pela_queda": [{"linha": k.split("|")[1], "sem_L0_preto": not x["L0p"], "sem_L0_blur": not x["L0b"]} for k, x in iv if not (x["L0p"] and x["L0b"])]}
OUTJ = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "regra": "G pareado: runs LoRA -> baseline LoRA; runs DoRA -> baseline DoRA (rodada 17); M3AE -> imagem cinza; IC 95 % por imagem, p unilateral bootstrap",
        "por_linha": POR, "tabela1": T1, "tabela2": T2, "holm_iut_v": HI, "blur4_v": B4, "texto_ganho": TX_, "cascata_mimic_yes": CASC, "segundos": round(time.time() - T0)}
json.dump(OUTJ, open(f"{OUT}/analysis/rodada19.json", "w"), indent=1)
for k, v in T1.items(): print("T1", k, v)
for k, v in T2.items():
    for g, y in v.items(): print("T2", k, g, f"{100*y['G_atual']['media']:+.1f} ({100*y['G_atual']['dp']:.1f}) -> {100*y['G']['media']:+.1f} ({100*y['G']['dp']:.1f})", y["declared_atual"], "->", y["declared"])
print("HOLM", HI); print("B4", B4); print("CASC", json.dumps(CASC))
for k, v in TX_.items(): print("TX", k, {s: (round(100*x["min"], 1), round(100*x["max"], 1), x["significativos"]) for s, x in v.items()})
