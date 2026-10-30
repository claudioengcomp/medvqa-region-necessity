"""Item 9 (CPU): method facts for the numbers sheet, each with its source file and sha256. Outputs: analysis/fatos_metodo.json, docs/item9_fatos_metodo.md."""
import collections, glob, json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
F = []
def add(rotulo, valor, fonte, extra=None): F.append({"rotulo": rotulo, "valor": valor, "fonte": fonte, "sha256": sha(fonte.split(" [")[0]) if os.path.exists(fonte.split(" [")[0]) else None, **({"nota": extra} if extra else {})})
kv = json.load(open(INV["KVASIR"])); s = kv["summary"]
add("Kvasir: ordem do posicionamento da mascara deslocada", "hflip, vflip, rot180, ate 50 translacoes aleatorias (semente 20260913); margem (dilatacao do alvo) 5 px; >= 80 % no campo de visao; area maxima 40 % do campo de visao", f"{CODE_ROOT}/harness/isbi_placebo/masks.py", "place_placebo(margin_px=5, min_fov_frac=0.8); place_placebos_by_factor(max_area_frac=0.4)")
add("Kvasir: metodo por unidade (imagem x alvo)", s["images"]["placebo_methods"], INV["KVASIR"])
add("Kvasir: imagens de teste / com mascara / unidades", f"{s['n_images']} / {units if False else ''}", INV["KVASIR"]) if False else None
mp = json.load(open(f"{KV_META}/kvasir_vqa_to_seg_instrument_map.json"))
add("Kvasir: mascaras casadas (Kvasir-SEG polipos / Kvasir-Instrument instrumentos)", f"{len(mp['polyps'])} / {len(mp['instrument'])} (instrumentos sem par: {len(mp['instrument_unmatched'])})", f"{KV_META}/kvasir_vqa_to_seg_instrument_map.json")
add("Kvasir: imagens de teste com mascara / total; unidades; excluidas (sem posicao / area > max)", f"{s['images']['with_target'] + s['images']['excluded']['no_valid_placement'] + s['images']['excluded']['area_gt_max']}/{s['n_images']}; {s['images']['with_target']}; {s['images']['excluded']['no_valid_placement']} / {s['images']['excluded']['area_gt_max']}", INV["KVASIR"])
he = json.load(open(INV["HEAL"]))["summary"]; hm = json.load(open(f"{ISBI}/manifest_heal.json"))
add("HEAL: regra da mascara deslocada", "outra anatomia da mesma imagem com razao de area 0,7-1,4 e sobreposicao <= 5 % do alvo; senao espelho horizontal; senao posicionador do Kvasir com >= 80 % dentro do atlas toracico (pixels anotados em >= 2 % das mascaras)", f"{CODE_ROOT}/harness/isbi_placebo/heal/inventory_heal.py", "AREA_RATIO = (0.7, 1.4); MAX_OVERLAP = 0.05; thorax_atlas MIN_FREQ = 0.02")
add("HEAL: metodo por unidade (1 360)", dict(collections.Counter(u["placebo_method"].split(":")[0] for u in hm["units"])), f"{ISBI}/manifest_heal.json")
add("HEAL: fechadas sem posicao valida", he["n_closed_without_placement"], INV["HEAL"])
mi = json.load(open(INV["MIMIC"])); ms_ = mi["summary"]
add("MIMIC: regra da regiao-alvo", "uniao das caixas do Chest ImaGenome das regioes-folha (mais finas) com o atributo mapeado; regiao-mae descartada quando uma descendente tem o atributo", f"{V7M}/scripts/16_inventory_mimic.py")
add("MIMIC: regra da mascara deslocada (v2, alvos com > 1 caixa)", "por caixa: anatomia homologa sem o atributo (razao 0,8-1,25) -> translacao vertical com area exata (pares bilaterais juntos) -> espelho horizontal -> anatomia ampliada (razao 0,5-2,0); >= 80 % no atlas, inteira no filme, sem tocar o alvo dilatado em 5 px, caixas sem sobreposicao entre si; alvos de 1 caixa: regra do HEAL", f"{V7M}/scripts/16_inventory_mimic.py")
add("MIMIC: metodos por caixa (avaliaveis)", ms_.get("placebo_methods_per_box"), INV["MIMIC"])
add("MIMIC: metodos por unidade (avaliaveis)", ms_.get("placebo_methods"), INV["MIMIC"])
add("MIMIC: avaliaveis / total (inventario v2)", f"{ms_['n_evaluable']}/{ms_['n_questions']}", INV["MIMIC"], "o prompt cita 2 152/3 000, que e o inventario v1 (11/10); as predicoes existentes usam o v2")
add("MIMIC: teto de area do alvo", "40 % do quadro inteiro", INV["MIMIC"])
add("blur 10 %", "filtro gaussiano com sigma = 10 % da largura da imagem, aplicado so na regiao", f"{CODE_ROOT}/harness/isbi_placebo/conditions.py", "fill_region: sigma = float(fill[4:]) / 100.0 * img.shape[1]")
add("cor media da regiao", "media RGB dos pixels da propria regiao (remove a forma, mantem a cor local)", f"{CODE_ROOT}/harness/isbi_placebo/conditions.py", "fill_region('regmean')")
add("codificacao das condicoes", "C0 = bytes originais do arrow (HEAL/MIMIC: PNG lado maior 1024); demais = PNG sem perda a partir dos pixels decodificados", f"{CODE_ROOT}/harness/isbi_placebo/conditions.py", "encode_png")
jp = f"{ISBI}/necessity_QWEN2VL_LORA_KVASIR_seed0_jpeg_pilot.json"
if os.path.exists(jp):
    d = json.load(open(jp)); r = d.get("c0_reference") or {}
    add("reencode JPEG (piloto Qwen2-VL LoRA s0, Kvasir): predicoes da intacta que mudam", f"{r.get('n_disagree_pred')} de {r.get('n_common')} = {100 * r.get('disagree_pred_rate', 0):.2f} %", jp)
    add("reencode JPEG: delta de acuracia da intacta", f"{r.get('delta_pp'):+.2f} pp", jp)
add("composicao de lote (0,6-0,7 %)", "sem fonte localizada na gpu1", f"{PLC}/docs/isbi/placebo/preregistration_v2.md", "o pre-registro (E1) registra 0 predicoes diferentes na intacta reproduzida em bytes originais ('a inferencia independe da composicao dos lotes')")
# recipes and trainable parameters (Kvasir seed 0 as the reference of each configuration)
rec = {}
for cfg, p in (("Qwen2-VL LoRA, encoder congelado", f"{P0}/outputs/qwen2vl_lora_kvasir_seed0.json"), ("Qwen2-VL DoRA, encoder congelado", f"{P0}/outputs/qwen2vl_dora_kvasir_seed0.json"),
               ("SmolVLM2 LoRA, encoder afinado", f"{P0}/outputs/smolvlm2_lora_kvasir_seed0.json"), ("SmolVLM2 DoRA, encoder afinado", f"{P0}/outputs/smolvlm2_dora_kvasir_seed0.json"),
               ("Qwen2-VL LoRA, encoder afinado", f"{V5Q}/qwen2vl_lora_vt_kvasir_seed0.json"), ("Qwen2-VL DoRA, encoder afinado", f"{V5Q}/qwen2vl_dora_vt_kvasir_seed0.json"),
               ("SmolVLM2 LoRA, encoder congelado", f"{V5S}/smolvlm2_lora_ft_kvasir_seed0.json"), ("SmolVLM2 DoRA, encoder congelado", f"{V5S}/smolvlm2_dora_ft_kvasir_seed0.json")):
    if not os.path.exists(p): add(f"receita: {cfg}", "registro de treino ausente", p); continue
    d = json.load(open(p)); tr = d.get("train", {}); pa = (d.get("efficiency") or {}).get("params") or {}
    add(f"receita: {cfg} (Kvasir semente 0)", f"lr {tr.get('lr')}; epocas {tr.get('epochs')}; grad_accum {tr.get('grad_accum_steps')}; parametros treinaveis {pa.get('trainable_params')} de {pa.get('total_params')} ({pa.get('trainable_ratio')})", p)
yml = "configs/training/heal/qwen2vl_lora_heal.yaml"
if os.path.exists(yml):
    t = open(yml).read(); g = lambda k: (re.search(rf"^\s*{k}:\s*(.+)$", t, re.M) or [None, None])[1]
    add("receita LoRA/DoRA (YAML do HEAL)", f"r {g('r')}; lora_alpha {g('lora_alpha')}; target_modules {g('target_modules')}; lr {g('lr')}; epocas {g('epochs')}; batch {g('batch_size')} x grad_accum {g('grad_accum_steps')}", yml)
add("text-decoder-only", "mesma receita de ajuste, sem imagem; LoRA so no modelo de linguagem (Qwen2-VL e SmolVLM2: LoRA em todas as celulas, inclusive para as linhas DoRA); M3AE: treinado com imagem cinza constante (384x384, RGB 128) no treino, validacao e teste", f"{V7T}/README.md")
add("classificador so-pergunta (TF-IDF)", "TF-IDF de palavras 1-2-gramas + regressao logistica (C = 1), sem imagem; Kvasir por item publicado; HEAL alinhado aos 1 446 qids; MIMIC M0 subset nas fechadas", f"{CODE_ROOT}/harness/isbi_placebo/heal/m0_heal.py")
out = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "fatos": F}; json.dump(out, open(f"{OUT}/analysis/fatos_metodo.json", "w"), indent=1, ensure_ascii=False)
L = ["# Item 9 — fatos de método (com fonte)", "", "| fato | valor | fonte | sha256 | nota |", "|---|---|---|---|---|"]
L += [f"| {x['rotulo']} | {json.dumps(x['valor'], ensure_ascii=False) if not isinstance(x['valor'], str) else x['valor']} | `{x['fonte']}` | `{(x['sha256'] or '—')[:12]}` | {x.get('nota', '')} |" for x in F]
open(f"{OUT}/docs/item9_fatos_metodo.md", "w").write("\n".join(L) + "\n"); print(len(F), "fatos")
