"""14/10/2026 (authors, approved): HEAL dose inventory, on CPU, without arrows. Same rule as Kvasir and MIMIC v2:
harness.isbi_placebo.masks.place_placebos_by_factor -- target dilated in place (dilate_to_area, factors 1.5 and 2 in area over the target mask),
control occlusion (`placebo` in the code) RE-PLACED to the dilated shape with exact area, >= 80 % inside the HEAL thoracic atlas (thorax_atlas_256.npy via atlas_for_shape),
no overlap with the dilated target (+5 px), dilated target <= 40 % of the FOV; seed 20260913, 50 random translations (function defaults).
Unit = (image, anatomy) from the control-occlusion manifest (1 360 units, 1 446 evaluable questions). Masks from the parquet reconstituted on 14/10
(v7_txt/data/heal/heal_annotations_test.parquet); resolution = that of the published C0 PNG. Paired subset = units valid at all three levels
(1x = the published control occlusion, valid for all evaluable questions; 1.5x; 2x). STOPPING POINT: only counts per class and per anatomy."""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import collections, hashlib, io, json, os, sys, time
from multiprocessing import Pool
sys.path.insert(0, os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-placebo")
import numpy as np, pandas as pd
from PIL import Image
from harness.isbi_placebo.masks import place_placebos_by_factor
from harness.isbi_placebo.heal.heal_rle import decode_rle, resize_mask
from harness.isbi_placebo.heal.thorax_atlas import atlas_for_shape
from harness.interventions.arrow_io import read_arrow
PL = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-placebo"; V7 = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt"; SEED = 20260913
ANN = f"{V7}/data/heal/heal_annotations_test.parquet"; ATLAS = np.load(f"{PL}/data/isbi_placebo/heal/thorax_atlas_256.npy")
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""): h.update(b)
    return h.hexdigest()
ann = pd.read_parquet(ANN, columns=["image_id", "anatomy", "mask_rle", "mask_h", "mask_w"]).drop_duplicates(["image_id", "anatomy"])
RLE = {(r.image_id, r.anatomy): (list(r.mask_rle), int(r.mask_h), int(r.mask_w)) for r in ann.itertuples(index=False)}
df = read_arrow(f"{PL}/data/isbi_placebo/vqa_heal_placebo_C0.arrow"); HW = {}
for k, b in zip(df["image_id"], df["image"]): HW[k] = Image.open(io.BytesIO(b)).size[::-1]
def do(u):
    k = f"heal/{u['image_id']}#{u['anatomy']}"; H, W = HW[k]; r, h, w = RLE[(u["image_id"], u["anatomy"])]
    t = resize_mask(decode_rle(r, h, w), H, W); fov = atlas_for_shape(ATLAS, H, W)
    meth, why = place_placebos_by_factor(t, fov, seed=SEED)
    return {"unit": k, "image_id": u["image_id"], "anatomy": u["anatomy"], "qids": u["qids"], "methods": meth, "reasons": why, "target_area_frac_fov": float((t & fov).sum() / max(fov.sum(), 1))}
def main():
    mh = json.load(open(f"{PL}/results/isbi_placebo/manifest_heal.json")); inv = json.load(open(f"{PL}/results/isbi_placebo/inventory_heal_test.json"))
    qcls = {q["qid"]: q["question_class"] for q in inv["questions"]}
    t0 = time.time()
    with Pool(8) as p: units = p.map(do, mh["units"], chunksize=8)
    S = {"por_nivel": {}, "motivos": collections.Counter(), "por_classe": {}, "por_anatomia": {}}
    def ok(u, lv): return all(u["methods"][k] for k in lv)
    for nome, lv in (("1.5", ["1.5"]), ("2", ["2"]), ("pareado", ["1.5", "2"])):
        sel = [u for u in units if ok(u, lv)]; S["por_nivel"][nome] = {"unidades": len(sel), "perguntas": sum(len(u["qids"]) for u in sel)}
        pc = collections.Counter(qcls[q] for u in sel for q in u["qids"]); S["por_classe"][nome] = dict(pc)
        pa = collections.defaultdict(lambda: [0, 0])
        for u in sel: pa[u["anatomy"]][0] += 1; pa[u["anatomy"]][1] += len(u["qids"])
        S["por_anatomia"][nome] = {a: {"unidades": v[0], "perguntas": v[1]} for a, v in sorted(pa.items())}
    S["base"] = {"unidades": len(units), "perguntas": sum(len(u["qids"]) for u in units), "por_classe": dict(collections.Counter(qcls[q] for u in units for q in u["qids"])),
                 "por_anatomia": {a: {"unidades": sum(1 for u in units if u["anatomy"] == a), "perguntas": sum(len(u["qids"]) for u in units if u["anatomy"] == a)} for a in sorted({u["anatomy"] for u in units})}}
    for u in units:
        for k, r in u["reasons"].items():
            if r: S["motivos"][f"{k}:{r}"] += 1
    S["motivos"] = dict(S["motivos"])
    out = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "script": __file__, "script_sha256": sha(__file__), "anotacoes": {"path": ANN, "sha256": sha(ANN)}, "atlas": f"{PL}/data/isbi_placebo/heal/thorax_atlas_256.npy",
           "regra": "place_placebos_by_factor(t, atlas_for_shape(ATLAS, H, W), seed=20260913): n_random 50, margin 5 px, min_fov_frac 0.8, max_area_frac 0.4, fatores 1.5 e 2", "segundos": round(time.time() - t0, 1), "resumo": S, "unidades": units}
    json.dump(out, open(f"{V7}/analysis/heal_dose_inventory.json", "w"), indent=1)
    print(json.dumps({"segundos": out["segundos"], **S}, indent=1))
if __name__ == "__main__": main()
