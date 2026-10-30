"""Round 9, item 1 (21/10/2026, CPU): Holm with two families, on the same one-sided bootstrap p values of round 8 (recomputed here with the same
code and the same per-image replicates; now stored per run, class and criterion). Variants:
  'rodada8' (8 tests on Medical-Diff-VQA): Kvasir polyp and instrument with {polyp, instrument, 'Is there text?'}, negative control with {polyp,
     instrument, negative control}; HEAL {yes, no}; Medical-Diff-VQA {yes, no, 6 entities};
  'tabela1': only the rows of Table 1 -- Kvasir {polyp, instrument, negative control}; HEAL {yes, no}; Medical-Diff-VQA {yes, no}.
Fine-tuned and zero-shot on the three benchmarks. Disagreements per class between p < 0.025 and the CI rule. Output: analysis/holm_familias.json."""
import collections, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
import engine as E, analise_bases as AB
T0 = time.time(); NV2 = f"{OUT}/analysis/necessity_v2"
def lo(bk, k): c = (bk or {}).get(k); return c[0] if c else None
CIK = {"L0": "custo_alvo_preto_ci_by_image", "L1": "delta_preto_ci_by_image", "L2": "delta_blur10_ci_by_image", "L3": "headroom_ci_by_image"}
TCL = {"KVASIR": ["dependent_polyp", "dependent_instrument", "negative_control"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no"]}
P = {}; CI = {}
for b in BASES:
    inv = json.load(open(INV[b])); IMG = {int(q["qid"]): q["image_id"] for q in inv["questions"]}; Bb = E.Base(IMG); G, extra, fam_reg = AB.classes(b, inv)
    need = sorted(set(fam_reg) | set(TCL[b]) | ({"controle_texto"} if b == "KVASIR" else set()))
    recs = [json.load(open(f"{NV2}/{L['line']}_{b}.json")) for L in lines(b)] + [json.load(open(f"{NV2}/{m}_ZEROSHOT_{b}_{b}.json")) for m in ZS]
    for r in recs:
        C = {c: E.load_correct(p) for c, p in r["files"].items() if c in E.CORE}; TX = E.load_correct(r["txt_file"]) if r.get("txt_file") else None
        core = [c for c in E.CORE if c in C]
        for c in need:
            qs = [q for q in G[c] if all(q in C[k] for k in core)]
            if not qs or not all(k in C for k in ("C0", "T", "P", "T_blur10", "P_blur10")): continue
            v = {k: np.array([C[k][q] for q in qs], float) for k in C}
            d = {"L0": Bb.reps(qs, v["C0"] - v["T"]), "L1": Bb.reps(qs, v["P"] - v["T"]), "L2": Bb.reps(qs, v["P_blur10"] - v["T_blur10"])}
            q2 = [q for q in qs if TX and q in TX]; d["L3"] = Bb.reps(q2, np.array([C["C0"][q] for q in q2], float) - np.array([TX[q] for q in q2], float)) if q2 else None
            P[(b, r["line"], c)] = {k: (float(np.mean(x <= 0)) if x is not None else 1.0) for k, x in d.items()}
            bk = r["by_class"].get(c) or {}; CI[(b, r["line"], c)] = {k: (lo(bk, CIK[k]) or 0) > 0 for k in CIK}
def holm_adj(p):
    k = sorted(p, key=lambda x: p[x]); m = len(k); out = {}; run = 0.0
    for i, key in enumerate(k): run = max(run, min(1.0, (m - i) * p[key])); out[key] = run
    return out
FAM = {"rodada8": {"KVASIR": {"dependent_polyp": ["dependent_polyp", "dependent_instrument", "controle_texto"], "dependent_instrument": ["dependent_polyp", "dependent_instrument", "controle_texto"], "negative_control": ["dependent_polyp", "dependent_instrument", "negative_control"]},
                   "HEAL": {c: ["closed_yes", "closed_no"] for c in TCL["HEAL"]}, "MIMIC": None},
       "tabela1": {"KVASIR": {c: TCL["KVASIR"] for c in TCL["KVASIR"]}, "HEAL": {c: TCL["HEAL"] for c in TCL["HEAL"]}, "MIMIC": {c: TCL["MIMIC"] for c in TCL["MIMIC"]}}}
mimic_fam8 = json.load(open(f"{OUT}/analysis/bases_raw.json"))["bases"]["MIMIC"]["familia_holm"]; FAM["rodada8"]["MIMIC"] = {c: mimic_fam8 for c in TCL["MIMIC"]}
def verdict(ok): L1 = ok["L1"]; L2 = L1 and ok["L2"]; return {"L0": ok["L0"], "L1": L1, "L2": L2, "L3": L2 and ok["L3"]}
RES = {}; LIN = {}
for var, fams in FAM.items():
    for b in BASES:
        lines_b = sorted({ln for (bb, ln, c) in P if bb == b})
        for c in TCL[b]:
            fam = fams[b][c]; cnt = {"afinados": collections.Counter(), "zero_shot": collections.Counter()}; nl = collections.Counter()
            for ln in lines_b:
                if (b, ln, c) not in P: continue
                kind = "zero_shot" if "ZEROSHOT" in ln else "afinados"; nl[kind] += 1
                adj = {k: holm_adj({cc: P[(b, ln, cc)][k] for cc in fam if (b, ln, cc) in P})[c] for k in ("L0", "L1", "L2", "L3")}
                vh = verdict({k: adj[k] < 0.025 for k in adj}); cnt[kind].update({k: int(vv) for k, vv in vh.items()})
                LIN.setdefault(var, {}).setdefault(f"{b}|{c}", {})[ln] = {"p": P[(b, ln, c)], "p_holm": adj, "veredito_holm": vh}
            for kind in cnt: RES.setdefault(var, {})[f"{b}|{c}|{kind}"] = {"linhas": nl[kind], **{k: cnt[kind][k] for k in ("L0", "L1", "L2", "L3")}, "familia": fam}
SEM = {}; DIS = {}
for (b, ln, c), p in P.items():
    if c not in TCL[b]: continue
    kind = "zero_shot" if "ZEROSHOT" in ln else "afinados"; key = f"{b}|{c}|{kind}"
    vs = verdict({k: p[k] < 0.025 for k in p}); s = SEM.setdefault(key, collections.Counter()); s.update({k: int(v) for k, v in vs.items()}); s["linhas"] += 1
    d = DIS.setdefault(key, {"testes": 0, "discordam": 0, "casos": []})
    for k in ("L0", "L1", "L2", "L3"):
        d["testes"] += 1
        if (p[k] < 0.025) != CI[(b, ln, c)][k]: d["discordam"] += 1; d["casos"].append({"linha": ln, "criterio": k, "p": p[k], "ic_inf_maior_0": CI[(b, ln, c)][k]})
out = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "regra": "p unilateral bootstrap = fracao das 2 000 replicas por imagem <= 0; Holm por linha e criterio sobre a familia; passa se p ajustado < 0,025",
       "familias": {v: {b: {c: f for c, f in x.items()} for b, x in fams.items()} for v, fams in FAM.items()}, "contagens": RES, "sem_holm": {k: dict(v) for k, v in SEM.items()}, "discordancias_p_vs_IC": DIS, "por_linha": LIN, "segundos": round(time.time() - T0)}
json.dump(out, open(f"{OUT}/analysis/holm_familias.json", "w"), indent=1)
r8 = json.load(open(f"{OUT}/analysis/rodada8.json"))["item4"]["tabela1"]
for k, x in r8.items():
    b, c = k.split("|")[:2]; kind = "zero_shot" if k.endswith("zero_shot") else "afinados"; y = RES["rodada8"][f"{b}|{c}|{kind}"]
    print("confere r8", k, "OK" if all(x["com_holm"][d] == y[d] for d in ("L0", "L1", "L2", "L3")) else f"DIFERE {x['com_holm']} {y}")
for k in RES["tabela1"]: print(k, "r8:", [RES["rodada8"][k][d] for d in ("L0", "L1", "L2", "L3")], "tab1:", [RES["tabela1"][k][d] for d in ("L0", "L1", "L2", "L3")], "sem:", [SEM[k][d] for d in ("L0", "L1", "L2", "L3")], "de", RES["tabela1"][k]["linhas"], "| discordam", DIS[k]["discordam"], "/", DIS[k]["testes"])
print("segundos", out["segundos"])
