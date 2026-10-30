"""v7_artigo1/scripts/engine.py -- the single statistical engine of the paper (round 1, 19/10/2026).
Metric (definitions of harness/isbi_placebo/compute_necessity.py): Acc per condition; Delta = Acc(P) - Acc(T), paired; cost of the displaced
mask = Acc(C0) - Acc(P); cost of the target = Acc(C0) - Acc(T); sufficiency = Acc(S)/Acc(C0). Alignment: evaluable qids present in all the main
conditions loaded for the run (as in compute_necessity: missing ones are reported).
Inference (harness/v7_sham/shamstats.py, the routine of heal_sham, kvasir_sham and placebo_mimic): percentile 95 % CI by PER-IMAGE bootstrap,
2 000 replicates, seed 20260913, replicates FIXED PER BENCHMARK (one weight matrix over the sorted list of all images of the benchmark's test
inventory, the same for every run, condition and class); the per-item mean is reweighted by the sampled images (all questions/units of an image
enter together). Mid-p McNemar (exact binomial with half weight on the observed value) on the P x T discordant items.
Holm per run (and per fill) over the family of classes declared for the benchmark."""
import collections, json, os, sys
import numpy as np
from common import CODE_ROOT
sys.path.insert(0, CODE_ROOT)
from harness.v7_sham.shamstats import ImageBootstrap, holm, mcnemar_midp
N_BOOT, SEED = 2000, 20260913
FILLS = {"preto": ("T", "P", "S"), "blur10": ("T_blur10", "P_blur10", "S_blur10"), "regmean": ("T_regmean", "P_regmean", "S_regmean")}
CORE = ["C0", "T", "P", "S", "T_blur10", "P_blur10", "T_regmean", "P_regmean"]   # S_blur10/S_regmean only on MIMIC (see item 1)
class Base:
    def __init__(self, image_of: dict):
        self.IMG = image_of; self.bs = ImageBootstrap(sorted(set(image_of.values())), N_BOOT, SEED); self.n_img = len(self.bs.ids)
    def reps(self, qs, v):
        idx = np.array([self.bs.index[self.IMG[q]] for q in qs]); n = self.n_img
        num = np.bincount(idx, weights=np.asarray(v, float), minlength=n); den = np.bincount(idx, minlength=n).astype(float)
        return (self.bs.W @ num) / np.maximum(self.bs.W @ den, 1e-9)
def ci(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    return [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))] if len(x) else None
def load_correct(p): return {int(x["qid"]): bool(x["correct"]) for x in json.load(open(p))["predictions"]}
def load_pred(p): return {int(x["qid"]): x["predicted"] for x in json.load(open(p))["predictions"]}
def block(B: Base, qs, C: dict, TX=None, M0=None):
    """C: cond -> {qid: correct}; qs already aligned. Returns the block of one class."""
    if not qs: return {"n": 0}
    n = len(qs); v = {c: np.array([C[c][q] for q in qs], float) for c in C}; R = {}
    def R_(c):
        if c not in R: R[c] = B.reps(qs, v[c])
        return R[c]
    b = {"n": n, "n_imagens": len({B.IMG[q] for q in qs}), "acc": {c: float(v[c].mean()) for c in v}, "acc_ci_by_image": {c: ci(R_(c)) for c in v}}
    for f, (t, p, s) in FILLS.items():
        if t not in v or p not in v: continue
        d = v[p] - v[t]; rd = B.reps(qs, d); mc = mcnemar_midp(v[p].astype(bool), v[t].astype(bool))
        b[f"delta_{f}"] = float(d.mean()); b[f"delta_{f}_ci_by_image"] = ci(rd); b[f"mcnemar_midp_{f}"] = mc
        b[f"custo_mascara_deslocada_{f}"] = float((v["C0"] - v[p]).mean()); b[f"custo_mascara_deslocada_{f}_ci_by_image"] = ci(B.reps(qs, v["C0"] - v[p]))
        b[f"custo_alvo_{f}"] = float((v["C0"] - v[t]).mean()); b[f"custo_alvo_{f}_ci_by_image"] = ci(B.reps(qs, v["C0"] - v[t]))
        if s in v:
            r0 = R_("C0"); rs = R_(s); ratio = np.where(r0 > 0, rs / np.where(r0 > 0, r0, 1), np.nan)
            b[f"suficiencia_{f}"] = float(v[s].mean() / v["C0"].mean()) if v["C0"].mean() > 0 else None; b[f"suficiencia_{f}_ci_by_image"] = ci(ratio)
    ex = {f: (b.get(f"delta_{f}_ci_by_image") or [0, 0])[0] > 0 for f in FILLS if f"delta_{f}_ci_by_image" in b}
    b["exclui_zero_por_cima"] = ex
    if all(k in ex for k in ("preto", "blur10")):
        b["criterio_B"] = bool(ex["preto"] and ex["blur10"])
        if "regmean" in ex: b["criterio_A"] = bool(ex["preto"] and (ex["blur10"] or ex["regmean"])); b["criterio_C"] = bool(ex["preto"] and ex["blur10"] and ex["regmean"])
    if TX is not None:
        q2 = [q for q in qs if q in TX]
        if q2:
            vt = np.array([TX[q] for q in q2], float); vc = np.array([C["C0"][q] for q in q2], float); rh = B.reps(q2, vc - vt)
            b["n_txt"] = len(q2); b["acc_txt"] = float(vt.mean()); b["acc_txt_ci_by_image"] = ci(B.reps(q2, vt))
            b["headroom"] = float((vc - vt).mean()); b["headroom_ci_by_image"] = ci(rh)
            b["resoluvel"] = bool(b["headroom"] >= 0.10 and b["headroom_ci_by_image"] and b["headroom_ci_by_image"][0] > 0)
    if M0 is not None:
        q3 = [q for q in qs if q in M0]
        if q3:
            vm = np.array([M0[q] for q in q3], float); vc = np.array([C["C0"][q] for q in q3], float)
            b["n_m0"] = len(q3); b["acc_m0"] = float(vm.mean()); b["headroom_m0"] = float((vc - vm).mean()); b["headroom_m0_ci_by_image"] = ci(B.reps(q3, vc - vm))
    return b
def holm_line(by_class: dict, family: list):
    for f in FILLS:
        pv = {k: by_class[k][f"mcnemar_midp_{f}"]["p_midp"] for k in family if k in by_class and f"mcnemar_midp_{f}" in by_class[k]}
        for k, p in holm(pv).items(): by_class[k][f"p_holm_{f}"] = p
def ipr_block(B: Base, qs, aff_c: dict, aff_0: dict):
    qs = [q for q in qs if q in aff_c and q in aff_0]
    if not qs: return {"n": 0}
    a = np.array([aff_c[q] for q in qs], bool); z = np.array([aff_0[q] for q in qs], bool); d = a.astype(float) - z.astype(float)
    return {"n": len(qs), "n_imagens": len({B.IMG[q] for q in qs}), "taxa_afirma_intacta": float(z.mean()), "taxa_afirma_oclusor": float(a.mean()), "taxa_induzida": float(d.mean()),
            "taxa_induzida_ci_by_image": ci(B.reps(qs, d)), "mcnemar_midp": mcnemar_midp(a, z), "n_induzidas": int((a & ~z).sum()), "n_revertidas": int((~a & z).sum())}
