# Phase U Baseline Comparison

## Scope

This comparison uses the frozen canonical evaluation contract and compares Phase U against:

- H0 control
- H1 diversity patch
- H2 commitment patch
- Phase Q Dataset v1.2

## Metric Comparison

| Metric | H0 | H1 | H2 | Phase Q v1.2 | Phase U micro-patch | Reading |
|---|---:|---:|---:|---:|---:|---|
| exact JSON validity | `0.045` | `0.44` | `0.48` | `0.03` | `0.0` | Phase U falls below every baseline |
| tool-name accuracy | `0.07142857142857142` | `0.7142857142857143` | `0.7714285714285715` | `0.07142857142857142` | `0.0` | Phase U loses tool selection entirely |
| argument accuracy | `0.06428571428571428` | `0.6285714285714286` | `0.6928571428571428` | `0.04285714285714286` | `0.0` | Phase U loses argument realization entirely |
| wrapper leakage | `0.0` | `0.0` | `0.005` | `0.0` | `0.0` | Safety remains clean |
| no-call correctness | `0.9166666666666666` | `0.9` | `0.8` | `0.7666666666666667` | `1.0` | Phase U improves safety above every baseline |
| adversarial no-call correctness | `0.75` | `0.7` | `0.4` | `0.3` | `1.0` | Phase U improves adversarial safety above every baseline |

## Failure-Mode Comparison

| Run | Direct-answer substitution | Scalar substitution | Malformed partial JSON | Near-canonical wrapper drift | Reading |
|---|---:|---:|---:|---:|---|
| H1 | `12` | `0` | `8` | `32` | Diverse schema success with some envelope drift |
| H2 | `9` | `0` | `6` | `29` | Stronger commitment-side realization, but safety regresses |
| Phase Q v1.2 | `37` | `0` | `3` | `94` | Wrapper drift dominates the failure surface |
| Phase U micro-patch | `125` | `0` | `15` | `0` | Direct-answer substitution dominates; wrapper drift disappears |

## Reading

Phase U does not recover the Phase R schema-realization signal.

The patch eliminates the wrapper-drift symptom seen in Phase Q, but it does so by collapsing into direct-answer substitution rather than by producing the canonical `tool_calls` envelope. That is not schema recovery; it is capability collapse with preserved refusal behavior.

The safety surfaces are now stronger than every baseline, but the tool-call surfaces are weaker than H0 and far weaker than H1/H2.

