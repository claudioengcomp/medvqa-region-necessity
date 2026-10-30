"""Write or verify SHA-256 checksums (portable replacement for sha256sum).  write <root> <out>  |  verify <sumsfile>"""
import hashlib, os, sys
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""): h.update(b)
    return h.hexdigest()
cmd = sys.argv[1]
if cmd == "write":
    root, out = sys.argv[2], sys.argv[3]; L = []
    for dp, dn, fn in os.walk(root):
        for f in sorted(fn):
            p = os.path.join(dp, f); rel = os.path.relpath(p, root)
            if rel == os.path.relpath(out, root) or f.startswith("."): continue
            L.append(f"{sha(p)}  {rel}")
    open(out, "w").write("\n".join(sorted(L, key=lambda s: s.split("  ", 1)[1])) + "\n"); print(len(L), "files")
elif cmd == "verify":
    sums = sys.argv[2]; root = os.path.dirname(sums); bad = 0; n = 0
    for line in open(sums):
        h, rel = line.rstrip("\n").split("  ", 1); n += 1
        p = os.path.join(root, rel)
        if not os.path.exists(p) or sha(p) != h: bad += 1; print("MISMATCH", rel)
    print(f"{n} files checked, {bad} mismatches"); sys.exit(1 if bad else 0)
