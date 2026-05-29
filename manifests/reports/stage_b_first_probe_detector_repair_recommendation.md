# Stage B First Probe Detector Repair Recommendation

## Recommendation
`MARK_NONCOMPUTABLE_WITH_GOVERNANCE_FLAG`

## Why this is the smallest safe repair now
1. It enables detector execution on the already-produced eval summary without retraining or rerunning eval.
2. It avoids unsafe proxy substitution for metrics that are not semantically present (notably `direct_answer_substitution_count`).
3. With current threshold profile status rules (`noncomputable_status = halt_progression`), safety is preserved: missing critical metrics cannot silently pass.

## Required guardrails for this recommendation
- Missing metrics must be reported per-rule with explicit noncomputable reasons.
- Final detector status must remain governance-conservative (`halt_progression` or stricter) when required metrics are noncomputable.
- Noncomputable metrics must be surfaced in both `collapse_watch_interpretation` and `gate_assessment` outputs.

## Follow-on alignment (next phase after minimal safe repair)
1. Add strict alias mapping for truly equivalent metrics only (no semantic proxies).
2. Disambiguate `wrapper_leakage_overall` baseline candidate paths.
3. Plan a schema-convergence update between canonical eval summary and threshold profile metric catalog to restore full computability.

## Why not choose profile-only change as first repair
- Direct profile edits can weaken governance semantics if unavailable metrics are dropped or proxied.
- Detector-side noncomputable handling preserves existing governance intent while exposing schema debt explicitly.
