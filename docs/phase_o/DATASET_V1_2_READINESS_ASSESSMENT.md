# Dataset V1.2 Readiness Assessment

## Status

**Ready**

## Basis

Dataset v1.2 is ready for future execution review because:

1. The candidate exists on disk under `data/v1_2/`.
2. The candidate is contamination-clean against every frozen canonical eval split.
3. The train-split tool-positive density lands inside the Phase N target range.
4. The anchor core is concentrated enough to plausibly recover tool-call capability.
5. The breadth-restoration tools remain represented.
6. The explicit safety-calibration block is still present and isolated.
7. All 26 tool families remain represented.

## Measured Checks

| Check | Value | Target / expectation | Result |
|---|---:|---:|---|
| Train tool-positive density | `0.6449` | `0.63` to `0.65` | PASS |
| Core anchor share | `0.5212` | `0.45` to `0.55` | PASS |
| `rg_search + read_file` share | `0.3116` | `0.30` to `0.40` | PASS |
| Tool families represented | `26` | `26` | PASS |
| Heldout/tool-holdout overlap | `0 / 0 / 0` | `0 / 0 / 0` | PASS |
| All frozen eval splits clean | `0 / 0 / 0` | `0 / 0 / 0` | PASS |
| Safety block present | yes | yes | PASS |

## Supporting Summary

| Item | Value |
|---|---:|
| Train rows | `2160` |
| Val rows | `240` |
| Total rows | `2400` |
| Tool-positive rows | `1548` |
| Runtime-alignment rows | `360` |
| No-call direct rows | `240` |
| Refusal rows | `180` |
| Adversarial no-call rows | `72` |

## Decision

**Ready**

This is the correct operational state for a pre-execution candidate:

- the dataset exists,
- the contamination checks pass,
- the structural targets are met,
- and the repository now contains a complete evidence record for the next governed decision.

## Boundary Reminder

 Readiness here does not authorize training.
 It only means the Dataset v1.2 candidate is structurally ready for future execution review.
