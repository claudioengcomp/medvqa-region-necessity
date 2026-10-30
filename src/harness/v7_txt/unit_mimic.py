"""3a CPU test (2026-10-10): load_dataset_by_enum(DatasetName.MIMIC, 'validation') and one batch through the Qwen2-VL collator with and without image."""
import os   # released package: the original absolute data root is read from the LAB_ROOT environment variable
import json, time, torch
from med_vlm.enums import DatasetName, ModelName
from med_vlm.data.loader import load_dataset_by_enum
from med_vlm.models.loader import load_model_bundle
from med_vlm.training.spec_registry import MODEL_SPECS
t0 = time.time(); ds = load_dataset_by_enum(DatasetName.MIMIC, "validation", preprocessor=None); print("validation", len(ds), ds.column_names, round(time.time() - t0), "s")
ex = [ds[i] for i in range(4)]; print([(e["id"], e["question"], e["answers"]) for e in ex]); print("image types", [type(e["image"]).__name__ for e in ex], [getattr(e["image"], "size", None) for e in ex])
b = load_model_bundle(ModelName.QWEN2VL); out = {"n_validation": len(ds), "ids": [e["id"] for e in ex]}
for no_image in (False, True):
    spec = MODEL_SPECS[ModelName.QWEN2VL](max_length=1024 if no_image else 8192, no_image=no_image); batch = spec.build_collator(b.processor)(ex)
    out["no_image=%s" % no_image] = {"keys": sorted(batch.keys()), "input_ids": list(batch["input_ids"].shape), "labels_nonmasked": int((batch["labels"] != -100).sum())}
    print("no_image", no_image, out["no_image=%s" % no_image])
ds2 = load_dataset_by_enum(DatasetName.MIMIC, "validation", preprocessor=None, drop_image=True); print("drop_image:", ds2[0]["image"], len(ds2))
json.dump(out, open(os.environ.get("LAB_ROOT", "LAB_ROOT") + "/v7_mimic/logs/unit_mimic_dataset.json", "w"), indent=1); print("ALL_OK")
