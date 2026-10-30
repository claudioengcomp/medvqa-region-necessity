#!/usr/bin/env bash
# Redo of the missing files of the HEAL-train batch down to zero (max 3 passes), with sha256 verification between passes.
cd "$HOME/Documents/doutorado/data_drive_sync.nosync/raw/vindr-cxr/1.0.0"
AP="s3://arn:aws:s3:us-east-1:724665945834:accesspoint/vindr-cxr-v1-0-0-01/vindr-cxr/1.0.0"
PY="$HOME/Documents/doutorado/rescoring/.venv312/bin/python"; R="$HOME/Documents/doutorado/med-vqa-icdip-p0"
for pass in 1 2 3; do
  n=$(wc -l < ids_redo_heal_train.txt | tr -d ' '); echo "redo passada $pass $(date -u +%FT%TZ): $n ids"; [ "$n" -eq 0 ] && break
  xargs -P 16 -I{} sh -c 'aws s3 cp --only-show-errors "'"$AP"'/{}" "{}"' < ids_redo_heal_train.txt
  find train -name '*.dicom.*' -delete
  (cd $R && $PY -m harness.isbi_placebo.heal.vindr_verify --base "$HOME/Documents/doutorado/data_drive_sync.nosync/raw/vindr-cxr/1.0.0" --list "$HOME/Documents/doutorado/data_drive_sync.nosync/raw/vindr-cxr/1.0.0/ids_heal_train.txt" --heal-items data/isbi_placebo/heal/heal_items.parquet --manifest data/isbi_placebo/heal/vindr_manifest.json --redo "$HOME/Documents/doutorado/data_drive_sync.nosync/raw/vindr-cxr/1.0.0/ids_redo_heal_train.txt" --delete-corrupt 2>/dev/null | grep -E '"n_verified"|"n_missing"|"n_corrupt"' | tr -d ' \n'; echo)
done
echo "REDO_DONE $(date -u +%FT%TZ) restantes=$(wc -l < ids_redo_heal_train.txt | tr -d ' ')"
