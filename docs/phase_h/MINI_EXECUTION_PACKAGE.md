# Mini Execution Package

## Purpose

This package is the Phase H handoff for GPT-5.4-Mini.

The next agent should execute the designed proving experiment, not redesign it.

## Execution Mode

- bounded internal-first experiment only
- no external data
- no Dataset v1.1 implementation
- no eval or scoring changes
- no governance redesign

## Exact Execution Sequence

1. Read the Phase H bundle and create `docs/phase_i/PHASE_I_CODEX_JOURNAL.md`.
2. Confirm the control surfaces are frozen:
   - `evals/canonical_eval_manifest_v1.json`
   - `scripts/train_lora_sft.py`
   - `scripts/eval_canonical_manifest.py`
   - base model path
   - tokenizer / prompt-template mode
3. Create a fresh bounded control config and run manifest by cloning the `stage_b_llama31_8b_base_v1_i10r_microprobe` shape and replacing only:
   - run name
   - dataset paths
   - output paths
   - lineage notes
4. Use exact i3 recovery dataset bytes for the control:
   - `data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl`
   - `data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl`
5. Build the diversity patch dataset variant:
   - tool-positive slice only
   - bounded patch budget `80` to `120` rows
   - restore omitted or underrepresented internal tool families first
   - keep non-tool slices unchanged
   - keep total row counts unchanged
6. Build the commitment patch dataset variant:
   - tool-positive slice only
   - bounded patch budget `80` to `120` rows
   - use anchor-light / paraphrastic tool-expected rows over existing tool intents
   - keep tool-family breadth near control
   - keep non-tool slices unchanged
7. Prepare the schema patch dataset variant now but execute it only conditionally:
   - tool-positive slice only
   - bounded patch budget `80` to `120` rows
   - derive rows from Phase E `missing_tool_calls` and `payload_not_object` archetypes
   - keep non-tool slices unchanged
8. Prepare a methodology-only plan now but execute it only conditionally:
   - preferred: existing trainer-side geometry or exposure weighting on exact control dataset bytes
   - fallback: schedule-only extension to `0.35` epochs on exact control dataset bytes
9. For each dataset variant, generate a compact validation artifact that records:
   - row counts by category
   - tool counts
   - contamination overlap checks
   - bounded patch size used
   - frozen non-tool-slice confirmation
10. Train and evaluate `H0_control_i3_micro`.
11. Train and evaluate `H2_commitment_patch`.
12. Train and evaluate `H1_diversity_patch`.
13. Apply the Phase H decision gates.
14. Run `H3_schema_patch` only if the first-screen result requires it.
15. Run `H4_methodology_only` only if the first-screen result requires it.
16. Write the Phase I comparison bundle and recommendation.

## Required Validations

Before any training run:

1. `git status --short --branch`
2. verify frozen control files unchanged
3. row-count audit for each dataset variant
4. contamination overlap audit against heldout and tool-holdout
5. bounded patch-size audit
6. frozen non-tool-slice confirmation

After each training run:

1. training summary exists
2. masking audit exists
3. canonical eval summary exists
4. kill metrics evaluated immediately
5. run-level comparison versus `H0` updated

At experiment end:

1. final hypothesis decision recorded
2. final stop-rule outcome recorded
3. final recommendation recorded

## Expected Outputs

Mini should produce, at minimum:

### Under `docs/phase_i/`

- `PHASE_I_CODEX_JOURNAL.md`
- `CONTROL_SURFACE_VERIFICATION.md`
- `DATASET_VARIANT_VALIDATION.md`
- `RUN_COMPARISON_MATRIX.md`
- `BOTTLENECK_ATTRIBUTION_DECISION.md`
- `PHASE_I_COMPLETION_AND_NEXT_STEP_RECOMMENDATION.md`

### Under dataset/config/manifest locations

- new bounded dataset variants
- matching config files
- matching run manifests
- per-variant validation artifacts
- train summaries
- eval summaries

## Escalation Triggers

Escalate instead of improvising if any of the following occurs:

1. control surfaces drift from the declared frozen contract
2. bounded dataset variants cannot be created without redesign
3. methodology-only probe requires trainer changes beyond an existing supported surface
4. contamination overlap cannot be cleared
5. two runs trip kill metrics
6. results land in the inconclusive band after all allowed conditional runs

## Completion Criteria

Mini is finished when all of the following are true:

1. the control run and first-screen pair are complete,
2. any conditionally required follow-up run is complete,
3. the Phase H decision thresholds have been applied,
4. one of `A/B/C/D/E` or `inconclusive_external_first` is documented,
5. and the final recommendation is written without redesigning the experiment.

## Non-Negotiable Boundaries

Mini must not:

1. import external data,
2. create Dataset v1.1,
3. change evaluation semantics,
4. change scoring semantics,
5. silently add extra runs,
6. retry weak metric outcomes,
7. promote a checkpoint without explicit review.

## Sources Used

- `docs/Phase_H_Work_packages.md`
- `docs/phase_h/CANDIDATE_INTERVENTION_ANALYSIS.md`
- `docs/phase_h/EXPERIMENTAL_MATRIX.md`
- `docs/phase_h/SUCCESS_AND_FAILURE_CRITERIA.md`
- `docs/phase_h/STOP_RULES_AND_DECISION_GATES.md`
- `configs/lora/stage_b_llama31_8b_base_v1_i10r_microprobe.config.json`
- `scripts/train_lora_sft.py`
- `scripts/eval_canonical_manifest.py`
