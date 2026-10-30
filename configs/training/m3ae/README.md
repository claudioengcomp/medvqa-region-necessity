# M3AE runs

M3AE (Chen et al., MICCAI 2022) is fine-tuned with the upstream code patched as described in `src/m3ae_patch/README.md`, starting
from the authors' pretrained checkpoint `m3ae.ckpt` (SHA-256 in `environment/VERSIONS.md`), CLIP-ViT-B/16 image encoder at 384 px,
RoBERTa-base text encoder, batch 16 per GPU, one GPU, the upstream VQA fine-tuning schedule; the checkpoint with the best validation
metric is used. Three seeds per benchmark.

Command (upstream Sacred interface; `<task>` = `task_finetune_vqa_kvasir`, `task_finetune_vqa_heal` or `task_finetune_vqa_mimic`):

```
python main.py with data_root=<arrow dir> num_gpus=1 num_nodes=1 <task> per_gpu_batchsize=16 clip16 text_roberta image_size=384 \
    tokenizer=downloaded/roberta-base load_path=downloaded/pretrained/m3ae.ckpt seed=<s>
```

- Runs with image: `<arrow dir>` holds the benchmark's train/val/test arrows in the M3AE format (`src/harness/run_finetune_m3ae.sh`).
- Grey-image no-image baseline (superseded by the no-image run): the same with arrows whose images are a constant grey 384x384 image
  (`src/harness/v7_txt/run_m3ae_txt.sh`, `m3ae_txt_train.py`).
- No-image baseline used by the paper: the same arrows with `no_image=True` (image path removed: the visual encoder is not run, the
  cross-attention to image tokens is dropped from the text-side fusion layers keeping residual and layer norm, and the image half
  of the classifier input is zero): `src/harness/v7_txt/m3ae_semimg_train.py`, `m3ae_semimg_cfg.py`.
- Inference on the occlusion arrows: `src/harness/v7_txt/m3ae_infer_v7.py` (and `m3ae_mimic_predict.py`, `m3ae_semimg_predict.py`).
