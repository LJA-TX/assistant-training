# Phase F Closure And Dataset Evolution Assessment

## Executive Summary

Phase F established that Dataset v1.0 is balanced at the category level but too narrow in tool-positive coverage. The best external augmentation path is not a full redesign. It is an incremental v1.1 expansion that preserves the strong runtime/no-call structure while broadening canonical tool-call diversity.

## Current Dataset Findings

- Dataset v1.0 matches the charter's category mix.
- The train tool-positive slice is effectively one repeated `rg_search` case.
- The validation tool-positive slice is broader, but still limited.
- The current dataset therefore teaches no-call discipline better than tool-call specificity.

## External Dataset Findings

- xLAM / APIGen is the strongest primary source family for tool-call positives.
- When2Call is the strongest source for no-call and tool-decision behavior.
- APIGen-MT and ToolACE are useful secondary supplements.
- Glaive is a lower-priority broad-format fallback.
- BFCL-related public datasets should stay evaluation-only.
- ToolBench is a legacy fallback, not a preferred primary source.

## Compatibility Findings

- High fit: xLAM / APIGen, When2Call
- Medium fit: APIGen-MT, ToolACE, Glaive
- Low fit: BFCL-related datasets, ToolBench

## Behavioral Impact Findings

- Exact JSON validity is most likely to improve from more varied xLAM / APIGen-style tool-call positives.
- Tool-name accuracy and argument accuracy are also most likely to improve from diversified tool-positive coverage.
- Wrapper leakage is best protected by keeping the current runtime-style discipline and avoiding overly conversational legacy corpora.
- No-call correctness should remain strong if When2Call is used as a targeted supplement and not over-weighted.

## Risk Findings

- The highest training risk is style drift from legacy or conversational tool corpora.
- The highest governance risk is benchmark contamination from BFCL assets.
- The highest license risk is APIGen-MT's NC license if downstream use needs broader distribution.
- The highest overfitting risk is leaving the tool-positive slice concentrated in a tiny repeated pattern.

## Recommended Dataset Strategy

**Strategy A: Incremental Dataset v1.1 expansion**

This is the smallest change that addresses the actual weakness.

## Recommended Next Action

Proceed to Dataset Implementation for a v1.1 expansion that:

- broadens tool-positive coverage,
- preserves the runtime/no-call/refusal balance,
- uses high-verification external sources first,
- canonicalizes everything into the runtime schema,
- keeps BFCL assets out of training.

## Go / No-Go Recommendation

**Go** for dataset evolution implementation work.

**No-Go** for any serious training attempt until the v1.1 dataset is implemented and validated.

## Sources Used

- `CURRENT_DATASET_ASSESSMENT.md`
- `EXTERNAL_DATASET_SURVEY.md`
- `DATASET_COMPATIBILITY_ASSESSMENT.md`
- `BEHAVIORAL_GAP_MAPPING.md`
- `DATASET_RISK_ASSESSMENT.md`
- `DATASET_EVOLUTION_STRATEGY.md`
