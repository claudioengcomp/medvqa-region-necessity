"""Distribution of the answers under C0, T and P in the polyp count and polyp presence
templates (request of 14/09/2026, round 2, item 1): tests the hypothesis that the black shape
of the control occlusion/target is read as a lesion (e.g. under T does the count drop to "0"? under P
does it stay "1"?). Distributions only; no interpretation beyond the table.
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

from med_vlm.metrics.process_text import normalize_text

DEFAULT_TEMPLATES = ["How many polyps are in the image?", "Are there any abnormalities in the image? Check all that are present.",
                     "How many findings are present?", "Does this image contain any finding?", "Have all polyps been removed?",
                     "How many instrumnets are in the image?", "Are there any instruments in the image? Check all that are present."]


def diag_answers(inventory: str, preds: dict[str, str], templates=None) -> dict:
    templates = templates or DEFAULT_TEMPLATES
    inv = [q for q in json.loads(Path(inventory).read_text())["questions"] if q["evaluable"] and q["question"] in templates]
    loaded = {c: {r["qid"]: r for r in json.loads(Path(p).read_text())["predictions"]} for c, p in preds.items()}
    out = {"predictions": preds, "templates": {}}
    for t in templates:
        qids = [q["qid"] for q in inv if q["question"] == t and all(q["qid"] in d for d in loaded.values())]
        if not qids:
            continue
        ref = loaded[next(iter(loaded))]
        out["templates"][t] = {"n": len(qids), "gold": dict(collections.Counter(normalize_text(ref[q]["gold"]) for q in qids).most_common()),
                               "answers": {c: dict(collections.Counter(normalize_text(d[q]["predicted"]) for q in qids).most_common()) for c, d in loaded.items()}}
    return out


def render(out: dict) -> str:
    L = [f"# Distribuição das respostas sob cada condição ({Path(out['predictions']['T']).stem})", "",
         "Respostas normalizadas pela régua do P0; até 8 mais frequentes por condição, o resto em `outras`.", ""]
    for t, d in out["templates"].items():
        keys = []
        for c in ("gold",) + tuple(d["answers"]):
            src = d["gold"] if c == "gold" else d["answers"][c]
            keys += [k for k, _ in sorted(src.items(), key=lambda kv: -kv[1])[:8]]
        keys = list(dict.fromkeys(keys))
        L += [f"## {t} (n = {d['n']})", "", "| condição | " + " | ".join(f"`{k}`" for k in keys) + " | outras |", "|---|" + "---:|" * (len(keys) + 1)]
        for c in ("gold",) + tuple(d["answers"]):
            src = d["gold"] if c == "gold" else d["answers"][c]
            L.append(f"| {c} | " + " | ".join(str(src.get(k, 0)) for k in keys) + f" | {sum(v for k, v in src.items() if k not in keys)} |")
        L.append("")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inventory", required=True); ap.add_argument("--pred", action="append", required=True)
    ap.add_argument("--output-json", required=True); ap.add_argument("--output-md")
    a = ap.parse_args(argv)
    out = diag_answers(a.inventory, dict(kv.split("=", 1) for kv in a.pred))
    Path(a.output_json).write_text(json.dumps(out, indent=1) + "\n")
    md = render(out)
    if a.output_md:
        Path(a.output_md).write_text(md)
    print(md)


if __name__ == "__main__":
    main()
