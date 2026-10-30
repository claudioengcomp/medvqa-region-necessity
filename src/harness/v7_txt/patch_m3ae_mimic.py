"""v7_mimic A (2026-10-11): MIMIC support in the M3AE worktree (v7_txt/worktree_m3ae @14da377 + patch), by the same mechanism as
harness/patch_m3ae_heal.py: vqa_mimic_dataset.py and vqa_mimic_datamodule.py generated from the upstream VQA-RAD modules of the clone
(harness.patch_m3ae_kvasir.module_source, names changed to mimic/MIMIC);
imports in the __init__ files; "vqa_mimic" entry in _datamodules; named config task_finetune_vqa_mimic = copy of task_finetune_vqa_heal with
vqa_label_size 82 (v7_mimic's answer_vocab.json, no=0/yes=1). Idempotent; does not touch anything of HEAL/Kvasir/SLAKE."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from harness import patch_m3ae_kvasir as K
WM = pathlib.Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_txt/worktree_m3ae"); V = json.load(open(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic/data/answer_vocab.json")); assert len(V) == 82 and V["no"] == 0 and V["yes"] == 1
for sub in ("datasets", "datamodules"):
    dst = WM / "m3ae" / sub / ("vqa_mimic_%s.py" % sub[:-1])
    t = K.module_source(str(WM), sub[:-1], "mimic", "harness/v7_txt/patch_m3ae_mimic.py")
    if not dst.exists(): dst.write_text(t); print("criado", dst)
    else: assert dst.read_text() == t, "divergente: %s" % dst; print("ja existia igual", dst)
p = WM / "m3ae/datasets/__init__.py"; t = p.read_text(); line = "from .vqa_mimic_dataset import VQAMIMICDataset\n"
if line not in t: p.write_text(t.rstrip("\n") + "\n" + line); print("import dataset ok")
p = WM / "m3ae/datamodules/__init__.py"; t = p.read_text(); line = "from .vqa_mimic_datamodule import VQAMIMICDataModule\n"
if line not in t: t = t.replace("from .vqa_heal_datamodule import VQAHEALDataModule\n", "from .vqa_heal_datamodule import VQAHEALDataModule\n" + line, 1); assert line in t
if '"vqa_mimic": VQAMIMICDataModule,' not in t: t = t.replace('    "vqa_heal": VQAHEALDataModule,\n', '    "vqa_heal": VQAHEALDataModule,\n    "vqa_mimic": VQAMIMICDataModule,\n', 1); assert '"vqa_mimic"' in t
p.write_text(t); print("datamodules __init__ ok")
p = WM / "m3ae/config.py"; t = p.read_text()
if "def task_finetune_vqa_mimic" not in t:
    m = re.search(r"@ex\.named_config\ndef task_finetune_vqa_heal\(\):\n(?:    .*\n|\n)*?    vqa_label_size = 288\n", t); assert m, "bloco heal nao achado"
    blk = m.group(0).replace("heal", "mimic").replace("vqa_label_size = 288", "vqa_label_size = 82"); assert blk.count("mimic") >= 2
    t = t[:m.end()] + "\n\n# v7_mimic (2026-10-11): copia de task_finetune_vqa_heal com vqa_label_size 82 (answer_vocab.json do v7_mimic)\n" + blk + t[m.end():]; p.write_text(t); print("named config ok")
else: print("named config ja existia")
# data_root with links to the arrows (v7_mimic/data is read-only; nothing is copied)
DR = pathlib.Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic/m3ae_arrows/data_root"); DR.mkdir(parents=True, exist_ok=True)
for s in ("train", "val", "test"):
    l = DR / ("vqa_mimic_%s.arrow" % s); tgt = pathlib.Path(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic/data/vqa_mimic_%s.arrow" % s); assert tgt.exists()
    if not l.exists(): l.symlink_to(tgt)
    print(l, "->", l.resolve())
print("FIM patch m3ae mimic")
