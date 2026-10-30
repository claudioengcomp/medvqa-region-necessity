"""v7_mimic/scripts/15_entity_map.py -- 2026-10-11 -- mapping entity (Diff-VQA) -> attributes (ImaGenome), <loc> -> regions,
and validation (sensitivity/specificity) on the gold (gold_object_attribute_with_coordinates.txt x Diff-VQA presence questions)
and on the silver (scene graphs x test questions "is there <e>?"). Outputs: analysis/entity_map.json, docs/entity_map.md,
analysis/entity_validation.json. Does not decide cutoffs."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json, re, zipfile, collections
from pathlib import Path
import pandas as pd
RAW = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/raw/chest-imagenome/1.0.0"); V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic")
DV = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/raw/medical-diff-vqa/1.0.1")

# ---- entity -> ImaGenome attributes (category|label). status: exact | approx | none
ENTITY_MAP = {
    "atelectasis": {"attrs": ["anatomicalfinding|atelectasis", "anatomicalfinding|linear/patchy atelectasis", "anatomicalfinding|lobar/segmental collapse"], "status": "exact", "note": "inclui variantes linear/patchy e colapso lobar/segmentar"},
    "pleural effusion": {"attrs": ["anatomicalfinding|pleural effusion"], "status": "exact", "note": ""},
    "lung opacity": {"attrs": ["anatomicalfinding|lung opacity", "anatomicalfinding|airspace opacity"], "status": "exact", "note": "lung opacity é pai de consolidation/atelectasis/edema na ontologia (propagado pelos autores)"},
    "cardiomegaly": {"attrs": ["anatomicalfinding|enlarged cardiac silhouette"], "status": "exact", "note": ""},
    "edema": {"attrs": ["anatomicalfinding|pulmonary edema/hazy opacity"], "status": "exact", "note": ""},
    "pneumonia": {"attrs": ["disease|pneumonia"], "status": "exact", "note": "categoria disease"},
    "consolidation": {"attrs": ["anatomicalfinding|consolidation"], "status": "exact", "note": ""},
    "vascular congestion": {"attrs": ["anatomicalfinding|vascular congestion"], "status": "exact", "note": "vascular redistribution deixado fora"},
    "pneumothorax": {"attrs": ["anatomicalfinding|pneumothorax", "anatomicalfinding|hydropneumothorax"], "status": "exact", "note": ""},
    "infection": {"attrs": ["disease|pneumonia"], "status": "approx", "note": "Diff-VQA usa 'infection' como sinônimo de pneumonia/infecção; ImaGenome não tem rótulo próprio"},
    "calcification": {"attrs": ["anatomicalfinding|vascular calcification", "anatomicalfinding|calcified nodule"], "status": "approx", "note": "Diff-VQA não distingue calcificação vascular de nódulo calcificado"},
    "fracture": {"attrs": ["anatomicalfinding|rib fracture", "anatomicalfinding|clavicle fracture", "anatomicalfinding|spinal fracture"], "status": "exact", "note": "união das três fraturas"},
    "emphysema": {"attrs": ["disease|copd/emphysema"], "status": "exact", "note": "categoria disease"},
    "enlargement of the cardiac silhouette": {"attrs": ["anatomicalfinding|enlarged cardiac silhouette"], "status": "exact", "note": ""},
    "pleural thickening": {"attrs": ["anatomicalfinding|pleural/parenchymal scarring"], "status": "approx", "note": "ImaGenome agrupa espessamento pleural em pleural/parenchymal scarring"},
    "hernia": {"attrs": ["anatomicalfinding|hernia"], "status": "exact", "note": ""},
    "blunting of the costophrenic angle": {"attrs": ["anatomicalfinding|costophrenic angle blunting"], "status": "exact", "note": ""},
    "scoliosis": {"attrs": ["anatomicalfinding|scoliosis"], "status": "exact", "note": ""},
    "granuloma": {"attrs": ["disease|granulomatous disease", "anatomicalfinding|calcified nodule"], "status": "approx", "note": ""},
    "heart failure": {"attrs": ["disease|fluid overload/heart failure"], "status": "exact", "note": "categoria disease"},
    "pneumomediastinum": {"attrs": ["anatomicalfinding|pneumomediastinum"], "status": "exact", "note": ""},
    "hilar congestion": {"attrs": ["anatomicalfinding|enlarged hilum"], "status": "approx", "note": "congestão hilar ≈ hilo aumentado"},
    "tortuosity of the thoracic aorta": {"attrs": ["anatomicalfinding|tortuous aorta"], "status": "exact", "note": ""},
    "tortuosity of the descending aorta": {"attrs": ["anatomicalfinding|tortuous aorta"], "status": "approx", "note": "ImaGenome não separa descendente"},
    "contusion": {"attrs": [], "status": "none", "note": "sem rótulo no ImaGenome"},
    "hematoma": {"attrs": [], "status": "none", "note": "sem rótulo"},
    "air collection": {"attrs": [], "status": "none", "note": "ambíguo (sub-diaphragmatic/subcutaneous air/pneumothorax)"},
    "gastric distention": {"attrs": [], "status": "none", "note": "sem rótulo"},
    "hypoxemia": {"attrs": [], "status": "none", "note": "não é achado de imagem"},
    "hypertensive heart disease": {"attrs": [], "status": "none", "note": "sem rótulo"},
    "thymoma": {"attrs": [], "status": "none", "note": "superior mediastinal mass/enlargement seria aproximação fraca; deixado fora"},
}
# ---- <loc> -> regioes (regras)
SIDE = {"right": "right", "left": "left"}
BOTH_LUNGS = ["right lung", "left lung"]


def loc_to_regions(loc: str):
    s = " " + re.sub(r"\s+", " ", loc.lower().strip()) + " "
    sides = [k for k in ("right", "left") if f" {k} " in s]
    bilateral = (" bilateral " in s) or (len(sides) == 2) or (" lungs " in s) or (" lobes " in s) or (" bases " in s)
    if " rib " in s or " soft tissue" in s or " chest wall " in s:
        return [], "sem caixa (costela/partes moles)"
    if " pericardi" in s:
        return ["cardiac silhouette"], "pericardial -> cardiac silhouette"
    zones = []
    if re.search(r" (apical|apex|apices) ", s): zones.append("apical zone")
    if re.search(r" (upper|superior) ", s): zones.append("upper lung zone")
    if re.search(r" (mid|middle) ", s): zones.append("mid lung zone")
    if re.search(r" (lower|inferior|base|basal|basilar|bibasilar) ", s): zones.append("lower lung zone")
    retro = " retrocardiac " in s
    if " hemithorax " in s and not zones: zones = []
    if bilateral or not sides:
        sides_eff = ["right", "left"]
    else:
        sides_eff = sides
    if " bibasilar " in s: sides_eff = ["right", "left"]
    regions = []
    if retro:
        regions = [f"{sd} lower lung zone" for sd in (sides_eff if sides else ["left"])] + ["cardiac silhouette"]
        return sorted(set(regions)), "retrocardiac -> zona inferior do lado (padrão esquerdo) + cardiac silhouette"
    if not zones:
        return [f"{sd} lung" for sd in sides_eff], "lado inteiro" if sides else "ambos os pulmões"
    for sd in sides_eff:
        for zn in zones:
            regions.append(f"{sd} {zn}")
    return sorted(set(regions)), "lado × zona"


def aggregate_last(g):
    """(bbox_name, category|label) -> final context ('yes'/'no'), AGGREGATION=last, INCLUDE_SECTIONS=all."""
    out = {}
    for a in g["attributes"]:
        b = a["bbox_name"]
        for lst in a["attributes"]:
            for x in lst:
                cat, ctx, lab = x.split("|")
                if cat in ("laterality", "severity", "temporal", "texture"): continue
                out[(b, f"{cat}|{lab}")] = ctx
    return out


def main():
    ent = json.load(open(V7 / "analysis/entities.json"))["entities"]
    emap = {}
    for e, n in ent.items():
        k = e.strip(); m = ENTITY_MAP.get(k)
        emap[k] = {"n_diffvqa": n, **(m or {"attrs": [], "status": "none", "note": "não mapeado"})}
    # locs observados (pool inteiro) -> regioes
    pool = pd.read_parquet(V7 / "data/pool_single_image_all_splits.parquet", columns=["question", "template"])
    locs = pool[pool.template.str.contains("<loc>")].question.str.extract(r" in the (.+?)(?: area)?\?$")[0].value_counts()
    locmap = {l: {"n": int(n), "regions": loc_to_regions(l)[0], "rule": loc_to_regions(l)[1]} for l, n in locs.items()}
    json.dump({"entity_map": emap, "loc_map": locmap, "aggregation": "last per (bbox_name, categoria|rotulo), todas as secoes",
               "provenance": {"script": "v7_mimic/scripts/15_entity_map.py", "date": pd.Timestamp.now("UTC").strftime("%Y-%m-%dT%H:%M:%SZ")}},
              open(V7 / "analysis/entity_map.json", "w"), indent=1, ensure_ascii=False)
    # ---- validacao
    z = zipfile.ZipFile(RAW / "silver_dataset/scene_graph.zip"); sg = {Path(n).name.replace("_SceneGraph.json", ""): n for n in z.namelist() if n.endswith("_SceneGraph.json")}
    ents_sorted = sorted((e.strip() for e in ent), key=len, reverse=True)
    ent_re = re.compile(r"\b(" + "|".join(re.escape(e) for e in ents_sorted) + r")\b")
    def entity_of(q):
        m = ent_re.search(q); return m.group(1) if m else None
    # gold: relation 1/0 per (dicom, bbox, label) -> presence of some mapped attribute in some region (aggregated per image: any yes)
    ga = pd.read_csv(RAW / "gold_dataset/gold_object_attribute_with_coordinates.txt", sep="\t")
    ga["dicom_id"] = ga.image_id.str.replace(".dcm", "", regex=False); ga["key"] = ga.categoryID + "|" + ga.label_name
    gold_yes = collections.defaultdict(set); gold_any = collections.defaultdict(set)
    for r in ga.itertuples(index=False):
        gold_any[r.dicom_id].add(r.key)
        if int(r.relation) == 1: gold_yes[r.dicom_id].add(r.key)
    q = pd.read_csv(DV / "mimic_pair_questions.csv", usecols=["study_id", "question_type", "question", "answer"])
    m = pd.read_csv(DV / "mimic_all.csv", usecols=["study_id", "dicom_id"])
    qm = q.merge(m, on="study_id"); pres = qm[(qm.question_type == "presence") & ~qm.question.str.contains(" in the ") & ~qm.question.str.contains("bilateral")].copy()
    pres["entity"] = pres.question.map(entity_of)
    def validate(df, present_fn, label):
        rows = {}
        for e, g in df.groupby("entity"):
            attrs = emap.get(e, {}).get("attrs", [])
            if not attrs: rows[e] = {"status": emap.get(e, {}).get("status", "none"), "n": int(len(g)), "note": "sem mapeamento"}; continue
            tp = fp = tn = fn = 0; n_na = 0
            for r in g.itertuples(index=False):
                p = present_fn(r.dicom_id, attrs)
                if p is None: n_na += 1; continue
                y = r.answer == "yes"
                if y and p: tp += 1
                elif y and not p: fn += 1
                elif (not y) and p: fp += 1
                else: tn += 1
            rows[e] = {"status": emap[e]["status"], "n": tp + fp + tn + fn, "n_sem_scene_graph": n_na, "n_yes": tp + fn, "n_no": fp + tn, "tp": tp, "fn": fn, "fp": fp, "tn": tn,
                       "sensitivity": round(tp / (tp + fn), 3) if tp + fn else None, "specificity": round(tn / (tn + fp), 3) if tn + fp else None,
                       "ppv": round(tp / (tp + fp), 3) if tp + fp else None, "agreement": round((tp + tn) / (tp + fp + tn + fn), 3) if tp + fp + tn + fn else None}
        return rows
    def gold_present(d, attrs):
        if d not in gold_any: return None
        return any(a in gold_yes[d] for a in attrs)
    pres_gold = pres[pres.dicom_id.isin(gold_any.keys())]
    val_gold = validate(pres_gold, gold_present, "gold")
    # silver: whole test set ("is there <e>?" + "is there evidence of <e> in this image?") -> any yes in some region (last)
    test = pd.read_parquet(V7 / "data/items_test.parquet"); tq = test[test.template_id.isin(["T06", "T07"])].copy(); tq["entity"] = tq.question.map(entity_of)
    cache = {}
    def silver_present(d, attrs):
        if d not in sg: return None
        if d not in cache: cache[d] = aggregate_last(json.loads(z.read(sg[d])))
        agg = cache[d]
        return any(ctx == "yes" and key in attrs for (b, key), ctx in agg.items())
    val_silver = validate(tq, silver_present, "silver")
    # silver also on the whole test pool (all presence questions without loc in the test split, not only the sampled ones)
    pool_all = pd.read_parquet(V7 / "data/pool_single_image_all_splits.parquet"); pt = pool_all[(pool_all.split == "test") & pool_all.template_id.isin(["T06", "T07"])].copy(); pt["entity"] = pt.question.map(entity_of)
    val_silver_pool = validate(pt, silver_present, "silver_pool")
    # table finding -> most frequent regions (silver, test scene graphs): for the sham units (closed_no)
    reg_counter = {e: collections.Counter() for e in emap}
    for d in test.dicom_id.unique():
        if d not in sg: continue
        if d not in cache: cache[d] = aggregate_last(json.loads(z.read(sg[d])))
        for (b, key), ctx in cache[d].items():
            if ctx != "yes": continue
            for e, mm in emap.items():
                if key in mm["attrs"]: reg_counter[e][b] += 1
    finding_regions = {e: dict(c.most_common(8)) for e, c in reg_counter.items() if c}
    out = {"gold": {"n_questions": int(len(pres_gold)), "n_images": int(pres_gold.dicom_id.nunique()), "by_entity": val_gold},
           "silver_test_items": {"n_questions": int(len(tq)), "by_entity": val_silver},
           "silver_test_pool": {"n_questions": int(len(pt)), "by_entity": val_silver_pool},
           "finding_to_regions_silver_test": finding_regions, "loc_unmapped_test": {}}
    tl = test[test.template_id.isin(["T02", "T03"])].question.str.extract(r" in the (.+?)(?: area)?\?$")[0]
    out["loc_unmapped_test"] = {l: int(n) for l, n in tl.value_counts().items() if not loc_to_regions(l)[0]}
    json.dump(out, open(V7 / "analysis/entity_validation.json", "w"), indent=1, ensure_ascii=False)
    # ---- docs/entity_map.md
    L = ["# Mapeamento entidade → atributo do ImaGenome, e <loc> → regiões (v7_mimic)", "",
         f"Gerado por `scripts/15_entity_map.py`; JSON em `analysis/entity_map.json`, validação em `analysis/entity_validation.json`. Presença de um achado numa imagem = algum atributo mapeado com contexto `yes` em alguma região, após agregação `last` por (região, atributo) (gold: `relation == 1`).", "",
         "## Entidades", "| entidade (Diff-VQA) | n no Diff-VQA | atributos do ImaGenome | status | nota |", "|---|---:|---|---|---|"]
    for e, mm in sorted(emap.items(), key=lambda kv: -kv[1]["n_diffvqa"]):
        L.append(f"| {e} | {mm['n_diffvqa']} | {'; '.join(mm['attrs']) or '—'} | {mm['status']} | {mm['note']} |")
    def table(v, title):
        T = ["", f"## {title}", "| entidade | status | n | yes/no | TP | FN | FP | TN | sens. | espec. | VPP | concord. |", "|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for e, r in sorted(v.items(), key=lambda kv: -kv[1].get("n", 0)):
            if "tp" not in r: T.append(f"| {e} | {r['status']} | {r['n']} | — | — | — | — | — | — | — | — | sem mapeamento |"); continue
            T.append(f"| {e} | {r['status']} | {r['n']} | {r['n_yes']}/{r['n_no']} | {r['tp']} | {r['fn']} | {r['fp']} | {r['tn']} | {r['sensitivity']} | {r['specificity']} | {r['ppv']} | {r['agreement']} |")
        return T
    L += table(val_gold, f"Validação no gold (manual): perguntas `is there <e>?`/`is there evidence of <e> in this image?` do Diff-VQA (todos os splits) em imagens com anotação gold de atributos — n = {len(pres_gold)} perguntas em {pres_gold.dicom_id.nunique()} imagens")
    L += table(val_silver, f"Validação no silver: itens do nosso teste (templates T06/T07), n = {len(tq)}")
    L += table(val_silver_pool, f"Validação no silver: todas as perguntas T06/T07 do split test (pool elegível), n = {len(pt)}")
    L += ["", "## Achado → regiões mais frequentes no silver (scene graphs das 1 445 imagens de teste; para a região esperada dos negativos)", "| entidade | regiões (n) |", "|---|---|"]
    for e, c in sorted(finding_regions.items(), key=lambda kv: -sum(kv[1].values())):
        L.append(f"| {e} | " + ", ".join(f"{b} ({n})" for b, n in c.items()) + " |")
    L += ["", "## <loc> → regiões (regras: lado × zona; `bibasilar`/`bases`/`lobes`/`lungs`/`bilateral` = ambos os lados; `retrocardiac` = zona inferior do lado (padrão esquerdo) + cardiac silhouette; `pericardial` = cardiac silhouette; costela/partes moles = sem caixa)", "| <loc> | n (pool) | regiões | regra |", "|---|---:|---|---|"]
    for l, mm in sorted(locmap.items(), key=lambda kv: -kv[1]["n"])[:80]:
        L.append(f"| {l} | {mm['n']} | {', '.join(mm['regions']) or '—'} | {mm['rule']} |")
    L += ["", f"<loc> sem região no teste (perguntas): {out['loc_unmapped_test']}"]
    (V7 / "docs/entity_map.md").write_text("\n".join(L) + "\n")
    print(json.dumps({"gold_n": len(pres_gold), "silver_items_n": len(tq), "silver_pool_n": len(pt), "loc_unmapped_test": out["loc_unmapped_test"]}))
    for e, r in sorted(val_gold.items(), key=lambda kv: -kv[1].get("n", 0))[:12]: print("gold", e, {k: r[k] for k in r if k in ("n", "sensitivity", "specificity", "agreement")})
    for e, r in sorted(val_silver.items(), key=lambda kv: -kv[1].get("n", 0))[:12]: print("silver", e, {k: r[k] for k in r if k in ("n", "sensitivity", "specificity", "agreement")})


if __name__ == "__main__":
    main()
