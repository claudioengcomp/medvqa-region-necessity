"""v7_mimic/scripts/20_gallery_mimic.py -- 2026-10-12 -- review galleries of the occlusion experiment on MIMIC (qc/gallery_mimic.html,
qc/gallery_mimic_sham.html), in the format of the repository's galleries: reuses, without editing, _gallery_html from
harness/isbi_placebo/make_placebo_conditions.py (@2b7e731). What changes stays outside the function: (a) the distribution table is
inserted before "<h2>Amostra de unidades" by .replace, as make_heal_conditions.py did; (b) the <h2> title of the sample is
replaced by .replace to list the extra panels (T_blur10, P_blur10); (c) own thumbnails (JPEG, long side 512) instead of
_thumb (PNG 220) to fit in 8 MB; (d) rich caption passed through the target_key/placebo_method/questions fields (the function
inserts them as is). Condition images read from the delivered ARROWS (bytes identical to those delivered for inference)."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import base64, collections, io, json, random, sys, time
from pathlib import Path
import numpy as np, pandas as pd
from PIL import Image, ImageDraw
sys.path.insert(0, os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-placebo")
from harness.isbi_placebo.make_placebo_conditions import _gallery_html  # noqa: E402
from harness.interventions.arrow_io import read_arrow  # noqa: E402
V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic"); DER = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/derived/mimic_png/test"); QC = V7 / "qc"
SEED = 20260913; SIDE = 512; JPEG_Q = 72
MAIN = ["pleural effusion", "atelectasis", "lung opacity", "cardiomegaly", "edema", "vascular congestion", "consolidation", "pneumonia"]
METHODS = ["anatomy", "hflip", "vflip", "translate", "rot180"]
GROUPS = ["pulmões/zonas", "coração", "mediastino/aorta", "ângulos costofrênicos", "outros"]


def agroup(regions):
    r = " ".join(regions)
    if "costophrenic" in r and not any(k in r for k in ("lung", "zone", "hilar")): return "ângulos costofrênicos"
    if any(k in r for k in ("lung", "zone", "hilar")): return "pulmões/zonas"
    if any(k in r for k in ("cardiac", "atrium", "cavoatrial")): return "coração"
    if any(k in r for k in ("mediastinum", "aort", "trachea", "svc", "carina")): return "mediastino/aorta"
    return "outros"


def thumb(img, boxes_red=(), boxes_blue=()):
    """target boxes in red and control-occlusion boxes in blue, numbered 1..n in the order of the target regions (control occlusion i paired with target i)."""
    from PIL import ImageFont
    im = img.convert("RGB"); dr = ImageDraw.Draw(im)
    try: font = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
    except Exception: font = ImageFont.load_default()
    for i, b in enumerate(boxes_red, 1):
        dr.rectangle(b, outline=(255, 0, 0), width=4); dr.text((b[0] + 6, b[1] + 4), str(i), fill=(255, 0, 0), font=font)
    for i, b in enumerate(boxes_blue, 1):
        dr.rectangle(b, outline=(0, 90, 255), width=4); dr.text((b[2] - 34, b[3] - 46), str(i), fill=(0, 90, 255), font=font)
    im.thumbnail((SIDE, SIDE)); buf = io.BytesIO(); im.save(buf, format="JPEG", quality=JPEG_Q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def umethod(u):
    """unit method: 1-box target = HEAL method; multi-box = 'multi:' + distinct per-box methods."""
    ms = sorted({x.split(":")[0] for x in u["placebo_method"].split("|")})
    return ms[0] if len(u["target_regions"]) == 1 else "multi:" + "+".join(ms)


def nbox(u): return "4+" if len(u["target_regions"]) >= 4 else str(len(u["target_regions"]))


def dist_table(units, qs):
    by = collections.Counter(); byq = collections.Counter(); bybox = collections.Counter()
    meths = sorted({umethod(u) for u in units}, key=lambda m: (m.startswith("multi"), m))
    for u in units:
        k = (umethod(u), agroup(u["target_regions"])); by[k] += 1; byq[k] += len(u["qids"]); bybox[(umethod(u), nbox(u))] += 1
    NB = ["1", "2", "3", "4+"]
    h = ["<h2>Distribuição final dos placebos: unidades (perguntas), por método × grupo anatômico do alvo, e por nº de caixas-alvo</h2>",
         "<p class='cap'>Grupo pelo conjunto de regiões-alvo: qualquer pulmão/zona/hilo → pulmões/zonas; só ângulos costofrênicos → ângulos; coração; mediastino/aorta/traqueia; o resto → outros. Alvos de uma caixa: choose_placebo do HEAL (outra anatomia torácica, hflip, vflip, rot180, translação). Alvos com mais de uma caixa (regra v2): um placebo por caixa, em ordem anatomia homóloga (0,8–1,25) → translação vertical (pares simétricos juntos, vtrans_pair) → hflip → anatomia 0,5–2,0 (anatomy_wide); 'multi:' lista os métodos por caixa presentes na unidade.</p>",
         "<table border='1'><tr><th>método</th>" + "".join(f"<th>{g}</th>" for g in GROUPS) + "<th>total</th>" + "".join(f"<th>{n} caixa{'s' if n != '1' else ''}</th>" for n in NB) + "</tr>"]
    for t in meths:
        h.append(f"<tr><td>{t}</td>" + "".join(f"<td>{by[(t, g)]} ({byq[(t, g)]})</td>" for g in GROUPS) + f"<td>{sum(by[(t, g)] for g in GROUPS)} ({sum(byq[(t, g)] for g in GROUPS)})</td>" + "".join(f"<td>{bybox[(t, n)]}</td>" for n in NB) + "</tr>")
    h.append("<tr><td><b>total</b></td>" + "".join(f"<td>{sum(by[(t, g)] for t in meths)} ({sum(byq[(t, g)] for t in meths)})</td>" for g in GROUPS) + f"<td>{len(units)} ({sum(len(u['qids']) for u in units)})</td>" + "".join(f"<td>{sum(bybox[(t, n)] for t in meths)}</td>" for n in NB) + "</tr></table>")
    return "\n".join(h), {"by_method_group": {f"{t}|{g}": [by[(t, g)], byq[(t, g)]] for t in meths for g in GROUPS}, "by_method_nboxes": {f"{t}|{n}": bybox[(t, n)] for t in meths for n in NB}}


def load_images(tag, conds, wanted_ids):
    """image_id -> {cond: PIL} read from the delivered arrows."""
    man = json.load(open(V7 / f"data/conditions/manifest_mimic_{tag}.json")); out = collections.defaultdict(dict)
    for c in conds:
        df = read_arrow(man["conditions"][c]["file"]); df = df[df.image_id.isin(wanted_ids)]
        for iid, b in zip(df.image_id, df.image): out[iid][c] = Image.open(io.BytesIO(b)); out[iid][c].load()
        del df
    return out


def main():
    rng = random.Random(SEED)
    inv = json.load(open(V7 / "results/inventory_mimic_test.json")); Q = {q["qid"]: q for q in inv["questions"]}
    manp = json.load(open(V7 / "data/conditions/manifest_mimic_placebo.json")); units = manp["units_by_group"]["main1"]["units"]
    mans = json.load(open(V7 / "data/conditions/manifest_mimic_sham.json")); sunits = mans["units_by_group"]["sham"]["units"]
    boxes = {u["image_id"]: u for u in inv["units"]}  # all_boxes_png per unit (image_id repeated across units: same boxes)
    perbox = {(u["image_id"], tuple(u["target_regions"]), u["placebo_method"]): u.get("placebo_per_box") for u in inv["units"]}
    for u in units + sunits:
        u["entity"] = Q[u["qids"][0]]["entity"]; u["method"] = u["placebo_method"].split(":")[0] if len(u["target_regions"]) == 1 else "multi"
        u["arrow_id"] = f"mimic/{u['image_id']}#{'+'.join(u['target_regions'])}"  # image_id of the arrow rows
    areas = sorted(u["target_area_frac"] for u in units); qcut = [areas[int(len(areas) * p)] for p in (.25, .5, .75)]
    def quart(a): return sum(a > c for c in qcut)
    # --- stratified sample (~30): >=2 per main entity, 5 methods, 4 quartiles
    pool = units[:]; rng.shuffle(pool); chosen = []; used = set()
    def take(pred, n):
        k = 0
        for u in pool:
            if k >= n: break
            if id(u) not in used and pred(u): chosen.append(u); used.add(id(u)); k += 1
    for e in MAIN: take(lambda u, e=e: u["entity"] == e, 2)
    def has(u, m): return m in {x.split(":")[0] for x in u["placebo_method"].split("|")}
    for m in ["anatomy", "vtrans_pair", "vtrans", "hflip", "vflip", "translate", "rot180", "anatomy_wide"]:
        if not any(has(u, m) for u in chosen): take(lambda u, m=m: has(u, m), 1)
    for n in ("2", "3", "4+"):
        if sum(nbox(u) == n for u in chosen) < 3: take(lambda u, n=n: nbox(u) == n, 3 - sum(nbox(u) == n for u in chosen))
    for qi in range(4):
        need = 2 - sum(quart(u["target_area_frac"]) == qi for u in chosen)
        if need > 0: take(lambda u, qi=qi: quart(u["target_area_frac"]) == qi, need)
    take(lambda u: True, max(0, 30 - len(chosen)))
    chosen.sort(key=lambda u: (u["entity"] or "", u["image_id"]))
    sham_pick = sorted(rng.sample(sunits, 4), key=lambda u: u["image_id"])
    sham16 = sorted(rng.sample(sunits, 16), key=lambda u: u["image_id"])
    # --- condition images (from the arrows)
    ids = {u["arrow_id"] for u in chosen}; imgs = load_images("placebo", ["T", "P", "S", "T_blur10", "P_blur10"], ids)
    sids = {u["arrow_id"] for u in sham_pick + sham16}; simgs = load_images("sham", ["SHAM_black", "SHAM_blur10"], sids)
    def legend(u, cls_note=""):
        qs = [Q[q] for q in u["qids"]]
        tk = (f"{u['entity']} · {cls_note or '/'.join(u['classes'])}<br>regiões-alvo: {', '.join(u['target_regions'])}"
              f"<br>target_area_frac: {u['target_area_frac']:.3f} (placebo {u['placebo_area_frac']:.3f}, sobreposição {u['overlap_frac']:.3f})")
        if u.get("placebo_scheme") == "per_box":
            pm = "regra v2, por caixa: " + "; ".join(f"{i}: {r} → {b['method']} (razão de área {b['area_ratio']:.2f}" + (f", dy {b['dy_boxes']:+.2f} alturas" if b.get("dy_boxes") is not None else "") + ")" for i, (r, b) in enumerate(zip(u["target_regions"], perbox[(u["image_id"], tuple(u["target_regions"]), u["placebo_method"])]), 1))
        else:
            pm = f"regra v2, alvo de 1 caixa (choose_placebo do HEAL): {u['placebo_method']}"
        return tk, pm, [f"{q['question']} → <b>{q['answer']}</b> [{q['template_id']}]" for q in qs]
    def unit_boxes(u):
        ab = boxes[u["image_id"]]["all_boxes_png"]; red = [ab[r] for r in u["target_regions"]]
        return red, list(u["placebo_boxes_png"] or [])
    gallery = []
    for u in chosen:
        orig = Image.open(DER / f"{u['image_id']}.png"); red, blue = unit_boxes(u); tk, pm, qs = legend(u)
        panels = [("original + caixas numeradas (vermelho alvo i, azul placebo i)", thumb(orig, red, blue))] + [(c, thumb(imgs[u["arrow_id"]][c])) for c in ("T", "P", "S", "T_blur10", "P_blur10")]
        gallery.append({"image_id": u["image_id"], "target_key": tk, "placebo_method": pm, "qids": u["qids"], "questions": qs, "panels": panels})
    for u in sham_pick:
        orig = Image.open(DER / f"{u['image_id']}.png"); red, blue = unit_boxes(u); tk, pm, qs = legend(u, "closed_no_sham (região esperada)")
        panels = [("original + caixas (vermelho região esperada, azul placebo)", thumb(orig, red, blue)), ("SHAM_black", thumb(simgs[u["arrow_id"]]["SHAM_black"])), ("SHAM_blur10", thumb(simgs[u["arrow_id"]]["SHAM_blur10"]))]
        gallery.append({"image_id": u["image_id"], "target_key": tk, "placebo_method": pm, "qids": u["qids"], "questions": qs, "panels": panels})
    table, counts = dist_table(units, Q)
    html = _gallery_html("MIMIC (Diff-VQA, teste) — v2", gallery, [])
    html = html.replace("<h2>Amostra de unidades: original, alvo+placebo, T, P, S</h2>", table + f"\n<h2>Amostra estratificada de {len(chosen)} unidades (+ {len(sham_pick)} closed_no_sham): original com caixas numeradas, T, P, S, T_blur10, P_blur10 · semente {SEED} · inventário/condições v2 (placebo por caixa)</h2>", 1)
    html = html.replace("<h2 id='review'>Review de placebos: alvo (vermelho) e placebo (azul)</h2><table>", "<h2 id='review'>Review de placebos</h2><p class='cap'>Sem amostra adicional: a revisão é feita nas unidades acima; os 12 PNG por condição estão em qc/conditions/.</p><table>", 1)
    (QC / "gallery_mimic.html").write_text(html)
    # --- occluder-test gallery (`sham`, 16)
    g2 = []
    for u in sham16:
        orig = Image.open(DER / f"{u['image_id']}.png"); red, blue = unit_boxes(u); tk, pm, qs = legend(u, "closed_no_sham (região esperada)")
        panels = [("original + caixas", thumb(orig, red, blue)), ("SHAM_black", thumb(simgs[u["arrow_id"]]["SHAM_black"])), ("SHAM_blur10", thumb(simgs[u["arrow_id"]]["SHAM_blur10"]))]
        g2.append({"image_id": u["image_id"], "target_key": tk, "placebo_method": pm, "qids": u["qids"], "questions": qs, "panels": panels})
    sdist = collections.Counter(agroup(u["target_regions"]) for u in sunits); sm = collections.Counter(umethod(u) for u in sunits)
    h2 = _gallery_html("MIMIC sham (Diff-VQA, teste) — negativos closed_no_sham — v2", g2, [])
    h2 = h2.replace("<p>Vermelho = alvo; azul = placebo.", "<p>Vermelho = região esperada do achado (duas regiões-folha mais frequentes no silver); azul = placebo. Gold \"no\" e ImaGenome sem o atributo.", 1)
    h2 = h2.replace("<h2>Amostra de unidades: original, alvo+placebo, T, P, S</h2>", f"<p>{len(sunits)} unidades/perguntas; grupo da região esperada: {dict(sdist)}; método de placebo: {dict(sm)}.</p><h2>Amostra de 16 negativos: original com caixas, SHAM_black, SHAM_blur10 · semente {SEED}</h2>", 1)
    h2 = h2.replace("<h2 id='review'>Review de placebos: alvo (vermelho) e placebo (azul)</h2><table>", "<h2 id='review'>Review</h2><table>", 1)
    (QC / "gallery_mimic_sham.html").write_text(h2)
    rep = {"date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "seed": SEED, "thumb_side": SIDE, "jpeg_q": JPEG_Q, "n_sample": len(chosen), "n_sham_in_main": len(sham_pick), "n_sham_gallery": len(g2),
           "sample_entities": dict(collections.Counter(u["entity"] for u in chosen)), "sample_methods_per_box": dict(collections.Counter(x.split(":")[0] for u in chosen for x in u["placebo_method"].split("|"))), "sample_nboxes": dict(collections.Counter(nbox(u) for u in chosen)),
           "sample_area_quartiles": dict(collections.Counter(quart(u["target_area_frac"]) for u in chosen)), "area_quartile_cuts": qcut,
           "distribution": counts, "sham_groups": dict(sdist), "sham_methods": dict(sm),
           "bytes": {"gallery_mimic.html": (QC / "gallery_mimic.html").stat().st_size, "gallery_mimic_sham.html": (QC / "gallery_mimic_sham.html").stat().st_size}}
    json.dump(rep, open(V7 / "analysis/gallery_mimic_report.json", "w"), indent=1, ensure_ascii=False); print(json.dumps(rep, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
