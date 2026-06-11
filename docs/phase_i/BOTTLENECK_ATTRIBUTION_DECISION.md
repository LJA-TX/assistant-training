# Phase I Bottleneck Attribution Decision

## Current Decision

**Pending execution**

## Why This Is Pending

The Phase I treatment datasets were built successfully, but the first-screen runs have not been executed yet.
Without the H0/H2/H1 metrics, there is no basis for a valid attribution decision under the Phase H thresholds.

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
The only correct state at this point is "ready for first-screen execution."
