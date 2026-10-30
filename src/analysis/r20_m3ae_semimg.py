"""Round 20 (23/10/2026, CPU): no-image baseline of M3AE = M3AE without image (variant without an image path; same benchmark and seed), instead of
M3AE with a grey image (authors' decision). LoRA and DoRA as in round 19 (baseline of the same adapter type). Nothing else changes: occlusions, C,
Delta_nec, replicates (2 000, seed 20260913, fixed per benchmark), normalisation. 'atual' = paired G of round 19; 'novo' = the same with the
no-image M3AE. Reads the predictions in their source directory (read-only). txt_file of common.py does not change. Output: analysis/rodada20.json."""
import collections, json, os, statistics, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
import engine as E, analise_bases as AB
T0 = time.time(); NV2 = f"{OUT}/analysis/necessity_v2"; SEMI = M3AE_NOIMG_DIRS
TCL = {"KVASIR": ["dependent_polyp", "dependent_instrument", "negative_control"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no"]}
SHA_REL = {("KVASIR", 0): "1e888b3063159bb8", ("KVASIR", 1): "1e888b3063159bb8", ("KVASIR", 2): "1e888b3063159bb8", ("HEAL", 0): "b0c882cfba5d9de3", ("HEAL", 1): "f892a0585d22055f", ("HEAL", 2): "36f01785dba9b5f0", ("MIMIC", 0): "35f783423fe4925d", ("MIMIC", 1): "c5d0eebe4e69be23", ("MIMIC", 2): "fe62fa295580245f"}   # sha256 of the predictions list (sort_keys, compact JSON) of each no-image M3AE prediction file; the released files carry edited stamps, so the digest covers the predictions only
import hashlib as _hl
def pred_digest(q): return _hl.sha256(json.dumps(json.load(open(q))["predictions"], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
PRED = {}
for (b, s), h in SHA_REL.items():
    p = first_existing(SEMI, f"M3AE_SEMIMG_{b}_seed{s}_TXT.json"); assert pred_digest(p).startswith(h), (p, pred_digest(p)); PRED[(b, s)] = {"arquivo": p, "sha256": sha(p), "predictions_sha256": pred_digest(p)}
def lo(c): return c[0] if c else None
R19 = json.load(open(f"{OUT}/analysis/rodada19.json")); P19 = R19["por_linha"]
R14 = json.load(open(f"{OUT}/analysis/rodada14.json"))["por_linha"]; R15 = json.load(open(f"{OUT}/analysis/rodada15.json"))["por_linha"]
POR = {}; ACC = {}
for b in BASES:
    inv = json.load(open(INV[b])); IMG = {int(q["qid"]): q["image_id"] for q in inv["questions"]}; Bb = E.Base(IMG); G, extra, _ = AB.classes(b, inv)
    for L in lines(b):
        key = f"{b}|{L['line']}"; o = P19[key]; rec = {k: o[k] for k in ("metodo", "familia", "encoder", "grupo", "semente")}; rec["classes"] = {}
        if L["fam"] != "M3AE":
            rec.update(baseline=o["baseline"], baseline_sha256=o["baseline_sha256"], baseline_tipo=o["baseline_tipo"])
            for c, x in o["classes"].items():
                rec["classes"][c] = {**{k: x[k] for k in ("n", "L0p", "L0b", "L1", "L2b")}, "G": x["G"], "G_ci": x["G_ci"], "p_G": x["p_G"], "G_atual": x["G"], "G_atual_ci": x["G_ci"], "p_G_atual": x["p_G"]}
            POR[key] = rec; continue
        r = json.load(open(f"{NV2}/{L['line']}_{b}.json")); C = {c: E.load_correct(p) for c, p in r["files"].items() if c in E.CORE}; core = [c for c in E.CORE if c in C]
        tf = PRED[(b, L["seed"])]["arquivo"]; TX = E.load_correct(tf); TXg = E.load_correct(o["baseline"]); assert set(TX) == set(TXg), (b, L["line"])
        rec.update(baseline=tf, baseline_sha256=sha(tf), baseline_tipo="M3AE sem imagem (variante sem caminho de imagem)", baseline_atual=o["baseline"])
        uni = set()
        for c in G:
            qs = [q for q in G[c] if all(q in C[k] for k in core)]
            if not qs: continue
            bk = E.block(Bb, qs, C, TX); q2 = [q for q in qs if q in TX]; uni |= set(q2)
            reps = Bb.reps(q2, np.array([C["C0"][q] for q in q2], float) - np.array([TX[q] for q in q2], float))
            bg = E.block(Bb, qs, C, TXg); x = o["classes"][c]; assert bg["headroom"] == x["G"] and bg["headroom_ci_by_image"] == x["G_ci"], (key, c)   # reproduces round 19
            rec["classes"][c] = {**{k: x[k] for k in ("n", "L0p", "L0b", "L1", "L2b")}, "G": bk["headroom"], "G_ci": bk["headroom_ci_by_image"], "p_G": float(np.mean(reps <= 0)),
                                 "acc_txt": bk["acc_txt"], "acc_txt_cinza": bg["acc_txt"], "G_atual": x["G"], "G_atual_ci": x["G_ci"], "p_G_atual": x["p_G"]}
        uni = sorted(uni); ACC[key] = {"n_itens": len(uni), "acc_sem_imagem": float(np.mean([TX[q] for q in uni])), "acc_cinza": float(np.mean([TXg[q] for q in uni])),
                                      "por_classe": {c: {"n": y["n"], "sem_imagem": y["acc_txt"], "cinza": y["acc_txt_cinza"], "dif": y["acc_txt"] - y["acc_txt_cinza"]} for c, y in rec["classes"].items()}}
        ACC[key]["dif"] = ACC[key]["acc_sem_imagem"] - ACC[key]["acc_cinza"]
        POR[key] = rec
    print(b, round(time.time() - T0), "s", flush=True)
def crit(x, gkey):
    g = (lo(x[gkey + "_ci"]) or 0) > 0; i = x["L0p"]; ii = x["L1"]; iii = ii and x["L2b"]; iv = iii and g; v = iv and x["L0p"] and x["L0b"]
    return {"i": i, "ii": ii, "iii": iii, "iv": iv, "v": v, "ganho": g}
SG = (("atual", "G_atual"), ("novo", "G"))
T1 = {f"{b}|{c}": {s: {k: sum(crit(v["classes"][c], g)[k] for kk, v in POR.items() if kk.startswith(b + "|")) for k in ("i", "ii", "iii", "iv", "v", "ganho")} for s, g in SG} for b in BASES for c in TCL[b]}
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
    for s, pk in (("atual", "p_G_atual"), ("novo", "p_G")):
        piut = {c: max(p14[c]["p"]["L1_preto"], p14[c]["p"]["L2_blur10"], p14[c]["p"]["L0_preto"], p14[c]["p"]["L0_blur10"], v["classes"][c][pk]) for c in TCL[b]}
        for c, a in holm_adj(piut).items(): HI.setdefault(f"{b}|{c}", {"atual": 0, "novo": 0}); HI[f"{b}|{c}"][s] += int(a < 0.025)
for k in HI: assert HI[k]["atual"] == R19["holm_iut_v"][k]["pareado"], k
B4 = {}
for key, v in R15.items():
    if v["zero_shot"] or v["fora"]: continue
    b = key.split("|")[0]
    for c, x in v["classes"].items():
        t = x["testes"]; y = B4.setdefault(f"{b}|{c}", {"runs": 0, "atual": 0, "novo": 0}); y["runs"] += 1
        for s, g in SG: y[s] += t["L1_preto"] and t["delta_blur4"] and (lo(POR[key]["classes"][c][g + "_ci"]) or 0) > 0 and t["L0_preto"] and t["L0_blur4"]
for k in B4: assert B4[k]["atual"] == R19["blur4_v"][k]["pareado"], k
TX_ = {}
for b in BASES:
    for c in TCL[b]:
        xs = [(k, v["classes"][c]) for k, v in POR.items() if k.startswith(b + "|")]
        TX_[f"{b}|{c}"] = {s: {"min": min(x[g] for _, x in xs), "max": max(x[g] for _, x in xs), "arg_min": min(xs, key=lambda kx: kx[1][g])[0].split("|")[1], "arg_max": max(xs, key=lambda kx: kx[1][g])[0].split("|")[1],
                               "significativos": sum((lo(x[g + "_ci"]) or 0) > 0 for _, x in xs)} for s, g in SG}
CASC = {}
for s, g in SG:
    xs = [(k, v["classes"]["closed_yes"]) for k, v in POR.items() if k.startswith("MIMIC|")]
    ii = [(k, x) for k, x in xs if x["L1"]]; iii = [(k, x) for k, x in ii if x["L2b"]]; iv = [(k, x) for k, x in iii if (lo(x[g + "_ci"]) or 0) > 0]; v_ = [(k, x) for k, x in iv if x["L0p"] and x["L0b"]]
    CASC[s] = {"ii": len(ii), "iii": len(iii), "iv": len(iv), "v": len(v_), "tirados_pela_queda": [k.split("|")[1] for k, x in iv if not (x["L0p"] and x["L0b"])]}
M3 = {k: {c: {"G_atual": x["G_atual"], "G_atual_ci": x["G_atual_ci"], "G": x["G"], "G_ci": x["G_ci"], "p_G": x["p_G"], "sig_atual": crit(x, "G_atual")["ganho"], "sig": crit(x, "G")["ganho"],
              "v_atual": crit(x, "G_atual")["v"], "v": crit(x, "G")["v"]} for c, x in v["classes"].items()} for k, v in POR.items() if v["familia"] == "M3AE"}
OUTJ = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "fonte": {"predicoes_sem_imagem": {f"{b}|seed{s}": v for (b, s), v in PRED.items()}},
        "regra": "G = A_int - A_text; LoRA -> baseline LoRA; DoRA -> baseline DoRA (rodada 17); M3AE -> M3AE sem imagem (variante sem caminho de imagem); IC 95 % por imagem, p unilateral bootstrap",
        "por_linha": POR, "m3ae": M3, "acuracia_sem_imagem_vs_cinza": ACC, "tabela1": T1, "tabela2": T2, "holm_iut_v": HI, "blur4_v": B4, "texto_ganho": TX_, "cascata_mimic_yes": CASC, "segundos": round(time.time() - T0)}
json.dump(OUTJ, open(f"{OUT}/analysis/rodada20.json", "w"), indent=1)
for k, v in T1.items(): print("T1", k, v)
for k, v in T2.items():
    for g, y in v.items():
        if "M3AE" in g: print("T2", k, g, f"{100*y['G_atual']['media']:+.1f} ({100*y['G_atual']['dp']:.1f}) -> {100*y['G']['media']:+.1f} ({100*y['G']['dp']:.1f})", y["declared_atual"], "->", y["declared"])
print("HOLM", HI); print("B4", B4); print("CASC", json.dumps(CASC))
for k, v in TX_.items(): print("TX", k, {s: (round(100*x["min"], 1), x["arg_min"], round(100*x["max"], 1), x["arg_max"], x["significativos"]) for s, x in v.items()})
for k, v in M3.items(): print("M3", k, {c: (round(100*x["G_atual"], 1), round(100*x["G"], 1), [round(100*u, 1) for u in x["G_ci"]], x["sig_atual"], x["sig"], x["v_atual"], x["v"]) for c, x in v.items()})
for k, v in ACC.items(): print("ACC", k, v["n_itens"], round(100*v["acc_sem_imagem"], 2), round(100*v["acc_cinza"], 2), round(100*v["dif"], 2))
