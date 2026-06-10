# Training Readiness Assessment

## Scope

Assess readiness of the dataset pipeline, evaluation pipeline, and training pipeline.
Do not run training.

## Inputs

- [docs/goal_charter_v5a.md](../goal_charter_v5a.md)
- [docs/appendix_a_operational_execution_contract_v3a.md](../appendix_a_operational_execution_contract_v3a.md)
- [docs/metric_specification_v1a.md](../metric_specification_v1a.md)
- [evals/canonical_eval_manifest_v1.json](../../evals/canonical_eval_manifest_v1.json)
- [data/v1_0/dataset_v1_0_summary.json](../../data/v1_0/dataset_v1_0_summary.json)
- [data/v1_0/dataset_v1_0_leakage_report.json](../../data/v1_0/dataset_v1_0_leakage_report.json)
- [configs/lora/stage_b_llama31_8b_base_v1_i3.config.json](../../configs/lora/stage_b_llama31_8b_base_v1_i3.config.json)
- [manifests/runs/stage_b_llama31_8b_base_v1_i3.run_manifest.json](../../manifests/runs/stage_b_llama31_8b_base_v1_i3.run_manifest.json)
- [artifacts/stage_b_llama31_8b_base_v1_i3/training_summary.json](../../artifacts/stage_b_llama31_8b_base_v1_i3/training_summary.json)
- [evals/runs/canonical_eval_20260526T033138Z/summary.json](../../evals/runs/canonical_eval_20260526T033138Z/summary.json)
- [evals/runs/stage_b_v1_i10r_residual_nocall_probe_eval_20260528T165520Z/summary.json](../../evals/runs/stage_b_v1_i10r_residual_nocall_probe_eval_20260528T165520Z/summary.json)

## Readiness Criteria

| Criterion | Status | Basis |
|---|---|---|
| Dataset builder and manifesting | Ready with caveats | `scripts/build_dataset_v1.py` exists, the canonical v1 dataset summary is present, and the canonical mix matches the charter target proportions on paper. Caveat: the synthetic ratio is 0.55, which is above the preferred under-0.50 level, and the leakage report still records controlled overlap values that must remain interpreted carefully. |
| Evaluation contract and scorer integrity | Ready | The eval manifest is frozen, split hashes and decode defaults are pinned, the scorer path is versioned, and canonical eval run history exists for the base model and later adapter lineages. |
| Training script, preflight, and masking controls | Ready with caveats | `scripts/train_lora_sft.py`, `scripts/preflight_lora_run.py`, run manifests, masking audits, and adapter artifacts are present. Caveat: the clean restart baseline is operationally valid, but the baseline adapter is not promotion-eligible under Appendix A thresholds. |

## Determination

Training infrastructure readiness: ready with caveats.

The caveats are not missing infrastructure. They are baseline discipline and dataset-shape caveats:

- preserve the frozen eval manifest
- preserve assistant-only masking
- preserve fail-fast preflight behavior
- preserve the clean restart baseline lineage from `stage_b_llama31_8b_base_v1_i3`
- do not treat later probe gains as a replacement for baseline revalidation

## Required Controls

- Keep the canonical eval manifest frozen for baseline revalidation.
- Keep the base model path fixed at `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base`.
- Keep the clean restart adapter fixed at `stage_b_llama31_8b_base_v1_i3` until Phase E completes.
- Keep masking audits required for any serious run.
- Keep no-call behavior and wrapper-leakage checks part of the evaluation gate.

## Deferred Or Blocking Items

- No promotion-eligible checkpoint exists yet.
- Later probe lineages are informative, but they are not a clean substitute for the accepted restart baseline.
- No training should begin in this Phase D thread.

## Boundary Confirmation

This readiness assessment does not authorize out-of-scope execution, evaluation changes, or training launch.
