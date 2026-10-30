# Artefatos pré-computados

Saídas de scripts de `harness/prepro/` que dependem de dados brutos
só acessíveis localmente (não em Colab) — commitadas aqui pra sessões
Colab não precisarem re-gerar.

## `vqa_slack_test_pathology_labels.json`

Saída de `harness/prepro/build_slake_pathology_labels.py --modality X-Ray --location Lung`,
rodado em 21/08/2026 contra `~/Downloads/Slake1.0/{train,test,validate}.json`
(dataset bruto original do SLAKE, só existe localmente no Mac do
candidato — não em Colab, não redistribuído por licença). 130 imagens,
rótulo de patologia por `image_id`.

**Não confirmado**: se o prefixo `imgs/` das chaves bate com a coluna
`image_id` do `vqa_slack_test.arrow` real (gerado só em Colab, nunca
commitado). Confirmar isso é o primeiro passo de qualquer sessão que
for usar este arquivo — ver Task 3, Step 5 do plano
`docs/superpowers/plans/2026-08-21-kvasir-targeted-pathology-swap-condition.md`.
