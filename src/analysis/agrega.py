"""Items 3-7 (CPU): aggregates analysis/necessity_v2/*.json into analysis/{criterio,headroom,oclusor_negativos,doses,zeroshot}.json and writes
docs/item2..item7 and docs/estatistica.md. Mean (SD, ddof=1) over the three seeds = description of the three runs (conditional on the three models;
seeds are not resampled). Numbers only."""
import collections, glob, json, os, re, socket, statistics, sys, time
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
T0 = time.time(); NV2 = f"{OUT}/analysis/necessity_v2"
R = {b: [json.load(open(f)) for f in sorted(glob.glob(f"{NV2}/*_{b}.json"))] for b in BASES}
FT = {b: [r for r in R[b] if not r.get("zero_shot")] for b in BASES}; ZSR = {b: [r for r in R[b] if r.get("zero_shot")] for b in BASES}
ORDER = {l["line"]: i for b in BASES for i, l in enumerate(lines(b))}
for b in BASES: FT[b].sort(key=lambda r: ORDER[r["line"]])
MAIN = {"KVASIR": ["dependent_polyp", "dependent_instrument", "controle_texto", "dependent_polyp_secondary", "negative_control"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no", "closed_yes|so_exatas", "closed_no|so_exatas"]}
def config(line): return re.sub(r"_seed\d$", "", line)
def grp(r): return f"{r['family']}, encoder {r['encoder']}"
def ms(xs):
    xs = [x for x in xs if x is not None]
    if not xs: return None
    return {"media": statistics.mean(xs), "dp": statistics.stdev(xs) if len(xs) > 1 else None, "min": min(xs), "max": max(xs), "n": len(xs)}
KEYS = ["acc.C0", "acc_txt", "headroom", "acc_m0", "headroom_m0", "custo_mascara_deslocada_preto", "custo_alvo_preto", "delta_preto", "delta_blur10", "delta_regmean", "suficiencia_preto"]
def res_ic(bk):
    """round 2 (item 15): resolvable (`resoluvel`) = lower bound of the per-image 95 % CI of the headroom > 0 (without the 0.10 threshold)."""
    c = (bk or {}).get("headroom_ci_by_image"); return bool(c and c[0] > 0)
def res_010(bk): return bool((bk or {}).get("resoluvel"))   # round-1 version: headroom >= 0.10 and CI > 0
EXCL_DOSE = {"HEAL": {"QWEN2VL_DORA_HEAL_seed2": "1x do adapter original (ausente na gpu1); 1,5x e 2x do retreino de 03/10: dois checkpoints na mesma celula; fora das medias de dose (item 20)"}}
def get(b, k):
    if k.startswith("acc."): return (b.get("acc") or {}).get(k[4:])
    return b.get(k)
def agg(rs, cls):
    out = {k: ms([get(r["by_class"].get(cls, {}), k) for r in rs]) for k in KEYS}
    for c in ("A", "B", "C"): out[f"criterio_{c}"] = sum(1 for r in rs if r["by_class"].get(cls, {}).get(f"criterio_{c}")) 
    out["resoluvel"] = sum(1 for r in rs if res_ic(r["by_class"].get(cls))); out["resoluvel_ic_e_010"] = sum(1 for r in rs if res_010(r["by_class"].get(cls)))
    out["B_e_resoluvel"] = sum(1 for r in rs if res_ic(r["by_class"].get(cls)) and r["by_class"].get(cls, {}).get("criterio_B")); out["n_linhas"] = len(rs)
    return out
# ---------------- item 3: criterio
crit = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "definicao": {"B (artigo)": "IC 95 % por imagem de Delta exclui zero por cima sob preto E sob blur 10 %", "A (so interno)": "preto E (blur 10 % OU cor media)", "C (so interno)": "preto E blur 10 % E cor media",
        "antigo": "e3.necessary dos necessity_*.json: preto E (blur 10 % OU cor media), IC por bootstrap pareado por PERGUNTA (10 000, semente 42)"}, "bases": {}}
for b in BASES:
    B = {"por_classe": {}, "por_linha": {}}
    for cls in MAIN[b]:
        rs = FT[b]
        tot = {c: sum(1 for r in rs if r["by_class"].get(cls, {}).get(f"criterio_{c}")) for c in ("A", "B", "C")}
        antigo = sum(1 for r in rs if ((r.get("necessity_antigo") or {}).get("by_class", {}).get(cls.split("|")[0], {}).get("e3") or {}).get("necessary")) if "|" not in cls else None
        by = collections.OrderedDict()
        for r in rs: by.setdefault(grp(r), []).append(r)
        res = sum(1 for r in rs if res_ic(r["by_class"].get(cls))); bres = sum(1 for r in rs if res_ic(r["by_class"].get(cls)) and r["by_class"].get(cls, {}).get("criterio_B"))
        B["por_classe"][cls] = {"n_linhas": len(rs), "total": tot, "antigo_e3_ic_por_pergunta": antigo, "resoluveis": res, "B_entre_resoluveis": bres, "resoluveis_ic_e_010": sum(1 for r in rs if res_010(r["by_class"].get(cls))),
                                "por_grupo": {g: {c: sum(1 for r in v if r["by_class"].get(cls, {}).get(f"criterio_{c}")) for c in ("A", "B", "C")} | {"resoluveis": sum(1 for r in v if res_ic(r["by_class"].get(cls))), "B_entre_resoluveis": sum(1 for r in v if res_ic(r["by_class"].get(cls)) and r["by_class"].get(cls, {}).get("criterio_B")), "n": len(v), "antigo": sum(1 for r in v if ((r.get("necessity_antigo") or {}).get("by_class", {}).get(cls, {}).get("e3") or {}).get("necessary"))} for g, v in by.items()}}
    for r in FT[b]: B["por_linha"][r["line"]] = {cls: {c: r["by_class"].get(cls, {}).get(f"criterio_{c}") for c in ("A", "B", "C")} | {"antigo": ((r.get("necessity_antigo") or {}).get("by_class", {}).get(cls, {}).get("e3") or {}).get("necessary"),
                                                    "resoluvel": res_ic(r["by_class"].get(cls)), "resoluvel_ic_e_010": res_010(r["by_class"].get(cls)), "B_e_resoluvel": res_ic(r["by_class"].get(cls)) and bool(r["by_class"].get(cls, {}).get("criterio_B"))} for cls in MAIN[b] if "|" not in cls}
    # strata: entities (Medical-Diff-VQA, closed-ended yes, n >= 20) and anatomies (HEAL, closed-ended yes)
    est = {}
    keys = [k for k in FT[b][0]["by_class"] if k.startswith("entidade=")] if b == "MIMIC" else ([f"anatomia={a}|closed_yes" for a in ("Aorta", "Heart", "Right upper lung", "Left upper lung")] if b == "HEAL" else [])
    for k in keys:
        def bk(r): return r["by_class"].get(k) if k in r["by_class"] else r["extra"].get(k)
        by = collections.OrderedDict()
        for r in FT[b]: by.setdefault(grp(r), []).append(r)
        est[k] = {"n": (bk(FT[b][0]) or {}).get("n"), "resoluveis": sum(1 for r in FT[b] if res_ic(bk(r))), "B_entre_resoluveis": sum(1 for r in FT[b] if res_ic(bk(r)) and (bk(r) or {}).get("criterio_B")), "B": sum(1 for r in FT[b] if (bk(r) or {}).get("criterio_B")), "n_linhas": len(FT[b]),
                  "por_grupo": {g: {"resoluveis": sum(1 for r in v if res_ic(bk(r))), "B_entre_resoluveis": sum(1 for r in v if res_ic(bk(r)) and (bk(r) or {}).get("criterio_B")), "n": len(v)} for g, v in by.items()},
                  "por_linha": {r["line"]: {"resoluvel": res_ic(bk(r)), "B": bool((bk(r) or {}).get("criterio_B")), "B_e_resoluvel": res_ic(bk(r)) and bool((bk(r) or {}).get("criterio_B"))} for r in FT[b]}}
    B["por_estrato"] = est
    crit["bases"][b] = B
crit["citado_no_prompt"] = {"KVASIR": "15/15 (publicadas) e 12/12 + 11/12 (encoder invertido; polipo, instrumento)", "HEAL": "0/27", "MIMIC": "16/27 e 19/27"}
json.dump(crit, open(f"{OUT}/analysis/criterio.json", "w"), indent=1)
# ---------------- item 4: headroom (run x class; aggregates; entities/anatomies/Kvasir classes)
EXTRA_SEL = {"HEAL": [f"anatomia={a}|closed_yes" for a in ("Aorta", "Heart", "Right upper lung", "Left upper lung")] + [f"anatomia={a}" for a in ("Aorta", "Heart", "Right upper lung", "Left upper lung")], "KVASIR": [], "MIMIC": []}
FIELDS = ["n", "n_imagens", "acc", "acc_ci_by_image", "n_txt", "acc_txt", "acc_txt_ci_by_image", "headroom", "headroom_ci_by_image", "resoluvel", "n_m0", "acc_m0", "headroom_m0", "headroom_m0_ci_by_image",
          "delta_preto", "delta_preto_ci_by_image", "delta_blur10", "delta_blur10_ci_by_image", "delta_regmean", "delta_regmean_ci_by_image", "custo_mascara_deslocada_preto", "custo_mascara_deslocada_preto_ci_by_image",
          "custo_alvo_preto", "suficiencia_preto", "suficiencia_preto_ci_by_image", "suficiencia_blur10", "suficiencia_regmean", "criterio_A", "criterio_B", "criterio_C", "p_holm_preto", "p_holm_blur10", "mcnemar_midp_preto", "mcnemar_midp_blur10"]
def sel(bk): return {k: bk.get(k) for k in FIELDS if k in bk} | {"resoluvel": res_ic(bk), "resoluvel_ic_e_010": res_010(bk)}
hd = {"t": crit["t"], "rotulo_m3ae": "text-decoder-only (grey image): o braco so-texto do M3AE e treinado com imagem cinza constante", "regra_resoluvel": "limite inferior do IC 95 % por imagem do headroom > 0 (rodada 2, sem limiar); a versao da rodada 1 (headroom >= 0,10 e IC > 0) fica em resoluvel_ic_e_010",
      "bases": {}}
for b in BASES:
    H = {"linhas": {}, "agregado_por_config": {}, "agregado_por_grupo": {}, "extra": {}}
    clsl = MAIN[b] + [k for k in FT[b][0]["by_class"] if k.startswith("entidade=")]
    for r in FT[b]:
        H["linhas"][r["line"]] = {"family": r["family"], "method": r["method"], "encoder": r["encoder"], "seed": r["seed"], "txt_line": r.get("txt_line"), "classes": {c: sel(r["by_class"][c]) for c in clsl if c in r["by_class"]}}
        H["extra"][r["line"]] = {k: sel(r["extra"][k]) for k in EXTRA_SEL[b] if k in r["extra"]}
    byc = collections.OrderedDict(); byg = collections.OrderedDict()
    for r in FT[b]: byc.setdefault(config(r["line"]), []).append(r); byg.setdefault(grp(r), []).append(r)
    for c, rs in byc.items(): H["agregado_por_config"][c] = {cls: agg(rs, cls) for cls in clsl}
    for g, rs in byg.items(): H["agregado_por_grupo"][g] = {cls: agg(rs, cls) for cls in clsl}
    if EXTRA_SEL[b]:
        H["agregado_extra_por_grupo"] = {}
        for g, rs in byg.items():
            H["agregado_extra_por_grupo"][g] = {k: {kk: ms([(r["extra"].get(k) or {}).get(kk) if kk != "acc.C0" else ((r["extra"].get(k) or {}).get("acc") or {}).get("C0") for r in rs]) for kk in KEYS} | {"criterio_B": sum(1 for r in rs if (r["extra"].get(k) or {}).get("criterio_B")), "n": (rs[0]["extra"].get(k) or {}).get("n")} for k in EXTRA_SEL[b]}
    hd["bases"][b] = H
json.dump(hd, open(f"{OUT}/analysis/headroom.json", "w"), indent=1)
# ---------------- item 5: occluder test on negative items
oc = {"t": crit["t"], "definicao": "taxa de afirmativa induzida = P(afirma | oclusor) - P(afirma | intacta), pareada por item; IC 95 % bootstrap por imagem (replicas da base); McNemar mid-p; Holm por linha sobre as condicoes da base", "bases": {}}
for b in BASES:
    O = {"linhas": {}, "agregado_por_grupo": {}, "zeroshot": {}}
    for r in FT[b]: O["linhas"][r["line"]] = {"family": r["family"], "encoder": r["encoder"], "method": r["method"], "seed": r["seed"], **r["oclusor_negativos"]}
    for r in ZSR[b]: O["zeroshot"][r["line"]] = r["oclusor_negativos"]
    conds = sorted({c for r in FT[b] for c in r["oclusor_negativos"].get("conds", {})})
    byg = collections.OrderedDict()
    for r in FT[b]: byg.setdefault(grp(r), []).append(r)
    for g, rs in byg.items():
        O["agregado_por_grupo"][g] = {c: {"taxa_induzida": ms([r["oclusor_negativos"]["conds"].get(c, {}).get("taxa_induzida") for r in rs]),
                                          "n_ic_exclui_zero_por_cima": sum(1 for r in rs if (r["oclusor_negativos"]["conds"].get(c, {}).get("taxa_induzida_ci_by_image") or [0])[0] > 0),
                                          "n_ic_exclui_zero_por_baixo": sum(1 for r in rs if (r["oclusor_negativos"]["conds"].get(c, {}).get("taxa_induzida_ci_by_image") or [0, 0])[1] < 0), "n_linhas": len(rs)} for c in conds}
    O["cobertura"] = {r["line"]: {c: r["oclusor_negativos"]["conds"].get(c, {}).get("n", 0) for c in conds} for r in FT[b]}
    oc["bases"][b] = O
json.dump(oc, open(f"{OUT}/analysis/oclusor_negativos.json", "w"), indent=1)
# ---------------- item 6: doses
raw = json.load(open(f"{OUT}/analysis/bases_raw.json"))["bases"]
ds = {"t": crit["t"], "definicao": "Delta = Acc(P_k) - Acc(T_k), preto, k = 1, 1,5, 2, no subconjunto pareado (unidades com posicao valida em 1,5x e 2x); IC por imagem (replicas da base). Blur 10 % nao existe para as doses (so preto).", "bases": {}}
for b in BASES:
    D = {"fonte_pareado": raw[b]["dose_fonte"], "unidades_base": raw[b]["dose_unidades_base"], "unidades_validas_1.5_e_2": raw[b]["dose_unidades_validas_1.5_e_2"], "qids_pareados": raw[b]["dose_qids_pareados"], "linhas": {}, "agregado_por_grupo": {}}
    for r in FT[b]: D["linhas"][r["line"]] = r["doses"]
    byg = collections.OrderedDict()
    for r in FT[b]: byg.setdefault(grp(r), []).append(r)
    D["excluidas_das_medias"] = EXCL_DOSE.get(b, {}); D["valores_excluidos"] = {ln: D["linhas"][ln] for ln in EXCL_DOSE.get(b, {})}
    byg = collections.OrderedDict()
    for r in FT[b]:
        if r["line"] not in EXCL_DOSE.get(b, {}): byg.setdefault(grp(r), []).append(r)
    for g, rs in byg.items():
        D["agregado_por_grupo"][g] = {cls: {"n_linhas": len(rs)} | {L: {"delta": ms([((r["doses"].get("by_class") or {}).get(cls, {}).get("niveis", {}).get(L) or {}).get("delta_preto") for r in rs]),
                                                "n_ic_exclui_zero_por_cima": sum(1 for r in rs if ((((r["doses"].get("by_class") or {}).get(cls, {}).get("niveis", {}).get(L) or {}).get("delta_preto_ci_by_image")) or [0])[0] > 0)} for L in ("1", "1.5", "2")} | {"n_pareado": (rs[0]["doses"].get("by_class") or {}).get(cls, {}).get("n_pareado"), "n_classe": (rs[0]["doses"].get("by_class") or {}).get(cls, {}).get("n_classe")} for cls in raw[b]["familia_holm"]}
    ds["bases"][b] = D
json.dump(ds, open(f"{OUT}/analysis/doses.json", "w"), indent=1)
# ---------------- item 7: zero-shot
H = os.path.join(os.environ.get("HF_HOME", os.path.expanduser("~/.cache/huggingface")), "hub")
def hub_meta(rid):
    d = f"{H}/models--" + rid.replace("/", "--"); snaps = sorted(glob.glob(d + "/snapshots/*")); m = {"repo": rid, "snapshots": [os.path.basename(s) for s in snaps]}
    if snaps:
        s = snaps[0]; gc = f"{s}/generation_config.json"; ix = glob.glob(f"{s}/*.safetensors.index.json")
        m["generation_config"] = json.load(open(gc)) if os.path.exists(gc) else None
        if ix: md = json.load(open(ix[0])).get("metadata") or {}; m["safetensors_total_size_bytes"] = md.get("total_size"); m["parametros_estimados_bf16"] = (md.get("total_size") or 0) // 2 if md.get("total_size") else None
    return m
zs = {"t": crit["t"], "modelos": {}, "bases": {}}
for b in BASES:
    Z = {}
    for r in ZSR[b]:
        m = r["family"]; pv = r.get("provenance_c0") or {}
        if m not in zs["modelos"] and pv.get("base_model"):
            zs["modelos"][m] = {"base_model": pv.get("base_model"), "prompting": pv.get("prompting"), "dtype": pv.get("dtype"), "versions": pv.get("versions"), "git_commit": (pv.get("git") or {}).get("commit"), "hub": hub_meta(pv["base_model"]),
                                "max_new_tokens": 512 if m == "MEDVLTHINKER" else 64, "max_new_tokens_fonte": "med_vlm/training/spec_registry.py (default_max_new_tokens: chat template 64; MedVLThinker 512); harness/extract_predictions_circle.py:114",
                                "decodificacao_fonte": "med_vlm/training/generation.py: model.generate(**inputs, max_new_tokens=...) sem do_sample/temperature explicitos -> generation_config.json do snapshot do Hub"}
        Z[r["line"]] = {"classes": {c: sel(r["by_class"][c]) for c in MAIN[b] if c in r["by_class"]}, "conds": r["conds"], "txt_file": r["txt_file"], "oclusor_negativos": r["oclusor_negativos"]}
        if b == "MIMIC": Z[r["line"]]["entidades"] = {c: sel(v) for c, v in r["by_class"].items() if c.startswith("entidade=")}
    zs["bases"][b] = Z
zs["nota_llava_med"] = "celulas com acuracia 0 do LLaVA-Med: respostas fora do formato (ver docs/item7_zeroshot.md, contagem de predicoes vazias/longas por base e classe)"
# count of answers outside the format in LLaVA-Med (closed-ended: not yes/no)
sys.path.insert(0, CODE_ROOT); from med_vlm.metrics.process_text import normalize_text
fora = {}
for b in BASES:
    inv = json.load(open(INV[b])); cl = {q["qid"]: q["question_class"] for q in inv["questions"] if q["evaluable"]}
    for m in ZS:
        p = zs_file(m, b, "C0")
        if not os.path.exists(p): continue
        P = {int(x["qid"]): normalize_text(str(x["predicted"])) for x in json.load(open(p))["predictions"]}
        c = collections.Counter()
        for q, cc in cl.items():
            if q not in P: continue
            c[(cc, "total")] += 1
            if P[q] == "": c[(cc, "vazia")] += 1
            if cc in ("closed_yes", "closed_no", "closed_no_sham") and P[q] not in ("yes", "no", "positive", "negative"): c[(cc, "fechada_fora_de_yes_no")] += 1
            if len(P[q].split()) > 5: c[(cc, "mais_de_5_palavras")] += 1
        acc = {}
        for cc in sorted(set(cl.values())):
            qq = [q for q in cl if cl[q] == cc and q in P]
            if qq: acc[cc] = sum(bool(x["correct"]) for x in json.load(open(p))["predictions"] if int(x["qid"]) in set(qq)) / len(qq)
        c.update({(cc, "acuracia_C0_x1000"): round(1000 * v) for cc, v in acc.items()})
        fora[f"{m}_{b}"] = {f"{k[0]}|{k[1]}": v for k, v in sorted(c.items())}
zs["respostas_fora_do_formato_C0"] = fora
json.dump(zs, open(f"{OUT}/analysis/zeroshot.json", "w"), indent=1)
# ---------------- item 27: ladder of verdicts
LCLS = {"KVASIR": ["dependent_polyp", "dependent_instrument"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no"]}
def lo(bk, k): c = (bk or {}).get(k); return None if not c else c[0]
def steps(bk, floor="headroom"):
    L0 = (lo(bk, "custo_alvo_preto_ci_by_image") or 0) > 0; L1 = (lo(bk, "delta_preto_ci_by_image") or 0) > 0; L2 = L1 and (lo(bk, "delta_blur10_ci_by_image") or 0) > 0
    L3 = L2 and (lo(bk, f"{floor}_ci_by_image") or 0) > 0
    return {"L0": L0, "L1": L1, "L2": L2, "L3": L3}
def explain(bk):
    return {"custo_alvo_preto": bk.get("custo_alvo_preto"), "custo_alvo_preto_ci": bk.get("custo_alvo_preto_ci_by_image"), "custo_mascara_deslocada_preto": bk.get("custo_mascara_deslocada_preto"), "custo_mascara_deslocada_preto_ci": bk.get("custo_mascara_deslocada_preto_ci_by_image"),
            "delta_preto": bk.get("delta_preto"), "delta_preto_ci": bk.get("delta_preto_ci_by_image"), "delta_blur10": bk.get("delta_blur10"), "delta_blur10_ci": bk.get("delta_blur10_ci_by_image"),
            "headroom": bk.get("headroom"), "headroom_ci": bk.get("headroom_ci_by_image"), "headroom_m0": bk.get("headroom_m0"), "headroom_m0_ci": bk.get("headroom_m0_ci_by_image")}
esc = {"t": crit["t"], "definicao": {"L0": "queda bruta: IC de Acc(C0) - Acc(T preto) com limite inferior > 0", "L1": "controle pareado: IC de Delta preto com limite inferior > 0", "L2": "L1 e IC de Delta blur 10 % com limite inferior > 0 (criterio B)",
       "L3": "L2 e IC do headroom (Acc C0 - text-only arm da mesma linha; zero-shot: com imagem - sem imagem) com limite inferior > 0", "L3_tfidf (so interno)": "L2 e IC de Acc(C0) - Acc(TF-IDF) com limite inferior > 0"}, "bases": {}}
for b in BASES:
    E = {}
    for cls in LCLS[b]:
        rows = {}
        for r in FT[b] + ZSR[b]:
            bk = r["by_class"].get(cls) or {}
            if not bk.get("n"): continue
            st = steps(bk); st["L3_tfidf"] = st["L2"] and (lo(bk, "headroom_m0_ci_by_image") or 0) > 0
            rows[r["line"]] = {"zero_shot": bool(r.get("zero_shot")), "grupo": grp(r) if not r.get("zero_shot") else r["family"], "veredito": st, "numeros": explain(bk)}
        ft = {k: v for k, v in rows.items() if not v["zero_shot"]}; zz = {k: v for k, v in rows.items() if v["zero_shot"]}
        cont = {d: sum(1 for v in ft.values() if v["veredito"][d]) for d in ("L0", "L1", "L2", "L3", "L3_tfidf")}
        gr = collections.OrderedDict()
        for k, v in ft.items(): gr.setdefault(v["grupo"], []).append(v)
        mud = {}
        for a, d in (("L0", "L1"), ("L1", "L2"), ("L2", "L3")):
            mud[f"{a}->{d}"] = {k: {"de": v["veredito"][a], "para": v["veredito"][d], **{kk: v["numeros"][kk] for kk in (("custo_mascara_deslocada_preto", "custo_mascara_deslocada_preto_ci", "delta_preto", "delta_preto_ci") if a == "L0" else (("delta_blur10", "delta_blur10_ci") if a == "L1" else ("headroom", "headroom_ci")))}} for k, v in rows.items() if v["veredito"][a] != v["veredito"][d]}
        E[cls] = {"n_linhas": len(ft), "contagens": cont, "por_grupo": {g: {d: sum(1 for v in vs if v["veredito"][d]) for d in ("L0", "L1", "L2", "L3")} | {"n": len(vs)} for g, vs in gr.items()},
                  "zero_shot": {k: v["veredito"] for k, v in zz.items()}, "mudancas": mud, "linhas": rows}
    esc["bases"][b] = E
json.dump(esc, open(f"{OUT}/analysis/escada_vereditos.json", "w"), indent=1)
print("agregados ok", round(time.time() - T0), "s")
