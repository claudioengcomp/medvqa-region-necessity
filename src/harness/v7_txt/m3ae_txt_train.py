"""Wrapper (lapa) around run_m3ae_txt.sh for infer_scheduler_v7: bash <script> <bench> <seed>; inherits CUDA_VISIBLE_DEVICES."""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import subprocess, sys
import os
mode = sys.argv[3] if len(sys.argv) > 3 else "gray"; assert mode in ("gray", "img", "rediv", "redivgray", "qlevel", "qlevelgray"), mode   # 17/10: rediv/redivgray (extra_runs)   # 13/10: img = _gpu1 retraining with real images
sys.exit(subprocess.call(["bash", os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/worktree/harness/v7_txt/run_m3ae_txt.sh", sys.argv[1], sys.argv[2]], env=dict(os.environ, M3AE_MODE=mode)))
