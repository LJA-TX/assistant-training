# Phase ZH Ablation Progress Report

## Current Result

Treatment A completed successfully and is a valid ablation datapoint.

## Comparison Summary

| Metric | ZG Control | Treatment A | Delta |
|---|---:|---:|---:|
| exact JSON validity | `0.05` | `0.04` | `-0.01` |
| tool-name accuracy | `0.18571428571428572` | `0.15` | `-0.03571428571428571` |
| argument accuracy | `0.12857142857142856` | `0.10714285714285714` | `-0.021428571428571432` |
| wrapper leakage | `0.0` | `0.0` | `0.0` |
| no-call correctness | `0.7` | `0.6666666666666666` | `-0.033333333333333326` |
| adversarial no-call correctness | `0.1` | `0.0` | `-0.1` |

## Reading Against Baselines

Treatment A remains far below the H1/H2 capability floor:

- H1 exact JSON validity: `0.44`
- H2 exact JSON validity: `0.48`
- Treatment A exact JSON validity: `0.04`

It is only a narrow capability improvement over Phase Q and remains substantially below H1/H2 on tool-name and argument realization.

## Failure-Mode Shift

| Run | Direct-answer substitution | Scalar substitution | Malformed partial JSON | Near-canonical wrapper or envelope drift |
|---|---:|---:|---:|---:|
| ZG Control | `37` | `36` | `4` | `53` |
| Treatment A | `50` | `42` | `9` | `31` |

Treatment A pushes the model away from wrapper drift and toward substitution-style failures. That does not improve capability and it does not preserve the ZG safety level.

## Progress Assessment

- Promotion outcome: `Do Not Promote`
- Attribution outcome: `Negative relative response`
- Operational outcome: `Success`

## Next Reading

The topology sweep still needs the remaining arms before any topology conclusion is justified.
