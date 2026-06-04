# Stage C Package 2A Implementation Summary

## Scope

Stage C Package 2A replaces bounded-sample evidence with the first reproducible full-run gate-evidence package for the nearest migration candidate:

1. `read_file_exact_valid_rate`

This is an evidence-generation slice.

It does not:

1. migrate detector authority;
2. migrate threshold authority;
3. alter comparability policy;
4. create replacement metrics;
5. open the migration gate.

## Delivered Artifacts

Implementation files:

1. `scripts/stage_c_package2a_gate_evidence_bundle.py`
2. `tests/test_stage_c_package2a_gate_evidence_bundle.py`

Tracked evidence artifacts:

1. [stage_c_package2a_read_file_exact_valid_gate_evidence_run_a.json](/opt/ai-stack/assistant-training/manifests/reports/stage_c_package2a_read_file_exact_valid_gate_evidence_run_a.json:1)
2. [stage_c_package2a_read_file_exact_valid_gate_evidence_run_b.json](/opt/ai-stack/assistant-training/manifests/reports/stage_c_package2a_read_file_exact_valid_gate_evidence_run_b.json:1)
3. [stage_c_package2a_read_file_exact_valid_gate_stability_assessment.json](/opt/ai-stack/assistant-training/manifests/reports/stage_c_package2a_read_file_exact_valid_gate_stability_assessment.json:1)

Documentation files:

1. `STAGE_C_PACKAGE_2A_IMPLEMENTATION_SUMMARY.md`
2. `STAGE_C_PACKAGE_2A_RUNTIME_VALIDATION_REPORT.md`
3. `STAGE_C_PACKAGE_2A_ACCEPTANCE_ASSESSMENT.md`

## What The Bundler Does

The Package 2A bundler is read-only.

Per run, it consumes:

1. `summary.json`
2. `comparison_rows.jsonl`
3. Stage C row-fact metadata
4. Stage C Family A scorer evidence
5. Stage C guardrail artifact
6. Stage C runtime-contract summary
7. Package 1B governance report
8. Package 1C reconciliation report
9. Package 1D readiness assessment

For the focus surface, it emits:

1. manifest identity
2. runtime configuration
3. raw artifact hashes
4. normalized semantic digests
5. row-identity snapshot
6. guardrail snapshot
7. legacy-surface snapshot
8. Package 1B snapshot
9. Package 1C reconciliation snapshot
10. Package 1D readiness snapshot
11. dependency inventory

## Why Raw Hashes And Normalized Digests Both Exist

Raw file hashes capture exact artifact reproducibility.

Normalized semantic digests capture stable meaning when expected run-specific fields differ, including:

1. `generated_utc` in `summary.json`
2. `extraction_timestamp_utc` in row-fact provenance
3. run-directory and artifact-path strings embedded in Package 1B/1C/1D outputs

This distinction is required because full-run gate evidence needs both:

1. byte-level preservation visibility;
2. semantic stability visibility.

## Dependency Inventory Scope

Package 2A inventories current consumers for `read_file_exact_valid_rate` only.

It records:

1. threshold-profile dependency:
   - metric path `failure_profile.read_file_exact_valid.rate`
   - catastrophic rule `read_file_exact_valid_rate_lt_0_40`
   - watch rule `read_file_exact_valid_rate_lt_0_70`
2. detector dependency locations:
   - `scripts/post_eval_collapse_detector.py::_resolve_metric_from_catalog`
   - `scripts/post_eval_collapse_detector.py::_resolve_required_metrics`
   - `scripts/post_eval_collapse_detector.py::_run_detector`

It does not perform detector-impact or threshold-impact assessment.

## Package 2A Determination

Package 2A provides the first full-run evidence bundle needed by Package 1E, but it does not satisfy all gate criteria by itself.

Current result:

1. `read_file_exact_valid_rate` remains `gate-not-open`

Reason:

1. full-run and repeated full-run evidence now exist;
2. but detector/threshold impact review and rollback review remain out of scope and absent.
