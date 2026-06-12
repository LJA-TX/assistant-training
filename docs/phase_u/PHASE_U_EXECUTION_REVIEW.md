# Phase U Execution Review

## Executive Summary

The controlled execution completed successfully from an operational standpoint.

Training ran on the 60-row Phase T schema-repair micro-patch, the frozen canonical evaluation contract completed, and contamination remained clean. The run did **not** recover tool-call capability. Exact JSON validity stayed at `0.0`, tool-name accuracy stayed at `0.0`, and argument accuracy stayed at `0.0`.

The experiment therefore preserves the safety gain but does not demonstrate schema-realization recovery.

## Promoted Assets

| Asset | Path | Notes |
|---|---|---|
| Promoted config | [configs/lora/stage_b_llama31_8b_base_v1_phase_u_schema_repair_micro_patch.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_u_schema_repair_micro_patch.config.json) | Controlled execution config |
| Promoted manifest | [manifests/runs/stage_b_llama31_8b_base_v1_phase_u_schema_repair_micro_patch.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_u_schema_repair_micro_patch.run_manifest.json) | Prepared-not-started run manifest |
| Patch train JSONL | [data/v1_2/dataset_v1_2_phase_t_schema_repair_patch_train.jsonl](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_t_schema_repair_patch_train.jsonl) | 60-row schema-repair treatment |
| Patch summary | [data/v1_2/dataset_v1_2_phase_t_schema_repair_patch_summary.json](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_t_schema_repair_patch_summary.json) | Composition and lineage summary |
| Patch leakage report | [data/v1_2/dataset_v1_2_phase_t_schema_repair_patch_leakage_report.json](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_t_schema_repair_patch_leakage_report.json) | Frozen split overlap audit |
| Patch readiness assessment | [data/v1_2/dataset_v1_2_phase_t_schema_repair_patch_readiness_assessment.json](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_t_schema_repair_patch_readiness_assessment.json) | Ready-for-execution marker |
| Training summary | [artifacts/stage_b_llama31_8b_base_v1_phase_u_schema_repair_micro_patch/training_summary.json](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_u_schema_repair_micro_patch/training_summary.json) | Runtime and exposure evidence |
| Canonical eval summary | [evals/runs/phase_u_schema_repair_micro_patch_eval_20260612T111945Z/summary.json](/opt/ai-stack/assistant-training/evals/runs/phase_u_schema_repair_micro_patch_eval_20260612T111945Z/summary.json) | Frozen evaluator output |
| Canonical comparison rows | [evals/runs/phase_u_schema_repair_micro_patch_eval_20260612T111945Z/comparison_rows.jsonl](/opt/ai-stack/assistant-training/evals/runs/phase_u_schema_repair_micro_patch_eval_20260612T111945Z/comparison_rows.jsonl) | Row-level evaluation evidence |
| Scorer evidence | [evals/runs/phase_u_schema_repair_micro_patch_eval_20260612T111945Z/stage_c_family_a_scorer_evidence_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_u_schema_repair_micro_patch_eval_20260612T111945Z/stage_c_family_a_scorer_evidence_artifact.json) | Frozen family-A evidence |
| Runtime contract summary | [evals/runs/phase_u_schema_repair_micro_patch_eval_20260612T111945Z/stage_c_runtime_contract_summary_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_u_schema_repair_micro_patch_eval_20260612T111945Z/stage_c_runtime_contract_summary_artifact.json) | Frozen runtime evidence |

## Validation Results

- `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_u_schema_repair_micro_patch.run_manifest.json`: PASS
- `git diff --check`: PASS
- Training run: completed
- Canonical evaluation: completed

## Training Summary

| Item | Value |
|---|---|
| Train rows | `60` |
| Val rows | `240` |
| Train runtime | `6.4985s` |
| Train loss | `2.0565669536590576` |
| Eval loss | `2.5757219791412354` |
| Train samples / second | `1.847` |
| Train steps / second | `0.154` |
| Row identity digest | `d5308e9fa27efa7a5189152029c0025efad1fb2144e4ea20d5e475bf3c97726a` |

The exposure drift audit reports exact match on all dimensions and the patch remains contamination-clean.

## Canonical Evaluation Summary

### Aggregate Adapter Metrics

| Metric | Candidate |
|---|---:|
| exact JSON validity | `0.0` |
| invalid JSON rate | `0.7` |
| tool-name accuracy | `0.0` |
| argument accuracy | `0.0` |
| wrapper leakage | `0.0` |
| no-call correctness | `1.0` |
| adversarial no-call correctness | `1.0` |

### Failure Profile

| Failure mode | Candidate count |
|---|---:|
| direct-answer substitution | `125` |
| scalar substitution | `0` |
| malformed partial JSON | `15` |
| near-canonical wrapper or envelope drift | `0` |

### Interpretation

The patch improved safety relative to Phase Q, but it did not recover tool-call capability.

The key signal is that the failure distribution moved away from wrapper drift and into direct-answer substitution. That means the patch did not teach a stable `tool_calls` envelope; it mostly caused the model to answer directly on tool prompts.

## Contamination Status

Contamination stayed clean.

- The Phase T patch reports zero overlap with all frozen eval splits.
- The run did not mutate the dataset.
- The frozen canonical evaluation contract remained unchanged.

## Readiness Determination

**Executed successfully, but not promotable.**

The run is a valid controlled experiment, but it does not show schema-realization recovery.

