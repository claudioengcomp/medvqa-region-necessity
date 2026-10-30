#!/usr/bin/env bash
# Runs LaPA inference on SLAKE for ONE condition (C0/C1/C2), without
# modifying any file of the LaPA repository -- it only swaps which .arrow
# is in the expected place before calling main.py. Isolates only the SLAKE section
# of the original test.sh (running the whole test.sh would also try VQA-RAD and
# MedVQA-2019, which we do not have).
#
# Assumes environment/colab_setup.sh has already run ('lapa' environment active,
# checkpoints/data in place) and that harness/interventions/make_c1_blank_images.py
# and make_c2_shuffled_pairs.py have already generated the C1/C2 arrows.
#
# Usage: bash harness/run_condition.sh <C0|C1|C2> <LAPA_DIR> <RESULTS_LOG_DIR>

set -euo pipefail

CONDITION="${1:?condição obrigatória: C0, C1 ou C2}"
LAPA_DIR="${2:?caminho do repositório LaPA clonado}"
LOG_DIR="${3:?diretório onde salvar o log}"

source activate lapa

# main.py (same code base as M3AE) calls pl.loggers.WandbLogger(...)
# unconditionally, even with test_only=True. Without this, wandb tries to
# authenticate and hangs/fails asking for an API key (confirmed in a real run on
# the M3AE fallback, same main.py/stack). We do not need external logging
# to run inference.
export WANDB_MODE=disabled

ARROW_DIR="${LAPA_DIR}/data/finetune_arrows"
TARGET="${ARROW_DIR}/vqa_slack_test.arrow"
BACKUP="${ARROW_DIR}/vqa_slack_test.arrow.c0_backup"

if [ ! -f "${BACKUP}" ]; then
  cp "${TARGET}" "${BACKUP}"
fi

case "${CONDITION}" in
  C0) SOURCE="${BACKUP}" ;;
  C1) SOURCE="${ARROW_DIR}/vqa_slack_test_c1.arrow" ;;
  C2) SOURCE="${ARROW_DIR}/vqa_slack_test_c2.arrow" ;;
  *) echo "ERRO: condição inválida: ${CONDITION} (use C0, C1 ou C2)" >&2; exit 1 ;;
esac

if [ ! -f "${SOURCE}" ]; then
  echo "ERRO: ${SOURCE} não existe. Gere as condições C1/C2 antes:" >&2
  echo "  python -m harness.interventions.make_c1_blank_images --input ${BACKUP} --output ${ARROW_DIR}/vqa_slack_test_c1.arrow" >&2
  echo "  python -m harness.interventions.make_c2_shuffled_pairs --input ${BACKUP} --output ${ARROW_DIR}/vqa_slack_test_c2.arrow" >&2
  exit 1
fi

cp "${SOURCE}" "${TARGET}"

mkdir -p "${LOG_DIR}"
LOG_FILE="${LOG_DIR}/LaPA_SLAKE_${CONDITION}.log"

cd "${LAPA_DIR}"
python main.py with data_root=data/ \
  num_gpus=1 num_nodes=1 \
  task_finetune_vqa_slack \
  per_gpu_batchsize=16 \
  clip16 text_roberta \
  image_size=384 \
  test_only=True \
  tokenizer=download/roberta-base \
  ans_token_path=download/external_data/SLAKE/ans_tokenizer.pt \
  ans_tokenizer_dict_path=download/external_data/SLAKE/ans_tokenizer_dict.pkl \
  adj_feat_path=download/external_data/adj_matrix.pt \
  organ_disease_feat=download/external_data/organ_disease_info.pt \
  latent_prompt_size=32 \
  load_path=download/checkpoints/SLAKE_best.ckpt \
  2>&1 | tee "${LOG_FILE}"

echo "Condição ${CONDITION} concluída. Log em ${LOG_FILE}"
