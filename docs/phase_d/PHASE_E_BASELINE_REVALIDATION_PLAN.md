# Phase E Baseline Revalidation Plan

## Scope

This plan is executable by a future Codex thread with minimal ambiguity.
It prepares Phase E by revalidating the frozen canonical baseline before any new training or promotion work.

## Inputs

- [docs/goal_charter_v5a.md](../goal_charter_v5a.md)
- [docs/appendix_a_operational_execution_contract_v3a.md](../appendix_a_operational_execution_contract_v3a.md)
- [docs/metric_specification_v1a.md](../metric_specification_v1a.md)
- [docs/current/current_status.md](../current/current_status.md)
- [docs/continuity/project_state_continuity_v1.md](../continuity/project_state_continuity_v1.md)
- [manifests/runs/stage_b_llama31_8b_base_v1_i3.run_manifest.json](../../manifests/runs/stage_b_llama31_8b_base_v1_i3.run_manifest.json)
- [artifacts/stage_b_llama31_8b_base_v1_i3/training_summary.json](../../artifacts/stage_b_llama31_8b_base_v1_i3/training_summary.json)
- [evals/canonical_eval_manifest_v1.json](../../evals/canonical_eval_manifest_v1.json)
- [data/v1_0/dataset_v1_0_summary.json](../../data/v1_0/dataset_v1_0_summary.json)
- [data/v1_0/dataset_v1_0_leakage_report.json](../../data/v1_0/dataset_v1_0_leakage_report.json)

## Revalidation Target

- Canonical model path: `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base`
- Clean restart adapter: `stage_b_llama31_8b_base_v1_i3`
- Frozen eval manifest: `evals/canonical_eval_manifest_v1.json`

## Execution Plan

1. Confirm the repo is still on `main` and that the working tree contains no unexpected drift.
2. Reconfirm the canonical model and tokenizer path used by the frozen manifest.
3. Reconfirm the canonical eval manifest hashes, split hashes, decode defaults, and evaluation order.
4. Reconfirm the dataset manifest and leakage report hashes that anchor the clean restart baseline.
5. Revalidate the base model against the frozen manifest using the canonical evaluator.
6. Revalidate the `stage_b_llama31_8b_base_v1_i3` adapter against the same manifest and decode defaults.
7. Compare the adapter delta to the Appendix A minimum-promising gate:
   - exact JSON validity delta should improve by at least 10 percentage points
   - tool-name accuracy delta should improve by at least 5 percentage points
   - invalid JSON should decrease
   - wrapper leakage should not worsen by more than 5 percentage points
   - no-call correctness should not degrade by more than 10 percentage points
8. Capture summary.json and comparison_rows.jsonl for both base and adapter runs.
9. Record the resulting baseline judgment in the next thread before any new training is started.

## Canonical Invocation Shape

Use the same evaluator entrypoint for both baseline runs.

Base model:

```bash
python scripts/eval_canonical_manifest.py \
  --manifest evals/canonical_eval_manifest_v1.json \
  --model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base \
  --out-dir evals/runs/<new_baseline_run_name>
```

Clean restart adapter:

```bash
python scripts/eval_canonical_manifest.py \
  --manifest evals/canonical_eval_manifest_v1.json \
  --model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base \
  --adapter-dir artifacts/adapters/stage_b_llama31_8b_base_v1_i3 \
  --out-dir evals/runs/<new_i3_revalidation_run_name>
```

The future thread should keep the output directories separate so the base and adapter summaries are easy to compare.

## Required Artifacts

- Canonical eval summary for the base model
- Canonical eval summary for the i3 adapter
- Comparison rows for both runs
- A short note that confirms the manifest hash set used during revalidation
- A short note that confirms the clean restart baseline remained `stage_b_llama31_8b_base_v1_i3`

## Unresolved Blockers To Watch

- The clean restart adapter is not promotion-eligible under the Appendix A gate, so revalidation must not be confused with promotion.
- Later probe lineages exist, but they are not the canonical restart point.
- Any change to the eval manifest, scorer semantics, or model path would require a new evaluation generation.
- Any repo drift away from `main` should be resolved before revalidation starts.

## Definition Of Done

- The base model and the i3 adapter are both revalidated against the same frozen canonical manifest.
- The baseline artifact set is complete enough for a future training thread to proceed without guessing the authoritative starting point.
- The next thread can distinguish "baseline revalidated" from "promotion approved."

## Boundary Confirmation

This plan does not authorize training, metric changes, or evaluation redesign.
