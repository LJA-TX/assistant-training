# Stage C Package 1D Runtime Validation Report

## Scope

This report captures representative runtime validation for Stage C Package 1D over the live canonical evaluator path.

The goal is assessment-only runtime verification.

## Runtime Commands

Canonical evaluator run:

```bash
python scripts/eval_canonical_manifest.py \
  --manifest evals/canonical_eval_manifest_v1.json \
  --out-dir /tmp/stage_c_package1d_runtime_validation_run \
  --max-samples-per-split 3
```

Package 1C reconciliation:

```bash
python scripts/stage_c_package1c_passive_reconciliation_surface.py \
  --run-dir /tmp/stage_c_package1d_runtime_validation_run
```

Package 1D readiness assessment:

```bash
python scripts/stage_c_package1d_migration_readiness_assessment.py \
  --run-dir /tmp/stage_c_package1d_runtime_validation_run
```

Reproducibility check:

```bash
python scripts/stage_c_package1d_migration_readiness_assessment.py \
  --run-dir /tmp/stage_c_package1d_runtime_validation_run
sha256sum /tmp/stage_c_package1d_runtime_validation_run/stage_c_package1d_migration_readiness_assessment.json
```

Legacy-surface stability check:

```bash
sha256sum /tmp/stage_c_package1d_runtime_validation_run/summary.json
sha256sum /tmp/stage_c_package1d_runtime_validation_run/comparison_rows.jsonl
```

## Runtime Output Directory

`/tmp/stage_c_package1d_runtime_validation_run`

## Runtime Results

Package 1C reconciliation counts:

1. `aligned`: 1
2. `requires_future_migration`: 2
3. `not_comparable`: 1

Package 1D readiness counts:

1. `migration-ready`: 1
2. `migration-blocked`: 1
3. `insufficient-evidence`: 1
4. `not-comparable`: 1

Per-surface readiness results:

1. `read_file_exact_valid_rate` -> `migration-ready`
2. `read_file_symbol_name_exact_valid_rate` -> `insufficient-evidence`
3. `direct_answer_substitution_count` -> `migration-blocked`
4. `no_anchor_exact_valid_share` -> `not-comparable`

## Runtime Evidence

### `read_file_exact_valid_rate`

Result:

1. direct reconciliation remained aligned;
2. no guardrail or legacy-policy blocker was present.

Assessment result:

1. `migration-ready`

### `read_file_symbol_name_exact_valid_rate`

Observed blocker class:

1. no declared authoritative symbol-membership rows were emitted in the sampled runtime run.

Assessment result:

1. `insufficient-evidence`

Visible evidence:

1. `declared_symbol_membership_row_ids = []`
2. reconciliation reason code `authoritative_declared_symbol_membership_unavailable`

### `direct_answer_substitution_count`

Observed blocker class:

1. authoritative Family A scorer evidence preserved explicit missing-evidence rows.

Assessment result:

1. `migration-blocked`

Visible evidence:

1. reconciliation reason code `authoritative_family_a_subtype_surface_incomplete`
2. missing-evidence row ids:
   - `heldout_validation:1`
   - `heldout_validation:3`
   - `tool_holdout:1`
   - `tool_holdout:2`
   - `tool_holdout:3`

### `no_anchor_exact_valid_share`

Observed disposition:

1. semantic non-equivalence carried forward from Package 1C.

Assessment result:

1. `not-comparable`

Visible evidence:

1. reconciliation reason code `legacy_no_anchor_share_semantic_mismatch`

## Integrity Checks

Runtime integrity checks all passed:

1. `row_id_uniqueness_preserved = true`
2. `family_a_rows_resolve_to_row_facts = true`
3. `guardrails_clear = true`
4. `legacy_surface_policy_preserved = true`
5. `package1c_surface_count_matches = true`

## Legacy-Surface Stability

`summary.json` hash before and after Package 1D:

1. `ac5eab9930694ad434582a3df6a33adaa29700c9b66a51f2471ac4d834e66205`

`comparison_rows.jsonl` hash before and after Package 1D:

1. `65cea053b18415a0b8cb9899703f88d976b4eff51da2e8c2fc071b6e37ed94f0`

Package 1D report reproducibility hash:

1. `bd44ca10a3c1bf68fe5825505fd74fa10846808e0bd533664617fff273d0160c`

No legacy output drift was observed.

## Boundary Confirmation

Confirmed unchanged:

1. detector authority;
2. threshold authority;
3. comparability policy;
4. historical metric identities;
5. `summary.json`;
6. `comparison_rows.jsonl`;
7. detector-facing metrics;
8. threshold-facing inputs.
