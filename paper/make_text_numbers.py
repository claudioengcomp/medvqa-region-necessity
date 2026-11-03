"""List of the numbers cited by the text of the paper, with the lines of the numbers sheet that support them.
The LaTeX source of the paper is not distributed before acceptance; this script reads it from a local path and writes paper/text_numbers.md,
which lists every distinct number of the text body (tables excluded, integers 0-100 and years ignored, grant numbers and exponents excluded as
'no source expected') and, for each, up to three labels of the sheet whose value contains that number. reproduce.sh checks the list against
the regenerated sheet with `--check`. Usage: python paper/make_text_numbers.py <main.tex> --sheet results/numbers_artigo1.md [--out paper/text_numbers.md]
       python paper/make_text_numbers.py --check paper/text_numbers.md --sheet reproduce_out/docs/numbers_artigo1.md"""
import argparse, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import verify_numbers as V
def check(md, sheet):
    """--check: every number of the list (first column) that is not marked '(no source expected)' must be in the sheet; exit 1 otherwise."""
    src = V.junta(V.MILHAR_FOLHA, pathlib.Path(sheet).read_text()).replace(',', '.'); srcnums = {m.group(0).lstrip('+-\u2212') for m in re.finditer(r'[+\-\u2212]?\d+(?:\.\d+)?', src)}
    rows = [l for l in pathlib.Path(md).read_text().splitlines() if l.startswith("| ") and not l.startswith("| number")]
    missing = [l.split("|")[1].strip() for l in rows if "(no source expected)" not in l and not (V.forms(l.split("|")[1].strip()) & srcnums)]
    print(f"{len(rows)} numbers in {md}; {len(missing)} without a source in the sheet" + (": " + ", ".join(missing) if missing else ""))
    sys.exit(1 if missing else 0)
def main():
    if "--check" in sys.argv:
        ap = argparse.ArgumentParser(); ap.add_argument("--check"); ap.add_argument("--sheet", required=True); a = ap.parse_args(); return check(a.check, a.sheet)
    ap = argparse.ArgumentParser(); ap.add_argument("tex"); ap.add_argument("--sheet", required=True); ap.add_argument("--out", default="paper/text_numbers.md"); ap.add_argument("--version", default=""); a = ap.parse_args()
    t = pathlib.Path(a.tex).read_text(); t = re.sub(r'(?m)(?<!\\)%.*$', '', t)
    body = t[t.index('\\begin{document}'):] if '\\begin{document}' in t else t
    body = re.sub(r'\\input\{[^}]*\}', '', body)                                  # tables are checked separately
    body = re.sub(r'\\mbox\{([^}]*)\}', r'\1', body)
    body = re.sub(r'\\(cite|ref|label|url|includegraphics|eqref|autoref|cref|multicolumn|multirow)(\[[^\]]*\])?\{[^}]*\}', '', body)
    body = re.sub(r'\\(setcounter|addtocounter)\{[^}]*\}\{[^}]*\}', '', body)
    body = V.junta(V.MILHAR_TEX, body)
    sheet = pathlib.Path(a.sheet).read_text(); rows = re.findall(r"^- \*\*(.+?)\*\* — `(.*)`  $", sheet, re.M)
    src = V.junta(V.MILHAR_FOLHA, sheet).replace(',', '.'); srcnums = {m.group(0).lstrip('+-\u2212') for m in re.finditer(r'[+\-\u2212]?\d+(?:\.\d+)?', src)}
    num_re = re.compile(r'(?<![\w.])[+\-\u2212]?\d[\d{},]*(?:\.\d+)?(?:\s*\\times\s*10\^\{?-?\d+\}?|e-?\d+)?')
    trivial = {str(i) for i in range(0, 101)} | {str(y) for y in range(1900, 2031)}
    NOSRC = re.compile(r"\d{4}/\d{5}-\d|\d{6}/\d{4}-\d|10\^|e-\d")   # grant numbers and exponents: no source expected
    seen = []
    for m in num_re.finditer(body):
        raw = m.group(0); v = V.norm(raw).replace(',', '.').replace('\u2212', '-').lstrip('+-').rstrip('.').strip('{}'); v = re.sub(r'\s*\\times\s*10\^\{?(-?\d+)\}?', lambda mm: 'e' + mm.group(1), v)
        if not re.search(r'\d', v) or v in trivial or any(v == s for s, _ in seen): continue
        ctx = body[max(0, m.start() - 12):m.end() + 12]; seen.append((v, bool(NOSRC.search(ctx))))
    def labels(v):
        fs = V.forms(v); out = []
        for lbl, val in rows:
            vals = {x.lstrip('+-\u2212') for x in re.findall(r'[+\-\u2212]?\d+(?:\.\d+)?', V.junta(V.MILHAR_FOLHA, val).replace(',', '.'))}
            if fs & vals: out.append(lbl)
            if len(out) == 3: break
        return out
    L = [f"# Numbers cited by the text of the paper{(' (' + a.version + ')') if a.version else ''}", "",
         "One line per distinct number of the text body (tables excluded; integers 0-100 and years ignored). The second column lists up to three labels of",
         "`results/numbers_artigo1.md` whose value contains the number; `make_text_numbers.py --check` verifies this file against the regenerated sheet in `reproduce.sh`.",
         "Grant numbers and the bootstrap exponent have no source in the sheet and are listed with `(no source expected)`.", "", "| number | sheet label(s) |", "|---|---|"]
    ok = 0; nosrc = 0
    for v, ns in seen:
        lb = labels(v)
        if lb: ok += 1; L.append(f"| {v} | {'; '.join('`' + x.replace('|', '/') + '`' for x in lb)} |")
        elif ns: nosrc += 1; L.append(f"| {v} | (no source expected) |")
        else: L.append(f"| {v} | **no source** |")
    L += ["", f"Numbers: {len(seen)}; with a sheet source: {ok}; no source expected: {nosrc}; without source: {len(seen) - ok - nosrc}."]
    pathlib.Path(a.out).write_text("\n".join(L) + "\n"); print(L[-1])
if __name__ == "__main__": main()
