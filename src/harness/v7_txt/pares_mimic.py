"""Measure pipeline on MIMIC (ESPEC_MEDIDA_MIMIC.md section 4; Amendment 10): matrix of same-question pairs, whole eligible pool, HEAL rule
(harness/medida/phase0_final.py full_pool): receiver i and donor j with the same question_key, test x test, never the same image.
Canonical functions imported from the measure pipeline's worktree (question_key, label, answer_sig, strata_of; not reimplemented). Absolute edges under MedSigLIP
from v6_medida/design/strata_edges.json (read-only). Distance d = 1 - cos per ruler (MIMIC__TEST__<regua>.npy, order of image_ids.json MIMIC__TEST).
informativo = len(sig_i & sig_j) == 0 (as in HEAL). Flags: mesmo_paciente (same patient; D3, sensitivity; subject_id from items_test.parquet),
escopo_denominador_zero (template with constant y across the images: negative control), controle_positivo (projection question_type, D5).
Outputs: v7_mimic/data/conditions_medida/design_matrix_mimic.parquet and v7_mimic/analysis/medida_pares_mimic.json (counts: stopping point)."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import collections, hashlib, json, sys, time
from pathlib import Path
import numpy as np, pandas as pd, pyarrow as pa
sys.path.insert(0, os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-medida")
from harness.medida.common import question_key, label, answer_sig, strata_of, RULERS, PRIMARY, sha256_file
R = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic"); E = R / "data/conditions_medida/embeddings"; EDGES_F = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v6_medida/design/strata_edges.json")
def main():
    edges = json.loads(EDGES_F.read_text())["edges"]
    with pa.memory_map(str(R / "data/vqa_mimic_test.arrow"), "rb") as f:
        try: t = pa.ipc.open_file(f).read_all()
        except Exception: t = pa.ipc.open_stream(pa.memory_map(str(R / "data/vqa_mimic_test.arrow"))).read_all()
    rows = []
    for img, qs, ans, qids, ats in zip(t.column("image_id").to_pylist(), t.column("questions").to_pylist(), t.column("answers").to_pylist(), t.column("question_id").to_pylist(), t.column("answer_type").to_pylist()):
        for q, a, qq, at in zip(qs, ans, qids, ats): rows.append({"qid": int(qq), "img": str(img), "lab": label(str(img)), "q": q, "qkey": question_key(q), "refs": list(a), "y": " | ".join(map(str, a)), "sig": answer_sig(a), "closed": int(at) == 0})
    T = pd.DataFrame(rows)
    it = pd.read_parquet(R / "data/items_test.parquet"); IT = it.set_index("qid")
    miss = [q for q in T.qid if q not in IT.index]; assert not miss, ("qid do arrow fora de items_test", miss[:5])
    T["subject_id"] = [IT.loc[q, "subject_id"] for q in T.qid]; T["question_type"] = [IT.loc[q, "question_type"] for q in T.qid]; T["template_id"] = [IT.loc[q, "template_id"] for q in T.qid]
    ids = json.loads((E / "image_ids.json").read_text())["MIMIC__TEST"]; lab_idx = {label(i): k for k, i in enumerate(ids)}
    DM = {}
    for r in RULERS:
        X = np.load(E / f"MIMIC__TEST__{r}.npy").astype(np.float64); assert len(X) == len(ids), (r, X.shape, len(ids))
        X = X / np.clip(np.linalg.norm(X, axis=1, keepdims=True), 1e-12, None); D = np.clip(1.0 - X @ X.T, 0.0, 2.0); np.fill_diagonal(D, 0.0); DM[r] = D
    scope = {k for k, g in T.groupby("qkey") if g.lab.nunique() >= 2 and g.y.nunique() == 1}
    out = []; n_same = 0
    for k, g in T.groupby("qkey"):
        recs = list(g.itertuples())
        for qi in recs:
            for qj in recs:
                if qj.lab == qi.lab: n_same += 1; continue
                a, b = lab_idx[qi.lab], lab_idx[qj.lab]
                r = {"benchmark": "MIMIC", "qid": qi.qid, "image_id_receptora": qi.img, "image_id_doadora": qj.img, "qid_doadora": qj.qid, "qkey": k, "y_i": qi.y, "y_j": qj.y, "informativo": len(qi.sig & qj.sig) == 0,
                     "fechada": bool(qi.closed), "question_type": qi.question_type, "template_id": qi.template_id, "mesmo_paciente": bool(qi.subject_id == qj.subject_id), "escopo_denominador_zero": k in scope}
                for rl in RULERS: r["d_" + rl] = float(DM[rl][a, b]); r["estrato_" + rl] = int(strata_of([r["d_" + rl]], edges)[0])
                r["estrato"] = r["estrato_" + PRIMARY]; out.append(r)
    M = pd.DataFrame(out).sort_values(["qid", "estrato", "image_id_doadora"]).reset_index(drop=True)
    vt = sorted({x for x in T.question_type.unique() if "view" in str(x).lower() or "projec" in str(x).lower()}); M["controle_positivo"] = M.question_type.isin(vt)
    f = R / "data/conditions_medida/design_matrix_mimic.parquet"; M.to_parquet(f, index=False)
    est = M[~M.escopo_denominador_zero]
    cnt = lambda g, col="estrato": {str(k): {"pares": int(len(x)), "informativos": int(x.informativo.sum()), "nao_informativos": int((~x.informativo).sum())} for k, x in g.groupby(col)}
    st = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "script": __file__, "script_sha256": sha256_file(__file__), "matriz": str(f), "matriz_sha256": sha256_file(f), "bordas": edges, "bordas_fonte": str(EDGES_F),
          "embeddings_sha256": {r: json.loads((E / f"MIMIC__TEST__{r}.meta.json").read_text())["sha256"] for r in RULERS},
          "n_perguntas": int(len(T)), "n_imagens": int(T.img.nunique()), "n_qkeys": int(T.qkey.nunique()), "n_qkeys_com_pares": int(M.qkey.nunique()), "pares_mesma_imagem_excluidos": n_same,
          "pares_total": int(len(M)), "pares_estimacao": int(len(est)), "pares_escopo_denominador_zero": int(M.escopo_denominador_zero.sum()), "qkeys_escopo_denominador_zero": len(scope), "receptoras_estimacao": int(est.qid.nunique()),
          "por_estrato_medsiglip (estimacao)": cnt(est), "por_estrato_por_regua (estimacao)": {rl: cnt(est, "estrato_" + rl) for rl in RULERS},
          "estratos_reportaveis_ge300_cada_grupo (medsiglip)": [k for k, v in cnt(est).items() if v["informativos"] >= 300 and v["nao_informativos"] >= 300],
          "por_tipo_de_pergunta (estimacao)": {qt: {"pares": int(len(x)), "informativos": int(x.informativo.sum()), "receptoras": int(x.qid.nunique())} for qt, x in est.groupby("question_type")},
          "por_tipo_e_estrato (estimacao)": {qt: cnt(x) for qt, x in est.groupby("question_type")},
          "mesmo_paciente (sensibilidade, D3)": {"pares": int(M.mesmo_paciente.sum()), "por_estrato_medsiglip": cnt(M[M.mesmo_paciente])},
          "controle_positivo (D5)": {"question_types": vt, "pares": int(M.controle_positivo.sum()), "por_estrato_medsiglip": cnt(M[M.controle_positivo])},
          "controle_negativo (escopo_denominador_zero)": {"qkeys": len(scope), "pares": int(M.escopo_denominador_zero.sum())}}
    (R / "analysis").mkdir(exist_ok=True); json.dump(st, open(R / "analysis/medida_pares_mimic.json", "w"), indent=1, ensure_ascii=False, default=str)
    print(json.dumps({k: st[k] for k in ("n_perguntas", "n_imagens", "n_qkeys", "n_qkeys_com_pares", "pares_total", "pares_estimacao", "receptoras_estimacao", "estratos_reportaveis_ge300_cada_grupo (medsiglip)")}, ensure_ascii=False))
    print(json.dumps(st["por_estrato_medsiglip (estimacao)"])); print(json.dumps({k: v for k, v in st["mesmo_paciente (sensibilidade, D3)"].items() if k == "pares"}), json.dumps(st["controle_positivo (D5)"]["question_types"]), st["controle_positivo (D5)"]["pares"])
if __name__ == "__main__": main()
