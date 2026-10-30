"""F1 -- mask inventory of Kvasir-VQA-x1 (clean test set) for the ISBI paper.

For each image in the arrow: is there a mask (Kvasir-SEG for polyp,
Kvasir-Instrument for instrument)? Does the resolution match? What fraction of the FOV
does the target occupy? Is there a valid control occlusion placement (plan v2 §2)? For each
question: pre-registered class (§1 of the plan), target required by the class, and whether
it is evaluable -- with the reason when it is not.

Generates no condition; only measures. The output feeds Gate P0 of the plan
(Kvasir >= 600 evaluable questions and >= 80 per main type).

Usage:
    python -m harness.isbi_placebo.inventory_kvasir         --arrow $LAB_ROOT/.../data/finetune_arrows/vqa_kvasir_test_clean.arrow         --map data/isbi_placebo/kvasir_vqa_to_seg_instrument_map.json         --seg-dir $LAB_ROOT/.../data_drive_sync/raw/Kvasir-SEG         --instrument-dir $LAB_ROOT/.../data_drive_sync/raw/kvasir-instrument         --seed 20260913         --output-json results/isbi_placebo/inventory_kvasir.json         --output-md docs/isbi/placebo/inventory_kvasir.md
"""
from __future__ import annotations
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable

import argparse
import collections
import hashlib
import io
import json
import os
from pathlib import Path

import numpy as np
from PIL import Image

from harness.interventions.arrow_io import read_arrow
from harness.isbi_placebo.masks import (
    area_fraction,
    binarize_mask,
    classify_kvasir_question,
    fov_mask,
    place_placebo,
    place_placebos_by_factor,
)

TARGET_BY_CLASS = {
    "dependent_polyp": "polyp",
    "dependent_polyp_secondary": "polyp",
    "dependent_instrument": "instrument",
    "negative_control": "any",
    "excluded": None,
}


def _image_seed(seed: int, image_id: str) -> int:
    """Per-image seed, stable across runs and independent of the arrow order."""
    h = hashlib.sha256(f"{seed}:{image_id}".encode()).digest()
    return int.from_bytes(h[:4], "little")


def _mask_paths(kind: str, entry, seg_dir: str, instrument_dir: str) -> list[str]:
    names = entry if isinstance(entry, list) else [entry]
    root = os.path.join(seg_dir if kind == "polyp" else instrument_dir, "masks")
    out = []
    for n in names:
        stem = os.path.splitext(n)[0]
        cands = [p for p in os.listdir(root) if os.path.splitext(p)[0] == stem]
        if not cands:
            raise FileNotFoundError(f"mascara de {n} nao encontrada em {root}")
        out.append(os.path.join(root, cands[0]))
    return out


def _load_union_mask(paths: list[str]) -> tuple[np.ndarray | None, str | None]:
    masks = [binarize_mask(np.array(Image.open(p))) for p in paths]
    if len({m.shape for m in masks}) != 1:
        return None, "mask_files_disagree"
    return np.logical_or.reduce(masks), None


def load_target_mask(image_id: str, mapping: dict, seg_dir: str, instrument_dir: str) -> tuple[np.ndarray | None, str | None]:
    """(union mask of the target, type) of the image, or (None, None) if there is no mask.
    Used by the generator (F2) to rebuild exactly the target the inventory measured."""
    if image_id in mapping["polyps"]:
        kind, entry = "polyp", mapping["polyps"][image_id]
    elif image_id in mapping["instrument"]:
        kind, entry = "instrument", mapping["instrument"][image_id]
    else:
        return None, None
    mask, err = _load_union_mask(_mask_paths(kind, entry, seg_dir, instrument_dir))
    return (mask, kind) if err is None else (None, kind)


def _inspect_image(image_bytes: bytes, image_id: str, mapping: dict, seg_dir: str, instrument_dir: str,
                   seed: int, max_area_frac: float, n_random: int, min_fov_frac: float = 0.8,
                   fov_opening: int = 0) -> dict:
    rec = {"image_id": image_id, "target_kind": None, "n_mask_files": 0, "exclusion": None,
           "width": None, "height": None, "fov_frac": None, "area_frac_fov": None, "placebo_method": None,
           "placebo_method_by_factor": {}, "dose_reason_by_factor": {}}
    if image_id in mapping["polyps"]:
        kind, entry = "polyp", mapping["polyps"][image_id]
    elif image_id in mapping["instrument"]:
        kind, entry = "instrument", mapping["instrument"][image_id]
    else:
        rec["exclusion"] = "no_mask"
        return rec
    rec["target_kind"] = kind
    paths = _mask_paths(kind, entry, seg_dir, instrument_dir)
    rec["n_mask_files"] = len(paths)
    img = np.array(Image.open(io.BytesIO(image_bytes)).convert("RGB"))
    rec["height"], rec["width"] = img.shape[:2]
    target, err = _load_union_mask(paths)
    if err:
        rec["exclusion"] = err
        return rec
    if target.shape != img.shape[:2]:
        rec["exclusion"] = "size_mismatch"
        return rec
    if not target.any():
        rec["exclusion"] = "empty_mask"
        return rec
    fov = fov_mask(img, opening=fov_opening)
    rec["fov_frac"] = float(fov.mean())
    rec["area_frac_fov"] = area_fraction(target, fov)
    if rec["area_frac_fov"] > max_area_frac:
        rec["exclusion"] = "area_gt_max"
        return rec
    img_seed = _image_seed(seed, image_id)
    placebo, how = place_placebo(target, fov, seed=img_seed, n_random=n_random, min_fov_frac=min_fov_frac)
    if placebo is None:
        rec["exclusion"] = how
        return rec
    rec["placebo_method"] = how
    rec["placebo_method_by_factor"], rec["dose_reason_by_factor"] = place_placebos_by_factor(
        target, fov, seed=img_seed, n_random=n_random, min_fov_frac=min_fov_frac, max_area_frac=max_area_frac)
    return rec


def build_inventory(arrow: str, map_path: str, seg_dir: str, instrument_dir: str, seed: int,
                    max_area_frac: float = 0.4, n_random: int = 50, min_fov_frac: float = 0.8,
                    fov_opening: int = 0) -> dict:
    mapping = json.loads(Path(map_path).read_text())
    df = read_arrow(arrow)
    images, questions = [], []
    for row in df.itertuples(index=False):
        image_id = row.image_id.split("/", 1)[1] if "/" in row.image_id else row.image_id
        rec = _inspect_image(row.image, image_id, mapping, seg_dir, instrument_dir, seed, max_area_frac, n_random,
                             min_fov_frac, fov_opening)
        images.append(rec)
        has_target = rec["exclusion"] is None
        for q, qid in zip(row.questions, row.question_id):
            cls = classify_kvasir_question(q)
            need = TARGET_BY_CLASS[cls]
            qrec = {"qid": int(qid), "image_id": image_id, "question": q, "question_class": cls,
                    "target_kind": None, "evaluable": False, "reason": None}
            if need is None:
                qrec["reason"] = "excluded_class"
            elif rec["target_kind"] is None:
                qrec["reason"] = "no_mask"
            elif need != "any" and rec["target_kind"] != need:
                qrec["reason"] = f"no_{need}_mask"
            elif not has_target:
                qrec["reason"] = rec["exclusion"]
            else:
                qrec["target_kind"] = rec["target_kind"]
                qrec["evaluable"] = True
            questions.append(qrec)
    return {"params": {"arrow": arrow, "map": map_path, "seed": seed, "max_area_frac": max_area_frac,
                       "n_random": n_random, "min_fov_frac": min_fov_frac, "fov_opening": fov_opening},
            "images": images, "questions": questions, "summary": _summarize(images, questions)}


def _summarize(images: list[dict], questions: list[dict]) -> dict:
    ev = [q for q in questions if q["evaluable"]]
    by_class = collections.Counter(q["question_class"] for q in ev)
    by_template = collections.Counter(q["question"] for q in ev)
    by_template_all = collections.Counter(q["question"] for q in questions)
    reasons = collections.Counter(q["reason"] for q in questions if not q["evaluable"])
    with_target = [i for i in images if i["exclusion"] is None]
    fracs = np.array([i["area_frac_fov"] for i in images if i["area_frac_fov"] is not None])
    return {
        "n_images": len(images),
        "n_questions": len(questions),
        "n_evaluable": len(ev),
        "evaluable_by_class": dict(by_class),
        "evaluable_by_template": dict(by_template),
        "total_by_template": dict(by_template_all),
        "not_evaluable_reasons": dict(reasons),
        "images": {
            "with_target": len(with_target),
            "by_kind": dict(collections.Counter(i["target_kind"] for i in with_target)),
            "excluded": dict(collections.Counter(i["exclusion"] for i in images if i["exclusion"])),
            "placebo_methods": dict(collections.Counter(
                i["placebo_method"].split(":")[0] for i in with_target)),
            "dose_valid": {
                "1.5": sum(i["placebo_method_by_factor"].get("1.5") is not None for i in with_target),
                "2": sum(i["placebo_method_by_factor"].get("2") is not None for i in with_target),
                "all_levels": sum(all(i["placebo_method_by_factor"].get(k) is not None for k in ("1.5", "2"))
                                  for i in with_target),
            },
            "dose_reasons": dict(collections.Counter(
                f"{k}:{v}" for i in with_target for k, v in i["dose_reason_by_factor"].items() if v)),
        },
        "area_frac_fov_quantiles": (
            {str(p): float(np.quantile(fracs, p / 100)) for p in (0, 10, 25, 50, 75, 90, 100)} if fracs.size else {}),
    }


def render_markdown(inv: dict) -> str:
    s, p = inv["summary"], inv["params"]
    lines = [f"# Inventário F1 — Kvasir (seed {p['seed']}, área máx. {p['max_area_frac']:.0%} do FOV)", "",
             f"Arrow: `{p['arrow']}`", "",
             f"Imagens: {s['n_images']}; com alvo válido: {s['images']['with_target']} "
             f"({', '.join(f'{k}={v}' for k, v in sorted(s['images']['by_kind'].items()))}); "
             f"excluídas: {', '.join(f'{k}={v}' for k, v in sorted(s['images']['excluded'].items())) or 'nenhuma'}.", "",
             f"Perguntas: {s['n_questions']}; avaliáveis: {s['n_evaluable']}.", "",
             "| classe | avaliáveis |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(s["evaluable_by_class"].items())]
    lines += ["", "| template | total | avaliáveis |", "|---|---:|---:|"]
    for q, n in sorted(s["total_by_template"].items(), key=lambda kv: -kv[1]):
        lines.append(f"| {q} | {n} | {s['evaluable_by_template'].get(q, 0)} |")
    lines += ["", "| motivo de não avaliável | perguntas |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(s["not_evaluable_reasons"].items(), key=lambda kv: -kv[1])]
    lines += ["", "| método do placebo | imagens |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(s["images"]["placebo_methods"].items())]
    dv = s["images"]["dose_valid"]
    lines += ["", f"Dose (placebo recolocado para o alvo dilatado): válidas a 1,5× = {dv['1.5']}, a 2× = {dv['2']}, "
              f"**nos três níveis = {dv['all_levels']}** (subconjunto pareado da dose). Motivos: "
              + (", ".join(f"{k}={v}" for k, v in sorted(s["images"]["dose_reasons"].items())) or "nenhum") + "."]
    if s["area_frac_fov_quantiles"]:
        lines += ["", "Fração do FOV ocupada pelo alvo (quantis, imagens com máscara): "
                  + ", ".join(f"p{k}={v:.3f}" for k, v in s["area_frac_fov_quantiles"].items())]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arrow", required=True)
    ap.add_argument("--map", required=True)
    ap.add_argument("--seg-dir", required=True)
    ap.add_argument("--instrument-dir", required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--max-area-frac", type=float, default=0.4)
    ap.add_argument("--n-random", type=int, default=50)
    ap.add_argument("--min-fov-frac", type=float, default=0.8)
    ap.add_argument("--fov-opening", type=int, default=0)
    ap.add_argument("--output-json", required=True)
    ap.add_argument("--output-md")
    args = ap.parse_args(argv)
    inv = build_inventory(args.arrow, args.map, args.seg_dir, args.instrument_dir, args.seed,
                          args.max_area_frac, args.n_random, args.min_fov_frac, args.fov_opening)
    Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_json).write_text(json.dumps(inv, indent=1) + "\n")
    md = render_markdown(inv)
    if args.output_md:
        Path(args.output_md).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output_md).write_text(md)
    print(md)


if __name__ == "__main__":
    main()
