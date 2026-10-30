# Changes to the upstream M3AE code

Upstream: https://github.com/zhjohnchan/M3AE (commit in `UPSTREAM_COMMIT.txt`; no license file is declared upstream, checked on
2026-10-30). No upstream file is redistributed here, modified or not: everything is expressed as hunks.

Hunks over upstream files (`m3ae_changes.patch`): `m3ae/config.py`, `m3ae/datamodules/__init__.py`, `m3ae/datasets/__init__.py`,
`m3ae/modules/m3ae_module.py`, `m3ae/modules/language_encoders/bert_model.py`. New modules (`new_modules.patch`, as hunks over their
templates): `m3ae/datamodules/vqa_{kvasir,heal,mimic}_datamodule.py`, `m3ae/datasets/vqa_{kvasir,heal,mimic}_dataset.py`. To reproduce our M3AE runs:

1. `git clone https://github.com/zhjohnchan/M3AE && cd M3AE && git checkout <commit>`
2. `git apply <this dir>/m3ae_changes.patch` — adds the datasets to `m3ae/config.py`, `m3ae/datamodules/__init__.py` and
   `m3ae/datasets/__init__.py`, the `no_image` configuration flag and the no-image forward path in `m3ae/modules/m3ae_module.py`
   and `m3ae/modules/language_encoders/bert_model.py` (`forward_text_only`).
3. `patch -p0 < <this dir>/new_modules.patch` after copying the upstream templates it names (comment lines `# cp <template> <new>`):
   the six new dataset/datamodule modules of this work (Kvasir-VQA-x1, HEAL-MedVQA, Medical-Diff-VQA) are the upstream
   `vqa_vqa_rad_*` modules with the names changed and are therefore distributed only as hunks against those templates. The generators
   used in this work (`src/harness/patch_m3ae_kvasir.py`, `patch_m3ae_heal.py`, `v7_txt/patch_m3ae_mimic.py`) produce byte-identical
   modules by reading the templates from the clone.
4. Download the authors' `m3ae.ckpt` and `roberta-base` as instructed upstream (checksum in `environment/VERSIONS.md`).
5. Install `environment/environment-m3ae.yml` (the authors' own pin list is `requirements.txt` in the upstream repository).

The no-image path is the set of hunks of `m3ae_changes.patch` marked "no-image variant" (config flag `no_image`, the text-only forward
in `m3ae_module.py` and `forward_text_only` in `bert_model.py`). `tests/m3ae_no_image_tests.py` and
`tests/no_image_tests.json` are the tests run before training: with the flag off, logits identical to the upstream code; with the flag on,
logits identical for grey, black, random, real and no image; the visual encoder is never called; initialisation unchanged (one batch of
16 validation questions of VQA-RAD, used as a unit-test batch; the test script keeps that dataset reference).

Training and inference wrappers used by the paper are in `src/harness/v7_txt/` (see `configs/training/m3ae/README.md`).
