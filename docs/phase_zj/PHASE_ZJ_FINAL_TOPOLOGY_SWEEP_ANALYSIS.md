# Phase ZJ Final Topology Sweep Analysis

## Completed Sweep

| Arm | Exact JSON | Tool name | Arg | No-call | Adversarial no-call |
|---|---:|---:|---:|---:|---:|
| ZG Control | `0.05` | `0.18571428571428572` | `0.12857142857142856` | `0.7` | `0.1` |
| ZH Treatment A | `0.04` | `0.15` | `0.10714285714285714` | `0.6666666666666666` | `0.0` |
| ZI Treatment B | `0.04` | `0.12142857142857143` | `0.09285714285714286` | `0.6666666666666666` | `0.0` |
| ZJ Treatment C | `0.04` | `0.17142857142857143` | `0.09285714285714286` | `0.6833333333333333` | `0.05` |

## Trajectory

- Exact JSON validity flattened at `0.04` from ZH through ZJ.
- Tool-name accuracy fell from ZG to ZI and then recovered partially at ZJ.
- Argument accuracy declined from ZG and then flattened at ZI/ZJ.
- No-call correctness stayed in a narrow band around `0.67` to `0.70`.
- Adversarial no-call correctness remained poor across the sweep.

The sweep therefore does not show a topology setting that recovers H1/H2-style exact tool-call realization.

## Comparison With H1/H2

| Baseline | Exact JSON | Tool name | Arg | No-call | Adversarial no-call |
|---|---:|---:|---:|---:|---:|
| H1 | `0.44` | `0.7142857142857143` | `0.6285714285714286` | `0.9` | `0.7` |
| H2 | `0.48` | `0.7714285714285715` | `0.6928571428571428` | `0.8` | `0.4` |

ZJ is still far below both H1 and H2 on every capability metric.

## Comparison With Phase Q And Phase U

ZJ improves on Phase Q and Phase U for tool-call realization, but it does not close the gap to H1/H2.

- Better than Phase Q on exact JSON, tool-name accuracy, and argument accuracy.
- Worse than Phase Q on no-call correctness and adversarial no-call correctness.
- Much better than Phase U on capability.
- Much worse than Phase U on safety.

## Topology Hypothesis Assessment

**Weakened**

Topology is not a sufficient explanation for H1/H2 success.

The sweep shows some movement across the arms, so topology is not completely irrelevant, but the effect is not strong, stable, or large enough to explain the H1/H2 capability floor.

## Residual Interpretation

The most defensible reading is that topology is a secondary contributor at best.

The remaining gap is still dominated by some other factor or interaction that the topology sweep did not isolate.
