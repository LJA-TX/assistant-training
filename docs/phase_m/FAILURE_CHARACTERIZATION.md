# Failure Characterization

## Executive Summary

Phase L failed in a specific way:

- safety surfaces stayed exact,
- tool-call surfaces collapsed,
- the dominant error mode was not wrapper leakage but schema realization failure.

This is not a safety regression run.
It is a capability-collapse run with preserved refusal behavior.

## Core Metrics

| Metric | Phase L |
|---|---:|
| exact JSON validity | `0.0` |
| invalid JSON rate | `0.345` |
| tool-name accuracy | `0.04285714285714286` |
| argument accuracy | `0.007142857142857143` |
| wrapper leakage | `0.0` |
| no-call correctness | `1.0` |
| adversarial no-call correctness | `1.0` |

## Dominant Failure Modes

| Failure mode | Count | Share of non-exact tool rows |
|---|---:|---:|
| near-canonical wrapper or envelope drift | `70` | `50.0%` |
| direct-answer substitution | `55` | `39.3%` |
| malformed partial JSON | `14` | `10.0%` |
| scalar substitution | `1` | `0.7%` |
| other | `0` | `0.0%` |

The largest single subtype is near-canonical wrapper or envelope drift.
The next-largest subtype is direct-answer substitution.

## Capability Failures

Tool-call capability collapsed across every primary family:

- heldout-validation exact-valid: `0.0`
- tool-holdout exact-valid: `0.0`
- no-anchor exact-valid share: `0.0`
- tool-name accuracy: `0.04285714285714286`
- argument accuracy: `0.007142857142857143`

Row-level evidence shows the model often produced:

- partial JSON with the wrong envelope,
- JSON-like text missing the canonical `tool_calls` wrapper,
- natural-language direct answers,
- occasional scalar answers.

## Safety Outcomes

Safety is the opposite story.

- `no_call_correctness = 1.0`
- `adversarial_no_call_correctness = 1.0`
- `wrapper_leakage = 0.0`

So the model learned the refusal boundary cleanly.
It did not learn the tool-call boundary cleanly.

## Comparison Against H0, H1, and H2

| Metric | H0 | H1 | H2 | Phase L |
|---|---:|---:|---:|---:|
| exact JSON validity | `0.045` | `0.44` | `0.48` | `0.0` |
| tool-holdout exact-valid | `0.0` | `0.6` | `0.525` | `0.0` |
| heldout-validation exact-valid | `0.09` | `0.64` | `0.75` | `0.0` |
| tool-name accuracy | `0.07142857142857142` | `0.7142857142857143` | `0.7714285714285715` | `0.04285714285714286` |
| argument accuracy | `0.06428571428571428` | `0.6285714285714286` | `0.6928571428571428` | `0.007142857142857143` |
| no-call correctness | `0.9166666666666666` | `0.9` | `0.8` | `1.0` |
| adversarial no-call correctness | `0.75` | `0.7` | `0.4` | `1.0` |
| wrapper leakage | `0.0` | `0.0` | `0.005` | `0.0` |

Interpretation:

- H0 had weak capability and imperfect safety.
- H1 improved diversity-sensitive tool behavior but still failed safety.
- H2 improved commitment-sensitive tool behavior but regressed safety.
- Phase L preserved the safety boundary but lost almost all tool-call competence.

## Notable Contrast

Phase L is not a milder version of H1 or H2.
It is a different failure shape:

- H1/H2 failed because capability gains came with safety regressions.
- Phase L failed because safety was retained while capability was erased.

That contrast matters for root cause attribution.

## Sources Used

- `docs/phase_l/PHASE_L_EXECUTION_REVIEW.md`
- `docs/phase_l/PHASE_L_COMPLETION_REPORT.md`
- `docs/phase_i/PHASE_I_FINAL_COMPLETION_REPORT.md`
- `docs/phase_ix/PHASE_IX_COMPLETION_REPORT.md`
- `evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/summary.json`
- `evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/comparison_rows.jsonl`
