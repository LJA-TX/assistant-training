# Phase ZC Final Ablation Analysis

## Executive Summary

The completed anchor-concentration sweep supports a **mixed response**.

Treatment C shows that increasing anchor concentration can still improve exact tool-call realization after the Treatment A/B plateau, but the effect is not monotonic across all target metrics and it does not recover the H1/H2 regime.

## Sweep Summary

| Arm | Anchor rows | exact JSON | tool-name | argument | no-call | adversarial no-call | wrapper leakage |
|---|---:|---:|---:|---:|---:|---:|---:|
| Control | `726` | `0.055` | `0.2` | `0.1357142857142857` | `0.6666666666666666` | `0.0` | `0.0` |
| Treatment A | `819` | `0.07` | `0.21428571428571427` | `0.15` | `0.7333333333333333` | `0.25` | `0.005` |
| Treatment B | `912` | `0.07` | `0.21428571428571427` | `0.15` | `0.7333333333333333` | `0.25` | `0.005` |
| Treatment C | `1011` | `0.085` | `0.2857142857142857` | `0.18571428571428572` | `0.6666666666666666` | `0.0` | `0.0` |

## Interpretation

### Control to Treatment A

The first anchor increase produced a modest positive response:

- better exact JSON validity
- better tool-name accuracy
- better argument accuracy
- better no-call calibration

### Treatment A to Treatment B

The sweep then flattened:

- no additional gain on the exact-call metrics
- no additional gain on no-call calibration

### Treatment B to Treatment C

The sweep then moved again, but not uniformly:

- exact JSON validity improved
- tool-name accuracy improved
- argument accuracy improved
- no-call correctness dropped back to Control
- adversarial no-call correctness dropped to zero
- wrapper leakage remained zero

That is the definition of a mixed response, not a linear response or a simple threshold response.

## Anchor-Concentration Assessment

Anchor concentration is a real contributor to capability recovery. The curve is not flat end-to-end, and the highest-anchor arm is better than Control on exact-call metrics.

Anchor concentration is not a sufficient explanation for H1/H2-style success, because:

- Treatment C still sits far below H1/H2 on exact JSON validity, tool-name accuracy, and argument accuracy.
- Treatment C does not preserve the safety gains seen in Treatment A/B.
- The response is non-monotonic across the sweep.

## The Smallest Model Consistent With The Evidence

The smallest model that fits the observed evidence is:

- anchor concentration helps,
- but it acts together with at least one other factor,
- and it does not by itself explain the H1/H2 success regime.

The data are not consistent with a single-factor story where anchor concentration alone accounts for the H1/H2 lift.

## Boundary Confirmation

- No Treatment D exists.
- No evaluator logic changed.
- No scoring logic changed.
- No governance or threshold changes were made.
