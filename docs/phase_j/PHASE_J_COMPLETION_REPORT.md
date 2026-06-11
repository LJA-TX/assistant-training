# Phase J Completion Report

## Executive Summary

Phase J is complete as a documentation-only design package.
The repository evidence now supports a combined-bottleneck interpretation: H2 demonstrates a strong commitment signal, H1 demonstrates a strong diversity signal, and neither run resolves the safety problem.

The formal project determination remains `inconclusive_external_first`.

## Key Findings

1. H0 established a real comparator, but it is not safety-clean and it does not show meaningful tool-holdout competence.
2. H2 showed that commitment pressure can lift tool-call realization, heldout accuracy, and no-anchor performance.
3. H1 showed that diversity restoration can lift tool-holdout and tail-tool behavior, and can outperform H2 on several safety and holdout metrics.
4. All observed runs still fail at least one safety invariant, so capability gains alone are not enough.

## Combined Bottleneck Assessment

The smallest model consistent with the evidence is a two-lever content model plus a separate safety gate.

- Diversity explains the H1 tail-tool and tool-holdout lift.
- Commitment explains the H2 heldout-validation and tool-call realization lift.
- Safety/no-call behavior remains a separate constraint that neither content lever solved.

That is why the strongest scientific interpretation is `Combined Bottleneck (E)`.

## Dataset V1.1 Design Guidance

Dataset v1.1 should try to combine:

- H1-style diversity restoration,
- H2-style commitment pressure,
- and explicit safety-calibration rows that keep refusal behavior exact.

It should also be built with:

- zero contamination overlap,
- frozen evaluation semantics,
- and validation that treats wrapper leakage and no-call regressions as hard failures.

## Recommended Next Phase

Phase K should be an external-first, safety-calibrated Dataset v1.1 build and validation phase.

That recommendation follows both the scientific interpretation and the formal project determination.
It is the only next step that is consistent with the evidence without reopening the internal-only loop.

## Confidence Assessment

| Claim | Confidence | Why |
|---|---|---|
| H0 is a valid but unsafe baseline | High | The control completed cleanly and its metrics are directly recorded. |
| H2 is a real commitment signal | High | The reported gains on tool-holdout, heldout validation, tool-name, and argument accuracy are large and consistent. |
| H1 is a real diversity signal | High | The reported gains on tool-holdout, no-anchor, and tail-tool metrics are large and consistent. |
| The bottleneck is combined rather than singular | High | H1 and H2 split the metric families rather than producing a single winner. |
| Phase K should be external-first and safety-calibrated | High | That matches the formal determination and the unresolved safety gap. |
| The exact v1.1 mix is fully specified | Medium | H3 and H4 were not executed, so schema and methodology remain untested. |

## Boundary Confirmation

This phase did not modify datasets, training code, evaluators, scoring, or governance.
It only synthesized the repository evidence into a next-step design package.

## Sources Used

- `docs/phase_i/H0_CHECKPOINT_REPORT.md`
- `docs/phase_i/H2_CHECKPOINT_REPORT.md`
- `docs/phase_ix/H1_EXCEPTION_CHECKPOINT_REPORT.md`
- `docs/phase_ix/H1_EXCEPTION_SCIENTIFIC_INTERPRETATION.md`
- `docs/phase_i/PHASE_I_FINAL_COMPLETION_REPORT.md`
- `docs/phase_i/BOTTLENECK_ATTRIBUTION_DECISION.md`

