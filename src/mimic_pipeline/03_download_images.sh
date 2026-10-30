#!/bin/bash
# v7_mimic/scripts/03_download_images.sh -- 2026-10-10 -- gpu-server-a
# Downloads ONLY the listed images (paths "files/p1x/pxxxxxxxx/sxxxxxxxx/<dicom_id>.jpg", checked against IMAGE_FILENAMES)
# de https://physionet.org/files/mimic-cxr-jpg/2.1.0/ (credenciais via ~/.netrc), mantendo a arvore files/... em
# doutorado/data/raw/mimic-cxr-jpg/2.1.0/. --cut-dirs=3 (not 2): the URL path is /files/mimic-cxr-jpg/2.1.0/files/...;
# with 2, wget created 2.1.0/files/... inside the destination (verified empirically with 3 images at 04:41 UTC).
# PhysioNet delivers ~100 KB/s per IP; we run NSHARDS processes in parallel (<= 4) over slices of the list, test+val first.
#   usage: 03_download_images.sh <list> <tag>      (nohup setsid ... > logs/wget_images_<tag>.log)
set -u
LIST=${1:?lista}; TAG=${2:?tag}; NSHARDS=${NSHARDS:-4}
DST=${LAB_ROOT}/doutorado/data/raw/mimic-cxr-jpg/2.1.0
LOGD=${LAB_ROOT}/v7_mimic/logs; TMP=${LAB_ROOT}/tmp/v7_mimic/shards_$TAG
mkdir -p "$TMP"; cd "$DST"
split -n l/$NSHARDS -d "$LIST" "$TMP/shard_"
echo "[$(date -u +%FT%TZ)] start tag=$TAG n=$(wc -l < $LIST) shards=$NSHARDS"
for s in "$TMP"/shard_*; do
  nice -n 19 ionice -c3 wget -N -c -x -nH --cut-dirs=3 --no-verbose --tries=5 --waitretry=10 \
    -i "$s" -B https://physionet.org/files/mimic-cxr-jpg/2.1.0/ > "$LOGD/wget_images_${TAG}_$(basename $s).log" 2>&1 &
done
wait
echo "[$(date -u +%FT%TZ)] done tag=$TAG; jpg presentes da lista: $(while read p; do [ -f "$p" ] && echo x; done < $LIST | wc -l)/$(wc -l < $LIST)"
