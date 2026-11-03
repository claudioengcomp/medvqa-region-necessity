#!/bin/bash
# 14/10/2026: regenerates txt_floors -> decomposition -> own_floor_ceilings -> figures, on CPU, from the v7_txt worktree
source ${LAB_ROOT}/miniconda3/etc/profile.d/conda.sh && conda activate circle
export CUDA_VISIBLE_DEVICES="" HF_HOME=${LAB_ROOT}/cache/huggingface
cd ${LAB_ROOT}/v7_txt/worktree
for m in txt_floors decomposicao own_floor_ceilings make_figs_v7; do
  echo "[$(date -u +%FT%TZ)] $m start load=$(cut -d" " -f1 /proc/loadavg)"
  nice -n 19 ionice -c3 python -u -m harness.v7_txt.$m > ${LAB_ROOT}/v7_mimic/logs/gen_$m.log 2>&1; echo "[$(date -u +%FT%TZ)] $m exit=$?"
done
