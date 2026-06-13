# Phase Z Baseline Comparison

## Comparison Table

| Metric | H0 | H1 | H2 | Phase Q | Phase U | Phase Z Control |
|---|---:|---:|---:|---:|---:|---:|
| exact JSON validity | `0.045` | `0.44` | `0.48` | `0.03` | `0.0` | `0.055` |
| tool-name accuracy | `0.07142857142857142` | `0.7142857142857143` | `0.7714285714285715` | `0.07142857142857142` | `0.0` | `0.2` |
| argument accuracy | `0.06428571428571428` | `0.6285714285714286` | `0.6928571428571428` | `0.04285714285714286` | `0.0` | `0.1357142857142857` |
| wrapper leakage | `0.0` | `0.0` | `0.005` | `0.0` | `0.0` | `0.0` |
| no-call correctness | `0.9166666666666666` | `0.9` | `0.8` | `0.7666666666666667` | `1.0` | `0.6666666666666666` |
| adversarial no-call correctness | `0.75` | `0.7` | `0.4` | `0.3` | `1.0` | `0.0` |

## Control Arm Interpretation

The control arm is clearly better than Phase Q on exact JSON, tool-name accuracy, and argument accuracy:

- exact JSON validity: `0.055` vs `0.03`
- tool-name accuracy: `0.2` vs `0.0714`
- argument accuracy: `0.1357` vs `0.0429`

It is still far below H1/H2 on the same capability metrics:

- H1 exact JSON validity: `0.44`
- H2 exact JSON validity: `0.48`
- H1 tool-name accuracy: `0.7143`
- H2 tool-name accuracy: `0.7714`
- H1 argument accuracy: `0.6286`
- H2 argument accuracy: `0.6929`

The safety picture is weaker than Phase Q and Phase U:

- adversarial no-call correctness fell to `0.0`
- wrapper leakage remained `0.0`
- no-call correctness fell to `0.6667`

## Failure-Mode Comparison

| Run | Direct-answer substitution | Scalar substitution | Malformed partial JSON | Near-canonical wrapper/envelope drift |
|---|---:|---:|---:|---:|
| Phase Q | `37` | `0` | `3` | `94` |
| Phase U | `125` | `0` | `15` | `0` |
| Phase Z Control | `38` | `38` | `3` | `50` |

The control arm shifts the error mix away from the Phase Q pattern:

- direct-answer substitution remains high;
- scalar substitution appears strongly;
- wrapper/envelope drift is lower than Phase Q but still present;
- adversarial refusal behavior collapses completely.

## Baseline Reading

The control arm is not a return to H1/H2 capability.

It is a partial recovery over Phase Q with a sharper safety regression than either Phase Q or Phase U.

The result supports continuing the ablation sequence rather than promotion.
