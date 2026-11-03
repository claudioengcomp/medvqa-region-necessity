"""DoRA configurations of Qwen2.5-VL-7B (frozen, fine-tuned and no-image) for the three benchmarks, derived from the LoRA 7B YAMLs (read-only; sha
checked against their manifest_configs.json). Changes, the same as for the 2B DoRA no-image baselines: peft LORA -> DORA (the only recipe change);
run_name/wandb_run_name; outputs_dir/results_json_dir -> the task directory; checkpoint_every removed (no intermediate snapshot: final adapter only);
checkpoint_dir -> the task directory (unused without checkpoint_every; avoids writing into the source directory). Writes configs/ and logs/diff_configs_lora_dora_7b.txt."""
import difflib, hashlib, json, os
W = os.environ.get("LAB_ROOT", "LAB_ROOT") + ""; Q = f"{W}/v7_txt/extra_runs/qwen25vl7b"; T = f"{W}/v7_txt/extra_runs/q25_artigo1"
os.makedirs(f"{T}/configs", exist_ok=True); os.makedirs(f"{T}/logs", exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
MAN = json.load(open(f"{Q}/configs/manifest_configs.json")); EXP = {"vt_kvasir": "59c53d6d2544", "kvasir": "d88fb2b935ec", "txt_kvasir": "f7e952be51e2", "vt_heal": "d113be8a06af", "heal": "a9f3be2cd53c",
       "txt_heal": "6c96c62511a3", "vt_mimic": "30a955655859", "mimic": "132d933e0fa2", "txt_mimic": "24995807c327"}
out, reg = [], {}
for k, h in EXP.items():
    src = f"{Q}/configs/qwen25vl_lora_{k}.yaml"; assert sha(src).startswith(h), (src, sha(src))
    old = open(src).read().splitlines(); new = []; seen = set()
    for l in old:
        s = l.strip()
        if s.startswith("peft:"): assert s == "peft: LORA", s; l = l.replace("LORA", "DORA"); seen.add("peft")
        elif s.startswith("run_name:"): assert "qwen25vl_lora_" in l; l = l.replace("qwen25vl_lora_", "qwen25vl_dora_"); seen.add("run")
        elif s.startswith("wandb_run_name:"): assert "qwen25vl_lora_" in l; l = l.replace("qwen25vl_lora_", "qwen25vl_dora_"); seen.add("wandb")
        elif s.startswith("outputs_dir:"): l = f"outputs_dir: {T}"; seen.add("out")
        elif s.startswith("results_json_dir:"): l = f"results_json_dir: {T}/logs"; seen.add("res")
        elif s.startswith("checkpoint_every:"): seen.add("ckpt"); continue
        elif s.startswith("checkpoint_dir:"): l = l.split("checkpoint_dir:")[0] + f"checkpoint_dir: {T}/ckpt_int"; seen.add("ckdir")
        elif s.startswith("#"): seen.add("hdr"); continue   # the header of the source config is replaced by ours
        new.append(l)
    assert seen == {"peft", "run", "wandb", "out", "res", "ckpt", "ckdir", "hdr"}, (k, seen)
    new = [f"# Qwen2.5-VL-7B DoRA (27/10/2026): copy of {src} (sha256 {sha(src)[:16]}) with LoRA replaced by DoRA (peft), run names and output directories changed, and without checkpoint_every (final adapter only)."] + new
    dst = f"{T}/configs/qwen25vl_dora_{k}.yaml"; open(dst, "w").write("\n".join(new) + "\n"); reg[os.path.basename(dst)] = {"fonte": src, "fonte_sha256": sha(src), "sha256": sha(dst)}
    out.append("".join(difflib.unified_diff([x + "\n" for x in old], [x + "\n" for x in new], fromfile=src, tofile=dst, n=0)))
open(f"{T}/logs/diff_configs_lora_dora_7b.txt", "w").write("\n".join(out)); json.dump(reg, open(f"{T}/configs/manifest_configs_dora.json", "w"), indent=1); print("ok", len(out), "configs")
