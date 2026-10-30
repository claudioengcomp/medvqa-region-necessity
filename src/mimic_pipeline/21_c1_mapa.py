"""executor 2, 14/10/2026: v7_txt/docs/c1_mapa.md -- where each generator defines c1 (gray image), per benchmark and run; existence and short sha256
of the 27 *_C1.json files of HEAL (v7_txt/results) and MIMIC (v7_mimic/results)."""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import hashlib, os, sys, time, json
sys.path.insert(0, os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/worktree")
from harness.v7_txt.txt_floors import cells
V7 = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt"; MIMIC = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic"
def sh(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()[:12] if p and os.path.exists(p) else "—"
L = ["# Mapa das entradas C1 (imagem cinza) nos geradores — exec2, " + time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()), "",
     "Fontes: `harness/v7_txt/txt_floors.py::cells()` define `c1` por (base, familia, semente) e e importado por `decomposicao.py` (linha 31: `C1 = preds(c['c1']) if c['c1'] and os.path.exists(c['c1'])`); `own_floor_ceilings.py` **nao usa C1** (so C0, T, P, TXT, M0). Convencao: C1 = imagem cinza da **linha congelada** da familia (Kvasir/SLAKE/VQA-RAD: p0/v5; HEAL: `v7_txt/results`; MIMIC: `v7_mimic/results`, desde 14/10). Patch: `v7_txt/patches/c1_mimic_heal_20261014.patch`.", "",
     "## Caminhos definidos em `cells()` (apos o patch)", "", "| base | linha TXT | caminho esperado de c1 | existe | sha256 curto |", "|---|---|---|---|---|"]
for bench in ("HEAL", "MIMIC", "KVASIR", "SLAKE", "VQARAD"):
    for fam in ("QWEN2VL", "SMOLVLM", "M3AE"):
        for s in range(3):
            c = cells(bench, fam, s)
            if c is None: continue
            p = c["c1"]; L.append(f"| {bench} | {fam}_{'LORA_' if fam != 'M3AE' else ''}TXT_{bench}_seed{s} | `{p}` | {'sim' if p and os.path.exists(p) else 'NAO'} | {sh(p)} |")
# the 27 runs of each benchmark (all runs with C1 executed)
def lines27(bench, root):
    out = [f"M3AE_{bench}_seed{s}" for s in range(3)]
    for F in ("QWEN2VL", "SMOLVLM"):
        for pe in ("LORA", "DORA"):
            for s in range(3):
                n = f"{F}_{pe}_{bench}_seed{s}"
                if bench == "MIMIC" and F == "QWEN2VL" and pe == "LORA": n = f"QWEN2VL_LORA_FROZEN_MIMIC_seed{s}"
                if bench == "HEAL" and F == "QWEN2VL" and pe == "DORA" and s == 2: n = "QWEN2VL_DORA_HEAL_seed2_retrain20261003"
                out.append(n)
    for F, tag in (("QWEN2VL", "VT"), ("SMOLVLM", "FT")):
        for pe in ("LORA", "DORA"):
            for s in range(3): out.append(f"{F}_{pe}_{tag}_{bench}_seed{s}")
    return [(n, f"{root}/{n}_C1.json") for n in out]
consumed = {c["c1"] for b in ("HEAL", "MIMIC") for f in ("QWEN2VL", "SMOLVLM", "M3AE") for s in range(3) for c in [cells(b, f, s)] if c}
missing = []
for bench, root in (("HEAL", f"{V7}/results"), ("MIMIC", f"{MIMIC}/results")):
    L += ["", f"## {bench}: as 27 linhas com C1 em `{root}`", "", "| linha | arquivo | existe | sha256 curto | modificado | consumido por |", "|---|---|---|---|---|---|"]
    for n, p in lines27(bench, root):
        ex = os.path.exists(p); missing += [] if ex else [p]
        who = "txt_floors + decomposicao (coluna C1 da linha congelada)" if p in consumed else "nenhum gerador (linha DoRA ou adaptada: sem coluna C1)"
        L.append(f"| {n} | `{os.path.basename(p)}` | {'sim' if ex else 'NAO'} | {sh(p)} | {time.strftime('%Y-%m-%d %H:%M', time.gmtime(os.path.getmtime(p))) if ex else '—'} | {who} |")
L += ["", f"Arquivos ausentes: {len(missing)}" + ("" if not missing else " — " + ", ".join(missing)), "",
      "Observacoes: (1) os geradores consomem 9 dos 27 C1 de cada base (a linha congelada de cada familia × semente: HEAL QWEN2VL_LORA, SMOLVLM_LORA_FT, M3AE; MIMIC QWEN2VL_LORA_FROZEN, SMOLVLM_LORA_FT, M3AE); os 18 restantes (DoRA, adaptadas VT/FT, inclusive `QWEN2VL_DORA_HEAL_seed2_retrain20261003_C1.json`) existem, mas nenhuma coluna dos geradores os le. (2) `txt_floors.py` so itera a familia QWEN2VL no MIMIC (linha `for fam in (('QWEN2VL',) if bench == 'MIMIC' ...)`), entao sua tabela do MIMIC tem C1 so para o Qwen; `decomposicao.py` itera as tres familias. Nada disso foi alterado (fora do escopo)."]
open(f"{V7}/docs/c1_mapa.md", "w").write("\n".join(L) + "\n"); print("c1_mapa.md ok; ausentes:", len(missing))
