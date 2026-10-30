#!/bin/bash
# v7_mimic/scripts/04_download_medgemma.sh -- 2026-10-10 -- gpu-server-a
# Downloads google/medgemma-1.5-4b-it to the default HF cache (~/.cache/huggingface, the same one used by the other zero-shot models). Does not load the model.
source ${LAB_ROOT}/miniconda3/etc/profile.d/conda.sh && conda activate circle
export CUDA_VISIBLE_DEVICES=""
echo "[$(date -u +%FT%TZ)] start"
nice -n 19 ionice -c3 hf download google/medgemma-1.5-4b-it 2>&1
echo "[$(date -u +%FT%TZ)] exit=$?"
