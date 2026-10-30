"""Round 9, item 3: candidates for the protocol figure, three per benchmark, strips of 7.0 x 1.25 in: intact (target in red, control in blue) |
target (black) | target (blur) | control occlusion (black) | target only (| box-artefact question, Kvasir only). Frames read from the existing
condition arrows (nothing generated); masks = pixels that change between the occluded (black) and the intact condition. Rules, fixed before looking
at the images:
- Kvasir-VQA-x1: polyp unit with mirror control (hflip), no target-control overlap, intact image whose answer to "Is there a green/black box
  artefact?" is "no", area (area_frac_fov) between the 1st and the 3rd quartile of these units, mean luminance of the polyp >= median of the
  remaining ones; order = salience (RGB distance between the polyp mean and that of a 15 px ring around it, inside the field of view), first three.
  Sixth frame: image of the SHAM_ART_black arrow, without the box (answer "no"), with the occluder >= 99.9 % inside the field of view; the one of
  the pair itself if it qualifies, otherwise the qualified ones by image_id, without repetition.
- HEAL-MedVQA: evaluable closed-ended yes questions; 1 with 'anatomy' control and 2 with 'hflip'; target (target_area_frac) closest to the median
  of the closed-ended yes; no target-control overlap; distinct images.
- Medical-Diff-VQA: evaluable closed-ended yes; 2 with control 'vtrans_pair' only and >= 2 target regions; 1 with control 'anatomy' only and >= 2
  regions; target (target_area_frac_thorax) closest to the group median; distinct images.
Ids of HEAL-MedVQA and Medical-Diff-VQA (credentialed) only in logs/candidatos_ids_CREDENCIADO.json, on the lab server."""
import io, json, os, re, sys, time, collections
import numpy as np, pyarrow as pa
from PIL import Image
from scipy import ndimage as ndi
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
plt.rcParams.update({"font.size": 8, "font.family": "serif", "font.serif": ["STIXGeneral"], "pdf.fonttype": 42, "ps.fonttype": 42})
A = f"{PLC}/data/isbi_placebo"; MC = f"{V7M}/data/conditions"; TB = {}
def table(p):
    if p not in TB:
        s = pa.memory_map(p)
        try: TB[p] = pa.ipc.open_file(s).read_all()
        except Exception: TB[p] = pa.ipc.open_stream(pa.memory_map(p)).read_all()
    return TB[p]
QIDX = {}
def row_by_qid(p, qid):
    if p not in QIDX: QIDX[p] = {int(q): i for i, ql in enumerate(table(p).column("question_id").to_pylist()) for q in ql}
    return QIDX[p][int(qid)]
def row_by_img(p, img_id):
    ids = [x.split("/")[-1] for x in table(p).column("image_id").to_pylist()]; hit = [i for i, x in enumerate(ids) if x == img_id]; assert len(hit) == 1, (os.path.basename(p), len(hit)); return hit[0]
def pic(p, i): return np.asarray(Image.open(io.BytesIO(table(p).column("image")[i].as_py())).convert("RGB"))
def changed(a, b): return np.any(np.abs(a.astype(int) - b.astype(int)) > 0, axis=2)
def fov(a):
    m = a.max(axis=2) > 20; lab, n = ndi.label(m)
    if n == 0: return m
    k = 1 + int(np.argmax(ndi.sum(m, lab, range(1, n + 1)))); return ndi.binary_fill_holes(lab == k)
OUTI = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__))}; IDS = {}
# ---------------- Kvasir
inv = json.load(open(INV["KVASIR"])); IM = {x["image_id"]: x for x in inv["images"]}; QK = {int(q["qid"]): q for q in inv["questions"]}
TE = f"{PLC}/data/finetune_arrows/vqa_kvasir_test_clean.arrow"; tt = table(TE)
BOX = {}
for iid, ql, al in zip(tt.column("image_id").to_pylist(), tt.column("questions").to_pylist(), tt.column("answers").to_pylist()):
    for q, a in zip(ql, al):
        if q == "Is there a green/black box artefact?": BOX[iid.split("/")[-1]] = (a[0] if a else None)
C0K = f"{A}/vqa_kvasir_placebo_C0.arrow"; units = [x.split("/")[-1] for x in table(C0K).column("image_id").to_pylist()]
cand = [u for u in units if IM.get(u, {}).get("target_kind") == "polyp" and IM[u].get("placebo_method") == "hflip"]
F = {"unidades_polipo_hflip": len(cand)}
q1, q3 = np.percentile([IM[u]["area_frac_fov"] for u in cand], [25, 75])
c2 = []
for u in cand:
    c0, t, p = pic(C0K, row_by_img(C0K, u)), pic(f"{A}/vqa_kvasir_placebo_T.arrow", row_by_img(f"{A}/vqa_kvasir_placebo_T.arrow", u)), pic(f"{A}/vqa_kvasir_placebo_P.arrow", row_by_img(f"{A}/vqa_kvasir_placebo_P.arrow", u))
    mt, mp = changed(t, c0), changed(p, c0)
    if not (mt.any() and mp.any()) or (mt & mp).any() or BOX.get(u) != "no" or not (q1 <= IM[u]["area_frac_fov"] <= q3): continue
    fv = fov(c0); ring = ndi.binary_dilation(mt, iterations=15) & ~mt & fv
    lum = float((c0[mt] @ [0.299, 0.587, 0.114]).mean()); sal = float(np.linalg.norm(c0[mt].mean(0) - c0[ring].mean(0)))
    c2.append({"u": u, "lum": lum, "sal": sal, "area": IM[u]["area_frac_fov"]})
F.update({"sem_sobreposicao_sem_caixa_area_IQR": len(c2), "area_q1_q3": [float(q1), float(q3)]})
med_l = float(np.median([x["lum"] for x in c2])); c3 = sorted([x for x in c2 if x["lum"] >= med_l], key=lambda x: (-x["sal"], x["u"]))
F.update({"luminancia_mediana": med_l, "apos_luminancia": len(c3)}); KV = c3[:3]
SA = f"{V7S}/data/vqa_kvasir_sham_SHAM_ART_black.arrow"; sids = [x.split("/")[-1] for x in table(SA).column("image_id").to_pylist()]
def art_ok(iid):
    if BOX.get(iid) != "no": return None
    a = pic(SA, row_by_img(SA, iid)); c = pic(TE, row_by_img(TE, iid)); occ = changed(a, c); fv = fov(c)
    return float((occ & fv).sum() / max(occ.sum(), 1)) if occ.any() else None
used = set(); ARTS = []
for k in KV:
    f_own = art_ok(k["u"]) if k["u"] in sids else None
    if f_own is not None and f_own >= 0.999 and k["u"] not in used: ARTS.append((k["u"], f_own)); used.add(k["u"]); continue
    for iid in sorted(sids):
        if iid in used: continue
        f = art_ok(iid)
        if f is not None and f >= 0.999: ARTS.append((iid, f)); used.add(iid); break
F["sexto_quadro"] = [{"image_id": a, "fracao_do_oclusor_no_campo_de_visao": f, "mesma_imagem_do_par": a == k["u"]} for (a, f), k in zip(ARTS, KV)]
OUTI["kvasir"] = {"funil": F, "candidatos": []}
for i, k in enumerate(KV):
    u = k["u"]; qs = [q for q in QK.values() if q["image_id"] == u and q["evaluable"] and q["question_class"] == "dependent_polyp"]
    OUTI["kvasir"]["candidatos"].append({"cand": i + 1, "image_id": u, "alvo": "polyp", "metodo_controle": "hflip", "area_frac_fov": k["area"], "luminancia_polipo": k["lum"], "saliencia": k["sal"],
                                         "perguntas_polipo_avaliaveis": len(qs), "pergunta": qs[0]["question"] if qs else None, "sexto_quadro_image_id": ARTS[i][0]})
# ---------------- HEAL
H = json.load(open(INV["HEAL"])); hq = [q for q in H["questions"] if q["evaluable"] and q["question_class"] == "closed_yes"]
medh = float(np.median([q["target_area_frac"] for q in hq])); kind = lambda q: (q.get("placebo") or {}).get("method", "").split(":")[0]
HC = {c: f"{A}/vqa_heal_placebo_{c}.arrow" for c in ("C0", "T", "T_blur10", "P", "S")}
def pick(qs, n, keyf, med, arrows, used_img):
    out = []
    for q in sorted(qs, key=lambda q: (abs(keyf(q) - med), q["qid"])):
        if q["image_id"] in used_img: continue
        c0 = pic(arrows["C0"], row_by_qid(arrows["C0"], q["qid"])); t = pic(arrows["T"], row_by_qid(arrows["T"], q["qid"])); p = pic(arrows["P"], row_by_qid(arrows["P"], q["qid"]))
        mt, mp = changed(t, c0), changed(p, c0)
        if not (mt.any() and mp.any()) or (mt & mp).any(): continue
        out.append(q); used_img.add(q["image_id"])
        if len(out) == n: break
    return out
uh = set(); HE = pick([q for q in hq if kind(q) == "anatomy"], 1, lambda q: q["target_area_frac"], medh, HC, uh) + pick([q for q in hq if kind(q) == "hflip"], 2, lambda q: q["target_area_frac"], medh, HC, uh)
OUTI["heal"] = {"mediana_target_area_frac_fechada_sim": medh, "candidatos": [{"cand": i + 1, "alvo": q["anatomy"], "metodo_controle": q["placebo"]["method"], "pergunta": q["question"], "target_area_frac": q["target_area_frac"]} for i, q in enumerate(HE)]}
IDS["heal"] = [{"cand": i + 1, "image_id": q["image_id"], "qid": q["qid"]} for i, q in enumerate(HE)]
# ---------------- Medical-Diff-VQA
M = json.load(open(INV["MIMIC"])); mq = [q for q in M["questions"] if q["evaluable"] and q["question_class"] == "closed_yes"]
kinds = lambda q: tuple(sorted({p.split(":")[0] for p in (q.get("placebo_method") or "").split("|") if p}))
MCa = {c: f"{MC}/vqa_mimic_placebo_{c}.arrow" for c in ("C0", "T", "T_blur10", "P", "S")}
gv = [q for q in mq if kinds(q) == ("vtrans_pair",) and len(q["target_regions"]) >= 2]; ga = [q for q in mq if kinds(q) == ("anatomy",) and len(q["target_regions"]) >= 2]
um = set(); key = lambda q: q["target_area_frac_thorax"]
ME = pick(gv, 2, key, float(np.median([key(q) for q in gv])), MCa, um) + pick(ga, 1, key, float(np.median([key(q) for q in ga])), MCa, um)
OUTI["mimic"] = {"grupos": {"vtrans_pair_2+": len(gv), "anatomy_2+": len(ga)}, "candidatos": [{"cand": i + 1, "alvo": ", ".join(q["target_regions"]), "entidade": q["entity"], "metodo_controle": q["placebo_method"].split(":")[0] if "|" not in q["placebo_method"] else "|".join(sorted({x.split(':')[0] for x in q['placebo_method'].split('|')})), "pergunta": q["question"], "target_area_frac_thorax": q["target_area_frac_thorax"], "n_regioes": len(q["target_regions"])} for i, q in enumerate(ME)]}
IDS["mimic"] = [{"cand": i + 1, "image_id": q["image_id"], "qid": q["qid"]} for i, q in enumerate(ME)]
# ---------------- desenho
def small(a, h):
    im = Image.fromarray(a); w = round(im.width * h / im.height); return np.asarray(im.resize((w, h), Image.LANCZOS))
def smallmask(m, shape): return np.asarray(Image.fromarray(m.astype(np.uint8) * 255).resize((shape[1], shape[0]), Image.NEAREST)) > 127
LAB = ["intact: target (red), control (blue)", "target (black)", "target (blur)", "control occlusion (black)", "target only", "box-artefact question"]
def wrap(fig, txt, width_in):
    t = fig.text(0, 0, txt); fig.canvas.draw(); w = t.get_window_extent().width / fig.dpi; t.remove()
    if w <= width_in: return txt
    words = txt.split(" "); return min(((" ".join(words[:k]) + "\n" + " ".join(words[k:])) for k in range(1, len(words))), key=lambda s: max(len(x) for x in s.split("\n")))
def strip(frames, mt, mp, fname):
    W, H_in = 7.0, 1.25; n = len(frames); GAP = 0.05; slot = (W - 0.04 - (n - 1) * GAP) / n; lab_h = 0.26; img_h = H_in - 0.03 - lab_h
    fig = plt.figure(figsize=(W, H_in)); labels = []; axes = []
    for i, arr in enumerate(frames):
        a = small(arr, 420); ax = fig.add_axes([(0.02 + i * (slot + GAP)) / W, (H_in - 0.02 - img_h) / H_in, slot / W, img_h / H_in]); ax.imshow(a, interpolation="lanczos"); ax.set_axis_off(); ax.set_anchor("C")
        if i == 0:
            for m, col in ((mt, "red"), (mp, "blue")): ax.contour(smallmask(m, a.shape).astype(float), levels=[0.5], colors=[col], linewidths=0.8)
        labels.append(fig.text((0.02 + i * (slot + GAP) + slot / 2) / W, (H_in - 0.02 - img_h - 0.03) / H_in, wrap(fig, LAB[i], slot), ha="center", va="top", linespacing=1.0)); axes.append(ax)
    fig.canvas.draw(); rr = fig.canvas.get_renderer(); fb = fig.bbox; texts = [t for t in fig.findobj(matplotlib.text.Text) if t.get_visible() and t.get_text().strip()]
    bbs = [(t.get_text(), t.get_window_extent(rr)) for t in labels]
    chk = {"min_fontsize_pt": min(t.get_fontsize() for t in texts), "textos_fora": [t.get_text() for t in texts if (lambda e: e.x0 < fb.x0 - .5 or e.x1 > fb.x1 + .5 or e.y0 < fb.y0 - .5 or e.y1 > fb.y1 + .5)(t.get_window_extent(rr))],
           "rotulos_sobrepostos": [[a, b] for i, (a, ea) in enumerate(bbs) for (b, eb) in bbs[i + 1:] if ea.overlaps(eb)], "rotulos_sobre_imagens": [a for a, ea in bbs for ax in axes if ea.overlaps(ax.get_window_extent(rr))]}
    for ext in ("pdf", "png"): fig.savefig(f"{OUT}/figs/{fname}.{ext}", dpi=300)
    plt.close(fig); raw = open(f"{OUT}/figs/{fname}.pdf", "rb").read(); mb = [float(x) for x in re.search(rb"/MediaBox\s*\[\s*([\d.\s-]+)\]", raw).group(1).split()]
    chk.update({"pdf_pagina_in": [round(mb[2] / 72, 3), round(mb[3] / 72, 3)], "pdf_fontes": sorted({f.decode() for f in re.findall(rb"/BaseFont\s*/([A-Za-z0-9+\-]+)", raw)}), "pdf_type3": bool(re.search(rb"/Subtype\s*/Type3", raw)),
                "mascara_alvo_px": int(mt.sum()), "mascara_controle_px": int(mp.sum()), "sobreposicao_px": int((mt & mp).sum()), "sha256_pdf": sha(f"{OUT}/figs/{fname}.pdf"), "sha256_png": sha(f"{OUT}/figs/{fname}.png")})
    return chk
KC = {c: f"{A}/vqa_kvasir_placebo_{c}.arrow" for c in ("C0", "T", "T_blur10", "P", "S")}
for i, k in enumerate(KV):
    fr = [pic(KC[c], row_by_img(KC[c], k["u"])) for c in ("C0", "T", "T_blur10", "P", "S")] + [pic(SA, row_by_img(SA, ARTS[i][0]))]
    OUTI["kvasir"]["candidatos"][i]["figura"] = strip(fr, changed(fr[1], fr[0]), changed(fr[3], fr[0]), f"protocolo_kvasir_cand{i + 1}")
for name, CA, picks in (("heal", HC, HE), ("mimic", MCa, ME)):
    for i, q in enumerate(picks):
        fr = [pic(CA[c], row_by_qid(CA[c], q["qid"])) for c in ("C0", "T", "T_blur10", "P", "S")]
        OUTI[name]["candidatos"][i]["figura"] = strip(fr, changed(fr[1], fr[0]), changed(fr[3], fr[0]), f"protocolo_{name}_cand{i + 1}")
json.dump(OUTI, open(f"{OUT}/analysis/candidatos_figura.json", "w"), indent=1); json.dump(IDS, open(f"{W}/v7_artigo1/logs/candidatos_ids_CREDENCIADO.json", "w"), indent=1)
for b in ("kvasir", "heal", "mimic"):
    for c in OUTI[b]["candidatos"]: print(b, {k: v for k, v in c.items() if k not in ("figura",)}, {k: v for k, v in c["figura"].items() if not k.startswith("sha")})
print("funil kvasir", json.dumps(OUTI["kvasir"]["funil"])); print("mimic grupos", OUTI["mimic"]["grupos"], "heal mediana", medh)
