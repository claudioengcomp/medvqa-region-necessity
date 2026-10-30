"""Item 1 (CPU): inventory of the 81 runs, coverage run x condition x benchmark, checkpoint stamp per prediction file, unit counts.
Outputs: analysis/inventario_linhas.json, analysis/cobertura.json, docs/item1_inventario.md. Sources are read only."""
import collections, glob, json, os, socket, sys, time
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
T0 = time.time()
def prov(p):
    try: return json.load(open(p)).get("provenance") or {}
    except Exception: return {}
def ckpt_from_prov(pv):
    for k in ("checkpoint_sha256", "adapter_sha256", "adapter_model_sha256", "weights_sha256"):
        if pv.get(k): return pv[k], k
    return None, None
ADS = json.load(open(f"{PLC}/manifests/adapters_sha256.json"))["files"]
def recovered(base, L):
    """sha recovered outside the prediction JSON: (sha, file, how)."""
    ln, s = L["line"], L["seed"]
    if L["fam"] == "M3AE" and base in ("KVASIR", "HEAL"):
        ck = sorted(glob.glob(f"{W}/doutorado/M3AE/checkpoints/task_finetune_vqa_{base.lower()}-seed{s}-from_downloaded_pretrained_m3ae.ckpt_dummy/*/checkpoints/*.ckpt"))
        if len(ck) == 1: return sha(ck[0]), ck[0], "recuperado: unico .ckpt no diretorio de treino da configuracao (M3AE/checkpoints)"
        return None, ";".join(f"{c} sha256={sha(c)}" for c in ck), f"nao carimbado: {len(ck)} .ckpt candidatos (shas listados)"
    if base == "KVASIR" and L["pack"].startswith("15"):
        cfg = f"{'qwen2vl' if L['fam'] == 'QWEN2VL' else 'smolvlm2'}_{L['method'].lower()}_kvasir_seed{s}"
        if L["fam"] == "SMOLVLM" and L["method"] == "DORA" and s in (1, 2):
            p = f"{PLC}/outputs/models/smolvlm2_dora_kvasir_e6_seed{s}/adapter_model.safetensors"; return sha(p), p, "recuperado: adapter E6 (preregistration_v2.md, E6: as linhas SMOLVLM_DORA_KVASIR_seed1-2 foram substituidas pelos adapters _e6)"
        p = f"{P0}/outputs/models/{cfg}/adapter_model.safetensors"; return sha(p), p, "recuperado: adapter em p0/outputs/models por convencao de nome (linha publicada de 01/10)"
    if base == "HEAL" and L["pack"].startswith("15"):
        cfg = f"{'qwen2vl' if L['fam'] == 'QWEN2VL' else 'smolvlm2'}_{L['method'].lower()}_heal_seed{s}"
        k = f"{cfg}/adapter_model.safetensors"
        if k in ADS: return ADS[k]["sha256"], f"{PLC}/manifests/adapters_sha256.json [{k}]", "recuperado: manifests/adapters_sha256.json do worktree placebo (04/10)"
        return None, f"{PLC}/outputs/models/{cfg}", "nao carimbado: adapter original ausente na gpu1"
    return None, None, "nao carimbado"
inv = {}; cov = {}; uncstamped = []
for base in BASES:
    rows = []
    for L in lines(base):
        conds = COND_MAIN + COND_DOSE + COND_OTHER + SHAM[base]
        files = {c: find(base, L["line"], c) for c in conds}
        tf = txt_file(base, L["fam"], L["seed"])
        stamps = {}
        for c, p in list(files.items()) + [("TXT", tf)]:
            if p is None: continue
            pv = prov(p); cs, key = ckpt_from_prov(pv)
            stamps[c] = {"file": p, "file_sha256": sha(p), "checkpoint_sha256": cs, "fonte_do_sha": f"carimbo do JSON ({key})" if cs else None,
                         "host": pv.get("host"), "t": pv.get("t") or pv.get("date") or pv.get("timestamp") or pv.get("start") or pv.get("t_start") or pv.get("end"),
                         "commit": pv.get("git_commit") or pv.get("commit") or pv.get("worktree_commit") or pv.get("git_commit_isbi_worktree") or pv.get("git_commit_p0")
                                   or ((pv.get("git") or {}).get("commit") if isinstance(pv.get("git"), dict) else None) or ((pv.get("git") or {}).get("head") if isinstance(pv.get("git"), dict) else None)
                                   or (json.dumps(pv.get("git"))[:120] if pv.get("git") else None)}
        rec_sha, rec_file, rec_how = recovered(base, L)
        own = next(((c, st) for c, st in stamps.items() if c != "TXT" and st["checkpoint_sha256"] and st["fonte_do_sha"].startswith("carimbo")), None)
        for c, st in stamps.items():
            if c == "TXT": continue
            if st["checkpoint_sha256"] is None and own and not (L["line"] in DOSE_ALIAS and base == "HEAL" and c in COND_DOSE + COND_OTHER):
                st["checkpoint_sha256"] = own[1]["checkpoint_sha256"]; st["fonte_do_sha"] = f"recuperado do carimbo da condicao {own[0]} da mesma linha ({own[1]['file']})"
            if st["checkpoint_sha256"] is None and rec_sha:
                st["checkpoint_sha256"] = rec_sha; st["fonte_do_sha"] = f"{rec_how} ({rec_file})"
            if st["checkpoint_sha256"] is None:
                st["fonte_do_sha"] = rec_how; uncstamped.append({"base": base, "line": L["line"], "cond": c, "file": st["file"], "motivo": rec_how})
        if L["line"] in DOSE_ALIAS and base == "HEAL":
            for c in COND_DOSE + COND_OTHER:
                if c in stamps: stamps[c]["nota"] = "arquivo do retreino de 03/10 (QWEN2VL_DORA_HEAL_seed2_retrain20261003); 1x vem do adapter original"
        rows.append({**L, "files": files, "txt_file": tf, "txt_line": txt_line(base, L["fam"], L["seed"]), "stamps": stamps})
        cov.setdefault(base, {})[L["line"]] = {c: (files[c] is not None) for c in conds} | {"TXT": tf is not None}
    inv[base] = rows
# zero-shot
zs = {}
for base in BASES:
    for m in ZS:
        conds = ["C0", "T", "P", "S", "T_blur10", "P_blur10", "T_regmean", "P_regmean", "TXT"] + SHAM[base]
        fs = {c: (zs_file(m, base, c) if os.path.exists(zs_file(m, base, c)) else None) for c in conds}
        pv = prov(fs["C0"]) if fs["C0"] else {}
        zs[f"{m}_{base}"] = {"files": fs, "base_model": pv.get("base_model"), "file_sha256": {c: sha(p) for c, p in fs.items() if p}}
        cov.setdefault(base, {})[f"{m}_ZEROSHOT"] = {c: fs[c] is not None for c in conds}
# unit counts
units = {}
d = json.load(open(INV["KVASIR"])); ev = [q for q in d["questions"] if q["evaluable"]]; s = d["summary"]
units["KVASIR"] = {"fonte": INV["KVASIR"], "fonte_sha256": sha(INV["KVASIR"]), "n_perguntas": s["n_questions"], "n_avaliaveis": len(ev),
    "por_classe": dict(collections.Counter(q["question_class"] for q in ev)), "imagens_com_pergunta_avaliavel": len({q["image_id"] for q in ev}),
    "unidades_imagem_x_alvo": s["images"]["with_target"], "unidades_por_tipo": s["images"]["by_kind"], "imagens_teste": s["n_images"],
    "imagens_excluidas": s["images"]["excluded"], "imagens_com_mascara": s["images"]["with_target"] + s["images"]["excluded"]["no_valid_placement"] + s["images"]["excluded"]["area_gt_max"],
    "nota": "303 = 243 unidades + 44 sem posicao valida + 16 area > max (imagens com mascara); a unidade estatistica do Kvasir e a imagem (uma imagem = um alvo)"}
d = json.load(open(INV["HEAL"])); ev = [q for q in d["questions"] if q["evaluable"]]; s = d["summary"]
multi = [q for q in ev if q.get("n_anatomies_in_image", 1) >= 2]
units["HEAL"] = {"fonte": INV["HEAL"], "fonte_sha256": sha(INV["HEAL"]), "n_perguntas": s["n_questions"], "n_avaliaveis": len(ev), "por_classe": dict(collections.Counter(q["question_class"] for q in ev)),
    "unidades_imagem_x_anatomia": len({(q["image_id"], q["anatomy"]) for q in ev}), "imagens": len({q["image_id"] for q in ev}), "sem_posicao_valida": s["n_closed_without_placement"],
    "perguntas_em_imagens_com_2+_anatomias": len(multi), "metodos_placebo_unidades": s["placebo_methods"]}
d = json.load(open(INV["MIMIC"])); ev = [q for q in d["questions"] if q["evaluable"]]; s = d["summary"]
v1 = f"{W}/tmp/v7_mimic/inventory_mimic_test_v1_final.json"; d1 = json.load(open(v1)) if os.path.exists(v1) else None
units["MIMIC"] = {"fonte": INV["MIMIC"], "fonte_sha256": sha(INV["MIMIC"]), "versao": s.get("version"), "n_perguntas": s["n_questions"], "n_avaliaveis": len(ev),
    "por_classe": dict(collections.Counter(q["question_class"] for q in ev)), "por_classe_so_exatas": dict(collections.Counter(q["question_class"] for q in ev if q.get("entity_map_quality") == "exata")),
    "imagens": len({q["image_id"] for q in ev}), "imagens_por_classe": {k: len({q["image_id"] for q in ev if q["question_class"] == k}) for k in ("closed_yes", "closed_no", "closed_no_sham", "open")},
    "v1": ({"fonte": v1, "fonte_sha256": sha(v1), "n_avaliaveis": d1["summary"]["n_evaluable"], "por_classe": d1["summary"]["evaluable_by_class"]} if d1 else None),
    "explicacao_473_443": "473 (e 2 152 avaliaveis) = inventario v1 (11/10, regiao mais fina, placebo por bloco); 443 (e 1 985) = inventario v2 (12/10, placebo por caixa, decisao do candidato apos a galeria). As predicoes T/P/S existentes foram geradas sobre os arrows v2 (sha no manifesto de condicoes). 430 = v2 so exatas.",
    "conjunto_fixado": "v2 completo (443 fechadas-sim, 54-67 fechadas-nao conforme alinhamento, 391 negativas do oclusor); so exatas como variante de sensibilidade"}
# zero-shot: same qids?
qid_check = {}
for base in BASES:
    ref = find(base, lines(base)[0]["line"], "T"); R = {int(x["qid"]) for x in json.load(open(ref))["predictions"]}
    for m in ZS:
        p = zs_file(m, base, "T")
        if os.path.exists(p): Z = {int(x["qid"]) for x in json.load(open(p))["predictions"]}; qid_check[f"{m}_{base}"] = {"ref": ref, "n_ref": len(R), "n_zs": len(Z), "iguais": R == Z, "so_ref": len(R - Z), "so_zs": len(Z - R)}
out = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "host": HOST, "script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__)), "lines": inv, "zeroshot": zs, "unidades": units, "zeroshot_qids": qid_check, "nao_carimbados": uncstamped}
json.dump(out, open(f"{OUT}/analysis/inventario_linhas.json", "w"), indent=1)
json.dump({"t": out["t"], "script": os.path.relpath(__file__), "cobertura": cov}, open(f"{OUT}/analysis/cobertura.json", "w"), indent=1)
# markdown
M = ["# Item 1 — inventário das 81 linhas, cobertura e unidades", "", f"Gerado {out['t']} na {out['host']} por `scripts/item1_inventario.py` (sha256 `{out['script_sha256']}`). JSON: `analysis/inventario_linhas.json`, `analysis/cobertura.json`. Só leitura nas fontes.", ""]
M += ["## Unidades por base", ""]
for b, u in units.items():
    M += [f"### {b}", "", "```", json.dumps(u, indent=1, ensure_ascii=False), "```", ""]
for b in BASES:
    M += [f"## {b}: linhas e checkpoints", "", "| linha | família | método | encoder | semente | pacote | sha256 do checkpoint (C0) | fonte do sha |", "|---|---|---|---|---|---|---|---|"]
    for r in inv[b]:
        st = r["stamps"].get("C0") or r["stamps"].get("T") or {}
        M.append(f"| {r['line']} | {r['family']} | {r['method']} | {r['encoder']} | {r['seed']} | {r['pack']} | `{(st.get('checkpoint_sha256') or 'não carimbado')[:16]}` | {st.get('fonte_do_sha')} |")
    conds = list(next(iter(cov[b].values())).keys())
    M += ["", f"### {b}: cobertura linha × condição (✓ existe, ✗ falta)", "", "| linha | " + " | ".join(conds) + " |", "|---|" + "---|" * len(conds)]
    for ln, c in cov[b].items():
        M.append(f"| {ln} | " + " | ".join("✓" if c.get(k) else "✗" for k in conds) + " |")
    falt = {ln: [k for k, v in c.items() if not v] for ln, c in cov[b].items() if not ln.endswith("ZEROSHOT")}
    falt = {k: v for k, v in falt.items() if v}
    M += ["", f"Faltas nas 27 linhas afinadas: " + (json.dumps(falt, ensure_ascii=False) if falt else "nenhuma"), ""]
M += ["## Zero-shot: mesmos qids das linhas afinadas (condição T)", "", "| modelo × base | n afinada | n zero-shot | iguais | só afinada | só zero-shot |", "|---|---|---|---|---|---|"]
M += [f"| {k} | {v['n_ref']} | {v['n_zs']} | {v['iguais']} | {v['so_ref']} | {v['so_zs']} |" for k, v in qid_check.items()]
M += ["", f"## Predições sem sha de checkpoint recuperável: {len(uncstamped)}", ""] + [f"- {x['base']} {x['line']} {x['cond']}: {x['motivo']} (`{x['file']}`)" for x in uncstamped[:200]]
M += ["", f"Tempo de CPU (parede): {time.time() - T0:.0f} s."]
open(f"{OUT}/docs/item1_inventario.md", "w").write("\n".join(M) + "\n"); print("ok", round(time.time() - T0), "s; nao carimbados:", len(uncstamped))
