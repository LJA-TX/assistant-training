# JSON And Schema Failure Analysis

## Executive Summary

Phase L did not fail because of wrapper leakage.
It failed because the model could not reliably emit the canonical tool-call envelope.

The collapse is dominated by schema realization failure:

- `invalid_json`
- `invalid_schema`
- `near-canonical wrapper or envelope drift`

Direct-answer and scalar substitutions are real regressions, but they are secondary to the schema failure.

## Aggregate Class Breakdown

| Class | Count |
|---|---:|
| `invalid_json` | `69` |
| `invalid_schema` | `63` |
| `wrong_arguments` | `6` |
| `wrong_tool_name` | `2` |

On tool-expected rows, `132 / 140` rows failed either JSON validity or schema validity.
That is `94.28571428571429%` of the tool-call surface.

## Parse-Mode Breakdown

### Heldout Validation

| Parse mode / schema reason | Count |
|---|---:|
| strict | `53` |
| invalid | `47` |
| `missing_tool_calls` | `44` |
| `payload_not_parsed` | `47` |
| `ok` | `8` |
| `payload_not_object` | `1` |

### Tool Holdout

| Parse mode / schema reason | Count |
|---|---:|
| strict | `18` |
| invalid | `22` |
| `missing_tool_calls` | `18` |
| `payload_not_parsed` | `22` |

Interpretation:

- Many rows were syntactically parseable but failed the canonical envelope check.
- The most common schema reason on heldout validation was `missing_tool_calls`.
- Tool holdout never reached an exact-valid state.

## Failure Subtype Breakdown

| Failure subtype | Count |
|---|---:|
| near-canonical wrapper or envelope drift | `70` |
| direct-answer substitution | `55` |
| malformed partial JSON | `14` |
| scalar substitution | `1` |

This is the failure stack that explains the collapse:

1. The model most often produced the wrong tool-call envelope.
2. When it did not drift into wrapper-like JSON, it often answered directly.
3. A smaller slice produced malformed partial JSON.
4. Scalar substitution was rare.

## What The Failures Look Like

The row-level outputs show recurring patterns:

- JSON-like text with `{"function": ...}` or `{"functions": ...}` instead of the canonical `{"tool_calls": ...}` envelope.
- Partial tool-call objects that stop mid-structure.
- Direct natural-language answers on rows where a tool call was required.
- Occasional scalar answers such as `120`.

## Dominant Contributor To Capability Collapse

The dominant contributor is schema-emission failure, especially near-canonical wrapper or envelope drift.

Why:

- It is the largest failure subtype.
- It covers half of the non-exact tool rows.
- It explains why the model can remain non-leaky and still fail exact-validity.
- It is consistent with the high `invalid_schema` count and the `missing_tool_calls` schema reason.

Direct-answer substitution is the next-largest contributor, but it is not the main driver.

## Wrapper Behavior

Wrapper leakage is `0.0`, so the model is not leaking the evaluation wrapper back verbatim.

That matters because the failure is not "the model parrots the harness."
The failure is subtler:

- the model emits the wrong structured envelope,
- or it falls back to direct answer text,
- while still respecting the no-call safety boundary.

## Sources Used

- `evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/summary.json`
- `evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/comparison_rows.jsonl`
- `evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/stage_c_family_a_scorer_evidence_artifact.json`
- `docs/phase_l/PHASE_L_EXECUTION_REVIEW.md`
