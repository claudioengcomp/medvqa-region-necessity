"""Items 2, 4, 5, 6, 7 (CPU): applies engine.py to the 27 fine-tuned runs per benchmark (Kvasir, HEAL, MIMIC), to the 4 zero-shot models per benchmark,
to the occluder test on images without the finding, and to the doses. Outputs: analysis/necessity_v2/<run>_<benchmark>.json (one per fine-tuned or
zero-shot run) and analysis/bases_raw.json (index + check of the point estimates against the existing necessity_*.json). Usage: analise_bases.py [BENCHMARK,...]"""
import collections, glob, json, os, socket, sys, time
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__)))
from common import *
import engine as E
sys.path.insert(0, CODE_ROOT)
from med_vlm.metrics.process_text import normalize_text
T0 = time.time(); NV2 = f"{OUT}/analysis/necessity_v2"; os.makedirs(NV2, exist_ok=True)
Q_TEXT = "Is there text?"
def old_nec(base, line):
    c = [f"{ISBI}/necessity_{line}.json", f"{V5Q}/results_placebo/necessity_{line}.json", f"{V5S}/results_placebo/necessity_{line}.json", f"{V6}/necessity/necessity_{line}.json", f"{W}/v5_analysis/placebo_tower/necessity/necessity_{line}.json",
         f"{V7M}/analysis/necessity_{line}.json", f"{V7Z}/analysis/necessity_{line}.json"]
    c += [f"{d}/necessity_{line}.json" for d in CFG["kvasir"]["predictions"]]   # released copies of the earlier per-run reports (default configuration)
    return next((p for p in c if os.path.exists(p)), None)
def classes(base, inv):
    ev = [q for q in inv["questions"] if q["evaluable"]]; G = collections.OrderedDict(); fam = []; extra = collections.OrderedDict()
    if base == "KVASIR":
        for k in ("dependent_polyp", "dependent_instrument", "negative_control", "dependent_polyp_secondary"): G[k] = [q["qid"] for q in ev if q["question_class"] == k]
        G["controle_texto"] = [q["qid"] for q in ev if q["question_class"] == "negative_control" and q["question"] == Q_TEXT]
        for t in sorted({q["question"] for q in ev if q["question_class"] == "negative_control"}): extra["template=" + t] = [q["qid"] for q in ev if q["question"] == t]
        fam = ["dependent_polyp", "dependent_instrument", "controle_texto"]
    elif base == "HEAL":
        for k in ("closed_yes", "closed_no"): G[k] = [q["qid"] for q in ev if q["question_class"] == k]
        for a in sorted({q["anatomy"] for q in ev}):
            for k in ("closed_yes", "closed_no"): extra[f"anatomia={a}|{k}"] = [q["qid"] for q in ev if q["anatomy"] == a and q["question_class"] == k]
            extra[f"anatomia={a}"] = [q["qid"] for q in ev if q["anatomy"] == a]
        fam = ["closed_yes", "closed_no"]
    else:
        for k in ("closed_yes", "closed_no", "open"): G[k] = [q["qid"] for q in ev if q["question_class"] == k]
        ents = collections.Counter(q["entity"] for q in ev if q["question_class"] == "closed_yes")
        for e, n in ents.most_common():
            if n >= 20: G[f"entidade={e}"] = [q["qid"] for q in ev if q["question_class"] == "closed_yes" and q["entity"] == e]
        G["closed_yes|so_exatas"] = [q["qid"] for q in ev if q["question_class"] == "closed_yes" and q.get("entity_map_quality") == "exata"]
        G["closed_no|so_exatas"] = [q["qid"] for q in ev if q["question_class"] == "closed_no" and q.get("entity_map_quality") == "exata"]
        fam = ["closed_yes", "closed_no"] + [k for k in G if k.startswith("entidade=")]
    return G, extra, fam
def m0_for(base):
    if base == "MIMIC":
        from harness.v7_txt.mimic_floors import mimic_floors
        return mimic_floors()["piso_subset"], f"{V7M}/results/M0_question_only_MIMIC_subset.json (piso composto: M0 subset nas fechadas + prior por template nas abertas)"
    return E.load_correct(M0[base]), M0[base]
def analyse_line(B, base, line, files, txtp, G, extra, fam, M0, zs=False):
    have = {c: p for c, p in files.items() if p and c in E.CORE + ["S_blur10", "S_regmean"]}
    C = {c: E.load_correct(p) for c, p in have.items()}
    TX = E.load_correct(txtp) if txtp else None
    core = [c for c in E.CORE if c in C]
    def al(qs): return [q for q in qs if all(q in C[c] for c in core)]
    rec = {"line": line, "base": base, "zero_shot": zs, "conds": sorted(have), "files": have, "files_sha256": {c: sha(p) for c, p in have.items()}, "txt_file": txtp, "txt_sha256": sha(txtp),
           "by_class": {}, "extra": {}}
    for k, qs in G.items(): rec["by_class"][k] = E.block(B, al(qs), C, TX, M0); rec["by_class"][k]["n_avaliaveis"] = len(qs)
    for k, qs in extra.items(): rec["extra"][k] = E.block(B, al(qs), C, TX, M0)
    E.holm_line(rec["by_class"], fam); rec["holm_family"] = fam
    op = old_nec(base, line)
    if op:
        o = json.load(open(op)); rec["necessity_antigo"] = {"file": os.path.basename(op), "sha256": sha(op), "n_boot": o.get("n_boot"), "seed": o.get("seed"), "by_class": {}}
        for k, b in (o.get("by_class") or {}).items():
            mine = rec["by_class"].get(k, {})
            rec["necessity_antigo"]["by_class"][k] = {"n": b.get("n"), "delta_nec": b.get("delta_nec"), "delta_nec_ci": b.get("delta_nec_ci"), "delta_nec_blur10": b.get("delta_nec_blur10"), "delta_nec_blur10_ci": b.get("delta_nec_blur10_ci"),
                                                       "delta_nec_regmean": b.get("delta_nec_regmean"), "delta_nec_regmean_ci": b.get("delta_nec_regmean_ci"), "e3": b.get("e3"), "sufficiency": b.get("sufficiency"),
                                                       "ponto_igual": (mine.get("n") == b.get("n") and abs((mine.get("delta_preto") or 0) - (b.get("delta_nec") or 0)) < 1e-12) if mine.get("n") else None}
    return rec
def dose_qids(base):
    if base == "KVASIR":
        m = json.load(open(f"{KV_META}/manifest_kvasir.json")); U = m["units"]; ok = [u for u in U if all(u.get("placebo_method_by_factor", {}).get(k) is not None for k in ("1.5", "2"))]
        return [q for u in ok for q in u["qids"]], len(U), len(ok), f"{KV_META}/manifest_kvasir.json"
    if base == "HEAL":
        p = f"{V7T}/analysis/heal_dose_inventory.json"; U = json.load(open(p))["unidades"]; ok = [u for u in U if all(u["methods"].get(k) for k in ("1.5", "2"))]
        return [q for u in ok for q in u["qids"]], len(U), len(ok), p
    p = f"{V7M}/analysis/manifest_mimic_placebo_dose_compat.json"; U = json.load(open(p))["units"]; ok = [u for u in U if all(u["placebo_method_by_factor"].get(k) is not None for k in ("1.5", "2"))]
    return [q for u in ok for q in u["qids"]], len(U), len(ok), p
def doses(B, base, line, files, G, fam, pq):
    need = {"1": ("T", "P"), "1.5": ("T1.5", "P1.5"), "2": ("T2", "P2")}
    if any(files.get(c) is None for lv in need.values() for c in lv): return {"status": "faltam " + ",".join(c for lv in need.values() for c in lv if files.get(c) is None)}
    C = {c: E.load_correct(files[c]) for lv in need.values() for c in lv}; C["C0"] = E.load_correct(files["C0"]); pqs = set(pq); out = {"status": "ok", "by_class": {}}
    for k in fam:
        qs = [q for q in G[k] if q in pqs and all(q in C[c] for c in C)]
        lv = {}
        for L, (t, p) in need.items():
            b = E.block(B, qs, {"C0": C["C0"], "T": C[t], "P": C[p]}) if qs else {"n": 0}
            lv[L] = {k2: b.get(k2) for k2 in ("n", "n_imagens", "delta_preto", "delta_preto_ci_by_image", "mcnemar_midp_preto")}
        out["by_class"][k] = {"n_classe": len(G[k]), "n_pareado": len(qs), "niveis": lv}
    return out
def sham(B, base, line, c0_full, zs, inv, files):
    """affirmative-answer rate induced by each occluder condition on negative items."""
    yes = ("yes", "positive") if zs else ("yes",)
    if base == "KVASIR":
        import importlib.util
        spec = importlib.util.spec_from_file_location("kvasir_sham", f"{CODE_ROOT}/harness/v7_sham/kvasir_sham.py"); KS = importlib.util.module_from_spec(spec); spec.loader.exec_module(KS)
        si = json.load(open(f"{KV_OCC_META}/inventory_kvasir_sham.json")); Qs = collections.defaultdict(dict)
        for u in si["units"]:
            if u["generated"]:
                for q in u["questions"]: Qs[u["condition"]][int(q["qid"])] = q["question"]
        if not c0_full or not os.path.exists(c0_full): return {"status": "C0 completa ausente"}
        P0 = E.load_pred(c0_full); out = {"status": "ok", "c0": c0_full, "c0_sha256": sha(c0_full), "regra_afirma": "kvasir_sham.affirms (ART: yes; contagem != 0; tipo/presenca != none)", "conds": {}}
        for c in SHAM["KVASIR"]:
            if c == "C0_cross": continue
            p = find(base, line, c) or ""
            if not os.path.exists(p): out["conds"][c] = {"status": "ausente"}; continue
            Pc = E.load_pred(p); qs = [q for q in Qs[c] if q in Pc and q in P0]
            a = {q: KS.affirms(Qs[c][q], Pc[q]) for q in qs}; z = {q: KS.affirms(Qs[c][q], P0[q]) for q in qs}
            out["conds"][c] = E.ipr_block(B, qs, a, z) | {"file": p, "sha256": sha(p), "n_inventario": len(Qs[c])}
        fam = [c for c in out["conds"] if out["conds"][c].get("n")]
    else:
        if base == "HEAL":
            qs = [q["qid"] for q in inv["questions"] if q["evaluable"] and q["question_class"] == "closed_no"]; conds = {"alvo_preto": "T", "mascara_deslocada_preto": "P", "alvo_blur10": "T_blur10", "mascara_deslocada_blur10": "P_blur10"}
        else:
            qs = [q["qid"] for q in inv["questions"] if q["evaluable"] and q["question_class"] == "closed_no_sham"]; conds = {"oclusor_preto": "SHAM_black", "oclusor_blur10": "SHAM_blur10"}
        if files.get("C0") is None: return {"status": "C0 ausente"}
        P0 = {q: normalize_text(str(v)) in yes for q, v in E.load_pred(files["C0"]).items()}; out = {"status": "ok", "c0": files["C0"], "regra_afirma": f"normalize_text(pred) in {yes}", "n_itens": len(qs), "conds": {}}
        for k, c in conds.items():
            p = files.get(c) or (zs_file(line.split("_ZEROSHOT")[0], base, c) if zs else None)
            if not p or not os.path.exists(p): out["conds"][k] = {"status": "ausente"}; continue
            Pc = {q: normalize_text(str(v)) in yes for q, v in E.load_pred(p).items()}
            out["conds"][k] = E.ipr_block(B, qs, Pc, P0) | {"file": p, "sha256": sha(p)}
        fam = [k for k in out["conds"] if out["conds"][k].get("n")]
    hp = E.holm({k: out["conds"][k]["mcnemar_midp"]["p_midp"] for k in fam})
    for k, v in hp.items(): out["conds"][k]["p_holm"] = v
    return out
def c0_full_kvasir(line, zs):
    if ALIAS_TESTE and line.startswith("QWEN25VL_"): return c0_full_kvasir(alias_teste(line), zs)
    if zs: return first_existing(ZS_DIRS, f"{line}_C0.json")   # reference of the occluder test: the main zero-shot intact-image run (no instruction suffix)
    for d in KV_FULL:
        p = f"{d}/{line}_C0.json"
        if os.path.exists(p): return p
    return None
def run(base):
    t0 = time.time(); inv = json.load(open(INV[base])); IMG = {int(q["qid"]): q["image_id"] for q in inv["questions"]}
    B = E.Base(IMG); G, extra, fam = classes(base, inv); M0v, m0src = m0_for(base); pq, nU, nUok, dsrc = dose_qids(base)
    idx = {"base": base, "n_imagens_replicas": B.n_img, "inventario": INV[base], "inventario_sha256": sha(INV[base]), "m0": m0src, "familia_holm": fam,
           "classes_n": {k: len(v) for k, v in G.items()}, "dose_fonte": dsrc, "dose_unidades_base": nU, "dose_unidades_validas_1.5_e_2": nUok, "dose_qids_pareados": len(pq), "linhas": [], "zeroshot": []}
    for L in lines(base):
        files = {c: find(base, L["line"], c) for c in COND_MAIN + COND_DOSE + SHAM[base]}
        txtp = txt_file(base, L["fam"], L["seed"])
        rec = analyse_line(B, base, L["line"], files, txtp, G, extra, fam, M0v)
        rec.update({k: L[k] for k in ("family", "fam", "method", "encoder", "seed", "pack")}); rec["txt_line"] = txt_line(base, L["fam"], L["seed"])
        rec["doses"] = doses(B, base, L["line"], files, G, fam, pq)
        rec["oclusor_negativos"] = sham(B, base, L["line"], c0_full_kvasir(L["line"], False) if base == "KVASIR" else None, False, inv, files)
        json.dump(rec, open(f"{NV2}/{L['line']}_{base}.json", "w"), indent=1); idx["linhas"].append(L["line"])
        print(base, L["line"], round(time.time() - t0), "s", {k: (rec["by_class"][k].get("n"), round(rec["by_class"][k].get("delta_preto", float("nan")), 4)) for k in fam[:3]}, flush=True)
    for m in ZS:
        line = f"{m}_ZEROSHOT_{base}"; files = {c: (zs_file(m, base, c) if os.path.exists(zs_file(m, base, c)) else None) for c in COND_MAIN + SHAM[base]}
        txtp = zs_file(m, base, "TXT") if os.path.exists(zs_file(m, base, "TXT")) else None
        rec = analyse_line(B, base, line, files, txtp, G, extra, fam, M0v, zs=True); rec["family"] = m
        rec["oclusor_negativos"] = sham(B, base, line, c0_full_kvasir(line, True) if base == "KVASIR" else None, True, inv, files)
        try: pv = json.load(open(files["C0"])).get("provenance") or {}; rec["provenance_c0"] = pv
        except Exception: pass
        json.dump(rec, open(f"{NV2}/{line}_{base}.json", "w"), indent=1); idx["zeroshot"].append(line); print(base, line, round(time.time() - t0), "s", flush=True)
    idx["segundos"] = round(time.time() - t0); return idx
if __name__ == "__main__":
    bases = sys.argv[1].split(",") if len(sys.argv) > 1 else BASES
    p = f"{OUT}/analysis/bases_raw.json"; R = json.load(open(p)) if os.path.exists(p) else {"bases": {}}
    for b in bases: R["bases"][b] = run(b)
    R.update({"t": time.strftime("%Y-%m-%d %H:%M:%S"), "host": HOST, "engine": f"{SCRIPTS}/engine.py", "engine_sha256": sha(f"{SCRIPTS}/engine.py"), "script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)),
              "shamstats": f"{CODE_ROOT}/harness/v7_sham/shamstats.py", "shamstats_sha256": sha(f"{CODE_ROOT}/harness/v7_sham/shamstats.py"),
              "compute_necessity_v7txt_sha256": sha(f"{CODE_ROOT}/harness/isbi_placebo/compute_necessity.py"), "compute_necessity_placebo_sha256": sha(f"{PLC}/harness/isbi_placebo/compute_necessity.py")})
    if os.path.exists(p):   # released code: keep the benchmarks not recomputed in this call (e.g. reproduce.sh --kvasir)
        _old = json.load(open(p)); _old.get("bases", {}).update(R.get("bases", {})); R["bases"] = _old["bases"]
    json.dump(R, open(p, "w"), indent=1); print("FIM", round(time.time() - T0), "s")
