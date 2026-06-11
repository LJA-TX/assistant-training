# Phase I Bottleneck Attribution Decision

## Current Decision

**inconclusive_external_first**

## Why This Is Pending

The Phase I control run completed, but it violated the Phase H hard-stop invariant:

- adapter-side `adversarial no_call_correctness = 0.75`
- Phase H requires `no_call` and `adversarial` correctness to remain exactly `1.0`

Because H0 is not trustworthy, the experiment cannot proceed to `H2_commitment_patch` or `H1_diversity_patch`.
That leaves no defensible basis for A/B/C/D/E attribution.

## Required Inputs Before Decision

- `H0_control_i3_micro` canonical eval summary
- `H2_commitment_patch` canonical eval summary
- `H1_diversity_patch` canonical eval summary
- comparison rows for each run
- immediate kill-metric checks

## Decision Rules To Apply Later

- favor `A` if diversity clearly outperforms commitment on the declared thresholds
- favor `B` if commitment improves direct-answer/scalar substitution and no-anchor exact-valid as specified
- favor `C` only if the schema probe is later required and materially reduces invalid-schema behavior
- favor `D` only if a methodology-only probe later wins on frozen control bytes
- favor `E` if the treatments split metric families without a single clean winner
- use `inconclusive_external_first` if the internal-only evidence stays within the inconclusive band

## Interim Conclusion

No bottleneck attribution should be recorded yet.
The only correct state now is "halted after H0 control failure; escalate externally."
