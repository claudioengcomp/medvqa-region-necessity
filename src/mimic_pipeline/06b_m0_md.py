"""v7_mimic/scripts/06b_m0_md.py -- renders docs/m0_mimic.md from the two M0 JSON files."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json
from pathlib import Path
V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic")
R = {t: json.load(open(V7 / f"results/M0_question_only_MIMIC_{t}.json")) for t in ("subset", "full")}
tmpl = json.load(open(V7 / "analysis/subset_report.json"))["template_ids"]
def cell(d):
    return f"{d['accuracy']:.3f} [{d['ci95_low']:.3f}, {d['ci95_high']:.3f}]" if d.get("accuracy") is not None else "—"
s, f = R["subset"], R["full"]
L = ["# M0 só-pergunta (TF-IDF + LR) no subconjunto MIMIC/Diff-VQA de imagem única", "",
     f"Gerado em {f['provenance']['date']} ({f['provenance']['host']}) por `scripts/06_m0_mimic.py` (mesmas três decisões do M0 do HEAL/Kvasir: TF-IDF 1–2-gramas, LR C=1, sem imagem). "
     f"Teste: {s['n_test']} perguntas em {s['n_test_images']} imagens (`data/items_test.parquet`). IC 95 % por bootstrap por imagem (B = {f['provenance']['B']}, semente {f['provenance']['seed_bootstrap']}).",
     "Treinos: **subset** = fechadas do `items_train.parquet` (n = {}; prior no {:.1f} %); **full** = todas as fechadas de imagem única do split train do MIMIC-CXR-JPG após os mesmos filtros (`data/pool_train_eligible.parquet`, n = {}; prior no {:.1f} %).".format(
         s["train_rows_closed"], 100 * s["train_prior_closed"]["no"], f["train_rows_closed"], 100 * f["train_prior_closed"]["no"]),
     "A LR só responde yes/no, então nas abertas o M0 nunca acerta; para elas o piso reportado é a **resposta majoritária por template no treino** (coluna *prior*). Números em `results/M0_question_only_MIMIC_{subset,full}.json`.", "",
     "## Global", "| conjunto | n | M0 subset | M0 full | prior-majoritário subset | prior-majoritário full |", "|---|---:|---|---|---|---|",
     f"| fechadas | {s['overall_closed']['n']} | {cell(s['overall_closed'])} | {cell(f['overall_closed'])} | {cell(s['by_answer_type']['closed']['prior_majority'])} | {cell(f['by_answer_type']['closed']['prior_majority'])} |",
     f"| abertas | {s['by_answer_type']['open']['m0']['n']} | {cell(s['by_answer_type']['open']['m0'])} | {cell(f['by_answer_type']['open']['m0'])} | {cell(s['by_answer_type']['open']['prior_majority'])} | {cell(f['by_answer_type']['open']['prior_majority'])} |",
     f"| todas | {s['overall_all_m0']['n']} | {cell(s['overall_all_m0'])} | {cell(f['overall_all_m0'])} | {cell(s['overall_all_prior'])} | {cell(f['overall_all_prior'])} |", "",
     "## Por question_type", "| tipo | n | imagens | M0 subset | M0 full | prior subset | prior full |", "|---|---:|---:|---|---|---|---|"]
for k, v in s["by_question_type"].items():
    w = f["by_question_type"][k]
    L.append(f"| {k} | {v['m0']['n']} | {v['n_images']} | {cell(v['m0'])} | {cell(w['m0'])} | {cell(v['prior_majority'])} | {cell(w['prior_majority'])} |")
L += ["", "## Por template", "| template | texto | n | imagens | M0 subset | M0 full | prior subset | prior full |", "|---|---|---:|---:|---|---|---|---|"]
for k, v in sorted(s["by_template"].items()):
    w = f["by_template"][k]
    L.append(f"| {k} | `{tmpl.get(k, '')}` | {v['m0']['n']} | {v['n_images']} | {cell(v['m0'])} | {cell(w['m0'])} | {cell(v['prior_majority'])} | {cell(w['prior_majority'])} |")

(V7 / "docs/m0_mimic.md").write_text("\n".join(L) + "\n"); print("\n".join(L))
