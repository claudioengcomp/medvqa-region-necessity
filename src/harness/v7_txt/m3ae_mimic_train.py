"""Wrapper (lapa) around run_m3ae_mimic.sh for infer_scheduler_v7: <script> <seed> [img|gray]; inherits CUDA_VISIBLE_DEVICES.
13/10: optional mode (default img, identical to the 11/10 one); gray = text-only M3AE on MIMIC (M3AE_MODE=gray)."""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import os, subprocess, sys
mode = sys.argv[2] if len(sys.argv) > 2 else "img"; assert mode in ("img", "gray"), mode
env = dict(os.environ, M3AE_MODE=mode)
sys.exit(subprocess.call(["bash", os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/worktree/harness/v7_txt/run_m3ae_mimic.sh", sys.argv[1]], env=env))
