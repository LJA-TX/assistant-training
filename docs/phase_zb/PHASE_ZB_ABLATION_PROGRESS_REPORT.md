# Phase ZB Ablation Progress Report

## Executive Summary

Treatment B provides evidence for a **flat response** relative to Treatment A.

The anchor-concentration sweep is still scientifically useful, but Treatment B does not show a new capability jump beyond the Treatment A plateau. The run is still better than Control, and still far below H1/H2.

## Trajectory Summary

| Arm | Anchor rows | exact JSON | tool-name | argument | no-call | adversarial no-call |
|---|---:|---:|---:|---:|---:|---:|
| Control | `726` | `0.055` | `0.2` | `0.1357142857142857` | `0.6666666666666666` | `0.0` |
| Treatment A | `819` | `0.07` | `0.21428571428571427` | `0.15` | `0.7333333333333333` | `0.25` |
| Treatment B | `912` | `0.07` | `0.21428571428571427` | `0.15` | `0.7333333333333333` | `0.25` |

## Interpretation

### Control to Treatment A

The sweep initially showed a modest positive response:

- better exact JSON validity
- better tool-name and argument accuracy
- better no-call and adversarial no-call behavior

### Treatment A to Treatment B

The sweep then flattened:

- no change in exact JSON validity
- no change in tool-name accuracy
- no change in argument accuracy
- no change in wrapper leakage
- no change in no-call correctness
- no change in adversarial no-call correctness

That makes Treatment B a plateau point, not a new recovery point.

## Failure-Shape Note

Treatment B does not introduce a new failure regime. It stays in the same envelope-drift / substitution mix as Treatment A:

- direct-answer substitution remains substantial
- scalar substitution remains substantial
- near-canonical wrapper drift remains the dominant non-exact category

## Progress Assessment

The sweep has not recovered H1/H2-style tool-call competence.

At the same time, Treatment B does not invalidate the ablation. The run is contamination-clean, operationally valid, and still informative because it separates:

- a modest gain from Control
- a plateau from Treatment A to Treatment B

## Boundary Confirmation

- No Treatment C was launched.
- No evaluator logic changed.
- No scoring logic changed.
- No governance or threshold changes were made.
