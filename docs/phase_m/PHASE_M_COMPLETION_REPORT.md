# Phase M Completion Report

## Executive Summary

Phase M attributes the Phase L failure to a dataset signal-shape problem, not a training-system failure.

Dataset v1.1 preserved safety because it successfully taught refusal discipline.
It collapsed tool-call capability because the positive tool-call signal was diluted, flattened, and overrun by safety-calibration pressure under a fixed training budget.

## Key Findings

1. The run is safety-clean: `no_call_correctness = 1.0`, `adversarial_no_call_correctness = 1.0`, `wrapper_leakage = 0.0`.
2. The run is capability-broken: `exact_json_validity = 0.0`, `tool_holdout_exact_valid = 0.0`, `heldout_validation_exact_valid = 0.0`.
3. The dominant failure mode is schema-emission collapse, especially near-canonical wrapper or envelope drift.
4. The Phase L dataset shifted 108 rows away from tool-positive supervision and into safety calibration relative to the H1/H2-style mix.
5. The tool-positive distribution was flattened across all 26 families, which likely reduced the repeated anchor signal needed for tool-call realization.

## Ranked Hypotheses

| Rank | Hypothesis | Confidence |
|---|---|---|
| 1 | Dataset rebalancing diluted tool-positive supervision too far | High |
| 2 | Safety over-calibration pushed refusal correctness ahead of tool-call realization | High |
| 3 | Schema-emission degradation is the proximate mechanism | High |
| 4 | Tool-family flattening under a fixed 0.2-epoch budget caused underfitting | Medium-High |
| 5 | Prompt-template interaction contributed secondarily | Low-Medium |
| 6 | Trainer-geometry interaction caused the failure | Low |
| 7 | Evaluation or scoring drift caused the failure | Very Low |

## Confidence Assessment

High confidence:

- the failure is real,
- the evaluation is frozen,
- the safety boundary is preserved,
- the capability boundary is not,
- the dataset mix is the main changed control surface.

Medium confidence:

- the exact proportional contribution of safety over-calibration versus tool-positive dilution.

Low confidence:

- prompt-template or trainer-geometry as the primary root cause.

## Recommended Next Action

Return to dataset design, not training.

The next actionable step is to design a rebalanced candidate that restores stronger tool-positive repetition while keeping the explicit safety rows exact and contamination-clean.

## Recommended Next Phase

A new dataset redesign and validation phase should precede any additional training authorization.

That phase should focus on:

- stronger positive tool-call density,
- less flattening across tools,
- explicit safety calibration that does not crowd out tool-call schema learning,
- and a pre-execution review that checks the resulting mix before training.

## Supporting Documents

- [Failure Characterization](/opt/ai-stack/assistant-training/docs/phase_m/FAILURE_CHARACTERIZATION.md)
- [JSON And Schema Failure Analysis](/opt/ai-stack/assistant-training/docs/phase_m/JSON_AND_SCHEMA_FAILURE_ANALYSIS.md)
- [Comparative Behavioral Analysis](/opt/ai-stack/assistant-training/docs/phase_m/H0_H1_H2_PHASEL_COMPARATIVE_ANALYSIS.md)
- [Root Cause Assessment](/opt/ai-stack/assistant-training/docs/phase_m/ROOT_CAUSE_ASSESSMENT.md)
- [Corrective Action Analysis](/opt/ai-stack/assistant-training/docs/phase_m/CORRECTIVE_ACTION_ANALYSIS.md)
