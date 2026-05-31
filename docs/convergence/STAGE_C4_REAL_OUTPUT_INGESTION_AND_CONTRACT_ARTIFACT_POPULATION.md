# Stage C4 Real Output Ingestion and Contract Artifact Population

## Scope

This artifact records Stage C4 implementation for bounded real-output ingestion and contract artifact population.

This slice does not run live inference and does not execute full benchmark scoring.

## Authoritative Inputs

Implementation aligned to:

- Stage C0 contract-lock artifacts
- Stage C1 evaluator foundation artifacts
- Stage C2 aggregation/state/reconciliation foundation artifacts
- Stage C3 runtime integration artifacts
- Stage B fixture corpus and doctrine artifacts

## Implemented Artifacts

- `scripts/stage_c4_real_output_ingestion.py`
- `tests/test_stage_c4_real_output_ingestion.py`
- `reports/stage_c4/input/stage_c4_sample_output_records.jsonl`
- `reports/stage_c4/contract_artifacts/*`

## WP10: Model Output Record Contract

Implemented model-output record contract fields:

1. fixture/source references:
   - `fixture_id`
   - `source_definition_id`
2. model and prompt/input identity:
   - `model_identifier`
   - `prompt_reference` (or `input_reference` alias)
3. raw output:
   - `raw_model_response` (preserved verbatim when string)
4. parsed payload support:
   - `parse_status`
   - `parse_error`
   - `parsed_tool_call_payload` (only when present in strict JSON object)
   - `embedded_payload_candidate` (preserved as candidate when wrapper/leakage exists)
5. tool/no-call status surfaces:
   - `tool_call_status`
   - `tool_call_entry_issue_count`
   - `no_call_expected`
   - `no_call_emitted`
   - `no_call_status`
   - `wrapper_or_prose_leakage`
6. provenance/evidence:
   - `evidence_provenance`
   - `line_number`
   - `record_id`

## WP11: Output Ingestion Path

Implemented bounded ingestion behavior:

1. preserves raw output text,
2. preserves parse errors,
3. preserves embedded wrapper/leakage indicators,
4. preserves partial/missing tool-call payloads without repair,
5. preserves invalid JSONL input lines as flagged records,
6. emits contract issues without inferring missing fields.

Explicit non-repair behaviors enforced:

- no tool-call reconstruction,
- no argument reconstruction,
- no fallback tool-name inference,
- no repair-by-inference on malformed outputs.

## WP12: Contract Artifact Population From Output Records

Extended runtime path:

1. runs Stage C3 fixture-baseline integration as a bounded baseline reference,
2. ingests model-output records,
3. builds C1 row-fact records from ingested outputs,
4. builds C2 state-axis records from ingested outputs,
5. builds C2 aggregation/reconciliation summaries from ingested outputs,
6. emits C4 contract artifacts.

Emitted C4 artifacts:

1. `c4_output_inventory_artifact.json`
2. `c4_parse_toolcall_status_artifact.json`
3. `c4_row_fact_metadata_artifact.json`
4. `c4_state_axis_from_outputs_artifact.json`
5. `c4_aggregation_summary_from_outputs_artifact.json`
6. `c4_reconciliation_summary_from_outputs_artifact.json`
7. `c4_validation_issues_artifact.json`
8. `c4_governance_guardrails_artifact.json`
9. `c4_runtime_contract_summary_artifact.json`
10. `c4_runtime_integration_summary.json`

## Validation Executed

1. `pytest -q tests/test_stage_c4_real_output_ingestion.py` -> pass (`5 passed`)
2. `python scripts/stage_c4_real_output_ingestion.py --output-records-path reports/stage_c4/input/stage_c4_sample_output_records.jsonl --artifacts-dir reports/stage_c4/contract_artifacts` -> pass

Runtime output highlights for sample input:

- output records ingested: `6`
- parse status distribution:
  - `strict_json_object`: `4`
  - `invalid_json_with_embedded_object`: `1`
  - `invalid_json`: `1`
- tool-call status distribution includes explicit partial/missing/unavailable states
- reconciliation summary: `4 pass`, `0 fail`, `0 blocked`
- governance guardrail status: no collapsed-state/inference/substitution/reconstruction behavior detected

## Boundary Confirmation

Not implemented in this slice:

1. live model inference,
2. full benchmark scoring,
3. detector projection migration,
4. threshold-profile migration,
5. full comparability engine behavior beyond required contract preservation,
6. catalog changes or new fixture authoring.

## Remaining Gaps

Remaining milestones before full implementation readiness:

1. connect ingestion path to larger evaluator runtime execution loops,
2. expand from bounded contract population to scoring/report execution over larger corpora,
3. implement detector projection migration,
4. implement threshold-profile migration,
5. implement full comparability engine behavior.

## Recommended Next Milestone

Recommended next milestone:

- `Stage C5 - Evaluator Scoring Path Integration (No Live Inference)`

Entry focus:

1. consume ingested output records in bounded scoring flows,
2. populate family-level scored summaries under contract constraints,
3. preserve non-repair and non-inference guardrails under expanded runtime execution.
