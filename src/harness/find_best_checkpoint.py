"""Locates the 'best' checkpoint saved by a real M3AE training run (items 3 and
4 of the extended scope -- training from scratch starting from pretrained/m3ae.ckpt).

PyTorch Lightning saves checkpoints under
`<log_dir>/<run_name>/version_N/checkpoints/`, with the 'best' file name
derived from epoch/step (not predictable in advance -- e.g.
'epoch=7-step=344.ckpt') and, because of `save_last=True` in
`ModelCheckpoint` (main.py), also a `last.ckpt` next to it -- which is NOT the
checkpoint that main.py uses for `trainer.test(ckpt_path="best", ...)`.
"""
from __future__ import annotations

import glob
import os


def find_best_checkpoint(search_root: str, after_timestamp: float = 0.0) -> str:
    """Search recursively for `**/checkpoints/*.ckpt` under `search_root`,
    ignore files named 'last.ckpt', keep only those modified after
    `after_timestamp` (isolates the checkpoint of ONE specific training run
    in a Colab session where several runs may happen) and return the
    most recent among the remaining candidates. Raises FileNotFoundError if
    no candidate is left."""
    candidates = glob.glob(os.path.join(search_root, "**", "checkpoints", "*.ckpt"), recursive=True)
    candidates = [c for c in candidates if os.path.basename(c) != "last.ckpt"]
    candidates = [c for c in candidates if os.path.getmtime(c) >= after_timestamp]
    if not candidates:
        raise FileNotFoundError(
            f"Nenhum checkpoint 'best' encontrado sob {search_root} "
            f"(modificado depois de {after_timestamp})"
        )
    return max(candidates, key=os.path.getmtime)


def _parse_args():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--search-root", required=True)
    parser.add_argument("--after-timestamp", type=float, default=0.0)
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    print(find_best_checkpoint(args.search_root, after_timestamp=args.after_timestamp))
