# Phase ZI Ablation Progress Report

## Current Result

Treatment B completed successfully and is a valid ablation datapoint.

## Comparison Summary

| Metric | ZG Control | ZH Treatment A | Treatment B | Delta vs ZG | Delta vs ZH |
|---|---:|---:|---:|---:|---:|
| exact JSON validity | `0.05` | `0.04` | `0.04` | `-0.01` | `0.0` |
| tool-name accuracy | `0.18571428571428572` | `0.15` | `0.12142857142857143` | `-0.06428571428571428` | `-0.02857142857142858` |
| argument accuracy | `0.12857142857142856` | `0.10714285714285714` | `0.09285714285714286` | `-0.0357142857142857` | `-0.01428571428571429` |
| wrapper leakage | `0.0` | `0.0` | `0.0` | `0.0` | `0.0` |
| no-call correctness | `0.7` | `0.6666666666666666` | `0.6666666666666666` | `-0.033333333333333326` | `0.0` |
| adversarial no-call correctness | `0.1` | `0.0` | `0.0` | `-0.1` | `0.0` |

## Reading Against Baselines

Treatment B remains far below the H1/H2 capability floor:

- H1 exact JSON validity: `0.44`
- H2 exact JSON validity: `0.48`
- Treatment B exact JSON validity: `0.04`

Compared with Phase Q, it improves exact-call realization somewhat but still does not approach the H1/H2 regime.

Compared with Phase U, it is much better on tool-call surfaces but much worse on refusal safety.

## Failure-Mode Shift

| Run | Direct-answer substitution | Scalar substitution | Malformed partial JSON | Near-canonical wrapper or envelope drift |
|---|---:|---:|---:|---:|
| ZG Control | `37` | `36` | `4` | `53` |
| ZH Treatment A | `50` | `42` | `9` | `31` |
| Treatment B | `53` | `48` | `2` | `29` |

Treatment B continues the shift away from wrapper drift and toward substitution-style failures. That does not improve capability and it does not recover adversarial safety.

## Progress Assessment

- Promotion outcome: `Do Not Promote`
- Attribution outcome: `Flat-to-negative relative response`
- Operational outcome: `Success`

## Next Reading

Treatment C is still required before any final topology interpretation is justified.
