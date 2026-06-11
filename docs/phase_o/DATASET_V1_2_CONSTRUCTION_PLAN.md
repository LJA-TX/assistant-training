# Dataset V1.2 Construction Plan

## Purpose

Phase O constructs a Dataset v1.2 candidate that follows the Phase N recommendation:

- anchor-weighted hybrid design;
- modest tool-positive density restoration;
- explicit safety calibration preserved;
- all 26 tool families retained;
- contamination clean against the frozen canonical evaluation assets.

## Construction Inputs

| Input | Role |
|---|---|
| `data/tool_ft_allaliases_20260525_from_qual_reports_freq.jsonl` | External tool-call lineage source for the tool-positive core. |
| `evals/data/canonical_v1/*.jsonl` | Frozen contamination-validation target set. |
| Phase N recommendation | Governs the tool-density, core-anchor, and breadth targets. |

## Source Categories

| Source category | Role in v1.2 | Rationale |
|---|---|---|
| `canonical_case_template` | Anchor diversity backbone | Supplies literal, canonical tool-call examples that preserve the canonical envelope. |
| `contrastive_positive` | Commitment pressure | Supplies paraphrastic tool-expected prompts that prevent the model from overfitting one lexical shell. |
| `contrastive_negative` | Long-tail resistance | Keeps the tool-positive core from becoming a single pattern family. |
| `runtime_alignment` | Guardrail calibration | Keeps the assistant explicit about uncertainty and limits when no tool is needed. |
| `no_call_direct` | Direct-answer calibration | Preserves exact direct-answer behavior on non-tool tasks. |
| `refusal` | Safety calibration | Preserves refusal behavior on harmful requests. |
| `adversarial` | Ambiguity discipline | Trains the model to ask for missing targets or paths instead of speculating. |

## Construction Shape

| Slice | Rows | Role |
|---|---:|---|
| Tool-positive | `1548` | Primary capability substrate. |
| Runtime alignment | `360` | Non-tool guardrail calibration. |
| No-call direct calibration | `240` | Explicit direct-answer calibration. |
| Refusal calibration | `180` | Safety refusal calibration. |
| Adversarial no-call calibration | `72` | Ambiguity discipline, reduced from v1.1 to restore tool-positive signal. |

## Target Thresholds

| Target | Range or requirement |
|---|---|
| Train tool-positive density | `0.63` to `0.65` |
| Core anchor share (`rg_search`, `read_file`, `find_files`, `debug_tools`, `run_command`) | `0.45` to `0.55` of tool-positive rows |
| `rg_search + read_file` share | `0.30` to `0.40` of tool-positive rows |
| Tool families represented | `26` |
| Contamination overlap | `0` on prompt, target, and source case ID |
| Safety block | Explicit and separated from tool-positive rows |

## Rationale

The candidate keeps the breadth restored in v1.1, but it reintroduces repetition pressure on the canonical tool core.

The deliberate budget shift is:

- more exposure to the anchor core;
- less over-calibration on adversarial no-call;
- no removal of the explicit safety block;
- no collapse back to H2-style narrowness.

That is the smallest shape that remains consistent with the Phase N evidence while keeping the candidate operationally auditable.

## Acceptance Criteria

The candidate is acceptable if all of the following are true:

1. The train split lands inside the tool-positive density window.
2. The core anchor share lands inside the target window.
3. `rg_search` and `read_file` together remain materially more frequent than the long tail.
4. All 26 tool families remain represented.
5. Contamination validation is zero against every frozen canonical eval split.

## Outcome

The constructed v1.2 candidate satisfies the above thresholds and is documented in:

- [Dataset V1.2 Composition Analysis](/opt/ai-stack/assistant-training/docs/phase_o/DATASET_V1_2_COMPOSITION_ANALYSIS.md)
 - [Dataset V1.2 Tool Distribution Report](/opt/ai-stack/assistant-training/docs/phase_o/DATASET_V1_2_TOOL_DISTRIBUTION_REPORT.md)
 - [Contamination Validation Report](/opt/ai-stack/assistant-training/docs/phase_o/CONTAMINATION_VALIDATION_REPORT_V1_2.md)
 - [Dataset V1.2 Readiness Assessment](/opt/ai-stack/assistant-training/docs/phase_o/DATASET_V1_2_READINESS_ASSESSMENT.md)
