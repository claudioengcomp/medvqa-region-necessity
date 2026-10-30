"""Compare regenerated figures with the published ones: PDF after removing the creation/modification dates (a difference fails);
PNG byte by byte (a difference is reported as a warning only: font rendering differs across machines).
Usage: compare_figures.py <dir_published> <dir_regenerated> <name> [<name> ...]"""
import hashlib, os, re, sys
def pdf_norm(p): return re.sub(rb"/(CreationDate|ModDate)\s*\([^)]*\)", b"", open(p, "rb").read())
a, b, names = sys.argv[1], sys.argv[2], sys.argv[3:]; bad = 0
for n in names:
    for ext in ("png", "pdf"):
        x, y = os.path.join(a, f"{n}.{ext}"), os.path.join(b, f"{n}.{ext}")
        if not os.path.exists(x): print(f"  {n}.{ext}: not published (skipped)"); continue
        same = (pdf_norm(x) == pdf_norm(y)) if ext == "pdf" else (open(x, "rb").read() == open(y, "rb").read())
        if same: print(f"  {n}.{ext}: identical")
        elif ext == "png": print(f"  {n}.{ext}: differs (warning only: PNG bytes vary with the font rendering of the machine; the PDF content is compared exactly)")
        else: print(f"  {n}.{ext}: DIFFERS"); bad += 1
sys.exit(0 if bad == 0 else 2)
