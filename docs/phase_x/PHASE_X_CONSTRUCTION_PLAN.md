# Phase X Construction Plan

## Objective

Turn the Phase W preservation ablation into a mechanically executable construction specification without changing the causal question.

## Evidence Base

Phase V established that H1/H2 preserved a joint control surface:

- frozen scaffold,
- exact-tool-request cue on most tool-positive rows,
- high anchor concentration,
- small patch-local intervention.

Phase Q showed that restoring anchors without the preserved cue/scaffold did not recover capability.

Phase U showed that canonical schema alone does not recover capability if the surrounding preservation context is lost.

Sources:

- [Phase V control surface comparison](/opt/ai-stack/assistant-training/docs/phase_v/CONTROL_SURFACE_COMPARISON.md)
- [Phase V preservation model](/opt/ai-stack/assistant-training/docs/phase_v/PRESERVATION_MODEL_ANALYSIS.md)
- [Phase W anchor concentration experiment](/opt/ai-stack/assistant-training/docs/phase_w/ANCHOR_CONCENTRATION_EXPERIMENT.md)
- [Phase Q execution review](/opt/ai-stack/assistant-training/docs/phase_q/PHASE_Q_EXECUTION_REVIEW.md)
- [Phase U execution review](/opt/ai-stack/assistant-training/docs/phase_u/PHASE_U_EXECUTION_REVIEW.md)

## Construction Principle

Build one control arm and three treatment arms from the same frozen scaffold.

Hold constant:

- train row count,
- validation row count,
- safety row count,
- exact-tool-request cue,
- patch-local replacement shape,
- canonical `tool_calls` envelope,
- scaffold provenance,
- and canonical evaluation contract.

Vary only:

- anchor concentration inside the tool-positive slice.

## Arm Summary

The train split stays at `2160` rows for every arm.
The validation split stays frozen at `240` rows for every arm.
The train tool-positive slice stays at `1393` rows for every arm.
The train safety slice stays at `767` rows for every arm.

| Arm | Target core anchor share | Realized anchor rows | Realized long-tail rows | Notes |
|---|---:|---:|---:|---|
| Control | `0.5212` | `726` | `667` | v1.2-level anchor baseline on the preserved cue/scaffold |
| Treatment A | `0.5879` | `819` | `574` | midpoint lift test |
| Treatment B | `0.6546` | `912` | `481` | H1-like anchor level |
| Treatment C | `0.7258` | `1011` | `382` | H2-like anchor level |

## Construction Method

1. Start from the frozen Stage B recovery scaffold.
2. Preserve the non-tool surface exactly.
3. Preserve the safety block exactly.
4. Replace only the tool-positive slice.
5. Keep the exact-tool-request cue identical on every tool-positive row.
6. Keep the canonical single-call `tool_calls` envelope identical on every tool-positive row.
7. Reallocate tool-positive mass between the five anchor tools and the 21 long-tail tools to hit the target anchor count for the arm.

## Recommendation

Proceed to dataset construction after this plan is reviewed and approved.

This is the highest-information next step because it isolates the remaining unresolved variable without introducing a new prompt regime or scaffold change.
