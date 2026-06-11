# Phase I Bottleneck Attribution Decision

## Current Decision

**inconclusive_external_first**

## Why This Is Pending

The Phase I control run completed, and the H2 commitment probe completed, but both runs violated the Phase H hard-stop invariant:

- `H0_control_i3_micro`: adapter-side `adversarial no_call_correctness = 0.75`
- `H2_commitment_patch`: adapter-side `wrapper_leakage = 0.005`, `no_call_correctness = 0.8`, and `adversarial no_call_correctness = 0.4`
- Phase H requires `no_call` and `adversarial` correctness to remain exactly `1.0`

The H2 probe also triggered the run-level ceiling for additional internal-only runs because it became the second kill-tripped run after H0.
That blocked `H1_diversity_patch`, so the first-screen pair was never completed.
Without the H1 comparator, the published A/B/C/D/E thresholds cannot be applied as written.

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

The strongest signal observed is commitment-dominant:

- `H2` raised tool-holdout exact-valid from `0.0` to `0.525`
- `H2` raised heldout-validation exact-valid from `0.09` to `0.75`
- `H2` raised no-anchor exact-valid from `0.0` to `0.84375`
- `H2` sharply improved tool-name and argument accuracy

That signal is not formally decidable under the published Phase H framework because the first-screen pair was truncated before `H1_diversity_patch` could run and the H2 probe was not safety-clean.
The official attribution state remains `inconclusive_external_first`.
