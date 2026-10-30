"""v7_mimic/scripts/00b_schema_md.py -- generates docs/schema.md from analysis/schema_stats.json (+ MIMIC tables if present)."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import gzip, json, hashlib
from pathlib import Path
import pandas as pd
V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic"); RAW_M = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/data/raw/mimic-cxr-jpg/2.1.0")
r = json.load(open(V7 / "analysis/schema_stats.json")); p = r["pair_questions"]; m = r["mimic_all"]
L = ["# Esquema real das tabelas (Medical-Diff-VQA 1.0.1 e MIMIC-CXR-JPG 2.1.0)", "",
     f"Gerado em {r['provenance']['date']} ({r['provenance']['host']}) por `scripts/00_schema_stats.py` + `scripts/00b_schema_md.py`; números completos em `analysis/schema_stats.json`.",
     "Fonte: `doutorado/data/raw/medical-diff-vqa/1.0.1/` (sha256 conferidos contra SHA256SUMS.txt: 5/5 OK para os arquivos de dados; `libs/` conferida à parte, ver relatório final).", "",
     "## O que o README.md (934 bytes) e a página do projeto dizem",
     "- README.md do pacote: só descreve os três arquivos (`mimic_pair_questions.csv` = pares pergunta-resposta finais; `mimic_all.csv` = metadados do MIMIC-CXR e rótulos do MIMIC-CXR-JPG, \"só para referência\"; `all_diseases.json` = KeyInfo intermediário por estudo) e a pasta `libs/` (7 CSV para extração de palavras-chave). **Não menciona** ref_id/study_id nem a coluna split.",
     "- Página pública do projeto (physionet.org/content/medical-diff-vqa/1.0.1/, cópia em `tmp/v7_mimic/diffvqa_project_page.html`), seção *Release Notes*: \"Version 1.0.1: In mimic_pair_questions.csv, some study_id and ref_id are switched to ensure the reference study id precedes the main study id for 'difference' questions. The answers for the affected entries are updated accordingly.\" A correção afeta só as perguntas `difference` (excluídas aqui).",
     "- Mesma página, colunas: `study_id` = estudo principal; `ref_id` = estudo de referência; `split` (pair_questions) = train/val/test do Diff-VQA; em `mimic_all.csv`, `split` = \"train/val/test split used in MIMIC-CXR-JPG. It is only for reference purposes\" e `view` = \"PA or AP view of the image\" (na prática há também lateral, Erect etc., ver abaixo).", "",
     "## mimic_pair_questions.csv",
     f"Colunas e tipos (pandas): {p['columns']}. Linhas: {p['n_rows']}; estudos distintos: {p['n_studies']}; pacientes: {p['n_subjects']}; linhas com ref_id == study_id: {p['ref_eq_study']}.", "",
     "### Contagens por question_type × split (coluna split do Diff-VQA)", "| question_type | train | val | test | total |", "|---|---:|---:|---:|---:|"]
for t, d in sorted(p["by_type_split"].items()):
    L.append(f"| {t} | {d.get('train',0)} | {d.get('val',0)} | {d.get('test',0)} | {p['by_type'][t]} |")
L += ["", "### Três linhas de exemplo por question_type (study_id, subject_id, ref_id, question → answer, split)"]
for t, ex in sorted(p["examples"].items()):
    L.append(f"- **{t}**")
    for e in ex:
        L.append(f"  - {e[0]}, {e[1]}, {e[2]}, \"{e[3]}\" → \"{e[4][:120]}\" ({e[5]})")
L += ["", "### Vocabulário de respostas por tipo", "| tipo | respostas distintas | fração yes/no | palavras (mediana / máx) | perguntas distintas |", "|---|---:|---:|---|---:|"]
for t, a in sorted(p["answers"].items()):
    L.append(f"| {t} | {a['n_distinct']} | {a['yes_no_frac']:.3f} | {a['n_words_answer_median']:.0f} / {a['n_words_answer_max']} | {p['questions_distinct'][t]['n_distinct']} |")
for t, a in sorted(p["answers"].items()):
    L += ["", f"**{t} — top-30 respostas**: " + ", ".join(f"{k} ({v})" for k, v in a["top30"].items())]
    L += [f"**{t} — perguntas mais frequentes**: " + "; ".join(f"\"{k}\" ({v})" for k, v in list(p["questions_distinct"][t]["top15"].items())[:6])]
L += ["", "### Menções a comparação fora de `difference`", " ".join(f"{t}: {d['n']};" for t, d in sorted(p["comparison_words_non_difference"].items())) + " (regex compar|previous|prior|reference|change|earlier|interval|since).", "",
      "## mimic_all.csv", f"Colunas: {list(m['columns'])}. Linhas: {m['n_rows']} = estudos distintos {m['n_studies']} = dicom distintos {m['n_dicom']} (uma imagem por estudo). Pacientes: {m['n_subjects']}.",
      f"- `view`: {m['view']}", "- `split` (MIMIC-CXR-JPG, referência): " + str(m["split"]) + f"; pacientes em dois splits: {m['subject_in_two_splits']}.",
      f"- Junção perguntas × mimic_all por study_id: {r['join']['questions_without_mimic_all_row']} perguntas sem linha; concordância entre `split` do Diff-VQA e `split` do mimic_all: {100*r['join']['split_agree_frac']:.1f} % das perguntas (são divisões diferentes).",
      "- Exemplos: " + "; ".join(str(e) for e in m["examples"]), "",
      "## all_diseases.json", f"Lista de 227 835 registros (study_id, subject_id, entity{{nome → location/type/level/post_location (+ *2)}}, no_entity). Entidades distintas: {r['all_diseases']['n_entities_distinct']} (lista em `analysis/entities.json`). Top: " + ", ".join(f"{k} ({v})" for k, v in list(r["all_diseases"]["entities_top40"].items())[:15]) + ".", ""]
# MIMIC-CXR-JPG tables, if present
L += ["## MIMIC-CXR-JPG 2.1.0 (tabelas em `doutorado/data/raw/mimic-cxr-jpg/2.1.0/`)"]
for name in ("mimic-cxr-2.0.0-split.csv.gz", "mimic-cxr-2.0.0-metadata.csv.gz", "mimic-cxr-2.0.0-chexpert.csv.gz"):
    f = RAW_M / name
    if not f.is_file():
        L.append(f"- {name}: ainda não baixado"); continue
    try:
        df = pd.read_csv(f, dtype=str, keep_default_na=False)
    except Exception as e:
        L.append(f"- {name}: download incompleto ({type(e).__name__})"); continue
    L.append(f"- **{name}** ({f.stat().st_size} bytes): {len(df)} linhas; colunas {list(df.columns)}.")
    if "split" in df.columns:
        L.append(f"  - split (por imagem): {df.split.value_counts().to_dict()}; por estudo: {df.drop_duplicates('study_id').split.value_counts().to_dict()}; por paciente: {df.drop_duplicates('subject_id').split.value_counts().to_dict()}; pacientes em >1 split: {int((df.groupby('subject_id').split.nunique() > 1).sum())}.")
    if "ViewPosition" in df.columns:
        L.append(f"  - ViewPosition: {df.ViewPosition.replace('', 'NA').value_counts().to_dict()}")
    L.append("  - exemplo: " + str(df.head(2).values.tolist())[:400])
f = RAW_M / "IMAGE_FILENAMES"
if f.is_file():
    n = sum(1 for _ in open(f)); L.append(f"- **IMAGE_FILENAMES** ({f.stat().st_size} bytes): {n} linhas; primeira: `{open(f).readline().strip()}`")
else:
    L.append("- IMAGE_FILENAMES: ainda não baixado")
(V7 / "docs/schema.md").write_text("\n".join(L) + "\n"); print("schema.md", len(L), "linhas")
