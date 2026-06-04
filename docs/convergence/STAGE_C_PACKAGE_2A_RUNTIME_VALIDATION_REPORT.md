# Stage C Package 2A Runtime Validation Report

## Scope

This report captures the first full-run gate-evidence execution bundle for `read_file_exact_valid_rate`.

The package objective is evidence generation, not migration.

## Runtime Commands

Full canonical run A:

```bash
python scripts/eval_canonical_manifest.py \
  --manifest evals/canonical_eval_manifest_v1.json \
  --out-dir /tmp/stage_c_package2a_full_run_a
```

Full canonical run B:

```bash
python scripts/eval_canonical_manifest.py \
  --manifest evals/canonical_eval_manifest_v1.json \
  --out-dir /tmp/stage_c_package2a_full_run_b
```

Consumers on each run:

```bash
python scripts/stage_c_package1b_passive_governance_consumer.py --run-dir /tmp/stage_c_package2a_full_run_a
python scripts/stage_c_package1c_passive_reconciliation_surface.py --run-dir /tmp/stage_c_package2a_full_run_a
python scripts/stage_c_package1d_migration_readiness_assessment.py --run-dir /tmp/stage_c_package2a_full_run_a

python scripts/stage_c_package1b_passive_governance_consumer.py --run-dir /tmp/stage_c_package2a_full_run_b
python scripts/stage_c_package1c_passive_reconciliation_surface.py --run-dir /tmp/stage_c_package2a_full_run_b
python scripts/stage_c_package1d_migration_readiness_assessment.py --run-dir /tmp/stage_c_package2a_full_run_b
```

Bundle creation:

```bash
python scripts/stage_c_package2a_gate_evidence_bundle.py build \
  --run-dir /tmp/stage_c_package2a_full_run_a \
  --bundle-label run_a \
  --output-path manifests/reports/stage_c_package2a_read_file_exact_valid_gate_evidence_run_a.json

python scripts/stage_c_package2a_gate_evidence_bundle.py build \
  --run-dir /tmp/stage_c_package2a_full_run_b \
  --bundle-label run_b \
  --output-path manifests/reports/stage_c_package2a_read_file_exact_valid_gate_evidence_run_b.json

python scripts/stage_c_package2a_gate_evidence_bundle.py compare \
  --left-bundle-path manifests/reports/stage_c_package2a_read_file_exact_valid_gate_evidence_run_a.json \
  --right-bundle-path manifests/reports/stage_c_package2a_read_file_exact_valid_gate_evidence_run_b.json \
  --output-path manifests/reports/stage_c_package2a_read_file_exact_valid_gate_stability_assessment.json
```

## Frozen Manifest Identity

Manifest:

1. path: `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json`
2. sha256: `5c09163b90ed07d310ed5715cae301797cb2aee7917ec486f727f7f6a24150cf`
3. version: `v1`

Dataset row counts:

1. `heldout_validation`: `100`
2. `tool_holdout`: `40`
3. `no_call`: `20`
4. `adversarial`: `20`
5. `direct_answer`: `20`

Total rows:

1. `200`

## Full-Run Findings

### Run A

Focus-surface legacy value:

1. `rows = 27`
2. `count = 0`
3. `rate = 0.0`

Focus-surface reconciliation:

1. `aligned`
2. reason code: `direct_stage_c_rate_matches_legacy_rate`

Focus-surface readiness:

1. `migration-ready`

Guardrails:

1. all false
2. `guardrails_clear = true`

Package 1B snapshot:

1. row-fact records: `200`
2. tool-expected population: `140`
3. Family A missing-evidence rows: `134`
4. ownership conflicts: `0`

### Run B

Focus-surface legacy value:

1. `rows = 27`
2. `count = 0`
3. `rate = 0.0`

Focus-surface reconciliation:

1. `aligned`
2. reason code: `direct_stage_c_rate_matches_legacy_rate`

Focus-surface readiness:

1. `migration-ready`

Guardrails:

1. all false
2. `guardrails_clear = true`

Package 1B snapshot:

1. row-fact records: `200`
2. tool-expected population: `140`
3. Family A missing-evidence rows: `134`
4. ownership conflicts: `0`

## Cross-Run Stability Findings

Stable across runs:

1. manifest identity
2. runtime configuration
3. semantic summary digest
4. semantic row-fact digest
5. `comparison_rows.jsonl` raw hash
6. row-identity digest
7. read-file row-identity digest
8. Package 1B semantic snapshot
9. focus-surface reconciliation snapshot
10. focus-surface readiness snapshot
11. guardrail-clear status
12. legacy focus-surface value
13. readiness integrity checks

Raw hash equalities:

1. `comparison_rows.jsonl` -> equal
2. `stage_c_family_a_scorer_evidence_artifact.json` -> equal
3. `stage_c_governance_guardrails_artifact.json` -> equal
4. `summary.json` -> different
5. `stage_c_row_fact_metadata_artifact.json` -> different
6. `stage_c_runtime_contract_summary_artifact.json` -> different
7. Package 1B/1C/1D report files -> different

Expected causes of raw-hash drift:

1. `summary.json` embeds `generated_utc`
2. row-fact metadata embeds provenance extraction timestamps
3. runtime-contract summary embeds run-specific generation metadata
4. Package 1B/1C/1D outputs embed run-specific paths or path-derived references

## Focus Surface Conclusion

For `read_file_exact_valid_rate`:

1. reconciliation remained `aligned`
2. readiness remained `migration-ready`
3. integrity checks remained stable
4. guardrails remained clear
5. legacy surfaces remained unchanged in meaning across both full runs

## Dependency Inventory

Current threshold dependencies:

1. threshold profile metric path: `failure_profile.read_file_exact_valid.rate`
2. catastrophic rule: `read_file_exact_valid_rate_lt_0_40`
3. watch rule: `read_file_exact_valid_rate_lt_0_70`

Current detector dependency locations:

1. `scripts/post_eval_collapse_detector.py::_resolve_metric_from_catalog`
2. `scripts/post_eval_collapse_detector.py::_resolve_required_metrics`
3. `scripts/post_eval_collapse_detector.py::_run_detector`

This is inventory only.

No impact analysis was performed in Package 2A.

## Package 2A Recommendation

`read_file_exact_valid_rate` remains `gate-not-open`.

Reason:

1. Package 2A closes the full-run and repeated-full-run evidence gap;
2. it does not close the still-required detector/threshold impact review or rollback review gap defined by Package 1E.
