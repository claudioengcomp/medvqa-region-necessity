"""diagnosis of the per-box v2 rule: why each target box finds no control occlusion (units with exclusion reason 'sem placebo por caixa')."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json, zipfile, collections, sys
from pathlib import Path
import numpy as np, pandas as pd
from scipy import ndimage
sys.path.insert(0, os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic/scripts")
import importlib; inv_mod = importlib.import_module("16_inventory_mimic")
from harness.isbi_placebo.heal.thorax_atlas import atlas_for_shape
V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic"); RAW = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/raw/chest-imagenome/1.0.0"); DER = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/derived/mimic_png")
inv = json.load(open(V7 / "results/inventory_mimic_test.json")); Q = inv["questions"]
emap = json.load(open(V7 / "analysis/entity_map.json"))["entity_map"]
z = zipfile.ZipFile(RAW / "silver_dataset/scene_graph.zip"); sg = {Path(n).name.replace("_SceneGraph.json", ""): n for n in z.namelist() if n.endswith("_SceneGraph.json")}
pm = json.load(open(DER / "png_manifest_test.json"))["items"]; atlas = np.load(V7 / "data/thorax_atlas_mimic_256.npy")
fail = [q for q in Q if q["exclusion_reason"] == "sem placebo por caixa"]
print("unidades/perguntas falhas:", len(fail), "| n caixas:", dict(collections.Counter(len(q["target_regions"]) for q in fail)))
print("conjuntos-alvo mais comuns:", collections.Counter(tuple(q["target_regions"]) for q in fail).most_common(8))
why_box = collections.Counter(); why_region = collections.Counter(); first_fail = collections.Counter(); cache = {}
for q in fail[:600]:
    d = q["image_id"]; it = pm[d]; H, W = it["png_h"], it["png_w"]
    if d not in cache:
        g = json.loads(z.read(sg[d])); objs = {o["bbox_name"]: o for o in g["objects"]}; agg = inv_mod.aggregate_last(g)
        boxes = {}; masks = {}
        for n, o in objs.items():
            m, b = inv_mod.box_mask(o, it, H, W)
            if m.any(): boxes[n] = b; masks[n] = m
        cache[d] = (boxes, masks, agg, atlas_for_shape(atlas, H, W))
    boxes, masks, agg, fov = cache[d]
    attrs = emap.get(q["entity"], {}).get("attrs", []); attr_yes = {b for (b, k), c in agg.items() if c == "yes" and k in attrs}
    target = np.any([masks[r] for r in q["target_regions"]], axis=0); forbidden = ndimage.binary_dilation(target, iterations=5)
    used = set(); taken = np.zeros_like(target); failed_here = False
    for r in q["target_regions"]:
        tb = boxes[r]; ta = (tb[2]-tb[0])*(tb[3]-tb[1]); reasons = []
        for c in inv_mod.box_candidates(r, q["target_regions"]):
            if c in q["target_regions"]: reasons.append(f"{c}:no_alvo"); continue
            if c in attr_yes: reasons.append(f"{c}:tem_atributo"); continue
            if c not in boxes: reasons.append(f"{c}:sem_caixa"); continue
            if c in used: reasons.append(f"{c}:ja_usada"); continue
            cb = boxes[c]; ratio = (cb[2]-cb[0])*(cb[3]-cb[1])/ta
            if not (0.8 <= ratio <= 1.25): reasons.append(f"{c}:area_{ratio:.2f}"); continue
            m = masks[c]
            if (m & forbidden).any(): reasons.append(f"{c}:sobrepoe_alvo_{(m&target).sum()/m.sum():.2f}"); continue
            if (m & taken).any(): reasons.append(f"{c}:sobrepoe_placebo"); continue
            if (m & fov).sum()/m.sum() < 0.8: reasons.append(f"{c}:fora_atlas"); continue
            reasons.append(f"{c}:OK"); used.add(c); taken |= m; break
        if not reasons or not reasons[-1].endswith(":OK"):
            hb = [W-tb[2], tb[1], W-tb[0], tb[3]]; m = np.zeros((H, W), bool); m[hb[1]:hb[3], hb[0]:hb[2]] = True
            if (m & forbidden).any(): hr = f"hflip:sobrepoe_alvo_{(m&target).sum()/m.sum():.2f}"
            elif (m & taken).any(): hr = "hflip:sobrepoe_placebo"
            elif (m & fov).sum()/m.sum() < 0.8: hr = "hflip:fora_atlas"
            else: hr = "hflip:OK"; taken |= m
            reasons.append(hr)
        if not reasons[-1].endswith(":OK") and not failed_here:
            failed_here = True; first_fail[(r, reasons[-1].split(":")[0] + ":" + reasons[-1].split(":")[1].split("_")[0])] += 1
            for x in reasons: why_box[x.split(":")[1].split("_")[0] if not x.startswith("hflip") else "hflip_" + x.split(":")[1].split("_")[0]] += 1
            why_region[r] += 1
print("\nprimeira caixa que falha (regiao, ultimo motivo):"); [print(" ", k, v) for k, v in first_fail.most_common(15)]
print("\nmotivos de rejeicao de candidatas na caixa que falha:", dict(why_box.most_common()))
print("\nregiao-alvo que falha:", dict(why_region.most_common(10)))
