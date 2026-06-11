# Root Cause Assessment

## Executive Summary

The strongest evidence-backed explanation is not a trainer or evaluator defect.
It is a dataset shift:

- fewer tool-positive examples,
- more safety-calibration examples,
- flatter tool-family frequencies,
- the same frozen trainer geometry,
- the same frozen evaluation contract.

The result is a model that learned the refusal boundary more strongly than the tool-call boundary.

## Ranked Hypotheses

| Rank | Hypothesis | Confidence | Evidence |
|---|---|---|---|
| 1 | Dataset composition / weighting shift toward safety-calibration and away from tool-positive density | High | Phase L moved from `1404` tool-positive / `756` runtime-assistant rows in H1/H2-style data to `1296` tool-positive / `864` runtime-assistant rows. The model preserved safety and lost capability. |
| 2 | Safety over-calibration | High | `no_call_correctness = 1.0`, `adversarial_no_call_correctness = 1.0`, `wrapper_leakage = 0.0`, while all tool-call metrics collapsed. |
| 3 | Schema-emission degradation as the proximate mechanism | High | `132 / 140` tool rows are `invalid_json` or `invalid_schema`; `70` rows are near-canonical wrapper or envelope drift; heldout validation has `44` `missing_tool_calls` schema reasons. |
| 4 | Tool-positive dilution from a flattened 26-tool distribution under a fixed 0.2-epoch budget | Medium-High | Phase L tool counts are tightly balanced at `46-56` rows per tool, while H1/H2 training data were heavily skewed toward high-frequency anchor tools such as `rg_search`, `read_file`, and `find_files`. |
| 5 | Prompt-template interaction | Low-Medium | The prompt template itself is unchanged from H1/H2, but the Phase L mix puts more weight on the runtime-assistant side, which may interact with the lower tool-positive density. |
| 6 | Trainer-geometry interaction | Low | The model, LoRA geometry, quantization, optimizer, and epoch budget are the same as H1/H2. Training completed normally and does not show a geometry anomaly. |
| 7 | Evaluation or scoring drift | Very Low | The canonical eval manifest is frozen and unchanged. The failure is visible in row-level outputs, not just in aggregate scoring. |

## Evidence By Hypothesis

### Dataset Composition

The Phase L dataset is broader and more balanced than the H1/H2 training sets.

That is true, but the balance appears to be too aggressive for the fixed training budget.

Evidence:

- all `26` tool families are represented,
- tool counts are tightly clustered at `46-56`,
- tool-positive rows were reduced relative to H1/H2-style data,
- safety rows were expanded.

### Dataset Weighting

The train mix shifted away from tool-positive examples and toward runtime-assistant / safety-calibration examples.

Evidence:

- Phase L: `1296` tool-positive rows and `864` runtime-assistant rows,
- H1/H2-style data: `1404` tool-positive rows and `756` runtime-assistant rows.

That 108-row shift is small in absolute terms but large enough to matter under a `0.2` epoch budget.

### Safety Over-Calibration

Safety over-calibration is strongly supported.

Evidence:

- no-call and adversarial no-call are both perfect,
- wrapper leakage is zero,
- capability falls to zero on the tool-call surface.

The model learned "do not overstep" more reliably than "emit canonical tool calls."

### Schema-Emission Degradation

This is the proximate failure mode.

Evidence:

- `invalid_json = 69`,
- `invalid_schema = 63`,
- `70` near-canonical wrapper or envelope drift rows,
- `44` heldout-validation rows with `missing_tool_calls`,
- row examples show `{"function": ...}` and `{"functions": ...}` shapes instead of canonical `{"tool_calls": ...}`.

### Prompt-Template Interaction

This is a plausible secondary factor, not the main cause.

Evidence:

- the prompt-template configuration is identical to H1/H2,
- the training uses the same tokenizer chat template fallback,
- the only prompt-side change is how much the runtime-assistant half of the dataset is emphasized.

### Trainer-Geometry Interaction

This is weakly supported as a cause.

Evidence:

- the geometry is unchanged from H1/H2,
- training runtime and losses are normal,
- no instability, divergence, or hidden retry behavior is reported.

### Other Evidence-Supported Causes

The most credible additional factor is signal dilution:

- more tools,
- fewer repetitions per tool,
- the same small epoch budget.

That combination is consistent with underfitting the tool-call schema while still teaching the refusal boundary.

## Bottom-Line Attribution

The best-supported root cause is:

**Phase L over-optimized safety calibration and tool-family breadth relative to the fixed training budget, which diluted the positive tool-call signal and produced schema-emission collapse rather than tool-call competence.**

## Sources Used

- `docs/phase_l/PHASE_L_EXECUTION_REVIEW.md`
- `docs/phase_l/PHASE_L_COMPLETION_REPORT.md`
- `docs/phase_j/COMBINED_BOTTLENECK_MODEL.md`
- `docs/phase_j/CANDIDATE_REMEDIATION_STRATEGIES.md`
- `data/v1_1/dataset_v1_1_summary.json`
- `evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/summary.json`
- `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl`
