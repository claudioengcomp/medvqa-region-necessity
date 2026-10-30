"""Compare JSON files of two directories field by field, ignoring volatile fields (time stamps, script paths and their hashes, host name).
Usage: compare_json.py <dir_published> <dir_regenerated> [--glob PATTERN]"""
import glob, json, os, sys
VOL = {"t", "segundos", "script", "script_sha256", "host", "engine", "engine_sha256", "shamstats", "shamstats_sha256"}
volatile = lambda k: k in VOL or (k.startswith("compute_necessity_") and k.endswith("_sha256"))
def norm(x):
    if isinstance(x, dict): return {k: norm(v) for k, v in x.items() if not volatile(k)}
    if isinstance(x, list): return [norm(v) for v in x]
    return x
def diff(x, y, p, out):
    if type(x) != type(y): out.append(f"{p}: type"); return
    if isinstance(x, dict):
        for k in set(x) | set(y):
            if k not in x or k not in y: out.append(f"{p}/{k}: only in one side"); continue
            diff(x[k], y[k], f"{p}/{k}", out)
    elif isinstance(x, list):
        if len(x) != len(y): out.append(f"{p}: length {len(x)} vs {len(y)}"); return
        for i, (u, v) in enumerate(zip(x, y)): diff(u, v, f"{p}[{i}]", out)
    elif x != y and not (isinstance(x, float) and isinstance(y, float) and abs(x - y) <= 1e-9 * max(1.0, abs(x))): out.append(f"{p}: {str(x)[:60]} vs {str(y)[:60]}")
a, b = sys.argv[1], sys.argv[2]; pat = sys.argv[sys.argv.index("--glob") + 1] if "--glob" in sys.argv else "*.json"
files = sorted(os.path.basename(f) for f in glob.glob(os.path.join(a, pat))); bad = 0
for f in files:
    if not os.path.exists(os.path.join(b, f)): print("  missing in regenerated:", f); bad += 1; continue
    out = []; diff(norm(json.load(open(os.path.join(a, f)))), norm(json.load(open(os.path.join(b, f)))), "", out)
    if out: bad += 1; print(f"  {f}: {len(out)} differences, e.g. {out[0]}")
print(f"  {len(files)} files compared, {len(files) - bad} identical (volatile fields ignored)"); sys.exit(1 if bad else 0)
