#!/bin/bash
source ${LAB_ROOT}/miniconda3/etc/profile.d/conda.sh && conda activate circle
export CUDA_VISIBLE_DEVICES=""
cd ${LAB_ROOT}/v7_mimic
for g in main1 sham blur regmean dose; do
  L=$(cut -d. -f1 /proc/loadavg); W=8; [ "$L" -gt 150 ] && W=4
  echo "[$(date -u +%FT%TZ)] group $g start load=$L workers=$W"
  nice -n 19 ionice -c3 python scripts/17_make_mimic_conditions.py --group $g --workers $W
  echo "[$(date -u +%FT%TZ)] group $g exit=$?"
done
