# Conditions evaluated per fine-tuned run

<!-- glossary:start -->

| condition suffix | content | used in the paper |
|---|---|---|
| `C0` | intact image | yes (image gain, raw drop) |
| `TXT` | no image (question only; no-image baseline run) | yes (image gain) |
| `T`, `P` | target / control occlusion, black fill | yes |
| `T_blur10`, `P_blur10` | target / control occlusion, blur sigma = 10 % of the image width | yes |
| `T_blur`, `P_blur` | target / control occlusion, blur sigma = 4 % of the median width (fixed) | yes (sensitivity analysis) |
| `SHAM_*` (Kvasir-VQA-x1), `SHAM_black`, `SHAM_blur10` (Medical-Diff-VQA) | occluder on images without the target | yes (occluder test) |
| `S`, `S_blur10` | everything outside the target occluded | supplementary (sufficiency) |
| `T_regmean`, `P_regmean` | region-mean fill | supplementary |
| `T1.5`, `P1.5`, `T2`, `P2` | enlarged occlusions | supplementary |
| `C1` | blank image | supplementary |

Per-item prediction file name: `<RUN>_<condition>.json`, where `<RUN>` = `<FAMILY>_<ADAPTER>[_VT|_FT]_<BENCH>_seed<s>` (see the README glossary for
`VT`/`FT`) or `M3AE_<BENCH>_seed<s>`; no-image baselines: `<FAMILY>_LORA_TXT_<BENCH>_seed<s>_TXT.json`, `<FAMILY>_DORA_TXT_...`,
`M3AE_TXT_...` (grey image; superseded) and `M3AE_SEMIMG_...` (image path removed; used by the paper).
<!-- glossary:end -->
