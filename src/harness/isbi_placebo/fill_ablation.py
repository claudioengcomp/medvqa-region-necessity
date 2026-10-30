"""Fill ablation (plan v2 §2, F-mean/F-blur; pre-registration §3.7).

On the SAME stratified subset of 300 questions, compares Δ_nec =
Acc(P) − Acc(T) with three fills: black (T, P from the main batteries,
restricted to the subset), image mean (T_mean, P_mean) and Gaussian blur
(T_blur, P_blur). Per class, overall and on the artefact box template, with
paired bootstrap and McNemar. Pre-registered reading: "dominant artifact" if the
negative control drops as much as the dependents; with F-mean/F-blur, if the
Δ_nec of the dependents survives and the negative control stays at zero, the control occlusion controls
the fill artifact.
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

from harness.stats.compute_ldv import bootstrap_paired_diff_ci, mcnemar_test

Q_GREENBOX = "Is there a green/black box artefact?"
FILLS = {"black": ("T", "P"), "mean": ("T_mean", "P_mean"), "blur": ("T_blur", "P_blur"),
         # sigma ablation (execution, 14/09/2026): blur = 1, 3, 10 % of the width; regmean = region mean color
         "blur1pct": ("T_blur1", "P_blur1"), "blur3pct": ("T_blur3", "P_blur3"), "blur10pct": ("T_blur10", "P_blur10"),
         "regmean": ("T_regmean", "P_regmean"),
         # E3 (14/09): mean colour of the surroundings (15 px ring), sixth level: "the context suffices" vs "the blob suffices"
         "ringmean": ("T_ringmean", "P_ringmean")}


def _stats(qids, c0, t, p, n_boot, seed):
    n = len(qids)
    if n == 0:
        return {"n": 0}
    ct = [bool(t[q]["correct"]) for q in qids]; cp = [bool(p[q]["correct"]) for q in qids]
    out = {"n": n, "acc_T": sum(ct) / n, "acc_P": sum(cp) / n, "delta_nec": (sum(cp) - sum(ct)) / n,
           "delta_nec_ci": list(bootstrap_paired_diff_ci(cp, ct, n_boot=n_boot, seed=seed)), "mcnemar": mcnemar_test(cp, ct)}
    if c0 is not None:
        c = [bool(c0[q]["correct"]) for q in qids]
        out["acc_C0"] = sum(c) / n; out["vdd_T"] = out["acc_C0"] - out["acc_T"]; out["vdd_P"] = out["acc_C0"] - out["acc_P"]
    return out


def fill_ablation(inventory: str, subset_json: str, preds: dict[str, str], n_boot: int = 10000, seed: int = 42) -> dict:
    keep = set(json.loads(Path(subset_json).read_text())["qids"])
    inv = {q["qid"]: q for q in json.loads(Path(inventory).read_text())["questions"] if q["evaluable"] and q["qid"] in keep}
    loaded = {c: {r["qid"]: r for r in json.loads(Path(p).read_text())["predictions"]} for c, p in preds.items()}
    out = {"inventory": inventory, "subset": subset_json, "predictions": preds, "n_subset": len(inv), "n_boot": n_boot, "fills": {}}
    c0 = loaded.get("C0")
    for fill, (tc, pc) in FILLS.items():
        if tc not in loaded or pc not in loaded:
            out["fills"][fill] = {"status": "pendente", "missing": [c for c in (tc, pc) if c not in loaded]}
            continue
        t, p = loaded[tc], loaded[pc]
        qids = [q for q in inv if q in t and q in p and (c0 is None or q in c0)]
        by_class = collections.defaultdict(list)
        for q in qids:
            by_class[inv[q]["question_class"]].append(q)
        out["fills"][fill] = {"status": "ok", "conditions": [tc, pc], "n_aligned": len(qids),
                              "pooled": _stats(qids, c0, t, p, n_boot, seed),
                              "by_class": {k: _stats(v, c0, t, p, n_boot, seed) for k, v in sorted(by_class.items())},
                              "greenbox": _stats([q for q in qids if inv[q]["question"] == Q_GREENBOX], c0, t, p, n_boot, seed)}
    return out


def render(out: dict) -> str:
    L = [f"# Ablação de preenchimento — {Path(out['predictions'].get('T', 'x')).stem.replace('_T', '')}", "",
         f"Subconjunto estratificado: {out['n_subset']} perguntas (`{out['subset']}`). Δ_nec = Acc(P) − Acc(T) por preenchimento, "
         f"IC bootstrap pareado ({out['n_boot']}), McNemar P vs T.", "",
         "| preenchimento | grupo | n | Acc(C0) | Acc(T) | Acc(P) | Δ_nec (pp) | IC 95 % | McNemar p |", "|---|---|---:|---:|---:|---:|---:|---|---:|"]
    def row(fill, name, s):
        if s.get("n", 0) == 0:
            return f"| {fill} | {name} | 0 | — | — | — | — | — | — |"
        ci = s["delta_nec_ci"]
        return (f"| {fill} | {name} | {s['n']} | {100 * s.get('acc_C0', float('nan')):.1f} | {100 * s['acc_T']:.1f} | {100 * s['acc_P']:.1f} | "
                f"{100 * s['delta_nec']:+.1f} | [{100 * ci[0]:+.1f}, {100 * ci[1]:+.1f}] | {s['mcnemar']['p_value']:.3g} |")
    for fill, d in out["fills"].items():
        if d.get("status") != "ok":
            L.append(f"| {fill} | pendente (falta {', '.join(d['missing'])}) | | | | | | | |"); continue
        L.append(row(fill, "todas", d["pooled"]))
        L += [row(fill, k, s) for k, s in d["by_class"].items()]
        L.append(row(fill, "caixa de artefato (template)", d["greenbox"]))
    L += ["", "Leitura pré-registrada: artefato dominante se o controle negativo cai tanto quanto os dependentes; o placebo controla o "
          "artefato do preenchimento se o Δ_nec dos dependentes se mantém com média e blur enquanto o negativo fica em zero."]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inventory", required=True); ap.add_argument("--subset", required=True); ap.add_argument("--pred", action="append", required=True)
    ap.add_argument("--n-boot", type=int, default=10000); ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--output-json", required=True); ap.add_argument("--output-md")
    a = ap.parse_args(argv)
    out = fill_ablation(a.inventory, a.subset, dict(kv.split("=", 1) for kv in a.pred), a.n_boot, a.seed)
    Path(a.output_json).write_text(json.dumps(out, indent=1) + "\n")
    md = render(out)
    if a.output_md:
        Path(a.output_md).write_text(md)
    print(md)


if __name__ == "__main__":
    main()
