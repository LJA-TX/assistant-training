# Phase IX Completion Report

## Executive Summary

The operator-authorized H1 exception run completed successfully as a diagnostic, report-only follow-up.

`H1_diversity_patch` produced the missing diversity datapoint, materially improved the diversity-sensitive metrics relative to H0, and split the first-screen evidence with H2 rather than cleanly replacing it.

The official Phase I determination remains unchanged.

## H1 Results

`H1_diversity_patch` completed training and canonical evaluation.

- Training runtime `160.474` seconds
- Training loss `0.5263751833527176`
- Internal eval loss `0.412889301776886`
- Adapter aggregate metrics:
  - exact JSON validity `0.44`
  - invalid JSON rate `0.1`
  - tool-name accuracy `0.7142857142857143`
  - argument accuracy `0.6285714285714286`
  - wrapper leakage `0.0`
  - no-call correctness `0.9`
  - adversarial no-call correctness `0.7`
- Tool-holdout exact-valid `0.6`
- Heldout-validation exact-valid `0.64`
- No-anchor exact-valid `0.8636363636363636`

## Comparison Against H0

H1 materially outperformed H0 on the intended diversity-sensitive metrics:

- tool-holdout exact-valid: `0.6` vs `0.0`
- heldout-validation exact-valid: `0.64` vs `0.09`
- tool-name accuracy: `0.7142857142857143` vs `0.07142857142857142`
- argument accuracy: `0.6285714285714286` vs `0.06428571428571428`
- no-anchor exact-valid: `0.8636363636363636` vs `0.0`
- read-file exact-valid: `0.5185185185185185` vs `0.0`
- read-file symbol-name exact-valid: `0.8461538461538461` vs `0.0`

The run still regressed safety relative to the ideal invariant:

- no-call correctness: `0.9` vs `1.0` ideal
- adversarial no-call correctness: `0.7` vs `1.0` ideal

## Comparison Against H2

H1 and H2 split the metric families:

- H1 beat H2 on tool-holdout exact-valid, no-anchor exact-valid, wrapper leakage, no-call correctness, and adversarial no-call correctness.
- H2 beat H1 on heldout-validation exact-valid, tool-name accuracy, argument accuracy, and direct-answer suppression.

This is the core new evidence from the exception run.

## Scientific Interpretation

The exception datapoint does not support a single-factor story.

The strongest scientific interpretation is a combined bottleneck:

- diversity restoration helps the heldout/tool-holdout edge and tail-tool coverage;
- commitment pressure helps broader tool-call realization and heldout accuracy;
- neither intervention alone explains the full response surface.

In the Phase H category set, this is best described as `E`.

## Remaining Uncertainties

- Whether a safety-clean diversity variant would preserve the H1 tool-holdout lift
- Whether H1 and H2 can be combined without reintroducing wrapper leakage or adversarial no-call regressions
- Whether the combined explanation generalizes beyond this frozen i3 surface

## Recommended Research Interpretation

Treat the exception run as evidence for a combined bottleneck (`E`) rather than a clean A or B winner.

Use that interpretation for follow-on research planning only.

## Governance Note

Phase I remains formally closed.

The official Phase I determination remains:

`inconclusive_external_first`

This exception run does not reopen Phase I and does not authorize any additional internal runs.

## Repository Record

- Authority commit: `c19c741` (`Phase IX: record H1 exception authority`) pushed successfully to `origin/main`
- Documentation commit: `c54719f` (`Phase IX: document H1 exception results`) pushed successfully to `origin/main`
- Validation outcome: `git diff --check` PASS
