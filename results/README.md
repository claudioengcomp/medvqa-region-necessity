# Results

- `numbers_artigo1.md`: the numbers sheet; one number per line with its source file and SHA-256. Every number of the paper is here
  (labels use the internal names; see the README glossary). Four citations of the sheet point to files that are not included
  (two earlier sheets and one directory listing); their checksum field is empty.
- `analysis/`: per-run statistics and aggregates written by `src/analysis`: `necessity_v2/<run>_<benchmark>.json` (117 fine-tuned runs and 12 zero-shot files; accuracies,
  image gain, control-occlusion drop, necessity effect, raw drops and their bootstrap intervals per question class) and the
  aggregates cited by the sheet (criteria counts, image gains per group, occluder test, enlarged occlusions, zero-shot models,
  Holm correction, overlap strata, control-placement counts, which file and checkpoint each run/condition used). File names keep
  the internal names (README glossary). For the credentialed benchmarks these are the only item-derived quantities released; the
  HEAL-MedVQA control-placement file has its per-unit list removed (counts kept).
- `predictions/kvasir/`: per-item predictions of every Kvasir-VQA-x1 run (39 fine-tuned runs, 4 zero-shot models) and condition read by the analysis
  (`<run>_<condition>.json` with `qid`, `predicted`, `gold`, `correct`). Sub-directories: `occlusion` (default encoder setting),
  `occlusion_encoder_swapped`, `full_test`, `full_test_encoder_swapped` (intact image on the whole test set), `no_image`,
  `no_image_dora`, `no_image_m3ae`, `occluder`, `zero_shot`, `blur4`. Provenance stamps were kept except the host name, GPU index
  and device list; absolute paths of the original server were made relative; names of untracked files that belong to other studies of
  the authors (not distributed) were removed from `git.untracked`, their number kept in `git.untracked_omitted`.
- `tables/`: the three tables of the paper (`table_criteria.tex`, `table1_necessity_slim.tex` without the HEAL-MedVQA yes-questions block,
  `table2_occluder_negatives.tex`) and two supplementary tables (`table1_necessity.tex` with all groups and quantities, `table3_zeroshot.tex`), generated from the sheet.
- `figs/`: supplementary figure of per-run image gains and necessity effects (`fig1_necessity*`), generated from `analysis/`.
  The protocol figure of the paper shows a chest X-ray and is not distributed; `src/analysis/fig_protocol_final.py` regenerates it
  from the occlusion arrows.
- `SHA256SUMS`: checksums of every file in this directory (`python tools/checksums.py verify results/SHA256SUMS`).
