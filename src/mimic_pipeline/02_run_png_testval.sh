#!/bin/bash
# runs 02_png_from_jpg.py for test and val (8 workers, nice 19)
source ${LAB_ROOT}/miniconda3/etc/profile.d/conda.sh && conda activate circle
export CUDA_VISIBLE_DEVICES=""
cd ${LAB_ROOT}/v7_mimic
RAW=${LAB_ROOT}/doutorado/data/raw/mimic-cxr-jpg/2.1.0; DER=${LAB_ROOT}/doutorado/data/derived/mimic_png
for s in test val; do
  echo "[$(date -u +%FT%TZ)] png $s start"; uptime
  nice -n 19 ionice -c3 python scripts/02_png_from_jpg.py --items data/items_$s.parquet --split $s --jpg-root $RAW \
     --stage ${LAB_ROOT}/tmp/v7_mimic/stage/$s --out-dir $DER/$s --manifest $DER/png_manifest_$s.json --workers 8
  echo "[$(date -u +%FT%TZ)] png $s exit=$?"
done
