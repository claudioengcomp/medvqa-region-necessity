"""Round 12 (21/10/2026, CPU): (1) maximum Delta black among the declared runs (both fills, significant gain and raw drop) and among the 27, per class;
(2) Medical-Diff-VQA, yes-questions, per entity: runs with a significant gain / declared (L3 and L0) / 27. Source: analysis/necessity_v2/*.json
(per-image 95 % CI). Output: analysis/rodada12.json."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
def lo(bk, k): c = (bk or {}).get(k); return c[0] if c else None
def st(bk):
    L0 = (lo(bk, "custo_alvo_preto_ci_by_image") or 0) > 0; L1 = (lo(bk, "delta_preto_ci_by_image") or 0) > 0; L2 = L1 and (lo(bk, "delta_blur10_ci_by_image") or 0) > 0
    g = (lo(bk, "headroom_ci_by_image") or 0) > 0; return {"L0": L0, "ganho": g, "L3": L2 and g, "declarado": L2 and g and L0}
R = {b: {L["line"]: json.load(open(f"{OUT}/analysis/necessity_v2/{L['line']}_{b}.json")) for L in lines(b)} for b in BASES}
out = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "item1": {}, "item2": {}}
DR = json.load(open(f"{OUT}/analysis/declarados_r11.json"))["classes"]
for b, c in (("KVASIR", "dependent_polyp"), ("KVASIR", "dependent_instrument"), ("MIMIC", "closed_yes"), ("HEAL", "closed_yes")):
    rows = {ln: r["by_class"][c] for ln, r in R[b].items()}; dec = [ln for ln, bk in rows.items() if st(bk)["declarado"]]
    assert sorted(dec) == sorted(DR[f"{b}|{c}"]["linhas_declaradas"]), (b, c)
    mx = lambda ls: max(((rows[l]["delta_preto"], l) for l in ls), default=(None, None))
    md, ma = mx(dec), mx(rows)
    out["item1"][f"{b}|{c}"] = {"declarados": len(dec), "max_delta_preto_declarados": md[0], "linha_max_declarados": md[1], "max_delta_preto_27": ma[0], "linha_max_27": ma[1],
                                "min_delta_preto_declarados": min((rows[l]["delta_preto"] for l in dec), default=None)}
ents = [k for k in next(iter(R["MIMIC"].values()))["by_class"] if k.startswith("entidade=")]
for e in ents:
    xs = [st(r["by_class"][e]) for r in R["MIMIC"].values()]; n = next(iter(R["MIMIC"].values()))["by_class"][e]["n"]
    out["item2"][e.split("=", 1)[1]] = {"perguntas": n, "ganho_significativo": sum(x["ganho"] for x in xs), "declarados_L3_e_L0": sum(x["declarado"] for x in xs), "L3_sem_exigir_L0": sum(x["L3"] for x in xs), "runs": len(xs)}
json.dump(out, open(f"{OUT}/analysis/rodada12.json", "w"), indent=1)
for k, v in out["item1"].items(): print(k, v)
for k, v in out["item2"].items(): print(k, v)
