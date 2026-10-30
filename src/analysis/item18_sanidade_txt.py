"""Item 18 (CPU, read-only): sanity check of the text-only arm. (a) items that disagree between seeds of the same family and between families at
the same seed, over the whole set of TXT predictions of each benchmark (normalised prediction); (b) per class, fraction of items whose TXT prediction
is the majority answer of the template in the training set (template = exact question text; MIMIC also by template_id). Training sets: Kvasir
vqa_kvasir_train_clean.arrow, HEAL vqa_heal_train.arrow (text columns only, memory-mapped), MIMIC items_train.parquet. Outputs:
analysis/sanidade_txt.json, docs/item18_sanidade_txt.md."""
import collections, itertools, json, os, sys, time
import numpy as np, pandas as pd, pyarrow as pa
sys.path.insert(0, os.path.dirname(os.path.relpath(__file__))); from common import *
sys.path.insert(0, CODE_ROOT); from med_vlm.metrics.process_text import normalize_text
T0 = time.time()
TRAIN = {"KVASIR": f"{P0}/data/finetune_arrows/vqa_kvasir_train_clean.arrow", "HEAL": f"{PLC}/data/finetune_arrows/vqa_heal_train.arrow", "MIMIC": f"{V7M}/data/items_train.parquet"}
def train_majority(b):
    qa = collections.defaultdict(collections.Counter); tq = collections.defaultdict(collections.Counter)
    if b == "MIMIC":
        d = pd.read_parquet(TRAIN[b])
        for q, a, t in zip(d.question, d.answer, d.template_id): qa[q][normalize_text(str(a))] += 1; tq[t][normalize_text(str(a))] += 1
    else:
        with pa.memory_map(TRAIN[b]) as src:
            rd = pa.ipc.open_file(src)
            for i in range(rd.num_record_batches):
                bt = rd.get_batch(i).select(["questions", "answers"]).to_pydict()
                for qs, ans in zip(bt["questions"], bt["answers"]):
                    for q, a in zip(qs, ans): qa[q][normalize_text(str(a[0] if isinstance(a, list) else a))] += 1
    return {q: c.most_common(1)[0][0] for q, c in qa.items()}, {t: c.most_common(1)[0][0] for t, c in tq.items()}
FAM = ["QWEN2VL", "SMOLVLM", "M3AE"]
out = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "treino": {b: {"arquivo": p, "sha256": sha(p)} for b, p in TRAIN.items()}, "bases": {}}
for b in BASES:
    P = {}
    for f in FAM:
        for s in range(3):
            p = txt_file(b, f, s); P[(f, s)] = {int(x["qid"]): normalize_text(str(x["predicted"])) for x in json.load(open(p))["predictions"]}
    B = {"arquivos": {f"{f}_s{s}": txt_file(b, f, s) for f in FAM for s in range(3)}, "pares_sementes": {}, "pares_familias": {}}
    for f in FAM:
        for s1, s2 in itertools.combinations(range(3), 2):
            c = sorted(set(P[(f, s1)]) & set(P[(f, s2)])); B["pares_sementes"][f"{f} s{s1}-s{s2}"] = {"n": len(c), "discordantes": sum(P[(f, s1)][q] != P[(f, s2)][q] for q in c)}
    for s in range(3):
        for f1, f2 in itertools.combinations(FAM, 2):
            c = sorted(set(P[(f1, s)]) & set(P[(f2, s)])); B["pares_familias"][f"s{s} {f1}-{f2}"] = {"n": len(c), "discordantes": sum(P[(f1, s)][q] != P[(f2, s)][q] for q in c)}
    maj_q, maj_t = train_majority(b); inv = json.load(open(INV[b])); Q = {q["qid"]: q for q in inv["questions"]}
    G = {}
    ev = [q for q in inv["questions"] if q["evaluable"]]
    if b == "KVASIR":
        for k in ("dependent_polyp", "dependent_instrument", "dependent_polyp_secondary"): G[k] = [q["qid"] for q in ev if q["question_class"] == k]
        G["controle_texto"] = [q["qid"] for q in ev if q["question"] == "Is there text?"]
    elif b == "HEAL":
        for k in ("closed_yes", "closed_no"): G[k] = [q["qid"] for q in ev if q["question_class"] == k]
    else:
        it = pd.read_parquet(f"{V7M}/data/items_test.parquet"); TID = dict(zip(it.qid, it.template_id))
        for k in ("closed_yes", "closed_no"): G[k] = [q["qid"] for q in ev if q["question_class"] == k]
        for e in ("pleural effusion", "atelectasis", "lung opacity", "cardiomegaly", "edema", "vascular congestion"): G[f"entidade={e}"] = [q["qid"] for q in ev if q["question_class"] == "closed_yes" and q.get("entity") == e]
    cls = {}
    for k, qs in G.items():
        row = {"n": len(qs), "n_template_no_treino": sum(1 for q in qs if Q[q]["question"] in maj_q)}
        for f in FAM:
            for s in range(3):
                qq = [q for q in qs if q in P[(f, s)] and Q[q]["question"] in maj_q]
                row[f"{f}_s{s}_frac_majoritaria_template"] = (sum(P[(f, s)][q] == maj_q[Q[q]["question"]] for q in qq) / len(qq)) if qq else None
                if b == "MIMIC":
                    qt = [q for q in qs if q in P[(f, s)] and TID.get(q) in maj_t]
                    row[f"{f}_s{s}_frac_majoritaria_template_id"] = (sum(P[(f, s)][q] == maj_t[TID[q]] for q in qt) / len(qt)) if qt else None
                row[f"{f}_s{s}_respostas_distintas"] = len({P[(f, s)][q] for q in qs if q in P[(f, s)]})
        cls[k] = row
    B["classes"] = cls; out["bases"][b] = B; print(b, round(time.time() - T0), "s", flush=True)
json.dump(out, open(f"{OUT}/analysis/sanidade_txt.json", "w"), indent=1)
L = ["# Item 18 — sanidade do text-only arm (só leitura; nada alterado na folha)", "", "Predições TXT normalizadas (`normalize_text`). Template = texto exato da pergunta (Medical-Diff-VQA: também `template_id`, entidade mascarada). Fonte: `analysis/sanidade_txt.json`.", ""]
for b, B in out["bases"].items():
    L += [f"## {b}", "", "Itens discordantes entre sementes (mesma família) e entre famílias (mesma semente), no conjunto inteiro:", "", "| par | n | discordantes |", "|---|---|---|"]
    L += [f"| {k} | {v['n']} | {v['discordantes']} |" for k, v in list(B["pares_sementes"].items()) + list(B["pares_familias"].items())]
    L += ["", "Por classe: fração dos itens cuja predição TXT é a resposta majoritária do template no treino (Q s0 / s1 / s2; S ...; M ...) e nº de respostas distintas:", "", "| classe | n | n com template no treino | Qwen2-VL s0/s1/s2 | SmolVLM2 s0/s1/s2 | M3AE s0/s1/s2 | respostas distintas Q/S/M (s0) |", "|---|---|---|---|---|---|---|"]
    for k, r in B["classes"].items():
        fr = lambda f: " / ".join("—" if r[f"{f}_s{s}_frac_majoritaria_template"] is None else f"{r[f'{f}_s{s}_frac_majoritaria_template']:.3f}" for s in range(3))
        L.append(f"| {k} | {r['n']} | {r['n_template_no_treino']} | {fr('QWEN2VL')} | {fr('SMOLVLM')} | {fr('M3AE')} | {r['QWEN2VL_s0_respostas_distintas']}/{r['SMOLVLM_s0_respostas_distintas']}/{r['M3AE_s0_respostas_distintas']} |")
    if b == "MIMIC":
        L += ["", "Medical-Diff-VQA, por `template_id` (entidade mascarada):", "", "| classe | Qwen2-VL s0/s1/s2 | SmolVLM2 | M3AE |", "|---|---|---|---|"]
        for k, r in B["classes"].items():
            fr = lambda f: " / ".join("—" if r[f"{f}_s{s}_frac_majoritaria_template_id"] is None else f"{r[f'{f}_s{s}_frac_majoritaria_template_id']:.3f}" for s in range(3))
            L.append(f"| {k} | {fr('QWEN2VL')} | {fr('SMOLVLM')} | {fr('M3AE')} |")
    L.append("")
L.append(f"Tempo: {time.time() - T0:.0f} s.")
open(f"{OUT}/docs/item18_sanidade_txt.md", "w").write("\n".join(L) + "\n"); print("ok")
