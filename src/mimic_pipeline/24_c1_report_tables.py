"""14/10/2026: (a) real diff by key between before/after in the JSON files (C1 keys and provenance stamp only); (b) report tables:
mean per family (5 benchmarks) with C1; TXT - C1 per run and family (HEAL, MIMIC) with CI; C1 coverage (n)."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json, re, collections
from pathlib import Path
A = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/tmp/v7/snapshot_before_20261014"); V = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt")
EXP = {"c1", "txt_menos_c1", "C1_frozen", "t", "definitions"}
def changes(a, b, path, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b: out["struct"].append(path + "/" + k); continue
            if k in EXP and json.dumps(a[k], sort_keys=True) != json.dumps(b[k], sort_keys=True):
                m = re.search(r"benchmarks/([A-Z]+)", path + "/" + k); out["changed"][(m.group(1) if m else "-", k)] += 1; continue
            if k in EXP: continue
            changes(a[k], b[k], path + "/" + k, out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): out["other"].append(path); return
        for i, (x, y) in enumerate(zip(a, b)): changes(x, y, f"{path}[{i}]", out)
    elif a != b: out["other"].append(path)
print("## Diff real por chave (antes -> depois)")
for name in ("txt_floors", "decomposicao", "own_floor_ceilings"):
    out = {"changed": collections.Counter(), "struct": [], "other": []}; changes(json.load(open(A / f"analysis/{name}.json")), json.load(open(V / f"analysis/{name}.json")), "", out)
    print(f"{name}.json: mudancas em chaves esperadas: " + ", ".join(f"{b}:{k}={n}" for (b, k), n in sorted(out["changed"].items())) + f" | estrutura {len(out['struct'])} | outras {len(out['other'])}")
D = json.load(open(V / "analysis/decomposicao.json"))
print("\n## Media (DP) por familia, 5 bases (decomposicao.json by_family)")
print("| base | familia | desenho | piso TXT | C0 congelada | ganho torre | C0 adaptada | ganho adapt. | soma | M0 | TXT-M0 | C1 | TXT-C1 |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
def ms(d):
    if not d: return "—"
    return f"{d['mean']:.3f} ({d['sd']:.3f})" if isinstance(d, dict) and d.get("sd") is not None else (f"{d['mean']:.3f}" if isinstance(d, dict) else f"{d:.3f}")
for bench, B in D["benchmarks"].items():
    for fam, fb in B["by_family"].items():
        print(f"| {bench} | {fam} | {fb['design'][:22]} | " + " | ".join(ms(fb.get(k)) for k in ("piso_proprio", "c0_congelada", "ganho_torre", "c0_adaptada", "ganho_adaptacao", "soma", "m0", "txt_menos_m0", "c1", "txt_menos_c1")) + " |")
print("\n## HEAL e MIMIC: C1 e TXT - C1 por linha (IC 95 % bootstrap por imagem) e media por familia")
print("| base | linha | n linha | n C1 | Acc TXT (nos qids C1) | Acc C1 | TXT - C1 [IC] | mid-p |")
print("|---|---|---|---|---|---|---|---|")
fam_acc = collections.defaultdict(list)
for bench in ("HEAL", "MIMIC"):
    for r in D["benchmarks"][bench]["lines"]:
        if r.get("status") != "ok": print(f"| {bench} | {r['line']} | {r.get('status')} |"); continue
        o = r["overall"]
        if "c1" not in o: print(f"| {bench} | {r['line']} | {r['n']} | — | | | | |"); continue
        d = o["txt_menos_c1"]; fam_acc[(bench, r["family"])].append(d["diff"])
        txt_on_c1 = o["c1"]["acc"] + d["diff"]
        print(f"| {bench} | {r['line']} | {r['n']} | {o['c1']['n']} | {txt_on_c1:.3f} | {o['c1']['acc']:.3f} [{o['c1']['ci'][0]:.3f}, {o['c1']['ci'][1]:.3f}] | {d['diff']:+.3f} [{d['ci'][0]:+.3f}, {d['ci'][1]:+.3f}] | {d['midp']:.2g} |")
print("\n| base | familia | media TXT - C1 (3 sementes) | DP |"); print("|---|---|---|---|")
import statistics as st
for (b, f), v in sorted(fam_acc.items()): print(f"| {b} | {f} | {st.mean(v):+.3f} | {st.stdev(v):.3f} |" if len(v) > 1 else f"| {b} | {f} | {v[0]:+.3f} | — |")
print("\n## Cobertura de C1 por classe (HEAL/MIMIC, decomposicao by_class: n C1 / n classe)")
for bench in ("HEAL", "MIMIC"):
    r = next(x for x in D["benchmarks"][bench]["lines"] if x.get("status") == "ok" and x["family"] == "QWEN2VL")
    print(bench, {k: f"{v['c1']['n']}/{v['piso_proprio']['n']}" if "c1" in v else f"0/{v['piso_proprio']['n']}" for k, v in r["by_class"].items() if not k.startswith("template")})
