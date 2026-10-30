# Software, hardware and model snapshots

## Hardware and drivers (fine-tuning and inference)
- GPUs: NVIDIA RTX 5000 Ada Generation (32 GB), one job per GPU; CPU-only analysis.
- NVIDIA driver 580.178.04; torch 2.13.0 built for CUDA 13.0 (`torch.version.cuda = 13.0`).
- Python 3.13.15 for the VLM pipeline and the analysis; Python 3.8.20 for M3AE (torch 1.9.0+cu111, pytorch-lightning 1.3.2, transformers 4.6.0).

## Key libraries (VLM pipeline and analysis)
transformers 5.15.1, peft 0.20.0, accelerate 0.34.2, datasets 4.8.5, pyarrow 25.0.1, numpy 2.5.2, pandas 3.0.5, scipy 1.18.1,
matplotlib 3.11.1, pillow 12.3.0, scikit-learn 1.9.0 (question-only TF-IDF baseline). Full list: `pip-freeze-full.txt`; pinned subset: `requirements.txt`.

## Model weights (Hugging Face Hub), snapshot commit and SHA-256 of the weight shards
| model | Hub id | snapshot | weight shards (sha256) |
|---|---|---|---|
| Qwen2-VL-2B | Qwen/Qwen2-VL-2B-Instruct | 895c3a49bc3fa70a340399125c650a463535e71c | 994ac2b03f97de8bc647d0fe5eba2e4b632b3e28dc03574c29bdfc36cf47e1b9, 92540d8353c8d226a589a3b179bdb33851c970ee2cc2ac7ba035f79425e7b833 |
| SmolVLM2-2.2B | HuggingFaceTB/SmolVLM2-2.2B-Instruct | 482adb537c021c86670beed01cd58990d01e72e4 | 7c88a90e78f567460b2369a0369cc4dafbfda5607c9cb090b30fa4437b0282f2, cf3d0958a8240f71054a6812038f2a6bfbe2e5124573a3b363f6b120c9a52657 |
| MedGemma 1.5 4B (zero-shot) | google/medgemma-1.5-4b-it | 91850547d9f0b2fdd21aa7c5f4f3d1a8a52c243b | 5e4c75b0ef1fb009caee567ab244f9e354e915fda748d1b76179cc453a39b4b5, 958e39df78c35ddb812fbcb8b5e7f46e07f1b153c1589f2d3f0b41c3b0748d30 |
| Qwen2.5-VL 7B (zero-shot) | Qwen/Qwen2.5-VL-7B-Instruct | cc594898137f460bfe9f0759e9844b3ce807cfb5 | e97b877e47fde53a6c6e77aafb36e58e91ee9d95c4a3eeac6f1b5c0e6a1c986e, a9a300a43b4724eee2abe7c18ceb26768d0ab011eb0cad19d9bfd2476a24d024, 111223d173e00bbee81cba1216fad28668df3476706b7fd26f4d5b50f8b3a507, ef47f634fa57d46ee134edcc09f34085a47da1e16c12a2abe0d67118be6d72ed, 0c859795ad3a627a9b95bcb762e059d5b768a4a36fdd4affeff269d93fdecc67 |
| LLaVA-Med v1.5 7B (zero-shot) | chaoyinshe/llava-med-v1.5-mistral-7b-hf (HF-format conversion of microsoft/llava-med-v1.5-mistral-7b) | 627be53734c667cbb1669608dac747a4485a22d7 | 17de3525100fa468b7bffb0acbc4b67b8569610b9c09f515a9912d142924de61, 62a406583e36c94cdbb416a51925ff07d8fcb720eb5c9f78d7d3d4b3ba7f7b55, 85b39f21159f21f4fd97417c491efe7a1ee6080320a07091adb57f40667ff1b8, fb4a00008716c0774241b63a3d402fd7064e793781334988071a6ff1b5854d06 |
| MedVLThinker 7B (zero-shot) | UCSC-VLAA/MedVLThinker-7B-RL_PMC | 75ef8116d2f6664bcc4f850990a873999e7fbbf6 | c1290c4d146901ce9d67af8a80c0beed34b18a59adbd856e0b7c30e611a70dc8, a67018ee71fdfca6d5ffe0bf53f29e5a50338b78e6755d434c55cdc445582c7c, f1eddd40ba91356c8b64d846e31692174d427d178a2e7443a820a22d81a8111c, 397efede324ae685ee0f6a3aab21e6c05a4fbd8172209ebec18b82477191148a |
| M3AE (pretrained starting point) | m3ae.ckpt from the M3AE authors' release (see src/m3ae_patch/README.md) | -- | 469cf69b18cd75fbc3a010f202fb42c0cc074b34db75a0bfab442db982885442 |
| RoBERTa-base tokenizer/weights for M3AE | roberta-base (as distributed with M3AE) | -- | -- |

## Datasets (versions)
- Kvasir-VQA-x1: Hugging Face `SimulaMet/Kvasir-VQA-x1`, snapshot 61e41148c3214bc5140ad0ab4c28520a512e2a73 (train 143,594 question-answer pairs / 6,212 images; our image-disjoint re-split in `data/kvasir/split_image_ids.json`).
- Kvasir-SEG and Kvasir-Instrument: official releases at datasets.simula.no (polyp and instrument masks).
- HEAL-MedVQA (annotations: Hugging Face `MM-Hallu/HEAL-MedVQA`); images from VinDr-CXR 1.0.0 (PhysioNet, credentialed).
- Medical-Diff-VQA 1.0.1 (PhysioNet, credentialed); images from MIMIC-CXR-JPG 2.1.0 (PhysioNet, credentialed); regions from Chest ImaGenome 1.0.0 (PhysioNet, credentialed).
