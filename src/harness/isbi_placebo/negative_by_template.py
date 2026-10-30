"""Item 2 (14/09, authors): open negative control by template, for the 15 Kvasir runs and the fills black,
blur 4 %, blur 10 %, region mean color and 15 px ring (where it exists): Δ_nec with CI and sign for
"Is there text?", "green/black box" and "procedure", separately. Question to answer: does "Is there text?"
stay within zero in the 30 black and blur cells? If so, it is the paper's pure negative; box and procedure
become controls with an explained failure (fill artifact and confounder, respectively).

Reads necessity_<ckpt>.json (by_template, whole set) and, for the ring, the _fill300 predictions
(300 stratified). Nothing here triggers inference.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from harness.stats.compute_ldv import bootstrap_paired_diff_ci, mcnemar_test

TEMPLATES = {"text": "Is there text?", "box": "Is there a green/black box artefact?",
             "procedure": "What type of procedure is the image taken from?"}
FILLS = [("black", "preto"), ("blur", "blur 4 %"), ("blur10", "blur 10 %"), ("regmean", "cor média região"), ("ringmean", "anel 15 px")]
_RE = re.compile(r"^necessity_(?P<key>[A-Z0-9]+(?:_[A-Z0-9]+)?_KVASIR_seed\d)\.json$")


def _cell(s: dict, fill: str) -> dict | None:
    k = "delta_nec" if fill == "black" else f"delta_nec_{fill}"
    if k not in s:
        return None
    lo, hi = s[f"{k}_ci"]
    return {"n": s["n"], "delta": s[k], "ci": [lo, hi], "excludes_zero": lo > 0 or hi < 0,
            "within_zero": lo <= 0 <= hi, "p": (s.get("mcnemar") if fill == "black" else s.get(f"mcnemar_{fill}", {})).get("p_value")}


def _ring_from_fill300(results_dir: str, key: str, inv_by_qid: dict, n_boot: int, seed: int) -> dict:
    t = Path(results_dir, f"{key}_T_ringmean_fill300.json"); p = Path(results_dir, f"{key}_P_ringmean_fill300.json")
    if not (t.is_file() and p.is_file()):
        return {}
    pt = {r["qid"]: r for r in json.loads(t.read_text())["predictions"]}
    pp = {r["qid"]: r for r in json.loads(p.read_text())["predictions"]}
    out = {}
    for tag, q in TEMPLATES.items():
        qids = [i for i in pt if i in pp and inv_by_qid.get(i) == q]
        if not qids:
            continue
        ct = [bool(pt[i]["correct"]) for i in qids]; cp = [bool(pp[i]["correct"]) for i in qids]
        d = (sum(cp) - sum(ct)) / len(qids); lo, hi = bootstrap_paired_diff_ci(cp, ct, n_boot=n_boot, seed=seed)
        out[tag] = {"n": len(qids), "delta": d, "ci": [lo, hi], "excludes_zero": lo > 0 or hi < 0, "within_zero": lo <= 0 <= hi,
                    "p": mcnemar_test(cp, ct)["p_value"], "subset": "fill300"}
    return out


def collect(results_dir: str, inventory: str | None = None, n_boot: int = 10000, seed: int = 42) -> dict:
    inv_by_qid = {}
    if inventory and Path(inventory).is_file():
        inv_by_qid = {q["qid"]: q["question"] for q in json.loads(Path(inventory).read_text())["questions"] if q["evaluable"]}
    rows = {}
    for path in sorted(Path(results_dir).glob("necessity_*_KVASIR_seed*.json")):
        m = _RE.match(path.name)
        if not m:
            continue
        nec = json.loads(path.read_text()); key = m["key"]
        rows[key] = {tag: {} for tag in TEMPLATES}
        for tag, q in TEMPLATES.items():
            s = nec["by_template"].get(q, {})
            for fill, _ in FILLS[:-1]:
                c = _cell(s, fill)
                if c:
                    rows[key][tag][fill] = c
        for tag, c in _ring_from_fill300(results_dir, key, inv_by_qid, n_boot, seed).items():
            rows[key][tag]["ringmean"] = c
    # central question: "Is there text?" within zero in every black and blur cell
    text_cells = [(k, f, r["text"][f]) for k, r in rows.items() for f in ("black", "blur") if f in r["text"]]
    verdict = {"n_cells": len(text_cells), "n_within_zero": sum(c["within_zero"] for _, _, c in text_cells),
               "failures": [{"checkpoint": k, "fill": f, "delta": c["delta"], "ci": c["ci"]} for k, f, c in text_cells if not c["within_zero"]],
               "max_abs_delta": max((abs(c["delta"]) for _, _, c in text_cells), default=None)}
    verdict["pure_negative"] = verdict["n_cells"] > 0 and verdict["n_within_zero"] == verdict["n_cells"]
    return {"templates": TEMPLATES, "fills": [f for f, _ in FILLS], "rows": rows, "text_verdict": verdict}


def _fmt(c: dict | None) -> str:
    if not c:
        return "—"
    lo, hi = c["ci"]; mark = "**" if c["excludes_zero"] else ""
    return f"{mark}{100 * c['delta']:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}]{mark}"


def render(out: dict) -> str:
    v = out["text_verdict"]
    L = ["# Controle negativo por template (Kvasir, 15 linhas × preenchimentos)", "",
         "Δ_nec = Acc(P) − Acc(T) em pp, IC 95 % bootstrap pareado, sinal preservado; **negrito** = IC exclui zero. "
         "Preto, blur 4 %, blur 10 % e cor média da região no conjunto inteiro (243 texto, 243 caixa, 242 procedimento); "
         "anel de 15 px nas 300 estratificadas (n menor).", "",
         f"**\"Is there text?\" nas células de preto e blur:** {v['n_within_zero']}/{v['n_cells']} com IC contendo zero"
         + (f"; |Δ_nec| máximo {100 * v['max_abs_delta']:.1f} pp" if v["max_abs_delta"] is not None else "") + ". "
         + ("**Negativo puro: sim.**" if v["pure_negative"] else "**Negativo puro: não** (falhas: " + "; ".join(f"{f['checkpoint']} {f['fill']} {100 * f['delta']:+.1f} [{100 * f['ci'][0]:+.1f}, {100 * f['ci'][1]:+.1f}]" for f in v["failures"]) + ")."), ""]
    for tag, q in out["templates"].items():
        L += [f"## {q}", "", "| checkpoint | " + " | ".join(lab for _, lab in FILLS) + " |", "|---|" + "---|" * len(FILLS)]
        for key, r in out["rows"].items():
            L.append(f"| {key} | " + " | ".join(_fmt(r[tag].get(f)) for f, _ in FILLS) + " |")
        L.append("")
    L += ["Leitura pré-registrada (E2/E3): texto = negativo puro se ficar dentro de zero sob preto e blur; caixa = controle com falha "
          "explicada por artefato do preenchimento sólido (sinal negativo sob preto, some sob blur); procedimento = confundidor "
          "(dependência pequena e genuína: colonoscopias viram gastroscopia com o pólipo coberto)."]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results-dir", default="results/isbi_placebo"); ap.add_argument("--docs-dir", default="docs/isbi/placebo")
    ap.add_argument("--inventory", default=None); ap.add_argument("--n-boot", type=int, default=10000); ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args(argv)
    out = collect(a.results_dir, a.inventory or str(Path(a.results_dir, "inventory_kvasir_test_clean.json")), a.n_boot, a.seed)
    Path(a.results_dir, "negative_by_template.json").write_text(json.dumps(out, indent=1) + "\n")
    md = render(out); Path(a.docs_dir, "negative_by_template.md").write_text(md); print(md)


if __name__ == "__main__":
    main()
