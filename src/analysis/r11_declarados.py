"""Round 11 (21/10/2026, CPU): final declaration = both fills with a significant gain AND a raw drop (L3 and L0), per group (family x encoder),
for the classes of Table 1. Sources: analysis/rodada8.json (item1: L3_linhas and L3_sem_L0 per class) and analysis/criterio.json (resolvable runs
per group, CI rule without threshold). Output: analysis/declarados_r11.json."""
import collections, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
I1 = json.load(open(f"{OUT}/analysis/rodada8.json"))["item1"]; CR = json.load(open(f"{OUT}/analysis/criterio.json"))
TCL = {"KVASIR": ["dependent_polyp", "dependent_instrument", "negative_control"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no"]}
out = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "regra": "declarado = L3 (L1 e Delta blur 10 % e image gain, IC 95 % por imagem > 0) e L0 (queda bruta > 0)", "classes": {}}
for b in BASES:
    G = {L["line"]: f"{L['family']}, encoder {L['encoder']}" for L in lines(b)}
    for c in TCL[b]:
        x = I1[f"{b}|{c}|afinados"]; dec = sorted(set(x["L3_linhas"]) - set(x["L3_sem_L0"])); assert len(dec) == x["L3_e_L0"], (b, c)
        pg = CR["bases"][b]["por_classe"][c].get("por_grupo", {}); grupos = collections.OrderedDict()
        for ln, g in G.items(): grupos.setdefault(g, {"runs": 0, "declarados": 0, "resoluveis": pg.get(g, {}).get("resoluveis")}); grupos[g]["runs"] += 1; grupos[g]["declarados"] += ln in dec
        out["classes"][f"{b}|{c}"] = {"declarados": len(dec), "linhas_declaradas": dec, "por_grupo": grupos, "runs": len(G)}
json.dump(out, open(f"{OUT}/analysis/declarados_r11.json", "w"), indent=1)
for k, v in out["classes"].items(): print(k, v["declarados"], {g: (x["declarados"], x["resoluveis"], x["runs"]) for g, x in v["por_grupo"].items()})
