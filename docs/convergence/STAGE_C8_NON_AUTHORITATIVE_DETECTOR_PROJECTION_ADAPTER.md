# Stage C8 Non-Authoritative Detector Projection Adapter

## Scope

This artifact records Stage C8 implementation of a non-authoritative detector projection adapter.

This slice validates projection behavior and detector-consumer compatibility without enabling detector migration.

## Authoritative Inputs

Implementation aligned to:

- Stage C7 migration gate artifacts
- Stage C6 reporting artifacts
- existing detector and threshold-profile artifacts
- Stage B doctrine artifacts
- Stage C0 contract-lock artifacts

## Implemented Artifacts

- `scripts/stage_c8_non_authoritative_detector_projection_adapter.py`
- `tests/test_stage_c8_non_authoritative_detector_projection_adapter.py`

## WP22: Projection Adapter

Implemented a bounded adapter that projects only C7-classified unambiguous metrics:

1. `no_call_correctness_aggregate`
2. `wrapper_leakage_overall`
3. `invalid_json_overall`
4. `read_file_exact_valid_rate`
5. `read_file_symbol_name_exact_valid_rate`
6. `direct_answer_substitution_count`

Adapter output remains explicitly non-authoritative:

- `authoritative_detector_output=false`
- `detector_migration_enabled=false`
- `threshold_profile_migration_enabled=false`

Adapter emits:

1. migration-candidate non-authoritative detector-input summary
2. non-authoritative baseline summary for compatibility-only delta-rule execution
3. per-metric mapping evidence and projection status

## WP23: Explicit Noncomputable Handling

Implemented explicit noncomputable emission with blocker reason codes and evidence for unresolved metrics:

1. `no_call_correctness_adversarial`:
   - `projection_status=noncomputable_blocked`
   - reason code: `blocked_adversarial_subset_mapping_unavailable`
2. `no_anchor_exact_valid_share`:
   - `projection_status=noncomputable_blocked`
   - reason code: `blocked_no_anchor_share_semantic_mismatch`

Implemented explicit noncomputable handling for unambiguous metrics when required source concepts are absent in the current run:

- `projection_status=noncomputable_missing_source`
- reason code: `source_family_concept_missing_in_current_run`

No unresolved metric is inferred, approximated, or substituted.

## WP24: Detector Consumer Compatibility Harness

Implemented compatibility harness checks for:

1. schema continuity against threshold-profile metric catalog coverage,
2. required field presence and metric-level evidence presence,
3. consumer readability via detector execution (`post_eval_collapse_detector._run_detector`) on projected summaries,
4. axis preservation from Stage C6 projection-preparation records,
5. evidence preservation and guardrail continuity.

Harness emits compatibility artifacts and detector output artifacts:

- compatibility collapse-watch output
- compatibility gate-assessment output
- compatibility check report with pass/fail status per check

## WP25: Projection Validation

Implemented validation checks for:

1. unambiguous mapping stability (`computed` or explicit source-missing noncomputable),
2. unresolved metrics remaining explicitly noncomputable with blocker reason codes,
3. no collapsed-state behavior,
4. no inference/substitution/reconstruction behavior,
5. migration flags remaining disabled,
6. compatibility harness pass/fail integration.

## Emitted Stage C8 Artifact Classes

The Stage C8 adapter emits:

1. `c8_projection_adapter_artifact.json`
2. `c8_projected_eval_summary_non_authoritative.json`
3. `c8_projected_baseline_summary_non_authoritative.json`
4. `c8_noncomputable_metric_artifact.json`
5. `c8_detector_consumer_compatibility_artifact.json`
6. `c8_projection_validation_artifact.json`
7. `c8_projection_adapter_summary.json`

Plus embedded Stage C6-on-demand reporting artifacts under the selected `artifacts_dir`.

## Boundary Confirmation

Not implemented in this slice:

1. authoritative detector migration,
2. threshold-profile migration,
3. detector output replacement in manifest-linked flows,
4. doctrine redesign,
5. catalog modification,
6. fixture authoring,
7. live model inference.

## Recommended Next Milestone

Recommended next milestone:

- Stage C9 bounded migration-prep follow-up for blocker closure:
  1. adversarial subset mapping contract closure,
  2. no-anchor share semantic equivalence/bridge contract,
  3. baseline-delta comparability gate contract for detector migration path.
