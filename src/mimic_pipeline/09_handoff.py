"""v7_mimic/scripts/09_handoff.py -- writes HANDOFF_GPU.md from the manifests (arrows, vocab, M0, PNG)."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json, socket, time
from pathlib import Path
V7 = Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic"); D = V7 / "data"
man = {s: json.load(open(D / f"manifest_mimic_{s}.json")) for s in ("train", "val", "test")}
for _s in man:  # absolute paths (the manifest stores the path relative to the cwd at generation time)
    man[_s]["file"]["path"] = str((V7 / man[_s]["file"]["path"]).resolve()) if not man[_s]["file"]["path"].startswith("/") else man[_s]["file"]["path"]
    man[_s]["vocab_file"] = str(D / "answer_vocab.json")
vocab = json.load(open(D / "answer_vocab.json"))
m0 = {t: json.load(open(V7 / f"results/M0_question_only_MIMIC_{t}.json")) for t in ("subset", "full")}
sub = json.load(open(V7 / "analysis/subset_report.json"))
png = {s: json.load(open(f"{os.environ.get('LAB_ROOT', 'LAB_ROOT')}/doutorado/data/derived/mimic_png/png_manifest_{s}.json")) for s in ("train", "val", "test")}
val_check = json.load(open(V7 / "logs/validate_arrows_medvlm.json")) if (V7 / "logs/validate_arrows_medvlm.json").is_file() else {}
def ci(d): return f"{d['accuracy']:.3f} [{d['ci95_low']:.3f}, {d['ci95_high']:.3f}]"
L = [f"# HANDOFF_GPU — MIMIC/Diff-VQA de imagem única (v7_mimic) → executor de GPU", "",
     f"Escrito em {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} na {socket.gethostname()} pelo executor só-CPU (P4). Nenhum YAML criado, nada lançado. "
     "Imagens (JPG/PNG/arrow) são dados credenciados do PhysioNet: ficam na gpu1.", "",
     "## Arrows (formato M3AE/med_vlm, uma linha por imagem; mesmo esquema de `data/finetune_arrows/vqa_heal_*.arrow`)",
     "| split | arquivo | sha256 | bytes | imagens | perguntas | pacientes |", "|---|---|---|---:|---:|---:|---:|"]
for s in ("train", "val", "test"):
    m = man[s]; L.append(f"| {s} | `{m['file']['path']}` | `{m['file']['sha256']}` | {m['file']['bytes']} | {m['n_images']} | {m['n_questions']} | {m['n_subjects']} |")
L += ["", f"- Vocabulário: `{man['test']['vocab_file']}` ({len(vocab)} respostas; `no`=0, `yes`=1, resto por frequência em train+val+test, como no HEAL). "
      "Respostas abertas de vocabulário fixo: `data/open_answer_vocab_fixed.json` (location 44, level 18, type 14).",
      "- `answer_type`: 0 = fechada (presence, view yes/no), 1 = aberta (location, level, type). `image_id` = `mimic/<dicom_id>`. `question_id` únicos: test 3 200 000+, val 3 210 000+, train 3 220 000+ (HEAL usa 3 000 000 e 3 100 000).",
      "- Itens tabulares (qid, subject_id, study_id, dicom_id, image_path, question_type, template_id, template, question, answer, answer_type, split, ViewPosition): `data/items_{train,val,test}.parquet`. Manifestos: `data/manifest_mimic_{split}.json`.",
      f"- PNG derivados (lado maior 1024, mesmo pipeline do heal_png, leitor JPEG): `doutorado/data/derived/mimic_png/{{train,val,test}}/<dicom_id>.png`; manifestos `png_manifest_*.json` (n = {png['train']['n_items']}/{png['val']['n_items']}/{png['test']['n_items']}, erros {len(png['train'].get('errors',{}))}/{len(png['val'].get('errors',{}))}/{len(png['test'].get('errors',{}))}).",
      "- Validação em CPU com `harness.circle_data_bridge.load_condition_dataset` + `med_vlm.data.normalizer.build_normalizer` (CUDA_VISIBLE_DEVICES=\"\", torch.cuda.is_available()=False), `logs/validate_arrows_medvlm.json`: " + "; ".join(f"{k}: sha=manifesto {r['sha256_matches_manifest']}, len(ds)=perguntas {r['ds_len_equals_questions']}, labels=vocab {r['answer_labels_match_vocab']}, answer_type {r['answer_type_values']}, batch de 8 OK (ids {r['batch8_ids'][0]}…{r['batch8_ids'][-1]}, imagens modo {r['example']['image_mode']} lado maior 1024)" for k, r in val_check.get("splits", {}).items()) + ".", "",
      "## Contagens (docs/subset.md)", "| split | perguntas | imagens | pacientes | fechadas | abertas | PA / AP |", "|---|---:|---:|---:|---:|---:|---|"]
for s in ("train", "val", "test"):
    r = sub["step5"][s]; L.append(f"| {s} | {r['n_questions']} | {r['n_images']} | {r['n_subjects']} | {r['by_answer_type'].get('closed',0)} | {r['by_answer_type'].get('open',0)} | {r['ViewPosition'].get('PA',0)} / {r['ViewPosition'].get('AP',0)} |")
L += ["", "Templates (12 no subconjunto): " + "; ".join(f"{k} `{v}`" for k, v in sorted(sub["template_ids"].items()) if k in m0["subset"]["by_template"]), "",
      "## M0 só-pergunta (docs/m0_mimic.md; `results/M0_question_only_MIMIC_{subset,full}.json`)",
      f"- Fechadas (n = {m0['subset']['overall_closed']['n']}): M0 subset {ci(m0['subset']['overall_closed'])}; M0 full {ci(m0['full']['overall_closed'])}; prior-majoritário por template {ci(m0['subset']['by_answer_type']['closed']['prior_majority'])}.",
      f"- Abertas (n = {m0['subset']['by_answer_type']['open']['m0']['n']}): prior-majoritário por template subset {ci(m0['subset']['by_answer_type']['open']['prior_majority'])}, full {ci(m0['full']['by_answer_type']['open']['prior_majority'])}.",
      f"- Todas (n = 3000): M0 subset {ci(m0['subset']['overall_all_m0'])}; prior subset {ci(m0['subset']['overall_all_prior'])}; prior full {ci(m0['full']['overall_all_prior'])}.", "",
      "## Hiperparâmetros sugeridos (copiar os YAMLs do HEAL, mudando só dados e caminhos)",
      "Base: `med-vqa-icdip-placebo/med_vlm/configs/qwen2vl_lora_heal.yaml` (@2b7e731): QWEN2VL, LORA r=16 alpha=32, lr 2e-4, warmup 0.05, 3 épocas, batch 4 × grad_accum 4, max_length 8192, gradient_checkpointing, compile, eval_every 5000, checkpoint_every 15000 (+ `checkpoint_dir` do patch herdado), eval batch 2 / max_new_tokens 64, preprocessing denoise gaussian + CLAHE 2.0 (8,8), augmentation rot 5°, brilho/contraste 0.85–1.15, sem flips.",
      "O que muda: `dataset: MIMIC` (novo enum, p. ex. `DatasetName.MIMIC = \"mimic-local\"`, e `_MIMIC_ARROW_PATH` em `med_vlm/data/loader.py` apontando para os três arrows acima, no mesmo ramo do HEAL), `run_name`/`wandb_run_name`, `outputs_dir`/`results_json_dir` do executor de GPU. Nada mais.",
      "| braço | target_modules | diferenças | fonte do YAML de referência |", "|---|---|---|---|",
      "| `qwen2vl_lora_txt_mimic` | `^.*model\\.layers\\.\\d+\\.self_attn\\.(q|k|v|o)_proj$` (só LM) | `data.no_image: true`, `max_length 1024` | `v7_txt/configs/qwen2vl_lora_txt_heal.yaml` (patch `no_image` do v7_txt) |",
      "| `qwen2vl_lora_mimic` | `[q_proj, k_proj, v_proj, o_proj]` | nenhuma (linha publicada) | `med_vlm/configs/qwen2vl_lora_heal.yaml` |",
      "| `qwen2vl_lora_vt_mimic` | `.*self_attn\\.(q|k|v|o)_proj$|.*visual\\.blocks\\.\\d+\\.attn\\.(qkv|proj)$` (LM + torre) | nenhuma | `v6_tower_heal/worktree/med_vlm/configs/qwen2vl_lora_vt_heal.yaml` |",
      "Sementes 0, 1, 2 em cada braço (9 treinos). Teste em `vqa_mimic_test.arrow` com `harness.extract_predictions_circle` (condição C0; `--no-image` no braço txt), `--progress-checkpoint`, carimbo de proveniência; `--condition-arrow` deve ter o sha256 da tabela acima.",
      "Pré-processamento em cache: o `.map()` do med_vlm (`_kvasir_preprocess_cache_path`) grava em `data/finetune_arrows/preprocessed_cache/` relativo ao cwd do worktree; prever ~1,5× o tamanho do arrow de treino.", "",
      "## Patch sugerido para o worktree do GPU (`v7_txt/worktree`, base 2b7e731) — não aplicado por mim",
      "Os arrows locais entram pelo mesmo caminho do HEAL: `DatasetName.MIMIC` em `med_vlm/enums.py` e `_MIMIC_ARROW_PATH` + ramo em `load_dataset_by_enum` em `med_vlm/data/loader.py`. "
      "`run_experiment.py` resolve `DatasetName[cfg[\"dataset\"]]`, então o YAML usa `dataset: MIMIC`. Em `harness/extract_predictions_circle.py` o `--dataset` é texto livre (só rótulo do registro), e o arrow de teste vai em `--condition-arrow`. "
      "Caminhos absolutos; o cache do `.map()` cai em `data/finetune_arrows/preprocessed_cache/` relativo ao cwd (hash do caminho absoluto + mtime do arrow + repr do preprocessador).",
      "```diff",
      "--- a/med_vlm/enums.py",
      "+++ b/med_vlm/enums.py",
      "@@ class DatasetName(str, enum.Enum):",
      "     HEAL = \"heal-local\"",
      "+    # MIMIC-CXR-JPG 2.1.0 + Medical-Diff-VQA 1.0.1 (imagem única, PhysioNet, credenciado): arrows locais",
      "+    # gerados por $LAB_ROOT/v7_mimic/scripts/05_make_arrows.py (P4, 2026-10-10); nunca passa pelo HF.",
      "+    MIMIC = \"mimic-local\"",
      "     # Virtual union of all four datasets above",
      "     COMBINED = \"combined\"",
      "--- a/med_vlm/data/loader.py",
      "+++ b/med_vlm/data/loader.py",
      "@@ _HEAL_ARROW_PATH = {",
      "     \"test\": \"data/finetune_arrows/vqa_heal_test.arrow\",",
      " }",
      "+",
      "+# MIMIC (P4, 2026-10-10): mesmo formato M3AE; arrows em v7_mimic/data (sha256 em manifest_mimic_<split>.json).",
      "+_MIMIC_ARROW_PATH = {",
      f"+    \"train\": \"{man['train']['file']['path']}\",",
      f"+    \"validation\": \"{man['val']['file']['path']}\",",
      f"+    \"test\": \"{man['test']['file']['path']}\",",
      "+}",
      "@@ def load_dataset_by_enum(",
      "     if dataset_enum == med_vlm.enums.DatasetName.HEAL:",
      "         arrow_path = _HEAL_ARROW_PATH[split]",
      "         ...",
      "+    if dataset_enum == med_vlm.enums.DatasetName.MIMIC:",
      "+        arrow_path = _MIMIC_ARROW_PATH[split]",
      "+        ds = load_condition_dataset(arrow_path)",
      "+        cache_file_name = _kvasir_preprocess_cache_path(arrow_path, preprocessor)",
      "+        return _normalize(",
      "+            ds,",
      "+            preprocessor=preprocessor,",
      "+            answers_key=\"answers\",",
      "+            id_key=\"id\",",
      "+            cache_file_name=cache_file_name,",
      "+        )",
      "```",
      "No YAML: `dataset: MIMIC`. Na predição: `--dataset MIMIC --condition C0 --condition-arrow " + man['test']['file']['path'] + "` (sha256 acima).", "",
      "## MedGemma", "`google/medgemma-1.5-4b-it` baixado em `~/.cache/huggingface/hub/models--google--medgemma-1.5-4b-it` (snapshot 91850547d9f0b2fdd21aa7c5f4f3d1a8a52c243b, 8,1 GiB; `docs/downloads_medgemma.md`). Gemma3ForConditionalGeneration, bf16, SigLIP 896. Não registrado em lugar nenhum; a inferência zero-shot é do executor de GPU.", "",
      "## Fonte dos dados brutos (só leitura para o GPU)",
      "`doutorado/data/raw/mimic-cxr-jpg/2.1.0/files/p1x/p<subject>/s<study>/<dicom_id>.jpg` (só as 9 550 imagens do subconjunto; sha256 conferidos contra SHA256SUMS.txt, ver relatório final) e `doutorado/data/raw/medical-diff-vqa/1.0.1/` (tabelas + libs)."]
(V7 / "HANDOFF_GPU.md").write_text("\n".join(L) + "\n"); print("HANDOFF_GPU.md", len(L), "linhas")
