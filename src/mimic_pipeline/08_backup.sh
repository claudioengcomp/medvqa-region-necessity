#!/bin/bash
# v7_mimic/scripts/08_backup.sh -- backup only of docs/analysis/configs/scripts/logs/manifest.json/README.md (never data/, never images)
set -u
SRC=${LAB_ROOT}/v7_mimic; DST=gdrive:Pesquisa/doutorado/v7_mimic; R=~/bin/rclone
LOG=$SRC/logs/rclone_backup.log
for d in docs analysis configs scripts logs results; do
  [ -d $SRC/$d ] && $R copy $SRC/$d $DST/$d --transfers 4 --checkers 8 --exclude "*.png" --exclude "*.jpg" --exclude "*.arrow" --exclude "*.parquet" --log-file=$LOG --log-level INFO
done
for f in manifest.json README.md; do [ -f $SRC/$f ] && $R copyto $SRC/$f $DST/$f --log-file=$LOG --log-level INFO; done
echo "--- check"
for d in docs analysis configs scripts logs results; do [ -d $SRC/$d ] && $R check $SRC/$d $DST/$d --checksum --exclude "*.png" --exclude "*.jpg" --exclude "*.arrow" --exclude "*.parquet" 2>&1 | tail -2; done
$R lsl $DST | wc -l
