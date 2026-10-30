"""Round 13 (22/10/2026, CPU). Items 1-2: per image-target pair of the condition arrows (Kvasir 243, HEAL 1 360, Medical-Diff-VQA 1 266 units):
target mask = union of the pixels changed by T (black), T_blur10 or T_blur (4 %) relative to the intact image (a target pixel that no fill changes
is left out); mean absolute change inside the mask (0-255, mean over channels) for black, blur 10 % and blur 4 %; blur/black ratios; equivalent
diameter sqrt(4 area/pi) in px and in % of the width; sigma/diameter for the sigma of each blur (blur 10 % = 0.10 x image width; blur 4 % = fixed
sigma of the benchmark: Kvasir 25 px, HEAL and Medical-Diff-VQA from the round-10 manifest); fraction of pairs with sigma < diameter/2.
Item 3: raw drop under blur 10 % = per-image CI of Acc(C0) - Acc(T_blur10) (custo_alvo_blur10, already computed on the same replicates in
analysis/necessity_v2) among the declared runs (L3 and raw drop under black). Output: analysis/rodada13.json."""
import io, json, os, sys, time
from concurrent.futures import ProcessPoolExecutor
import numpy as np, pyarrow as pa
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
A = f"{PLC}/data/isbi_placebo"; TK = LAB_BLUR4_ARROWS; BM = json.load(open(f"{BLUR4_META}/manifest_blur4_r10.json"))
ARW = {"KVASIR": {c: f"{A}/vqa_kvasir_placebo_{c}.arrow" for c in ("C0", "T", "T_blur10", "T_blur")},
       "HEAL": {"C0": f"{A}/vqa_heal_placebo_C0.arrow", "T": f"{A}/vqa_heal_placebo_T.arrow", "T_blur10": f"{A}/vqa_heal_placebo_T_blur10.arrow", "T_blur": f"{TK}/vqa_heal_placebo_T_blur.arrow"},
       "MIMIC": {"C0": f"{V7M}/data/conditions/vqa_mimic_placebo_C0.arrow", "T": f"{V7M}/data/conditions/vqa_mimic_placebo_T.arrow", "T_blur10": f"{V7M}/data/conditions/vqa_mimic_placebo_T_blur10.arrow", "T_blur": f"{TK}/vqa_mimic_placebo_T_blur.arrow"}}
SIG4 = {"KVASIR": 25.0, "HEAL": BM["heal"]["sigma_px"], "MIMIC": BM["mimic"]["sigma_px"]}
def table(p):
    s = pa.memory_map(p)
    try: return pa.ipc.open_file(s).read_all()
    except Exception: return pa.ipc.open_stream(pa.memory_map(p)).read_all()
def dec(b): return np.asarray(Image.open(io.BytesIO(b)).convert("RGB")).astype(np.int16)
def unit(args):
    base, bs = args; c0, t, b10, b4 = (dec(b) for b in bs); H, Wd = c0.shape[:2]
    m = np.any(t != c0, 2) | np.any(b10 != c0, 2) | np.any(b4 != c0, 2); a = int(m.sum())
    if a == 0: return None
    ch = lambda x: float(np.abs(x[m] - c0[m]).mean())
    d = (4 * a / np.pi) ** 0.5; s10 = 0.10 * Wd; s4 = SIG4[base]
    return {"preto": ch(t), "blur10": ch(b10), "blur4": ch(b4), "area_px": a, "diam_px": d, "diam_pct_largura": 100 * d / Wd, "sigma10_px": s10, "sigma4_px": s4, "largura": Wd}
def stats(xs):
    xs = np.asarray(xs, float); return {"mediana": float(np.median(xs)), "q1": float(np.percentile(xs, 25)), "q3": float(np.percentile(xs, 75)), "n": int(len(xs))}
OUTJ = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "arrows": {b: {c: {"file": p, "sha256": sha(p)} for c, p in d.items()} for b, d in ARW.items()}, "itens_1_2": {}, "item3": {}}
for b, d in ARW.items():
    T_ = {c: table(p) for c, p in d.items()}; ids = [T_[c].column("image_id").to_pylist() for c in d]; assert all(x == ids[0] for x in ids), b
    jobs = [(b, [T_[c].column("image")[i].as_py() for c in ("C0", "T", "T_blur10", "T_blur")]) for i in range(len(ids[0]))]
    with ProcessPoolExecutor(max_workers=6) as ex: R = [r for r in ex.map(unit, jobs, chunksize=4) if r]
    OUTJ["itens_1_2"][b] = {"pares": len(R), "pares_sem_mascara": len(jobs) - len(R), "sigma4_px": SIG4[b],
        "alteracao_preto": stats([r["preto"] for r in R]), "alteracao_blur10": stats([r["blur10"] for r in R]), "alteracao_blur4": stats([r["blur4"] for r in R]),
        "razao_blur10_preto": stats([r["blur10"] / r["preto"] for r in R]), "razao_blur4_preto": stats([r["blur4"] / r["preto"] for r in R]),
        "diametro_px": stats([r["diam_px"] for r in R]), "diametro_pct_largura": stats([r["diam_pct_largura"] for r in R]),
        "sigma4_sobre_diametro": stats([r["sigma4_px"] / r["diam_px"] for r in R]), "sigma10_sobre_diametro": stats([r["sigma10_px"] / r["diam_px"] for r in R]),
        "fracao_sigma4_menor_meio_diametro": float(np.mean([r["sigma4_px"] < r["diam_px"] / 2 for r in R])), "fracao_sigma10_menor_meio_diametro": float(np.mean([r["sigma10_px"] < r["diam_px"] / 2 for r in R]))}
    print(b, json.dumps({k: (round(v["mediana"], 3) if isinstance(v, dict) else v) for k, v in OUTJ["itens_1_2"][b].items()}), flush=True)
def lo(bk, k): c = (bk or {}).get(k); return c[0] if c else None
TCL = {"KVASIR": ["dependent_polyp", "dependent_instrument", "negative_control"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no"]}
for b in BASES:
    recs = [(L["line"], False) for L in lines(b)] + [(f"{m}_ZEROSHOT_{b}", True) for m in ZS]
    for c in TCL[b]:
        for kind in ("afinados", "zero_shot"):
            dec_, sem = [], []
            for ln, zs in recs:
                if zs != (kind == "zero_shot"): continue
                bk = json.load(open(f"{OUT}/analysis/necessity_v2/{ln}_{b}.json"))["by_class"].get(c) or {}
                if not bk.get("n"): continue
                L0 = (lo(bk, "custo_alvo_preto_ci_by_image") or 0) > 0; L1 = (lo(bk, "delta_preto_ci_by_image") or 0) > 0; L2 = L1 and (lo(bk, "delta_blur10_ci_by_image") or 0) > 0; g = (lo(bk, "headroom_ci_by_image") or 0) > 0
                if L2 and g and L0:
                    dec_.append(ln); L0b = (lo(bk, "custo_alvo_blur10_ci_by_image") or 0) > 0
                    if not L0b: sem.append({"linha": ln, "queda_bruta_blur10": bk.get("custo_alvo_blur10"), "ic": bk.get("custo_alvo_blur10_ci_by_image")})
            OUTJ["item3"][f"{b}|{c}|{kind}"] = {"declarados": len(dec_), "tambem_queda_bruta_blur10": len(dec_) - len(sem), "sem_queda_bruta_blur10": sem}
json.dump(OUTJ, open(f"{OUT}/analysis/rodada13.json", "w"), indent=1)
for k, v in OUTJ["item3"].items(): print(k, v["declarados"], v["tambem_queda_bruta_blur10"], v["sem_queda_bruta_blur10"])
