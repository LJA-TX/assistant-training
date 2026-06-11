# H0 Control Checkpoint

## Outcome

`H0_control_i3_micro` completed training and canonical evaluation, but the run is not trustworthy under the Phase H hard-stop rules.

The adapter-side canonical eval reports `no_call_correctness = 0.9166666666666666` overall and `adversarial no_call_correctness = 0.75`, which trips the Phase H kill metric (`no_call` or `adversarial` correctness below `1.0`).

## Artifact Links

- [Training summary](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro/training_summary.json)
- [Canonical eval summary](/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h0_control_i3_micro_eval_20260611T103048Z/summary.json)
- [Canonical eval comparison rows](/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h0_control_i3_micro_eval_20260611T103048Z/comparison_rows.jsonl)

## Training And Eval Results

- Training runtime: `160.8993` seconds
- Training loss: `0.519467106571904`
- Eval runtime: `30.4528` seconds
- Eval loss: `0.39338502287864685`

### Adapter Vs Base Deltas

- Exact JSON validity: `+0.045` (`+4.5` pp)
- Invalid JSON rate: `-0.555` (`-55.5` pp)
- Tool-name accuracy: `+0.07142857142857142` (`+7.142857` pp)
- Argument accuracy: `+0.06428571428571428` (`+6.428571` pp)
- Wrapper leakage: `0.0`
- No-call correctness: `-0.08333333333333337` (`-8.333333` pp)

### Adapter Aggregate Metrics

- Exact JSON validity: `0.045`
- Invalid JSON rate: `0.145`
- Tool-name accuracy: `0.07142857142857142`
- Argument accuracy: `0.06428571428571428`
- Wrapper leakage: `0.0`
- No-call correctness: `0.9166666666666666`
- Adversarial no-call correctness: `0.75`

## Stop-Rule Outcome

- Phase H kill metric tripped: `adversarial` correctness below `1.0`
- H0 is not trustworthy
- Internal-only continuation is halted
- `H2_commitment_patch` and `H1_diversity_patch` were not started

## Current Bottleneck Assessment

No hypothesis attribution is defensible from the current state.
The experiment is blocked at the control stage because the H0 adapter violates the no-call/adversarial hard-stop invariant.
