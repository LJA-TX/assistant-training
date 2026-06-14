# Completed Ablation Summary

## Bottom Line

The completed Control / A / B / C sweep supports **anchor concentration as contributory, but not sufficient**.

Anchor concentration improved exact-call realization, but the effect was non-monotonic and came with safety regression at the highest anchor level. The full sweep does not recover the H1/H2 capability regime.

## Evidence Summary

| Arm | Anchor rows | exact JSON | tool-name | argument | no-call | adversarial no-call | wrapper leakage | Dominant failure shape |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Control | `726` | `0.055` | `0.2` | `0.1357142857142857` | `0.6666666666666666` | `0.0` | `0.0` | direct-answer + scalar substitution |
| Treatment A | `819` | `0.07` | `0.21428571428571427` | `0.15` | `0.7333333333333333` | `0.25` | `0.005` | direct-answer + scalar substitution + drift |
| Treatment B | `912` | `0.07` | `0.21428571428571427` | `0.15` | `0.7333333333333333` | `0.25` | `0.005` | same plateau as A |
| Treatment C | `1011` | `0.085` | `0.2857142857142857` | `0.18571428571428572` | `0.6666666666666666` | `0.0` | `0.0` | more exact-call output, but safety collapse returns |

Supporting run artifacts:

- [Phase Z completion report](/opt/ai-stack/assistant-training/docs/phase_z/PHASE_Z_COMPLETION_REPORT.md)
- [Phase ZA completion report](/opt/ai-stack/assistant-training/docs/phase_za/PHASE_ZA_COMPLETION_REPORT.md)
- [Phase ZB completion report](/opt/ai-stack/assistant-training/docs/phase_zb/PHASE_ZB_COMPLETION_REPORT.md)
- [Phase ZC completion report](/opt/ai-stack/assistant-training/docs/phase_zc/PHASE_ZC_COMPLETION_REPORT.md)
- [Treatment C eval summary](/opt/ai-stack/assistant-training/evals/runs/phase_zc_treatment_c_eval_20260613T212800Z/summary.json)

## Trajectory

1. Control establishes the baseline: weak exact-call behavior, no adversarial safety.
2. Treatment A produces the first positive move.
3. Treatment B plateaus at the Treatment A level.
4. Treatment C improves exact-call realization further, but safety falls apart again.

## Comparison To H1/H2

H1/H2 remain far above the sweep on the exact-call metrics:

- H1 exact JSON validity: `0.44`
- H1 tool-name accuracy: `0.7142857142857143`
- H1 argument accuracy: `0.6285714285714286`
- H2 exact JSON validity: `0.48`
- H2 tool-name accuracy: `0.7714285714285715`
- H2 argument accuracy: `0.6928571428571428`

The sweep therefore shows that anchor concentration alone does not explain the successful H1/H2 regime.
