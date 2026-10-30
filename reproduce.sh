#!/usr/bin/env bash
# CPU-only reproduction of the paper's numbers from the per-run statistics released in results/.
#   bash reproduce.sh            regenerate the numbers sheet, the tables and the supplementary figure; compare with results/; check the tables' numbers
#   bash reproduce.sh --kvasir   additionally recompute the Kvasir-VQA-x1 per-run statistics from the released per-item predictions (about 10 min)
# Environment: environment/environment-analysis.yml (conda) or the pinned packages in environment/requirements.txt. Run from any directory.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python}"
export MRN_CONFIG="${MRN_CONFIG:-config/paths.yaml}" MRN_OUT=reproduce_out LC_ALL=C PYTHONDONTWRITEBYTECODE=1 SOURCE_DATE_EPOCH=1761782400
export MPLCONFIGDIR="${MPLCONFIGDIR:-$PWD/reproduce_out/.mpl}"
if [ -d reproduce_out ]; then rm -rf reproduce_out; fi
mkdir -p reproduce_out/analysis reproduce_out/docs reproduce_out/tables reproduce_out/figs reproduce_out/logs reproduce_out/manifests "$MPLCONFIGDIR"
echo "[1/6] checksums of results/"
$PY tools/checksums.py verify results/SHA256SUMS
cp -R results/analysis/. reproduce_out/analysis/
if [ "${1:-}" = "--kvasir" ]; then
  echo "[2/6] Kvasir-VQA-x1 per-run statistics from results/predictions (bootstrap, 2 000 replicates)"
  $PY src/analysis/analise_bases.py KVASIR > reproduce_out/logs/analise_bases.log
  $PY tools/compare_json.py results/analysis/necessity_v2 reproduce_out/analysis/necessity_v2 --glob '*KVASIR*.json'
  cp results/analysis/bases_raw.json reproduce_out/analysis/bases_raw.json   # the sheet cites this file's checksum; the recompute rewrites it with a new time stamp
else
  echo "[2/6] (skipped: run with --kvasir to recompute the Kvasir-VQA-x1 per-run statistics)"
fi
echo "[3/6] numbers sheet"
$PY src/analysis/make_numbers_artigo1.py > reproduce_out/logs/make_numbers.log
$PY tools/compare_sheet.py results/numbers_artigo1.md reproduce_out/docs/numbers_artigo1.md
echo "[4/6] tables"
$PY src/analysis/make_tables_artigo1.py > reproduce_out/logs/make_tables.log
for t in table_criteria table1_necessity_slim table2_occluder_negatives table1_necessity table3_zeroshot; do
  if diff -q <(tail -n +2 "results/tables/$t.tex") <(tail -n +2 "reproduce_out/tables/$t.tex") > /dev/null; then echo "  $t.tex: identical"; else echo "  $t.tex: DIFFERS"; diff <(tail -n +2 "results/tables/$t.tex") <(tail -n +2 "reproduce_out/tables/$t.tex") || true; exit 1; fi
done
echo "[5/6] supplementary figure (per-run image gain and necessity effects)"
$PY src/analysis/fig1_artigo1.py > reproduce_out/logs/fig1.log
$PY tools/compare_figures.py results/figs reproduce_out/figs fig1_necessity_full fig_ladder
echo "[6/6] every number in the paper tables is in the numbers sheet"
$PY paper/verify_numbers.py reproduce_out/tables/table_criteria.tex reproduce_out/tables/table1_necessity_slim.tex reproduce_out/tables/table2_occluder_negatives.tex --sheet reproduce_out/docs/numbers_artigo1.md
echo "OK: reproduction complete (outputs in reproduce_out/)"
