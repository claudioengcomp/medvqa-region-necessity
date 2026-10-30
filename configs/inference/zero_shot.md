# Zero-shot models: prompts and decoding

Driver: `python -m harness.extract_predictions_circle --model <KEY> --peft ZEROSHOT --dataset <BENCH> --condition <COND> --condition-arrow <arrow>
--instruction "Answer with a single word or a short phrase." --instruction-mode <mode> --output <json>` (`--no-image` for the no-image condition).

| model key | Hub id (snapshot in environment/VERSIONS.md) | instruction mode | max new tokens |
|---|---|---|---|
| MEDGEMMA | google/medgemma-1.5-4b-it | system message (Gemma 3 chat template) | 64 |
| QWEN25VL | Qwen/Qwen2.5-VL-7B-Instruct | system message | 64 |
| LLAVA_MED | chaoyinshe/llava-med-v1.5-mistral-7b-hf | prefix of the question text (template without a system role) | 64 |
| MEDVLTHINKER | UCSC-VLAA/MedVLThinker-7B-RL_PMC | appended to the model's reasoning system prompt (`_MEDVLTHINKER_SYSTEM_PROMPT` in `src/med_vlm/training/spec_registry.py`); answer read from `<answer>` tags | 512 |

Decoding is greedy; bf16 (LLaVA-Med: dtype auto); images capped at 512x512 pixels for the Qwen family (`src/med_vlm/models/loader.py`).
Answers are normalised like the fine-tuned runs (`src/med_vlm/metrics/process_text.py`); on closed-ended questions `negative` is read as
`no` and `positive` as `yes` (`src/harness/v7_txt/rescore_e7.py`). Conditions: intact image, no image, target and control occlusion
(black and blur), sufficiency, and the occluder test on the no-questions of Medical-Diff-VQA.
