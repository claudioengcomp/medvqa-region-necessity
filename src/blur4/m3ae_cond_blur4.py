"""Round 10 (lapa env): prediction of the published M3AE (HEAL or MIMIC) on a T_blur/P_blur arrow, with its own data_root in
v7_txt/extra_runs/blur4_r10/data/m3ae_root/<bench>_<cond> (test -> arrow of the condition; train/validation -> canonical ones, for the vocabulary only).
Same best checkpoint and same inference (m3ae_infer_v7.py) as m3ae_cond_extra_runs.py; only the condition recorded in the JSON changes.
Usage: m3ae_cond_blur4.py <heal|mimic> <seed> <arrow> <sha256> <cond> <output>"""
# released package: occurrences of the original absolute data root were replaced by the LAB_ROOT environment variable
import glob, os, subprocess, sys
bench, seed, arrow, sha, cond, out = sys.argv[1:7]; W = os.environ.get("LAB_ROOT", "LAB_ROOT") + ""
C = {"heal": (f"{W}/doutorado/M3AE/checkpoints/task_finetune_vqa_heal-seed{seed}-from_*/*/checkpoints/epoch=*.ckpt", f"{W}/doutorado/M3AE/data/finetune_arrows", "vqa_heal", 288, "HEAL"),
     "mimic": (f"{W}/v7_mimic/m3ae/task_finetune_vqa_mimic-seed{seed}-from_*/*/checkpoints/epoch=*.ckpt", f"{W}/v7_mimic/data", "vqa_mimic", 82, "MIMIC")}[bench]
cands = glob.glob(C[0])
if len(cands) != 1: print("esperado exatamente 1 checkpoint best, achei", cands); sys.exit(3)
dr = f"{W}/v7_txt/extra_runs/blur4_r10/data/m3ae_root/{bench}_{cond}"; os.makedirs(dr, exist_ok=True)
for name, tgt in ((f"{C[2]}_test.arrow", arrow), (f"{C[2]}_train.arrow", f"{C[1]}/{C[2]}_train.arrow"), (f"{C[2]}_val.arrow", f"{C[1]}/{C[2]}_val.arrow")):
    l = os.path.join(dr, name)
    if not os.path.islink(l): os.symlink(tgt, l)
    assert os.path.realpath(l) == os.path.realpath(tgt), (l, tgt)
cmd = [sys.executable, "-u", f"{W}/v7_txt/worktree/harness/v7_txt/m3ae_infer_v7.py", "--name", f"M3AE_{C[4]}_seed{seed}_{cond}", "--checkpoint", cands[0], "--data-root", dr + "/", "--dataset-key", C[2], "--vqa-label-size", str(C[3]),
       "--dataset", C[4], "--condition", cond, "--output", out, "--model-label", "M3AE", "--arrow-sha256", sha, "--extra", f"rodada 10 do artigo 1: blur 4 % ({cond}); arrow {arrow}"]
print(" ".join(cmd), flush=True); sys.exit(subprocess.call(cmd))
