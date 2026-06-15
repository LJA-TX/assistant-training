# D0 Hash Authority Verification

## Purpose

This section defines how D0 treats published SHA-256 values.

For every published hash used by D0, the implementation must identify:

- the authoritative source artifact whose bytes are being hashed
- the published claim source that records the hash
- corroborating sources that echo the same hash
- the conflict rule if the values disagree

## Authority Rule

Hash authority follows the D0 precedence chain:

1. canonical contracts and governance artifacts
2. executed machine-readable source artifacts
3. published comparison and bundle manifests
4. narrative reports, journals, and continuity notes
5. draft artifacts and unapproved notes

The raw bytes of the authoritative source artifact are the ground truth for the computed hash.
The published claim source is the repository assertion about that value.

If the computed hash does not match the published claim, D0 fails closed.

## Conflict Handling

When hash claims disagree:

1. compute the raw-byte SHA-256 of the authoritative source artifact
2. compare that value to the published claim source
3. if the values differ, mark the artifact as uncertified and stop the affected surface family
4. if two published sources disagree, the higher-precedence source wins as the claim, but the discrepancy is still a failure
5. do not normalize, repair, or reinterpret bytes to make a hash match

## Registry

### Control and treatment datasets

| Hash label | Value | Authoritative source | Published claim source | Corroborating sources | Conflict handling |
|---|---|---|---|---|---|
| `i3_train_sha256` | `c19dbab14d930c39b90f85de8f7bf820f1ac37035756a9ca5063f823369e3f9a` | `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl` | `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json` | `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_i3.run_manifest.json`, `/opt/ai-stack/assistant-training/docs/phase_i/CONTROL_SURFACE_VERIFICATION.md` | Raw bytes must hash to the published value; any disagreement is fatal. |
| `i3_val_sha256` | `d1bde5c675e22a88df250ac91e13522bb4d9ff8685d86e3b885f6d8d106d661f` | `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl` | `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json` | `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_i3.run_manifest.json`, `/opt/ai-stack/assistant-training/docs/phase_i/CONTROL_SURFACE_VERIFICATION.md` | Raw bytes must hash to the published value; any disagreement is fatal. |
| `shared_control_val_sha256` | `d1bde5c675e22a88df250ac91e13522bb4d9ff8685d86e3b885f6d8d106d661f` | `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl` | `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json` | `H0`, `H1`, and `H2` config/manifest materials that explicitly reuse the control val bytes | Reuse of the control val hash is expected; any mismatch is fatal. |
| `H1_train_sha256` | `fb488f828b9ff42f2c067031ae4e7d65edecd791420c2d6daf79e27422e4e947` | `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl` | `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json` | `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.run_manifest.json`, `/opt/ai-stack/assistant-training/evals/baselines/llama31/internal_reference_regimes/h1_diversity_patch_20260611T125835Z/package_manifest.json`, `/opt/ai-stack/assistant-training/docs/phase_i/DATASET_VARIANT_VALIDATION.md` | Raw bytes must hash to the published value; any disagreement is fatal. |
| `H2_train_sha256` | `41834b7dd1b06bf90bfdb38b77c15f67a3dfdab802d164b0edddfcc686a75fd5` | `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl` | `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json` | `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.run_manifest.json`, `/opt/ai-stack/assistant-training/evals/baselines/llama31/internal_reference_regimes/h2_commitment_patch_20260611T120228Z/package_manifest.json`, `/opt/ai-stack/assistant-training/docs/phase_i/DATASET_VARIANT_VALIDATION.md` | Raw bytes must hash to the published value; any disagreement is fatal. |

### Eval contract and code hashes

| Hash label | Value | Authoritative source | Published claim source | Corroborating sources | Conflict handling |
|---|---|---|---|---|---|
| `dataset_manifest_sha256` | `86f68710d7257bb43793fb6a47245a232a3d390e55890604e8926676e6a2b4fd` | `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_summary.json` | `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json` | `/opt/ai-stack/assistant-training/manifests/reports/stage_c_package2a_read_file_exact_valid_gate_evidence_run_a.json`, `/opt/ai-stack/assistant-training/docs/phase_i/CONTROL_SURFACE_VERIFICATION.md` | If the summary bytes do not hash to the published value, eval-surface certification fails. |
| `canonical_eval_manifest_sha256` | `a5035f41e89764519df3079d8786392b8c6d21dd2da487d00748dd595ec3d9a0` | `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json` | `/opt/ai-stack/assistant-training/docs/phase_i/CONTROL_SURFACE_VERIFICATION.md` | `/opt/ai-stack/assistant-training/docs/phase_i/EXECUTION_GATE_APPROVAL.md`, `/opt/ai-stack/assistant-training/manifests/reports/stage_c_package2a_read_file_exact_valid_gate_evidence_run_a.json` | If the manifest bytes do not hash to the published value, eval-contract certification fails. |
| `scorer_sha256` | `08a5cec22a781193365bed85b709ceebef534846602004bbfa047f4e0b59d738` | `/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py` | `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json` | `/opt/ai-stack/assistant-training/docs/phase_i/CONTROL_SURFACE_VERIFICATION.md`, `/opt/ai-stack/assistant-training/docs/phase_e_remediation/REMEDIATION_RECOMMENDATION.md` | If the scorer bytes differ, evaluation contract certification fails. |
| `training_script_sha256` | `28900accae3d6abf05ddb9e86b41c03ad3c812a683f3af343bffa94281e14c8b` | `/opt/ai-stack/assistant-training/scripts/train_lora_sft.py` | `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json` | `/opt/ai-stack/assistant-training/docs/phase_i/CONTROL_SURFACE_VERIFICATION.md` | If the script bytes differ, training/eval code certification fails. |
| `dataset_builder_sha256` | `05843673f68fc8a492e889fb9e96e87dff09d189f5df220b092f233de82839d9` | `/opt/ai-stack/assistant-training/scripts/build_dataset_v1.py` | `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json` | `/opt/ai-stack/assistant-training/docs/phase_i/CONTROL_SURFACE_VERIFICATION.md` | If the builder bytes differ, source generation certification fails. |
| `metric_spec_sha256` | `793a884bbd783c3559828ab2cf84e4ceccc2aab256a80cf360c624dd8a549a3d` | `/opt/ai-stack/assistant-training/docs/metric_specification_v1a.md` | `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json` | `/opt/ai-stack/assistant-training/docs/phase_i/CONTROL_SURFACE_VERIFICATION.md` | If the metric spec bytes differ, eval-surface fidelity fails. |
| `microprobe_config_sha256` | `d84ccad264787f1660c0709e4078c616b16ea4edda155f71269395c5f1859806` | `/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_i10r_microprobe.config.json` | `/opt/ai-stack/assistant-training/docs/phase_i/CONTROL_SURFACE_VERIFICATION.md` | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_reproducibility_snapshot.json` | If the template config bytes differ, the control comparison surface is not reliable. |

### Evaluation split hashes

| Hash label | Value | Authoritative source | Published claim source | Corroborating sources | Conflict handling |
|---|---|---|---|---|---|
| `heldout_validation_sha256` | `78d47d4fb974f0f3245eaf81a17a847febc2667da5926bd372f625cd00b127a5` | `/opt/ai-stack/assistant-training/evals/data/canonical_v1/heldout_validation.jsonl` | `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json` | `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h0_control_i3_micro_eval_20260611T103048Z/summary.json`, `/opt/ai-stack/assistant-training/evals/baselines/llama31/canonical_baselines/base_original_20260526T0044Z/summary.json` | If the split bytes differ, the canonical eval contract is broken. |
| `tool_holdout_sha256` | `ca492290645cdf3e374bdd456b9488500c594b080180caae9b3b73fe288d0f45` | `/opt/ai-stack/assistant-training/evals/data/canonical_v1/tool_holdout.jsonl` | `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json` | `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h0_control_i3_micro_eval_20260611T103048Z/summary.json`, `/opt/ai-stack/assistant-training/evals/baselines/llama31/canonical_baselines/base_original_20260526T0044Z/summary.json` | If the split bytes differ, the canonical eval contract is broken. |
| `no_call_sha256` | `0584f529d86b8b319b2abaaa2410e504d614243f32a56a3a1eae44e8f8768fa7` | `/opt/ai-stack/assistant-training/evals/data/canonical_v1/no_call.jsonl` | `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json` | `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h0_control_i3_micro_eval_20260611T103048Z/summary.json`, `/opt/ai-stack/assistant-training/manifests/reports/stage_c_package2a_read_file_exact_valid_gate_evidence_run_a.json` | If the split bytes differ, the canonical eval contract is broken. |
| `adversarial_sha256` | `c500b8195722355b54dc7ddb612690daa9ef530ba4b030bcd04c7c2b2b50c5cc` | `/opt/ai-stack/assistant-training/evals/data/canonical_v1/adversarial.jsonl` | `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json` | `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h0_control_i3_micro_eval_20260611T103048Z/summary.json`, `/opt/ai-stack/assistant-training/manifests/reports/stage_c_package2a_read_file_exact_valid_gate_evidence_run_a.json` | If the split bytes differ, the canonical eval contract is broken. |
| `direct_answer_sha256` | `969d1d5dde3b17515c45c9a5f4b69beb1d908063f61ce470f778d625b1b1afbd` | `/opt/ai-stack/assistant-training/evals/data/canonical_v1/direct_answer.jsonl` | `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json` | `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h0_control_i3_micro_eval_20260611T103048Z/summary.json`, `/opt/ai-stack/assistant-training/manifests/reports/stage_c_package2a_read_file_exact_valid_gate_evidence_run_a.json` | If the split bytes differ, the canonical eval contract is broken. |

### Environment hashes

| Hash label | Value | Authoritative source | Published claim source | Corroborating sources | Conflict handling |
|---|---|---|---|---|---|
| `environment_snapshot_sha256` | `ae3f853694c2f940bf015772d4e639004f49eb4646f54395ad8a536d05f187d3` | `/opt/ai-stack/assistant-training/manifests/environment/canonical_env_snapshot_v1.json` | `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json` | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_reproducibility_snapshot.json` | If the environment snapshot differs, certification is not comparable. |
| `dependency_lock_sha256` | `e75c5cc0673060e154baf99ff12a85a6ad8d10bee3e2d54181f859c861493cf5` | `/opt/ai-stack/assistant-training/manifests/environment/pip_freeze_llama_venv_20260526.txt` | `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json` | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_reproducibility_snapshot.json` | If the dependency lock differs, comparability is broken and the run stops. |

## Not Certified By Published Hash Alone

The following surfaces are not certified by a single published hash claim:

- final `H0` config and manifest
- final `H1` config and manifest
- final `H2` config and manifest
- pairwise config diff certifications
- pairwise manifest diff certifications

Those surfaces are certified by field-level diff rules and authority precedence, not by a file hash alone.

## Current Blocking Status

No hash-authority gap is currently known to block D0 implementation.

If any authoritative source above cannot be located or its computed hash disagrees with the published claim, the future certification run must stop and emit a failure report.
