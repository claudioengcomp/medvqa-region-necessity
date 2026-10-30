"""Extract per-item predictions from M3AE for ONE condition (C0/C1/C2/C4_*)
of ANY dataset supported by M3AE (--dataset-key), computing
accuracy/n/n_correct directly from the forward pass, without parsing the
PyTorch Lightning log. Writes a complete results record (harness/results_schema.py,
including 'predictions') ready for paired McNemar/bootstrap analysis via
harness.stats.compute_vdd.compute_summary_vs_baseline.

This script only runs inside the dedicated M3AE environment, with the M3AE
repository cloned locally; M3AE pins an older dependency stack (its own conda
environment) than the generative models, so the two cannot share one
environment. It is NOT covered by the local pytest suite (no GPU/torch on a
development laptop). The pure condition-swapping logic is isolated in
harness/interventions/arrow_swap.py, which is tested locally.

`--dataset-key` (default 'vqa_slack') drives TWO things at once, taking
advantage of M3AE using the same key in both places: the Sacred named config
('task_finetune_<dataset_key>') and the arrow file name
('<dataset_key>_test.arrow'). For VQA-RAD, pass --dataset-key vqa_vqa_rad.

Usage (inside the M3AE environment, cwd = repository root):
    python -m harness.inference.extract_predictions_m3ae \
        --m3ae-dir path/to/M3AE \
        --condition-arrow path/to/M3AE/data/finetune_arrows/vqa_slack_test_c1.arrow \
        --model M3AE --dataset SLAKE --condition C1 \
        --dataset-key vqa_slack \
        --checkpoint downloaded/finetuned/vqa/slack/m3ae_finetuned_vqa_slack_84.3.ckpt \
        --output results/M3AE_SLAKE_C1.json

Kvasir (clean split, vqa_label_size=500 -- see the build_m3ae_config docstring):
    python -m harness.inference.extract_predictions_m3ae \
        --m3ae-dir path/to/M3AE \
        --condition-arrow path/to/M3AE/data/finetune_arrows/vqa_kvasir_test.arrow \
        --model M3AE --dataset KVASIR --condition C0 \
        --dataset-key vqa_kvasir --vqa-label-size 500 \
        --checkpoint <the seed's .ckpt checkpoint> \
        --output results/M3AE_KVASIR_seed0_C0.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from harness.interventions.arrow_swap import swap_test_arrow
from harness.results_schema import validate_results_dict


def _enter_m3ae_dir(m3ae_dir: str) -> None:
    """Importing `m3ae.*` and resolving the relative paths in the Sacred
    config (`data_root=data/finetune_arrows/`,
    `tokenizer=downloaded/roberta-base`, `load_path=downloaded/...`) requires
    BOTH `cwd == m3ae_dir` AND `m3ae_dir` on sys.path -- exactly what M3AE's
    own launch scripts do by `cd`-ing into the M3AE directory before invoking
    `main.py`. That requirement is independent of (and cannot be satisfied by)
    the cwd of the process invoking this script via
    `python -m harness.inference.extract_predictions_m3ae`, which must keep running
    from this repository's root in order to import `src.*` in the first place
    -- hence the chdir happens HERE, inside the function, rather than being
    imposed on the caller."""
    if m3ae_dir not in sys.path:
        sys.path.insert(0, m3ae_dir)
    os.chdir(m3ae_dir)


def build_m3ae_config(checkpoint: str, dataset_key: str = "vqa_slack",
                       vqa_label_size: int | None = None) -> dict:
    """Reuse the Sacred config parser from M3AE's own main.py (m3ae.config.ex),
    with the SAME arguments used to fine-tune these checkpoints -- no config
    value is reconstructed by hand, which removes any risk of drifting from
    the config actually used at training/evaluation time. Assumes
    _enter_m3ae_dir() has already run (cwd == m3ae_dir).

    image_size=384 is fixed for every supported dataset: it is the value used
    for SLAKE AND the same value that M3AE's own fine-tuning script passes
    explicitly for VQA-RAD (overriding the 576 default of the
    task_finetune_vqa_vqa_rad named config) -- this is not a choice of ours,
    it is what the M3AE authors already use in both cases.

    vqa_label_size (optional): overrides the hardcoded default of the Sacred
    named config. task_finetune_vqa_kvasir declares vqa_label_size=501, which
    is stale -- that is the answer-vocabulary size of the older, leaked split.
    The Kvasir clean-split checkpoint was trained with vqa_label_size=500 (the
    same override applied at fine-tuning time). Without passing it here, the
    head built by M3AETransformerSS(config) comes out with 501 classes and
    load_state_dict on the checkpoint (500 classes) fails with a shape
    mismatch. SLAKE/VQA-RAD do not need this (their named configs already
    match the existing checkpoints), so the None default preserves the
    previous behaviour with no override."""
    sys.argv = [
        "main.py", "with",
        "data_root=data/finetune_arrows/",
        "num_gpus=1", "num_nodes=1",
        f"task_finetune_{dataset_key}",
        "per_gpu_batchsize=16",
        "clip16", "text_roberta",
        "image_size=384",
        "test_only=True",
        "tokenizer=downloaded/roberta-base",
        f"load_path={checkpoint}",
    ]
    if vqa_label_size is not None:
        sys.argv.append(f"vqa_label_size={vqa_label_size}")
    from m3ae.config import ex

    captured: dict = {}

    @ex.main
    def _capture(_config):
        captured["config"] = _config

    ex.run_commandline()
    return captured["config"]


def _move_batch_to_device(batch: dict, device: str) -> dict:
    import torch

    moved = {}
    for k, v in batch.items():
        if isinstance(v, torch.Tensor):
            moved[k] = v.to(device)
        elif isinstance(v, list) and len(v) > 0 and isinstance(v[0], torch.Tensor):
            moved[k] = [t.to(device) for t in v]
        else:
            moved[k] = v
    return moved


def extract_predictions(m3ae_dir: str, checkpoint: str, dataset_key: str = "vqa_slack",
                         vqa_label_size: int | None = None) -> tuple[list[dict], dict]:
    """Run M3AE's forward pass over the CURRENT test_dataloader (whichever
    file sits at '<dataset_key>_test.arrow' at call time -- swap it in
    beforehand via harness.interventions.arrow_swap.swap_test_arrow, BEFORE
    calling this function, because swap_test_arrow takes m3ae_dir and
    operates outside of here) and return (predictions, meta).
    meta['accuracy'] is recomputed directly from the predictions, never read
    from any log.

    vqa_label_size: forwarded straight to build_m3ae_config() -- see the
    docstring there for the rationale (the Kvasir clean-split checkpoint
    needs 500, not the named config's default of 501)."""
    import copy

    _enter_m3ae_dir(m3ae_dir)  # cwd + sys.path -> from here on, m3ae.* is importable

    import torch

    config = copy.deepcopy(build_m3ae_config(checkpoint, dataset_key=dataset_key,
                                              vqa_label_size=vqa_label_size))

    from m3ae.datamodules.multitask_datamodule import MTDataModule
    from m3ae.modules import M3AETransformerSS

    # MTDataModule (not VQASLACKDataModule directly): this is what main.py
    # actually uses. Found while running for real -- VQASLACKDataModule on its
    # own inherits BaseDataModule.test_dataloader(), which passes
    # collate_fn=self.test_dataset.collate WITHOUT binding mlm_collator (a
    # mandatory positional argument of BaseDataset.collate), blowing up with
    # "TypeError: collate() missing 1 required positional argument:
    # 'mlm_collator'" as soon as the DataLoader tries to assemble the first
    # batch. MTDataModule.setup() builds the collate_fn correctly via
    # functools.partial(dataset.collate, mlm_collator=...) before handing it
    # to the DataLoader -- see m3ae/datamodules/multitask_datamodule.py.
    # dist=False (not dist=True as in main.py): we do not run DDP here, so no
    # DistributedSampler is needed -- MTDataModule already handles dist=False
    # internally (test_sampler=None, sequential iteration).
    dm = MTDataModule(config, dist=False)
    dm.setup(stage="test")

    model = M3AETransformerSS(config)  # loads the checkpoint by itself: test_only=True + load_path (m3ae_module.py, block "5. Load Models For Testing")
    model.eval()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # id2answer lives on the per-dataset datamodule (dm.dms[0]), not on the
    # MTDataModule wrapper -- since config["datasets"] always holds a single
    # dataset (fixed by the task_finetune_<dataset_key> named config),
    # dm.dms[0] is always the right datamodule, whatever the dataset is.
    id2answer = dm.dms[0].id2answer

    predictions: list[dict] = []
    n_correct = 0
    with torch.no_grad():
        for batch in dm.test_dataloader():
            batch_on_device = _move_batch_to_device(batch, device)
            infer = model.infer(batch_on_device, mask_text=False, mask_image=False)
            vqa_logits = model.vqa_head(infer["multi_modal_cls_feats"])

            vqa_targets = torch.zeros(len(vqa_logits), config["vqa_label_size"], device=device)
            for i, (labels, scores) in enumerate(zip(batch["vqa_labels"], batch["vqa_scores"])):
                for label, score in zip(labels, scores):
                    vqa_targets[i, label] = score

            pred_label_ids = vqa_logits.argmax(dim=-1)
            for i in range(len(pred_label_ids)):
                pid = int(pred_label_ids[i].item())
                item_score = float(vqa_targets[i, pid].item())
                correct = item_score >= 0.5
                n_correct += int(correct)
                gold_answers = batch["vqa_answer"][i]
                predictions.append({
                    "qid": int(batch["qid"][i]),
                    "predicted": str(id2answer[pid]),
                    "gold": str(gold_answers[0]) if gold_answers else "",
                    "correct": bool(correct),
                })

    n = len(predictions)
    meta = {"n": n, "n_correct": n_correct, "accuracy": (n_correct / n) if n else 0.0}
    return predictions, meta


def build_results_record_from_predictions(model: str, dataset: str, condition: str,
                                           predictions: list[dict], meta: dict) -> dict:
    record = {
        "model": model, "dataset": dataset, "condition": condition,
        "accuracy": meta["accuracy"], "n": meta["n"], "n_correct": meta["n_correct"],
        "predictions": predictions,
    }
    validate_results_dict(record)
    return record


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m3ae-dir", required=True)
    parser.add_argument("--condition-arrow", required=True,
                         help="Path to the .arrow of this condition (e.g.: vqa_slack_test_c4_occ_25.arrow)")
    parser.add_argument("--model", default="M3AE")
    parser.add_argument("--dataset", default="SLAKE")
    parser.add_argument("--dataset-key", default="vqa_slack",
                         help="Dataset key in M3AE (drives the Sacred named config "
                              "'task_finetune_<dataset_key>' and the arrow name "
                              "'<dataset_key>_test.arrow'). E.g.: vqa_slack, vqa_vqa_rad.")
    parser.add_argument("--condition", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--vqa-label-size", type=int, default=None,
                         help="Overrides vqa_label_size from the Sacred named config (e.g.: 500 "
                              "for the Kvasir clean-split, whose checkpoint does not match the "
                              "hardcoded default of 501 in the named config). Omitting it preserves "
                              "the current behaviour (SLAKE/VQA-RAD do not need this).")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    output_path = os.path.abspath(args.output)  # resolve BEFORE the chdir inside _enter_m3ae_dir
    test_arrow_filename = f"{args.dataset_key}_test.arrow"
    with swap_test_arrow(args.m3ae_dir, args.condition_arrow, test_arrow_filename=test_arrow_filename):
        predictions, meta = extract_predictions(args.m3ae_dir, args.checkpoint, dataset_key=args.dataset_key,
                                                  vqa_label_size=args.vqa_label_size)
    args.output = output_path
    record = build_results_record_from_predictions(
        args.model, args.dataset, args.condition, predictions, meta,
    )
    with open(args.output, "w", encoding="utf-8") as fp:
        json.dump(record, fp, indent=2, ensure_ascii=False)
    print(f"{args.model}/{args.dataset}/{args.condition}: "
          f"accuracy={record['accuracy']:.4f} ({record['n_correct']}/{record['n']}) -> {args.output}")
