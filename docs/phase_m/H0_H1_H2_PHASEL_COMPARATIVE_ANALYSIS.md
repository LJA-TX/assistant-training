# H0 H1 H2 Phase L Comparative Analysis

## Executive Summary

The four runs form a clean comparison:

- H0: weak capability, weak safety.
- H1: better diversity-sensitive capability, but safety not clean.
- H2: better commitment-sensitive capability, but safety not clean.
- Phase L: safety clean, capability collapsed.

Phase L did not land on a better point in the H1/H2 trade space.
It landed off the trade space entirely.

## Comparison Table

| Metric | H0 | H1 | H2 | Phase L |
|---|---:|---:|---:|---:|
| exact JSON validity | `0.045` | `0.44` | `0.48` | `0.0` |
| tool-holdout exact-valid | `0.0` | `0.6` | `0.525` | `0.0` |
| heldout-validation exact-valid | `0.09` | `0.64` | `0.75` | `0.0` |
| tool-name accuracy | `0.07142857142857142` | `0.7142857142857143` | `0.7714285714285715` | `0.04285714285714286` |
| argument accuracy | `0.06428571428571428` | `0.6285714285714286` | `0.6928571428571428` | `0.007142857142857143` |
| no-anchor exact-valid | `0.0` | `0.8636363636363636` | `0.84375` | `0.0` |
| wrapper leakage | `0.0` | `0.0` | `0.005` | `0.0` |
| no-call correctness | `0.9166666666666666` | `0.9` | `0.8` | `1.0` |
| adversarial no-call correctness | `0.75` | `0.7` | `0.4` | `1.0` |

## Tool-Call Behavior

- H0 barely produced valid tool calls.
- H1 restored tool-holdout and no-anchor behavior.
- H2 restored heldout-validation and tool-name/argument accuracy.
- Phase L lost tool-call realization on every primary family.

Phase L is therefore not a combined improvement over H1 and H2.

## Schema Adherence

- H0: mostly invalid JSON, with almost no tool-call realization.
- H1: significantly improved schema adherence and exact-validity.
- H2: similar or stronger schema adherence than H1 on heldout and accuracy, but with safety regressions.
- Phase L: strict schema adherence collapsed back to near-zero utility even though safety stayed clean.

## Safety Calibration

- H0 already had a safety problem on adversarial no-call.
- H1 and H2 both still missed the safety target.
- Phase L achieved the safety target exactly:
  - `no_call_correctness = 1.0`
  - `adversarial_no_call_correctness = 1.0`
  - `wrapper_leakage = 0.0`

That is the one area where Phase L is better than all earlier runs.

## Direct-Answer Tendencies

- H0 had direct-answer-like leakage on tool rows and poor canonicalization.
- H1 and H2 reduced different parts of the direct-answer surface, with H2 explicitly improving direct-answer suppression relative to H1.
- Phase L regressed the direct-answer surface on tool rows:
  - `55` direct-answer substitutions
  - `1` scalar substitution

That is far worse than H2 and inconsistent with the Phase L goal.

## Refusal Tendencies

The refusal surface is now exact:

- no-call rows are refused correctly.
- adversarial no-call rows are refused correctly.
- direct-answer rows are refused correctly when they should be refused.

But the model does not transfer that refusal discipline into tool-call formatting.
It refuses the right things and fails the wrong things.

## Sources Used

- `docs/phase_i/PHASE_I_FINAL_COMPLETION_REPORT.md`
- `docs/phase_ix/PHASE_IX_COMPLETION_REPORT.md`
- `docs/phase_l/PHASE_L_EXECUTION_REVIEW.md`
- `evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/summary.json`
