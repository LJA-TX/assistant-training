# Stage C Package 2B Threshold Impact Review And Hazard Assessment

## Scope

This artifact covers:

1. threshold-impact review for `read_file_exact_valid_rate`;
2. legacy-versus-authoritative semantic comparison for the same surface;
3. migration hazards that remain relevant before any future authorization review.

This is assessment only.

## Conformance Targets

This review checks:

1. every active threshold rule using the surface is inventoried;
2. current legacy behavior is explicit;
3. authoritative Stage C semantics are compared against the legacy surface;
4. hazards are recorded without performing migration analysis or cutover planning.

## Findings

### 1. Active Threshold Rules

Current threshold profile:

- `manifests/reports/stage_b_v1_threshold_profile.json`

Active rules for `read_file_exact_valid_rate`:

| Rule ID | Classification | Metric Path | Comparator | Threshold | Current Legacy Behavior |
|---|---|---|---|---|---|
| `read_file_exact_valid_rate_lt_0_40` | catastrophic | `failure_profile.read_file_exact_valid.rate` | `lt` | `0.4` | Package 2A full runs produced `rate=0.0`, so the rule predicate is true |
| `read_file_exact_valid_rate_lt_0_70` | watch | `failure_profile.read_file_exact_valid.rate` | `lt` | `0.7` | Package 2A full runs produced `rate=0.0`, so the rule predicate is true |

Status precedence is:

1. `catastrophic_halt`
2. `halt_progression`
3. `watch`
4. `pass`

So on the current full-run legacy value, the catastrophic outcome dominates overall status.

### 2. Threshold Impact

Threshold dependence for this surface is direct:

1. the threshold profile names `read_file_exact_valid_rate` in both catastrophic and watch groups;
2. the detector does not synthesize or bridge this metric itself;
3. threshold behavior therefore depends on the legacy evaluator preserving:
   - path continuity,
   - numeric computability,
   - legacy denominator construction.

There is no baseline-delta rule for this surface.

That reduces one class of migration hazard relative to `direct_answer_substitution_count`, but it does not remove:

1. path-coupling risk;
2. semantic drift risk;
3. rollback requirements.

### 3. Legacy Versus Authoritative Source Semantics

| Dimension | Legacy Surface | Authoritative Stage C Surface |
|---|---|---|
| Source artifact | `summary.json` | `stage_c_row_fact_metadata_artifact.json` + `stage_c_family_a_scorer_evidence_artifact.json` |
| Construction site | `scripts/eval_canonical_manifest.py::_build_failure_profile` | `scripts/stage_c_package1c_passive_reconciliation_surface.py::_build_read_file_exact_valid_surface` consuming emitted Stage C artifacts |
| Ownership authority | legacy evaluator `failure_profile` | dataset metadata declares `read_file` eligibility; scorer emits `exact_valid`; evaluator/consumer aggregates only |
| Denominator source | `read_file_rows = tool_rows where expected_primary_tool_name == "read_file"` | `records[].membership_markers.family_b1_read_file_eligible == true` |
| Numerator source | exact-valid rows within the legacy `read_file_rows` slice | `sides.base.records[].exact_valid == true` joined by `row_id` over the authoritative read-file eligible set |
| Row identity dependency | implicit row list position inside current eval rows; not surfaced in the legacy metric | explicit `row_id` join required between row-fact and scorer-evidence artifacts |
| Split / row-set visibility | not carried inside the metric itself | explicit `split_id`, row identity, manifest row-set identity, and row ID list are preserved in Stage C artifacts |
| Package 2A full-run result | `rows=27`, `count=0`, `rate=0.0` | `rows=27`, `count=0`, `rate=0.0`, `missing_family_a_row_ids=[]` |

### 4. Semantic Comparison Determination

For the current frozen manifest and current authoritative artifacts:

1. Package 2A showed direct alignment in both repeated full runs;
2. Package 1C classified the surface as `aligned`;
3. Package 1D classified the surface as `migration-ready`;
4. the authoritative denominator and numerator are governed by declared ownership rather than legacy `failure_profile` construction.

This means:

1. current runtime evidence supports semantic alignment for this one surface;
2. legacy and authoritative ownership models are still not identical in structure;
3. detector and threshold consumers remain coupled to the legacy path until a future authorized migration slice.

### 5. Migration Hazards

#### 5.1 Detector Metric Resolution Assumption

Active detector code requires `failure_profile.read_file_exact_valid.rate` to exist as a numeric scalar. Any future migration that changes:

1. path name;
2. scalar availability;
3. numeric computability behavior;

would change detector resolution behavior immediately.

#### 5.2 Threshold Profile Path Assumption

The threshold profile is path-based and legacy-specific. It does not express:

1. authoritative artifact identity;
2. Family B1 ownership contract;
3. row-fact / scorer-evidence join requirements.

That means path continuity is still part of threshold behavior today.

#### 5.3 Legacy Versus Stage C Structural Mismatch

The legacy surface is a flat summary metric.

The authoritative surface depends on:

1. row-fact emission,
2. scorer-evidence emission,
3. `row_id` join integrity,
4. declared `read_file` eligibility.

Package 2A proved this structure is stable for the current frozen manifest, but any future migration review must keep the structural mismatch explicit.

#### 5.4 Noncomputable And Missing-Artifact Behavior

Current live detector behavior treats unresolved required metrics as noncomputable rule inputs.

For this surface, eventual migration review must preserve explicit behavior if:

1. Stage C row-fact artifacts are missing;
2. Family A scorer evidence is missing;
3. row IDs do not resolve cleanly;
4. authoritative read-file denominator cannot be formed.

Package 2B does not authorize how that preservation would be implemented; it only records that the hazard exists.

#### 5.5 Legacy Surface Stability Requirement

Package 1E requires legacy-surface stability before migration authorization.

Package 2A showed repeated full-run semantic stability for:

1. legacy focus-surface value;
2. reconciliation status;
3. readiness status;
4. row identity stability;
5. guardrail-clear status.

That closes the evidence gap for stability, but not the separate need to preserve rollback visibility.

#### 5.6 Rollback Requirement Remains Open

Package 1E explicitly requires a rollback-review record before any surface may become `gate-open`.

Package 2B does not satisfy that requirement.

### 6. Surface-Specific Effect If Source Were Eventually Migrated

If an eventual authorized migration preserved current Package 2A semantics exactly, the likely threshold effect for this focus surface would be unchanged because:

1. current authoritative and legacy values reconcile exactly;
2. this surface uses absolute thresholds only;
3. current repeated full-run evidence shows stable denominator, numerator, and row identity.

But Package 2B does not treat that as sufficient for gate opening because hazards remain around:

1. detector path assumptions;
2. threshold-profile path assumptions;
3. noncomputable handling for missing or partial authoritative inputs;
4. rollback evidence.

## Validation Results

Validation evidence used:

1. `manifests/reports/stage_b_v1_threshold_profile.json`
2. `scripts/eval_canonical_manifest.py`
3. `scripts/stage_c_package1c_passive_reconciliation_surface.py`
4. `scripts/stage_c_package1d_migration_readiness_assessment.py`
5. Package 2A full-run gate-evidence bundle and stability assessment

No additional runtime execution was required in Package 2B.

## Governance Concerns

1. Active threshold behavior still depends on a legacy scalar path rather than an authoritative Family B1 contract surface.
2. Current evidence shows alignment, but alignment alone does not satisfy rollback or future missing-artifact handling requirements.
3. The detector and threshold systems remain migration-disabled by current authority and must remain so after this review.

## Residual Ambiguities

1. Package 2B does not specify the future authoritative detector-input contract for this surface.
2. Package 2B does not define the rollback artifact format required by Package 1E.

## Determination

The threshold-impact review requirement from Package 1E is satisfied for `read_file_exact_valid_rate`.

The semantic comparison shows:

1. current repeated full-run alignment is strong;
2. active threshold dependence is explicit;
3. migration hazards are now enumerated rather than implicit.

Package 2B therefore closes the detector/threshold impact-review evidence gap for this focus surface.

It does not close the rollback-review gap.

## Boundary Confirmation

This review does not:

1. modify threshold rules;
2. modify threshold profile paths;
3. generate a replacement metric;
4. change detector rule evaluation;
5. authorize migration.
