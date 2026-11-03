"""Items 11/17/22: Figure 1 v4 (figs/fig1_necessity.{pdf,png} = reduced, one class per panel; figs/fig1_necessity_full.{pdf,png} = full, internal
only) and the ladder figure (figs/fig_ladder.{pdf,png}). Per-run values from analysis/headroom.json and counts from analysis/escada_vereditos.json
(the same sources as the numbers sheet). Three panels on the same x scale; grey band from 0 to the image gain; hatched when the image gain is not
resolvable (lower CI bound <= 0); non-resolvable runs with grey markers ("not resolvable: Delta not read"); hollow marker = black, filled = blur 10 %.
Group labels inside the panel (no text crosses the frame). Vocabulary of the paper (item 22); no internal label."""
import json, os, re, sys, time
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
plt.rcParams.update({"font.size": 9, "font.family": "serif", "pdf.fonttype": 42, "ps.fonttype": 42, "axes.titlesize": 9, "legend.fontsize": 7})
H = json.load(open(f"{OUT}/analysis/headroom.json")); ESC = json.load(open(f"{OUT}/analysis/escada_vereditos.json"))
PANEL = [("KVASIR", "Kvasir-VQA-x1", [("dependent_polyp", "polyp"), ("dependent_instrument", "instrument")]),
         ("HEAL", "HEAL-MedVQA", [("closed_yes", "closed-ended, answer yes"), ("closed_no", "closed-ended, answer no")]),
         ("MIMIC", "Medical-Diff-VQA", [("closed_yes", "closed-ended, answer yes"), ("closed_no", "closed-ended, answer no")])]
GRP = [("Qwen2-VL-2B", "congelado", "Qwen2-VL-2B · frozen enc."), ("Qwen2-VL-2B", "afinado", "Qwen2-VL-2B · fine-tuned enc."),
       ("SmolVLM2-2.2B", "congelado", "SmolVLM2-2.2B · frozen enc."), ("SmolVLM2-2.2B", "afinado", "SmolVLM2-2.2B · fine-tuned enc."), ("M3AE", "ajuste completo", "M3AE · full fine-tuning")]
COL = ["#1f4e79", "#c55a11"]; GREY = "0.6"
def res(k): c = k.get("headroom_ci_by_image"); return bool(c and c[0] > 0)
def rows(base):
    R = H["bases"][base]["linhas"]; out = []
    for fam, enc, lab in GRP:
        ls = sorted([r for r in R.values() if r["family"] == fam and r["encoder"] == enc], key=lambda r: ({"LORA": 0, "DORA": 1}.get(r["method"], 2), r["seed"]))
        out.append((lab, [(f"{'LoRA' if r['method'] == 'LORA' else ('DoRA' if r['method'] == 'DORA' else 'full')}, seed {r['seed']}", r) for r in ls]))
    return out
def draw(npc, fname):
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 5.9 if npc == 2 else 5.2), sharey=True)
    allx = []
    for base, _, cls in PANEL:
        for c, _ in cls[:npc]:
            for r in H["bases"][base]["linhas"].values():
                k = r["classes"].get(c) or {}
                for key in ("delta_preto_ci_by_image", "delta_blur10_ci_by_image"):
                    if k.get(key): allx += [100 * k[key][0], 100 * k[key][1]]
                if k.get("headroom") is not None: allx += [100 * k["headroom"], 0]
    lo, hi = min(allx) - 3, max(allx) + 3; texts = []; outside = 0
    for ax, (base, title, cls) in zip(axes, PANEL):
        y = 0; yt, yl = [], []
        for glab, items in rows(base):
            if ax is axes[0]: ax.text(lo + 0.01 * (hi - lo), y + 0.25, glab, fontsize=6.3, fontweight="bold", ha="left", va="bottom")
            y -= 0.75
            for lab, r in items:
                for j, (c, cname) in enumerate(cls[:npc]):
                    k = r["classes"].get(c) or {}; off = (0.18 if j == 0 else -0.18) if npc == 2 else 0.0; h = 0.32 if npc == 2 else 0.6
                    hr = k.get("headroom"); ok = res(k); col = COL[j] if ok else GREY
                    if hr is not None:
                        ax.barh(y + off, 100 * hr, height=h, left=0, color="0.88", edgecolor="0.5" if not ok else "none", hatch="////" if not ok else None, linewidth=0.4, zorder=1)
                    for key, ci, fill, dy in (("delta_preto", "delta_preto_ci_by_image", "none", 0.07 if npc == 2 else 0.12), ("delta_blur10", "delta_blur10_ci_by_image", col, -0.07 if npc == 2 else -0.12)):
                        if k.get(key) is None: continue
                        x = 100 * k[key]; c_ = k[ci]; outside += int(100 * c_[0] < lo or 100 * c_[1] > hi)
                        ax.errorbar(x, y + off + dy, xerr=[[x - 100 * c_[0]], [100 * c_[1] - x]], fmt="o", ms=3.0, mfc=fill, mec=col, ecolor=col, elinewidth=0.8, capsize=0, zorder=3)
                yt.append(y); yl.append(lab); y -= 1
            y -= 0.35
        ax.axvline(0, color="k", lw=0.7, zorder=2); ax.set_xlim(lo, hi); ax.set_title(title); ax.set_xlabel("Δ (necessity effect), pp")
        ax.grid(axis="x", alpha=0.25, lw=0.5); ax.tick_params(axis="y", length=0)
        if ax is axes[0]: ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=6.3)
        ax.set_ylim(y + 0.6, 1.0)
    handles = [Line2D([], [], marker="o", ls="", mfc="none", mec="0.2", label="Δ, black fill (95% CI)"), Line2D([], [], marker="o", ls="", mfc="0.2", mec="0.2", label="Δ, Gaussian blur (σ = 10% of width)"),
               Patch(facecolor="0.88", label="image gain above the text-only arm"), Line2D([], [], marker="o", ls="", mfc=GREY, mec=GREY, label="not resolvable: Δ not read (hatched band)")]
    handles += ([Patch(color=COL[0], label="polyp / closed-ended, answer yes"), Patch(color=COL[1], label="instrument / closed-ended, answer no")] if npc == 2 else [Patch(color=COL[0], label="polyp (Kvasir-VQA-x1); closed-ended, answer yes (X-ray)")])
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    texts += [t.get_text() for t in fig.findobj(matplotlib.text.Text)]
    # no text crosses the panel frame: check the bounding boxes of the texts of panel 0 against the axes
    fig.canvas.draw(); rr = fig.canvas.get_renderer(); ab = axes[0].get_window_extent(rr)
    cross = [t.get_text() for t in axes[0].texts if (lambda e: e.x0 < ab.x0 - 0.5 or e.x1 > ab.x1 + 0.5)(t.get_window_extent(rr))]
    for ext in ("pdf", "png"): fig.savefig(f"{OUT}/figs/{fname}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig); return texts, outside, cross
t1, o1, c1 = [], 0, []   # round 4: the main figure (v5) comes from scripts/fig1_v5.py; here only the full figure and the ladder
t2, o2, c2 = draw(2, "fig1_necessity_full")
# ladder figure
LB = [("KVASIR", "dependent_polyp", "Kvasir-VQA-x1\npolyp"), ("KVASIR", "dependent_instrument", "Kvasir-VQA-x1\ninstrument"), ("HEAL", "closed_yes", "HEAL-MedVQA\nanswer yes"), ("HEAL", "closed_no", "HEAL-MedVQA\nanswer no"),
      ("MIMIC", "closed_yes", "Medical-Diff-VQA\nanswer yes"), ("MIMIC", "closed_no", "Medical-Diff-VQA\nanswer no")]
STEPS = [("L0", "raw drop"), ("L1", "matched control"), ("L2", "dual fill"), ("L3", "image gain readable")]; SC = ["#bdd7ee", "#6fa8dc", "#2e75b6", "#1f3864"]
fig, ax = plt.subplots(figsize=(7.0, 2.4)); w = 0.2
for i, (b, c, lab) in enumerate(LB):
    E_ = ESC["bases"][b][c]
    for j, (d, dl) in enumerate(STEPS):
        val = E_["contagens"][d]; ax.bar(i + (j - 1.5) * w, val, w, color=SC[j], label=dl if i == 0 else None); ax.text(i + (j - 1.5) * w, val + 0.4, str(val), ha="center", fontsize=6.5)
ax.set_xticks(range(len(LB))); ax.set_xticklabels([x[2] for x in LB], fontsize=7); ax.set_ylabel("runs declared necessary (of 27)"); ax.set_ylim(0, 31); ax.legend(ncol=4, frameon=False, loc="upper right", fontsize=7)
ax.grid(axis="y", alpha=0.25, lw=0.5); fig.tight_layout(); t3 = [t.get_text() for t in fig.findobj(matplotlib.text.Text)]
for ext in ("pdf", "png"): fig.savefig(f"{OUT}/figs/fig_ladder.{ext}", dpi=300, bbox_inches="tight")
plt.close(fig)
for old in ("fig1_necessity_reduced.pdf", "fig1_necessity_reduced.png"):
    p = f"{OUT}/figs/{old}"
    if os.path.exists(p): os.rename(p, f"{OUT}/logs/{old}.rodada1")   # the reduced figure became the main one; the round-1 copy stays in logs/ (nothing deleted)
BAD = re.compile(r"placebo|sham|\bTXT\b|\bC0\b|\bC1\b|\bM0\b|\bE[0-9]+\b|torre|tower|\bVT\b|\bFT\b|\bv[5-7]\b|RADORIG|piso|\barms?\b|nΔ|headroom|text-decoder|closed-form|visual encoder|displaced", re.I)
WL = re.compile(r"text-only arm", re.I)
hits = sorted({t for t in t1 + t2 + t3 if BAD.search(WL.sub("", t))})
man = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "fontes": {"headroom.json": sha(f"{OUT}/analysis/headroom.json"), "escada_vereditos.json": sha(f"{OUT}/analysis/escada_vereditos.json")},
       "files": {f: sha(f"{OUT}/figs/{f}") for f in sorted(os.listdir(f"{OUT}/figs")) if f.endswith((".pdf", ".png"))}, "grep_termos_internos_nos_textos": hits, "excecao_grep": "'text-only arm' removido antes do grep (item 22)",
       "ic_fora_da_area_visivel": {"principal": o1, "completa": o2}, "textos_que_cruzam_a_moldura_do_painel_1": {"principal": c1, "completa": c2},
       "nota": "pdftotext ausente no servidor; verificacao feita sobre os objetos Text da figura; conferencia por pdftotext feita a parte"}
json.dump(man, open(f"{OUT}/figs/manifest.json", "w"), indent=1); print("figs ok;", {k: man[k] for k in ("grep_termos_internos_nos_textos", "ic_fora_da_area_visivel", "textos_que_cruzam_a_moldura_do_painel_1")})
