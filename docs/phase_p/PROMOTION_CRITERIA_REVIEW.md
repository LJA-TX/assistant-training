# Promotion Criteria Review

## Verdict

The existing Phase L promotion criteria remain scientifically valid for Dataset v1.2.

No threshold changes are required at this stage.

## Review

| Criterion family | Assessment | Why it remains valid |
|---|---|---|
| Contamination | Valid unchanged | The canonical eval contract is frozen and v1.2 remains contamination-clean. |
| Safety | Valid unchanged | `no_call_correctness = 1.0` and `adversarial_no_call_correctness = 1.0` remain the correct gating surfaces. |
| Exact JSON / tool-call structure | Valid unchanged | Phase M showed the failure was schema-emission collapse, so exact JSON is still the right capability gate. |
| Tool-holdout / heldout validation | Valid unchanged | These remain the decisive heldout capability checks. |
| H2 regression control | Valid unchanged | Direct-answer and scalar-substitution non-regression remains necessary. |
| Decode / scoring invariance | Valid unchanged | The comparison only remains meaningful if the evaluator contract stays frozen. |

## Evidence

The thresholds in Phase L were calibrated against the strongest observed baseline values, not arbitrary convenience values.

That design choice still matches the Phase P question:

- preserve the safety contract;
- recover tool-call competence;
- avoid a tradeoff where one family improves by harming the other.

Dataset v1.2 was built specifically to target those same metric families without changing the evaluation surface.

## Conclusion

The promotion criteria remain appropriate and scientifically defensible as-is.
The right action is to apply them unchanged to the first governed v1.2 run.
