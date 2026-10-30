#!/usr/bin/env bash
# Trains M3AE from scratch starting from the pre-trained checkpoint
# (downloaded/pretrained/m3ae.ckpt) for ONE dataset -- items 3 (SLAKE,
# 4th independent seed) and 4 (VQA-RAD, 2nd dataset) of the extended scope.
#
# Unlike harness/run_extract_predictions_m3ae.sh (which only runs
# inference, without WandbLogger): this path runs the REAL main.py, which
# builds a pl.loggers.WandbLogger(...) unconditionally -- that is why
# WANDB_MODE=disabled is required here (same bug documented in
# HANDOFF_P0_Execucao_Harness.md §1.3, item 4).
#
# At the end of training, main.py already runs trainer.test(ckpt_path="best", ...)
# by itself (default behaviour when "finetune" is in exp_name and
# test_only=False) -- we do not need to call test separately here. Use
# harness/find_best_checkpoint.py afterwards to locate the saved file.
#
# Real-cost instrumentation (wall-clock time + peak GPU memory) --
# resolves, on the M3AE side, the same pending item already resolved on the generative side
# (Task 5 of the Kvasir integration plan). Does NOT use
# torch.cuda.max_memory_allocated(): that counter is per PROCESS, and
# `python main.py` runs inside here (after 'source activate lapa'),
# in a different process from whoever CALLS this script -- a torch.cuda counter
# from outside would see nothing. Instead, it polls `nvidia-smi` every 5s
# in a background process during the whole training and takes the peak -- it measures the
# whole physical device, which is safe on Colab (1 GPU, exclusive use
# by this session).
#
# Usage: bash harness/run_finetune_m3ae.sh <task_finetune_vqa_slack|task_finetune_vqa_vqa_rad|task_finetune_vqa_kvasir> \
#          <M3AE_DIR> <RESULTS_LOG_DIR> [extra Sacred args, e.g. clip_resizedcrop]

set -euo pipefail

TASK="${1:?named config obrigatório: task_finetune_vqa_slack, task_finetune_vqa_vqa_rad ou task_finetune_vqa_kvasir}"
M3AE_DIR="${2:?caminho do repositório M3AE clonado}"
LOG_DIR="${3:?diretório onde salvar o log}"
shift 3
EXTRA_ARGS=("$@")

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
export WANDB_MODE=disabled

mkdir -p "${LOG_DIR}"
LOG_FILE="${LOG_DIR}/finetune_${TASK}.log"
GPU_MEM_LOG="${LOG_DIR}/finetune_${TASK}_gpu_mem.log"
COST_FILE="${LOG_DIR}/finetune_${TASK}_cost.json"

cd "${M3AE_DIR}"

: > "${GPU_MEM_LOG}"
( while true; do
    nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits >> "${GPU_MEM_LOG}" 2>/dev/null
    sleep 5
  done ) &
GPU_POLL_PID=$!
trap 'kill "${GPU_POLL_PID}" 2>/dev/null || true' EXIT

_start_ts=$(date +%s)
# python -u (unbuffered): without it, Python's stdout becomes
# block-buffered as soon as it stops being an interactive terminal (here, the
# other end is 'tee') -- real finding in execution (Colab, 22/08/2026): the
# notebook cell printed nothing for minutes, ambiguous whether it was
# stuck or just buffered, with no way to check without interrupting (Colab only
# runs one cell at a time). With -u, each line appears as soon as it is
# printed, both in the cell and in LOG_FILE.
python -u main.py with data_root=data/finetune_arrows/ \
  num_gpus=1 num_nodes=1 \
  "${TASK}" \
  per_gpu_batchsize=16 \
  clip16 text_roberta \
  image_size=384 \
  tokenizer=downloaded/roberta-base \
  load_path=downloaded/pretrained/m3ae.ckpt \
  "${EXTRA_ARGS[@]}" \
  2>&1 | tee "${LOG_FILE}"
_end_ts=$(date +%s)

python3 -c "
import json
train_wall_time_s = ${_end_ts} - ${_start_ts}
try:
    peak_mem_mib = max(int(l) for l in open('${GPU_MEM_LOG}') if l.strip())
except ValueError:
    peak_mem_mib = 0  # nvidia-smi unavailable / empty log -- must not stop the training because of this
json.dump({
    'run_name': '${TASK}',
    'train_wall_time_s': train_wall_time_s,
    'train_peak_memory_gb': round(peak_mem_mib / 1024, 3),
}, open('${COST_FILE}', 'w'), indent=2)
print(f'custo de treino: wall_time={train_wall_time_s}s peak_mem={peak_mem_mib/1024:.2f}GB -> ${COST_FILE}')
"

echo "Fine-tuning (${TASK}) concluído. Log em ${LOG_FILE}"
