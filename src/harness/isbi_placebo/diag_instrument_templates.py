"""EXPLORATORY (item 6, 15/09/2026, authors; recorded without interpretation). On the runs with E3, per
instrument template (How many, Where, Any): Acc(T) under black and under blur 10 %, paired
difference with bootstrap CI and McNemar. Alongside, the distribution of the answers given under T for each
fill (black, blur 4 %, blur 10 %, mean color) for "Any instruments" and "How many":
how many "no"/"0" versus others, with the gold as reference.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from harness.stats.compute_ldv import bootstrap_paired_diff_ci, mcnemar_test

TEMPLATES = {"any": "Are there any instruments in the image? Check all that are present.",
             "howmany": "How many instrumnets are in the image?", "where": "Where in the image is the instrument?"}
DIST_TEMPLATES = ("any", "howmany")
FILLS_T = [("black", "T"), ("blur", "T_blur"), ("blur10", "T_blur10"), ("regmean", "T_regmean")]
NEG = {"no", "none", "0", "zero", "nothing", "no instruments", "no instrument"}
_RE = re.compile(r"^(?P<key>[A-Z0-9]+(?:_[A-Z0-9]+)?_KVASIR_seed\d)_T\.json$")


def is_negative(ans: str) -> bool:
    a = re.sub(r"[^a-z0-9 ]", "", str(ans).strip().lower()).strip()
    return a in NEG or a.startswith("no ") or a == "no" or a.startswith("0 ") or a == "0"


def _rows(p: Path) -> dict:
    return {r["qid"]: r for r in json.loads(p.read_text())["predictions"]}


def collect(results_dir: str, inventory: str, n_boot: int = 10000, seed: int = 42) -> dict:
    inv = json.loads(Path(inventory).read_text())["questions"]
    qids = {tag: [q["qid"] for q in inv if q["evaluable"] and q["question"] == tmpl] for tag, tmpl in TEMPLATES.items()}
    out = {"templates": TEMPLATES, "rows": {}}
    for p in sorted(Path(results_dir).glob("*_KVASIR_seed?_T.json")):
        m = _RE.match(p.name)
        if not m:
            continue
        key = m["key"]; b10 = Path(results_dir, f"{key}_T_blur10.json")
        if not b10.is_file():
            continue   # only runs with E3
        t_black, t_b10 = _rows(p), _rows(b10)
        row = {"acc": {}, "answers": {}}
        for tag, ids in qids.items():
            ids2 = [i for i in ids if i in t_black and i in t_b10]
            if not ids2:
                continue
            ca = [bool(t_black[i]["correct"]) for i in ids2]; cb = [bool(t_b10[i]["correct"]) for i in ids2]
            lo, hi = bootstrap_paired_diff_ci(cb, ca, n_boot=n_boot, seed=seed)
            row["acc"][tag] = {"n": len(ids2), "acc_T_black": sum(ca) / len(ids2), "acc_T_blur10": sum(cb) / len(ids2),
                               "diff_blur10_minus_black": (sum(cb) - sum(ca)) / len(ids2), "diff_ci": [lo, hi], "mcnemar": mcnemar_test(cb, ca)}
        for tag in DIST_TEMPLATES:
            ids = qids[tag]
            dist = {}
            gold = [t_black[i]["gold"] for i in ids if i in t_black]
            dist["gold"] = {"n": len(gold), "negative": sum(is_negative(g) for g in gold)}
            for fill, cond in FILLS_T:
                f = p if fill == "black" else Path(results_dir, f"{key}_{cond}.json")
                if not f.is_file():
                    continue
                rows = _rows(f); preds = [rows[i]["predicted"] for i in ids if i in rows]
                dist[fill] = {"n": len(preds), "negative": sum(is_negative(x) for x in preds)}
            row["answers"][tag] = dist
        out["rows"][key] = row
    return out


def render(out: dict) -> str:
    L = ["# EXPLORATÓRIO — templates de instrumento: Acc(T) preto × blur 10 % e respostas dadas sob T", "",
         "Registro sem interpretação. Linhas com E3 (T_blur10 em disco). Diferença = Acc(T blur 10 %) − Acc(T preto), "
         "IC 95 % bootstrap pareado, McNemar. \"no/0\" = resposta negativa (no, none, 0, zero…).", "",
         "## Acc(T) por template", "", "| linha | template | n | Acc(T) preto | Acc(T) blur 10 % | diferença (pp) | IC 95 % | McNemar p |",
         "|---|---|---:|---:|---:|---:|---|---:|"]
    names = {"any": "Any instruments", "howmany": "How many", "where": "Where"}
    for key, r in out["rows"].items():
        for tag, s in r["acc"].items():
            lo, hi = s["diff_ci"]
            L.append(f"| {key} | {names[tag]} | {s['n']} | {100 * s['acc_T_black']:.1f} | {100 * s['acc_T_blur10']:.1f} | "
                     f"{100 * s['diff_blur10_minus_black']:+.1f} | [{100 * lo:+.1f}, {100 * hi:+.1f}] | {s['mcnemar']['p_value']:.3g} |")
    L += ["", "## Respostas dadas sob T: \"no/0\" / total, por preenchimento", "",
          "| linha | template | ouro | preto | blur 4 % | blur 10 % | cor média região |", "|---|---|---:|---:|---:|---:|---:|"]
    for key, r in out["rows"].items():
        for tag, d in r["answers"].items():
            cell = lambda f: f"{d[f]['negative']} / {d[f]['n']}" if f in d else "—"
            L.append(f"| {key} | {names[tag]} | {cell('gold')} | {cell('black')} | {cell('blur')} | {cell('blur10')} | {cell('regmean')} |")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results-dir", default="results/isbi_placebo"); ap.add_argument("--docs-dir", default="docs/isbi/placebo")
    ap.add_argument("--inventory", default="results/isbi_placebo/inventory_kvasir_test_clean.json")
    ap.add_argument("--n-boot", type=int, default=10000); ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args(argv)
    out = collect(a.results_dir, a.inventory, a.n_boot, a.seed)
    Path(a.results_dir, "diag_instrument_templates.json").write_text(json.dumps(out, indent=1) + "\n")
    md = render(out); Path(a.docs_dir, "diag_instrument_templates.md").write_text(md); print(md)


if __name__ == "__main__":
    main()
