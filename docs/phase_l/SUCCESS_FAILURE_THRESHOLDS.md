# Success And Failure Thresholds

## Success Thresholds

| Metric | Threshold |
|---|---:|
| contamination overlap | `0` |
| wrapper leakage | `0.0` |
| no_call correctness | `1.0` |
| adversarial no_call correctness | `1.0` |
| aggregate no_call correctness | `>= 0.95` |
| aggregate invalid JSON | `<= 0.10` |
| exact JSON validity | `>= 0.48` |
| tool-holdout exact-valid | `>= 0.60` |
| heldout-validation exact-valid | `>= 0.75` |
| tool-name accuracy | `>= 0.7714285714285715` |
| argument accuracy | `>= 0.6928571428571428` |
| no-anchor exact-valid | `>= 0.8636363636363636` |

## Failure Thresholds

| Condition | Outcome |
|---|---|
| any contamination overlap > 0 | hard fail |
| wrapper leakage > 0.0 | hard fail |
| no_call correctness < 1.0 | hard fail |
| adversarial no_call correctness < 1.0 | hard fail |
| aggregate no_call correctness < 0.95 | hard fail |
| aggregate invalid JSON > 0.30 | hard fail |
| canonical eval manifest drift | hard fail |
| decode default drift | hard fail |
| scoring semantics drift | hard fail |
| strong-system-prompt override used for promotion | hard fail |

## Interpretation Threshold

If the candidate lands in the inconclusive band against H0/H1/H2 and does not clearly preserve both the H1 family and the H2 family, treat the run as non-promotable even if it is otherwise clean.

## Notes

- The success thresholds are intentionally stricter than the hard-fail thresholds.
- A run can be non-failing and still non-promotable.
- That distinction matters here because the whole Phase L question is about preserving both capability families at once.
