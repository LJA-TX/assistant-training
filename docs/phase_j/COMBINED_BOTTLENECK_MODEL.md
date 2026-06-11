# Phase J Combined Bottleneck Model

## Summary

The smallest model consistent with the repository evidence is not a single-lever story.
It is a two-part content model with a separate safety gate:

1. diversity contributes to tail-tool and tool-holdout coverage;
2. commitment contributes to canonical tool-call realization and heldout accuracy;
3. safety/no-call behavior is a separate constraint that all observed runs failed to satisfy.

## Diversity Contribution

H1 provides the strongest evidence for the diversity term.

- `tool_holdout_exact_valid` moved from `0.0` in H0 to `0.6` in H1.
- `heldout_validation_exact_valid` moved from `0.09` in H0 to `0.64` in H1.
- `no_anchor_exact_valid` moved from `0.0` in H0 to `0.8636363636363636` in H1.
- H1 also improved `read_file` exact-valid behavior and `read_file` symbol-name exact-valid behavior relative to the control.

Interpretation:

- Diversity is not a cosmetic effect.
- It matters most on tail families, tool-holdout coverage, and the long tail of exact-valid recovery.
- The H1 signal is real even though it is not safety-clean.

## Commitment Contribution

H2 provides the strongest evidence for the commitment term.

- `tool_holdout_exact_valid` moved from `0.0` in H0 to `0.525` in H2.
- `heldout_validation_exact_valid` moved from `0.09` in H0 to `0.75` in H2.
- `tool_name_accuracy` moved from `0.07142857142857142` in H0 to `0.7714285714285715` in H2.
- `argument_accuracy` moved from `0.06428571428571428` in H0 to `0.6928571428571428` in H2.
- `no_anchor_exact_valid` moved from `0.0` in H0 to `0.84375` in H2.
- H2 also reduced direct-answer substitution compared with H0.

Interpretation:

- Commitment pressure is the strongest lever for broad canonicalization and heldout exact-valid movement.
- It is not enough by itself to explain the H1/H2 split, because H1 wins the tool-holdout slice and the safety metrics.

## Safety/No-Call Contribution

Safety is not explained away by either content lever.

- H0 failed on adversarial no-call correctness.
- H2 introduced wrapper leakage and worsened no-call and adversarial no-call correctness.
- H1 kept wrapper leakage at `0.0`, but still failed no-call and adversarial no-call correctness.

Interpretation:

- Safety/no-call behavior acts like a separate gate rather than a simple byproduct of better tool accuracy.
- The repository shows a repeated tradeoff: capability gains arrive together with safety regressions unless the dataset design explicitly controls for them.

## Interactions Among The Three

The observed interactions are the key reason the bottleneck is combined rather than singular.

- H1 and H2 split the metric families.
- H2 is stronger on heldout validation, tool-name accuracy, and argument accuracy.
- H1 is stronger on tool-holdout exact-valid, no-anchor exact-valid, wrapper leakage, and no-call/adversarial safety.
- Neither run is safety-clean.

What this means:

- Diversity and commitment are partially independent, not interchangeable.
- Both appear necessary to explain the full response surface.
- Safety cannot be treated as an afterthought because it is the condition that still blocks continuation.

## Smallest Supported Model

The smallest model justified by the evidence is:

- one diversity term,
- one commitment term,
- one safety/no-call term.

The repository does not currently justify adding a separate schema-dominance term or a methodology-dominance term, because H3 and H4 were not executed.
That is an absence of evidence, not evidence against those possibilities.

## Sources Used

- `docs/phase_i/H0_CHECKPOINT_REPORT.md`
- `docs/phase_i/H2_CHECKPOINT_REPORT.md`
- `docs/phase_ix/H1_EXCEPTION_CHECKPOINT_REPORT.md`
- `docs/phase_ix/H1_EXCEPTION_SCIENTIFIC_INTERPRETATION.md`
- `docs/phase_i/RUN_COMPARISON_MATRIX.md`
- `docs/phase_i/PHASE_I_FINAL_COMPLETION_REPORT.md`

