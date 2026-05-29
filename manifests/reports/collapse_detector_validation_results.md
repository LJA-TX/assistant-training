# Collapse Detector Validation Results

## Validation Scope
- Synthetic fixtures only.
- No real eval execution.
- Verify all required status classes and fail-fast behaviors.

## Test Matrix

1. `pass` case
- Input summary: `summary_pass.json`
- Baseline: provided
- Expected: `pass`
- Observed: `pass`
- Result: `PASS`

2. `watch` case
- Input summary: `summary_watch.json`
- Baseline: provided
- Geometry context: provided
- Expected: `watch`
- Observed: `watch`
- Result: `PASS`

3. `halt_progression` case
- Input summary: `summary_halt.json`
- Baseline: provided
- Expected: `halt_progression`
- Observed: `halt_progression`
- Result: `PASS`

4. `catastrophic_halt` case
- Input summary: `summary_catastrophic.json`
- Baseline: provided
- Expected: `catastrophic_halt`
- Observed: `catastrophic_halt`
- Result: `PASS`

5. Missing metric fail-fast
- Input summary: `summary_missing_metric.json`
- Baseline: provided
- Expected: non-zero exit with missing metric error
- Observed: exit code `1`, error: `required metric 'no_call_correctness_adversarial' not found in summary`
- Result: `PASS`

6. Missing baseline for delta rule behavior
- Input summary: `summary_watch.json`
- Baseline: omitted
- Profile policy: `missing_baseline_policy=fail_fast`
- Expected: non-zero exit
- Observed: exit code `1`, error: `baseline summary is required because threshold profile includes delta_vs_baseline rules`
- Result: `PASS`

## Additional Guards
- `python -m py_compile scripts/post_eval_collapse_detector.py`: `PASS`
- Detector is standalone and post-eval only.
- No dataset/config mutation performed during validation.

## Validation Artifacts
- Fixtures: `/opt/ai-stack/assistant-training/manifests/reports/phase4_validation/fixtures`
- Outputs: `/opt/ai-stack/assistant-training/manifests/reports/phase4_validation/outputs`

