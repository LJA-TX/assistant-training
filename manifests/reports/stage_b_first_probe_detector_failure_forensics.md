# Stage B First Probe Collapse-Detector Failure Forensics

## Scope
Bounded read-only analysis of collapse-detector failure after successful training and canonical eval.

Failure observed:
- `RuntimeError: eval_summary: required metric 'direct_answer_substitution_count' not found in summary`

## 1. Detector Expectation Source
Detector requirement is profile-driven, not hardcoded to this specific metric name.

- Resolution path:
  - `scripts/post_eval_collapse_detector.py:305-323` (`_resolve_required_metrics`)
  - `scripts/post_eval_collapse_detector.py:136-193` (`_resolve_metric_from_catalog`)
- Behavior:
  - For every `metric_id` used by any rule in threshold profile, detector resolves metric from `metric_catalog`.
  - Missing metric raises fail-fast runtime error (`required metric ... not found in summary`).

Conclusion:
- `direct_answer_substitution_count` is required because threshold profile declares it, not because detector hardcodes it.

## 2. Eval Summary Reality
Inspected live eval summary:
- `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_mh_eval/summary.json`

Findings:
- Summary schema is `base/adapter/per_split/aggregate/delta_adapter_minus_base`.
- No `failure_profile` object exists.
- No field named `direct_answer_substitution_count` exists.
- Direct-answer-related fields present are refusal/no-call style fields, e.g.:
  - `adapter.per_split.direct_answer.no_call_correctness.rate`
  - `adapter.per_split.direct_answer.class_counts.refusal_expected`

Equivalence check:
- No strict equivalent to old metric path
  `failure_profile.failure_categories_non_exact_tool_rows.direct_answer_substitution`
  exists in this eval summary.

## 3. Baseline Summary Comparison
Inspected baseline summary:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`

Findings:
- Baseline contains `failure_profile.failure_categories_non_exact_tool_rows.direct_answer_substitution` (value `11`).
- Baseline uses older schema style (`metrics.*`, `failure_profile.*`).
- Detector metric catalog mostly resolves against baseline schema.

Important latent issue:
- `wrapper_leakage_overall` is ambiguous on baseline under current candidate paths (multiple matches), so detector would fail later even after first missing-metric fix.

## 4. Threshold Profile Analysis
Inspected threshold profile:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json`

Findings:
- `metric_catalog.direct_answer_substitution_count.path` =
  `failure_profile.failure_categories_non_exact_tool_rows.direct_answer_substitution`
- This metric is referenced by tradeoff watch rule:
  - `direct_answer_substitution_delta_gt_3`
  - basis: `delta_vs_baseline`
- Other catalog metrics also point to old schema (`metrics.*`, `failure_profile.*`).

Profile dependency classification:
- `direct_answer_substitution_count` is required by threshold-profile metric mapping and rule graph.
- Not a detector hardcoded metric name.

## 5. Root-Cause Classification
Primary classification:
- `THRESHOLD_PROFILE_STALE_METRIC`

Supporting detail:
- `EVAL_SUMMARY_MISSING_REQUIRED_METRIC` is true symptomatically, but root mismatch is profile/catalog schema drift.
- Baseline is not missing the metric; baseline and threshold profile are aligned for this metric.
- Additional latent mismatch exists: baseline ambiguity for `wrapper_leakage_overall` under current candidate paths.

## 6. Can detector run on already-produced eval summary without rerun?
Yes, but only with schema-compatibility repair in detector/profile behavior.

Hard blocker inventory from this analysis:
- All 8 profile metrics are non-resolvable on current eval summary schema under existing metric catalog.
- 1 of 8 (`wrapper_leakage_overall`) is ambiguous on baseline under existing catalog.



# Stage B First Probe Detector Failure Forensics Addendum

Metric resolvability snapshot:
- profile metrics: 8
- resolvable in eval summary: 0
- resolvable in baseline summary: 7

Non-resolvable in eval summary:
- direct_answer_substitution_count, invalid_json_overall, no_anchor_exact_valid_share, no_call_correctness_adversarial, no_call_correctness_aggregate, read_file_exact_valid_rate, read_file_symbol_name_exact_valid_rate, wrapper_leakage_overall

Non-resolvable in baseline summary:
- wrapper_leakage_overall
