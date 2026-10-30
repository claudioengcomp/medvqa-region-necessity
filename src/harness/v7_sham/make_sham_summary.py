"""Single summary of the occluder test (`sham`; 2026-10-10, authors' request): one table per benchmark x family x condition with mean IPR (SD)
across seeds, P(affirms|C0) -> P(affirms|sham), n of items and of images, sensitivity of the positive control where available.
Kvasir: published and VT/FT separate; SLAKE: 22 and 16 pure; HEAL: T, P, S and fills. Source of the numbers sheet of the
control-occlusion study; cites source files and sha256. No interpretation."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import collections, hashlib, json, time
R = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_sham"
def sha(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()
K = json.load(open(f"{R}/analysis/kvasir_sham.json")); H = json.load(open(f"{R}/analysis/heal_sham_from_necessity.json")); S = json.load(open(f"{R}/analysis/slake_sham.json"))
inv_k = json.load(open(f"{R}/inventory_kvasir_sham.json")); inv_s = json.load(open(f"{R}/inventory_slake_sham.json"))
imgs_k = collections.defaultdict(set); items_k = collections.defaultdict(int)
for u in inv_k["units"]:
    if u["generated"]: imgs_k[u["condition"]].add(u["image_id"]); items_k[u["condition"]] += len(u["questions"])
imgs_s = {"all_22": len({u["image_id"] for u in inv_s["units"] if u["generated"]}), "pure_16": len({u["image_id"] for u in inv_s["units"] if u["generated"] and any(q["pure_negative"] for q in u["questions"])})}
f = lambda m, sd: (f"{m:+.3f} ({sd:.3f})" if sd is not None else f"{m:+.3f}")
M = ["# Resumo do sham (artigo A, Placebo) -- fonte da folha de numeros", "", f"Gerado {time.strftime('%Y-%m-%d %H:%M:%S')} por harness/v7_sham/make_sham_summary.py. IPR = P(afirma | condicao) - P(afirma | C0), pareada por item; media (DP) entre as 3 sementes da celula; n de itens por linha e n de imagens; sensibilidade do controle positivo = P(yes | SHAM_ART_black). Numeros sem interpretacao.", "",
     "Fontes: " + "; ".join(f"`{p}` (sha256 {sha(p)[:16]}…)" for p in (f"{R}/analysis/kvasir_sham.json", f"{R}/analysis/heal_sham_from_necessity.json", f"{R}/analysis/slake_sham.json", f"{R}/inventory_kvasir_sham.json", f"{R}/inventory_slake_sham.json")) + ".", ""]
# Kvasir
for group, pred in (("publicadas", lambda k: "_VT" not in k and "_FT" not in k and "ZEROSHOT" not in k), ("VT/FT", lambda k: "_VT" in k or "_FT" in k), ("zero-shot (14/10; uma linha por modelo, sem DP)", lambda k: "ZEROSHOT" in k)):
    M += [f"## Kvasir -- {group}", "", "Afirma: ART yes; contagem != 0; tipo/presenca != none. SHAM_ART_black = controle positivo (resposta correta = yes); SHAM_ART_blur10 = sham do ART; POL e INS sham nas duas versoes.", "", "| familia | condicao | IPR media (DP) | P(afirma\\|C0) -> P(afirma\\|sham) | Acc C0 -> Acc cond | n itens | n imagens | sensibilidade controle positivo (DP) |", "|---|---|---|---|---|---|---|---|"]
    for fam, v in K["by_family"].items():
        if not pred(fam): continue
        for c, b in v.items():
            sens = f(b["sensitivity_p_yes_mean"], b["sensitivity_p_yes_sd"]) if "sensitivity_p_yes_mean" in b else "-"
            M.append(f"| {fam} | {c} | {f(b['ipr_mean'], b['ipr_sd'])} | {b['rate_c0_mean']:.3f} -> {b['rate_cond_mean']:.3f} | {b['acc_c0_mean']:.3f} -> {b['acc_sham_mean']:.3f} | {items_k[c]} | {len(imgs_k[c])} | {sens} |")
    M.append("")
# HEAL
M += ["## HEAL -- closed_no (T, P, S e preenchimentos)", "", f"Afirma: predicao normalizada == yes. Itens: {H['n_items']} closed_no avaliaveis em {H['n_images']} imagens (mesmos para todas as linhas e condicoes). T em closed_no = anatomia perguntada ocultada numa imagem sem o achado.", "", "| familia | grupo | condicao | IPR media (DP) | P(yes\\|C0) -> P(yes\\|cond) | n itens | n imagens |", "|---|---|---|---|---|---|---|"]
for fam, v in H["by_family"].items():
    for c in H["conditions"]:
        b = v[c]; M.append(f"| {fam} | {v['group']} | {c} | {f(b['ipr_mean'], b['ipr_sd'])} | {b['rate_c0_mean']:.3f} -> {b['rate_cond_mean']:.3f} | {H['n_items']} | {H['n_images']} |")
M.append("")
# SLAKE
M += ["## SLAKE -- negativos por polaridade do template (P2.3)", "", f"Afirma: resposta que afirma doenca (gold invertido por template). {S['n_items']} itens em {S['n_images']} imagens; {S['n_pure_negative']} pure_negative em {imgs_s['pure_16']} imagens. C0 de referencia: _C0.json do teste completo (p0/results). So IC por bootstrap (no slake_sham.md); sem Holm.", "", "| familia | condicao | subconjunto | IPR media (DP) | P(afirma\\|C0) -> P(afirma\\|sham) | n itens | n imagens |", "|---|---|---|---|---|---|---|"]
for fam, v in S["by_family"].items():
    for c, d in v.items():
        for sub, n_it, n_im in (("all_22", S["n_items"], S["n_images"]), ("pure_16", S["n_pure_negative"], imgs_s["pure_16"])):
            b = d[sub]; M.append(f"| {fam} | {c} | {sub} | {f(b['ipr_mean'], b['ipr_sd'])} | {b['rate_c0_mean']:.3f} -> {b['rate_cond_mean']:.3f} | {n_it} | {n_im} |")
# MIMIC (13/10, authors): closed_no_sham from inventory v2, 27 runs (read from v7_mimic/analysis/placebo_mimic.json)
PM = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic/analysis/placebo_mimic.json"; P = json.load(open(PM))
Lm = [r for r in P["linhas"] if "completo" in r]; s0 = Lm[0]["completo"]["sham"]
pp = lambda x: f"{100 * x:+.1f}"; pc = lambda c: f"[{100 * c[0]:+.1f}, {100 * c[1]:+.1f}]"
M += ["", "## MIMIC -- closed_no_sham (inventario v2)", "", f"Afirma: predicao normalizada == yes. Itens: {s0['n_alinhadas']} closed_no_sham avaliaveis em {s0['n_imagens']} imagens. IPR_c = P(yes|c) - P(yes|C0), pareada por item; IC 95 % por bootstrap por imagem (2 000, seed 20260913); McNemar mid-p; Holm por linha sobre SHAM_black e SHAM_blur10. Fonte: `{PM}` (sha256 {sha(PM)[:16]}…). Valores em pp.", "",
      "| linha | familia | grupo | n | P(yes\\|C0) | SHAM_black: IPR [IC] | Holm | SHAM_blur10: IPR [IC] | Holm |", "|---|---|---|---|---|---|---|---|---|"]
for r in Lm:
    s = r["completo"]["sham"]; c = s["conds"]
    M.append(f"| {r['line']} | {r['family']} | {r['group']} | {s['n_alinhadas']} | {c['SHAM_black']['rate_c0']:.3f} | {pp(c['SHAM_black']['ipr'])} {pc(c['SHAM_black']['ipr_ci'])} | {s['holm']['SHAM_black']:.3g} | {pp(c['SHAM_blur10']['ipr'])} {pc(c['SHAM_blur10']['ipr_ci'])} | {s['holm']['SHAM_blur10']:.3g} |")
open(f"{R}/docs/sham_summary.md", "w").write("\n".join(M) + "\n"); print("FIM", len(M), "linhas")
