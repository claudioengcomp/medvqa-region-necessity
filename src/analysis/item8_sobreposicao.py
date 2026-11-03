"""Item 8 (CPU): overlap of the displaced mask with another annotated anatomy (HEAL) and with another Chest ImaGenome region (MIMIC).
HEAL: native RLE masks from inputs/heal_annotations_test.parquet (copy with recorded sha); target = anatomy of the unit; displaced mask =
another anatomy (method anatomy:<X>) or harness.isbi_placebo.conditions.apply_placement(target, method); 'other anatomies' = anatomies
annotated on the same image (all questions of the HEAL test set), except the target's. MIMIC: boxes on the PNG (inventory v2,
units[].all_boxes_png and placebo_boxes_png); 'other regions' = leaf regions of the image (no children in the hierarchy of
analysis/region_hierarchy.json of v7_mimic), except the target's and its descendants. Measures per evaluable unit: any overlap
(> 0 px) and overlap > 50 % of the area of the other region. Counts and fractions only. Outputs: analysis/placebo_geometry_heal.json,
analysis/placebo_geometry_mimic.json, docs/item8_sobreposicao.md."""
import collections, json, os, sys, time
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
sys.path.insert(0, CODE_ROOT)
from harness.isbi_placebo.conditions import apply_placement
from harness.isbi_placebo.heal.heal_rle import decode_rle
T0 = time.time(); PQ = f"{LAB_INPUTS}/heal_annotations_test.parquet"
# ---------------- HEAL
inv = json.load(open(INV["HEAL"])); ev = [q for q in inv["questions"] if q["evaluable"]]
units = collections.OrderedDict()
for q in ev: units.setdefault((q["image_id"], q["anatomy"]), []).append(q)
ann = pd.read_parquet(PQ); rle = {}
for r in ann.itertuples(index=False): rle.setdefault((r.image_id, r.anatomy), (r.mask_rle, int(r.mask_h), int(r.mask_w)))
anat_by_img = collections.defaultdict(set)
for (img, a) in rle: anat_by_img[img].add(a)
cnt = collections.Counter(); by_m = collections.defaultdict(collections.Counter); cache = {}; estrato = []
def mask(img, a):
    k = (img, a)
    if k not in cache: cache[k] = decode_rle(*rle[k]).astype(bool)
    return cache[k]
for (img, a), qs in units.items():
    m = qs[0]["placebo"]["method"]; mk = m.split(":")[0]; others = sorted(anat_by_img[img] - {a}); nq = len(qs)
    cnt["unidades"] += 1; cnt["perguntas"] += nq
    if not others: estrato.append({"qids": [q["qid"] for q in qs], "estrato": "a_uma_anatomia"}); continue
    cnt["unidades_2+"] += 1; cnt["perguntas_2+"] += nq; by_m[mk]["unidades_2+"] += 1
    t = mask(img, a); pl = mask(img, m.split(":", 1)[1]) if m.startswith("anatomy:") else apply_placement(t, m)
    anyov = False; big = False
    for o in others:
        om = mask(img, o); inter = int((pl & om).sum())
        if inter > 0: anyov = True
        if om.sum() > 0 and inter / om.sum() > 0.5: big = True
    for k, v in (("qualquer_sobreposicao", anyov), ("sobreposicao_maior_50pct_da_outra", big)):
        if v: cnt[f"unidades_{k}"] += 1; cnt[f"perguntas_{k}"] += nq; by_m[mk][k] += 1
    estrato.append({"qids": [q["qid"] for q in qs], "estrato": "c_multi_com_sobreposicao" if anyov else "b_multi_sem_sobreposicao", "sobreposicao_maior_50pct": big})
    cache.clear()
heal = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "fonte_mascaras": PQ, "fonte_mascaras_sha256": sha(PQ), "inventario": INV["HEAL"], "inventario_sha256": sha(INV["HEAL"]),
        "contagens": dict(cnt), "por_metodo": {k: dict(v) for k, v in by_m.items()}, "estrato_por_unidade": estrato, "estrato_contagem": dict(collections.Counter(e["estrato"] for e in estrato)),
        "fracoes": {"unidades_qualquer_sobre_2+": cnt["unidades_qualquer_sobreposicao"] / max(cnt["unidades_2+"], 1), "unidades_maior50_sobre_2+": cnt["unidades_sobreposicao_maior_50pct_da_outra"] / max(cnt["unidades_2+"], 1),
                    "perguntas_qualquer_sobre_total": cnt["perguntas_qualquer_sobreposicao"] / cnt["perguntas"], "perguntas_maior50_sobre_total": cnt["perguntas_sobreposicao_maior_50pct_da_outra"] / cnt["perguntas"]},
        "nota_407": "contagem previa do protocolo: 407/1 446 perguntas em imagens com >= 2 anatomias; contagem aqui: perguntas_2+ (anatomias anotadas no parquet de teste do HEAL, todas as perguntas da imagem)"}
json.dump(heal, open(f"{OUT}/analysis/placebo_geometry_heal.json", "w"), indent=1)
# ---------------- MIMIC
H = json.load(open(f"{V7M}/analysis/region_hierarchy.json"))["hierarchy"]
def desc(r):
    out = set()
    for c in H.get(r, []): out |= {c} | desc(c)
    return out
PARENTS = set(H)
mi = json.load(open(INV["MIMIC"])); ev = {q["qid"]: q for q in mi["questions"] if q["evaluable"]}
cnt = collections.Counter(); by_m = collections.defaultdict(collections.Counter)
def area(b): return max(0, b[2] - b[0]) * max(0, b[3] - b[1])
def inter(a, b): return area([max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])])
for u in mi["units"]:
    qs = [q for q in u["qids"] if q in ev]
    if not qs: continue
    cls = ev[qs[0]]["question_class"]; cnt["unidades"] += 1; cnt["perguntas"] += len(qs); cnt[f"unidades_{cls}"] += 1
    excl = set(u["target_regions"]) | {d for r in u["target_regions"] for d in desc(r)}
    others = [r for r in u["all_boxes_png"] if r not in PARENTS and r not in excl]
    pbs = u.get("placebo_boxes_png") or []
    toks = {x.split(":")[0] for x in (u["placebo_method"] or "").split("|")}; mk = "+".join(sorted(toks))
    anyov = any(inter(pb, u["all_boxes_png"][o]) > 0 for pb in pbs for o in others)
    big = any(area(u["all_boxes_png"][o]) > 0 and sum(inter(pb, u["all_boxes_png"][o]) for pb in pbs) / area(u["all_boxes_png"][o]) > 0.5 for o in others)
    by_m[mk]["unidades"] += 1
    for k, v in (("qualquer_sobreposicao", anyov), ("sobreposicao_maior_50pct_da_outra", big)):
        if v: cnt[f"unidades_{k}"] += 1; cnt[f"unidades_{k}_{cls}"] += 1; cnt[f"perguntas_{k}"] += len(qs); by_m[mk][k] += 1
mimic = {"t": heal["t"], "inventario": INV["MIMIC"], "inventario_sha256": sha(INV["MIMIC"]), "hierarquia": f"{V7M}/analysis/region_hierarchy.json", "contagens": dict(cnt), "por_metodo": {k: dict(v) for k, v in by_m.items()},
         "fracoes": {"unidades_qualquer": cnt["unidades_qualquer_sobreposicao"] / cnt["unidades"], "unidades_maior50": cnt["unidades_sobreposicao_maior_50pct_da_outra"] / cnt["unidades"]},
         "nota": "as anatomias homologas do posicionamento v2 sao, por construcao, outra regiao da imagem (sobreposicao total com ela propria); 'outras regioes' exclui as do alvo e suas descendentes, inclui a regiao usada como mascara deslocada"}
json.dump(mimic, open(f"{OUT}/analysis/placebo_geometry_mimic.json", "w"), indent=1)
L = ["# Item 8 — sobreposição da máscara deslocada com outra anatomia/região", "", __doc__.split("\n", 1)[1].replace("\n", " "), "",
     "## HEAL", "", f"Máscaras: `{PQ}` (sha256 `{heal['fonte_mascaras_sha256']}`, copia local, sha registrado).", "",
     "| medida | valor |", "|---|---|"] + [f"| {k} | {v} |" for k, v in heal["contagens"].items()] + [f"| fração {k} | {v} |" for k, v in heal["fracoes"].items()] + ["", "Por método (unidades em imagens com ≥ 2 anatomias):", "", "```", json.dumps(heal["por_metodo"], indent=1), "```", "",
     "## MIMIC", "", "| medida | valor |", "|---|---|"] + [f"| {k} | {v} |" for k, v in mimic["contagens"].items()] + [f"| fração {k} | {v} |" for k, v in mimic["fracoes"].items()] + ["", "Por método da unidade:", "", "```", json.dumps(mimic["por_metodo"], indent=1), "```", "", mimic["nota"], "", f"Tempo: {time.time() - T0:.0f} s."]
open(f"{OUT}/docs/item8_sobreposicao.md", "w").write("\n".join(L) + "\n"); print(json.dumps(heal["contagens"]), json.dumps(heal["fracoes"])); print(json.dumps(mimic["contagens"]), json.dumps(mimic["fracoes"]))
