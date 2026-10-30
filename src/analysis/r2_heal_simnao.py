"""Round 2, items 23 and 24 (CPU). 23: HEAL stratified by the geometry of the control (a: image with a single annotated anatomy; b: multi-anatomy
without overlap of the displaced mask with another anatomy; c: multi-anatomy with overlap; analysis/placebo_geometry_heal.json), per run and class
(closed-ended yes and closed-ended no): cost of the displaced mask, Delta black and blur 10 %, per-image CI (replicates of the benchmark). 24: HEAL
and Medical-Diff-VQA, per fine-tuned and zero-shot run: sensitivity (Acc on closed-ended yes), specificity (Acc on closed-ended no), affirmative rate
on closed-ended items, under the conditions intact, target occluded (black, blur 10 %), displaced mask (black, blur 10 %) and text-only arm / no image;
per-image CI. Affirmative = normalize_text(pred) == 'yes' (zero-shot: also 'positive', E7). Outputs: analysis/heal_estratificado.json,
analysis/simnao.json, docs/item23_heal_estratificado.md, docs/item24_simnao.md."""
import collections, glob, json, os, statistics, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
import engine as E
sys.path.insert(0, CODE_ROOT); from med_vlm.metrics.process_text import normalize_text
T0 = time.time(); NV2 = f"{OUT}/analysis/necessity_v2"
def grp(r): return f"{r['family']}, encoder {r['encoder']}" if not r.get("zero_shot") else r["family"]
def ms(xs):
    xs = [x for x in xs if x is not None]
    return None if not xs else {"media": statistics.mean(xs), "dp": statistics.stdev(xs) if len(xs) > 1 else None, "n": len(xs)}
def rec(b): return sorted([json.load(open(f)) for f in glob.glob(f"{NV2}/*_{b}.json")], key=lambda r: r["line"])
# ---------------- 23
inv = json.load(open(INV["HEAL"])); IMG = {int(q["qid"]): q["image_id"] for q in inv["questions"]}; B = E.Base(IMG); CL = {q["qid"]: q["question_class"] for q in inv["questions"] if q["evaluable"]}
geo = json.load(open(f"{OUT}/analysis/placebo_geometry_heal.json")); ST = {}
for u in geo["estrato_por_unidade"]:
    for q in u["qids"]: ST[q] = u["estrato"]
out23 = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "fonte_estrato": f"{OUT}/analysis/placebo_geometry_heal.json", "fonte_estrato_sha256": sha(f"{OUT}/analysis/placebo_geometry_heal.json"), "estrato_unidades": geo["estrato_contagem"],
         "estrato_perguntas": {k: {c: sum(1 for q in ST if ST[q] == k and CL.get(q) == c) for c in ("closed_yes", "closed_no")} for k in sorted(set(ST.values()))}, "linhas": {}, "agregado_por_grupo": {}}
R = [r for r in rec("HEAL") if not r.get("zero_shot")]
for r in R:
    C = {c: E.load_correct(p) for c, p in r["files"].items() if c in E.CORE}; core = [c for c in E.CORE if c in C]
    row = {}
    for k in sorted(set(ST.values())):
        for c in ("closed_yes", "closed_no"):
            qs = [q for q in ST if ST[q] == k and CL.get(q) == c and all(q in C[x] for x in core)]
            bk = E.block(B, qs, C) if qs else {"n": 0}
            row[f"{k}|{c}"] = {x: bk.get(x) for x in ("n", "n_imagens", "custo_mascara_deslocada_preto", "custo_mascara_deslocada_preto_ci_by_image", "custo_mascara_deslocada_blur10", "custo_mascara_deslocada_blur10_ci_by_image", "delta_preto", "delta_preto_ci_by_image", "delta_blur10", "delta_blur10_ci_by_image", "criterio_B")}
    out23["linhas"][r["line"]] = {"grupo": grp(r), "estratos": row}
gg = collections.OrderedDict()
for ln, v in out23["linhas"].items(): gg.setdefault(v["grupo"], []).append(v)
for g, vs in gg.items():
    out23["agregado_por_grupo"][g] = {k: {x: ms([v["estratos"][k].get(x) for v in vs]) for x in ("custo_mascara_deslocada_preto", "custo_mascara_deslocada_blur10", "delta_preto", "delta_blur10")} | {"n": vs[0]["estratos"][k]["n"], "B": sum(1 for v in vs if v["estratos"][k].get("criterio_B")), "n_linhas": len(vs)} for k in vs[0]["estratos"]}
json.dump(out23, open(f"{OUT}/analysis/heal_estratificado.json", "w"), indent=1)
# ---------------- 24
COND = {"intacta": "C0", "alvo_preto": "T", "alvo_blur10": "T_blur10", "mascara_deslocada_preto": "P", "mascara_deslocada_blur10": "P_blur10"}
out24 = {"t": out23["t"], "definicao": "sensibilidade = Acc nas fechadas-sim; especificidade = Acc nas fechadas-nao; taxa afirmativa = P(predicao = sim) nas fechadas avaliaveis (sim + nao); IC 95 % bootstrap por imagem (replicas da base)", "bases": {}}
for b in ("HEAL", "MIMIC"):
    inv = json.load(open(INV[b])); IMG = {int(q["qid"]): q["image_id"] for q in inv["questions"]}; Bb = E.Base(IMG)
    ev = [q for q in inv["questions"] if q["evaluable"] and q["question_class"] in ("closed_yes", "closed_no")]; cy = [q["qid"] for q in ev if q["question_class"] == "closed_yes"]; cn = [q["qid"] for q in ev if q["question_class"] == "closed_no"]
    Bout = {}
    for r in rec(b):
        zs = bool(r.get("zero_shot")); yes = ("yes", "positive") if zs else ("yes",); files = dict(r["files"]); files["texto"] = r.get("txt_file")
        row = {"grupo": grp(r), "zero_shot": zs, "condicoes": {}}
        allc = {k: files.get(v) for k, v in COND.items()} | {"text_only_ou_sem_imagem": files.get("texto")}
        P = {k: {int(x["qid"]): x for x in json.load(open(p))["predictions"]} for k, p in allc.items() if p}
        common = set(q["qid"] for q in ev)
        for k in P: common &= set(P[k])
        y = [q for q in cy if q in common]; n_ = [q for q in cn if q in common]; al = y + n_
        for k, d in P.items():
            sv = np.array([bool(d[q]["correct"]) for q in y], float); sp = np.array([bool(d[q]["correct"]) for q in n_], float); af = np.array([normalize_text(str(d[q]["predicted"])) in yes for q in al], float)
            row["condicoes"][k] = {"n_sim": len(y), "n_nao": len(n_), "sensibilidade": float(sv.mean()) if len(y) else None, "sensibilidade_ci": E.ci(Bb.reps(y, sv)) if len(y) else None,
                                   "especificidade": float(sp.mean()) if len(n_) else None, "especificidade_ci": E.ci(Bb.reps(n_, sp)) if len(n_) else None, "taxa_afirmativa": float(af.mean()), "taxa_afirmativa_ci": E.ci(Bb.reps(al, af))}
        Bout[r["line"]] = row
    gg = collections.OrderedDict()
    for ln, v in Bout.items():
        if not v["zero_shot"]: gg.setdefault(v["grupo"], []).append(v)
    agg = {g: {k: {x: ms([v["condicoes"].get(k, {}).get(x) for v in vs]) for x in ("sensibilidade", "especificidade", "taxa_afirmativa")} for k in vs[0]["condicoes"]} | {"n_linhas": len(vs)} for g, vs in gg.items()}
    out24["bases"][b] = {"linhas": Bout, "agregado_por_grupo": agg}
json.dump(out24, open(f"{OUT}/analysis/simnao.json", "w"), indent=1)
# ---------------- docs
f = lambda x: "—" if x is None else f"{100 * x:+.1f}"; a = lambda x: "—" if x is None else f"{100 * x:.1f}"; ci = lambda c: "" if not c else f"[{100 * c[0]:+.1f}, {100 * c[1]:+.1f}]"; cia = lambda c: "" if not c else f"[{100 * c[0]:.1f}, {100 * c[1]:.1f}]"
msf = lambda m, fn=f: "—" if not m else (f"{fn(m['media'])} ({100 * m['dp']:.1f})" if m.get("dp") is not None else fn(m["media"]))
L = ["# Item 23 — HEAL estratificado pela geometria da máscara deslocada", "", f"Estratos (unidades): {out23['estrato_unidades']}; perguntas por estrato e classe: {out23['estrato_perguntas']}. a = imagem com uma só anatomia anotada; b = várias anatomias, máscara deslocada sem tocar outra anatomia; c = várias anatomias, toca outra. Fonte: `analysis/heal_estratificado.json`; IC por imagem (réplicas da base).", "",
     "## Média (DP) por família × grupo do encoder", "", "| grupo | estrato \\| classe | n | custo desloc. preto (pp) | custo desloc. blur | Δ preto | Δ blur | B |", "|---|---|---|---|---|---|---|---|"]
for g, gv in out23["agregado_por_grupo"].items():
    for k, x in gv.items(): L.append(f"| {g} | {k} | {x['n']} | {msf(x['custo_mascara_deslocada_preto'])} | {msf(x['custo_mascara_deslocada_blur10'])} | {msf(x['delta_preto'])} | {msf(x['delta_blur10'])} | {x['B']}/{x['n_linhas']} |")
L += ["", "## Por linha", "", "| linha | estrato \\| classe | n | custo desloc. preto [IC] | Δ preto [IC] | Δ blur [IC] |", "|---|---|---|---|---|---|"]
for ln, v in out23["linhas"].items():
    for k, x in v["estratos"].items(): L.append(f"| {ln} | {k} | {x['n']} | {f(x['custo_mascara_deslocada_preto'])} {ci(x['custo_mascara_deslocada_preto_ci_by_image'])} | {f(x['delta_preto'])} {ci(x['delta_preto_ci_by_image'])} | {f(x['delta_blur10'])} {ci(x['delta_blur10_ci_by_image'])} |")
open(f"{OUT}/docs/item23_heal_estratificado.md", "w").write("\n".join(L) + "\n")
L = ["# Item 24 — leitura conjunta sim/não", "", out24["definicao"] + ". Fonte: `analysis/simnao.json`.", ""]
for b, Bv in out24["bases"].items():
    L += [f"## {b} — média (DP) por grupo (afinadas)", "", "| grupo | condição | sensibilidade | especificidade | taxa afirmativa |", "|---|---|---|---|---|"]
    for g, gv in Bv["agregado_por_grupo"].items():
        for k, x in gv.items():
            if k == "n_linhas": continue
            L.append(f"| {g} | {k} | {msf(x['sensibilidade'], a)} | {msf(x['especificidade'], a)} | {msf(x['taxa_afirmativa'], a)} |")
    L += ["", f"## {b} — por linha e zero-shot", "", "| linha | condição | n sim/não | sensibilidade [IC] | especificidade [IC] | taxa afirmativa [IC] |", "|---|---|---|---|---|---|"]
    for ln, v in Bv["linhas"].items():
        for k, x in v["condicoes"].items(): L.append(f"| {ln} | {k} | {x['n_sim']}/{x['n_nao']} | {a(x['sensibilidade'])} {cia(x['sensibilidade_ci'])} | {a(x['especificidade'])} {cia(x['especificidade_ci'])} | {a(x['taxa_afirmativa'])} {cia(x['taxa_afirmativa_ci'])} |")
    L.append("")
open(f"{OUT}/docs/item24_simnao.md", "w").write("\n".join(L) + "\n"); print("ok", round(time.time() - T0), "s")
