"""Counterfactual consistency under occlusion (plan v2 §3; analysis request of 14/09/2026, item 2).

If the target is entirely covered in T, the counterfactually correct answer
changes: there is no polyp to count, there is no instrument, "all polyps have been
removed". The metric is the fraction of answers under T that match this reference,
against the same fraction under P (control occlusion: same shape and area, different position), paired by
question: paired bootstrap (10,000) for the difference and McNemar T vs P.
Scoring rule: answer_matches(normalize_text(...)) from med_vlm, the same one used for the existing prediction caches.

References per template (Kvasir), fixed here:
    "How many polyps are in the image?"                                  -> "0"    (target = polyp)
    "Are there any abnormalities in the image? Check all that are present." -> "none" (target = polyp)
    "Have all polyps been removed?"                                      -> "yes"  (target = polyp)
    "How many instrumnets are in the image?"                             -> "0"    (target = instrument)
    "Are there any instruments in the image? Check all that are present." -> "none" (target = instrument)
"none" is the absence string of the training vocabulary (kvasir_answer_vocab_clean.json);
in the clean test set it is never gold for the abnormalities template (every evaluable image
has a polyp), which is recorded in the report.

Inclusion: an item enters only if the whole mask of the required type is covered in T. In
Kvasir the generator covers the UNION of the masks of the image's target type, so the
condition is equivalent to the image's `target_kind` == type required by the template; polyp
items in an image whose target is an instrument (and vice versa) are excluded and counted.
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

from harness.stats.compute_ldv import bootstrap_paired_diff_ci, mcnemar_test
from med_vlm.metrics.process_text import answer_matches, normalize_text

CF_REFERENCE: dict[str, tuple[str, str]] = {
    "How many polyps are in the image?": ("0", "polyp"),
    "Are there any abnormalities in the image? Check all that are present.": ("none", "polyp"),
    "Have all polyps been removed?": ("yes", "polyp"),
    "How many instrumnets are in the image?": ("0", "instrument"),
    "Are there any instruments in the image? Check all that are present.": ("none", "instrument"),
}


def _hit(pred: str, ref: str) -> bool:
    return answer_matches(normalize_text(pred), [normalize_text(ref)])


def _stats(items: list[dict], has_c0: bool, n_boot: int, seed: int) -> dict:
    n = len(items)
    if n == 0:
        return {"n": 0}
    t = [i["hit_T"] for i in items]; p = [i["hit_P"] for i in items]
    out = {"n": n, "frac_T": sum(t) / n, "frac_P": sum(p) / n, "diff": (sum(t) - sum(p)) / n,
           "diff_ci": list(bootstrap_paired_diff_ci(t, p, n_boot=n_boot, seed=seed)), "mcnemar": mcnemar_test(t, p)}
    if has_c0:
        out["frac_C0"] = sum(i["hit_C0"] for i in items) / n
    return out


def cf_consistency(inventory: str, preds: dict[str, str], n_boot: int = 10000, seed: int = 42) -> dict:
    inv = json.loads(Path(inventory).read_text())["questions"]
    loaded = {c: {r["qid"]: r for r in json.loads(Path(p).read_text())["predictions"]} for c, p in preds.items()}
    if "T" not in loaded or "P" not in loaded:
        raise ValueError("cf_consistency exige as condicoes T e P")
    has_c0 = "C0" in loaded
    items, excluded = [], collections.Counter()
    for q in inv:
        ref = CF_REFERENCE.get(q["question"])
        if ref is None:
            excluded["template_without_reference"] += 1
            continue
        if not q["evaluable"]:
            excluded["not_evaluable"] += 1
            continue
        if q.get("target_kind") != ref[1]:
            excluded["target_not_fully_covered"] += 1
            continue
        if q["qid"] not in loaded["T"] or q["qid"] not in loaded["P"] or (has_c0 and q["qid"] not in loaded["C0"]):
            excluded["missing_prediction"] += 1
            continue
        it = {"qid": q["qid"], "question": q["question"], "question_class": q["question_class"], "reference": ref[0],
              "hit_T": _hit(loaded["T"][q["qid"]]["predicted"], ref[0]), "hit_P": _hit(loaded["P"][q["qid"]]["predicted"], ref[0])}
        if has_c0:
            it["hit_C0"] = _hit(loaded["C0"][q["qid"]]["predicted"], ref[0])
        items.append(it)
    by_t = collections.defaultdict(list); by_c = collections.defaultdict(list)
    for it in items:
        by_t[it["question"]].append(it); by_c[it["question_class"]].append(it)
    return {"inventory": inventory, "predictions": preds, "reference": {k: {"answer": v[0], "target": v[1]} for k, v in CF_REFERENCE.items()},
            "n_included": len(items), "excluded": dict(excluded), "n_boot": n_boot, "seed": seed,
            "pooled": _stats(items, has_c0, n_boot, seed),
            "by_template": {k: _stats(v, has_c0, n_boot, seed) for k, v in sorted(by_t.items())},
            "by_class": {k: _stats(v, has_c0, n_boot, seed) for k, v in sorted(by_c.items())}}


def render_markdown(out: dict) -> str:
    L = [f"# Consistência contrafactual sob oclusão — {Path(out['predictions']['T']).stem}", "",
         "Referência contrafactual por template (resposta correta quando o alvo está inteiramente coberto):", "",
         "| template | referência | alvo |", "|---|---|---|"]
    L += [f"| {k} | `{v['answer']}` | {v['target']} |" for k, v in out["reference"].items()]
    L += ["", "`none` é a string de ausência do vocabulário de treino; no teste limpo ela nunca é gold para o template de "
          "anormalidades (todas as imagens avaliáveis têm pólipo).", "",
          f"Itens incluídos: {out['n_included']}; excluídos: " + (", ".join(f"{k}={v}" for k, v in out["excluded"].items()) or "nenhum") + ".", "",
          "Métrica: fração das respostas que acertam a referência sob T, sob P (e sob C0), pareada; diferença T − P com IC "
          f"bootstrap ({out['n_boot']}) e McNemar T vs P (b = acerta em T e erra em P).", "",
          "| grupo | n | sob C0 | sob T | sob P | T − P (pp) | IC 95 % | McNemar p | b / c |", "|---|---:|---:|---:|---:|---:|---|---:|---|"]
    def row(name, s):
        if s.get("n", 0) == 0:
            return f"| {name} | 0 | — | — | — | — | — | — | — |"
        ci = s["diff_ci"]; mc = s["mcnemar"]
        c0 = f"{100 * s['frac_C0']:.1f}" if "frac_C0" in s else "—"
        return (f"| {name} | {s['n']} | {c0} | {100 * s['frac_T']:.1f} | {100 * s['frac_P']:.1f} | {100 * s['diff']:+.1f} | "
                f"[{100 * ci[0]:+.1f}, {100 * ci[1]:+.1f}] | {mc['p_value']:.3g} | {mc['b']} / {mc['c']} |")
    L.append(row("todas", out["pooled"]))
    L += [row(k, s) for k, s in out["by_class"].items()]
    L += [row(k, s) for k, s in out["by_template"].items()]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inventory", required=True); ap.add_argument("--pred", action="append", required=True)
    ap.add_argument("--n-boot", type=int, default=10000); ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--output-json", required=True); ap.add_argument("--output-md")
    a = ap.parse_args(argv)
    out = cf_consistency(a.inventory, dict(kv.split("=", 1) for kv in a.pred), a.n_boot, a.seed)
    Path(a.output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(a.output_json).write_text(json.dumps(out, indent=1) + "\n")
    md = render_markdown(out)
    if a.output_md:
        Path(a.output_md).write_text(md)
    print(md)


if __name__ == "__main__":
    main()
