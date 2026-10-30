"""v7_mimic/scripts/10b_imagenome_files_md.py -- docs/imagenome_files.md from the aws s3 ls listings."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
L = ["# Chest ImaGenome v1.0.0 — árvore no access point S3 (aws s3 ls --recursive, 2026-10-11)", "",
     "Access point `s3://arn:aws:s3:us-east-1:724665945834:accesspoint/chest-imagenome-v1-0-0-01/chest-imagenome/1.0.0/`. Listagens brutas em `logs/imagenome_ls_<pasta>.txt`.", ""]
tot = 0
for d in ["silver_dataset", "gold_dataset", "semantics", "utils", "analysis"]:
    rows = [l.split() for l in open(f"{os.environ.get('LAB_ROOT', 'LAB_ROOT')}/v7_mimic/logs/imagenome_ls_{d}.txt") if l.strip()]
    s = sum(int(r[2]) for r in rows); tot += s
    L += [f"## {d} — {len(rows)} objetos, {s/1048576:.1f} MB", "", "| MB | arquivo |", "|---:|---|"]
    for r in sorted(rows, key=lambda r: -int(r[2])):
        L.append(f"| {int(r[2])/1048576:.2f} | `{r[3].replace('chest-imagenome/1.0.0/', '')}` |")
    L.append("")
L += [f"Total do registro: {tot/1048576:.0f} MB (+ LICENSE.txt 2,5 KB, SHA256SUMS.txt 7 KB).", "",
      "## Baixado (scripts/10_download_imagenome.sh)",
      "LICENSE.txt, SHA256SUMS.txt, `semantics/` inteira, `gold_dataset/` inteira, `utils/` inteira, `analysis/` inteira (2 MB, estatísticas objeto–atributo), e de `silver_dataset/` só `scene_graph.zip` (972 MB, um JSON por imagem com caixas + atributos por região) e `splits/*.csv` (34 MB). **Não** baixados: `study_level_attribute_rdfgraphs.json` (4,4 GB, grafos RDF por estudo, redundante com os scene graphs para o nosso uso) e `cxr-mimic-v2.0.0-processed-sentences_all.txt` (235 MB, sentenças dos laudos). sha256 conferidos no fim de `logs/download_imagenome.log`.", ""]
open(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic/docs/imagenome_files.md", "w").write("\n".join(L)); print("imagenome_files.md ok", len(L))
