# Folha de numeros -- artigo 1 (teste de necessidade da regiao com controle de posicao) -- rodada 1

Gerada 2026-10-30 19:13:47 por v7_artigo1/scripts/make_numbers_artigo1.py (sha256 19dbb23de46d). Um numero por linha; fonte e sha256 abaixo. Acuracia em %, diferencas em pp (uma casa), razoes com tres casas; IC 95 % por bootstrap por imagem (2 000 replicas, semente 20260913, replicas fixas por base). Media (DP) entre as 3 sementes (condicional aos tres modelos). Delta = Acc(mascara deslocada) - Acc(alvo ocluido); headroom = Acc(intacta) - Acc(text-decoder-only da mesma familia e semente); criterio B = IC de Delta exclui zero por cima sob preto E sob blur 10 %. HEAL e Medical-Diff-VQA: so perguntas fechadas no corpo (abertas do MIMIC so no JSON); Kvasir-VQA-x1: as classes do inventario (polipo, instrumento, controle negativo, polipo secundario; abertas e fechadas, como na folha de 01/10). Bases: Kvasir-VQA-x1, HEAL-MedVQA, Medical-Diff-VQA (SLAKE so na S11).

## S1. Contagens (resumo e introducao)

- **linhas afinadas por base / total** — `27 / 81 (3 bases)`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **familias / sementes** — `3 (Qwen2-VL-2B, SmolVLM2-2.2B, M3AE) / 3 (0, 1, 2)`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **linhas por base: Qwen2-VL (LoRA, DoRA) x (encoder congelado, afinado) x 3; SmolVLM2 idem; M3AE ajuste completo x 3** — `12 + 12 + 3 = 27`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **Kvasir-VQA-x1: perguntas avaliaveis (polipo / instrumento / controle negativo / polipo secundario)** — `2121 (943 / 314 / 728 / 136)`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **Kvasir-VQA-x1: unidades imagem x alvo (polipo / instrumento) / imagens de teste com mascara / imagens de teste** — `243 (136 / 107) / 303 / 1291`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **HEAL-MedVQA: fechadas avaliaveis (sim / nao) / unidades imagem x anatomia / imagens** — `1446 (711 / 735) / 1360 / 1135`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **Medical-Diff-VQA: avaliaveis / perguntas do subconjunto de teste (inventario v2)** — `1985 / 3000`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **Medical-Diff-VQA: fechadas-sim / fechadas-nao (alinhadas) / negativas do oclusor / abertas** — `443 / 67 / 391 / 1084`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **Medical-Diff-VQA: fechadas-sim so com mapeamento exato de entidade** — `430`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **criterio B sem condicao de headroom, Kvasir-VQA-x1, polipo (linhas necessarias / linhas)** — `25/27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Kvasir-VQA-x1, polipo: resoluveis / necessarias entre as resoluveis / linhas** — `27 / 25 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Kvasir-VQA-x1, instrumento (linhas necessarias / linhas)** — `25/27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Kvasir-VQA-x1, instrumento: resoluveis / necessarias entre as resoluveis / linhas** — `27 / 25 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Kvasir-VQA-x1, controle 'Is there text?' (linhas necessarias / linhas)** — `0/27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Kvasir-VQA-x1, controle 'Is there text?': resoluveis / necessarias entre as resoluveis / linhas** — `27 / 0 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Kvasir-VQA-x1, polipo secundario (linhas necessarias / linhas)** — `25/27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Kvasir-VQA-x1, polipo secundario: resoluveis / necessarias entre as resoluveis / linhas** — `27 / 25 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, HEAL-MedVQA, fechada-sim (linhas necessarias / linhas)** — `0/27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, fechada-sim: resoluveis / necessarias entre as resoluveis / linhas** — `21 / 0 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, HEAL-MedVQA, fechada-nao (linhas necessarias / linhas)** — `0/27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, fechada-nao: resoluveis / necessarias entre as resoluveis / linhas** — `21 / 0 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Medical-Diff-VQA, fechada-sim (linhas necessarias / linhas)** — `12/27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, fechada-sim: resoluveis / necessarias entre as resoluveis / linhas** — `27 / 12 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Medical-Diff-VQA, fechada-nao (linhas necessarias / linhas)** — `0/27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, fechada-nao: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder congelado** — `6/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder afinado** — `6/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder afinado** — `5/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 5 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder congelado** — `6/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Kvasir-VQA-x1, polipo, M3AE, encoder ajuste completo** — `2/3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Kvasir-VQA-x1, polipo, M3AE, encoder ajuste completo: resoluveis / necessarias entre as resoluveis / linhas** — `3 / 2 / 3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder congelado** — `6/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder afinado** — `6/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder afinado** — `5/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 5 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder congelado** — `6/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Kvasir-VQA-x1, instrumento, M3AE, encoder ajuste completo** — `2/3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Kvasir-VQA-x1, instrumento, M3AE, encoder ajuste completo: resoluveis / necessarias entre as resoluveis / linhas** — `3 / 2 / 3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder congelado** — `0/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `5 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder afinado** — `0/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `4 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder afinado** — `0/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder congelado** — `0/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, HEAL-MedVQA, fechada-sim, M3AE, encoder ajuste completo** — `0/3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, fechada-sim, M3AE, encoder ajuste completo: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder congelado** — `3/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 3 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder afinado** — `2/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 2 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder afinado** — `3/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 3 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder congelado** — `3/6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 3 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Medical-Diff-VQA, fechada-sim, M3AE, encoder ajuste completo** — `1/3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE, encoder ajuste completo: resoluveis / necessarias entre as resoluveis / linhas** — `3 / 1 / 3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Aorta, fechada-sim: resoluveis / necessarias entre as resoluveis / linhas (criterio B sem condicao: 1)** — `0 / 0 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Aorta, fechada-sim, Qwen2-VL-2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Aorta, fechada-sim, SmolVLM2-2.2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Aorta, fechada-sim, Qwen2-VL-2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Aorta, fechada-sim, SmolVLM2-2.2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Aorta, fechada-sim, M3AE, encoder ajuste completo: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Heart, fechada-sim: resoluveis / necessarias entre as resoluveis / linhas (criterio B sem condicao: 0)** — `0 / 0 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Heart, fechada-sim, Qwen2-VL-2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Heart, fechada-sim, SmolVLM2-2.2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Heart, fechada-sim, Qwen2-VL-2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Heart, fechada-sim, SmolVLM2-2.2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Heart, fechada-sim, M3AE, encoder ajuste completo: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Right upper lung, fechada-sim: resoluveis / necessarias entre as resoluveis / linhas (criterio B sem condicao: 1)** — `14 / 0 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Right upper lung, fechada-sim, Qwen2-VL-2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `5 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Right upper lung, fechada-sim, SmolVLM2-2.2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `2 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Right upper lung, fechada-sim, Qwen2-VL-2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `5 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Right upper lung, fechada-sim, SmolVLM2-2.2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `2 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Right upper lung, fechada-sim, M3AE, encoder ajuste completo: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Left upper lung, fechada-sim: resoluveis / necessarias entre as resoluveis / linhas (criterio B sem condicao: 1)** — `7 / 0 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Left upper lung, fechada-sim, Qwen2-VL-2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `3 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Left upper lung, fechada-sim, SmolVLM2-2.2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Left upper lung, fechada-sim, Qwen2-VL-2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `3 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Left upper lung, fechada-sim, SmolVLM2-2.2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **HEAL-MedVQA, Left upper lung, fechada-sim, M3AE, encoder ajuste completo: resoluveis / necessarias entre as resoluveis / linhas** — `1 / 0 / 3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, pleural effusion: resoluveis / necessarias entre as resoluveis / linhas (criterio B sem condicao: 0)** — `27 / 0 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, pleural effusion, Qwen2-VL-2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, pleural effusion, SmolVLM2-2.2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, pleural effusion, Qwen2-VL-2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, pleural effusion, SmolVLM2-2.2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, pleural effusion, M3AE, encoder ajuste completo: resoluveis / necessarias entre as resoluveis / linhas** — `3 / 0 / 3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, atelectasis: resoluveis / necessarias entre as resoluveis / linhas (criterio B sem condicao: 0)** — `0 / 0 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, atelectasis, Qwen2-VL-2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, atelectasis, SmolVLM2-2.2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, atelectasis, Qwen2-VL-2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, atelectasis, SmolVLM2-2.2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, atelectasis, M3AE, encoder ajuste completo: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, lung opacity: resoluveis / necessarias entre as resoluveis / linhas (criterio B sem condicao: 0)** — `2 / 0 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, lung opacity, Qwen2-VL-2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, lung opacity, SmolVLM2-2.2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `1 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, lung opacity, Qwen2-VL-2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `1 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, lung opacity, SmolVLM2-2.2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, lung opacity, M3AE, encoder ajuste completo: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, cardiomegaly: resoluveis / necessarias entre as resoluveis / linhas (criterio B sem condicao: 0)** — `0 / 0 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, cardiomegaly, Qwen2-VL-2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, cardiomegaly, SmolVLM2-2.2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, cardiomegaly, Qwen2-VL-2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, cardiomegaly, SmolVLM2-2.2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, cardiomegaly, M3AE, encoder ajuste completo: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, edema: resoluveis / necessarias entre as resoluveis / linhas (criterio B sem condicao: 9)** — `12 / 5 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, edema, Qwen2-VL-2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, edema, SmolVLM2-2.2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `4 / 1 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, edema, Qwen2-VL-2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `2 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, edema, SmolVLM2-2.2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `4 / 2 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, edema, M3AE, encoder ajuste completo: resoluveis / necessarias entre as resoluveis / linhas** — `2 / 2 / 3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, vascular congestion: resoluveis / necessarias entre as resoluveis / linhas (criterio B sem condicao: 1)** — `23 / 1 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, vascular congestion, Qwen2-VL-2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `4 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, vascular congestion, SmolVLM2-2.2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `4 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, vascular congestion, Qwen2-VL-2B, encoder afinado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 1 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, vascular congestion, SmolVLM2-2.2B, encoder congelado: resoluveis / necessarias entre as resoluveis / linhas** — `6 / 0 / 6`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **Medical-Diff-VQA, vascular congestion, M3AE, encoder ajuste completo: resoluveis / necessarias entre as resoluveis / linhas** — `3 / 0 / 3`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>

## S1b. Escada de vereditos (L0 queda bruta; L1 controle pareado; L2 dois preenchimentos; L3 image gain legivel)

- **escada, Kvasir-VQA-x1, polipo: L0 / L1 / L2 / L3 (linhas)** — `27 / 27 / 25 / 25 de 27`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, polipo: L3 com TF-IDF no lugar do text-only arm (so interno)** — `25 de 27`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder congelado: L0 / L1 / L2 / L3** — `6 / 6 / 6 / 6 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder afinado: L0 / L1 / L2 / L3** — `6 / 6 / 6 / 6 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder afinado: L0 / L1 / L2 / L3** — `6 / 6 / 5 / 5 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder congelado: L0 / L1 / L2 / L3** — `6 / 6 / 6 / 6 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, polipo, M3AE, encoder ajuste completo: L0 / L1 / L2 / L3** — `3 / 3 / 2 / 2 de 3`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, polipo, zero-shot LLAVA_MED: L0 / L1 / L2 / L3** — `nao / nao / nao / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, polipo, zero-shot MEDGEMMA: L0 / L1 / L2 / L3** — `sim / sim / sim / sim`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, polipo, zero-shot MEDVLTHINKER: L0 / L1 / L2 / L3** — `sim / sim / sim / sim`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, polipo, zero-shot QWEN25VL: L0 / L1 / L2 / L3** — `nao / nao / nao / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, polipo: linhas afinadas que mudam em L0->L1 (perdem / ganham)** — `0 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, polipo: linhas afinadas que mudam em L1->L2 (perdem / ganham)** — `2 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, polipo: linhas afinadas que mudam em L2->L3 (perdem / ganham)** — `0 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, instrumento: L0 / L1 / L2 / L3 (linhas)** — `27 / 26 / 25 / 25 de 27`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, instrumento: L3 com TF-IDF no lugar do text-only arm (so interno)** — `25 de 27`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder congelado: L0 / L1 / L2 / L3** — `6 / 6 / 6 / 6 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder afinado: L0 / L1 / L2 / L3** — `6 / 6 / 6 / 6 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder afinado: L0 / L1 / L2 / L3** — `6 / 5 / 5 / 5 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder congelado: L0 / L1 / L2 / L3** — `6 / 6 / 6 / 6 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, instrumento, M3AE, encoder ajuste completo: L0 / L1 / L2 / L3** — `3 / 3 / 2 / 2 de 3`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, instrumento, zero-shot LLAVA_MED: L0 / L1 / L2 / L3** — `nao / nao / nao / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, instrumento, zero-shot MEDGEMMA: L0 / L1 / L2 / L3** — `nao / nao / nao / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, instrumento, zero-shot MEDVLTHINKER: L0 / L1 / L2 / L3** — `sim / sim / sim / sim`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, instrumento, zero-shot QWEN25VL: L0 / L1 / L2 / L3** — `sim / sim / sim / sim`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, instrumento: linhas afinadas que mudam em L0->L1 (perdem / ganham)** — `1 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, instrumento: linhas afinadas que mudam em L1->L2 (perdem / ganham)** — `1 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Kvasir-VQA-x1, instrumento: linhas afinadas que mudam em L2->L3 (perdem / ganham)** — `0 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-sim: L0 / L1 / L2 / L3 (linhas)** — `0 / 1 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-sim: L3 com TF-IDF no lugar do text-only arm (so interno)** — `0 de 27`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder congelado: L0 / L1 / L2 / L3** — `0 / 0 / 0 / 0 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: L0 / L1 / L2 / L3** — `0 / 0 / 0 / 0 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder afinado: L0 / L1 / L2 / L3** — `0 / 0 / 0 / 0 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: L0 / L1 / L2 / L3** — `0 / 0 / 0 / 0 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-sim, M3AE, encoder ajuste completo: L0 / L1 / L2 / L3** — `0 / 1 / 0 / 0 de 3`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-sim, zero-shot LLAVA_MED: L0 / L1 / L2 / L3** — `nao / nao / nao / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-sim, zero-shot MEDGEMMA: L0 / L1 / L2 / L3** — `nao / nao / nao / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-sim, zero-shot MEDVLTHINKER: L0 / L1 / L2 / L3** — `nao / nao / nao / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-sim, zero-shot QWEN25VL: L0 / L1 / L2 / L3** — `nao / nao / nao / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-sim: linhas afinadas que mudam em L0->L1 (perdem / ganham)** — `0 / 1`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-sim: linhas afinadas que mudam em L1->L2 (perdem / ganham)** — `1 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-sim: linhas afinadas que mudam em L2->L3 (perdem / ganham)** — `0 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-nao: L0 / L1 / L2 / L3 (linhas)** — `27 / 0 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-nao: L3 com TF-IDF no lugar do text-only arm (so interno)** — `0 de 27`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder congelado: L0 / L1 / L2 / L3** — `6 / 0 / 0 / 0 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder afinado: L0 / L1 / L2 / L3** — `6 / 0 / 0 / 0 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder afinado: L0 / L1 / L2 / L3** — `6 / 0 / 0 / 0 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder congelado: L0 / L1 / L2 / L3** — `6 / 0 / 0 / 0 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-nao, M3AE, encoder ajuste completo: L0 / L1 / L2 / L3** — `3 / 0 / 0 / 0 de 3`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-nao, zero-shot LLAVA_MED: L0 / L1 / L2 / L3** — `nao / nao / nao / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-nao, zero-shot MEDGEMMA: L0 / L1 / L2 / L3** — `sim / sim / sim / sim`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-nao, zero-shot MEDVLTHINKER: L0 / L1 / L2 / L3** — `sim / sim / nao / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-nao, zero-shot QWEN25VL: L0 / L1 / L2 / L3** — `sim / nao / nao / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-nao: linhas afinadas que mudam em L0->L1 (perdem / ganham)** — `27 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-nao: linhas afinadas que mudam em L1->L2 (perdem / ganham)** — `0 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, HEAL-MedVQA, fechada-nao: linhas afinadas que mudam em L2->L3 (perdem / ganham)** — `0 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-sim: L0 / L1 / L2 / L3 (linhas)** — `18 / 18 / 12 / 12 de 27`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-sim: L3 com TF-IDF no lugar do text-only arm (so interno)** — `12 de 27`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder congelado: L0 / L1 / L2 / L3** — `6 / 4 / 3 / 3 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: L0 / L1 / L2 / L3** — `5 / 5 / 2 / 2 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder afinado: L0 / L1 / L2 / L3** — `3 / 3 / 3 / 3 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: L0 / L1 / L2 / L3** — `1 / 3 / 3 / 3 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-sim, M3AE, encoder ajuste completo: L0 / L1 / L2 / L3** — `3 / 3 / 1 / 1 de 3`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-sim, zero-shot LLAVA_MED: L0 / L1 / L2 / L3** — `sim / sim / sim / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-sim, zero-shot MEDGEMMA: L0 / L1 / L2 / L3** — `sim / sim / sim / sim`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-sim, zero-shot MEDVLTHINKER: L0 / L1 / L2 / L3** — `sim / sim / sim / sim`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-sim, zero-shot QWEN25VL: L0 / L1 / L2 / L3** — `sim / sim / sim / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-sim: linhas afinadas que mudam em L0->L1 (perdem / ganham)** — `3 / 3`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-sim: linhas afinadas que mudam em L1->L2 (perdem / ganham)** — `6 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-sim: linhas afinadas que mudam em L2->L3 (perdem / ganham)** — `0 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-nao: L0 / L1 / L2 / L3 (linhas)** — `0 / 0 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-nao: L3 com TF-IDF no lugar do text-only arm (so interno)** — `0 de 27`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder congelado: L0 / L1 / L2 / L3** — `0 / 0 / 0 / 0 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder afinado: L0 / L1 / L2 / L3** — `0 / 0 / 0 / 0 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder afinado: L0 / L1 / L2 / L3** — `0 / 0 / 0 / 0 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder congelado: L0 / L1 / L2 / L3** — `0 / 0 / 0 / 0 de 6`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-nao, M3AE, encoder ajuste completo: L0 / L1 / L2 / L3** — `0 / 0 / 0 / 0 de 3`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-nao, zero-shot LLAVA_MED: L0 / L1 / L2 / L3** — `nao / nao / nao / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-nao, zero-shot MEDGEMMA: L0 / L1 / L2 / L3** — `nao / nao / nao / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-nao, zero-shot MEDVLTHINKER: L0 / L1 / L2 / L3** — `nao / sim / nao / nao`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-nao, zero-shot QWEN25VL: L0 / L1 / L2 / L3** — `nao / sim / sim / sim`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-nao: linhas afinadas que mudam em L0->L1 (perdem / ganham)** — `0 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-nao: linhas afinadas que mudam em L1->L2 (perdem / ganham)** — `0 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **escada, Medical-Diff-VQA, fechada-nao: linhas afinadas que mudam em L2->L3 (perdem / ganham)** — `0 / 0`  
  <sub>v7_artigo1/analysis/escada_vereditos.json · sha256 66d9dd0396c9</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates, 728 perguntas): resoluveis / necessarias entre as resoluveis / linhas** — `27 / 0 / 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio B sem condicao de headroom, Kvasir-VQA-x1, controle negativo (3 templates) (linhas necessarias / linhas)** — `0/27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **escada, Kvasir-VQA-x1, controle negativo (3 templates): L0 / L1 / L2 / L3 (linhas)** — `25 / 0 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>

## S2. Setup (bases, modelos, receitas, text-decoder-only, TF-IDF, proveniencia do encoder invertido)

- **receita: Qwen2-VL LoRA, encoder congelado (Kvasir semente 0)** — `lr 0.0002; epocas 3; grad_accum 4; parametros treinaveis 4358144 de 2213343744 (0.001969031702289439)`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **receita: Qwen2-VL DoRA, encoder congelado (Kvasir semente 0)** — `lr 0.0002; epocas 3; grad_accum 4; parametros treinaveis 4458496 de 2213444096 (0.002014279921529132)`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **receita: SmolVLM2 LoRA, encoder afinado (Kvasir semente 0)** — `lr 0.0002; epocas 3; grad_accum 4; parametros treinaveis 9277440 de 2256062320 (0.004112226828911357)`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **receita: SmolVLM2 DoRA, encoder afinado (Kvasir semente 0)** — `lr 0.0002; epocas 3; grad_accum 4; parametros treinaveis 9567360 de 2256352240 (0.004240189022969215)`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **receita: Qwen2-VL LoRA, encoder afinado (Kvasir semente 0)** — `lr 0.0002; epocas 3; grad_accum 4; parametros treinaveis 8290304 de 2217275904 (0.0037389591367696564)`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **receita: Qwen2-VL DoRA, encoder afinado (Kvasir semente 0)** — `lr 0.0002; epocas 3; grad_accum 4; parametros treinaveis 8554496 de 2217540096 (0.0038576511042260767)`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **receita: SmolVLM2 LoRA, encoder congelado (Kvasir semente 0)** — `lr 0.0002; epocas 3; grad_accum 4; parametros treinaveis 6291456 de 2253076336 (0.0027923847494530697)`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **receita: SmolVLM2 DoRA, encoder congelado (Kvasir semente 0)** — `lr 0.0002; epocas 3; grad_accum 4; parametros treinaveis 6488064 de 2253272944 (0.002879395510994961)`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **receita LoRA/DoRA (YAML do HEAL)** — `r 16; lora_alpha 32; target_modules [q_proj, k_proj, v_proj, o_proj]; lr 2e-4; epocas 3; batch 4 x grad_accum 4`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **text-decoder-only** — `mesma receita de ajuste, sem imagem; LoRA so no modelo de linguagem (Qwen2-VL e SmolVLM2: LoRA em todas as celulas, inclusive para as linhas DoRA); M3AE: treinado com imagem cinza constante (384x384, RGB 128) no treino, validacao e teste`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **classificador so-pergunta (TF-IDF)** — `TF-IDF de palavras 1-2-gramas + regressao logistica (C = 1), sem imagem; Kvasir por item publicado; HEAL alinhado aos 1 446 qids; MIMIC M0 subset nas fechadas`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **zero-shot LLAVA_MED: checkpoint do Hub / snapshot / bytes dos pesos** — `chaoyinshe/llava-med-v1.5-mistral-7b-hf / 627be53734c667cbb1669608dac747a4485a22d7 / 15133487104`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA: checkpoint do Hub / snapshot / bytes dos pesos** — `google/medgemma-1.5-4b-it / 91850547d9f0b2fdd21aa7c5f4f3d1a8a52c243b / 8600158944`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER: checkpoint do Hub / snapshot / bytes dos pesos** — `UCSC-VLAA/MedVLThinker-7B-RL_PMC / 75ef8116d2f6664bcc4f850990a873999e7fbbf6 / 16584333312`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL: checkpoint do Hub / snapshot / bytes dos pesos** — `Qwen/Qwen2.5-VL-7B-Instruct / cc594898137f460bfe9f0759e9844b3ce807cfb5 / 16584333312`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **proveniencia Kvasir-VQA-x1 QWEN2VL_LORA_VT_KVASIR_seed0: sha256 dos pesos (fonte)** — `0efbbb5ba5dafbef35e805a0363385704225c1263b790562ac69dfdab59ce4f4 (carimbo do JSON (checkpoint_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Kvasir-VQA-x1 SMOLVLM_LORA_FT_KVASIR_seed0: sha256 dos pesos (fonte)** — `ad466add324294e2e8b6e4d004752aab99519555c0f591724e74aaba6c42ef20 (carimbo do JSON (checkpoint_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Kvasir-VQA-x1 QWEN2VL_DORA_VT_KVASIR_seed0: sha256 dos pesos (fonte)** — `77ede13faf69ca81c45fb5b456ff290347a2e14ec961c98b65bae03f4e05a1f0 (carimbo do JSON (checkpoint_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Kvasir-VQA-x1 SMOLVLM_DORA_FT_KVASIR_seed0: sha256 dos pesos (fonte)** — `d0d67581002c5d1e1c29d3bfeaed151a1cec5ce29980224d455d1efbb3f14c8c (carimbo do JSON (checkpoint_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Kvasir-VQA-x1 QWEN2VL_LORA_VT_KVASIR_seed1: sha256 dos pesos (fonte)** — `f79a4269225bd1c6538fe76f60586674e2c05f92bc016ba7fd6b45ec7520991e (carimbo do JSON (checkpoint_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Kvasir-VQA-x1 SMOLVLM_LORA_FT_KVASIR_seed1: sha256 dos pesos (fonte)** — `ba173a72eab9a7c94447990f03010b81c9df5f84880b9055edb3ad930d914ffc (carimbo do JSON (checkpoint_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Kvasir-VQA-x1 QWEN2VL_DORA_VT_KVASIR_seed1: sha256 dos pesos (fonte)** — `1253090b5c3d5c10492b9a3b8580c568b9c9b0a9d45a104b62f65ea93c0bcf07 (carimbo do JSON (checkpoint_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Kvasir-VQA-x1 SMOLVLM_DORA_FT_KVASIR_seed1: sha256 dos pesos (fonte)** — `f79aa5234c1b27bec3fbd5b5e7e34ef89e1db64b2708925085b10dccd6ea685e (carimbo do JSON (checkpoint_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Kvasir-VQA-x1 QWEN2VL_LORA_VT_KVASIR_seed2: sha256 dos pesos (fonte)** — `908841de9b45529fd90c053f5375ad03de113d5f3cdf1683fa7b1e66dc1ab7bf (carimbo do JSON (checkpoint_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Kvasir-VQA-x1 SMOLVLM_LORA_FT_KVASIR_seed2: sha256 dos pesos (fonte)** — `7d3b23dbc4e46d0b0bb06d5885fc81456de5f0973dff5139d5d8f6fc388fe0c2 (carimbo do JSON (checkpoint_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Kvasir-VQA-x1 QWEN2VL_DORA_VT_KVASIR_seed2: sha256 dos pesos (fonte)** — `1e2bf195f8bf92190e4a85d737031e30f85fd0cecd56e9e8c7b6e9dc75a83b9c (carimbo do JSON (checkpoint_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Kvasir-VQA-x1 SMOLVLM_DORA_FT_KVASIR_seed2: sha256 dos pesos (fonte)** — `35fd8cc00fa4e591bf633d610446f283dee0e3e3e52af4f642be94e57dbf391b (carimbo do JSON (checkpoint_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia HEAL-MedVQA QWEN2VL_LORA_VT_HEAL_seed0: sha256 dos pesos (fonte)** — `975c31fc75b52d799626894dc26139fa15fbb6e233e47bbb23fad05a04ea5b72 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia HEAL-MedVQA SMOLVLM_LORA_FT_HEAL_seed0: sha256 dos pesos (fonte)** — `11ce18f82bdeba9ff36dabfae84b81a1e6eb7b0cb9502471ea2ff12f52896ab6 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia HEAL-MedVQA QWEN2VL_DORA_VT_HEAL_seed0: sha256 dos pesos (fonte)** — `6e464f395f41eec6cd98dce0e846ce80fcf6025be780d3ec0f36d967130bb578 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia HEAL-MedVQA SMOLVLM_DORA_FT_HEAL_seed0: sha256 dos pesos (fonte)** — `f1b35e37e71fddf91c9a02669e7b3e6a9c84a46912c2337e38c84a62ba354d7f (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia HEAL-MedVQA QWEN2VL_LORA_VT_HEAL_seed1: sha256 dos pesos (fonte)** — `b106aa87d9ea19dac6b4e426cb7f05805625a118500796ee50210940a1cc099d (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia HEAL-MedVQA SMOLVLM_LORA_FT_HEAL_seed1: sha256 dos pesos (fonte)** — `fb5710a971a5b8af59ec130bdf86bc8bad310b2f4b2c6896c253d7cf31493615 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia HEAL-MedVQA QWEN2VL_DORA_VT_HEAL_seed1: sha256 dos pesos (fonte)** — `b27a04f0c65cf1ea62b9ca05a4cf99c396e5df93b8ecc013723c296d89df3567 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia HEAL-MedVQA SMOLVLM_DORA_FT_HEAL_seed1: sha256 dos pesos (fonte)** — `1bff962e21857fc75828570d0733375d8b736b63495c948b6d7d52fb6f3da559 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia HEAL-MedVQA QWEN2VL_LORA_VT_HEAL_seed2: sha256 dos pesos (fonte)** — `0e859ed321a29d9732456374d59c3404874981ea918461a3d534f697cafe21c4 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia HEAL-MedVQA SMOLVLM_LORA_FT_HEAL_seed2: sha256 dos pesos (fonte)** — `1bda958fcd5b1a17c8554382855d6450bf7e2109c307d87441f61e52b8b29cdf (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia HEAL-MedVQA QWEN2VL_DORA_VT_HEAL_seed2: sha256 dos pesos (fonte)** — `4da6fa4999bf07f44bc110b9f6d2b7375a8412bb9ea4641ebc7b6578ead29cdf (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia HEAL-MedVQA SMOLVLM_DORA_FT_HEAL_seed2: sha256 dos pesos (fonte)** — `cdb5b770878e72aa493ac470c46535cde84b2c452d2b6dd1a143c292ab0b6266 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Medical-Diff-VQA QWEN2VL_LORA_VT_MIMIC_seed0: sha256 dos pesos (fonte)** — `684928e1ca2538ecc8472165c19383c0cf4d18421f4b05fb2d2d87a3bb824981 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Medical-Diff-VQA SMOLVLM_LORA_FT_MIMIC_seed0: sha256 dos pesos (fonte)** — `fb0f7c36cfb7c24f132c1e2ef00db23d84014e4a5a6730f1f6d07f934b7fec4a (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Medical-Diff-VQA QWEN2VL_DORA_VT_MIMIC_seed0: sha256 dos pesos (fonte)** — `058549f626407937bca83fc8cbc918abcb4ccee777bf46b3175c0066109f95ea (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Medical-Diff-VQA SMOLVLM_DORA_FT_MIMIC_seed0: sha256 dos pesos (fonte)** — `57eee8fa761d11ba6bf309ea140cdb8c178238615cf85136258b6664149ccae1 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Medical-Diff-VQA QWEN2VL_LORA_VT_MIMIC_seed1: sha256 dos pesos (fonte)** — `99f03873e0678412c0bd3515da858949c6be30227ab8d54d19189f0126347939 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Medical-Diff-VQA SMOLVLM_LORA_FT_MIMIC_seed1: sha256 dos pesos (fonte)** — `b13c56f1be75a3ea3159a1ee949b8277559d2c4492e2b55aa5e8c653a3ded9d7 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Medical-Diff-VQA QWEN2VL_DORA_VT_MIMIC_seed1: sha256 dos pesos (fonte)** — `e96f3e6d15a81d2cfb84514d7734457d76894d6e0dce84e981dab6aba7b2236a (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Medical-Diff-VQA SMOLVLM_DORA_FT_MIMIC_seed1: sha256 dos pesos (fonte)** — `f8c92c9b584ef346caee062d6329d93069ef61108f923bec9c4de5f10d3ca4f5 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Medical-Diff-VQA QWEN2VL_LORA_VT_MIMIC_seed2: sha256 dos pesos (fonte)** — `5edd7ce1580646650d88ff9fb599dc22738ec87480d1de71c1e88cb2c6beebfd (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Medical-Diff-VQA SMOLVLM_LORA_FT_MIMIC_seed2: sha256 dos pesos (fonte)** — `c2dc45dd7e3009830f4f0eba291d16e27250c3d5ac2504663b1419c706856242 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Medical-Diff-VQA QWEN2VL_DORA_VT_MIMIC_seed2: sha256 dos pesos (fonte)** — `63d1884ca1ec3442bf37da8f5c9205d38b87a83dc88e4c4e15a07721fb9e9ec0 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **proveniencia Medical-Diff-VQA SMOLVLM_DORA_FT_MIMIC_seed2: sha256 dos pesos (fonte)** — `57fb29eb1f657c0ec98516f389c0a0a131c33cb5775c6c549811dbbce2be2e35 (carimbo do JSON (adapter_sha256))`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **Kvasir-VQA-x1: perguntas distintas no teste (perguntas do teste) / entre as avaliáveis (avaliáveis)** — `18 (10779) / 14 (2121)`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1: perguntas distintas entre as avaliáveis, pólipo / instrumento / controle negativo / pólipo secundário (perguntas)** — `7 (943) / 3 (314) / 3 (728) / 1 (136)`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA: perguntas distintas nas fechadas avaliáveis (fechadas) / fechada-sim / fechada-não** — `293 (1446) / 127 (711) / 261 (735)`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA: perguntas distintas no teste (perguntas do teste)** — `317 (2851)`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA: perguntas distintas nas fechadas avaliáveis (fechadas) / fechada-sim / fechada-não** — `147 (510) / 110 (443) / 43 (67)`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA: perguntas distintas no teste (perguntas do teste)** — `286 (3000)`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1: templates (cada pergunta distinta é um template; sem campo de template no inventário), teste / avaliáveis** — `18 / 14`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA: templates fechados / abertos (padrões de texto com achado e anatomia substituídos; perguntas sem casamento único: 0)** — `3 / 3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA: templates fechados (fechadas avaliáveis por template)** — `Is there {achado} in the {anatomia} of this patient? (484); Does {anatomia} suffer from {achado}? (482); Does the patient have {achado} at {anatomia}? (480)`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA: templates (template_id do inventário), teste / fechadas avaliáveis** — `12 / 5 (T00 20, T02 119, T03 45, T06 168, T07 158)`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA: linhas nas médias de dose / linhas** — `26 / 27`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA: proveniência da linha fora das médias de dose (QWEN2VL_DORA_HEAL_seed2)** — `1x do adapter original (ausente na gpu1); 1,5x e 2x do retreino de 03/10: dois checkpoints na mesma celula; fora das medias de dose (item 20); original ausente também no Drive (S10)`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>

## S3. Kvasir-VQA-x1

- **Kvasir-VQA-x1, polipo: n perguntas / imagens (alinhadas)** — `943 / 136`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `58.8 (0.5) / 28.8 (0.0) / 27.6 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+29.9 (0.5); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `+9.2 (1.4) / +5.8 (1.3) / +5.1 (1.9)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-2.1 (1.3) / 0.940 (0.021) / 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `62.0 (0.7) / 27.6 (0.0) / 27.6 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+34.5 (0.7); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `+20.3 (3.6) / +8.7 (1.7) / +9.4 (2.6)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.5 (0.6) / 0.743 (0.059) / 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `63.9 (0.6) / 28.8 (0.0) / 27.6 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+35.1 (0.6); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `+14.2 (1.8) / +5.7 (3.6) / +5.1 (2.5)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.2 (0.8) / 0.954 (0.015) / 5/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `58.3 (0.4) / 27.6 (0.0) / 27.6 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+30.7 (0.4); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `+10.8 (1.4) / +7.8 (1.4) / +7.2 (1.2)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.5 (1.1) / 0.766 (0.035) / 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, M3AE, encoder ajuste completo: Acc intacta / text-decoder-only / TF-IDF (%)** — `58.4 (0.4) / 27.6 (0.0) / 27.6 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, M3AE, encoder ajuste completo: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+30.8 (0.4); 3/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, M3AE, encoder ajuste completo: Delta preto / blur 10 % / cor media (pp)** — `+7.1 (0.5) / +3.1 (1.5) / +3.5 (1.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo, M3AE, encoder ajuste completo: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.4 (0.8) / 0.487 (0.198) / 2/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo: faixa de Delta preto nas 27 linhas (pp)** — `+6.8 a +26.2`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo: faixa de Delta blur 10 % nas 27 linhas (pp)** — `+0.2 a +11.5`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo: faixa de Delta cor media nas 27 linhas (pp)** — `+2.4 a +14.0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo: faixa de headroom nas 27 linhas (pp)** — `+29.3 a +35.9`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo: faixa de custo da mascara deslocada, preto nas 27 linhas (pp)** — `-3.8 a +1.2`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo: faixa da suficiencia (preto) nas 27 linhas** — `0.345 a 0.977`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento: n perguntas / imagens (alinhadas)** — `314 / 107`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `72.2 (0.8) / 0.0 (0.0) / 0.0 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+72.2 (0.8); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `+27.7 (1.8) / +36.0 (2.6) / +25.4 (3.8)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+3.1 (1.5) / 0.539 (0.058) / 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `74.8 (0.8) / 0.0 (0.0) / 0.0 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+74.8 (0.8); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `+18.0 (5.6) / +17.4 (5.6) / +16.1 (4.3)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+3.9 (2.2) / 0.450 (0.073) / 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `75.0 (1.2) / 0.0 (0.0) / 0.0 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+75.0 (1.2); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `+23.0 (14.3) / +32.1 (11.1) / +20.3 (8.5)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+3.0 (2.0) / 0.759 (0.081) / 5/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `70.3 (1.3) / 0.0 (0.0) / 0.0 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+70.3 (1.3); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `+23.7 (2.4) / +44.9 (2.2) / +29.2 (1.2)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+5.1 (0.7) / 0.470 (0.066) / 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, M3AE, encoder ajuste completo: Acc intacta / text-decoder-only / TF-IDF (%)** — `70.5 (0.5) / 0.0 (0.0) / 0.0 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, M3AE, encoder ajuste completo: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+70.5 (0.5); 3/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, M3AE, encoder ajuste completo: Delta preto / blur 10 % / cor media (pp)** — `+26.5 (13.1) / +10.3 (8.5) / +7.6 (6.4)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento, M3AE, encoder ajuste completo: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+1.2 (1.3) / 0.702 (0.152) / 2/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento: faixa de Delta preto nas 27 linhas (pp)** — `+4.8 a +47.1`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento: faixa de Delta blur 10 % nas 27 linhas (pp)** — `+4.5 a +48.7`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento: faixa de Delta cor media nas 27 linhas (pp)** — `+2.9 a +34.7`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento: faixa de headroom nas 27 linhas (pp)** — `+68.2 a +77.1`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento: faixa de custo da mascara deslocada, preto nas 27 linhas (pp)** — `-0.3 a +6.7`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, instrumento: faixa da suficiencia (preto) nas 27 linhas** — `0.368 a 0.906`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?': n perguntas / imagens (alinhadas)** — `243 / 243`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `99.2 (0.0) / 86.4 (0.0) / 86.4 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', Qwen2-VL-2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+12.8 (0.0); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', Qwen2-VL-2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `+0.1 (0.5) / -0.1 (0.6) / +0.2 (0.7)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', Qwen2-VL-2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+1.0 (0.6) / 0.244 (0.005) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `98.6 (0.2) / 86.4 (0.0) / 86.4 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', SmolVLM2-2.2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+12.1 (0.2); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', SmolVLM2-2.2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `+0.3 (0.4) / +0.1 (0.2) / +0.0 (0.4)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+0.5 (0.5) / 0.255 (0.003) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `98.7 (0.3) / 86.4 (0.0) / 86.4 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', Qwen2-VL-2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+12.3 (0.3); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', Qwen2-VL-2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `+0.3 (0.3) / +0.3 (0.3) / +0.4 (0.3)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', Qwen2-VL-2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+0.3 (0.3) / 0.258 (0.003) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `98.4 (0.3) / 86.4 (0.0) / 86.4 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', SmolVLM2-2.2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+11.9 (0.3); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', SmolVLM2-2.2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `-0.2 (0.2) / -0.1 (0.4) / -0.1 (0.4)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+1.0 (0.2) / 0.243 (0.001) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', M3AE, encoder ajuste completo: Acc intacta / text-decoder-only / TF-IDF (%)** — `98.8 (0.0) / 86.4 (0.0) / 86.4 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', M3AE, encoder ajuste completo: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+12.3 (0.0); 3/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', M3AE, encoder ajuste completo: Delta preto / blur 10 % / cor media (pp)** — `-1.5 (0.2) / -0.8 (0.7) / -0.5 (1.3)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', M3AE, encoder ajuste completo: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+3.3 (0.4) / 0.531 (0.193) / 0/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?': faixa de Delta preto nas 27 linhas (pp)** — `-1.6 a +0.8`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?': faixa de Delta blur 10 % nas 27 linhas (pp)** — `-1.6 a +0.8`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?': faixa de Delta cor media nas 27 linhas (pp)** — `-1.6 a +0.8`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?': faixa de headroom nas 27 linhas (pp)** — `+11.5 a +12.8`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?': faixa de custo da mascara deslocada, preto nas 27 linhas (pp)** — `+0.0 a +3.7`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, controle 'Is there text?': faixa da suficiencia (preto) nas 27 linhas** — `0.237 a 0.750`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario: n perguntas / imagens (alinhadas)** — `136 / 136`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `96.9 (0.7) / 0.0 (0.0) / 0.0 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, Qwen2-VL-2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+96.9 (0.7); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, Qwen2-VL-2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `+26.5 (7.9) / +12.9 (4.6) / +10.3 (5.1)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, Qwen2-VL-2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-1.6 (0.6) / 0.991 (0.040) / 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `98.9 (0.6) / 0.0 (0.0) / 0.0 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, SmolVLM2-2.2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+98.9 (0.6); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, SmolVLM2-2.2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `+24.0 (14.9) / +8.0 (3.8) / +6.2 (3.3)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.4 (0.4) / 1.007 (0.009) / 5/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `98.5 (0.0) / 0.0 (0.0) / 0.0 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, Qwen2-VL-2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+98.5 (0.0); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, Qwen2-VL-2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `+28.6 (13.9) / +7.4 (4.7) / +6.2 (3.4)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, Qwen2-VL-2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.7 (0.5) / 1.015 (0.000) / 5/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `98.3 (0.8) / 0.0 (0.0) / 0.0 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, SmolVLM2-2.2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+98.3 (0.8); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, SmolVLM2-2.2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `+35.9 (8.2) / +22.2 (1.7) / +22.1 (4.6)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.5 (0.8) / 0.981 (0.057) / 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, M3AE, encoder ajuste completo: Acc intacta / text-decoder-only / TF-IDF (%)** — `98.5 (0.7) / 0.0 (0.0) / 0.0 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, M3AE, encoder ajuste completo: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+98.5 (0.7); 3/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, M3AE, encoder ajuste completo: Delta preto / blur 10 % / cor media (pp)** — `+5.9 (0.7) / +4.2 (0.4) / +4.4 (0.7)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario, M3AE, encoder ajuste completo: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.5 (0.4) / 0.373 (0.427) / 3/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario: faixa de Delta preto nas 27 linhas (pp)** — `+5.1 a +50.0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario: faixa de Delta blur 10 % nas 27 linhas (pp)** — `+2.2 a +24.3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario: faixa de Delta cor media nas 27 linhas (pp)** — `+2.9 a +28.7`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario: faixa de headroom nas 27 linhas (pp)** — `+96.3 a +100.0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario: faixa de custo da mascara deslocada, preto nas 27 linhas (pp)** — `-2.2 a +0.7`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, polipo secundario: faixa da suficiencia (preto) nas 27 linhas** — `0.111 a 1.031`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Kvasir-VQA-x1, pólipo: n perguntas por linha (faixas abaixo)** — `943`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `57.7 – 64.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `27.6 – 28.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `+29.3 – +35.9`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `-3.8 – +1.2`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-2.3 – +1.6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `+6.8 – +26.2`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `+0.2 – +11.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `+2.4 – +14.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.345 – 0.977`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento: n perguntas por linha (faixas abaixo)** — `314`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `68.2 – 77.1`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `0.0 – 0.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `+68.2 – +77.1`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `-0.3 – +6.7`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-1.3 – +3.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `+4.8 – +47.1`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `+4.5 – +48.7`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `+2.9 – +34.7`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.368 – 0.906`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?": n perguntas por linha (faixas abaixo)** — `243`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?": acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `97.9 – 99.2`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?": text-only arm, mínimo – máximo entre as 27 linhas (%)** — `86.4 – 86.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?": image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `+11.5 – +12.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?": custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `+0.0 – +3.7`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?": custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `+0.0 – +2.9`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?": Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `-1.6 – +0.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?": Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-1.6 – +0.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?": Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `-1.6 – +0.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?": suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.237 – 0.750`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo: image gain against the question-only classifier (TF-IDF), mínimo – máximo entre as 27 linhas (pp)** — `+30.1 – +37.2`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, Qwen2-VL-2B, encoder congelado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+31.2 (0.5) / +29.9 (0.5); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, SmolVLM2-2.2B, encoder afinado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+34.5 (0.7) / +34.5 (0.7); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, Qwen2-VL-2B, encoder afinado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+36.3 (0.6) / +35.1 (0.6); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, SmolVLM2-2.2B, encoder congelado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+30.7 (0.4) / +30.7 (0.4); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, M3AE, encoder ajuste completo: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 3 linhas (pp); linhas com IC > 0** — `+30.8 (0.4) / +30.8 (0.4); 3/3 / 3/3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, QWEN2VL_LORA_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+31.3 [+28.7, +33.9] / +30.0 [+27.4, +32.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, SMOLVLM_LORA_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+35.5 [+32.9, +38.0] / +35.5 [+32.9, +38.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, QWEN2VL_LORA_VT_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+37.2 [+34.6, +40.0] / +35.9 [+33.3, +38.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, SMOLVLM_LORA_FT_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+30.8 [+28.0, +33.4] / +30.8 [+28.0, +33.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, QWEN2VL_DORA_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+31.6 [+29.0, +34.0] / +30.3 [+27.8, +32.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, SMOLVLM_DORA_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+34.3 [+31.4, +36.9] / +34.3 [+31.4, +36.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, QWEN2VL_DORA_VT_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+36.7 [+33.9, +39.3] / +35.4 [+32.8, +38.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, SMOLVLM_DORA_FT_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+31.3 [+28.6, +33.9] / +31.3 [+28.6, +33.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, M3AE_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+31.2 [+28.5, +33.7] / +31.2 [+28.5, +33.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, QWEN2VL_LORA_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+30.5 [+27.8, +33.3] / +29.3 [+26.6, +32.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, SMOLVLM_LORA_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+34.8 [+32.0, +37.5] / +34.8 [+32.0, +37.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, QWEN2VL_LORA_VT_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+35.8 [+33.2, +38.5] / +34.6 [+31.9, +37.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, SMOLVLM_LORA_FT_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+30.1 [+27.4, +32.7] / +30.1 [+27.4, +32.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, QWEN2VL_DORA_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+30.5 [+27.8, +33.2] / +29.3 [+26.5, +31.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, SMOLVLM_DORA_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+34.0 [+31.5, +36.6] / +34.0 [+31.5, +36.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, QWEN2VL_DORA_VT_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+36.6 [+33.7, +39.4] / +35.3 [+32.5, +38.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, SMOLVLM_DORA_FT_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+30.4 [+27.6, +33.1] / +30.4 [+27.6, +33.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, M3AE_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+30.4 [+27.7, +33.2] / +30.4 [+27.7, +33.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, QWEN2VL_LORA_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+31.7 [+29.1, +34.1] / +30.4 [+28.0, +32.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, SMOLVLM_LORA_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+34.6 [+31.6, +37.3] / +34.6 [+31.6, +37.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, QWEN2VL_LORA_VT_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+35.9 [+33.4, +38.5] / +34.7 [+32.0, +37.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, SMOLVLM_LORA_FT_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+30.9 [+28.1, +33.5] / +30.9 [+28.1, +33.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, QWEN2VL_DORA_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+31.5 [+28.9, +33.9] / +30.2 [+27.6, +32.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, SMOLVLM_DORA_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+33.6 [+30.9, +36.1] / +33.6 [+30.9, +36.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, QWEN2VL_DORA_VT_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+35.7 [+32.8, +38.4] / +34.5 [+31.6, +37.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, SMOLVLM_DORA_FT_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+30.6 [+27.9, +33.3] / +30.6 [+27.9, +33.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, pólipo, M3AE_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+30.9 [+28.1, +33.6] / +30.9 [+28.1, +33.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento: image gain against the question-only classifier (TF-IDF), mínimo – máximo entre as 27 linhas (pp)** — `+68.2 – +77.1`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder congelado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+72.2 (0.8) / +72.2 (0.8); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder afinado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+74.8 (0.8) / +74.8 (0.8); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder afinado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+75.0 (1.2) / +75.0 (1.2); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder congelado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+70.3 (1.3) / +70.3 (1.3); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, M3AE, encoder ajuste completo: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 3 linhas (pp); linhas com IC > 0** — `+70.5 (0.5) / +70.5 (0.5); 3/3 / 3/3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, QWEN2VL_LORA_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+70.7 [+66.1, +75.2] / +70.7 [+66.1, +75.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, SMOLVLM_LORA_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+74.2 [+69.9, +78.6] / +74.2 [+69.9, +78.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, QWEN2VL_LORA_VT_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+74.2 [+69.9, +78.7] / +74.2 [+69.9, +78.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, SMOLVLM_LORA_FT_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+70.7 [+66.2, +75.4] / +70.7 [+66.2, +75.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, QWEN2VL_DORA_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+72.9 [+68.5, +77.7] / +72.9 [+68.5, +77.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, SMOLVLM_DORA_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+75.2 [+70.6, +79.8] / +75.2 [+70.6, +79.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, QWEN2VL_DORA_VT_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+73.9 [+69.4, +78.5] / +73.9 [+69.4, +78.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, SMOLVLM_DORA_FT_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+68.2 [+63.3, +73.0] / +68.2 [+63.3, +73.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, M3AE_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+71.0 [+65.7, +76.1] / +71.0 [+65.7, +76.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, QWEN2VL_LORA_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+72.0 [+67.8, +76.2] / +72.0 [+67.8, +76.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, SMOLVLM_LORA_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+74.8 [+70.4, +79.5] / +74.8 [+70.4, +79.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, QWEN2VL_LORA_VT_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+74.8 [+70.2, +79.7] / +74.8 [+70.2, +79.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, SMOLVLM_LORA_FT_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+70.4 [+65.9, +74.9] / +70.4 [+65.9, +74.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, QWEN2VL_DORA_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+72.6 [+68.0, +77.4] / +72.6 [+68.0, +77.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, SMOLVLM_DORA_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+74.2 [+70.0, +78.5] / +74.2 [+70.0, +78.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, QWEN2VL_DORA_VT_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+74.5 [+69.6, +79.4] / +74.5 [+69.6, +79.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, SMOLVLM_DORA_FT_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+69.7 [+65.0, +74.8] / +69.7 [+65.0, +74.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, M3AE_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+70.4 [+65.4, +75.2] / +70.4 [+65.4, +75.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, QWEN2VL_LORA_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+72.6 [+68.4, +77.0] / +72.6 [+68.4, +77.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, SMOLVLM_LORA_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+76.1 [+72.0, +80.3] / +76.1 [+72.0, +80.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, QWEN2VL_LORA_VT_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+75.5 [+71.2, +79.9] / +75.5 [+71.2, +79.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, SMOLVLM_LORA_FT_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+72.0 [+67.4, +76.3] / +72.0 [+67.4, +76.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, QWEN2VL_DORA_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+72.6 [+67.9, +77.5] / +72.6 [+67.9, +77.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, SMOLVLM_DORA_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+74.2 [+70.3, +78.2] / +74.2 [+70.3, +78.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, QWEN2VL_DORA_VT_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+77.1 [+72.7, +81.4] / +77.1 [+72.7, +81.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, SMOLVLM_DORA_FT_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+70.7 [+66.1, +75.2] / +70.7 [+66.1, +75.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, instrumento, M3AE_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+70.1 [+65.2, +74.9] / +70.1 [+65.2, +74.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?": image gain against the question-only classifier (TF-IDF), mínimo – máximo entre as 27 linhas (pp)** — `+11.5 – +12.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", Qwen2-VL-2B, encoder congelado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+12.8 (0.0) / +12.8 (0.0); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", SmolVLM2-2.2B, encoder afinado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+12.1 (0.2) / +12.1 (0.2); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", Qwen2-VL-2B, encoder afinado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+12.3 (0.3) / +12.3 (0.3); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", SmolVLM2-2.2B, encoder congelado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+11.9 (0.3) / +11.9 (0.3); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", M3AE, encoder ajuste completo: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 3 linhas (pp); linhas com IC > 0** — `+12.3 (0.0) / +12.3 (0.0); 3/3 / 3/3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", QWEN2VL_LORA_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.8 [+8.5, +17.1] / +12.8 [+8.5, +17.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", SMOLVLM_LORA_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.9 [+7.8, +16.2] / +11.9 [+7.8, +16.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", QWEN2VL_LORA_VT_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.9 [+7.8, +16.2] / +11.9 [+7.8, +16.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", SMOLVLM_LORA_FT_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.9 [+7.8, +16.2] / +11.9 [+7.8, +16.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", QWEN2VL_DORA_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.8 [+8.5, +17.1] / +12.8 [+8.5, +17.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", SMOLVLM_DORA_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.3 [+8.1, +16.7] / +12.3 [+8.1, +16.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", QWEN2VL_DORA_VT_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.9 [+7.8, +16.2] / +11.9 [+7.8, +16.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", SMOLVLM_DORA_FT_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.9 [+7.8, +16.2] / +11.9 [+7.8, +16.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", M3AE_KVASIR_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.3 [+7.8, +16.8] / +12.3 [+7.8, +16.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", QWEN2VL_LORA_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.8 [+8.5, +17.1] / +12.8 [+8.5, +17.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", SMOLVLM_LORA_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.3 [+8.1, +16.7] / +12.3 [+8.1, +16.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", QWEN2VL_LORA_VT_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.8 [+8.5, +17.1] / +12.8 [+8.5, +17.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", SMOLVLM_LORA_FT_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.9 [+7.8, +16.2] / +11.9 [+7.8, +16.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", QWEN2VL_DORA_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.8 [+8.5, +17.1] / +12.8 [+8.5, +17.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", SMOLVLM_DORA_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.9 [+7.8, +16.2] / +11.9 [+7.8, +16.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", QWEN2VL_DORA_VT_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.3 [+8.2, +16.5] / +12.3 [+8.2, +16.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", SMOLVLM_DORA_FT_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.5 [+7.3, +15.6] / +11.5 [+7.3, +15.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", M3AE_KVASIR_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.3 [+7.9, +16.6] / +12.3 [+7.9, +16.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", QWEN2VL_LORA_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.8 [+8.5, +17.1] / +12.8 [+8.5, +17.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", SMOLVLM_LORA_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.9 [+7.8, +16.2] / +11.9 [+7.8, +16.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", QWEN2VL_LORA_VT_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.3 [+8.2, +16.5] / +12.3 [+8.2, +16.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", SMOLVLM_LORA_FT_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.9 [+7.8, +16.2] / +11.9 [+7.8, +16.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", QWEN2VL_DORA_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.8 [+8.5, +17.1] / +12.8 [+8.5, +17.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", SMOLVLM_DORA_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.3 [+8.1, +16.7] / +12.3 [+8.1, +16.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", QWEN2VL_DORA_VT_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.3 [+8.1, +16.7] / +12.3 [+8.1, +16.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", SMOLVLM_DORA_FT_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.3 [+8.2, +16.5] / +12.3 [+8.2, +16.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, controle "Is there text?", M3AE_KVASIR_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.3 [+8.1, +16.6] / +12.3 [+8.1, +16.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template ("Is there a green/black box artefact?"): perguntas avaliáveis / n por linha** — `243 / 243`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_LORA_KVASIR_seed0: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-6.6 [-11.0, -2.5] / -3.7 [-7.3, -0.4] / -7.0 [-11.0, -3.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_LORA_KVASIR_seed0: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-4.5 [-9.3, +0.4] / -11.9 [-16.7, -7.5] / -4.5 [-8.1, -0.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_LORA_VT_KVASIR_seed0: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-4.1 [-7.4, -1.2] / -0.8 [-2.1, +0.0] / -0.4 [-1.8, +0.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_LORA_FT_KVASIR_seed0: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-3.7 [-6.5, -1.2] / -0.4 [-2.6, +1.6] / -2.1 [-3.9, -0.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_DORA_KVASIR_seed0: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-8.2 [-12.1, -4.7] / -4.9 [-8.8, -1.3] / -6.6 [-10.8, -3.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_DORA_KVASIR_seed0: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-8.2 [-12.9, -3.3] / -4.9 [-8.8, -1.4] / -4.9 [-8.4, -1.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_DORA_VT_KVASIR_seed0: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-2.5 [-5.6, +0.4] / -0.8 [-2.6, +0.8] / -1.6 [-3.4, -0.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_DORA_FT_KVASIR_seed0: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-2.9 [-8.1, +2.4] / -2.1 [-5.5, +1.7] / -0.8 [-4.4, +2.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, M3AE_KVASIR_seed0: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-2.9 [-7.0, +0.9] / -0.8 [-3.0, +1.2] / -2.1 [-4.7, +0.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_LORA_KVASIR_seed1: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-7.0 [-11.5, -2.6] / -5.8 [-10.6, -1.2] / -4.9 [-9.8, -0.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_LORA_KVASIR_seed1: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-8.6 [-13.3, -4.1] / -4.9 [-8.4, -1.3] / -0.8 [-4.0, +2.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_LORA_VT_KVASIR_seed1: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-7.0 [-11.6, -2.5] / -4.5 [-7.6, -1.8] / -1.2 [-4.2, +1.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_LORA_FT_KVASIR_seed1: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-4.5 [-8.9, +0.0] / -0.4 [-4.1, +3.3] / -0.8 [-3.8, +2.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_DORA_KVASIR_seed1: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-7.8 [-12.4, -3.3] / -4.9 [-8.5, -1.6] / -4.1 [-8.1, -0.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_DORA_KVASIR_seed1: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-11.9 [-17.2, -6.9] / -8.6 [-12.8, -5.0] / -7.4 [-11.7, -3.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_DORA_VT_KVASIR_seed1: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-8.2 [-12.7, -3.7] / -4.5 [-8.2, -1.2] / -8.2 [-12.4, -4.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_DORA_FT_KVASIR_seed1: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-3.3 [-7.9, +1.3] / -1.6 [-4.3, +0.8] / +2.1 [+0.4, +4.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, M3AE_KVASIR_seed1: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-3.7 [-7.7, +0.4] / +0.0 [+0.0, +0.0] / +0.0 [-1.6, +1.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_LORA_KVASIR_seed2: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-8.2 [-13.1, -3.6] / -5.3 [-10.8, -0.4] / -4.9 [-9.9, +0.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_LORA_KVASIR_seed2: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-12.8 [-17.9, -8.0] / -13.2 [-18.8, -7.7] / -11.1 [-17.0, -5.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_LORA_VT_KVASIR_seed2: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-7.8 [-13.4, -2.4] / -2.9 [-5.8, -0.4] / -2.1 [-4.6, +0.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_LORA_FT_KVASIR_seed2: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-2.9 [-7.0, +1.3] / -0.8 [-2.9, +1.1] / -1.2 [-3.1, +0.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_DORA_KVASIR_seed2: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-11.5 [-16.7, -6.2] / -11.9 [-18.0, -6.0] / -10.7 [-16.4, -5.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_DORA_KVASIR_seed2: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-6.6 [-11.5, -2.0] / -9.9 [-14.6, -5.6] / -8.2 [-12.7, -4.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_DORA_VT_KVASIR_seed2: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-4.5 [-8.8, +0.0] / -2.1 [-4.9, +0.8] / -0.8 [-4.3, +2.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_DORA_FT_KVASIR_seed2: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-4.5 [-9.1, +0.4] / -1.2 [-3.7, +1.2] / +0.0 [-1.6, +1.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, M3AE_KVASIR_seed2: Δ preto [IC] / Δ blur 10 % [IC] / Δ cor média [IC] (pp)** — `-7.8 [-12.4, -3.1] / -0.8 [-3.0, +1.2] / -2.5 [-5.3, +0.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, Δ preto, 27 linhas: linhas com limite superior do IC < 0 / com limite inferior do IC > 0; mínimo – máximo (pp)** — `17/27 / 0/27; -12.8 – -2.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, Δ blur 10 %, 27 linhas: linhas com limite superior do IC < 0 / com limite inferior do IC > 0; mínimo – máximo (pp)** — `15/27 / 0/27; -13.2 – +0.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, Δ cor média, 27 linhas: linhas com limite superior do IC < 0 / com limite inferior do IC > 0; mínimo – máximo (pp)** — `13/27 / 1/27; -11.1 – +2.1`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, Δ preto, 15 linhas de 01/10: linhas com limite superior do IC < 0 / com limite inferior do IC > 0; mínimo – máximo (pp)** — `12/15 / 0/15; -12.8 – -2.9`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, Δ blur 10 %, 15 linhas de 01/10: linhas com limite superior do IC < 0 / com limite inferior do IC > 0; mínimo – máximo (pp)** — `12/15 / 0/15; -13.2 – +0.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, Δ cor média, 15 linhas de 01/10: linhas com limite superior do IC < 0 / com limite inferior do IC > 0; mínimo – máximo (pp)** — `10/15 / 0/15; -11.1 – +0.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_LORA_KVASIR_seed0: Δ blur 4 % [IC] (pp)** — `-1.6 [-4.6, +1.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_LORA_KVASIR_seed0: Δ blur 4 % [IC] (pp)** — `-3.3 [-5.9, -0.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_DORA_KVASIR_seed0: Δ blur 4 % [IC] (pp)** — `-2.5 [-5.5, +0.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_DORA_KVASIR_seed0: Δ blur 4 % [IC] (pp)** — `-3.7 [-6.2, -1.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, M3AE_KVASIR_seed0: Δ blur 4 % [IC] (pp)** — `+0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_LORA_KVASIR_seed1: Δ blur 4 % [IC] (pp)** — `-2.1 [-5.1, +1.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_LORA_KVASIR_seed1: Δ blur 4 % [IC] (pp)** — `-0.8 [-2.5, +0.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_DORA_KVASIR_seed1: Δ blur 4 % [IC] (pp)** — `-0.8 [-3.2, +1.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_DORA_KVASIR_seed1: Δ blur 4 % [IC] (pp)** — `-2.9 [-5.3, -1.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, M3AE_KVASIR_seed1: Δ blur 4 % [IC] (pp)** — `+0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_LORA_KVASIR_seed2: Δ blur 4 % [IC] (pp)** — `-2.5 [-5.7, +0.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_LORA_KVASIR_seed2: Δ blur 4 % [IC] (pp)** — `-3.3 [-6.0, -0.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, QWEN2VL_DORA_KVASIR_seed2: Δ blur 4 % [IC] (pp)** — `-4.5 [-8.9, -0.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, SMOLVLM_DORA_KVASIR_seed2: Δ blur 4 % [IC] (pp)** — `-0.8 [-2.2, +0.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, M3AE_KVASIR_seed2: Δ blur 4 % [IC] (pp)** — `+0.4 [-0.9, +1.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, Δ blur 4 %, 15 linhas de 01/10 (as 12 de encoder invertido não têm predições sob blur 4 %): linhas com limite superior do IC < 0 / com limite inferior do IC > 0; mínimo – máximo (pp)** — `5/15 / 0/15; -4.5 – +0.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Kvasir-VQA-x1, artefact-box template, folha de 01/10 (15 linhas, IC por pergunta): IC exclui zero sob preto / blur 4 % / blur 10 % / cor média** — `12/15 / 5/15 / 11/15 / 10/15`  
  <sub>results/previous_sheets/numbers_isbi.md · sha256 </sub>

## S4. HEAL-MedVQA

- **HEAL-MedVQA, fechada-sim: n perguntas / imagens (alinhadas)** — `711 / 629`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `94.3 (1.4) / 91.7 (1.0) / 73.6 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+2.6 (1.2); 5/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `-0.6 (0.3) / -0.6 (0.5) / -0.3 (0.2)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-2.3 (1.1) / 0.979 (0.022) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `92.3 (0.7) / 89.8 (0.8) / 73.6 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+2.5 (1.3); 4/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `-0.2 (0.6) / +0.0 (0.4) / -0.1 (0.4)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-2.3 (0.6) / 0.342 (0.157) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `95.6 (0.8) / 91.7 (1.0) / 73.6 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+3.9 (1.2); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `+0.0 (0.3) / +0.2 (0.4) / +0.4 (0.6)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-1.1 (0.7) / 0.818 (0.175) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `93.1 (0.4) / 89.8 (0.8) / 73.6 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+3.2 (0.6); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `-0.8 (0.6) / -1.8 (0.3) / -1.9 (0.5)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+0.6 (0.8) / 0.099 (0.055) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, M3AE, encoder ajuste completo: Acc intacta / text-decoder-only / TF-IDF (%)** — `89.2 (3.6) / 90.6 (1.8) / 73.6 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, M3AE, encoder ajuste completo: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `-1.4 (2.2); 0/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, M3AE, encoder ajuste completo: Delta preto / blur 10 % / cor media (pp)** — `+1.8 (1.4) / +0.9 (0.2) / +1.1 (0.3)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, M3AE, encoder ajuste completo: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-2.4 (0.2) / 0.415 (0.566) / 0/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim: faixa de Delta preto nas 27 linhas (pp)** — `-1.4 a +3.2`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim: faixa de Delta blur 10 % nas 27 linhas (pp)** — `-2.1 a +1.1`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim: faixa de Delta cor media nas 27 linhas (pp)** — `-2.5 a +1.4`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim: faixa de headroom nas 27 linhas (pp)** — `-3.0 a +5.3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim: faixa de custo da mascara deslocada, preto nas 27 linhas (pp)** — `-3.5 a +2.1`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim: faixa da suficiencia (preto) nas 27 linhas** — `0.048 a 1.067`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao: n perguntas / imagens (alinhadas)** — `735 / 669`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `81.5 (2.4) / 79.6 (1.0) / 60.1 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+1.9 (1.9); 3/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `-0.0 (0.6) / -0.5 (0.4) / +0.6 (0.5)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+5.9 (1.8) / 0.882 (0.033) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `88.1 (1.4) / 80.7 (0.8) / 60.1 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+7.4 (1.9); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `-0.7 (0.9) / -1.0 (1.2) / +0.0 (0.7)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+7.2 (0.9) / 1.031 (0.062) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `84.5 (2.2) / 79.6 (1.0) / 60.1 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+4.9 (2.6); 5/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `-0.7 (0.6) / -0.3 (0.6) / -0.7 (0.7)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+4.8 (1.8) / 0.945 (0.057) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `83.8 (0.3) / 80.7 (0.8) / 60.1 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+3.2 (1.0); 4/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `+0.1 (0.2) / +0.6 (0.4) / +0.5 (0.5)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+3.5 (0.6) / 1.178 (0.011) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, M3AE, encoder ajuste completo: Acc intacta / text-decoder-only / TF-IDF (%)** — `90.2 (4.0) / 79.3 (2.4) / 60.1 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, M3AE, encoder ajuste completo: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+10.9 (3.5); 3/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, M3AE, encoder ajuste completo: Delta preto / blur 10 % / cor media (pp)** — `-0.1 (1.2) / +0.0 (0.5) / -0.3 (0.7)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao, M3AE, encoder ajuste completo: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+3.2 (0.9) / 0.769 (0.495) / 0/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao: faixa de Delta preto nas 27 linhas (pp)** — `-1.8 a +0.8`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao: faixa de Delta blur 10 % nas 27 linhas (pp)** — `-2.9 a +1.2`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao: faixa de Delta cor media nas 27 linhas (pp)** — `-1.9 a +1.5`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao: faixa de headroom nas 27 linhas (pp)** — `-1.4 a +14.4`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao: faixa de custo da mascara deslocada, preto nas 27 linhas (pp)** — `+2.2 a +8.4`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-nao: faixa da suficiencia (preto) nas 27 linhas** — `0.197 a 1.187`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim: n perguntas por linha (faixas abaixo)** — `711`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `85.5 – 97.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `88.5 – 92.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `-3.0 – +5.3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `-3.5 – +2.1`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-3.2 – +1.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `-1.4 – +3.2`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-2.1 – +1.1`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `-2.5 – +1.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.048 – 1.067`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não: n perguntas por linha (faixas abaixo)** — `735`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `77.0 – 92.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `77.7 – 82.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `-1.4 – +14.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `+2.2 – +8.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `+2.0 – +7.6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `-1.8 – +0.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-2.9 – +1.2`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `-1.9 – +1.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.197 – 1.187`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Aorta: n perguntas por linha (faixas abaixo)** — `201`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Aorta: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `92.5 – 96.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Aorta: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `96.5 – 96.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Aorta: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `-4.0 – +0.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Aorta: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `-4.0 – +0.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Aorta: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-3.5 – +0.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Aorta: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `-0.5 – +4.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Aorta: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-0.5 – +2.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Aorta: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `-0.5 – +2.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Aorta: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.005 – 1.075`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Heart: n perguntas por linha (faixas abaixo)** — `140`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Heart: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `95.7 – 100.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Heart: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `100.0 – 100.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Heart: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `-4.3 – +0.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Heart: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `-1.4 – +0.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Heart: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-2.1 – +0.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Heart: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `-0.7 – +2.9`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Heart: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-0.7 – +1.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Heart: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `-0.7 – +0.7`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Heart: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.000 – 1.014`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Right upper lung: n perguntas por linha (faixas abaixo)** — `91`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Right upper lung: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `76.9 – 97.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Right upper lung: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `80.2 – 86.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Right upper lung: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `-6.6 – +13.2`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Right upper lung: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `-7.7 – +0.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Right upper lung: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-7.7 – +0.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Right upper lung: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `-4.4 – +5.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Right upper lung: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-4.4 – +7.7`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Right upper lung: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `-5.5 – +8.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Right upper lung: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.084 – 1.071`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Left upper lung: n perguntas por linha (faixas abaixo)** — `73`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Left upper lung: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `74.0 – 94.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Left upper lung: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `78.1 – 84.9`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Left upper lung: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `-6.8 – +13.7`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Left upper lung: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `-12.3 – +1.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Left upper lung: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-9.6 – +1.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Left upper lung: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `-2.7 – +6.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Left upper lung: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-6.8 – +6.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Left upper lung: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `-5.5 – +6.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, anatomia Left upper lung: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.016 – 1.075`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim: image gain against the question-only classifier (TF-IDF), mínimo – máximo entre as 27 linhas (pp)** — `+12.0 – +23.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder congelado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+20.8 (1.4) / +2.6 (1.2); 6/6 / 5/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+18.8 (0.7) / +2.5 (1.3); 6/6 / 4/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder afinado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+22.0 (0.8) / +3.9 (1.2); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+19.5 (0.4) / +3.2 (0.6); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, M3AE, encoder ajuste completo: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 3 linhas (pp); linhas com IC > 0** — `+15.7 (3.6) / -1.4 (2.2); 3/3 / 0/3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, QWEN2VL_LORA_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+23.1 [+20.1, +26.2] / +3.8 [+2.3, +5.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, SMOLVLM_LORA_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+18.7 [+15.6, +21.8] / +1.5 [-0.6, +3.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, QWEN2VL_LORA_VT_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+21.7 [+18.6, +24.8] / +2.4 [+0.8, +3.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, SMOLVLM_LORA_FT_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.8 [+16.9, +22.8] / +2.7 [+0.8, +4.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, QWEN2VL_DORA_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+21.5 [+18.6, +24.7] / +2.3 [+0.9, +3.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, SMOLVLM_DORA_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+17.4 [+14.2, +20.6] / +0.3 [-1.8, +2.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, QWEN2VL_DORA_VT_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+22.2 [+19.2, +25.5] / +3.0 [+1.6, +4.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, SMOLVLM_DORA_FT_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+20.1 [+17.2, +23.2] / +3.0 [+1.0, +4.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, M3AE_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+15.9 [+12.6, +19.3] / -2.3 [-4.6, +0.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, QWEN2VL_LORA_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.4 [+16.6, +22.5] / +1.3 [-0.3, +2.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, SMOLVLM_LORA_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.1 [+16.1, +22.2] / +3.0 [+0.9, +5.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, QWEN2VL_LORA_VT_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+23.5 [+20.4, +26.7] / +5.3 [+3.5, +7.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, SMOLVLM_LORA_FT_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.0 [+16.0, +22.2] / +2.8 [+0.7, +5.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, QWEN2VL_DORA_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.8 [+16.9, +22.7] / +1.7 [+0.3, +3.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, SMOLVLM_DORA_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.5 [+16.5, +22.6] / +3.4 [+1.4, +5.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, QWEN2VL_DORA_VT_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+21.5 [+18.4, +24.7] / +3.4 [+1.5, +5.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, SMOLVLM_DORA_FT_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.3 [+16.3, +22.3] / +3.1 [+1.2, +5.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, M3AE_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.1 [+15.7, +22.6] / +1.1 [-1.5, +3.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, QWEN2VL_LORA_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.5 [+16.4, +22.6] / +2.5 [+0.9, +4.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, SMOLVLM_LORA_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+18.6 [+15.5, +21.6] / +3.1 [+1.0, +5.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, QWEN2VL_LORA_VT_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+21.2 [+18.2, +24.4] / +4.2 [+2.1, +6.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, SMOLVLM_LORA_FT_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.5 [+16.6, +22.6] / +4.1 [+2.1, +6.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, QWEN2VL_DORA_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+21.2 [+18.3, +24.4] / +4.2 [+2.4, +6.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, SMOLVLM_DORA_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.1 [+16.1, +22.2] / +3.7 [+1.5, +5.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, QWEN2VL_DORA_VT_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+22.1 [+18.9, +25.3] / +5.1 [+3.1, +7.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, SMOLVLM_DORA_FT_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.3 [+16.3, +22.3] / +3.8 [+1.7, +5.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, M3AE_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.0 [+8.5, +15.5] / -3.0 [-5.7, -0.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não: image gain against the question-only classifier (TF-IDF), mínimo – máximo entre as 27 linhas (pp)** — `+16.9 – +32.7`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, Qwen2-VL-2B, encoder congelado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+21.3 (2.4) / +1.9 (1.9); 6/6 / 3/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, SmolVLM2-2.2B, encoder afinado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+28.0 (1.4) / +7.4 (1.9); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, Qwen2-VL-2B, encoder afinado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+24.4 (2.2) / +4.9 (2.6); 6/6 / 5/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, SmolVLM2-2.2B, encoder congelado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+23.7 (0.3) / +3.2 (1.0); 6/6 / 4/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, M3AE, encoder ajuste completo: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 3 linhas (pp); linhas com IC > 0** — `+30.0 (4.0) / +10.9 (3.5); 3/3 / 3/3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, QWEN2VL_LORA_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+16.9 [+12.3, +21.2] / -1.4 [-3.6, +1.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, SMOLVLM_LORA_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+28.4 [+24.4, +32.4] / +8.8 [+6.1, +11.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, QWEN2VL_LORA_VT_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+25.4 [+21.2, +29.6] / +7.2 [+4.7, +9.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, SMOLVLM_LORA_FT_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+23.8 [+19.6, +27.8] / +4.2 [+1.8, +6.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, QWEN2VL_DORA_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+20.5 [+16.2, +24.8] / +2.3 [+0.3, +4.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, SMOLVLM_DORA_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+30.2 [+26.1, +34.0] / +10.6 [+7.8, +13.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, QWEN2VL_DORA_VT_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+25.3 [+21.0, +29.4] / +7.1 [+4.4, +9.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, SMOLVLM_DORA_FT_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+23.8 [+19.7, +27.7] / +4.2 [+1.8, +6.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, M3AE_HEAL_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+32.0 [+27.8, +35.8] / +14.4 [+11.7, +17.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, QWEN2VL_LORA_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+23.0 [+18.7, +27.1] / +3.4 [+1.2, +5.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, SMOLVLM_LORA_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+27.5 [+23.3, +31.7] / +6.8 [+4.0, +9.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, QWEN2VL_LORA_VT_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.9 [+15.3, +24.3] / +0.3 [-2.4, +3.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, SMOLVLM_LORA_FT_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+23.5 [+19.3, +27.6] / +2.9 [+0.5, +5.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, QWEN2VL_DORA_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+23.4 [+19.2, +27.4] / +3.8 [+1.8, +6.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, SMOLVLM_DORA_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+26.0 [+21.6, +30.0] / +5.3 [+2.6, +8.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, QWEN2VL_DORA_VT_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+25.7 [+21.3, +29.8] / +6.1 [+3.3, +8.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, SMOLVLM_DORA_FT_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+24.2 [+19.9, +28.2] / +3.5 [+1.1, +6.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, M3AE_HEAL_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+25.4 [+21.0, +29.7] / +7.5 [+4.4, +10.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, QWEN2VL_LORA_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+22.6 [+18.3, +26.7] / +2.0 [-0.1, +4.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, SMOLVLM_LORA_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+27.8 [+23.5, +31.7] / +6.4 [+3.7, +9.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, QWEN2VL_LORA_VT_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+24.9 [+20.2, +29.2] / +4.4 [+1.5, +7.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, SMOLVLM_LORA_FT_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+23.3 [+19.2, +27.2] / +1.9 [-0.4, +4.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, QWEN2VL_DORA_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+21.5 [+17.2, +25.7] / +1.0 [-1.3, +3.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, SMOLVLM_DORA_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+28.0 [+23.7, +32.1] / +6.7 [+3.9, +9.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, QWEN2VL_DORA_VT_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+25.2 [+20.7, +29.3] / +4.6 [+1.8, +7.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, SMOLVLM_DORA_FT_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+23.5 [+19.4, +27.5] / +2.2 [-0.1, +4.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-não, M3AE_HEAL_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+32.7 [+28.5, +36.4] / +10.7 [+8.0, +13.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **HEAL-MedVQA, fechada-sim, Aorta, Qwen2-VL-2B, encoder congelado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `201 / 96.5 (0.0) / +0.0 (0.0) / -0.2 (0.3) / -0.3 (0.3) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Heart, Qwen2-VL-2B, encoder congelado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `140 / 99.6 (0.4) / -0.4 (0.4) / +0.0 (0.0) / +0.0 (0.0) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Right upper lung, Qwen2-VL-2B, encoder congelado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `91 / 93.6 (2.3) / +7.9 (2.7) / -0.5 (1.5) / -1.6 (1.3) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Left upper lung, Qwen2-VL-2B, encoder congelado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `73 / 88.6 (2.8) / +6.4 (1.4) / -1.8 (0.7) / -1.4 (1.5) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Aorta, SmolVLM2-2.2B, encoder afinado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `201 / 96.1 (0.4) / -0.4 (0.4) / +0.3 (0.3) / +0.4 (0.2) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Heart, SmolVLM2-2.2B, encoder afinado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `140 / 99.5 (0.4) / -0.5 (0.4) / +0.0 (0.0) / +0.2 (0.4) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Right upper lung, SmolVLM2-2.2B, encoder afinado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `91 / 87.7 (1.6) / +4.6 (3.5) / -0.5 (2.1) / +1.1 (1.8) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Left upper lung, SmolVLM2-2.2B, encoder afinado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `73 / 83.1 (2.1) / +2.7 (3.5) / +1.8 (3.0) / +2.7 (2.3) / 1`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Aorta, Qwen2-VL-2B, encoder afinado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `201 / 96.2 (0.4) / -0.3 (0.4) / +0.0 (0.0) / +0.1 (0.2) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Heart, Qwen2-VL-2B, encoder afinado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `140 / 99.8 (0.4) / -0.2 (0.4) / +0.0 (0.0) / +0.0 (0.0) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Right upper lung, Qwen2-VL-2B, encoder afinado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `91 / 94.9 (1.8) / +9.2 (2.2) / +1.1 (1.2) / +0.9 (1.8) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Left upper lung, Qwen2-VL-2B, encoder afinado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `73 / 90.6 (2.0) / +8.4 (3.1) / -0.9 (0.7) / -0.2 (1.0) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Aorta, SmolVLM2-2.2B, encoder congelado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `201 / 96.4 (0.3) / -0.2 (0.3) / -0.1 (0.2) / -0.1 (0.2) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Heart, SmolVLM2-2.2B, encoder congelado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `140 / 99.3 (0.0) / -0.7 (0.0) / -0.2 (0.4) / -0.2 (0.4) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Right upper lung, SmolVLM2-2.2B, encoder congelado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `91 / 90.7 (0.6) / +7.5 (2.3) / -2.9 (1.9) / -3.5 (1.3) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Left upper lung, SmolVLM2-2.2B, encoder congelado: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `73 / 83.8 (1.6) / +3.4 (1.7) / +0.0 (2.1) / -4.6 (1.7) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Aorta, M3AE, encoder ajuste completo: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `201 / 94.2 (1.5) / -2.3 (1.5) / +2.7 (1.3) / +1.3 (0.8) / 1`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Heart, M3AE, encoder ajuste completo: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `140 / 97.6 (1.6) / -2.4 (1.6) / +1.4 (1.2) / +0.7 (0.7) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Right upper lung, M3AE, encoder ajuste completo: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `91 / 86.1 (8.4) / +1.1 (7.2) / +4.0 (2.5) / +6.2 (2.5) / 1`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, fechada-sim, Left upper lung, M3AE, encoder ajuste completo: n / Acc intacta (%) / headroom (pp) / Delta preto / blur 10 % (pp) / criterio B** — `73 / 84.5 (9.3) / +3.7 (9.3) / +2.7 (2.7) / +3.7 (2.9) / 0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL-MedVQA, estrato a_uma_anatomia: unidades / perguntas fechadas-sim / fechadas-nao** — `830 / 395 / 472`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, estrato c_multi_com_sobreposicao: unidades / perguntas fechadas-sim / fechadas-nao** — `328 / 199 / 162`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, estrato b_multi_sem_sobreposicao: unidades / perguntas fechadas-sim / fechadas-nao** — `202 / 117 / 101`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, a_uma_anatomia|closed_yes, M3AE, encoder ajuste completo: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `-3.3 (0.3) / -3.3 (0.7); +2.5 (1.4) / +1.1 (0.5); 0/3`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, a_uma_anatomia|closed_no, M3AE, encoder ajuste completo: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+3.8 (0.9) / +3.3 (0.5); -0.8 (1.5) / -0.5 (0.6); 0/3`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, b_multi_sem_sobreposicao|closed_yes, M3AE, encoder ajuste completo: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `-2.0 (0.5) / -2.6 (0.0); +1.4 (2.5) / +1.1 (2.0); 0/3`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, b_multi_sem_sobreposicao|closed_no, M3AE, encoder ajuste completo: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+2.0 (1.7) / +2.6 (2.1); +1.3 (1.5) / +0.0 (2.0); 0/3`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, c_multi_com_sobreposicao|closed_yes, M3AE, encoder ajuste completo: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `-1.0 (0.9) / -1.8 (0.8); +0.5 (0.9) / +0.5 (1.3); 0/3`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, c_multi_com_sobreposicao|closed_no, M3AE, encoder ajuste completo: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+2.1 (0.9) / +1.2 (1.1); +1.2 (1.2) / +1.6 (1.8); 1/3`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, a_uma_anatomia|closed_yes, Qwen2-VL-2B, encoder congelado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `-1.8 (0.7) / -1.9 (0.7); -0.4 (0.4) / +0.0 (0.4); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, a_uma_anatomia|closed_no, Qwen2-VL-2B, encoder congelado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+7.0 (1.3) / +5.9 (0.7); -0.4 (0.8) / -0.7 (0.4); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, b_multi_sem_sobreposicao|closed_yes, Qwen2-VL-2B, encoder congelado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `-4.0 (1.8) / -3.3 (1.4); -0.7 (0.6) / -1.0 (0.8); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, b_multi_sem_sobreposicao|closed_no, Qwen2-VL-2B, encoder congelado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+6.3 (3.4) / +4.3 (1.2); -0.3 (1.0) / -0.5 (0.8); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, c_multi_com_sobreposicao|closed_yes, Qwen2-VL-2B, encoder congelado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `-2.1 (2.2) / -1.3 (2.0); -0.8 (0.4) / -1.5 (1.1); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, c_multi_com_sobreposicao|closed_no, Qwen2-VL-2B, encoder congelado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+2.8 (2.5) / +3.6 (2.0); +1.2 (1.0) / +0.0 (2.2); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, a_uma_anatomia|closed_yes, Qwen2-VL-2B, encoder afinado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `-1.2 (0.7) / -0.8 (0.6); +0.2 (0.3) / +0.2 (0.3); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, a_uma_anatomia|closed_no, Qwen2-VL-2B, encoder afinado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+6.9 (2.4) / +5.3 (1.1); -1.1 (1.1) / -0.6 (0.9); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, b_multi_sem_sobreposicao|closed_yes, Qwen2-VL-2B, encoder afinado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `-1.1 (1.0) / -1.1 (1.0); -0.6 (0.4) / +0.0 (0.0); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, b_multi_sem_sobreposicao|closed_no, Qwen2-VL-2B, encoder afinado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+2.1 (2.0) / +2.0 (2.1); +0.0 (0.9) / +0.5 (0.8); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, c_multi_com_sobreposicao|closed_yes, Qwen2-VL-2B, encoder afinado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `-1.0 (1.4) / -1.2 (1.3); +0.2 (0.9) / +0.4 (0.8); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, c_multi_com_sobreposicao|closed_no, Qwen2-VL-2B, encoder afinado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+0.5 (0.6) / +0.3 (0.6); -0.3 (0.8) / +0.1 (0.5); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, a_uma_anatomia|closed_yes, SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+0.4 (1.0) / +0.8 (0.8); -0.0 (0.6) / -2.4 (0.7); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, a_uma_anatomia|closed_no, SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+4.6 (0.7) / +4.6 (0.6); +0.4 (0.5) / +0.7 (0.4); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, b_multi_sem_sobreposicao|closed_yes, SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `-1.7 (1.1) / -1.1 (1.0); -0.3 (0.9) / -1.7 (0.8); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, b_multi_sem_sobreposicao|closed_no, SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+2.5 (1.4) / +1.2 (1.2); -0.5 (1.4) / +1.0 (0.6); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, c_multi_com_sobreposicao|closed_yes, SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+2.3 (0.9) / +0.5 (1.0); -2.5 (1.0) / -0.7 (1.2); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, c_multi_com_sobreposicao|closed_no, SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+0.9 (1.5) / +2.1 (0.9); -0.2 (0.5) / -0.2 (0.8); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, a_uma_anatomia|closed_yes, SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `-2.0 (0.8) / -1.8 (0.9); -0.5 (0.9) / -1.1 (0.6); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, a_uma_anatomia|closed_no, SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+9.6 (1.5) / +8.7 (1.1); -1.2 (1.3) / -1.8 (1.3); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, b_multi_sem_sobreposicao|closed_yes, SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `-2.1 (1.5) / -2.0 (1.5); -0.1 (1.6) / +0.3 (0.4); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, b_multi_sem_sobreposicao|closed_no, SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+1.0 (1.5) / +1.0 (1.9); +0.7 (1.0) / +0.7 (2.3); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, c_multi_com_sobreposicao|closed_yes, SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `-2.8 (0.8) / -3.2 (1.3); +0.3 (1.0) / +1.9 (0.9); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **HEAL-MedVQA, c_multi_com_sobreposicao|closed_no, SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada preto / blur; Delta preto / blur (pp); criterio B** — `+4.2 (1.7) / +3.4 (1.1); -0.3 (1.8) / +0.1 (0.8); 0/6`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>

## S5. Medical-Diff-VQA

- **Medical-Diff-VQA, fechada-sim: n perguntas / imagens (alinhadas)** — `443 / 443`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `76.1 (0.8) / 68.0 (2.0) / 63.9 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+8.1 (1.8); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `+2.2 (1.0) / +1.8 (0.7) / +2.2 (1.2)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+1.9 (0.9) / 0.796 (0.020) / 3/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `80.6 (1.8) / 64.8 (3.0) / 63.9 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+15.8 (1.9); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `+2.8 (1.4) / +1.6 (1.0) / +2.1 (1.3)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+0.2 (0.7) / 0.694 (0.050) / 2/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `79.1 (2.5) / 68.0 (2.0) / 63.9 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+11.1 (3.6); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `+2.4 (2.3) / +2.6 (2.3) / +2.2 (1.6)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.1 (1.1) / 0.818 (0.045) / 3/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `76.1 (2.0) / 64.8 (3.0) / 63.9 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+11.3 (2.5); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `+2.6 (0.5) / +3.5 (0.8) / +3.5 (0.5)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.4 (0.6) / 0.823 (0.039) / 3/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE, encoder ajuste completo: Acc intacta / text-decoder-only / TF-IDF (%)** — `80.6 (5.0) / 62.2 (3.7) / 63.9 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE, encoder ajuste completo: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+18.4 (4.6); 3/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE, encoder ajuste completo: Delta preto / blur 10 % / cor media (pp)** — `+5.5 (1.1) / +2.6 (1.5) / +4.9 (0.8)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE, encoder ajuste completo: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+5.4 (3.9) / 0.726 (0.129) / 1/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim: faixa de Delta preto nas 27 linhas (pp)** — `+0.0 a +6.8`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim: faixa de Delta blur 10 % nas 27 linhas (pp)** — `-0.7 a +6.3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim: faixa de Delta cor media nas 27 linhas (pp)** — `+0.5 a +5.6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim: faixa de headroom nas 27 linhas (pp)** — `+6.1 a +21.2`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim: faixa de custo da mascara deslocada, preto nas 27 linhas (pp)** — `-1.4 a +7.7`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim: faixa da suficiencia (preto) nas 27 linhas** — `0.626 a 0.901`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao: n perguntas / imagens (alinhadas)** — `67 / 67`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `76.4 (4.4) / 80.6 (1.3) / 64.2 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `-4.2 (5.3); 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `+0.5 (2.4) / +0.2 (2.0) / +0.5 (1.2)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+0.0 (2.5) / 0.888 (0.048) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `80.6 (2.8) / 80.1 (0.8) / 64.2 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+0.5 (2.4); 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `-0.2 (1.7) / +0.5 (1.8) / +1.2 (1.1)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-2.0 (1.5) / 0.970 (0.070) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `73.9 (4.0) / 80.6 (1.3) / 64.2 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `-6.7 (3.2); 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `+0.2 (2.6) / +1.7 (3.2) / +0.0 (2.3)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.2 (1.1) / 0.943 (0.046) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `80.8 (1.1) / 80.1 (0.8) / 64.2 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+0.7 (0.8); 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `-0.2 (1.7) / -0.7 (0.8) / -0.7 (0.8)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-2.7 (1.7) / 0.969 (0.044) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, M3AE, encoder ajuste completo: Acc intacta / text-decoder-only / TF-IDF (%)** — `73.6 (7.5) / 79.6 (8.5) / 64.2 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, M3AE, encoder ajuste completo: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `-6.0 (5.4); 0/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, M3AE, encoder ajuste completo: Delta preto / blur 10 % / cor media (pp)** — `+1.5 (1.5) / +7.0 (4.8) / +2.5 (3.8)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, M3AE, encoder ajuste completo: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.5 (2.3) / 1.018 (0.088) / 0/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao: faixa de Delta preto nas 27 linhas (pp)** — `-4.5 a +4.5`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao: faixa de Delta blur 10 % nas 27 linhas (pp)** — `-3.0 a +10.4`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao: faixa de Delta cor media nas 27 linhas (pp)** — `-3.0 a +6.0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao: faixa de headroom nas 27 linhas (pp)** — `-11.9 a +3.0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao: faixa de custo da mascara deslocada, preto nas 27 linhas (pp)** — `-4.5 a +3.0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao: faixa da suficiencia (preto) nas 27 linhas** — `0.818 a 1.114`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato: n perguntas / imagens (alinhadas)** — `430 / 430`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `76.7 (0.9) / 68.2 (2.0) / 64.2 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, Qwen2-VL-2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+8.5 (1.8); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, Qwen2-VL-2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `+2.3 (1.1) / +1.8 (0.8) / +2.1 (1.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, Qwen2-VL-2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+1.6 (0.9) / 0.799 (0.020) / 3/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `81.8 (1.6) / 65.4 (2.8) / 64.2 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, SmolVLM2-2.2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+16.4 (1.6); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, SmolVLM2-2.2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `+2.8 (1.5) / +1.6 (1.0) / +2.0 (1.3)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.0 (0.5) / 0.694 (0.048) / 2/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `79.7 (2.6) / 68.2 (2.0) / 64.2 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, Qwen2-VL-2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+11.5 (3.6); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, Qwen2-VL-2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `+2.4 (2.4) / +2.5 (2.5) / +2.2 (1.8)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, Qwen2-VL-2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.2 (1.1) / 0.817 (0.044) / 3/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `77.5 (1.9) / 65.4 (2.8) / 64.2 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, SmolVLM2-2.2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+12.1 (2.7); 6/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, SmolVLM2-2.2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `+2.7 (0.6) / +3.6 (0.7) / +3.7 (0.6)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.6 (0.6) / 0.821 (0.038) / 3/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, M3AE, encoder ajuste completo: Acc intacta / text-decoder-only / TF-IDF (%)** — `81.6 (5.2) / 63.1 (3.7) / 64.2 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, M3AE, encoder ajuste completo: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+18.4 (4.3); 3/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, M3AE, encoder ajuste completo: Delta preto / blur 10 % / cor media (pp)** — `+5.7 (1.4) / +2.8 (1.2) / +5.0 (0.9)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato, M3AE, encoder ajuste completo: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+5.3 (3.8) / 0.720 (0.123) / 1/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato: faixa de Delta preto nas 27 linhas (pp)** — `+0.0 a +7.2`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato: faixa de Delta blur 10 % nas 27 linhas (pp)** — `-0.9 a +6.5`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato: faixa de Delta cor media nas 27 linhas (pp)** — `+0.2 a +5.8`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato: faixa de headroom nas 27 linhas (pp)** — `+6.3 a +21.2`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato: faixa de custo da mascara deslocada, preto nas 27 linhas (pp)** — `-1.4 a +7.7`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato: faixa da suficiencia (preto) nas 27 linhas** — `0.627 a 0.899`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas: n perguntas / imagens (alinhadas)** — `65 / 65`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `75.6 (4.5) / 80.0 (1.4) / 63.1 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, Qwen2-VL-2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `-4.4 (5.5); 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, Qwen2-VL-2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `+0.5 (2.5) / +0.3 (2.0) / +0.5 (1.3)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, Qwen2-VL-2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `+0.0 (2.6) / 0.883 (0.050) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `80.0 (2.9) / 79.5 (0.8) / 63.1 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, SmolVLM2-2.2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+0.5 (2.5); 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, SmolVLM2-2.2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `-0.3 (1.8) / +0.5 (1.9) / +1.3 (1.2)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, SmolVLM2-2.2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-2.1 (1.6) / 0.969 (0.073) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only / TF-IDF (%)** — `73.1 (4.1) / 80.0 (1.4) / 63.1 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, Qwen2-VL-2B, encoder afinado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `-6.9 (3.3); 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, Qwen2-VL-2B, encoder afinado: Delta preto / blur 10 % / cor media (pp)** — `+0.3 (2.6) / +1.8 (3.3) / +0.0 (2.4)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, Qwen2-VL-2B, encoder afinado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.3 (1.2) / 0.941 (0.048) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only / TF-IDF (%)** — `80.3 (1.2) / 79.5 (0.8) / 63.1 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, SmolVLM2-2.2B, encoder congelado: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `+0.8 (0.8); 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, SmolVLM2-2.2B, encoder congelado: Delta preto / blur 10 % / cor media (pp)** — `-0.3 (1.8) / -0.8 (0.8) / -0.8 (0.8)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, SmolVLM2-2.2B, encoder congelado: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-2.8 (1.8) / 0.968 (0.046) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, M3AE, encoder ajuste completo: Acc intacta / text-decoder-only / TF-IDF (%)** — `72.8 (7.7) / 79.5 (7.9) / 63.1 (0.0)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, M3AE, encoder ajuste completo: headroom sobre o text-decoder-only (pp); linhas resoluveis** — `-6.7 (5.4); 0/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, M3AE, encoder ajuste completo: Delta preto / blur 10 % / cor media (pp)** — `+1.5 (1.5) / +7.2 (4.9) / +2.6 (3.9)`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas, M3AE, encoder ajuste completo: custo da mascara deslocada, preto (pp) / suficiencia, preto / criterio B** — `-0.5 (2.4) / 1.019 (0.092) / 0/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas: faixa de Delta preto nas 27 linhas (pp)** — `-4.6 a +4.6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas: faixa de Delta blur 10 % nas 27 linhas (pp)** — `-3.1 a +10.8`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas: faixa de Delta cor media nas 27 linhas (pp)** — `-3.1 a +6.2`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas: faixa de headroom nas 27 linhas (pp)** — `-12.3 a +3.1`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas: faixa de custo da mascara deslocada, preto nas 27 linhas (pp)** — `-4.6 a +3.1`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-nao, so exatas: faixa da suficiencia (preto) nas 27 linhas** — `0.811 a 1.119`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim: n perguntas por linha (faixas abaixo)** — `443`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `73.1 – 86.2`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `58.0 – 69.3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `+6.1 – +21.2`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `-1.4 – +7.7`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-1.8 – +6.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `+0.0 – +6.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-0.7 – +6.3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `+0.5 – +5.6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.626 – 0.901`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não: n perguntas por linha (faixas abaixo)** — `67`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `65.7 – 83.6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `70.1 – 86.6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `-11.9 – +3.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `-4.5 – +3.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-4.5 – +3.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `-4.5 – +4.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-3.0 – +10.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `-3.0 – +6.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.818 – 1.114`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade pleural effusion: n perguntas por linha (faixas abaixo)** — `96`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade pleural effusion: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `64.6 – 87.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade pleural effusion: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `35.4 – 35.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade pleural effusion: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `+29.2 – +52.1`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade pleural effusion: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `-5.2 – +7.3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade pleural effusion: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-4.2 – +6.2`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade pleural effusion: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `-2.1 – +9.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade pleural effusion: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-2.1 – +6.2`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade pleural effusion: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `-1.0 – +10.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade pleural effusion: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.345 – 0.774`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade atelectasis: n perguntas por linha (faixas abaixo)** — `87`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade atelectasis: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `92.0 – 100.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade atelectasis: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `94.3 – 100.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade atelectasis: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `-4.6 – +2.3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade atelectasis: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `-1.1 – +11.5`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade atelectasis: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-2.3 – +10.3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade atelectasis: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `-2.3 – +4.6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade atelectasis: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-5.7 – +1.1`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade atelectasis: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `-4.6 – +2.3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade atelectasis: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.737 – 1.037`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade lung opacity: n perguntas por linha (faixas abaixo)** — `66`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade lung opacity: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `83.3 – 92.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade lung opacity: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `84.8 – 93.9`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade lung opacity: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `-7.6 – +6.1`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade lung opacity: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `-3.0 – +6.1`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade lung opacity: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-3.0 – +3.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade lung opacity: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `-4.5 – +6.1`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade lung opacity: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-1.5 – +6.1`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade lung opacity: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `-1.5 – +3.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade lung opacity: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.800 – 1.109`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade cardiomegaly: n perguntas por linha (faixas abaixo)** — `58`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade cardiomegaly: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `91.4 – 100.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade cardiomegaly: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `100.0 – 100.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade cardiomegaly: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `-8.6 – +0.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade cardiomegaly: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `-1.7 – +1.7`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade cardiomegaly: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-1.7 – +1.7`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade cardiomegaly: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `+0.0 – +13.8`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade cardiomegaly: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `+0.0 – +1.7`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade cardiomegaly: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `+0.0 – +5.2`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade cardiomegaly: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.603 – 1.094`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade edema: n perguntas por linha (faixas abaixo)** — `45`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade edema: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `57.8 – 91.1`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade edema: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `13.3 – 100.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade edema: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `-35.6 – +66.7`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade edema: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `-8.9 – +13.3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade edema: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-8.9 – +11.1`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade edema: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `+0.0 – +33.3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade edema: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-2.2 – +28.9`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade edema: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `+0.0 – +28.9`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade edema: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.179 – 1.079`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade vascular congestion: n perguntas por linha (faixas abaixo)** — `23`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade vascular congestion: acurácia intacta, mínimo – máximo entre as 27 linhas (%)** — `17.4 – 91.3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade vascular congestion: text-only arm, mínimo – máximo entre as 27 linhas (%)** — `13.0 – 13.0`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade vascular congestion: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp)** — `+4.3 – +78.3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade vascular congestion: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp)** — `-8.7 – +30.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade vascular congestion: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-13.0 – +21.7`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade vascular congestion: Δ preto, mínimo – máximo entre as 27 linhas (pp)** — `-17.4 – +21.7`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade vascular congestion: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp)** — `-13.0 – +30.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade vascular congestion: Δ cor média, mínimo – máximo entre as 27 linhas (pp)** — `-8.7 – +30.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, entidade vascular congestion: suficiência (preto), mínimo – máximo entre as 27 linhas (razão)** — `0.188 – 1.571`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim: image gain against the question-only classifier (TF-IDF), mínimo – máximo entre as 27 linhas (pp)** — `+9.3 – +22.3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder congelado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+12.3 (0.8) / +8.1 (1.8); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+16.7 (1.8) / +15.8 (1.9); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder afinado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+15.2 (2.5) / +11.1 (3.6); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+12.2 (2.0) / +11.3 (2.5); 6/6 / 6/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE, encoder ajuste completo: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 3 linhas (pp); linhas com IC > 0** — `+16.7 (5.0) / +18.4 (4.6); 3/3 / 3/3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, QWEN2VL_LORA_FROZEN_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+13.3 [+9.6, +17.1] / +7.9 [+4.2, +11.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, SMOLVLM_LORA_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+16.5 [+12.6, +20.7] / +17.8 [+14.0, +21.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, QWEN2VL_LORA_VT_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+16.3 [+12.6, +20.1] / +10.8 [+7.4, +14.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, SMOLVLM_LORA_FT_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+10.4 [+7.1, +13.8] / +11.7 [+8.7, +15.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, QWEN2VL_DORA_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.5 [+8.0, +15.3] / +6.1 [+2.4, +9.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, SMOLVLM_DORA_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+16.7 [+12.5, +20.8] / +18.1 [+14.2, +22.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, QWEN2VL_DORA_VT_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.5 [+8.0, +14.9] / +6.1 [+2.5, +9.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, SMOLVLM_DORA_FT_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+9.3 [+5.9, +12.7] / +10.6 [+7.4, +13.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+22.3 [+17.8, +26.9] / +21.2 [+16.8, +25.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, QWEN2VL_LORA_FROZEN_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.7 [+8.4, +15.4] / +6.3 [+2.7, +9.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, SMOLVLM_LORA_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+15.1 [+11.4, +19.1] / +15.8 [+12.0, +19.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, QWEN2VL_LORA_VT_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+14.7 [+11.0, +18.4] / +9.3 [+5.8, +12.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, SMOLVLM_LORA_FT_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+14.0 [+10.3, +17.5] / +14.7 [+11.1, +18.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, QWEN2VL_DORA_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+13.3 [+9.7, +17.0] / +7.9 [+4.2, +11.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, SMOLVLM_DORA_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+14.4 [+10.6, +18.3] / +15.1 [+11.2, +18.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, QWEN2VL_DORA_VT_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+16.7 [+12.8, +20.6] / +11.3 [+7.6, +15.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, SMOLVLM_DORA_FT_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.9 [+9.2, +16.6] / +13.5 [+9.8, +17.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+14.9 [+10.9, +19.0] / +20.8 [+16.5, +25.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, QWEN2VL_LORA_FROZEN_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.7 [+8.2, +15.4] / +10.2 [+6.8, +13.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, SMOLVLM_LORA_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+18.1 [+13.9, +22.2] / +13.3 [+9.6, +17.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, QWEN2VL_LORA_VT_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+18.5 [+14.7, +22.5] / +16.9 [+13.1, +20.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, SMOLVLM_LORA_FT_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+14.0 [+10.2, +17.8] / +9.3 [+5.8, +12.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, QWEN2VL_DORA_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.0 [+8.4, +15.6] / +10.4 [+7.1, +13.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, SMOLVLM_DORA_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.4 [+15.4, +23.5] / +14.7 [+10.8, +18.7]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, QWEN2VL_DORA_VT_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+13.5 [+10.1, +17.0] / +12.0 [+8.7, +15.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, SMOLVLM_DORA_FT_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.9 [+9.1, +16.7] / +8.1 [+4.9, +11.5]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+12.9 [+8.5, +17.5] / +13.1 [+8.7, +17.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não: image gain against the question-only classifier (TF-IDF), mínimo – máximo entre as 27 linhas (pp)** — `+1.5 – +19.4`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, Qwen2-VL-2B, encoder congelado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+12.2 (4.4) / -4.2 (5.3); 3/6 / 0/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, SmolVLM2-2.2B, encoder afinado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+16.4 (2.8) / +0.5 (2.4); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, Qwen2-VL-2B, encoder afinado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+9.7 (4.0) / -6.7 (3.2); 3/6 / 0/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, SmolVLM2-2.2B, encoder congelado: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 6 linhas (pp); linhas com IC > 0** — `+16.7 (1.1) / +0.7 (0.8); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, M3AE, encoder ajuste completo: image gain against the question-only classifier (TF-IDF) / image gain above the text-only arm, média (DP) entre as 3 linhas (pp); linhas com IC > 0** — `+9.5 (7.5) / -6.0 (5.4); 1/3 / 0/3`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, QWEN2VL_LORA_FROZEN_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+10.4 [+0.0, +21.0] / -7.5 [-14.3, -1.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, SMOLVLM_LORA_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.4 [+9.6, +30.0] / +3.0 [+0.0, +7.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, QWEN2VL_LORA_VT_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+14.9 [+4.8, +25.5] / -3.0 [-7.6, +0.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, SMOLVLM_LORA_FT_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+17.9 [+7.9, +28.1] / +1.5 [-3.2, +6.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, QWEN2VL_DORA_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.9 [+1.7, +22.7] / -6.0 [-12.0, -1.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, SMOLVLM_DORA_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+19.4 [+9.6, +30.0] / +3.0 [+0.0, +7.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, QWEN2VL_DORA_VT_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.9 [+1.6, +23.0] / -6.0 [-11.9, -1.4]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, SMOLVLM_DORA_FT_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+16.4 [+6.8, +26.4] / +0.0 [-5.4, +5.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, M3AE_MIMIC_seed0: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+1.5 [-7.6, +10.3] / -4.5 [-12.7, +3.2]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, QWEN2VL_LORA_FROZEN_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+16.4 [+6.6, +26.5] / +1.5 [-3.3, +6.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, SMOLVLM_LORA_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+14.9 [+5.5, +24.6] / -1.5 [-6.8, +3.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, QWEN2VL_LORA_VT_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+9.0 [+0.0, +18.8] / -6.0 [-14.3, +1.8]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, SMOLVLM_LORA_FT_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+17.9 [+8.0, +27.9] / +1.5 [-5.1, +8.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, QWEN2VL_DORA_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+17.9 [+8.1, +27.9] / +3.0 [-2.9, +9.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, SMOLVLM_DORA_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+16.4 [+5.8, +27.1] / +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, QWEN2VL_DORA_VT_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+6.0 [-2.7, +14.7] / -9.0 [-16.9, -1.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, SMOLVLM_DORA_FT_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+16.4 [+6.8, +26.6] / +0.0 [-6.1, +5.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, M3AE_MIMIC_seed1: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+10.4 [+0.0, +21.9] / -11.9 [-23.2, -1.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, QWEN2VL_LORA_FROZEN_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+6.0 [-1.6, +14.1] / -10.4 [-18.0, -3.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, SMOLVLM_LORA_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.9 [+3.3, +21.0] / -3.0 [-10.3, +3.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, QWEN2VL_LORA_VT_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+4.5 [-6.4, +15.5] / -11.9 [-21.1, -3.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, SMOLVLM_LORA_FT_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+14.9 [+4.2, +26.3] / +0.0 [-7.6, +7.1]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, QWEN2VL_DORA_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+10.4 [+0.0, +21.0] / -6.0 [-12.3, -1.3]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, SMOLVLM_DORA_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+16.4 [+6.9, +26.3] / +1.5 [-4.8, +8.0]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, QWEN2VL_DORA_VT_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+11.9 [+1.5, +22.7] / -4.5 [-10.9, +1.6]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, SMOLVLM_DORA_FT_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+16.4 [+6.2, +26.8] / +1.5 [-4.8, +7.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-não, M3AE_MIMIC_seed2: image gain against the question-only classifier (TF-IDF) [IC] / image gain above the text-only arm [IC] (pp)** — `+16.4 [+4.3, +28.8] / -1.5 [-9.2, +5.9]`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **Medical-Diff-VQA, fechada-sim, pleural effusion: n itens / imagens; criterio B (linhas)** — `96 / 96; 0/27`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `73.6 (1.9) / 35.4 (0.0) / +38.2 (1.9) / +2.1 (1.9) / +0.2 (2.0) / +1.6 (2.4) / 0.505 (0.023) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `83.7 (2.7) / 35.4 (0.0) / +48.3 (2.7) / +3.0 (1.4) / +2.4 (1.7) / -1.2 (1.8) / 0.503 (0.042) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `73.1 (3.4) / 35.4 (0.0) / +37.7 (3.4) / +2.4 (2.4) / +2.4 (1.9) / -1.2 (1.8) / 0.533 (0.055) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `72.6 (5.5) / 35.4 (0.0) / +37.2 (5.5) / +0.0 (1.5) / +2.6 (1.6) / -2.8 (1.7) / 0.681 (0.062) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, M3AE, encoder ajuste completo: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `82.6 (4.3) / 35.4 (0.0) / +47.2 (4.3) / +5.9 (4.3) / +5.6 (0.6) / +5.6 (2.2) / 0.427 (0.071) / 0/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, atelectasis: n itens / imagens; criterio B (linhas)** — `87 / 87; 0/27`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `98.1 (1.6) / 98.5 (0.6) / -0.4 (1.2) / -0.6 (0.6) / -0.6 (1.2) / -0.2 (0.9) / 1.002 (0.020) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `95.2 (1.3) / 96.9 (1.2) / -1.7 (1.9) / -0.6 (1.2) / +0.0 (1.3) / +0.4 (0.6) / 0.940 (0.026) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `99.2 (0.6) / 98.5 (0.6) / +0.8 (0.9) / +0.0 (0.0) / -0.2 (0.5) / -0.2 (0.5) / 1.002 (0.005) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `95.2 (1.8) / 96.9 (1.2) / -1.7 (1.0) / +0.8 (0.9) / +0.2 (0.5) / +0.0 (0.0) / 0.954 (0.022) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, M3AE, encoder ajuste completo: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `94.3 (2.3) / 96.9 (2.9) / -2.7 (2.4) / +1.5 (2.9) / -3.8 (2.4) / +6.9 (6.1) / 0.869 (0.153) / 0/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, lung opacity: n itens / imagens; criterio B (linhas)** — `66 / 66; 0/27`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `88.4 (2.5) / 88.4 (2.1) / +0.0 (2.5) / +0.5 (0.8) / +0.3 (1.1) / +0.3 (1.8) / 0.980 (0.042) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `87.4 (1.8) / 85.4 (0.8) / +2.0 (2.3) / +0.0 (1.4) / -0.3 (1.1) / +1.5 (1.0) / 0.877 (0.060) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `88.1 (2.6) / 88.4 (2.1) / -0.3 (3.2) / -0.3 (1.8) / +0.0 (1.0) / +0.8 (2.1) / 1.017 (0.035) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `86.9 (1.2) / 85.4 (0.8) / +1.5 (1.4) / +0.0 (1.0) / +0.3 (1.1) / +0.3 (1.8) / 0.930 (0.027) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, M3AE, encoder ajuste completo: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `85.4 (1.7) / 90.9 (3.0) / -5.6 (3.5) / +2.5 (6.1) / +2.5 (3.8) / +2.5 (4.9) / 1.001 (0.128) / 0/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, cardiomegaly: n itens / imagens; criterio B (linhas)** — `58 / 58; 0/27`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `100.0 (0.0) / 100.0 (0.0) / +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0) / 0.991 (0.014) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `100.0 (0.0) / 100.0 (0.0) / +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0) / 0.739 (0.111) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `100.0 (0.0) / 100.0 (0.0) / +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0) / 1.000 (0.000) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `100.0 (0.0) / 100.0 (0.0) / +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0) / 0.897 (0.044) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, M3AE, encoder ajuste completo: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `96.6 (4.6) / 100.0 (0.0) / -3.4 (4.6) / +7.5 (6.1) / +1.7 (0.0) / +0.0 (1.7) / 0.915 (0.171) / 0/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, edema: n itens / imagens; criterio B (linhas)** — `45 / 45; 9/27`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `63.7 (5.2) / 85.2 (23.0) / -21.5 (18.5) / +11.5 (5.0) / +10.7 (3.3) / +5.2 (6.7) / 0.243 (0.061) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `83.7 (2.7) / 70.4 (23.0) / +13.3 (21.6) / +13.7 (4.7) / +5.9 (6.5) / -0.4 (2.6) / 0.301 (0.102) / 2/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `79.6 (7.1) / 85.2 (23.0) / -5.6 (25.1) / +10.7 (12.5) / +12.2 (11.0) / -0.7 (5.0) / 0.407 (0.347) / 2/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `81.1 (4.2) / 70.4 (23.0) / +10.7 (20.6) / +19.3 (6.1) / +21.9 (2.6) / -3.0 (2.3) / 0.479 (0.041) / 3/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, M3AE, encoder ajuste completo: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `78.5 (13.4) / 41.5 (24.4) / +37.0 (28.9) / +12.6 (6.8) / +10.4 (2.6) / +8.1 (3.4) / 0.289 (0.092) / 2/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, fechada-sim, vascular congestion: n itens / imagens; criterio B (linhas)** — `23 / 23; 1/27`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, vascular congestion, Qwen2-VL-2B, encoder congelado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `35.5 (15.9) / 13.0 (0.0) / +22.5 (15.9) / +10.1 (5.9) / +7.2 (3.5) / +6.5 (12.5) / 0.624 (0.168) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, vascular congestion, SmolVLM2-2.2B, encoder afinado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `47.8 (20.0) / 13.0 (0.0) / +34.8 (20.0) / +0.7 (11.5) / +2.9 (10.5) / +7.2 (5.9) / 0.449 (0.278) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, vascular congestion, Qwen2-VL-2B, encoder afinado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `49.3 (16.4) / 13.0 (0.0) / +36.2 (16.4) / +8.0 (7.5) / +10.9 (14.7) / +5.1 (8.4) / 0.381 (0.180) / 1/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, vascular congestion, SmolVLM2-2.2B, encoder congelado: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `42.8 (11.5) / 13.0 (0.0) / +29.7 (11.5) / +11.6 (3.5) / +9.4 (7.5) / +3.6 (3.3) / 0.954 (0.351) / 0/6`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, vascular congestion, M3AE, encoder ajuste completo: Acc intacta / text-decoder-only (%) / headroom (pp) / Delta preto / blur 10 % (pp) / custo desloc. (pp) / suficiencia / B** — `65.2 (26.1) / 13.0 (0.0) / +52.2 (26.1) / +5.8 (9.1) / +8.7 (13.0) / +14.5 (10.0) / 0.749 (0.434) / 0/3`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, QWEN2VL_LORA_FROZEN_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 64.4; -35.6 [-50.0, -21.6]; +2.2 [-9.1, +14.0]; +13.3 [+0.0, +27.6]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, SMOLVLM_LORA_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `55.6 / 86.7; +31.1 [+15.6, +46.7]; +15.6 [+5.6, +26.8]; +4.4 [-4.0, +14.3]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, QWEN2VL_LORA_VT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 80.0; -20.0 [-32.0, -8.7]; +6.7 [+0.0, +14.8]; +6.7 [+0.0, +14.6]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, SMOLVLM_LORA_FT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `55.6 / 80.0; +24.4 [+10.4, +39.1]; +15.6 [+0.0, +32.3]; +22.2 [+8.6, +36.7]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, QWEN2VL_DORA_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 66.7; -33.3 [-47.5, -19.5]; +13.3 [+0.0, +27.9]; +13.3 [-2.8, +29.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, SMOLVLM_DORA_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `55.6 / 80.0; +24.4 [+7.1, +41.7]; +8.9 [+1.9, +18.2]; +0.0 [-6.1, +6.4]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, QWEN2VL_DORA_VT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 66.7; -33.3 [-48.2, -20.0]; +15.6 [+5.4, +26.7]; +20.0 [+9.1, +32.4]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, SMOLVLM_DORA_FT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `55.6 / 73.3; +17.8 [+2.6, +33.3]; +17.8 [+2.4, +33.3]; +20.0 [+4.4, +35.7]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, M3AE_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `55.6 / 91.1; +35.6 [+19.3, +51.4]; +11.1 [+2.4, +21.1]; +8.9 [+2.0, +17.7]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, QWEN2VL_LORA_FROZEN_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 64.4; -35.6 [-50.0, -21.2]; +11.1 [-0.0, +23.8]; +6.7 [-5.7, +19.5]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, SMOLVLM_LORA_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `55.6 / 82.2; +26.7 [+9.3, +44.2]; +17.8 [+7.0, +30.0]; +8.9 [+2.0, +18.9]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, QWEN2VL_LORA_VT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 82.2; -17.8 [-29.4, -7.3]; +33.3 [+20.0, +47.9]; +28.9 [+16.3, +42.9]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, SMOLVLM_LORA_FT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `55.6 / 82.2; +26.7 [+11.3, +42.1]; +31.1 [+15.4, +46.2]; +24.4 [+9.1, +39.5]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, QWEN2VL_DORA_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 71.1; -28.9 [-42.3, -15.8]; +15.6 [+3.2, +28.2]; +11.1 [+0.0, +23.1]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, SMOLVLM_DORA_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `55.6 / 82.2; +26.7 [+10.9, +41.7]; +8.9 [-2.9, +20.9]; -2.2 [-12.5, +7.9]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, QWEN2VL_DORA_VT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 86.7; -13.3 [-23.8, -4.4]; +8.9 [+0.0, +20.0]; +13.3 [+4.4, +24.1]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, SMOLVLM_DORA_FT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `55.6 / 82.2; +26.7 [+11.3, +42.1]; +15.6 [+0.0, +31.1]; +24.4 [+10.2, +38.5]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, M3AE_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `13.3 / 80.0; +66.7 [+53.2, +80.0]; +20.0 [+7.5, +33.3]; +13.3 [+2.2, +25.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, QWEN2VL_LORA_FROZEN_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `55.6 / 57.8; +2.2 [-14.3, +20.0]; +15.6 [+2.1, +29.8]; +13.3 [+0.0, +27.3]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, SMOLVLM_LORA_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 84.4; -15.6 [-27.1, -6.5]; +11.1 [-2.0, +24.4]; +8.9 [+2.0, +17.9]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, QWEN2VL_LORA_VT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `55.6 / 84.4; +28.9 [+12.8, +44.9]; +0.0 [-6.1, +6.1]; +6.7 [+0.0, +15.4]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, SMOLVLM_LORA_FT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 84.4; -15.6 [-27.0, -5.7]; +20.0 [+4.9, +35.6]; +17.8 [+2.1, +33.3]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, QWEN2VL_DORA_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `55.6 / 57.8; +2.2 [-14.3, +20.0]; +11.1 [+0.0, +23.2]; +6.7 [-8.1, +22.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, SMOLVLM_DORA_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 86.7; -13.3 [-24.4, -4.1]; +20.0 [+6.7, +33.3]; +15.6 [+4.0, +28.2]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, QWEN2VL_DORA_VT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `55.6 / 77.8; +22.2 [+6.4, +37.1]; +0.0 [-6.1, +6.3]; -2.2 [-7.8, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, SMOLVLM_DORA_FT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 84.4; -15.6 [-27.0, -5.7]; +15.6 [+0.0, +31.4]; +22.2 [+6.7, +37.5]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, edema, M3AE_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `55.6 / 64.4; +8.9 [-10.4, +27.1]; +6.7 [-5.1, +18.2]; +8.9 [+2.0, +17.6]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, QWEN2VL_LORA_FROZEN_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 75.0; +39.6 [+29.3, +49.5]; -1.0 [-4.8, +2.4]; -1.0 [-3.4, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, SMOLVLM_LORA_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 80.2; +44.8 [+34.4, +54.9]; +3.1 [-1.1, +8.1]; +1.0 [-3.6, +5.8]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, QWEN2VL_LORA_VT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 75.0; +39.6 [+29.8, +49.5]; +0.0 [+0.0, +0.0]; +1.0 [+0.0, +3.5]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, SMOLVLM_LORA_FT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 67.7; +32.3 [+23.1, +42.2]; +1.0 [-5.7, +7.9]; +3.1 [-1.2, +8.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, QWEN2VL_DORA_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 69.8; +34.4 [+25.0, +44.6]; +3.1 [-1.1, +8.2]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, SMOLVLM_DORA_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 84.4; +49.0 [+38.5, +59.4]; +3.1 [-1.1, +7.9]; +5.2 [+1.1, +10.1]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, QWEN2VL_DORA_VT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 68.8; +33.3 [+24.0, +43.3]; +1.0 [-2.3, +4.6]; +2.1 [-2.0, +5.9]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, SMOLVLM_DORA_FT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 64.6; +29.2 [+20.2, +38.1]; +0.0 [-7.1, +7.1]; +1.0 [-4.5, +6.7]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, M3AE_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 87.5; +52.1 [+41.8, +62.6]; +9.4 [+3.0, +16.3]; +5.2 [-1.2, +12.2]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, QWEN2VL_LORA_FROZEN_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 75.0; +39.6 [+30.1, +49.5]; +3.1 [-1.1, +7.9]; -2.1 [-6.0, +2.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, SMOLVLM_LORA_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 81.2; +45.8 [+35.2, +55.8]; +2.1 [-2.8, +7.1]; +3.1 [-2.2, +8.8]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, QWEN2VL_LORA_VT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 72.9; +37.5 [+27.8, +47.6]; +5.2 [+1.1, +10.1]; +5.2 [-1.1, +12.4]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, SMOLVLM_LORA_FT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 78.1; +42.7 [+32.7, +52.9]; -1.0 [-6.7, +4.5]; +1.0 [-3.4, +5.8]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, QWEN2VL_DORA_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 74.0; +38.5 [+28.9, +48.5]; +4.2 [+0.0, +9.5]; +3.1 [+0.0, +7.1]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, SMOLVLM_DORA_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 83.3; +47.9 [+37.6, +58.5]; +3.1 [-2.3, +8.8]; +3.1 [-1.1, +7.8]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, QWEN2VL_DORA_VT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 78.1; +42.7 [+32.9, +53.0]; +3.1 [+0.0, +7.2]; +2.1 [-1.9, +6.3]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, SMOLVLM_DORA_FT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 77.1; +41.7 [+31.4, +52.1]; +2.1 [-2.0, +6.4]; +3.1 [-2.2, +8.3]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, M3AE_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 81.2; +45.8 [+35.2, +55.8]; +1.0 [-6.4, +8.5]; +6.2 [+0.9, +12.2]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, QWEN2VL_LORA_FROZEN_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 74.0; +38.5 [+28.7, +48.5]; +1.0 [-2.3, +4.9]; +2.1 [+0.0, +5.6]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, SMOLVLM_LORA_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 85.4; +50.0 [+39.6, +60.2]; +1.0 [-3.4, +5.7]; +1.0 [-3.5, +5.9]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, QWEN2VL_LORA_VT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 74.0; +38.5 [+29.0, +48.6]; +5.2 [+0.0, +11.0]; +4.2 [+0.9, +8.7]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, SMOLVLM_LORA_FT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 76.0; +40.6 [+30.5, +51.0]; +0.0 [-6.5, +6.1]; +5.2 [-1.0, +11.4]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, QWEN2VL_DORA_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 74.0; +38.5 [+29.1, +48.2]; +2.1 [-1.9, +6.3]; -1.0 [-4.5, +2.3]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, SMOLVLM_DORA_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 87.5; +52.1 [+41.8, +62.5]; +5.2 [+0.0, +10.5]; +1.0 [-4.3, +6.8]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, QWEN2VL_DORA_VT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 69.8; +34.4 [+25.0, +44.6]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, SMOLVLM_DORA_FT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 71.9; +36.5 [+26.6, +46.1]; -2.1 [-8.0, +3.5]; +2.1 [-4.0, +8.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, pleural effusion, M3AE_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `35.4 / 79.2; +43.8 [+33.7, +53.6]; +7.3 [+0.0, +14.7]; +5.2 [-1.1, +12.4]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, QWEN2VL_LORA_FROZEN_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `97.7 / 97.7; +0.0 [-3.4, +3.2]; -1.1 [-4.0, +0.0]; -2.3 [-5.9, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, SMOLVLM_LORA_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `97.7 / 93.1; -4.6 [-9.4, -1.1]; -2.3 [-6.3, +0.0]; -2.3 [-6.3, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, QWEN2VL_LORA_VT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `97.7 / 100.0; +2.3 [+0.0, +5.7]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, SMOLVLM_LORA_FT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `97.7 / 97.7; +0.0 [+0.0, +0.0]; +2.3 [+0.0, +5.9]; +1.1 [+0.0, +3.8]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, QWEN2VL_DORA_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `97.7 / 95.4; -2.3 [-6.0, +0.0]; -1.1 [-4.0, +0.0]; -1.1 [-4.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, SMOLVLM_DORA_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `97.7 / 94.3; -3.4 [-7.8, +0.0]; +0.0 [+0.0, +0.0]; +1.1 [+0.0, +3.8]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, QWEN2VL_DORA_VT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `97.7 / 98.9; +1.1 [+0.0, +3.8]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, SMOLVLM_DORA_FT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `97.7 / 95.4; -2.3 [-5.9, +0.0]; +1.1 [+0.0, +3.6]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, M3AE_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 96.6; -3.4 [-7.7, +0.0]; +1.1 [-5.1, +6.8]; -5.7 [-12.9, +1.1]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, QWEN2VL_LORA_FROZEN_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `98.9 / 97.7; -1.1 [-3.8, +0.0]; +0.0 [-3.3, +3.2]; +1.1 [+0.0, +3.8]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, SMOLVLM_LORA_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `97.7 / 96.6; -1.1 [-3.8, +0.0]; -1.1 [-3.8, +0.0]; +0.0 [-3.4, +3.2]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, QWEN2VL_LORA_VT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `98.9 / 98.9; +0.0 [-3.3, +3.2]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, SMOLVLM_LORA_FT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `97.7 / 96.6; -1.1 [-4.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, QWEN2VL_DORA_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `98.9 / 98.9; +0.0 [-3.3, +3.2]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, SMOLVLM_DORA_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `97.7 / 96.6; -1.1 [-4.0, +0.0]; +1.1 [+0.0, +4.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, QWEN2VL_DORA_VT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `98.9 / 98.9; +0.0 [-3.3, +3.2]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, SMOLVLM_DORA_FT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `97.7 / 95.4; -2.3 [-5.8, +0.0]; +1.1 [+0.0, +3.8]; +0.0 [-3.4, +3.4]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, M3AE_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `96.6 / 92.0; -4.6 [-11.1, +1.3]; +4.6 [-1.3, +10.9]; -4.6 [-12.5, +2.4]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, QWEN2VL_LORA_FROZEN_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `98.9 / 100.0; +1.1 [+0.0, +3.8]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, SMOLVLM_LORA_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `95.4 / 95.4; +0.0 [-4.4, +4.3]; -1.1 [-4.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, QWEN2VL_LORA_VT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `98.9 / 100.0; +1.1 [+0.0, +3.8]; +0.0 [+0.0, +0.0]; -1.1 [-4.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, SMOLVLM_LORA_FT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `95.4 / 93.1; -2.3 [-6.3, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, QWEN2VL_DORA_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `98.9 / 98.9; +0.0 [-3.2, +3.3]; -1.1 [-3.8, +0.0]; -1.1 [-3.8, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, SMOLVLM_DORA_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `95.4 / 95.4; +0.0 [-4.4, +4.3]; +0.0 [+0.0, +0.0]; +1.1 [+0.0, +3.8]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, QWEN2VL_DORA_VT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `98.9 / 98.9; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, SMOLVLM_DORA_FT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `95.4 / 93.1; -2.3 [-6.3, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, atelectasis, M3AE_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `94.3 / 94.3; +0.0 [-4.7, +4.7]; -1.1 [-5.1, +2.5]; -1.1 [-5.2, +2.5]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, QWEN2VL_LORA_FROZEN_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `86.4 / 90.9; +4.5 [-1.6, +11.7]; +1.5 [+0.0, +5.0]; +1.5 [+0.0, +5.1]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, SMOLVLM_LORA_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `86.4 / 86.4; +0.0 [-4.4, +4.2]; +0.0 [+0.0, +0.0]; -1.5 [-5.3, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, QWEN2VL_LORA_VT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `86.4 / 92.4; +6.1 [+1.3, +12.3]; -3.0 [-7.4, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, SMOLVLM_LORA_FT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `86.4 / 87.9; +1.5 [-3.4, +7.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, QWEN2VL_DORA_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `86.4 / 86.4; +0.0 [-6.0, +6.1]; +1.5 [+0.0, +5.2]; +1.5 [+0.0, +5.2]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, SMOLVLM_DORA_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `86.4 / 86.4; +0.0 [-4.4, +4.2]; -1.5 [-5.1, +0.0]; -1.5 [-5.1, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, QWEN2VL_DORA_VT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `86.4 / 84.8; -1.5 [-5.3, +0.0]; +1.5 [+0.0, +5.2]; -1.5 [-5.2, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, SMOLVLM_DORA_FT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `86.4 / 86.4; +0.0 [-4.6, +4.6]; -1.5 [-5.2, +0.0]; -1.5 [-5.1, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, M3AE_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `93.9 / 86.4; -7.6 [-16.5, +0.0]; -4.5 [-12.8, +3.0]; -1.5 [-9.7, +6.5]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, QWEN2VL_LORA_FROZEN_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `87.9 / 87.9; +0.0 [-4.5, +4.3]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, SMOLVLM_LORA_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `84.8 / 90.9; +6.1 [+1.3, +12.7]; +0.0 [-4.1, +4.5]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, QWEN2VL_LORA_VT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `87.9 / 86.4; -1.5 [-7.1, +3.4]; +0.0 [-4.3, +4.5]; +1.5 [+0.0, +5.2]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, SMOLVLM_LORA_FT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `84.8 / 87.9; +3.0 [+0.0, +8.1]; +0.0 [+0.0, +0.0]; +1.5 [+0.0, +5.3]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, QWEN2VL_DORA_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `87.9 / 84.8; -3.0 [-7.6, +0.0]; +0.0 [+0.0, +0.0]; -1.5 [-5.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, SMOLVLM_DORA_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `84.8 / 86.4; +1.5 [-3.6, +7.1]; +1.5 [+0.0, +5.3]; +0.0 [-4.6, +4.5]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, QWEN2VL_DORA_VT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `87.9 / 87.9; +0.0 [-4.4, +4.2]; +1.5 [+0.0, +5.2]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, SMOLVLM_DORA_FT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `84.8 / 84.8; +0.0 [-6.1, +6.1]; +0.0 [+0.0, +0.0]; +1.5 [+0.0, +5.3]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, M3AE_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `87.9 / 86.4; -1.5 [-9.1, +6.3]; +6.1 [-3.0, +15.6]; +6.1 [+0.0, +13.8]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, QWEN2VL_LORA_FROZEN_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `90.9 / 90.9; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, SMOLVLM_LORA_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `84.8 / 86.4; +1.5 [+0.0, +5.2]; -1.5 [-5.2, +0.0]; +1.5 [+0.0, +5.3]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, QWEN2VL_LORA_VT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `90.9 / 89.4; -1.5 [-6.7, +3.5]; -1.5 [-5.3, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, SMOLVLM_LORA_FT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `84.8 / 87.9; +3.0 [+0.0, +8.1]; +1.5 [+0.0, +4.8]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, QWEN2VL_DORA_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `90.9 / 89.4; -1.5 [-6.8, +3.4]; +0.0 [-4.6, +4.4]; +0.0 [-4.5, +4.4]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, SMOLVLM_DORA_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `84.8 / 87.9; +3.0 [+0.0, +8.1]; +1.5 [+0.0, +5.3]; +0.0 [-4.3, +4.4]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, QWEN2VL_DORA_VT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `90.9 / 87.9; -3.0 [-7.9, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, SMOLVLM_DORA_FT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `84.8 / 86.4; +1.5 [+0.0, +5.3]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, lung opacity, M3AE_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `90.9 / 83.3; -7.6 [-14.6, -1.6]; +6.1 [+0.0, +13.6]; +3.0 [-4.3, +10.7]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, QWEN2VL_LORA_FROZEN_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, SMOLVLM_LORA_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, QWEN2VL_LORA_VT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, SMOLVLM_LORA_FT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, QWEN2VL_DORA_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, SMOLVLM_DORA_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, QWEN2VL_DORA_VT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, SMOLVLM_DORA_FT_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, M3AE_MIMIC_seed0: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +6.9 [+1.4, +14.3]; +1.7 [+0.0, +5.7]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, QWEN2VL_LORA_FROZEN_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, SMOLVLM_LORA_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, QWEN2VL_LORA_VT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, SMOLVLM_LORA_FT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, QWEN2VL_DORA_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, SMOLVLM_DORA_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, QWEN2VL_DORA_VT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, SMOLVLM_DORA_FT_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, M3AE_MIMIC_seed1: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 98.3; -1.7 [-5.9, +0.0]; +13.8 [+3.8, +24.6]; +1.7 [-4.0, +7.8]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, QWEN2VL_LORA_FROZEN_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, SMOLVLM_LORA_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, QWEN2VL_LORA_VT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, SMOLVLM_LORA_FT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, QWEN2VL_DORA_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, SMOLVLM_DORA_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, QWEN2VL_DORA_VT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, SMOLVLM_DORA_FT_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 100.0; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **Medical-Diff-VQA, cardiomegaly, M3AE_MIMIC_seed2: text-only arm / intacta (%); headroom [IC]; Delta preto [IC]; Delta blur 10 % [IC] (pp)** — `100.0 / 91.4; -8.6 [-16.7, -2.0]; +1.7 [-4.3, +8.5]; +1.7 [-3.7, +7.9]`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>

## S6. Oclusor em imagens sem o achado (taxa de afirmativa induzida)

- **Kvasir-VQA-x1, SHAM_ART_black, Qwen2-VL-2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+81.7 (9.9); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_ART_blur10, Qwen2-VL-2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+59.2 (9.4); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_INS_black, Qwen2-VL-2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+13.0 (1.5); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_INS_blur10, Qwen2-VL-2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+3.9 (0.5); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q1_black, Qwen2-VL-2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+1.7 (0.5); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q1_blur10, Qwen2-VL-2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+0.4 (0.7); 1/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q3_black, Qwen2-VL-2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+15.7 (3.7); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q3_blur10, Qwen2-VL-2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+6.0 (1.4); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_ART_black, SmolVLM2-2.2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+69.4 (18.4); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_ART_blur10, SmolVLM2-2.2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+37.3 (11.2); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_INS_black, SmolVLM2-2.2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+3.8 (1.0); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_INS_blur10, SmolVLM2-2.2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+0.4 (0.8); 1/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q1_black, SmolVLM2-2.2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+0.4 (0.2); 1/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q1_blur10, SmolVLM2-2.2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+0.2 (0.3); 1/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q3_black, SmolVLM2-2.2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `-0.4 (0.3); 0/6 / 1/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q3_blur10, SmolVLM2-2.2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `-0.5 (0.4); 0/6 / 1/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_ART_black, Qwen2-VL-2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+82.0 (10.8); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_ART_blur10, Qwen2-VL-2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+54.1 (13.8); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_INS_black, Qwen2-VL-2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+11.6 (4.3); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_INS_blur10, Qwen2-VL-2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+0.6 (0.5); 2/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q1_black, Qwen2-VL-2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+3.6 (2.3); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q1_blur10, Qwen2-VL-2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+1.1 (0.7); 4/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q3_black, Qwen2-VL-2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+8.6 (3.6); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q3_blur10, Qwen2-VL-2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+4.1 (3.4); 4/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_ART_black, SmolVLM2-2.2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+60.1 (14.7); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_ART_blur10, SmolVLM2-2.2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+24.6 (6.8); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_INS_black, SmolVLM2-2.2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+5.8 (1.8); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_INS_blur10, SmolVLM2-2.2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+0.6 (0.3); 3/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q1_black, SmolVLM2-2.2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+1.4 (0.1); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q1_blur10, SmolVLM2-2.2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+0.3 (0.2); 0/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q3_black, SmolVLM2-2.2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+4.5 (1.3); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q3_blur10, SmolVLM2-2.2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+0.6 (0.2); 0/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_ART_black, M3AE, encoder ajuste completo: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+46.9 (10.5); 3/3 / 0/3`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_ART_blur10, M3AE, encoder ajuste completo: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+22.2 (10.2); 3/3 / 0/3`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_INS_black, M3AE, encoder ajuste completo: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+7.7 (8.3); 3/3 / 0/3`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_INS_blur10, M3AE, encoder ajuste completo: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+2.4 (2.1); 3/3 / 0/3`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q1_black, M3AE, encoder ajuste completo: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+0.4 (0.4); 1/3 / 0/3`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q1_blur10, M3AE, encoder ajuste completo: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+0.7 (0.5); 2/3 / 0/3`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q3_black, M3AE, encoder ajuste completo: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+0.7 (1.2); 1/3 / 0/3`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q3_blur10, M3AE, encoder ajuste completo: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+0.2 (0.6); 1/3 / 0/3`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_ART_black: itens por linha** — `532`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_ART_blur10: itens por linha** — `532`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q1_black: itens por linha** — `1196`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q1_blur10: itens por linha** — `1196`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q3_black: itens por linha** — `1199`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_POL_Q3_blur10: itens por linha** — `1199`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_INS_black: itens por linha** — `1411`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Kvasir-VQA-x1, SHAM_INS_blur10: itens por linha** — `1411`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, alvo_blur10, Qwen2-VL-2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+4.6 (0.9); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, alvo_preto, Qwen2-VL-2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+5.9 (1.5); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, mascara_deslocada_blur10, Qwen2-VL-2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+5.2 (0.9); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, mascara_deslocada_preto, Qwen2-VL-2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+5.9 (1.8); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, alvo_blur10, SmolVLM2-2.2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+5.4 (1.1); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, alvo_preto, SmolVLM2-2.2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+6.5 (0.7); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, mascara_deslocada_blur10, SmolVLM2-2.2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+6.5 (0.9); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, mascara_deslocada_preto, SmolVLM2-2.2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+7.2 (0.9); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, alvo_blur10, Qwen2-VL-2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+3.4 (1.3); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, alvo_preto, Qwen2-VL-2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+4.1 (1.8); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, mascara_deslocada_blur10, Qwen2-VL-2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+3.7 (0.8); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, mascara_deslocada_preto, Qwen2-VL-2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+4.8 (1.8); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, alvo_blur10, SmolVLM2-2.2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+4.1 (0.2); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, alvo_preto, SmolVLM2-2.2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+3.6 (0.5); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, mascara_deslocada_blur10, SmolVLM2-2.2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+3.6 (0.5); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, mascara_deslocada_preto, SmolVLM2-2.2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+3.5 (0.6); 6/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, alvo_blur10, M3AE, encoder ajuste completo: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+2.8 (0.8); 3/3 / 0/3`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, alvo_preto, M3AE, encoder ajuste completo: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+3.1 (1.2); 3/3 / 0/3`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, mascara_deslocada_blur10, M3AE, encoder ajuste completo: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+2.8 (0.7); 3/3 / 0/3`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, mascara_deslocada_preto, M3AE, encoder ajuste completo: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `+3.2 (0.9); 3/3 / 0/3`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, alvo_preto: itens por linha** — `735`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, mascara_deslocada_preto: itens por linha** — `735`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, alvo_blur10: itens por linha** — `735`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **HEAL-MedVQA, mascara_deslocada_blur10: itens por linha** — `735`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Medical-Diff-VQA, oclusor_blur10, Qwen2-VL-2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `-1.6 (0.7); 0/6 / 3/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Medical-Diff-VQA, oclusor_preto, Qwen2-VL-2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `-1.4 (0.5); 0/6 / 2/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Medical-Diff-VQA, oclusor_blur10, SmolVLM2-2.2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `-0.2 (0.8); 0/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Medical-Diff-VQA, oclusor_preto, SmolVLM2-2.2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `-0.2 (0.4); 0/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Medical-Diff-VQA, oclusor_blur10, Qwen2-VL-2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `-1.0 (0.5); 0/6 / 1/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Medical-Diff-VQA, oclusor_preto, Qwen2-VL-2B, encoder afinado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `-1.4 (0.7); 0/6 / 3/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Medical-Diff-VQA, oclusor_blur10, SmolVLM2-2.2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `-1.2 (0.7); 0/6 / 1/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Medical-Diff-VQA, oclusor_preto, SmolVLM2-2.2B, encoder congelado: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `-1.2 (0.7); 0/6 / 0/6`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Medical-Diff-VQA, oclusor_blur10, M3AE, encoder ajuste completo: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `-3.7 (0.9); 0/3 / 3/3`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Medical-Diff-VQA, oclusor_preto, M3AE, encoder ajuste completo: taxa induzida (pp) media (DP); linhas com IC > 0 / IC < 0** — `-5.5 (2.4); 0/3 / 3/3`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Medical-Diff-VQA, oclusor_preto: itens por linha** — `391`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>
- **Medical-Diff-VQA, oclusor_blur10: itens por linha** — `391`  
  <sub>v7_artigo1/analysis/oclusor_negativos.json · sha256 c79f83c2e163</sub>

## S7. Zero-shot sob o mesmo teste

- **zero-shot LLAVA_MED: decodificacao (do_sample / temperature / max_new_tokens)** — `nao definido (gulosa) / nao definido / 64`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA: decodificacao (do_sample / temperature / max_new_tokens)** — `nao definido (gulosa) / nao definido / 64`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER: decodificacao (do_sample / temperature / max_new_tokens)** — `True / 1e-06 / 512`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL: decodificacao (do_sample / temperature / max_new_tokens)** — `True / 1e-06 / 64`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_KVASIR, polipo: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `0.0 / 0.0; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_KVASIR, polipo: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+0.0 [+0.0, +0.0] / +0.0 [+0.0, +0.0]; nao; —`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_KVASIR, instrumento: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `0.0 / 0.0; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_KVASIR, instrumento: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+0.0 [+0.0, +0.0] / +0.0 [+0.0, +0.0]; nao; —`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_KVASIR, controle 'Is there text?': Acc intacta / sem imagem (%); headroom [IC] (pp)** — `83.1 / 86.4; -3.3 [-5.7, -1.2]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_KVASIR, controle 'Is there text?': Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+0.4 [-2.2, +3.1] / +2.1 [-0.8, +5.0]; nao; 1.000`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_KVASIR, polipo secundario: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `0.0 / 0.0; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_KVASIR, polipo secundario: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+0.0 [+0.0, +0.0] / +0.0 [+0.0, +0.0]; nao; —`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_KVASIR, polipo: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `14.0 / 0.0; +14.0 [+11.8, +16.1]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_KVASIR, polipo: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+5.5 [+3.5, +7.4] / +5.4 [+3.5, +7.2]; sim; 1.568`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_KVASIR, instrumento: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `3.8 / 31.5; -27.7 [-30.3, -24.8]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_KVASIR, instrumento: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+1.0 [-1.0, +3.1] / +0.3 [-1.6, +2.2]; nao; 4.500`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_KVASIR, controle 'Is there text?': Acc intacta / sem imagem (%); headroom [IC] (pp)** — `81.1 / 86.4; -5.3 [-12.8, +1.5]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_KVASIR, controle 'Is there text?': Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `-2.9 [-7.7, +1.7] / -3.3 [-8.5, +1.7]; nao; 0.244`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_KVASIR, polipo secundario: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `77.9 / 0.0; +77.9 [+70.6, +84.6]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_KVASIR, polipo secundario: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+52.2 [+43.0, +61.0] / +44.9 [+34.7, +54.5]; sim; 0.953`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_KVASIR, polipo: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `35.4 / 1.4; +34.0 [+31.4, +36.4]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_KVASIR, polipo: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+6.8 [+4.2, +9.2] / +6.9 [+4.6, +9.1]; sim; 0.596`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_KVASIR, instrumento: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `30.6 / 0.0; +30.6 [+28.7, +32.3]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_KVASIR, instrumento: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+10.2 [+7.2, +13.3] / +10.2 [+7.0, +13.4]; sim; 0.760`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_KVASIR, controle 'Is there text?': Acc intacta / sem imagem (%); headroom [IC] (pp)** — `65.4 / 13.6; +51.9 [+45.0, +58.9]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_KVASIR, controle 'Is there text?': Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+2.1 [-3.7, +8.0] / -1.6 [-7.7, +4.6]; nao; 0.340`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_KVASIR, polipo secundario: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `98.5 / 59.6; +39.0 [+29.9, +47.2]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_KVASIR, polipo secundario: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+1.5 [+0.0, +3.8] / +0.0 [-2.1, +2.1]; nao; 0.955`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_KVASIR, polipo: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `24.9 / 14.7; +10.2 [+8.6, +11.7]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_KVASIR, polipo: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `-0.6 [-2.2, +0.8] / -1.0 [-2.7, +0.7]; nao; 0.983`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_KVASIR, instrumento: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `29.9 / 1.6; +28.3 [+25.1, +31.2]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_KVASIR, instrumento: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+8.6 [+5.3, +12.0] / +12.4 [+9.1, +15.6]; sim; 0.904`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_KVASIR, controle 'Is there text?': Acc intacta / sem imagem (%); headroom [IC] (pp)** — `97.5 / 86.4; +11.1 [+7.1, +15.3]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_KVASIR, controle 'Is there text?': Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `-0.8 [-3.5, +1.7] / -0.8 [-3.6, +1.7]; nao; 0.266`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_KVASIR, polipo secundario: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `100.0 / 0.0; +100.0 [+100.0, +100.0]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_KVASIR, polipo secundario: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+0.0 [+0.0, +0.0] / +0.0 [+0.0, +0.0]; nao; 1.000`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_HEAL, fechada-sim: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `80.0 / 99.0; -19.0 [-22.1, -16.2]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_HEAL, fechada-sim: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+0.6 [-0.8, +1.9] / -0.1 [-1.2, +1.0]; nao; 0.833`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_HEAL, fechada-nao: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `23.4 / 20.1; +3.3 [+1.0, +5.6]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_HEAL, fechada-nao: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `-1.4 [-2.9, +0.1] / -0.4 [-1.7, +0.8]; nao; 1.349`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_HEAL, fechada-sim: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `29.1 / 38.7; -9.6 [-14.9, -4.4]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_HEAL, fechada-sim: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+0.6 [-2.9, +4.1] / -12.1 [-16.2, -8.4]; nao; 0.198`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_HEAL, fechada-nao: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `70.3 / 45.3; +25.0 [+21.0, +29.2]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_HEAL, fechada-nao: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+8.6 [+5.0, +12.3] / +14.4 [+10.9, +18.0]; sim; 0.810`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_HEAL, fechada-sim: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `36.3 / 42.1; -5.8 [-10.5, -1.1]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_HEAL, fechada-sim: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `-6.9 [-10.4, -3.6] / -2.1 [-5.5, +1.1]; nao; 0.651`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_HEAL, fechada-nao: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `79.7 / 56.7; +23.0 [+18.8, +27.3]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_HEAL, fechada-nao: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+3.3 [+0.1, +6.7] / +0.0 [-3.0, +3.0]; nao; 0.942`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_HEAL, fechada-sim: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `53.6 / 98.5; -44.9 [-48.5, -41.1]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_HEAL, fechada-sim: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `-10.3 [-13.7, -6.9] / -3.9 [-7.3, -0.6]; nao; 1.147`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_HEAL, fechada-nao: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `72.0 / 46.9; +25.0 [+21.2, +29.0]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_HEAL, fechada-nao: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+1.8 [-1.4, +5.0] / -0.5 [-3.5, +2.4]; nao; 0.913`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_MIMIC, fechada-sim: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `63.4 / 98.2; -34.8 [-39.2, -30.8]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_MIMIC, fechada-sim: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+1.6 [+0.2, +3.0] / +1.6 [+0.5, +2.8]; sim; 0.897`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_MIMIC, fechada-nao: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `0.0 / 0.0; +0.0 [+0.0, +0.0]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot LLAVA_MED_ZEROSHOT_MIMIC, fechada-nao: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+0.0 [+0.0, +0.0] / +0.0 [+0.0, +0.0]; nao; —`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_MIMIC, fechada-sim: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `83.7 / 20.5; +63.2 [+58.1, +68.1]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_MIMIC, fechada-sim: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+15.1 [+11.4, +19.0] / +13.5 [+10.0, +17.2]; sim; 0.598`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_MIMIC, fechada-nao: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `46.3 / 43.3; +3.0 [-9.2, +16.2]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDGEMMA_ZEROSHOT_MIMIC, fechada-nao: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `-4.5 [-14.5, +5.7] / -7.5 [-18.1, +2.8]; nao; 0.677`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_MIMIC, fechada-sim: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `52.6 / 39.5; +13.1 [+8.2, +18.2]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_MIMIC, fechada-sim: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+9.3 [+5.2, +13.5] / +6.3 [+2.0, +10.5]; sim; 0.768`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_MIMIC, fechada-nao: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `35.8 / 29.9; +6.0 [-3.9, +16.4]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot MEDVLTHINKER_ZEROSHOT_MIMIC, fechada-nao: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+11.9 [+1.5, +23.3] / +6.0 [-1.6, +14.7]; nao; 1.292`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_MIMIC, fechada-sim: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `73.4 / 79.0; -5.6 [-10.8, -0.7]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_MIMIC, fechada-sim: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+9.3 [+5.2, +12.9] / +5.2 [+1.8, +8.7]; sim; 0.834`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_MIMIC, fechada-nao: Acc intacta / sem imagem (%); headroom [IC] (pp)** — `25.4 / 1.5; +23.9 [+13.1, +34.9]`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **zero-shot QWEN25VL_ZEROSHOT_MIMIC, fechada-nao: Delta preto [IC] / blur 10 % [IC] (pp); criterio B; suficiencia** — `+16.4 [+7.5, +26.7] / +9.0 [+1.4, +18.0]; sim; 0.941`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>

## S7b. Leitura conjunta sim/nao (HEAL-MedVQA e Medical-Diff-VQA)

- **HEAL-MedVQA, M3AE, encoder ajuste completo, intacta: sensibilidade / especificidade / taxa afirmativa (%)** — `89.2 (3.6) / 90.2 (4.0) / 48.9 (3.7)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, M3AE, encoder ajuste completo, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `89.9 (4.9) / 87.1 (3.1) / 50.8 (4.0)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, M3AE, encoder ajuste completo, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `91.0 (3.5) / 87.3 (3.5) / 51.2 (3.5)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, M3AE, encoder ajuste completo, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `91.7 (3.6) / 87.0 (4.3) / 51.7 (3.9)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, M3AE, encoder ajuste completo, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `92.0 (3.4) / 87.4 (4.1) / 51.6 (3.7)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, M3AE, encoder ajuste completo, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%)** — `90.6 (1.8) / 79.3 (2.4) / 55.1 (2.1)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, Qwen2-VL-2B, encoder congelado, intacta: sensibilidade / especificidade / taxa afirmativa (%)** — `94.3 (1.4) / 81.5 (2.4) / 55.8 (1.9)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, Qwen2-VL-2B, encoder congelado, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `97.1 (0.5) / 75.6 (1.4) / 60.2 (0.9)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, Qwen2-VL-2B, encoder congelado, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `96.9 (0.5) / 76.8 (1.9) / 59.4 (1.2)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, Qwen2-VL-2B, encoder congelado, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `96.6 (0.6) / 75.5 (1.7) / 59.9 (1.1)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, Qwen2-VL-2B, encoder congelado, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `96.3 (0.9) / 76.3 (2.1) / 59.4 (1.5)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, Qwen2-VL-2B, encoder congelado, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%)** — `91.7 (1.0) / 79.6 (1.0) / 55.5 (1.0)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, Qwen2-VL-2B, encoder afinado, intacta: sensibilidade / especificidade / taxa afirmativa (%)** — `95.6 (0.8) / 84.5 (2.2) / 54.9 (1.5)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, Qwen2-VL-2B, encoder afinado, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `96.7 (0.7) / 80.5 (2.6) / 57.5 (1.5)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, Qwen2-VL-2B, encoder afinado, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `96.3 (0.7) / 81.1 (2.7) / 57.0 (1.6)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, Qwen2-VL-2B, encoder afinado, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `96.7 (0.5) / 79.7 (2.4) / 57.9 (1.4)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, Qwen2-VL-2B, encoder afinado, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `96.6 (0.5) / 80.8 (2.4) / 57.2 (1.4)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, Qwen2-VL-2B, encoder afinado, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%)** — `91.7 (1.0) / 79.6 (1.0) / 55.5 (1.0)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, SmolVLM2-2.2B, encoder congelado, intacta: sensibilidade / especificidade / taxa afirmativa (%)** — `93.1 (0.4) / 83.8 (0.3) / 54.0 (0.2)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, SmolVLM2-2.2B, encoder congelado, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `93.2 (0.9) / 80.2 (0.5) / 55.9 (0.6)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, SmolVLM2-2.2B, encoder congelado, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `94.4 (0.6) / 79.7 (0.4) / 56.8 (0.4)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, SmolVLM2-2.2B, encoder congelado, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `92.5 (1.0) / 80.3 (0.6) / 55.5 (0.8)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, SmolVLM2-2.2B, encoder congelado, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `92.7 (0.8) / 80.2 (0.8) / 55.6 (0.7)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, SmolVLM2-2.2B, encoder congelado, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%)** — `89.8 (0.8) / 80.7 (0.8) / 54.0 (0.8)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, SmolVLM2-2.2B, encoder afinado, intacta: sensibilidade / especificidade / taxa afirmativa (%)** — `92.3 (0.7) / 88.1 (1.4) / 51.4 (1.0)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, SmolVLM2-2.2B, encoder afinado, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `94.8 (0.4) / 81.6 (1.0) / 55.9 (0.5)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, SmolVLM2-2.2B, encoder afinado, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `94.5 (0.4) / 82.7 (1.2) / 55.3 (0.8)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, SmolVLM2-2.2B, encoder afinado, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `94.6 (0.7) / 80.9 (1.5) / 56.2 (1.0)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, SmolVLM2-2.2B, encoder afinado, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `94.5 (0.5) / 81.7 (1.0) / 55.8 (0.6)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, SmolVLM2-2.2B, encoder afinado, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%)** — `89.8 (0.8) / 80.7 (0.8) / 54.0 (0.8)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot LLAVA_MED, intacta: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `80.0 / 23.4 / 78.3 [76.1, 80.4]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot LLAVA_MED, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `84.2 / 22.6 / 80.8 [78.7, 82.9]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot LLAVA_MED, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `84.2 / 22.2 / 81.0 [78.9, 83.0]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot LLAVA_MED, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `84.8 / 21.2 / 81.7 [79.7, 83.8]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot LLAVA_MED, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `84.1 / 21.8 / 81.1 [79.1, 83.1]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot LLAVA_MED, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `99.0 / 20.1 / 89.3 [87.7, 90.8]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot MEDGEMMA, intacta: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `29.1 / 70.3 / 20.4 [18.3, 22.6]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot MEDGEMMA, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `41.9 / 56.7 / 28.8 [26.5, 30.9]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot MEDGEMMA, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `48.9 / 55.2 / 34.4 [32.0, 36.9]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot MEDGEMMA, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `42.5 / 65.3 / 26.8 [24.6, 29.1]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot MEDGEMMA, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `36.8 / 69.7 / 24.3 [22.2, 26.5]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot MEDGEMMA, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `38.7 / 45.3 / 28.1 [25.9, 30.5]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot MEDVLTHINKER, intacta: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `36.3 / 79.7 / 24.8 [22.6, 27.1]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot MEDVLTHINKER, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `49.9 / 68.4 / 35.5 [33.1, 38.1]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot MEDVLTHINKER, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `43.2 / 73.9 / 30.8 [28.4, 33.2]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot MEDVLTHINKER, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `43.0 / 71.7 / 32.6 [30.2, 35.0]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot MEDVLTHINKER, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `41.1 / 73.9 / 29.5 [27.2, 31.8]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot MEDVLTHINKER, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `42.1 / 56.7 / 29.5 [27.3, 31.8]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot QWEN25VL, intacta: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `53.6 / 72.0 / 40.6 [38.1, 43.2]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot QWEN25VL, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `77.2 / 58.2 / 59.2 [56.8, 61.7]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot QWEN25VL, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `69.8 / 64.2 / 52.5 [50.1, 55.0]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot QWEN25VL, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `66.9 / 60.0 / 53.3 [50.6, 55.8]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot QWEN25VL, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `65.8 / 63.7 / 50.8 [48.2, 53.4]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **HEAL-MedVQA, zero-shot QWEN25VL, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `98.5 / 46.9 / 75.4 [73.2, 77.5]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, M3AE, encoder ajuste completo, intacta: sensibilidade / especificidade / taxa afirmativa (%)** — `80.6 (5.0) / 73.6 (7.5) / 73.5 (5.3)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, M3AE, encoder ajuste completo, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `69.7 (4.9) / 72.6 (6.7) / 64.1 (4.6)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, M3AE, encoder ajuste completo, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `74.0 (4.0) / 69.2 (11.2) / 68.3 (4.8)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, M3AE, encoder ajuste completo, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `75.2 (3.8) / 74.1 (5.2) / 68.7 (3.6)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, M3AE, encoder ajuste completo, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `76.5 (2.5) / 76.1 (7.9) / 69.6 (3.2)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, M3AE, encoder ajuste completo, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%)** — `62.2 (3.7) / 79.6 (8.5) / 56.7 (4.2)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, Qwen2-VL-2B, encoder congelado, intacta: sensibilidade / especificidade / taxa afirmativa (%)** — `76.1 (0.8) / 76.4 (4.4) / 69.2 (0.8)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, Qwen2-VL-2B, encoder congelado, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `72.0 (0.9) / 75.9 (4.1) / 65.8 (0.9)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, Qwen2-VL-2B, encoder congelado, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `73.4 (0.7) / 75.6 (4.6) / 67.0 (0.4)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, Qwen2-VL-2B, encoder congelado, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `74.3 (0.7) / 76.4 (3.0) / 67.6 (0.5)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, Qwen2-VL-2B, encoder congelado, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `75.3 (0.8) / 75.9 (3.5) / 68.6 (0.5)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, Qwen2-VL-2B, encoder congelado, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%)** — `68.0 (2.0) / 80.6 (1.3) / 61.6 (1.7)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, Qwen2-VL-2B, encoder afinado, intacta: sensibilidade / especificidade / taxa afirmativa (%)** — `79.1 (2.5) / 73.9 (4.0) / 72.1 (2.5)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, Qwen2-VL-2B, encoder afinado, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `76.8 (2.9) / 73.9 (3.4) / 70.1 (2.6)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, Qwen2-VL-2B, encoder afinado, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `77.0 (2.6) / 73.1 (4.5) / 70.4 (2.3)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, Qwen2-VL-2B, encoder afinado, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `79.2 (2.6) / 74.1 (3.6) / 72.2 (2.7)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, Qwen2-VL-2B, encoder afinado, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `79.6 (2.5) / 74.9 (4.1) / 72.4 (2.5)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, Qwen2-VL-2B, encoder afinado, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%)** — `68.0 (2.0) / 80.6 (1.3) / 61.6 (1.7)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, SmolVLM2-2.2B, encoder congelado, intacta: sensibilidade / especificidade / taxa afirmativa (%)** — `76.1 (2.0) / 80.8 (1.1) / 68.6 (1.7)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, SmolVLM2-2.2B, encoder congelado, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `74.0 (1.8) / 83.8 (1.7) / 66.4 (1.4)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, SmolVLM2-2.2B, encoder congelado, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `73.5 (1.3) / 82.1 (1.3) / 66.2 (1.1)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, SmolVLM2-2.2B, encoder congelado, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `76.5 (1.8) / 83.6 (1.6) / 68.6 (1.5)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, SmolVLM2-2.2B, encoder congelado, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `77.0 (1.6) / 81.3 (0.8) / 69.3 (1.3)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, SmolVLM2-2.2B, encoder congelado, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%)** — `64.8 (3.0) / 80.1 (0.8) / 58.9 (2.7)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, SmolVLM2-2.2B, encoder afinado, intacta: sensibilidade / especificidade / taxa afirmativa (%)** — `80.6 (1.8) / 80.6 (2.8) / 72.5 (1.7)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, SmolVLM2-2.2B, encoder afinado, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `77.6 (1.7) / 82.8 (1.8) / 69.7 (1.5)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, SmolVLM2-2.2B, encoder afinado, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `79.3 (1.8) / 81.3 (1.2) / 71.3 (1.5)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, SmolVLM2-2.2B, encoder afinado, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%)** — `80.4 (1.7) / 82.6 (2.6) / 72.2 (1.4)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, SmolVLM2-2.2B, encoder afinado, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%)** — `80.9 (1.6) / 81.8 (2.2) / 72.6 (1.4)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, SmolVLM2-2.2B, encoder afinado, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%)** — `64.8 (3.0) / 80.1 (0.8) / 58.9 (2.7)`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot LLAVA_MED, intacta: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `63.4 / 0.0 / 68.2 [64.2, 71.9]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot LLAVA_MED, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `58.9 / 0.0 / 64.3 [60.0, 68.2]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot LLAVA_MED, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `59.6 / 0.0 / 64.9 [60.7, 68.7]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot LLAVA_MED, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `60.5 / 0.0 / 65.7 [61.4, 69.5]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot LLAVA_MED, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `61.2 / 0.0 / 66.3 [62.2, 70.2]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot LLAVA_MED, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `98.2 / 0.0 / 98.4 [97.3, 99.4]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot MEDGEMMA, intacta: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `83.7 / 46.3 / 78.2 [74.5, 81.7]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot MEDGEMMA, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `69.1 / 43.3 / 65.5 [61.2, 69.7]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot MEDGEMMA, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `69.3 / 44.8 / 66.5 [62.2, 70.7]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot MEDGEMMA, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `84.2 / 38.8 / 79.6 [76.0, 83.0]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot MEDGEMMA, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `82.8 / 37.3 / 78.0 [74.3, 81.5]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot MEDGEMMA, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `20.5 / 43.3 / 23.5 [20.0, 27.2]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot MEDVLTHINKER, intacta: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `52.6 / 35.8 / 53.5 [49.2, 57.8]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot MEDVLTHINKER, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `41.8 / 41.8 / 43.1 [38.7, 47.4]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot MEDVLTHINKER, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `45.8 / 37.3 / 47.3 [43.0, 51.6]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot MEDVLTHINKER, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `51.0 / 53.7 / 50.0 [45.7, 54.3]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot MEDVLTHINKER, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `52.1 / 43.3 / 52.0 [47.7, 56.1]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot MEDVLTHINKER, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `39.5 / 29.9 / 41.8 [37.6, 46.1]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot QWEN25VL, intacta: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `73.4 / 25.4 / 73.5 [69.7, 77.2]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot QWEN25VL, alvo_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `61.6 / 22.4 / 63.7 [59.7, 68.0]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot QWEN25VL, alvo_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `65.2 / 23.9 / 66.7 [62.7, 70.7]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot QWEN25VL, mascara_deslocada_preto: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `70.9 / 38.8 / 69.6 [65.4, 73.5]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot QWEN25VL, mascara_deslocada_blur10: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `70.4 / 32.8 / 70.0 [65.9, 73.7]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>
- **Medical-Diff-VQA, zero-shot QWEN25VL, text_only_ou_sem_imagem: sensibilidade / especificidade / taxa afirmativa (%) [IC]** — `79.0 / 1.5 / 81.6 [78.2, 85.0]`  
  <sub>v7_artigo1/analysis/simnao.json · sha256 5fa3c43c026d</sub>

## S8. Doses (mascara dilatada 1,5x e 2x, preto, subconjunto pareado)

- **Kvasir-VQA-x1: unidades validas em 1,5x e 2x / unidades; perguntas pareadas** — `165 / 243; 1415`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `603 / 943; +8.8 (1.3) / +8.0 (1.0) / +9.0 (1.2); 6 / 6 / 6`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `231 / 314; +26.3 (2.7) / +24.7 (2.1) / +18.0 (3.1); 6 / 6 / 6`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', Qwen2-VL-2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `165 / 243; +0.4 (0.3) / -0.2 (0.6) / +1.6 (0.6); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `603 / 943; +18.8 (3.8) / +20.5 (4.5) / +21.0 (4.2); 6 / 6 / 6`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `231 / 314; +18.0 (5.4) / +23.7 (5.9) / +29.1 (6.9); 6 / 6 / 6`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', SmolVLM2-2.2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `165 / 243; +0.5 (0.6) / +0.1 (1.0) / +1.9 (0.8); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `603 / 943; +12.8 (1.6) / +14.0 (1.3) / +16.9 (2.1); 6 / 6 / 6`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `231 / 314; +24.2 (14.1) / +25.8 (15.2) / +31.6 (14.3); 5 / 5 / 6`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', Qwen2-VL-2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `165 / 243; +0.7 (0.2) / +0.1 (0.5) / +1.7 (0.5); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `603 / 943; +9.8 (2.0) / +9.7 (1.1) / +10.8 (0.7); 6 / 6 / 6`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `231 / 314; +22.3 (3.3) / +23.4 (3.0) / +25.2 (4.0); 6 / 6 / 6`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', SmolVLM2-2.2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `165 / 243; +0.4 (0.3) / -0.3 (0.3) / +1.5 (0.8); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Kvasir-VQA-x1, polipo, M3AE, encoder ajuste completo (3 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `603 / 943; +4.9 (0.9) / +3.3 (1.5) / +4.5 (1.8); 3 / 1 / 2`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Kvasir-VQA-x1, instrumento, M3AE, encoder ajuste completo (3 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `231 / 314; +27.8 (12.6) / +44.0 (14.1) / +54.0 (10.8); 3 / 3 / 3`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Kvasir-VQA-x1, controle 'Is there text?', M3AE, encoder ajuste completo (3 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `165 / 243; -0.6 (1.0) / -0.8 (0.9) / -1.2 (0.6); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **HEAL-MedVQA: unidades validas em 1,5x e 2x / unidades; perguntas pareadas** — `879 / 1360; 938`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder congelado (5 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `430 / 711; -1.0 (0.3) / -0.2 (0.5) / -0.4 (0.2); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder congelado (5 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `508 / 735; -0.3 (0.7) / -0.3 (0.6) / -1.2 (0.7); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `430 / 711; -0.5 (1.0) / -1.0 (0.5) / -1.6 (1.1); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `508 / 735; -0.5 (0.9) / +1.3 (0.8) / +0.3 (1.4); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `430 / 711; +0.1 (0.4) / +0.4 (0.7) / -0.2 (0.6); 0 / 2 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `508 / 735; -0.2 (1.0) / -0.6 (0.7) / -1.1 (0.6); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `430 / 711; -1.2 (0.9) / +0.7 (0.6) / -1.0 (0.9); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `508 / 735; +0.4 (0.2) / +1.3 (1.4) / +0.3 (0.4); 0 / 1 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **HEAL-MedVQA, fechada-sim, M3AE, encoder ajuste completo (3 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `430 / 711; +1.2 (1.5) / +1.4 (1.6) / +2.9 (1.7); 0 / 1 / 2`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **HEAL-MedVQA, fechada-nao, M3AE, encoder ajuste completo (3 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `508 / 735; +0.6 (0.9) / +0.7 (0.7) / +0.7 (0.4); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **HEAL-MedVQA: linha fora das medias de dose** — `QWEN2VL_DORA_HEAL_seed2: 1x do adapter original (ausente na gpu1); 1,5x e 2x do retreino de 03/10: dois checkpoints na mesma celula; fora das medias de dose (item 20)`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA: unidades validas em 1,5x e 2x / unidades; perguntas pareadas** — `372 / 1266; 482`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `126 / 443; +0.9 (1.2) / -1.6 (2.8) / -0.7 (1.4); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `29 / 67; +0.6 (4.0) / +0.0 (0.0) / +1.1 (3.6); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=pleural effusion, Qwen2-VL-2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `27 / 96; -1.2 (1.9) / -2.5 (4.5) / -0.6 (2.8); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=atelectasis, Qwen2-VL-2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `29 / 87; -0.6 (2.6) / +0.0 (2.2) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=lung opacity, Qwen2-VL-2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `15 / 66; +2.2 (3.4) / +0.0 (4.2) / -2.2 (5.4); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=cardiomegaly, Qwen2-VL-2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `24 / 58; +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=edema, Qwen2-VL-2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `1 / 45; +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=vascular congestion, Qwen2-VL-2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `2 / 23; +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `126 / 443; +2.2 (0.9) / +1.6 (1.7) / +1.9 (1.4); 0 / 1 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `29 / 67; -1.1 (2.8) / -1.7 (6.1) / -1.1 (3.6); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=pleural effusion, SmolVLM2-2.2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `27 / 96; +6.8 (1.5) / +6.2 (4.5) / +4.9 (3.8); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=atelectasis, SmolVLM2-2.2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `29 / 87; -1.1 (2.8) / +0.0 (4.9) / +1.1 (2.8); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=lung opacity, SmolVLM2-2.2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `15 / 66; +2.2 (3.4) / +2.2 (6.9) / -1.1 (5.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=cardiomegaly, SmolVLM2-2.2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `24 / 58; +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=edema, SmolVLM2-2.2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `1 / 45; +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=vascular congestion, SmolVLM2-2.2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `2 / 23; +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `126 / 443; +0.3 (1.0) / -0.3 (1.0) / +0.1 (0.9); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `29 / 67; +0.0 (3.1) / -1.7 (1.9) / -2.9 (4.6); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=pleural effusion, Qwen2-VL-2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `27 / 96; +0.0 (2.3) / -0.6 (2.8) / -1.9 (4.5); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=atelectasis, Qwen2-VL-2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `29 / 87; +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=lung opacity, Qwen2-VL-2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `15 / 66; +0.0 (7.3) / -1.1 (5.0) / +3.3 (3.7); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=cardiomegaly, Qwen2-VL-2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `24 / 58; +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=edema, Qwen2-VL-2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `1 / 45; +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=vascular congestion, Qwen2-VL-2B, encoder afinado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `2 / 23; +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `126 / 443; +0.8 (1.3) / +3.4 (1.2) / +2.8 (0.8); 0 / 3 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `29 / 67; +0.0 (3.8) / -1.7 (1.9) / +1.1 (6.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=pleural effusion, SmolVLM2-2.2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `27 / 96; +0.0 (4.7) / +9.3 (2.0) / +5.6 (5.6); 0 / 0 / 1`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=atelectasis, SmolVLM2-2.2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `29 / 87; +1.7 (1.9) / +2.9 (2.6) / +4.0 (2.6); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=lung opacity, SmolVLM2-2.2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `15 / 66; +0.0 (4.2) / -1.1 (2.7) / -2.2 (5.4); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=cardiomegaly, SmolVLM2-2.2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `24 / 58; +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=edema, SmolVLM2-2.2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `1 / 45; +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=vascular congestion, SmolVLM2-2.2B, encoder congelado (6 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `2 / 23; +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE, encoder ajuste completo (3 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `126 / 443; +1.9 (1.7) / +5.0 (7.2) / +3.2 (6.0); 0 / 2 / 1`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, fechada-nao, M3AE, encoder ajuste completo (3 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `29 / 67; +2.3 (2.0) / -1.1 (5.3) / +1.1 (7.2); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=pleural effusion, M3AE, encoder ajuste completo (3 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `27 / 96; +0.0 (3.7) / +3.7 (12.8) / +8.6 (4.3); 0 / 1 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=atelectasis, M3AE, encoder ajuste completo (3 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `29 / 87; +0.0 (3.4) / +4.6 (5.3) / +2.3 (4.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=lung opacity, M3AE, encoder ajuste completo (3 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `15 / 66; +0.0 (6.7) / +0.0 (6.7) / -4.4 (10.2); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=cardiomegaly, M3AE, encoder ajuste completo (3 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `24 / 58; +2.8 (2.4) / +5.6 (8.7) / +6.9 (14.6); 0 / 0 / 1`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=edema, M3AE, encoder ajuste completo (3 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `1 / 45; +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **Medical-Diff-VQA, entidade=vascular congestion, M3AE, encoder ajuste completo (3 linhas): n pareado / n classe; Delta 1x / 1,5x / 2x (pp) media (DP); linhas IC>0** — `2 / 23; +0.0 (0.0) / +0.0 (0.0) / +0.0 (0.0); 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>

## S9. Metodo e estatistica

- **bootstrap por imagem: replicas / semente / imagens por base (Kvasir / HEAL / MIMIC)** — `2000 / 20260913 / 1291 / 2079 / 1445`  
  <sub>v7_artigo1/analysis/bases_raw.json · sha256 c298bde508a7</sub>
- **Holm por linha, familia de classes, Kvasir-VQA-x1** — `dependent_polyp, dependent_instrument, controle_texto`  
  <sub>v7_artigo1/analysis/bases_raw.json · sha256 c298bde508a7</sub>
- **Holm por linha, familia de classes, HEAL-MedVQA** — `closed_yes, closed_no`  
  <sub>v7_artigo1/analysis/bases_raw.json · sha256 c298bde508a7</sub>
- **Holm por linha, familia de classes, Medical-Diff-VQA** — `closed_yes, closed_no, entidade=pleural effusion, entidade=atelectasis, entidade=lung opacity, entidade=cardiomegaly, entidade=edema, entidade=vascular congestion`  
  <sub>v7_artigo1/analysis/bases_raw.json · sha256 c298bde508a7</sub>
- **regra de resolubilidade (headroom legivel)** — `limite inferior do IC 95 % por imagem do headroom (Acc intacta - text-only arm da mesma familia e semente; zero-shot: com imagem - sem imagem) > 0; sem limiar de 0,10 (a rodada 1 usou tambem headroom >= 0,10; as duas versoes estao em criterio.json)`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **independencia das linhas** — `as 27 linhas por base sao 3 sementes x 9 configuracoes (familia x adaptador x encoder) e nao sao independentes; as proporcoes necessarias / resoluveis / linhas sao descritivas, sem IC`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **artefact-box template (Kvasir-VQA-x1): estatística** — `IC 95 % por imagem (réplicas fixas da base Kvasir) nas 27 linhas, sob preto, blur 10 % e cor média; blur 4 % = sigma fixo de 25 px (sigma / largura mediana 0.040 no Kvasir), predições só nas 15 linhas de 01/10; a folha de 01/10 usava IC por pergunta`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **image gain against the question-only classifier (TF-IDF)** — `Acc(intacta) - Acc(TF-IDF) nos mesmos itens, IC por imagem; Medical-Diff-VQA: TF-IDF do subconjunto nas fechadas (piso composto); ilustração apenas, não muda contagem nenhuma (a escada com TF-IDF fica só interna)`  
  <sub>v7_artigo1/analysis/rodada3.json · sha256 a88991cab120</sub>
- **McNemar** — `mid-p exato (binomial, meio peso no observado) nos discordantes entre mascara deslocada e alvo ocluido (shamstats.mcnemar_midp)`  
  <sub>v7_artigo1/analysis/bases_raw.json · sha256 c298bde508a7</sub>
- **Kvasir: ordem do posicionamento da mascara deslocada** — `hflip, vflip, rot180, ate 50 translacoes aleatorias (semente 20260913); margem (dilatacao do alvo) 5 px; >= 80 % no campo de visao; area maxima 40 % do campo de visao`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **Kvasir: metodo por unidade (imagem x alvo)** — `{"translate": 60, "hflip": 112, "rot180": 31, "vflip": 40}`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **Kvasir: mascaras casadas (Kvasir-SEG polipos / Kvasir-Instrument instrumentos)** — `1000 / 590 (instrumentos sem par: 410)`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **Kvasir: imagens de teste com mascara / total; unidades; excluidas (sem posicao / area > max)** — `303/1291; 243; 44 / 16`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **HEAL: regra da mascara deslocada** — `outra anatomia da mesma imagem com razao de area 0,7-1,4 e sobreposicao <= 5 % do alvo; senao espelho horizontal; senao posicionador do Kvasir com >= 80 % dentro do atlas toracico (pixels anotados em >= 2 % das mascaras)`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **HEAL: metodo por unidade (1 360)** — `{"hflip": 653, "anatomy": 153, "translate": 520, "rot180": 20, "vflip": 14}`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **HEAL: fechadas sem posicao valida** — `69`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **MIMIC: regra da regiao-alvo** — `uniao das caixas do Chest ImaGenome das regioes-folha (mais finas) com o atributo mapeado; regiao-mae descartada quando uma descendente tem o atributo`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **MIMIC: regra da mascara deslocada (v2, alvos com > 1 caixa)** — `por caixa: anatomia homologa sem o atributo (razao 0,8-1,25) -> translacao vertical com area exata (pares bilaterais juntos) -> espelho horizontal -> anatomia ampliada (razao 0,5-2,0); >= 80 % no atlas, inteira no filme, sem tocar o alvo dilatado em 5 px, caixas sem sobreposicao entre si; alvos de 1 caixa: regra do HEAL`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **MIMIC: metodos por caixa (avaliaveis)** — `{"anatomy": 1043, "vtrans": 534, "hflip": 155, "vtrans_pair": 1674, "translate": 125, "vflip": 67, "anatomy_wide": 2}`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **MIMIC: metodos por unidade (avaliaveis)** — `{"multi:anatomy": 173, "multi:hflip+vtrans": 32, "multi:anatomy+vtrans": 179, "hflip": 105, "multi:vtrans_pair": 656, "anatomy": 448, "multi:vtrans": 101, "multi:vtrans+vtrans_pair": 40, "translate": 125, "multi:anatomy+vtrans+vtrans_pair": 20, "vflip": 67, "multi:anatomy+vtrans_pair": 25, "multi:hflip+vtrans_pair": 5, "multi:hflip": 2, "multi:anatomy+hflip+vtrans": 3, "multi:hflip+vtrans+vtrans_pair": 2, "multi:anatomy+anatomy_wide": 1, "multi:anatomy_wide+hflip": 1}`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **MIMIC: avaliaveis / total (inventario v2)** — `1985/3000`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **MIMIC: teto de area do alvo** — `40 % do quadro inteiro`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **blur 10 %** — `filtro gaussiano com sigma = 10 % da largura da imagem, aplicado so na regiao`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **cor media da regiao** — `media RGB dos pixels da propria regiao (remove a forma, mantem a cor local)`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **codificacao das condicoes** — `C0 = bytes originais do arrow (HEAL/MIMIC: PNG lado maior 1024); demais = PNG sem perda a partir dos pixels decodificados`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **reencode JPEG (piloto Qwen2-VL LoRA s0, Kvasir): predicoes da intacta que mudam** — `50 de 2121 = 2.36 %`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **reencode JPEG: delta de acuracia da intacta** — `+0.19 pp`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **composicao de lote (0,6-0,7 %)** — `sem fonte localizada na gpu1`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>

## S10. Limitacoes

- **HEAL: perguntas / unidades em imagens com >= 2 anatomias anotadas** — `579 / 530 (de 1446 / 1360)`  
  <sub>v7_artigo1/analysis/placebo_geometry_heal.json · sha256 d47551dfe083</sub>
- **HEAL: unidades em que a mascara deslocada toca outra anatomia (qualquer / > 50 % da outra)** — `328 / 175 de 530 (61.9 % / 33.0 %)`  
  <sub>v7_artigo1/analysis/placebo_geometry_heal.json · sha256 d47551dfe083</sub>
- **HEAL: perguntas afetadas (qualquer / > 50 %) sobre o total** — `361 / 196 de 1446`  
  <sub>v7_artigo1/analysis/placebo_geometry_heal.json · sha256 d47551dfe083</sub>
- **Medical-Diff-VQA: unidades em que alguma caixa da mascara deslocada toca outra regiao-folha (qualquer / > 50 % da outra)** — `1656 / 1397 de 1657`  
  <sub>v7_artigo1/analysis/placebo_geometry_mimic.json · sha256 70d353366fb8</sub>
- **Kvasir: mascaras (Kvasir-SEG polipos / Kvasir-Instrument instrumentos casados)** — `1000 / 590 (instrumentos sem par: 410)`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **Kvasir: TF-IDF no instrumento (acuracia, todas as linhas)** — `0.0`  
  <sub>v7_artigo1/analysis/headroom.json · sha256 ead5e6908e4a</sub>
- **HEAL: fechadas sem posicao valida da mascara deslocada** — `69`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **LLaVA-Med KVASIR: por classe, acuracia da intacta (%) / respostas vazias / com mais de 5 palavras / fechadas fora de yes-no, sobre o total** — `dependent_instrument 0.0 / 0 / 210 / 0 de 314; dependent_polyp 0.0 / 0 / 808 / 0 de 943; dependent_polyp_secondary 0.0 / 0 / 0 / 0 de 136; negative_control 43.1 / 0 / 250 / 0 de 728`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **LLaVA-Med HEAL: por classe, acuracia da intacta (%) / respostas vazias / com mais de 5 palavras / fechadas fora de yes-no, sobre o total** — `closed_no 23.4 / 0 / 0 / 0 de 735; closed_yes 80.0 / 0 / 0 / 0 de 711`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **LLaVA-Med MIMIC: por classe, acuracia da intacta (%) / respostas vazias / com mais de 5 palavras / fechadas fora de yes-no, sobre o total** — `closed_no 0.0 / 0 / 0 / 0 de 67; closed_no_sham 64.7 / 0 / 0 / 0 de 391; closed_yes 63.4 / 0 / 0 / 0 de 443; open 0.0 / 0 / 1084 / 0 de 1084`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **decodificacao com amostragem (do_sample = True no generation_config do Hub, temperatura 1e-6)** — `MEDVLTHINKER, QWEN25VL`  
  <sub>v7_artigo1/analysis/zeroshot.json · sha256 35d8feb9d4d5</sub>
- **HEAL-MedVQA: controle de posicao por geometria (unidades: uma anatomia / varias sem sobreposicao / varias com sobreposicao)** — `830 / 202 / 328`  
  <sub>v7_artigo1/analysis/heal_estratificado.json · sha256 d372fc9c8e44</sub>
- **Medical-Diff-VQA: as regioes-folha do Chest ImaGenome cobrem o torax inteiro; qualquer caixa deslocada toca outra regiao por construcao** — `1656 de 1657 unidades`  
  <sub>v7_artigo1/analysis/placebo_geometry_mimic.json · sha256 70d353366fb8</sub>
- **natureza do alvo por base** — `Kvasir-VQA-x1: mascara binaria de segmentacao (Kvasir-SEG / Kvasir-Instrument, harness/isbi_placebo/inventory_kvasir.py, masks.binarize_mask); HEAL-MedVQA: mascara de segmentacao em RLE (harness/isbi_placebo/heal/heal_rle.py, decode_rle); Medical-Diff-VQA: caixa anatomica (bounding box) do Chest ImaGenome (v7_mimic/scripts/16_inventory_mimic.py, box_mask) -- a mascara deslocada no Medical-Diff-VQA tambem e caixa`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **adapter original de QWEN2VL_DORA_HEAL_seed2 no Drive (rclone lsf, sem download)** — `nao encontrado em gdrive:Pesquisa/doutorado/ (outputs_models tem qwen2vl_dora_heal_seed0 e seed1) nem em gdrive:doutorado/pesquisa/P0_ICDIP/checkpoints_backup/ (log v7_artigo1/logs/rclone_lsf_dora_heal_seed2.txt)`  
  <sub>results/logs/rclone_lsf_dora_heal_seed2.txt · sha256 </sub>
- **predicoes sem sha de checkpoint recuperavel** — `13 (QWEN2VL_DORA_HEAL_seed2: adapter original ausente na gpu1)`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **suficiencia sob blur 10 % e cor media** — `so no Medical-Diff-VQA; Kvasir e HEAL nao tem S_blur10/S_regmean (54 linhas); suficiencia so sob preto`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **composicao de lote** — `sem fonte localizada na gpu1`  
  <sub>v7_artigo1/analysis/fatos_metodo.json · sha256 c1e8a24a0153</sub>
- **Medical-Diff-VQA: 473 / 443 fechadas-sim** — `473 (e 2 152 avaliaveis) = inventario v1 (11/10, regiao mais fina, placebo por bloco); 443 (e 1 985) = inventario v2 (12/10, placebo por caixa, decisao do candidato apos a galeria). As predicoes T/P/S existentes foram geradas sobre os arrows v2 (sha no manifesto de condicoes). 430 = v2 so exatas.`  
  <sub>v7_artigo1/analysis/inventario_linhas.json · sha256 c1b7e95185eb</sub>
- **Kvasir-VQA-x1, split oficial do HF: imagens do teste oficial que aparecem no treino oficial, por img_id / imagens do teste oficial** — `3821 / 4058`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **Kvasir-VQA-x1, split oficial do HF: pares pergunta-resposta (treino / teste)** — `143594 / 15955`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **Kvasir-VQA-x1, nosso split: imagens (treino / val / teste)** — `4514 / 644 / 1291`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **Kvasir-VQA-x1, nosso split: intersecoes por image_id (treino-teste / val-teste / treino-val)** — `0 / 0 / 0`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **Kvasir-VQA-x1, nosso split: imagens do teste que sao copia byte a byte (md5) de uma imagem do treino / da val (outro image_id)** — `34 / 2`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **Kvasir-VQA-x1, nosso split: imagens da val com copia byte a byte no treino; md5 repetidos dentro do teste** — `19; 7`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **Kvasir-VQA-x1: unidades do teste de necessidade com copia byte a byte no treino ou na val / unidades** — `2 / 243`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>

## S-split. Sensibilidade sem as 2 unidades duplicadas (Kvasir-VQA-x1; so o que muda)

- **unidade duplicada kvasir/clb0lbwz3doqs086u0kqy5ut2: copia no treino; perguntas avaliaveis retiradas por classe** — `kvasir/clb0lbwzadoy8086u7rog5t28; dependent_instrument 3, negative_control 3`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **unidade duplicada kvasir/clb0lbwz4doro086ua6fxbql5: copia no treino; perguntas avaliaveis retiradas por classe** — `kvasir/clb0lbwzbdoz0086u4leqb9pu; dependent_instrument 3, negative_control 3`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **perguntas retiradas por classe (polipo / instrumento / controle negativo / polipo secundario / 'Is there text?' / artefact-box template)** — `0 / 6 / 6 / 0 / 2 / 2`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **regra** — `mesmo engine e mesma matriz de replicas (2 000, semente 20260913, todas as imagens do inventario); so os qids das 2 imagens saem; nada re-inferido`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, instrumento: n perguntas por linha (completo: 314)** — `308`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, instrumento: image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp) (completo: +68.2 – +77.1)** — `+68.2 – +76.9`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, instrumento: custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp) (completo: -0.3 – +6.7)** — `-0.3 – +6.8`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, instrumento: custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp) (completo: -1.3 – +3.5)** — `-1.3 – +3.2`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, instrumento: Δ preto, mínimo – máximo entre as 27 linhas (pp) (completo: +4.8 – +47.1)** — `+5.2 – +47.1`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, instrumento: Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp) (completo: +4.5 – +48.7)** — `+3.6 – +48.7`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, instrumento: suficiência (preto), mínimo – máximo entre as 27 linhas (razão) (completo: 0.368 – 0.906)** — `0.373 – 0.904`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, controle negativo (3 templates): n perguntas por linha (completo: 728)** — `722`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, controle negativo (3 templates): image gain above the text-only arm, mínimo – máximo entre as 27 linhas (pp) (completo: +17.6 – +18.7)** — `+17.5 – +18.6`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, controle negativo (3 templates): custo do controle pareado, preto, mínimo – máximo entre as 27 linhas (pp) (completo: +1.5 – +8.9)** — `+1.5 – +9.0`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, controle negativo (3 templates): custo do controle pareado, blur 10 %, mínimo – máximo entre as 27 linhas (pp) (completo: +0.4 – +7.0)** — `+0.4 – +6.9`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, controle negativo (3 templates): Δ preto, mínimo – máximo entre as 27 linhas (pp) (completo: -4.1 – +0.4)** — `-4.0 – +0.4`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, controle negativo (3 templates): Δ blur 10 %, mínimo – máximo entre as 27 linhas (pp) (completo: -4.4 – +1.0)** — `-4.3 – +1.0`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, controle negativo (3 templates): suficiência (preto), mínimo – máximo entre as 27 linhas (razão) (completo: 0.543 – 0.776)** — `0.541 – 0.777`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, artefact-box template, Δ blur 10 %, 27 linhas: linhas com limite superior do IC < 0 / com limite inferior do IC > 0 (folha completa: 15/27 / 0/27)** — `13/27 / 0/27`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, artefact-box template, Δ blur 10 %, 15 linhas de 01/10: linhas com limite superior do IC < 0 / com limite inferior do IC > 0 (folha completa: 12/15 / 0/15)** — `10/15 / 0/15`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, artefact-box template, Δ cor média, 27 linhas: linhas com limite superior do IC < 0 / com limite inferior do IC > 0 (folha completa: 13/27 / 1/27)** — `12/27 / 1/27`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades, Kvasir-VQA-x1, artefact-box template, Δ cor média, 15 linhas de 01/10: linhas com limite superior do IC < 0 / com limite inferior do IC > 0 (folha completa: 10/15 / 0/15)** — `9/15 / 0/15`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>
- **sem as 2 unidades: quantidades que nao mudam no valor impresso** — `escada e resoluveis/necessarias de polipo; polipo: image gain above the text-only arm; polipo: custo do controle pareado, preto; polipo: custo do controle pareado, blur 10 %; polipo: Δ preto; polipo: Δ blur 10 %; polipo: suficiência (preto); escada e resoluveis/necessarias de instrumento; escada e resoluveis/necessarias de controle negativo (3 templates); artefact-box template, Δ preto, 27 linhas: 17/27 / 0/27; artefact-box template, Δ preto, 15 linhas de 01/10: 12/15 / 0/15`  
  <sub>v7_artigo1/analysis/split_kvasir.json · sha256 310c5eed567c</sub>

## S12. Verificacoes adicionais (rodada 8)

- **Kvasir-VQA-x1, polipo, afinados: L3 e L0 / L3 / linhas** — `25 / 25 / 27`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, polipo, zero-shot (4 modelos): L3 e L0 / L3 / linhas** — `2 / 2 / 4`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, instrumento, afinados: L3 e L0 / L3 / linhas** — `25 / 25 / 27`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, instrumento, zero-shot (4 modelos): L3 e L0 / L3 / linhas** — `2 / 2 / 4`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), afinados: L3 e L0 / L3 / linhas** — `0 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), zero-shot (4 modelos): L3 e L0 / L3 / linhas** — `0 / 0 / 4`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **HEAL-MedVQA, fechada-sim, afinados: L3 e L0 / L3 / linhas** — `0 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **HEAL-MedVQA, fechada-sim, zero-shot (4 modelos): L3 e L0 / L3 / linhas** — `0 / 0 / 4`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **HEAL-MedVQA, fechada-nao, afinados: L3 e L0 / L3 / linhas** — `0 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **HEAL-MedVQA, fechada-nao, zero-shot (4 modelos): L3 e L0 / L3 / linhas** — `1 / 1 / 4`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Medical-Diff-VQA, fechada-sim, afinados: L3 e L0 / L3 / linhas** — `9 / 12 / 27`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Medical-Diff-VQA, fechada-sim, zero-shot (4 modelos): L3 e L0 / L3 / linhas** — `2 / 2 / 4`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Medical-Diff-VQA, fechada-nao, afinados: L3 e L0 / L3 / linhas** — `0 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Medical-Diff-VQA, fechada-nao, zero-shot (4 modelos): L3 e L0 / L3 / linhas** — `0 / 1 / 4`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Medical-Diff-VQA, fechada-sim, afinados: linhas que passam em L1 sem passar em L0 / delas entre as L3** — `3 / 3`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, instrumento, baseline sem imagem: acuracia nas 9 linhas (3 familias x 3 sementes) (%)** — `0.0`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, instrumento, baseline sem imagem: respostas previstas (pergunta -> resposta: vezes nas 9 linhas)** — `Where in the image is the instrument? -> none: 954; How many instrumnets are in the image? -> 0: 936; Are there any instruments in the image? Check all that are present. -> none: 936`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, instrumento, respostas de referencia, 'How many instrumnets are in the image?': respostas distintas; mais frequentes (vezes); contem 'none' ou '0'** — `2; 1 99, 2 5; nao`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, instrumento, respostas de referencia, 'Are there any instruments in the image? Check all that are present.': respostas distintas; mais frequentes (vezes); contem 'none' ou '0'** — `8; tube 76, biopsy forceps 17, polyp snare; tube 4, metal clip 3, polyp snare 1, biopsy forceps; tube 1; nao`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, instrumento, respostas de referencia, 'Where in the image is the instrument?': respostas distintas; mais frequentes (vezes); contem 'none' ou '0'** — `40; lower-center; lower-right 19, center; center-right; upper-center; upper-right 9, center; upper-center 9, center; lower-center; lower-right 7, center; center-left; upper-center; upper-left 7, center; center-right; lower-center; lower-right 5; nao`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, treino, 'Are there any instruments in the image? Check all that are present.': perguntas; resposta majoritaria (fracao %)** — `2213; none (67.0)`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, treino, 'How many instrumnets are in the image?': perguntas; resposta majoritaria (fracao %)** — `2496; 0 (71.4)`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, treino, 'Where in the image is the instrument?': perguntas; resposta majoritaria (fracao %)** — `2220; none (66.4)`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Holm (regra)** — `p unilateral bootstrap por criterio (fracao das 2 000 replicas por imagem <= 0); Holm por linha sobre a familia de classes registrada (Kvasir: polipo, instrumento, 'Is there text?'; controle negativo de 3 templates no lugar de 'Is there text?' para a linha dele; HEAL: sim, nao; Medical-Diff-VQA: sim, nao e as 6 entidades); passa se p ajustado < 0,025`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Holm: testes em que p < 0,025 concorda / discorda da regra do IC (sem Holm)** — `1639 / 1`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, polipo: L0 / L1 / L2 / L3 com Holm (sem Holm, p bootstrap < 0,025)** — `27 / 27 / 25 / 25 de 27 (27 / 27 / 25 / 25)`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, instrumento: L0 / L1 / L2 / L3 com Holm (sem Holm, p bootstrap < 0,025)** — `27 / 26 / 25 / 25 de 27 (27 / 26 / 25 / 25)`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates): L0 / L1 / L2 / L3 com Holm (sem Holm, p bootstrap < 0,025)** — `25 / 0 / 0 / 0 de 27 (25 / 0 / 0 / 0)`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **HEAL-MedVQA, fechada-sim: L0 / L1 / L2 / L3 com Holm (sem Holm, p bootstrap < 0,025)** — `0 / 1 / 0 / 0 de 27 (0 / 1 / 0 / 0)`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **HEAL-MedVQA, fechada-nao: L0 / L1 / L2 / L3 com Holm (sem Holm, p bootstrap < 0,025)** — `27 / 0 / 0 / 0 de 27 (27 / 0 / 0 / 0)`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Medical-Diff-VQA, fechada-sim: L0 / L1 / L2 / L3 com Holm (sem Holm, p bootstrap < 0,025)** — `13 / 8 / 2 / 2 de 27 (18 / 18 / 11 / 11)`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Medical-Diff-VQA, fechada-nao: L0 / L1 / L2 / L3 com Holm (sem Holm, p bootstrap < 0,025)** — `0 / 0 / 0 / 0 de 27 (0 / 0 / 0 / 0)`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Medical-Diff-VQA, fechada-sim, zero-shot (4 modelos): L0 / L1 / L2 / L3 com Holm (sem Holm, p bootstrap < 0,025)** — `4 / 3 / 3 / 2 de 4 (4 / 4 / 4 / 2)`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, polipo, 15 linhas de 01/10: dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `8 / 14 de 15`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, polipo, 15 linhas de 01/10: L2 com blur 4 % / com blur 10 %; Delta blur 4 %, minimo – maximo (pp)** — `8 / 14; +1.7 – +3.9`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, instrumento, 15 linhas de 01/10: dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `12 / 14 de 15`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, instrumento, 15 linhas de 01/10: L2 com blur 4 % / com blur 10 %; Delta blur 4 %, minimo – maximo (pp)** — `12 / 14; +1.9 – +27.1`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), 15 linhas de 01/10: dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `0 / 0 de 15`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), 15 linhas de 01/10: L2 com blur 4 % / com blur 10 %; Delta blur 4 %, minimo – maximo (pp)** — `0 / 0; -1.4 – +0.1`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, fine-tuning, treino: arquivo; imagens / pares pergunta-resposta / bytes** — `vqa_kvasir_train_clean.arrow; 4514 / 38211 / 247544682`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Kvasir-VQA-x1, fine-tuning, validacao: arquivo; imagens / pares pergunta-resposta / bytes** — `vqa_kvasir_val_clean.arrow; 644 / 5494 / 34439906`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **HEAL-MedVQA, fine-tuning, treino: arquivo; imagens / pares pergunta-resposta / bytes** — `vqa_heal_train.arrow; 6709 / 14740 / 2536490386`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **HEAL-MedVQA, fine-tuning, validacao: arquivo; imagens / pares pergunta-resposta / bytes** — `vqa_heal_val.arrow; 746 / 1640 / 282989898`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Medical-Diff-VQA, fine-tuning, treino: arquivo; imagens / pares pergunta-resposta / bytes** — `vqa_mimic_train.arrow; 7387 / 15000 / 2866116714`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Medical-Diff-VQA, fine-tuning, validacao: arquivo; imagens / pares pergunta-resposta / bytes** — `vqa_mimic_val.arrow; 718 / 1500 / 282323250`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **HEAL-MedVQA e Medical-Diff-VQA: nota dos arquivos de treino** — `HEAL: data/finetune_arrows/vqa_heal_train.arrow e data/isbi_placebo/vqa_heal_train.arrow sao o mesmo arquivo (hard link, mesmo sha); gerado por harness/isbi_placebo/heal/make_heal_train_arrows.py. Medical-Diff-VQA: tabela de itens v7_mimic/data/items_train.parquet.`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>

## S13. Holm por familia da Tabela 1 e variante com queda bruta (rodada 9)

- **Holm, familias (rodada 9)** — `familia da Tabela 1: Kvasir-VQA-x1 {polipo, instrumento, controle negativo}; HEAL-MedVQA {sim, nao}; Medical-Diff-VQA {sim, nao}. Familia da rodada 8: Kvasir-VQA-x1 {polipo, instrumento, 'Is there text?'} (controle negativo com ele no lugar de 'Is there text?'); HEAL-MedVQA {sim, nao}; Medical-Diff-VQA {sim, nao e as 6 entidades} (8 testes). Mesmos p unilaterais bootstrap; passa se p ajustado < 0,025`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, polipo, afinados: L0 / L1 / L2 / L3 com Holm, familia da Tabela 1** — `27 / 27 / 25 / 25 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, polipo, afinados: L0 / L1 / L2 / L3 com Holm, familia da rodada 8** — `27 / 27 / 25 / 25 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, polipo, afinados: L0 / L1 / L2 / L3 sem Holm (p bootstrap < 0,025)** — `27 / 27 / 25 / 25 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, polipo, afinados: testes em que p < 0,025 e a regra do IC discordam / testes** — `0 / 108`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, polipo, zero-shot (4 modelos): L0 / L1 / L2 / L3 com Holm, familia da Tabela 1** — `2 / 2 / 2 / 2 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, polipo, zero-shot (4 modelos): L0 / L1 / L2 / L3 com Holm, familia da rodada 8** — `2 / 2 / 2 / 2 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, polipo, zero-shot (4 modelos): L0 / L1 / L2 / L3 sem Holm (p bootstrap < 0,025)** — `2 / 2 / 2 / 2 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, polipo, zero-shot (4 modelos): testes em que p < 0,025 e a regra do IC discordam / testes** — `0 / 16`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, instrumento, afinados: L0 / L1 / L2 / L3 com Holm, familia da Tabela 1** — `27 / 26 / 25 / 25 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, instrumento, afinados: L0 / L1 / L2 / L3 com Holm, familia da rodada 8** — `27 / 26 / 25 / 25 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, instrumento, afinados: L0 / L1 / L2 / L3 sem Holm (p bootstrap < 0,025)** — `27 / 26 / 25 / 25 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, instrumento, afinados: testes em que p < 0,025 e a regra do IC discordam / testes** — `0 / 108`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, instrumento, zero-shot (4 modelos): L0 / L1 / L2 / L3 com Holm, familia da Tabela 1** — `2 / 2 / 2 / 2 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, instrumento, zero-shot (4 modelos): L0 / L1 / L2 / L3 com Holm, familia da rodada 8** — `2 / 2 / 2 / 2 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, instrumento, zero-shot (4 modelos): L0 / L1 / L2 / L3 sem Holm (p bootstrap < 0,025)** — `2 / 2 / 2 / 2 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, instrumento, zero-shot (4 modelos): testes em que p < 0,025 e a regra do IC discordam / testes** — `0 / 16`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), afinados: L0 / L1 / L2 / L3 com Holm, familia da Tabela 1** — `25 / 0 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), afinados: L0 / L1 / L2 / L3 com Holm, familia da rodada 8** — `25 / 0 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), afinados: L0 / L1 / L2 / L3 sem Holm (p bootstrap < 0,025)** — `25 / 0 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), afinados: testes em que p < 0,025 e a regra do IC discordam / testes** — `0 / 108`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), zero-shot (4 modelos): L0 / L1 / L2 / L3 com Holm, familia da Tabela 1** — `2 / 0 / 0 / 0 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), zero-shot (4 modelos): L0 / L1 / L2 / L3 com Holm, familia da rodada 8** — `2 / 0 / 0 / 0 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), zero-shot (4 modelos): L0 / L1 / L2 / L3 sem Holm (p bootstrap < 0,025)** — `2 / 0 / 0 / 0 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), zero-shot (4 modelos): testes em que p < 0,025 e a regra do IC discordam / testes** — `0 / 16`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-sim, afinados: L0 / L1 / L2 / L3 com Holm, familia da Tabela 1** — `0 / 1 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-sim, afinados: L0 / L1 / L2 / L3 com Holm, familia da rodada 8** — `0 / 1 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-sim, afinados: L0 / L1 / L2 / L3 sem Holm (p bootstrap < 0,025)** — `0 / 1 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-sim, afinados: testes em que p < 0,025 e a regra do IC discordam / testes** — `0 / 108`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-sim, zero-shot (4 modelos): L0 / L1 / L2 / L3 com Holm, familia da Tabela 1** — `0 / 0 / 0 / 0 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-sim, zero-shot (4 modelos): L0 / L1 / L2 / L3 com Holm, familia da rodada 8** — `0 / 0 / 0 / 0 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-sim, zero-shot (4 modelos): L0 / L1 / L2 / L3 sem Holm (p bootstrap < 0,025)** — `0 / 0 / 0 / 0 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-sim, zero-shot (4 modelos): testes em que p < 0,025 e a regra do IC discordam / testes** — `0 / 16`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-nao, afinados: L0 / L1 / L2 / L3 com Holm, familia da Tabela 1** — `27 / 0 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-nao, afinados: L0 / L1 / L2 / L3 com Holm, familia da rodada 8** — `27 / 0 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-nao, afinados: L0 / L1 / L2 / L3 sem Holm (p bootstrap < 0,025)** — `27 / 0 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-nao, afinados: testes em que p < 0,025 e a regra do IC discordam / testes** — `0 / 108`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-nao, zero-shot (4 modelos): L0 / L1 / L2 / L3 com Holm, familia da Tabela 1** — `3 / 1 / 1 / 1 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-nao, zero-shot (4 modelos): L0 / L1 / L2 / L3 com Holm, familia da rodada 8** — `3 / 1 / 1 / 1 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-nao, zero-shot (4 modelos): L0 / L1 / L2 / L3 sem Holm (p bootstrap < 0,025)** — `3 / 2 / 1 / 1 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **HEAL-MedVQA, fechada-nao, zero-shot (4 modelos): testes em que p < 0,025 e a regra do IC discordam / testes** — `0 / 16`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-sim, afinados: L0 / L1 / L2 / L3 com Holm, familia da Tabela 1** — `17 / 14 / 8 / 8 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-sim, afinados: L0 / L1 / L2 / L3 com Holm, familia da rodada 8 (8 testes)** — `13 / 8 / 2 / 2 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-sim, afinados: L0 / L1 / L2 / L3 sem Holm (p bootstrap < 0,025)** — `18 / 18 / 11 / 11 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-sim, afinados: testes em que p < 0,025 e a regra do IC discordam / testes** — `1 / 108`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-sim, zero-shot (4 modelos): L0 / L1 / L2 / L3 com Holm, familia da Tabela 1** — `4 / 4 / 4 / 2 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-sim, zero-shot (4 modelos): L0 / L1 / L2 / L3 com Holm, familia da rodada 8 (8 testes)** — `4 / 3 / 3 / 2 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-sim, zero-shot (4 modelos): L0 / L1 / L2 / L3 sem Holm (p bootstrap < 0,025)** — `4 / 4 / 4 / 2 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-sim, zero-shot (4 modelos): testes em que p < 0,025 e a regra do IC discordam / testes** — `0 / 16`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-nao, afinados: L0 / L1 / L2 / L3 com Holm, familia da Tabela 1** — `0 / 0 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-nao, afinados: L0 / L1 / L2 / L3 com Holm, familia da rodada 8 (8 testes)** — `0 / 0 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-nao, afinados: L0 / L1 / L2 / L3 sem Holm (p bootstrap < 0,025)** — `0 / 0 / 0 / 0 de 27`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-nao, afinados: testes em que p < 0,025 e a regra do IC discordam / testes** — `0 / 108`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-nao, zero-shot (4 modelos): L0 / L1 / L2 / L3 com Holm, familia da Tabela 1** — `0 / 2 / 1 / 1 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-nao, zero-shot (4 modelos): L0 / L1 / L2 / L3 com Holm, familia da rodada 8 (8 testes)** — `0 / 1 / 0 / 0 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-nao, zero-shot (4 modelos): L0 / L1 / L2 / L3 sem Holm (p bootstrap < 0,025)** — `0 / 2 / 1 / 1 de 4`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Medical-Diff-VQA, fechada-nao, zero-shot (4 modelos): testes em que p < 0,025 e a regra do IC discordam / testes** — `0 / 16`  
  <sub>v7_artigo1/analysis/holm_familias.json · sha256 48851860cc0c</sub>
- **Tabela 1, variante com queda bruta (tables/table_criteria_rawdrop.tex), linha 'Kvasir-VQA-x1 & polyp': coluna '...and raw drop' (L3 e L0)** — `25`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Tabela 1, variante com queda bruta (tables/table_criteria_rawdrop.tex), linha 'Kvasir-VQA-x1 & instrument': coluna '...and raw drop' (L3 e L0)** — `25`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Tabela 1, variante com queda bruta (tables/table_criteria_rawdrop.tex), linha 'Kvasir-VQA-x1 & negative control': coluna '...and raw drop' (L3 e L0)** — `0`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Tabela 1, variante com queda bruta (tables/table_criteria_rawdrop.tex), linha 'HEAL-MedVQA & closed-ended, yes-questions': coluna '...and raw drop' (L3 e L0)** — `0`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Tabela 1, variante com queda bruta (tables/table_criteria_rawdrop.tex), linha 'HEAL-MedVQA & closed-ended, no-questions': coluna '...and raw drop' (L3 e L0)** — `0`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Tabela 1, variante com queda bruta (tables/table_criteria_rawdrop.tex), linha 'Medical-Diff-VQA & closed-ended, yes-questions': coluna '...and raw drop' (L3 e L0)** — `9`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Tabela 1, variante com queda bruta (tables/table_criteria_rawdrop.tex), linha 'Medical-Diff-VQA & closed-ended, no-questions': coluna '...and raw drop' (L3 e L0)** — `n.s.`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>
- **Tabela 1, variante com queda bruta (tables/table_criteria_rawdrop.tex), linha 'Medical-Diff-VQA & yes-questions, zero-shot (4 models)': coluna '...and raw drop' (L3 e L0)** — `2`  
  <sub>v7_artigo1/analysis/rodada8.json · sha256 04c4187cc3ec</sub>

## S15. Declaracao final por grupo: dois preenchimentos, ganho significativo e queda bruta (rodada 11)

- **declaracao final (regra)** — `declarado = L3 (L1 e Delta blur 10 % e image gain, IC 95 % por imagem > 0) e L0 (queda bruta > 0); decisao do Claudio de 21/10/2026`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, polipo: declarados (dois preenchimentos, ganho significativo e queda bruta) / linhas** — `25 / 27`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder congelado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder afinado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder afinado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `5 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder congelado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, polipo, M3AE, encoder ajuste completo: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `2 / 3 / 3`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, instrumento: declarados (dois preenchimentos, ganho significativo e queda bruta) / linhas** — `25 / 27`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder congelado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder afinado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder afinado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `5 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder congelado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, instrumento, M3AE, encoder ajuste completo: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `2 / 3 / 3`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates): declarados (dois preenchimentos, ganho significativo e queda bruta) / linhas** — `0 / 27`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), Qwen2-VL-2B, encoder congelado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), SmolVLM2-2.2B, encoder afinado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), Qwen2-VL-2B, encoder afinado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), SmolVLM2-2.2B, encoder congelado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), M3AE, encoder ajuste completo: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 3 / 3`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **HEAL-MedVQA, fechada-sim: declarados (dois preenchimentos, ganho significativo e queda bruta) / linhas** — `0 / 27`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder congelado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 5 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 4 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder afinado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **HEAL-MedVQA, fechada-sim, M3AE, encoder ajuste completo: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 0 / 3`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **HEAL-MedVQA, fechada-nao: declarados (dois preenchimentos, ganho significativo e queda bruta) / linhas** — `0 / 27`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder congelado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 3 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder afinado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder afinado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 5 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder congelado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 4 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **HEAL-MedVQA, fechada-nao, M3AE, encoder ajuste completo: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 3 / 3`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Medical-Diff-VQA, fechada-sim: declarados (dois preenchimentos, ganho significativo e queda bruta) / linhas** — `9 / 27`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder congelado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `3 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `2 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder afinado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `2 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `1 / 6 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE, encoder ajuste completo: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `1 / 3 / 3`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Medical-Diff-VQA, fechada-nao: declarados (dois preenchimentos, ganho significativo e queda bruta) / linhas** — `0 / 27`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder congelado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder afinado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder afinado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder congelado: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>
- **Medical-Diff-VQA, fechada-nao, M3AE, encoder ajuste completo: declarados (dois preenchimentos, ganho significativo e queda bruta) / resoluveis / linhas** — `0 / 0 / 3`  
  <sub>v7_artigo1/analysis/declarados_r11.json · sha256 3ab8c85b6bc4</sub>

## S16. Maximos de Delta entre os declarados e entidades pela regra final (rodada 12)

- **Kvasir-VQA-x1, polipo: Delta preto maximo entre os 25 runs declarados (dois preenchimentos, ganho significativo e queda bruta) / maximo entre os 27 (pp)** — `+26.2 / +26.2`  
  <sub>v7_artigo1/analysis/rodada12.json · sha256 3b62479329b3</sub>
- **Kvasir-VQA-x1, instrumento: Delta preto maximo entre os 25 runs declarados (dois preenchimentos, ganho significativo e queda bruta) / maximo entre os 27 (pp)** — `+47.1 / +47.1`  
  <sub>v7_artigo1/analysis/rodada12.json · sha256 3b62479329b3</sub>
- **Medical-Diff-VQA, fechada-sim: Delta preto maximo entre os 9 runs declarados (dois preenchimentos, ganho significativo e queda bruta) / maximo entre os 27 (pp)** — `+6.8 / +6.8`  
  <sub>v7_artigo1/analysis/rodada12.json · sha256 3b62479329b3</sub>
- **HEAL-MedVQA, fechada-sim: Delta preto maximo entre os 0 runs declarados (dois preenchimentos, ganho significativo e queda bruta) / maximo entre os 27 (pp)** — `— / +3.2`  
  <sub>v7_artigo1/analysis/rodada12.json · sha256 3b62479329b3</sub>
- **Medical-Diff-VQA, fechada-sim, entidade pleural effusion (96 perguntas): runs com ganho significativo / declarados (dois preenchimentos, ganho significativo e queda bruta) / runs** — `27 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada12.json · sha256 3b62479329b3</sub>
- **Medical-Diff-VQA, fechada-sim, entidade atelectasis (87 perguntas): runs com ganho significativo / declarados (dois preenchimentos, ganho significativo e queda bruta) / runs** — `0 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada12.json · sha256 3b62479329b3</sub>
- **Medical-Diff-VQA, fechada-sim, entidade lung opacity (66 perguntas): runs com ganho significativo / declarados (dois preenchimentos, ganho significativo e queda bruta) / runs** — `2 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada12.json · sha256 3b62479329b3</sub>
- **Medical-Diff-VQA, fechada-sim, entidade cardiomegaly (58 perguntas): runs com ganho significativo / declarados (dois preenchimentos, ganho significativo e queda bruta) / runs** — `0 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada12.json · sha256 3b62479329b3</sub>
- **Medical-Diff-VQA, fechada-sim, entidade edema (45 perguntas): runs com ganho significativo / declarados (dois preenchimentos, ganho significativo e queda bruta) / runs** — `12 / 5 / 27`  
  <sub>v7_artigo1/analysis/rodada12.json · sha256 3b62479329b3</sub>
- **Medical-Diff-VQA, fechada-sim, entidade vascular congestion (23 perguntas): runs com ganho significativo / declarados (dois preenchimentos, ganho significativo e queda bruta) / runs** — `23 / 1 / 27`  
  <sub>v7_artigo1/analysis/rodada12.json · sha256 3b62479329b3</sub>

## S14. Holm da coluna com queda bruta e blur 4 % nas tres bases (rodada 10)

- **Tabela 1, variante com queda bruta, linha 'Kvasir-VQA-x1 & polyp': '...and raw drop' (L3 e L0) com Holm, familia da Tabela 1 / familia da rodada 8** — `25 / 25 de 27`  
  <sub>v7_artigo1/analysis/holm_rawdrop.json · sha256 b07ab36719a6</sub>
- **Tabela 1, variante com queda bruta, linha 'Kvasir-VQA-x1 & instrument': '...and raw drop' (L3 e L0) com Holm, familia da Tabela 1 / familia da rodada 8** — `25 / 25 de 27`  
  <sub>v7_artigo1/analysis/holm_rawdrop.json · sha256 b07ab36719a6</sub>
- **Tabela 1, variante com queda bruta, linha 'Kvasir-VQA-x1 & negative control': '...and raw drop' (L3 e L0) com Holm, familia da Tabela 1 / familia da rodada 8** — `0 / 0 de 27`  
  <sub>v7_artigo1/analysis/holm_rawdrop.json · sha256 b07ab36719a6</sub>
- **Tabela 1, variante com queda bruta, linha 'HEAL-MedVQA & closed-ended, yes-questions': '...and raw drop' (L3 e L0) com Holm, familia da Tabela 1 / familia da rodada 8** — `0 / 0 de 27`  
  <sub>v7_artigo1/analysis/holm_rawdrop.json · sha256 b07ab36719a6</sub>
- **Tabela 1, variante com queda bruta, linha 'HEAL-MedVQA & closed-ended, no-questions': '...and raw drop' (L3 e L0) com Holm, familia da Tabela 1 / familia da rodada 8** — `0 / 0 de 27`  
  <sub>v7_artigo1/analysis/holm_rawdrop.json · sha256 b07ab36719a6</sub>
- **Tabela 1, variante com queda bruta, linha 'Medical-Diff-VQA & closed-ended, yes-questions': '...and raw drop' (L3 e L0) com Holm, familia da Tabela 1 / familia da rodada 8** — `6 / 2 de 27`  
  <sub>v7_artigo1/analysis/holm_rawdrop.json · sha256 b07ab36719a6</sub>
- **Tabela 1, variante com queda bruta, linha 'Medical-Diff-VQA & closed-ended, no-questions': '...and raw drop' (L3 e L0) com Holm, familia da Tabela 1 / familia da rodada 8** — `n.s. / n.s.`  
  <sub>v7_artigo1/analysis/holm_rawdrop.json · sha256 b07ab36719a6</sub>
- **Tabela 1, variante com queda bruta, linha 'Medical-Diff-VQA & yes-questions, zero-shot (4 models)': '...and raw drop' (L3 e L0) com Holm, familia da Tabela 1 / familia da rodada 8** — `2 / 2 de 4`  
  <sub>v7_artigo1/analysis/holm_rawdrop.json · sha256 b07ab36719a6</sub>
- **Kvasir-VQA-x1: blur 4 % (T_blur/P_blur), sigma fixo (px) / razao sigma/largura mediana** — `25 / 0.0399`  
  <sub>data/kvasir/blur_sigma_report.json · sha256 c7cf4ca28329</sub>
- **HEAL-MedVQA: blur 4 % (T_blur/P_blur), sigma fixo (px) / largura mediana (px) / razao sigma/largura mediana (min - max por unidade); razao se fossem 25 px** — `33.99 / 851 / 0.0399 (0.0332 - 0.0479); 0.0294`  
  <sub>data/blur4/manifest_blur4_r10.json · sha256 ad209e900ef3</sub>
- **HEAL-MedVQA: blur 4 %, unidades; T preto regerado identico ao arrow existente (pixels)** — `1360; 1360/1360`  
  <sub>data/blur4/manifest_blur4_r10.json · sha256 ad209e900ef3</sub>
- **Medical-Diff-VQA: blur 4 % (T_blur/P_blur), sigma fixo (px) / largura mediana (px) / razao sigma/largura mediana (min - max por unidade); razao se fossem 25 px** — `35.10 / 879 / 0.0399 (0.0343 - 0.0464); 0.0284`  
  <sub>data/blur4/manifest_blur4_r10.json · sha256 ad209e900ef3</sub>
- **Medical-Diff-VQA: blur 4 %, unidades; T preto regerado identico ao arrow existente (pixels)** — `1266; 1266/1266`  
  <sub>data/blur4/manifest_blur4_r10.json · sha256 ad209e900ef3</sub>
- **adaptadores e checkpoints da inferencia de blur 4 % conferidos contra o carimbo da C0 (sha256) / total; excecao** — `65 / 66; HEAL-MedVQA QWEN2VL_DORA_HEAL_seed2 no adapter do retreino de 03/10 (original ausente na gpu1), fora das contagens`  
  <sub>data/blur4/manifest_adaptadores_blur4_r10.json · sha256 b1c3e122e509</sub>
- **Kvasir-VQA-x1, polipo, todos os runs (27): Delta blur 4 %, minimo – maximo (pp)** — `+0.1 – +6.6`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, polipo, todos os runs (27): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `13 / 25`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, polipo, todos os runs (27): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `13 / 25`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, polipo, 15 runs de 01/10 (15): Delta blur 4 %, minimo – maximo (pp)** — `+1.7 – +3.9`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, polipo, 15 runs de 01/10 (15): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `8 / 14`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, polipo, 15 runs de 01/10 (15): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `8 / 14`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, polipo, 12 runs de encoder invertido (12): Delta blur 4 %, minimo – maximo (pp)** — `+0.1 – +6.6`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, polipo, 12 runs de encoder invertido (12): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `5 / 11`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, polipo, 12 runs de encoder invertido (12): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `5 / 11`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, instrumento, todos os runs (27): Delta blur 4 %, minimo – maximo (pp)** — `+1.9 – +27.1`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, instrumento, todos os runs (27): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `23 / 25`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, instrumento, todos os runs (27): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `23 / 25`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, instrumento, 15 runs de 01/10 (15): Delta blur 4 %, minimo – maximo (pp)** — `+1.9 – +27.1`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, instrumento, 15 runs de 01/10 (15): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `12 / 14`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, instrumento, 15 runs de 01/10 (15): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `12 / 14`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, instrumento, 12 runs de encoder invertido (12): Delta blur 4 %, minimo – maximo (pp)** — `+9.6 – +24.2`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, instrumento, 12 runs de encoder invertido (12): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `11 / 11`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, instrumento, 12 runs de encoder invertido (12): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `11 / 11`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), todos os runs (27): Delta blur 4 %, minimo – maximo (pp)** — `-1.4 – +0.5`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), todos os runs (27): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), todos os runs (27): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), 15 runs de 01/10 (15): Delta blur 4 %, minimo – maximo (pp)** — `-1.4 – +0.1`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), 15 runs de 01/10 (15): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), 15 runs de 01/10 (15): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), 12 runs de encoder invertido (12): Delta blur 4 %, minimo – maximo (pp)** — `-1.0 – +0.5`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), 12 runs de encoder invertido (12): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), 12 runs de encoder invertido (12): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-sim, todos os runs (26): Delta blur 4 %, minimo – maximo (pp)** — `-2.0 – +1.8`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-sim, todos os runs (26): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-sim, todos os runs (26): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-sim, 15 runs de 01/10 (14): Delta blur 4 %, minimo – maximo (pp)** — `-0.8 – +1.8`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-sim, 15 runs de 01/10 (14): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-sim, 15 runs de 01/10 (14): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-sim, 12 runs de encoder invertido (12): Delta blur 4 %, minimo – maximo (pp)** — `-2.0 – +1.1`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-sim, 12 runs de encoder invertido (12): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-sim, 12 runs de encoder invertido (12): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-nao, todos os runs (26): Delta blur 4 %, minimo – maximo (pp)** — `-1.6 – +1.5`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-nao, todos os runs (26): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-nao, todos os runs (26): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-nao, 15 runs de 01/10 (14): Delta blur 4 %, minimo – maximo (pp)** — `-1.6 – +1.5`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-nao, 15 runs de 01/10 (14): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-nao, 15 runs de 01/10 (14): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-nao, 12 runs de encoder invertido (12): Delta blur 4 %, minimo – maximo (pp)** — `-1.2 – +0.5`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-nao, 12 runs de encoder invertido (12): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, fechada-nao, 12 runs de encoder invertido (12): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Medical-Diff-VQA, fechada-sim, todos os runs (27): Delta blur 4 %, minimo – maximo (pp)** — `-0.5 – +6.3`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Medical-Diff-VQA, fechada-sim, todos os runs (27): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `10 / 12`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Medical-Diff-VQA, fechada-sim, todos os runs (27): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `7 / 9`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Medical-Diff-VQA, fechada-sim, 12 runs de encoder invertido (12): Delta blur 4 %, minimo – maximo (pp)** — `+0.2 – +6.3`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Medical-Diff-VQA, fechada-sim, 12 runs de encoder invertido (12): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `6 / 6`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Medical-Diff-VQA, fechada-sim, 12 runs de encoder invertido (12): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `3 / 3`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Medical-Diff-VQA, fechada-nao, todos os runs (27): Delta blur 4 %, minimo – maximo (pp)** — `-1.5 – +6.0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Medical-Diff-VQA, fechada-nao, todos os runs (27): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Medical-Diff-VQA, fechada-nao, todos os runs (27): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Medical-Diff-VQA, fechada-nao, 12 runs de encoder invertido (12): Delta blur 4 %, minimo – maximo (pp)** — `-1.5 – +4.5`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Medical-Diff-VQA, fechada-nao, 12 runs de encoder invertido (12): dois preenchimentos com ganho significativo (L3) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **Medical-Diff-VQA, fechada-nao, 12 runs de encoder invertido (12): L3 e queda bruta (L0) com blur 4 % / com blur 10 %** — `0 / 0`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>
- **HEAL-MedVQA, QWEN2VL_DORA_HEAL_seed2 (blur 4 % no adapter do retreino de 03/10; fora das contagens): Delta blur 4 % [IC] por classe (pp)** — `fechada-sim -0.1 [-1.0, +0.7]; fechada-nao +0.0 [-1.2, +1.2]`  
  <sub>v7_artigo1/analysis/blur4_r10.json · sha256 0369af75450b</sub>

## S17. Escala do blur e queda bruta sob blur (rodada 13)

- **mascara do alvo nos itens 1-2 (regra)** — `uniao dos pixels alterados pelo preto, pelo blur 10 % ou pelo blur 4 % em relacao a imagem intacta; alteracao = media absoluta, na escala 0-255, da media dos canais dentro da mascara`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Kvasir-VQA-x1: pares imagem-alvo medidos** — `243`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Kvasir-VQA-x1: alteracao media dentro do alvo, preto / blur 10 % / blur 4 % (0-255; mediana [IQR])** — `128.3 [74.0, 159.5] / 26.9 [20.4, 42.7] / 15.3 [12.3, 20.8]`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Kvasir-VQA-x1: razao blur 10 % / preto e blur 4 % / preto da alteracao dentro do alvo (mediana [IQR])** — `0.222 [0.157, 0.530] / 0.133 [0.095, 0.285]`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Kvasir-VQA-x1: diametro equivalente do alvo, px / % da largura (mediana [IQR])** — `193.3 [149.0, 257.0] / 27.8 [21.9, 34.6]`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Kvasir-VQA-x1: sigma / diametro do alvo, blur 4 % / blur 10 % (mediana [IQR])** — `0.129 [0.097, 0.168] / 0.359 [0.289, 0.457]`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Kvasir-VQA-x1: fracao dos pares com sigma < metade do diametro, blur 4 % / blur 10 % (%)** — `99.6 / 81.5`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **HEAL-MedVQA: pares imagem-alvo medidos** — `1360`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **HEAL-MedVQA: alteracao media dentro do alvo, preto / blur 10 % / blur 4 % (0-255; mediana [IQR])** — `155.7 [114.1, 197.9] / 25.4 [20.5, 30.2] / 11.2 [8.0, 15.6]`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **HEAL-MedVQA: razao blur 10 % / preto e blur 4 % / preto da alteracao dentro do alvo (mediana [IQR])** — `0.158 [0.113, 0.256] / 0.075 [0.040, 0.138]`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **HEAL-MedVQA: diametro equivalente do alvo, px / % da largura (mediana [IQR])** — `256.1 [216.7, 292.2] / 28.9 [24.0, 33.2]`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **HEAL-MedVQA: sigma / diametro do alvo, blur 4 % / blur 10 % (mediana [IQR])** — `0.133 [0.116, 0.157] / 0.346 [0.302, 0.416]`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **HEAL-MedVQA: fracao dos pares com sigma < metade do diametro, blur 4 % / blur 10 % (%)** — `99.7 / 86.5`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Medical-Diff-VQA: pares imagem-alvo medidos** — `1266`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Medical-Diff-VQA: alteracao media dentro do alvo, preto / blur 10 % / blur 4 % (0-255; mediana [IQR])** — `141.8 [116.8, 167.6] / 23.0 [17.0, 28.9] / 11.0 [8.1, 14.3]`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Medical-Diff-VQA: razao blur 10 % / preto e blur 4 % / preto da alteracao dentro do alvo (mediana [IQR])** — `0.161 [0.111, 0.231] / 0.080 [0.052, 0.118]`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Medical-Diff-VQA: diametro equivalente do alvo, px / % da largura (mediana [IQR])** — `315.0 [231.9, 392.7] / 34.1 [24.9, 43.2]`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Medical-Diff-VQA: sigma / diametro do alvo, blur 4 % / blur 10 % (mediana [IQR])** — `0.111 [0.089, 0.151] / 0.293 [0.232, 0.401]`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Medical-Diff-VQA: fracao dos pares com sigma < metade do diametro, blur 4 % / blur 10 % (%)** — `99.7 / 80.4`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Kvasir-VQA-x1, polipo, afinados: declarados (regra final) que tambem tem queda bruta sob blur 10 % (IC > 0) / declarados** — `24 / 25`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Kvasir-VQA-x1, polipo, QWEN2VL_LORA_KVASIR_seed1: declarado sem queda bruta sob blur 10 %: Acc(C0) - Acc(T blur 10 %) [IC] (pp)** — `+2.4 [-0.3, +5.2]`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Kvasir-VQA-x1, polipo, zero-shot (4 modelos): declarados (regra final) que tambem tem queda bruta sob blur 10 % (IC > 0) / declarados** — `2 / 2`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Kvasir-VQA-x1, instrumento, afinados: declarados (regra final) que tambem tem queda bruta sob blur 10 % (IC > 0) / declarados** — `25 / 25`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Kvasir-VQA-x1, instrumento, zero-shot (4 modelos): declarados (regra final) que tambem tem queda bruta sob blur 10 % (IC > 0) / declarados** — `2 / 2`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), afinados: declarados (regra final) que tambem tem queda bruta sob blur 10 % (IC > 0) / declarados** — `0 / 0`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), zero-shot (4 modelos): declarados (regra final) que tambem tem queda bruta sob blur 10 % (IC > 0) / declarados** — `0 / 0`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **HEAL-MedVQA, fechada-sim, afinados: declarados (regra final) que tambem tem queda bruta sob blur 10 % (IC > 0) / declarados** — `0 / 0`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **HEAL-MedVQA, fechada-sim, zero-shot (4 modelos): declarados (regra final) que tambem tem queda bruta sob blur 10 % (IC > 0) / declarados** — `0 / 0`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **HEAL-MedVQA, fechada-nao, afinados: declarados (regra final) que tambem tem queda bruta sob blur 10 % (IC > 0) / declarados** — `0 / 0`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **HEAL-MedVQA, fechada-nao, zero-shot (4 modelos): declarados (regra final) que tambem tem queda bruta sob blur 10 % (IC > 0) / declarados** — `1 / 1`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Medical-Diff-VQA, fechada-sim, afinados: declarados (regra final) que tambem tem queda bruta sob blur 10 % (IC > 0) / declarados** — `8 / 9`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Medical-Diff-VQA, fechada-sim, SMOLVLM_LORA_MIMIC_seed1: declarado sem queda bruta sob blur 10 %: Acc(C0) - Acc(T blur 10 %) [IC] (pp)** — `+1.8 [-0.2, +3.8]`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Medical-Diff-VQA, fechada-sim, zero-shot (4 modelos): declarados (regra final) que tambem tem queda bruta sob blur 10 % (IC > 0) / declarados** — `2 / 2`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Medical-Diff-VQA, fechada-nao, afinados: declarados (regra final) que tambem tem queda bruta sob blur 10 % (IC > 0) / declarados** — `0 / 0`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>
- **Medical-Diff-VQA, fechada-nao, zero-shot (4 modelos): declarados (regra final) que tambem tem queda bruta sob blur 10 % (IC > 0) / declarados** — `0 / 0`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>

## S18. Declaracao final com queda bruta sob preto e sob blur 10 % (rodada 14)

- **declaracao final (regra, decisao A do Claudio, 22/10/2026)** — `declarado = Delta preto e Delta blur 10 % (IC > 0), image gain (IC > 0) e queda bruta sob preto e sob blur 10 % (IC > 0); recalculada a partir das predicoes (mesmas replicas); IC 95 % por imagem`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **recalculo a partir das predicoes: intervalos iguais aos de analysis/necessity_v2 / diferentes** — `2015 / 0`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, polipo, afinados: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / linhas** — `24 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, polipo, afinados: declarados pela regra final com Holm, familia da Tabela 1 / linhas** — `24 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, polipo, afinados: declarados pela regra da rodada 11 (queda bruta so sob preto) que tambem tem queda bruta sob blur 10 % / declarados pela regra da rodada 11** — `24 / 25`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, polipo, afinados, QWEN2VL_LORA_KVASIR_seed1: sai da declaracao pela queda bruta sob blur 10 %: Acc(C0) - Acc(T blur 10 %) [IC] (pp)** — `+2.4 [-0.3, +5.2]`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, polipo, zero-shot (4 modelos): declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / linhas** — `2 / 4`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, polipo, zero-shot (4 modelos): declarados pela regra final com Holm, familia da Tabela 1 / linhas** — `2 / 4`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, polipo, zero-shot (4 modelos): declarados pela regra da rodada 11 (queda bruta so sob preto) que tambem tem queda bruta sob blur 10 % / declarados pela regra da rodada 11** — `2 / 2`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, instrumento, afinados: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / linhas** — `25 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, instrumento, afinados: declarados pela regra final com Holm, familia da Tabela 1 / linhas** — `25 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, instrumento, afinados: declarados pela regra da rodada 11 (queda bruta so sob preto) que tambem tem queda bruta sob blur 10 % / declarados pela regra da rodada 11** — `25 / 25`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, instrumento, zero-shot (4 modelos): declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / linhas** — `2 / 4`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, instrumento, zero-shot (4 modelos): declarados pela regra final com Holm, familia da Tabela 1 / linhas** — `2 / 4`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, instrumento, zero-shot (4 modelos): declarados pela regra da rodada 11 (queda bruta so sob preto) que tambem tem queda bruta sob blur 10 % / declarados pela regra da rodada 11** — `2 / 2`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), afinados: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / linhas** — `0 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), afinados: declarados pela regra final com Holm, familia da Tabela 1 / linhas** — `0 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), afinados: declarados pela regra da rodada 11 (queda bruta so sob preto) que tambem tem queda bruta sob blur 10 % / declarados pela regra da rodada 11** — `0 / 0`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), zero-shot (4 modelos): declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / linhas** — `0 / 4`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), zero-shot (4 modelos): declarados pela regra final com Holm, familia da Tabela 1 / linhas** — `0 / 4`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), zero-shot (4 modelos): declarados pela regra da rodada 11 (queda bruta so sob preto) que tambem tem queda bruta sob blur 10 % / declarados pela regra da rodada 11** — `0 / 0`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-sim, afinados: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / linhas** — `0 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-sim, afinados: declarados pela regra final com Holm, familia da Tabela 1 / linhas** — `0 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-sim, afinados: declarados pela regra da rodada 11 (queda bruta so sob preto) que tambem tem queda bruta sob blur 10 % / declarados pela regra da rodada 11** — `0 / 0`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-sim, zero-shot (4 modelos): declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / linhas** — `0 / 4`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-sim, zero-shot (4 modelos): declarados pela regra final com Holm, familia da Tabela 1 / linhas** — `0 / 4`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-sim, zero-shot (4 modelos): declarados pela regra da rodada 11 (queda bruta so sob preto) que tambem tem queda bruta sob blur 10 % / declarados pela regra da rodada 11** — `0 / 0`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-nao, afinados: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / linhas** — `0 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-nao, afinados: declarados pela regra final com Holm, familia da Tabela 1 / linhas** — `0 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-nao, afinados: declarados pela regra da rodada 11 (queda bruta so sob preto) que tambem tem queda bruta sob blur 10 % / declarados pela regra da rodada 11** — `0 / 0`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-nao, zero-shot (4 modelos): declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / linhas** — `1 / 4`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-nao, zero-shot (4 modelos): declarados pela regra final com Holm, familia da Tabela 1 / linhas** — `1 / 4`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-nao, zero-shot (4 modelos): declarados pela regra da rodada 11 (queda bruta so sob preto) que tambem tem queda bruta sob blur 10 % / declarados pela regra da rodada 11** — `1 / 1`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, afinados: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / linhas** — `8 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, afinados: declarados pela regra final com Holm, familia da Tabela 1 / linhas** — `5 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, afinados: declarados pela regra da rodada 11 (queda bruta so sob preto) que tambem tem queda bruta sob blur 10 % / declarados pela regra da rodada 11** — `8 / 9`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, afinados, SMOLVLM_LORA_MIMIC_seed1: sai da declaracao pela queda bruta sob blur 10 %: Acc(C0) - Acc(T blur 10 %) [IC] (pp)** — `+1.8 [-0.2, +3.8]`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, zero-shot (4 modelos): declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / linhas** — `2 / 4`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, zero-shot (4 modelos): declarados pela regra final com Holm, familia da Tabela 1 / linhas** — `2 / 4`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, zero-shot (4 modelos): declarados pela regra da rodada 11 (queda bruta so sob preto) que tambem tem queda bruta sob blur 10 % / declarados pela regra da rodada 11** — `2 / 2`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-nao, afinados: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / linhas** — `0 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-nao, afinados: declarados pela regra final com Holm, familia da Tabela 1 / linhas** — `0 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-nao, afinados: declarados pela regra da rodada 11 (queda bruta so sob preto) que tambem tem queda bruta sob blur 10 % / declarados pela regra da rodada 11** — `0 / 0`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-nao, zero-shot (4 modelos): declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / linhas** — `0 / 4`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-nao, zero-shot (4 modelos): declarados pela regra final com Holm, familia da Tabela 1 / linhas** — `0 / 4`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-nao, zero-shot (4 modelos): declarados pela regra da rodada 11 (queda bruta so sob preto) que tambem tem queda bruta sob blur 10 % / declarados pela regra da rodada 11** — `0 / 0`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder congelado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `5 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder afinado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder afinado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `5 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder congelado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, polipo, M3AE, encoder ajuste completo: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `2 / 3 / 3`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder congelado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder afinado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder afinado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `5 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder congelado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `6 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, instrumento, M3AE, encoder ajuste completo: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `2 / 3 / 3`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), Qwen2-VL-2B, encoder congelado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), SmolVLM2-2.2B, encoder afinado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), Qwen2-VL-2B, encoder afinado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), SmolVLM2-2.2B, encoder congelado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), M3AE, encoder ajuste completo: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 3 / 3`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder congelado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 5 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 4 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder afinado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-sim, M3AE, encoder ajuste completo: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 0 / 3`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder congelado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 3 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder afinado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-nao, Qwen2-VL-2B, encoder afinado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 5 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B, encoder congelado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 4 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **HEAL-MedVQA, fechada-nao, M3AE, encoder ajuste completo: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 3 / 3`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder congelado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `3 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `1 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder afinado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `2 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `1 / 6 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE, encoder ajuste completo: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `1 / 3 / 3`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder congelado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder afinado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B, encoder afinado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B, encoder congelado: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 0 / 6`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-nao, M3AE, encoder ajuste completo: declarados pela regra final (L3, queda bruta sob preto e sob blur 10 %) / resoluveis / linhas** — `0 / 0 / 3`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, entidade pleural effusion (96 perguntas): ganho significativo / declarados pela regra final / runs** — `27 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, entidade atelectasis (87 perguntas): ganho significativo / declarados pela regra final / runs** — `0 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, entidade lung opacity (66 perguntas): ganho significativo / declarados pela regra final / runs** — `2 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, entidade cardiomegaly (58 perguntas): ganho significativo / declarados pela regra final / runs** — `0 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, entidade edema (45 perguntas): ganho significativo / declarados pela regra final / runs** — `12 / 3 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim, entidade vascular congestion (23 perguntas): ganho significativo / declarados pela regra final / runs** — `23 / 1 / 27`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, polipo: Delta preto maximo entre os 24 declarados pela regra final / maximo entre os 27 (pp)** — `+26.2 / +26.2`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Kvasir-VQA-x1, instrumento: Delta preto maximo entre os 25 declarados pela regra final / maximo entre os 27 (pp)** — `+47.1 / +47.1`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>
- **Medical-Diff-VQA, fechada-sim: Delta preto maximo entre os 8 declarados pela regra final / maximo entre os 27 (pp)** — `+6.8 / +6.8`  
  <sub>v7_artigo1/analysis/rodada14.json · sha256 c4dc3cc361c4</sub>

## S19. Regra final com blur 4 % (rodada 15)

- **regra final com blur 4 % (regra)** — `regra final com blur 4 %: Delta preto, Delta blur 4 %, image gain, queda bruta sob preto e queda bruta sob blur 4 %, todos com IC > 0; mesmas replicas; HEAL-MedVQA sem QWEN2VL_DORA_HEAL_seed2 (adapter do retreino); zero-shot sem predicoes sob blur 4 %`  
  <sub>v7_artigo1/analysis/rodada15.json · sha256 ff8d2c365dd0</sub>
- **Kvasir-VQA-x1, polipo: declarados pela regra final com blur 4 % / declarados com blur 4 % e queda bruta so sob preto (S14) / runs** — `9 / 13 / 27`  
  <sub>v7_artigo1/analysis/rodada15.json · sha256 ff8d2c365dd0</sub>
- **Kvasir-VQA-x1, polipo, QWEN2VL_LORA_KVASIR_seed0: sai da regra final com blur 4 % so pela queda bruta sob blur 4 %: Acc(C0) - Acc(T blur 4 %) [IC] (pp)** — `+2.4 [+0.0, +4.7]`  
  <sub>v7_artigo1/analysis/rodada15.json · sha256 ff8d2c365dd0</sub>
- **Kvasir-VQA-x1, polipo, QWEN2VL_DORA_KVASIR_seed1: sai da regra final com blur 4 % so pela queda bruta sob blur 4 %: Acc(C0) - Acc(T blur 4 %) [IC] (pp)** — `+1.6 [-0.8, +4.2]`  
  <sub>v7_artigo1/analysis/rodada15.json · sha256 ff8d2c365dd0</sub>
- **Kvasir-VQA-x1, polipo, SMOLVLM_DORA_FT_KVASIR_seed1: sai da regra final com blur 4 % so pela queda bruta sob blur 4 %: Acc(C0) - Acc(T blur 4 %) [IC] (pp)** — `+2.9 [-0.2, +5.8]`  
  <sub>v7_artigo1/analysis/rodada15.json · sha256 ff8d2c365dd0</sub>
- **Kvasir-VQA-x1, polipo, QWEN2VL_DORA_VT_KVASIR_seed2: sai da regra final com blur 4 % so pela queda bruta sob blur 4 %: Acc(C0) - Acc(T blur 4 %) [IC] (pp)** — `+3.0 [+0.0, +5.9]`  
  <sub>v7_artigo1/analysis/rodada15.json · sha256 ff8d2c365dd0</sub>
- **Kvasir-VQA-x1, instrumento: declarados pela regra final com blur 4 % / declarados com blur 4 % e queda bruta so sob preto (S14) / runs** — `23 / 23 / 27`  
  <sub>v7_artigo1/analysis/rodada15.json · sha256 ff8d2c365dd0</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates): declarados pela regra final com blur 4 % / declarados com blur 4 % e queda bruta so sob preto (S14) / runs** — `0 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada15.json · sha256 ff8d2c365dd0</sub>
- **HEAL-MedVQA, fechada-sim: declarados pela regra final com blur 4 % / declarados com blur 4 % e queda bruta so sob preto (S14) / runs** — `0 / 0 / 26`  
  <sub>v7_artigo1/analysis/rodada15.json · sha256 ff8d2c365dd0</sub>
- **HEAL-MedVQA, fechada-nao: declarados pela regra final com blur 4 % / declarados com blur 4 % e queda bruta so sob preto (S14) / runs** — `0 / 0 / 26`  
  <sub>v7_artigo1/analysis/rodada15.json · sha256 ff8d2c365dd0</sub>
- **Medical-Diff-VQA, fechada-sim: declarados pela regra final com blur 4 % / declarados com blur 4 % e queda bruta so sob preto (S14) / runs** — `7 / 7 / 27`  
  <sub>v7_artigo1/analysis/rodada15.json · sha256 ff8d2c365dd0</sub>
- **Medical-Diff-VQA, fechada-nao: declarados pela regra final com blur 4 % / declarados com blur 4 % e queda bruta so sob preto (S14) / runs** — `0 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada15.json · sha256 ff8d2c365dd0</sub>
- **regra final com blur 4 %, zero-shot** — `sem predicoes sob blur 4 % para os 12 pares modelo x base (nada a contar)`  
  <sub>v7_artigo1/analysis/rodada15.json · sha256 ff8d2c365dd0</sub>

## S20. Holm como teste de intersecao-uniao (rodada 16)

- **procedimento das rodadas 8, 9 e 14 (Holm por condicao)** — `para cada run e cada condicao separadamente, os p unilaterais bootstrap das classes da familia foram ajustados por Holm; o run foi declarado se todas as condicoes passaram com p ajustado < 0,025 (Holm por condicao, depois a conjuncao); nao era IUT`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **IUT (regra)** — `IUT: p do run = maximo dos cinco p unilaterais; Holm por run sobre as classes da Tabela 1 do benchmark; declarado se p ajustado < 0,025`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **Kvasir-VQA-x1, polipo, afinados: declarados pela regra final com IUT e Holm / com Holm por condicao (rodada 14) / sem Holm / runs** — `24 / 24 / 24 / 27`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **Kvasir-VQA-x1, polipo, zero-shot (4 modelos): declarados pela regra final com IUT e Holm / com Holm por condicao (rodada 14) / sem Holm / runs** — `2 / 2 / 2 / 4`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **Kvasir-VQA-x1, instrumento, afinados: declarados pela regra final com IUT e Holm / com Holm por condicao (rodada 14) / sem Holm / runs** — `25 / 25 / 25 / 27`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **Kvasir-VQA-x1, instrumento, zero-shot (4 modelos): declarados pela regra final com IUT e Holm / com Holm por condicao (rodada 14) / sem Holm / runs** — `2 / 2 / 2 / 4`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), afinados: declarados pela regra final com IUT e Holm / com Holm por condicao (rodada 14) / sem Holm / runs** — `0 / 0 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), zero-shot (4 modelos): declarados pela regra final com IUT e Holm / com Holm por condicao (rodada 14) / sem Holm / runs** — `0 / 0 / 0 / 4`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **HEAL-MedVQA, fechada-sim, afinados: declarados pela regra final com IUT e Holm / com Holm por condicao (rodada 14) / sem Holm / runs** — `0 / 0 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **HEAL-MedVQA, fechada-sim, zero-shot (4 modelos): declarados pela regra final com IUT e Holm / com Holm por condicao (rodada 14) / sem Holm / runs** — `0 / 0 / 0 / 4`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **HEAL-MedVQA, fechada-nao, afinados: declarados pela regra final com IUT e Holm / com Holm por condicao (rodada 14) / sem Holm / runs** — `0 / 0 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **HEAL-MedVQA, fechada-nao, zero-shot (4 modelos): declarados pela regra final com IUT e Holm / com Holm por condicao (rodada 14) / sem Holm / runs** — `1 / 1 / 1 / 4`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **Medical-Diff-VQA, fechada-sim, afinados: declarados pela regra final com IUT e Holm / com Holm por condicao (rodada 14) / sem Holm / runs** — `5 / 5 / 8 / 27`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **Medical-Diff-VQA, fechada-sim, zero-shot (4 modelos): declarados pela regra final com IUT e Holm / com Holm por condicao (rodada 14) / sem Holm / runs** — `2 / 2 / 2 / 4`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **Medical-Diff-VQA, fechada-nao, afinados: declarados pela regra final com IUT e Holm / com Holm por condicao (rodada 14) / sem Holm / runs** — `0 / 0 / 0 / 27`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **Medical-Diff-VQA, fechada-nao, zero-shot (4 modelos): declarados pela regra final com IUT e Holm / com Holm por condicao (rodada 14) / sem Holm / runs** — `0 / 0 / 0 / 4`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **runs cuja declaracao muda entre IUT com Holm e Holm por condicao** — `0`  
  <sub>v7_artigo1/analysis/rodada16.json · sha256 f3ff43fea900</sub>
- **alteracao de pixels dentro do alvo (definicao, rodada 13)** — `por par imagem-alvo, media, sobre os pixels da mascara-alvo, da diferenca absoluta entre a imagem intacta e a preenchida, na escala 0-255, com a media dos tres canais; mediana [IQR] entre os pares; mascara = uniao dos pixels alterados pelo preto, pelo blur 10 % ou pelo blur 4 %`  
  <sub>v7_artigo1/analysis/rodada13.json · sha256 614776c7a592</sub>

## S21. Baseline sem imagem com DoRA (rodada 17; base do baseline pareado, ver S22)

- **baseline sem imagem DoRA (regra)** — `mesma receita do baseline sem imagem LoRA (adaptador so no modelo de linguagem, rank 16, alfa 32, projecoes de atencao, lr 2e-4, 3 epocas, batch 4 x 4, mesmo split, mesma entrada sem imagem, mesmos scripts), trocando so LoRA por DoRA; G_DoRA = Acc(intacta) - Acc(baseline sem imagem DoRA da mesma familia e semente); criterio (iv) = Delta preto e Delta blur 10 % e ganho (IC > 0); (v) = (iv) e queda bruta sob preto e sob blur 10 % (IC > 0)`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B: acuracia do baseline sem imagem LoRA / DoRA, media (minimo – maximo) entre sementes (%)** — `28.8 (28.8 – 28.8) / 28.8 (28.8 – 28.8)`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B: acuracia do baseline sem imagem LoRA / DoRA, media (minimo – maximo) entre sementes (%)** — `27.6 (27.6 – 27.6) / 27.6 (27.6 – 27.6)`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B: acuracia do baseline sem imagem LoRA / DoRA, media (minimo – maximo) entre sementes (%)** — `0.0 (0.0 – 0.0) / 0.0 (0.0 – 0.0)`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B: acuracia do baseline sem imagem LoRA / DoRA, media (minimo – maximo) entre sementes (%)** — `0.0 (0.0 – 0.0) / 0.0 (0.0 – 0.0)`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), Qwen2-VL-2B: acuracia do baseline sem imagem LoRA / DoRA, media (minimo – maximo) entre sementes (%)** — `79.9 (79.9 – 79.9) / 79.9 (79.9 – 79.9)`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), SmolVLM2-2.2B: acuracia do baseline sem imagem LoRA / DoRA, media (minimo – maximo) entre sementes (%)** — `79.9 (79.9 – 79.9) / 79.9 (79.9 – 79.9)`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B: acuracia do baseline sem imagem LoRA / DoRA, media (minimo – maximo) entre sementes (%)** — `91.7 (90.6 – 92.8) / 91.5 (90.9 – 92.4)`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B: acuracia do baseline sem imagem LoRA / DoRA, media (minimo – maximo) entre sementes (%)** — `89.8 (89.0 – 90.7) / 89.6 (88.9 – 90.6)`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **HEAL-MedVQA, fechada-nao, Qwen2-VL-2B: acuracia do baseline sem imagem LoRA / DoRA, media (minimo – maximo) entre sementes (%)** — `79.6 (78.4 – 80.7) / 79.3 (78.4 – 80.5)`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **HEAL-MedVQA, fechada-nao, SmolVLM2-2.2B: acuracia do baseline sem imagem LoRA / DoRA, media (minimo – maximo) entre sementes (%)** — `80.7 (79.7 – 81.5) / 81.1 (80.3 – 81.8)`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B: acuracia do baseline sem imagem LoRA / DoRA, media (minimo – maximo) entre sementes (%)** — `68.0 (65.5 – 69.3) / 68.0 (65.0 – 69.5)`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B: acuracia do baseline sem imagem LoRA / DoRA, media (minimo – maximo) entre sementes (%)** — `64.8 (62.5 – 68.6) / 62.8 (62.3 – 63.0)`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Medical-Diff-VQA, fechada-nao, Qwen2-VL-2B: acuracia do baseline sem imagem LoRA / DoRA, media (minimo – maximo) entre sementes (%)** — `80.6 (79.1 – 82.1) / 80.6 (77.6 – 83.6)`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Medical-Diff-VQA, fechada-nao, SmolVLM2-2.2B: acuracia do baseline sem imagem LoRA / DoRA, media (minimo – maximo) entre sementes (%)** — `80.1 (79.1 – 80.6) / 82.6 (82.1 – 83.6)`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Kvasir-VQA-x1, polipo: G atual - G_DoRA nos 12 runs DoRA, media / minimo / maximo (pp)** — `+0.0 / -0.0 / -0.0`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Kvasir-VQA-x1, instrumento: G atual - G_DoRA nos 12 runs DoRA, media / minimo / maximo (pp)** — `+0.0 / -0.0 / -0.0`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates): G atual - G_DoRA nos 12 runs DoRA, media / minimo / maximo (pp)** — `+0.0 / -0.0 / -0.0`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **HEAL-MedVQA, fechada-sim: G atual - G_DoRA nos 12 runs DoRA, media / minimo / maximo (pp)** — `-0.2 / -0.4 / +0.3`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **HEAL-MedVQA, fechada-nao: G atual - G_DoRA nos 12 runs DoRA, media / minimo / maximo (pp)** — `+0.1 / -0.7 / +0.5`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Medical-Diff-VQA, fechada-sim: G atual - G_DoRA nos 12 runs DoRA, media / minimo / maximo (pp)** — `-1.0 / -5.6 / +0.5`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Medical-Diff-VQA, fechada-nao: G atual - G_DoRA nos 12 runs DoRA, media / minimo / maximo (pp)** — `+1.2 / -3.0 / +3.0`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Kvasir-VQA-x1, polipo: criterio (iv) dois preenchimentos com ganho significativo, atual / com G_DoRA nos runs DoRA (linhas)** — `25 / 25 de 27`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Kvasir-VQA-x1, polipo: criterio (v) declarado pela regra final, atual / com G_DoRA nos runs DoRA (linhas)** — `24 / 24 de 27`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Kvasir-VQA-x1, instrumento: criterio (iv) dois preenchimentos com ganho significativo, atual / com G_DoRA nos runs DoRA (linhas)** — `25 / 25 de 27`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Kvasir-VQA-x1, instrumento: criterio (v) declarado pela regra final, atual / com G_DoRA nos runs DoRA (linhas)** — `25 / 25 de 27`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates): criterio (iv) dois preenchimentos com ganho significativo, atual / com G_DoRA nos runs DoRA (linhas)** — `0 / 0 de 27`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates): criterio (v) declarado pela regra final, atual / com G_DoRA nos runs DoRA (linhas)** — `0 / 0 de 27`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **HEAL-MedVQA, fechada-sim: criterio (iv) dois preenchimentos com ganho significativo, atual / com G_DoRA nos runs DoRA (linhas)** — `0 / 0 de 27`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **HEAL-MedVQA, fechada-sim: criterio (v) declarado pela regra final, atual / com G_DoRA nos runs DoRA (linhas)** — `0 / 0 de 27`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **HEAL-MedVQA, fechada-nao: criterio (iv) dois preenchimentos com ganho significativo, atual / com G_DoRA nos runs DoRA (linhas)** — `0 / 0 de 27`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **HEAL-MedVQA, fechada-nao: criterio (v) declarado pela regra final, atual / com G_DoRA nos runs DoRA (linhas)** — `0 / 0 de 27`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Medical-Diff-VQA, fechada-sim: criterio (iv) dois preenchimentos com ganho significativo, atual / com G_DoRA nos runs DoRA (linhas)** — `12 / 12 de 27`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Medical-Diff-VQA, fechada-sim: criterio (v) declarado pela regra final, atual / com G_DoRA nos runs DoRA (linhas)** — `8 / 8 de 27`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Medical-Diff-VQA, fechada-nao: criterio (iv) dois preenchimentos com ganho significativo, atual / com G_DoRA nos runs DoRA (linhas)** — `0 / 0 de 27`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **Medical-Diff-VQA, fechada-nao: criterio (v) declarado pela regra final, atual / com G_DoRA nos runs DoRA (linhas)** — `0 / 0 de 27`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>
- **runs DoRA cujo estado nos criterios (iv) ou (v) muda com G_DoRA** — `0`  
  <sub>v7_artigo1/analysis/rodada17.json · sha256 9fa1ca5e4730</sub>

## S22. Ganho de imagem com baseline sem imagem do mesmo adaptador (rodada 19)

- **ganho de imagem pareado (regra, decisao do Claudio de 22/10/2026)** — `G pareado: runs LoRA -> baseline LoRA; runs DoRA -> baseline DoRA (rodada 17); M3AE -> imagem cinza; IC 95 % por imagem, p unilateral bootstrap; oclusoes, C, Delta_nec, replicas e normalizacao inalterados`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, polipo: criterios (i) / (ii) / (iii) / (iv) / (v), ganho pareado (linhas de 27)** — `27 / 27 / 25 / 25 / 24`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, polipo: ganho de imagem pareado, minimo – maximo entre as 27 linhas (pp); linhas com ganho significativo** — `+29.3 – +35.9; 27/27`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, polipo: declarados pela regra final com IUT e Holm, ganho pareado (linhas de 27)** — `24`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, instrumento: criterios (i) / (ii) / (iii) / (iv) / (v), ganho pareado (linhas de 27)** — `27 / 26 / 25 / 25 / 25`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, instrumento: ganho de imagem pareado, minimo – maximo entre as 27 linhas (pp); linhas com ganho significativo** — `+68.2 – +77.1; 27/27`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, instrumento: declarados pela regra final com IUT e Holm, ganho pareado (linhas de 27)** — `25`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates): criterios (i) / (ii) / (iii) / (iv) / (v), ganho pareado (linhas de 27)** — `25 / 0 / 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates): ganho de imagem pareado, minimo – maximo entre as 27 linhas (pp); linhas com ganho significativo** — `+17.6 – +18.7; 27/27`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates): declarados pela regra final com IUT e Holm, ganho pareado (linhas de 27)** — `0`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **HEAL-MedVQA, fechada-sim: criterios (i) / (ii) / (iii) / (iv) / (v), ganho pareado (linhas de 27)** — `0 / 1 / 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **HEAL-MedVQA, fechada-sim: ganho de imagem pareado, minimo – maximo entre as 27 linhas (pp); linhas com ganho significativo** — `-3.0 – +5.3; 21/27`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **HEAL-MedVQA, fechada-sim: declarados pela regra final com IUT e Holm, ganho pareado (linhas de 27)** — `0`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **HEAL-MedVQA, fechada-nao: criterios (i) / (ii) / (iii) / (iv) / (v), ganho pareado (linhas de 27)** — `27 / 0 / 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **HEAL-MedVQA, fechada-nao: ganho de imagem pareado, minimo – maximo entre as 27 linhas (pp); linhas com ganho significativo** — `-1.4 – +14.4; 21/27`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **HEAL-MedVQA, fechada-nao: declarados pela regra final com IUT e Holm, ganho pareado (linhas de 27)** — `0`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Medical-Diff-VQA, fechada-sim: criterios (i) / (ii) / (iii) / (iv) / (v), ganho pareado (linhas de 27)** — `18 / 18 / 12 / 12 / 8`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Medical-Diff-VQA, fechada-sim: ganho de imagem pareado, minimo – maximo entre as 27 linhas (pp); linhas com ganho significativo** — `+5.9 – +21.2; 27/27`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Medical-Diff-VQA, fechada-sim: declarados pela regra final com IUT e Holm, ganho pareado (linhas de 27)** — `5`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Medical-Diff-VQA, fechada-nao: criterios (i) / (ii) / (iii) / (iv) / (v), ganho pareado (linhas de 27)** — `0 / 0 / 0 / 0 / 0`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Medical-Diff-VQA, fechada-nao: ganho de imagem pareado, minimo – maximo entre as 27 linhas (pp); linhas com ganho significativo** — `-11.9 – +3.0; 0/27`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Medical-Diff-VQA, fechada-nao: declarados pela regra final com IUT e Holm, ganho pareado (linhas de 27)** — `0`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder congelado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+29.9 (0.5); 5/6/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder afinado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+34.5 (0.7); 6/6/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder afinado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+35.1 (0.6); 5/6/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder congelado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+30.7 (0.4); 6/6/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, polipo, M3AE, encoder ajuste completo: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+30.8 (0.4); 2/3/3`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder congelado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+72.2 (0.8); 6/6/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder afinado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+74.8 (0.8); 6/6/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder afinado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+75.0 (1.2); 5/6/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder congelado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+70.3 (1.3); 6/6/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, instrumento, M3AE, encoder ajuste completo: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+70.5 (0.5); 2/3/3`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder congelado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+2.7 (1.0); 0/5/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+2.6 (1.3); 0/4/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder afinado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+4.0 (1.0); 0/6/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+3.3 (0.6); 0/6/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **HEAL-MedVQA, fechada-sim, M3AE, encoder ajuste completo: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `-1.4 (2.2); 0/0/3`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder congelado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+8.1 (2.0); 3/6/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+16.8 (2.4); 1/6/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder afinado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+11.1 (3.6); 2/6/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+12.3 (2.3); 1/6/6`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE, encoder ajuste completo: ganho de imagem pareado, media (DP) (pp); Declared (nec. / sig. gain / runs)** — `+18.4 (4.6); 1/3/3`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, polipo: regra final com blur 4 % e ganho pareado: declarados / runs** — `9 / 27`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, instrumento: regra final com blur 4 % e ganho pareado: declarados / runs** — `23 / 27`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates): regra final com blur 4 % e ganho pareado: declarados / runs** — `0 / 27`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **HEAL-MedVQA, fechada-sim: regra final com blur 4 % e ganho pareado: declarados / runs** — `0 / 26`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **HEAL-MedVQA, fechada-nao: regra final com blur 4 % e ganho pareado: declarados / runs** — `0 / 26`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Medical-Diff-VQA, fechada-sim: regra final com blur 4 % e ganho pareado: declarados / runs** — `7 / 27`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Medical-Diff-VQA, fechada-nao: regra final com blur 4 % e ganho pareado: declarados / runs** — `0 / 27`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Medical-Diff-VQA, fechada-sim, ganho pareado: linhas em (ii) / (iii) / (iv) / (v)** — `18 / 12 / 12 / 8`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>
- **Medical-Diff-VQA, fechada-sim, ganho pareado: tirados pelo criterio de dois preenchimentos / pela condicao do ganho / pela queda bruta** — `6 / 0 / 4`  
  <sub>v7_artigo1/analysis/rodada19.json · sha256 87508fa56a5b</sub>

## S23. Baseline sem imagem do M3AE: M3AE sem imagem (rodada 20)

- **ganho de imagem (regra, decisao do Claudio de 23/10/2026)** — `G = A_int - A_text; LoRA -> baseline LoRA; DoRA -> baseline DoRA (rodada 17); M3AE -> M3AE sem imagem (variante sem caminho de imagem); IC 95 % por imagem, p unilateral bootstrap; oclusoes, C, Delta_nec, replicas e normalizacao inalterados`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **predicoes do M3AE sem imagem, KVASIR|seed0: sha256** — `c3546b51566a6925`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **predicoes do M3AE sem imagem, KVASIR|seed1: sha256** — `14f77b962eaa555e`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **predicoes do M3AE sem imagem, KVASIR|seed2: sha256** — `a7582f325e86cffc`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **predicoes do M3AE sem imagem, HEAL|seed0: sha256** — `69f9644270b9d602`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **predicoes do M3AE sem imagem, HEAL|seed1: sha256** — `48492d6f2f0bfc62`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **predicoes do M3AE sem imagem, HEAL|seed2: sha256** — `0727bc52aa77f23f`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **predicoes do M3AE sem imagem, MIMIC|seed0: sha256** — `dc7217e4e4736c8f`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **predicoes do M3AE sem imagem, MIMIC|seed1: sha256** — `d68e8fff4cdfd413`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **predicoes do M3AE sem imagem, MIMIC|seed2: sha256** — `6c1a519657f6902e`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, polipo, M3AE_KVASIR_seed0: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+31.2 [+28.5, +33.7], p = 0.0000; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, instrumento, M3AE_KVASIR_seed0: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+71.0 [+65.7, +76.1], p = 0.0000; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), M3AE_KVASIR_seed0: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+18.3 [+15.4, +20.8], p = 0.0000; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, polipo, M3AE_KVASIR_seed1: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+30.4 [+27.7, +33.2], p = 0.0000; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, instrumento, M3AE_KVASIR_seed1: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+70.4 [+65.4, +75.2], p = 0.0000; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), M3AE_KVASIR_seed1: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+17.9 [+15.0, +20.5], p = 0.0000; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, polipo, M3AE_KVASIR_seed2: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+30.9 [+28.1, +33.6], p = 0.0000; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, instrumento, M3AE_KVASIR_seed2: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+70.1 [+65.2, +74.9], p = 0.0000; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates), M3AE_KVASIR_seed2: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+18.3 [+15.4, +20.9], p = 0.0000; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-sim, M3AE_HEAL_seed0: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `-2.0 [-4.5, +0.6], p = 0.9375; nao`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-nao, M3AE_HEAL_seed0: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+12.8 [+10.0, +15.6], p = 0.0000; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-sim, M3AE_HEAL_seed1: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+3.4 [+0.6, +6.1], p = 0.0090; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-nao, M3AE_HEAL_seed1: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+4.4 [+1.3, +7.5], p = 0.0015; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-sim, M3AE_HEAL_seed2: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `-4.5 [-7.2, -1.8], p = 0.9995; nao`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-nao, M3AE_HEAL_seed2: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+11.8 [+9.1, +14.7], p = 0.0000; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE_MIMIC_seed0: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+21.9 [+17.5, +26.3], p = 0.0000; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-nao, M3AE_MIMIC_seed0: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `-11.9 [-21.1, -3.7], p = 0.9995; nao`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE_MIMIC_seed1: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+12.6 [+8.6, +16.8], p = 0.0000; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-nao, M3AE_MIMIC_seed1: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+13.4 [+3.3, +23.9], p = 0.0045; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE_MIMIC_seed2: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+13.1 [+8.7, +17.6], p = 0.0000; sim`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-nao, M3AE_MIMIC_seed2: ganho de imagem com M3AE sem imagem (pp), IC 95 %, p; significativo** — `+3.0 [-4.3, +10.4], p = 0.2740; nao`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, M3AE_KVASIR_seed0: acuracia sem imagem / cinza / diferenca nos itens do artigo 1 (%, pp; n itens)** — `39.70 / 39.70 / +0.0 (2121)`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, M3AE_KVASIR_seed1: acuracia sem imagem / cinza / diferenca nos itens do artigo 1 (%, pp; n itens)** — `39.70 / 39.70 / +0.0 (2121)`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, M3AE_KVASIR_seed2: acuracia sem imagem / cinza / diferenca nos itens do artigo 1 (%, pp; n itens)** — `39.70 / 39.70 / +0.0 (2121)`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, M3AE_HEAL_seed0: acuracia sem imagem / cinza / diferenca nos itens do artigo 1 (%, pp; n itens)** — `85.27 / 84.58 / +0.7 (1446)`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, M3AE_HEAL_seed1: acuracia sem imagem / cinza / diferenca nos itens do artigo 1 (%, pp; n itens)** — `85.20 / 84.72 / +0.5 (1446)`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, M3AE_HEAL_seed2: acuracia sem imagem / cinza / diferenca nos itens do artigo 1 (%, pp; n itens)** — `85.41 / 85.20 / +0.2 (1446)`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, M3AE_MIMIC_seed0: acuracia sem imagem / cinza / diferenca nos itens do artigo 1 (%, pp; n itens)** — `54.45 / 53.83 / +0.6 (1594)`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, M3AE_MIMIC_seed1: acuracia sem imagem / cinza / diferenca nos itens do artigo 1 (%, pp; n itens)** — `53.76 / 52.95 / +0.8 (1594)`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, M3AE_MIMIC_seed2: acuracia sem imagem / cinza / diferenca nos itens do artigo 1 (%, pp; n itens)** — `54.14 / 54.96 / -0.8 (1594)`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, polipo: criterios (i) / (ii) / (iii) / (iv) / (v), M3AE sem imagem (linhas de 27); linhas com ganho significativo** — `27 / 27 / 25 / 25 / 24; 27/27`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, polipo: ganho de imagem, minimo – maximo entre as 27 linhas (pp), M3AE sem imagem** — `+29.3 – +35.9`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, polipo: declarados pela regra final com IUT e Holm, M3AE sem imagem (linhas de 27)** — `24`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, instrumento: criterios (i) / (ii) / (iii) / (iv) / (v), M3AE sem imagem (linhas de 27); linhas com ganho significativo** — `27 / 26 / 25 / 25 / 25; 27/27`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, instrumento: ganho de imagem, minimo – maximo entre as 27 linhas (pp), M3AE sem imagem** — `+68.2 – +77.1`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, instrumento: declarados pela regra final com IUT e Holm, M3AE sem imagem (linhas de 27)** — `25`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates): criterios (i) / (ii) / (iii) / (iv) / (v), M3AE sem imagem (linhas de 27); linhas com ganho significativo** — `25 / 0 / 0 / 0 / 0; 27/27`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates): ganho de imagem, minimo – maximo entre as 27 linhas (pp), M3AE sem imagem** — `+17.6 – +18.7`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates): declarados pela regra final com IUT e Holm, M3AE sem imagem (linhas de 27)** — `0`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-sim: criterios (i) / (ii) / (iii) / (iv) / (v), M3AE sem imagem (linhas de 27); linhas com ganho significativo** — `0 / 1 / 0 / 0 / 0; 22/27`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-sim: ganho de imagem, minimo – maximo entre as 27 linhas (pp), M3AE sem imagem** — `-4.5 – +5.3`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-sim: declarados pela regra final com IUT e Holm, M3AE sem imagem (linhas de 27)** — `0`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-nao: criterios (i) / (ii) / (iii) / (iv) / (v), M3AE sem imagem (linhas de 27); linhas com ganho significativo** — `27 / 0 / 0 / 0 / 0; 21/27`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-nao: ganho de imagem, minimo – maximo entre as 27 linhas (pp), M3AE sem imagem** — `-1.4 – +12.8`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-nao: declarados pela regra final com IUT e Holm, M3AE sem imagem (linhas de 27)** — `0`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-sim: criterios (i) / (ii) / (iii) / (iv) / (v), M3AE sem imagem (linhas de 27); linhas com ganho significativo** — `18 / 18 / 12 / 12 / 8; 27/27`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-sim: ganho de imagem, minimo – maximo entre as 27 linhas (pp), M3AE sem imagem** — `+5.9 – +21.9`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-sim: declarados pela regra final com IUT e Holm, M3AE sem imagem (linhas de 27)** — `5`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-nao: criterios (i) / (ii) / (iii) / (iv) / (v), M3AE sem imagem (linhas de 27); linhas com ganho significativo** — `0 / 0 / 0 / 0 / 0; 1/27`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-nao: ganho de imagem, minimo – maximo entre as 27 linhas (pp), M3AE sem imagem** — `-11.9 – +13.4`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-nao: declarados pela regra final com IUT e Holm, M3AE sem imagem (linhas de 27)** — `0`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder congelado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+29.9 (0.5); 5/6/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder afinado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+34.5 (0.7); 6/6/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, polipo, Qwen2-VL-2B, encoder afinado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+35.1 (0.6); 5/6/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, polipo, SmolVLM2-2.2B, encoder congelado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+30.7 (0.4); 6/6/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, polipo, M3AE, encoder ajuste completo: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+30.8 (0.4); 2/3/3`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder congelado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+72.2 (0.8); 6/6/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder afinado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+74.8 (0.8); 6/6/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, instrumento, Qwen2-VL-2B, encoder afinado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+75.0 (1.2); 5/6/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, instrumento, SmolVLM2-2.2B, encoder congelado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+70.3 (1.3); 6/6/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, instrumento, M3AE, encoder ajuste completo: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+70.5 (0.5); 2/3/3`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder congelado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+2.7 (1.0); 0/5/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+2.6 (1.3); 0/4/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-sim, Qwen2-VL-2B, encoder afinado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+4.0 (1.0); 0/6/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+3.3 (0.6); 0/6/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-sim, M3AE, encoder ajuste completo: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `-1.0 (4.0); 0/1/3`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder congelado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+8.1 (2.0); 3/6/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder afinado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+16.8 (2.4); 1/6/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-sim, Qwen2-VL-2B, encoder afinado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+11.1 (3.6); 2/6/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-sim, SmolVLM2-2.2B, encoder congelado: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+12.3 (2.3); 1/6/6`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE, encoder ajuste completo: ganho de imagem, media (DP) (pp); Declared (nec. / sig. gain / runs), M3AE sem imagem** — `+15.9 (5.2); 1/3/3`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, polipo: regra final com blur 4 %, M3AE sem imagem: declarados / runs** — `9 / 27`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, instrumento: regra final com blur 4 %, M3AE sem imagem: declarados / runs** — `23 / 27`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Kvasir-VQA-x1, controle negativo (3 templates): regra final com blur 4 %, M3AE sem imagem: declarados / runs** — `0 / 27`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-sim: regra final com blur 4 %, M3AE sem imagem: declarados / runs** — `0 / 26`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **HEAL-MedVQA, fechada-nao: regra final com blur 4 %, M3AE sem imagem: declarados / runs** — `0 / 26`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-sim: regra final com blur 4 %, M3AE sem imagem: declarados / runs** — `7 / 27`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-nao: regra final com blur 4 %, M3AE sem imagem: declarados / runs** — `0 / 27`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>
- **Medical-Diff-VQA, fechada-sim, M3AE sem imagem: linhas em (ii) / (iii) / (iv) / (v)** — `18 / 12 / 12 / 8`  
  <sub>v7_artigo1/analysis/rodada20.json · sha256 878e489251db</sub>

## S11. Suplemento interno (nao vai ao corpo)

- **criterio A / C (so interno) e criterio antigo (IC por pergunta), Kvasir-VQA-x1, polipo** — `A 26/27 / C 25/27 / antigo 27`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio A / C (so interno) e criterio antigo (IC por pergunta), Kvasir-VQA-x1, instrumento** — `A 25/27 / C 24/27 / antigo 26`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio A / C (so interno) e criterio antigo (IC por pergunta), Kvasir-VQA-x1, controle 'Is there text?'** — `A 0/27 / C 0/27 / antigo 0`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio A / C (so interno) e criterio antigo (IC por pergunta), Kvasir-VQA-x1, polipo secundario** — `A 26/27 / C 23/27 / antigo 26`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio A / C (so interno) e criterio antigo (IC por pergunta), Kvasir-VQA-x1, controle negativo (3 templates)** — `A 0/27 / C 0/27 / antigo 0`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio A / C (so interno) e criterio antigo (IC por pergunta), HEAL-MedVQA, fechada-sim** — `A 0/27 / C 0/27 / antigo 0`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio A / C (so interno) e criterio antigo (IC por pergunta), HEAL-MedVQA, fechada-nao** — `A 0/27 / C 0/27 / antigo 0`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio A / C (so interno) e criterio antigo (IC por pergunta), Medical-Diff-VQA, fechada-sim** — `A 16/27 / C 9/27 / antigo 16`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio A / C (so interno) e criterio antigo (IC por pergunta), Medical-Diff-VQA, fechada-nao** — `A 0/27 / C 0/27 / antigo 0`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio A / C (so interno) e criterio antigo (IC por pergunta), Medical-Diff-VQA, fechada-sim, so entidades com mapeamento exato** — `A 15/27 / C 8/27 / antigo —`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **criterio A / C (so interno) e criterio antigo (IC por pergunta), Medical-Diff-VQA, fechada-nao, so exatas** — `A 0/27 / C 0/27 / antigo —`  
  <sub>v7_artigo1/analysis/criterio.json · sha256 671f446335a2</sub>
- **doses, HEAL-MedVQA, QWEN2VL_DORA_HEAL_seed2 (fora das medias), fechada-sim: Delta 1x / 1,5x / 2x [IC] (pp)** — `+0.0 [-0.9, +0.9] / -1.2 [-2.6, +0.2] / -0.9 [-2.5, +0.5]`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **doses, HEAL-MedVQA, QWEN2VL_DORA_HEAL_seed2 (fora das medias), fechada-nao: Delta 1x / 1,5x / 2x [IC] (pp)** — `+0.6 [-1.1, +2.3] / -0.6 [-2.5, +1.2] / -4.7 [-7.0, -2.5]`  
  <sub>v7_artigo1/analysis/doses.json · sha256 275459ea2e62</sub>
- **SLAKE (fora do artigo): criterio antigo nas fechadas (E8), doenca / orgao** — `0/16 / 0/16 (folha antiga; nao recomputado nesta rodada)`  
  <sub>results/previous_sheets/numbers_isbi.md · sha256 </sub>
- **Delta normalizado (so suplemento)** — `existe em v7_txt/docs/numbers_own_floor.md e v7_mimic/docs/numbers_placebo_mimic.md; nao reproduzido aqui`  
  <sub>results/previous_sheets/numbers_own_floor.md · sha256 </sub>
