# Phase N Completion Report

## Executive Summary

Phase N concludes that Dataset v1.2 should be an **anchor-weighted hybrid with modest density restoration**.

The Phase L collapse was caused by a combination of:

- reduced tool-positive density,
- excessive flattening of the tool-positive family distribution.

The stronger proximate issue is the flattening of the canonical tool core.

## Key Findings

1. H1/H2 train data ran at `65%` tool-positive density.
2. Dataset v1.1 train data dropped to `60%` tool-positive density.
3. The tool-positive core in H1/H2 was heavily concentrated around repeated anchors such as `rg_search` and `read_file`.
4. Dataset v1.1 flattened that core almost completely.
5. Dataset v1.1 preserved safety exactly, so the redesign must keep the explicit safety block rather than removing it.

## Answer To The Required Question

The collapse was driven by **C. a combination of both**.

If one factor is dominant, it is **B: excessive tool-family flattening under a fixed training budget**.

## Recommended Next Action

Design Dataset v1.2 so that it:

- restores more tool-positive density,
- restores a repeated anchor core,
- keeps all 26 tool families represented,
- and preserves the explicit no-call and adversarial calibration rows.

## Recommended Next Phase

Proceed to a dataset-construction and validation phase for v1.2, with contamination checks and composition checks performed before any new training authorization.

## Validation

No training or evaluation reruns were performed in Phase N.

This phase is documentation-only.

## Supporting Documents

- [Dataset Shape Analysis](/opt/ai-stack/assistant-training/docs/phase_n/DATASET_SHAPE_ANALYSIS.md)
- [Tool Frequency Analysis](/opt/ai-stack/assistant-training/docs/phase_n/TOOL_FREQUENCY_ANALYSIS.md)
- [Dataset V1.2 Design Options](/opt/ai-stack/assistant-training/docs/phase_n/DATASET_V1_2_DESIGN_OPTIONS.md)
- [Dataset V1.2 Recommendation](/opt/ai-stack/assistant-training/docs/phase_n/DATASET_V1_2_RECOMMENDATION.md)
