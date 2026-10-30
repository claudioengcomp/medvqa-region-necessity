"""Multi-configuration consolidator (analysis request of 14/09, item 8).

Reads results/isbi_placebo/necessity_<MODEL>_<PEFT>_<DATASET>_seed<N>.json (ignores
suffixes such as _jpeg_pilot) and produces summary_all.{json,md}: one row per
checkpoint x seed with Δ_nec, 95 % CI and p per class, marking "pending" for
what has not arrived yet, and the automatic check of the feasibility rule of the
pre-registration (§6, P3):

  in at least one dependent type, the 95 % CI of Δ_nec excludes zero in >= 4 of the 5
  fine-tuned Kvasir configurations, AND the negative control has a CI including
  zero in all of them, with |Δ_nec| <= 2 pp at the point estimate.

Configuration = model x method (the three seeds are never pooled): counts as
"excludes zero" when ALL available seeds exclude zero; the report also gives
the count per seed. The decision only stops being "pending" when the
five configurations have all three seeds.

E2 (15/09/2026): the rule is evaluated and reported under BOTH fills --
black (primary) and blur (mandatory robustness arm) -- and the negative
control is also reported per template (text, artifact box,
procedure), because the aggregate under black hides a cancellation.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

NEG_TEMPLATES = {"Is there text?": "texto", "Is there a green/black box artefact?": "caixa", "What type of procedure is the image taken from?": "procedimento"}
EXPECTED = ["QWEN2VL_LORA", "QWEN2VL_DORA", "SMOLVLM_LORA", "SMOLVLM_DORA", "M3AE"]   # 5 fine-tuned configurations (M3AE = the model only)
# SLAKE (clarified by the authors, 15/09): the 5th configuration is the from-scratch M3AE trained in the lab (M3AE_SCRATCH; only seed 0
# has a checkpoint on disk); the fine-tuned checkpoint released by the M3AE authors (M3AE, one seed) enters as an extra reference.
EXPECTED_BY_DATASET = {"KVASIR": EXPECTED, "SLAKE": ["QWEN2VL_LORA", "QWEN2VL_DORA", "SMOLVLM_LORA", "SMOLVLM_DORA", "M3AE_SCRATCH"],
                       "HEAL": ["QWEN2VL_LORA", "QWEN2VL_DORA", "SMOLVLM_LORA", "SMOLVLM_DORA", "M3AE"]}   # HEAL: E5 (15/09), M3AE from scratch = M3AE_HEAL
EXTRA_BY_DATASET = {"KVASIR": ["MEDVLTHINKER_ZEROSHOT"], "SLAKE": ["M3AE", "MEDVLTHINKER_ZEROSHOT"], "HEAL": ["MEDVLTHINKER_ZEROSHOT"]}
EXTRA = ["MEDVLTHINKER_ZEROSHOT"]
SEEDS = (0, 1, 2)
DATASETS = ("KVASIR", "SLAKE", "HEAL")
DEPENDENT = {"KVASIR": ["dependent_polyp", "dependent_instrument"], "SLAKE": ["dependent_disease", "dependent_organ"], "HEAL": ["closed_yes", "closed_no"]}
_RE = re.compile(r"^necessity_(?P<cfg>[A-Z0-9]+(?:_[A-Z0-9]+)?)_(?P<ds>KVASIR|SLAKE|HEAL)_seed(?P<seed>\d)\.json$")


def discover(results_dir: str) -> dict[str, dict]:
    found = {}
    for p in sorted(Path(results_dir).glob("necessity_*.json")):
        m = _RE.match(p.name)
        if m:
            found[f"{m['cfg']}_{m['ds']}_seed{m['seed']}"] = {"path": str(p), "config": m["cfg"], "dataset": m["ds"], "seed": int(m["seed"])}
    return found


def _class_row(st: dict) -> dict:
    lo, hi = st["delta_nec_ci"]
    row = {"n": st["n"], "delta_nec": st["delta_nec"], "ci": [lo, hi], "p": st["mcnemar"]["p_value"], "p_holm": st.get("p_holm"),
           "sufficiency": st.get("sufficiency"), "excludes_zero": (lo > 0) or (hi < 0),
           "within_2pp_and_includes_zero": (lo <= 0 <= hi) and abs(st["delta_nec"]) <= 0.02}
    if "delta_nec_blur" in st:
        blo, bhi = st["delta_nec_blur_ci"]
        row["blur"] = {"delta_nec": st["delta_nec_blur"], "ci": [blo, bhi], "p": st["mcnemar_blur"]["p_value"],
                       "excludes_zero": (blo > 0) or (bhi < 0), "within_2pp_and_includes_zero": (blo <= 0 <= bhi) and abs(st["delta_nec_blur"]) <= 0.02}
    return row


def _neg_templates(nec: dict) -> dict:
    out = {}
    for q, short in NEG_TEMPLATES.items():
        st = nec.get("by_template", {}).get(q)
        if st and "delta_nec" in st:
            out[short] = {"n": st["n"], "delta_nec": st["delta_nec"], "ci": st["delta_nec_ci"],
                          **({"delta_nec_blur": st["delta_nec_blur"], "ci_blur": st["delta_nec_blur_ci"]} if "delta_nec_blur" in st else {})}
    return out


def _viability_for_fill(ds_rows: list[dict], ds: str, fill: str) -> dict:
    def get(r, cls):
        c = r["classes"].get(cls)
        if not c:
            return None
        return c if fill == "black" else c.get("blur")
    by_class = {}
    for cls in DEPENDENT[ds]:
        per_cfg = {}
        n_runs = n_runs_ok = 0
        for cfg in EXPECTED_BY_DATASET[ds]:
            seeds_ok = [get(r, cls)["excludes_zero"] for r in ds_rows if r["config"] == cfg and r["status"] == "ok" and get(r, cls)]
            n_runs += len(seeds_ok); n_runs_ok += sum(seeds_ok)
            per_cfg[cfg] = {"n_seeds": len(seeds_ok), "n_exclude_zero": sum(seeds_ok), "all_seeds_exclude_zero": bool(seeds_ok) and all(seeds_ok)}
        by_class[cls] = {"per_config": per_cfg, "configs_all_seeds_exclude_zero": sum(v["all_seeds_exclude_zero"] for v in per_cfg.values()),
                         "configs_with_data": sum(v["n_seeds"] > 0 for v in per_cfg.values()), "seed_runs_exclude_zero": f"{n_runs_ok}/{n_runs}"}
    neg = [get(r, "negative_control")["within_2pp_and_includes_zero"] for r in ds_rows if r["status"] == "ok" and get(r, "negative_control")]
    n_avail = sum(1 for r in ds_rows if r["status"] == "ok" and get(r, "negative_control"))
    complete = n_avail == len(ds_rows)
    any_class_ok = any(v["configs_all_seeds_exclude_zero"] >= 4 for v in by_class.values())
    neg_ok = bool(neg) and all(neg)
    decision = "pendente" if not complete else ("viável" if any_class_ok and neg_ok else "não atinge a regra")
    return {"fill": fill, "n_rows_ok": n_avail, "n_rows_total": len(ds_rows), "by_class": by_class,
            "negative_control": {"n_available": len(neg), "all_available_ok": neg_ok, "n_ok": sum(neg)}, "decision": decision,
            "partial_read": None if complete else ("regra satisfeita até aqui" if any_class_ok and neg_ok else "ainda não satisfeita")}


def summarize(results_dir: str) -> dict:
    found = discover(results_dir)
    rows = []
    for ds in DATASETS:
        for cfg in EXPECTED_BY_DATASET[ds] + EXTRA_BY_DATASET[ds]:
            for seed in (SEEDS if cfg in EXPECTED_BY_DATASET[ds] else (0,)):
                key = f"{cfg}_{ds}_seed{seed}"
                if key in found:
                    nec = json.loads(Path(found[key]["path"]).read_text())
                    classes = {k: _class_row(v) for k, v in nec["by_class"].items() if "delta_nec_ci" in v}
                    rows.append({"checkpoint": key, "config": cfg, "dataset": ds, "seed": seed, "status": "ok",
                                 "n_aligned": nec.get("n_aligned"), "conditions": list(nec.get("predictions", {})), "classes": classes,
                                 "negative_templates": _neg_templates(nec)})
                else:
                    rows.append({"checkpoint": key, "config": cfg, "dataset": ds, "seed": seed, "status": "pendente", "classes": {}})
    viability = {}
    for ds in DATASETS:
        ds_rows = [r for r in rows if r["dataset"] == ds and r["config"] in EXPECTED_BY_DATASET[ds]]
        black = _viability_for_fill(ds_rows, ds, "black"); blur = _viability_for_fill(ds_rows, ds, "blur")
        viability[ds] = {**black, "fills": {"black": black, "blur": blur}, "n_expected_configs": len(EXPECTED_BY_DATASET[ds])}
    return {"results_dir": results_dir, "rows": rows, "viability": viability}


def render(out: dict) -> str:
    L = ["# Consolidado multi-configuração — necessidade com placebo posicional", "",
         "Uma linha por checkpoint × seed; `pendente` = necessity_*.json ainda não existe. Δ_nec em pp com IC 95 % (bootstrap pareado) e p de McNemar (Holm dentro do dataset).", ""]
    for ds in DATASETS:
        rows = [r for r in out["rows"] if r["dataset"] == ds]
        classes = DEPENDENT[ds] + ["negative_control"]
        L += [f"## {ds}", "", "| checkpoint | status | " + " | ".join(f"{c}: Δ_nec [IC] p" for c in classes) + " | blur: " + " / ".join(classes) + " |",
              "|---|---|" + "---|" * (len(classes) + 1)]
        for r in rows:
            if r["status"] != "ok":
                L.append(f"| {r['checkpoint']} | pendente |" + " — |" * (len(classes) + 1)); continue
            cells, bcells = [], []
            for c in classes:
                s = r["classes"].get(c)
                if not s:
                    cells.append("—"); bcells.append("—"); continue
                mark = "✓" if (s["excludes_zero"] if c != "negative_control" else s["within_2pp_and_includes_zero"]) else "✗"
                cells.append(f"{100 * s['delta_nec']:+.1f} [{100 * s['ci'][0]:+.1f}, {100 * s['ci'][1]:+.1f}] p={s['p']:.2g} {mark}")
                b = s.get("blur")
                bcells.append(f"{100 * b['delta_nec']:+.1f} [{100 * b['ci'][0]:+.1f}, {100 * b['ci'][1]:+.1f}] "
                              + ("✓" if (b["excludes_zero"] if c != "negative_control" else b["within_2pp_and_includes_zero"]) else "✗") if b else "pendente")
            L.append(f"| {r['checkpoint']} | ok | " + " | ".join(cells) + " | " + " / ".join(bcells) + " |")
        v = out["viability"][ds]
        for fill, vf in v["fills"].items():
            L += ["", f"**Viabilidade ({ds}, preenchimento {fill}):** {vf['n_rows_ok']}/{vf['n_rows_total']} linhas disponíveis; decisão: **{vf['decision']}**"
                  + (f" ({vf['partial_read']})" if vf["partial_read"] else "") + ".", ""]
            for cls, b in vf["by_class"].items():
                L.append(f"- {cls}: configurações com todas as seeds disponíveis excluindo zero = {b['configs_all_seeds_exclude_zero']}/{b['configs_with_data']} "
                         f"(regra: ≥ 4 de {v['n_expected_configs']}); por seed: {b['seed_runs_exclude_zero']}.")
            n = vf["negative_control"]
            L.append(f"- controle negativo: IC inclui zero e |Δ_nec| ≤ 2 pp em {n['n_ok']}/{n['n_available']} linhas disponíveis"
                     + (" (todas)" if n["all_available_ok"] else " (**falha em ao menos uma**)" if n["n_available"] else "") + ".")
        neg_rows = [r for r in rows if r["status"] == "ok" and r.get("negative_templates")]
        if neg_rows:
            L += ["", f"### Controle negativo por template ({ds}) — Δ_nec preto [IC] · blur [IC]", "",
                  "| checkpoint | " + " | ".join(NEG_TEMPLATES.values()) + " |", "|---|" + "---|" * len(NEG_TEMPLATES)]
            for r in neg_rows:
                cells = []
                for short in NEG_TEMPLATES.values():
                    t = r["negative_templates"].get(short)
                    if not t:
                        cells.append("—"); continue
                    cell = f"{100 * t['delta_nec']:+.1f} [{100 * t['ci'][0]:+.1f}, {100 * t['ci'][1]:+.1f}]"
                    if "delta_nec_blur" in t:
                        cell += f" · {100 * t['delta_nec_blur']:+.1f} [{100 * t['ci_blur'][0]:+.1f}, {100 * t['ci_blur'][1]:+.1f}]"
                    cells.append(cell)
                L.append(f"| {r['checkpoint']} | " + " | ".join(cells) + " |")
        L.append("")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results-dir", default="results/isbi_placebo")
    ap.add_argument("--output-json", default="results/isbi_placebo/summary_all.json")
    ap.add_argument("--output-md", default="docs/isbi/placebo/summary_all.md")
    a = ap.parse_args(argv)
    out = summarize(a.results_dir)
    Path(a.output_json).write_text(json.dumps(out, indent=1) + "\n")
    md = render(out)
    Path(a.output_md).write_text(md)
    print(md)


if __name__ == "__main__":
    main()
