"""Round 11 (authors' decision, 21/10/2026): final Fig. 1 = protocol figure, 7.0 x 2.3 in. Row 1 = protocolo_kvasir_cand3 (six frames);
row 2 = protocolo_heal_cand2 (five frames, left-aligned; sixth slot empty). Row label on the left; frame labels as requested;
target (red) and control (blue) contours on the intact frame. Frames from the existing condition arrows (nothing generated); choices of round 9
(analysis/candidatos_figura.json; HEAL qid in logs/candidatos_ids_CREDENCIADO.json). Output: figs/fig_protocol.{pdf,png} (the round-8 one goes to logs)."""
import io, json, os, re, sys, time
import numpy as np, pyarrow as pa
from PIL import Image
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
plt.rcParams.update({"font.size": 8, "font.family": "serif", "font.serif": ["STIXGeneral"], "pdf.fonttype": 42, "ps.fonttype": 42})
A = f"{PLC}/data/isbi_placebo"; TB = {}
def table(p):
    if p not in TB:
        s = pa.memory_map(p)
        try: TB[p] = pa.ipc.open_file(s).read_all()
        except Exception: TB[p] = pa.ipc.open_stream(pa.memory_map(p)).read_all()
    return TB[p]
def row_by_img(p, iid):
    ids = [x.split("/")[-1] for x in table(p).column("image_id").to_pylist()]; hit = [i for i, x in enumerate(ids) if x == iid]; assert len(hit) == 1; return hit[0]
def row_by_qid(p, qid):
    hit = [i for i, ql in enumerate(table(p).column("question_id").to_pylist()) if int(qid) in [int(q) for q in ql]]; assert len(hit) == 1; return hit[0]
def pic(p, i): return np.asarray(Image.open(io.BytesIO(table(p).column("image")[i].as_py())).convert("RGB"))
def changed(a, b): return np.any(np.abs(a.astype(int) - b.astype(int)) > 0, axis=2)
def small(a, h):
    im = Image.fromarray(a); w = round(im.width * h / im.height); return np.asarray(im.resize((w, h), Image.LANCZOS))
def smallmask(m, shape): return np.asarray(Image.fromarray(m.astype(np.uint8) * 255).resize((shape[1], shape[0]), Image.NEAREST)) > 127
CF = json.load(open(f"{OUT}/analysis/candidatos_figura.json")); IDS = json.load(open(f"{W}/v7_artigo1/logs/candidatos_ids_CREDENCIADO.json"))
KV = CF["kvasir"]["candidatos"][2]; assert KV["cand"] == 3; HQ = next(x for x in IDS["heal"] if x["cand"] == 2)
KC = {c: f"{A}/vqa_kvasir_placebo_{c}.arrow" for c in ("C0", "T", "T_blur10", "P", "S")}; SA = f"{V7S}/data/vqa_kvasir_sham_SHAM_ART_black.arrow"
kfr = [pic(KC[c], row_by_img(KC[c], KV["image_id"])) for c in ("C0", "T", "T_blur10", "P", "S")] + [pic(SA, row_by_img(SA, KV["sexto_quadro_image_id"]))]
HC = {c: f"{A}/vqa_heal_placebo_{c}.arrow" for c in ("C0", "T", "T_blur10", "P", "S")}
hfr = [pic(HC[c], row_by_qid(HC[c], HQ["qid"])) for c in ("C0", "T", "T_blur10", "P", "S")]
LAB = ["intact (target red, control blue)", "target, black", "target, blur", "control occlusion, black", "target only", "box-artefact occluder"]
ROWS = [("Kvasir-VQA-x1", kfr), ("HEAL-MedVQA", hfr)]
def wrap(fig, txt, width_in):
    t = fig.text(0, 0, txt); fig.canvas.draw(); w = t.get_window_extent().width / fig.dpi; t.remove()
    if w <= width_in: return txt
    words = txt.split(" "); return min(((" ".join(words[:k]) + "\n" + " ".join(words[k:])) for k in range(1, len(words))), key=lambda s: max(len(x) for x in s.split("\n")))
W_, H_ = 7.0, 2.3; LBL = 0.20; GAP = 0.05; slot = (W_ - LBL - 0.02 - 5 * GAP) / 6; lab_h = 0.26; top = 0.03; img_h = (H_ - top - 0.01 - 2 * lab_h) / 2
fig = plt.figure(figsize=(W_, H_)); axes = []; labels = []; chk = {"mascaras": {}}
for ri, (rname, frames) in enumerate(ROWS):
    y0 = H_ - top - (ri + 1) * img_h - ri * lab_h
    fig.text(LBL / 2 / W_, (y0 + img_h / 2) / H_, rname, rotation=90, ha="center", va="center")
    mt, mp = changed(frames[1], frames[0]), changed(frames[3], frames[0]); chk["mascaras"][rname] = {"alvo_px": int(mt.sum()), "controle_px": int(mp.sum()), "sobreposicao_px": int((mt & mp).sum())}
    for ci, arr in enumerate(frames):
        a = small(arr, 420); ax = fig.add_axes([(LBL + ci * (slot + GAP)) / W_, y0 / H_, slot / W_, img_h / H_]); ax.imshow(a, interpolation="lanczos"); ax.set_axis_off(); ax.set_anchor("C")
        if ci == 0:
            for m, col in ((mt, "red"), (mp, "blue")): ax.contour(smallmask(m, a.shape).astype(float), levels=[0.5], colors=[col], linewidths=0.8)
        labels.append(fig.text((LBL + ci * (slot + GAP) + slot / 2) / W_, (y0 - 0.03) / H_, wrap(fig, LAB[ci], slot), ha="center", va="top", linespacing=1.0)); axes.append(ax)
fig.canvas.draw(); rr = fig.canvas.get_renderer(); fb = fig.bbox; texts = [t for t in fig.findobj(matplotlib.text.Text) if t.get_visible() and t.get_text().strip()]
bbs = [(t.get_text(), t.get_window_extent(rr)) for t in labels]
chk.update({"min_fontsize_pt": min(t.get_fontsize() for t in texts), "textos": [t.get_text() for t in texts],
            "textos_fora": [t.get_text() for t in texts if (lambda e: e.x0 < fb.x0 - .5 or e.x1 > fb.x1 + .5 or e.y0 < fb.y0 - .5 or e.y1 > fb.y1 + .5)(t.get_window_extent(rr))],
            "rotulos_sobrepostos": [[a, b] for i, (a, ea) in enumerate(bbs) for (b, eb) in bbs[i + 1:] if ea.overlaps(eb)], "rotulos_sobre_imagens": [a for a, ea in bbs for ax in axes if ea.overlaps(ax.get_window_extent(rr))]})
for ext in ("pdf", "png"):
    p = f"{OUT}/figs/fig_protocol.{ext}"
    if os.path.exists(p) and not os.path.exists(f"{OUT}/logs/fig_protocol_r8_20261021.{ext}"): os.rename(p, f"{OUT}/logs/fig_protocol_r8_20261021.{ext}")
    fig.savefig(p, dpi=300)
plt.close(fig); raw = open(f"{OUT}/figs/fig_protocol.pdf", "rb").read(); mb = [float(x) for x in re.search(rb"/MediaBox\s*\[\s*([\d.\s-]+)\]", raw).group(1).split()]
chk.update({"t": time.strftime("%Y-%m-%d %H:%M:%S"), "script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "pdf_pagina_in": [round(mb[2] / 72, 3), round(mb[3] / 72, 3)], "pdf_fontes": sorted({f.decode() for f in re.findall(rb"/BaseFont\s*/([A-Za-z0-9+\-]+)", raw)}),
            "pdf_type3": bool(re.search(rb"/Subtype\s*/Type3", raw)), "sha256_pdf": sha(f"{OUT}/figs/fig_protocol.pdf"), "sha256_png": sha(f"{OUT}/figs/fig_protocol.png"),
            "linhas": {"Kvasir-VQA-x1": "protocolo_kvasir_cand3", "HEAL-MedVQA": "protocolo_heal_cand2"}})
json.dump(chk, open(f"{OUT}/logs/fig_protocol_final_checagens.json", "w"), indent=1); print(json.dumps({k: v for k, v in chk.items() if k != "textos"}, ensure_ascii=False))
