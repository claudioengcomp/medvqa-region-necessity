"""Single command of the incremental analysis (request of 14/09): regenerates everything that has
inputs in results/isbi_placebo/ and flags what is missing. Idempotent: running again with more
files only adds.

    python -m harness.isbi_placebo.report_all [--n-boot 10000] [--results-dir ...] [--docs-dir ...]
    make -C docs/isbi/placebo

Per checkpoint (MODEL_PEFT_DATASET_seedN) with C0, T and P present:
  necessity_<ckpt>.{json,md}  (+S, dose, F-mean/F-blur, C4_OCC_75 and the C0 reference from the
                               P0 cache when they exist; M0 per type; SLAKE per class only)
  Kvasir: cf_consistency_<ckpt>, diag_greenbox_<ckpt> (if geometry exists),
          diag_procedure_<ckpt>, diag_size_<ckpt>, figs/fig_quadrants_<ckpt>.{png,pdf}
Then: e3_coverage.{json,md} (what exists on disk per run x fill),
diag_placebo_cost.{json,md} and diag_instrument_templates.{json,md} (exploratory, items 4 and 6 of 15/09), negative_by_template.{json,md} (negative control per template x fill),
p3_table.{json,md} (P3 table and summary per family), slake_table.{json,md} (SLAKE, separate from P3; decision of 15/09), heal_table.{json,md} (HEAL, E5), e3_report.{json,md} (E3, ring),
summary_all.{json,md} (feasibility rule), diag_size_overlap.md (consistency
across seeds) and report_all_status.md (what ran and what is pending).
Nothing here triggers inference or touches arrows, manifests or rules.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
from pathlib import Path

from harness.isbi_placebo import cf_consistency as cf, diag_answers as da, diag_greenbox as dg, diag_templates as dt, diag_instrument_templates as dit, diag_placebo_cost as dpc, e3_coverage as e3c, e3_report as e3, fig_fill_sensitivity as ffs, negative_by_template as nbt, p3_table as p3t, slake_table as slt, heal_table as hlt, fig_quadrants as fq, fill_ablation as fa, summary_all as sa
from harness.isbi_placebo.compute_necessity import compute_necessity, render_markdown

CONDS = ["C0", "T", "P", "S", "T1.5", "P1.5", "T2", "P2", "S2", "T_mean", "P_mean", "T_blur", "P_blur",
         "T_blur10", "P_blur10", "T_regmean", "P_regmean", "T_ringmean", "P_ringmean"]   # E3: plausible fills on the whole set
FILL300_CONDS = ["T_mean", "P_mean", "T_blur", "P_blur", "T_blur1", "P_blur1", "T_blur3", "P_blur3", "T_blur10", "P_blur10", "T_regmean", "P_regmean", "T_ringmean", "P_ringmean"]
_RE = re.compile(r"^(?P<cfg>[A-Z0-9]+(?:_[A-Z0-9]+)?)_(?P<ds>KVASIR|SLAKE|HEAL)_seed(?P<seed>\d)_(?P<cond>" + "|".join(re.escape(c) for c in CONDS) + r")(?P<subset>_mvt500)?\.json$")  # cfg = MODEL_METHOD or just MODEL (M3AE); _mvt500 = MedVLThinker on the 500 stratified questions
KVASIR_EXTRAS = ["cf_consistency", "diag_greenbox", "diag_procedure", "diag_size", "diag_answers", "fig_quadrants"]


def discover_checkpoints(results_dir: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(Path(results_dir).glob("*.json")):
        m = _RE.match(p.name)
        if not m:
            continue
        key = f"{m['cfg']}_{m['ds']}_seed{m['seed']}" + (m["subset"] or "")
        out.setdefault(key, {"config": m["cfg"], "dataset": m["ds"], "seed": int(m["seed"]), "subset": m["subset"], "conds": {}})["conds"][m["cond"]] = str(p)
    return out


def plan_steps(checkpoints: dict[str, dict]) -> list[dict]:
    steps = []
    for key, ck in checkpoints.items():
        missing = [c for c in ("C0", "T", "P") if c not in ck["conds"]]
        if missing:
            steps.append({"checkpoint": key, "status": "pendente", "missing": missing, "artifacts": []})
        else:
            steps.append({"checkpoint": key, "status": "ready", "missing": [],
                          "artifacts": ["necessity"] + (KVASIR_EXTRAS if ck["dataset"] == "KVASIR" else [])})
    return steps


def _p0_cache(results_root: str, cfg: str, ds: str, seed: int, cond: str) -> str | None:
    """P0 file: Kvasir always with _seedN; SLAKE seed 0 without suffix (P0 convention)."""
    cands = [f"{cfg}_{ds}_seed{seed}_{cond}.json"] + ([f"{cfg}_{ds}_{cond}.json"] if seed == 0 else [])
    for c in cands:
        p = os.path.join(results_root, c)
        if os.path.exists(p):
            return p
    return None


def run(results_dir: str, docs_dir: str, results_root: str, n_boot: int, seed: int) -> dict:
    ck = discover_checkpoints(results_dir)
    steps = plan_steps(ck)
    status = {"ran": [], "pending": [], "skipped": []}
    inv = {"KVASIR": os.path.join(results_dir, "inventory_kvasir_test_clean.json"), "SLAKE": os.path.join(results_dir, "inventory_slake_test.json"), "HEAL": os.path.join(results_dir, "inventory_heal_test.json")}
    m0 = {"KVASIR": os.path.join(results_dir, "m0_by_type_kvasir.json"), "SLAKE": os.path.join(results_dir, "m0_by_type_slake.json"), "HEAL": os.path.join(results_dir, "m0_by_type_heal.json")}
    man = {"KVASIR": os.path.join(results_dir, "manifest_kvasir.json"), "SLAKE": os.path.join(results_dir, "manifest_slake.json"), "HEAL": os.path.join(results_dir, "manifest_heal.json")}
    geo = {"KVASIR": os.path.join(results_dir, "placebo_geometry_kvasir.json"), "SLAKE": os.path.join(results_dir, "placebo_geometry_slake.json"), "HEAL": os.path.join(results_dir, "placebo_geometry_heal.json")}
    Path(docs_dir, "figs").mkdir(parents=True, exist_ok=True)
    for st in steps:
        key = st["checkpoint"]; c = ck[key]; ds = c["dataset"]
        if st["status"] != "ready":
            status["pending"].append({"checkpoint": key, "missing": st["missing"]}); continue
        preds = {cond: path for cond, path in c["conds"].items()}
        c4 = _p0_cache(results_root, c["config"], ds, c["seed"], "C4_OCC_75")
        if c4:
            preds["C4_OCC_75"] = c4
        c0ref = _p0_cache(results_root, c["config"], ds, c["seed"], "C0")
        paired = None
        if os.path.exists(man[ds]):
            mj = json.loads(Path(man[ds]).read_text())
            if any("placebo_method_by_factor" in u for u in mj["units"]):   # HEAL has no dose (E5/D4): paired stays None
                paired = [q for u in mj["units"] if all(u.get("placebo_method_by_factor", {}).get(k) is not None for k in ("1.5", "2")) for q in u["qids"]]
        nec = compute_necessity(inv[ds], preds, n_boot, seed, paired, c0ref, m0[ds] if os.path.exists(m0[ds]) else None)
        nec_json = os.path.join(results_dir, f"necessity_{key}.json")
        Path(nec_json).write_text(json.dumps(nec, indent=1) + "\n")
        Path(docs_dir, f"necessity_{key}.md").write_text(render_markdown(nec, template_table=(ds == "KVASIR")))
        done = ["necessity"]
        if ds == "KVASIR":
            base = {k: preds[k] for k in ("C0", "T", "P")}
            out = cf.cf_consistency(inv[ds], base, n_boot, seed)
            Path(results_dir, f"cf_consistency_{key}.json").write_text(json.dumps(out, indent=1) + "\n")
            Path(docs_dir, f"cf_consistency_{key}.md").write_text(cf.render_markdown(out)); done.append("cf_consistency")
            if os.path.exists(geo[ds]):
                out = dg.diag_greenbox(inv[ds], geo[ds], base)
                Path(results_dir, f"diag_greenbox_{key}.json").write_text(json.dumps(out, indent=1) + "\n")
                Path(docs_dir, f"diag_greenbox_{key}.md").write_text(dg.render(out)); done.append("diag_greenbox")
            else:
                status["skipped"].append({"checkpoint": key, "artifact": "diag_greenbox", "reason": "sem placebo_geometry_kvasir.json"})
            out = dt.diag_procedure(inv[ds], base)
            Path(results_dir, f"diag_procedure_{key}.json").write_text(json.dumps(out, indent=1) + "\n")
            Path(docs_dir, f"diag_procedure_{key}.md").write_text(dt.render_procedure(out)); done.append("diag_procedure")
            out = dt.diag_size(inv[ds], base)
            Path(results_dir, f"diag_size_{key}.json").write_text(json.dumps(out, indent=1) + "\n")
            Path(docs_dir, f"diag_size_{key}.md").write_text(dt.render_size(out)); done.append("diag_size")
            out = da.diag_answers(inv[ds], base)
            Path(results_dir, f"diag_answers_{key}.json").write_text(json.dumps(out, indent=1) + "\n")
            Path(docs_dir, f"diag_answers_{key}.md").write_text(da.render(out)); done.append("diag_answers")
            fq.make_figure(nec_json, inv[ds], os.path.join(docs_dir, "figs", f"fig_quadrants_{key}")); done.append("fig_quadrants")
            fills = {c: os.path.join(results_dir, f"{key}_{c}_fill300.json") for c in FILL300_CONDS}
            fills = {c: p for c, p in fills.items() if os.path.exists(p)}
            subset = os.path.join(docs_dir, "fill_ablation_subset_kvasir.json")
            if fills and os.path.exists(subset):
                out = fa.fill_ablation(inv[ds], subset, {**base, **fills}, n_boot, seed)
                Path(results_dir, f"fill_ablation_{key}.json").write_text(json.dumps(out, indent=1) + "\n")
                Path(docs_dir, f"fill_ablation_{key}.md").write_text(fa.render(out)); done.append("fill_ablation")
        status["ran"].append({"checkpoint": key, "artifacts": done, "conditions": sorted(preds)})
    if os.path.exists(inv["KVASIR"]):
        ffs.make_figure(results_dir, inv["KVASIR"], os.path.join(docs_dir, "figs", "fig_fill_sensitivity_kvasir"))
    cov = e3c.collect(results_dir)
    Path(results_dir, "e3_coverage.json").write_text(json.dumps(cov, indent=1) + "\n")
    Path(docs_dir, "e3_coverage.md").write_text(e3c.render(cov))
    if os.path.exists(inv["KVASIR"]):
        dpc_out = dpc.collect(results_dir, inv["KVASIR"], n_boot, seed)
        Path(results_dir, "diag_placebo_cost.json").write_text(json.dumps(dpc_out, indent=1) + "\n")
        Path(docs_dir, "diag_placebo_cost.md").write_text(dpc.render(dpc_out))
        dit_out = dit.collect(results_dir, inv["KVASIR"], n_boot, seed)
        Path(results_dir, "diag_instrument_templates.json").write_text(json.dumps(dit_out, indent=1) + "\n")
        Path(docs_dir, "diag_instrument_templates.md").write_text(dit.render(dit_out))
    nbt_out = nbt.collect(results_dir, inv["KVASIR"], n_boot, seed)
    Path(results_dir, "negative_by_template.json").write_text(json.dumps(nbt_out, indent=1) + "\n")
    Path(docs_dir, "negative_by_template.md").write_text(nbt.render(nbt_out))
    p3_out = p3t.collect(results_dir)
    Path(results_dir, "p3_table.json").write_text(json.dumps(p3_out, indent=1) + "\n")
    Path(docs_dir, "p3_table.md").write_text(p3t.render(p3_out))
    slt_out = slt.collect(results_dir)
    Path(results_dir, "slake_table.json").write_text(json.dumps(slt_out, indent=1) + "\n")
    Path(docs_dir, "slake_table.md").write_text(slt.render(slt_out))
    hlt_out = hlt.collect(results_dir)
    Path(results_dir, "heal_table.json").write_text(json.dumps(hlt_out, indent=1) + "\n")
    Path(docs_dir, "heal_table.md").write_text(hlt.render(hlt_out))
    e3out = e3.collect(results_dir)
    Path(results_dir, "e3_report.json").write_text(json.dumps(e3out, indent=1) + "\n")
    Path(docs_dir, "e3_report.md").write_text(e3.render(e3out, inv["KVASIR"]))
    summ = sa.summarize(results_dir)
    Path(results_dir, "summary_all.json").write_text(json.dumps(summ, indent=1) + "\n")
    Path(docs_dir, "summary_all.md").write_text(sa.render(summ))
    _size_overlap(results_dir, docs_dir)
    _write_status(docs_dir, status, summ)
    return status


def _size_overlap(results_dir: str, docs_dir: str) -> None:
    by_cfg = collections.defaultdict(dict)
    for p in sorted(Path(results_dir).glob("diag_size_*.json")):
        m = re.match(r"diag_size_(?P<cfg>[A-Z0-9]+(?:_[A-Z0-9]+)?_KVASIR)_seed(?P<seed>\d)\.json", p.name)
        if m:
            by_cfg[m["cfg"]][int(m["seed"])] = {it["qid"] for it in json.loads(p.read_text())["right_under_P_wrong_under_C0"]}
    L = ["# Tamanho do pólipo: itens que acertam sob P e erram sob C0 — consistência entre seeds", "",
         "| configuração | seeds | itens por seed | interseção de todas | união |", "|---|---|---|---:|---:|"]
    for cfg, seeds in sorted(by_cfg.items()):
        sets = [seeds[s] for s in sorted(seeds)]
        inter = set.intersection(*sets) if sets else set(); union = set.union(*sets) if sets else set()
        L.append(f"| {cfg} | {', '.join(str(s) for s in sorted(seeds))} | {', '.join(str(len(s)) for s in sets)} | {len(inter)} | {len(union)} |")
        if len(sets) >= 2:
            L.append(f"| | | qids na interseção: {sorted(inter) or '—'} | | |")
    L += ["", "Leitura: consistente entre seeds se a interseção for uma fração substancial da união; caso contrário, não consistente. Sem outra interpretação."]
    Path(docs_dir, "diag_size_overlap.md").write_text("\n".join(L) + "\n")


def _write_status(docs_dir: str, status: dict, summ: dict) -> None:
    L = ["# report_all — estado da última execução", "", "## Rodou", ""]
    L += [f"- {r['checkpoint']}: {', '.join(r['artifacts'])} (condições: {', '.join(r['conditions'])})" for r in status["ran"]] or ["- nada"]
    L += ["", "## Pendente (falta C0, T ou P)", ""] + ([f"- {p['checkpoint']}: falta {', '.join(p['missing'])}" for p in status["pending"]] or ["- nada"])
    L += ["", "## Pulado", ""] + ([f"- {s['checkpoint']} / {s['artifact']}: {s['reason']}" for s in status["skipped"]] or ["- nada"])
    L += ["", "## Regra de viabilidade (pré-registro §6, P3)", ""]
    for ds, v in summ["viability"].items():
        L.append(f"- {ds}: {v['n_rows_ok']}/{v['n_rows_total']} linhas; decisão **{v['decision']}**" + (f" ({v['partial_read']})" if v["partial_read"] else ""))
    Path(docs_dir, "report_all_status.md").write_text("\n".join(L) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results-dir", default="results/isbi_placebo"); ap.add_argument("--docs-dir", default="docs/isbi/placebo")
    ap.add_argument("--results-root", default="results", help="cache do P0 (C4_OCC_75 e C0 de referência)")
    ap.add_argument("--n-boot", type=int, default=10000); ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args(argv)
    st = run(a.results_dir, a.docs_dir, a.results_root, a.n_boot, a.seed)
    print(json.dumps({"ran": [r["checkpoint"] for r in st["ran"]], "pending": st["pending"], "skipped": st["skipped"]}, indent=1))


if __name__ == "__main__":
    main()
