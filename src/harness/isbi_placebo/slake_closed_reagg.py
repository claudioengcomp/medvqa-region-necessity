"""E8 (01/10/2026, pre-registration §7): reading of the SLAKE headroom on the evaluable CLOSED-ENDED questions.

The SLAKE M0 (`M0_question_only_SLAKE_C0.json`) exists only on the 416 closed-ended questions; Δ_nec and Acc(C0) of
`slake_table.md` were measured on the 388 evaluable ones, which include 212 open-ended. Here both sides of the headroom
are on the same subset: the evaluable closed-ended questions (disease 92, organ 24, negative control 60).

Nothing is re-inferred and no statistic is rewritten: the inventory is copied with `evaluable` unset outside
the closed-ended set and handed to `compute_necessity.compute_necessity`, which computes Acc, Δ_nec
(paired bootstrap 10,000), McNemar, Holm, sufficiency, E3 and headroom exactly as on the 388. The M0 per
class comes from `m0_by_type_slake.json` (already over the evaluable closed-ended questions), hence `n_m0 == n`.

Outputs: `results/isbi_placebo/inventory_slake_test_closed.json`, `slake_closed_<cell>.json` (16 cells,
C0/T/P/S + blur 10 % + region mean color; no C4 and no dose), `slake_closed_summary.json` (P2 decision) and
`docs/isbi/placebo/slake_closed_table.md` (format of `slake_table.md`).

    python -m harness.isbi_placebo.slake_closed_reagg --all [--n-boot 10000] [--jobs 8]
    python -m harness.isbi_placebo.slake_closed_reagg --cell QWEN2VL_LORA_SLAKE_seed0
"""
from __future__ import annotations

import argparse
import json
import multiprocessing
from pathlib import Path

from harness.isbi_placebo import slake_table
from harness.isbi_placebo.compute_necessity import compute_necessity

M0_FILE = "results/M0_question_only_SLAKE_C0.json"
M0_BY_TYPE = "results/isbi_placebo/m0_by_type_slake.json"
INVENTORY = "results/isbi_placebo/inventory_slake_test.json"
RESULTS = "results/isbi_placebo"
DOCS = "docs/isbi/placebo"
CORE = ("C0", "T", "P", "S", "T_blur10", "P_blur10", "T_regmean", "P_regmean")
CLASSES = ("dependent_disease", "dependent_organ", "negative_control")
PREFIX = "slake_closed"
RULE_MIN_NO_MARGIN = 14   # plan, Task 3: headroom <= 0 on disease in >= 14/16 cells -> regime B confirmed


def closed_qids(m0_path: str = M0_FILE) -> set[int]:
    """The qids where the M0 exists: the closed-ended questions of the SLAKE test set (416)."""
    return {p["qid"] for p in json.loads(Path(m0_path).read_text())["predictions"]}


def closed_inventory(inventory: str, qids: set[int], out_path: str) -> dict:
    """Copy of the inventory with `evaluable` restricted to the closed-ended set; no question is removed."""
    inv = json.loads(Path(inventory).read_text())
    by_class: dict[str, int] = {}
    for q in inv["questions"]:
        q["evaluable_388"] = bool(q["evaluable"])
        q["evaluable"] = bool(q["evaluable"]) and q["qid"] in qids
        if q["evaluable"]:
            by_class[q["question_class"]] = by_class.get(q["question_class"], 0) + 1
    n = sum(by_class.values())
    inv["summary"] = {**inv.get("summary", {}), "amendment": "E8", "source_inventory": inventory, "closed_qids_source": M0_FILE,
                      "n_closed_qids": len(qids), "n_evaluable_388": sum(q["evaluable_388"] for q in inv["questions"]),
                      "n_evaluable_closed": n, "evaluable_closed_by_class": dict(sorted(by_class.items()))}
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps(inv, indent=1) + "\n")
    return {"n_evaluable_closed": n, "by_class": dict(sorted(by_class.items()))}


def _class_summary(s: dict) -> dict:
    acc = s.get("acc", {}); ci = s.get("delta_nec_ci")
    out = {"n": s.get("n"), "acc_c0": acc.get("C0"), "acc_t": acc.get("T"), "acc_p": acc.get("P"), "acc_s": acc.get("S"),
           "delta_nec": s.get("delta_nec"), "ci": ci, "p_mcnemar": (s.get("mcnemar") or {}).get("p_value"), "p_holm": s.get("p_holm"),
           "m0": s.get("acc_m0"), "n_m0": s.get("n_m0"), "headroom": s.get("ceiling"), "no_margin": s.get("no_margin"),
           "sufficiency": s.get("sufficiency"), "e3": (s.get("e3") or {}).get("necessary")}
    for f in ("blur10", "regmean"):
        out[f"delta_nec_{f}"] = s.get(f"delta_nec_{f}"); out[f"ci_{f}"] = s.get(f"delta_nec_{f}_ci")
    return out


def reaggregate(cell: str, classes: tuple[str, ...] = CLASSES, n_boot: int = 10000, seed: int = 42,
                results_dir: str = RESULTS, out_dir: str | None = None) -> dict:
    """Re-aggregates one cell (e.g. QWEN2VL_LORA_SLAKE_seed0) on the evaluable closed-ended questions. Writes
    `<out_dir>/slake_closed_<cell>.json` (full output of compute_necessity + E8 provenance stamp) and returns the
    summary per class: n, acc_c0/t/p/s, delta_nec, ci, p_mcnemar, m0, headroom, sufficiency, e3."""
    out_dir = out_dir or results_dir
    nec = json.loads(Path(results_dir, f"necessity_{cell}.json").read_text())
    preds = {c: p for c, p in nec["predictions"].items() if c in CORE}
    missing = [c for c in CORE if c not in preds]
    if missing:
        raise FileNotFoundError(f"{cell}: condicoes ausentes na necessity_{cell}.json: {missing}")
    inv_closed = str(Path(out_dir, "inventory_slake_test_closed.json"))
    counts = closed_inventory(INVENTORY, closed_qids(M0_FILE), inv_closed)
    out = compute_necessity(inv_closed, preds, n_boot=n_boot, seed=seed, m0_by_type=M0_BY_TYPE)
    out = {"amendment": "E8", "cell": cell, "source_necessity": str(Path(results_dir, f"necessity_{cell}.json")),
           "closed_qids_source": M0_FILE, "closed_counts": counts, **out}
    Path(out_dir, f"{PREFIX}_{cell}.json").write_text(json.dumps(out, indent=1) + "\n")
    return {cls: _class_summary(out["by_class"].get(cls, {})) for cls in classes}


def decide_regime(rows: dict[str, dict], cls: str = "dependent_disease") -> dict:
    """Rule of the plan (Task 3): headroom <= 0 on disease in >= 14/16 cells -> regime B confirmed."""
    hs = {k: r[cls]["headroom"] for k, r in rows.items() if r.get(cls, {}).get("headroom") is not None}
    n_no = sum(h <= 0 for h in hs.values())
    return {"class": cls, "n_cells": len(hs), "n_no_margin": n_no, "n_positive": len(hs) - n_no, "rule": f">= {RULE_MIN_NO_MARGIN}/16 com teto <= 0",
            "regime": "B" if n_no >= RULE_MIN_NO_MARGIN else "small headroom, no necessity (ou Limitacoes)",
            "headroom_by_cell": dict(sorted(hs.items())), "e3_by_cell": {k: r[cls].get("e3") for k, r in rows.items()},
            "n_e3_yes": sum(bool(r[cls].get("e3")) for r in rows.values())}


def _worker(args):
    cell, n_boot, seed, results_dir = args
    return cell, reaggregate(cell, n_boot=n_boot, seed=seed, results_dir=results_dir)


def cells(results_dir: str = RESULTS) -> list[str]:
    return sorted(p.name[len("necessity_"):-len(".json")] for p in Path(results_dir).glob("necessity_*_SLAKE_seed*.json")
                  if slake_table._RE.match(p.name))


def run_all(n_boot: int = 10000, seed: int = 42, jobs: int = 4, results_dir: str = RESULTS, docs_dir: str = DOCS) -> dict:
    todo = [(c, n_boot, seed, results_dir) for c in cells(results_dir)]
    if jobs > 1:
        with multiprocessing.Pool(jobs) as pool:
            rows = dict(pool.map(_worker, todo))
    else:
        rows = dict(map(_worker, todo))
    decision = decide_regime(rows)
    summary = {"amendment": "E8", "n_boot": n_boot, "seed": seed, "n_cells": len(rows), "rows": rows, "decision": decision}
    Path(results_dir, f"{PREFIX}_summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    table = slake_table.collect(results_dir, prefix=PREFIX)
    Path(results_dir, f"{PREFIX}_table.json").write_text(json.dumps(table, indent=1) + "\n")
    intro = ("Δ_nec = Acc(P) − Acc(T) em pp, IC 95 % bootstrap pareado, **176 perguntas fechadas avaliáveis (doença 92, órgão 24, "
             "negativo 60)** — emenda E8: M0 e Acc(C0) no mesmo subconjunto e na mesma régua. A tabela de 388 (`slake_table.md`) continua "
             "reportada; a decisão de regime usa esta. **Negrito** = IC exclui zero (para cima em doença e órgão; qualquer lado no controle "
             "negativo). Preto, blur 10 % da largura e cor média da própria região. E3 = preto E (blur 10 % ou cor média). Teto = Acc(C0) − M0 "
             "por classe, em pp; \"sem margem\" = teto ≤ 0, nΔ_nec indefinido. Gerado por `harness/isbi_placebo/slake_closed_reagg.py`.")
    md = slake_table.render(table, title="# Tabela do SLAKE nas fechadas avaliáveis (E8) — células × preenchimento × classe", intro=intro)
    md += (f"\n## Decisão P2 (regra: teto ≤ 0 na doença em ≥ {RULE_MIN_NO_MARGIN}/16)\n\n"
           f"Teto ≤ 0 na doença em **{decision['n_no_margin']}/{decision['n_cells']}** células; E3 \"sim\" na doença em {decision['n_e3_yes']}/{decision['n_cells']}. "
           f"Regime: **{decision['regime']}**.\n")
    Path(docs_dir, f"{PREFIX}_table.md").write_text(md)
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true"); ap.add_argument("--cell")
    ap.add_argument("--n-boot", type=int, default=10000); ap.add_argument("--seed", type=int, default=42); ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--results-dir", default=RESULTS); ap.add_argument("--docs-dir", default=DOCS)
    a = ap.parse_args(argv)
    if a.all:
        s = run_all(a.n_boot, a.seed, a.jobs, a.results_dir, a.docs_dir)
        print(json.dumps(s["decision"], indent=1, ensure_ascii=False))
    elif a.cell:
        print(json.dumps(reaggregate(a.cell, n_boot=a.n_boot, seed=a.seed, results_dir=a.results_dir), indent=1))
    else:
        ap.error("--all ou --cell")


if __name__ == "__main__":
    main()
