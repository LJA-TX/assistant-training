# Stage B i10r Micro-Probe Checkpoint

## Scope and Boundaries
- Purpose: bounded instrumentation probe for procedural commitment behavior, not promotion.
- Parent checkpoint: `stage_b_llama31_8b_base_v1_i9`.
- Dataset: revised exposure geometry `dataset_v1_0_stage_b_recovery_i10r_{train,val}.jsonl`.
- Training scope: single micro-probe run (~0.20 epoch), deterministic settings, no hidden retries.
- Eval scope: canonical eval manifest unchanged; decode defaults unchanged.
- Governance constraints preserved: no topology mutation, no threshold relaxation, no canonization/promotion.

## Revised Exposure Geometry Rationale
- Revision strategy: reduce ritualized legacy dominance while preserving lineage continuity and stress behavior.
- Exposure change (targeted families):
  - before (`i10`): legacy `0.790123`, healthy conversion `0.209877`
  - after (`i10r`): legacy `0.660566`, healthy conversion `0.339434`
- Diversity proxy improvements after revision:
  - prompt uniqueness ratio: `+0.178307`
  - skeleton uniqueness ratio: `+0.134004`
  - unique tool-args ratio: `+0.017782`

## i9 vs i10r Micro-Probe (Primary Metrics)

| Metric | i9 | i10r micro-probe | Delta |
|---|---:|---:|---:|
| Heldout exact-valid | 0.15 | 0.66 | +0.51 |
| Heldout invalid_json | 0.58 | 0.14 | -0.44 |
| Heldout tool_name_accuracy | 0.15 | 0.74 | +0.59 |
| Heldout argument_accuracy | 0.15 | 0.70 | +0.55 |
| read_file exact-valid | 0.00 | 0.703704 (19/27) | +0.703704 |
| Scalar substitution share (non-exact tool rows) | 0.40 | 0.00 | -0.40 |
| Direct-answer substitution share (non-exact tool rows) | 0.496 | 0.226415 | -0.269585 |
| Wrapper leakage | 0.00 | 0.00 | 0.00 |
| No-call correctness (aggregate expected no-call rows) | 1.00 | 0.916667 (55/60) | -0.083333 |

## Anchor Dependence / Generalization

| Exact-valid anchor bucket share | i9 | i10r micro-probe |
|---|---:|---:|
| Literal `tool_calls` anchor | 0.266667 | 0.057471 |
| Paraphrastic tool-call anchor | 0.333333 | 0.080460 |
| No-anchor phrasing | 0.048000 | 0.862069 |

Interpretation: i10r gains are not explained by literal-anchor dependence; no-anchor exact-valid behavior dominates.

## Hard-Stop Trigger and Halt Rationale
- Hard-stop condition activated: `no_call_correctness_lt_1`.
- Trigger source: adversarial no-call degradation (`15/20 = 0.75`) caused aggregate no-call correctness to drop to `0.916667`.
- Other collapse-watch triggers were not active:
  - wrapper leakage remained `0.0`
  - scalar substitution did not rebound
  - anchor dependence did not materially strengthen
  - shell concentration rise was not detected

## Why Progression Halted
Progression halted because governance treats no-call correctness as a hard invariant. This is a report-only checkpoint, not a continuation authorization.

## Why This Is Not i4/i5-Style Collapse
- i4/i5 pattern: broad overconstraint collapse with suppressed useful behavior.
- i10r observed pattern: substantial procedural commitment gains (exact-valid, tool/argument accuracy, read_file emergence) with a localized no-call adversarial regression.
- Therefore: this is an invariant breach requiring targeted remediation, not a global schema-collapse regime.

## Principal Remaining Risks
- No-call/adversarial refusal robustness regression under commitment pressure.
- Potential future cross-talk between procedural commitment reinforcement and refusal boundaries.
- Residual near-canonical drift in non-exact tool rows.

## Recommended Next Direction
- Next phase should be bounded no-call/remediation design.
- Do **not** proceed with forward training progression from this checkpoint until no-call invariants are restored.

## Preservation Status
This checkpoint is intended to preserve the i10r micro-probe state exactly as observed, including both major gains and the hard-stop condition.
