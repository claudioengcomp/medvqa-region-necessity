#!/usr/bin/env bash
# P1.3 (2026-10-09): fine-tune of the "no-image" M3AE = constant gray image (384x384 RGB 128) in training, validation and test,
# with the SAME hyperparameters and seeds as the reference runs (hparams.yaml of the reference checkpoints), in the worktree
# v7_txt/worktree_m3ae (14da377 + patch with the uncommitted M3AE changes). Adapted from
# med-vqa-icdip-placebo/harness/run_finetune_m3ae.sh (same cost measurement: nvidia-smi every 5 s -> _cost.json).
# Usage: bash run_m3ae_txt.sh <slack|kvasir|heal|vqa_rad> <seed> [extra sacred args]
# 13/10/2026 (authors; `piso`, the no-image floor): vqa_rad (vqa_label_size 498, clip, reference hparams.yaml); M3AE_MODE=img (default gray = command identical to that of 09/10/2026):
# retraining with the reference recipe and real images (data_root = M3AE/data/finetune_arrows, read-only), checkpoints in v7_txt/m3ae_gpu1,
# name M3AE_SCRATCH_<SLAKE|VQARAD>_seed<s>_gpu1 (nothing existing is overwritten). Memory poll only on the training GPU (-i), nvidia-smi from the driver workaround.
set -euo pipefail
BENCH="${1:?slack|kvasir|heal|vqa_rad}"; SEED="${2:?seed}"; shift 2; EXTRA=("$@")
WM=${LAB_ROOT}/v7_txt/worktree_m3ae; ROOT=${LAB_ROOT}/v7_txt
DATA_ROOT=$ROOT/m3ae_arrows/data_root/; LOG_DIR=$ROOT/logs; CK=$ROOT/m3ae
case "$BENCH" in
  slack)  TASK=task_finetune_vqa_slack;  LS=222; TK="clip"; [ "$SEED" = "0" ] && TK="clip_resizedcrop" ;;   # reference seed 0 used clip_resizedcrop; seeds 1-2 clip (hparams.yaml)
  kvasir) TASK=task_finetune_vqa_kvasir; LS=500; TK="clip" ;;   # vqa_label_size 500 (clean split), as in the reference runs
  heal)   TASK=task_finetune_vqa_heal;   LS=288; TK="clip" ;;
  vqa_rad) TASK=task_finetune_vqa_vqa_rad; LS=498; TK="clip" ;;   # 13/10: reference hparams.yaml (seeds 0 and 1): label 498, clip
  *) echo "bench invalido"; exit 1 ;;
esac
source ${LAB_ROOT}/miniconda3/etc/profile.d/conda.sh; conda activate lapa; export WANDB_MODE=disabled
NAME=M3AE_TXT_${BENCH}_seed${SEED}
MODE="${M3AE_MODE:-gray}"
if [ "$MODE" = img ]; then DATA_ROOT=${LAB_ROOT}/doutorado/M3AE/data/finetune_arrows/; CK=$ROOT/m3ae_gpu1; NAME=M3AE_SCRATCH_$(case $BENCH in slack) echo SLAKE ;; vqa_rad) echo VQARAD ;; *) echo X ;; esac)_seed${SEED}_gpu1; case $BENCH in slack|vqa_rad) ;; *) echo "img so para slack e vqa_rad"; exit 1 ;; esac; elif [ "$MODE" = rediv ] || [ "$MODE" = redivgray ]; then [ "$BENCH" = vqa_rad ] || { echo "rediv so para vqa_rad"; exit 1; }; PJ=$ROOT/extra_runs; LOG_DIR=$PJ/logs; if [ "$MODE" = rediv ]; then DATA_ROOT=$PJ/data/vqarad_rediv/; CK=$PJ/m3ae; NAME=M3AE_SCRATCH_VQARAD_REDIV_seed${SEED}; else DATA_ROOT=$PJ/data/vqarad_rediv/data_root_cinza/; CK=$PJ/m3ae_txt; NAME=M3AE_TXT_VQARAD_REDIV_seed${SEED}; fi   # 17/10 (extra_runs, item 5)
elif [ "$MODE" = qlevel ] || [ "$MODE" = qlevelgray ]; then [ "$BENCH" = vqa_rad ] || { echo "qlevel so para vqa_rad"; exit 1; }; PJ=$ROOT/extra_runs; LOG_DIR=$PJ/logs; if [ "$MODE" = qlevel ]; then DATA_ROOT=$PJ/data/vqarad_qlevel/; CK=$PJ/m3ae_qlevel; NAME=M3AE_SCRATCH_VQARAD_QLEVEL_seed${SEED}; else DATA_ROOT=$PJ/data/vqarad_qlevel/data_root_cinza/; CK=$PJ/m3ae_txt_qlevel; NAME=M3AE_TXT_VQARAD_QLEVEL_seed${SEED}; fi   # 19/10 (item 9)
elif [ "$MODE" != gray ]; then echo "M3AE_MODE invalido"; exit 1; fi
mkdir -p "$LOG_DIR" "$CK"
LOG_FILE=$LOG_DIR/${NAME}.log; GPU_MEM_LOG=$LOG_DIR/${NAME}.gpu_mem.log; COST_FILE=$LOG_DIR/${NAME}_cost.json
cd "$WM"
: > "$GPU_MEM_LOG"
NVSMI=nvidia-smi; [ -x ${LAB_ROOT}/nvidia-580.173.02/nvidia-smi ] && NVSMI=${LAB_ROOT}/nvidia-580.173.02/nvidia-smi   # 13/10: driver workaround
( while true; do $NVSMI -i "${CUDA_VISIBLE_DEVICES}" --query-gpu=memory.used --format=csv,noheader,nounits >> "$GPU_MEM_LOG" 2>/dev/null; sleep 5; done ) &   # 13/10: only the training GPU
GPU_POLL_PID=$!; trap 'kill "$GPU_POLL_PID" 2>/dev/null || true' EXIT
_start_ts=$(date +%s)
echo "[run_m3ae_txt] $(date) mode=$MODE name=$NAME bench=$BENCH seed=$SEED task=$TASK label_size=$LS transform=$TK data_root=$DATA_ROOT cwd=$WM CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-}" | tee "$LOG_FILE"
python -u main.py with data_root="$DATA_ROOT" num_gpus=1 num_nodes=1 "$TASK" per_gpu_batchsize=16 clip16 text_roberta image_size=384 \
  tokenizer=downloaded/roberta-base load_path=downloaded/pretrained/m3ae.ckpt seed="$SEED" vqa_label_size="$LS" "train_transform_keys=[\"$TK\"]" \
  default_root_dir="$CK" log_dir="$CK/result" "${EXTRA[@]}" 2>&1 | tee -a "$LOG_FILE"
_end_ts=$(date +%s)
python3 -c "
import json
t = ${_end_ts} - ${_start_ts}
try: peak = max(int(l) for l in open('${GPU_MEM_LOG}') if l.strip())
except ValueError: peak = 0
json.dump({'run_name': '${NAME}', 'task': '${TASK}', 'seed': ${SEED}, 'vqa_label_size': ${LS}, 'train_transform_keys': ['${TK}'], 'data_root': '${DATA_ROOT}', 'train_wall_time_s': t, 'train_peak_memory_gb': round(peak / 1024, 3), 'note': 'pico = nvidia-smi da placa inteira (inclui terceiros), como nas linhas publicadas'}, open('${COST_FILE}', 'w'), indent=2)
print(f'custo de treino: wall_time={t}s peak_mem={peak/1024:.2f}GB -> ${COST_FILE}')
"
echo "FIM_TREINO_M3AE_TXT $NAME" | tee -a "$LOG_FILE"
