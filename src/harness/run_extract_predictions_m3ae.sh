#!/usr/bin/env bash
# Activates the conda environment 'lapa' (torch/pytorch-lightning/transformers) and runs
# harness.extract_predictions_m3ae with the received arguments -- without this, a
# subprocess launched directly from the notebook kernel falls into the base Python of
# the notebook environment, which does not have the heavy stack.
#
# Usage: bash harness/run_extract_predictions_m3ae.sh <extract_predictions_m3ae args>

set -euo pipefail

# On installations where the shell was not initialised by conda, this script, run as a new
# bash process, does not inherit the shell functions of its caller, and a bare `source activate lapa`
# fails with "activate: No such file or directory". Explicitly sourcing conda.sh + `conda activate`
# fixes it, with a fallback to the old `source activate` syntax for environments that support it.
if [ -f "${LAB_ROOT}/miniconda3/etc/profile.d/conda.sh" ]; then
  source ${LAB_ROOT}/miniconda3/etc/profile.d/conda.sh
fi
conda activate lapa 2>/dev/null || source activate lapa
# -u (unbuffered): same finding documented in run_finetune_m3ae.sh --
# the stdout of subprocess.run(['bash', ...]) in the notebook is not an interactive
# terminal, so Python block-buffers without it.
exec python -u -m harness.extract_predictions_m3ae "$@"
