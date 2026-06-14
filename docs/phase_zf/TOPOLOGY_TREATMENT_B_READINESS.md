# Topology Treatment B Readiness

## Dataset

- Train: [dataset_v1_2_phase_zf_treatment_b_train.jsonl](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_zf_treatment_b_train.jsonl)
- Val: [dataset_v1_2_phase_zf_treatment_b_val.jsonl](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_zf_treatment_b_val.jsonl)
- Summary: [dataset_v1_2_phase_zf_treatment_b_summary.json](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_zf_treatment_b_summary.json)
- Leakage report: [dataset_v1_2_phase_zf_treatment_b_leakage_report.json](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_zf_treatment_b_leakage_report.json)
- Readiness: [dataset_v1_2_phase_zf_treatment_b_readiness_assessment.json](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_zf_treatment_b_readiness_assessment.json)

## Topology

- Pattern: `four_clusters_25_plus_25_plus_25_plus_25_rg_search_rows`
- Position span: `420`
- Mean gap: `4.242424`
- Median gap: `1`

## Validation

- Contamination: zero across all frozen eval surfaces.
- Exact cue: retained on all tool-positive rows.
- Scaffold: invariant relative to the frozen phase_y control surface.
- Envelope: canonical single-call `tool_calls` structure retained.
- Safety: preserved.
- Family coverage: all 26 tool families represented.

## Determination

Ready and scientifically admissible.
