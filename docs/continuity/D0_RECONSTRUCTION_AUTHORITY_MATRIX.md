# D0 Reconstruction Authority Matrix

## Scope

This matrix governs Stage D0 reconstruction verification for the frozen `i3`, `H0`, `H1`, and `H2` surfaces.

It is planning-only.

- No reconstruction is executed here.
- No datasets are modified here.
- No training is launched here.
- No threshold, evaluator, or topology changes are authorized here.

## Authority Precedence

When artifacts disagree, use the highest-precedence source available and treat lower-precedence artifacts as stale, derived, or non-authoritative.

1. Canonical contracts and governance artifacts
2. Executed machine-readable source artifacts
3. Published comparison and bundle manifests
4. Narrative reports, journals, and continuity notes
5. Draft artifacts and unapproved local notes

If a lower tier conflicts with a higher tier, the higher tier wins and the conflict must be reported, not repaired by inference.

## Surface Matrix

| Reconstruction surface | Authoritative source(s) | Corroborators | Conflict rule |
|---|---|---|---|
| Control scaffold bytes and row identity | `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl`, `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl` | `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json`, `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_i3.run_manifest.json` | JSONL bytes win over summaries or prose. |
| H0 control comparator | `/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.json`, `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.run_manifest.json` | `/opt/ai-stack/assistant-training/docs/phase_i/H0_CHECKPOINT_REPORT.md`, `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h0_control_i3_micro_eval_20260611T103048Z/summary.json` | Final config and manifest win over checkpoint prose. Shared control bytes still come from `i3`. |
| H1 replacement surface | `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl`, `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_val.jsonl`, `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json` | `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/summary.json`, `/opt/ai-stack/assistant-training/evals/baselines/llama31/internal_reference_regimes/h1_diversity_patch_20260611T125835Z/package_manifest.json`, `/opt/ai-stack/assistant-training/docs/phase_ix/H1_EXCEPTION_CHECKPOINT_REPORT.md` | Train JSONL wins over summary if counts or row identity disagree. Package manifest wins over README prose. |
| H2 replacement surface | `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl`, `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_val.jsonl`, `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json` | `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h2_commitment_patch_eval_20260611T120228Z/summary.json`, `/opt/ai-stack/assistant-training/evals/baselines/llama31/internal_reference_regimes/h2_commitment_patch_20260611T120228Z/package_manifest.json`, `/opt/ai-stack/assistant-training/docs/phase_i/H2_CHECKPOINT_REPORT.md` | Train JSONL wins over summary if counts or row identity disagree. Package manifest wins over README prose. |
| Patch accounting surface | Variant summary JSON files and the corresponding train JSONL files | Published bundle manifests, checkpoint reports | Recompute counts from JSONL if summary prose disagrees. |
| Tool-family distribution surface | Variant summary JSON files and direct recomputation from train JSONL | Published bundle metric snapshots, checkpoint reports | Recomputed counts from JSONL win over prose or report summaries. |
| Config fidelity surface | Final config JSON files | Draft config files, execution-gate approval note, checkpoint reports | Final config JSON wins. Any unlisted delta is a failure. |
| Manifest fidelity surface | Final run manifest JSON files | Draft run-manifest files, execution-gate approval note, checkpoint reports | Final run manifest JSON wins. Any unlisted delta is a failure. |
| Eval-surface fidelity | `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json` and the executed eval bundles under `/opt/ai-stack/assistant-training/evals/runs/` | `comparison_rows.jsonl`, `summary.json`, `stage_c_*` artifacts, published bundle `package_manifest.json` files | The canonical eval manifest wins over summaries or prose if any mismatch appears. |
| Published baseline interpretation | Published bundle `package_manifest.json` files under `/opt/ai-stack/assistant-training/evals/baselines/llama31/` | README surfaces and project-wide comparison tables | Bundle manifest wins over README prose or directory naming. |
| Governance and closure state | `/opt/ai-stack/assistant-training/docs/phase_h/*`, `/opt/ai-stack/assistant-training/docs/phase_i/*`, `/opt/ai-stack/assistant-training/docs/current/status/TRAINING_RUN_HISTORY.md` | Continuity notes and journals | Governance docs win over continuity prose when execution authority is ambiguous. |

## Reconstruction Surfaces That Must Never Be Inferred

- row identity
- patch slot assignment
- patch accounting totals
- tool-family counts
- config promotion deltas
- run-manifest promotion deltas
- eval contract values
- bundle class or role
- missing evidence

If one of these is absent, record it as missing. Do not repair it by reconstruction.
