# Data: what is here and how to rebuild the rest

No image, mask or pixel data is distributed. This directory holds the derived files for the public benchmark and the parameters of
the occlusions; everything else is rebuilt by the scripts below from the official sources (see the README for sources and terms).

## Kvasir-VQA-x1 (public)
- `kvasir/split_image_ids.json`: our image-disjoint split (train / val / test image ids) of SimulaMet/Kvasir-VQA-x1
  (snapshot 61e41148c3214bc5140ad0ab4c28520a512e2a73). The official split assigns image-question pairs, not images, to the
  partitions; 94 % of its test images also appear in training.
- `kvasir/inventory_kvasir_test_clean.json`: test inventory: for every question its class (polyp, instrument, negative control,
  ...), target kind, whether it is evaluable and why not; for every image the mask availability, field-of-view fraction, target
  area and the control-occlusion placement method.
- `kvasir/manifest_kvasir.json`: per unit (image x target) the placement of the control occlusion actually used (method, pixel
  offsets/scale, areas), the enlarged-occlusion variants and the checksums of the arrows.
- `kvasir/kvasir_vqa_to_seg_instrument_map.json`: correspondence between Kvasir-VQA-x1 images and the Kvasir-SEG / Kvasir-Instrument masks.
- `kvasir/M0_question_only_KVASIR_C0.json`: question-only classifier predictions (supplementary).
- `kvasir/blur_sigma_report.json`: image widths and the 4 % blur scale (25 px = 4 % of the median width, 626 px).
- `kvasir/occluder/`: inventory and manifest of the occluder test (occluder placed on images without the target: box-artefact
  rectangle, polyp-shaped and instrument-shaped donor masks; placement, sizes, questions).
- `blur4/`: scale and checksums of the fixed-scale blur arrows for the three benchmarks (HEAL-MedVQA 33.99 px, Medical-Diff-VQA 35.10 px).

## Control-occlusion placement (parameters; pixel coordinates only for Kvasir-VQA-x1)
- Kvasir-VQA-x1: candidate placements in order horizontal flip, vertical flip, 180-degree rotation, then up to 50 random integer
  translations; seed per image = sha256("20260913:<image_id>"); the control must not touch the target dilated by 5 px, must have
  at least 80 % of its area inside the field of view, and targets above 40 % of the field of view are excluded.
- HEAL-MedVQA: another annotated anatomy of the same image with area ratio 0.7-1.4 and overlap at most 5 % of the target; otherwise
  the horizontal mirror of the target; otherwise the Kvasir placer constrained to at least 80 % inside a thoracic atlas built from the
  annotations.
- Medical-Diff-VQA (targets with several boxes get one control per box): homologous anatomy without the finding (area ratio
  0.8-1.25) -> vertical translation with exact area (bilateral pairs move together) -> horizontal mirror per box -> enlarged
  anatomy (0.5-2.0x); constraints: at least 80 % inside the thoracic atlas, entirely inside the film, not touching the target dilated
  by 5 px, no overlap among control boxes.
- Fills: black; Gaussian blur with sigma = 10 % of the image width; Gaussian blur with a fixed sigma = 4 % of the benchmark's median
  width; region mean (supplementary). Occluded images are encoded as lossless PNG from the decoded pixels; the intact condition keeps
  the original bytes.

## Rebuilding the arrows (each script documents its command line in its module docstring; run from `src/`)
- Kvasir-VQA-x1: `harness/prepro/build_kvasir_clean_split.py` (download, atomic questions, image-disjoint split) ->
  `harness/isbi_placebo/inventory_kvasir.py` (needs the Kvasir-SEG and Kvasir-Instrument mask folders) ->
  `harness/isbi_placebo/make_placebo_conditions.py` (intact, target, control, enlarged, fills) -> `harness/v7_sham/make_kvasir_sham.py`
  (occluder test) -> `blur4/make_blur4_arrows.py` (fixed-scale blur).
- HEAL-MedVQA (credentialed): `harness/isbi_placebo/heal/heal_ids.py`, `run_aws_download.sh` / `vindr_verify.py` (VinDr-CXR DICOMs),
  `dicom_to_png.py`, `inventory_heal.py`, `thorax_atlas.py`, `make_heal_conditions.py`, `make_heal_train_arrows.py`; enlarged
  occlusions: `harness/v7_txt/make_heal_dose_arrows.py`.
- Medical-Diff-VQA (credentialed): `mimic_pipeline/01_download_tables.sh` ... `18_validate_conditions.py` (subset, images from
  MIMIC-CXR-JPG, Chest ImaGenome regions, test items, control placement, arrows); occluder test and blank-image condition in
  `harness/v7_txt/` (`placebo_mimic.py`, `make_c1_mimic_fechadas.py` is not needed by the paper).
- M3AE inputs: the same arrows in the M3AE arrow format (`harness/v7_txt/make_gray_arrows_mimic.py` and the wrappers in `src/m3ae_patch/README.md`).
- Absolute paths of the original server were replaced by the `LAB_ROOT` environment variable in these scripts; set it to the root
  of your copy of the data.
