"""Round 3 (items 28-31, CPU, 19/10/2026): minimum-maximum ranges over the 27 runs; image gain against TF-IDF per group; the box-artefact template
of Kvasir under the single statistical engine (per-image CI, replicates of the benchmark); setup lines. Reads analysis/necessity_v2/*.json,
analysis/doses.json, the test inventories and (for blur 4 % only) the T_blur/P_blur predictions of the 15 runs of 01/10. Output: analysis/rodada3.json."""
import collections, json, os, re, statistics, sys, time
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
import engine as E
NV2 = f"{OUT}/analysis/necessity_v2"; T0 = time.time()
def grp(L): return f"{L['family']}, encoder {L['encoder']}"
def recs(b): return [(L, json.load(open(f"{NV2}/{L['line']}_{b}.json"))) for L in lines(b)]
R = {b: recs(b) for b in BASES}
QTY = [("acc_C0", lambda k: (k.get("acc") or {}).get("C0")), ("acc_txt", lambda k: k.get("acc_txt")), ("headroom", lambda k: k.get("headroom")),
       ("custo_mascara_deslocada_preto", lambda k: k.get("custo_mascara_deslocada_preto")), ("custo_mascara_deslocada_blur10", lambda k: k.get("custo_mascara_deslocada_blur10")),
       ("delta_preto", lambda k: k.get("delta_preto")), ("delta_blur10", lambda k: k.get("delta_blur10")), ("delta_regmean", lambda k: k.get("delta_regmean")),
       ("suficiencia_preto", lambda k: k.get("suficiencia_preto")), ("headroom_m0", lambda k: k.get("headroom_m0")), ("acc_m0", lambda k: k.get("acc_m0"))]
def faixa(b, getblk):
    out = {}
    for q, f in QTY:
        xs = [(L["line"], f(getblk(r) or {})) for L, r in R[b]]; xs = [(l, x) for l, x in xs if x is not None]
        if not xs: out[q] = None; continue
        lo = min(xs, key=lambda t: t[1]); hi = max(xs, key=lambda t: t[1])
        out[q] = {"min": lo[1], "max": hi[1], "linha_min": lo[0], "linha_max": hi[0], "n_linhas": len(xs)}
    n = {(getblk(r) or {}).get("n") for L, r in R[b]}; out["n_por_linha"] = sorted(x for x in n if x is not None)
    return out
crit = json.load(open(f"{OUT}/analysis/criterio.json"))
CLS28 = {"KVASIR": ["dependent_polyp", "dependent_instrument", "controle_texto"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no"]}
I28 = {b: {c: faixa(b, lambda r, c=c: r["by_class"].get(c)) for c in CLS28[b]} for b in BASES}
ents = [c for c in R["MIMIC"][0][1]["by_class"] if c.startswith("entidade=")]
I28["MIMIC"].update({c: faixa("MIMIC", lambda r, c=c: r["by_class"].get(c)) for c in ents if R["MIMIC"][0][1]["by_class"][c]["n"] >= 20})
anat = [k for k in crit["bases"]["HEAL"]["por_estrato"]]   # the four anatomies of item 15 (closed-ended yes)
I28["HEAL"].update({k: faixa("HEAL", lambda r, k=k: r["extra"].get(k)) for k in anat})
# item 29
def ms(xs):
    xs = [x for x in xs if x is not None]
    return None if not xs else {"media": statistics.mean(xs), "dp": statistics.stdev(xs) if len(xs) > 1 else None, "n": len(xs)}
I29 = {}
for b in BASES:
    I29[b] = {}
    for c in CLS28[b]:
        G = collections.OrderedDict(); per = {}
        for L, r in R[b]:
            k = r["by_class"].get(c) or {}; G.setdefault(grp(L), []).append(k)
            per[L["line"]] = {"grupo": grp(L), "n": k.get("n"), "n_m0": k.get("n_m0"), "acc_C0": (k.get("acc") or {}).get("C0"), "acc_m0": k.get("acc_m0"), "gain_tfidf": k.get("headroom_m0"), "gain_tfidf_ci": k.get("headroom_m0_ci_by_image"),
                              "acc_txt": k.get("acc_txt"), "gain_txt": k.get("headroom"), "gain_txt_ci": k.get("headroom_ci_by_image")}
        I29[b][c] = {"por_linha": per, "por_grupo": {g: {"n_linhas": len(ks), "gain_tfidf": ms([k.get("headroom_m0") for k in ks]), "gain_txt": ms([k.get("headroom") for k in ks]),
                                                        "gain_tfidf_ic_inf_maior_0": sum(1 for k in ks if k.get("headroom_m0_ci_by_image") and k["headroom_m0_ci_by_image"][0] > 0),
                                                        "gain_txt_ic_inf_maior_0": sum(1 for k in ks if k.get("headroom_ci_by_image") and k["headroom_ci_by_image"][0] > 0)} for g, ks in G.items()},
                     "faixa_gain_tfidf": I28[b][c]["headroom_m0"], "faixa_gain_txt": I28[b][c]["headroom"],
                     "n_m0_igual_n": all(v["n_m0"] == v["n"] for v in per.values())}
# item 30
TPL = "template=Is there a green/black box artefact?"
inv = json.load(open(INV["KVASIR"])); IMG = {int(q["qid"]): q["image_id"] for q in inv["questions"]}; B = E.Base(IMG)
qs_t = [q["qid"] for q in inv["questions"] if q["evaluable"] and q["question"] == TPL.split("=", 1)[1]]
I30 = {"template": TPL.split("=", 1)[1], "n_avaliaveis": len(qs_t), "linhas": {}, "contagens_27": {}, "contagens_15": {}, "blur4": {"linhas": {}, "contagens_15": {}}}
for L, r in R["KVASIR"]:
    k = r["extra"][TPL]; I30["linhas"][L["line"]] = {"pack": L["pack"], "n": k["n"]} | {f: {"delta": k.get(f"delta_{f}"), "ci": k.get(f"delta_{f}_ci_by_image")} for f in ("preto", "blur10", "regmean")}
def cnt(rows, f):
    v = [x[f] for x in rows if x.get(f) and x[f].get("ci")]
    return {"ic_sup_menor_0": sum(1 for x in v if x["ci"][1] < 0), "ic_inf_maior_0": sum(1 for x in v if x["ci"][0] > 0), "n_linhas": len(v),
            "min": min(x["delta"] for x in v), "max": max(x["delta"] for x in v)}
for f in ("preto", "blur10", "regmean"):
    I30["contagens_27"][f] = cnt(I30["linhas"].values(), f); I30["contagens_15"][f] = cnt([x for x in I30["linhas"].values() if x["pack"].startswith("15 de")], f)
sig = json.load(open(f"{KV_META}/blur_sigma_report.json")); I30["blur4"]["sigma"] = {"blur_sigma_px": sig["blur_sigma_px"], "sigma_sobre_largura_kvasir": sig["datasets"]["kvasir"]["sigma_over_width"], "fonte": f"{KV_META}/blur_sigma_report.json", "sha256": sha(f"{KV_META}/blur_sigma_report.json")}
for L, r in R["KVASIR"]:
    pt, pp_ = f"{ISBI}/{L['line']}_T_blur.json", f"{ISBI}/{L['line']}_P_blur.json"
    if not (os.path.exists(pt) and os.path.exists(pp_)):
        I30["blur4"]["linhas"][L["line"]] = {"status": "sem predicoes T_blur/P_blur", "pack": L["pack"]}; continue
    C = {c: E.load_correct(p) for c, p in r["files"].items() if c in E.CORE}; C4 = {"C0": C["C0"], "T": E.load_correct(pt), "P": E.load_correct(pp_)}
    al = [q for q in qs_t if all(q in C[c] for c in E.CORE) and q in C4["T"] and q in C4["P"]]
    b4 = E.block(B, al, C4)
    I30["blur4"]["linhas"][L["line"]] = {"pack": L["pack"], "n": b4["n"], "blur4": {"delta": b4["delta_preto"], "ci": b4["delta_preto_ci_by_image"]}, "files": {"T": pt, "P": pp_}, "sha256": {"T": sha(pt), "P": sha(pp_)}}
ok4 = [x for x in I30["blur4"]["linhas"].values() if "blur4" in x]; I30["blur4"]["contagens_15"] = cnt(ok4, "blur4"); I30["blur4"]["n_linhas_com_predicoes"] = len(ok4)
# item 31
S = {}
for b in BASES:
    q = json.load(open(INV[b]))["questions"]; ev = [x for x in q if x["evaluable"]]; S[b] = {"inventario": INV[b], "inventario_sha256": sha(INV[b]), "perguntas_teste": len(q), "distintas_teste": len({x["question"] for x in q}),
                                                                                  "avaliaveis": len(ev), "distintas_avaliaveis": len({x["question"] for x in ev})}
    cl = [x for x in ev if x["question_class"] in ("closed_yes", "closed_no")]
    if b != "KVASIR": S[b].update({"fechadas_avaliaveis": len(cl), "distintas_fechadas_avaliaveis": len({x["question"] for x in cl}), "por_classe": {c: {"n": sum(1 for x in cl if x["question_class"] == c), "distintas": len({x["question"] for x in cl if x["question_class"] == c})} for c in ("closed_yes", "closed_no")}})
    else: S[b]["por_classe_avaliaveis"] = {c: {"n": sum(1 for x in ev if x["question_class"] == c), "distintas": len({x["question"] for x in ev if x["question_class"] == c})} for c in ("dependent_polyp", "dependent_instrument", "negative_control", "dependent_polyp_secondary")}
    if b == "KVASIR": S[b]["templates"] = {"regra": "cada pergunta distinta do teste e um template (sem campo de template no inventario)", "teste": S[b]["distintas_teste"], "avaliaveis": S[b]["distintas_avaliaveis"]}
    elif b == "MIMIC": S[b]["templates"] = {"regra": "campo template_id do inventario", "teste": len({x["template_id"] for x in q}), "fechadas_avaliaveis": len({x["template_id"] for x in cl}), "ids_fechadas": dict(collections.Counter(x["template_id"] for x in cl))}
    else:
        PAT = [("Is there {achado} in the {anatomia} of this patient?", r"^Is there .+ in the {A} of this patient\?$"), ("Does {anatomia} suffer from {achado}?", r"^Does {A} suffer from .+\?$"),
               ("Does the patient have {achado} at {anatomia}?", r"^Does the patient have .+ at {A}\?$"), ("List all abnormalities in {anatomia}?", r"^List all abnormalities in {A}\?$"),
               ("What abnormalities are present in {anatomia}?", r"^What abnormalities are present in {A}\?$"), ("What abnormalities does {anatomia} suffer from?", r"^What abnormalities does {A} suffer from\?$")]
        hit = collections.Counter(); bad = 0
        for x in q:
            m = [t for t, rx in PAT if re.match(rx.replace("{A}", re.escape(x["anatomy"])), x["question"])]
            if len(m) != 1: bad += 1
            else: hit[(m[0], x["question_class"] if x["question_class"] == "open" else "fechada")] += 1
        S[b]["templates"] = {"regra": "padroes de texto (achado e anatomia substituidos); cada pergunta casa exatamente um padrao", "perguntas_sem_casamento_unico": bad,
                             "fechadas": sorted({t for (t, k) in hit if k == "fechada"}), "abertas": sorted({t for (t, k) in hit if k == "open"}), "contagem": {f"{t} | {k}": v for (t, k), v in hit.items()},
                             "fechadas_avaliaveis_por_template": dict(collections.Counter(next(t for t, rx in PAT if re.match(rx.replace("{A}", re.escape(x["anatomy"])), x["question"])) for x in cl))}
ds = json.load(open(f"{OUT}/analysis/doses.json"))["bases"]["HEAL"]
S["HEAL"]["doses"] = {"linhas_nas_medias": sum(next(iter(g.values()))["n_linhas"] for g in ds["agregado_por_grupo"].values()), "linhas": 27, "excluidas": ds["excluidas_das_medias"]}
out = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "engine_sha256": sha(f"{OUT}/scripts/engine.py"),
       "fontes": {"necessity_v2": NV2, "criterio": sha(f"{OUT}/analysis/criterio.json"), "doses": sha(f"{OUT}/analysis/doses.json")},
       "item28_faixas": I28, "item29_gain_tfidf": I29, "item30_caixa_artefato": I30, "item31_setup": S, "segundos": round(time.time() - T0)}
json.dump(out, open(f"{OUT}/analysis/rodada3.json", "w"), indent=1)
print("ok", out["segundos"], "s; blur4 linhas", I30["blur4"]["n_linhas_com_predicoes"], "; HEAL doses", S["HEAL"]["doses"]["linhas_nas_medias"], "; HEAL sem casamento", S["HEAL"]["templates"]["perguntas_sem_casamento_unico"])
print(json.dumps(I30["contagens_27"]), json.dumps(I30["contagens_15"]), json.dumps(I30["blur4"]["contagens_15"]))
print({b: {c: v["n_m0_igual_n"] for c, v in I29[b].items()} for b in BASES})
