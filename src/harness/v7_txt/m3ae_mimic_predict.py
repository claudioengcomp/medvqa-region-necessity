"""v7_mimic A: M3AE prediction on the MIMIC test set (lapa): locates the Lightning best checkpoint in v7_mimic/<ck>/<run>/<version>/checkpoints/epoch=*.ckpt
(save_top_k=1, monitor val/the_metric, as in main.py) and runs m3ae_infer_v7.
Usage: m3ae_mimic_predict.py <seed> <output.json> [img|gray]
  img (default, identical to the 11/10 one): checkpoints in v7_mimic/m3ae, real data_root (v7_mimic/m3ae_arrows/data_root), condition C0.
  gray (13/10, text-only M3AE): checkpoints in v7_mimic/m3ae_txt, gray data_root (v7_mimic/m3ae_arrows_gray/data_root), condition TXT."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import glob, subprocess, sys
seed, out = sys.argv[1], sys.argv[2]; mode = sys.argv[3] if len(sys.argv) > 3 else "img"; assert mode in ("img", "gray"), mode
R = os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic"
ck, droot, cond, name, extra = (("m3ae", "/m3ae_arrows/data_root/", "C0", "M3AE_MIMIC_seed%s" % seed, "linha publicada do M3AE replicada no MIMIC (mesma receita das publicadas; vocab 82)") if mode == "img" else
                                ("m3ae_txt", "/m3ae_arrows_gray/data_root/", "TXT", "M3AE_TXT_MIMIC_seed%s" % seed, "M3AE so-texto no MIMIC: imagem cinza constante 384x384 RGB 128 no treino, validacao e teste (mesma receita; vocab 82)"))
cands = glob.glob("%s/%s/task_finetune_vqa_mimic-seed%s-from_*/*/checkpoints/epoch=*.ckpt" % (R, ck, seed))
if len(cands) != 1: print("esperado exatamente 1 checkpoint best, achei", cands); sys.exit(3)
cmd = [sys.executable, "-u", os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/worktree/harness/v7_txt/m3ae_infer_v7.py", "--name", name, "--checkpoint", cands[0], "--data-root", R + droot, "--dataset-key", "vqa_mimic", "--vqa-label-size", "82",
       "--dataset", "MIMIC", "--condition", cond, "--output", out, "--model-label", "M3AE", "--extra", extra + "; cost=" + R + "/logs/" + name + "_cost.json"]
print(" ".join(cmd), flush=True); sys.exit(subprocess.call(cmd))
