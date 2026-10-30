"""Counts of runs whose necessity effect under both fills (level L3) and whose raw drop (level L0) pass the Holm-corrected test, per benchmark,
question class and group (fine-tuned runs / zero-shot models), read from analysis/holm_familias.json (per-run Holm verdicts). Writes
analysis/holm_rawdrop.json, cited by the numbers sheet."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
H = json.load(open(f"{OUT}/analysis/holm_familias.json")); out = {}
for fam, classes in H["por_linha"].items():
    out[fam] = {}
    for cls, runs in classes.items():
        for grp, sel in (("afinados", lambda n: "ZEROSHOT" not in n), ("zero_shot", lambda n: "ZEROSHOT" in n)):
            rs = {n: v for n, v in runs.items() if sel(n)}
            if not rs: continue
            out[fam][f"{cls}|{grp}"] = {"linhas": len(rs), "L3_e_L0_holm": sum(1 for v in rs.values() if v["veredito_holm"].get("L3") and v["veredito_holm"].get("L0")), "L3_holm": sum(1 for v in rs.values() if v["veredito_holm"].get("L3"))}
json.dump({"t": time.strftime("%Y-%m-%d %H:%M:%S"), "fonte": "analysis/holm_familias.json (por_linha, veredito_holm)", "regra": "L3 e L0 com Holm: veredito_holm L3 e veredito_holm L0 da mesma linha", "contagens": out}, open(f"{OUT}/analysis/holm_rawdrop.json", "w"), indent=1)
print("holm_rawdrop ok", {k: len(v) for k, v in out.items()})
