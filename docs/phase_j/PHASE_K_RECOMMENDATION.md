# Phase J Phase K Recommendation

## Recommendation

Phase K should be an external-first, safety-calibrated Dataset v1.1 build and validation phase.

That is the most defensible next implementation phase because:

- the formal project determination remains `inconclusive_external_first`,
- H1 and H2 split the metric families rather than producing a single winner,
- and every observed run still fails at least one safety invariant.

## Objectives

1. Build a Dataset v1.1 candidate that combines the H1 diversity lesson with the H2 commitment lesson.
2. Keep the refusal surface exact so no-call and adversarial no-call correctness return to `1.0`.
3. Preserve or improve tool-holdout exact-valid, heldout-validation exact-valid, tool-name accuracy, and argument accuracy.
4. Keep the candidate interpretable without post-hoc threshold changes.
5. Maintain strict contamination and canonical-eval contract discipline.

## Entry Criteria

1. The Phase J documentation package is complete and reviewed.
2. The canonical evaluation manifest remains frozen.
3. The H0, H1, H2, and H1-exception evidence has been reviewed and accepted as the design basis.
4. Candidate source material is decontaminated before any dataset build begins.
5. Acceptance thresholds are fixed before construction starts.

## Exit Criteria

1. A Dataset v1.1 candidate is built and documented.
2. Contamination checks are zero for heldout-validation and tool-holdout.
3. Validation confirms no wrapper leakage and exact no-call safety.
4. The candidate either shows a clean capability lift over H0/H1/H2 or is rejected without reinterpretation.
5. The next phase decision is written from the measured result, not from a preferred narrative.

## Risks

1. Contamination or license problems in the external-first path.
2. Capability dilution if diversity and commitment are mixed without discipline.
3. Safety regression if tool-call pressure is increased without refusal calibration.
4. False confidence if the validation plan allows post-hoc metric swapping.
5. Scope creep if the work expands into schema or methodology redesign before the current bottleneck is handled.

## Success Metrics

1. `wrapper_leakage = 0.0`
2. `no_call_correctness = 1.0`
3. `adversarial_no_call_correctness = 1.0`
4. Zero contamination overlap against heldout-validation and tool-holdout
5. Nonzero tool-holdout exact-valid if the control remains at zero
6. Improved heldout-validation exact-valid versus H0
7. Improved tool-name and argument accuracy versus H0
8. Retained or improved no-anchor exact-valid versus H1 and H2
9. Aggregate invalid JSON at or below `0.30`

## Rationale

Phase K should not be another single-lever internal probe.
The repository already answered the narrow internal question as far as it can without redesigning the experiment: diversity and commitment both matter, and safety still blocks promotion.

The next phase should therefore attempt a decontaminated, safety-calibrated Dataset v1.1 that can hold both capability gains at once.

## Sources Used

- `docs/phase_i/BOTTLENECK_ATTRIBUTION_DECISION.md`
- `docs/phase_i/PHASE_I_FINAL_COMPLETION_REPORT.md`
- `docs/phase_ix/PHASE_IX_COMPLETION_REPORT.md`
- `docs/phase_ix/H1_EXCEPTION_SCIENTIFIC_INTERPRETATION.md`
- `docs/phase_h/STOP_RULES_AND_DECISION_GATES.md`
- `docs/phase_h/SUCCESS_AND_FAILURE_CRITERIA.md`
