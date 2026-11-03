# Controlled region-occlusion tests in medical VQA

Code, derived data and per-run results for the paper **"When a Drop Is Not Evidence: Controlled Region-Occlusion Tests in Medical VQA"**
(C. Leite and J. Almeida, submitted to IEEE ISBI 2027).

The protocol measures whether a medical visual question answering model *needs* the image region a question is about. For each
fine-tuned run it compares the accuracy drop under a black or blurred occlusion of the target region with the drop under a
shape- and size-matched control occlusion elsewhere in the image, requires the drop to hold under both fills, and only reads
the comparison when the same model's image gain (accuracy with the image minus the accuracy of a no-image baseline fine-tuned
with the same recipe) is significant. All intervals are image-level paired bootstraps (2 000 replicates, fixed seed).

## Contents

```
README.md              this file (pipeline, reproduction, datasets, licenses, glossary)
LICENSE                MIT, code only; LICENSE-DATA.md: terms of the derived data (CC BY-NC 4.0 and research-only use of the masks)
CITATION.cff
reproduce.sh           CPU-only reproduction from results/ (numbers sheet, tables, figure, number check)
config/paths.yaml      the only place where paths are set (relative to this directory)
configs/training/      YAML of every fine-tuning run (117 with image: 81 of the 2B models and M3AE, 36 of Qwen2.5-VL-7B; the no-image baselines) and the M3AE command lines
configs/inference/     zero-shot prompts and the list of occlusion conditions
data/kvasir/           Kvasir-VQA-x1: image-disjoint split, test inventory, mask correspondences, control-occlusion placements, blur scale
data/blur4/            parameters and checksums of the fixed-scale blur (4 % of the median image width)
environment/           pinned software versions, conda environments, model snapshots (VERSIONS.md)
src/med_vlm/           fine-tuning and inference of Qwen2-VL-2B, Qwen2.5-VL-7B and SmolVLM2-2.2B (LoRA / DoRA, frozen or fine-tuned vision encoder)
src/harness/           data construction (splits, inventories, occlusion arrows, occluder arrows), inference driver (and its earlier version in legacy/), job scheduler and the 7B battery scripts (v7_txt/), statistics
src/m3ae_patch/        patch over the upstream M3AE commit (datasets, no-image path), its tests, and our dataset modules; upstream code not copied
src/mimic_pipeline/    Medical-Diff-VQA: subset, images, regions, test items and occlusion arrows (credentialed inputs)
src/blur4/             fixed-scale blur arrows
src/analysis/          per-run statistics, criteria (i)-(v), Holm correction, numbers sheet, tables, figure
results/               per-run statistics of the three benchmarks, per-item predictions for Kvasir-VQA-x1, numbers sheet, tables, figure
models/MANIFEST.md     path, size and SHA-256 of every adapter / checkpoint (weights available on request)
paper/                 verify_numbers.py (every number of the tables and of the text list is in the numbers sheet) and text_numbers.md (the numbers cited by the submitted text)
tools/                 checksum and comparison helpers used by reproduce.sh
```

## Pipeline

1. **Data.** Kvasir-VQA-x1 is re-split by image (`data/kvasir/split_image_ids.json`); polyp and instrument masks come from Kvasir-SEG and
   Kvasir-Instrument (`data/kvasir/kvasir_vqa_to_seg_instrument_map.json`). HEAL-MedVQA items use VinDr-CXR images and the
   HEAL annotations; Medical-Diff-VQA items use MIMIC-CXR-JPG images and Chest ImaGenome regions. The test inventories mark, for
   each question, its class, the target region and whether a valid control occlusion exists. Occlusion arrows (intact; target and
   control occluded with black, blur at 10 % of the image width, and blur at a fixed 4 % scale; occluder on images without the
   target) are written by the occlusion and occluder modules of `src/harness`, `src/blur4` and `src/mimic_pipeline` (see `data/README.md`).
2. **Fine-tuning.** `python -m med_vlm.run_experiment --config <yaml> --seed <0|1|2>` for the 2B and 7B models (configs in `configs/training`;
   the 7B DoRA runs through the wrapper `src/harness/v7_txt/qwen25vl_7b/train_dora_q25.py`, queued by `make_jobs_q25_artigo1.py` and run by `infer_scheduler_v7.py`);
   M3AE through the wrappers in `src/harness/v7_txt` and the patch in `src/m3ae_patch`. The no-image baselines use the same recipe
   with the question only.
3. **Inference.** `python -m harness.extract_predictions_circle --model ... --peft ... --dataset ... --condition ... --condition-arrow ...
   --adapter-dir ... --output ...` writes one JSON per run and condition (`qid`, `predicted`, `gold`, `correct`, provenance).
   Zero-shot models use the same driver without an adapter (`configs/inference/zero_shot.md`).
4. **Analysis.** `src/analysis/analise_bases.py` computes, per run and question class, the accuracies, the image gain, the
   control-occlusion drop, the necessity effect and the bootstrap intervals; the other scripts aggregate them (criteria (i)-(v),
   Holm correction, fixed-scale blur, overlap strata, occluder test) into `results/analysis/`; `make_numbers_artigo1.py` writes the
   numbers sheet; `make_tables_artigo1.py` and `fig1_artigo1.py` produce the tables and the figure from the sheet / the aggregates.

## Reproducing the numbers without a GPU

```bash
conda env create -f environment/environment-analysis.yml && conda activate medvqa-rn-analysis
bash reproduce.sh            # sheet, tables, figure and number check from results/ (about 1 min)
bash reproduce.sh --kvasir   # also recompute the Kvasir-VQA-x1 per-run statistics from results/predictions (about 15 min)
```

`reproduce.sh` verifies the checksums of `results/`, regenerates `numbers_artigo1.md`, the five tables and the supplementary figure into
`reproduce_out/`, and compares them with the published files (every line of the sheet except its time stamp; the tables except
their header comment; PNG bytes and PDF content). PNG bytes can differ across machines (font rendering); the PDF content and
every number are compared exactly. With `--kvasir` it recomputes the per-run statistics of the 39 Kvasir-VQA-x1
runs (27 of the 2B models and M3AE, 12 of Qwen2.5-VL-7B) and the four zero-shot models from the released per-item predictions and compares them field by
field with `results/analysis/necessity_v2`. The last step also checks the list of numbers cited by the submitted text (`paper/text_numbers.md`) against the sheet.

Numbers that need the credentialed data (HEAL-MedVQA, Medical-Diff-VQA) are regenerated from the released per-run aggregates, not
recomputed from items: the aggregates in `results/analysis/` are the output of the same scripts run on the credentialed items. To
recompute them, rebuild the items with the scripts listed in `data/README.md`, run inference, and point `config/paths.yaml`
(see `config/paths.credentialed.example.yaml`) to the resulting files; the whole analysis then runs with the same commands.

## Reproducing the study (GPU and credentialed access)

- Datasets: see `data/README.md` for sources, credentials and the scripts that rebuild every arrow.
- Software: `environment/environment.yml` (2B models, zero-shot, analysis) and `environment/environment-m3ae.yml`; exact model
  snapshots and weight checksums in `environment/VERSIONS.md`.
- Fine-tuning recipe (all 2B and 7B runs): rank 16, alpha 32, learning rate 2e-4, 3 epochs, batch 4 with 4 accumulation steps, bf16;
  adapters on the attention projections of the language model (frozen encoder) or also on the attention of the vision encoder
  (fine-tuned encoder); M3AE fully fine-tuned from the authors' pretrained checkpoint. Seeds 0, 1, 2.
- Statistics: image-level bootstrap with 2 000 replicates, seed 20260913, the same replicates for every run and condition of a
  benchmark (`src/harness/v7_sham/shamstats.py`, `src/analysis/engine.py`); one-sided bootstrap p-values; Holm correction over
  the question subsets of a run (intersection-union test).

## Datasets and licenses

| dataset | use in the paper | source | license / terms |
|---|---|---|---|
| Kvasir-VQA-x1 | endoscopy questions and images | https://huggingface.co/datasets/SimulaMet/Kvasir-VQA-x1 | CC BY-NC 4.0 |
| Kvasir-SEG | polyp masks | https://datasets.simula.no/kvasir-seg/ | research and educational use; cite the dataset paper |
| Kvasir-Instrument | instrument masks | https://datasets.simula.no/kvasir-instrument/ | research and education use; cite the dataset paper |
| HEAL-MedVQA | chest X-ray questions, anatomy masks | https://huggingface.co/datasets/MM-Hallu/HEAL-MedVQA (annotations); images: VinDr-CXR 1.0.0, https://physionet.org/content/vindr-cxr/1.0.0/ | PhysioNet credentialed access (VinDr-CXR) |
| Medical-Diff-VQA | chest X-ray questions | https://physionet.org/content/medical-diff-vqa/1.0.1/ | PhysioNet credentialed access |
| MIMIC-CXR-JPG 2.1.0 | images of Medical-Diff-VQA | https://physionet.org/content/mimic-cxr-jpg/2.1.0/ | PhysioNet credentialed access |
| Chest ImaGenome 1.0.0 | anatomical regions of Medical-Diff-VQA | https://physionet.org/content/chest-imagenome/1.0.0/ | PhysioNet credentialed access |

Model licenses, read from the primary sources on 2026-10-30:

| model | source read | license / terms |
|---|---|---|
| Qwen2-VL-2B-Instruct | https://huggingface.co/Qwen/Qwen2-VL-2B-Instruct (card metadata) | apache-2.0 |
| SmolVLM2-2.2B-Instruct | https://huggingface.co/HuggingFaceTB/SmolVLM2-2.2B-Instruct (card metadata and text) | apache-2.0 |
| M3AE (code and pretrained weights) | https://github.com/zhjohnchan/M3AE (file list; GitHub API `/license` returns 404) | no license file declared; code used under its authors' terms with attribution; not redistributed here (patch only) |
| MedGemma 1.5 4B | https://huggingface.co/google/medgemma-1.5-4b-it (gated card) | Health AI Developer Foundations terms of use, https://developers.google.com/health-ai-developer-foundations/terms |
| Qwen2.5-VL-7B-Instruct | https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct (card metadata) | apache-2.0 |
| LLaVA-Med v1.5 Mistral-7B | https://huggingface.co/microsoft/llava-med-v1.5-mistral-7b (card: "mistralai/Mistral-7B-Instruct-v0.2 license", metadata apache-2.0); weights loaded from the community conversion https://huggingface.co/chaoyinshe/llava-med-v1.5-mistral-7b-hf (declared apache-2.0; not an official Microsoft release) | apache-2.0 / Mistral-7B-Instruct-v0.2 terms |
| MedVLThinker-7B-RL_PMC | https://huggingface.co/UCSC-VLAA/MedVLThinker-7B-RL_PMC (card text) | Apache 2.0 |

Dataset terms were read on the same date from https://huggingface.co/datasets/SimulaMet/Kvasir-VQA-x1 (CC BY-NC 4.0),
https://datasets.simula.no/kvasir-seg/ and https://datasets.simula.no/kvasir-instrument/ (terms of use quoted in `LICENSE-DATA.md`)
and https://huggingface.co/datasets/MM-Hallu/HEAL-MedVQA (annotations declared MIT; the images come from VinDr-CXR, whose
PhysioNet terms we follow for everything derived from them).

Nothing derived from the credentialed datasets at the item level is distributed here: no image, mask, box, coordinate,
question text, reference answer, identifier or per-item prediction. For those benchmarks the repository contains per-run
aggregates and the scripts that rebuild the items from the official files. For Kvasir-VQA-x1 the per-item predictions,
question text and reference answers are distributed under the dataset's CC BY-NC 4.0 terms (see `LICENSE-DATA.md`).

## Glossary: names in the code and in the numbers sheet → terms of the paper

<!-- glossary:start -->
The research code and the numbers sheet keep their original internal names. Correspondence:

| name in code / sheet / file names | term in the paper |
|---|---|
| `placebo`, `P`, `mascara deslocada` | shape- and size-matched control occlusion; `C` = control-occlusion drop |
| `T` | target-region occlusion (black fill) |
| `S` | everything outside the target occluded (sufficiency; supplementary only) |
| `C0` | intact image |
| `C1` | blank image (supplementary only) |
| `_blur10` | blur fill with sigma = 10 % of the image width |
| `_blur` (blur 4 %) | blur fill with a fixed sigma = 4 % of the median image width of the benchmark |
| `_regmean`, `cor media` | region-mean fill (supplementary only) |
| `T1.5`, `T2`, `P1.5`, `P2`, `doses` | enlarged occlusions (1.5x, 2x area; supplementary only) |
| `TXT`, `text-decoder-only`, `so-texto`, `sem imagem` | no-image baseline (same recipe, question only) |
| `headroom`, `ganho`, `G` | image gain (intact accuracy minus no-image-baseline accuracy) |
| `Delta`, `Delta_nec` | necessity effect (control-occluded accuracy minus target-occluded accuracy) |
| `custo da mascara deslocada` | control-occlusion drop `C` |
| `queda bruta`, `custo do alvo` | raw drop (intact minus target-occluded accuracy) |
| `sham`, `SHAM_*`, `oclusor em negativos` | occluder test on images without the target; `taxa induzida` = occluder-induced affirmative rate |
| `SHAM_ART`, `SHAM_POL_Q1`/`Q3`, `SHAM_INS` | box-artefact, polyp-shaped (first/third quartile area) and instrument-shaped occluders (Kvasir-VQA-x1) |
| `VT` (Qwen2-VL), `FT` (SmolVLM2) | runs with the vision-encoder setting swapped relative to the default (fine-tuned encoder for Qwen2-VL, frozen for SmolVLM2) |
| `encoder congelado` / `afinado` | frozen / fine-tuned vision encoder |
| `LORA`, `DORA` | adapter type |
| `M0`, `TF-IDF`, `question-only` | question-only classifier (TF-IDF + logistic regression; supplementary) |
| `L0`, `L1`, `L2`, `L3`, `escada` | criteria (i) raw drop, (ii) matched control, (iii) both fills, (iv) significant gain; `regra final` = criterion (v) |
| `resoluvel`, `resoluveis` | run with a significant image gain (lower CI bound above zero) |
| `declarado`, `necessaria` | run passing the necessity test (criterion (v)) |
| `IUT`, `Holm` | intersection-union test with Holm correction over the question subsets of a run |
| `polipo`, `instrumento`, `controle negativo` | polyp, instrument and negative-control question classes (Kvasir-VQA-x1) |
| `fechada-sim` / `fechada-nao`, `closed_yes` / `closed_no` | closed-ended questions whose reference answer is yes / no |
| `KVASIR`, `HEAL`, `MIMIC` | Kvasir-VQA-x1, HEAL-MedVQA, Medical-Diff-VQA |
| `linha`, `run` | one fine-tuned model (configuration x seed) |
| `rodada N`, `item N`, `S1..S25` | internal revision rounds and sheet sections; the paper uses sections S22-S25 (paired no-image baselines, criteria per subset with the 7B, lines cited by the text) |
| `QWEN25VL` | Qwen2.5-VL-7B; fine-tuned runs `QWEN25VL_{LORA,DORA}[_VT]_<benchmark>_seed<s>` (`_VT` = fine-tuned vision encoder), zero-shot model `QWEN25VL_ZEROSHOT` |
| `QWEN25VL_LORA_TXT`, `QWEN25VL_DORA_TXT` | no-image baselines of the 7B runs (LoRA and DoRA, same recipe, question only) |
| `C0_full`, `results_c0full` | intact-image predictions on the whole test set (reference of the occluder test; `full_test` directories) |
| `q25`, `qwen25vl_7b` | the Qwen2.5-VL-7B battery (scripts in `src/harness/v7_txt/qwen25vl_7b/`) |
| `v5_*`, `v6_*`, `v7_*`, `isbi_placebo`, `extra_runs` | directories of the original lab layout, kept in file paths recorded by the scripts |
| `E3`, `E6`, `E7`, `emenda`, `pre-registro`, `plano v2`, `§N` | internal protocol document of the study and its amendments (not distributed; E7: `negative`→`no`, `positive`→`yes` normalisation of zero-shot answers) |
| `piso`, `torre`, `braco`, `regime`, `RADORIG` | items of other internal studies that appear only inside the sheet or in script comments; not used by the paper |
<!-- glossary:end -->

Console messages, dictionary keys and the labels of the numbers sheet keep their original Portuguese names; the glossary gives the correspondence.

## Code provenance

`src/CODE_PROVENANCE.md` lists, for every released code file, the SHA-256 of the lab source and of the released copy, the upstream
commit and uncommitted-diff hash of the working tree, the code states recorded in the provenance stamps of the released predictions,
and the checks of the script hashes cited by the numbers sheet. `src/analysis/CHANGES_FOR_RELEASE.diff` is the complete diff between
the lab analysis scripts and the released ones (path configuration, host name and comment wording only).

## Model weights

`models/MANIFEST.md` lists the 117 fine-tuned runs (81 of the 2B models and M3AE, 36 of Qwen2.5-VL-7B), the no-image baselines
(LoRA and DoRA of the three families, grey-image M3AE) and the 9 no-image M3AE runs (39.9 GiB in total) with the path in the authors'
archive, size and SHA-256. The weights are available on request until a public host is chosen.

## What changed for the 7B

The submitted paper reports 117 fine-tuned runs (39 per benchmark): the 81 runs of Qwen2-VL-2B, SmolVLM2-2.2B and M3AE plus 36 runs of
Qwen2.5-VL-7B (LoRA and DoRA, frozen and fine-tuned vision encoder, three seeds, same recipe). The 7B family is enabled by default in
`src/analysis/common.py` (`A1_FAMILIAS_EXTRA=""` restores the 27-run analysis). `results/predictions/kvasir/` holds the per-item predictions of the
12 Kvasir-VQA-x1 7B runs (intact image, target and control occlusions under black, blur 10 % and blur 4 %, the eight occluder conditions, the
full-test intact predictions and the no-image baselines); for HEAL-MedVQA and Medical-Diff-VQA only per-run aggregates are released, as for the 2B
runs. `results/analysis/` was regenerated with the 39 lines (36 new `necessity_v2` files), the sheet has sections S24 (criteria per question subset,
fine-tuned and zero-shot) and S25 (lines cited by the text), Table 1 has two column blocks (fine-tuned runs of 39; zero-shot models of 4) and
Tables 2 and 3 have the two 7B groups; Table 2 reads the image gain and the pass counts from the paired no-image baselines (sheet section S23)
and leaves the HEAL-MedVQA yes-questions block to the supplementary table (`A1_TABELA2_SEM_HEAL_SIM=0` restores it). `configs/training/` has the
18 7B configurations, `models/MANIFEST.md` the 54 7B adapters, `src/harness/v7_txt/qwen25vl_7b/` the battery scripts and job list, and
`environment/VERSIONS.md` the software versions of the 7B runs.

## Licenses of this repository

Code: MIT (`LICENSE`). Data files derived from Kvasir-VQA-x1, Kvasir-SEG and Kvasir-Instrument (`results/predictions/kvasir/`, `data/kvasir/`,
`data/blur4/`, the Kvasir entries of `results/analysis/`): research and educational use only, CC BY-NC 4.0 with citation of the dataset
papers (`LICENSE-DATA.md`).

## Citation

See `CITATION.cff`. Please also cite the datasets you use (Kvasir-VQA-x1, Kvasir-SEG, Kvasir-Instrument, HEAL-MedVQA,
VinDr-CXR, Medical-Diff-VQA, MIMIC-CXR-JPG, Chest ImaGenome) and the model papers (Qwen2-VL, SmolVLM2, M3AE, LoRA, DoRA).
