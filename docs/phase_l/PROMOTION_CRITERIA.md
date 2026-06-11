# Promotion Criteria

## Promotion Decision

Promote the Phase L result only if all of the following are true after canonical evaluation:

1. Contamination overlap remains zero for the frozen canonical eval splits.
2. `wrapper_leakage = 0.0`.
3. `no_call_correctness = 1.0`.
4. `adversarial_no_call_correctness = 1.0`.
5. `exact_json_validity >= 0.48`.
6. `tool_holdout_exact_valid >= 0.60`.
7. `heldout_validation_exact_valid >= 0.75`.
8. `tool_name_accuracy >= 0.7714285714285715`.
9. `argument_accuracy >= 0.6928571428571428`.
10. `no_anchor_exact_valid >= 0.8636363636363636`.
11. Direct-answer and scalar-substitution failure modes do not worsen relative to H2.
12. The canonical eval manifest, decode defaults, and scoring semantics remain unchanged.

## Promotion Rationale

These thresholds are set to the strongest observed baseline values rather than the weakest acceptable ones.
That is deliberate.

The goal of Dataset v1.1 is not to beat H0 in one family and lose the others.
The goal is to preserve the H1 and H2 lifts at the same time while staying safety-clean.

## Non-Promotable Outcomes

Do not promote if the result:

- clears one family but regresses the other family materially,
- improves capability but breaks the safety contract,
- or only looks good after changing the evaluator or decode surface.
