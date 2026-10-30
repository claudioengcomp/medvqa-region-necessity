"""Per-template diagnostics over the cache (analysis request of 14/09/2026, items 4 and 5).

- diag_procedure: "What type of procedure is the image taken from?" -- confusion
  matrix colonoscopy x gastroscopy under C0, T and P (a prediction outside the two
  labels goes to "other").
- diag_size: "What is the size of the polyp?" -- item-by-item list of those that are
  correct under P and wrong under C0 (and the reverse), with the given answer and the reference.
  No interpretation beyond consistent/not across seeds (done in the consolidator).
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

from med_vlm.metrics.process_text import normalize_text

Q_PROCEDURE = "What type of procedure is the image taken from?"
Q_SIZE = "What is the size of the polyp?"


def _load(inventory: str, preds: dict[str, str], template: str):
    inv = [q for q in json.loads(Path(inventory).read_text())["questions"] if q["evaluable"] and q["question"] == template]
    loaded = {c: {r["qid"]: r for r in json.loads(Path(p).read_text())["predictions"]} for c, p in preds.items()}
    qids = [q["qid"] for q in inv if all(q["qid"] in d for d in loaded.values())]
    meta = {q["qid"]: q for q in inv}
    return qids, meta, loaded


def diag_procedure(inventory: str, preds: dict[str, str]) -> dict:
    qids, meta, loaded = _load(inventory, preds, Q_PROCEDURE)
    labels = sorted({normalize_text(loaded[next(iter(loaded))][q]["gold"]) for q in qids})
    conf = {}
    acc = {}
    for c, d in loaded.items():
        m = {g: {**{l: 0 for l in labels}, "other": 0} for g in labels}
        for q in qids:
            g = normalize_text(d[q]["gold"]); p = normalize_text(d[q]["predicted"])
            m[g][p if p in labels else "other"] += 1
        conf[c] = m
        acc[c] = sum(bool(d[q]["correct"]) for q in qids) / len(qids) if qids else None
    return {"template": Q_PROCEDURE, "n": len(qids), "labels": labels, "confusion": conf, "acc": acc, "predictions": preds}


def render_procedure(out: dict) -> str:
    L = [f"# Diagnóstico — {out['template']} ({Path(out['predictions']['T']).stem})", "",
         f"n = {out['n']} perguntas avaliáveis. Linhas = gold; colunas = predição (`other` = fora dos dois rótulos).", ""]
    for c, m in out["confusion"].items():
        L += [f"**{c}** — acurácia {100 * out['acc'][c]:.1f} %", "", "| gold \\ pred | " + " | ".join(out["labels"] + ["other"]) + " |",
              "|---|" + "---:|" * (len(out["labels"]) + 1)]
        L += [f"| {g} | " + " | ".join(str(m[g][k]) for k in out["labels"] + ["other"]) + " |" for g in out["labels"]]
        L.append("")
    return "\n".join(L) + "\n"


def diag_size(inventory: str, preds: dict[str, str]) -> dict:
    qids, meta, loaded = _load(inventory, preds, Q_SIZE)
    def item(q):
        return {"qid": q, "image_id": meta[q]["image_id"], "gold": loaded["C0"][q]["gold"],
                **{f"pred_{c}": loaded[c][q]["predicted"] for c in ("C0", "T", "P") if c in loaded}}
    right_p_wrong_c0 = [item(q) for q in qids if loaded["P"][q]["correct"] and not loaded["C0"][q]["correct"]]
    wrong_p_right_c0 = [item(q) for q in qids if loaded["C0"][q]["correct"] and not loaded["P"][q]["correct"]]
    acc = {c: sum(bool(d[q]["correct"]) for q in qids) / len(qids) if qids else None for c, d in loaded.items()}
    return {"template": Q_SIZE, "n": len(qids), "acc": acc, "predictions": preds,
            "right_under_P_wrong_under_C0": right_p_wrong_c0, "wrong_under_P_right_under_C0": wrong_p_right_c0}


def render_size(out: dict) -> str:
    L = [f"# Diagnóstico — {out['template']} ({Path(out['predictions']['P']).stem})", "",
         f"n = {out['n']}; acurácia: " + ", ".join(f"{c} {100 * a:.1f} %" for c, a in out["acc"].items()) + ".", ""]
    for key, title in (("right_under_P_wrong_under_C0", "Acerta sob P e erra sob C0"), ("wrong_under_P_right_under_C0", "Erra sob P e acerta sob C0")):
        rows = out[key]
        L += [f"## {title} ({len(rows)})", "", "| qid | imagem | gold | pred C0 | pred T | pred P |", "|---|---|---|---|---|---|"]
        L += [f"| {r['qid']} | {r['image_id']} | {r['gold']} | {r.get('pred_C0', '—')} | {r.get('pred_T', '—')} | {r.get('pred_P', '—')} |" for r in rows]
        L.append("")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--which", choices=["procedure", "size"], required=True)
    ap.add_argument("--inventory", required=True); ap.add_argument("--pred", action="append", required=True)
    ap.add_argument("--output-json", required=True); ap.add_argument("--output-md")
    a = ap.parse_args(argv)
    preds = dict(kv.split("=", 1) for kv in a.pred)
    out, md = (diag_procedure(a.inventory, preds), None) if a.which == "procedure" else (diag_size(a.inventory, preds), None)
    md = render_procedure(out) if a.which == "procedure" else render_size(out)
    Path(a.output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(a.output_json).write_text(json.dumps(out, indent=1) + "\n")
    if a.output_md:
        Path(a.output_md).write_text(md)
    print(md)


if __name__ == "__main__":
    main()
