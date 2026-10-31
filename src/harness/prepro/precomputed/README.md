# Precomputed artefacts

Outputs of `harness/prepro/` scripts that depend on raw data available only locally; committed here so that they do not have to be
regenerated.

## `vqa_slack_test_pathology_labels.json`

Output of `harness/prepro/build_slake_pathology_labels.py --modality X-Ray --location Lung`, run on 21/08/2026 against the original
raw SLAKE files `Slake1.0/{train,test,validate}.json` (not redistributed, by licence). 130 images, one pathology label per `image_id`.

**Not confirmed**: whether the `imgs/` prefix of the keys matches the `image_id` column of the actual `vqa_slack_test.arrow`. Confirm
this before using the file.
