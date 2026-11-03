# Training configurations

One YAML per configuration; the seed is passed on the command line: `python -m med_vlm.run_experiment --config <yaml> --seed <0|1|2>`
(run from `src/`). Output and checkpoint directories (`outputs_dir`, `results_json_dir`, `checkpoint_dir`) are written as `${OUTPUT_ROOT}/<group>`; set them to your own paths. Nothing else was changed in the files.

- `kvasir/`, `heal/`, `mimic/`: the 2B runs with image. `qwen2vl_{lora,dora}_<bench>.yaml` = frozen vision encoder (adapter on the
  language-model attention projections); `qwen2vl_{lora,dora}_vt_<bench>.yaml` = fine-tuned encoder (adapter also on the vision
  attention); `smolvlm2_{lora,dora}_<bench>.yaml` = fine-tuned encoder (default for SmolVLM2); `smolvlm2_{lora,dora}_ft_<bench>.yaml` =
  frozen encoder. `smolvlm2_dora_kvasir_e6.yaml` is the configuration of seeds 1 and 2 of the SmolVLM2 DoRA Kvasir run (rerun after a
  crash of the original jobs; identical recipe). `qwen2vl_dora_heal_seed2_retrain20261003.yaml`: retraining of one run whose
  adapter file had been lost (same recipe).
- `no_image/`: the no-image baselines (`data.no_image: true`; adapter on the language model only), LoRA and DoRA, three benchmarks, three families.
- Qwen2.5-VL-7B (`qwen25vl_*.yaml`, 18 files): `qwen25vl_lora_<bench>.yaml` / `qwen25vl_dora_<bench>.yaml` = frozen vision encoder, `qwen25vl_{lora,dora}_vt_<bench>.yaml` =
  fine-tuned encoder, `no_image/qwen25vl_{lora,dora}_txt_<bench>.yaml` = no-image baselines; same recipe as the 2B runs (the header of each file names its
  source configuration). The DoRA files are written by `src/harness/v7_txt/qwen25vl_7b/make_configs_q25_dora.py` from the LoRA ones.
- `m3ae/`: command lines of the M3AE runs (full fine-tuning from the authors' pretrained checkpoint; grey-image and no-image baselines).

Common recipe: rank 16, alpha 32, learning rate 2e-4, warm-up 5 %, 3 epochs, batch 4 x 4 accumulation steps, max length 8192
(1024 for the no-image runs), bf16, gradient checkpointing; the last epoch is kept.
