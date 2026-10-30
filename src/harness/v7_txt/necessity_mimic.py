"""v7_mimic block C (2026-10-13, authors): per-run necessity on MIMIC (control occlusion v2) with the HEAL routine,
harness.isbi_placebo.compute_necessity (same worktree and parameters as the published HEAL necessity results: paired bootstrap
10 000, seed 42; E3 = black AND (blur 10 % OR region mean color) with CI excluding zero). 24 VLM runs (15 published minus
M3AE + 12 fine-tuned-encoder (tower) runs); M3AE pending (appendix once available). Two variants: full (inventory v2) and exact-only
(evaluable && entity_map_quality == 'exata'). Conditions: C0, C1, T, P, S, T/P/S_blur10, T/P/S_regmean and doses T1.5, P1.5, T2, P2
(doses outside the main alignment; only on the paired subset of units valid at 1.5x and 2x, as in Kvasir).
The v2 manifest (units_by_group.dose) is converted to the format the routine reads (units[].placebo_method_by_factor), without changing
any rule. Outputs: analysis/necessity_<RUN>[_so_exatas].json, docs/necessity_<RUN>[_so_exatas].md, provenance stamp in each JSON.
The per-image CI (2 000, seed 20260913), mid-p and Holm live in the aggregator placebo_mimic.py."""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import hashlib, json, os, socket, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
R = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic"; W = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/worktree"; PY = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/miniconda3/envs/circle/bin/python"
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""): h.update(b)
    return h.hexdigest()
LINES = [f"{fam}_MIMIC_seed{s}" for fam in ("QWEN2VL_LORA_FROZEN", "QWEN2VL_DORA", "SMOLVLM_LORA", "SMOLVLM_DORA", "QWEN2VL_LORA_VT", "QWEN2VL_DORA_VT", "SMOLVLM_LORA_FT", "SMOLVLM_DORA_FT", "M3AE") for s in range(3)]   # 13/10: M3AE (appendix) comes in once the batteries complete
GROUP = {l: ("torre" if any(t in l for t in ("_VT_", "_FT_")) else "publicada") for l in LINES}
CONDS = ["C0", "C1", "T", "P", "S", "T_blur10", "P_blur10", "S_blur10", "T_regmean", "P_regmean", "S_regmean", "T1.5", "P1.5", "T2", "P2"]
INV = f"{R}/results/inventory_mimic_test.json"; INV_EX = f"{R}/analysis/inventory_mimic_test_so_exatas.json"; MAN = f"{R}/data/conditions/manifest_mimic_placebo.json"; MAN_C = f"{R}/analysis/manifest_mimic_placebo_dose_compat.json"
def prep():
    if os.path.exists(INV_EX) and os.path.exists(MAN_C):   # 13/10: do not rewrite (their sha is in the necessity results already computed)
        cnt = {v: sum(1 for q in json.load(open(p))["questions"] if q["evaluable"]) for v, p in (("completo", INV), ("so_exatas", INV_EX))}
        units = json.load(open(MAN_C))["units"]; return cnt, sum(len(u["qids"]) for u in units if all(u["placebo_method_by_factor"].get(k) is not None for k in ("1.5", "2")))
    d = json.load(open(INV)); Q = d["questions"]
    ex = dict(d); ex["questions"] = [dict(q, evaluable=bool(q["evaluable"] and q.get("entity_map_quality") == "exata")) for q in Q]
    ex["provenance"] = dict(d.get("provenance") or {}, variante="so exatas: evaluable && entity_map_quality == 'exata' (bloco C v2, 13/10)", fonte=INV, fonte_sha256=sha(INV), gerado_por=__file__, t=time.strftime("%Y-%m-%d %H:%M:%S"))
    json.dump(ex, open(INV_EX, "w"))
    m = json.load(open(MAN)); units = []
    for u in m["units_by_group"]["dose"]["units"]:
        dz = u.get("dose") or {}
        f = {k: ((dz.get("P" + k) or {}).get("method") if ((dz.get("T" + k) or {}).get("method") is not None and (dz.get("P" + k) or {}).get("method") is not None) else None) for k in ("1.5", "2")}
        units.append({"image_id": u["image_id"], "qids": u["qids"], "placebo_method_by_factor": f, "dose": dz})
    json.dump({"units": units, "provenance": {"fonte": MAN, "fonte_sha256": sha(MAN), "regra": "placebo_method_by_factor[k] = metodo do P<k> do manifesto v2 (None quando o par T<k>/P<k> nao tem colocacao valida); conversao de formato, sem regra nova", "gerado_por": __file__, "t": time.strftime("%Y-%m-%d %H:%M:%S")}}, open(MAN_C, "w"))
    cnt = {v: sum(1 for q in json.load(open(p))["questions"] if q["evaluable"]) for v, p in (("completo", INV), ("so_exatas", INV_EX))}
    paired = sum(len(u["qids"]) for u in units if all(u["placebo_method_by_factor"].get(k) is not None for k in ("1.5", "2")))
    return cnt, paired
def run(line, var):
    inv = INV if var == "completo" else INV_EX; suf = "" if var == "completo" else "_so_exatas"
    oj = f"{R}/analysis/necessity_{line}{suf}.json"; om = f"{R}/docs/necessity_{line}{suf}.md"; lg = f"{R}/logs/necessity/necessity_{line}{suf}.log"
    files = {c: f"{R}/results/{line}_{c}.json" for c in CONDS}; miss = [c for c, p in files.items() if not os.path.exists(p)]
    if miss: return line, var, "faltam " + ",".join(miss)
    cmd = [PY, "-m", "harness.isbi_placebo.compute_necessity", "--inventory", inv, "--manifest", MAN_C, "--n-boot", "10000", "--seed", "42", "--output-json", oj, "--output-md", om] + sum((["--pred", f"{c}={p}"] for c, p in files.items()), [])
    t0 = time.time(); rc = subprocess.call(cmd, cwd=W, stdout=open(lg, "w"), stderr=subprocess.STDOUT, env=dict(os.environ, CUDA_VISIBLE_DEVICES="", PYTHONDONTWRITEBYTECODE="1", OMP_NUM_THREADS="2", MKL_NUM_THREADS="2"))
    if rc != 0: return line, var, f"rc={rc} (log {lg})"
    d = json.load(open(oj))
    d["provenance"] = {"line": line, "group": GROUP[line], "variant": var, "routine": "harness.isbi_placebo.compute_necessity (worktree v7_txt, mesma rotina e parametros das necessidades publicadas do HEAL: n_boot 10000, seed 42)",
                       "inventory": inv, "inventory_sha256": sha(inv), "manifest_dose": MAN_C, "manifest_dose_sha256": sha(MAN_C), "manifest_v2": MAN, "manifest_v2_sha256": sha(MAN),
                       "predictions_sha256": {c: sha(p) for c, p in files.items()}, "placebo_rule": "v2", "host": socket.gethostname(), "seconds": round(time.time() - t0, 1), "t": time.strftime("%Y-%m-%d %H:%M:%S"), "driver": __file__, "driver_sha256": sha(__file__)}
    json.dump(d, open(oj, "w"), indent=1); return line, var, "ok %.0fs n_aligned=%s" % (time.time() - t0, d.get("n_aligned"))
if __name__ == "__main__":
    os.makedirs(f"{R}/logs/necessity", exist_ok=True)
    cnt, paired = prep(); print("avaliaveis:", cnt, "| qids pareados nas doses (1,5x e 2x):", paired, flush=True)
    sel = sys.argv[2].split(",") if len(sys.argv) > 2 else None   # 13/10: optional filter by run prefix (e.g. M3AE)
    jobs = [(l, v) for l in LINES for v in ("completo", "so_exatas") if sel is None or any(l.startswith(x) for x in sel)]
    with ThreadPoolExecutor(int(sys.argv[1]) if len(sys.argv) > 1 else 6) as ex:
        for r in ex.map(lambda a: run(*a), jobs): print(*r, flush=True)
    print("FIM")
