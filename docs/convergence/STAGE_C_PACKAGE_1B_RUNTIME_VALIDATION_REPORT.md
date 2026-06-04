# Stage C Package 1B Runtime Validation Report

## Scope

This report records representative runtime validation for the first passive governance consumer over authoritative Stage C Package 1/1A artifacts.

Validated scope:

1. real canonical evaluator execution;
2. consumer execution over emitted Stage C artifacts;
3. alignment between consumer output and source artifacts;
4. unchanged legacy detector-facing surfaces.

## Runtime Commands

Canonical evaluator run:

```bash
python scripts/eval_canonical_manifest.py \
  --manifest evals/canonical_eval_manifest_v1.json \
  --out-dir /tmp/stage_c_package1b_runtime_validation_run \
  --max-samples-per-split 3
```

Passive governance consumer:

```bash
python scripts/stage_c_package1b_passive_governance_consumer.py \
  --run-dir /tmp/stage_c_package1b_runtime_validation_run
```

Both commands exited `0`.

## Runtime Output Directory

- `/tmp/stage_c_package1b_runtime_validation_run`

## Emitted Consumer Artifact

Confirmed present:

- `stage_c_package1b_passive_governance_report.json`

## Consumer Findings

Observed reported values:

1. Family A tool-expected population count: `6`
2. Family A non-exact tool-expected count: `6`
3. Family A subtype-assigned count: `1`
4. Family A missing-evidence count: `5`
5. Family A missing-evidence reason counts:
   - `current canonical evaluator does not emit approved direct-answer or scalar substitution evidence`: `5`
6. declared symbol-membership row count: `0`
7. declared anchor row count: `0`
8. ownership-conflict row count: `0`

Observed integrity checks:

1. `row_id_uniqueness_preserved = true`
2. `row_fact_count_matches_runtime_summary = true`
3. `family_a_side_record_count_matches_runtime_summary = true`
4. `tool_expected_row_ids_have_family_a_records = true`
5. `family_a_row_ids_resolve_to_row_facts = true`
6. `guardrails_clear = true`

## Ownership-Preservation Evidence

The consumer report preserved authority boundaries:

1. Family A tool-expected population count was consumed from `stage_c_row_fact_metadata_artifact.json` using dataset-owned `family_a_tool_expected_eligible`.
2. Family A subtype-assigned and missing-evidence counts were consumed from `stage_c_family_a_scorer_evidence_artifact.json` using scorer-owned `subtype_assignment` and `missing_evidence`.
3. Guardrail status was consumed from `stage_c_governance_guardrails_artifact.json`.
4. Legacy-surface preservation policy was consumed from `stage_c_runtime_contract_summary_artifact.json`.

No prompt-derived or detector-derived facts were used.

## Legacy Surface Stability

File-hash validation before and after consumer execution:

1. `summary.json` SHA-256 before consumer:
   - `19c33c8269a3519cd7ee362b410cc863ca0743724a8e0bf3d383cce7936b213e`
2. `summary.json` SHA-256 after consumer:
   - `19c33c8269a3519cd7ee362b410cc863ca0743724a8e0bf3d383cce7936b213e`
3. `comparison_rows.jsonl` SHA-256 before consumer:
   - `65cea053b18415a0b8cb9899703f88d976b4eff51da2e8c2fc071b6e37ed94f0`
4. `comparison_rows.jsonl` SHA-256 after consumer:
   - `65cea053b18415a0b8cb9899703f88d976b4eff51da2e8c2fc071b6e37ed94f0`

Unchanged-file results:

1. `summary_unchanged = true`
2. `comparison_rows_unchanged = true`

The consumer therefore left legacy detector-facing outputs untouched.

## Guardrails And Policy

The consumer observed:

1. guardrail status remained clear (`inference/substitution/reconstruction = false`);
2. runtime contract summary still declared:
   - `summary_json = preserved`
   - `comparison_rows_jsonl = preserved`
   - `detector_metrics = unchanged`
   - `threshold_behavior = unchanged`
   - `comparability_policy = unchanged`

## Runtime Risks / Remaining Limitations

1. The first passive governance consumer only answers a Family A coverage question; it is not a full governance-family surface.
2. The bounded runtime sample still exercises only one approved subtype-assignment path and five explicit missing-evidence rows.
3. Current runtime output contained no declared B1 or B2 governed memberships, so the ownership-gap portion of the report was zero-valued in this run.

## Determination

Runtime validation was successful for Package 1B.

The consumer executed successfully on a real canonical evaluator run, consumed only authoritative Stage C artifacts, produced governance-facing output aligned with those artifacts, and left all legacy detector-facing and threshold-facing surfaces unchanged.
