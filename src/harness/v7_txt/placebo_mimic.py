"""v7_mimic block C (2026-10-13, authors): aggregator of control occlusion v2 on MIMIC, same analysis as HEAL, for the 24 VLM runs
(15 published minus M3AE + 12 fine-tuned-encoder (tower) runs); M3AE pending (appendix once available).
Per run x class (closed_yes, closed_no, open; inventory v2; full and exact-only variants), on the qids aligned across all main
conditions (C0, C1, T, P, S, T/P/S_blur10, T/P/S_regmean -- the same alignment as compute_necessity):
- Acc per condition; Delta_nec = Acc(P) - Acc(T) paired under black, blur 10 % and region mean color; 95 % CI by PER-IMAGE bootstrap
  (2 000, seed 20260913, fixed replicates over the 1 445 test images, the same as own_floor_ceilings); McNemar mid-p (P x T);
  Holm per run over the three classes, per fill;
- E3 (pre-registration §7): necessary if the CI of Delta_nec excludes zero upwards under black AND under at least one plausible fill (blur 10 % or mean color);
  alongside, the E3 of the HEAL routine (compute_necessity: paired per-item CI, 10 000, seed 42), read from necessity_<RUN>.json;
- sufficiency Acc(S)/Acc(C0) with CI by the ratio over the replicates;
- image gain (`teto` in the code): M0 gain = Acc(C0) - M0 no-image baseline (M0 subset on closed-ended, per-template prior on open-ended); own gain = Acc(C0) - Acc(TXT of the same
  family and seed: QWEN2VL_LORA_TXT / SMOLVLM_LORA_TXT); nDelta = Delta_nec/gain (CI by the ratio; replicate with gain <= 0 discarded and counted);
  E9: not usable (n.u.) if gain < 0.10 or lower CI bound of the gain <= 0;
- occluder test (`sham`): IPR_c = P(yes|c) - P(yes|C0) on the evaluable closed_no_sham (391), c = SHAM_black, SHAM_blur10; affirms = normalize_text(pred) == 'yes';
  mid-p; per-image CI (replicates over the occluder-test images, as in heal_sham); Holm per run over the two conditions;
- doses: 'dose' block of compute_necessity (paired subset of 482 questions valid at 1.5x and 2x), transcribed;
- strata: n_target_boxes (1 / 2+) and placebo_scheme (single_box / per_box) of the unit (v2 manifest), and entity (closed_yes, n >= 30).
Negative control: the MIMIC v2 inventory has no pure negative-control class (as in HEAL: every closed-ended question with a target names
a finding or region); recorded. Outputs: analysis/placebo_mimic.json, docs/placebo_mimic.md, docs/numbers_placebo_mimic.md. No interpretation."""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import collections, hashlib, json, os, socket, sys, time
import numpy as np
sys.path.insert(0, os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/worktree")
from med_vlm.metrics.process_text import normalize_text
from harness.v7_sham.shamstats import ImageBootstrap, holm, mcnemar_midp, paired_block
from harness.v7_txt.txt_floors import mimic_floors
R = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic"; N_BOOT, SEED = 2000, 20260913
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""): h.update(b)
    return h.hexdigest()
FAMS = [("QWEN2VL_LORA_FROZEN", "QWEN2VL", "publicada"), ("QWEN2VL_DORA", "QWEN2VL", "publicada"), ("SMOLVLM_LORA", "SMOLVLM", "publicada"), ("SMOLVLM_DORA", "SMOLVLM", "publicada"),
        ("QWEN2VL_LORA_VT", "QWEN2VL", "torre"), ("QWEN2VL_DORA_VT", "QWEN2VL", "torre"), ("SMOLVLM_LORA_FT", "SMOLVLM", "torre"), ("SMOLVLM_DORA_FT", "SMOLVLM", "torre"),
        ("M3AE", "M3AE", "publicada")]   # 13/10: M3AE (appendix); own no-image baseline (`piso`) = text-only M3AE once it exists
TXT = {"QWEN2VL": "QWEN2VL_LORA_TXT", "SMOLVLM": "SMOLVLM_LORA_TXT", "M3AE": "M3AE_TXT"}
CORE = ["C0", "C1", "T", "P", "S", "T_blur10", "P_blur10", "S_blur10", "T_regmean", "P_regmean", "S_regmean"]
FILLS = {"preto": ("T", "P", "S"), "blur10": ("T_blur10", "P_blur10", "S_blur10"), "regmean": ("T_regmean", "P_regmean", "S_regmean")}
CLASSES = ["closed_yes", "closed_no", "open"]; SHAM = ["SHAM_black", "SHAM_blur10"]
INV = {"completo": f"{R}/results/inventory_mimic_test.json", "so_exatas": f"{R}/analysis/inventory_mimic_test_so_exatas.json"}
MAN = f"{R}/data/conditions/manifest_mimic_placebo.json"
inputs = {}
def load_correct(p): inputs[p] = sha(p); return {int(x["qid"]): bool(x["correct"]) for x in json.load(open(p))["predictions"]}
def load_pred(p): inputs[p] = sha(p); return {int(x["qid"]): normalize_text(str(x["predicted"])) for x in json.load(open(p))["predictions"]}
inv_all = json.load(open(INV["completo"])); IMG = {q["qid"]: q["image_id"] for q in inv_all["questions"]}
BS = ImageBootstrap(sorted(set(IMG.values())), N_BOOT, SEED)
def reps(qs, v):
    idx = np.array([BS.index[IMG[q]] for q in qs]); n = len(BS.ids)
    num = np.bincount(idx, weights=np.asarray(v, float), minlength=n); den = np.bincount(idx, minlength=n).astype(float)
    return (BS.W @ num) / np.maximum(BS.W @ den, 1e-9)
def ci(x): x = np.asarray(x, float); x = x[np.isfinite(x)]; return [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))] if len(x) else None
M0 = mimic_floors()["piso_subset"]
man = json.load(open(MAN)); UNIT = {}
for u in man["units_by_group"]["main1"]["units"]:
    for q in u["qids"]: UNIT[int(q)] = {"n_target_boxes": u["n_target_boxes"], "placebo_scheme": u["placebo_scheme"]}
def block(qs, C, TX, nec_cls):
    qs = [q for q in qs if (TX is None or q in TX) and q in M0]
    if len(qs) == 0: return {"n": 0}
    n = len(qs); v = {c: np.array([C[c][q] for q in qs], float) for c in C}; r = {c: reps(qs, v[c]) for c in ("C0", "S")}
    b = {"n": n, "n_imagens": len({IMG[q] for q in qs}), "acc": {c: float(v[c].mean()) for c in v}, "acc_ci": {c: ci(reps(qs, v[c])) for c in ("C0", "C1", "T", "P", "S")}}
    rd = {}
    for f, (t, p, s) in FILLS.items():
        d = v[p] - v[t]; rd[f] = reps(qs, d); mc = mcnemar_midp(v[p].astype(bool), v[t].astype(bool))
        b[f"delta_nec_{f}"] = float(d.mean()); b[f"delta_nec_{f}_ci"] = ci(rd[f]); b[f"mcnemar_{f}"] = mc
        rs = reps(qs, v[s]); ratio = np.where(r["C0"] > 0, rs / r["C0"], np.nan)
        b[f"suficiencia_{f}"] = float(v[s].mean() / v["C0"].mean()) if v["C0"].mean() > 0 else None; b[f"suficiencia_{f}_ci"] = ci(ratio)
    b["c0_menos_c1"] = float((v["C0"] - v["C1"]).mean()); b["c0_menos_c1_ci"] = ci(reps(qs, v["C0"] - v["C1"]))
    b["e3"] = {"preto_exclui_zero": b["delta_nec_preto_ci"][0] > 0, "plausivel_exclui_zero": {f: b[f"delta_nec_{f}_ci"][0] > 0 for f in ("blur10", "regmean")}}
    b["e3"]["necessario"] = b["e3"]["preto_exclui_zero"] and any(b["e3"]["plausivel_exclui_zero"].values())
    b["e3"]["so_solido"] = b["e3"]["preto_exclui_zero"] and not any(b["e3"]["plausivel_exclui_zero"].values())
    b["e3_rotina_heal"] = (nec_cls or {}).get("e3")
    floors = {"m0": np.array([M0[q] for q in qs], float)}
    if TX is not None: floors["proprio"] = np.array([TX[q] for q in qs], float)
    for fl, fv in floors.items():
        tv = v["C0"] - fv; rt = reps(qs, tv); teto = float(tv.mean()); tci = ci(rt)
        b[f"acc_piso_{fl}"] = float(fv.mean()); b[f"teto_{fl}"] = teto; b[f"teto_{fl}_ci"] = tci
        ratio = rd["preto"] / rt; drop = int((rt <= 0).sum()); ratio[rt <= 0] = np.nan
        b[f"ndelta_{fl}"] = float(b["delta_nec_preto"] / teto) if teto > 0 else None; b[f"ndelta_{fl}_ci"] = ci(ratio) if teto > 0 else None; b[f"ndelta_{fl}_reps_descartadas"] = drop
        b[f"utilizavel_E9_{fl}"] = bool(teto >= 0.10 and tci and tci[0] > 0); b[f"ndelta_{fl}_reportado"] = b[f"ndelta_{fl}"] if b[f"utilizavel_E9_{fl}"] else "n.u."
    return b
def analyse(line, fam, var, inv):
    files = {c: f"{R}/results/{line}_{c}.json" for c in CORE}; C = {c: load_correct(p) for c, p in files.items()}
    s = int(line[-1]); tp = f"{R}/results/{TXT[fam]}_MIMIC_seed{s}_TXT.json"; TX = load_correct(tp) if os.path.exists(tp) else None
    suf = "" if var == "completo" else "_so_exatas"; nj = f"{R}/analysis/necessity_{line}{suf}.json"; nec = json.load(open(nj)) if os.path.exists(nj) else {}
    if nec: inputs[nj] = sha(nj)
    Q = [q for q in inv["questions"] if q["evaluable"]]; aligned = [q["qid"] for q in Q if all(q["qid"] in C[c] for c in CORE)]
    al = set(aligned); cls = {k: [q["qid"] for q in Q if q["question_class"] == k and q["qid"] in al] for k in CLASSES}
    out = {"line": line, "variant": var, "txt": tp if TX else None, "necessity_json": nj if nec else None, "n_avaliaveis": collections.Counter(q["question_class"] for q in Q),
           "n_alinhadas": {k: len(v) for k, v in cls.items()}, "by_class": {k: block(v, C, TX, (nec.get("by_class") or {}).get(k)) for k, v in cls.items()}}
    for f in FILLS: 
        hp = holm({k: out["by_class"][k][f"mcnemar_{f}"]["p_midp"] for k in CLASSES if out["by_class"][k].get("n")})
        for k, p in hp.items(): out["by_class"][k][f"p_holm_{f}"] = p
    if var == "completo":
        out["estratos"] = {}
        for key, fn in (("n_target_boxes", lambda q: "1" if UNIT[q]["n_target_boxes"] == 1 else "2+"), ("placebo_scheme", lambda q: UNIT[q]["placebo_scheme"])):
            for k in ("closed_yes", "closed_no", "open"):
                for val in sorted({fn(q) for q in cls[k] if q in UNIT}):
                    out["estratos"][f"{k}|{key}={val}"] = block([q for q in cls[k] if q in UNIT and fn(q) == val], C, TX, None)
        # 13/10 (authors): C1 on the single-gold subset -- 'yes' rate under C1 and under C0 on the closed-ended questions (aligned)
        PC = {c: load_pred(f"{R}/results/{line}_{c}.json") for c in ("C0", "C1")}
        out["p_sim_c1"] = {k: {"n": len(cls[k]), "p_yes_C1": float(np.mean([PC["C1"][q] == "yes" for q in cls[k]])), "p_yes_C0": float(np.mean([PC["C0"][q] == "yes" for q in cls[k]]))} for k in ("closed_yes", "closed_no")}
        sq = [q for q in Q if q["question_class"] == "closed_no_sham"]; P = {c: load_pred(f"{R}/results/{line}_{c}.json") for c in ["C0"] + SHAM}
        common = [q["qid"] for q in sq if all(q["qid"] in P[c] for c in P)]; bss = ImageBootstrap([IMG[q] for q in common], N_BOOT, SEED)
        aff = {c: np.array([P[c][q] == "yes" for q in common]) for c in P}
        out["sham"] = {"n_avaliaveis": len(sq), "n_alinhadas": len(common), "n_imagens": len(bss.ids), "conds": {c: paired_block(aff[c], aff["C0"], [IMG[q] for q in common], bss) for c in SHAM}}
        out["sham"]["holm"] = holm({c: out["sham"]["conds"][c]["mcnemar"]["p_midp"] for c in SHAM})
        out["dose_rotina_heal"] = nec.get("dose")
    # 13/10 (authors): entities (closed_yes, n >= 30 in the full variant) in both variants
    ent_c = collections.Counter(q["entity"] for q in json.load(open(INV["completo"]))["questions"] if q["evaluable"] and q["question_class"] == "closed_yes")
    EN = {q["qid"]: q["entity"] for q in Q}
    out["por_entidade"] = {e: block([q for q in cls["closed_yes"] if EN[q] == e], C, TX, None) for e, n in ent_c.most_common() if n >= 30}
    # 13/10 (authors, per-entity saturation): P(yes | C0, black T, black P) on the same qids as the entity block
    PY = {c: load_pred(f"{R}/results/{line}_{c}.json") for c in ("C0", "T", "P")}
    for e, b in out["por_entidade"].items():
        qs = [q for q in cls["closed_yes"] if EN[q] == e and (TX is None or q in TX) and q in M0]
        b["p_sim"] = {c: float(np.mean([PY[c][q] == "yes" for q in qs])) for c in PY} if qs else None
    return out
def geometria_entidades():
    """13/10 (authors): target geometry per entity in closed_yes (inventory v2, evaluable). Control-occlusion method per box (token before ':'),
    grouped: broad anatomy = anatomy:<whole lung>; homologous anatomy = the other anatomy entries; vertical translation = vtrans, vtrans_pair;
    mirror = hflip, vflip; free translation = translate. Edema: fraction of items whose target contains 'left lung' and 'right lung'."""
    Q = [q for q in inv_all["questions"] if q["evaluable"] and q["question_class"] == "closed_yes"]
    ents = [e for e, n in collections.Counter(q["entity"] for q in Q).most_common() if n >= 30]; out = {"regra": geometria_entidades.__doc__}
    def cat(m):
        k, _, rest = m.partition(":")
        if k == "anatomy": return "anatomia larga" if rest in ("left lung", "right lung") else "anatomia homologa"
        return {"vtrans": "translacao vertical", "vtrans_pair": "translacao vertical", "hflip": "espelho", "vflip": "espelho", "translate": "translacao livre"}.get(k, k)
    for e in ents:
        qs = [q for q in Q if q["entity"] == e]; af = np.array([q["target_area_frac"] for q in qs], float)
        nb = collections.Counter(UNIT[q["qid"]]["n_target_boxes"] for q in qs if q["qid"] in UNIT)
        meth = collections.Counter(cat(m) for q in qs for m in (q.get("placebo_method") or "").split("|") if m)
        out[e] = {"n": len(qs), "n_caixas": {str(k): v for k, v in sorted(nb.items())}, "target_area_frac": {"mediana": float(np.median(af)), "q1": float(np.percentile(af, 25)), "q3": float(np.percentile(af, 75))},
                  "regioes_top3": collections.Counter(r for q in qs for r in q["target_regions"]).most_common(3), "metodo_placebo_por_caixa": dict(meth.most_common()),
                  "metodo_placebo_tokens": dict(collections.Counter(m.split(":")[0] for q in qs for m in (q.get("placebo_method") or "").split("|") if m).most_common())}
        if e == "edema": out[e]["fracao_alvo_dois_pulmoes_inteiros"] = float(np.mean([("left lung" in q["target_regions"] and "right lung" in q["target_regions"]) for q in qs]))
    return out
def main():
    t0 = time.time(); res = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "host": socket.gethostname(), "script": __file__, "script_sha256": sha(__file__), "regra": __doc__, "n_boot": N_BOOT, "seed": SEED, "n_imagens_teste": len(BS.ids),
           "inventario": {v: {"path": p, "sha256": sha(p)} for v, p in INV.items()}, "inventario_v2_resumo": inv_all["summary"], "manifesto": {"path": MAN, "sha256": sha(MAN)},
           "controle_negativo": "o inventario v2 do MIMIC nao tem classe de controle negativo puro (como o HEAL); registrado", "M3AE": "anexo: linhas M3AE_MIMIC_seed0-2; teto proprio pendente ate o M3AE so-texto (M3AE_TXT_MIMIC) sair", "linhas": []}
    for fam_key, fam, grp in FAMS:
        for s in range(3):
            line = f"{fam_key}_MIMIC_seed{s}"; rec = {"line": line, "family": fam, "group": grp, "seed": s}
            if any(not os.path.exists(f"{R}/results/{line}_{c}.json") for c in CORE + ["C0"] + SHAM): res["linhas"].append({"line": line, "family": fam, "group": grp, "status": "pendente"}); continue
            for var, p in INV.items(): rec[var] = analyse(line, fam, var, json.load(open(p)))
            res["linhas"].append(rec); print(line, round(time.time() - t0), "s", {k: round(v.get("delta_nec_preto", float("nan")), 4) for k, v in rec["completo"]["by_class"].items()}, flush=True)
    res["geometria_entidades"] = geometria_entidades()
    res["entradas_sha256"] = inputs
    json.dump(res, open(f"{R}/analysis/placebo_mimic.json", "w"), indent=1, default=lambda o: dict(o) if isinstance(o, collections.Counter) else str(o)); print("json ok", round(time.time() - t0), "s", flush=True)
    from harness.v7_txt.placebo_mimic_render import render; render(res)
if __name__ == "__main__": main()
