#!/usr/bin/env bash
# Runs M3AE inference on SLAKE for ONE condition (C0/C1/C2) -- fallback
# for M1 (see spec §11). Same logic as LaPA's run_condition.sh, but with
# M3AE's own conventions (data_root=data/finetune_arrows/, folder
# 'downloaded' with "ed", without LaPA's extra args).
#
# Assumes environment/colab_setup_m3ae.sh has already run and that
# harness/interventions/make_c1_blank_images.py and make_c2_shuffled_pairs.py
# have already generated the C1/C2 arrows (same schema and output location as
# LaPA's prepro, since the prepro_vqa_slack() function is identical in both
# repositories).
#
# Usage: bash harness/run_condition_m3ae.sh <C0|C1|C2> <M3AE_DIR> <RESULTS_LOG_DIR>

set -euo pipefail

CONDITION="${1:?condição obrigatória: C0, C1 ou C2}"
M3AE_DIR="${2:?caminho do repositório M3AE clonado}"
LOG_DIR="${3:?diretório onde salvar o log}"

ARROW_DIR="${M3AE_DIR}/data/finetune_arrows"
TARGET="${ARROW_DIR}/vqa_slack_test.arrow"
BACKUP="${ARROW_DIR}/vqa_slack_test.arrow.c0_backup"

# A bare `source activate lapa` (old syntax) only works on Colab
# (condacolab patches the environment to support it) -- on gpu-server-a
# (vanilla miniconda) this script, run as a new bash process, does not
# inherit functions from the shell that invoked it, so it fails with "activate: No
# such file or directory". Explicitly sourcing conda.sh + `conda activate`
# (current syntax) fixes it, with a fallback to the original `source activate`
# to preserve compatibility with Colab.
if [ -f "${LAB_ROOT}/miniconda3/etc/profile.d/conda.sh" ]; then
  source ${LAB_ROOT}/miniconda3/etc/profile.d/conda.sh
fi
conda activate lapa 2>/dev/null || source activate lapa

# main.py calls pl.loggers.WandbLogger(...) unconditionally, even with
# test_only=True. Without this, wandb tries to authenticate and hangs/fails asking for an
# API key (confirmed in a real run). We do not need external logging
# to run inference.
export WANDB_MODE=disabled

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
LOG_FILE="${LOG_DIR}/M3AE_SLAKE_${CONDITION}.log"

cd "${M3AE_DIR}"
# -u: same finding as in run_finetune_m3ae.sh -- without unbuffered stdout,
# 'python main.py | tee' prints nothing for minutes when the output is not
# an interactive terminal (the case of subprocess.run(['bash', ...]) in a
# notebook).
python -u main.py with data_root=data/finetune_arrows/ \
  num_gpus=1 num_nodes=1 \
  task_finetune_vqa_slack \
  per_gpu_batchsize=16 \
  clip16 text_roberta \
  image_size=384 \
  test_only=True \
  tokenizer=downloaded/roberta-base \
  load_path=downloaded/finetuned/vqa/slack/m3ae_finetuned_vqa_slack_84.3.ckpt \
  2>&1 | tee "${LOG_FILE}"

echo "Condição ${CONDITION} concluída. Log em ${LOG_FILE}"
