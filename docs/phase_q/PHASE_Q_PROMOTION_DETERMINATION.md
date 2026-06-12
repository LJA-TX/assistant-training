# Phase Q Promotion Determination

## Determination

**Do Not Promote**

## Basis

The frozen Phase L promotion criteria require all of the following, among others:

- `wrapper_leakage = 0.0`
- `no_call_correctness = 1.0`
- `adversarial_no_call_correctness = 1.0`
- `exact_json_validity >= 0.48`
- `tool_holdout_exact_valid >= 0.60`
- `heldout_validation_exact_valid >= 0.75`
- `tool_name_accuracy >= 0.7714285714285715`
- `argument_accuracy >= 0.6928571428571428`
- `no_anchor_exact_valid >= 0.8636363636363636`
- direct-answer and scalar-substitution failure modes do not worsen relative to H2

Phase Q fails those criteria decisively.

## Primary Failures

1. Safety regressed below the frozen contract.
   - `no_call_correctness = 0.7666666666666667`
   - `adversarial_no_call_correctness = 0.3`
   - Aggregate no-call correctness is below the `0.95` success threshold.

2. Tool-call capability remains far below the frozen target.
   - `exact_json_validity = 0.03`
   - `tool_holdout_exact_valid = 0.0`
   - `heldout_validation_exact_valid = 0.06`
   - `tool_name_accuracy = 0.07142857142857142`
   - `argument_accuracy = 0.04285714285714286`

3. The diversity tail did not recover.
   - `read_file_exact_valid = 0.0`
   - `read_file_symbol_name_exact_valid = 0.0`
   - `no_anchor_exact_valid share = 0.0`

4. The failure profile is still dominated by non-exact tool emission.
   - `direct-answer substitution = 37`
   - `malformed partial JSON = 3`
   - `near-canonical wrapper or envelope drift = 94`

## Positive Findings

Phase Q is not a pure regression to Phase L.

- Exact JSON validity improved from `0.0` in Phase L to `0.03`.
- Invalid JSON rate improved from `0.345` to `0.2`.
- Wrapper leakage remained `0.0`.

Those improvements are insufficient to offset the capability and safety failures.

## Comparison Judgment

Relative to the published baselines:

- H1 remains substantially stronger on the diversity-sensitive tail.
- H2 remains substantially stronger on the commitment-sensitive metrics.
- Phase Q does not close either gap.
- Phase Q is worse than H0/H1/H2 on no-call safety.

## Final Statement

The candidate is scientifically useful as evidence that the anchor-weighted hybrid moves the surface away from the Phase L collapse, but it is not promotable as a governed release candidate.
