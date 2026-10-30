"""P2.1 (2026-10-09): HEAL occluder test (`sham` in the code) with no new image -- on the already published per-condition prediction files
(T, P, S, T_blur10, P_blur10, T_regmean, P_regmean; C0 as base), restricted to the evaluable closed_no items of the
inventory: IPR_c = P(yhat = yes | c) - P(yhat = yes | C0), paired per item; McNemar mid-p; bootstrap by image
(2000, seed 20260913, the same replicates for all runs); Holm over the conditions per run; also per anatomy.
T on closed_no = "hide the queried anatomy in an image without the finding". No image file is created."""
from __future__ import annotations
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import argparse, collections, hashlib, json, os, time
import numpy as np
from med_vlm.metrics.process_text import normalize_text
from harness.v7_sham.shamstats import ImageBootstrap, holm, paired_block

ISBI = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-placebo/results/isbi_placebo"; V6R = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v6_tower_heal/results"; V6P = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v6_tower_heal/results_placebo"
CONDS = ["T", "P", "S", "T_blur10", "P_blur10", "T_regmean", "P_regmean"]
PUB = ["M3AE_HEAL_seed%d", "QWEN2VL_LORA_HEAL_seed%d", "QWEN2VL_DORA_HEAL_seed%d", "SMOLVLM_LORA_HEAL_seed%d", "SMOLVLM_DORA_HEAL_seed%d"]
VTFT = ["QWEN2VL_LORA_VT_HEAL_seed%d", "QWEN2VL_DORA_VT_HEAL_seed%d", "SMOLVLM_LORA_FT_HEAL_seed%d", "SMOLVLM_DORA_FT_HEAL_seed%d"]
def sha(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()
def lines():
    L = []
    for t in PUB:
        for s in range(3): n = t % s; L.append({"line": n, "group": "publicada", "family": n.split("_")[0], "seed": s, "files": {c: f"{ISBI}/{n}_{c}.json" for c in ["C0"] + CONDS}})
    for t in VTFT:
        for s in range(3): n = t % s; L.append({"line": n, "group": "VT/FT", "family": n.split("_")[0], "seed": s, "files": {**{"C0": f"{V6R}/{n}_C0.json"}, **{c: f"{V6P}/{n}_{c}.json" for c in CONDS}}})
    return L
def preds(p): return {int(x["qid"]): normalize_text(str(x["predicted"])) for x in json.load(open(p))["predictions"]}
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--inventory", default=f"{ISBI}/inventory_heal_test.json"); ap.add_argument("--out-json", required=True); ap.add_argument("--out-md", required=True)
    ap.add_argument("--n-boot", type=int, default=2000); ap.add_argument("--seed", type=int, default=20260913); a = ap.parse_args()
    inv = json.load(open(a.inventory)); items = [q for q in inv["questions"] if q["question_class"] == "closed_no" and q["evaluable"]]
    qids = [q["qid"] for q in items]; img_of = {q["qid"]: q["image_id"] for q in items}; anat_of = {q["qid"]: q["anatomy"] for q in items}
    bs = ImageBootstrap([img_of[q] for q in qids], a.n_boot, a.seed)
    out = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "inventory": a.inventory, "inventory_sha256": sha(a.inventory), "selection": "question_class == closed_no and evaluable", "n_items": len(qids), "n_images": len(bs.ids),
           "anatomies": dict(collections.Counter(anat_of[q] for q in qids)), "conditions": CONDS, "affirmative": "normalize_text(predicted) == 'yes'", "n_boot": a.n_boot, "seed": a.seed, "bootstrap": "por imagem, replicas fixas compartilhadas por todas as linhas", "lines": []}
    for L in lines():
        missing = [c for c, p in L["files"].items() if not os.path.exists(p)]
        rec = {**{k: L[k] for k in ("line", "group", "family", "seed")}, "files": {c: {"path": p, "sha256": sha(p) if os.path.exists(p) else None} for c, p in L["files"].items()}, "missing": missing}
        if missing: out["lines"].append(rec); continue
        P = {c: preds(p) for c, p in L["files"].items()}
        common = [q for q in qids if all(q in P[c] for c in P)]; rec["n_aligned"] = len(common); rec["n_not_aligned"] = len(qids) - len(common)
        aff = {c: np.array([P[c][q] == "yes" for q in common]) for c in P}; imgs = [img_of[q] for q in common]
        rec["overall"] = {c: paired_block(aff[c], aff["C0"], imgs, bs) for c in CONDS}
        rec["holm"] = holm({c: rec["overall"][c]["mcnemar"]["p_midp"] for c in CONDS})
        rec["by_anatomy"] = {}
        for an in sorted(set(anat_of[q] for q in common)):
            sel = np.array([anat_of[q] == an for q in common]); im = [img_of[q] for q, s in zip(common, sel) if s]
            rec["by_anatomy"][an] = {c: paired_block(aff[c][sel], aff["C0"][sel], im, bs) for c in CONDS}
        out["lines"].append(rec); print(L["line"], "n", len(common), {c: round(rec["overall"][c]["ipr"], 4) for c in CONDS}, flush=True)
    # mean and SD over seeds per family x group
    fam = collections.defaultdict(list)
    for r in out["lines"]:
        if "overall" in r: fam[(r["group"], r["family"], r["line"].rsplit("_seed", 1)[0])].append(r)
    out["by_family"] = {}
    for (g, f, key), rs in fam.items():
        out["by_family"][key] = {"group": g, "family": f, "n_seeds": len(rs), **{c: {"ipr_mean": float(np.mean([r["overall"][c]["ipr"] for r in rs])), "ipr_sd": float(np.std([r["overall"][c]["ipr"] for r in rs], ddof=1)) if len(rs) > 1 else None,
                                                                               "rate_c0_mean": float(np.mean([r["overall"][c]["rate_c0"] for r in rs])), "rate_cond_mean": float(np.mean([r["overall"][c]["rate_cond"] for r in rs]))} for c in CONDS}}
    json.dump(out, open(a.out_json, "w"), indent=1)
    # markdown
    M = ["# HEAL sham (P2.1) -- taxa de afirmativa induzida em closed_no", "", f"Gerado {out['t']}. Itens: {len(qids)} closed_no avaliaveis em {len(bs.ids)} imagens. Afirma = predicao normalizada == 'yes'. IPR_c = P(yes|c) - P(yes|C0), pareada por item; IC 95 % por bootstrap por imagem ({a.n_boot} replicas, seed {a.seed}, as mesmas em todas as linhas); McNemar mid-p; Holm sobre as {len(CONDS)} condicoes por linha. Numeros sem interpretacao.", "",
         "## Por linha", "", "| linha | grupo | n | P(yes\\|C0) | " + " | ".join(f"{c}: IPR [IC] p_Holm" for c in CONDS) + " |", "|---|---|---|---|" + "---|" * len(CONDS)]
    for r in out["lines"]:
        if "overall" not in r: M.append(f"| {r['line']} | {r['group']} | faltam: {r['missing']} |"); continue
        o = r["overall"]; M.append(f"| {r['line']} | {r['group']} | {r['n_aligned']} | {o['T']['rate_c0']:.3f} | " + " | ".join(f"{o[c]['ipr']:+.3f} [{o[c]['ipr_ci'][0]:+.3f}, {o[c]['ipr_ci'][1]:+.3f}] {r['holm'][c]:.3g}" for c in CONDS) + " |")
    M += ["", "## Media e DP entre sementes (IPR)", "", "| celula | grupo | n sementes | " + " | ".join(CONDS) + " |", "|---|---|---|" + "---|" * len(CONDS)]
    for k, v in out["by_family"].items():
        M.append(f"| {k} | {v['group']} | {v['n_seeds']} | " + " | ".join(f"{v[c]['ipr_mean']:+.3f} ({v[c]['ipr_sd']:.3f})" if v[c]["ipr_sd"] is not None else f"{v[c]['ipr_mean']:+.3f}" for c in CONDS) + " |")
    M += ["", "## Por anatomia (T e P, IPR [IC], mid-p sem Holm)", "", "| linha | anatomia | n | T | P | S |", "|---|---|---|---|---|---|"]
    for r in out["lines"]:
        if "by_anatomy" not in r: continue
        for an, d in r["by_anatomy"].items():
            M.append(f"| {r['line']} | {an} | {d['T']['n']} | " + " | ".join(f"{d[c]['ipr']:+.3f} [{d[c]['ipr_ci'][0]:+.3f}, {d[c]['ipr_ci'][1]:+.3f}] p={d[c]['mcnemar']['p_midp']:.3g}" for c in ("T", "P", "S")) + " |")
    open(a.out_md, "w").write("\n".join(M) + "\n"); print("FIM", a.out_json, a.out_md)
if __name__ == "__main__": main()
