"""v7_mimic block A (2026-10-11): generates the 6 MIMIC parity YAMLs from the published HEAL YAMLs (placebo repo @2b7e731:
qwen2vl_dora_heal, smolvlm2_lora_heal, smolvlm2_dora_heal) and from the fine-tuned-encoder (tower) ones (v6_tower_heal/worktree: qwen2vl_dora_vt_heal, smolvlm2_lora_ft_heal,
smolvlm2_dora_ft_heal), by textual substitution (preserves the rest of the file), changing ONLY: dataset: MIMIC, run_name, wandb_run_name,
outputs_dir -> v7_mimic (+ results_json_dir), train.checkpoint_every 15000 + checkpoint_dir in tmp/v7 (same convention as the three YAMLs already
used on MIMIC on 10/10; the published one has 5000 -- only the frequency of the intermediate checkpoint changes, not the training). Checks via yaml.safe_load
that no other key differs from the source. Does not overwrite an existing YAML."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import hashlib, json, pathlib, re, sys, yaml
PL = pathlib.Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/doutorado/med-vqa-icdip-placebo/med_vlm/configs"); V6 = pathlib.Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v6_tower_heal/worktree/med_vlm/configs")
OUT = pathlib.Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic/configs"); OUT.mkdir(exist_ok=True)
SRC = {"qwen2vl_dora_mimic": (PL / "qwen2vl_dora_heal.yaml", "publicada: Qwen2-VL DoRA, torre congelada"), "smolvlm2_lora_mimic": (PL / "smolvlm2_lora_heal.yaml", "publicada: SmolVLM2 LoRA, regex padrao (adapta a torre)"),
       "smolvlm2_dora_mimic": (PL / "smolvlm2_dora_heal.yaml", "publicada: SmolVLM2 DoRA, regex padrao (adapta a torre)"), "qwen2vl_dora_vt_mimic": (V6 / "qwen2vl_dora_vt_heal.yaml", "torre: Qwen2-VL DoRA VT (LM + visual.blocks)"),
       "smolvlm2_lora_ft_mimic": (V6 / "smolvlm2_lora_ft_heal.yaml", "torre: SmolVLM2 LoRA FT (regex text_model.layers, torre congelada)"), "smolvlm2_dora_ft_mimic": (V6 / "smolvlm2_dora_ft_heal.yaml", "torre: SmolVLM2 DoRA FT (regex text_model.layers, torre congelada)")}
ALLOWED = {("run_name",), ("dataset",), ("logging", "wandb_run_name"), ("outputs_dir",), ("results_json_dir",), ("train", "checkpoint_every"), ("train", "checkpoint_dir")}
def flat(d, p=()):
    for k, v in d.items():
        if isinstance(v, dict): yield from flat(v, p + (k,))
        else: yield p + (k,), v
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
rep = {}
for name, (src, desc) in SRC.items():
    dst = OUT / (name + ".yaml")
    if dst.exists(): print("ja existe, nao sobrescrevo:", dst); continue
    t = src.read_text(); s = yaml.safe_load(t)
    t = re.sub(r"^run_name: .*$", "run_name: %s" % name, t, count=1, flags=re.M)
    t = re.sub(r"^dataset: HEAL\s*$", "dataset: MIMIC", t, count=1, flags=re.M)
    t = re.sub(r'^(\s*)wandb_run_name: .*$', r'\1wandb_run_name: "%s"' % name, t, count=1, flags=re.M)
    t = re.sub(r"^outputs_dir: .*$", "outputs_dir: $LAB_ROOT/v7_mimic\nresults_json_dir: $LAB_ROOT/v7_mimic/logs", t, count=1, flags=re.M)
    t = re.sub(r"^(\s*)checkpoint_dir: .*\n", "", t, flags=re.M)
    t = re.sub(r"^(\s*)checkpoint_every: .*$", r"\1checkpoint_every: 15000\n\1checkpoint_dir: $LAB_ROOT/tmp/v7/checkpoints_mimic", t, count=1, flags=re.M)
    head = "# v7_mimic (2026-10-11): copia de %s (sha256 %s; %s), mudando so dataset: MIMIC, run_name/wandb_run_name, outputs_dir/results_json_dir e train.checkpoint_every 15000 + checkpoint_dir (convencao dos YAMLs do MIMIC de 10/10; publicado: 5000).\n" % (src, sha(src)[:16], desc)
    d = yaml.safe_load(t); a, b = dict(flat(s)), dict(flat(d)); diff = {k for k in set(a) | set(b) if a.get(k) != b.get(k)}
    assert diff <= ALLOWED, (name, diff - ALLOWED)
    assert d["dataset"] == "MIMIC" and d["run_name"] == name and d["logging"]["wandb_run_name"] == name and d["train"]["checkpoint_dir"].endswith("checkpoints_mimic"), name
    dst.write_text(head + t); rep[name] = {"source": str(src), "source_sha256": sha(src), "yaml_sha256": sha(dst), "changed_keys": sorted(".".join(k) for k in diff), "peft": d["peft"], "model": d["model"], "target_modules": d["peft_config"]["target_modules"], "compile": d["train"].get("compile")}
    print(name, "<-", src.name, "| chaves alteradas:", rep[name]["changed_keys"])
json.dump(rep, open(OUT / "configs_mimic_paridade.json", "w"), indent=1); print("FIM", len(rep))
