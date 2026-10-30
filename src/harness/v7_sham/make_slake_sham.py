"""P2.3 (2026-10-09, selection redone at 20:40 at the authors' request): SLAKE occluder test (`sham` in the code) -- the negative is the IMAGE WITHOUT DISEASE,
selected by template POLARITY among the closed-ended (yes/no) dependent_disease questions: "healthy" polarity (gold
"yes" = no disease: "Is the lung healthy?", "Does this image look normal?", "... normal appearing?" etc.) and "presence"
polarity (gold "no" = without the queried disease: "Can X be observed ...?", "Does ... look abnormal?", "Is there any
abnormality ...?", "Are there abnormalities ...?", "Does the patient have ...?" etc.). Template, polarity and gold are
recorded per item; "affirms" in the analysis = answer that affirms disease = gold inverted per template ("no" in the
healthy ones, "yes" in the presence ones). Does not require `evaluable` from the control-occlusion inventory (which required a disease
region in the image itself; the negative does not have one). DONOR disease mask from ANOTHER evaluable image of the inventory
(seeded draw per image; image area fraction preserved), positioned by the rule of the SLAKE P (FOV per modality with opening 4,
>= 95 % in the FOV, X-ray = whole frame); fills black and blur10. Conditions: SHAM_DIS_black, SHAM_DIS_blur10."""
from __future__ import annotations
import argparse, collections, hashlib, io, json, os, re, time
import numpy as np, pandas as pd
from PIL import Image
from harness.interventions.arrow_io import read_arrow, write_arrow
from harness.isbi_placebo.conditions import fill_region, encode_png
from harness.isbi_placebo.inventory_slake import entity_regions, read_legend, fov_for_modality
from harness.v7_sham.make_kvasir_sham import sha256, image_seed, scaled_crop, place, gold

HEALTHY_RE = re.compile(r"\b(healthy|normal)\b", re.I); PRESENCE_RE = re.compile(r"abnormal|observed|evidence|is there|are there|is/are there|does the patient have", re.I)
def polarity(q):
    if "abnormal" not in q.lower() and HEALTHY_RE.search(q): return "healthy"
    if PRESENCE_RE.search(q): return "presence"
    return None

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--arrow", required=True); ap.add_argument("--inventory", required=True); ap.add_argument("--slake-root", required=True)
    ap.add_argument("--out-dir", required=True); ap.add_argument("--examples-dir", required=True); ap.add_argument("--inventory-out", required=True); ap.add_argument("--manifest", required=True); ap.add_argument("--seed", type=int, default=20260913)
    a = ap.parse_args(); t0 = time.time()
    df = read_arrow(a.arrow); inv = json.load(open(a.inventory)); legend = read_legend(os.path.join(a.slake_root, "mask.txt"))
    rowq = {}; atype = {}
    for ri, row in enumerate(df.itertuples(index=False)):
        for qi, (q, ans, qid, t) in enumerate(zip(row.questions, row.answers, row.question_id, row.answer_type)): rowq[int(qid)] = (ri, qi); atype[int(qid)] = int(t)
    items = []; dropped = collections.Counter()
    for q in inv["questions"]:
        if q["question_class"] != "dependent_disease" or atype[q["qid"]] != 0: continue
        g = gold(df.iloc[rowq[q["qid"]][0]].answers[rowq[q["qid"]][1]]); pol = polarity(q["question"])
        if g not in ("yes", "no"): dropped["gold_not_yes_no"] += 1; continue
        if pol is None: dropped["template_sem_polaridade:" + q["question"]] += 1; continue
        if (pol == "healthy" and g == "yes") or (pol == "presence" and g == "no"):
            items.append({**q, "gold": g, "polarity": pol, "affirms_disease_answer": "no" if pol == "healthy" else "yes"})
        else: dropped["com_doenca"] += 1
    counts = {"n_negatives_selected": len(items), "by_polarity": dict(collections.Counter(i["polarity"] for i in items)), "placebo_evaluable_among_selected": sum(bool(i["evaluable"]) for i in items),
              "templates": [(t, n) for t, n in collections.Counter("%s | %s | gold %s" % (i["question"], i["polarity"], i["gold"]) for i in items).most_common()], "dropped": dict(dropped), "n_images": len({i["image_id"] for i in items})}
    # donors: disease regions of the evaluable dependent_disease units (any gold), per image
    donors = {}
    for q in inv["questions"]:
        if q["question_class"] == "dependent_disease" and q["evaluable"] and q["target_entities"]:
            key = (q["image_id"], tuple(q["target_entities"]))
            if key in donors: continue
            regs = entity_regions(os.path.join(a.slake_root, "imgs", q["image_id"]), legend)
            try: m = np.logical_or.reduce([regs[n.lower()]["mask"] for n in q["target_entities"]])
            except KeyError: continue
            if m.any(): donors[key] = {"mask": m, "frac": float(m.sum() / m.size), "source": q["region_source"]}
    dkeys = sorted(donors); counts["donor_pool"] = len(dkeys); print(json.dumps(counts, indent=1), flush=True)
    os.makedirs(a.out_dir, exist_ok=True); rows_out = {"SHAM_DIS_black": [], "SHAM_DIS_blur10": []}; recs = []; fails = collections.Counter(); ex = 0
    by_row = collections.defaultdict(list)
    for q in items: by_row[rowq[q["qid"]][0]].append(q)
    for ri, qs in sorted(by_row.items()):
        row = df.iloc[ri]; img = np.array(Image.open(io.BytesIO(row.image)).convert("RGB")); H, W = img.shape[:2]; xm = re.search(r"(xmlab\d+)", row.image_id).group(1)
        fov = fov_for_modality(img, qs[0].get("modality"), opening=4) if not qs[0].get("xray") else np.ones((H, W), bool)
        rng = np.random.default_rng(image_seed(a.seed, xm)); pool = [k for k in dkeys if k[0] != xm]; d = donors[pool[int(rng.integers(0, len(pool)))]]
        region, pl = place(scaled_crop(d["mask"], d["frac"] * H * W), fov, rng, min_fov_frac=0.95)
        idxs = [rowq[q["qid"]][1] for q in qs]
        for fill in ("black", "blur10"):
            cond = "SHAM_DIS_" + fill
            rec = {"image_id": xm, "condition": cond, "fill": fill, "donor_image": pool and d and [k for k in pool if donors[k] is d][0][0], "donor_entities": [k for k in pool if donors[k] is d][0][1], "donor_frac": d["frac"], "donor_source": d["source"], "placement": pl, "height": H, "width": W, "fov_px": int(fov.sum()), "xray": bool(qs[0].get("xray")), "modality": qs[0].get("modality"),
                   "questions": [{"qid": q["qid"], "question": q["question"], "gold": q["gold"], "polarity": q["polarity"], "affirms_disease_answer": q["affirms_disease_answer"], "placebo_evaluable": q["evaluable"], "target_entities_in_inventory": q["target_entities"]} for q in qs], "seed_image": image_seed(a.seed, xm)}
            if region is None: fails[cond] += 1; rec["generated"] = False; recs.append(rec); continue
            out = fill_region(img, region, fill); rec["generated"] = True; rec["region_px"] = int(region.sum()); recs.append(rec)
            rows_out[cond].append({"image": encode_png(out), "questions": [row.questions[i] for i in idxs], "answers": [list(row.answers[i]) for i in idxs], "answer_labels": [list(row.answer_labels[i]) for i in idxs], "answer_scores": [[float(x) for x in row.answer_scores[i]] for i in idxs], "image_id": row.image_id, "question_id": [int(row.question_id[i]) for i in idxs], "answer_type": [int(row.answer_type[i]) for i in idxs], "split": "test"})
            if ex < 24: os.makedirs(os.path.join(a.examples_dir, cond), exist_ok=True); Image.fromarray(np.concatenate([img, np.zeros((H, 8, 3), np.uint8) + 255, out], axis=1)).save(os.path.join(a.examples_dir, cond, f"{xm}.png")); ex += 1
    man = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "source_arrow": a.arrow, "source_sha256": sha256(a.arrow), "inventory_placebo": a.inventory, "seed": a.seed, "counts": {k: (v if not isinstance(v, list) else v) for k, v in counts.items()}, "placement_failures": dict(fails),
           "note": "selecao por polaridade do template (negativo = imagem sem doenca); 'afirma' = gold invertido por template", "conditions": {}}
    for cond, rows in rows_out.items():
        fn = f"vqa_slake_sham_{cond}.arrow"; p = os.path.join(a.out_dir, fn); write_arrow(pd.DataFrame(rows), p)
        man["conditions"][cond] = {"file": fn, "sha256": sha256(p), "bytes": os.path.getsize(p), "n_rows": len(rows), "n_questions": int(sum(len(r["questions"]) for r in rows))}; print(cond, man["conditions"][cond])
    json.dump({"params": vars(a), "counts": man["counts"], "units": recs}, open(a.inventory_out, "w"), indent=1); json.dump(man, open(a.manifest, "w"), indent=1); print("FIM", round(time.time() - t0), "s")
if __name__ == "__main__": main()
