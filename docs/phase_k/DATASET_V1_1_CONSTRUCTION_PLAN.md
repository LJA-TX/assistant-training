# Phase K Dataset V1.1 Construction Plan

## Context

Phase J concluded that the strongest supported remediation shape is an external-first, safety-calibrated hybrid.
This plan implements that guidance by building a new candidate around external tool-call lineage, balanced diversity/commitment pressure, and explicit safety calibration rows.

## Construction Shape

| Slice | Planned role | Rationale |
|---|---|---|
| External tool-positive core | Primary capability substrate | This is the external-first component. It carries the diversity and commitment lessons from Phase J without reusing Phase I training rows. |
| Diversity sub-slice | H1-inspired coverage expansion | This slice keeps tool-family breadth broad and prevents the candidate from collapsing into a single literal anchor pattern. |
| Commitment sub-slice | H2-inspired commitment pressure | This slice adds paraphrastic and anchor-light tool-expected prompts so canonical tool-call realization is still exercised under less literal phrasing. |
| Runtime-alignment slice | Guardrail behavior | This slice teaches the assistant to stay explicit, cautious, and bounded when no tool is needed. |
| No-call direct calibration slice | Explicit no-call examples | These rows teach the model to answer directly when no tool is required, without inventing a tool call. |
| Refusal calibration slice | Safety calibration | These rows keep harmful or disallowed requests on a refusal track. |
| Adversarial no-call slice | Ambiguity discipline | These rows teach the model to ask for the missing target or resource instead of making speculative tool calls. |

## Source Categories

| Source category | Source evidence | Role in v1.1 |
|---|---|---|
| `canonical_case_template` | External tool-call corpus in `data/tool_ft_allaliases_20260525_from_qual_reports_freq.jsonl` | Main diversity backbone. It supplies the broad tool-family coverage used by the diversity sub-slice. |
| `contrastive_positive` | External tool-call corpus in the same source file | Commitment pressure. These cases are the best fit for anchor-light and paraphrastic tool-expected prompts. |
| `contrastive_negative` | External tool-call corpus in the same source file | Commitment contrast. These cases are used to keep the model from relying on a narrow literal shell. |
| `runtime_alignment` templates | Phase J design guidance | Non-tool guardrail training that keeps the assistant explicit about uncertainty and limits. |
| `no_call_direct` templates | Phase J design guidance | Explicit no-call / direct-answer calibration. |
| `refusal` templates | Phase J design guidance | Explicit refusal calibration for harmful requests. |
| `adversarial` templates | Phase J design guidance | Explicit no-call discipline under ambiguity and malformed requests. |

## Acceptance Thresholds

| Threshold | Value |
|---|---|
| Total rows | `2400` |
| Train / val split | `2160 / 240` |
| Tool-positive total | `1440` |
| Diversity rows | `720` |
| Commitment rows | `720` |
| Safety rows | `600` |
| Tool-family coverage | all `26` tools represented |
| Per-tool balance | `55` or `56` rows per tool |
| Prompt overlap with heldout/tool-holdout | `0` |
| Target overlap with heldout/tool-holdout | `0` |
| Case-id overlap with heldout/tool-holdout | `0` |
| Canonical eval contract | unchanged |
| Evaluation semantics | unchanged |
| Governance | unchanged |

## Contamination Safeguards

1. Candidate prompts and targets are regenerated from repository-local safe surfaces instead of copied verbatim from the canonical eval splits.
2. Each tool-positive row carries a new Phase K source case ID and lineage metadata back to the external corpus.
3. The builder validates prompt, target, and case-ID overlap against `heldout_validation`, `tool_holdout`, `no_call`, `adversarial`, and `direct_answer`.
4. The dataset build does not alter eval manifests, scoring logic, or governance artifacts.

## Rationale

This plan is intentionally conservative on the total row budget.
It keeps the Phase I scale while changing the content mix so future training can test whether the combined bottleneck can be addressed without sacrificing safety.

## Sources Used

- `docs/phase_j/LESSONS_LEARNED_INVENTORY.md`
- `docs/phase_j/COMBINED_BOTTLENECK_MODEL.md`
- `docs/phase_j/DATASET_V1_1_DESIGN_REQUIREMENTS.md`
- `docs/phase_j/CANDIDATE_REMEDIATION_STRATEGIES.md`
- `docs/phase_j/PHASE_K_RECOMMENDATION.md`
- `scripts/build_dataset_v1_1.py`

