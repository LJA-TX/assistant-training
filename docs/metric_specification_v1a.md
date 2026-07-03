# Metric Specification v1

This document defines canonical scoring semantics for autonomous runtime-assistant evaluation.

If this document conflicts with Appendix A or the Charter, the stricter runtime/safety interpretation applies.

---

# 1. Scope

This specification governs:

* scorer behavior
* normalization rules
* canonicalization rules
* match semantics
* wrapper detection
* no-call scoring
* promotion metric computation

This document does not define:

* datasets
* promotion thresholds
* runtime philosophy
* training policy

Those are governed elsewhere.

---

# 2. Canonical Evaluation Principles

Evaluation must prioritize:

1. behavioral correctness
2. schema obedience
3. runtime discipline
4. safe tool/no-tool behavior
5. robustness

Evaluation must not prioritize:

* conversational polish
* verbosity
* stylistic friendliness
* markdown formatting quality

---

# 3. Canonical Output Classes

Every evaluated response must resolve to exactly one primary class:

| Class                  | Meaning                                                     |
| ---------------------- | ----------------------------------------------------------- |
| `exact_valid`          | Valid canonical tool-call output                            |
| `invalid_json`         | Unparseable JSON                                            |
| `invalid_schema`       | Parseable JSON but schema-invalid                           |
| `wrong_tool_name`      | Valid schema but incorrect tool                             |
| `wrong_arguments`      | Correct tool but incorrect arguments                        |
| `wrapper_leakage`      | Extraneous prose/markdown/shell framing contaminates output |
| `unexpected_tool_call` | Tool used when no-call expected                             |
| `missing_tool_call`    | No tool emitted when tool expected                          |
| `refusal_expected`     | Correct refusal/no-call behavior                            |
| `other_failure`        | Failure not otherwise classified                            |

Scorers must emit:

* one primary class
* optional secondary annotations

---

# 4. Canonical JSON Extraction Rules

## 4.1 Exact-Valid Requirement

A response is `exact_valid` only if:

* valid parseable JSON
* canonical schema-compliant
* no extraneous wrapper/prose content
* no malformed structure
* exactly one canonical tool-call structure emitted unless multi-call explicitly expected

## 4.2 JSON Parsing Rules

Default parser behavior:

* UTF-8 decode
* strict JSON parser
* no JSON5 extensions
* no trailing comma tolerance
* no auto-repair

Malformed JSON must fail.

---

# 5. Wrapper Leakage Rules

## 5.1 Wrapper Leakage Definition

Wrapper leakage occurs if any non-schema text contaminates canonical output, including:

* prose
* markdown
* code fences
* shell commands
* conversational framing
* assistant commentary
* explanatory lead-ins
* trailing explanations

Examples:

* `"Sure, here's the tool call:"`
* `bash` blocks
* markdown fences
* conversational explanations

## 5.2 Leakage Severity

Wrapper leakage is binary:

* present
* absent

No partial-credit leakage scoring.

## 5.3 Leakage Interaction

If wrapper leakage exists alongside otherwise valid JSON:

* classify as `wrapper_leakage`
* not `exact_valid`

---

# 6. Tool-Name Accuracy

## 6.1 Correctness Rule

Tool-name accuracy is correct iff:

* emitted tool name exactly matches canonical expected tool name

Matching is:

* case-sensitive
* whitespace-sensitive

No fuzzy matching.

## 6.2 Alias Handling

Aliases are permitted only if:

* explicitly declared in canonical schema/version metadata

Otherwise:

* alias mismatch = incorrect tool.

---

# 7. Argument Accuracy

## 7.1 General Rule

Argument accuracy is correct iff:

* canonicalized emitted arguments semantically match expected arguments

## 7.2 Canonicalization Rules

Canonicalization may normalize:

* object key ordering
* insignificant whitespace
* numeric formatting equivalence
* path separator normalization where documented
* ordering of semantically unordered collections where documented

Canonicalization must not:

* invent missing arguments
* infer omitted required values
* silently coerce incompatible types

## 7.3 Partial Match Policy

Argument scoring is binary:

* correct
* incorrect

No partial-credit scoring unless future metric versions explicitly add it.

## 7.4 Missing vs Extra Arguments

Incorrect if:

* required argument missing
* prohibited argument present
* semantically incorrect value supplied

---

# 8. No-Call Correctness

## 8.1 Correctness Rule

No-call correctness is correct iff:

* no tool is emitted
* and canonical expected behavior is:

  * direct answer
  * refusal
  * no-call
  * clarification-only response

## 8.2 Unexpected Tool Usage

Unexpected tool usage is incorrect even if:

* tool itself is valid
* arguments are correct

Tool discipline matters.

## 8.3 Refusal Behavior

Correct refusal behavior must:

* avoid fabricated execution
* avoid fake claims of access
* avoid hallucinated runtime state

---

# 9. Multi-Tool Evaluation

## 9.1 Multi-Tool Expectations

If multi-tool behavior is explicitly expected:

* tool order matters only if declared order-sensitive
* all required calls must be present
* prohibited extra calls invalidate exact-valid status

## 9.2 Multi-Tool Failure Priority

Failure priority:

1. invalid_json
2. invalid_schema
3. wrapper_leakage
4. missing_tool_call
5. unexpected_tool_call
6. wrong_tool_name
7. wrong_arguments

Secondary annotations may record:
- missing_required_tool
- prohibited_extra_tool

---

# 10. Failure Classification Priority

If multiple failures coexist, classify using highest-priority failure:

1. invalid_json
2. invalid_schema
3. wrapper_leakage
4. missing_tool_call
5. unexpected_tool_call
6. wrong_tool_name
7. wrong_arguments
8. other_failure

This guarantees deterministic classification.

---

# 11. Metric Computation Rules

## 11.1 Exact JSON Validity

`exact_valid_rows / total_rows`

## 11.2 Tool-Name Accuracy

`correct_tool_name_rows / tool_expected_rows`

## 11.3 Argument Accuracy

`correct_argument_rows / tool_expected_rows`

## 11.4 Wrapper Leakage Rate

`wrapper_leakage_rows / total_rows`

## 11.5 No-Call Correctness

`correct_no_call_rows / no_call_expected_rows`

---

# 12. Delta Computation Rules

Unless otherwise documented:

* all deltas use absolute percentage-point deltas
* not relative percentages

Example:

* base: 12%
* adapter: 21%
* delta: +9 percentage points

not:

* +75%

---

# 13. Minimum Evaluation Integrity Rules

Promotion evals must use:

* frozen canonical eval manifest
* frozen decode settings
* frozen scorer version
* fixed tokenizer version
* fixed prompt serialization contract

Cross-version comparisons require:

* explicit version annotation
* preserved prior manifests

---

# 14. Determinism Requirements

Canonical promotion scoring should be deterministic whenever practical.

Required:

* fixed seeds
* fixed decode parameters
* fixed scorer version
* fixed evaluation ordering

Non-deterministic exploratory evals:

* permitted for diagnostics
* prohibited as sole promotion basis

---

# 15. Logging Requirements

Canonical eval outputs must preserve:

* raw model output
* parsed output
* canonicalized output
* failure class
* secondary annotations
* scorer version
* eval manifest version
* decode parameters
* tokenizer version

---

# 16. Prohibited Evaluator Behavior

Scorers/evaluators must not:

* auto-repair malformed JSON
* infer omitted arguments
* silently rewrite tool names
* strip wrapper leakage before scoring
* hallucinate semantic equivalence
* downgrade schema violations to warnings

Promotion scoring must remain conservative.

---

# 17. Future Versioning

Changes to:

* scoring semantics
* canonicalization rules
* failure taxonomy
* match semantics
* parsing behavior

require:

* new metric-spec version
* updated eval manifest references
* preserved historical comparability where practical

---

# 18. Final Principle

The evaluation system exists to measure:

* disciplined runtime behavior
* schema obedience
* safe tool/no-tool discrimination
* reliable structured-output generation

—not conversational pleasantness or stylistic polish.

