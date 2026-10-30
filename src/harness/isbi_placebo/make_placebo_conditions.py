"""F2 -- materializes the paper's conditions from the F1 inventory.

Reads the original arrow and the inventory (`inventory_kvasir.py` / `inventory_slake.py`),
rebuilds the target and the control occlusion of each evaluable unit (control occlusion position = method
recorded in the inventory), and writes one arrow per condition with ONLY the evaluable
questions, at the original resolution: C0 with the original bytes of the arrow, the others
as lossless PNG from the decoded pixels (amendment of 14/09/2026 to
pre-registration §3.1; see conditions.py). Writes a manifest with the sha256 of each arrow (format accepted by
`harness/prepro/verify_arrow_integrity.py`) and an HTML gallery for the authors' visual
review (Gate P1): N units with original, target, control occlusion, T, P,
S, and M control occlusions with both contours.

Unit = (image, target). In Kvasir there is one target per image (polyp or
instrument); in SLAKE one image may have several targets (liver, cancer...), and
each becomes one arrow row with the questions that depend on it.

Usage (Kvasir):
    python -m harness.isbi_placebo.make_placebo_conditions --dataset kvasir         --arrow .../vqa_kvasir_test_clean.arrow         --inventory results/isbi_placebo/inventory_kvasir_test_clean.json         --map data/isbi_placebo/kvasir_vqa_to_seg_instrument_map.json         --seg-dir .../Kvasir-SEG --instrument-dir .../kvasir-instrument         --out-dir data/isbi_placebo --conditions T,P,S         --manifest results/isbi_placebo/manifest_kvasir.json         --gallery docs/isbi/placebo/gallery_kvasir.html --seed 20260913
"""
from __future__ import annotations

import argparse
import base64
import collections
import hashlib
import io
import json
import os
import random
import re
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from harness.interventions.arrow_io import read_arrow, write_arrow
from harness.isbi_placebo.conditions import CONDITIONS, apply_placement, encode_png, make_condition_image
from harness.isbi_placebo.masks import dilate_to_area
from harness.isbi_placebo.inventory_kvasir import load_target_mask
from harness.isbi_placebo.inventory_slake import entity_regions, read_legend


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _units_kvasir(df: pd.DataFrame, inv: dict, src: dict) -> list[dict]:
    mapping = json.loads(Path(src["map"]).read_text())
    images = {r["image_id"]: r for r in inv["images"]}
    qids_by_img = collections.defaultdict(list)
    for q in inv["questions"]:
        if q["evaluable"]:
            qids_by_img[q["image_id"]].append(q["qid"])
    units = []
    for idx, row in enumerate(df.itertuples(index=False)):
        image_id = row.image_id.split("/", 1)[1] if "/" in row.image_id else row.image_id
        rec = images.get(image_id)
        if not rec or rec["exclusion"] is not None or not qids_by_img.get(image_id):
            continue
        target, kind = load_target_mask(image_id, mapping, src["seg_dir"], src["instrument_dir"])
        units.append({"row": idx, "image_id": image_id, "target_key": kind, "target": target,
                      "placebo_method": rec["placebo_method"], "qids": sorted(qids_by_img[image_id]),
                      "placebo_method_by_factor": rec.get("placebo_method_by_factor", {}),
                      "dose_reason_by_factor": rec.get("dose_reason_by_factor", {}), "xray": False})
    return units


def _units_slake(df: pd.DataFrame, inv: dict, src: dict) -> list[dict]:
    legend = read_legend(os.path.join(src["slake_root"], "mask.txt"))
    groups = collections.defaultdict(list)
    method, qrec = {}, {}
    for q in inv["questions"]:
        if q["evaluable"]:
            key = (q["image_id"], tuple(q["target_entities"]))
            groups[key].append(q["qid"])
            method[key] = q["placebo_method"]
            qrec[key] = q
    units = []
    for idx, row in enumerate(df.itertuples(index=False)):
        xm = re.search(r"(xmlab\d+)", row.image_id).group(1)
        keys = [k for k in groups if k[0] == xm]
        if not keys:
            continue
        regions = entity_regions(os.path.join(src["slake_root"], "imgs", xm), legend)
        for key in sorted(keys, key=lambda k: k[1]):
            target = np.logical_or.reduce([regions[n]["mask"] for n in key[1]])
            units.append({"row": idx, "image_id": xm, "target_key": "+".join(key[1]), "target": target,
                          "placebo_method": method[key], "qids": sorted(groups[key]),
                          "placebo_method_by_factor": qrec[key].get("placebo_method_by_factor", {}),
                          "dose_reason_by_factor": qrec[key].get("dose_reason_by_factor", {}),
                          "xray": bool(qrec[key].get("xray", False))})
    return units


def _subset_row(row, qids: list[str], image_bytes: bytes) -> dict:
    keep = [i for i, q in enumerate(row.question_id) if q in set(qids)]
    return {"image": image_bytes, "questions": [row.questions[i] for i in keep],
            "answers": [row.answers[i] for i in keep], "answer_labels": [row.answer_labels[i] for i in keep],
            "answer_scores": [row.answer_scores[i] for i in keep], "image_id": row.image_id,
            "question_id": [row.question_id[i] for i in keep], "answer_type": [row.answer_type[i] for i in keep],
            "split": row.split}


def _thumb(arr: np.ndarray, max_w: int = 256) -> str:
    im = Image.fromarray(np.asarray(arr, np.uint8))
    if im.width > max_w:
        im = im.resize((max_w, int(im.height * max_w / im.width)))
    buf = io.BytesIO(); im.save(buf, format="JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def _overlay(img: np.ndarray, target: np.ndarray, placebo: np.ndarray | None) -> np.ndarray:
    out = img.astype(np.float32)
    out[target] = 0.5 * out[target] + 0.5 * np.array([255, 0, 0])
    if placebo is not None:
        out[placebo] = 0.5 * out[placebo] + 0.5 * np.array([0, 90, 255])
    return np.clip(out, 0, 255).astype(np.uint8)


def _gallery_html(dataset: str, gallery: list[dict], review: list[dict]) -> str:
    h = [f"<!doctype html><meta charset='utf-8'><title>Galeria F2 — {dataset}</title>",
         "<style>body{font-family:sans-serif} table{border-collapse:collapse} td{padding:4px;vertical-align:top;font-size:12px}"
         " img{display:block} .cap{color:#555}</style>",
         f"<h1>Galeria F2 — {dataset}</h1>",
         "<p>Vermelho = alvo; azul = placebo. Cada linha é uma unidade (imagem, alvo). Revisar: alinhamento da máscara com a "
         "lesão/órgão, placebo sem tocar o alvo, placebo dentro do campo de visão.</p>",
         "<h2>Amostra de unidades: original, alvo+placebo, T, P, S</h2><table>"]
    for g in gallery:
        h.append("<tr>" + "".join(f"<td><img src='{src}'><div class='cap'>{cap}</div></td>" for cap, src in g["panels"])
                 + f"<td><b>{g['image_id']}</b><br>alvo: {g['target_key']}<br>placebo: {g['placebo_method']}"
                 f"<br>perguntas: {len(g['qids'])}<br>{'<br>'.join(g['questions'][:4])}</td></tr>")
    h.append("</table><h2 id='review'>Review de placebos: alvo (vermelho) e placebo (azul)</h2><table>")
    for i in range(0, len(review), 4):
        h.append("<tr>" + "".join(f"<td><img src='{r['src']}'><div class='cap'>{r['image_id']} · {r['target_key']} · "
                                  f"{r['placebo_method']}</div></td>" for r in review[i:i + 4]) + "</tr>")
    h.append("</table>")
    return "\n".join(h)


def generate(dataset: str, arrow: str, inventory: str, out_dir: str, conditions: list[str], mask_sources: dict,
             manifest_path: str, gallery_path: str | None, gallery_n: int, review_n: int, seed: int) -> dict:
    for c in conditions:
        if c not in CONDITIONS:
            raise ValueError(f"condicao desconhecida: {c}")
    inv = json.loads(Path(inventory).read_text())
    df = read_arrow(arrow)
    units = _units_kvasir(df, inv, mask_sources) if dataset == "kvasir" else _units_slake(df, inv, mask_sources)
    os.makedirs(out_dir, exist_ok=True)
    rng = random.Random(seed)
    gallery_idx = set(rng.sample(range(len(units)), min(gallery_n, len(units))))
    review_idx = set(rng.sample(range(len(units)), min(review_n, len(units))))
    rows_by_cond: dict[str, list[dict]] = {c: [] for c in conditions}
    overlap_flags = collections.Counter()
    unit_records, gallery, review = [], [], []
    for ui, u in enumerate(units):
        row = df.iloc[u["row"]]
        img = np.array(Image.open(io.BytesIO(row.image)).convert("RGB"))
        placebo = apply_placement(u["target"], u["placebo_method"])
        placebo_by_factor = {float(k): apply_placement(dilate_to_area(u["target"], float(k)), m)
                             for k, m in u["placebo_method_by_factor"].items() if m is not None}
        dropped = {}
        info_by_cond = {}
        panels = []
        for c in conditions:
            fac = re.match(r"^P(1\.5|2)$", c)
            if fac and float(fac.group(1)) not in placebo_by_factor:
                dropped[c] = u["dose_reason_by_factor"].get(fac.group(1), "no_replaced_placebo")
                continue
            out_img, info = make_condition_image(img, u["target"], placebo, c, placebo_by_factor=placebo_by_factor)
            info_by_cond[c] = {"region_px": info["region_px"], "overlaps_target": info["overlaps_target"]}
            if info["overlaps_target"]:
                overlap_flags[c] += 1
            rows_by_cond[c].append(_subset_row(row, u["qids"], row.image if c == "C0" else encode_png(out_img)))
            if ui in gallery_idx and c in ("T", "P", "S"):
                panels.append((c, _thumb(out_img)))
        unit_records.append({"image_id": u["image_id"], "target_key": u["target_key"], "row": u["row"],
                             "placebo_method": u["placebo_method"], "qids": u["qids"], "xray": u["xray"],
                             "placebo_method_by_factor": u["placebo_method_by_factor"], "dropped": dropped,
                             "target_px": int(u["target"].sum()), "conditions": info_by_cond})
        if ui in gallery_idx:
            questions = [row.questions[i] for i, q in enumerate(row.question_id) if q in set(u["qids"])]
            gallery.append({"image_id": u["image_id"], "target_key": u["target_key"], "placebo_method": u["placebo_method"],
                            "qids": u["qids"], "questions": questions,
                            "panels": [("original", _thumb(img)), ("alvo+placebo", _thumb(_overlay(img, u["target"], placebo)))] + panels})
        if ui in review_idx:
            review.append({"image_id": u["image_id"], "target_key": u["target_key"], "placebo_method": u["placebo_method"],
                           "src": _thumb(_overlay(img, u["target"], placebo))})
    paired = [u for u in unit_records if all(u["placebo_method_by_factor"].get(k) is not None for k in ("1.5", "2"))]
    manifest = {"dataset": dataset, "source_arrow": arrow, "source_sha256": _sha256(arrow), "inventory": inventory,
                "inventory_seed": inv["params"]["seed"], "inventory_params": inv["params"], "gallery_seed": seed,
                "n_units": len(units), "n_questions": sum(len(u["qids"]) for u in units),
                "n_xray_units": sum(u["xray"] for u in unit_records),
                "encoding": {"C0": "source bytes", "others": "PNG lossless from decoded pixels"},
                "dose": {"paired_units": len(paired), "paired_questions": sum(len(u["qids"]) for u in paired),
                         "valid_by_factor": {k: sum(u["placebo_method_by_factor"].get(k) is not None for u in unit_records)
                                             for k in ("1.5", "2")}},
                "conditions": {}, "checksums": {}, "units": unit_records}
    for c in conditions:
        fname = f"vqa_{dataset}_placebo_{c}.arrow"
        path = os.path.join(out_dir, fname)
        write_arrow(pd.DataFrame(rows_by_cond[c]), path)
        sha = _sha256(path)
        manifest["conditions"][c] = {"file": fname, "sha256": sha, "n_rows": len(rows_by_cond[c]),
                                     "n_questions": sum(len(r["questions"]) for r in rows_by_cond[c]),
                                     "n_overlap_flagged": overlap_flags[c], "bytes": os.path.getsize(path)}
        manifest["checksums"][fname] = sha
    Path(manifest_path).parent.mkdir(parents=True, exist_ok=True)
    if os.path.exists(manifest_path):  # same source and same inventory: adds conditions, does not delete the others
        old = json.loads(Path(manifest_path).read_text())
        if old.get("source_sha256") == manifest["source_sha256"] and old.get("inventory_seed") == manifest["inventory_seed"]:
            manifest["conditions"] = {**old.get("conditions", {}), **manifest["conditions"]}
            manifest["checksums"] = {**old.get("checksums", {}), **manifest["checksums"]}
    Path(manifest_path).write_text(json.dumps(manifest, indent=1) + "\n")
    if gallery_path:
        Path(gallery_path).parent.mkdir(parents=True, exist_ok=True)
        Path(gallery_path).write_text(_gallery_html(dataset, gallery, review))
    return {"n_units": len(units), "n_questions": manifest["n_questions"],
            "conditions": {c: v["n_questions"] for c, v in manifest["conditions"].items()}}


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dataset", choices=["kvasir", "slake"], required=True)
    ap.add_argument("--arrow", required=True)
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--conditions", default=",".join(CONDITIONS), help="lista separada por virgula")
    ap.add_argument("--map"); ap.add_argument("--seg-dir"); ap.add_argument("--instrument-dir")
    ap.add_argument("--slake-root")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--gallery")
    ap.add_argument("--gallery-n", type=int, default=10)
    ap.add_argument("--review-n", type=int, default=50)
    ap.add_argument("--seed", type=int, required=True)
    a = ap.parse_args(argv)
    src = ({"map": a.map, "seg_dir": a.seg_dir, "instrument_dir": a.instrument_dir} if a.dataset == "kvasir"
           else {"slake_root": a.slake_root})
    if any(v is None for v in src.values()):
        ap.error(f"fontes de mascara incompletas para {a.dataset}: {src}")
    out = generate(a.dataset, a.arrow, a.inventory, a.out_dir, [c for c in a.conditions.split(",") if c], src,
                   a.manifest, a.gallery, a.gallery_n, a.review_n, a.seed)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
