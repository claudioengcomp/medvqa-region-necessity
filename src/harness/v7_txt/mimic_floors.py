"""Question-only floors of Medical-Diff-VQA used by the analysis (per-item correctness of the question-only classifier on the closed-ended
questions and of the per-template majority answer on the open-ended ones). Inputs are read from the lab layout under LAB_ROOT (credentialed data)."""
import json, os
MIMIC = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic"
def mimic_items():
    import pandas as pd
    d = pd.read_parquet(f"{MIMIC}/data/items_test.parquet"); return {int(r.qid): r for r in d.itertuples()}
def mimic_floors():
    """M0 subset/full and per-template prior subset/full per item (dicts qid -> correct), gold from items_test.parquet."""
    from med_vlm.metrics.process_text import answer_matches, normalize_text
    it = mimic_items(); out = {}
    for tag in ("subset", "full"):
        d = json.load(open(f"{MIMIC}/results/M0_question_only_MIMIC_{tag}.json"))
        m0 = {int(q): bool(answer_matches(normalize_text(str(p)), [normalize_text(str(it[int(q)].answer))])) for q, p in d["predictions"].items()}
        pr = {int(q): bool(answer_matches(normalize_text(str(p)), [normalize_text(str(it[int(q)].answer))])) for q, p in d["prior_predictions"].items()}
        # question-only classifier only on the closed-ended questions; per-template majority answer on the open-ended ones
        out["M0_" + tag + "_fechadas"] = {q: v for q, v in m0.items() if it[q].answer_type == "closed"}
        out["prior_" + tag + "_abertas"] = {q: v for q, v in pr.items() if it[q].answer_type == "open"}
        out["piso_" + tag] = {**out["M0_" + tag + "_fechadas"], **out["prior_" + tag + "_abertas"]}
    return out
