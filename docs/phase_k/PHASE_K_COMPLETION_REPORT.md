# Phase K Completion Report

## Executive Summary

Phase K is complete.
A Dataset v1.1 candidate now exists under `data/v1_1/` and has been validated for contamination and composition readiness.

The candidate follows the Phase J guidance:

- external-first tool-positive lineage,
- balanced diversity and commitment pressure,
- explicit safety calibration,
- and zero overlap with the frozen canonical eval splits.

## Dataset Summary

| Item | Value |
|---|---:|
| Train rows | `2160` |
| Val rows | `240` |
| Total rows | `2400` |
| Tool-positive rows | `1440` |
| Runtime-alignment rows | `360` |
| No-call direct calibration rows | `240` |
| Refusal calibration rows | `180` |
| Adversarial no-call calibration rows | `180` |
| Diversity rows | `720` |
| Commitment rows | `720` |
| Safety rows | `600` |
| Tool families represented | `26` |

## Validation Results

- `git diff --check` was run before commit preparation and passed.
- The builder-side validation completed successfully.
- The candidate's contamination report shows zero overlap against heldout validation, tool holdout, no-call, adversarial, and direct-answer splits.
- The composition analysis shows a balanced diversity/commitment split and full tool-family coverage.

## Contamination Results

| Split | Prompt | Target | Case ID |
|---|---:|---:|---:|
| Heldout validation | `0` | `0` | `0` |
| Tool holdout | `0` | `0` | `0` |
| No-call | `0` | `0` | `0` |
| Adversarial | `0` | `0` | `0` |
| Direct-answer | `0` | `0` | `0` |

## Readiness Determination

**Ready**

The candidate is ready for a future governed training evaluation because the data package is complete, contamination-clean, and composition-balanced.

## Risks

1. The candidate is synthetic and derived from external lineage rather than copied directly from the source corpus.
2. The current phase does not measure model behavior, so no performance claim is justified yet.
3. The external-first design is intentionally conservative and will still need governed training to determine whether the combined bottleneck is actually resolved.

## Recommended Next Phase

Future training evaluation of `data/v1_1/` under the frozen canonical eval contract.

That next phase should be governed as a training step, not as an evaluation rewrite.

## Evidence Files

- [Dataset v1.1 train split](/opt/ai-stack/assistant-training/data/v1_1/dataset_v1_1_train.jsonl)
- [Dataset v1.1 val split](/opt/ai-stack/assistant-training/data/v1_1/dataset_v1_1_val.jsonl)
- [Dataset v1.1 summary](/opt/ai-stack/assistant-training/data/v1_1/dataset_v1_1_summary.json)
- [Dataset v1.1 contamination report](/opt/ai-stack/assistant-training/data/v1_1/dataset_v1_1_leakage_report.json)
- [Dataset v1.1 readiness assessment](/opt/ai-stack/assistant-training/data/v1_1/dataset_v1_1_readiness_assessment.json)
- [Builder script](/opt/ai-stack/assistant-training/scripts/build_dataset_v1_1.py)

