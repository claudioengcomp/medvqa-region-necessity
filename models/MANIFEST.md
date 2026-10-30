# Model weights

Adapters (LoRA/DoRA, PEFT format: `adapter_model.safetensors` + `adapter_config.json`) and M3AE Lightning checkpoints of every run used by the paper. They are not in this repository (total 37.6 GiB); they are **available on request** from the authors until a public host is chosen. Each row gives the run directory and weight file in the authors' archive, the size and the SHA-256 of the weight file, so that a copy can be verified.

Base models (Hugging Face Hub, exact snapshots in `environment/VERSIONS.md`): Qwen/Qwen2-VL-2B-Instruct, HuggingFaceTB/SmolVLM2-2.2B-Instruct; M3AE pretrained checkpoint `m3ae.ckpt` from the authors of M3AE (see `src/m3ae_patch/README.md`).

| group | run | benchmark | file | bytes | sha256 |
|---|---|---|---|---|---|
| fine-tuned run (image) | QWEN2VL_LORA_KVASIR_seed0 | KVASIR | `qwen2vl_lora_kvasir_seed0/adapter_model.safetensors` | 17465792 | 5ed27639d67e7bd210ddece9418c3d34fafc3e268c7f7da06bdb62b95a89c793 |
| fine-tuned run (image) | SMOLVLM_LORA_KVASIR_seed0 | KVASIR | `smolvlm2_lora_kvasir_seed0/adapter_model.safetensors` | 37162792 | 5d82316e1af7e6a643d4bcec683018c68c57667cf6830764dbedf35f81474b1a |
| fine-tuned run (image) | QWEN2VL_LORA_VT_KVASIR_seed0 | KVASIR | `qwen2vl_lora_vt_kvasir_seed0/adapter_model.safetensors` | 33211608 | 0efbbb5ba5dafbef35e805a0363385704225c1263b790562ac69dfdab59ce4f4 |
| fine-tuned run (image) | SMOLVLM_LORA_FT_KVASIR_seed0 | KVASIR | `smolvlm2_lora_ft_kvasir_seed0/adapter_model.safetensors` | 25193648 | ad466add324294e2e8b6e4d004752aab99519555c0f591724e74aaba6c42ef20 |
| fine-tuned run (image) | QWEN2VL_DORA_KVASIR_seed0 | KVASIR | `qwen2vl_dora_kvasir_seed0/adapter_model.safetensors` | 17884336 | 7d2de8c9d405627bb69c07c3aebc949095c929f6462de2ad4f2d38d968b4d061 |
| fine-tuned run (image) | SMOLVLM_DORA_KVASIR_seed0 | KVASIR | `smolvlm2_dora_kvasir_seed0/adapter_model.safetensors` | 38349864 | 99f75336c7c9e5d706fda36b9b571764b1c9cf5cf02e5b1124fe24e8a5df2b8a |
| fine-tuned run (image) | QWEN2VL_DORA_VT_KVASIR_seed0 | KVASIR | `qwen2vl_dora_vt_kvasir_seed0/adapter_model.safetensors` | 34294424 | 77ede13faf69ca81c45fb5b456ff290347a2e14ec961c98b65bae03f4e05a1f0 |
| fine-tuned run (image) | SMOLVLM_DORA_FT_KVASIR_seed0 | KVASIR | `smolvlm2_dora_ft_kvasir_seed0/adapter_model.safetensors` | 25994464 | d0d67581002c5d1e1c29d3bfeaed151a1cec5ce29980224d455d1efbb3f14c8c |
| fine-tuned run (image) | M3AE_KVASIR_seed0 | KVASIR | `checkpoints/epoch=11-step=7175.ckpt` | 1391902021 | b5eb66842582ebfa828d81cb4cb5c3619a7a698e09fa4e91e30d34e3480758b1 |
| fine-tuned run (image) | QWEN2VL_LORA_KVASIR_seed1 | KVASIR | `qwen2vl_lora_kvasir_seed1/adapter_model.safetensors` | 17465792 | f768ae40ada16b55d394934c0f5b38655ad55354dd17deae253a1ad42d8c818c |
| fine-tuned run (image) | SMOLVLM_LORA_KVASIR_seed1 | KVASIR | `smolvlm2_lora_kvasir_seed1/adapter_model.safetensors` | 37162792 | 83b5c709c730966c615e2dd57fac45a5af480f2e6ec1b845593b49f438ef588a |
| fine-tuned run (image) | QWEN2VL_LORA_VT_KVASIR_seed1 | KVASIR | `qwen2vl_lora_vt_kvasir_seed1/adapter_model.safetensors` | 33211608 | f79a4269225bd1c6538fe76f60586674e2c05f92bc016ba7fd6b45ec7520991e |
| fine-tuned run (image) | SMOLVLM_LORA_FT_KVASIR_seed1 | KVASIR | `smolvlm2_lora_ft_kvasir_seed1/adapter_model.safetensors` | 25193648 | ba173a72eab9a7c94447990f03010b81c9df5f84880b9055edb3ad930d914ffc |
| fine-tuned run (image) | QWEN2VL_DORA_KVASIR_seed1 | KVASIR | `qwen2vl_dora_kvasir_seed1/adapter_model.safetensors` | 17884336 | ab7773ea953e55144858c322c7d96aeb2828e74931b514902a943d30c8c064ac |
| fine-tuned run (image) | SMOLVLM_DORA_KVASIR_seed1 | KVASIR | `smolvlm2_dora_kvasir_e6_seed1/adapter_model.safetensors` | 38349864 | 379e3ba638e5cf124d42f52406421c5f3357a9aedb74fd559427eff8b9d03423 |
| fine-tuned run (image) | QWEN2VL_DORA_VT_KVASIR_seed1 | KVASIR | `qwen2vl_dora_vt_kvasir_seed1/adapter_model.safetensors` | 34294424 | 1253090b5c3d5c10492b9a3b8580c568b9c9b0a9d45a104b62f65ea93c0bcf07 |
| fine-tuned run (image) | SMOLVLM_DORA_FT_KVASIR_seed1 | KVASIR | `smolvlm2_dora_ft_kvasir_seed1/adapter_model.safetensors` | 25994464 | f79aa5234c1b27bec3fbd5b5e7e34ef89e1db64b2708925085b10dccd6ea685e |
| fine-tuned run (image) | M3AE_KVASIR_seed1 | KVASIR | `checkpoints/epoch=7-step=4783.ckpt` | 1391902021 | 55b8104599d2c1d7baeee2fde78e27155b3dca2a8a0dd457fd39f3b9b239b8f9 |
| fine-tuned run (image) | QWEN2VL_LORA_KVASIR_seed2 | KVASIR | `qwen2vl_lora_kvasir_seed2/adapter_model.safetensors` | 17465792 | d46821999f09f8f903cbeba65db9a10e05d472fa4b97e23dc5090158e1e5125f |
| fine-tuned run (image) | SMOLVLM_LORA_KVASIR_seed2 | KVASIR | `smolvlm2_lora_kvasir_seed2/adapter_model.safetensors` | 37162792 | 1c389293f10a53bf0b9b3d1e54062babffc1dfd79866179585c63a05012285fd |
| fine-tuned run (image) | QWEN2VL_LORA_VT_KVASIR_seed2 | KVASIR | `qwen2vl_lora_vt_kvasir_seed2/adapter_model.safetensors` | 33211608 | 908841de9b45529fd90c053f5375ad03de113d5f3cdf1683fa7b1e66dc1ab7bf |
| fine-tuned run (image) | SMOLVLM_LORA_FT_KVASIR_seed2 | KVASIR | `smolvlm2_lora_ft_kvasir_seed2/adapter_model.safetensors` | 25193648 | 7d3b23dbc4e46d0b0bb06d5885fc81456de5f0973dff5139d5d8f6fc388fe0c2 |
| fine-tuned run (image) | QWEN2VL_DORA_KVASIR_seed2 | KVASIR | `qwen2vl_dora_kvasir_seed2/adapter_model.safetensors` | 17884336 | ca7a3d5a8a1b2da5059b69be414ba005977022bc7de3800243501835040193e2 |
| fine-tuned run (image) | SMOLVLM_DORA_KVASIR_seed2 | KVASIR | `smolvlm2_dora_kvasir_e6_seed2/adapter_model.safetensors` | 38349864 | fac37fdbdd07faaa481021d33978a4d5078630cb25926d10b27f4c03637701db |
| fine-tuned run (image) | QWEN2VL_DORA_VT_KVASIR_seed2 | KVASIR | `qwen2vl_dora_vt_kvasir_seed2/adapter_model.safetensors` | 34294424 | 1e2bf195f8bf92190e4a85d737031e30f85fd0cecd56e9e8c7b6e9dc75a83b9c |
| fine-tuned run (image) | SMOLVLM_DORA_FT_KVASIR_seed2 | KVASIR | `smolvlm2_dora_ft_kvasir_seed2/adapter_model.safetensors` | 25994464 | 35fd8cc00fa4e591bf633d610446f283dee0e3e3e52af4f642be94e57dbf391b |
| fine-tuned run (image) | M3AE_KVASIR_seed2 | KVASIR | `checkpoints/epoch=7-step=4783.ckpt` | 1391902021 | 7cab84c3363d4d6aa97056c456ff5ee60e0ea6dc3879c73b01530e46a18c3618 |
| fine-tuned run (image) | QWEN2VL_LORA_HEAL_seed0 | HEAL | `qwen2vl_lora_heal_seed0/adapter_model.safetensors` | 17465792 | f49efa043da66eb6f830f26cd802dd93303ff824ea005ce51f29ead897098c75 |
| fine-tuned run (image) | SMOLVLM_LORA_HEAL_seed0 | HEAL | `smolvlm2_lora_heal_seed0/adapter_model.safetensors` | 37162792 | 8fa7a70fc9e21dbc5758feb67979f5e4a4145c7fa02ee6b5e75dbfed3359fe53 |
| fine-tuned run (image) | QWEN2VL_LORA_VT_HEAL_seed0 | HEAL | `qwen2vl_lora_vt_heal_seed0/adapter_model.safetensors` | 33211608 | 975c31fc75b52d799626894dc26139fa15fbb6e233e47bbb23fad05a04ea5b72 |
| fine-tuned run (image) | SMOLVLM_LORA_FT_HEAL_seed0 | HEAL | `smolvlm2_lora_ft_heal_seed0/adapter_model.safetensors` | 25193648 | 11ce18f82bdeba9ff36dabfae84b81a1e6eb7b0cb9502471ea2ff12f52896ab6 |
| fine-tuned run (image) | QWEN2VL_DORA_HEAL_seed0 | HEAL | `qwen2vl_dora_heal_seed0/adapter_model.safetensors` | 17884336 | 981171bdc1f119fdc4f2b228e58986e092e87f7ca97346fc806277b06a6b4622 |
| fine-tuned run (image) | SMOLVLM_DORA_HEAL_seed0 | HEAL | `smolvlm2_dora_heal_seed0/adapter_model.safetensors` | 38349864 | 2c6037ce18137b2aa6bf334162f1a58a64dfa68970016eca08c3126f76ed8f48 |
| fine-tuned run (image) | QWEN2VL_DORA_VT_HEAL_seed0 | HEAL | `qwen2vl_dora_vt_heal_seed0/adapter_model.safetensors` | 34294424 | 6e464f395f41eec6cd98dce0e846ce80fcf6025be780d3ec0f36d967130bb578 |
| fine-tuned run (image) | SMOLVLM_DORA_FT_HEAL_seed0 | HEAL | `smolvlm2_dora_ft_heal_seed0/adapter_model.safetensors` | 25994464 | f1b35e37e71fddf91c9a02669e7b3e6a9c84a46912c2337e38c84a62ba354d7f |
| fine-tuned run (image) | M3AE_HEAL_seed0 | HEAL | `checkpoints/epoch=6-step=1616.ckpt` | 1390598661 | 04508f9b5d854b0d2d9b62fa5a8466c7d95b26d2c7f70e19e0e849e21b9e7835 |
| fine-tuned run (image) | QWEN2VL_LORA_HEAL_seed1 | HEAL | `qwen2vl_lora_heal_seed1/adapter_model.safetensors` | 17465792 | 310ae4ef3686b3b922757995a784a66f46e38dcab51b8b53bc67733dd48a41d1 |
| fine-tuned run (image) | SMOLVLM_LORA_HEAL_seed1 | HEAL | `smolvlm2_lora_heal_seed1/adapter_model.safetensors` | 37162792 | b4e3a7772780e9896795d71415c5fb91f9cf40f63ebf89626d36d00afd154a63 |
| fine-tuned run (image) | QWEN2VL_LORA_VT_HEAL_seed1 | HEAL | `qwen2vl_lora_vt_heal_seed1/adapter_model.safetensors` | 33211608 | b106aa87d9ea19dac6b4e426cb7f05805625a118500796ee50210940a1cc099d |
| fine-tuned run (image) | SMOLVLM_LORA_FT_HEAL_seed1 | HEAL | `smolvlm2_lora_ft_heal_seed1/adapter_model.safetensors` | 25193648 | fb5710a971a5b8af59ec130bdf86bc8bad310b2f4b2c6896c253d7cf31493615 |
| fine-tuned run (image) | QWEN2VL_DORA_HEAL_seed1 | HEAL | `qwen2vl_dora_heal_seed1/adapter_model.safetensors` | 17884336 | 72831c355b042d1f8cc9b88682a74763ccc030aac8c720142f7c711f5d7c934d |
| fine-tuned run (image) | SMOLVLM_DORA_HEAL_seed1 | HEAL | `smolvlm2_dora_heal_seed1/adapter_model.safetensors` | 38349864 | e5b77a4fa552152748f3c3f9207c97a6ebd753405663daa9f5a9802d7999d611 |
| fine-tuned run (image) | QWEN2VL_DORA_VT_HEAL_seed1 | HEAL | `qwen2vl_dora_vt_heal_seed1/adapter_model.safetensors` | 34294424 | b27a04f0c65cf1ea62b9ca05a4cf99c396e5df93b8ecc013723c296d89df3567 |
| fine-tuned run (image) | SMOLVLM_DORA_FT_HEAL_seed1 | HEAL | `smolvlm2_dora_ft_heal_seed1/adapter_model.safetensors` | 25994464 | 1bff962e21857fc75828570d0733375d8b736b63495c948b6d7d52fb6f3da559 |
| fine-tuned run (image) | M3AE_HEAL_seed1 | HEAL | `checkpoints/epoch=2-step=692.ckpt` | 1390598661 | 026ecb7427782721e95d26a8c0e6b2a6a2af99f605b256ec155edf2753ab0f4f |
| fine-tuned run (image) | QWEN2VL_LORA_HEAL_seed2 | HEAL | `qwen2vl_lora_heal_seed2/adapter_model.safetensors` | 17465792 | 866327abeeedebbd1f8fbe7a2ae610781c202ca374ea7647433815cbc47030fa |
| fine-tuned run (image) | SMOLVLM_LORA_HEAL_seed2 | HEAL | `smolvlm2_lora_heal_seed2/adapter_model.safetensors` | 37162792 | 41b68001c1b26db7a0586ca3eab49bb1dfedfbf8d9c97ac1fedda9bf9f87311c |
| fine-tuned run (image) | QWEN2VL_LORA_VT_HEAL_seed2 | HEAL | `qwen2vl_lora_vt_heal_seed2/adapter_model.safetensors` | 33211608 | 0e859ed321a29d9732456374d59c3404874981ea918461a3d534f697cafe21c4 |
| fine-tuned run (image) | SMOLVLM_LORA_FT_HEAL_seed2 | HEAL | `smolvlm2_lora_ft_heal_seed2/adapter_model.safetensors` | 25193648 | 1bda958fcd5b1a17c8554382855d6450bf7e2109c307d87441f61e52b8b29cdf |
| fine-tuned run (image) | QWEN2VL_DORA_HEAL_seed2 | HEAL | `qwen2vl_dora_heal_seed2_retrain20261003/adapter_model.safetensors` | 17884336 | 5b3d4c974dd507d61113955e503c4d95b9c61de59db2a62a1aee5e0dcf64c816 |
| fine-tuned run (image) | SMOLVLM_DORA_HEAL_seed2 | HEAL | `smolvlm2_dora_heal_seed2/adapter_model.safetensors` | 38349864 | dc08c26e804586995459317079c4a356ac63283f66e4c0fddc40b7d4ac2953e1 |
| fine-tuned run (image) | QWEN2VL_DORA_VT_HEAL_seed2 | HEAL | `qwen2vl_dora_vt_heal_seed2/adapter_model.safetensors` | 34294424 | 4da6fa4999bf07f44bc110b9f6d2b7375a8412bb9ea4641ebc7b6578ead29cdf |
| fine-tuned run (image) | SMOLVLM_DORA_FT_HEAL_seed2 | HEAL | `smolvlm2_dora_ft_heal_seed2/adapter_model.safetensors` | 25994464 | cdb5b770878e72aa493ac470c46535cde84b2c452d2b6dd1a143c292ab0b6266 |
| fine-tuned run (image) | M3AE_HEAL_seed2 | HEAL | `checkpoints/epoch=6-step=1616.ckpt` | 1390598661 | 91ddb991183c19d1c28942eb7cf3a1e7d015601650f0425158868802def698d3 |
| fine-tuned run (image) | QWEN2VL_LORA_FROZEN_MIMIC_seed0 | MIMIC | `qwen2vl_lora_mimic_seed0/adapter_model.safetensors` | 17465792 | 06591b5aea8a72ece49d8d7293fef80334ea50839fb1c1261597dc11a7ecc624 |
| fine-tuned run (image) | SMOLVLM_LORA_MIMIC_seed0 | MIMIC | `smolvlm2_lora_mimic_seed0/adapter_model.safetensors` | 37162792 | 86b4cae1e9f71087f74c7b0c437a4bccbf03d3f966b40336b3bbd9877bf5b3b9 |
| fine-tuned run (image) | QWEN2VL_LORA_VT_MIMIC_seed0 | MIMIC | `qwen2vl_lora_vt_mimic_seed0/adapter_model.safetensors` | 33211608 | 684928e1ca2538ecc8472165c19383c0cf4d18421f4b05fb2d2d87a3bb824981 |
| fine-tuned run (image) | SMOLVLM_LORA_FT_MIMIC_seed0 | MIMIC | `smolvlm2_lora_ft_mimic_seed0/adapter_model.safetensors` | 25193648 | fb0f7c36cfb7c24f132c1e2ef00db23d84014e4a5a6730f1f6d07f934b7fec4a |
| fine-tuned run (image) | QWEN2VL_DORA_MIMIC_seed0 | MIMIC | `qwen2vl_dora_mimic_seed0/adapter_model.safetensors` | 17884336 | 3f22e21f1dd4b08ba71096500667a57d1d70ef979330b2feec3b7e0b232269e0 |
| fine-tuned run (image) | SMOLVLM_DORA_MIMIC_seed0 | MIMIC | `smolvlm2_dora_mimic_seed0/adapter_model.safetensors` | 38349864 | f8459ce27de4fb0f0f50a9419b33f96f064c31d3abdefdcdae4390bd548bd587 |
| fine-tuned run (image) | QWEN2VL_DORA_VT_MIMIC_seed0 | MIMIC | `qwen2vl_dora_vt_mimic_seed0/adapter_model.safetensors` | 34294424 | 058549f626407937bca83fc8cbc918abcb4ccee777bf46b3175c0066109f95ea |
| fine-tuned run (image) | SMOLVLM_DORA_FT_MIMIC_seed0 | MIMIC | `smolvlm2_dora_ft_mimic_seed0/adapter_model.safetensors` | 25994464 | 57eee8fa761d11ba6bf309ea140cdb8c178238615cf85136258b6664149ccae1 |
| fine-tuned run (image) | M3AE_MIMIC_seed0 | MIMIC | `checkpoints/epoch=5-step=1409.ckpt` | 1389332293 | 2e0f766e823af03796deb25b5a26eaccfcb47733b7c0875b6937975134aa75fc |
| fine-tuned run (image) | QWEN2VL_LORA_FROZEN_MIMIC_seed1 | MIMIC | `qwen2vl_lora_mimic_seed1/adapter_model.safetensors` | 17465792 | ece25580011142c74433497ad8d4d2f6cc1bb4ac3f338b7355570efdaa1182e9 |
| fine-tuned run (image) | SMOLVLM_LORA_MIMIC_seed1 | MIMIC | `smolvlm2_lora_mimic_seed1/adapter_model.safetensors` | 37162792 | 3857d9a9a79574858c247d84b5a2903b600a5c21ecd6bc1ff3f4befca267ddf6 |
| fine-tuned run (image) | QWEN2VL_LORA_VT_MIMIC_seed1 | MIMIC | `qwen2vl_lora_vt_mimic_seed1/adapter_model.safetensors` | 33211608 | 99f03873e0678412c0bd3515da858949c6be30227ab8d54d19189f0126347939 |
| fine-tuned run (image) | SMOLVLM_LORA_FT_MIMIC_seed1 | MIMIC | `smolvlm2_lora_ft_mimic_seed1/adapter_model.safetensors` | 25193648 | b13c56f1be75a3ea3159a1ee949b8277559d2c4492e2b55aa5e8c653a3ded9d7 |
| fine-tuned run (image) | QWEN2VL_DORA_MIMIC_seed1 | MIMIC | `qwen2vl_dora_mimic_seed1/adapter_model.safetensors` | 17884336 | 3589b33bff2d5d38c64cc3a8e2224b8a445b7dbbb373ba2977f374413d365972 |
| fine-tuned run (image) | SMOLVLM_DORA_MIMIC_seed1 | MIMIC | `smolvlm2_dora_mimic_seed1/adapter_model.safetensors` | 38349864 | 4b79988b19acb37b1eccecddab59457d5cec406729ee44cea81e1a559dc84dc4 |
| fine-tuned run (image) | QWEN2VL_DORA_VT_MIMIC_seed1 | MIMIC | `qwen2vl_dora_vt_mimic_seed1/adapter_model.safetensors` | 34294424 | e96f3e6d15a81d2cfb84514d7734457d76894d6e0dce84e981dab6aba7b2236a |
| fine-tuned run (image) | SMOLVLM_DORA_FT_MIMIC_seed1 | MIMIC | `smolvlm2_dora_ft_mimic_seed1/adapter_model.safetensors` | 25994464 | f8c92c9b584ef346caee062d6329d93069ef61108f923bec9c4de5f10d3ca4f5 |
| fine-tuned run (image) | M3AE_MIMIC_seed1 | MIMIC | `checkpoints/epoch=5-step=1409.ckpt` | 1389332293 | c8c0857074f3d179d386aa75eaed087fbb0b1321dec159cb98bea2570da8bf1e |
| fine-tuned run (image) | QWEN2VL_LORA_FROZEN_MIMIC_seed2 | MIMIC | `qwen2vl_lora_mimic_seed2/adapter_model.safetensors` | 17465792 | eff26f493528837beee4d2969c0ab30ce16c72cf96d73d426a6fc63e1bae3c75 |
| fine-tuned run (image) | SMOLVLM_LORA_MIMIC_seed2 | MIMIC | `smolvlm2_lora_mimic_seed2/adapter_model.safetensors` | 37162792 | 978e16d88628b385d083cc20d0c070dcea77c7932b8cb251df21761746eb21cb |
| fine-tuned run (image) | QWEN2VL_LORA_VT_MIMIC_seed2 | MIMIC | `qwen2vl_lora_vt_mimic_seed2/adapter_model.safetensors` | 33211608 | 5edd7ce1580646650d88ff9fb599dc22738ec87480d1de71c1e88cb2c6beebfd |
| fine-tuned run (image) | SMOLVLM_LORA_FT_MIMIC_seed2 | MIMIC | `smolvlm2_lora_ft_mimic_seed2/adapter_model.safetensors` | 25193648 | c2dc45dd7e3009830f4f0eba291d16e27250c3d5ac2504663b1419c706856242 |
| fine-tuned run (image) | QWEN2VL_DORA_MIMIC_seed2 | MIMIC | `qwen2vl_dora_mimic_seed2/adapter_model.safetensors` | 17884336 | c3e14f1ee1ded971fcc0d5cc62fc8d8cd7eaf2b69687f5c709e63094822044ce |
| fine-tuned run (image) | SMOLVLM_DORA_MIMIC_seed2 | MIMIC | `smolvlm2_dora_mimic_seed2/adapter_model.safetensors` | 38349864 | b88bdf9b0f2cf2f3d340aeb3c4b4507113a83edda81655d1eb9809e67ebf354e |
| fine-tuned run (image) | QWEN2VL_DORA_VT_MIMIC_seed2 | MIMIC | `qwen2vl_dora_vt_mimic_seed2/adapter_model.safetensors` | 34294424 | 63d1884ca1ec3442bf37da8f5c9205d38b87a83dc88e4c4e15a07721fb9e9ec0 |
| fine-tuned run (image) | SMOLVLM_DORA_FT_MIMIC_seed2 | MIMIC | `smolvlm2_dora_ft_mimic_seed2/adapter_model.safetensors` | 25994464 | 57fb29eb1f657c0ec98516f389c0a0a131c33cb5775c6c549811dbbce2be2e35 |
| fine-tuned run (image) | M3AE_MIMIC_seed2 | MIMIC | `checkpoints/epoch=6-step=1644.ckpt` | 1389332293 | c04d20b490de4558fb651f2a82d00c6ead2054efd64ee583b6ee7ef95872dd11 |
| no-image baseline, LoRA | QWEN2VL_LORA_TXT_KVASIR_seed0 | KVASIR | `qwen2vl_lora_txt_kvasir_seed0/adapter_model.safetensors` | 17465792 | ac809593e7b3a161301f0a0f739c47ba99dcf5fda11161be84d466d83381a98f |
| no-image baseline, DoRA | QWEN2VL_DORA_TXT_KVASIR_seed0 | KVASIR | `qwen2vl_dora_txt_kvasir_seed0/adapter_model.safetensors` | 17884336 | 5f0ac30f5a0fc5eb9f4b17dc9cbda6a56c18dee8ae9fdb023c830f66f3dd2055 |
| no-image baseline, LoRA | SMOLVLM_LORA_TXT_KVASIR_seed0 | KVASIR | `smolvlm2_lora_txt_kvasir_seed0/adapter_model.safetensors` | 25193648 | cf39c00f68b3ed718add0fcaaac0ae4348cf64892f72a8fa7a0bb1df96a8afa3 |
| no-image baseline, DoRA | SMOLVLM_DORA_TXT_KVASIR_seed0 | KVASIR | `smolvlm2_dora_txt_kvasir_seed0/adapter_model.safetensors` | 25994464 | 5c26cad2705617db03741edc49108fa16dc44ae57110cf352d2aa6aab10dfa21 |
| no-image baseline, M3AE (grey image; superseded) | M3AE_TXT_KVASIR_seed0 | KVASIR | `checkpoints/epoch=4-step=2989.ckpt` | 1391902149 | 87d64f6fd6675d2e61a405b07bfc2f6c84e0bd7214b77a9e36774da22582069d |
| no-image baseline, M3AE (image path removed; used by the paper) | M3AE_SEMIMG_KVASIR_seed0 | KVASIR | `checkpoints/epoch=4-step=2989.ckpt` | 1391902277 | 3c78fd1e35632dd3568c720f294b1b78986fb9b0835716c3813bf52e84eab133 |
| no-image baseline, LoRA | QWEN2VL_LORA_TXT_KVASIR_seed1 | KVASIR | `qwen2vl_lora_txt_kvasir_seed1/adapter_model.safetensors` | 17465792 | 181e442f035045848ef9d615a8a4f8ae3c00d86b182ad422ecfb560205897d2b |
| no-image baseline, DoRA | QWEN2VL_DORA_TXT_KVASIR_seed1 | KVASIR | `qwen2vl_dora_txt_kvasir_seed1/adapter_model.safetensors` | 17884336 | 3f5a53edc4360890913a67d1251ee4fd641d7cae4073769a40547b6701d772d0 |
| no-image baseline, LoRA | SMOLVLM_LORA_TXT_KVASIR_seed1 | KVASIR | `smolvlm2_lora_txt_kvasir_seed1/adapter_model.safetensors` | 25193648 | 8d220b3c9e23b4bbc2696d1f850f445188fb037bb01f9da6623265c39ab792f2 |
| no-image baseline, DoRA | SMOLVLM_DORA_TXT_KVASIR_seed1 | KVASIR | `smolvlm2_dora_txt_kvasir_seed1/adapter_model.safetensors` | 25994464 | ec02b4e8742e1425bd6a27db10bfba882586dc19a7404264138ab7f552a5268c |
| no-image baseline, M3AE (grey image; superseded) | M3AE_TXT_KVASIR_seed1 | KVASIR | `checkpoints/epoch=0-step=597.ckpt` | 1391902149 | ffed437b5e6da6f92769d633dbb3720056f4fe0f4ecfa3b0cd4317b7ba6af9cd |
| no-image baseline, M3AE (image path removed; used by the paper) | M3AE_SEMIMG_KVASIR_seed1 | KVASIR | `checkpoints/epoch=4-step=2989.ckpt` | 1391902277 | dde505979c8aaf1f3bda09691ffd12fc21fc63ad32d030d6eb84862ef0219464 |
| no-image baseline, LoRA | QWEN2VL_LORA_TXT_KVASIR_seed2 | KVASIR | `qwen2vl_lora_txt_kvasir_seed2/adapter_model.safetensors` | 17465792 | 73217515c94cb4409355d7e13077be0403c30226f1f6a7a5ffc1524ecd4afa27 |
| no-image baseline, DoRA | QWEN2VL_DORA_TXT_KVASIR_seed2 | KVASIR | `qwen2vl_dora_txt_kvasir_seed2/adapter_model.safetensors` | 17884336 | 9a3f744c2aa4e3b0fd811a2d7ba13b9ccffb0f203fdd3abbc4196130aa4b56e0 |
| no-image baseline, LoRA | SMOLVLM_LORA_TXT_KVASIR_seed2 | KVASIR | `smolvlm2_lora_txt_kvasir_seed2/adapter_model.safetensors` | 25193648 | 163faca0c69166617f47e845cae22e1c47565f889fa0f6403536076fa2e583b2 |
| no-image baseline, DoRA | SMOLVLM_DORA_TXT_KVASIR_seed2 | KVASIR | `smolvlm2_dora_txt_kvasir_seed2/adapter_model.safetensors` | 25994464 | 30b326811167c3ae64e2907e3b26cad6fcd065128b736a8b5378aafc8119dad5 |
| no-image baseline, M3AE (grey image; superseded) | M3AE_TXT_KVASIR_seed2 | KVASIR | `checkpoints/epoch=6-step=4185.ckpt` | 1391902149 | 8385f696c4de9397da8f9f1a2b9642b2194122a60e022b72b76fce5ef7770dad |
| no-image baseline, M3AE (image path removed; used by the paper) | M3AE_SEMIMG_KVASIR_seed2 | KVASIR | `checkpoints/epoch=4-step=2989.ckpt` | 1391902277 | 589aba92b418dade394b663cee60d6d26585f31c2922c08f37d3ef633d381efe |
| no-image baseline, LoRA | QWEN2VL_LORA_TXT_HEAL_seed0 | HEAL | `qwen2vl_lora_txt_heal_seed0/adapter_model.safetensors` | 17465792 | da34c2ed53693b29cba5df5eec1643b95f99c7bc4748ecebb31a895284bab6a9 |
| no-image baseline, DoRA | QWEN2VL_DORA_TXT_HEAL_seed0 | HEAL | `qwen2vl_dora_txt_heal_seed0/adapter_model.safetensors` | 17884336 | 7e341bd13bfa2de7b69bcc085253db30498786b1c3b19c6b029da43315ce1dbd |
| no-image baseline, LoRA | SMOLVLM_LORA_TXT_HEAL_seed0 | HEAL | `smolvlm2_lora_txt_heal_seed0/adapter_model.safetensors` | 25193648 | 173f4792e9f3f26d6eeee434df2dee8c4224acafb4e489af4dc4efbd6042dcd9 |
| no-image baseline, DoRA | SMOLVLM_DORA_TXT_HEAL_seed0 | HEAL | `smolvlm2_dora_txt_heal_seed0/adapter_model.safetensors` | 25994464 | 9cf6a979183807af4e205444fb49240a39d9f6300d6963617d8bf74786938c4f |
| no-image baseline, M3AE (grey image; superseded) | M3AE_TXT_HEAL_seed0 | HEAL | `checkpoints/epoch=7-step=1847.ckpt` | 1390598789 | 079ea4525e99a7e1bfc0cc36f6dddf1cf669de64e7e3a1e27e5244b9db0582cc |
| no-image baseline, M3AE (image path removed; used by the paper) | M3AE_SEMIMG_HEAL_seed0 | HEAL | `checkpoints/epoch=5-step=1385.ckpt` | 1390598917 | 9edfdcdf4296da245ef7bfc5e7235a93ba116b1b4f8b8c38e17586906a7c7b4d |
| no-image baseline, LoRA | QWEN2VL_LORA_TXT_HEAL_seed1 | HEAL | `qwen2vl_lora_txt_heal_seed1/adapter_model.safetensors` | 17465792 | 05c1bd90a473574685403c0edb3bbc340c3f866868d9ac9d4543828cd897cb5c |
| no-image baseline, DoRA | QWEN2VL_DORA_TXT_HEAL_seed1 | HEAL | `qwen2vl_dora_txt_heal_seed1/adapter_model.safetensors` | 17884336 | 39ec3faf5ae04f612db015ed6d7207b457e8d019189235d681ebe0274ef6f003 |
| no-image baseline, LoRA | SMOLVLM_LORA_TXT_HEAL_seed1 | HEAL | `smolvlm2_lora_txt_heal_seed1/adapter_model.safetensors` | 25193648 | 27ec368c0971f33c3d85aec6aaa373cc79150cdc61e45deb09adc5bcc827f1d8 |
| no-image baseline, DoRA | SMOLVLM_DORA_TXT_HEAL_seed1 | HEAL | `smolvlm2_dora_txt_heal_seed1/adapter_model.safetensors` | 25994464 | 58ddd785e9c9225fac43af77a58488c6ede7312b140a832fcc4cbaa3df5b84db |
| no-image baseline, M3AE (grey image; superseded) | M3AE_TXT_HEAL_seed1 | HEAL | `checkpoints/epoch=7-step=1847.ckpt` | 1390598789 | a6ab5f57e48fd83517c3fce640a4746a4498318210674f2017ef555f40ee7f80 |
| no-image baseline, M3AE (image path removed; used by the paper) | M3AE_SEMIMG_HEAL_seed1 | HEAL | `checkpoints/epoch=8-step=2078.ckpt` | 1390598917 | 141462cd093120e21ef631e36b672a6d5ef2af6c9b3a83591af6096912e5ef7b |
| no-image baseline, LoRA | QWEN2VL_LORA_TXT_HEAL_seed2 | HEAL | `qwen2vl_lora_txt_heal_seed2/adapter_model.safetensors` | 17465792 | 3a49bb3301d7b85566e542ad18e62e022b2347991cd15aa8c6fba71a781bb467 |
| no-image baseline, DoRA | QWEN2VL_DORA_TXT_HEAL_seed2 | HEAL | `qwen2vl_dora_txt_heal_seed2/adapter_model.safetensors` | 17884336 | 97b26fce1f522e2c631b182a95356353907ffd31232fe5515aa3fea526bd3f2e |
| no-image baseline, LoRA | SMOLVLM_LORA_TXT_HEAL_seed2 | HEAL | `smolvlm2_lora_txt_heal_seed2/adapter_model.safetensors` | 25193648 | f0df253623cbb0024fe60e6a8f4fc852beb3082efc70e3cae0fe0464fa2f8f89 |
| no-image baseline, DoRA | SMOLVLM_DORA_TXT_HEAL_seed2 | HEAL | `smolvlm2_dora_txt_heal_seed2/adapter_model.safetensors` | 25994464 | 7a5bdfa7528e453ec7e851ad6f00b888b44fae0265d007cb88ed11fd6be95891 |
| no-image baseline, M3AE (grey image; superseded) | M3AE_TXT_HEAL_seed2 | HEAL | `checkpoints/epoch=8-step=2078.ckpt` | 1390598789 | 0c6087f81b039ecf75bef0d0959c4c112ed2461c884c980c3f2b416534d7d1e5 |
| no-image baseline, M3AE (image path removed; used by the paper) | M3AE_SEMIMG_HEAL_seed2 | HEAL | `checkpoints/epoch=10-step=2540.ckpt` | 1390598917 | 2a74a6600d47d532491c40f65bff1f4cb796e6d8fbd9df458f9c6fe025aef63a |
| no-image baseline, LoRA | QWEN2VL_LORA_TXT_MIMIC_seed0 | MIMIC | `qwen2vl_lora_txt_mimic_seed0/adapter_model.safetensors` | 17465792 | 59347389835bb5f95882bb25dd8034ad8514f93ea33e2e4de20982b48c317a5d |
| no-image baseline, DoRA | QWEN2VL_DORA_TXT_MIMIC_seed0 | MIMIC | `qwen2vl_dora_txt_mimic_seed0/adapter_model.safetensors` | 17884336 | 9ccf2cfb888bc7407d1dec68adad8f6c4fe0dad28b47b5548ce193afbfc0e344 |
| no-image baseline, LoRA | SMOLVLM_LORA_TXT_MIMIC_seed0 | MIMIC | `smolvlm2_lora_txt_mimic_seed0/adapter_model.safetensors` | 25193648 | f980d71abe95c0614f51352eb6d0922913651f29b8289fcc2a26df65b610b02e |
| no-image baseline, DoRA | SMOLVLM_DORA_TXT_MIMIC_seed0 | MIMIC | `smolvlm2_dora_txt_mimic_seed0/adapter_model.safetensors` | 25994464 | 798b22120e50fdf8569f21109c6be421e2faeca8ae4229a580bf4659d891e88d |
| no-image baseline, M3AE (grey image; superseded) | M3AE_TXT_MIMIC_seed0 | MIMIC | `checkpoints/epoch=6-step=1644.ckpt` | 1389332293 | 865d87f88537cfd065b4c358ae181aece56783aa2c94ca7b329db765a57abae2 |
| no-image baseline, M3AE (image path removed; used by the paper) | M3AE_SEMIMG_MIMIC_seed0 | MIMIC | `checkpoints/epoch=7-step=1879.ckpt` | 1389332421 | 1f4ab1a72b89c27730569533837f018724feb012440bd2a2dcda2ce1ba7a70cb |
| no-image baseline, LoRA | QWEN2VL_LORA_TXT_MIMIC_seed1 | MIMIC | `qwen2vl_lora_txt_mimic_seed1/adapter_model.safetensors` | 17465792 | 5cdffce739114c7fa86b0a39d310281f496494546f1d2c499de1baa0666ac7dd |
| no-image baseline, DoRA | QWEN2VL_DORA_TXT_MIMIC_seed1 | MIMIC | `qwen2vl_dora_txt_mimic_seed1/adapter_model.safetensors` | 17884336 | 8d091a6121b40cf047d3f79c6b25bb1837cd2a2ab938fbdbde5c61ab7ed9a21b |
| no-image baseline, LoRA | SMOLVLM_LORA_TXT_MIMIC_seed1 | MIMIC | `smolvlm2_lora_txt_mimic_seed1/adapter_model.safetensors` | 25193648 | fc3f86de7e5a146d9cbbd1c0efa17aa8c484d0e687be33209974cabb62d44a1f |
| no-image baseline, DoRA | SMOLVLM_DORA_TXT_MIMIC_seed1 | MIMIC | `smolvlm2_dora_txt_mimic_seed1/adapter_model.safetensors` | 25994464 | 37639fe956bdbf6132f8a1e8973ccf9d814412f0300e08dbf4391c9c5522090d |
| no-image baseline, M3AE (grey image; superseded) | M3AE_TXT_MIMIC_seed1 | MIMIC | `checkpoints/epoch=7-step=1879.ckpt` | 1389332293 | 24601363dce585efcb94a8849868c3f58ba3c5ad9aea849fc98aa0dca4c308c1 |
| no-image baseline, M3AE (image path removed; used by the paper) | M3AE_SEMIMG_MIMIC_seed1 | MIMIC | `checkpoints/epoch=6-step=1644.ckpt` | 1389332421 | b44a3990080cfa921e107e34937bc180930da886f716d5878a8c6a5ab7f3ffa6 |
| no-image baseline, LoRA | QWEN2VL_LORA_TXT_MIMIC_seed2 | MIMIC | `qwen2vl_lora_txt_mimic_seed2/adapter_model.safetensors` | 17465792 | 64619d49d66977cb0eb1c851a05bd2aaa0a74060420e2766a018160d00a117be |
| no-image baseline, DoRA | QWEN2VL_DORA_TXT_MIMIC_seed2 | MIMIC | `qwen2vl_dora_txt_mimic_seed2/adapter_model.safetensors` | 17884336 | 2a98ea009628c710889fcc295afb868bcd5645b9706aa2b4e2d85df627fbf598 |
| no-image baseline, LoRA | SMOLVLM_LORA_TXT_MIMIC_seed2 | MIMIC | `smolvlm2_lora_txt_mimic_seed2/adapter_model.safetensors` | 25193648 | 9529982ed04d33c716dc94f9d765071947294beba25795c4483a675558852f72 |
| no-image baseline, DoRA | SMOLVLM_DORA_TXT_MIMIC_seed2 | MIMIC | `smolvlm2_dora_txt_mimic_seed2/adapter_model.safetensors` | 25994464 | 7e1eca919b4d78ea5ccb9c5ecea851b48fa38d5b5eff707ff5b4c719a29b9d69 |
| no-image baseline, M3AE (grey image; superseded) | M3AE_TXT_MIMIC_seed2 | MIMIC | `checkpoints/epoch=13-step=3289.ckpt` | 1389332293 | e77dae3670166bf02d726a7de224a3cf4e59c720bebbd352d9408beb70cdd9ba |
| no-image baseline, M3AE (image path removed; used by the paper) | M3AE_SEMIMG_MIMIC_seed2 | MIMIC | `checkpoints/epoch=7-step=1879.ckpt` | 1389332421 | c369c5363e750a16cbd4001950ff3d409eb1ff79aa83b44eb42972104f2fe9bb |

Rows: 135 (135 with a verified file; 0 missing at manifest time).
