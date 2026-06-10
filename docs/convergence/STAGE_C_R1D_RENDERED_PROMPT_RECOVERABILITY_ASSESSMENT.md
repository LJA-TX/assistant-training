# Stage C R1D Rendered Prompt Recoverability Assessment

## Executive Summary

This is a strictly observational assessment of the frozen repository record. No code was modified, no runtime evaluations were run, and no datasets, detectors, scorers, thresholds, governance controls, migration status, or training artifacts were changed.

The key conclusion is narrow:

- **The exact rendered prompts for the affected Stage C rows are not recoverable from existing Stage C evidence.**

What is preserved:

- the underlying `system` and `user` message content in the canonical datasets
- the prompt contract and rendering path in the evaluator code and manifest
- the model continuation in `generated_text`
- exact prompt-prefix tails for some unrelated Stage B snapshot rows

What is missing:

- a row-level rendered prompt snapshot for the affected Stage C rows
- the exact tokenizer chat template text for the frozen `llama-3.1-8b-base` revision as a repository artifact
- a per-row record showing whether tokenizer-native rendering or fallback rendering was used

So the repository supports **prompt-family reconstruction** with moderate confidence, but not **exact row-level prompt recovery** for the affected Stage C cohort.

## A. Prompt Recoverability Inventory

### Artifact Families

| Artifact family | Path(s) | What it preserves | Relevance to Stage C recoverability |
|---|---|---|---|
| Canonical input datasets | [evals/data/canonical_v1/heldout_validation.jsonl](/opt/ai-stack/assistant-training/evals/data/canonical_v1/heldout_validation.jsonl#L1), [evals/data/canonical_v1/tool_holdout.jsonl](/opt/ai-stack/assistant-training/evals/data/canonical_v1/tool_holdout.jsonl#L10) | Exact `messages` content for each row, including `system` and `user` text; tool rows also preserve assistant `tool_calls` targets in the source record | Directly preserves the input message content, but not the rendered prompt string |
| Canonical eval manifest | [evals/canonical_eval_manifest_v1.json](/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json#L16) | `chat_template_mode`, `add_generation_prompt`, `allow_custom_fallback`, `custom_template_name`, and frozen `prompt_contract` | Directly preserves the intended prompt construction rule, but not the per-row rendered prompt |
| Evaluator implementation | [scripts/eval_canonical_manifest.py](/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py#L801) | The concrete rendering path: chat-template application when available, fallback to `generic_roles_v1`, then prompt-prefix tokenization and continuation-only decoding | Directly preserves the construction algorithm, but not the exact row-specific rendered prompt text |
| Stage C comparison rows | [evals/runs/canonical_eval_20260526T112440Z/comparison_rows.jsonl](/opt/ai-stack/assistant-training/evals/runs/canonical_eval_20260526T112440Z/comparison_rows.jsonl#L41) | `user_prompt`, `generated_text`, parse status, schema status, tool prediction outputs | Preserves the prompt input text and model continuation, but not the rendered prompt prefix itself |
| Stage B prompt-prefix snapshots | [manifests/reports/stage_b_v1_i10r_residual_nocall_probe_masking_audit_raw.snapshot.json](/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_residual_nocall_probe_masking_audit_raw.snapshot.json#L13), [manifests/reports/stage_b_v1_i10r_counterbalanced_probe_masking_audit_raw.snapshot.json](/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_counterbalanced_probe_masking_audit_raw.snapshot.json#L13), [manifests/reports/stage_b_v1_i10r_nocall_probe_masking_audit_raw.snapshot.json](/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_nocall_probe_masking_audit_raw.snapshot.json#L13) | `prompt_template_mode`, `fallback_used`, `custom_template_name`, and `decoded_prompt_prefix_tail` for selected Stage B rows such as `ra_00326`, `nc_00193`, `i3_cov_find_files_003`, `rp_50007`, and `i3_debug_tools_010` | Demonstrates that exact prompt-prefix tails can be archived, but these snapshots do not cover the affected Stage C `p0_*` / `p2_*` rows |

### Representative Stage C Rows

| Representative row | Preserved prompt components | Missing prompt components |
|---|---|---|
| `heldout_validation:1` / `p0_read_file_2` | `system` text, `user` text, `source_case_id`, expected tool metadata, `generated_text` continuation | Exact rendered prompt string, tokenizer template text, per-row render-path flag |
| `heldout_validation:2` / `p0_rg_search_4` | `system` text, `user` text, `source_case_id`, expected tool metadata, `generated_text` continuation | Exact rendered prompt string, tokenizer template text, per-row render-path flag |
| `heldout_validation:3` / `p0_read_file_3` | `system` text, `user` text, `source_case_id`, expected tool metadata, `generated_text` continuation | Exact rendered prompt string, tokenizer template text, per-row render-path flag |
| `tool_holdout:15` / `p2_debug_tools_1` | `system` text, `user` text, `source_case_id`, expected tool metadata, `generated_text` continuation | Exact rendered prompt string, tokenizer template text, per-row render-path flag |
| `tool_holdout:10` / `p2_get_system_datetime_1` | `system` text, `user` text, `source_case_id`, expected tool metadata, `generated_text` continuation | Exact rendered prompt string, tokenizer template text, per-row render-path flag |

### Inventory Assessment

The repository preserves the ingredients needed to describe the prompt construction path, but not the exact rendered prompt for the affected Stage C rows.

The only exact prompt renderings I found are in Stage B snapshot artifacts, and those are for unrelated representative rows, not for the affected Stage C cohort.

## B. Reconstruction Feasibility Assessment

| Reconstruction target | Feasibility from existing repo artifacts | Confidence | Why |
|---|---|---|---|
| Prompt-family / skeleton reconstruction | Feasible | Moderate to high | The datasets preserve the `system` and `user` messages, and the manifest/code preserve the rendering rule |
| Exact row-level prompt recovery for the affected Stage C rows | Not feasible | High | No Stage C artifact stores the rendered prompt prefix, and no Stage C artifact stores the tokenizer-specific template text needed to rebuild it exactly |
| Exact row-level prompt recovery for unrelated Stage B snapshot rows | Feasible for the rows actually snapshotted | High | Those artifacts include `decoded_prompt_prefix_tail` and the render-path flags |
| Deterministic exact reconstruction from Stage C evidence alone | Not feasible | High | The prompt text itself is absent, and the row-level render-path choice is not recorded |

### What can be reconstructed

- The prompt is chat-structured.
- The prompt is built from the first `system` and `user` messages.
- A generation prompt is appended.
- The continuation is decoded without the prompt prefix.

### What cannot be reconstructed

- The exact rendered prompt string for the affected Stage C rows.
- Whether the tokenizer-native path or the fallback path was used for any specific affected row.
- The exact tokenizer chat template string at the frozen revision.

## C. Missing-Evidence Analysis

The minimum information missing for exact reconstruction is:

1. the exact rendered prompt text for each affected row, or an equivalent row-level `prompt_prefix` snapshot
2. the exact tokenizer chat template text for the frozen `llama-3.1-8b-base` revision if native rendering was used
3. a per-row indicator of whether the tokenizer-native path or the fallback path rendered that row

The repository already preserves:

- the row messages
- the prompt contract
- the rendering algorithm
- the generated continuation

That is sufficient for family-level reconstruction, but not for exact row-level recovery.

## D. Confidence Assessment

| Conclusion | Confidence | Why |
|---|---|---|
| The exact rendered prompts for the affected Stage C rows are not recoverable from existing Stage C evidence | High | No Stage C artifact stores the rendered prompt text or a row-level render trace |
| Prompt-family reconstruction is possible | Moderate to high | The message content and prompt contract are both preserved |
| Stage B snapshot artifacts preserve exact prompt-prefix tails for some unrelated rows | High | The Stage B masking-audit snapshots explicitly store `decoded_prompt_prefix_tail` and render-path flags |
| The affected Stage C rows are not covered by those exact Stage B prompt snapshots | High | The exact `p0_*` / `p2_*` affected rows do not appear in the prompt-prefix snapshot artifacts reviewed here |
| A row-specific native-vs-fallback decision cannot be inferred with high confidence from the current record | High | That decision is not recorded per affected row |

## E. Direct Answer

**Can the exact rendered prompts for the affected rows be recovered from existing Stage C evidence?**

No.

The existing Stage C record preserves the prompt inputs and the continuation output, but not the exact rendered prompt strings for the affected rows. Exact recovery would require either:

- a row-level rendered prompt snapshot for each affected row, or
- the exact frozen tokenizer chat template plus a per-row render-path record that identifies native versus fallback rendering

Neither is present in the Stage C evidence set.
