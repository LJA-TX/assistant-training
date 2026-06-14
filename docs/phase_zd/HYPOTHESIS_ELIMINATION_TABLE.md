# Hypothesis Elimination Table

## Classification Legend

- `ruled out`: evidence directly contradicts the hypothesis as a primary explanation.
- `weakened`: evidence shows the hypothesis is not sufficient and not the main differentiator.
- `contributory`: evidence suggests the hypothesis helps, but it is not sufficient on its own.
- `still viable`: evidence has not falsified the hypothesis, but it is not yet isolated.
- `untested`: the hypothesis has not been directly isolated by the available runs.

## Table

| Hypothesis | Status | Evidence basis |
|---|---|---|
| Schema-only repair | `ruled out` | Phase U kept the canonical envelope but collapsed to `0.0` exact JSON, `0.0` tool-name accuracy, and `0.0` argument accuracy. |
| Anchor concentration | `contributory` | Phase ZC improved exact JSON from `0.055` to `0.085` and tool-name accuracy from `0.2` to `0.2857`, but did not recover H1/H2 and broke adversarial no-call safety. |
| Strict cue preservation | `still viable` | The exact-tool-request cue is preserved in the Phase Y arms and in the H1/H2-successful patches, but it is not isolated by the completed sweep. |
| Frozen scaffold preservation | `still viable` | The frozen scaffold is present across the preserved ablation and earlier successful patches, but it is a background condition rather than a differentiator. |
| Patch scale / low-delta locality | `contributory` | H1/H2 were small positive patches on a frozen scaffold; the later full-corpus interventions did not reproduce the H1/H2 regime. |
| Row replacement topology | `untested` | The sweep varied anchor concentration, not the local replacement topology itself. |
| Prompt regime | `contributory` | H1/H2 preserved a narrow, exact-tool-request tool-positive regime; v1.2 widened prompt styles and did not recover capability. |
| Safety block interaction | `weakened` | Safety calibration clearly affects no-call behavior, but Phase ZC shows it does not explain exact-call recovery by itself. |
| Trainer geometry | `ruled out` | The same trainer geometry appears across the successful H1/H2 patches and the later failed runs, so it is not the discriminant. |

## Notes

- The elimination table is about causal explanation, not promotion.
- A hypothesis can remain viable even if it is not the primary explanation.
- The completed anchor sweep only isolates one axis: anchor concentration.
