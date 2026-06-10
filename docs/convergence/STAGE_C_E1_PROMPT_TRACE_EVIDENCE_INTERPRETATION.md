# Stage C E1 Prompt Trace Evidence Interpretation

## Executive Summary

The E1 render-only bundle now preserves the exact rendered prompts for one representative affected row and one clean control row:

- [prompt trace bundle](/opt/ai-stack/assistant-training/manifests/reports/stage_c_prompt_trace_evidence/stage_c_e1_prompt_trace_20260609T221315792398Z/)
- [prompt_traces.jsonl](/opt/ai-stack/assistant-training/manifests/reports/stage_c_prompt_trace_evidence/stage_c_e1_prompt_trace_20260609T221315792398Z/prompt_traces.jsonl)
- [validation_report.json](/opt/ai-stack/assistant-training/manifests/reports/stage_c_prompt_trace_evidence/stage_c_e1_prompt_trace_20260609T221315792398Z/validation_report.json)

The validation report confirms render-only execution: exact prompt hash match, no generation path, no scoring path, and no detector path. That materially reduces the Stage C blind spot around "what was sent to the model" for the representative rows. It does not, by itself, settle whether the downstream contamination is primarily corpus-construction, prompt/harness construction, or model continuation bias.

## What The Bundle Directly Shows

The two trace records share the same canonical fallback render path:

- `prompt_template_mode=tokenizer_native`
- `render_path_used=generic_roles_v1_fallback`
- `fallback_used=true`
- `custom_template_name=generic_roles_v1`

The affected row (`heldout_validation:2 / p0_rg_search_4`) renders a chat-shaped prompt that includes:

- role delimiters
- the tool name `rg_search`
- the literal string `tool_calls`
- the runtime file path in the user task
- the concise system instruction to use only the exact requested tool and stop when the result is sufficient

The clean control row (`direct_answer:1 / da_92001`) renders the same wrapper shape, but its user message is a generic direct-answer question and does not carry the tool-specific markers above.

The raw prompt snapshots are:

- [affected prompt](/opt/ai-stack/assistant-training/manifests/reports/stage_c_prompt_trace_evidence/stage_c_e1_prompt_trace_20260609T221315792398Z/rows/heldout_validation_2_p0_rg_search_4.prompt.txt)
- [control prompt](/opt/ai-stack/assistant-training/manifests/reports/stage_c_prompt_trace_evidence/stage_c_e1_prompt_trace_20260609T221315792398Z/rows/direct_answer_1_da_92001.prompt.txt)

## What Appears In Generated Text But Not In The Rendered Prompt

E1 itself does not preserve `generated_text`; it is a render-only trace. So there is no new generated-text evidence inside the bundle to compare directly against the prompt snapshots.

Using the earlier Stage C runtime-forensics record, the post-prompt continuation markers for the dominant contaminated regime are still the same continuation-only families identified before E1:

- answer-like prefixes
- transcript replay / contamination tails
- wrapper or prose leakage
- malformed JSON or tool-label repetition

Those markers are output-side continuation phenomena, not prompt-side evidence. E1 does not move them into the prompt surface.

## Hypothesis Impact

| Hypothesis | Effect of E1 | Reading |
|---|---|---|
| Prompt/harness construction | Strengthened | The exact prompt surface is now observed, and it carries the row-specific tool/task content through the same canonical render path. |
| Model continuation bias | Mostly unchanged | E1 does not run generation, so it does not test continuation directly; it only removes uncertainty about the pre-generation surface. |
| Corpus-construction contribution | Slightly strengthened | The affected prompt now shows that the row content itself carries the tool-specific task text that later participates in the contaminated regime. |
| Renderer-only explanation | Weakened | The same renderer produces a clean control prompt and the affected prompt’s special markers come from row content, not from a divergent render path. |

## Affected Versus Control

The affected prompt differs from the clean control prompt in three concrete ways:

1. It is tool-directed rather than direct-answer oriented.
2. It contains the tool marker stack (`rg_search`, `tool_calls`, the runtime file path).
3. It carries the exact tool-use system instruction that was previously only known indirectly from the frozen record.

The control prompt shares the same wrapper structure, but its content is generic and clean.

## Direct Answer

E1 materially reduces the Stage C uncertainty boundary around prompt recovery: we now know the exact rendered prompt for the representative affected row and a clean control row.

It does not materially resolve the remaining causal question. The bundle narrows the space of explanations, but it does not distinguish cleanly between corpus-construction effects, prompt/harness effects, and model continuation bias for the downstream contaminated outputs.
