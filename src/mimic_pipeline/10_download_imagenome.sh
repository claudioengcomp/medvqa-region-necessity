#!/bin/bash
# v7_mimic/scripts/10_download_imagenome.sh -- 2026-10-11 -- Chest ImaGenome 1.0.0 (PhysioNet, S3 access point), only what is needed.
set -u
source ${LAB_ROOT}/miniconda3/etc/profile.d/conda.sh && conda activate awscli
AP=s3://arn:aws:s3:us-east-1:724665945834:accesspoint/chest-imagenome-v1-0-0-01/chest-imagenome/1.0.0
DST=${LAB_ROOT}/doutorado/data/raw/chest-imagenome/1.0.0; mkdir -p "$DST"; cd "$DST"
echo "[$(date -u +%FT%TZ)] start"
for f in LICENSE.txt SHA256SUMS.txt; do nice -n 19 aws s3 cp --region us-east-1 --only-show-errors "$AP/$f" "$f"; done
for d in semantics gold_dataset utils analysis; do nice -n 19 ionice -c3 aws s3 cp --region us-east-1 --only-show-errors --recursive "$AP/$d/" "$d/"; echo "[$(date -u +%FT%TZ)] $d ok"; done
mkdir -p silver_dataset/splits
for f in splits/train.csv splits/valid.csv splits/test.csv scene_graph.zip; do nice -n 19 ionice -c3 aws s3 cp --region us-east-1 --only-show-errors "$AP/silver_dataset/$f" "silver_dataset/$f"; echo "[$(date -u +%FT%TZ)] silver_dataset/$f ok"; done
echo "[$(date -u +%FT%TZ)] download done; sha256:"
# checks everything downloaded against SHA256SUMS.txt
ok=0; bad=0; while read -r h p; do [ -f "$p" ] || continue; g=$(nice -n 19 sha256sum "$p" | cut -c1-64); if [ "$g" = "$h" ]; then ok=$((ok+1)); else bad=$((bad+1)); echo "MISMATCH $p"; fi; done < SHA256SUMS.txt
echo "[$(date -u +%FT%TZ)] sha ok=$ok mismatch=$bad; nao baixados: $(while read -r h p; do [ -f "$p" ] || echo "$p"; done < SHA256SUMS.txt | tr "\n" " ")"
