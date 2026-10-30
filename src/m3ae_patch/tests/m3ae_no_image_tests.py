"""No-image variant (22/10/2026): 1-epoch run + validation of the text-only M3AE on VQA-RAD split by image, seed 0, with the grey arrows (D1), same
recipe as the published text-only run (run_m3ae_txt.sh, redivgray mode). Variant: 'semimg' (worktree_m3ae_semimg, no_image=True) or 'cinza'
(worktree_m3ae, published code). Stops at the end of the epoch-0 validation (m3ae_memtest_site, M3AE_MEMTEST_UNTIL=val_epoch0), without saving a
checkpoint and without the test. Output: extra_runs/m3ae_semimg/ensaio/"""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import json, os, subprocess, sys, threading, time
var = sys.argv[1]; W = os.environ.get("LAB_ROOT", "LAB_ROOT") + ""; V = W + "/v7_txt"; OUT = V + "/extra_runs/m3ae_semimg/ensaio"; os.makedirs(OUT + "/ckpt", exist_ok=True)
WM = V + ("/worktree_m3ae_semimg" if var == "semimg" else "/worktree_m3ae"); H = V + "/worktree/harness/v7_txt"; dev = os.environ.get("CUDA_VISIBLE_DEVICES", "")
NAME = f"NO_IMAGE_TEST_{var}_VQARAD_REDIV_seed0"; MEMLOG = f"{OUT}/{NAME}_torch.jsonl"; open(MEMLOG, "w").close()
cmd = [sys.executable, "-u", "main.py", "with", "data_root=" + V + "/extra_runs/data/vqarad_rediv/data_root_cinza/", "num_gpus=1", "num_nodes=1", "task_finetune_vqa_vqa_rad", "per_gpu_batchsize=16",
       "clip16", "text_roberta", "image_size=384", "tokenizer=downloaded/roberta-base", "load_path=downloaded/pretrained/m3ae.ckpt", "seed=0", "vqa_label_size=498", 'train_transform_keys=["clip"]',
       "default_root_dir=" + OUT + "/ckpt/" + var, "log_dir=" + OUT + "/ckpt/" + var + "/result"] + (["no_image=True"] if var == "semimg" else [])
NV = W + "/nvidia-580.173.02/nvidia-smi" if "580.173.02" in open("/proc/driver/nvidia/version").read() else "nvidia-smi"
def tree(root):
    kids = {}
    for p in os.listdir("/proc"):
        if p.isdigit():
            try: kids.setdefault(int(open(f"/proc/{p}/stat").read().rsplit(")", 1)[1].split()[1]), []).append(int(p))
            except Exception: pass
    out, st = set(), [root]
    while st: x = st.pop(); out.add(x); st += kids.get(x, [])
    return out
rec = []; stop = threading.Event()
def poll(pid):
    while not stop.is_set():
        try:
            o = subprocess.run([NV, "--query-compute-apps=pid,used_memory", "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=20).stdout
            pids = tree(pid); rec.append(sum(int(y) for x, y in (l.split(",") for l in o.strip().splitlines() if "," in l) if int(x) in pids))
        except Exception: pass
        stop.wait(5)
env = dict(os.environ, WANDB_MODE="disabled", M3AE_MEMTEST_OUT=MEMLOG, M3AE_MEMTEST_UNTIL="val_epoch0", PYTHONPATH=H + "/m3ae_memtest_site")
print("[no_image_test]", time.strftime("%F %T"), NAME, "placa", dev, "\n" + " ".join(cmd), flush=True)
t0 = time.time(); pr = subprocess.Popen(cmd, cwd=WM, env=env); th = threading.Thread(target=poll, args=(pr.pid,), daemon=True); th.start(); rc = pr.wait(); stop.set(); th.join(10); dt = time.time() - t0
L = [json.loads(x) for x in open(MEMLOG) if x.strip()]; tr = [x for x in L if x["phase"] == "train"]; va = [x for x in L if x["phase"] == "val"]; fim = [x for x in L if x["phase"] == "fim"]
t_tr = (tr[-1]["t"] - tr[0]["t"]) / max(len(tr) - 1, 1) if len(tr) > 1 else None
res = {"variante": var, "codigo": WM, "rc": rc, "concluiu": bool(fim), "placa": dev, "tempo_total_s": round(dt), "lotes_treino": len(tr), "passos_otimizacao": fim[0]["global_step"] if fim else None,
       "segundos_por_lote_treino": round(t_tr, 4) if t_tr else None, "segundos_por_passo_otimizacao": round(t_tr * 4, 4) if t_tr else None, "lotes_val": len(va),
       "torch_max_allocated_mib": max((x["max_allocated_mib"] for x in L), default=None), "torch_max_reserved_mib": max((x["max_reserved_mib"] for x in L), default=None),
       "nvsmi_proc_max_mib": max(rec) if rec else None, "perda_inicio_fim": None, "cmd": cmd}
json.dump(res, open(f"{OUT}/{NAME}.json" if fim else f"{OUT}/{NAME}_INCOMPLETO.json", "w"), indent=1); print(json.dumps(res)[:600], flush=True); sys.exit(0 if fim else 1)
