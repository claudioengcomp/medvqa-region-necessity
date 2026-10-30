"""F6 -- necessity/sufficiency analysis over the prediction cache (plan v2 §3).

Never re-infers. Reads the inventory (class, template, evaluable, xray flag) and the
per-condition prediction files (harness format: predictions[{qid,
predicted, gold, correct}]), aligns on the evaluable qids present in ALL
given conditions (missing ones are reported, never silently dropped) and
computes, per class, per template, overall and per xray flag:

- Acc per condition; VDD(cond) = Acc(C0) - Acc(cond);
- Δ_nec = Acc(P) - Acc(T), paired; 95 % CI by paired bootstrap
  (`harness.stats.compute_ldv.bootstrap_paired_diff_ci`, 10,000 by default);
- McNemar P vs T on the discordant pairs (b = correct under P and wrong under T; c = the reverse),
  exact if b+c < 25, with Cohen's g; Holm over the classes of the main table
  (dependent + negative control; the secondary class stays out);
- sufficiency = Acc(S)/Acc(C0); flip rate P(pred_cond != pred_C0);
- dose: Δ_nec at 1x, 1.5x and 2x ONLY on the paired subset (qids of the units
  valid at all three levels, from the manifest);
- C0 reproduction: item-by-item disagreement against a reference cache,
  restricted to the evaluable qids (reading: 0 % in the same environment; 2.7-5.9 % across
  environments).

Usage:
    python -m harness.isbi_placebo.compute_necessity         --inventory results/isbi_placebo/inventory_kvasir_test_clean.json         --pred C0=results/isbi_placebo/QWEN2VL_LORA_KVASIR_seed0_C0.json         --pred T=... --pred P=... --pred S=...         --pred C4_OCC_75=$LAB_ROOT/.../med-vqa-icdip-p0/results/QWEN2VL_LORA_KVASIR_seed0_C4_OCC_75.json         --c0-reference $LAB_ROOT/.../med-vqa-icdip-p0/results/QWEN2VL_LORA_KVASIR_seed0_C0.json         --manifest results/isbi_placebo/manifest_kvasir.json         --output-json results/isbi_placebo/necessity_QWEN2VL_LORA_KVASIR_seed0.json         --output-md docs/isbi/placebo/necessity_QWEN2VL_LORA_KVASIR_seed0.md
"""
from __future__ import annotations
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable

import argparse
import collections
import json
from pathlib import Path

import numpy as np

from harness.isbi_placebo.compare_prediction_files import compare_predictions
from harness.stats.compute_ldv import bootstrap_paired_diff_ci, mcnemar_test

MAIN_TABLE_CLASSES = ("dependent_polyp", "dependent_instrument", "dependent_organ", "dependent_disease",
                      "negative_control")
DOSE_LEVELS = {"1": ("T", "P"), "1.5": ("T1.5", "P1.5"), "2": ("T2", "P2")}
PLAUSIBLE_FILLS = {"blur": ("T_blur", "P_blur"),              # E2: sigma = 25 px (4 % of the width)
                   "blur10": ("T_blur10", "P_blur10"),        # E3: sigma = 10 % of the width
                   "regmean": ("T_regmean", "P_regmean"),     # E3: mean colour of the region itself
                   "ringmean": ("T_ringmean", "P_ringmean")}  # mean colour of the surroundings (15 px ring)
E3_PLAUSIBLE = ("blur10", "regmean")   # the two plausible fills that count toward the E3 criterion
DOSE_ONLY = {"T1.5", "P1.5", "T2", "P2"}   # exist (P) only for the units with a valid dilated control occlusion: outside the main table


def _load_preds(path: str) -> dict[int, dict]:
    d = json.loads(Path(path).read_text())
    return {p["qid"]: p for p in d["predictions"]}


def holm(pvals: dict[str, float]) -> dict[str, float]:
    """Holm (step-down) correction; returns the adjusted p per key."""
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out, running = {}, 0.0
    for i, (k, p) in enumerate(items):
        running = max(running, (m - i) * p)
        out[k] = min(1.0, running)
    return out


def _group_stats(qids: list[int], preds: dict[str, dict[int, dict]], n_boot: int, seed: int) -> dict:
    n = len(qids)
    if n == 0:
        return {"n": 0}
    correct = {c: [bool(preds[c][q]["correct"]) for q in qids] for c in preds}
    acc = {c: sum(v) / n for c, v in correct.items()}
    out = {"n": n, "acc": acc}
    out.update(_paired_component_cis(correct, n_boot, seed))   # acc_ci per condition and sufficiency_ci (request of 15/09/2026, HEAL)
    if "C0" in acc:
        out["vdd"] = {c: acc["C0"] - acc[c] for c in acc if c != "C0"}
        out["vdd_ci"] = {c: list(bootstrap_paired_diff_ci(correct["C0"], correct[c], n_boot=n_boot, seed=seed))
                         for c in acc if c != "C0"}
        out["flip_rate"] = {c: sum(preds[c][q]["predicted"] != preds["C0"][q]["predicted"] for q in qids) / n
                            for c in preds if c != "C0"}
        if "S" in acc:
            out["sufficiency"] = acc["S"] / acc["C0"] if acc["C0"] > 0 else None
    if "T" in acc and "P" in acc:
        out["delta_nec"] = acc["P"] - acc["T"]
        out["delta_nec_ci"] = list(bootstrap_paired_diff_ci(correct["P"], correct["T"], n_boot=n_boot, seed=seed))
        out["mcnemar"] = mcnemar_test(correct["P"], correct["T"])
    for name, (tc, pc) in PLAUSIBLE_FILLS.items():   # E2 (blur, mandatory) and E3 (blur 10 %, region mean color), same slice
        if tc in acc and pc in acc:
            out[f"delta_nec_{name}"] = acc[pc] - acc[tc]
            out[f"delta_nec_{name}_ci"] = list(bootstrap_paired_diff_ci(correct[pc], correct[tc], n_boot=n_boot, seed=seed))
            out[f"mcnemar_{name}"] = mcnemar_test(correct[pc], correct[tc])
    _attach_e3(out)
    return out


def _paired_component_cis(correct: dict[str, list[bool]], n_boot: int, seed: int, alpha: float = 0.05,
                          chunk: int = 1000) -> dict:
    """Percentile 95 % CI, PAIRED bootstrap (same question resamples for all conditions), of
    Acc(cond) per condition and of Acc(S)/Acc(C0). Authors' request (15/09/2026): the components next to Δ_nec
    in the HEAL table. Vectorized in blocks so as not to run out of memory (n_boot x n)."""
    conds = list(correct)
    if not conds:
        return {}
    n = len(correct[conds[0]])
    mats = {c: np.asarray(correct[c], dtype=np.float32) for c in conds}
    rng = np.random.RandomState(seed)
    accs = {c: np.empty(n_boot, dtype=np.float32) for c in conds}
    for start in range(0, n_boot, chunk):
        b = min(chunk, n_boot - start)
        idx = rng.randint(0, n, size=(b, n))
        for c in conds:
            accs[c][start:start + b] = mats[c][idx].mean(axis=1)
    lo, hi = 100 * alpha / 2, 100 * (1 - alpha / 2)
    out = {"acc_ci": {c: [float(np.percentile(a, lo)), float(np.percentile(a, hi))] for c, a in accs.items()}}
    if "C0" in accs and "S" in accs:
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.where(accs["C0"] > 0, accs["S"] / accs["C0"], np.nan)
        ratio = ratio[~np.isnan(ratio)]
        out["sufficiency_ci"] = [float(np.percentile(ratio, lo)), float(np.percentile(ratio, hi))] if ratio.size else None
    return out


def _attach_e3(stats: dict) -> None:
    """E3 criterion (pre-registration §7): 'necessary' only if the 95 % CI of Δ_nec excludes zero (above)
    under black AND under at least one plausible fill on the whole set (blur 10 % of the width
    or mean color of the region itself). Effect only under black = 'sensitivity to solid fill'.
    With no plausible fill loaded, `necessary` is None (not evaluable)."""
    if "delta_nec_ci" not in stats:
        return
    black = stats["delta_nec_ci"][0] > 0
    plausible = {name: stats[f"delta_nec_{name}_ci"][0] > 0 for name in E3_PLAUSIBLE if f"delta_nec_{name}_ci" in stats}
    stats["e3"] = {"black_excludes_zero": black, "plausible_excludes_zero": plausible,
                   "necessary": (black and any(plausible.values())) if plausible else None,
                   "solid_only": bool(plausible) and black and not any(plausible.values())}


def _attach_margin(stats: dict, m0: dict | None) -> None:
    """Headroom = Acc(C0) - Acc(M0_type); nΔ_nec = Δ_nec / headroom; headroom <= 0 -> 'no headroom' and
    nΔ_nec empty (never 0), pre-registered rule (§4 of the pre-registration)."""
    if not m0 or "acc" not in stats or "C0" not in stats["acc"] or "delta_nec" not in stats:
        return
    stats["acc_m0"] = m0["accuracy"]
    stats["n_m0"] = m0["n"]
    stats["ceiling"] = stats["acc"]["C0"] - m0["accuracy"]
    stats["no_margin"] = stats["ceiling"] <= 0
    stats["ndelta_nec"] = None if stats["no_margin"] else stats["delta_nec"] / stats["ceiling"]


def compute_necessity(inventory: str, preds: dict[str, str], n_boot: int = 10000, seed: int = 42,
                      paired_qids: list[int] | None = None, c0_reference: str | None = None,
                      m0_by_type: str | None = None) -> dict:
    inv = [q for q in json.loads(Path(inventory).read_text())["questions"] if q["evaluable"]]
    evaluable = [q["qid"] for q in inv]
    loaded = {c: _load_preds(p) for c, p in preds.items()}
    missing = {c: sum(q not in d for q in evaluable) for c, d in loaded.items()}
    core = {c: d for c, d in loaded.items() if c not in DOSE_ONLY}
    aligned = [q for q in evaluable if all(q in d for d in core.values())]
    meta = {q["qid"]: q for q in inv}
    groups: dict[str, dict[str, list[int]]] = {"by_class": collections.defaultdict(list),
                                               "by_template": collections.defaultdict(list),
                                               "by_xray": collections.defaultdict(list)}
    for q in aligned:
        m = meta[q]
        groups["by_class"][m["question_class"]].append(q)
        groups["by_template"][m["question"]].append(q)
        groups["by_xray"]["xray" if m.get("xray") else "no_xray"].append(q)
        if m.get("anatomy"):   # HEAL (E5): group by target anatomy; absent in Kvasir and SLAKE
            groups.setdefault("by_anatomy", collections.defaultdict(list))[m["anatomy"]].append(q)
    out = {"inventory": inventory, "predictions": preds, "n_evaluable": len(evaluable), "n_aligned": len(aligned),
           "missing_by_condition": {c: n for c, n in missing.items() if n}, "n_boot": n_boot, "seed": seed,
           "overall": _group_stats(aligned, core, n_boot, seed)}
    for g, d in groups.items():
        out[g] = {k: _group_stats(v, core, n_boot, seed) for k, v in sorted(d.items())}
    if m0_by_type:
        m0 = json.loads(Path(m0_by_type).read_text())
        out["m0_by_type"] = m0_by_type
        for k, st in out["by_template"].items():
            _attach_margin(st, m0["by_template"]["evaluable"].get(k))
        for k, st in out["by_class"].items():
            _attach_margin(st, m0["by_class"]["evaluable"].get(k))
        for k, st in out.get("by_anatomy", {}).items():
            _attach_margin(st, (m0.get("by_anatomy") or {}).get(k))
    main_p = {k: v["mcnemar"]["p_value"] for k, v in out["by_class"].items()
              if k in MAIN_TABLE_CLASSES and "mcnemar" in v}
    for k, p in holm(main_p).items():
        out["by_class"][k]["p_holm"] = p
    if paired_qids is not None:
        pq = [q for q in aligned if q in set(paired_qids)]
        dose = {"n_paired": len(pq), "by_class": {}}
        for cls, qids in groups["by_class"].items():
            sub = [q for q in qids if q in set(pq)]
            levels = {}
            for lvl, (t, p) in DOSE_LEVELS.items():
                if t in loaded and p in loaded:
                    sub_l = [q for q in sub if q in loaded[t] and q in loaded[p]]
                    st = _group_stats(sub_l, {"C0": loaded["C0"], "T": loaded[t], "P": loaded[p]} if "C0" in loaded
                                      else {"T": loaded[t], "P": loaded[p]}, n_boot, seed)
                    levels[lvl] = {k: st[k] for k in ("n", "delta_nec", "delta_nec_ci", "mcnemar") if k in st}
            dose["by_class"][cls] = levels
        out["dose"] = dose
    if c0_reference and "C0" in preds:
        out["c0_reference"] = {"reference": c0_reference,
                               **compare_predictions(Path(c0_reference), Path(preds["C0"]), qids=aligned)}
    return out


def _fmt(x, pct=True):
    if x is None:
        return "—"
    return f"{100 * x:+.1f}" if pct else f"{x:.3f}"


def _blur_col(s: dict) -> str:
    if "delta_nec_blur" not in s:
        return " — |"
    ci = s["delta_nec_blur_ci"]
    return f" {100 * s['delta_nec_blur']:+.1f} [{100 * ci[0]:+.1f}, {100 * ci[1]:+.1f}] p={s['mcnemar_blur']['p_value']:.2g} |"


def _margin_cols(s: dict) -> str:
    if "ceiling" not in s:
        return " — | — | — |"
    note = "" if s.get("n_m0") == s.get("n") else f" (M0 sobre n={s.get('n_m0')})"
    if s["no_margin"]:
        return f" {100 * s['acc_m0']:.1f}{note} | {100 * s['ceiling']:+.1f} | sem margem |"
    return f" {100 * s['acc_m0']:.1f}{note} | {100 * s['ceiling']:+.1f} | {s['ndelta_nec']:+.2f} |"


def render_markdown(out: dict, template_table: bool = True) -> str:
    conds = [c for c in out["predictions"] if c not in DOSE_ONLY]   # dose only in its own section
    L = [f"# Necessidade e suficiência — {Path(out['predictions'].get('T', '')).stem or 'análise'}", "",
         f"Perguntas avaliáveis: {out['n_evaluable']}; alinhadas em todas as condições: {out['n_aligned']}"
         + (f"; faltantes: {out['missing_by_condition']}" if out["missing_by_condition"] else "") + ".", ""]
    if "c0_reference" in out:
        r = out["c0_reference"]
        L += [f"Reprodução da C0 contra `{r['reference']}` nos {r['n_common']} qids avaliáveis: "
              f"{r['n_disagree_pred']} predições diferentes ({100 * r['disagree_pred_rate']:.2f} %), "
              f"Δ acurácia {r['delta_pp']:+.2f} pp.", ""]
    if "m0_by_type" in out:
        L += [f"Margem: Acc(M0_tipo) de `{out['m0_by_type']}`; teto = Acc(C0) − Acc(M0_tipo); nΔ_nec = Δ_nec / teto; "
              "teto ≤ 0 → \"sem margem\" e nΔ_nec vazio. Bruta e normalizada lado a lado.", ""]
    head = ("| grupo | n | " + " | ".join(f"Acc({c})" for c in conds)
            + " | Δ_nec (pp) | IC 95 % | McNemar p | p Holm | g | sufic. | M0_tipo | teto (pp) | nΔ_nec | Δ_nec blur [IC] p |")
    L += [head, "|" + "---|" * (head.count("|") - 1)]

    def row(name, s):
        if s.get("n", 0) == 0:
            return f"| {name} | 0 |" + " — |" * (len(conds) + 10)
        ci = s.get("delta_nec_ci"); mc = s.get("mcnemar", {})
        return (f"| {name} | {s['n']} | " + " | ".join(f"{100 * s['acc'][c]:.1f}" for c in conds)
                + f" | {_fmt(s.get('delta_nec'))} | " + (f"[{100 * ci[0]:+.1f}, {100 * ci[1]:+.1f}]" if ci else "—")
                + f" | {mc.get('p_value', float('nan')):.3g} | " + (f"{s['p_holm']:.3g}" if "p_holm" in s else "—")
                + f" | {_fmt(mc.get('cohens_g'), pct=False)} | {_fmt(s.get('sufficiency'), pct=False)} |" + _margin_cols(s) + _blur_col(s))
    L.append(row("todas", out["overall"]))
    for k, s in out["by_class"].items():
        L.append(row(k, s))
    for k, s in out["by_xray"].items():
        L.append(row(f"marca: {k}", s))
    if template_table:
        L += ["", "| template | n | Acc(C0) | Δ_nec (pp) | IC 95 % | McNemar p | VDD(T) | VDD(P) | sufic. | M0_tipo | teto (pp) | nΔ_nec | Δ_nec blur [IC] p |",
              "|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---|"]
        for k, s in sorted(out["by_template"].items(), key=lambda kv: -kv[1].get("n", 0)):
            ci = s.get("delta_nec_ci"); mc = s.get("mcnemar", {}); v = s.get("vdd", {})
            L.append(f"| {k} | {s['n']} | {100 * s['acc'].get('C0', float('nan')):.1f} | {_fmt(s.get('delta_nec'))} | "
                     + (f"[{100 * ci[0]:+.1f}, {100 * ci[1]:+.1f}]" if ci else "—")
                     + f" | {mc.get('p_value', float('nan')):.3g} | {_fmt(v.get('T'))} | {_fmt(v.get('P'))} | {_fmt(s.get('sufficiency'), pct=False)} |"
                     + _margin_cols(s) + _blur_col(s))
    else:
        L += ["", "(tabela por template omitida do relatório; está no JSON)"]
    if "dose" in out:
        L += ["", f"## Dose (subconjunto pareado, {out['dose']['n_paired']} perguntas)", "",
              "| classe | nível | n | Δ_nec (pp) | IC 95 % | McNemar p |", "|---|---|---:|---:|---|---:|"]
        for cls, levels in out["dose"]["by_class"].items():
            for lvl, s in levels.items():
                ci = s.get("delta_nec_ci")
                L.append(f"| {cls} | {lvl}× | {s['n']} | {_fmt(s.get('delta_nec'))} | "
                         + (f"[{100 * ci[0]:+.1f}, {100 * ci[1]:+.1f}]" if ci else "—") + f" | {s.get('mcnemar', {}).get('p_value', float('nan')):.3g} |")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--pred", action="append", required=True, help="COND=caminho (repetir)")
    ap.add_argument("--manifest", help="manifesto do gerador: os qids das unidades válidas nos três níveis definem a dose")
    ap.add_argument("--c0-reference", help="cache C0 de referência (P0) para a checagem de reprodução")
    ap.add_argument("--m0", help="m0_by_type_*.json: acrescenta Acc(M0_tipo), teto e nΔ_nec")
    ap.add_argument("--no-template-table", action="store_true", help="markdown só no nível de classe (SLAKE)")
    ap.add_argument("--n-boot", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--output-json", required=True)
    ap.add_argument("--output-md")
    a = ap.parse_args(argv)
    preds = dict(kv.split("=", 1) for kv in a.pred)
    paired = None
    if a.manifest:
        man = json.loads(Path(a.manifest).read_text())
        paired = [q for u in man["units"] if all(u["placebo_method_by_factor"].get(k) is not None for k in ("1.5", "2"))
                  for q in u["qids"]]
    out = compute_necessity(a.inventory, preds, a.n_boot, a.seed, paired, a.c0_reference, a.m0)
    Path(a.output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(a.output_json).write_text(json.dumps(out, indent=1) + "\n")
    md = render_markdown(out, template_table=not a.no_template_table)
    if a.output_md:
        Path(a.output_md).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output_md).write_text(md)
    print(md)


if __name__ == "__main__":
    main()
