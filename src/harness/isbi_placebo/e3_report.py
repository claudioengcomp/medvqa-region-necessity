"""Report of amendment E3 (pre-registration §7): Δ_nec per class and per template under black,
blur 4 % (E2), blur 10 % of the width and mean color of the region itself, on the WHOLE SET of
evaluable questions, with the column "necessary under the E3 criterion" per run; polyp
templates that survive blur 10 % and mean color; "How many polyps" and "Size" with CI; and the
result of the surroundings mean color (15 px ring) in the 300-item ablation (M3AE and Qwen).

Reads only `necessity_<ckpt>.json` (fields `delta_nec_<fill>` and `e3`, compute_necessity) and
`fill_ablation_<ckpt>.json` (`ringmean` level). Nothing here triggers inference.

    python -m harness.isbi_placebo.e3_report --results-dir results/isbi_placebo --docs-dir docs/isbi/placebo
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FILLS = [("black", "preto"), ("blur", "blur 4 %"), ("blur10", "blur 10 %"), ("regmean", "cor média região")]
E3_FILLS = ("blur10", "regmean")
CLASS_PT = {"dependent_polyp": "pólipo", "dependent_instrument": "instrumento", "negative_control": "controle negativo",
            "dependent_polyp_secondary": "secundária"}
Q_COUNT, Q_SIZE = "How many polyps are in the image?", "What is the size of the polyp?"
_RE = re.compile(r"^necessity_(?P<key>[A-Z0-9]+(?:_[A-Z0-9]+)?_KVASIR_seed\d)\.json$")


def _cell(s: dict, fill: str) -> str:
    k = "delta_nec" if fill == "black" else f"delta_nec_{fill}"
    if k not in s:
        return "—"
    lo, hi = s[f"{k}_ci"]
    return f"{100 * s[k]:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}]"


def _e3(s: dict) -> str:
    e = s.get("e3")
    if not e or e.get("necessary") is None:
        return "—"
    if e["necessary"]:
        return "sim"
    return "não (só preto)" if e.get("solid_only") else "não"


def _has_e3(nec: dict) -> bool:
    return any(f"delta_nec_{f}" in s for s in nec["by_class"].values() for f in E3_FILLS)


def collect(results_dir: str) -> dict:
    out = {"checkpoints": {}, "ring": {}}
    for p in sorted(Path(results_dir).glob("necessity_*_KVASIR_seed*.json")):
        m = _RE.match(p.name)
        if not m:
            continue
        nec = json.loads(p.read_text())
        if not _has_e3(nec):
            continue
        key = m["key"]
        rows = {"by_class": {}, "by_template": {}}
        for g in rows:
            for name, s in nec[g].items():
                if "delta_nec" not in s:
                    continue
                r = {"n": s["n"], "e3": s.get("e3")}
                for f, _ in FILLS:
                    k = "delta_nec" if f == "black" else f"delta_nec_{f}"
                    if k in s:
                        r[f] = {"delta": s[k], "ci": s[f"{k}_ci"]}
                rows[g][name] = r
        cls_of = {}
        out["checkpoints"][key] = {"n_aligned": nec["n_aligned"], **rows}
    for p in sorted(Path(results_dir).glob("fill_ablation_*_KVASIR_seed*.json")):
        fa = json.loads(p.read_text())
        key = p.stem.replace("fill_ablation_", "")
        lv = {f: fa["fills"].get(f) for f in ("black", "regmean", "ringmean")}
        if not lv["ringmean"] or lv["ringmean"].get("status") != "ok":
            continue
        out["ring"][key] = {f: {"pooled": d["pooled"], "by_class": d["by_class"], "greenbox": d["greenbox"]}
                            for f, d in lv.items() if d and d.get("status") == "ok"}
    return out


def _polyp_survivors(ck: dict, inventory_classes: dict[str, str]) -> dict:
    res = {}
    for q, r in ck["by_template"].items():
        if inventory_classes.get(q) != "dependent_polyp" or not r["e3"] or r["e3"]["necessary"] is None:
            continue
        res[q] = {"black": r["e3"]["black_excludes_zero"], **r["e3"]["plausible_excludes_zero"], "necessary": r["e3"]["necessary"]}
    return res


def render(out: dict, inventory: str | None = None) -> str:
    cls_of = {}
    if inventory and Path(inventory).is_file():
        cls_of = {q["question"]: q["question_class"] for q in json.loads(Path(inventory).read_text())["questions"]}
    L = ["# E3 — necessidade sob preto e sob preenchimento plausível (conjunto inteiro, Kvasir)", "",
         "Critério E3 (pré-registro §7): \"sim\" se o IC 95 % de Δ_nec = Acc(P) − Acc(T) exclui zero (para cima) sob preto "
         "E sob ao menos um preenchimento plausível (blur 10 % da largura ou cor média da própria região) nas perguntas "
         "avaliáveis. \"não (só preto)\" = sensibilidade ao preenchimento sólido, não necessidade. Blur 4 % (σ = 25 px, E2) "
         "fica na tabela por referência e não conta para o critério.", ""]
    hdr = "| linha | n | " + " | ".join(f"Δ_nec {lab} [IC]" for _, lab in FILLS) + " | E3 |"
    sep = "|---|---:|" + "---|" * len(FILLS) + "---|"
    if not out["checkpoints"]:
        L += ["*Nenhum checkpoint com blur 10 % ou cor média da região no conjunto inteiro ainda.*", ""]
    for key, ck in out["checkpoints"].items():
        L += [f"## {key} (n alinhado = {ck['n_aligned']})", "", "### Por classe", "", hdr, sep]
        for name, r in ck["by_class"].items():
            L.append(f"| {CLASS_PT.get(name, name)} | {r['n']} | " + " | ".join(_fmt(r.get(f)) for f, _ in FILLS) + f" | {_e3_row(r)} |")
        L += ["", "### Por template", "", hdr, sep]
        for name, r in sorted(ck["by_template"].items(), key=lambda kv: (cls_of.get(kv[0], "z"), kv[0])):
            L.append(f"| {name} | {r['n']} | " + " | ".join(_fmt(r.get(f)) for f, _ in FILLS) + f" | {_e3_row(r)} |")
        surv = _polyp_survivors(ck, cls_of)
        L += ["", "### Templates de pólipo: o que sobrevive", ""]
        if not surv:
            L.append("*Sem classes no inventário ou sem preenchimento plausível carregado.*")
        for q, v in surv.items():
            parts = [f"preto {'✓' if v['black'] else '✗'}"] + [f"{lab} {'✓' if v.get(f) else '✗'}" for f, lab in FILLS[2:] if f in v]
            L.append(f"- {q}: " + ", ".join(parts) + f" → **{'necessário' if v['necessary'] else 'não necessário pelo E3'}**")
        L += ["", "### \"How many polyps\" e \"Size\" com IC", ""]
        for q in (Q_COUNT, Q_SIZE):
            r = ck["by_template"].get(q)
            if r:
                L.append(f"- {q} (n = {r['n']}): " + "; ".join(f"{lab} {_fmt(r.get(f))}" for f, lab in FILLS if f in r) + f"; E3 = {_e3_row(r)}")
        L.append("")
    L += ["## Cor média do entorno (anel de 15 px) — ablação de 300", "",
          "Separa \"o contexto basta\" de \"a mancha basta\": se o Δ_nec do M3AE some com a cor da própria região mas volta com a cor do "
          "entorno, o modelo usa a cor local da região; se some nos dois, só o preto o move.", ""]
    if not out["ring"]:
        L.append("*Pendente: T_ringmean/P_ringmean ainda não rodados.*")
    for key, lv in out["ring"].items():
        L += [f"### {key}", "", "| preenchimento | grupo | n | Acc(T) | Acc(P) | Δ_nec (pp) | IC 95 % | McNemar p |", "|---|---|---:|---:|---:|---:|---|---:|"]
        for f in ("black", "regmean", "ringmean"):
            d = lv.get(f)
            if not d:
                continue
            for gname, s in [("todas", d["pooled"])] + [(CLASS_PT.get(k, k), v) for k, v in d["by_class"].items()] + [("caixa de artefato", d["greenbox"])]:
                if s.get("n", 0) == 0:
                    continue
                ci = s["delta_nec_ci"]
                L.append(f"| {f} | {gname} | {s['n']} | {100 * s['acc_T']:.1f} | {100 * s['acc_P']:.1f} | {100 * s['delta_nec']:+.1f} | "
                         f"[{100 * ci[0]:+.1f}, {100 * ci[1]:+.1f}] | {s['mcnemar']['p_value']:.3g} |")
        L.append("")
    return "\n".join(L) + "\n"


def _fmt(r: dict | None) -> str:
    if not r:
        return "—"
    lo, hi = r["ci"]
    return f"{100 * r['delta']:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}]"


def _e3_row(r: dict) -> str:
    return _e3({"e3": r.get("e3")})


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results-dir", default="results/isbi_placebo"); ap.add_argument("--docs-dir", default="docs/isbi/placebo")
    ap.add_argument("--inventory", default=None)
    a = ap.parse_args(argv)
    out = collect(a.results_dir)
    Path(a.results_dir, "e3_report.json").write_text(json.dumps(out, indent=1) + "\n")
    md = render(out, a.inventory or str(Path(a.results_dir, "inventory_kvasir_test_clean.json")))
    Path(a.docs_dir, "e3_report.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
