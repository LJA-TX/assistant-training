# Stage C E1 Prompt Trace Evidence Creation Plan

## Executive Summary

This is a design-only plan for the smallest experiment that can create the missing Stage C prompt evidence. No code is modified here, no runtime evaluation is run here, and no generation, scoring, detector execution, migration work, or retraining is proposed.

The minimum useful experiment is a **render-only prompt trace** on exactly two rows:

- one representative affected row from the dominant contaminated cohort
- one representative clean control row from the direct-answer family

The experiment must preserve the exact rendered prompt text, the render-path metadata, and the provenance needed to replay the render deterministically later. The raw prompt snapshot, not a tail excerpt, must become the durable evidence object.

## A. Experiment Design

### A1. Repository Components Exercised

| Component | Role in the experiment | Why it is required |
|---|---|---|
| [scripts/eval_canonical_manifest.py](/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py) | Prompt construction path | This is the canonical Stage C evaluator path that already defines `_build_rows`, `_prompt_prefix`, and `_render_custom_prompt_prefix`. The experiment should stop after render and never enter `_infer` or downstream classification. |
| [evals/canonical_eval_manifest_v1.json](/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json) | Frozen render contract | This file defines the tokenizer path, `chat_template_mode`, `add_generation_prompt`, `allow_custom_fallback`, and the prompt contract used for Stage C. |
| [evals/data/canonical_v1/heldout_validation.jsonl](/opt/ai-stack/assistant-training/evals/data/canonical_v1/heldout_validation.jsonl) | Affected-row source | This split contains the dominant contaminated regime and the selected affected row. |
| [evals/data/canonical_v1/direct_answer.jsonl](/opt/ai-stack/assistant-training/evals/data/canonical_v1/direct_answer.jsonl) | Clean control source | This split provides a clean direct-answer comparison row under the same evaluator contract. |
| `llama-3.1-8b-base` tokenizer | Chat-template renderer | The exact rendered prompt depends on the tokenizer-native chat template when present, or the documented fallback when not. |

If the experiment is wired through the existing evaluator module rather than a narrow helper, the import chain will also include [scripts/stage_c1_evaluator_foundation.py](/opt/ai-stack/assistant-training/scripts/stage_c1_evaluator_foundation.py), but the prompt-trace evidence itself should still come only from the render path.

### A2. Row Selection

| Row role | Selected row | Selection rationale |
|---|---|---|
| Representative affected row | `heldout_validation:2` / `p0_rg_search_4` | This row is already a clear member of the dominant prompt/task-echo regime and is one of the canonical affected examples used throughout the Stage C analyses. |
| Representative clean control row | `direct_answer:1` / `da_92001` | This row is a clean direct-answer control from the same frozen evaluation family and exercises the same prompt renderer without belonging to the contaminated cohort. |

The experiment should not broaden beyond these two rows. The point is not more sampling. The point is to create the missing exact prompt evidence with the smallest possible scope.

### A3. Minimal Procedure

1. Load the frozen manifest and the selected dataset rows.
2. Build the row objects using the existing prompt-construction path.
3. Render the prompt prefix for each selected row.
4. Capture the exact rendered prompt text and its provenance.
5. Stop before model generation, scoring, detector execution, or migration logic.

The experiment is render-only. No `model.generate`, no classifier pass, and no postprocessing beyond hash and integrity capture.

## B. Artifact Specification

### B1. Required Artifact Set

| Artifact | Recommended path family | Purpose |
|---|---|---|
| Run manifest | `manifests/reports/stage_c_prompt_trace_evidence/<run_id>/manifest.json` | Records the exact manifest, tokenizer, dataset, and render-contract provenance for the trace. |
| Row index | `manifests/reports/stage_c_prompt_trace_evidence/<run_id>/prompt_traces.jsonl` | One row per traced example; this is the machine-readable index and audit trail. |
| Raw prompt snapshot | `manifests/reports/stage_c_prompt_trace_evidence/<run_id>/rows/<split>_<row_index>_<source_case_id>.prompt.txt` | Byte-exact rendered prompt text, preserved without truncation or normalization. This is the evidence object. |
| Validation report | `manifests/reports/stage_c_prompt_trace_evidence/<run_id>/validation_report.json` | Records validator outcomes and any failures. |

### B2. What Each Snapshot Must Contain

Each row record should include the exact rendered prompt plus enough context to make the snapshot self-authenticating later. The raw prompt file should preserve the exact text; the JSONL index should point to that file and carry hashes and provenance.

Recommended row-record fields:

| Field | Purpose |
|---|---|
| `trace_id` | Stable identifier for the trace record |
| `split` | Source split name |
| `row_index_1based` | Source row position |
| `source_case_id` | Canonical row identity |
| `dataset_path` | Source dataset file |
| `dataset_sha256` | Dataset immutability check |
| `manifest_path` | Manifest used to render the prompt |
| `manifest_sha256` | Manifest immutability check |
| `system_text` | Exact system message used as input |
| `user_text` | Exact user message used as input |
| `render_path_used` | `tokenizer_native` or `generic_roles_v1_fallback` |
| `fallback_used` | Boolean render-path flag |
| `custom_template_name` | Fallback template identity when used |
| `tokenizer_path` | Exact tokenizer source |
| `tokenizer_chat_template_text` | Exact template text when available |
| `tokenizer_chat_template_sha256` | Template fingerprint |
| `rendered_prompt_path` | Path to the raw prompt file |
| `rendered_prompt_sha256` | Exact prompt hash |
| `rendered_prompt_char_count` | Length sanity check |
| `rendered_prompt_token_count` | Token-count sanity check |
| `prompt_contract` | Frozen render contract string |
| `captured_utc` | Capture timestamp |

The prompt file itself must be the canonical evidence. The JSON index is only the index.

### B3. Storage Rules

- Store the bundle as an immutable, versioned evidence artifact under `manifests/reports/`.
- Keep the raw prompt in a plain UTF-8 text file so exact line breaks are preserved.
- Keep the JSONL index separate from the raw prompt text so escaping does not obscure the evidence.
- Do not store only excerpts or tail snippets.
- Do not rely on `generated_text` or later reconstruction to stand in for the prompt snapshot.

## C. Metadata Specification

### C1. Run-Level Metadata

| Field | Why it matters |
|---|---|
| `run_id` | Unambiguous bundle identity |
| `created_utc` | Capture time |
| `manifest_path` | Frozen evaluation contract |
| `manifest_sha256` | Integrity of the contract file |
| `tokenizer_path` | Exact tokenizer source used for rendering |
| `tokenizer_revision` | If available, the exact tokenizer revision |
| `chat_template_mode` | Whether the renderer used tokenizer-native or fallback logic |
| `add_generation_prompt` | Ensures the assistant prefix is recorded correctly |
| `allow_custom_fallback` | Records whether fallback was permitted |
| `custom_template_name` | Records the fallback template identity |
| `render_only` | Must be `true` |
| `generation_invoked` | Must be `false` |
| `scoring_invoked` | Must be `false` |
| `detector_invoked` | Must be `false` |

### C2. Row-Level Metadata

| Field | Why it matters |
|---|---|
| `split` | Source partition |
| `row_index_1based` | Stable row address inside the split |
| `source_case_id` | Canonical row identity |
| `system_text_sha256` | Input provenance |
| `user_text_sha256` | Input provenance |
| `render_path_used` | Distinguishes native rendering from fallback rendering |
| `fallback_used` | Makes the render decision machine-readable |
| `rendered_prompt_sha256` | Exact prompt identity |
| `rendered_prompt_char_count` | Guards against truncation |
| `rendered_prompt_token_count` | Guards against accidental reserialization |
| `prompt_prefix_tail` | Optional quick-review aid only; not a substitute for the raw prompt |

### C3. How This Avoids the Old Blind Spot

The blind spot in Stage C was that the evidence record preserved messages and continuations but not the exact rendered prompt. The storage design above fixes that by making the raw prompt the authoritative object and by attaching enough metadata to re-derive or verify it later without ambiguity.

## D. Validation Specification

### D1. Required Validators

| Validator | Pass condition | Failure meaning |
|---|---|---|
| Row resolution validator | Each selected row resolves to exactly one dataset record | The trace is addressing the wrong row or an ambiguous row identity |
| Render exactness validator | The raw prompt text matches the prompt produced by the render path for that row | The snapshot is not an exact prompt trace |
| Hash validator | `rendered_prompt_sha256` matches the raw prompt bytes | The snapshot was altered, truncated, or misrecorded |
| Template provenance validator | The recorded template identity matches the actual render path | The render contract is incomplete |
| No-generation validator | No generation or scoring path was entered | The experiment exceeded its minimal evidence-only scope |
| Control cleanliness validator | The control row renders without the contamination markers observed in the affected row | The control is not a useful comparator and should be replaced |
| Completeness validator | Both selected rows have all required metadata fields and raw prompt files | The bundle is not self-sufficient as evidence |

### D2. Integrity Checks

- Verify UTF-8 preservation and newline preservation in the raw prompt file.
- Verify that the prompt snapshot is not truncated.
- Verify that row identity in the filename, JSONL index, and source dataset all agree.
- Verify that the prompt file hash and the JSONL index hash chain agree.
- Verify that the run manifest records `render_only=true` and all excluded surfaces as `false`.

## E. Expected Information Gain Assessment

### E1. What This Experiment Would Create

| Evidence created | Value |
|---|---|
| Exact rendered prompt for the affected row | Shows whether the contamination markers were already present before model continuation |
| Exact rendered prompt for the clean control row | Establishes a clean comparison under the same render contract |
| Render-path metadata | Distinguishes tokenizer-native rendering from fallback rendering |
| Template text or template fingerprint | Makes the prompt path reproducible later |
| Stable hashes and row IDs | Makes the evidence auditable and comparable across future analyses |

### E2. What It Would Strengthen or Weaken

| If the trace shows... | It strengthens | It weakens |
|---|---|---|
| The affected-row prompt already contains the echoed instruction or role markers | Prompt/harness construction as a carrier of the marker set; mixed-source contamination with a stronger prompt component | Pure continuation-only explanations |
| The affected-row prompt is clean and the control row is also clean | The case for the markers arising after rendering, not before it | Prompt-origin explanations that require the marker set to be present in the prompt |
| The affected row uses a different render path than the control row | Render-path differences as a real contributor | Claims that rendering mode is irrelevant |
| The affected and control rows share the same render path and only the affected row carries the suspicious text in its rendered prompt | Corpus-construction or prompt-source effects upstream of generation | Renderer-only explanations |

### E3. Remaining Limits After the Experiment

This experiment would not, by itself, prove corpus-construction contamination or model continuation bias. It would create the exact prompt evidence needed to compare those hypotheses against the rendered input surface instead of guessing from continuation-only artifacts.

### E4. Net Information Gain

The gain is high because the experiment turns the largest remaining Stage C uncertainty into a first-class artifact. It does so with the smallest possible scope: two rows, render only, no generation, and no scoring.
