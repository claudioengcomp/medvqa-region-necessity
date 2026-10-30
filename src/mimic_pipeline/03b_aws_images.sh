#!/bin/bash
# v7_mimic/scripts/03b_aws_images.sh -- 2026-10-10 -- gpu-server-a
# Download of the subset images through the PhysioNet S3 access point (aws s3 cp file by file, 4 workers, nice 19),
# only for the keys still missing on disk. Credentials: ~/.aws/credentials or the user's AWS_* variables (never read here).
# Env: conda awscli (outside circle/lapa). Usage: 03b_aws_images.sh <list of keys files/...jpg> <tag>
set -u
LIST=${1:?lista}; TAG=${2:?tag}; PAR=${PAR:-4}
AP="s3://arn:aws:s3:us-east-1:724665945834:accesspoint/mimic-cxr-jpg-v2-1-0-01/mimic-cxr-jpg/2.1.0"
DST=${LAB_ROOT}/doutorado/data/raw/mimic-cxr-jpg/2.1.0
TMP=${LAB_ROOT}/tmp/v7_mimic; mkdir -p "$TMP"
source ${LAB_ROOT}/miniconda3/etc/profile.d/conda.sh && conda activate awscli
cd "$DST"
MISSING="$TMP/missing_${TAG}.txt"
while read -r k; do [ -n "$k" ] && [ ! -f "$k" ] && echo "$k"; done < "$LIST" > "$MISSING"
echo "[$(date -u +%FT%TZ)] start tag=$TAG lista=$(wc -l < $LIST) faltantes=$(wc -l < $MISSING) workers=$PAR"
nice -n 19 ionice -c3 xargs -P "$PAR" -I{} sh -c 'aws s3 cp --region us-east-1 --only-show-errors "'"$AP"'/{}" "{}" || echo "FAIL {}"' < "$MISSING"
echo "[$(date -u +%FT%TZ)] done tag=$TAG presentes=$(while read -r k; do [ -f "$k" ] && echo x; done < $LIST | wc -l)/$(wc -l < $LIST)"
