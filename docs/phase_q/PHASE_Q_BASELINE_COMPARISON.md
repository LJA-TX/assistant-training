# Phase Q Baseline Comparison

## Scope

This comparison uses the frozen canonical evaluation contract and the published baseline results from:

- H0: Phase I control baseline
- H1: Phase IX operator-authorized exception run
- H2: Phase I commitment patch
- Phase L: Dataset v1.1 governed execution
- Phase Q: Dataset v1.2 governed execution

## Comparison Table

| Metric | H0 | H1 | H2 | Phase L v1.1 | Phase Q v1.2 | Reading |
|---|---:|---:|---:|---:|---:|---|
| exact JSON validity | `0.045` | `0.44` | `0.48` | `0.0` | `0.03` | Q improves over Phase L, but stays below H0/H1/H2 |
| invalid JSON rate | `0.145` | `0.1` | `0.085` | `0.345` | `0.2` | Q improves over Phase L, but stays above H0/H1/H2 |
| tool-name accuracy | `0.07142857142857142` | `0.7142857142857143` | `0.7714285714285715` | `0.04285714285714286` | `0.07142857142857142` | Q returns only to H0 control level |
| argument accuracy | `0.06428571428571428` | `0.6285714285714286` | `0.6928571428571428` | `0.007142857142857143` | `0.04285714285714286` | Q remains far below H1/H2 |
| tool-holdout exact-valid | `0.0` | `0.6` | `0.525` | `0.0` | `0.0` | Q shows no recovery on the tool-holdout slice |
| heldout-validation exact-valid | `0.09` | `0.64` | `0.75` | `0.0` | `0.06` | Q improves over Phase L, but remains below H0/H1/H2 |
| read-file exact-valid | `0.0` | `0.5185185185185185` | not reported | not reported | `0.0` | Q does not recover the H1 read-file lift |
| read-file symbol-name exact-valid | `0.0` | `0.8461538461538461` | not reported | not reported | `0.0` | Q does not recover the H1 symbol-name lift |
| no-anchor exact-valid share | `0.0` | `0.8636363636363636` | `0.84375` | `0.0` | `0.0` | Q does not recover the anchor-free tail |
| wrapper leakage | `0.0` | `0.0` | `0.005` | `0.0` | `0.0` | Q stays clean on wrapper leakage |
| no-call correctness | `0.9166666666666666` | `0.9` | `0.8` | `1.0` | `0.7666666666666667` | Q regresses below all baselines |
| adversarial no-call correctness | `0.75` | `0.7` | `0.4` | `1.0` | `0.3` | Q regresses below all baselines |

## Failure-Mode Comparison

| Run | Direct-answer substitution | Scalar substitution | Read |
|---|---:|---:|---|
| H1 | `12` | `0` | Diversity-lift signal without wrapper leakage |
| H2 | `9` | `0` | Stronger commitment-side realization, but safety regression |
| Phase L v1.1 | `55` | `1` | Capability collapse with clean safety surfaces |
| Phase Q v1.2 | `37` | `0` | Some capability recovery, but still far below H1/H2 and safety regresses |

## Interpretation

Phase Q is better than Phase L v1.1 on JSON-forming behavior, but it does not recover the H1 or H2 capability family. It also fails the safety contract because both no-call metrics fall below the published promotion thresholds.

The most important contrasts are:

- H1 still dominates the diversity-sensitive tail metrics.
- H2 still dominates the broader commitment-sensitive metrics.
- Phase Q does not recover either family cleanly.
- Phase Q regresses safety below all baselines on the no-call surfaces.

## Conclusion

The anchor-weighted hybrid moved the candidate away from the Phase L collapse, but not far enough to satisfy the frozen promotion criteria or to preserve the safety gains achieved by Phase L.
