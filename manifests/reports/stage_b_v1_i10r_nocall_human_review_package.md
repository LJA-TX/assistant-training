# Stage B i10r No-Call Restoration Human Review Package

- Generated UTC: 2026-05-27T18:21:39Z
- Iteration: stage_b_llama31_8b_base_v1_i10r_nocall

## Composition
- Added rows total: 16
- Added rows train: 14
- Added rows val: 2
- Altered existing rows: 0

## Localized Diff Checks
- additions_exact_match: True
- existing_rows_unchanged: True
- localized_family_only: True
- contrastive_pairs_pass: True

## Hygiene Gates
- ambiguity_hard_blocks_clean: True
- heldout_overlap_zero: True
- tool_holdout_overlap_zero: True
- forbidden_pattern_hits_zero: True

## Anti-Regression Telemetry
- read_file_baseline_exact_valid: 0.703704
- scalar_baseline_share: 0.0
- no_anchor_baseline_share: 0.862069
- additions_anchor_distribution: {'literal_tool_calls': 0, 'paraphrastic_tool_call': 0, 'no_anchor_phrase': 16}
- anti_regression_risk_pass: True

## Recommendation
- proceed_to_bounded_training_review_candidate_only_if_future_post_run_gates_hold

