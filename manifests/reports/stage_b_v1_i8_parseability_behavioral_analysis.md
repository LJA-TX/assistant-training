# Stage B v1 i8 Parseability Behavioral Analysis

- Generated (UTC): 2026-05-26T18:44:13Z
- Scope: behavioral forensics only (no training, no eval reruns, no dataset mutation).
- Focus tools: `rg_search`, `read_file`

## Source Artifacts
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_canonical_eval_summary.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_parseability_spill_guard_gate_assessment.json`
- `/opt/ai-stack/assistant-training/evals/runs/canonical_eval_20260526T172855Z/summary.json`
- `/opt/ai-stack/assistant-training/evals/runs/canonical_eval_20260526T172855Z/comparison_rows.jsonl`
- `/opt/ai-stack/assistant-training/evals/runs/canonical_eval_20260526T115513Z/summary.json`
- `/opt/ai-stack/assistant-training/evals/runs/canonical_eval_20260526T115513Z/comparison_rows.jsonl`

## Key Quantitative Readout
- i8 heldout `invalid_json`: **0.57** (i3: 0.43, i6: 0.39, i7: 0.66)
- i8 tool-expected `payload_not_parsed`: **82** (i7: 81, i6: 51, i3: 55)
- i8 spill composite (`payload_not_object + missing_tool_calls`): **54** (i7: 57, i3: 80)
- i8 exact-valid tool rows: **4/140** (all on `rg_search`)

## Commitment Failure Modes (Behavior-Level)
- `textual_result_substitution`: 54 (39.7% of non-exact tool rows)
- `scalar_result_substitution_nonobject`: 25 (18.4% of non-exact tool rows)
- `near_canonical_wrapper_key_drift`: 19 (14.0% of non-exact tool rows)
- `near_canonical_missing_tool_calls_envelope`: 16 (11.8% of non-exact tool rows)
- `scalar_or_token_result_substitution`: 11 (8.1% of non-exact tool rows)
- `code_excerpt_result_substitution`: 6 (4.4% of non-exact tool rows)
- `other_malformed_nonjson`: 3 (2.2% of non-exact tool rows)
- `noncanonical_object_missing_tool_calls`: 2 (1.5% of non-exact tool rows)

- Structural near misses: **37/136 (27.2%)**
- Semantic result substitution: **96/136 (70.6%)**
- Refusal-like noncommitment: **0** rows

## Parseability vs Spill Dynamics
- i7 -> i8 `invalid_json`: 0.66 -> 0.57 (improved by -0.09)
- i7 -> i8 `payload_not_object`: 39 -> 25 (improved by -14)
- i7 -> i8 `missing_tool_calls`: 18 -> 29 (worse by +11)
- i7 -> i8 spill composite: 57 -> 54 (improved by -3)
- Signature: spill got modestly better while parseability did not recover, consistent with reduced malformed-object behavior but persistent canonical-emission non-commitment.

## Canonical Emission Confidence Signals
- Exact-valid success is lexically concentrated: `pattern="tool_calls"` accounts for all exact-valid rows (`lexical_anchor_dependence=True`).
- `read_file` exact-valid rate: 0.000 (0 successes).
- `rg_search` exact-valid rate: 0.077.
- Decode-cap pressure among non-exact rows: 14/136 (10.3%).

## Tool-Specific Behavior
### rg_search
- `scalar_result_substitution_nonobject` + `match_count_only` + `pattern_def_create_app_literal`: 9 rows (18.8% of rg_search failures)
- `textual_result_substitution` + `other` + `pattern_validate_tool_arguments_literal`: 6 rows (12.5% of rg_search failures)
- `scalar_result_substitution_nonobject` + `match_count_only` + `pattern_tool_parse_mode_literal`: 6 rows (12.5% of rg_search failures)
- `near_canonical_wrapper_key_drift` + `binary_presence_report` + `pattern_contract_violation_literal`: 5 rows (10.4% of rg_search failures)
- `code_excerpt_result_substitution` + `symbol_extraction` + `pattern_regex_complex`: 4 rows (8.3% of rg_search failures)
### read_file
- `textual_result_substitution` + `symbol_extraction` + `range_1_25`: 7 rows (25.9% of read_file failures)
- `textual_result_substitution` + `symbol_extraction` + `range_1080_1104`: 6 rows (22.2% of read_file failures)
- `textual_result_substitution` + `range_presence_check` + `range_1500_1560`: 4 rows (14.8% of read_file failures)
- `near_canonical_wrapper_key_drift` + `range_presence_check` + `range_1500_1560`: 2 rows (7.4% of read_file failures)
- `scalar_or_token_result_substitution` + `symbol_extraction` + `range_1080_1104`: 2 rows (7.4% of read_file failures)

## Required Explicit Conclusions
- **regime**: serialization inhibition with uncertainty-averse non-commitment; not primary task misunderstanding.
- **structural_vs_semantic**: failures are predominantly semantically on-task but non-canonical (result substitution), with substantial structural near-miss subset.
- **knows_what_to_do**: yes in many cases; outputs often contain expected tool names/arguments or plausible task results, but canonical envelope commitment fails.
- **metrics_hiding_near_success**: yes; invalid_json/invalid_schema aggregate hides near-canonical wrapper-key drift and semantically correct result-substitution attempts.
- **more_dataset_hygiene_help**: likely low-to-moderate marginal impact alone; hygiene already improved spill stability without parseability recovery.
- **most_likely_leverage_point**: target canonical-emission commitment training that rewards exact envelope serialization under uncertainty while preserving current spill/no-call invariants.

## Most Likely Leverage Point
- Primary leverage is **canonical-emission commitment training**, not additional hygiene-first rebalancing.
- Immediate design focus should be near-miss repair: convert result-substitution + wrapper-key-drift outputs into strict `tool_calls` envelope outputs while preserving no-call/wrapper leakage invariants.
