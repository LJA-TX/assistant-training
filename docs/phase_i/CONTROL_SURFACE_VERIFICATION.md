# Phase I Control Surface Verification

## Scope

Verify the frozen surfaces required by the Phase H Mini execution package before any Phase I run is launched.

## Frozen Surfaces

| Surface | Evidence | Result |
|---|---|---|
| Canonical eval manifest | `evals/canonical_eval_manifest_v1.json` | Verified present and unchanged |
| Train script | `scripts/train_lora_sft.py` | Verified present and unchanged |
| Eval script | `scripts/eval_canonical_manifest.py` | Verified present and unchanged |
| Base model path | `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base` | Verified from the template config |
| Tokenizer / prompt-template mode | `tokenizer_chat_template` with `generic_roles_v1` fallback | Verified from the template config |
| Control train bytes | `data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl` | Verified present |
| Control val bytes | `data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl` | Verified present |
| Control config template | `configs/lora/stage_b_llama31_8b_base_v1_i10r_microprobe.config.json` | Verified present and used as the clone shape |

## Hash Snapshot

| File | SHA-256 |
|---|---|
| `evals/canonical_eval_manifest_v1.json` | `a5035f41e89764519df3079d8786392b8c6d21dd2da487d00748dd595ec3d9a0` |
| `scripts/train_lora_sft.py` | `faf6cd4b676e230c5d2797392bc2fca204752d012f3e80e71c0af4ced7288432` |
| `scripts/eval_canonical_manifest.py` | `08a5cec22a781193365bed85b709ceebef534846602004bbfa047f4e0b59d738` |
| `configs/lora/stage_b_llama31_8b_base_v1_i10r_microprobe.config.json` | `d84ccad264787f1660c0709e4078c616b16ea4edda155f71269395c5f1859806` |
| `data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl` | `c19dbab14d930c39b90f85de8f7bf820f1ac37035756a9ca5063f823369e3f9a` |
| `data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl` | `d1bde5c675e22a88df250ac91e13522bb4d9ff8685d86e3b885f6d8d106d661f` |

## Repository Status Snapshot

Current branch snapshot at verification time:

```text
## main...origin/main
?? configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.draft.json
?? configs/lora/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.config.draft.json
?? configs/lora/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.config.draft.json
?? data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json
?? data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl
?? data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_val.jsonl
?? data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json
?? data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl
?? data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_val.jsonl
?? data/v1_0/dataset_v1_0_phase_i_variant_build_report.json
?? docs/Phase_I_Work_packages.md
?? docs/phase_i/
?? manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.run_manifest.draft.json
?? manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.run_manifest.draft.json
?? manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.run_manifest.draft.json
?? scripts/build_phase_i_variants.py
```

## Conclusion

The frozen control surfaces are intact.
The current worktree contains the expected Phase I additions: dataset variants, validation summaries, draft configs, draft run manifests, the Phase I docs bundle, the Phase I builder, and the prompt-local Phase I work package file.
No control-surface drift was detected before dataset-variant construction.
