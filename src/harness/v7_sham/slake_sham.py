"""P2.3 analysis (2026-10-10): SLAKE occluder test (`sham`; negatives by template polarity). IPR = P(affirms disease | sham) - P(affirms disease | C0)
paired per item, affirms = normalized prediction == affirms_disease_answer (gold inverted per template: "no" in the healthy ones,
"yes" in the presence ones). Reports the 22 items and the 16 pure_negative separately; CI by bootstrap by image only (2000, seed
20260913), no Holm (authors' decision: small n). Per run and mean (SD) per family. No interpretation."""
from __future__ import annotations
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import collections, hashlib, json, os, time
import numpy as np
from med_vlm.metrics.process_text import normalize_text
from harness.v7_sham.shamstats import ImageBootstrap, paired_block
R = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_sham"; P0R = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-p0/results"; CONDS = ["SHAM_DIS_black", "SHAM_DIS_blur10"]
# reference C0 = the _C0.json of the FULL SLAKE test set (1,061 items, p0/results): the control-occlusion _C0.json cover only the 388 evaluable and would leave 13 of the 22 negatives unpaired
def pub(F, pe, s): return f"{P0R}/{F}_{pe}_SLAKE" + ("" if s == 0 else f"_seed{s}") + "_C0.json"
def sha(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()
def main():
    inv = json.load(open(f"{R}/inventory_slake_sham.json")); Q = {}
    for u in inv["units"]:
        if not u["generated"]: continue
        for q in u["questions"]: Q[q["qid"]] = {"image": u["image_id"], "q": q["question"], "aff": q["affirms_disease_answer"], "pol": q["polarity"], "pure": q["pure_negative"], "gold": q["gold"]}
    bs = ImageBootstrap([v["image"] for v in Q.values()], 2000, 20260913)
    lines = [(f"M3AE_SCRATCH_SLAKE_seed{s}", pub("M3AE", "SCRATCH", s), "M3AE_SCRATCH") for s in range(3)] + [(f"{F}_{pe}_SLAKE_seed{s}", pub(F, pe, s), f"{F}_{pe}") for F in ("QWEN2VL", "SMOLVLM") for pe in ("LORA", "DORA") for s in range(3)]
    # 14/10 (authors, item 2 of the wrap-up): the 12 VT/FT; C0 from the full v5 test set (as the published runs use the p0 one)
    lines += [(f"{F}_{pe}_{t}_SLAKE_seed{s}", f"{root}/{F}_{pe}_{t}_SLAKE_seed{s}_C0.json", f"{F}_{pe}_{t}") for F, t, root in (("QWEN2VL", "VT", os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v5_qwen_vt/results"), ("SMOLVLM", "FT", os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v5_smolvlm_ft/results")) for pe in ("LORA", "DORA") for s in range(3)]
    out = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "inventory": f"{R}/inventory_slake_sham.json", "inventory_sha256": sha(f"{R}/inventory_slake_sham.json"), "n_items": len(Q), "n_pure_negative": sum(v["pure"] for v in Q.values()), "n_images": len(bs.ids), "rule": "afirma = normalize_text(predicted) == affirms_disease_answer; so IC por bootstrap por imagem, sem Holm", "c0_reference": "p0/results _C0.json do teste completo (1061 itens); a C0 do placebo (388 avaliaveis) cobre so 9 dos 22 negativos", "lines": []}
    for line, c0p, fam in lines:
        C0 = {int(p["qid"]): p["predicted"] for p in json.load(open(c0p))["predictions"]}; rec = {"line": line, "family_cell": fam, "c0_file": c0p, "c0_sha256": sha(c0p), "conditions": {}, "missing": []}
        for cond in CONDS:
            p = f"{R}/results/{line}_{cond}.json"
            if not os.path.exists(p): rec["missing"].append(cond); continue
            S = {int(x["qid"]): x["predicted"] for x in json.load(open(p))["predictions"]}; blk = {"file": p, "sha256": sha(p)}
            for sub, sel in (("all_22", [q for q in Q if q in S and q in C0]), ("pure_16", [q for q in Q if q in S and q in C0 and Q[q]["pure"]])):
                ac = np.array([normalize_text(str(S[q])) == Q[q]["aff"] for q in sel]); a0 = np.array([normalize_text(str(C0[q])) == Q[q]["aff"] for q in sel])
                b = paired_block(ac, a0, [Q[q]["image"] for q in sel], bs); b.pop("mcnemar", None); b["by_polarity"] = {}
                for pol in ("healthy", "presence"):
                    ss = [q for q in sel if Q[q]["pol"] == pol]
                    if ss: bb = paired_block(np.array([normalize_text(str(S[q])) == Q[q]["aff"] for q in ss]), np.array([normalize_text(str(C0[q])) == Q[q]["aff"] for q in ss]), [Q[q]["image"] for q in ss], bs); bb.pop("mcnemar", None); b["by_polarity"][pol] = bb
                blk[sub] = b
            rec["conditions"][cond] = blk
        out["lines"].append(rec); print(line, {c: (round(b["all_22"]["ipr"], 3), round(b["pure_16"]["ipr"], 3)) for c, b in rec["conditions"].items()}, flush=True)
    fam = collections.defaultdict(list)
    for r in out["lines"]: fam[r["family_cell"]].append(r)
    out["by_family"] = {k: {c: {sub: {"ipr_mean": float(np.mean([r["conditions"][c][sub]["ipr"] for r in rs if c in r["conditions"]])), "ipr_sd": float(np.std([r["conditions"][c][sub]["ipr"] for r in rs if c in r["conditions"]], ddof=1)) if sum(c in r["conditions"] for r in rs) > 1 else None, "rate_c0_mean": float(np.mean([r["conditions"][c][sub]["rate_c0"] for r in rs if c in r["conditions"]])), "rate_cond_mean": float(np.mean([r["conditions"][c][sub]["rate_cond"] for r in rs if c in r["conditions"]]))} for sub in ("all_22", "pure_16")} for c in CONDS if any(c in r["conditions"] for r in rs)} for k, rs in fam.items()}
    json.dump(out, open(f"{R}/analysis/slake_sham.json", "w"), indent=1)
    M = ["# SLAKE sham (P2.3) -- negativos por polaridade do template", "", f"Gerado {out['t']}. {out['n_items']} itens em {out['n_images']} imagens; {out['n_pure_negative']} pure_negative (os 6 'Can X be observed on the <lobo>...?' ficam fora do subconjunto puro). Afirma = resposta que afirma doenca (gold invertido por template). IPR = P(afirma|sham) - P(afirma|C0), pareada por item; IC 95 % por bootstrap por imagem (2000, seed 20260913); sem Holm (n pequeno). Sem interpretacao.", "", "| linha | condicao | 22 itens: P(afirma\\|C0) -> P(afirma\\|sham), IPR [IC] | 16 puros: P(afirma\\|C0) -> P(afirma\\|sham), IPR [IC] | healthy (11) IPR | presence (11) IPR |", "|---|---|---|---|---|---|"]
    for r in out["lines"]:
        for c, b in r["conditions"].items():
            a, p_ = b["all_22"], b["pure_16"]; M.append(f"| {r['line']} | {c} | {a['rate_c0']:.3f} -> {a['rate_cond']:.3f}, {a['ipr']:+.3f} [{a['ipr_ci'][0]:+.3f}, {a['ipr_ci'][1]:+.3f}] | {p_['rate_c0']:.3f} -> {p_['rate_cond']:.3f}, {p_['ipr']:+.3f} [{p_['ipr_ci'][0]:+.3f}, {p_['ipr_ci'][1]:+.3f}] | " + " | ".join((f"{a['by_polarity'][pol]['ipr']:+.3f} [{a['by_polarity'][pol]['ipr_ci'][0]:+.3f}, {a['by_polarity'][pol]['ipr_ci'][1]:+.3f}]" if pol in a["by_polarity"] else "-") for pol in ("healthy", "presence")) + " |")
    M += ["", "## Por familia (media (DP) do IPR entre sementes; P(afirma|C0) -> P(afirma|sham) medios)", "", "| celula | condicao | 22 itens | 16 puros |", "|---|---|---|---|"]
    for k, v in out["by_family"].items():
        for c, d in v.items():
            f = lambda x: (f"{x['ipr_mean']:+.3f} ({x['ipr_sd']:.3f})" if x["ipr_sd"] is not None else f"{x['ipr_mean']:+.3f}") + f"; {x['rate_c0_mean']:.3f} -> {x['rate_cond_mean']:.3f}"
            M.append(f"| {k} | {c} | {f(d['all_22'])} | {f(d['pure_16'])} |")
    open(f"{R}/docs/slake_sham.md", "w").write("\n".join(M) + "\n"); print("FIM")
if __name__ == "__main__": main()
