# Phase ZA Ablation Progress Report

## Trajectory Summary

Phase ZA Treatment A moves in the right direction relative to the Phase Z Control baseline.

| Metric | Control | Treatment A | Delta |
|---|---:|---:|---:|
| exact JSON validity | `0.055` | `0.07` | `+0.015` |
| tool-name accuracy | `0.2` | `0.21428571428571427` | `+0.014285714285714277` |
| argument accuracy | `0.1357142857142857` | `0.15` | `+0.01428571428571429` |
| wrapper leakage | `0.0` | `0.005` | `+0.005` |
| no-call correctness | `0.6666666666666666` | `0.7333333333333333` | `+0.06666666666666665` |
| adversarial no-call correctness | `0.0` | `0.25` | `+0.25` |

## Failure-Mode Shift

| Failure mode | Control | Treatment A | Delta |
|---|---:|---:|---:|
| direct-answer substitution | `38` | `34` | `-4` |
| scalar substitution | `38` | `39` | `+1` |
| malformed partial JSON | `3` | `4` | `+1` |
| near-canonical wrapper/envelope drift | `50` | `49` | `-1` |

## Interpretation

Treatment A provides evidence for a **positive anchor-concentration response** relative to Control.

The signal is not large, and it is not uniformly clean:

- wrapper leakage appears once;
- scalar substitution increases slightly;
- malformed partial JSON increases slightly.

But the main capability metrics move upward, and the no-call surfaces improve as well. That is enough to justify continuing the sweep.

## Baseline Context

Relative to the Phase Z Control result, Treatment A is better on the main tool-call metrics and on no-call calibration.

Relative to H1/H2, Treatment A is still far below the recovered tool-call floor:

- H1 exact JSON validity: `0.44`
- H2 exact JSON validity: `0.48`
- H1 tool-name accuracy: `0.7142857142857143`
- H2 tool-name accuracy: `0.7714285714285715`

This means the trajectory is promising but incomplete.

## Scientific Judgment

The Treatment A result is best described as a **positive but modest response**.

It does not answer the ablation. It does show that increasing anchor concentration from the Control baseline can move the model in the desired direction.
