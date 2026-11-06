"""Item 10: the single numbers sheet of the paper (docs/numbers_artigo1.md): one line per number, label in bold, value between back-ticks,
<sub>source · sha256</sub>. Reads only the JSON files of v7_artigo1/analysis (no number is typed in). Accuracies in %, differences in pp,
one decimal place (one line per number); ratios (sufficiency) with three decimal places; the full precision stays in the JSON files. Mean (SD) over
the three seeds; range = minimum to maximum over the runs. Internal labels (C0, T, P, S, TXT, M0, E3, B) may appear: the sheet is internal."""
import collections, glob, hashlib, json, os, statistics, sys, time
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
A = f"{OUT}/analysis"; J = lambda n: json.load(open(f"{A}/{n}.json"))
SRC = {n: (f"v7_artigo1/analysis/{n}.json", sha(f"{A}/{n}.json")[:12]) for n in ("inventario_linhas", "criterio", "headroom", "oclusor_negativos", "doses", "zeroshot", "fatos_metodo", "placebo_geometry_heal", "placebo_geometry_mimic", "bases_raw", "escada_vereditos", "heal_estratificado", "simnao", "sanidade_txt", "rodada3", "split_kvasir", "rodada8", "holm_familias", "holm_rawdrop", "blur4_r10")}
inv, crit, hd, oc, ds, zs, fm, gh, gm, raw = (J(n) for n in ("inventario_linhas", "criterio", "headroom", "oclusor_negativos", "doses", "zeroshot", "fatos_metodo", "placebo_geometry_heal", "placebo_geometry_mimic", "bases_raw"))
esc, hst, sn = J("escada_vereditos"), J("heal_estratificado"), J("simnao")
r3f = lambda x: "—" if x is None else f"{x:.3f}"
L = []
NL = {b: len(lines(b)) for b in BASES}; N27 = NL["KVASIR"]
SRC["common"] = ("src/analysis/common.py (run list, lines())", sha(f"{SCRIPTS}/common.py")[:12]); SRC["generator"] = ("src/analysis/make_numbers_artigo1.py (text written in the generator)", sha(os.path.relpath(__file__))[:12])   # 27 runs (7B family disabled) or 39 (enabled)
def line(rot, val, src):
    """One sheet line; src is a source key (or path) or a tuple of them when the value is derived from several files."""
    ss = [SRC[k] if k in SRC else (k, (sha(k) or "")[:12]) for k in (src if isinstance(src, (tuple, list)) else (src,))]
    L.extend([f"- **{rot}** — `{val}`  ", "  <sub>" + " ; ".join(f"{a} · sha256 {b}" for a, b in ss) + "</sub>"])
def pct(x): return "—" if x is None else f"{100 * x:.1f}"
def pp(x): return "—" if x is None else f"{100 * x:+.1f}"
def cpp(c): return "—" if not c else f"[{100 * c[0]:+.1f}, {100 * c[1]:+.1f}]"
def r3(x): return "—" if x is None else f"{x:.3f}"
def msp(m, f=pct): return "—" if not m else (f"{f(m['media'])} ({100 * m['dp']:.1f})" if m.get("dp") is not None else f(m["media"]))
def msr(m): return "—" if not m else (f"{m['media']:.3f} ({m['dp']:.3f})" if m.get("dp") is not None else f"{m['media']:.3f}")
def rng(m, f=pp): return "—" if not m else f"{f(m['min'])} a {f(m['max'])}"
NAME = {"KVASIR": "Kvasir-VQA-x1", "HEAL": "HEAL-MedVQA", "MIMIC": "Medical-Diff-VQA"}
CLS = {"KVASIR": [("dependent_polyp", "polipo"), ("dependent_instrument", "instrumento"), ("controle_texto", "controle 'Is there text?'"), ("dependent_polyp_secondary", "polipo secundario"), ("negative_control", "controle negativo (3 templates)")],
       "HEAL": [("closed_yes", "fechada-sim"), ("closed_no", "fechada-nao")], "MIMIC": [("closed_yes", "fechada-sim"), ("closed_no", "fechada-nao"), ("closed_yes|so_exatas", "fechada-sim, so entidades com mapeamento exato"), ("closed_no|so_exatas", "fechada-nao, so exatas")]}
GROUPS = list(next(iter(hd["bases"]["KVASIR"]["agregado_por_grupo"].values())) and hd["bases"]["KVASIR"]["agregado_por_grupo"].keys())
def allrng(b, cls, key):
    xs = [(r["classes"].get(cls) or {}).get(key) for r in hd["bases"][b]["linhas"].values()]; xs = [x for x in xs if x is not None]
    return {"min": min(xs), "max": max(xs)} if xs else None
L += ["# Folha de numeros -- artigo 1 (teste de necessidade da regiao com controle de posicao) -- rodada 1", "",
      f"Gerada {time.strftime('%Y-%m-%d %H:%M:%S')} por v7_artigo1/scripts/make_numbers_artigo1.py (sha256 {sha(os.path.relpath(__file__))[:12]}). Um numero por linha; fonte e sha256 abaixo. Acuracia em %, diferencas em pp (uma casa), razoes com tres casas; IC 95 % por bootstrap por imagem (2 000 replicas, semente 20260913, replicas fixas por base). Media (DP) entre as 3 sementes (condicional aos tres modelos). Delta = Acc(mascara deslocada) - Acc(alvo ocluido); headroom = Acc(intacta) - Acc(text-decoder-only da mesma familia e semente); criterio B = IC de Delta exclui zero por cima sob preto E sob blur 10 %. HEAL e Medical-Diff-VQA: so perguntas fechadas no corpo (abertas do MIMIC so no JSON); Kvasir-VQA-x1: as classes do inventario (polipo, instrumento, controle negativo, polipo secundario; abertas e fechadas, como na folha de 01/10). Bases: Kvasir-VQA-x1, HEAL-MedVQA, Medical-Diff-VQA (SLAKE so na S11).", ""]
# ---------------- S1
L += ["## S1. Contagens (resumo e introducao)", ""]
line("linhas afinadas por base / total", f"{N27} / {3 * N27} (3 bases)", "common")
_fams = []
for _b in BASES:
    for _x in lines(_b):
        if _x["family"] not in _fams: _fams.append(_x["family"])
line("familias / sementes", f"{len(_fams)} ({', '.join(_fams)}) / 3 (0, 1, 2)", "common")
line("linhas por base: Qwen2-VL (LoRA, DoRA) x (encoder congelado, afinado) x 3; SmolVLM2 idem; M3AE ajuste completo x 3" + ("" if N27 == 27 else "; Qwen2.5-VL-7B idem (rodada 24)"), "12 + 12 + 3 = 27" if N27 == 27 else "12 + 12 + 3 + 12 = 39", "common")
U = inv["unidades"]
line("Kvasir-VQA-x1: perguntas avaliaveis (polipo / instrumento / controle negativo / polipo secundario)", f"{U['KVASIR']['n_avaliaveis']} ({U['KVASIR']['por_classe']['dependent_polyp']} / {U['KVASIR']['por_classe']['dependent_instrument']} / {U['KVASIR']['por_classe']['negative_control']} / {U['KVASIR']['por_classe']['dependent_polyp_secondary']})", "inventario_linhas")
line("Kvasir-VQA-x1: unidades imagem x alvo (polipo / instrumento) / imagens de teste com mascara / imagens de teste", f"{U['KVASIR']['unidades_imagem_x_alvo']} ({U['KVASIR']['unidades_por_tipo']['polyp']} / {U['KVASIR']['unidades_por_tipo']['instrument']}) / {U['KVASIR']['imagens_com_mascara']} / {U['KVASIR']['imagens_teste']}", "inventario_linhas")
line("HEAL-MedVQA: fechadas avaliaveis (sim / nao) / unidades imagem x anatomia / imagens", f"{U['HEAL']['n_avaliaveis']} ({U['HEAL']['por_classe']['closed_yes']} / {U['HEAL']['por_classe']['closed_no']}) / {U['HEAL']['unidades_imagem_x_anatomia']} / {U['HEAL']['imagens']}", "inventario_linhas")
line("Medical-Diff-VQA: avaliaveis / perguntas do subconjunto de teste (inventario v2)", f"{U['MIMIC']['n_avaliaveis']} / {U['MIMIC']['n_perguntas']}", "inventario_linhas")
line("Medical-Diff-VQA: fechadas-sim / fechadas-nao (alinhadas) / negativas do oclusor / abertas", f"{U['MIMIC']['por_classe'].get('closed_yes')} / {crit['bases']['MIMIC']['por_classe']['closed_no']['n_linhas'] and hd['bases']['MIMIC']['linhas'][next(iter(hd['bases']['MIMIC']['linhas']))]['classes']['closed_no']['n']} / {U['MIMIC']['por_classe'].get('closed_no_sham')} / {U['MIMIC']['por_classe'].get('open')}", ("inventario_linhas", "criterio", "headroom"))
line("Medical-Diff-VQA: fechadas-sim so com mapeamento exato de entidade", f"{U['MIMIC']['por_classe_so_exatas'].get('closed_yes')}", "inventario_linhas")
for b in BASES:
    for cls, nm in CLS[b]:
        v = crit["bases"][b]["por_classe"].get(cls)
        if not v or "|" in cls or cls == "negative_control": continue
        line(f"criterio B sem condicao de headroom, {NAME[b]}, {nm} (linhas necessarias / linhas)", f"{v['total']['B']}/{v['n_linhas']}", "criterio")
        line(f"{NAME[b]}, {nm}: resoluveis / necessarias entre as resoluveis / linhas", f"{v['resoluveis']} / {v['B_entre_resoluveis']} / {v['n_linhas']}", "criterio")
for b, cls in (("KVASIR", "dependent_polyp"), ("KVASIR", "dependent_instrument"), ("HEAL", "closed_yes"), ("MIMIC", "closed_yes")):
    for g, x in crit["bases"][b]["por_classe"][cls]["por_grupo"].items():
        line(f"criterio B sem condicao de headroom, {NAME[b]}, {dict(CLS[b])[cls]}, {g}", f"{x['B']}/{x['n']}", "criterio")
        line(f"{NAME[b]}, {dict(CLS[b])[cls]}, {g}: resoluveis / necessarias entre as resoluveis / linhas", f"{x['resoluveis']} / {x['B_entre_resoluveis']} / {x['n']}", "criterio")
for b in BASES:
    for k, v in crit["bases"][b].get("por_estrato", {}).items():
        nm = k.replace("entidade=", "").replace("anatomia=", "").replace("|closed_yes", ", fechada-sim")
        line(f"{NAME[b]}, {nm}: resoluveis / necessarias entre as resoluveis / linhas (criterio B sem condicao: {v['B']})", f"{v['resoluveis']} / {v['B_entre_resoluveis']} / {v['n_linhas']}", "criterio")
        for g, x in v["por_grupo"].items(): line(f"{NAME[b]}, {nm}, {g}: resoluveis / necessarias entre as resoluveis / linhas", f"{x['resoluveis']} / {x['B_entre_resoluveis']} / {x['n']}", "criterio")
# ---------------- S1b escada
L.extend(["", "## S1b. Escada de vereditos (L0 queda bruta; L1 controle pareado; L2 dois preenchimentos; L3 image gain legivel)", ""])
for b in BASES:
    for cls, E_ in esc["bases"][b].items():
        nm = dict(CLS[b]).get(cls, cls); c = E_["contagens"]
        line(f"escada, {NAME[b]}, {nm}: L0 / L1 / L2 / L3 (linhas)", f"{c['L0']} / {c['L1']} / {c['L2']} / {c['L3']} de {E_['n_linhas']}", "escada_vereditos")
        line(f"escada, {NAME[b]}, {nm}: L3 com TF-IDF no lugar do text-only arm (so interno)", f"{c['L3_tfidf']} de {E_['n_linhas']}", "escada_vereditos")
        for g, x in E_["por_grupo"].items(): line(f"escada, {NAME[b]}, {nm}, {g}: L0 / L1 / L2 / L3", f"{x['L0']} / {x['L1']} / {x['L2']} / {x['L3']} de {x['n']}", "escada_vereditos")
        for m, v in E_["zero_shot"].items(): line(f"escada, {NAME[b]}, {nm}, zero-shot {m.split('_ZEROSHOT')[0]}: L0 / L1 / L2 / L3", " / ".join("sim" if v[d] else "nao" for d in ("L0", "L1", "L2", "L3")), "escada_vereditos")
        for tr, ch in E_["mudancas"].items():
            ft = {k: v for k, v in ch.items() if "ZEROSHOT" not in k}
            line(f"escada, {NAME[b]}, {nm}: linhas afinadas que mudam em {tr} (perdem / ganham)", f"{sum(1 for v in ft.values() if v['de'] and not v['para'])} / {sum(1 for v in ft.values() if not v['de'] and v['para'])}", "escada_vereditos")
# ---------------- round 6: negative control of Kvasir (resolvable / necessary / runs and ladder), currently only in docs/item3_criterio.md
SK = J("split_kvasir")
_nc = crit["bases"]["KVASIR"]["por_classe"]["negative_control"]; _ne = SK["sensibilidade"]["completo"]["negative_control"]
line("Kvasir-VQA-x1, controle negativo (3 templates, 728 perguntas): resoluveis / necessarias entre as resoluveis / linhas", f"{_nc['resoluveis']} / {_nc['B_entre_resoluveis']} / {_nc['n_linhas']}", "criterio")
line("criterio B sem condicao de headroom, Kvasir-VQA-x1, controle negativo (3 templates) (linhas necessarias / linhas)", f"{_nc['total']['B']}/{_nc['n_linhas']}", "criterio")
line("escada, Kvasir-VQA-x1, controle negativo (3 templates): L0 / L1 / L2 / L3 (linhas)", f"{_ne['escada']['L0']} / {_ne['escada']['L1']} / {_ne['escada']['L2']} / {_ne['escada']['L3']} de 27", "split_kvasir")
# ---------------- S2
L += ["", "## S2. Setup (bases, modelos, receitas, text-decoder-only, TF-IDF, proveniencia do encoder invertido)", ""]
for x in fm["fatos"]:
    if x["rotulo"].startswith(("receita", "text-decoder-only", "classificador")): line(x["rotulo"], x["valor"] if isinstance(x["valor"], str) else json.dumps(x["valor"]), "fatos_metodo")
for m, v in zs["modelos"].items():
    line(f"zero-shot {m}: checkpoint do Hub / snapshot / bytes dos pesos", f"{v['base_model']} / {', '.join(v['hub'].get('snapshots') or [])} / {v['hub'].get('safetensors_total_size_bytes')}", "zeroshot")
for b in BASES:
    for r in inv["lines"][b]:
        if r["pack"] != "12 de encoder invertido": continue
        st = r["stamps"].get("C0") or r["stamps"].get("T") or {}
        line(f"proveniencia {NAME[b]} {r['line']}: sha256 dos pesos (fonte)", f"{st.get('checkpoint_sha256')} ({st.get('fonte_do_sha')})", "inventario_linhas")
# ---------------- round 3: items 28, 29, 30, 31
R3J = J("rodada3")
NM3 = {"dependent_polyp": "pólipo", "dependent_instrument": "instrumento", "controle_texto": "controle \"Is there text?\"", "closed_yes": "fechada-sim", "closed_no": "fechada-não"}
def nm3(c): return NM3.get(c) or (f"fechada-sim, entidade {c.split('=', 1)[1]}" if c.startswith("entidade=") else f"fechada-sim, anatomia {c.split('=', 1)[1].split('|')[0]}")
Q28 = [("acc_C0", "acurácia intacta", "%", pct), ("acc_txt", "text-only arm", "%", pct), ("headroom", "image gain above the text-only arm", "pp", pp),
       ("custo_mascara_deslocada_preto", "custo do controle pareado, preto", "pp", pp), ("custo_mascara_deslocada_blur10", "custo do controle pareado, blur 10 %", "pp", pp),
       ("delta_preto", "Δ preto", "pp", pp), ("delta_blur10", "Δ blur 10 %", "pp", pp), ("delta_regmean", "Δ cor média", "pp", pp), ("suficiencia_preto", "suficiência (preto)", "razão", r3f)]
def mm(x, f): return "—" if not x else f"{f(x['min'])} – {f(x['max'])}"
def ci3(c): return "—" if not c else f"[{100 * c[0]:+.1f}, {100 * c[1]:+.1f}]"
def r3_block(b):
    for c, F in R3J["item28_faixas"][b].items():
        line(f"{NAME[b]}, {nm3(c)}: n perguntas por linha (faixas abaixo)", "/".join(str(x) for x in F["n_por_linha"]), "rodada3")
        for k, lab, u, f in Q28: line(f"{NAME[b]}, {nm3(c)}: {lab}, mínimo – máximo entre as {(F[k] or {}).get('n_linhas', 27)} linhas ({u})", mm(F[k], f), "rodada3")
    for c, X in R3J["item29_gain_tfidf"][b].items():
        line(f"{NAME[b]}, {nm3(c)}: image gain against the question-only classifier (TF-IDF), mínimo – máximo entre as {NL[b]} linhas (pp)", mm(X["faixa_gain_tfidf"], pp), "rodada3")
        for g, x in X["por_grupo"].items():
            line(f"{NAME[b]}, {nm3(c)}, {g}: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as {x['n_linhas']} linhas (pp); linhas com IC > 0", f"{msp(x['gain_tfidf'], pp)} / {msp(x['gain_txt'], pp)}; {x['gain_tfidf_ic_inf_maior_0']}/{x['n_linhas']} / {x['gain_txt_ic_inf_maior_0']}/{x['n_linhas']}", "rodada3")
        for ln, x in X["por_linha"].items():
            line(f"{NAME[b]}, {nm3(c)}, {ln}: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)", f"{pp(x['gain_tfidf'])} {ci3(x['gain_tfidf_ci'])} / {pp(x['gain_txt'])} {ci3(x['gain_txt_ci'])}", "rodada3")
FN = {"preto": "preto", "blur10": "blur 10 %", "regmean": "cor média"}
def r3_box():
    X = R3J["item30_caixa_artefato"]; T_ = f"artefact-box template (\"{X['template']}\")"
    line(f"Kvasir-VQA-x1, {T_}: perguntas avaliáveis / n por linha", f"{X['n_avaliaveis']} / " + "/".join(str(x) for x in sorted({v['n'] for v in X['linhas'].values()})), "rodada3")
    for ln, v in X["linhas"].items():
        line(f"Kvasir-VQA-x1, artefact-box template, {ln}: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)", " / ".join(f"{pp(v[f]['delta'])} {ci3(v[f]['ci'])}" for f in ("preto", "blur10", "regmean")), "rodada3")
    for nl, key in ((f"{N27} linhas", "contagens_27"), ("15 linhas de 01/10", "contagens_15")):
        for f, c in X[key].items():
            line(f"Kvasir-VQA-x1, artefact-box template, Δ {FN[f]}, {nl}: linhas com limite superior do IC < 0 / com limite inferior do IC > 0; mínimo – máximo (pp)", f"{c['ic_sup_menor_0']}/{c['n_linhas']} / {c['ic_inf_maior_0']}/{c['n_linhas']}; {pp(c['min'])} – {pp(c['max'])}", "rodada3")
    b4 = X["blur4"]
    for ln, v in b4["linhas"].items():
        if "blur4" in v: line(f"Kvasir-VQA-x1, artefact-box template, {ln}: Δ blur 4 % [IC] (pp)", f"{pp(v['blur4']['delta'])} {ci3(v['blur4']['ci'])}", "rodada3")
    c = b4["contagens_15"]
    line(f"Kvasir-VQA-x1, artefact-box template, Δ blur 4 %, {b4['n_linhas_com_predicoes']} linhas de 01/10 (as 12 de encoder invertido não têm predições sob blur 4 %): linhas com limite superior do IC < 0 / com limite inferior do IC > 0; mínimo – máximo (pp)", f"{c['ic_sup_menor_0']}/{c['n_linhas']} / {c['ic_inf_maior_0']}/{c['n_linhas']}; {pp(c['min'])} – {pp(c['max'])}", "rodada3")
    line("Kvasir-VQA-x1, artefact-box template, folha de 01/10 (15 linhas, IC por pergunta): IC exclui zero sob preto / blur 4 % / blur 10 % / cor média", "12/15 / 5/15 / 11/15 / 10/15", ("generator", f"{PREV_SHEETS}/numbers_isbi.md"))
S3_ = R3J["item31_setup"]
line("Kvasir-VQA-x1: perguntas distintas no teste (perguntas do teste) / entre as avaliáveis (avaliáveis)", f"{S3_['KVASIR']['distintas_teste']} ({S3_['KVASIR']['perguntas_teste']}) / {S3_['KVASIR']['distintas_avaliaveis']} ({S3_['KVASIR']['avaliaveis']})", "rodada3")
pc_ = S3_["KVASIR"]["por_classe_avaliaveis"]
line("Kvasir-VQA-x1: perguntas distintas entre as avaliáveis, pólipo / instrumento / controle negativo / pólipo secundário (perguntas)", " / ".join(f"{pc_[c]['distintas']} ({pc_[c]['n']})" for c in ("dependent_polyp", "dependent_instrument", "negative_control", "dependent_polyp_secondary")), "rodada3")
for b in ("HEAL", "MIMIC"):
    x = S3_[b]; line(f"{NAME[b]}: perguntas distintas nas fechadas avaliáveis (fechadas) / fechada-sim / fechada-não", f"{x['distintas_fechadas_avaliaveis']} ({x['fechadas_avaliaveis']}) / {x['por_classe']['closed_yes']['distintas']} ({x['por_classe']['closed_yes']['n']}) / {x['por_classe']['closed_no']['distintas']} ({x['por_classe']['closed_no']['n']})", "rodada3")
    line(f"{NAME[b]}: perguntas distintas no teste (perguntas do teste)", f"{x['distintas_teste']} ({x['perguntas_teste']})", "rodada3")
line("Kvasir-VQA-x1: templates (cada pergunta distinta é um template; sem campo de template no inventário), teste / avaliáveis", f"{S3_['KVASIR']['templates']['teste']} / {S3_['KVASIR']['templates']['avaliaveis']}", "rodada3")
th = S3_["HEAL"]["templates"]
line("HEAL-MedVQA: templates fechados / abertos (padrões de texto com achado e anatomia substituídos; perguntas sem casamento único: " + str(th["perguntas_sem_casamento_unico"]) + ")", f"{len(th['fechadas'])} / {len(th['abertas'])}", "rodada3")
line("HEAL-MedVQA: templates fechados (fechadas avaliáveis por template)", "; ".join(f"{t} ({v})" for t, v in th["fechadas_avaliaveis_por_template"].items()), "rodada3")
tm = S3_["MIMIC"]["templates"]
line("Medical-Diff-VQA: templates (template_id do inventário), teste / fechadas avaliáveis", f"{tm['teste']} / {tm['fechadas_avaliaveis']} ({', '.join(f'{k} {v}' for k, v in sorted(tm['ids_fechadas'].items()))})", "rodada3")
hd_ = S3_["HEAL"]["doses"]
line("HEAL-MedVQA: linhas nas médias de dose / linhas", f"{hd_['linhas_nas_medias']} / {hd_['linhas']}", "rodada3")
for ln, why in hd_["excluidas"].items(): line(f"HEAL-MedVQA: proveniência da linha fora das médias de dose ({ln})", f"{why}; original ausente também no Drive (S10)", "rodada3")
# ---------------- S3-S5 per benchmark
def base_block(b, sec):
    H = hd["bases"][b]; L.extend(["", f"## {sec}. {NAME[b]}", ""])
    for cls, nm in CLS[b]:
        if cls == "negative_control": continue
        n0 = next(iter(H["linhas"].values()))["classes"].get(cls, {})
        if not n0.get("n"): continue
        line(f"{NAME[b]}, {nm}: n perguntas / imagens (alinhadas)", f"{n0['n']} / {n0.get('n_imagens')}", "headroom")
        for g, gg in H["agregado_por_grupo"].items():
            x = gg.get(cls) or {}
            line(f"{NAME[b]}, {nm}, {g}: Acc intacta / text-decoder-only / TF-IDF (%)", f"{msp(x.get('acc.C0'))} / {msp(x.get('acc_txt'))} / {msp(x.get('acc_m0'))}", "headroom")
            line(f"{NAME[b]}, {nm}, {g}: headroom sobre o text-decoder-only (pp); linhas resoluveis", f"{msp(x.get('headroom'), pp)}; {x.get('resoluvel')}/{x.get('n_linhas')}", "headroom")
            line(f"{NAME[b]}, {nm}, {g}: Delta preto / blur 10 % / cor media (pp)", f"{msp(x.get('delta_preto'), pp)} / {msp(x.get('delta_blur10'), pp)} / {msp(x.get('delta_regmean'), pp)}", "headroom")
            line(f"{NAME[b]}, {nm}, {g}: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B", f"{msp(x.get('custo_mascara_deslocada_preto'), pp)} / {msr(x.get('suficiencia_preto'))} / {x.get('criterio_B')}/{x.get('n_linhas')}", "headroom")
        for key, nk in (("delta_preto", "Delta preto"), ("delta_blur10", "Delta blur 10 %"), ("delta_regmean", "Delta cor media"), ("headroom", "headroom"), ("custo_mascara_deslocada_preto", "custo da mascara deslocada, preto")):
            line(f"{NAME[b]}, {nm}: faixa de {nk} nas {NL[b]} linhas (pp)", rng(allrng(b, cls, key)), "headroom")
        line(f"{NAME[b]}, {nm}: faixa da suficiencia (preto) nas {NL[b]} linhas", rng(allrng(b, cls, "suficiencia_preto"), r3), "headroom")
base_block("KVASIR", "S3"); r3_block("KVASIR"); r3_box(); base_block("HEAL", "S4"); r3_block("HEAL")
H = hd["bases"]["HEAL"]
for g, gg in H["agregado_extra_por_grupo"].items():
    for k, x in gg.items():
        if not k.endswith("|closed_yes"): continue
        line(f"HEAL-MedVQA, fechada-sim, {k.split('|')[0].replace('anatomia=', '')}, {g}: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B", f"{x.get('n')} / {msp(x.get('acc.C0'))} / {msp(x.get('headroom'), pp)} / {msp(x.get('delta_preto'), pp)} / {msp(x.get('delta_blur10'), pp)} / {x.get('criterio_B')}", "headroom")
for k, n in hst["estrato_unidades"].items(): line(f"HEAL-MedVQA, estrato {k}: unidades / perguntas fechadas-sim / fechadas-nao", f"{n} / {hst['estrato_perguntas'][k]['closed_yes']} / {hst['estrato_perguntas'][k]['closed_no']}", "heal_estratificado")
for g, gv in hst["agregado_por_grupo"].items():
    for k, x in gv.items():
        line(f"HEAL-MedVQA, {k}, {g}: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B", f"{msp(x['custo_mascara_deslocada_preto'], pp)} / {msp(x['custo_mascara_deslocada_blur10'], pp)}; {msp(x['delta_preto'], pp)} / {msp(x['delta_blur10'], pp)}; {x['B']}/{x['n_linhas']}", "heal_estratificado")
base_block("MIMIC", "S5"); r3_block("MIMIC")
H = hd["bases"]["MIMIC"]; ents = [c for c in next(iter(H["linhas"].values()))["classes"] if c.startswith("entidade=")]
for e in ents:
    r0 = next(iter(H["linhas"].values()))["classes"][e]
    tot = sum(1 for r in H["linhas"].values() if (r["classes"].get(e) or {}).get("criterio_B"))
    line(f"Medical-Diff-VQA, fechada-sim, {e.replace('entidade=', '')}: n itens / imagens; criterio B (linhas)", f"{r0['n']} / {r0['n_imagens']}; {tot}/{NL['MIMIC']}", "headroom")
    for g, gg in H["agregado_por_grupo"].items():
        x = gg.get(e) or {}
        line(f"Medical-Diff-VQA, {e.replace('entidade=', '')}, {g}: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B", f"{msp(x.get('acc.C0'))} / {msp(x.get('acc_txt'))} / {msp(x.get('headroom'), pp)} / {msp(x.get('delta_preto'), pp)} / {msp(x.get('delta_blur10'), pp)} / {msp(x.get('custo_mascara_deslocada_preto'), pp)} / {msr(x.get('suficiencia_preto'))} / {x.get('criterio_B')}/{x.get('n_linhas')}", "headroom")
ENT19 = ["edema", "pleural effusion", "atelectasis", "lung opacity", "cardiomegaly"]
for e in ENT19:
    for ln, r in H["linhas"].items():
        k = r["classes"].get(f"entidade={e}") or {}
        if not k.get("n"): continue
        line(f"Medical-Diff-VQA, {e}, {ln}: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)", f"{pct(k.get('acc_txt'))} / {pct(k['acc'].get('C0'))}; {pp(k.get('headroom'))} {cpp(k.get('headroom_ci_by_image'))}; {pp(k.get('delta_preto'))} {cpp(k.get('delta_preto_ci_by_image'))}; {pp(k.get('delta_blur10'))} {cpp(k.get('delta_blur10_ci_by_image'))}", "headroom")
# ---------------- S6 oclusor
L += ["", "## S6. Oclusor em imagens sem o achado (taxa de afirmativa induzida)", ""]
for b in BASES:
    O = oc["bases"][b]
    for g, gg in O["agregado_por_grupo"].items():
        for c, x in gg.items():
            line(f"{NAME[b]}, {c}, {g}: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0", f"{msp(x['taxa_induzida'], pp)}; {x['n_ic_exclui_zero_por_cima']}/{x['n_linhas']} / {x['n_ic_exclui_zero_por_baixo']}/{x['n_linhas']}", "oclusor_negativos")
    ns = collections.defaultdict(set)
    for r in O["linhas"].values():
        for c, x in (r.get("conds") or {}).items(): ns[c].add(x.get("n"))
    for c, v in ns.items(): line(f"{NAME[b]}, {c}: itens por linha", "/".join(str(x) for x in sorted(v, key=lambda z: z or 0)), "oclusor_negativos")
# ---------------- S7 zero-shot
L += ["", "## S7. Zero-shot sob o mesmo teste", ""]
for m, v in zs["modelos"].items():
    gc = (v["hub"].get("generation_config") or {})
    line(f"zero-shot {m}: decodificacao (do_sample / temperature / max_new_tokens)", f"{gc.get('do_sample', 'nao definido (gulosa)')} / {gc.get('temperature', 'nao definido')} / {v['max_new_tokens']}", "zeroshot")
for b in BASES:
    for ln, r in zs["bases"][b].items():
        for cls, nm in CLS[b]:
            k = r["classes"].get(cls)
            if not k or not k.get("n") or "|" in cls or cls == "negative_control": continue
            line(f"zero-shot {ln}, {nm}: Acc intacta / sem imagem (%); headroom [IC] (pp)", f"{pct(k['acc'].get('C0'))} / {pct(k.get('acc_txt'))}; {pp(k.get('headroom'))} {cpp(k.get('headroom_ci_by_image'))}", "zeroshot")
            line(f"zero-shot {ln}, {nm}: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia", f"{pp(k.get('delta_preto'))} {cpp(k.get('delta_preto_ci_by_image'))} / {pp(k.get('delta_blur10'))} {cpp(k.get('delta_blur10_ci_by_image'))}; {'sim' if k.get('criterio_B') else 'nao'}; {r3(k.get('suficiencia_preto'))}", "zeroshot")
L += ["", "## S7b. Leitura conjunta sim/nao (HEAL-MedVQA e Medical-Diff-VQA)", ""]
for b in ("HEAL", "MIMIC"):
    for g, gv in sn["bases"][b]["agregado_por_grupo"].items():
        for k, x in gv.items():
            if k == "n_linhas": continue
            line(f"{NAME[b]}, {g}, {k}: sensibilidade / especificidade / taxa afirmativa (%)", f"{msp(x['sensibilidade'])} / {msp(x['especificidade'])} / {msp(x['taxa_afirmativa'])}", "simnao")
    for ln, v in sn["bases"][b]["linhas"].items():
        if not v["zero_shot"]: continue
        for k, x in v["condicoes"].items():
            line(f"{NAME[b]}, zero-shot {ln.split('_ZEROSHOT')[0]}, {k}: sensibilidade / especificidade / taxa afirmativa (%) [IC]", f"{pct(x['sensibilidade'])} / {pct(x['especificidade'])} / {pct(x['taxa_afirmativa'])} [{100 * x['taxa_afirmativa_ci'][0]:.1f}, {100 * x['taxa_afirmativa_ci'][1]:.1f}]", "simnao")
# ---------------- S8 doses
L += ["", "## S8. Doses (mascara dilatada 1,5x e 2x, preto, subconjunto pareado)", ""]
for b in BASES:
    Dd = ds["bases"][b]; line(f"{NAME[b]}: unidades validas em 1,5x e 2x / unidades; perguntas pareadas", f"{Dd['unidades_validas_1.5_e_2']} / {Dd['unidades_base']}; {Dd['qids_pareados']}", "doses")
    for g, gg in Dd["agregado_por_grupo"].items():
        for cls, x in gg.items():
            nm = dict(CLS[b]).get(cls, cls)
            line(f"{NAME[b]}, {nm}, {g} ({x.get('n_linhas')} linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0", f"{x['n_pareado']} / {x['n_classe']}; {msp(x['1']['delta'], pp)} / {msp(x['1.5']['delta'], pp)} / {msp(x['2']['delta'], pp)}; {x['1']['n_ic_exclui_zero_por_cima']} / {x['1.5']['n_ic_exclui_zero_por_cima']} / {x['2']['n_ic_exclui_zero_por_cima']}", "doses")
    for ln, why in Dd.get("excluidas_das_medias", {}).items(): line(f"{NAME[b]}: linha fora das medias de dose", f"{ln}: {why}", "doses")
# ---------------- S9 method and statistics
L += ["", "## S9. Metodo e estatistica", ""]
line("bootstrap por imagem: replicas / semente / imagens por base (Kvasir / HEAL / MIMIC)", f"2000 / 20260913 / {raw['bases']['KVASIR']['n_imagens_replicas']} / {raw['bases']['HEAL']['n_imagens_replicas']} / {raw['bases']['MIMIC']['n_imagens_replicas']}", "bases_raw")
for b in BASES: line(f"Holm por linha, familia de classes, {NAME[b]}", ", ".join(raw["bases"][b]["familia_holm"]), "bases_raw")
line("regra de resolubilidade (headroom legivel)", "limite inferior do IC 95 % por imagem do headroom (Acc intacta - text-only arm da mesma familia e semente; zero-shot: com imagem - sem imagem) > 0; sem limiar de 0,10 (a rodada 1 usou tambem headroom >= 0,10; as duas versoes estao em criterio.json)", ("generator", "criterio"))
line("independencia das linhas", f"as {N27} linhas por base sao 3 sementes x {N27 // 3} configuracoes (familia x adaptador x encoder) e nao sao independentes; as proporcoes necessarias / resoluveis / linhas sao descritivas, sem IC", ("generator", "common"))
line("artefact-box template (Kvasir-VQA-x1): estatística", f"IC 95 % por imagem (réplicas fixas da base Kvasir) nas {N27} linhas, sob preto, blur 10 % e cor média; blur 4 % = sigma fixo de {R3J['item30_caixa_artefato']['blur4']['sigma']['blur_sigma_px']:.0f} px (sigma / largura mediana {R3J['item30_caixa_artefato']['blur4']['sigma']['sigma_sobre_largura_kvasir']['median']:.3f} no Kvasir), predições só nas 15 linhas de 01/10; a folha de 01/10 usava IC por pergunta", "rodada3")
line("image gain against the question-only classifier (TF-IDF)", "Acc(intacta) - Acc(TF-IDF) nos mesmos itens, IC por imagem; Medical-Diff-VQA: TF-IDF do subconjunto nas fechadas (piso composto); ilustração apenas, não muda contagem nenhuma (a escada com TF-IDF fica só interna)", ("generator", "rodada3"))
line("McNemar", "mid-p exato (binomial, meio peso no observado) nos discordantes entre mascara deslocada e alvo ocluido (shamstats.mcnemar_midp)", ("generator", "bases_raw"))
for x in fm["fatos"]:
    if not x["rotulo"].startswith(("receita", "text-decoder-only", "classificador")): line(x["rotulo"], x["valor"] if isinstance(x["valor"], str) else json.dumps(x["valor"]), "fatos_metodo")
# ---------------- S10 limitacoes
L += ["", "## S10. Limitacoes", ""]
c = gh["contagens"]; fr = gh["fracoes"]
line("HEAL: perguntas / unidades em imagens com >= 2 anatomias anotadas", f"{c['perguntas_2+']} / {c['unidades_2+']} (de {c['perguntas']} / {c['unidades']})", "placebo_geometry_heal")
line("HEAL: unidades em que a mascara deslocada toca outra anatomia (qualquer / > 50 % da outra)", f"{c['unidades_qualquer_sobreposicao']} / {c['unidades_sobreposicao_maior_50pct_da_outra']} de {c['unidades_2+']} ({100 * fr['unidades_qualquer_sobre_2+']:.1f} % / {100 * fr['unidades_maior50_sobre_2+']:.1f} %)", "placebo_geometry_heal")
line("HEAL: perguntas afetadas (qualquer / > 50 %) sobre o total", f"{c['perguntas_qualquer_sobreposicao']} / {c['perguntas_sobreposicao_maior_50pct_da_outra']} de {c['perguntas']}", "placebo_geometry_heal")
cm = gm["contagens"]; line("Medical-Diff-VQA: unidades em que alguma caixa da mascara deslocada toca outra regiao-folha (qualquer / > 50 % da outra)", f"{cm['unidades_qualquer_sobreposicao']} / {cm['unidades_sobreposicao_maior_50pct_da_outra']} de {cm['unidades']}", "placebo_geometry_mimic")
kvf = {x["rotulo"]: x["valor"] for x in fm["fatos"]}
line("Kvasir: mascaras (Kvasir-SEG polipos / Kvasir-Instrument instrumentos casados)", kvf["Kvasir: mascaras casadas (Kvasir-SEG polipos / Kvasir-Instrument instrumentos)"], "fatos_metodo")
xi = hd["bases"]["KVASIR"]["agregado_por_grupo"]; mi_ = [((g.get("dependent_instrument") or {}).get("acc_m0") or {}).get("media") for g in xi.values()]
line("Kvasir: TF-IDF no instrumento (acuracia, todas as linhas)", ", ".join(sorted({pct(x) for x in mi_ if x is not None})), "headroom")
line("HEAL: fechadas sem posicao valida da mascara deslocada", kvf["HEAL: fechadas sem posicao valida"], "fatos_metodo")
for k, v in zs["respostas_fora_do_formato_C0"].items():
    if k.startswith("LLAVA_MED"):
        cls_ = sorted({kk.split("|")[0] for kk in v})
        line(f"LLaVA-Med {k.split('_')[-1]}: por classe, acuracia da intacta (%) / respostas vazias / com mais de 5 palavras / fechadas fora de yes-no, sobre o total", "; ".join(f"{cc} {v.get(cc + '|acuracia_C0_x1000', 0) / 10:.1f} / {v.get(cc + '|vazia', 0)} / {v.get(cc + '|mais_de_5_palavras', 0)} / {v.get(cc + '|fechada_fora_de_yes_no', 0)} de {v.get(cc + '|total')}" for cc in cls_), "zeroshot")
line("decodificacao com amostragem (do_sample = True no generation_config do Hub, temperatura 1e-6)", ", ".join(m for m, v in zs["modelos"].items() if (v["hub"].get("generation_config") or {}).get("do_sample")), "zeroshot")
line("HEAL-MedVQA: controle de posicao por geometria (unidades: uma anatomia / varias sem sobreposicao / varias com sobreposicao)", " / ".join(str(hst["estrato_unidades"][k]) for k in ("a_uma_anatomia", "b_multi_sem_sobreposicao", "c_multi_com_sobreposicao")), "heal_estratificado")
line("Medical-Diff-VQA: as regioes-folha do Chest ImaGenome cobrem o torax inteiro; qualquer caixa deslocada toca outra regiao por construcao", f"{cm['unidades_qualquer_sobreposicao']} de {cm['unidades']} unidades", "placebo_geometry_mimic")
line("natureza do alvo por base", "Kvasir-VQA-x1: mascara binaria de segmentacao (Kvasir-SEG / Kvasir-Instrument, harness/isbi_placebo/inventory_kvasir.py, masks.binarize_mask); HEAL-MedVQA: mascara de segmentacao em RLE (harness/isbi_placebo/heal/heal_rle.py, decode_rle); Medical-Diff-VQA: caixa anatomica (bounding box) do Chest ImaGenome (v7_mimic/scripts/16_inventory_mimic.py, box_mask) -- a mascara deslocada no Medical-Diff-VQA tambem e caixa", ("generator", "fatos_metodo"))
line("adapter original de QWEN2VL_DORA_HEAL_seed2 no Drive (rclone lsf, sem download)", "nao encontrado em gdrive:Pesquisa/doutorado/ (outputs_models tem qwen2vl_dora_heal_seed0 e seed1) nem em gdrive:doutorado/pesquisa/P0_ICDIP/checkpoints_backup/ (log v7_artigo1/logs/rclone_lsf_dora_heal_seed2.txt)", ("generator", f"{OUT}/logs/rclone_lsf_dora_heal_seed2.txt"))
line("predicoes sem sha de checkpoint recuperavel", f"{len(inv['nao_carimbados'])} ({', '.join(sorted({x['line'] for x in inv['nao_carimbados']}))}: adapter original ausente na gpu1)", "inventario_linhas")
line("suficiencia sob blur 10 % e cor media", "so no Medical-Diff-VQA; Kvasir e HEAL nao tem S_blur10/S_regmean (54 linhas); suficiencia so sob preto", ("generator", "inventario_linhas"))
line("composicao de lote", kvf["composicao de lote (0,6-0,7 %)"], "fatos_metodo")
line("Medical-Diff-VQA: 473 / 443 fechadas-sim", U["MIMIC"]["explicacao_473_443"], "inventario_linhas")
# ---------------- round 6: Kvasir-VQA-x1 split (S10) and sensitivity without the 2 duplicated units (S-split)
_o = SK["oficial_hf"]; _n = SK["nosso_split"]
line("Kvasir-VQA-x1, split oficial do HF: imagens do teste oficial que aparecem no treino oficial, por img_id / imagens do teste oficial", f"{_o['imagens_do_teste_no_treino']} / {_o['imagens_do_teste']}", "split_kvasir")
line("Kvasir-VQA-x1, split oficial do HF: pares pergunta-resposta (treino / teste)", f"{_o['train']['pares_pergunta_resposta']} / {_o['test']['pares_pergunta_resposta']}", "split_kvasir")
line("Kvasir-VQA-x1, nosso split: imagens (treino / val / teste)", " / ".join(str(_n["arquivos"][k]["imagens"]) for k in ("train", "val", "test")), "split_kvasir")
line("Kvasir-VQA-x1, nosso split: intersecoes por image_id (treino-teste / val-teste / treino-val)", f"{_n['por_image_id']['treino_teste']} / {_n['por_image_id']['val_teste']} / {_n['por_image_id']['treino_val']}", "split_kvasir")
_b = _n["por_bytes_md5"]
line("Kvasir-VQA-x1, nosso split: imagens do teste que sao copia byte a byte (md5) de uma imagem do treino / da val (outro image_id)", f"{_b['teste_com_copia_no_treino']} / {_b['teste_com_copia_na_val']}", "split_kvasir")
line("Kvasir-VQA-x1, nosso split: imagens da val com copia byte a byte no treino; md5 repetidos dentro do teste", f"{_b['val_com_copia_no_treino']}; {_b['md5_repetidos_dentro_do_teste']}", "split_kvasir")
line("Kvasir-VQA-x1: unidades do teste de necessidade com copia byte a byte no treino ou na val / unidades", f"{len(_n['unidades']['duplicadas'])} / {_n['unidades']['n']}", "split_kvasir")
L += ["", "## S-split. Sensibilidade sem as 2 unidades duplicadas (Kvasir-VQA-x1; so o que muda)", ""]
for u in _n["unidades"]["duplicadas"]:
    line(f"unidade duplicada {u['image_id']}: copia no treino; perguntas avaliaveis retiradas por classe", f"{', '.join(u['copia_no_treino'] + u['copia_na_val'])}; " + ", ".join(f"{k} {v}" for k, v in sorted(SK["perguntas_avaliaveis_nas_unidades"][u["image_id"]].items())), "split_kvasir")
line("perguntas retiradas por classe (polipo / instrumento / controle negativo / polipo secundario / 'Is there text?' / artefact-box template)", " / ".join(str(SK["qids_retirados_por_classe"][k]) for k in ("dependent_polyp", "dependent_instrument", "negative_control", "dependent_polyp_secondary", "controle_texto", "artefato")), "split_kvasir")
line("regra", "mesmo engine e mesma matriz de replicas (2 000, semente 20260913, todas as imagens do inventario); so os qids das 2 imagens saem; nada re-inferido", ("generator", "split_kvasir"))
_C, _S = SK["sensibilidade"]["completo"], SK["sensibilidade"]["sem_duplicadas"]; _ig = []
NMS = {"dependent_polyp": "polipo", "dependent_instrument": "instrumento", "negative_control": "controle negativo (3 templates)"}
for c, nm in NMS.items():
    if _C[c]["escada"] == _S[c]["escada"] and (_C[c]["resoluveis"], _C[c]["B_entre_resoluveis"]) == (_S[c]["resoluveis"], _S[c]["B_entre_resoluveis"]): _ig.append(f"escada e resoluveis/necessarias de {nm}")
    else: line(f"sem as 2 unidades, Kvasir-VQA-x1, {nm}: L0 / L1 / L2 / L3; resoluveis / necessarias / linhas", f"{_S[c]['escada']['L0']} / {_S[c]['escada']['L1']} / {_S[c]['escada']['L2']} / {_S[c]['escada']['L3']}; {_S[c]['resoluveis']} / {_S[c]['B_entre_resoluveis']} / 27", "split_kvasir")
    if _C[c]["n_por_linha"] != _S[c]["n_por_linha"]: line(f"sem as 2 unidades, Kvasir-VQA-x1, {nm}: n perguntas por linha (completo: {'/'.join(map(str, _C[c]['n_por_linha']))})", "/".join(map(str, _S[c]["n_por_linha"])), "split_kvasir")
    for k, lab, u, f in Q28:
        if k not in _C[c]["faixas"]: continue
        a, b = mm(_C[c]["faixas"][k], f), mm(_S[c]["faixas"][k], f)
        if a == b: _ig.append(f"{nm}: {lab}"); continue
        line(f"sem as 2 unidades, Kvasir-VQA-x1, {nm}: {lab}, mínimo – máximo entre as 27 linhas ({u}) (completo: {a})", b, "split_kvasir")
_pk = {x["line"]: x["pack"] for x in lines("KVASIR")}; _pl = SK["sensibilidade"]["por_linha_sem_duplicadas"]
for f, fn in (("preto", "preto"), ("blur10", "blur 10 %"), ("regmean", "cor média")):
    for nl, sel in ((f"{N27} linhas", lambda ln: True), ("15 linhas de 01/10", lambda ln: _pk[ln].startswith("15 de"))):
        cis = [_pl[ln]["artefato"][f"delta_{f}_ci_by_image"] for ln in _pl if sel(ln)]; up = sum(1 for c_ in cis if c_[1] < 0); lw = sum(1 for c_ in cis if c_[0] > 0)
        old = R3J["item30_caixa_artefato"]["contagens_27" if nl == f"{N27} linhas" else "contagens_15"][f]
        if (up, lw) == (old["ic_sup_menor_0"], old["ic_inf_maior_0"]): _ig.append(f"artefact-box template, Δ {fn}, {nl}: {up}/{len(cis)} / {lw}/{len(cis)}"); continue
        line(f"sem as 2 unidades, Kvasir-VQA-x1, artefact-box template, Δ {fn}, {nl}: linhas com limite superior do IC < 0 / com limite inferior do IC > 0 (folha completa: {old['ic_sup_menor_0']}/{len(cis)} / {old['ic_inf_maior_0']}/{len(cis)})", f"{up}/{len(cis)} / {lw}/{len(cis)}", ("split_kvasir", "rodada3"))
line("sem as 2 unidades: quantidades que nao mudam no valor impresso", "; ".join(_ig), ("split_kvasir", "rodada3"))
# ---------------- round 8: checks of the extra runs
R8 = J("rodada8")
L += ["", "## S12. Verificacoes adicionais (rodada 8)", ""]
NM8 = {"dependent_polyp": "polipo", "dependent_instrument": "instrumento", "negative_control": "controle negativo (3 templates)", "closed_yes": "fechada-sim", "closed_no": "fechada-nao"}
for k, x in R8["item1"].items():
    b, c, kind = k.split("|")
    line(f"{NAME[b]}, {NM8[c]}, {'afinados' if kind == 'afinados' else 'zero-shot (4 modelos)'}: L3 e L0 / L3 / linhas", f"{x['L3_e_L0']} / {x['L3']} / {x['linhas']}", "rodada8")
_g = R8["item1_mimic_ganham_L0_L1_entre_os_L3"]
line("Medical-Diff-VQA, fechada-sim, afinados: linhas que passam em L1 sem passar em L0 / delas entre as L3", f"{len(_g['ganham'])} / {len(_g['entre_os_L3'])}", "rodada8")
I3 = R8["item3"]
line("Kvasir-VQA-x1, instrumento, baseline sem imagem: acuracia nas 9 linhas (3 familias x 3 sementes) (%)", ", ".join(sorted({f"{100 * v['acuracia']:.1f}" for v in I3["por_arquivo"].values()})), "rodada8")
line("Kvasir-VQA-x1, instrumento, baseline sem imagem: respostas previstas (pergunta -> resposta: vezes nas 9 linhas)", "; ".join(f"{k}: {n}" for k, n in I3["previstas_9_arquivos"].items()), "rodada8")
for t, r in I3["referencia_por_template"].items():
    line(f"Kvasir-VQA-x1, instrumento, respostas de referencia, '{t}': respostas distintas; mais frequentes (vezes); contem 'none' ou '0'", f"{r['distintas']}; " + ", ".join(f"{a} {n}" for a, n in r["top"]) + f"; {'sim' if r['contem_none_ou_0'] else 'nao'}", "rodada8")
for t, r in I3["treino_por_template"].items():
    line(f"Kvasir-VQA-x1, treino, '{t}': perguntas; resposta majoritaria (fracao %)", f"{r['n']}; {r['top'][0][0]} ({100 * r['frac_majoritaria']:.1f})", "rodada8")
I4 = R8["item4"]
line("Holm (regra)", "p unilateral bootstrap por criterio (fracao das 2 000 replicas por imagem <= 0); Holm por linha sobre a familia de classes registrada (Kvasir: polipo, instrumento, 'Is there text?'; controle negativo de 3 templates no lugar de 'Is there text?' para a linha dele; HEAL: sim, nao; Medical-Diff-VQA: sim, nao e as 6 entidades); passa se p ajustado < 0,025", "rodada8")
line("Holm: testes em que p < 0,025 concorda / discorda da regra do IC (sem Holm)", f"{I4['consistencia_p_menor_0025_vs_regra_do_IC'].get('igual', 0)} / {I4['consistencia_p_menor_0025_vs_regra_do_IC'].get('diferente', 0)}", "rodada8")
NM4 = {"KVASIR|dependent_polyp": "Kvasir-VQA-x1, polipo", "KVASIR|dependent_instrument": "Kvasir-VQA-x1, instrumento", "KVASIR|negative_control": "Kvasir-VQA-x1, controle negativo (3 templates)", "HEAL|closed_yes": "HEAL-MedVQA, fechada-sim",
       "HEAL|closed_no": "HEAL-MedVQA, fechada-nao", "MIMIC|closed_yes": "Medical-Diff-VQA, fechada-sim", "MIMIC|closed_no": "Medical-Diff-VQA, fechada-nao", "MIMIC|closed_yes|zero_shot": "Medical-Diff-VQA, fechada-sim, zero-shot (4 modelos)"}
for k, x in I4["tabela1"].items():
    line(f"{NM4[k]}: L0 / L1 / L2 / L3 com Holm (sem Holm, p bootstrap < 0,025)", f"{' / '.join(str(x['com_holm'][d]) for d in ('L0', 'L1', 'L2', 'L3'))} de {x['linhas']} ({' / '.join(str(x['sem_holm'][d]) for d in ('L0', 'L1', 'L2', 'L3'))})", "rodada8")
for c, x in R8["item5"]["contagens"].items():
    line(f"Kvasir-VQA-x1, {NM8[c]}, 15 linhas de 01/10: dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %", f"{x['L3_blur4']} / {x['L3_blur10']} de {x['linhas']}", "rodada8")
    line(f"Kvasir-VQA-x1, {NM8[c]}, 15 linhas de 01/10: L2 com blur 4 % / com blur 10 %; Delta blur 4 %, minimo – maximo (pp)", f"{x['L2_blur4']} / {x['L2_blur10']}; {pp(x['delta_blur4_min'])} – {pp(x['delta_blur4_max'])}", "rodada8")
for b, x in R8["item7"].items():
    if not isinstance(x, dict) or "train" not in x: continue
    for sp in ("train", "val"):
        y = x[sp]; line(f"{NAME[b]}, fine-tuning, {'treino' if sp == 'train' else 'validacao'}: arquivo; imagens / pares pergunta-resposta / bytes", f"{y['arquivo'].split(f"{W}/", 1)[-1]}; {y['imagens']} / {y['pares_pergunta_resposta']} / {y['bytes']}", "rodada8")
line("HEAL-MedVQA e Medical-Diff-VQA: nota dos arquivos de treino", R8["item7"]["nota"], "rodada8")
# ---------------- round 9: Holm with the Table 1 family; variant of Table 1 with the raw drop
HF = J("holm_familias")
L += ["", "## S13. Holm por familia da Tabela 1 e variante com queda bruta (rodada 9)", ""]
line("Holm, familias (rodada 9)", "familia da Tabela 1: Kvasir-VQA-x1 {polipo, instrumento, controle negativo}; HEAL-MedVQA {sim, nao}; Medical-Diff-VQA {sim, nao}. Familia da rodada 8: Kvasir-VQA-x1 {polipo, instrumento, 'Is there text?'} (controle negativo com ele no lugar de 'Is there text?'); HEAL-MedVQA {sim, nao}; Medical-Diff-VQA {sim, nao e as 6 entidades} (8 testes). Mesmos p unilaterais bootstrap; passa se p ajustado < 0,025", ("generator", "holm_familias"))
NM9 = {"dependent_polyp": "polipo", "dependent_instrument": "instrumento", "negative_control": "controle negativo (3 templates)", "closed_yes": "fechada-sim", "closed_no": "fechada-nao"}
for k in HF["contagens"]["tabela1"]:
    b, c, kind = k.split("|"); a, r = HF["contagens"]["tabela1"][k], HF["contagens"]["rodada8"][k]; sm = HF["sem_holm"][k]; d = HF["discordancias_p_vs_IC"][k]
    nm = f"{NAME[b]}, {NM9[c]}, {'afinados' if kind == 'afinados' else 'zero-shot (4 modelos)'}"
    line(f"{nm}: L0 / L1 / L2 / L3 com Holm, familia da Tabela 1", f"{a['L0']} / {a['L1']} / {a['L2']} / {a['L3']} de {a['linhas']}", "holm_familias")
    line(f"{nm}: L0 / L1 / L2 / L3 com Holm, familia da rodada 8{' (8 testes)' if b == 'MIMIC' else ''}", f"{r['L0']} / {r['L1']} / {r['L2']} / {r['L3']} de {r['linhas']}", "holm_familias")
    line(f"{nm}: L0 / L1 / L2 / L3 sem Holm (p bootstrap < 0,025)", f"{sm['L0']} / {sm['L1']} / {sm['L2']} / {sm['L3']} de {sm['linhas']}", "holm_familias")
    line(f"{nm}: testes em que p < 0,025 e a regra do IC discordam / testes", f"{d['discordam']} / {d['testes']}", "holm_familias")
R8b = J("rodada8")["item1"]
MAPV = [("Kvasir-VQA-x1 & polyp", "KVASIR|dependent_polyp|afinados"), ("Kvasir-VQA-x1 & instrument", "KVASIR|dependent_instrument|afinados"), ("Kvasir-VQA-x1 & negative control", "KVASIR|negative_control|afinados"),
        ("HEAL-MedVQA & closed-ended, yes-questions", "HEAL|closed_yes|afinados"), ("HEAL-MedVQA & closed-ended, no-questions", "HEAL|closed_no|afinados"), ("Medical-Diff-VQA & closed-ended, yes-questions", "MIMIC|closed_yes|afinados"),
        ("Medical-Diff-VQA & closed-ended, no-questions", "MIMIC|closed_no|afinados"), ("Medical-Diff-VQA & yes-questions, zero-shot (4 models)", "MIMIC|closed_yes|zero_shot")]
for row, k in MAPV:
    x = R8b[k]; ns = (k == "MIMIC|closed_no|afinados")   # previous column n.s. in Table 1 (no run with a significant gain)
    line(f"Tabela 1, variante com queda bruta (tables/table_criteria_rawdrop.tex), linha '{row}': coluna '...and raw drop' (L3 e L0)", "n.s." if ns else f"{x['L3_e_L0']}", "rodada8")
# ---------------- round 11: final declaration (two fills, significant gain and raw drop) per group
DR = J("declarados_r11"); SRC["declarados_r11"] = ("v7_artigo1/analysis/declarados_r11.json", sha(f"{A}/declarados_r11.json")[:12])
L += ["", "## S15. Declaracao final por grupo: dois preenchimentos, ganho significativo e queda bruta (rodada 11)", ""]
line("declaracao final (regra)", DR["regra"] + "; decisao do Claudio de 21/10/2026", "declarados_r11")
for k, x in DR["classes"].items():
    b, c = k.split("|"); nm = dict(CLS[b]).get(c, "controle negativo (3 templates)" if c == "negative_control" else c)
    line(f"{NAME[b]}, {nm}: declarados (dois preenchimentos, ganho significativo e queda bruta) / linhas", f"{x['declarados']} / {x['runs']}", "declarados_r11")
    for g, y in x["por_grupo"].items():
        line(f"{NAME[b]}, {nm}, {g}: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas", f"{y['declarados']} / {y['resoluveis']} / {y['runs']}", "declarados_r11")
# ---------------- round 12: maxima of Delta among the declared runs; Medical-Diff-VQA entities under the final rule
R12 = J("rodada12"); SRC["rodada12"] = ("v7_artigo1/analysis/rodada12.json", sha(f"{A}/rodada12.json")[:12])
L += ["", "## S16. Maximos de Delta entre os declarados e entidades pela regra final (rodada 12)", ""]
NM12 = {"dependent_polyp": "polipo", "dependent_instrument": "instrumento", "closed_yes": "fechada-sim"}
for k, x in R12["item1"].items():
    b, c = k.split("|")
    line(f"{NAME[b]}, {NM12[c]}: Delta preto maximo entre os {x['declarados']} runs declarados (dois preenchimentos, ganho significativo e queda bruta) / maximo entre os {NL[b]} (pp)", f"{pp(x['max_delta_preto_declarados']) if x['max_delta_preto_declarados'] is not None else '—'} / {pp(x['max_delta_preto_27'])}", "rodada12")
for e, x in R12["item2"].items():
    line(f"Medical-Diff-VQA, fechada-sim, entidade {e} ({x['perguntas']} perguntas): runs com ganho significativo / declarados (dois preenchimentos, ganho significativo e queda bruta) / runs", f"{x['ganho_significativo']} / {x['declarados_L3_e_L0']} / {x['runs']}", "rodada12")
# ---------------- round 10: Holm of the raw-drop column; blur 4 % on the three benchmarks
HR = J("holm_rawdrop"); B4 = J("blur4_r10"); BM_ = json.load(open(f"{BLUR4_META}/manifest_blur4_r10.json")); AD_ = json.load(open(f"{BLUR4_META}/manifest_adaptadores_blur4_r10.json"))
SRC["blur4_manifest"] = ("data/blur4/manifest_blur4_r10.json", sha(f"{BLUR4_META}/manifest_blur4_r10.json")[:12])
SRC["blur4_adaptadores"] = ("data/blur4/manifest_adaptadores_blur4_r10.json", sha(f"{BLUR4_META}/manifest_adaptadores_blur4_r10.json")[:12])
L += ["", "## S14. Holm da coluna com queda bruta e blur 4 % nas tres bases (rodada 10)", ""]
for row, k in MAPV:
    a, r = HR["contagens"]["tabela1"][k], HR["contagens"]["rodada8"][k]; ns = (k == "MIMIC|closed_no|afinados")
    line(f"Tabela 1, variante com queda bruta, linha '{row}': '...and raw drop' (L3 e L0) com Holm, familia da Tabela 1 / familia da rodada 8", "n.s. / n.s." if ns else f"{a['L3_e_L0_holm']} / {r['L3_e_L0_holm']} de {a['linhas']}", "holm_rawdrop")
KVR = json.load(open(f"{KV_META}/blur_sigma_report.json"))
line("Kvasir-VQA-x1: blur 4 % (T_blur/P_blur), sigma fixo (px) / razao sigma/largura mediana", f"{KVR['blur_sigma_px']:.0f} / {KVR['datasets']['kvasir']['sigma_over_width']['median']:.4f}", f"{KV_META}/blur_sigma_report.json")
for k, nm in (("heal", "HEAL-MedVQA"), ("mimic", "Medical-Diff-VQA")):
    x = BM_[k]
    line(f"{nm}: blur 4 % (T_blur/P_blur), sigma fixo (px) / largura mediana (px) / razao sigma/largura mediana (min - max por unidade); razao se fossem 25 px", f"{x['sigma_px']:.2f} / {x['largura_mediana_px']:.0f} / {x['razao_sigma_largura_mediana']:.4f} ({x['razao_por_unidade']['min']:.4f} - {x['razao_por_unidade']['max']:.4f}); {x['razao_se_fossem_25px']:.4f}", "blur4_manifest")
    line(f"{nm}: blur 4 %, unidades; T preto regerado identico ao arrow existente (pixels)", f"{x['unidades']}; {x['T_preto_pixels_identicos_ao_arrow_existente']}", "blur4_manifest")
nconf = sum(1 for v in AD_.values() if v.get("confere")); line("adaptadores e checkpoints da inferencia de blur 4 % conferidos contra o carimbo da C0 (sha256) / total; excecao", f"{nconf} / {len(AD_)}; HEAL-MedVQA QWEN2VL_DORA_HEAL_seed2 no adapter do retreino de 03/10 (original ausente na gpu1), fora das contagens", "blur4_adaptadores")
NM10 = {"dependent_polyp": "polipo", "dependent_instrument": "instrumento", "negative_control": "controle negativo (3 templates)", "closed_yes": "fechada-sim", "closed_no": "fechada-nao"}
for k, x in B4["contagens"].items():
    b, c, sub = k.split("|"); sub_ = {"27_runs": "todos os runs", "15_runs_01_10": "15 runs de 01/10", "12_runs_invertidos": "12 runs de encoder invertido"}[sub]
    nm = f"{NAME[b]}, {NM10[c]}, {sub_} ({x['runs']})"
    line(f"{nm}: Delta blur 4 %, minimo – maximo (pp)", f"{pp(x['delta_blur4_min'])} – {pp(x['delta_blur4_max'])}", "blur4_r10")
    line(f"{nm}: dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %", f"{x['L3_blur4']} / {x['L3_blur10']}", "blur4_r10")
    line(f"{nm}: L3 e queda bruta (L0) com blur 4 % / com blur 10 %", f"{x['L3_blur4_e_L0']} / {x['L3_blur10_e_L0']}", "blur4_r10")
for k, v in B4["por_linha"].items():
    if not v["fora_das_contagens"]: continue
    b, ln = k.split("|")
    line(f"{NAME[b]}, {ln} (blur 4 % no adapter do retreino de 03/10; fora das contagens): Delta blur 4 % [IC] por classe (pp)", "; ".join(f"{NM10[c]} {pp(v[c]['delta_blur4'])} {cpp(v[c]['delta_blur4_ci'])}" for c in ("closed_yes", "closed_no")), "blur4_r10")
# ---------------- round 13: blur scale and raw drop under blur
R13 = J("rodada13"); SRC["rodada13"] = ("v7_artigo1/analysis/rodada13.json", sha(f"{A}/rodada13.json")[:12])
L += ["", "## S17. Escala do blur e queda bruta sob blur (rodada 13)", ""]
line("mascara do alvo nos itens 1-2 (regra)", "uniao dos pixels alterados pelo preto, pelo blur 10 % ou pelo blur 4 % em relacao a imagem intacta; alteracao = media absoluta, na escala 0-255, da media dos canais dentro da mascara", ("generator", "rodada13"))
mq = lambda x, f="{:.1f}": f"{f.format(x['mediana'])} [{f.format(x['q1'])}, {f.format(x['q3'])}]"
for b, x in R13["itens_1_2"].items():
    nm = NAME[b]
    line(f"{nm}: pares imagem-alvo medidos", f"{x['pares']}", "rodada13")
    line(f"{nm}: alteracao media dentro do alvo, preto / blur 10 % / blur 4 % (0-255; mediana [IQR])", f"{mq(x['alteracao_preto'])} / {mq(x['alteracao_blur10'])} / {mq(x['alteracao_blur4'])}", "rodada13")
    line(f"{nm}: razao blur 10 % / preto e blur 4 % / preto da alteracao dentro do alvo (mediana [IQR])", f"{mq(x['razao_blur10_preto'], '{:.3f}')} / {mq(x['razao_blur4_preto'], '{:.3f}')}", "rodada13")
    line(f"{nm}: diametro equivalente do alvo, px / % da largura (mediana [IQR])", f"{mq(x['diametro_px'])} / {mq(x['diametro_pct_largura'])}", "rodada13")
    line(f"{nm}: sigma / diametro do alvo, blur 4 % / blur 10 % (mediana [IQR])", f"{mq(x['sigma4_sobre_diametro'], '{:.3f}')} / {mq(x['sigma10_sobre_diametro'], '{:.3f}')}", "rodada13")
    line(f"{nm}: fracao dos pares com sigma < metade do diametro, blur 4 % / blur 10 % (%)", f"{100 * x['fracao_sigma4_menor_meio_diametro']:.1f} / {100 * x['fracao_sigma10_menor_meio_diametro']:.1f}", "rodada13")
NM13 = {"dependent_polyp": "polipo", "dependent_instrument": "instrumento", "negative_control": "controle negativo (3 templates)", "closed_yes": "fechada-sim", "closed_no": "fechada-nao"}
for k, x in R13["item3"].items():
    b, c, kind = k.split("|")
    line(f"{NAME[b]}, {NM13[c]}, {'afinados' if kind == 'afinados' else 'zero-shot (4 modelos)'}: declarados (regra final) que tambem tem queda bruta sob blur 10 % (IC > 0) / declarados", f"{x['tambem_queda_bruta_blur10']} / {x['declarados']}", "rodada13")
    for y in x["sem_queda_bruta_blur10"]:
        line(f"{NAME[b]}, {NM13[c]}, {y['linha']}: declarado sem queda bruta sob blur 10 %: Acc(C0) - Acc(T blur 10 %) [IC] (pp)", f"{pp(y['queda_bruta_blur10'])} {cpp(y['ic'])}", "rodada13")
# ---------------- round 14: final declaration with the raw drop under both fills
R14 = J("rodada14"); SRC["rodada14"] = ("v7_artigo1/analysis/rodada14.json", sha(f"{A}/rodada14.json")[:12])
L += ["", "## S18. Declaracao final com queda bruta sob preto e sob blur 10 % (rodada 14)", ""]
line("declaracao final (regra, decisao A do Claudio, 22/10/2026)", R14["regra"] + "; recalculada a partir das predicoes (mesmas replicas); IC 95 % por imagem", ("rodada14", "generator"))
cf = R14["conferencia_necessity_v2"]; line("recalculo a partir das predicoes: intervalos iguais aos de analysis/necessity_v2 / diferentes", f"{cf.get('igual', 0)} / {cf.get('diferente', 0)}", "rodada14")
NM14 = {"dependent_polyp": "polipo", "dependent_instrument": "instrumento", "negative_control": "controle negativo (3 templates)", "closed_yes": "fechada-sim", "closed_no": "fechada-nao"}
for k, x in R14["contagens"].items():
    b, c, kind = k.split("|"); nm = f"{NAME[b]}, {NM14[c]}, {'afinados' if kind == 'afinados' else 'zero-shot (4 modelos)'}"
    line(f"{nm}: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / linhas", f"{x['declarados_regra_final']} / {x['linhas']}", "rodada14")
    line(f"{nm}: declarados pela regra final com Holm, familia da Tabela 1 / linhas", f"{x['declarados_holm_tabela1']} / {x['linhas']}", "rodada14")
    line(f"{nm}: declarados pela regra da rodada 11 (queda bruta so sob preto) que tambem tem queda bruta sob blur 10 % / declarados pela regra da rodada 11", f"{x['declarados_regra_final']} / {x['declarados_rodada11']}", "rodada14")
    for y in x["perdidos_pela_queda_sob_blur"]:
        line(f"{nm}, {y['linha']}: sai da declaracao pela queda bruta sob blur 10 %: Acc(C0) - Acc(T blur 10 %) [IC] (pp)", f"{pp(y['queda_bruta_blur10'])} {cpp(y['ic'])}", "rodada14")
for k, gg in R14["por_grupo"].items():
    b, c = k.split("|")
    for g, y in gg.items():
        line(f"{NAME[b]}, {NM14[c]}, {g}: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas", f"{y['declarados_regra_final']} / {y['resoluveis']} / {y['runs']}", "rodada14")
for e, x in R14["entidades_mimic"].items():
    line(f"Medical-Diff-VQA, fechada-sim, entidade {e} ({x['perguntas']} perguntas): ganho significativo / declarados pela regra final / runs", f"{x['ganho_significativo']} / {x['declarados_regra_final']} / {x['runs']}", "rodada14")
for k, x in R14["max_delta"].items():
    b, c = k.split("|")
    if x["declarados"]: line(f"{NAME[b]}, {NM14[c]}: Delta preto maximo entre os {x['declarados']} declarados pela regra final / maximo entre os {NL[b]} (pp)", f"{pp(x['max_delta_preto_declarados'])} / {pp(x['max_delta_preto_27'])}", "rodada14")
# ---------------- round 15: final rule with blur 4 %
R15 = J("rodada15"); SRC["rodada15"] = ("v7_artigo1/analysis/rodada15.json", sha(f"{A}/rodada15.json")[:12])
L += ["", "## S19. Regra final com blur 4 % (rodada 15)", ""]
line("regra final com blur 4 % (regra)", R15["regra"] + "; mesmas replicas; HEAL-MedVQA sem QWEN2VL_DORA_HEAL_seed2 (adapter do retreino); zero-shot sem predicoes sob blur 4 %", ("rodada15", "generator"))
NM15 = {"dependent_polyp": "polipo", "dependent_instrument": "instrumento", "negative_control": "controle negativo (3 templates)", "closed_yes": "fechada-sim", "closed_no": "fechada-nao"}
for k, x in R15["contagens"].items():
    b, c, kind = k.split("|"); nm = f"{NAME[b]}, {NM15[c]}"
    line(f"{nm}: declarados pela regra final com blur 4 % / declarados com blur 4 % e queda bruta so sob preto (S14) / runs", f"{x['declarados_final_blur4']} / {x['declarados_s14']} / {x['runs']}", "rodada15")
    for y in x["saem_so_pela_queda_bruta_blur4"]:
        line(f"{nm}, {y['linha']}: sai da regra final com blur 4 % so pela queda bruta sob blur 4 %: Acc(C0) - Acc(T blur 4 %) [IC] (pp)", f"{pp(y['queda_bruta_blur4'])} {cpp(y['ic'])}", "rodada15")
line("regra final com blur 4 %, zero-shot", f"sem predicoes sob blur 4 % para os {len(R15['zero_shot_sem_predicoes'])} pares modelo x base (nada a contar)", "rodada15")
# ---------------- round 16: Holm as an intersection-union test (IUT)
R16 = J("rodada16"); SRC["rodada16"] = ("v7_artigo1/analysis/rodada16.json", sha(f"{A}/rodada16.json")[:12])
L += ["", "## S20. Holm como teste de intersecao-uniao (rodada 16)", ""]
line("procedimento das rodadas 8, 9 e 14 (Holm por condicao)", "para cada run e cada condicao separadamente, os p unilaterais bootstrap das classes da familia foram ajustados por Holm; o run foi declarado se todas as condicoes passaram com p ajustado < 0,025 (Holm por condicao, depois a conjuncao); nao era IUT", ("generator", "rodada16"))
line("IUT (regra)", R16["regra"], "rodada16")
NM16 = {"dependent_polyp": "polipo", "dependent_instrument": "instrumento", "negative_control": "controle negativo (3 templates)", "closed_yes": "fechada-sim", "closed_no": "fechada-nao"}
for k, x in R16["contagens"].items():
    b, c, kind = k.split("|")
    line(f"{NAME[b]}, {NM16[c]}, {'afinados' if kind == 'afinados' else 'zero-shot (4 modelos)'}: declarados pela regra final com IUT e Holm / com Holm por condicao (rodada 14) / sem Holm / runs", f"{x['iut_holm']} / {x['holm_por_condicao_r14']} / {x['sem_holm_IC']} / {x['runs']}", "rodada16")
line("runs cuja declaracao muda entre IUT com Holm e Holm por condicao", str(len(R16["runs_que_mudam_vs_holm_por_condicao"])), "rodada16")
line("alteracao de pixels dentro do alvo (definicao, rodada 13)", "por par imagem-alvo, media, sobre os pixels da mascara-alvo, da diferenca absoluta entre a imagem intacta e a preenchida, na escala 0-255, com a media dos tres canais; mediana [IQR] entre os pares; mascara = uniao dos pixels alterados pelo preto, pelo blur 10 % ou pelo blur 4 %", ("generator", "rodada13"))
# ---------------- round 17: no-image baseline trained with DoRA (record only; nothing changes in the paper)
R17 = J("rodada17"); SRC["rodada17"] = ("v7_artigo1/analysis/rodada17.json", sha(f"{A}/rodada17.json")[:12])
L += ["", "## S21. Baseline sem imagem com DoRA (rodada 17; base do baseline pareado, ver S22)", ""]
line("baseline sem imagem DoRA (regra)", "mesma receita do baseline sem imagem LoRA (adaptador so no modelo de linguagem, rank 16, alfa 32, projecoes de atencao, lr 2e-4, 3 epocas, batch 4 x 4, mesmo split, mesma entrada sem imagem, mesmos scripts), trocando so LoRA por DoRA; " + R17["regra"], "rodada17")
NM17 = {"dependent_polyp": "polipo", "dependent_instrument": "instrumento", "negative_control": "controle negativo (3 templates)", "closed_yes": "fechada-sim", "closed_no": "fechada-nao"}
FAM17 = {"QWEN2VL": "Qwen2-VL-2B", "SMOLVLM": "SmolVLM2-2.2B"}
for k, x in R17["acc_txt_por_familia"].items():
    b, c, f = k.split("|")
    line(f"{NAME[b]}, {NM17[c]}, {FAM17[f]}: acuracia do baseline sem imagem LoRA / DoRA, media (minimo – maximo) entre sementes (%)", f"{pct(x['lora']['media'])} ({pct(x['lora']['min'])} – {pct(x['lora']['max'])}) / {pct(x['dora']['media'])} ({pct(x['dora']['min'])} – {pct(x['dora']['max'])})", "rodada17")
for k, x in R17["comparacao_G"].items():
    b, c = k.split("|"); y = x["G_menos_G_dora"]
    line(f"{NAME[b]}, {NM17[c]}: G atual - G_DoRA nos {x['runs_dora']} runs DoRA, media / minimo / maximo (pp)", f"{pp(y['media'])} / {pp(y['min'])} / {pp(y['max'])}", "rodada17")
for k, x in R17["contagens"].items():
    b, c = k.split("|")
    line(f"{NAME[b]}, {NM17[c]}: criterio (iv) dois preenchimentos com ganho significativo, atual / com G_DoRA nos runs DoRA (linhas)", f"{x['iv_atual']} / {x['iv_com_G_dora']} de {x['linhas']}", "rodada17")
    line(f"{NAME[b]}, {NM17[c]}: criterio (v) declarado pela regra final, atual / com G_DoRA nos runs DoRA (linhas)", f"{x['v_atual']} / {x['v_com_G_dora']} de {x['linhas']}", "rodada17")
line("runs DoRA cujo estado nos criterios (iv) ou (v) muda com G_DoRA", str(len(R17["runs_que_mudam"])), "rodada17")
for m in R17["runs_que_mudam"]:
    line(f"{NAME[m['base']]}, {NM17[m['classe']]}, {m['linha']}: G [IC] / G_DoRA [IC] (pp); (iv) e (v) atual -> com G_DoRA", f"{pp(m['G'])} {cpp(m['G_ci'])} / {pp(m['G_dora'])} {cpp(m['G_dora_ci'])}; {'sim' if m['iv'] else 'nao'} -> {'sim' if m['iv_dora'] else 'nao'}, {'sim' if m['v'] else 'nao'} -> {'sim' if m['v_dora'] else 'nao'}", "rodada17")
# ---------------- round 19: image gain with the baseline of the same adapter type (authors' decision)
R19 = J("rodada19"); SRC["rodada19"] = ("v7_artigo1/analysis/rodada19.json", sha(f"{A}/rodada19.json")[:12])
L += ["", "## S22. Ganho de imagem com baseline sem imagem do mesmo adaptador (rodada 19)", ""]
line("ganho de imagem pareado (regra, decisao do Claudio de 22/10/2026)", R19["regra"] + "; oclusoes, C, Delta_nec, replicas e normalizacao inalterados", ("rodada19", "generator"))
NM19 = {"dependent_polyp": "polipo", "dependent_instrument": "instrumento", "negative_control": "controle negativo (3 templates)", "closed_yes": "fechada-sim", "closed_no": "fechada-nao"}
for k, x in R19["tabela1"].items():
    b, c = k.split("|"); y = x["pareado"]
    line(f"{NAME[b]}, {NM19[c]}: criterios (i) / (ii) / (iii) / (iv) / (v), ganho pareado (linhas de {NL[b]})", f"{y['i']} / {y['ii']} / {y['iii']} / {y['iv']} / {y['v']}", "rodada19")
    t = R19["texto_ganho"][k]["pareado"]
    line(f"{NAME[b]}, {NM19[c]}: ganho de imagem pareado, minimo – maximo entre as {NL[b]} linhas (pp); linhas com ganho significativo", f"{pp(t['min'])} – {pp(t['max'])}; {t['significativos']}/{NL[b]}", "rodada19")
    line(f"{NAME[b]}, {NM19[c]}: declarados pela regra final com IUT e Holm, ganho pareado (linhas de {NL[b]})", f"{R19['holm_iut_v'][k]['pareado']}", "rodada19")
for k, gg in R19["tabela2"].items():
    b, c = k.split("|")
    for g, y in gg.items():
        line(f"{NAME[b]}, {NM19[c]}, {g}: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)", f"{pp(y['G']['media'])} ({100 * y['G']['dp']:.1f}); {y['declared']}", "rodada19")
for k, x in R19["blur4_v"].items():
    b, c = k.split("|")
    line(f"{NAME[b]}, {NM19[c]}: regra final com blur 4 % e ganho pareado: declarados / runs", f"{x['pareado']} / {x['runs']}", "rodada19")
cs = R19["cascata_mimic_yes"]["pareado"]
line("Medical-Diff-VQA, fechada-sim, ganho pareado: linhas em (ii) / (iii) / (iv) / (v)", f"{cs['ii']} / {cs['iii']} / {cs['iv']} / {cs['v']}", "rodada19")
line("Medical-Diff-VQA, fechada-sim, ganho pareado: tirados pelo criterio de dois preenchimentos / pela condicao do ganho / pela queda bruta", f"{cs['ii'] - cs['iii']} / {cs['iii'] - cs['iv']} / {cs['iv'] - cs['v']}", "rodada19")
# ---------------- round 20: no-image baseline of M3AE = M3AE without image (variant without an image path)
TCL20 = {"KVASIR": ["dependent_polyp", "dependent_instrument", "negative_control"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no"]}
R20 = J("rodada20"); SRC["rodada20"] = ("v7_artigo1/analysis/rodada20.json", sha(f"{A}/rodada20.json")[:12])
L += ["", "## S23. Baseline sem imagem do M3AE: M3AE sem imagem (rodada 20)", ""]
line("ganho de imagem (regra, decisao do Claudio de 23/10/2026)", R20["regra"] + "; oclusoes, C, Delta_nec, replicas e normalizacao inalterados", ("rodada20", "generator"))
for k, x in R20["fonte"]["predicoes_sem_imagem"].items():
    line(f"predicoes do M3AE sem imagem, {k}: sha256", x["sha256"][:16], "rodada20")
for k, v in R20["m3ae"].items():
    b, ln = k.split("|")
    for c in TCL20[b]:
        x = v[c]; line(f"{NAME[b]}, {NM19[c]}, {ln}: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo", f"{pp(x['G'])} [{pp(x['G_ci'][0])}, {pp(x['G_ci'][1])}], p = {x['p_G']:.4f}; {'sim' if x['sig'] else 'nao'}", "rodada20")
for k, x in R20["acuracia_sem_imagem_vs_cinza"].items():
    b, ln = k.split("|")
    line(f"{NAME[b]}, {ln}: acuracia sem imagem / cinza / diferenca nos itens do artigo 1 (%, pp; n itens)", f"{100 * x['acc_sem_imagem']:.2f} / {100 * x['acc_cinza']:.2f} / {pp(x['dif'])} ({x['n_itens']})", "rodada20")
for k, x in R20["tabela1"].items():
    b, c = k.split("|"); y = x["novo"]
    line(f"{NAME[b]}, {NM19[c]}: criterios (i) / (ii) / (iii) / (iv) / (v), M3AE sem imagem (linhas de {NL[b]}); linhas com ganho significativo", f"{y['i']} / {y['ii']} / {y['iii']} / {y['iv']} / {y['v']}; {y['ganho']}/{NL[b]}", "rodada20")
    t = R20["texto_ganho"][k]["novo"]
    line(f"{NAME[b]}, {NM19[c]}: ganho de imagem, minimo – maximo entre as {NL[b]} linhas (pp), M3AE sem imagem", f"{pp(t['min'])} – {pp(t['max'])}", "rodada20")
    line(f"{NAME[b]}, {NM19[c]}: declarados pela regra final com IUT e Holm, M3AE sem imagem (linhas de {NL[b]})", f"{R20['holm_iut_v'][k]['novo']}", "rodada20")
for k, gg in R20["tabela2"].items():
    b, c = k.split("|")
    for g, y in gg.items():
        line(f"{NAME[b]}, {NM19[c]}, {g}: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem", f"{pp(y['G']['media'])} ({100 * y['G']['dp']:.1f}); {y['declared']}", "rodada20")
for k, x in R20["blur4_v"].items():
    b, c = k.split("|")
    line(f"{NAME[b]}, {NM19[c]}: regra final com blur 4 %, M3AE sem imagem: declarados / runs", f"{x['novo']} / {x['runs']}", "rodada20")
cs = R20["cascata_mimic_yes"]["novo"]
line("Medical-Diff-VQA, fechada-sim, M3AE sem imagem: linhas em (ii) / (iii) / (iv) / (v)", f"{cs['ii']} / {cs['iii']} / {cs['iv']} / {cs['v']}", "rodada20")
# ---------------- S11 suplemento interno

# round 24 (02/11/2026): S24 -- criteria (i)-(v) per question subset, fine-tuned runs (rule of the paper: paired G of round 19, no-image M3AE of
# round 20, the other tests of round 14) and zero-shot models (round 14; G = with image minus without image of the same model); (v) also with the IUT and
# Holm within the run over the subsets of the benchmark (family of r19). Single source of Table 1 with two blocks. With the family disabled it reproduces the counts of 27.
L += ["", f"## S24. Criterios (i)-(v) por subconjunto com o 7B ({N27} linhas afinadas por base) e zero-shot (rodada 24)", ""]
SRC["rodada19"] = ("v7_artigo1/analysis/rodada19.json", sha(f"{A}/rodada19.json")[:12]); SRC["rodada20"] = ("v7_artigo1/analysis/rodada20.json", sha(f"{A}/rodada20.json")[:12])
_T24 = {"KVASIR": ["dependent_polyp", "dependent_instrument", "negative_control"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no"]}
_lo24 = lambda c: c[0] if c else None
def _crit24(b, Ln, c):
    src = R20 if Ln["fam"] == "M3AE" else R19; x = src["por_linha"][f"{b}|{Ln['line']}"]["classes"].get(c); y = R14["por_linha"][f"{b}|{Ln['line']}"]["classes"].get(c)
    if not x or not y: return None
    g = (_lo24(x["G_ci"]) or 0) > 0; i = x["L0p"]; ii = x["L1"]; iii = ii and x["L2b"]; iv = iii and g; v = iv and x["L0p"] and x["L0b"]
    p = dict(y["p"]); p["ganho"] = x["p_G"]; return {"i": i, "ii": ii, "iii": iii, "iv": iv, "v": v, "ganho": g, "p_iut": max(p.values())}
def _holm24(ps):   # Holm within the run: ps = {class: p}; declared if the adjusted p < 0.025
    o = sorted(ps.items(), key=lambda kv: kv[1]); m = len(o); run = 0; out = {}
    for k, (c, p) in enumerate(o): run = max(run, p * (m - k)); out[c] = min(1.0, run) < 0.025
    return out
def _zs24(b, c):   # zero-shot models of round 14; on Kvasir LLaVA-Med is left out (same reason as in Table 3)
    out = {k: 0 for k in ("i", "ii", "iii", "iv", "v", "ganho")}; n = 0
    for k, r in R14["por_linha"].items():
        if not r.get("zero_shot") or not k.startswith(b + "|") or c not in r["classes"]: continue
        if b == "KVASIR" and "LLAVA_MED" in k: continue
        t = r["classes"][c]["testes_ic"]; n += 1; i = t["L0_preto"]; ii = t["L1_preto"]; iii = ii and t["L2_blur10"]; iv = iii and t["ganho"]; v = r["classes"][c]["declarado_regra_final"]
        for kk, vv in (("i", i), ("ii", ii), ("iii", iii), ("iv", iv), ("v", v), ("ganho", t["ganho"])): out[kk] += int(vv)
    return out, n
for b in BASES:
    rows = {c: {k: 0 for k in ("i", "ii", "iii", "iv", "v", "v_holm", "ganho")} for c in _T24[b]}; nlin = 0
    for Ln in lines(b):
        cr = {c: _crit24(b, Ln, c) for c in _T24[b]}; cr = {c: x for c, x in cr.items() if x}
        if not cr: continue
        nlin += 1; hv = _holm24({c: x["p_iut"] for c, x in cr.items()})
        for c, x in cr.items():
            for k in ("i", "ii", "iii", "iv", "v", "ganho"): rows[c][k] += int(x[k])
            rows[c]["v_holm"] += int(hv[c])
    for c in _T24[b]:
        r = rows[c]; nm = f"{NAME[b]}, {NM14[c]}"
        line(f"Tabela 1, {nm}, afinados: (i) / (ii) / (iii) / (iv) / (v) (de {nlin} linhas; G pareado)", f"{r['i']} / {r['ii']} / {r['iii']} / {r['iv']} / {r['v']}", ("rodada19", "rodada20", "rodada14"))
        line(f"Tabela 1, {nm}, afinados: (v) com IUT e Holm dentro da linha / linhas com ganho significativo (de {nlin})", f"{r['v_holm']} / {r['ganho']}", ("rodada19", "rodada20", "rodada14"))
        z, nz = _zs24(b, c); line(f"Tabela 1, {nm}, zero-shot ({nz} modelos{', sem LLaVA-Med' if b == 'KVASIR' else ''}): (i) / (ii) / (iii) / (iv) / (v); com ganho significativo", f"{z['i']} / {z['ii']} / {z['iii']} / {z['iv']} / {z['v']}; {z['ganho']}", "rodada14")
# round 24b (03/11/2026): S25 -- lines cited by the text that the sheet did not have: blur 4 % on the 7B runs (Kvasir, polyp; round 15), the five
# quantities of the HEAL yes-run that meets (iv) but not (v) (necessity_v2; rule of _crit24), the range of the intact accuracy on HEAL yes-questions and
# the Medical-Diff-VQA yes-runs removed by the drop condition, with the sign of C (necessity_v2). With the family disabled the 7B lines and the HEAL run are not written.
L += ["", "## S25. Linhas citadas pelo texto da v32 (rodada 24b)", ""]
_pp2 = lambda x: "—" if x is None else f"{100 * x:+.2f}"; _ci2 = lambda c: "—" if not c else f"[{100 * c[0]:+.2f}, {100 * c[1]:+.2f}]"
def _nv25(b, Ln):
    f = f"{A}/necessity_v2/{Ln['line']}_{b}.json"; SRC[f"necessity_v2/{Ln['line']}_{b}"] = (f"v7_artigo1/analysis/necessity_v2/{Ln['line']}_{b}.json", sha(f)[:12]); return json.load(open(f))
_f25 = [Ln for Ln in lines("KVASIR") if Ln["fam"] == "QWEN25VL"]
if _f25:
    _t = [R15["por_linha"][f"KVASIR|{Ln['line']}"]["classes"]["dependent_polyp"] for Ln in _f25]
    line(f"Kvasir-VQA-x1, polipo, Qwen2.5-VL-7B ({len(_f25)} linhas): Delta blur 4 % significativo / queda blur 4 % significativa / declarados (v) blur 4 %", f"{sum(int(x['testes']['delta_blur4']) for x in _t)} / {sum(int(x['testes']['L0_blur4']) for x in _t)} / {sum(int(x['declarado_final_blur4']) for x in _t)}", "rodada15")
for Ln in lines("HEAL"):
    x = _crit24("HEAL", Ln, "closed_yes")
    if x and x["iv"] and not x["v"]:
        c = _nv25("HEAL", Ln)["by_class"]["closed_yes"]
        line(f"HEAL-MedVQA, fechada-sim, {Ln['line']}: queda alvo preto [IC] / queda alvo blur 10 % [IC] / custo mascara deslocada preto [IC] / Delta preto [IC] / Delta blur 10 % [IC] (pp)", " / ".join(f"{_pp2(c[k])} {_ci2(c[k + '_ci_by_image'])}" for k in ("custo_alvo_preto", "custo_alvo_blur10", "custo_mascara_deslocada_preto", "delta_preto", "delta_blur10")), (f"necessity_v2/{Ln['line']}_HEAL", "rodada19", "rodada20", "rodada14"))
_acc = {Ln["line"]: _nv25("HEAL", Ln)["by_class"]["closed_yes"]["acc"]["C0"] for Ln in lines("HEAL")}
SRC["necessity_v2_HEAL"] = (f"v7_artigo1/analysis/necessity_v2/*_HEAL.json ({len(_acc)} linhas)", hashlib.sha256("".join(sha(f"{A}/necessity_v2/{k}_HEAL.json") for k in sorted(_acc)).encode()).hexdigest()[:12])
line(f"HEAL-MedVQA, fechada-sim: acurácia intacta, minimo – maximo entre as {NL['HEAL']} linhas (%)", f"{100 * min(_acc.values()):.1f} – {100 * max(_acc.values()):.1f}", "necessity_v2_HEAL")
_rem = []
for Ln in lines("MIMIC"):
    x = _crit24("MIMIC", Ln, "closed_yes")
    if x and x["iv"] and not x["v"]:
        c = _nv25("MIMIC", Ln)["by_class"]["closed_yes"]; _rem.append((Ln["line"], c["custo_mascara_deslocada_preto"], c["custo_alvo_preto"], c["custo_alvo_preto_ci_by_image"], c["custo_alvo_blur10"], c["custo_alvo_blur10_ci_by_image"]))
_cs25 = R20["cascata_mimic_yes"]["novo"]; assert len(_rem) == _cs25["iv"] - _cs25["v"], (len(_rem), _cs25)
line("Medical-Diff-VQA, fechada-sim, ganho pareado: removidos pela condicao de queda com C < 0 / total removidos pela queda", f"{sum(1 for r in _rem if r[1] < 0)} / {len(_rem)}", ("rodada19", "rodada20", "rodada14") + tuple(f"necessity_v2/{r[0]}_MIMIC" for r in _rem))
line("Medical-Diff-VQA, fechada-sim, ganho pareado: runs removidos pela condicao de queda (C preto; queda preto [IC]; queda blur 10 % [IC]) (pp)", "; ".join(f"{r[0]} (C {_pp2(r[1])}; {_pp2(r[2])} {_ci2(r[3])}; {_pp2(r[4])} {_ci2(r[5])})" for r in _rem), ("rodada19", "rodada20", "rodada14") + tuple(f"necessity_v2/{r[0]}_MIMIC" for r in _rem))
L += ["", "## S11. Suplemento interno (nao vai ao corpo)", ""]
for b in BASES:
    for cls, nm in CLS[b]:
        v = crit["bases"][b]["por_classe"].get(cls)
        if v: line(f"criterio A / C (so interno) e criterio antigo (IC por pergunta), {NAME[b]}, {nm}", f"A {v['total']['A']}/{v['n_linhas']} / C {v['total']['C']}/{v['n_linhas']} / antigo {v['antigo_e3_ic_por_pergunta'] if v['antigo_e3_ic_por_pergunta'] is not None else '—'}", "criterio")
NI = f"{PREV_SHEETS}/numbers_isbi.md"
for b in BASES:
    for ln, v in ds["bases"][b].get("valores_excluidos", {}).items():
        for cls, x in (v.get("by_class") or {}).items():
            nv = x["niveis"]; line(f"doses, {NAME[b]}, {ln} (fora das medias), {dict(CLS[b]).get(cls, cls)}: Delta 1x / 1,5x / 2x [IC] (pp)", " / ".join(f"{pp(nv[k].get('delta_preto'))} {cpp(nv[k].get('delta_preto_ci_by_image'))}" for k in ("1", "1.5", "2")), "doses")
line("SLAKE (fora do artigo): criterio antigo nas fechadas (E8), doenca / orgao", "0/16 / 0/16 (folha antiga; nao recomputado nesta rodada)", ("generator", NI))
line("Delta normalizado (so suplemento)", "existe em v7_txt/docs/numbers_own_floor.md e v7_mimic/docs/numbers_placebo_mimic.md; nao reproduzido aqui", ("generator", f"{PREV_SHEETS}/numbers_own_floor.md"))
open(f"{OUT}/docs/numbers_artigo1.md", "w").write("\n".join(L) + "\n")
# manifest
man = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "folha": f"{OUT}/docs/numbers_artigo1.md", "folha_sha256": sha(f"{OUT}/docs/numbers_artigo1.md"), "n_linhas_folha": sum(1 for x in L if x.startswith("- **")),
       "scripts": {os.path.basename(p): sha(p) for p in sorted(glob.glob(f"{SCRIPTS}/*.py"))}, "analysis": {os.path.relpath(p, OUT): sha(p) for p in sorted(glob.glob(f"{A}/*.json")) + sorted(glob.glob(f"{A}/necessity_v2/*.json"))},
       "entradas_externas": {"heal_annotations_test.parquet": sha(f"{LAB_INPUTS}/heal_annotations_test.parquet")}}
json.dump(man, open(f"{OUT}/manifests/manifest_rodada1.json", "w"), indent=1); print("folha:", man["n_linhas_folha"], "numeros; sha", man["folha_sha256"][:16])
