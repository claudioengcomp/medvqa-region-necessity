#!/usr/bin/env bash
# v7_mimic A (2026-10-11): fine-tune of M3AE on MIMIC with the SAME recipe as the reference runs (run_finetune_m3ae.sh of the control-occlusion harness (`placebo` in the code) /
# run_m3ae_txt.sh of v7_txt: per_gpu_batchsize=16 clip16 text_roberta image_size=384 tokenizer roberta-base load_path pretrained m3ae.ckpt,
# transform clip), vqa_label_size=82 (answer_vocab.json of v7_mimic), real images (data_root = v7_mimic/m3ae_arrows/data_root, links to
# v7_mimic/data). Worktree v7_txt/worktree_m3ae (14da377 + HEAL patch + MIMIC patch). Cost: nvidia-smi every 5 s -> _cost.json.
# Usage: bash run_m3ae_mimic.sh <seed> [extra sacred args]
set -euo pipefail
SEED="${1:?seed}"; shift 1; EXTRA=("$@")
WM=${LAB_ROOT}/v7_txt/worktree_m3ae; ROOT=${LAB_ROOT}/v7_mimic
DATA_ROOT=$ROOT/m3ae_arrows/data_root/; LOG_DIR=$ROOT/logs; CK=$ROOT/m3ae
TASK=task_finetune_vqa_mimic; LS=82; TK="clip"
# 13/10/2026 (authors): modes selected by M3AE_MODE (default img = command identical to that of 11/10/2026): gray = no-image M3AE (constant gray image in training,
# validation and test, arrows from make_gray_arrows_mimic.py; checkpoints in v7_mimic/m3ae_txt); memtest = memory measurement (identical recipe,
# separate checkpoints and logs; the sitecustomize callback of m3ae_memtest stops after 20 steps). M3AE_PER_GPU (default 16) only in memtest.
MODE="${M3AE_MODE:-img}"; PG=16; NAME=M3AE_MIMIC_seed${SEED}
case "$MODE" in
  img) ;;
  gray) DATA_ROOT=$ROOT/m3ae_arrows_gray/data_root/; CK=$ROOT/m3ae_txt; NAME=M3AE_TXT_MIMIC_seed${SEED} ;;
  memtest) PG="${M3AE_PER_GPU:-16}"; LOG_DIR=$ROOT/logs/m3ae_memtest; CK=${LAB_ROOT}/tmp/v7/m3ae_memtest; NAME=M3AE_MIMIC_memtest_seed${SEED}_b${PG} ;;
  *) echo "M3AE_MODE invalido: $MODE"; exit 1 ;;
esac
source ${LAB_ROOT}/miniconda3/etc/profile.d/conda.sh; conda activate lapa; export WANDB_MODE=disabled
mkdir -p "$LOG_DIR" "$CK"
LOG_FILE=$LOG_DIR/${NAME}.log; GPU_MEM_LOG=$LOG_DIR/${NAME}.gpu_mem.log; COST_FILE=$LOG_DIR/${NAME}_cost.json
cd "$WM"
: > "$GPU_MEM_LOG"
NVSMI=nvidia-smi; [ -x ${LAB_ROOT}/nvidia-580.173.02/nvidia-smi ] && NVSMI=${LAB_ROOT}/nvidia-580.173.02/nvidia-smi   # 12/10: driver workaround
# 12/10/2026: poll ONLY the training GPU (-i), fixing the defect inherited from run_finetune_m3ae.sh (it logged the 4 GPUs interleaved)
( while true; do $NVSMI -i "${CUDA_VISIBLE_DEVICES}" --query-gpu=memory.used --format=csv,noheader,nounits >> "$GPU_MEM_LOG" 2>/dev/null; sleep 5; done ) &
GPU_POLL_PID=$!; trap 'kill "$GPU_POLL_PID" 2>/dev/null || true' EXIT
_start_ts=$(date +%s)
echo "[run_m3ae_mimic] $(date) mode=$MODE per_gpu_batchsize=$PG seed=$SEED task=$TASK label_size=$LS transform=$TK data_root=$DATA_ROOT cwd=$WM CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-}" | tee "$LOG_FILE"
python -u main.py with data_root="$DATA_ROOT" num_gpus=1 num_nodes=1 "$TASK" per_gpu_batchsize=$PG clip16 text_roberta image_size=384 \
  tokenizer=downloaded/roberta-base load_path=downloaded/pretrained/m3ae.ckpt seed="$SEED" vqa_label_size="$LS" "train_transform_keys=[\"$TK\"]" \
  default_root_dir="$CK" log_dir="$CK/result" "${EXTRA[@]}" 2>&1 | tee -a "$LOG_FILE"
_end_ts=$(date +%s)
python3 -c "
import json
t = ${_end_ts} - ${_start_ts}
try: peak = max(int(l) for l in open('${GPU_MEM_LOG}') if l.strip())
except ValueError: peak = 0
json.dump({'run_name': '${NAME}', 'task': '${TASK}', 'seed': ${SEED}, 'vqa_label_size': ${LS}, 'train_transform_keys': ['${TK}'], 'data_root': '${DATA_ROOT}', 'train_wall_time_s': t, 'train_peak_memory_gb': round(peak / 1024, 3), 'note': 'pico = nvidia-smi da placa do treino (-i ${CUDA_VISIBLE_DEVICES}; inclui terceiros nessa placa); 12/10: corrigido o poll das 4 placas', 'placa': '${CUDA_VISIBLE_DEVICES}', 'ld_library_path': '${LD_LIBRARY_PATH:-}'}, open('${COST_FILE}', 'w'), indent=2)
print(f'custo de treino: wall_time={t}s peak_mem={peak/1024:.2f}GB -> ${COST_FILE}')
"
echo "FIM_TREINO_M3AE_MIMIC $NAME" | tee -a "$LOG_FILE"
