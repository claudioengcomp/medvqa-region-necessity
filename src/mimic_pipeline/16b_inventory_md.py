"""v7_mimic/scripts/16b_inventory_md.py -- docs/inventory_mimic.md from the inventory."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json
V = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic"
d = json.load(open(f"{V}/results/inventory_mimic_test.json")); s = d["summary"]
fq = ", ".join(f"{k}: {v:.3f}" for k, v in s["target_area_frac_quantiles"].items())
fc = ", ".join(f"{k}: {v:.3f}" for k, v in s["target_area_frac_by_class_median"].items())
L = ["# Inventário do Placebo — teste MIMIC/Diff-VQA (Parada 2)", "",
     f"`results/inventory_mimic_test.json` (esquema do `inventory_heal_test.json`), gerado por `scripts/16_inventory_mimic.py` em {d['provenance']['date']}. Regiões = caixas do ImaGenome silver escaladas ao PNG 1024 (recorte ao quadro). Regras de concordância entre fontes do candidato (11/10). Detalhamento em `analysis/inventory_breakdown.txt`.", "",
     f"- Perguntas {s['n_questions']}; avaliáveis {s['n_evaluable']}; unidades {s['n_units']}.",
     f"- Por classe (todas): {s['by_class']}",
     f"- Avaliáveis por classe, com aproximadas: {s['evaluable_by_class_with_approx']}; só exatas: {s['evaluable_by_class_exact_only']}.",
     f"- Avaliáveis por template: {s['evaluable_by_template']}",
     f"- Avaliáveis por entidade: {s['evaluable_by_entity']}",
     f"- Motivos de exclusão: {s['exclusion_reasons']}",
     f"- Por classe × motivo: {s['exclusion_by_class']}",
     f"- Removidos por regra × entidade: {s['removed_by_rule_by_entity']}",
     f"- Método de placebo (avaliáveis): {s['placebo_methods']}",
     f"- target_area_frac (fração do quadro), avaliáveis: {fq}; mediana por classe: {fc}.",
     f"- Atlas torácico MIMIC (FOV do posicionador): caixas de 13 regiões torácicas das 718 imagens de validação, N 256, min_freq 0,02; cobre {s['thorax_atlas']['atlas_area_frac']:.3f} do quadro.",
     "- Referência (não critério): HEAL 711 fechadas-sim avaliáveis em 1 446.", ""]
open(f"{V}/docs/inventory_mimic.md", "w").write("\n".join(L) + "\n"); print("ok")
