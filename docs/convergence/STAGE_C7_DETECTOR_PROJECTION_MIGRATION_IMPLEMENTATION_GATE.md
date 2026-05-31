# Stage C7 Detector Projection Migration Implementation Gate

## Scope

This artifact defines the Stage C7 migration-readiness gate for detector projection.

This is a gate and safety assessment slice. It does not perform authoritative detector migration, does not migrate threshold-profile behavior, and does not replace existing detector outputs.

## Authoritative Inputs

Reviewed inputs:

- `docs/convergence/STAGE_C0_EVALUATOR_IMPLEMENTATION_ENTRY_CONTRACT_LOCK.md`
- `docs/convergence/STAGE_C0_EVALUATOR_CONTRACT_LOCK_DETERMINATION.md`
- `docs/convergence/STAGE_C6_SCORING_REPORT_INTEGRATION_AND_DETECTOR_PROJECTION_PREPARATION.md`
- `docs/convergence/STAGE_C6_SCORING_REPORT_AND_PROJECTION_PREPARATION_CONFORMANCE_REPORT.md`
- `docs/convergence/STAGE_B_EVALUATOR_IMPLEMENTATION_READINESS_ASSESSMENT.md`
- `docs/convergence/STAGE_B_EVALUATOR_ARCHITECTURE_DISCOVERY_AND_GAP_ANALYSIS.md`
- `scripts/post_eval_collapse_detector.py`
- `manifests/reports/stage_b_v1_threshold_profile.json`
- `scripts/stage_c4_real_output_ingestion.py`
- `scripts/stage_c5_scoring_path_integration.py`
- `scripts/stage_c6_scoring_report_integration.py`
- `reports/stage_c6/reporting_artifacts/c6_detector_projection_preparation_artifact.json`
- `reports/stage_c6/reporting_artifacts/scoring/*`
- `manifests/runs/stage_b_llama31_8b_base_v1_i10r_*.run_manifest.json`

## WP19 - Existing Detector Surface Inventory

### 19.1 Detector and Threshold-Profile Surfaces

| Surface | Location | Notes |
|---|---|---|
| Detector runtime | `scripts/post_eval_collapse_detector.py` | Profile-driven rule engine over metric-path catalogs; scalar gate status output (`pass`, `watch`, `halt_progression`, `catastrophic_halt`). |
| Threshold profile | `manifests/reports/stage_b_v1_threshold_profile.json` | Declares metric catalog, rule groups, status precedence, and baseline policy. |
| Detector outputs | `collapse_watch_interpretation.json`, `gate_assessment.json` | Include rule-level evidence, noncomputable handling, profile digest, and gate decision fields. |

### 19.2 Existing Detector Inputs

Detector requires:

1. `--eval-summary` (required)
2. `--threshold-profile` (required)
3. `--baseline-summary` (optional input, but required at runtime for delta rules under `missing_baseline_policy=fail_fast`)
4. `--geometry-context` (optional)

Input assumptions in current detector:

- metrics are resolved by path from profile `metric_catalog` (single-value resolution, ambiguity rejected).
- required metric absence is treated as noncomputable.
- baseline absence for delta rules fails fast under current profile policy.

### 19.3 Threshold-Profile Dependencies

Metric catalog dependencies:

| Metric ID | Legacy dependency path(s) |
|---|---|
| `no_call_correctness_aggregate` | `metrics.aggregate.no_call_correctness` or candidate legacy alternatives |
| `no_call_correctness_adversarial` | `metrics.probes.no_call_adversarial.no_call_correctness` or legacy alternative |
| `wrapper_leakage_overall` | `metrics.aggregate.wrapper_leakage` or candidate legacy alternatives |
| `invalid_json_overall` | `metrics.aggregate.invalid_json` or candidate legacy alternatives |
| `read_file_exact_valid_rate` | `failure_profile.read_file_exact_valid.rate` |
| `read_file_symbol_name_exact_valid_rate` | `failure_profile.read_file_symbol_name_exact_valid.rate` |
| `no_anchor_exact_valid_share` | `failure_profile.anchor_exact_share.no_anchor_phrase` |
| `direct_answer_substitution_count` | `failure_profile.failure_categories_non_exact_tool_rows.direct_answer_substitution` |

Rule groups:

- hard invariants: 3
- catastrophic thresholds: 3
- tradeoff watch thresholds: 3
- delta-vs-baseline rules: 1 (`direct_answer_substitution_delta_gt_3`)

Status precedence:

1. `catastrophic_halt`
2. `halt_progression`
3. `watch`
4. `pass`

### 19.4 Legacy Metric/Profile Assumptions

Current detector assumptions that remain active:

1. policy metrics are scalar values addressable by legacy path catalogs.
2. noncomputable metric resolution is explicit and blocking by policy (`noncomputable_status=halt_progression`).
3. baseline deltas are allowed only when baseline metrics are resolvable.
4. detector decisions are downstream of already-emitted metrics (detector does not reconstruct row facts).

### 19.5 Current Consumers and Compatibility Constraints

Observed active report consumers and linkage surfaces:

- run manifests referencing detector outputs (4 files):
  - `manifests/runs/stage_b_llama31_8b_base_v1_i10r_counterbalanced_probe.run_manifest.json`
  - `manifests/runs/stage_b_llama31_8b_base_v1_i10r_microprobe.run_manifest.json`
  - `manifests/runs/stage_b_llama31_8b_base_v1_i10r_nocall_probe.run_manifest.json`
  - `manifests/runs/stage_b_llama31_8b_base_v1_i10r_residual_nocall_probe.run_manifest.json`
- governance/reporting artifacts that persist detector-output schema expectations (`threshold_profile_id`, digests, active rules, progression flags).

Compatibility constraints for migration gate:

1. existing detector output schema cannot be silently broken for manifest-linked consumers.
2. migration must preserve explicit noncomputable reporting behavior.
3. migration cannot remove profile identity/digest lineage without replacement lineage fields.

## WP20 - Projection Mapping Gate

### 20.1 Gate Requirement

C6 reporting/scoring surfaces must map to detector-projection surfaces while preserving:

- completeness axis,
- current-run computability axis,
- comparability axis,
- non-inference guardrails,
- denominator/provenance visibility,
- scoring evidence visibility,
- validation issue visibility.

### 20.2 C6 Surfaces Available For Mapping

Available projection-oriented sources:

- `c6_detector_projection_preparation_artifact.json`
- `c5_parse_tool_nocall_scoring_summary_artifact.json`
- `c5_wrapper_leakage_scoring_summary_artifact.json`
- `c4_aggregation_summary_from_outputs_artifact.json`
- `c4_state_axis_from_outputs_artifact.json`
- `c4_row_fact_metadata_artifact.json`
- `c6_validation_issue_summary_artifact.json`
- `c6_governance_guardrail_summary_artifact.json`

### 20.3 Metric Mapping Gate Matrix

| Legacy metric ID | Candidate Stage C source | Gate finding |
|---|---|---|
| `no_call_correctness_aggregate` | C5 no-call scoring counts (`no_call_correctness` pass/fail over scored rows) | derivable with bounded adapter math |
| `no_call_correctness_adversarial` | no authoritative Stage C adversarial subset projection currently emitted | blocked (subset marker contract missing) |
| `wrapper_leakage_overall` | C5 wrapper summary (`wrapper_or_prose_leakage_count`, `record_count`) | derivable with bounded adapter math |
| `invalid_json_overall` | C5 parse status counts | derivable with bounded adapter math |
| `read_file_exact_valid_rate` | C4 Family B1 concept summary (`Read-file aggregate`) | derivable when B1 real-output records are present |
| `read_file_symbol_name_exact_valid_rate` | C4 Family B1 concept summary (`Symbol-name governed sub-slice`) | derivable when B1 real-output records are present |
| `no_anchor_exact_valid_share` | closest C4 B2 concept is `No-anchor governed sub-slice` rate | blocked (semantic mismatch vs legacy share definition) |
| `direct_answer_substitution_count` | C4 Family A concept summary (`Direct-answer governed subtype` numerator) | derivable with bounded adapter extraction |

### 20.4 Axis, Evidence, and Guardrail Preservation Findings

Current C6 preparation is structurally aligned with C0 contract requirements:

- independent state axes are present per record (`completeness`, `current_run_computability`, `comparability`),
- noncomputability and comparison-block reasons are retained,
- provenance and denominator provenance are retained,
- scoring-dimension evidence and fail reasons are retained,
- guardrail status indicates no collapsed-state, inference, substitution, or reconstruction behavior in current preparation artifact.

### 20.5 Mapping Risk Findings

Blocking/critical risks for authoritative migration:

1. `no_call_correctness_adversarial` has no authoritative Stage C adversarial-slice mapping contract yet.
2. `no_anchor_exact_valid_share` legacy semantics are not equivalent to currently emitted B2 governed-rate surface.
3. delta-vs-baseline rule evaluation requires baseline metric compatibility and comparability gating not yet formalized for detector migration path.
4. current C4/C5/C6 sample real-output run is Family A-only; full multi-family metric mapping is not yet demonstrated on ingested outputs.

## WP21 - Migration Safety Gate

### 21.1 Gate Checklist

| Gate condition | Result | Notes |
|---|---|---|
| Existing detector surfaces fully inventoried | pass | Inputs/outputs/profile dependencies/consumers documented. |
| C6 preserves required state axes and evidence | pass | Projection prep artifact retains independent axes and evidence fields. |
| Non-inference guardrails remain explicit | pass | Guardrail artifact reports no reconstruction/inference behavior. |
| Full legacy metric mapping is semantically complete | fail | Two metric mappings are unresolved/blocked (`no_call_correctness_adversarial`, `no_anchor_exact_valid_share`). |
| Baseline delta rule path is migration-safe | fail | No authoritative baseline comparability gate for detector projection path yet. |
| Backward compatibility impact is bounded and testable | partial | Output-consumer inventory exists, but no migration adapter compatibility test suite exists yet. |

### 21.2 Safety-Gate Determination

Safety-gate classification: **partially ready**.

Authoritative detector projection migration status: **not authorized in Stage C7**.

Reason:

- Core projection structures are available and contract-aligned, but blocking semantic mappings and baseline-delta gating remain unresolved.

### 21.3 Blocking Issues

1. Missing authoritative adversarial no-call subset mapping contract.
2. No authoritative equivalence contract between legacy `no_anchor_exact_valid_share` and Stage C B2 emitted surfaces.
3. Baseline-delta comparability enforcement for detector projection path is not yet locked.
4. No explicit migration compatibility test harness for detector-output consumer schema continuity.

### 21.4 Smallest Safe Next Implementation Slice

Recommended smallest safe slice (bounded, non-authoritative):

1. add a non-authoritative projection adapter that computes only unambiguous metric mappings from Stage C artifacts and emits explicit `noncomputable` for unresolved mappings.
2. emit a migration-candidate detector input artifact with per-metric provenance, denominator, and state-axis references.
3. add compatibility tests that assert:
   - no state-axis collapse,
   - no inferred/adapted values for unresolved metrics,
   - baseline-delta rule remains blocked without explicit comparability approval,
   - detector-output schema continuity checks against existing consumer expectations.
4. keep `detector_migration_enabled=false` and `threshold_profile_migration_enabled=false` until blockers are closed.

## Determination

Stage C7 establishes the migration gate and blocks authoritative migration at current state. Project status is partially ready for bounded, non-authoritative adapter work only.
