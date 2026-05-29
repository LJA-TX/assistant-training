# Stage B First Probe Detector Noncomputable Fix Summary

## Scope
Implemented governance-safe noncomputable handling in:

- `/opt/ai-stack/assistant-training/scripts/post_eval_collapse_detector.py`

Constraints honored:

- No training
- No eval rerun
- No eval-output mutation
- No baseline mutation
- No threshold-profile mutation
- No proxy metric mapping/substitution

## Root Cause Addressed
- Classified root cause: `THRESHOLD_PROFILE_STALE_METRIC`
- Prior behavior: unresolved required metric caused hard runtime failure.
- New behavior: unresolved metrics are captured as noncomputable and propagated to rule/gate outputs.

## Implementation Details
1. Missing metric resolution
- Metric resolution now records unresolved metrics instead of raising immediately.
- Each unresolved metric entry includes:
  - `metric_id`
  - `summary_side`
  - `reason`
  - `catalog_spec`
  - `affected_rules` / `affected_rule_ids`

2. Rule noncomputable behavior
- Rules depending on unresolved metrics are emitted as:
  - `status = "noncomputable"`
  - `triggered = null`
  - `computable = false`
  - `missing_metric_ids`
  - `missing_metric_sides`
  - explicit reason

3. Governance-safe status behavior
- Final status still obeys threshold-profile policy.
- With `status_decision_rules.noncomputable_status = halt_progression`, missing required metrics force conservative halt behavior.

4. Output contract extension
- Added to both detector outputs:
  - `noncomputable_metrics`
  - `noncomputable_rules`
  - `noncomputable_policy_applied`

## Validation Results
Validation artifact:

- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_detector_noncomputable_validation.json`

Observed:

1. Compile validation
- `python -m py_compile scripts/post_eval_collapse_detector.py` -> pass

2. Synthetic fixture validation
- `pass` control case -> `status=pass`, no noncomputable rules
- missing-metric case -> detector completes with `status=halt_progression`, noncomputable reporting populated

3. Required live-summary detector run
- Input eval summary:
  - `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_mh_eval/summary.json`
- Outputs emitted:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_collapse_watch_interpretation.json`
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_gate_assessment.json`
- Result:
  - detector completed without exception
  - `status=halt_progression`
  - `progression_allowed=false`
  - `halt_recommended=true`
  - `noncomputable_metrics.eval_summary` fully enumerated

## Governance Interpretation
- Missing profile metrics are no longer silent and no longer crash execution.
- They are explicitly reported and conservatively escalated per policy.
- Current first-probe governance outcome remains non-promotable until metric-schema alignment is resolved.

## Final Recommendation
`NOT_READY`
