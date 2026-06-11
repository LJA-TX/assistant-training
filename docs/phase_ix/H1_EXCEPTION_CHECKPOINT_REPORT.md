# H1 Exception Checkpoint Report

## Outcome

`H1_diversity_patch` completed training and canonical evaluation under the operator-authorized exception run.

The run is diagnostic/report-only and remains non-promotional. It is also not safety-clean under the Phase H kill metrics because `no_call_correctness = 0.9` and `adversarial no_call_correctness = 0.7`.

## Artifact Links

- [Training summary](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch/training_summary.json)
- [Canonical eval summary](/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/summary.json)
- [Canonical eval comparison rows](/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/comparison_rows.jsonl)

## Training And Eval Results

- Training runtime: `160.474` seconds
- Training loss: `0.5263751833527176`
- Internal eval loss: `0.412889301776886`

### Adapter Vs Base Deltas

- Exact JSON validity: `+0.44` (`+44` pp)
- Invalid JSON rate: `-0.60` (`-60` pp)
- Tool-name accuracy: `+0.7142857142857143` (`+71.428571` pp)
- Argument accuracy: `+0.6285714285714286` (`+62.857143` pp)
- Wrapper leakage: `0.0`
- No-call correctness: `-0.09999999999999998` (`-10` pp)

### Adapter Aggregate Metrics

- Exact JSON validity: `0.44`
- Invalid JSON rate: `0.1`
- Tool-name accuracy: `0.7142857142857143`
- Argument accuracy: `0.6285714285714286`
- Wrapper leakage: `0.0`
- No-call correctness: `0.9`
- Adversarial no-call correctness: `0.7`

### Tool-Holdout And Diagnostic Profile

- Tool-holdout exact JSON validity: `0.6`
- Heldout-validation exact JSON validity: `0.64`
- No-anchor exact-valid share: `0.8636363636363636`
- Read-file exact-valid rate: `0.5185185185185185`
- Read-file symbol-name exact-valid rate: `0.8461538461538461`
- Direct-answer substitution count on non-exact tool rows: `12`
- Scalar substitution count on non-exact tool rows: `0`
- Malformed partial JSON count on non-exact tool rows: `8`
- Near-canonical wrapper or envelope drift count on non-exact tool rows: `32`

## Kill Metrics

- Phase H kill metric tripped: `no_call` correctness below `1.0`
- Phase H kill metric tripped: `adversarial` correctness below `1.0`
- Phase H kill metric did not trip on wrapper leakage
- H1 remains report-only evidence

## Comparison Versus H0

- Exact JSON validity: `+0.395`
- Invalid JSON rate: `-0.045`
- Tool-name accuracy: `+0.6428571428571428`
- Argument accuracy: `+0.5642857142857143`
- Tool-holdout exact-valid: `+0.6`
- Heldout-validation exact-valid: `+0.55`
- Wrapper leakage: `0.0`
- No-call correctness: `-0.016666666666666607`
- Adversarial no-call correctness: `-0.05`
- Direct-answer substitution: `12` vs `18` non-exact tool rows

## Comparison Versus H2

- Exact JSON validity: `-0.04`
- Invalid JSON rate: `+0.015`
- Tool-name accuracy: `-0.05714285714285716`
- Argument accuracy: `-0.06428571428571428`
- Tool-holdout exact-valid: `+0.075`
- Heldout-validation exact-valid: `-0.11`
- No-anchor exact-valid: `+0.019886363636363757`
- Wrapper leakage: `-0.005`
- No-call correctness: `+0.1`
- Adversarial no-call correctness: `+0.3`
- Direct-answer substitution: `12` vs `9` non-exact tool rows

## Current Reading

H1 is a real diversity-lift signal:

- it moves tool-holdout exact-valid off the H0 zero baseline;
- it improves no-anchor exact-valid relative to H0 and H2;
- it improves read-file exact-valid and symbol-name exact-valid relative to the control;
- and it does so without introducing wrapper leakage.

The run still fails the no-call/adversarial safety invariant, so it remains report-only evidence rather than a promotion candidate.
