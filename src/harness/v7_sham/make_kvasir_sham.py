"""P2.2 (2026-10-09): Kvasir occluder tests (`sham` in the code) -- occluder placed on images WITHOUT the finding, on the clean test set.
Sets (gold read from the test arrow): ART = "Is there a green/black box artefact?" with gold no; POL = images with
"How many polyps are in the image?" = 0 or "What type of polyp is present?" = none (union per image);
INS = "Are there any instruments in the image? Check all that are present." = none or "How many instrumnets are in the
image?" = 0 (union per image). Occluders: ART = 4:3 rectangle with area = Q1 or Q3 (alternating per image, seeded draw)
of the FOV area fraction of the polyp masks of the control-occlusion inventory (there is no artifact mask in
mask_sources: declared); POL_Q1/POL_Q3 = donor mask drawn from Kvasir-SEG with image area fraction in
quartile 1 (<= P25) / quartile 3 (>= P75), rescaled to the same fraction of the target image; INS = donor from
kvasir-instrument with median area (P40-P60). Position: random integer translation within the frame with >= 80 % inside the
FOV (fov_mask from masks.py, opening 0, as in the Kvasir P), seed per image = sha256("20260913:<image_id>") as in the
inventory, up to 50 attempts. Fills black and blur10 (fill_region from conditions.py). Lossless PNG encoding
of the decoded pixels (as for T/P/S). Questions: native ones of the set + crossed (POL receives instrument presence;
INS receives polyp count), exact template text; crossed questions that do not exist in the image receive a new qid
(9000000+) and gold "unknown" (declared); C0_cross = original bytes with only the crossed questions."""
from __future__ import annotations
import argparse, collections, hashlib, io, json, os, random, time
from multiprocessing import Pool
from scipy import ndimage
import numpy as np, pandas as pd
from PIL import Image
from harness.interventions.arrow_io import read_arrow, write_arrow
from harness.isbi_placebo.conditions import fill_region, encode_png
from harness.isbi_placebo.masks import fov_mask, binarize_mask, _translate

Q_ART = "Is there a green/black box artefact?"; Q_POLN = "How many polyps are in the image?"; Q_POLT = "What type of polyp is present?"
Q_INSP = "Are there any instruments in the image? Check all that are present."; Q_INSN = "How many instrumnets are in the image?"
SETS = {"ART": {"native": [Q_ART], "cross": []}, "POL": {"native": [Q_POLN, Q_POLT], "cross": [Q_INSP]}, "INS": {"native": [Q_INSP, Q_INSN], "cross": [Q_POLN]}}
CONDS = ["SHAM_ART_black", "SHAM_ART_blur10", "SHAM_POL_Q1_black", "SHAM_POL_Q1_blur10", "SHAM_POL_Q3_black", "SHAM_POL_Q3_blur10", "SHAM_INS_black", "SHAM_INS_blur10"]
CROSS_QID0 = 9_000_000

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""): h.update(b)
    return h.hexdigest()
def image_seed(seed, image_id): return int.from_bytes(hashlib.sha256(f"{seed}:{image_id}".encode()).digest()[:4], "little")
def gold(a): return str(list(a)[0]).strip().lower() if len(a) else ""
def norm_iid(s): return s.split("/", 1)[1] if "/" in s else s

def donor_pool(mask_dir):
    out = []
    for n in sorted(os.listdir(mask_dir)):
        m = binarize_mask(np.array(Image.open(os.path.join(mask_dir, n))))
        if m.any(): out.append({"name": n, "mask": m, "frac": float(m.sum() / m.size), "h": m.shape[0], "w": m.shape[1]})
    return out

def scaled_crop(mask, target_px):
    ys, xs = np.nonzero(mask); crop = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    s = float(np.sqrt(target_px / max(crop.sum(), 1)))
    nh, nw = max(1, int(round(crop.shape[0] * s))), max(1, int(round(crop.shape[1] * s)))
    return np.array(Image.fromarray(crop.astype(np.uint8) * 255).resize((nw, nh), Image.NEAREST)) > 127

def place(shape, fov, rng, n_random=50, min_fov_frac=0.8):
    """Places `shape` (boolean cutout) in the frame of `fov`, entirely inside the frame, >= 80 % in the FOV."""
    H, W = fov.shape; h, w = shape.shape; fit = None
    if h > H or w > W:   # does not fit: shrink to the frame (recorded)
        s = min(H / h, W / w) * 0.98; shape = np.array(Image.fromarray(shape.astype(np.uint8) * 255).resize((max(1, int(w * s)), max(1, int(h * s))), Image.NEAREST)) > 127; h, w = shape.shape; fit = s
    n = int(shape.sum())
    for k in range(n_random):
        y0 = int(rng.integers(0, H - h + 1)); x0 = int(rng.integers(0, W - w + 1))
        cand = np.zeros((H, W), bool); cand[y0:y0 + h, x0:x0 + w] = shape
        if (cand & fov).sum() / max(n, 1) >= min_fov_frac: return cand, {"y0": y0, "x0": x0, "h": h, "w": w, "tries": k + 1, "fit_scale": fit, "fov_frac_inside": float((cand & fov).sum() / n)}
    return None, {"reason": "no_valid_placement", "tries": n_random, "fit_scale": fit}

def rect(area_px, aspect=4 / 3):
    w = max(1, int(round(np.sqrt(area_px * aspect)))); h = max(1, int(round(area_px / w))); return np.ones((h, w), bool)

def fill_fast(img, region, fill, blurred):
    """Same as conditions.fill_region for black/blur10, but reuses the Gaussian blur of the whole image (independent of the region)."""
    out = img.copy()
    if fill == "black": out[region] = 0
    else: out[region] = np.clip(np.round(blurred[region]), 0, 255).astype(np.uint8)
    return out

_G = {}
def _init(df, rows_by_set, native_q_index, answer_type_of, pool, q1_art, q3_art, seed, ex_idx):
    _G.update(df=df, rows_by_set=rows_by_set, native_q_index=native_q_index, answer_type_of=answer_type_of, pool=pool, q1_art=q1_art, q3_art=q3_art, seed=seed, ex_idx=ex_idx)

def _work(args):
    n_done, ri = args; df = _G["df"]; rows_by_set = _G["rows_by_set"]; native_q_index = _G["native_q_index"]; answer_type_of = _G["answer_type_of"]; pool = _G["pool"]; q1_art, q3_art, seed = _G["q1_art"], _G["q3_art"], _G["seed"]
    def subrow(row, items, image_bytes):
        return {"image": image_bytes, "questions": [i["q"] for i in items], "answers": [i["answers"] for i in items], "answer_labels": [i["labels"] for i in items], "answer_scores": [i["scores"] for i in items],
                "image_id": row.image_id, "question_id": [i["qid"] for i in items], "answer_type": [i["atype"] for i in items], "split": "test"}
    def qitem(ri, row, q, origin):
        if (ri, q) in native_q_index:
            k = native_q_index[(ri, q)]
            return {"q": q, "qid": int(row.question_id[k]), "answers": list(row.answers[k]), "labels": list(row.answer_labels[k]), "scores": [float(x) for x in row.answer_scores[k]], "atype": int(row.answer_type[k]), "origin": origin, "gold_known": True}
        return {"q": q, "qid": None, "answers": ["unknown"], "labels": [], "scores": [], "atype": answer_type_of.get(q, 1), "origin": origin, "gold_known": False}
    row = df.iloc[ri]; iid = norm_iid(row.image_id)
    img = np.array(Image.open(io.BytesIO(row.image)).convert("RGB")); H, W = img.shape[:2]; fov = fov_mask(img, opening=0); F = int(fov.sum())
    sigma = 10.0 / 100.0 * W; blurred = np.stack([ndimage.gaussian_filter(img[..., c].astype(np.float32), sigma) for c in range(3)], axis=-1)
    rng = np.random.default_rng(image_seed(seed, iid)); cross_items_img = []; rows_out = collections.defaultdict(list); inv_rows = []; examples = []; fails = collections.Counter()
    for s in SETS:
        if ri not in rows_by_set[s]: continue
        items = [qitem(ri, row, q, "native") for q in rows_by_set[s][ri]] + [qitem(ri, row, q, "cross") for q in SETS[s]["cross"]]
        cross_items_img += [i for i in items if i["origin"] == "cross"]
        shapes = {}
        if s == "ART":
            which = "Q1" if rng.integers(0, 2) == 0 else "Q3"; frac = q1_art if which == "Q1" else q3_art
            shapes["ART"] = (rect(frac * F), {"donor": None, "size_rule": f"rect 4:3, area {which} of polyp area_frac_fov x FOV", "frac_target": frac, "quartile": which})
        elif s == "POL":
            for qk in ("Q1", "Q3"):
                d = pool["POL_" + qk][int(rng.integers(0, len(pool["POL_" + qk])))]
                shapes["POL_" + qk] = (scaled_crop(d["mask"], d["frac"] * H * W), {"donor": "Kvasir-SEG/masks/" + d["name"], "size_rule": f"donor area fraction of image preserved ({qk})", "frac_target": d["frac"], "quartile": qk})
        else:
            d = pool["INS"][int(rng.integers(0, len(pool["INS"])))]
            shapes["INS"] = (scaled_crop(d["mask"], d["frac"] * H * W), {"donor": "kvasir-instrument/masks/" + d["name"], "size_rule": "donor area fraction of image preserved (median band P40-P60)", "frac_target": d["frac"], "quartile": "median"})
        for sk, (shape, meta) in shapes.items():
            region, pl = place(shape, fov, rng)
            for fill in ("black", "blur10"):
                cond = f"SHAM_{sk}_{fill}"
                rec = {"image_id": iid, "set": s, "condition": cond, "fill": fill, **meta, "placement": pl, "height": H, "width": W, "fov_px": F,
                       "questions": [{"qid": i["qid"], "question": i["q"], "origin": i["origin"], "gold": i["answers"][0] if i["answers"] else "", "gold_known": i["gold_known"]} for i in items], "seed_image": image_seed(seed, iid)}
                if region is None: fails[cond] += 1; rec["generated"] = False; inv_rows.append(rec); continue
                out = fill_fast(img, region, fill, blurred); rec["generated"] = True; rec["region_px"] = int(region.sum()); rec["region_frac_fov"] = float((region & fov).sum() / max(F, 1))
                rows_out[cond].append(subrow(row, items, encode_png(out))); inv_rows.append(rec)
                if n_done in _G["ex_idx"]: examples.append((cond, iid, np.concatenate([img, np.zeros((H, 8, 3), np.uint8) + 255, out], axis=1)))
    seen = set(); cx = [i for i in cross_items_img if not (i["qid"] in seen or seen.add(i["qid"]))]
    c0x = subrow(row, cx, row.image) if cx else None
    return n_done, dict(rows_out), inv_rows, examples, dict(fails), c0x

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arrow", required=True); ap.add_argument("--inventory", required=True); ap.add_argument("--seg-dir", required=True); ap.add_argument("--instrument-dir", required=True)
    ap.add_argument("--out-dir", required=True); ap.add_argument("--examples-dir", required=True); ap.add_argument("--inventory-out", required=True); ap.add_argument("--manifest", required=True)
    ap.add_argument("--seed", type=int, default=20260913); ap.add_argument("--n-examples", type=int, default=12); ap.add_argument("--counts-only", action="store_true"); ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args(); t0 = time.time()
    df = read_arrow(a.arrow); inv = json.load(open(a.inventory))
    # --- conjuntos
    rows_by_set = {s: {} for s in SETS}; q_counts = collections.Counter()
    native_q_index = {}   # (row, question) -> index of the question in the row
    for ri, row in enumerate(df.itertuples(index=False)):
        for qi, (q, ans) in enumerate(zip(row.questions, row.answers)):
            g = gold(ans); native_q_index[(ri, q)] = qi
            hit = None
            if q == Q_ART and g == "no": hit = "ART"
            elif (q == Q_POLN and g == "0") or (q == Q_POLT and g == "none"): hit = "POL"
            elif (q == Q_INSP and g == "none") or (q == Q_INSN and g == "0"): hit = "INS"
            if hit: q_counts[(hit, q)] += 1; rows_by_set[hit].setdefault(ri, set()).add(q)
    counts = {"by_set_question": {f"{s}|{q}": n for (s, q), n in sorted(q_counts.items())}, "images_by_set": {s: len(r) for s, r in rows_by_set.items()},
              "images_in_two_or_more_sets": len([r for r in set().union(*[set(x) for x in rows_by_set.values()]) if sum(r in x for x in rows_by_set.values()) >= 2]),
              "n_rows_arrow": len(df), "n_questions_arrow": int(sum(len(q) for q in df.questions))}
    # native questions per image in the set (all native questions of the set present in the image, not only those that matched the gold)
    for s in SETS:
        for ri in rows_by_set[s]:
            rows_by_set[s][ri] = [q for q in SETS[s]["native"] if (ri, q) in native_q_index]
    counts["native_questions_by_set"] = {s: int(sum(len(v) for v in r.values())) for s, r in rows_by_set.items()}
    counts["cross_questions_by_set"] = {s: {"n_images": len(r), "n_native_present": int(sum((ri, SETS[s]["cross"][0]) in native_q_index for ri in r))} for s, r in rows_by_set.items() if SETS[s]["cross"]}
    print(json.dumps(counts, indent=1), flush=True)
    if a.counts_only: return
    # --- donors and sizes
    polyp_fr = sorted(i["area_frac_fov"] for i in inv["images"] if i.get("target_kind") == "polyp" and i.get("area_frac_fov") is not None and i["exclusion"] != "area_gt_max")
    q1_art, q3_art = float(np.percentile(polyp_fr, 25)), float(np.percentile(polyp_fr, 75))
    seg = donor_pool(os.path.join(a.seg_dir, "masks")); ins = donor_pool(os.path.join(a.instrument_dir, "masks"))
    sf = np.array([d["frac"] for d in seg]); inf_ = np.array([d["frac"] for d in ins])
    pool = {"POL_Q1": [d for d in seg if d["frac"] <= np.percentile(sf, 25)], "POL_Q3": [d for d in seg if d["frac"] >= np.percentile(sf, 75)],
            "INS": [d for d in ins if np.percentile(inf_, 40) <= d["frac"] <= np.percentile(inf_, 60)]}
    sizes = {"polyp_area_frac_fov_inventory": {"n": len(polyp_fr), "q1": q1_art, "median": float(np.median(polyp_fr)), "q3": q3_art, "note": "sem mascara de artefato no mask_sources do inventario: ART usa retangulos 4:3 com area Q1/Q3 do FOV, alternados por imagem"},
             "kvasir_seg_masks": {"n": len(seg), "p25": float(np.percentile(sf, 25)), "p50": float(np.percentile(sf, 50)), "p75": float(np.percentile(sf, 75)), "pool_Q1": len(pool["POL_Q1"]), "pool_Q3": len(pool["POL_Q3"])},
             "kvasir_instrument_masks": {"n": len(ins), "p40": float(np.percentile(inf_, 40)), "p50": float(np.percentile(inf_, 50)), "p60": float(np.percentile(inf_, 60)), "pool_median": len(pool["INS"])}}
    print(json.dumps(sizes, indent=1), flush=True)
    # --- geracao
    os.makedirs(a.out_dir, exist_ok=True); os.makedirs(a.examples_dir, exist_ok=True)
    rows_out = {c: [] for c in CONDS}; rows_c0x = []; inv_rows = []
    answer_type_of = {}
    for row in df.itertuples(index=False):
        for q, t in zip(row.questions, row.answer_type): answer_type_of.setdefault(q, int(t))
    ex_rng = random.Random(a.seed); fails = collections.Counter()
    all_rows = sorted(set().union(*[set(r) for r in rows_by_set.values()]))
    ex_idx = set(ex_rng.sample(range(len(all_rows)), min(a.n_examples, len(all_rows))))
    with Pool(a.workers, initializer=_init, initargs=(df, rows_by_set, native_q_index, answer_type_of, pool, q1_art, q3_art, a.seed, ex_idx)) as P:
        for n_done, ro, ir, exs, fl, c0x in P.imap(_work, list(enumerate(all_rows)), chunksize=2):
            for c, rs in ro.items(): rows_out[c].extend(rs)
            inv_rows.extend(ir); fails.update(fl)
            if c0x: rows_c0x.append(c0x)
            for cond, iid, side in exs:
                os.makedirs(os.path.join(a.examples_dir, cond), exist_ok=True); Image.fromarray(side).save(os.path.join(a.examples_dir, cond, f"{iid}.png"))
            if n_done % 50 == 0: print(f"[{n_done}/{len(all_rows)}] {time.time() - t0:.0f}s", flush=True)
    assert all(q["qid"] is not None for u in inv_rows for q in u["questions"]), "pergunta cruzada sem qid nativo (nao esperado)"
    manifest = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "source_arrow": a.arrow, "source_sha256": sha256(a.arrow), "inventory_placebo": a.inventory, "seed": a.seed, "counts": counts, "sizes": sizes, "placement_failures": dict(fails),
                "fov": "masks.fov_mask(opening=0), >= 80 % da regiao dentro do FOV, inteira no quadro, translacao aleatoria (ate 50)", "encoding": {"C0_cross": "source bytes", "shams": "PNG lossless from decoded pixels"}, "cross_qid_start": CROSS_QID0, "n_cross_new_qids": 0, "conditions": {}}
    for cond in CONDS + ["C0_cross"]:
        rows = rows_c0x if cond == "C0_cross" else rows_out[cond]; fn = f"vqa_kvasir_sham_{cond}.arrow"; p = os.path.join(a.out_dir, fn)
        write_arrow(pd.DataFrame(rows), p)
        manifest["conditions"][cond] = {"file": fn, "sha256": sha256(p), "bytes": os.path.getsize(p), "n_rows": len(rows), "n_questions": int(sum(len(r["questions"]) for r in rows)),
                                        "n_cross_questions": int(sum(sum(1 for q in r["question_id"] if q >= CROSS_QID0) for r in rows))}
        print(cond, manifest["conditions"][cond], flush=True)
    json.dump({"params": vars(a), "counts": counts, "sizes": sizes, "placement_failures": dict(fails), "cross_qids": {}, "note_cross": "todas as perguntas cruzadas existem nativamente nas imagens (qids originais)", "units": inv_rows}, open(a.inventory_out, "w"), indent=1)
    json.dump(manifest, open(a.manifest, "w"), indent=1); print("FIM", round(time.time() - t0), "s")
if __name__ == "__main__": main()
