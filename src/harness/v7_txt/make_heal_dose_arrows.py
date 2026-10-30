"""14/10/2026 (authors, approved): HEAL dose arrows -- T1.5, P1.5, T2, P2, S2 -- on the paired subset of the inventory
(v7_txt/analysis/heal_dose_inventory.json: units valid at 1.5x and 2x; 879 units / 938 questions). Images by the same function as the Kvasir and SLAKE
doses (harness.isbi_placebo.conditions.make_condition_image): T = dilated target in black; P = control occlusion (`placebo`) re-placed to the dilated
shape (apply_placement(dilate_to_area(target, factor), method from the inventory)); S2 = everything outside the 2x dilated target in black. Each row is the one of the
published C0 arrow (vqa_heal_placebo_C0.arrow) with the image replaced (lossless PNG). Masks from the reconstituted parquet (E11).
Outputs: v7_txt/data/heal_dose/vqa_heal_placebo_{cond}.arrow + manifest_heal_dose.json (sha256 of each arrow, of the sources and of the script);
validation with load_condition_dataset (938 items per arrow). HEAL images never leave gpu1."""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import hashlib, io, json, os, socket, sys, time
from multiprocessing import Pool
sys.path.insert(0, os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-placebo")
import numpy as np, pandas as pd
from PIL import Image
from harness.isbi_placebo.conditions import make_condition_image, apply_placement, encode_png
from harness.isbi_placebo.masks import dilate_to_area
from harness.isbi_placebo.heal.heal_rle import decode_rle, resize_mask
from harness.interventions.arrow_io import read_arrow, write_arrow, count_questions
PL = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-placebo"; V7 = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt"; OUT = V7 + "/data/heal_dose"
CONDS = ["T1.5", "P1.5", "T2", "P2", "S2"]; INV = V7 + "/analysis/heal_dose_inventory.json"; ANN = V7 + "/data/heal/heal_annotations_test.parquet"
C0A = f"{PL}/data/isbi_placebo/vqa_heal_placebo_C0.arrow"
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""): h.update(b)
    return h.hexdigest()
ann = pd.read_parquet(ANN, columns=["image_id", "anatomy", "mask_rle", "mask_h", "mask_w"]).drop_duplicates(["image_id", "anatomy"])
RLE = {(r.image_id, r.anatomy): (list(r.mask_rle), int(r.mask_h), int(r.mask_w)) for r in ann.itertuples(index=False)}
DF = read_arrow(C0A); ROW = {k: i for i, k in enumerate(DF["image_id"])}
def do(u):
    k = u["unit"]; row = DF.iloc[ROW[k]]; img = np.array(Image.open(io.BytesIO(row["image"])).convert("RGB")); H, W = img.shape[:2]
    r, h, w = RLE[(u["image_id"], u["anatomy"])]; t = resize_mask(decode_rle(r, h, w), H, W)
    pbf = {float(f): apply_placement(dilate_to_area(t, float(f)), m) for f, m in u["methods"].items()}
    out = {}
    for c in CONDS:
        im, info = make_condition_image(img, t, None, c, placebo_by_factor=pbf); out[c] = (encode_png(im), info["region_px"], info["overlaps_target"])
    return k, out
def main():
    inv = json.load(open(INV)); units = [u for u in inv["unidades"] if all(u["methods"].get(f) for f in ("1.5", "2"))]
    assert len(units) == 879 and sum(len(u["qids"]) for u in units) == 938, (len(units), sum(len(u["qids"]) for u in units))
    os.makedirs(OUT, exist_ok=False); t0 = time.time()
    with Pool(8) as p: res = dict(p.map(do, units, chunksize=8))
    man = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "host": socket.gethostname(), "script": __file__, "script_sha256": sha(__file__), "inventario": {"path": INV, "sha256": sha(INV)},
           "anotacoes": {"path": ANN, "sha256": sha(ANN)}, "c0_publicado": {"path": C0A, "sha256": sha(C0A)}, "unidades": len(units), "perguntas": 938, "encoding": "PNG sem perda", "arrows": {}}
    from harness.circle_data_bridge import load_condition_dataset
    for c in CONDS:
        rows = []
        for u in units:
            row = DF.iloc[ROW[u["unit"]]].to_dict(); row["image"] = res[u["unit"]][c][0]; rows.append(row)
        df = pd.DataFrame(rows, columns=list(DF.columns)); o = f"{OUT}/vqa_heal_placebo_{c}.arrow"; write_arrow(df, o)
        n_ds = len(load_condition_dataset(o)); ov = sum(1 for u in units if res[u["unit"]][c][2])
        man["arrows"][c] = {"file": o, "sha256": sha(o), "n_rows": len(df), "n_questions": count_questions(df), "load_condition_dataset_n": n_ds, "n_overlap_flagged": ov, "bytes": os.path.getsize(o)}
        assert count_questions(df) == 938 and n_ds == 938, (c, count_questions(df), n_ds)
        print(c, man["arrows"][c], flush=True)
    man["segundos"] = round(time.time() - t0, 1); json.dump(man, open(f"{OUT}/manifest_heal_dose.json", "w"), indent=1); print("FIM", man["segundos"])
if __name__ == "__main__": main()
