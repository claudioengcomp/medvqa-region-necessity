"""P2.2 analysis (2026-10-09): per run and Kvasir occluder-test (`sham`) condition, IPR = P(affirms | sham) - P(affirms | C0) paired per
item, where affirms = ART: yes; POL count: != 0; POL type: != none; INS presence: != none; INS count: != 0 (crossed
likewise). C0 per item: the published _C0.json (native; the crossed questions also exist natively) -- and, as a control, the
C0_cross generated in this round in the same session. McNemar mid-p; bootstrap by image (2000, seed 20260913, shared
replicates); Holm over the 8 conditions per run; family x condition table with mean and SD across seeds; native vs crossed
contrast on the same image (paired difference with CI); classification of the changed answers in the open-ended questions
(mentions the finding / artifact box / other). No interpretation."""
from __future__ import annotations
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import argparse, collections, hashlib, json, os, re, time
import numpy as np
from med_vlm.metrics.process_text import normalize_text
from harness.v7_sham.shamstats import ImageBootstrap, holm, paired_block
R = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_sham"; P0R = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-p0/results"; V5Q = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v5_qwen_vt/results"; V5S = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v5_smolvlm_ft/results"
LABEL = {"SHAM_ART_black": "controle positivo (a intervencao cria o artefato perguntado; resposta correta = yes)", "SHAM_ART_blur10": "sham do ART"}   # authors' labeling, 09/10 21:00; POL and INS are occluder tests (sham) in both versions
CONDS = ["SHAM_ART_black", "SHAM_ART_blur10", "SHAM_POL_Q1_black", "SHAM_POL_Q1_blur10", "SHAM_POL_Q3_black", "SHAM_POL_Q3_blur10", "SHAM_INS_black", "SHAM_INS_blur10"]
Q_ART = "Is there a green/black box artefact?"; Q_POLN = "How many polyps are in the image?"; Q_POLT = "What type of polyp is present?"; Q_INSP = "Are there any instruments in the image? Check all that are present."; Q_INSN = "How many instrumnets are in the image?"
def affirms(q, pred):
    p = normalize_text(str(pred))
    if q == Q_ART: return p == "yes"
    if q in (Q_POLN, Q_INSN): return p not in ("0", "zero", "none", "no")
    if q in (Q_POLT, Q_INSP): return p not in ("none", "no", "")
    raise KeyError(q)
def kind(pred, q):
    p = normalize_text(str(pred))
    if q in (Q_POLN, Q_POLT) and re.search(r"polyp|paris|adenoma|lesion|abnormal", p): return "menciona_achado"
    if q in (Q_INSP, Q_INSN) and re.search(r"instrument|forceps|clip|tube|snare|needle|biopsy", p): return "menciona_achado"
    if re.search(r"box|artefact|artifact|rectangle|black|green|square", p): return "menciona_caixa"
    return "outro"
def sha(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()
def lines(group):
    L = []
    if group == "published":
        for s in range(3): L.append((f"M3AE_KVASIR_seed{s}", f"{P0R}/M3AE_KVASIR_seed{s}_C0.json", "M3AE"))
        for F in ("QWEN2VL", "SMOLVLM"):
            for pe in ("LORA", "DORA"):
                for s in range(3): L.append((f"{F}_{pe}_KVASIR_seed{s}", f"{P0R}/{F}_{pe}_KVASIR_seed{s}_C0.json", f"{F}_{pe}"))
    elif group == "zeroshot":   # 14/10 (authors): the 4 original zero-shot runs; C0 from the main battery (MedVLThinker with the registered system prompt, as in the occluder test)
        for m in ("MEDGEMMA", "QWEN25VL", "LLAVA_MED", "MEDVLTHINKER"): L.append((f"{m}_ZEROSHOT_KVASIR", f"{os.environ.get('LAB_ROOT', 'LAB_ROOT')}/v7_zeroshot/results/{m}_ZEROSHOT_KVASIR_C0.json", f"{m}_ZEROSHOT"))
    else:
        for pe in ("LORA", "DORA"):
            for s in range(3): L.append((f"QWEN2VL_{pe}_VT_KVASIR_seed{s}", f"{V5Q}/QWEN2VL_{pe}_VT_KVASIR_seed{s}_C0.json", f"QWEN2VL_{pe}_VT"))
        for pe in ("LORA", "DORA"):
            for s in range(3): L.append((f"SMOLVLM_{pe}_FT_KVASIR_seed{s}", f"{V5S}/SMOLVLM_{pe}_FT_KVASIR_seed{s}_C0.json", f"SMOLVLM_{pe}_FT"))
    return L
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--groups", default="published,vtft,zeroshot"); ap.add_argument("--out-json", default=f"{R}/analysis/kvasir_sham.json"); ap.add_argument("--out-md", default=f"{R}/docs/kvasir_sham.md"); a = ap.parse_args()
    inv = json.load(open(f"{R}/inventory_kvasir_sham.json")); units = [u for u in inv["units"] if u["generated"]]
    # qid -> (image_id, question, origin, set) per condition
    Q = collections.defaultdict(dict)
    for u in units:
        for q in u["questions"]: Q[u["condition"]][q["qid"]] = {"image": u["image_id"], "q": q["question"], "origin": q["origin"], "set": u["set"]}
    all_imgs = sorted({u["image_id"] for u in units}); bs = ImageBootstrap(all_imgs, 2000, 20260913)
    out = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "inventory": f"{R}/inventory_kvasir_sham.json", "inventory_sha256": sha(f"{R}/inventory_kvasir_sham.json"), "affirmative_rule": "ART: yes; contagem: != 0; tipo/presenca: != none", "labels": LABEL, "n_boot": 2000, "seed": 20260913, "conditions": CONDS, "lines": []}
    for group in a.groups.split(","):
        for line, c0p, fam in lines(group):
            if not os.path.exists(c0p): out["lines"].append({"line": line, "group": group, "missing": ["C0"]}); continue
            C0 = {int(p["qid"]): p["predicted"] for p in json.load(open(c0p))["predictions"]}; C0F = {int(p["qid"]): p["correct"] for p in json.load(open(c0p))["predictions"]}
            rec = {"line": line, "group": group, "family_cell": fam, "c0_file": c0p, "c0_sha256": sha(c0p), "conditions": {}, "missing": []}
            c0x_p = f"{R}/results/{line}_C0_cross.json"
            if os.path.exists(c0x_p):
                C0X = {int(p["qid"]): p["predicted"] for p in json.load(open(c0x_p))["predictions"]}; common = [q for q in C0X if q in C0]
                rec["c0_cross_vs_published_c0"] = {"n": len(common), "n_identical_pred": int(sum(normalize_text(str(C0X[q])) == normalize_text(str(C0[q])) for q in common)), "note": "mesma (imagem, pergunta); predicao da sessao atual x publicada"}
            for cond in CONDS:
                p = f"{R}/results/{line}_{cond}.json"
                if not os.path.exists(p): rec["missing"].append(cond); continue
                S = {int(x["qid"]): x["predicted"] for x in json.load(open(p))["predictions"]}; SF = {int(x["qid"]): x["correct"] for x in json.load(open(p))["predictions"]}; qs = [q for q in Q[cond] if q in S and q in C0]
                blocks = {}
                for origin in ("all", "native", "cross"):
                    sel = [q for q in qs if origin == "all" or Q[cond][q]["origin"] == origin]
                    if not sel: continue
                    ac = np.array([affirms(Q[cond][q]["q"], S[q]) for q in sel]); a0 = np.array([affirms(Q[cond][q]["q"], C0[q]) for q in sel])
                    blocks[origin] = paired_block(ac, a0, [Q[cond][q]["image"] for q in sel], bs)
                    # C0 accuracy and accuracy under the occluder test on the SAME items (authors' request, 09/10 20:40), with CI by image
                    for lab, src in (("acc_c0", C0F), ("acc_sham", SF)):
                        v = np.array([bool(src[q]) for q in sel], float); blocks[origin][lab] = float(v.mean()); blocks[origin][lab + "_ci"] = bs.ci_mean_diff([Q[cond][q]["image"] for q in sel], v)
                    if cond == "SHAM_ART_black":   # positive control: sensitivity = P(yes | black sham), CI by image
                        blocks[origin]["sensitivity_p_yes"] = float(ac.mean()); blocks[origin]["sensitivity_ci"] = bs.ci_mean_diff([Q[cond][q]["image"] for q in sel], ac.astype(float))
                    blocks[origin]["by_question"] = {}
                    for qt in sorted({Q[cond][q]["q"] for q in sel}):
                        ss = [q for q in sel if Q[cond][q]["q"] == qt]; blocks[origin]["by_question"][qt] = paired_block(np.array([affirms(qt, S[q]) for q in ss]), np.array([affirms(qt, C0[q]) for q in ss]), [Q[cond][q]["image"] for q in ss], bs)
                # native vs crossed contrast on the same image (paired difference of d = affirms_sham - affirms_C0 between the native presence/count question and the crossed one)
                if "native" in blocks and "cross" in blocks:
                    byimg = collections.defaultdict(dict)
                    for q in qs: byimg[Q[cond][q]["image"]].setdefault(Q[cond][q]["origin"], []).append(float(affirms(Q[cond][q]["q"], S[q])) - float(affirms(Q[cond][q]["q"], C0[q])))
                    imgs = [i for i in byimg if "native" in byimg[i] and "cross" in byimg[i]]; d = np.array([np.mean(byimg[i]["native"]) - np.mean(byimg[i]["cross"]) for i in imgs])
                    blocks["native_minus_cross_per_image"] = {"n_images": len(imgs), "mean": float(d.mean()) if len(imgs) else None, "ci": bs.ci_mean_diff(imgs, d) if len(imgs) else None}
                # changed answers in the open-ended questions (count/type)
                ch = collections.Counter()
                for q in qs:
                    if Q[cond][q]["q"] in (Q_POLN, Q_POLT, Q_INSN) and normalize_text(str(S[q])) != normalize_text(str(C0[q])): ch[kind(S[q], Q[cond][q]["q"])] += 1
                blocks["changed_open_answers"] = dict(ch); blocks["file"] = p; blocks["sha256"] = sha(p); blocks["n"] = len(qs); blocks["label"] = LABEL.get(cond, "sham")
                rec["conditions"][cond] = blocks
            done = [c for c in CONDS if c in rec["conditions"]]
            rec["holm_all"] = holm({c: rec["conditions"][c]["all"]["mcnemar"]["p_midp"] for c in done}) if done else {}
            out["lines"].append(rec); print(line, {c: round(rec["conditions"][c]["all"]["ipr"], 3) for c in done}, "missing", rec["missing"], flush=True)
    fam = collections.defaultdict(list)
    for r in out["lines"]:
        if "family_cell" in r: fam[r["family_cell"]].append(r)
    def msd(vals): return (float(np.mean(vals)), float(np.std(vals, ddof=1)) if len(vals) > 1 else None)
    out["by_family"] = {}
    for k, rs in fam.items():
        fb = {}
        for c in CONDS:
            rr = [r for r in rs if c in r["conditions"]]
            if not rr: continue
            b = {"n_seeds": len(rr)}
            for key in ("ipr", "rate_c0", "rate_cond", "acc_c0", "acc_sham") + (("sensitivity_p_yes",) if c == "SHAM_ART_black" else ()):
                m, sd = msd([r["conditions"][c]["all"][key] for r in rr]); b[key + "_mean"] = m; b[key + "_sd"] = sd
            b["ipr_mean"], b["ipr_sd"] = b["ipr_mean"], b["ipr_sd"]; fb[c] = b
        out["by_family"][k] = fb
    # table by occluder size (quartiles of sham_area_frac_fov over the generated POL units), POL, per family (authors' request, 10/10)
    pol_units = [u for u in units if u["set"] == "POL" and u.get("sham_area_frac_fov") is not None]
    qcut = np.percentile([u["sham_area_frac_fov"] for u in pol_units], [25, 50, 75]); size_bin = {}
    for u in pol_units: size_bin[(u["condition"], u["image_id"])] = int(np.searchsorted(qcut, u["sham_area_frac_fov"], side="right"))
    out["pol_by_size"] = {"quartile_edges_sham_area_frac_fov": [float(x) for x in qcut], "n_units": len(pol_units), "bins": {}}
    for k, rs in fam.items():
        for cond in [c for c in CONDS if "POL" in c]:
            for b in range(4):
                per_seed = []; pooled_ac, pooled_a0, pooled_img = [], [], []
                for r in rs:
                    if cond not in r["conditions"]: continue
                    S = {int(x["qid"]): x["predicted"] for x in json.load(open(r["conditions"][cond]["file"]))["predictions"]}; C0 = {int(p_["qid"]): p_["predicted"] for p_ in json.load(open(r["c0_file"]))["predictions"]}
                    sel = [q for q in Q[cond] if q in S and q in C0 and size_bin.get((cond, Q[cond][q]["image"])) == b]
                    if not sel: continue
                    ac = np.array([affirms(Q[cond][q]["q"], S[q]) for q in sel]); a0 = np.array([affirms(Q[cond][q]["q"], C0[q]) for q in sel]); im = [Q[cond][q]["image"] for q in sel]
                    per_seed.append(paired_block(ac, a0, im, bs)["ipr"]); pooled_ac += list(ac); pooled_a0 += list(a0); pooled_img += im
                if pooled_img:
                    pb = paired_block(np.array(pooled_ac), np.array(pooled_a0), pooled_img, bs)
                    out["pol_by_size"]["bins"][f"{k}|{cond}|Q{b + 1}"] = {"family": k, "condition": cond, "size_quartile": b + 1, "n_items_pooled": len(pooled_img), "n_seeds": len(per_seed), "ipr_seed_mean": float(np.mean(per_seed)), "ipr_seed_sd": float(np.std(per_seed, ddof=1)) if len(per_seed) > 1 else None, "ipr_pooled": pb["ipr"], "ipr_pooled_ci": pb["ipr_ci"], "rate_c0_pooled": pb["rate_c0"], "rate_cond_pooled": pb["rate_cond"]}
    json.dump(out, open(a.out_json, "w"), indent=1)
    M = ["# Kvasir sham (P2.2)", "", f"Gerado {out['t']}. IPR = P(afirma | sham) - P(afirma | C0) pareada por item ({out['affirmative_rule']}); IC 95 % bootstrap por imagem (2000, seed 20260913, replicas compartilhadas); McNemar mid-p; Holm sobre as 8 condicoes por linha. Sem interpretacao.", "", "Rotulagem (candidato, 09/10): SHAM_ART_black = CONTROLE POSITIVO (a intervencao cria o artefato perguntado; resposta correta = yes; coluna sensibilidade = P(yes | sham preto) [IC]); SHAM_ART_blur10 = sham do ART; POL e INS = sham nas duas versoes.", "", "## Controle positivo ART (preto): sensibilidade = P(yes | sham preto) [IC], P(yes | C0), IPR", "", "| linha | sensibilidade [IC] | P(yes\\|C0) | IPR [IC] | n |", "|---|---|---|---|---|"] + [
        (lambda b: f"| {r['line']} | {b['sensitivity_p_yes']:.3f} [{b['sensitivity_ci'][0]:.3f}, {b['sensitivity_ci'][1]:.3f}] | {b['rate_c0']:.3f} | {b['ipr']:+.3f} [{b['ipr_ci'][0]:+.3f}, {b['ipr_ci'][1]:+.3f}] | {b['n']} |")(r["conditions"]["SHAM_ART_black"]["all"]) for r in out["lines"] if "SHAM_ART_black" in r.get("conditions", {})] + ["",
        "## Por linha (todas as perguntas da condicao): IPR [IC] p_Holm | Acc C0 [IC] -> Acc sob a condicao [IC] nos mesmos itens (n)", "", "| linha | " + " | ".join(c + (" (controle positivo)" if c == "SHAM_ART_black" else "") for c in CONDS) + " |", "|---|" + "---|" * len(CONDS)]
    for r in out["lines"]:
        if "conditions" not in r: M.append(f"| {r['line']} | faltam {r.get('missing')} |"); continue
        M.append(f"| {r['line']} | " + " | ".join((lambda b: f"{b['ipr']:+.3f} [{b['ipr_ci'][0]:+.3f}, {b['ipr_ci'][1]:+.3f}] p={r['holm_all'][c]:.2g} \\| C0 {b['acc_c0']:.3f} [{b['acc_c0_ci'][0]:.3f}, {b['acc_c0_ci'][1]:.3f}] -> {b['acc_sham']:.3f} [{b['acc_sham_ci'][0]:.3f}, {b['acc_sham_ci'][1]:.3f}] (n={b['n']})")(r["conditions"][c]["all"]) if c in r["conditions"] else "-" for c in CONDS) + " |")
    f2 = lambda m, sd: f"{m:+.3f} ({sd:.3f})" if sd is not None else f"{m:+.3f}"
    M += ["", "## Familia x condicao (media (DP) entre sementes): IPR | P(afirma|C0) -> P(afirma|cond) | Acc C0 -> Acc cond", "", "| celula | " + " | ".join(c + (" (controle positivo)" if c == "SHAM_ART_black" else "") for c in CONDS) + " |", "|---|" + "---|" * len(CONDS)]
    for k, v in out["by_family"].items(): M.append(f"| {k} | " + " | ".join((f"IPR {f2(v[c]['ipr_mean'], v[c]['ipr_sd'])} \\| {v[c]['rate_c0_mean']:.3f} -> {v[c]['rate_cond_mean']:.3f} \\| Acc {v[c]['acc_c0_mean']:.3f} -> {v[c]['acc_sham_mean']:.3f} (n={v[c]['n_seeds']})") if c in v else "-" for c in CONDS) + " |")
    M += ["", "## Controle positivo por familia: sensibilidade = P(yes | sham preto), media (DP) entre sementes", ""]
    for k, v in out["by_family"].items():
        if "SHAM_ART_black" in v: M.append(f"- {k}: {f2(v['SHAM_ART_black']['sensitivity_p_yes_mean'], v['SHAM_ART_black']['sensitivity_p_yes_sd'])} (n={v['SHAM_ART_black']['n_seeds']})")
    M += ["", "## Nativa x cruzada (POL e INS): IPR nativa, IPR cruzada, diferenca por imagem [IC]", "", "| linha | condicao | IPR nativa | IPR cruzada | nativa - cruzada [IC] |", "|---|---|---|---|---|"]
    for r in out["lines"]:
        for c, b in r.get("conditions", {}).items():
            if "cross" in b: M.append(f"| {r['line']} | {c} | {b['native']['ipr']:+.3f} | {b['cross']['ipr']:+.3f} | {b['native_minus_cross_per_image']['mean']:+.3f} [{b['native_minus_cross_per_image']['ci'][0]:+.3f}, {b['native_minus_cross_per_image']['ci'][1]:+.3f}] |")
    M += ["", "## Respostas alteradas nas abertas (contagem/tipo): menciona achado / menciona caixa / outro", ""]
    for r in out["lines"]:
        for c, b in r.get("conditions", {}).items(): M.append(f"- {r['line']} {c}: {b['changed_open_answers']}")
    e = out["pol_by_size"]["quartile_edges_sham_area_frac_fov"]
    M += ["", f"## POL por tamanho do sham (quartis de sham_area_frac_fov sobre as {out['pol_by_size']['n_units']} unidades POL geradas; cortes {e[0]:.3f} / {e[1]:.3f} / {e[2]:.3f}): IPR media (DP) entre sementes | IPR agrupando as sementes [IC por imagem] (n itens)", "", "| celula | condicao | Q1 (menor) | Q2 | Q3 | Q4 (maior) |", "|---|---|---|---|---|---|"]
    for k in out["by_family"]:
        for cond in [c for c in CONDS if "POL" in c]:
            cells = []
            for b in range(1, 5):
                x = out["pol_by_size"]["bins"].get(f"{k}|{cond}|Q{b}")
                cells.append(f"{x['ipr_seed_mean']:+.3f} ({x['ipr_seed_sd']:.3f}) \\| {x['ipr_pooled']:+.3f} [{x['ipr_pooled_ci'][0]:+.3f}, {x['ipr_pooled_ci'][1]:+.3f}] (n={x['n_items_pooled']})" if x and x["ipr_seed_sd"] is not None else (f"{x['ipr_pooled']:+.3f} [{x['ipr_pooled_ci'][0]:+.3f}, {x['ipr_pooled_ci'][1]:+.3f}] (n={x['n_items_pooled']})" if x else "-"))
            M.append(f"| {k} | {cond} | " + " | ".join(cells) + " |")
    M += ["", "## C0_cross (sessao atual) x C0 publicada, mesma (imagem, pergunta)", ""]
    for r in out["lines"]:
        if "c0_cross_vs_published_c0" in r: M.append(f"- {r['line']}: {r['c0_cross_vs_published_c0']['n_identical_pred']}/{r['c0_cross_vs_published_c0']['n']} predicoes identicas")
    open(a.out_md, "w").write("\n".join(M) + "\n"); print("FIM")
if __name__ == "__main__": main()
