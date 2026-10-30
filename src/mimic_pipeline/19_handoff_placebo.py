"""v7_mimic/scripts/19_handoff_placebo.py -- HANDOFF_PLACEBO_GPU.md from the condition manifests and the inventory."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json, time, socket, collections
from pathlib import Path
V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic")
inv = json.load(open(V7 / "results/inventory_mimic_test.json")); s = inv["summary"]; Q = inv["questions"]
val = json.load(open(V7 / "logs/validate_conditions.json"))["arrows"]
L = ["# HANDOFF_PLACEBO_GPU — condições de imagem do Placebo no teste MIMIC/Diff-VQA (v7_mimic → executor de GPU)", "",
     "> **Nota de versão — v2, 2026-10-12.** Motivo: a galeria v1 mostrou que, em alvos com mais de uma região (2/3 das unidades), o placebo era um bloco único (hflip/vflip/rot180/translação do conjunto) ou uma única anatomia, com forma e posição sem correspondência caixa a caixa com o alvo. Regra v2 (decisão do candidato, 12/10): para alvos de mais de uma caixa, um placebo por caixa, na ordem anatomia homóloga sem o atributo (razão de área 0,8–1,25) → translação vertical com área exata (pares bilaterais simétricos deslocam juntos) → espelho horizontal por caixa → anatomia ampliada (0,5–2,0); restrições: ≥ 80 % no atlas torácico, inteira no filme, sem tocar o alvo dilatado em 5 px, caixas do placebo sem sobreposição entre si. Alvos de uma caixa inalterados. **Todas as baterias já rodadas no MIMIC com os arrows v1 de T, P, S e derivados (blur10, regmean, doses) ficam obsoletas e devem ser refeitas pelo executor de GPU com os sha abaixo.** C0 e C1 não mudam de conteúdo, mas foram regerados sobre o conjunto v2 de unidades (sha novos); o sham com região esperada de uma caixa não muda de pixel, o de duas caixas muda de placebo (irrelevante para SHAM_*, que ocluem a região esperada) — o conjunto de unidades do sham também mudou. Arrows v1 preservados em `tmp/v7_mimic/conditions_v1/`; inventário v1 em `tmp/v7_mimic/inventory_mimic_test_v1_final.json`.", "",
     f"Escrito em {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} na {socket.gethostname()} pelo executor só-CPU. Nada lançado. Arrows e PNG são dados credenciados (PhysioNet: MIMIC-CXR-JPG, Medical-Diff-VQA, Chest ImaGenome): ficam na gpu1.",
     "Formato M3AE/med_vlm idêntico ao `vqa_mimic_test.arrow` (mesmos `question_id`, respostas e `answer_type` 0 fechada / 1 aberta); uma linha por unidade (imagem × regiões-alvo), `image_id = mimic/<dicom_id>#<regiões>`. Todos validados em CPU com `load_condition_dataset` + normalizador do med_vlm (`logs/validate_conditions.json`).", "",
     "## Arrows (caminhos absolutos)", "| conjunto | condição | arquivo | sha256 | unidades | perguntas (fechadas/abertas) |", "|---|---|---|---|---:|---|"]
for tag in ("placebo", "sham"):
    man = json.load(open(V7 / f"data/conditions/manifest_mimic_{tag}.json"))
    for c, m in man["conditions"].items():
        L.append(f"| {tag} | {c} | `{m['file']}` | `{m['sha256']}` | {m['n_units']} | {m['n_questions']} ({m['n_by_answer_type']['closed']}/{m['n_by_answer_type']['open']}) |")
L += ["", "Manifestos: `data/conditions/manifest_mimic_{placebo,sham}.json` (sha, unidades, regiões, método do placebo, doses por unidade). Inventário: `results/inventory_mimic_test.json`.",
      "- C0 = PNG lado maior 1024 (o mesmo do `vqa_mimic_test.arrow`); C1 = cinza 384×384 RGB(128,128,128); T/P/S = alvo / placebo / tudo fora do alvo em preto; `_blur10` = blur gaussiano σ = 10 % da largura; `_regmean` = cor média da própria região.",
      "- Doses (preto): alvo dilatado ×1,5 / ×2 no lugar (T1.5/T2). Placebo da dose: alvos de 1 caixa → recolocado para a forma dilatada (regra pré-registrada do Kvasir, `place_placebos_by_factor`); alvos multicaixa (v2) → cada caixa do placebo dilatada no lugar (`dilate_to_area`), válida se não toca o alvo dilatado + 5 px, ≥ 80 % no atlas por caixa e sem sobreposição entre caixas. Unidades sem solução ou com alvo dilatado > 40 % do FOV ficam fora; comparações de dose devem usar só as perguntas presentes no par T_k/P_k.",
      "- Sham (closed_no_sham, gold \"no\" com o ImaGenome também negando): `sham_C0` e oclusor sobre a região esperada do achado (duas regiões-folha mais frequentes no silver) em preto (`SHAM_black`) e blur 10 % (`SHAM_blur10`).",
      "- `_mvt500` do HEAL não foi gerado (subconjunto de 500 do MedVLThinker; se necessário, amostrar dos arrows acima).", "",
      "## Contagens avaliáveis por classe", "| classe | total | avaliáveis (com aproximadas) | só exatas |", "|---|---:|---:|---:|"]
for c in ("closed_yes", "closed_no", "closed_no_sham", "open", "closed_view"):
    L.append(f"| {c} | {s['by_class'].get(c,0)} | {s['evaluable_by_class_with_approx'].get(c,0)} | {s['evaluable_by_class_exact_only'].get(c,0)} |")
L += ["", f"Motivos de exclusão: {s['exclusion_reasons']}. Detalhes em `docs/inventory_mimic.md`.", "",
      "## O que rodar (todas as linhas × todas as condições)",
      "Para cada linha MIMIC com adapter ou zero-shot: `harness.extract_predictions_circle` com `--condition <C> --condition-arrow <arquivo acima>` (conferir o sha antes), `--progress-checkpoint`, carimbo de proveniência, mesmo rescoring da C0. Condições placebo: C0, C1, T, P, S, T_blur10, P_blur10, S_blur10, T_regmean, P_regmean, S_regmean, T1.5, P1.5, T2, P2 (15); sham: C0, SHAM_black, SHAM_blur10 (3).",
      "Linhas previstas nos YAMLs/filas existentes (`configs/`, `v7_zeroshot/logs/jobs_zeroshot*.json`): qwen2vl_{lora,dora}_mimic, qwen2vl_{lora,dora}_vt_mimic, smolvlm2_{lora,dora}_mimic, smolvlm2_{lora,dora}_ft_mimic (sementes 0–2), M3AE MIMIC, e zero-shot MedVLThinker, LLaVA-Med, Qwen2.5-VL, MedGemma. O braço só-texto (`qwen2vl_lora_txt_mimic`, `--no-image`) não depende da imagem: basta a predição TXT já existente, ou rodar C0 para conferir invariância.",
      "", "## Classes para a análise",
      f"- `closed_yes` ({s['evaluable_by_class_with_approx']['closed_yes']}; {s['evaluable_by_class_exact_only']['closed_yes']} exatas): necessidade Δ_nec = Acc(C0) − Acc(T) contra Acc(C0) − Acc(P), por preenchimento e por entidade; `entity_map_quality` em cada pergunta do inventário separa exatas/aproximadas.",
      f"- `closed_no` ({s['evaluable_by_class_with_approx']['closed_no']}): mesmas condições, perguntas com <loc> e gold \"no\".",
      f"- `open` ({s['evaluable_by_class_with_approx']['open']}): mesmas condições, métrica de resposta aberta do rescoring.",
      f"- `closed_no_sham` ({s['evaluable_by_class_with_approx']['closed_no_sham']}): IPR = P(yes | SHAM_*) − P(yes | sham_C0), como no v7_sham.",
      "- Estratos úteis no inventário: `template_id`, `entity`, `target_regions`, `n_target_boxes`, `target_area_frac` (quadro) e `target_area_frac_thorax` (FOV), `placebo_method` (por caixa, separado por `|`), `placebo_scheme` (single_box / per_box), `placebo_rule` = v2 em todas as unidades."]
(V7 / "HANDOFF_PLACEBO_GPU.md").write_text("\n".join(L) + "\n"); print("ok", len(L))
