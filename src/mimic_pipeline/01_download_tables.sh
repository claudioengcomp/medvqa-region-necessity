#!/bin/bash
# v7_mimic/scripts/01_download_tables.sh -- 2026-10-10 -- gpu-server-a
# Downloads the tables (not the images) of Medical-Diff-VQA 1.0.1 and MIMIC-CXR-JPG 2.1.0 (PhysioNet, credentialed via ~/.netrc).
set -u
RAW=${LAB_ROOT}/doutorado/data/raw
D1=$RAW/medical-diff-vqa/1.0.1
D2=$RAW/mimic-cxr-jpg/2.1.0
mkdir -p "$D1" "$D2"
B1=https://physionet.org/files/medical-diff-vqa/1.0.1
B2=https://physionet.org/files/mimic-cxr-jpg/2.1.0
echo "[$(date -u +%FT%TZ)] start diff-vqa tables"
cd "$D1"
for f in mimic_pair_questions.csv mimic_all.csv all_diseases.json README.md LICENSE.txt SHA256SUMS.txt; do
  nice -n 19 ionice -c3 wget -N -c --no-verbose "$B1/$f" || echo "FAIL $f"
done
echo "[$(date -u +%FT%TZ)] start mimic-cxr-jpg tables"
cd "$D2"
for f in mimic-cxr-2.0.0-split.csv.gz mimic-cxr-2.0.0-metadata.csv.gz mimic-cxr-2.0.0-chexpert.csv.gz IMAGE_FILENAMES SHA256SUMS.txt README LICENSE.txt; do
  nice -n 19 ionice -c3 wget -N -c --no-verbose "$B2/$f" || echo "FAIL $f"
done
cd "$D1"
echo "[$(date -u +%FT%TZ)] start diff-vqa libs/"
nice -n 19 ionice -c3 wget -N -c --no-verbose -r -np -nH --cut-dirs=3 -R "index.html*" "$B1/libs/" || echo "FAIL libs"
echo "[$(date -u +%FT%TZ)] done"
