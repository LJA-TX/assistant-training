# Phase I Final Completion Report

## Executive Summary

Phase I resumed under the controlling continuation determination and executed `H2_commitment_patch` as a diagnostic/report-only probe.
`H2` completed training and canonical evaluation, but it tripped Phase H kill metrics on wrapper leakage and adversarial/no-call safety.
Because `H0` had already tripped a kill metric, the `H2` failure became the second kill-tripped run and blocked `H1_diversity_patch` under the run-level stop ceiling.

Formal Phase H attribution is therefore `inconclusive_external_first`.

The strongest observed signal is commitment-dominant, but it is not a formal winner because the first-screen pair was truncated before H1 could run and the H2 probe was not safety-clean.

## H0 Results

`H0_control_i3_micro` remains the comparative baseline.

- Training completed on the frozen i3 recovery bytes.
- Canonical evaluation completed.
- Adapter aggregate metrics:
  - exact JSON validity `0.045`
  - invalid JSON rate `0.145`
  - tool-name accuracy `0.07142857142857142`
  - argument accuracy `0.06428571428571428`
  - wrapper leakage `0.0`
  - no-call correctness `0.9166666666666666`
  - adversarial no-call correctness `0.75`
- Hard-stop outcome:
  - H0 tripped the Phase H kill metric on adversarial no-call safety.

## H2 Results

`H2_commitment_patch` completed training and canonical evaluation.

- Training runtime `159.4807` seconds
- Training loss `0.5947615747098569`
- Internal eval loss `0.4286271333694458`
- Adapter aggregate metrics:
  - exact JSON validity `0.48`
  - invalid JSON rate `0.085`
  - tool-name accuracy `0.7714285714285715`
  - argument accuracy `0.6928571428571428`
  - wrapper leakage `0.005`
  - no-call correctness `0.8`
  - adversarial no-call correctness `0.4`
- Key tool-slice metrics:
  - tool-holdout exact JSON validity `0.525`
  - heldout-validation exact JSON validity `0.75`
  - no-anchor exact-valid share `0.84375`
- Deltas versus H0:
  - exact JSON validity `+0.435`
  - invalid JSON rate `-0.060`
  - tool-name accuracy `+0.700`
  - argument accuracy `+0.629`
  - tool-holdout exact-valid `+0.525`
  - heldout-validation exact-valid `+0.660`
  - wrapper leakage `+0.005`
  - no-call correctness `-0.117`
  - adversarial no-call correctness `-0.350`
- Stop-rule outcome:
  - H2 tripped the Phase H kill metrics
  - H2 also became the second kill-tripped run, which blocked `H1_diversity_patch`

## H1 Results

`H1_diversity_patch` was not executed.

Reason:

- H0 had already tripped a kill metric.
- H2 tripped a second kill metric.
- The Phase H run-level stop rule forbids continuing to another internal-only run after two runs have tripped kill metrics.

## Attribution Findings

The data support a strong commitment-shift signal:

- `H2` moved tool-holdout exact-valid off zero.
- `H2` moved heldout-validation exact-valid sharply upward.
- `H2` moved no-anchor exact-valid sharply upward.
- `H2` materially improved tool-name and argument accuracy.

The same run introduced safety regressions:

- wrapper leakage appeared.
- no-call correctness dropped below `1.0`.
- adversarial no-call correctness dropped sharply below `1.0`.

Because H1 did not run, the first-screen pair never completed and the published A/B/C/D/E thresholds cannot be fully applied.

## Dominant Bottleneck Assessment

Provisional signal: `B`, commitment-dominant.

Formal decision: `inconclusive_external_first`.

This is the correct split under the published framework because the commitment signal is strong but the experiment did not complete the required first-screen comparison and the H2 probe was not safety-clean.

## Recommended Next Phase

External-first work focused on preserving the commitment gains while eliminating the safety regression is the safest next step.
No additional internal-only run should be launched unless a new governance route explicitly authorizes it.

## Confidence Assessment

Medium.

Confidence is high that:

- H0 is a valid comparator baseline.
- H2 materially improves tool-side capability.
- H2 materially worsens safety invariants.
- H1 was blocked by the stop-rule ceiling.

Confidence is lower on a formal winner because the first-screen pair was truncated before H1 could run.

## Unresolved Questions

- Would H1 have outperformed H2 on tool-holdout exact-valid?
- Can the commitment gains be retained without introducing wrapper leakage?
- Is the adversarial no-call regression intrinsic to the commitment patch or a trainer-surface side effect?
- What external-first remediation path best preserves the observed tool-holdout lift?
