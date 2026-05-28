# Stage B i10r Counterbalanced Human Review Package

- Generated UTC: 2026-05-28T14:44:20Z
- Iteration: stage_b_llama31_8b_base_v1_i10r_counterbalanced

## Composition
- Added rows total: 16
- Added rows train: 13
- Added rows val: 3
- Altered existing rows: 0

## Localized Diff Checks
- additions_exact_match: True
- existing_rows_unchanged: True
- localized_family_only: True
- contrastive_pairs_pass: True
- counterbalanced_block_pass: True

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
- additions_block_distribution: {'nocall_contrastive_pair_block_v2': 10, 'read_file_symbol_name_commitment_counterbalance_v1': 6}
- anti_regression_risk_pass: True

## Recommendation
- proceed_to_bounded_training_review_candidate_only_if_future_post_run_gates_hold

