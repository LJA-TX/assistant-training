# Phase J Dataset V1.1 Design Requirements

## Scope

This document defines requirements only.
It does not build Dataset v1.1, launch training, or change evaluation semantics.

## Design Goal

Dataset v1.1 should try to preserve the H1 and H2 capability gains at the same time while eliminating the safety failures that kept every observed run from being promotion-safe.

In practical terms, v1.1 must be designed to improve:

- tool-holdout exact-valid behavior,
- heldout validation exact-valid behavior,
- tool-name and argument accuracy,
- tail-tool coverage,
- and no-anchor exact-valid behavior,

without reintroducing:

- wrapper leakage,
- no-call regressions,
- adversarial no-call regressions,
- contamination overlap,
- or evaluation-contract drift.

## Required Capability Objectives

1. v1.1 must recover the tool-holdout lift shown by H1 and H2 rather than returning to the H0 zero baseline.
2. v1.1 must preserve or improve heldout-validation exact-valid behavior relative to H1 and H2.
3. v1.1 must improve tool-name and argument accuracy relative to H0 without depending on a single prompt family.
4. v1.1 must keep no-anchor exact-valid behavior materially above H0.
5. v1.1 should expose more than one tool family strongly enough that the model is not overfit to a literal anchor pattern.

## Required Safety Objectives

1. `wrapper_leakage` must remain `0.0`.
2. `no_call_correctness` must be `1.0`.
3. `adversarial_no_call_correctness` must be `1.0`.
4. Aggregate no-call correctness must remain at or above `0.95`.
5. Aggregate invalid JSON must remain at or below `0.30`.
6. Invalid-schema behavior must not be allowed to dominate the result.

## Required Diversity Objectives

1. v1.1 must include enough tail-tool coverage to preserve the H1 signal on tool-holdout exact-valid.
2. v1.1 must not collapse back to a narrow literal-anchor distribution.
3. v1.1 should include underrepresented tool families and task forms that broaden the model beyond the current internal recovery surface.
4. v1.1 should be able to demonstrate generalization on tool-positive rows that were not the same family as the strongest control rows.

## Required Commitment Objectives

1. v1.1 must preserve the commitment gains that H2 produced on heldout validation, tool-name accuracy, and argument accuracy.
2. v1.1 must include anchor-light or paraphrastic tool-expected examples, but not as a substitute for diversity.
3. v1.1 must reduce direct-answer and scalar-substitution failure modes relative to H0.
4. v1.1 must not regain commitment by weakening the refusal surface.

## Required Contamination Safeguards

1. Zero prompt overlap with heldout-validation and tool-holdout targets.
2. Zero target overlap with heldout-validation and tool-holdout targets.
3. Zero case-id overlap with heldout-validation and tool-holdout targets.
4. No accidental leakage from canonical eval prompts, scores, or answer strings into training rows.
5. No hidden reuse of no-call or adversarial rows as if they were ordinary positive examples.
6. All dataset construction must be auditable at the prompt, target, and case-id level.

## Required Validation Criteria

1. Validation must report row counts, tool-family counts, and patch composition.
2. Validation must report contamination overlap checks for heldout-validation and tool-holdout.
3. Validation must confirm frozen non-tool slices are unchanged, or else explain and version every change explicitly.
4. Validation must confirm the canonical eval manifest, decode defaults, and scoring semantics remain unchanged.
5. Evaluation must show at least one primary capability family improving materially over H0 without any kill-metric violation.
6. Any candidate that reintroduces wrapper leakage or no-call regression must be rejected, even if it improves capability metrics.

## Recommended Acceptance Shape

The most credible v1.1 candidate is a hybrid that combines:

- H1-style tail-tool diversity,
- H2-style commitment pressure,
- and explicit safety-calibration rows that keep refusal behavior exact.

That is the only shape currently supported by the evidence.

## Sources Used

- `docs/phase_h/EXPERIMENTAL_OBJECTIVES.md`
- `docs/phase_h/CANDIDATE_INTERVENTION_ANALYSIS.md`
- `docs/phase_h/SUCCESS_AND_FAILURE_CRITERIA.md`
- `docs/phase_h/STOP_RULES_AND_DECISION_GATES.md`
- `docs/phase_ix/H1_EXCEPTION_CHECKPOINT_REPORT.md`
- `docs/phase_ix/H1_EXCEPTION_SCIENTIFIC_INTERPRETATION.md`
- `docs/phase_i/PHASE_I_FINAL_COMPLETION_REPORT.md`
