"""Round 6 (21/10/2026, CPU): Kvasir-VQA-x1 split.
(a) official HF split (SimulaMet/Kvasir-VQA-x1, parquets copied from the cache to inputs/kvasir_vqa_x1_hf/, sha256 = blob name): images of the
    official test set that appear in the official training set, by img_id;
(b) our split (data/finetune_arrows/vqa_kvasir_{train,val,test}_clean.arrow): intersections by image_id and by md5 of the image bytes; units of
    data/isbi_placebo/vqa_kvasir_placebo_C0.arrow whose bytes repeat a training or validation image;
(c) sensitivity: the 27 Kvasir runs recomputed without the questions of the images of those units, with the same engine and the SAME replicate
    matrix (Base built over all images of the inventory; only the qids are removed), compared with the full computation (analysis/necessity_v2).
Output: analysis/split_kvasir.json. Nothing is re-inferred."""
import collections, hashlib, json, os, sys, time
import pyarrow as pa, pyarrow.parquet as pq
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
import engine as E
import analise_bases as AB
T0 = time.time(); A = f"{PLC}/data"
def arrow(p):
    with pa.memory_map(p) as s:
        try: r = pa.ipc.open_file(s)
        except Exception: r = pa.ipc.open_stream(s)
        return r.read_all()
def md5s(p):
    t = arrow(p); ids = t.column("image_id").to_pylist(); out = {}
    for i, b in zip(ids, t.column("image").to_pylist()): out[i] = hashlib.md5(b).hexdigest()
    return out
OUTJ = {"t": None, "script": os.path.relpath(__file__), "script_sha256": sha(os.path.relpath(__file__))}
# (a) official split
H = {}
for sp in ("train", "test"):
    p = f"{LAB_INPUTS}/kvasir_vqa_x1_hf/{sp}-00000-of-00001.parquet"; t = pq.read_table(p, columns=["img_id"]); H[sp] = {"arquivo": p, "sha256": sha(p), "linhas": t.num_rows, "img_ids": set(t.column("img_id").to_pylist())}
OUTJ["oficial_hf"] = {"fonte": "SimulaMet/Kvasir-VQA-x1, snapshot 61e41148c3214bc5140ad0ab4c28520a512e2a73 (cache ~/.cache/huggingface do gpu1, copiado para inputs/)",
                      **{sp: {"arquivo": H[sp]["arquivo"], "sha256": H[sp]["sha256"], "pares_pergunta_resposta": H[sp]["linhas"], "imagens": len(H[sp]["img_ids"])} for sp in H},
                      "imagens_do_teste_no_treino": len(H["test"]["img_ids"] & H["train"]["img_ids"]), "imagens_do_teste": len(H["test"]["img_ids"]),
                      "docstring": f"{PLC}/harness/prepro/build_kvasir_clean_split.py: 3,821 of its 4,058 test images (94%)", "docstring_sha256": sha(f"{CODE_ROOT}/harness/prepro/build_kvasir_clean_split.py"),
                      "nota_teste_automatico": "tests/prepro/test_kvasir_split.py so testa split_records_by_image em registros sinteticos; nao mede o split oficial"}
# (b) nosso split
F = {sp: f"{A}/finetune_arrows/vqa_kvasir_{sp}_clean.arrow" for sp in ("train", "val", "test")}; M = {sp: md5s(p) for sp, p in F.items()}
U = f"{A}/isbi_placebo/vqa_kvasir_placebo_C0.arrow"; MU = md5s(U)
inv_md5 = {sp: collections.defaultdict(set) for sp in M}
for sp in M:
    for i, h in M[sp].items(): inv_md5[sp][h].add(i)
def byte_inter(a, b): return sorted(i for i, h in M[a].items() if h in inv_md5[b])
dup_units = sorted(i for i, h in MU.items() if h in inv_md5["train"] or h in inv_md5["val"])
OUTJ["nosso_split"] = {"arquivos": {sp: {"arquivo": p, "sha256": sha(p), "imagens": len(M[sp])} for sp, p in F.items()},
    "por_image_id": {"treino_teste": len(set(M["train"]) & set(M["test"])), "val_teste": len(set(M["val"]) & set(M["test"])), "treino_val": len(set(M["train"]) & set(M["val"]))},
    "por_bytes_md5": {"teste_com_copia_no_treino": len(byte_inter("test", "train")), "teste_com_copia_na_val": len(byte_inter("test", "val")), "val_com_copia_no_treino": len(byte_inter("val", "train")),
                      "teste_com_copia_no_treino_ou_val": len(set(byte_inter("test", "train")) | set(byte_inter("test", "val"))),
                      "md5_repetidos_dentro_do_teste": sum(1 for h, s in inv_md5["test"].items() if len(s) > 1)},
    "unidades": {"arquivo": U, "sha256": sha(U), "n": len(MU), "duplicadas": [{"image_id": i, "copia_no_treino": sorted(inv_md5["train"].get(MU[i], [])), "copia_na_val": sorted(inv_md5["val"].get(MU[i], []))} for i in dup_units]}}
# (c) sensibilidade
inv = json.load(open(INV["KVASIR"])); IMG = {int(q["qid"]): q["image_id"] for q in inv["questions"]}; B = E.Base(IMG)
nid = lambda i: i.split("/", 1)[-1]   # the inventory stores the image_id without the "kvasir/" prefix of the arrows
drop = {nid(i) for i in dup_units}; ev = [q for q in inv["questions"] if q["evaluable"]]
OUTJ["perguntas_avaliaveis_nas_unidades"] = {i: dict(collections.Counter(q["question_class"] for q in ev if q["image_id"] == nid(i))) for i in dup_units}
OUTJ["perguntas_avaliaveis_nas_unidades_total"] = dict(collections.Counter(q["question_class"] for q in ev if q["image_id"] in drop))
G, extra, fam = AB.classes("KVASIR", inv); M0v, _ = AB.m0_for("KVASIR")
G2 = {k: [q for q in v if IMG[q] not in drop] for k, v in G.items()}; TPL = "template=Is there a green/black box artefact?"; X2 = {TPL: [q for q in extra[TPL] if IMG[q] not in drop]}
OUTJ["qids_retirados_por_classe"] = {k: len(G[k]) - len(G2[k]) for k in G} | {"artefato": len(extra[TPL]) - len(X2[TPL])}
assert sum(OUTJ["qids_retirados_por_classe"].values()) > 0, "nenhum qid retirado: conferir o formato do image_id"
CL = ["dependent_polyp", "dependent_instrument", "negative_control", "controle_texto"]
QK = ["headroom", "delta_preto", "delta_blur10", "custo_mascara_deslocada_preto", "custo_mascara_deslocada_blur10", "suficiencia_preto"]
def lo(bk, k): c = bk.get(k); return c[0] if c else None
def steps(bk):
    L0 = (lo(bk, "custo_alvo_preto_ci_by_image") or 0) > 0; L1 = (lo(bk, "delta_preto_ci_by_image") or 0) > 0; L2 = L1 and (lo(bk, "delta_blur10_ci_by_image") or 0) > 0
    return {"L0": L0, "L1": L1, "L2": L2, "L3": L2 and (lo(bk, "headroom_ci_by_image") or 0) > 0}
def summ(recs):
    s = {}
    for c in CL:
        bks = [r["by_class"][c] for r in recs]; st = [steps(b) for b in bks]
        s[c] = {"n_por_linha": sorted({b["n"] for b in bks}), "escada": {d: sum(x[d] for x in st) for d in ("L0", "L1", "L2", "L3")},
                "resoluveis": sum(1 for b in bks if (lo(b, "headroom_ci_by_image") or 0) > 0), "B": sum(1 for b in bks if b.get("criterio_B")),
                "B_entre_resoluveis": sum(1 for b in bks if b.get("criterio_B") and (lo(b, "headroom_ci_by_image") or 0) > 0),
                "faixas": {k: {"min": min(b[k] for b in bks if b.get(k) is not None), "max": max(b[k] for b in bks if b.get(k) is not None)} for k in QK}}
    t = [r["extra"][TPL] for r in recs]
    s["artefato"] = {"n_por_linha": sorted({b["n"] for b in t})} | {f: {"ic_sup_menor_0": sum(1 for b in t if b[f"delta_{f}_ci_by_image"][1] < 0), "ic_inf_maior_0": sum(1 for b in t if b[f"delta_{f}_ci_by_image"][0] > 0)} for f in ("preto", "blur10", "regmean")}
    return s
full, sem = [], []; por_linha = {}
for L in lines("KVASIR"):
    r = json.load(open(f"{OUT}/analysis/necessity_v2/{L['line']}_KVASIR.json")); full.append(r)
    r2 = AB.analyse_line(B, "KVASIR", L["line"], r["files"], r["txt_file"], G2, X2, fam, M0v); sem.append(r2)
    por_linha[L["line"]] = {c: {k: r2["by_class"][c].get(k) for k in ["n", "acc", "headroom", "headroom_ci_by_image", "delta_preto", "delta_preto_ci_by_image", "delta_blur10", "delta_blur10_ci_by_image",
                                                                        "custo_alvo_preto", "custo_alvo_preto_ci_by_image", "custo_mascara_deslocada_preto", "custo_mascara_deslocada_blur10", "suficiencia_preto", "criterio_B"]} for c in CL} | {"artefato": {k: v for k, v in r2["extra"][TPL].items() if k.startswith(("n", "delta_"))}}
SF, SS = summ(full), summ(sem)
OUTJ["sensibilidade"] = {"regra": "sem as perguntas avaliaveis das imagens das unidades duplicadas; mesma matriz de replicas (2000, semente 20260913, todas as imagens do inventario)", "completo": SF, "sem_duplicadas": SS, "por_linha_sem_duplicadas": por_linha}
OUTJ["t"] = time.strftime("%Y-%m-%d %H:%M:%S"); OUTJ["segundos"] = round(time.time() - T0)
json.dump(OUTJ, open(f"{OUT}/analysis/split_kvasir.json", "w"), indent=1)
print(json.dumps({"oficial": {k: OUTJ["oficial_hf"][k] for k in ("imagens_do_teste_no_treino", "imagens_do_teste")}, "nosso": {k: OUTJ["nosso_split"][k] for k in ("por_image_id", "por_bytes_md5")}, "unidades": OUTJ["nosso_split"]["unidades"]["duplicadas"], "perguntas": OUTJ["perguntas_avaliaveis_nas_unidades"], "retirados": OUTJ["qids_retirados_por_classe"]}, ensure_ascii=False))
for c in CL + ["artefato"]: print(c, "COMPLETO", json.dumps(SF[c]), "\n   SEM", json.dumps(SS[c]))
print("segundos", OUTJ["segundos"])
