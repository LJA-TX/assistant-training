# Phase ZG Baseline Comparison

## Scope

This comparison uses the frozen canonical evaluation contract and the repository-recorded baseline results from:

- H1: Phase IX operator-authorized exception run
- H2: Phase I commitment patch
- Phase Q: Dataset v1.2 governed execution
- Phase U: Schema-repair micro-patch
- Phase Z Control: prior preservation-ablation control arm
- Phase ZG Control: compact-local topology control arm

## Comparison Table

| Metric | H1 | H2 | Phase Q | Phase U | Phase Z Control | Phase ZG Control | Reading |
|---|---:|---:|---:|---:|---:|---:|---|
| exact JSON validity | `0.44` | `0.48` | `0.03` | `0.0` | `0.055` | `0.05` | ZG is slightly below Z on exact-call realization and far below H1/H2 |
| tool-name accuracy | `0.7142857142857143` | `0.7714285714285715` | `0.07142857142857142` | `0.0` | `0.2` | `0.18571428571428572` | ZG remains in the low-capability band |
| argument accuracy | `0.6285714285714286` | `0.6928571428571428` | `0.04285714285714286` | `0.0` | `0.1357142857142857` | `0.12857142857142856` | ZG remains far below H1/H2 |
| wrapper leakage | `0.0` | `0.005` | `0.0` | `0.0` | `0.0` | `0.0` | ZG stays clean on wrapper leakage |
| no-call correctness | `0.9` | `0.8` | `0.7666666666666667` | `1.0` | `0.6666666666666666` | `0.7` | ZG improves modestly over Z on refusal safety |
| adversarial no-call correctness | `0.7` | `0.4` | `0.3` | `1.0` | `0.0` | `0.1` | ZG recovers some adversarial safety relative to Z, but remains far below H1/H2 |

## Failure-Mode Comparison

| Run | Direct-answer substitution | Scalar substitution | Malformed partial JSON | Near-canonical wrapper or envelope drift |
|---|---:|---:|---:|---:|
| H1 | `12` | `0` | `8` | `32` |
| H2 | `9` | `0` | `6` | `29` |
| Phase Q | `37` | `0` | `3` | `94` |
| Phase U | `125` | `0` | `15` | `0` |
| Phase Z Control | `38` | `38` | `3` | `50` |
| Phase ZG Control | `37` | `36` | `4` | `53` |

## Interpretation

The ZG control does not recover the H1/H2 capability family.

- It remains an order of magnitude below H1/H2 on exact JSON, tool-name accuracy, and argument accuracy.
- It is only a marginal improvement over Phase Q on capability, and it does not close the gap to the H1/H2 floor.
- Compared with the earlier Z control, it loses a little exact-call realization but gains some refusal safety.
- The failure surface still splits between direct-answer substitution, scalar substitution, and wrapper/envelope drift instead of converging on exact canonical tool calls.

## Baseline Reading

The compact-local topology control establishes a valid baseline for the ablation, but it does not justify promotion.

The result supports continuing the topology sequence to the treatment arms rather than treating the control as sufficient evidence of recovery.
