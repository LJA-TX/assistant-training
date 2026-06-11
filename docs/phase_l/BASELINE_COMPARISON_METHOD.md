# Baseline Comparison Method

## Comparison Authority

Use the frozen canonical eval contract:

- `evals/canonical_eval_manifest_v1.json`

The manifest fixes the decode defaults and forbids promotion by strong-system-prompt override.

## Canonical Decode Defaults

| Field | Value |
|---|---|
| temperature | `0.0` |
| top_p | `1.0` |
| do_sample | `false` |
| repetition_penalty | `1.0` |
| max_new_tokens | `64` |
| seed | `1234` |

## Comparison Procedure

1. Train the selected draft config on Dataset v1.1.
2. Run the canonical evaluator with the frozen manifest and the same decode defaults.
3. Compare the result against H0, H1, and H2 using the same metric families reported in the Phase I and Phase IX completion reports.
4. Treat H1 as the diversity/safety comparator and H2 as the commitment comparator.
5. Treat H0 as the control baseline.
6. Do not retune thresholds after seeing the result.

## Baseline Metric Table

| Metric | H0 | H1 | H2 |
|---|---:|---:|---:|
| exact JSON validity | `0.045` | `0.44` | `0.48` |
| tool-holdout exact-valid | `0.0` | `0.6` | `0.525` |
| heldout-validation exact-valid | `0.09` | `0.64` | `0.75` |
| tool-name accuracy | `0.07142857142857142` | `0.7142857142857143` | `0.7714285714285715` |
| argument accuracy | `0.06428571428571428` | `0.6285714285714286` | `0.6928571428571428` |
| no-anchor exact-valid | `0.0` | `0.8636363636363636` | `0.84375` |
| wrapper leakage | `0.0` | `0.0` | `0.005` |
| no-call correctness | `0.9166666666666666` | `0.9` | `0.8` |
| adversarial no-call correctness | `0.75` | `0.7` | `0.4` |

## Comparison Rules

1. Compare the candidate to H0 for gross capability lift.
2. Compare the candidate to H1 for diversity-sensitive lift and safety retention.
3. Compare the candidate to H2 for commitment-sensitive lift and broader heldout performance.
4. Use the stronger of H1 and H2 as the family-specific benchmark where the metric family split cleanly.
5. Treat any result that only looks good under a relaxed benchmark as non-promotable.

## Interpretation Rule

The candidate should be read as successful only if it closes the combined bottleneck: the H1 family and the H2 family both improve without reintroducing safety regressions.

That means:

- H1-like gains should not be traded away for H2-like gains.
- H2-like gains should not be traded away for H1-like gains.
- A valid result must clear the frozen safety contract on the same evaluator contract that produced the baselines.
