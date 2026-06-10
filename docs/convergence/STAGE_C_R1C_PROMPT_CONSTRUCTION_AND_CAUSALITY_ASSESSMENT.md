# Stage C R1C Prompt Construction And Causality Assessment

## Executive Summary

This is a strictly observational assessment of the frozen Stage C evidence set. No code was modified, no new runtime evaluations were run, and no datasets, detectors, scorers, thresholds, governance controls, migration status, or training artifacts were changed.

The best supported causal reading is **D: a combination of corpus-construction effects, prompt/harness construction effects, and model continuation bias**.

What is directly evidenced:

1. The frozen evaluation pipeline is chat-template based and builds a prompt from the first `system` and `user` messages before generation.
2. The decoder strips the prompt and records only the model continuation in `generated_text`.
3. The dominant Stage C regime is prompt/task echo with transcript contamination.
4. The exact echoed system instruction exists in training-style tool data.

What is not directly evidenced:

1. The exact rendered prompt for the affected rows.
2. Whether the literal bracketed role markers were present in the prompt text or were generated during continuation.
3. Whether the echoed instruction entered the frozen outputs primarily through corpus construction, prompt serialization, or model memorization.

Bottom line:

1. Prompt/harness construction is the best evidenced proximal mechanism.
2. Model continuation bias is a necessary explanation for the observed continuation text.
3. Corpus-construction contamination remains plausible and supported by matching training-style data, but it is not isolated directly in the affected rows.

## Direct Answers

### What do we already know?

- The evaluator requires the first two messages to be `system` and `user`, stores them as `system_text` and `user_text`, and constructs `prompt_prefix` from them. See [scripts/eval_canonical_manifest.py](/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py#L845) and [scripts/eval_canonical_manifest.py](/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py#L861).
- The frozen manifest sets `chat_template_mode` to `tokenizer_native`, enables `add_generation_prompt`, and freezes the prompt contract as `tokenizer.apply_chat_template(messages, add_generation_prompt=true)`. See [evals/canonical_eval_manifest_v1.json](/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json#L19) and [evals/canonical_eval_manifest_v1.json](/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json#L116).
- The inference path tokenizes `row.prompt_prefix`, generates continuation, slices off the prompt tokens, and decodes only the new tokens. See [scripts/eval_canonical_manifest.py](/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py#L924) and [scripts/eval_canonical_manifest.py](/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py#L940).
- The authoritative missing-evidence cohort is dominated by prompt/task echo with transcript contamination, and the three ambiguous rows are boundary cases of that same regime. See [docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md#L112) and [docs/convergence/STAGE_C_R1A_RUNTIME_REGIME_CHARACTERIZATION_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_R1A_RUNTIME_REGIME_CHARACTERIZATION_ASSESSMENT.md#L14).
- The exact system instruction that reappears in the contaminated outputs is present in tool fine-tune style data. See [data/tool_ft_allaliases_20260525_from_qual_reports.jsonl](/opt/ai-stack/assistant-training/data/tool_ft_allaliases_20260525_from_qual_reports.jsonl#L1).
- The separate direct-answer control set uses a different system prompt. See [evals/data/canonical_v1/direct_answer.jsonl](/opt/ai-stack/assistant-training/evals/data/canonical_v1/direct_answer.jsonl#L1).

### What do we think we know?

- The observed runtime strings are best explained as transcript continuation over a chat-shaped prompt, not as clean direct-answer or scalar outputs.
- The prompt/harness path is likely a proximate contributor because the model is conditioned on a serialized chat prompt before generation.
- The exact echoed instruction is likely tied to earlier chat-formatted training or corpus construction, but the current artifacts do not isolate which stage introduced it.
- The literal `[SYSTEM]` and `[USER]` markers in the frozen outputs are not proof that those exact literals were in the prompt text for the affected rows.

### What do we not yet know?

- The exact rendered prompt for representative affected rows.
- Whether tokenizer-native template rendering or the custom `generic_roles_v1` fallback was actually used for any affected row.
- Whether the echoed system instruction is primarily a corpus-construction artifact, a prompt-serialization artifact, or a model memorization artifact.
- Whether corpus-construction effects dominate over prompt/harness effects, or whether they are simply co-contributors to the same output shape.

## A. Prompt Construction Trace Assessment

### Trace

| Step | What the artifacts show | Directness |
|---|---|---|
| Source row | The evaluator reads row metadata, requires a `system` message followed by a `user` message, and carries `source_case_id` through the row object. | Direct |
| Prompt serialization | The prompt is built as `prompt_prefix` using `tokenizer.apply_chat_template(messages, add_generation_prompt=true)` when available, with a `generic_roles_v1` fallback that renders `[SYSTEM]`, `[USER]`, and `[ASSISTANT]`. | Direct for the construction path, indirect for row-specific rendered text |
| Model inference | The prompt prefix is tokenized with `add_special_tokens=False`, the model generates, and only the new tokens after the prompt are decoded. | Direct |
| Output artifact | `generated_text` contains the continuation only, not the prompt prefix. | Direct |

### Representative frozen rows

| Representative row | Observable regime in the frozen output | Why it matters for prompt construction |
|---|---|---|
| `heldout_validation:1` | Task/prompt echo with transcript contamination | Shows the prompt-shaped task text is being replayed in continuation. See [docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md#L112). |
| `heldout_validation:4` | Pure transcript contamination | Shows literal transcript markers can appear without a stronger task echo. See [docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md#L115). |
| `heldout_validation:10` | Answer-prefix plus transcript contamination | Shows the model can start an answer and then fall back into transcript replay. See [docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md#L118). |
| `heldout_validation:44` | Instructional assertion plus transcript contamination | Shows meta-instruction text can appear before transcript replay. See [docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md#L121). |
| `heldout_validation:11` | Tool-label repetition | Shows a degenerate repetition mode rather than a clean payload. See [docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md#L124). |
| `heldout_validation:50` | Task/prompt echo without transcript contamination | Shows the task text can be echoed even when the transcript markers are absent. See [docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md#L127). |

### Assessment

The prompt construction path is known at the pipeline level, but not at the exact row-rendered-text level. The artifacts show a chat-style prompt builder, a generation prompt append, and a continuation-only decode path. They do not preserve the rendered prompt text for the affected rows.

That means the transcript markers seen in `generated_text` are observable outputs, but they are not direct proof that the same literals were already present in the prompt text sent to the model.

## B. Prompt Marker Provenance Analysis

| Marker or motif | Where it is observed | Was it already present in the rendered prompt? | Evidence strength | Interpretation |
|---|---|---|---|---|
| `system` / `user` message structure | In the input row messages and in the evaluator's prompt construction path | Yes, semantically. The row is built from those messages and rendered as a chat prompt. | High | This is the least ambiguous part of the prompt path. |
| Literal `[SYSTEM]` / `[USER]` delimiters | In the frozen outputs and in the fallback template definition | Not directly proven for the affected rows | Moderate | Could come from fallback serialization, tokenizer chat template behavior, or model continuation. |
| Exact echoed system instruction | In tool fine-tune style data and in the frozen outputs | Not directly proven for the affected rows | Moderate | Supports training-style reuse or memorization, but not a row-specific prompt snapshot. |
| Echoed task text | In user messages and in replayed output text | The user task is in the prompt; the echoed longer fragment is output continuation | High for user text, moderate for the replay | Supports prompt/task echo, but not a unique causal source. |
| Transcript contamination | In the frozen outputs | No direct evidence that the transcript markers existed verbatim in the prompt text | High as output evidence, low as prompt evidence | Strong sign of continuation behavior. |
| Wrapper leakage / tool-label repetition / answer-like prefixes | In the frozen outputs and operational sample artifacts | No direct evidence that these were in the prompt text | High as output evidence | These are continuation artifacts, not clean prompt evidence. |

### Prompt provenance conclusion

There is **no direct evidence** that the full contamination marker set already existed verbatim in the prompt text for the affected rows.

There **is** direct evidence that:

1. the prompt was chat-structured,
2. the generation prompt was appended,
3. the decoder recorded only continuation,
4. the exact echoed instruction exists in training-style chat data.

That combination is enough to support a mixed causal reading, but not enough to isolate the literal source of the echoed text.

## C. Competing Causal Hypothesis Comparison

| Hypothesis | Evidence for | Evidence against or limit | Current judgment | Confidence |
|---|---|---|---|---|
| Corpus-construction effects | The exact echoed instruction exists in tool fine-tune style data; the adversarial review notes this exact match is under-leveraged; the dominant outputs look like replayed prompt text. | No exact rendered prompt for affected rows; no direct upstream builder trace showing the contamination was injected during corpus construction. | Plausible upstream contributor, but not isolated | Moderate |
| Prompt/harness construction effects | The evaluator explicitly builds a chat prompt from `system` and `user` messages; the manifest freezes `tokenizer.apply_chat_template(messages, add_generation_prompt=true)`; the adversarial review says the exact rendered prompt is missing and eval-time prompt construction could be the proximate source. | No per-row rendered prompt snapshot; no proof that the custom fallback was used on affected rows. | Best evidenced proximal mechanism | High |
| Model continuation bias | The decoder keeps only the continuation after the prompt; the outputs show transcript replay, answer-like prefixes, and wrapper leakage; this is consistent with autoregressive continuation on a chat-formatted prompt. | Cannot be separated cleanly from prompt/harness or corpus effects without the exact prompt snapshot or an ablation. | Strong contributing mechanism | High |
| Combination of the above | All three mechanisms fit the same observed marker stack and the same missing-evidence gap. | None that is stronger than the evidence for each component individually. | Best overall explanation | High |

### Causal bottom line

If the question is "what best explains the observable frozen outputs," the answer is **D, with B and C the best-supported mechanisms**.

If the question is "where did the exact echoed instruction come from," the answer remains **underdetermined** between corpus construction, prompt serialization, and model memorization.

## D. Confidence Assessment

| Conclusion | Confidence | Why |
|---|---|---|
| The prompt pipeline is chat-template based and continuation-only decode is used. | High | The evaluator code and manifest state this directly. |
| The dominant regime is transcript-contaminated prompt/task echo. | High | The runtime-forensics cohort partitions it explicitly. |
| The exact rendered prompt for affected rows is unavailable. | High | No artifact in the reviewed set archives it. |
| Prompt/harness construction contributes materially. | High | The prompt builder is explicit and proximate to generation. |
| Model continuation bias contributes materially. | High | The output artifact is continuation only, and the observed markers are continuation-shaped. |
| Corpus-construction contamination contributes. | Moderate | Exact instruction overlap with training-style data is strong evidence, but it is not row-specific proof. |
| Literal `[SYSTEM]` / `[USER]` markers were already present in the prompt text for the affected rows. | Low | The rendered prompt is not archived, so this remains speculative. |
| A single-source explanation is sufficient. | Low | The observed marker stack is better explained as a combination. |

## Final Answer

The most defensible Stage C-R1C conclusion is that the dominant contamination regime is best explained by a **combination** of corpus-construction effects, prompt/harness construction effects, and model continuation bias.

The strongest direct evidence is for the **prompt/harness path** and **model continuation bias**. Corpus-construction contamination remains plausible and important, but the frozen artifacts do not isolate it as the unique or primary cause of the echoed markers.
