# License of the data files in this repository

**Scope.** The MIT license (`LICENSE`) covers only the source code. The files listed below are derived from third-party datasets, are
*not* MIT-licensed and keep the terms of their sources: **Kvasir-VQA-x1** (CC BY-NC 4.0; Gautam, Riegler and Halvorsen, 2025), with
masks from **Kvasir-SEG** (Jha et al., 2020) and **Kvasir-Instrument** (Jha et al., 2021), whose terms of use restrict them to research
and educational purposes and require citing the dataset papers. These derived files (question ids, question text, reference answers,
model predictions, image identifiers, mask correspondences, control-occlusion placements) are therefore shared for research and
educational purposes only, under CC BY-NC 4.0, and the three dataset papers must be cited together with ours. No image or mask
pixels are redistributed.

- `results/predictions/kvasir/` (per-item predictions carrying the Kvasir-VQA-x1 question text and reference answers);
- `data/kvasir/split_image_ids.json` (image-disjoint split of Kvasir-VQA-x1);
- `data/kvasir/kvasir_vqa_to_seg_instrument_map.json` (correspondence to the Kvasir-SEG / Kvasir-Instrument masks);
- `data/kvasir/inventory_kvasir_test_clean.json`, `data/kvasir/manifest_kvasir.json`, `data/kvasir/occluder/*` (test inventory, control-occlusion placements and occluder-test units, derived from the masks and the questions);
- `data/kvasir/M0_question_only_KVASIR_C0.json`, `data/kvasir/blur_sigma_report.json`, `data/blur4/*`;
- the Kvasir-VQA-x1 entries of `results/analysis/` and the tables/figure derived from them.

HEAL-MedVQA / VinDr-CXR, Medical-Diff-VQA, MIMIC-CXR-JPG and Chest ImaGenome are credentialed datasets. Nothing derived from them
at the item level is in this repository: only per-run aggregates (accuracies, effects, confidence intervals, counts) and the scripts
that rebuild the test items from the official files.

## Terms of use quoted from the sources (read 2026-10-30)

- Kvasir-VQA-x1 (https://huggingface.co/datasets/SimulaMet/Kvasir-VQA-x1): "Released under CC BY-NC 4.0 - for academic and non-commercial use. Please cite appropriately."
- Kvasir-SEG (https://datasets.simula.no/kvasir-seg/): "The use of the Kvasir-SEG dataset is restricted for research and educational purposes. The use of the Kvasir-SEG dataset for commercial purposes is forbidden without prior written permission. [...] In all documents and publications that use the Kvasir-SEG dataset or report experimental results based on the Kvasir-SEG dataset, a reference to the dataset paper has to be included."
- Kvasir-Instrument (https://datasets.simula.no/kvasir-instrument/): "The use of the Kvasir-instrument dataset is restricted to research and education purposes. The use of the dataset is forbidden for commercial use without prior written permission. [...] a reference to the dataset paper has to be included."
- HEAL-MedVQA (https://huggingface.co/datasets/MM-Hallu/HEAL-MedVQA): license tag MIT; images from VinDr-CXR (PhysioNet credentialed access), whose terms we follow for everything derived from them.
