# Digest Split Implementation Summary

## Decision Implemented
- Recommendation implemented: `SPLIT_INTO_DISTINCT_DIGEST_TYPES`.
- Added explicit typed digests:
  - `geometry_mapping_identity_digest`
  - `geometry_context_input_digest`
- Retained legacy field `geometry_context_digest` with explicit alias marker `geometry_context_digest_alias_of`.

## Code Changes
1. Mapping stack emitter updates
- File: `/opt/ai-stack/assistant-training/scripts/train_lora_sft.py`
- Added helpers:
  - `_build_geometry_mapping_identity_digest(...)`
  - `_build_geometry_context_input_digest(...)`
  - `_build_mapping_digest_fields(...)`
- Kept `_build_geometry_context_digest(...)` as backward-compatible alias to mapping identity digest.
- Updated emitters to include typed digest fields in:
  - `resolved_config`
  - `masking_audit.geometry_trace`
  - `training_summary`
  - `exposure_ledger_declared`
  - `exposure_row_identity_sidecar`
  - `exposure_ledger_realized` (default and weighted paths)
  - `exposure_ledger_drift`
  - `sampler_determinism_report`

2. Detector stack emitter updates
- File: `/opt/ai-stack/assistant-training/scripts/post_eval_collapse_detector.py`
- Added helpers:
  - `_build_geometry_mapping_identity_digest(...)`
  - `_build_geometry_context_input_digest(...)`
  - `_build_detector_digest_fields(...)`
- Updated detector outputs to include typed digests in:
  - `collapse_watch_interpretation`
  - `gate_assessment`
- Legacy alias behavior in detector outputs:
  - `geometry_context_digest_alias_of=geometry_context_input_digest`

## Backward Compatibility
- Preserved legacy `geometry_context_digest` for migration window.
- Alias semantics are explicit in every updated emitter:
  - Mapping emitters: alias to `geometry_mapping_identity_digest`
  - Detector emitters: alias to `geometry_context_input_digest`

## Affected Artifacts (from inventory scope)
Updated synthetic/example artifacts under `/opt/ai-stack/assistant-training/manifests/reports/` including:
- `exposure_ledger_declared_example.json`
- `exposure_ledger_realized_example.json`
- `exposure_ledger_drift_example.json`
- `sampler_determinism_report.json`
- `collapse_watch_interpretation_example.json`
- `gate_assessment_example.json`
- `integration_rehearsal/.../*.synthetic.json` (resolved, ledgers, sidecar, sampler, collapse, gate)
- `phase4_validation/outputs/*/{collapse_watch_interpretation.json,gate_assessment.json}`
- `integration_rehearsal_artifact_graph.json`

## Rehearsal Governance Update
- Replaced digest-equality governance with typed semantic checks:
  - Mapping identity consistency
  - Context input consistency
  - Legacy alias correctness
  - Semantic misuse detection
- Cross-type inequality is now expected when scopes differ and is no longer an automatic failure.

## Non-Goals Preserved
- No training/eval/sweep execution.
- No dataset modification.
- No sampler/loss/tensor contract behavior changes in default path.
- No commits or pushes.
