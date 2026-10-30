#!/bin/bash
# runs 02_png_from_jpg.py for train (workers according to load: 8, or 4 if load > 150)
source ${LAB_ROOT}/miniconda3/etc/profile.d/conda.sh && conda activate circle
export CUDA_VISIBLE_DEVICES=""
cd ${LAB_ROOT}/v7_mimic
RAW=${LAB_ROOT}/doutorado/data/raw/mimic-cxr-jpg/2.1.0; DER=${LAB_ROOT}/doutorado/data/derived/mimic_png
LOAD=$(cut -d. -f1 /proc/loadavg); W=8; [ "$LOAD" -gt 150 ] && W=4
echo "[$(date -u +%FT%TZ)] png train start load=$LOAD workers=$W"; uptime
nice -n 19 ionice -c3 python scripts/02_png_from_jpg.py --items data/items_train.parquet --split train --jpg-root $RAW \
   --stage ${LAB_ROOT}/tmp/v7_mimic/stage/train --out-dir $DER/train --manifest $DER/png_manifest_train.json --workers $W
echo "[$(date -u +%FT%TZ)] png train exit=$?"
