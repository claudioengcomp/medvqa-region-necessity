"""Round 14 (22/10/2026, CPU; authors' decision A): final declaration = Delta black and Delta blur 10 % with CI > 0, image gain with CI > 0 and raw
drop (Acc C0 - Acc T) with CI > 0 under black AND under blur 10 %. Recomputed from the predictions (files of each run, engine.block, 2 000 per-image
replicates, seed 20260913, replicates fixed per benchmark), fine-tuned and zero-shot; checked against analysis/necessity_v2. Holm per run over the
Table 1 family (one-sided bootstrap p = fraction of replicates <= 0; passes if adjusted p < 0.025) for the five tests. Output: analysis/rodada14.json."""
import collections, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
import engine as E, analise_bases as AB
T0 = time.time(); NV2 = f"{OUT}/analysis/necessity_v2"
TCL = {"KVASIR": ["dependent_polyp", "dependent_instrument", "negative_control"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no"]}
def lo(c): return c[0] if c else None
def holm_adj(p):
    k = sorted(p, key=lambda x: p[x]); m = len(k); out = {}; run = 0.0
    for i, key in enumerate(k): run = max(run, min(1.0, (m - i) * p[key])); out[key] = run
    return out
TESTS = ("L0_preto", "L0_blur10", "L1_preto", "L2_blur10", "ganho")
OUTJ = {"t": None, "script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "regra": "declarado = Delta preto e Delta blur 10 % (IC > 0), image gain (IC > 0) e queda bruta sob preto e sob blur 10 % (IC > 0)", "por_linha": {}, "conferencia_necessity_v2": collections.Counter()}
for b in BASES:
    inv = json.load(open(INV[b])); IMG = {int(q["qid"]): q["image_id"] for q in inv["questions"]}; Bb = E.Base(IMG); G, extra, _ = AB.classes(b, inv)
    cls = TCL[b] + ([k for k in G if k.startswith("entidade=")] if b == "MIMIC" else [])
    recs = [(L["line"], False, f"{L['family']}, encoder {L['encoder']}") for L in lines(b)] + [(f"{m}_ZEROSHOT_{b}", True, m) for m in ZS]
    for ln, zs, grp in recs:
        r = json.load(open(f"{NV2}/{ln}_{b}.json")); C = {c: E.load_correct(p) for c, p in r["files"].items() if c in E.CORE}; TX = E.load_correct(r["txt_file"]) if r.get("txt_file") else None
        core = [c for c in E.CORE if c in C]; rec = {"zero_shot": zs, "grupo": grp, "classes": {}}
        for c in cls:
            qs = [q for q in G[c] if all(q in C[k] for k in core)]
            if not qs: continue
            bk = E.block(Bb, qs, C, TX); v = {k: np.array([C[k][q] for q in qs], float) for k in C}
            reps = {"L0_preto": Bb.reps(qs, v["C0"] - v["T"]), "L0_blur10": Bb.reps(qs, v["C0"] - v["T_blur10"]), "L1_preto": Bb.reps(qs, v["P"] - v["T"]), "L2_blur10": Bb.reps(qs, v["P_blur10"] - v["T_blur10"])}
            q2 = [q for q in qs if TX and q in TX]; reps["ganho"] = Bb.reps(q2, np.array([C["C0"][q] for q in q2], float) - np.array([TX[q] for q in q2], float)) if q2 else None
            ok = {"L0_preto": (lo(bk.get("custo_alvo_preto_ci_by_image")) or 0) > 0, "L0_blur10": (lo(bk.get("custo_alvo_blur10_ci_by_image")) or 0) > 0, "L1_preto": (lo(bk.get("delta_preto_ci_by_image")) or 0) > 0,
                  "L2_blur10": (lo(bk.get("delta_blur10_ci_by_image")) or 0) > 0, "ganho": (lo(bk.get("headroom_ci_by_image")) or 0) > 0}
            old = r["by_class"].get(c) or {}
            for k in ("delta_preto_ci_by_image", "delta_blur10_ci_by_image", "custo_alvo_preto_ci_by_image", "custo_alvo_blur10_ci_by_image", "headroom_ci_by_image"):
                OUTJ["conferencia_necessity_v2"]["igual" if old.get(k) == bk.get(k) else "diferente"] += 1
            rec["classes"][c] = {"n": bk["n"], "delta_preto": bk.get("delta_preto"), "custo_alvo_blur10": bk.get("custo_alvo_blur10"), "custo_alvo_blur10_ci": bk.get("custo_alvo_blur10_ci_by_image"),
                                 "testes_ic": ok, "p": {k: (float(np.mean(x <= 0)) if x is not None else 1.0) for k, x in reps.items()},
                                 "declarado_regra_final": all(ok.values()), "declarado_rodada11": ok["L0_preto"] and ok["L1_preto"] and ok["L2_blur10"] and ok["ganho"]}
        fam = TCL[b]
        for k in TESTS:
            adj = holm_adj({c: rec["classes"][c]["p"][k] for c in fam if c in rec["classes"]})
            for c, a in adj.items(): rec["classes"][c].setdefault("p_holm_tabela1", {})[k] = a
        for c in fam:
            if c in rec["classes"]: rec["classes"][c]["declarado_holm_tabela1"] = all(rec["classes"][c]["p_holm_tabela1"][k] < 0.025 for k in TESTS)
        OUTJ["por_linha"][f"{b}|{ln}"] = rec
    print(b, round(time.time() - T0), "s", flush=True)
CR = json.load(open(f"{OUT}/analysis/criterio.json")); RES = {}; GRP = {}; ENT = {}; MAXD = {}
for b in BASES:
    for c in TCL[b]:
        for kind in ("afinados", "zero_shot"):
            xs = [(k, v["classes"][c]) for k, v in OUTJ["por_linha"].items() if k.startswith(b + "|") and v["zero_shot"] == (kind == "zero_shot") and c in v["classes"]]
            RES[f"{b}|{c}|{kind}"] = {"linhas": len(xs), "declarados_regra_final": sum(x["declarado_regra_final"] for _, x in xs), "declarados_rodada11": sum(x["declarado_rodada11"] for _, x in xs),
                                       "declarados_holm_tabela1": sum(x["declarado_holm_tabela1"] for _, x in xs), "resoluveis": sum(x["testes_ic"]["ganho"] for _, x in xs),
                                       "perdidos_pela_queda_sob_blur": [{"linha": k.split("|")[1], "queda_bruta_blur10": x["custo_alvo_blur10"], "ic": x["custo_alvo_blur10_ci"]} for k, x in xs if x["declarado_rodada11"] and not x["declarado_regra_final"]]}
        g = collections.OrderedDict()
        for k, v in OUTJ["por_linha"].items():
            if not k.startswith(b + "|") or v["zero_shot"]: continue
            y = g.setdefault(v["grupo"], {"declarados_regra_final": 0, "declarados_rodada11": 0, "runs": 0, "resoluveis": CR["bases"][b]["por_classe"][c].get("por_grupo", {}).get(v["grupo"], {}).get("resoluveis")})
            y["runs"] += 1; y["declarados_regra_final"] += v["classes"][c]["declarado_regra_final"]; y["declarados_rodada11"] += v["classes"][c]["declarado_rodada11"]
        GRP[f"{b}|{c}"] = g
        dec = [v["classes"][c]["delta_preto"] for k, v in OUTJ["por_linha"].items() if k.startswith(b + "|") and not v["zero_shot"] and v["classes"][c]["declarado_regra_final"]]
        al = [v["classes"][c]["delta_preto"] for k, v in OUTJ["por_linha"].items() if k.startswith(b + "|") and not v["zero_shot"]]
        MAXD[f"{b}|{c}"] = {"declarados": len(dec), "max_delta_preto_declarados": max(dec) if dec else None, "max_delta_preto_27": max(al)}
for k, v in OUTJ["por_linha"].items():
    if not k.startswith("MIMIC|") or v["zero_shot"]: continue
    for c, x in v["classes"].items():
        if c.startswith("entidade="):
            e = ENT.setdefault(c.split("=", 1)[1], {"perguntas": x["n"], "ganho_significativo": 0, "declarados_regra_final": 0, "runs": 0}); e["runs"] += 1; e["ganho_significativo"] += x["testes_ic"]["ganho"]; e["declarados_regra_final"] += x["declarado_regra_final"]
OUTJ.update({"contagens": RES, "por_grupo": GRP, "entidades_mimic": ENT, "max_delta": MAXD, "t": time.strftime("%Y-%m-%d %H:%M:%S"), "segundos": round(time.time() - T0)}); OUTJ["conferencia_necessity_v2"] = dict(OUTJ["conferencia_necessity_v2"])
json.dump(OUTJ, open(f"{OUT}/analysis/rodada14.json", "w"), indent=1)
print("conferencia", OUTJ["conferencia_necessity_v2"])
for k, v in RES.items(): print(k, {kk: vv for kk, vv in v.items() if kk != "perdidos_pela_queda_sob_blur"}, v["perdidos_pela_queda_sob_blur"])
for k, v in GRP.items(): print(k, {g: (y["declarados_regra_final"], y["declarados_rodada11"], y["resoluveis"], y["runs"]) for g, y in v.items()})
for k, v in ENT.items(): print(k, v)
for k, v in MAXD.items(): print(k, v)
