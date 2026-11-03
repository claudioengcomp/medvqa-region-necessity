"""Schema and validation for the result records of the P0 harness.

A "results record" describes the performance of ONE model under ONE condition
(C0/C1/C2) on ONE dataset. Two levels of detail are supported:

- Aggregate mode (always mandatory): model, dataset, condition, accuracy.
  'n'/'n_correct' are optional, but required for the bootstrap CI.
- Paired mode (optional): 'predictions', a list of
  {"qid": ..., "predicted": str, "gold": str, "correct": bool} per item.
  Required for the McNemar test and the paired bootstrap.
"""
from __future__ import annotations

REQUIRED_KEYS = ("model", "dataset", "condition", "accuracy")
VALID_CONDITIONS = (
    "C0", "C1", "C2", "C5", "C6",
    "C4_OCC_25", "C4_OCC_50", "C4_OCC_75",
    "C4_NOISE_25", "C4_NOISE_50", "C4_NOISE_75",
    # C7 reserved (26/08/2026): positional-occlusion control condition
    # -- renamed from C6 to C7 when C6 came to mean "same organ+modality,
    # free category".
    # Not implemented yet -- added here only to reserve the name.
    "C7",
    # ISBI 2027, placebo posicional (docs/isbi/placebo/preregistration_v2.md): C0 restrita
    # the evaluable questions (and C0_orig, diagnostic with the original bytes), target T,
    # control occlusion P (`placebo` in the code), sufficiency S, dose 1.5x/2x, and mean/blur fills.
    "C0_orig", "T", "P", "S", "T1.5", "P1.5", "T2", "P2", "S2",
    "T_mean", "P_mean", "T_blur", "P_blur",
    # blur sigma ablation (run of 14/09/2026): sigma = 1/3/10 % of the width, and region mean color
    "T_blur1", "P_blur1", "T_blur3", "P_blur3", "T_blur10", "P_blur10", "T_regmean", "P_regmean",
    "T_ringmean", "P_ringmean",   # E3: mean colour of the surroundings (15 px ring)
    # v7 (2026-10-09): text-only arm (TXT), C0 of the crossed questions of the occluder test (C0_cross) and the
    # occluder-test (`sham`) conditions of Kvasir/SLAKE (occluder on an image without the finding)
    "TXT", "C0_cross",
    "SHAM_ART_black", "SHAM_ART_blur10", "SHAM_POL_Q1_black", "SHAM_POL_Q1_blur10",
    "SHAM_POL_Q3_black", "SHAM_POL_Q3_blur10", "SHAM_INS_black", "SHAM_INS_blur10",
    "SHAM_DIS_black", "SHAM_DIS_blur10",
    # v7_mimic (2026-10-11): sufficiency with blur/region mean color (S_blur10, S_regmean) and the MIMIC occluder test
    "S_blur10", "S_regmean", "SHAM_black", "SHAM_blur10",
    # item 21 (22/10/2026): M3AE with a constant BLACK image -- text-only trained with black and tested with black; any model tested with black
    "TXT_PRETO", "C1_PRETO",
)


class ResultsSchemaError(ValueError):
    pass


def validate_results_dict(d: dict) -> None:
    """Raises ResultsSchemaError if `d` does not follow the schema. Returns nothing on success."""
    missing = [k for k in REQUIRED_KEYS if k not in d]
    if missing:
        raise ResultsSchemaError(f"Campos obrigatórios ausentes: {missing}")

    if d["condition"] not in VALID_CONDITIONS:
        raise ResultsSchemaError(
            f"condition={d['condition']!r} inválida, deve ser uma de {VALID_CONDITIONS}"
        )

    if not isinstance(d["accuracy"], (int, float)) or not (0.0 <= float(d["accuracy"]) <= 1.0):
        raise ResultsSchemaError(f"accuracy={d['accuracy']!r} deve ser um número entre 0 e 1")

    has_n = "n" in d
    has_n_correct = "n_correct" in d
    if has_n != has_n_correct:
        raise ResultsSchemaError("'n' e 'n_correct' devem estar ambos presentes ou ambos ausentes")
    if has_n and (not isinstance(d["n"], int) or d["n"] <= 0):
        raise ResultsSchemaError(f"n={d['n']!r} deve ser um inteiro positivo")
    if has_n_correct and (not isinstance(d["n_correct"], int) or not (0 <= d["n_correct"] <= d["n"])):
        raise ResultsSchemaError(f"n_correct={d['n_correct']!r} deve estar entre 0 e n")

    if "predictions" in d:
        preds = d["predictions"]
        if not isinstance(preds, list) or not preds:
            raise ResultsSchemaError("'predictions', se presente, deve ser uma lista não vazia")
        for i, p in enumerate(preds):
            for key in ("qid", "predicted", "gold", "correct"):
                if key not in p:
                    raise ResultsSchemaError(f"predictions[{i}] sem o campo '{key}'")
            if not isinstance(p["correct"], bool):
                raise ResultsSchemaError(f"predictions[{i}]['correct'] deve ser bool")


def has_paired_data(d: dict) -> bool:
    return "predictions" in d and len(d["predictions"]) > 0
