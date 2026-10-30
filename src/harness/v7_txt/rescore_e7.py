"""E7 (normalization of closed-ended answers): on CLOSED-ENDED questions, "negative" counts as "no" and
"positive" as "yes"; zero-shot only. Applies to the JSONs already written: keeps predicted_raw/correct_raw, rewrites
predicted/correct and records the counts in provenance.e7. Closed-ended = normalized gold in {yes, no}."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import argparse, json, sys
sys.path.insert(0, os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/worktree")
from med_vlm.metrics.process_text import answer_matches, normalize_text
MAP = {"negative": "no", "positive": "yes"}
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("files", nargs="+"); a = ap.parse_args()
    for f in a.files:
        d = json.load(open(f))
        if d.get("provenance", {}).get("e7", {}).get("applied"): print(f, "ja aplicado"); continue
        n_changed = n_flip_correct = n_closed = n_no_token = 0
        import re; YN = re.compile(r"\b(yes|no)\b")
        for p in d["predictions"]:
            g = normalize_text(str(p["gold"])); closed = g in ("yes", "no"); n_closed += closed
            if closed and not YN.search(normalize_text(str(p.get("predicted_raw", p["predicted"])))) and normalize_text(str(p.get("predicted_raw", p["predicted"]))) not in MAP: n_no_token += 1
            p.setdefault("predicted_raw", p["predicted"]); p.setdefault("correct_raw", p["correct"])
            if closed and normalize_text(str(p["predicted"])) in MAP:
                p["predicted"] = MAP[normalize_text(str(p["predicted"]))]; p["correct"] = bool(answer_matches(normalize_text(p["predicted"]), [g])); n_changed += 1; n_flip_correct += int(p["correct"] != p["correct_raw"])
        d["n_correct"] = sum(p["correct"] for p in d["predictions"]); d["accuracy"] = d["n_correct"] / max(d["n"], 1)
        d.setdefault("provenance", {})["e7"] = {"applied": True, "rule": "fechadas (gold yes/no): negative->no, positive->yes; demais itens intocados", "n_closed": n_closed, "n_closed_sem_token_sim_nao": n_no_token, "frac_closed_sem_token_sim_nao": (n_no_token / n_closed) if n_closed else None, "n_predictions_mapped": n_changed, "n_correct_flag_changed": n_flip_correct, "accuracy_before": sum(p["correct_raw"] for p in d["predictions"]) / max(d["n"], 1), "accuracy_after": d["accuracy"]}
        json.dump(d, open(f, "w"), indent=1); print(f, d["provenance"]["e7"])
if __name__ == "__main__": main()
