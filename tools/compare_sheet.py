"""Compare two numbers sheets: every line must be identical except the header line that records the generation time and the
output root in the file citations (the regenerated sheet cites reproduce_out/, the published one results/).
Usage: compare_sheet.py <published> <regenerated>"""
import re, sys
def norm(p): return [re.sub(r"^Gerada \S+ \S+ por", "Gerada <time> por", l).replace("<sub>reproduce_out/", "<sub>results/").replace(" ; reproduce_out/", " ; results/") for l in open(p).read().splitlines()]
a, b = norm(sys.argv[1]), norm(sys.argv[2])
na, nb = [l for l in a if l.startswith("- **")], [l for l in b if l.startswith("- **")]
print(f"  numeric lines: {len(na)} published, {len(nb)} regenerated; identical: {na == nb}; all lines identical (except the time stamp): {a == b}")
if a != b:
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y: print(f"  first difference at line {i + 1}:\n    published:   {x[:200]}\n    regenerated: {y[:200]}"); break
    if len(a) != len(b): print(f"  line counts differ: {len(a)} vs {len(b)}")
    sys.exit(1)
