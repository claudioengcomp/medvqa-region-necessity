"""F1 -- mask inventory of SLAKE (test set, English) for the ISBI paper.

Rules fixed before any number (plan v2 §1, SLAKE):
- negative control = modality and plane questions (content_type Modality/Plane);
- organ-dependent = question that names an organ (does it contain X? where is X? color,
  shape, count of X) -- target = region of that organ in the image;
- disease-dependent = abnormality/disease question -- target = region of the named
  disease, or union of the disease regions of the image;
- excluded = KG, main/largest organ, system, body part, size
  comparisons, descriptions by position/color ("the gray part on the left"), organ
  counting, and whatever matches no rule.

Region source: `mask.png` when it is a clean label map (every non-zero
value is in `mask.txt`) and carries the label; otherwise, the [x, y, w, h] box of
`detection.json` (the case of the X-rays, whose masks are not label maps).
The source is recorded per question. The regex is reviewed by hand on 50 items
by the authors (Gate P1).

SLAKE-specific rules (authors' decision, 14/09/2026):
- FOV = largest bright component with morphological OPENING (4 iterations) before
  filling holes, because the CT table, connected to the body, would make the hole filling
  swallow the background between body and table; a control occlusion is valid with >= 95 % inside the FOV.
- On X-rays (target from the detection.json box) the FOV is the whole frame.
- Each question carries `modality` and the `xray` flag: X-rays enter the pooled analysis
  with an origin flag, and a sensitivity analysis without X-rays is
  reported in one line.
- Dose: the control occlusion is re-placed for the dilated target (same search order,
  same seed); `placebo_method_by_factor` and `dose_reason_by_factor` per question.

Usage:
    python -m harness.isbi_placebo.inventory_slake         --arrow $LAB_ROOT/.../M3AE/data/finetune_arrows/vqa_slack_test.arrow         --slake-root $LAB_ROOT/.../data_drive_sync/raw/Slake1.0         --seed 20260913         --output-json results/isbi_placebo/inventory_slake_test.json         --output-md docs/isbi/placebo/inventory_slake_test.md
"""
from __future__ import annotations
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable

import argparse
import collections
import hashlib
import io
import json
import os
import re
from pathlib import Path

import numpy as np
from PIL import Image

from harness.interventions.arrow_io import read_arrow
from harness.isbi_placebo.masks import area_fraction, fov_mask, place_placebo, place_placebos_by_factor

ORGAN_TERMS = [
    "spinal cord", "small bowel", "temporal lobe", "femoral head", "humerus head", "brain stem",
    "liver", "heart", "lung", "spleen", "kidney", "brain", "brian", "bladder", "colon", "stomach",
    "rectum", "esophagus", "trachea", "larynx", "mandible", "parotid", "duodenum", "ear", "eye", "tooth",
]
DISEASE_TERMS = [
    "brain non-enhancing tumor", "brain enhancing tumor", "pulmonary infiltration", "pleural effusion",
    "brain edema", "brain tumor", "kidney cancer", "liver cancer", "lung cancer", "cardiomegaly",
    "pneumonia", "nodule", "atelectasis", "pneumothorax", "infiltration", "infiltrate", "effusion",
    "tumor", "cancer", "edema", "mass",
]
_PLURAL = {"kidneys": "kidney", "lungs": "lung", "ears": "ear", "eyes": "eye", "mandibles": "mandible",
           "temporal lobes": "temporal lobe", "femoral heads": "femoral head", "brian": "brain", "teeth": "tooth"}

_EXCLUDE = re.compile(
    r"part of the (human )?body|which part do the organs|where does the (picture|image)|"
    r"organs? in the image exist in|main organ|largest organ|biggest|bigger|smaller|organ system|"
    r"system (is|imaged|pictured|visualized)|study of the|appear(ing)? in pairs|how many organs|"
    r"(gray|black|white) (part|hole|points|spots|hollow)|(leftmost|rightmost) organ|"
    r"organ (on|located|with|in) the|which organ is abnormal|which organs?\b|organs? (in|appearing in)",
    re.I)
_DISEASE_HINT = re.compile(
    r"abnormal|normal|healthy|disease|which (side|lobe|hemisphere)|what part of the .* located|"
    r"hyperdense|hypodense|enhancing|density", re.I)


def _normalize(q: str) -> str:
    q = q.lower().replace("?", " ").replace(",", " ")
    for k, v in _PLURAL.items():
        q = re.sub(rf"\b{k}\b", v, q)
    return " ".join(q.split())


def _find_terms(q: str, vocab: list[str], with_side: bool,
                taken: np.ndarray | None = None) -> list[tuple[int, str]]:
    """Occurrences of vocabulary terms in q; `taken` marks spans already
    consumed (e.g. "brain" inside "brain edema" does not count as an organ)."""
    found = []
    if taken is None:
        taken = np.zeros(len(q), bool)
    for term in vocab:  # vocabulary sorted from longest to shortest
        for m in re.finditer(rf"\b{re.escape(term)}\b", q):
            if taken[m.start():m.end()].any():
                continue
            taken[m.start():m.end()] = True
            name, start = term, m.start()
            side = re.search(r"\b(left|right)\s+$", q[:start])
            if with_side and side:
                name, start = f"{side.group(1)} {term}", side.start()
            found.append((start, name))
    return sorted(found)


def classify_slake_question(question: str, content_type: str) -> tuple[str, list[str]]:
    """(class, named entities). Rules in the module docstring."""
    if content_type in ("Modality", "Plane"):
        return "negative_control", []
    if content_type == "KG":
        return "excluded", []
    q = _normalize(question)
    if _EXCLUDE.search(q):
        return "excluded", []
    taken = np.zeros(len(q), bool)
    diseases = _find_terms(q, DISEASE_TERMS, with_side=False, taken=taken)
    if content_type == "Abnormality" or diseases or _DISEASE_HINT.search(q):
        organs = _find_terms(q, ORGAN_TERMS, with_side=False, taken=taken)
        return "dependent_disease", [n for _, n in sorted(diseases + organs)]
    organs = _find_terms(q, ORGAN_TERMS, with_side=True)
    if organs:
        return "dependent_organ", [n for _, n in organs]
    return "excluded", []


def read_legend(path: str) -> dict[int, str]:
    out = {}
    for line in Path(path).read_text().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[int(k)] = v.strip()
    return out


def _is_disease(name: str) -> bool:
    n = name.lower()
    return any(t in n for t in ("cancer", "tumor", "edema", "cardiomegaly", "pneumonia", "nodule",
                                "atelectasis", "pneumothorax", "mass", "infiltrat", "effusion"))


def entity_regions(img_dir: str, legend: dict[int, str]) -> dict[str, dict]:
    """Regions available in the image: lowercase name -> {mask, source, is_disease}."""
    gray = np.array(Image.open(os.path.join(img_dir, "mask.png")).convert("L"))
    vals = {int(v) for v in np.unique(gray) if v}
    regions: dict[str, dict] = {}
    if vals and vals <= set(legend):
        for v in vals:
            name = legend[v]
            regions[name.lower()] = {"mask": gray == v, "source": "mask", "is_disease": _is_disease(name)}
    det_path = os.path.join(img_dir, "detection.json")
    if os.path.exists(det_path):
        h, w = gray.shape
        for item in json.loads(Path(det_path).read_text()):
            for name, (x, y, bw, bh) in item.items():
                key = name.lower()
                if key in regions:
                    continue
                m = np.zeros((h, w), bool)
                m[int(round(y)):int(round(y + bh)), int(round(x)):int(round(x + bw))] = True
                regions[key] = {"mask": m, "source": "bbox", "is_disease": _is_disease(name)}
    return regions


def _resolve(entities: list[str], regions: dict[str, dict], cls: str) -> tuple[list[str], str | None]:
    """Region names that account for the target, or (None, reason)."""
    names = []
    for e in entities:
        exact = [k for k in regions if k == e]
        partial = [k for k in regions if e in k.split() or k.endswith(" " + e)]
        names += exact or partial
    names = sorted(set(names))
    if cls == "dependent_disease":
        chosen = [n for n in names if regions[n]["is_disease"]] or [n for n in regions if regions[n]["is_disease"]]
        return (chosen, None) if chosen else ([], "no_disease_region")
    if cls == "dependent_organ":
        chosen = [n for n in names if not regions[n]["is_disease"]]
        return (chosen, None) if chosen else ([], "entity_not_in_image")
    if cls == "negative_control":
        disease = [n for n in regions if regions[n]["is_disease"]]
        if disease:
            return disease, None
        organs = sorted((n for n in regions if not regions[n]["is_disease"]),
                        key=lambda n: -int(regions[n]["mask"].sum()))
        return (organs[:1], None) if organs else ([], "no_region")
    return [], "excluded_class"


def fov_for_modality(img: np.ndarray, modality: str | None, opening: int = 4) -> np.ndarray:
    """X-ray: whole frame (target comes from a box). CT/MRI: body, with opening."""
    if modality and modality.lower().replace("-", "") == "xray":
        return np.ones(img.shape[:2], bool)
    return fov_mask(img, opening=opening)


def _image_seed(seed: int, image_id: str, key: str) -> int:
    h = hashlib.sha256(f"{seed}:{image_id}:{key}".encode()).digest()
    return int.from_bytes(h[:4], "little")


def build_inventory(arrow: str, slake_root: str, seed: int, max_area_frac: float = 0.4,
                    n_random: int = 50, min_fov_frac: float = 0.95, fov_opening: int = 4) -> dict:
    legend = read_legend(os.path.join(slake_root, "mask.txt"))
    meta = {x["qid"]: x for x in json.loads(Path(slake_root, "test.json").read_text())}
    df = read_arrow(arrow)
    images, questions = [], []
    for row in df.itertuples(index=False):
        xm = re.search(r"(xmlab\d+)", row.image_id).group(1)
        img_dir = os.path.join(slake_root, "imgs", xm)
        img = np.array(Image.open(io.BytesIO(row.image)).convert("RGB"))
        regions = entity_regions(img_dir, legend)
        gray_shape = np.array(Image.open(os.path.join(img_dir, "mask.png")).convert("L")).shape
        size_ok = gray_shape == img.shape[:2]
        modality = next((meta[q]["modality"] for q in row.question_id if q in meta), None)
        xray = bool(modality and modality.lower().replace("-", "") == "xray")
        fov = fov_for_modality(img, modality, opening=fov_opening)
        mask_clean = any(r["source"] == "mask" for r in regions.values())
        images.append({"image_id": xm, "height": int(img.shape[0]), "width": int(img.shape[1]),
                       "size_match": bool(size_ok), "mask_clean": bool(mask_clean),
                       "regions": {k: v["source"] for k, v in regions.items()},
                       "modality": modality, "xray": xray, "fov_frac": float(fov.mean())})
        cache: dict[str, dict] = {}
        for q, qid in zip(row.questions, row.question_id):
            ct = meta[qid]["content_type"] if qid in meta else "?"
            cls, ents = classify_slake_question(q, ct)
            rec = {"qid": int(qid), "image_id": xm, "question": q, "content_type": ct, "question_class": cls,
                   "modality": modality, "xray": xray,
                   "entities": ents, "target_entities": [], "region_source": None, "area_frac_fov": None,
                   "placebo_method": None, "placebo_method_by_factor": {}, "dose_reason_by_factor": {},
                   "evaluable": False, "reason": None}
            names, why = _resolve(ents, regions, cls)
            if why:
                rec["reason"] = why
            elif not size_ok:
                rec["reason"] = "size_mismatch"
            else:
                key = "|".join(names)
                if key not in cache:
                    target = np.logical_or.reduce([regions[n]["mask"] for n in names])
                    frac = area_fraction(target, fov)
                    if frac > max_area_frac:
                        cache[key] = {"frac": frac, "how": None, "reason": "area_gt_max", "by_factor": {}, "dose_reason": {}}
                    else:
                        u_seed = _image_seed(seed, xm, key)
                        placebo, how = place_placebo(target, fov, seed=u_seed, n_random=n_random,
                                                     min_fov_frac=min_fov_frac)
                        by_factor, dose_reason = ({}, {}) if placebo is None else place_placebos_by_factor(
                            target, fov, seed=u_seed, n_random=n_random, min_fov_frac=min_fov_frac,
                            max_area_frac=max_area_frac)
                        cache[key] = {"frac": frac, "how": how if placebo is not None else None,
                                      "reason": None if placebo is not None else how,
                                      "by_factor": by_factor, "dose_reason": dose_reason}
                c = cache[key]
                rec.update(target_entities=names, area_frac_fov=c["frac"], placebo_method=c["how"],
                           placebo_method_by_factor=c["by_factor"], dose_reason_by_factor=c["dose_reason"],
                           region_source="+".join(sorted({regions[n]["source"] for n in names})))
                if c["reason"]:
                    rec["reason"] = c["reason"]
                else:
                    rec["evaluable"] = True
            questions.append(rec)
    return {"params": {"arrow": arrow, "slake_root": slake_root, "seed": seed, "max_area_frac": max_area_frac,
                       "n_random": n_random, "min_fov_frac": min_fov_frac, "fov_opening": fov_opening},
            "images": images, "questions": questions, "summary": _summarize(images, questions)}


def _summarize(images: list[dict], questions: list[dict]) -> dict:
    ev = [q for q in questions if q["evaluable"]]
    fracs = np.array([q["area_frac_fov"] for q in questions if q["area_frac_fov"] is not None])
    units = {(q["image_id"], tuple(q["target_entities"])): q for q in ev}.values()
    return {
        "n_images": len(images),
        "n_questions": len(questions),
        "n_evaluable": len(ev),
        "evaluable_by_class": dict(collections.Counter(q["question_class"] for q in ev)),
        "evaluable_by_content_type": dict(collections.Counter(q["content_type"] for q in ev)),
        "evaluable_by_region_source": dict(collections.Counter(q["region_source"] for q in ev)),
        "questions_by_class": dict(collections.Counter(q["question_class"] for q in questions)),
        "not_evaluable_reasons": dict(collections.Counter(q["reason"] for q in questions if not q["evaluable"])),
        "images": {
            "mask_clean": sum(i["mask_clean"] for i in images),
            "size_mismatch": sum(not i["size_match"] for i in images),
            "by_modality": dict(collections.Counter(i["modality"] for i in images)),
            "placebo_methods": dict(collections.Counter(q["placebo_method"].split(":")[0] for q in ev)),
            "units": len(units),
            "dose_valid": {
                "1.5": sum(u["placebo_method_by_factor"].get("1.5") is not None for u in units),
                "2": sum(u["placebo_method_by_factor"].get("2") is not None for u in units),
                "all_levels": sum(all(u["placebo_method_by_factor"].get(k) is not None for k in ("1.5", "2"))
                                  for u in units),
            },
            "dose_reasons": dict(collections.Counter(
                f"{k}:{v}" for u in units for k, v in u["dose_reason_by_factor"].items() if v)),
        },
        "evaluable_xray": sum(q["xray"] for q in ev),
        "area_frac_fov_quantiles": (
            {str(p): float(np.quantile(fracs, p / 100)) for p in (0, 10, 25, 50, 75, 90, 100)} if fracs.size else {}),
    }


def render_markdown(inv: dict) -> str:
    s, p = inv["summary"], inv["params"]
    lines = [f"# Inventário F1 — SLAKE (seed {p['seed']}, área máx. {p['max_area_frac']:.0%} do FOV, "
             f"placebo ≥ {p['min_fov_frac']:.0%} no FOV, abertura {p['fov_opening']}; raio-X = quadro inteiro)", "",
             f"Arrow: `{p['arrow']}`", "",
             f"Imagens: {s['n_images']} ({', '.join(f'{k}={v}' for k, v in sorted(s['images']['by_modality'].items()))}); "
             f"máscara de rótulo limpa: {s['images']['mask_clean']}; resolução divergente: {s['images']['size_mismatch']}.", "",
             f"Perguntas: {s['n_questions']}; avaliáveis: {s['n_evaluable']}.", "",
             "| classe | perguntas | avaliáveis |", "|---|---:|---:|"]
    lines += [f"| {k} | {v} | {s['evaluable_by_class'].get(k, 0)} |" for k, v in sorted(s["questions_by_class"].items())]
    lines += ["", "| content_type | avaliáveis |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(s["evaluable_by_content_type"].items(), key=lambda kv: -kv[1])]
    lines += ["", "| fonte da região | avaliáveis |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(s["evaluable_by_region_source"].items())]
    lines += ["", "| motivo de não avaliável | perguntas |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(s["not_evaluable_reasons"].items(), key=lambda kv: -kv[1])]
    lines += ["", "| método do placebo | perguntas avaliáveis |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(s["images"]["placebo_methods"].items())]
    dv = s["images"]["dose_valid"]
    lines += ["", f"Perguntas avaliáveis em raio-X (marca de origem): {s['evaluable_xray']} de {s['n_evaluable']}.",
              "", f"Unidades (imagem, alvo): {s['images']['units']}. Dose (placebo recolocado para o alvo dilatado): "
              f"válidas a 1,5× = {dv['1.5']}, a 2× = {dv['2']}, **nos três níveis = {dv['all_levels']}**. Motivos: "
              + (", ".join(f"{k}={v}" for k, v in sorted(s["images"]["dose_reasons"].items())) or "nenhum") + "."]
    if s["area_frac_fov_quantiles"]:
        lines += ["", "Fração do FOV ocupada pelo alvo (quantis, perguntas com alvo): "
                  + ", ".join(f"p{k}={v:.3f}" for k, v in s["area_frac_fov_quantiles"].items())]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arrow", required=True)
    ap.add_argument("--slake-root", required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--max-area-frac", type=float, default=0.4)
    ap.add_argument("--n-random", type=int, default=50)
    ap.add_argument("--min-fov-frac", type=float, default=0.95)
    ap.add_argument("--fov-opening", type=int, default=4)
    ap.add_argument("--output-json", required=True)
    ap.add_argument("--output-md")
    args = ap.parse_args(argv)
    inv = build_inventory(args.arrow, args.slake_root, args.seed, args.max_area_frac, args.n_random,
                          args.min_fov_frac, args.fov_opening)
    Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_json).write_text(json.dumps(inv, indent=1) + "\n")
    md = render_markdown(inv)
    if args.output_md:
        Path(args.output_md).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output_md).write_text(md)
    print(md)


if __name__ == "__main__":
    main()
