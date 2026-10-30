#!/usr/bin/env bash
# Selective download of VinDr-CXR through the PhysioNet S3 access point, from a list of keys, 32 connections,
# resumable (skips files already complete), log every 15 min, stop conditions: <10 % free disk; average <1 MB/s for 30 min.
# Usage: bash run_aws_download.sh <id_list.txt> <batch_name>
set -uo pipefail
LIST=$1; NAME=$2; FLOOR_GB=${3:-0}   # absolute floor in GB (0 = only the 10 % rule)
cd "$HOME/Documents/doutorado/data_drive_sync.nosync/raw/vindr-cxr/1.0.0"
AP="s3://arn:aws:s3:us-east-1:724665945834:accesspoint/vindr-cxr-v1-0-0-01/vindr-cxr/1.0.0"
LOG=download_progress_${NAME}.log; STOP=STOP_${NAME}
sizes_expected() { awk 'NR==FNR{want[$1]=1;next} ($2 in want){print $2}' "$LIST" SHA256SUMS.txt; }
# missing = ids of the list without a local file (the partial file of aws cp is temporary and does not count)
missing() { while read -r rel; do [ -f "$rel" ] || echo "$rel"; done < "$LIST"; }
t0=$(date +%s); b0=$(du -sk train | cut -f1)
echo "inicio $(date -u +%FT%TZ) lote=$NAME ids=$(wc -l < $LIST | tr -d ' ') livre=$(df -h /System/Volumes/Data | awk 'NR==2{print $4}') piso_gb=$FLOOR_GB" >> $LOG
# watchdog: every 15 min, count, GB, average rate; stops on disk space (<10 %) or rate (<1 MB/s for 30 min)
( low=0; while [ ! -f $STOP ]; do sleep 900; [ -f $STOP ] && break
    n=$(ls train | wc -l | tr -d ' '); kb=$(du -sk train | cut -f1); now=$(date +%s)
    rate=$(awk -v a=$b0 -v b=$kb -v s=$((now-t0)) 'BEGIN{printf "%.2f", (b-a)/1024/s}')
    pct=$(df /System/Volumes/Data | awk 'NR==2{gsub("%","",$5); print 100-$5}')
    echo "$(date -u +%FT%TZ) arquivos_train=$n gb_train=$(awk -v k=$kb 'BEGIN{printf "%.1f",k/1e6}') taxa_media_MBps=$rate livre_pct=$pct" >> $LOG
    free_gb=$(df -k /System/Volumes/Data | awk 'NR==2{printf "%d", $4/1e6}')
    if [ "$FLOOR_GB" -gt 0 ]; then
      if [ "$free_gb" -le "$FLOOR_GB" ]; then echo "PARADA: disco com <=${FLOOR_GB} GB livres (piso absoluto)" >> $LOG; touch $STOP; pkill -f "aws s3 cp --only-show-errors"; break; fi
    elif [ "$pct" -le 10 ]; then echo "PARADA: disco com <=10 % livre" >> $LOG; touch $STOP; pkill -f "aws s3 cp --only-show-errors"; break; fi
    if awk -v r=$rate 'BEGIN{exit !(r<0.3)}'; then low=$((low+1)); else low=0; fi
    if [ $low -ge 2 ]; then echo "PARADA: taxa media <0,3 MB/s por >=30 min" >> $LOG; touch $STOP; pkill -f "aws s3 cp --only-show-errors"; break; fi
  done ) &
WATCH=$!
missing | xargs -P ${PAR:-32} -I{} sh -c '[ -f "'"$STOP"'" ] || aws s3 cp --only-show-errors "'"$AP"'/{}" "{}"'
touch $STOP; wait $WATCH 2>/dev/null
n=$(ls train | wc -l | tr -d ' '); kb=$(du -sk train | cut -f1); now=$(date +%s)
echo "fim $(date -u +%FT%TZ) arquivos_train=$n gb_train=$(awk -v k=$kb 'BEGIN{printf "%.1f",k/1e6}') faltantes_da_lista=$(missing | wc -l | tr -d ' ') segundos=$((now-t0)) taxa_media_MBps=$(awk -v a=$b0 -v b=$kb -v s=$((now-t0)) 'BEGIN{printf "%.2f",(b-a)/1024/s}')" >> $LOG
echo "DOWNLOAD_${NAME}_DONE" >> $LOG
