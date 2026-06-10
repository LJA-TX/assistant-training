# Evaluator Semantic Impact Assessment

## Scope

Determine whether the evaluator changes are documentation-only, diagnostics-only, infrastructure-only, scoring-affecting, or behavior-affecting.

## Assessment

| Change | Category | Purpose | Can evaluation results change? |
|---|---|---|---|
| Prompt-trace provenance fields on `EvalRow` | Diagnostics-only / Infrastructure-only | Record render path, fallback use, custom template name, and tokenizer chat-template fingerprint | Not the canonical scoring results; only supplementary evidence can change |
| `_prompt_prefix_with_meta` and `row_index_offset` plumbing | Infrastructure-only | Preserve row identity and emit prompt-trace metadata without changing the rendered prompt text | No canonical scoring change |
| Stage C row-fact builders and family A evidence builders | Diagnostics-only / Infrastructure-only | Emit supplemental evidence artifacts for downstream contract analysis | The supplemental artifacts can change; canonical score metrics should not |
| Failure profile assembly | Diagnostics-only | Produce a secondary breakdown of non-exact tool rows | Yes, the supplemental failure profile can change, but it is not the canonical scorer gate |
| `repo_paths` registry support for the E1 prompt trace script | Infrastructure-only | Make the new evidence-creation path discoverable | No scoring change |

## Scoring Path Check

The canonical scoring functions that drive the main evaluation metrics are unchanged in substance:

- `primary_class` assignment still uses the same parse/schema/wrapper/tool-call logic.
- `class_counts`, `exact_json_validity`, `invalid_json_rate`, `tool_name_accuracy`, `argument_accuracy`, `wrapper_leakage_rate`, and `no_call_correctness` are still computed from the same class outputs.
- The observed row-level differences in the fresh adapter rerun come from different generated texts, not from a changed canonical scoring rule.

## Conclusion

The material changes are Category B/C.
There is no evidence of Category D or Category E drift in the canonical scoring contract.
