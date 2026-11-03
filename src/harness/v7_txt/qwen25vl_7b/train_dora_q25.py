"""Qwen2.5-VL-7B DoRA training wrapper (env circle; cwd = v7_txt/worktree): runs the same med_vlm.run_experiment as the LoRA 7B runs and
writes a marker JSON (the job's output for the scheduler) with the final adapter, its sha256 and the adapter parameters (copy of the DoRA no-image wrapper).
Usage: train_dora_q25.py <config.yaml> <seed> <run_name> <marker.json>"""
import hashlib, json, os, subprocess, sys, time
cfg, seed, run, marker = sys.argv[1:5]; T = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/extra_runs/q25_artigo1"; t0 = time.time()
rc = subprocess.call([sys.executable, "-u", "-m", "med_vlm.run_experiment", "--config", cfg, "--seed", seed])
ad = f"{T}/models/{run}_seed{seed}"; f = f"{ad}/adapter_model.safetensors"
if rc != 0 or not os.path.exists(f): print("treino falhou rc=%s; adaptador %s existe=%s" % (rc, f, os.path.exists(f)), flush=True); sys.exit(rc or 4)
h = hashlib.sha256(open(f, "rb").read()).hexdigest(); cfgj = json.load(open(f"{ad}/adapter_config.json"))
json.dump({"run": f"{run}_seed{seed}", "adapter_dir": ad, "adapter_sha256": h, "adapter_bytes": os.path.getsize(f), "use_dora": cfgj.get("use_dora"), "r": cfgj.get("r"), "lora_alpha": cfgj.get("lora_alpha"),
           "target_modules": cfgj.get("target_modules"), "config": cfg, "seed": int(seed), "wall_seconds": round(time.time() - t0, 1), "accuracy": None, "n": None}, open(marker, "w"), indent=1)
print("ok", ad, h[:16], flush=True)
