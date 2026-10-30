#!/usr/bin/env bash
# Verifies by sha256, every 20 min, the new DICOMs of the HEAL-train batch (only those not yet verified in the manifest).
cd "$HOME/Documents/doutorado/med-vqa-icdip-p0"; B="$HOME/Documents/doutorado/data_drive_sync.nosync/raw/vindr-cxr/1.0.0"
PY="$HOME/Documents/doutorado/rescoring/.venv312/bin/python"
while true; do
  $PY -m harness.isbi_placebo.heal.vindr_verify --base $B --list $B/ids_heal_train.txt --heal-items data/isbi_placebo/heal/heal_items.parquet \
     --manifest data/isbi_placebo/heal/vindr_manifest.json --redo $B/ids_redo_heal_train.txt | grep -E '"n_verified"|"n_corrupt"|"n_missing"' | tr -d ' \n'
  echo " $(date -u +%FT%TZ)"
  grep -q "DONE\|PARADA" $B/download_progress_heal_train.log && { echo "VERIFY_LOOP_END $(date -u +%FT%TZ)"; break; }
  sleep 1200
done
