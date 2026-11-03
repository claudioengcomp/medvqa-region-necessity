#!/usr/bin/env bash
# (Re)launches the scheduler of the 7B battery on the given cards and the watchdog. Stops the previous one by the PID file (never by name).
# Usage: lanca_escalonador_q25.sh "<cards>"   e.g. "1" or "0 1 2 3"
set -u; G="$1"; MODO="${2:-par}"   # MODO=sempar: without --peer-state (the peer scheduler is stopped; its stopped state does not block a card)
 T=${LAB_ROOT}/v7_txt/extra_runs/q25_artigo1; PF=$T/logs/escalonador.pid; VF=$T/logs/vigia.pid
PY=${LAB_ROOT}/miniconda3/envs/circle/bin/python
PEER="--peer-state ${LAB_ROOT}/v7_txt/extra_runs/qwen25vl7b/logs/infer_state_q25.json"; [ "$MODO" = sempar ] && PEER=""
export HF_HOME=${LAB_ROOT}/cache/huggingface TMPDIR=${LAB_ROOT}/tmp/v7/q25_artigo1/tmp
A="--jobs $T/jobs_q25_artigo1.json --state $T/infer_state_q25_artigo1.json --log-dir $T/logs --gpus $G --slots 1 $PEER --poll 3 --read-gap 3 --min-free-ram-gb 60 --disk-min-gb 20 --launch-settle-s 0 --infer-only-first-free --free-card-wait-s 0"
cd ${LAB_ROOT}/v7_txt/worktree
$PY -m py_compile harness/v7_txt/infer_scheduler_v7.py || exit 2
timeout 300 $PY -B harness/v7_txt/infer_scheduler_v7.py $A --dry-run > $T/logs/dry_run_ultimo.txt 2>&1 || { echo "dry-run falhou"; exit 3; }
for f in $PF $VF; do [ -s $f ] && kill "$(cat $f)" 2>/dev/null; done; sleep 3
nohup setsid $PY -B harness/v7_txt/infer_scheduler_v7.py $A >> $T/infer_scheduler_q25_artigo1.log 2>&1 < /dev/null & echo $! > $PF
sleep 5; kill -0 "$(cat $PF)" || { echo "escalonador nao subiu"; exit 4; }
cd $T; nohup setsid nice -n 19 bash scripts/vigia_q25.sh "$(cat $PF)" > /dev/null 2>&1 < /dev/null & echo $! > $VF
echo "$G|$MODO" > $T/logs/placas_atuais.txt
echo "$(date '+%F %T') escalonador $(cat $PF) placas [$G] modo $MODO; vigia $(cat $VF)" | tee -a $T/logs/lancamentos_escalonador.log
