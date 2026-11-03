"""14/10/2026: identity proof -- compares the JSON and MD files from before (a snapshot taken before the change) and after (v7_txt/analysis, docs).
JSON: recursive diff by key; cells that involve the HEAL/MIMIC gray image (keys c1 / txt_menos_c1 / C1_frozen / files.c1 /
sha256.c1 / definitions) and the provenance stamp t are expected; any other difference is listed. MD: line-by-line diff with the
C1 columns masked (txt_floors: 6th column 'Acc C1'; decomposicao: columns 'C1' and 'TXT - C1'); only the 'Gerado' line may change."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json, re, sys, difflib, collections
from pathlib import Path
A = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/tmp/v7/snapshot_before_20261014"); V = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt")
EXPECTED_KEYS = {"c1", "txt_menos_c1", "C1_frozen", "t", "definitions"}
def walk(a, b, path, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k in EXPECTED_KEYS: out["expected"][path + "/" + k] += 1; continue
            if k not in a: out["added"].append(path + "/" + k); continue
            if k not in b: out["removed"].append(path + "/" + k); continue
            walk(a[k], b[k], path + "/" + k, out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): out["other"].append((path, f"len {len(a)} -> {len(b)}")); return
        for i, (x, y) in enumerate(zip(a, b)): walk(x, y, f"{path}[{i}]", out)
    else:
        if a != b and not (isinstance(a, float) and isinstance(b, float) and abs(a - b) < 1e-12): out["other"].append((path, f"{str(a)[:60]} -> {str(b)[:60]}"))
rep = {}
for name in ("txt_floors", "decomposicao", "own_floor_ceilings"):
    a = json.load(open(A / f"analysis/{name}.json")); b = json.load(open(V / f"analysis/{name}.json"))
    out = {"expected": collections.Counter(), "added": [], "removed": [], "other": []}; walk(a, b, "", out)
    # groups 'expected' by key type and by benchmark
    exp = collections.Counter()
    for k, n in out["expected"].items():
        m = re.search(r"benchmarks/([A-Z]+)", k); exp[(m.group(1) if m else "-", k.rsplit("/", 1)[-1])] += n
    rep[name] = {"expected_by_bench_key": {f"{b_}:{k}": n for (b_, k), n in sorted(exp.items())}, "added": out["added"][:30], "n_added": len(out["added"]), "removed": out["removed"][:30], "n_removed": len(out["removed"]), "other": out["other"][:40], "n_other": len(out["other"])}
    print(f"== {name}.json: esperadas {sum(exp.values())} | adicionadas {len(out['added'])} | removidas {len(out['removed'])} | OUTRAS {len(out['other'])}")
    for k, n in rep[name]["expected_by_bench_key"].items(): print("   esperada", k, n)
    for x in out["added"][:12]: print("   adicionada", x)
    for x in out["removed"][:12]: print("   removida", x)
    for x in out["other"][:25]: print("   OUTRA", x)
# ---- MD
def mask(line, name):
    if line.startswith("Gerado ") or line.startswith("Gerada "): return "Gerado <t>"
    if name == "txt_floors" and line.startswith("- ") and "(n=" in line: return re.sub(r"C1_frozen [0-9.]+ \([0-9.]+\); ", "", line)   # summary per family: new C1_frozen field
    if not line.startswith("|"): return line
    cells = line.split("|")
    if name == "decomposicao" and cells[1].strip().startswith(("linha", "familia")): return "<cabecalho de tabela (texto da nota de metodo, mudanca pedida)>"
    try:
        if name == "txt_floors" and len(cells) == 12 and cells[1].strip() not in ("linha", "---"):
            if "=" in cells[2]: cells[7] = " <C1> "           # per class: | run | class | n | TXT | C0f | C0a | C1 | M0 | ...
            else: cells[6] = " <C1> "                         # main: | run | n | TXT | C0f | C0a | C1 | M0 | ...
        if name == "decomposicao":
            if len(cells) == 14: cells[11] = " <C1> "; cells[12] = " <TXT-C1> "   # per run
            elif len(cells) == 13 and cells[2].strip() not in ("---",): cells[10] = " <C1> "; cells[11] = " <TXT-C1> "   # mean per family
    except Exception: pass
    return "|".join(cells)
for name in ("txt_floors", "decomposicao", "own_floor_ceilings", "numbers_own_floor"):
    a = open(A / f"docs/{name}.md").read().splitlines(); b = open(V / f"docs/{name}.md").read().splitlines()
    if name == "decomposicao":   # the line '- fam | classe | ... / C1 ;' and the header/note changed their text by authors' decision: masks the C1 field in the per-class lines
        a = [re.sub(r" / [0-9.\-]+ ;", " / <C1> ;", x) for x in a]; b = [re.sub(r" / [0-9.\-]+ ;", " / <C1> ;", x) for x in b]
    ma = [mask(x, name) for x in a]; mb = [mask(x, name) for x in b]
    d = [x for x in difflib.unified_diff(ma, mb, lineterm="", n=0) if x.startswith(("+", "-")) and not x.startswith(("+++", "---"))]
    rep[name + ".md"] = {"n_diff_lines_after_mask": len(d), "sample": d[:16]}
    print(f"== {name}.md: linhas diferentes apos mascarar C1 e carimbo: {len(d)}")
    for x in d[:12]: print("   ", x[:220])
json.dump(rep, open(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic/analysis/c1_identity_check.json", "w"), indent=1, ensure_ascii=False)
