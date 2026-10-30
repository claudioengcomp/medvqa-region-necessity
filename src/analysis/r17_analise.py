"""Round 17 (analysis, CPU): image gain of the 36 DoRA runs (Qwen2-VL-2B and SmolVLM2-2.2B x frozen/fine-tuned encoder x seeds 0-2 x 3 benchmarks)
against the DoRA no-image baseline of the same family and seed: G_DoRA = A_int - A_text,DoRA, per-image 95 % CI (engine.block, 2 000 replicates,
seed 20260913, replicates fixed per benchmark), per Table 1 class. Comparison with the current G (LoRA baseline). Recount of criteria (iv) and (v)
of Table 1 (final rule of round 14) with G_DoRA on the DoRA runs; LoRA and M3AE do not change. Output: analysis/rodada17.json. Nothing changes in the paper."""
import collections, json, os, statistics, sys, time
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
import engine as E, analise_bases as AB
T0 = time.time(); NV2 = f"{OUT}/analysis/necessity_v2"; TK = NOIMG_DORA_DIRS
TCL = {"KVASIR": ["dependent_polyp", "dependent_instrument", "negative_control"], "HEAL": ["closed_yes", "closed_no"], "MIMIC": ["closed_yes", "closed_no"]}
def lo(c): return c[0] if c else None
def ok(bk, k): return (lo(bk.get(k)) or 0) > 0
R14 = json.load(open(f"{OUT}/analysis/rodada14.json"))["por_linha"]
OUTJ = {"script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "regra": "G_DoRA = Acc(intacta) - Acc(baseline sem imagem DoRA da mesma familia e semente); criterio (iv) = Delta preto e Delta blur 10 % e ganho (IC > 0); (v) = (iv) e queda bruta sob preto e sob blur 10 % (IC > 0)", "por_linha": {}, "txt": {}}
for b in BASES:
    inv = json.load(open(INV[b])); IMG = {int(q["qid"]): q["image_id"] for q in inv["questions"]}; Bb = E.Base(IMG); G, extra, _ = AB.classes(b, inv)
    for L in lines(b):
        if L["method"] != "DORA": continue
        r = json.load(open(f"{NV2}/{L['line']}_{b}.json")); C = {c: E.load_correct(p) for c, p in r["files"].items() if c in E.CORE}
        tf = first_existing(TK, f"{L['fam']}_DORA_TXT_{b}_seed{L['seed']}_TXT.json"); TXd = E.load_correct(tf); core = [c for c in E.CORE if c in C]
        rec = {"familia": L["family"], "encoder": L["encoder"], "semente": L["seed"], "txt_dora": tf, "txt_dora_sha256": sha(tf), "classes": {}}
        for c in TCL[b]:
            qs = [q for q in G[c] if all(q in C[k] for k in core)]; bkd = E.block(Bb, qs, C, TXd); bk = r["by_class"][c]
            old = R14[f"{b}|{L['line']}"]["classes"][c]["testes_ic"]
            iv_old = old["L1_preto"] and old["L2_blur10"] and old["ganho"]; v_old = iv_old and old["L0_preto"] and old["L0_blur10"]
            gd = ok(bkd, "headroom_ci_by_image"); iv_new = old["L1_preto"] and old["L2_blur10"] and gd; v_new = iv_new and old["L0_preto"] and old["L0_blur10"]
            rec["classes"][c] = {"n": bkd["n"], "acc_txt_lora": bk.get("acc_txt"), "acc_txt_dora": bkd.get("acc_txt"), "G": bk.get("headroom"), "G_ci": bk.get("headroom_ci_by_image"),
                                 "G_dora": bkd.get("headroom"), "G_dora_ci": bkd.get("headroom_ci_by_image"), "iv": iv_old, "iv_dora": iv_new, "v": v_old, "v_dora": v_new}
            OUTJ["txt"].setdefault(f"{b}|{c}|{L['fam']}|{L['seed']}", {"lora": bk.get("acc_txt"), "dora": bkd.get("acc_txt")})
        OUTJ["por_linha"][f"{b}|{L['line']}"] = rec
    print(b, round(time.time() - T0), "s", flush=True)
def ms(xs):
    xs = [x for x in xs if x is not None]; return {"media": statistics.mean(xs), "min": min(xs), "max": max(xs), "n": len(xs)} if xs else None
CMP, TXT, CNT, MUDA = {}, {}, {}, []
for b in BASES:
    for c in TCL[b]:
        rows = [(k, v["classes"][c]) for k, v in OUTJ["por_linha"].items() if k.startswith(b + "|")]
        d = [x["G_dora"] - x["G"] for _, x in rows if x["G"] is not None and x["G_dora"] is not None]
        CMP[f"{b}|{c}"] = {"runs_dora": len(rows), "G_menos_G_dora": {"media": statistics.mean([-z for z in d]), "min": min(-z for z in d), "max": max(-z for z in d)}, "G_dora_menos_G": ms(d)}
        for fam in ("QWEN2VL", "SMOLVLM"):
            t = [v for k, v in OUTJ["txt"].items() if k.startswith(f"{b}|{c}|{fam}|")]
            TXT[f"{b}|{c}|{fam}"] = {"lora": ms([x["lora"] for x in t]), "dora": ms([x["dora"] for x in t])}
        allr = R14  # all fine-tuned runs: LoRA and M3AE unchanged
        iv0 = sum(1 for k, v in allr.items() if k.startswith(b + "|") and not v["zero_shot"] and (lambda t: t["L1_preto"] and t["L2_blur10"] and t["ganho"])(v["classes"][c]["testes_ic"]))
        v0 = sum(1 for k, v in allr.items() if k.startswith(b + "|") and not v["zero_shot"] and v["classes"][c]["declarado_regra_final"])
        div = sum(int(x["iv_dora"]) - int(x["iv"]) for _, x in rows); dv = sum(int(x["v_dora"]) - int(x["v"]) for _, x in rows)
        CNT[f"{b}|{c}"] = {"iv_atual": iv0, "iv_com_G_dora": iv0 + div, "v_atual": v0, "v_com_G_dora": v0 + dv, "linhas": 27}
        for k, x in rows:
            if x["iv"] != x["iv_dora"] or x["v"] != x["v_dora"]: MUDA.append({"base": b, "classe": c, "linha": k.split("|")[1], **{kk: x[kk] for kk in ("G", "G_ci", "G_dora", "G_dora_ci", "iv", "iv_dora", "v", "v_dora")}})
OUTJ.update({"comparacao_G": CMP, "acc_txt_por_familia": TXT, "contagens": CNT, "runs_que_mudam": MUDA, "t": time.strftime("%Y-%m-%d %H:%M:%S"), "segundos": round(time.time() - T0)})
json.dump(OUTJ, open(f"{OUT}/analysis/rodada17.json", "w"), indent=1)
for k, v in CNT.items(): print(k, v, CMP[k]["G_dora_menos_G"])
for k, v in TXT.items(): print("txt", k, {kk: (round(vv["media"], 4), round(vv["min"], 4), round(vv["max"], 4)) if vv else None for kk, vv in v.items()})
print("mudam:", [(m["base"], m["classe"], m["linha"], round(m["G"], 4), round(m["G_dora"], 4), m["G_dora_ci"], m["v"], m["v_dora"]) for m in MUDA])
