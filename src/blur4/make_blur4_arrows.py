"""Round 10, item A2 (21/10/2026, CPU): T_blur and P_blur arrows (Gaussian blur with a fixed sigma per benchmark) for HEAL-MedVQA and Medical-Diff-VQA,
with the same functions as the original generators (harness/isbi_placebo/conditions.fill_region and encode_png; masks from
harness/isbi_placebo/heal/make_heal_conditions and from v7_mimic/scripts/17_make_mimic_conditions.py), same seed, same units and order.
Sigma rule: the Kvasir-VQA-x1 one (T_blur/P_blur = fixed sigma of 25 px at the working resolution, median sigma/width ratio 0.039936):
sigma of the benchmark = 0.039936 x median width of the unit images at the working resolution (the PNG in the arrow). With a fixed 25 px the ratio
on the radiographs would be far from 0.040 (recorded in the manifest). Proof that masks and units are the same: the T (black) is regenerated
here and compared byte by byte with the existing T arrow, unit by unit. Output: <task directory>/data/."""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import hashlib, importlib.util, io, json, os, statistics, sys, time
from concurrent.futures import ProcessPoolExecutor
import numpy as np, pandas as pd, pyarrow as pa
from PIL import Image
from scipy import ndimage
W = os.environ.get("LAB_ROOT", "LAB_ROOT") + ""; PLC = f"{W}/doutorado/med-vqa-icdip-placebo"; sys.path.insert(0, PLC)
from harness.interventions.arrow_io import write_arrow
from harness.isbi_placebo.conditions import fill_region, encode_png
TASK = f"{W}/v7_txt/extra_runs/blur4_r10"; OUTD = f"{TASK}/data"; os.makedirs(OUTD, exist_ok=True)
# the annotation parquet is no longer in data/isbi_placebo/heal/ on the lab server; copy in v7_artigo1/inputs (sha f893df9b..., brought in round 1); the identity of the black T proves the masks
ANN_HEAL = f"{W}/v7_artigo1/inputs/heal_annotations_test.parquet"
KV_RATIO = json.load(open(f"{PLC}/results/isbi_placebo/blur_sigma_report.json"))["datasets"]["kvasir"]["sigma_over_width"]["median"]
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""): h.update(b)
    return h.hexdigest()
def table(p):
    s = pa.memory_map(p)
    try: return pa.ipc.open_file(s).read_all()
    except Exception: return pa.ipc.open_stream(pa.memory_map(p)).read_all()
def key(iid, qids): return (iid, tuple(qids))
# ---------------- HEAL
def heal_ctx():
    from harness.isbi_placebo.heal import make_heal_conditions as MH
    from harness.isbi_placebo.heal.heal_rle import decode_rle, resize_mask
    return MH, decode_rle, resize_mask
HEAL = {}
def heal_unit(args):
    u, ev, png_path, sigma = args
    MH, decode_rle, resize_mask = heal_ctx()
    png_bytes = open(png_path, "rb").read(); gray = np.asarray(Image.open(io.BytesIO(png_bytes)).convert("L"), np.uint8); rgb = np.stack([gray] * 3, axis=-1); H, Wd = gray.shape
    native = {a: decode_rle(*HEAL["rle"][(u["image_id"], a)]) for a in u["anatomies"]}
    by = {}
    for q in ev: by.setdefault(q["anatomy"], []).append(q)
    out = []
    for anatomy, ql in by.items():
        t_nat = native[anatomy]; method = ql[0]["placebo"]["method"]
        p_nat = MH.placebo_mask(t_nat, method, {a: m for a, m in native.items() if a != anatomy})
        t, pl = resize_mask(t_nat, H, Wd), resize_mask(p_nat, H, Wd)
        base = {"questions": [q["question"] for q in ql], "answers": [[q["answer"]] for q in ql], "answer_labels": [[MH.ANSWER_LABEL[q["answer"]]] for q in ql], "answer_scores": [[1.0] for _ in ql],
                "image_id": f"heal/{u['image_id']}#{anatomy}", "question_id": [q["qid"] for q in ql], "answer_type": [0] * len(ql), "split": "test"}
        out.append((base, encode_png(fill_region(rgb, t, "black")), encode_png(fill_region(rgb, t, "blur", blur_sigma=sigma)), encode_png(fill_region(rgb, pl, "blur", blur_sigma=sigma)), Wd))
    return out
def do_heal():
    global HEAL
    man = json.load(open(f"{PLC}/results/isbi_placebo/manifest_heal.json")); inv = json.load(open(f"{PLC}/results/isbi_placebo/inventory_heal_test.json"))
    ann = pd.read_parquet(ANN_HEAL, columns=["image_id", "anatomy", "mask_rle", "mask_h", "mask_w"])
    HEAL["rle"] = {(r.image_id, r.anatomy): (r.mask_rle, int(r.mask_h), int(r.mask_w)) for r in ann.itertuples(index=False)}
    medW = statistics.median(u["png_hw"][1] for u in man["units"]); sigma = KV_RATIO * medW
    qs = {q["qid"]: q for q in inv["questions"]}; png_dir = f"{W}/doutorado/data/derived/heal_png/test"
    jobs = []
    for u in inv["units"]:
        ev = [qs[q] for q in u["qids"] if qs[q]["evaluable"]]
        if ev: jobs.append((u, ev, f"{png_dir}/{u['image_id']}.png", sigma))
    rows = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for r in ex.map(heal_unit, jobs, chunksize=4): rows.extend(r)
    return rows, sigma, medW, f"{PLC}/data/isbi_placebo/vqa_heal_placebo_T.arrow", "heal"
# ---------------- MIMIC
def mimic_mod():
    spec = importlib.util.spec_from_file_location("mk17", f"{W}/v7_mimic/scripts/17_make_mimic_conditions.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
MM = None
def mimic_unit(args):
    global MM
    if MM is None: MM = mimic_mod()
    u, qs, sigma = args; png = (MM.DER / "test" / u["png"]).read_bytes()
    gray = np.asarray(Image.open(io.BytesIO(png)).convert("L"), np.uint8); rgb = np.stack([gray] * 3, -1); H, Wd = gray.shape
    t = np.any([MM.box(u["all_boxes_png"][r], H, Wd) for r in u["target_regions"]], axis=0); m = u["placebo_method"]
    if u.get("placebo_scheme") == "per_box": p = np.any([MM.box(b, H, Wd) for b in u["placebo_boxes_png"]], axis=0)
    else: p = MM.box(u["all_boxes_png"][m.split(":", 1)[1]], H, Wd) if m.startswith("anatomy:") else MM.apply_placement(t, m)
    bl = np.clip(np.round(ndimage.gaussian_filter(gray.astype(np.float32), sigma)), 0, 255).astype(np.uint8); blurred = np.stack([bl] * 3, -1)
    base = {"questions": [q["question"] for q in qs], "answers": [[q["answer"]] for q in qs], "answer_labels": [[MM.VOCAB[q["answer"]]] for q in qs], "answer_scores": [[1.0] for _ in qs],
            "image_id": f"mimic/{u['image_id']}#{'+'.join(u['target_regions'])}", "question_id": [q["qid"] for q in qs], "answer_type": [1 if q["question_class"] == "open" else 0 for q in qs], "split": "test"}
    return [(base, encode_png(MM.fill_region(rgb, t, "black")), encode_png(MM.blur_fill(rgb, blurred, t)), encode_png(MM.blur_fill(rgb, blurred, p)), Wd)]
def png_w(args):
    global MM
    if MM is None: MM = mimic_mod()
    return Image.open(MM.DER / "test" / args[0]["png"]).size[0]
def do_mimic():
    global MM
    MM = mimic_mod(); inv = json.load(open(f"{W}/v7_mimic/results/inventory_mimic_test.json")); Q = {q["qid"]: q for q in inv["questions"]}
    jobs = []
    for u in inv["units"]:
        qs = [Q[i] for i in u["qids"] if Q[i]["evaluable"] and Q[i]["question_class"] != "closed_no_sham"]
        if qs: jobs.append((u, qs))
    with ProcessPoolExecutor(max_workers=8) as ex: widths = list(ex.map(png_w, jobs, chunksize=16))
    medW = statistics.median(widths); sigma = KV_RATIO * medW; rows = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for r in ex.map(mimic_unit, [(u, qs, sigma) for u, qs in jobs], chunksize=4): rows.extend(r)
    return rows, sigma, medW, f"{W}/v7_mimic/data/conditions/vqa_mimic_placebo_T.arrow", "mimic"
def finish(rows, sigma, medW, t_arrow, name):
    tT = table(t_arrow); old = {key(i, q): b for i, q, b in zip(tT.column("image_id").to_pylist(), tT.column("question_id").to_pylist(), (x.as_py() for x in tT.column("image")))}
    order = [key(i, q) for i, q in zip(tT.column("image_id").to_pylist(), tT.column("question_id").to_pylist())]
    mine = {key(b["image_id"], b["question_id"]): (b, tb, tbl, pbl, wd) for b, tb, tbl, pbl, wd in rows}
    assert set(mine) == set(order), (name, len(mine), len(order))
    px = lambda by: np.asarray(Image.open(io.BytesIO(by)).convert("RGB"))   # PNG bytes change with the zlib/PIL version; the proof is pixel by pixel
    same = sum(1 for k in order if np.array_equal(px(mine[k][1]), px(old[k]))); same_bytes = sum(1 for k in order if mine[k][1] == old[k])
    out = {"base": name, "sigma_px": sigma, "largura_mediana_px": medW, "razao_sigma_largura_mediana": sigma / medW, "razao_kvasir": KV_RATIO,
           "razao_se_fossem_25px": 25.0 / medW, "razao_por_unidade": {"min": min(sigma / mine[k][4] for k in order), "max": max(sigma / mine[k][4] for k in order)},
           "unidades": len(order), "T_preto_pixels_identicos_ao_arrow_existente": f"{same}/{len(order)}", "T_preto_bytes_png_identicos": f"{same_bytes}/{len(order)}", "T_arrow_existente": t_arrow, "T_arrow_existente_sha256": sha(t_arrow), "arrows": {}}
    assert same == len(order), out
    for c, idx in (("T_blur", 2), ("P_blur", 3)):
        f = f"{OUTD}/vqa_{name}_placebo_{c}.arrow"; write_arrow(pd.DataFrame([{**mine[k][0], "image": mine[k][idx]} for k in order])[list(tT.schema.names)], f)
        out["arrows"][c] = {"file": f, "sha256": sha(f), "bytes": os.path.getsize(f), "n_units": len(order)}
    return out
if __name__ == "__main__":
    T0 = time.time(); res = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "script": __file__, "script_sha256": sha(__file__), "seed": 20260913}
    for fn in (do_heal, do_mimic):
        r = finish(*fn()); res[r["base"]] = r; print(json.dumps({k: v for k, v in r.items() if k != "arrows"}), {c: (v["bytes"], v["sha256"][:12]) for c, v in r["arrows"].items()}, round(time.time() - T0), "s", flush=True)
    json.dump(res, open(f"{OUTD}/manifest_blur4_r10.json", "w"), indent=1); print("FIM", round(time.time() - T0), "s")
