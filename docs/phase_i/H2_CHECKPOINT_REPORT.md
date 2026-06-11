# H2 Commitment Checkpoint

## Outcome

`H2_commitment_patch` completed training and canonical evaluation, but the run is not trustworthy under the Phase H hard-stop rules.

The adapter-side canonical eval reports `wrapper_leakage = 0.005`, `no_call_correctness = 0.8`, and `adversarial no_call_correctness = 0.4`, which trip the Phase H kill metrics.

## Artifact Links

- [Training summary](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch/training_summary.json)
- [Canonical eval summary](/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h2_commitment_patch_eval_20260611T120228Z/summary.json)
- [Canonical eval comparison rows](/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h2_commitment_patch_eval_20260611T120228Z/comparison_rows.jsonl)

## Training And Eval Results

- Training runtime: `159.4807` seconds
- Training loss: `0.5947615747098569`
- Internal eval loss: `0.4286271333694458`

### Adapter Vs Base Deltas

- Exact JSON validity: `+0.48` (`+48` pp)
- Invalid JSON rate: `-0.615` (`-61.5` pp)
- Tool-name accuracy: `+0.7714285714285715` (`+77.142857` pp)
- Argument accuracy: `+0.6928571428571428` (`+69.285714` pp)
- Wrapper leakage: `0.005`
- No-call correctness: `-0.19999999999999996` (`-20` pp)

### Adapter Aggregate Metrics

- Exact JSON validity: `0.48`
- Invalid JSON rate: `0.085`
- Tool-name accuracy: `0.7714285714285715`
- Argument accuracy: `0.6928571428571428`
- Wrapper leakage: `0.005`
- No-call correctness: `0.8`
- Adversarial no-call correctness: `0.4`

### Tool-Holdout And Diagnostic Profile

- Tool-holdout exact JSON validity: `0.525`
- Heldout-validation exact JSON validity: `0.75`
- No-anchor exact-valid share: `0.84375`
- Direct-answer substitution count on non-exact tool rows: `9`
- Scalar substitution count on non-exact tool rows: `0`
- Malformed partial JSON count on non-exact tool rows: `6`
- Near-canonical wrapper or envelope drift count on non-exact tool rows: `29`

## Stop-Rule Outcome

- Phase H kill metric tripped: `wrapper leakage > 0`
- Phase H kill metric tripped: `no_call` correctness below `1.0`
- Phase H kill metric tripped: `adversarial` correctness below `1.0`
- H2 is not a promotion candidate
- H1 was not launched because the run-level ceiling was reached after H0 and H2 each tripped kill metrics

## Current Bottleneck Assessment

H2 is a strong commitment-shift signal:

- tool-holdout exact-valid moved from `0.0` in H0 to `0.525`
- heldout-validation exact-valid moved from `0.09` in H0 to `0.75`
- no-anchor exact-valid moved from `0.0` in H0 to `0.84375`
- tool-name and argument accuracy both rose sharply

The gain is not safety-clean. The adapter introduces wrapper leakage and regresses no-call safety on the adversarial split, so the run remains report-only evidence.
