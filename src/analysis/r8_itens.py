"""Round 8 (21/10/2026, CPU): checks of the extra runs. Output: analysis/rodada8.json. Nothing re-inferred.
1. L3 and L0 among the declared runs (fine-tuned and zero-shot), per Table 1 class.
3. No-image baseline on the 314 instrument questions of Kvasir: distribution of the predicted and reference answers; answers in the training set.
4. Holm: for each criterion (L0 raw drop, L1 Delta black, L2 Delta blur 10 %, L3 image gain), one-sided bootstrap p = fraction of the 2 000
   per-image replicates (the benchmark's) <= 0; Holm per run over the registered family of classes (Kvasir: polyp, instrument, 'Is there text?'; for
   the 3-template negative control, the same family with it in place of 'Is there text?'; HEAL: yes, no; Medical-Diff-VQA: yes, no and the 6 entities);
   passes if adjusted p < 0.025 (equivalent to the two-sided 95 % CI). Without Holm, the same p < 0.025 is checked against the CI rule.
5. Blur 4 % (fixed sigma 25 px) instead of blur 10 % on the 15 Kvasir runs of 01/10.
7. Training files of the fine-tuning per benchmark."""
import collections, json, os, sys, time
import numpy as np, pyarrow as pa
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
import engine as E, analise_bases as AB
T0 = time.time(); NV2 = f"{OUT}/analysis/necessity_v2"; OUTJ = {"script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "engine_sha256": sha(f"{OUT}/scripts/engine.py")}
TCL = {"KVASIR": ["dependent_polyp", "dependent_instrument", "negative_control"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no"]}
def lo(bk, k): c = (bk or {}).get(k); return c[0] if c else None
def steps(bk):
    L0 = (lo(bk, "custo_alvo_preto_ci_by_image") or 0) > 0; L1 = (lo(bk, "delta_preto_ci_by_image") or 0) > 0; L2 = L1 and (lo(bk, "delta_blur10_ci_by_image") or 0) > 0
    return {"L0": L0, "L1": L1, "L2": L2, "L3": L2 and (lo(bk, "headroom_ci_by_image") or 0) > 0}
REC = {b: [json.load(open(f"{NV2}/{L['line']}_{b}.json")) for L in lines(b)] for b in BASES}
ZREC = {b: [json.load(open(f"{NV2}/{m}_ZEROSHOT_{b}_{b}.json")) for m in ZS] for b in BASES}
# ---- item 1
I1 = {}
for b in BASES:
    for c in TCL[b]:
        for kind, recs in (("afinados", REC[b]), ("zero_shot", ZREC[b])):
            st = {r["line"]: steps(r["by_class"].get(c)) for r in recs if (r["by_class"].get(c) or {}).get("n")}
            I1[f"{b}|{c}|{kind}"] = {"linhas": len(st), "L3": sum(v["L3"] for v in st.values()), "L3_e_L0": sum(v["L3"] and v["L0"] for v in st.values()),
                                     "L3_sem_L0": sorted(k for k, v in st.items() if v["L3"] and not v["L0"]), "L0": sum(v["L0"] for v in st.values()), "L1": sum(v["L1"] for v in st.values()), "L2": sum(v["L2"] for v in st.values()),
                                     "ganham_L0_para_L1": sorted(k for k, v in st.items() if v["L1"] and not v["L0"]), "perdem_L0_para_L1": sorted(k for k, v in st.items() if v["L0"] and not v["L1"]),
                                     "L3_linhas": sorted(k for k, v in st.items() if v["L3"])}
x = I1["MIMIC|closed_yes|afinados"]; OUTJ["item1_mimic_ganham_L0_L1_entre_os_L3"] = {"ganham": x["ganham_L0_para_L1"], "entre_os_L3": [k for k in x["ganham_L0_para_L1"] if k in x["L3_linhas"]]}
OUTJ["item1"] = I1
# ---- item 3
inv = json.load(open(INV["KVASIR"])); QK = {int(q["qid"]): q for q in inv["questions"]}
ins = [r for r in REC["KVASIR"]][0]
qs_ins = sorted(q for q, x in QK.items() if x["evaluable"] and x["question_class"] == "dependent_instrument")
I3 = {"n_avaliaveis": len(qs_ins), "templates": dict(collections.Counter(QK[q]["question"] for q in qs_ins)), "por_arquivo": {}}
gold_all = collections.Counter(); pred_all = collections.Counter()
for fam in ("QWEN2VL", "SMOLVLM", "M3AE"):
    for s in range(3):
        p = txt_file("KVASIR", fam, s); P = {int(x["qid"]): x for x in json.load(open(p))["predictions"]}; qq = [q for q in qs_ins if q in P]
        pc = collections.Counter((QK[q]["question"], P[q]["predicted"]) for q in qq); gc = collections.Counter((QK[q]["question"], P[q]["gold"]) for q in qq)
        I3["por_arquivo"][os.path.basename(p)] = {"sha256": sha(p), "n": len(qq), "acuracia": sum(P[q]["correct"] for q in qq) / len(qq), "previstas": {f"{t} -> {a}": n for (t, a), n in pc.most_common()},
                                                  "referencia_top": {f"{t} -> {a}": n for (t, a), n in gc.most_common(8)}, "referencia_distintas": len(gc), "previstas_distintas": len(pc),
                                                  "previstas_que_aparecem_na_referencia": sum(n for (t, a), n in pc.items() if (t, a) in gc)}
        pred_all.update(pc); gold_all.update(gc)
I3["previstas_9_arquivos"] = {f"{t} -> {a}": n for (t, a), n in pred_all.most_common()}
I3["referencia_por_template"] = {t: {"distintas": len([1 for (tt, a) in gold_all if tt == t]), "top": [(a, n // 9) for (tt, a), n in gold_all.most_common() if tt == t][:6],
                                     "contem_none_ou_0": any(a in ("none", "0") for (tt, a) in gold_all if tt == t)} for t in I3["templates"]}
tr = f"{PLC}/data/finetune_arrows/vqa_kvasir_train_clean.arrow"
with pa.memory_map(tr) as src:
    try: rd = pa.ipc.open_file(src)
    except Exception: rd = pa.ipc.open_stream(pa.memory_map(tr))
    t = rd.read_all().select(["questions", "answers"])
trc = collections.defaultdict(collections.Counter)
for qsl, asl in zip(t.column("questions").to_pylist(), t.column("answers").to_pylist()):
    for q, a in zip(qsl, asl):
        if q in I3["templates"]: trc[q][a[0] if a else ""] += 1
I3["treino_por_template"] = {q: {"n": sum(c.values()), "top": c.most_common(5), "frac_majoritaria": c.most_common(1)[0][1] / sum(c.values())} for q, c in trc.items()}
I3["treino_arquivo"] = {"arquivo": tr, "sha256": sha(tr)}
OUTJ["item3"] = I3
# ---- item 4 Holm
def holm_adj(p):
    k = sorted(p, key=lambda x: p[x]); m = len(k); out = {}; run = 0.0
    for i, key in enumerate(k): run = max(run, min(1.0, (m - i) * p[key])); out[key] = run
    return out
FAM = {"KVASIR": ["dependent_polyp", "dependent_instrument", "controle_texto"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": None}
I4 = {}; consist = collections.Counter()
for b in BASES:
    invb = json.load(open(INV[b])); IMG = {int(q["qid"]): q["image_id"] for q in invb["questions"]}; Bb = E.Base(IMG); G, extra, fam_reg = AB.classes(b, invb)
    fams = {"principal": fam_reg} if b != "KVASIR" else {"principal": fam_reg, "controle_negativo": ["dependent_polyp", "dependent_instrument", "negative_control"]}
    for r in REC[b] + (ZREC[b] if b == "MIMIC" else []):
        C = {c: E.load_correct(p) for c, p in r["files"].items() if c in E.CORE}; TX = E.load_correct(r["txt_file"]) if r.get("txt_file") else None
        core = [c for c in E.CORE if c in C]; al = lambda qs: [q for q in qs if all(q in C[c] for c in core)]
        pv = {}
        for c in set(sum(fams.values(), [])):
            qs = al(G[c]); 
            if not qs: continue
            v = {k: np.array([C[k][q] for q in qs], float) for k in C}; d = {}
            d["L0"] = Bb.reps(qs, v["C0"] - v["T"]); d["L1"] = Bb.reps(qs, v["P"] - v["T"]); d["L2"] = Bb.reps(qs, v["P_blur10"] - v["T_blur10"])
            q2 = [q for q in qs if TX and q in TX]; d["L3"] = Bb.reps(q2, np.array([C["C0"][q] for q in q2], float) - np.array([TX[q] for q in q2], float)) if q2 else None
            pv[c] = {k: (float(np.mean(x <= 0)) if x is not None else 1.0) for k, x in d.items()}
            bk = r["by_class"].get(c) or {}; ci_rule = {"L0": (lo(bk, "custo_alvo_preto_ci_by_image") or 0) > 0, "L1": (lo(bk, "delta_preto_ci_by_image") or 0) > 0,
                                                         "L2": (lo(bk, "delta_blur10_ci_by_image") or 0) > 0, "L3": (lo(bk, "headroom_ci_by_image") or 0) > 0}
            for k in ci_rule: consist["igual" if (pv[c][k] < 0.025) == ci_rule[k] else "diferente"] += 1
        for fname, fl in fams.items():
            for crit in ("L0", "L1", "L2", "L3"):
                adj = holm_adj({c: pv[c][crit] for c in fl if c in pv})
                for c, a in adj.items(): I4.setdefault(f"{b}|{c}|{fname}", {}).setdefault(r["line"], {})[crit] = {"p": pv[c][crit], "p_holm": a}
def count(key, zs=None):
    rows = I4[key]; out = {"sem_holm": collections.Counter(), "com_holm": collections.Counter(), "linhas": 0}
    for ln, x in rows.items():
        if zs is not None and ("ZEROSHOT" in ln) != zs: continue
        out["linhas"] += 1
        for tag, kk in (("sem_holm", "p"), ("com_holm", "p_holm")):
            ok = {k: x[k][kk] < 0.025 for k in x}; L0 = ok["L0"]; L1 = ok["L1"]; L2 = L1 and ok["L2"]; L3 = L2 and ok["L3"]
            out[tag].update({"L0": L0, "L1": L1, "L2": L2, "L3": L3})
    return {"linhas": out["linhas"], "sem_holm": {k: out["sem_holm"][k] for k in ("L0", "L1", "L2", "L3")}, "com_holm": {k: out["com_holm"][k] for k in ("L0", "L1", "L2", "L3")}}
OUTJ["item4"] = {"regra": "p unilateral bootstrap (replicas <= 0) por criterio; Holm por linha sobre a familia; passa se p ajustado < 0,025",
                 "familias": {"KVASIR": FAM["KVASIR"], "KVASIR_controle_negativo": ["dependent_polyp", "dependent_instrument", "negative_control"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": "closed_yes, closed_no e as 6 entidades (familia_holm de bases_raw)"},
                 "consistencia_p_menor_0025_vs_regra_do_IC": dict(consist),
                 "tabela1": {"KVASIR|dependent_polyp": count("KVASIR|dependent_polyp|principal"), "KVASIR|dependent_instrument": count("KVASIR|dependent_instrument|principal"),
                             "KVASIR|negative_control": count("KVASIR|negative_control|controle_negativo"), "HEAL|closed_yes": count("HEAL|closed_yes|principal"), "HEAL|closed_no": count("HEAL|closed_no|principal"),
                             "MIMIC|closed_yes": count("MIMIC|closed_yes|principal", zs=False), "MIMIC|closed_no": count("MIMIC|closed_no|principal", zs=False), "MIMIC|closed_yes|zero_shot": count("MIMIC|closed_yes|principal", zs=True)}}
# ---- item 5 blur 4 %
invk = json.load(open(INV["KVASIR"])); IMG = {int(q["qid"]): q["image_id"] for q in invk["questions"]}; Bk = E.Base(IMG); G, extra, _ = AB.classes("KVASIR", invk)
pk = {L["line"]: L["pack"] for L in lines("KVASIR")}; I5 = {"linhas": {}, "contagens": {}}
for r in REC["KVASIR"]:
    if not pk[r["line"]].startswith("15 de"): continue
    pt, pp_ = f"{ISBI}/{r['line']}_T_blur.json", f"{ISBI}/{r['line']}_P_blur.json"
    C = {c: E.load_correct(p) for c, p in r["files"].items() if c in E.CORE}; C4 = {"C0": C["C0"], "T": E.load_correct(pt), "P": E.load_correct(pp_)}
    I5["linhas"][r["line"]] = {"sha256": {"T_blur": sha(pt), "P_blur": sha(pp_)}}
    for c in TCL["KVASIR"]:
        qs = [q for q in G[c] if all(q in C[k] for k in E.CORE) and q in C4["T"] and q in C4["P"]]; b4 = E.block(Bk, qs, C4); bk = r["by_class"][c]
        s10 = steps(bk); L2b4 = s10["L1"] and (lo(b4, "delta_preto_ci_by_image") or 0) > 0; L3b4 = L2b4 and (lo(bk, "headroom_ci_by_image") or 0) > 0
        I5["linhas"][r["line"]][c] = {"n_blur4": b4["n"], "n_classe": bk["n"], "delta_blur4": b4["delta_preto"], "delta_blur4_ci": b4["delta_preto_ci_by_image"], "L2_blur10": s10["L2"], "L3_blur10": s10["L3"], "L2_blur4": L2b4, "L3_blur4": L3b4}
for c in TCL["KVASIR"]:
    xs = [v[c] for v in I5["linhas"].values()]
    I5["contagens"][c] = {"linhas": len(xs), "n_blur4": sorted({x["n_blur4"] for x in xs}), "n_classe": sorted({x["n_classe"] for x in xs}), "L2_blur10": sum(x["L2_blur10"] for x in xs), "L3_blur10": sum(x["L3_blur10"] for x in xs),
                          "L2_blur4": sum(x["L2_blur4"] for x in xs), "L3_blur4": sum(x["L3_blur4"] for x in xs), "delta_blur4_min": min(x["delta_blur4"] for x in xs), "delta_blur4_max": max(x["delta_blur4"] for x in xs)}
OUTJ["item5"] = I5
# ---- item 7
def arrow_info(p):
    with pa.memory_map(p) as src:
        try: rd = pa.ipc.open_file(src)
        except Exception: rd = pa.ipc.open_stream(pa.memory_map(p))
        t = rd.read_all().select(["questions"])
    return {"arquivo": p, "sha256": sha(p), "bytes": os.path.getsize(p), "imagens": t.num_rows, "pares_pergunta_resposta": sum(len(x) for x in t.column("questions").to_pylist())}
FA = f"{PLC}/data/finetune_arrows"
OUTJ["item7"] = {"KVASIR": {sp: arrow_info(f"{FA}/vqa_kvasir_{sp}_clean.arrow") for sp in ("train", "val")}, "HEAL": {sp: arrow_info(f"{FA}/vqa_heal_{sp}.arrow") for sp in ("train", "val")},
                 "MIMIC": {sp: arrow_info(f"{V7M}/data/vqa_mimic_{sp}.arrow") for sp in ("train", "val")},
                 "nota": "HEAL: data/finetune_arrows/vqa_heal_train.arrow e data/isbi_placebo/vqa_heal_train.arrow sao o mesmo arquivo (hard link, mesmo sha); gerado por harness/isbi_placebo/heal/make_heal_train_arrows.py. Medical-Diff-VQA: tabela de itens v7_mimic/data/items_train.parquet."}
OUTJ["item7"]["MIMIC"]["items_train_parquet"] = {"arquivo": f"{V7M}/data/items_train.parquet", "sha256": sha(f"{V7M}/data/items_train.parquet")}
OUTJ["t"] = time.strftime("%Y-%m-%d %H:%M:%S"); OUTJ["segundos"] = round(time.time() - T0)
json.dump(OUTJ, open(f"{OUT}/analysis/rodada8.json", "w"), indent=1, default=lambda o: list(o) if isinstance(o, (set, tuple)) else str(o))
print("segundos", OUTJ["segundos"])
for k, v in I1.items(): print("I1", k, {kk: v[kk] for kk in ("linhas", "L0", "L1", "L2", "L3", "L3_e_L0")}, "L3 sem L0:", v["L3_sem_L0"])
print("MIMIC ganham L0->L1:", OUTJ["item1_mimic_ganham_L0_L1_entre_os_L3"])
print("I3 previstas:", I3["previstas_9_arquivos"]); print("I3 acuracias:", {k: v["acuracia"] for k, v in I3["por_arquivo"].items()}); print("I3 ref:", json.dumps(I3["referencia_por_template"])); print("I3 treino:", json.dumps(I3["treino_por_template"]))
print("I4 consistencia:", dict(consist)); [print("I4", k, v) for k, v in OUTJ["item4"]["tabela1"].items()]
[print("I5", k, v) for k, v in I5["contagens"].items()]
print("I7", json.dumps({b: {sp: {k: v[k] for k in ("imagens", "pares_pergunta_resposta", "bytes")} for sp, v in x.items() if isinstance(v, dict) and "imagens" in v} for b, x in OUTJ["item7"].items() if isinstance(x, dict)}))
