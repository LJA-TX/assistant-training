# Stage C Package 1C Runtime Validation Report

## Scope

This report records representative runtime validation for the first passive reconciliation surface between authoritative Stage C artifacts and legacy detector-facing outputs.

Validated scope:

1. real canonical evaluator execution;
2. passive reconciliation consumer execution;
3. authoritative-to-legacy surface resolution;
4. unchanged legacy outputs before and after reconciliation.

## Runtime Commands

Canonical evaluator run:

```bash
python scripts/eval_canonical_manifest.py \
  --manifest evals/canonical_eval_manifest_v1.json \
  --out-dir /tmp/stage_c_package1c_runtime_validation_run \
  --max-samples-per-split 3
```

Passive reconciliation consumer:

```bash
python scripts/stage_c_package1c_passive_reconciliation_surface.py \
  --run-dir /tmp/stage_c_package1c_runtime_validation_run
```

Both commands exited `0`.

## Runtime Output Directory

- `/tmp/stage_c_package1c_runtime_validation_run`

## Emitted Reconciliation Artifact

Confirmed present:

- `stage_c_package1c_passive_reconciliation_report.json`

## Surface Results

Observed status mix:

1. `aligned`: `1`
2. `requires_future_migration`: `2`
3. `not_comparable`: `1`

Per-surface results:

1. `read_file_exact_valid_rate`
   - status: `aligned`
   - authoritative value:
     - `rows = 2`
     - `count = 0`
     - `rate = 0.0`
   - legacy value:
     - `rows = 2`
     - `count = 0`
     - `rate = 0.0`
2. `read_file_symbol_name_exact_valid_rate`
   - status: `requires_future_migration`
   - authoritative value:
     - `rows = 0`
     - `count = 0`
     - `rate = null`
   - legacy value:
     - `rows = 1`
     - `count = 0`
     - `rate = 0.0`
3. `direct_answer_substitution_count`
   - status: `requires_future_migration`
   - authoritative value:
     - `direct_answer_substitution_count = 0`
     - `non_exact_tool_expected_row_count = 6`
     - `missing_evidence_row_ids = 5`
   - legacy value:
     - `5`
4. `no_anchor_exact_valid_share`
   - status: `not_comparable`
   - authoritative support:
     - `declared_anchor_row_count = 0`
     - `declared_no_anchor_row_count = 0`
   - legacy value:
     - `0.0`

## Legacy Surface Stability

File-hash validation before and after consumer execution:

1. `summary.json` SHA-256 before consumer:
   - `ae43a1dae2e014520838466358231b38fdb74e48c496acc3d7735540698dcd6f`
2. `summary.json` SHA-256 after consumer:
   - `ae43a1dae2e014520838466358231b38fdb74e48c496acc3d7735540698dcd6f`
3. `comparison_rows.jsonl` SHA-256 before consumer:
   - `65cea053b18415a0b8cb9899703f88d976b4eff51da2e8c2fc071b6e37ed94f0`
4. `comparison_rows.jsonl` SHA-256 after consumer:
   - `65cea053b18415a0b8cb9899703f88d976b4eff51da2e8c2fc071b6e37ed94f0`

Unchanged-file results:

1. `summary_unchanged = true`
2. `comparison_rows_unchanged = true`

## Ownership And Missingness Preservation

Observed behavior:

1. authoritative read-file exact-valid alignment was consumed directly from Stage C row-fact eligibility plus Family A scorer exact-valid state;
2. authoritative symbol-name governed membership remained unavailable because no declared symbol-membership rows were emitted;
3. authoritative direct-answer subtype count remained blocked for migration readiness because explicit missing-evidence rows remained present;
4. no-anchor remained explicitly not-comparable rather than converted into an authoritative replacement metric.

No prompt-derived membership reconstruction or subtype reconstruction was observed.

## Integrity Checks

Observed reconciliation integrity checks:

1. `row_id_uniqueness_preserved = true`
2. `family_a_rows_resolve_to_row_facts = true`
3. `guardrails_clear = true`
4. `legacy_surface_policy_preserved = true`

## Runtime Risks / Remaining Limitations

1. The reconciliation surface is intentionally narrow and limited to four legacy compatibility-bearing surfaces.
2. The bounded runtime sample still contains zero declared authoritative symbol-name and anchor memberships, so those surfaces remain future-migration evidence rather than aligned comparisons.
3. The passive reconciliation surface does not compute or authorize any replacement metrics.

## Determination

Runtime validation was successful for Package 1C.

The consumer emitted a reconciliation artifact successfully, resolved authoritative and legacy inputs directly, produced reproducible statuses, and left all legacy detector-facing surfaces unchanged.
