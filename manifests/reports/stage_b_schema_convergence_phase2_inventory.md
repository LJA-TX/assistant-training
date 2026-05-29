# Stage B Schema Convergence Phase 2 Inventory

## Scope
Phase 2 inventory and semantic-equivalence review for all remaining noncomputable metrics after Phase 1.

## Remaining Noncomputable Metrics
Count: `4`

- `direct_answer_substitution_count`
- `no_anchor_exact_valid_share`
- `read_file_exact_valid_rate`
- `read_file_symbol_name_exact_valid_rate`

## Classification Outcome
- `safe_path_update_candidate`: `0`
- `eval_redesign_required`: `4`
- `uncertain_requires_human_review`: `0`

## Metric-by-Metric Review

### `direct_answer_substitution_count`
- Current mapping: `failure_profile.failure_categories_non_exact_tool_rows.direct_answer_substitution`
- Noncomputable reason: required metric not found in live eval summary
- Candidate live locations inspected:
  - `adapter.aggregate.class_counts.*`
  - `adapter.per_split.direct_answer.*`
  - `comparison_rows.jsonl` row classes/annotations
- Semantic assessment: no one-to-one equivalent exists in live summary
- Classification: `eval_redesign_required`
- Expected outcome: remains noncomputable

### `no_anchor_exact_valid_share`
- Current mapping: `failure_profile.anchor_exact_share.no_anchor_phrase`
- Noncomputable reason: required metric not found in live eval summary
- Candidate live locations inspected:
  - `adapter.aggregate.*`
  - `comparison_rows.jsonl` generated text
- Semantic assessment: no anchor-taxonomy field exists in live schema; text analysis would be reconstruction/inference
- Classification: `eval_redesign_required`
- Expected outcome: remains noncomputable

### `read_file_exact_valid_rate`
- Current mapping: `failure_profile.read_file_exact_valid.rate`
- Noncomputable reason: required metric not found in live eval summary
- Candidate live locations inspected:
  - `adapter.per_split.tool_holdout.exact_json_validity.rate`
  - `comparison_rows.jsonl` filtered read_file rows
- Semantic assessment: tool_holdout is mixed-tool aggregate; row filtering would require reconstruction/aggregation
- Classification: `eval_redesign_required`
- Expected outcome: remains noncomputable

### `read_file_symbol_name_exact_valid_rate`
- Current mapping: `failure_profile.read_file_symbol_name_exact_valid.rate`
- Noncomputable reason: required metric not found in live eval summary
- Candidate live locations inspected:
  - `adapter.per_split.tool_holdout.*`
  - `comparison_rows.jsonl` case/archetype subsets
- Semantic assessment: no symbol-name submetric exists in live schema; extraction would require reconstruction/inference
- Classification: `eval_redesign_required`
- Expected outcome: remains noncomputable

## Safe Candidate Determination (Phase 2 Rule Set)
All four remaining metrics fail one or more required safe conditions:
- no explicit one-to-one live field
- transformation/reconstruction/inference would be required

Therefore no additional safe candidates are eligible for Phase 2 mapping updates.

## Artifacts
Machine-readable inventory:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_schema_convergence_phase2_inventory.json`
