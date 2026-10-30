"""Round 16 (22/10/2026, CPU): Holm as an intersection-union test (IUT). p of the run (per class) = maximum of the five one-sided bootstrap p values
of round 14 (gain; Delta black; Delta blur 10 %; raw drop under black; raw drop under blur 10 %; p = fraction of the 2 000 per-image replicates <= 0);
Holm per run over the Table 1 classes of the benchmark (Kvasir {polyp, instrument, negative control}; HEAL {yes, no}; Medical-Diff-VQA {yes, no});
declared if adjusted p < 0.025. Compared with the per-condition Holm of round 14 (Holm on each of the five tests, then the conjunction).
Output: analysis/rodada16.json."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
R14 = json.load(open(f"{OUT}/analysis/rodada14.json"))
TCL = {"KVASIR": ["dependent_polyp", "dependent_instrument", "negative_control"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no"]}
TESTS = ("ganho", "L1_preto", "L2_blur10", "L0_preto", "L0_blur10")
def holm_adj(p):
    k = sorted(p, key=lambda x: p[x]); m = len(k); out = {}; run = 0.0
    for i, key in enumerate(k): run = max(run, min(1.0, (m - i) * p[key])); out[key] = run
    return out
por, cont, muda = {}, {}, []
for key, v in R14["por_linha"].items():
    b, ln = key.split("|"); fam = [c for c in TCL[b] if c in v["classes"]]
    piut = {c: max(v["classes"][c]["p"][t] for t in TESTS) for c in fam}; adj = holm_adj(piut)
    por[key] = {c: {"p_iut": piut[c], "p_iut_holm": adj[c], "declarado_iut_holm": adj[c] < 0.025, "declarado_holm_por_condicao": v["classes"][c]["declarado_holm_tabela1"],
                    "declarado_sem_holm_IC": v["classes"][c]["declarado_regra_final"], "teste_do_maximo": max(TESTS, key=lambda t: v["classes"][c]["p"][t])} for c in fam}
    for c in fam:
        x = por[key][c]
        if x["declarado_iut_holm"] != x["declarado_holm_por_condicao"]: muda.append({"base": b, "linha": ln, "classe": c, **x})
for b in BASES:
    for c in TCL[b]:
        for kind in ("afinados", "zero_shot"):
            xs = [por[k][c] for k, v in R14["por_linha"].items() if k.startswith(b + "|") and v["zero_shot"] == (kind == "zero_shot") and c in por[k]]
            cont[f"{b}|{c}|{kind}"] = {"runs": len(xs), "iut_holm": sum(x["declarado_iut_holm"] for x in xs), "holm_por_condicao_r14": sum(x["declarado_holm_por_condicao"] for x in xs), "sem_holm_IC": sum(x["declarado_sem_holm_IC"] for x in xs)}
out = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "fonte_p": "analysis/rodada14.json (p unilaterais bootstrap por run, classe e teste)", "fonte_p_sha256": sha(f"{OUT}/analysis/rodada14.json"),
       "regra": "IUT: p do run = maximo dos cinco p unilaterais; Holm por run sobre as classes da Tabela 1 do benchmark; declarado se p ajustado < 0,025", "contagens": cont, "runs_que_mudam_vs_holm_por_condicao": muda, "por_linha": por}
json.dump(out, open(f"{OUT}/analysis/rodada16.json", "w"), indent=1)
for k, v in cont.items(): print(k, v)
print("mudam:", [(m["base"], m["linha"], m["classe"], round(m["p_iut"], 4), round(m["p_iut_holm"], 4), m["declarado_iut_holm"], m["declarado_holm_por_condicao"]) for m in muda])
