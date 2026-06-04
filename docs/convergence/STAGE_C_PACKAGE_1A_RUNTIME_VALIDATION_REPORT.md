# Stage C Package 1A Runtime Validation Report

## Scope

This report records representative runtime validation for Stage C Package 1A after authoritative row-identity instantiation was implemented in the live canonical evaluator path.

Validated scope:

1. Stage C artifact emission during a real canonical evaluator execution;
2. row-identity uniqueness at runtime;
3. missingness preservation in emitted Stage C artifacts;
4. Family A scorer-evidence behavior at runtime;
5. unchanged legacy detector-facing surfaces;
6. unchanged Stage C guardrail reporting.

## Runtime Command

Manifest used:

- `evals/canonical_eval_manifest_v1.json`

Command executed:

```bash
python scripts/eval_canonical_manifest.py \
  --manifest evals/canonical_eval_manifest_v1.json \
  --out-dir /tmp/stage_c_package1a_runtime_validation_run \
  --max-samples-per-split 3
```

Command result:

- exit `0`

Runtime output directory:

- `/tmp/stage_c_package1a_runtime_validation_run`

## Emitted Artifacts

Confirmed present:

1. `summary.json`
2. `comparison_rows.jsonl`
3. `stage_c_row_fact_metadata_artifact.json`
4. `stage_c_family_a_scorer_evidence_artifact.json`
5. `stage_c_governance_guardrails_artifact.json`
6. `stage_c_runtime_contract_summary_artifact.json`

## Runtime Counts

Observed counts from the emitted Stage C artifacts:

1. row-fact record count: `15`
2. unique row-fact `row_id` count: `15`
3. Family A base-side record count: `15`
4. unique Family A base-side `row_id` count: `15`
5. duplicate `source_case_id` values still present in the sampled run:
   - `p0_find_files_1`: `2` rows

Coverage summary from emitted row-fact artifact:

1. Family A tool-expected eligible rows: `6`
2. Family B1 read-file eligible rows: `2`
3. declared symbol-name membership rows: `0`
4. symbol-name membership missing rows: `2`
5. declared anchor-eligible rows: `0`
6. anchor-eligible missing rows: `15`

## Row-Identity Runtime Findings

### Duplicate Provenance Labels No Longer Collide

The sampled runtime still contained a duplicated provenance label:

- `source_case_id = p0_find_files_1`

The emitted Stage C row IDs for those rows were:

1. `tool_holdout:1`
2. `tool_holdout:2`

These rows also carried identical expected tool identity and arguments, which confirms that exact duplicated corpus rows now remain distinct in Stage C artifacts without changing provenance labels.

### Missingness Preservation Remains Intact

Concrete runtime examples from `stage_c_row_fact_metadata_artifact.json`:

1. `heldout_validation:1`
   - `source_case_id = p0_read_file_2`
   - `family_b1_symbol_name_member = null`
   - `family_b2_anchor_eligible = false`
   - `symbol_name_membership_owner = null`
   - `anchor_assignment_owner = null`
2. `tool_holdout:1`
   - `source_case_id = p0_find_files_1`
   - `family_b1_symbol_name_member = null`
   - `family_b2_anchor_eligible = false`
   - `symbol_name_membership_owner = null`
   - `anchor_assignment_owner = null`

No prompt-derived B1 membership or B2 anchor ownership appeared in the new Stage C artifacts.

## Family A Runtime Findings

Observed Family A base-side summary:

1. tool-expected eligible rows: `6`
2. subtype-assigned rows: `1`
3. missing-evidence rows: `5`
4. emitted subtype counts:
   - `malformed output`: `1`

Concrete examples:

1. `heldout_validation:2`
   - `primary_outcome = invalid_json`
   - `subtype_assignment = malformed output`
   - `missing_evidence = false`
2. `heldout_validation:1`
   - `primary_outcome = invalid_json`
   - `subtype_assignment = null`
   - `missing_evidence = true`
   - missing-evidence reason:
     - `current canonical evaluator does not emit approved direct-answer or scalar substitution evidence`
3. `tool_holdout:1`
   - `primary_outcome = invalid_json`
   - `subtype_assignment = null`
   - `missing_evidence = true`

No fallback subtype synthesis was observed in the emitted Stage C Family A artifact.

## Legacy Surface Stability

The runtime run preserved legacy detector-facing outputs.

Validation checks:

1. recomputed `metrics` from `summary["base"]` matched emitted `summary["metrics"]`
2. recomputed `failure_profile` from `comparison_rows.jsonl` base rows matched emitted `summary["failure_profile"]`

Equality results:

1. `metrics_equal = true`
2. `failure_profile_equal = true`

Observed legacy compatibility-bearing values in `summary.json`:

1. `no_anchor_exact_valid_share = 0.0`
2. `read_file_exact_valid_rate = 0.0`
3. `read_file_symbol_name_exact_valid_rate = 0.0`
4. `direct_answer_substitution_count = 5`

## Governance Guardrails

Observed guardrail status in both Stage C guardrail artifacts:

1. `inference_behavior_detected = false`
2. `substitution_behavior_detected = false`
3. `reconstruction_behavior_detected = false`
4. `legacy_summary_modified = false`
5. `legacy_detector_surface_modified = false`

These reported states matched observed runtime behavior for the emitted Stage C artifacts and the preserved legacy surfaces.

## Runtime Risks / Remaining Limitations

1. The canonical corpus still does not provide a dataset-authored explicit `row_id`; Package 1A relies on split-plus-ordinal instantiation under the frozen manifest row set.
2. The bounded runtime sample validates repeated-case and exact-duplicate disambiguation, but it does not exercise all approved Family A subtype paths.
3. Runtime artifacts for this validation run were produced in `/tmp` and are not part of the committed repository state.

## Determination

Runtime validation was successful for the Package 1A objective.

Stage C artifacts emitted correctly, `row_id` uniqueness held at runtime, duplicate `source_case_id` values no longer collided, missingness preservation remained intact, legacy detector-facing outputs remained unchanged, and guardrail reporting remained aligned with observed behavior.
