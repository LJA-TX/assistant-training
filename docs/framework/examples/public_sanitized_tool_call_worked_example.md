# Public Sanitized Tool-Call Worked Example

Status: synthetic public demonstration; not training, evaluation, or model-performance evidence

This package is the compact public worked example for the Harborview Public Library scenario.
The structured source of truth is the colocated JSON fixture:
[public_sanitized_tool_call_worked_example.json](./public_sanitized_tool_call_worked_example.json)

## Why this example has three rows

The fixture uses exactly three synthetic rows because the public training regimen needs one compact micro-scenario that covers the three core behaviors the evaluator and serializer already distinguish:

1. a correct tool call;
2. a plain-text no-call restraint case;
3. a plausible but non-equivalent wrong-tool temptation.

That keeps the example small enough for review while still showing tool selection, argument fidelity, restraint, anti-substitution, and canonical evaluator interpretation.

## Fictional registry

The only registry in the example is the fictional Harborview Public Library circulation registry:

- `search_catalog`
- `get_availability`
- `place_hold`

The registry is intentionally small and internally complete. `get_availability` is a plausible substitute for `place_hold`, but it is not equivalent because it reads state instead of placing the hold.

## The three rows

| Row | Role | Expected behavior | Canonical evaluator label |
| --- | --- | --- | --- |
| `demo_row_availability_01` | `correct_tool_call` | Call `get_availability` with the resolved item and branch. | `exact_valid` |
| `demo_row_definition_02` | `no_call_restraint` | Answer in plain text with no tool call. | `refusal_expected` |
| `demo_row_hold_03` | `anti_substitution` | Call `place_hold` with the resolved item, branch, and patron reference. | `exact_valid` |

Row 1 demonstrates the correct tool-call path. Row 2 demonstrates the historical expected-no-call success label. `refusal_expected` is the canonical successful no-call label for this row, but `exact_valid` remains false because `exact_valid` denotes exact tool-call realization. No-call correctness is accounted for through the separate evaluator surface for that row.

Row 3 demonstrates anti-substitution: a tempting availability lookup is not enough when the requested circulation action is to place a hold.

## Dataset row, assistant message, and serialized assistant target

The fixture keeps three surfaces separate:

1. the complete dataset row;
2. the assistant message inside that row;
3. the serialized assistant target used by the training contract and scored by the evaluator.

For tool rows, the dataset row’s assistant message contains one tool call with:

- a deterministic synthetic call ID;
- `type: "function"`;
- the exact tool name;
- arguments encoded as a canonical sorted-key JSON string.

The serialized assistant target is the canonical training surface produced by the existing serializer. It does not include the dataset message wrapper or the synthetic call ID.

For the no-call row, the assistant message and the serialized assistant target are the same plain-text answer, and the assistant message has no `tool_calls` field.

## Exact evaluator labels

The example pins the canonical evaluator semantics exactly:

- `exact_valid`
- `refusal_expected`
- `invalid_json`
- `missing_tool_call`
- `wrong_tool_name`
- `wrong_arguments`

The richer direct-answer failure subtype for a tool-required row is `direct_answer_substitution`.

The `refusal_expected` label is historical evaluator vocabulary for the expected-no-call success case. It does not mean the assistant must refuse. It means the correct action for that row is a normal plain-text answer with no tool invocation.

## Deterministic rendering and hashing

The public demonstration uses one explicit fixture-only render contract:

```text
SYSTEM
{system content}
TOOLS
{canonical JSON registry}
USER
{user content}
ASSISTANT
```

The registry JSON uses UTF-8, `ensure_ascii=False`, `sort_keys=True`, and compact separators for the rendered prompt. Tool order is preserved by the registry array order. Real training and evaluation runs remain governed by their pinned tokenizer and rendering configuration.

The fixture stores and validates real recomputed SHA-256 values for:

- the registry;
- each row source surface;
- each rendered prompt;
- each serialized assistant target;
- each illustrative bad output, fabricated tool result, and illustrative post-tool response.

The hashes are over the documented synthetic source surfaces. They are not arbitrary placeholders.

## Lifecycle separation

Each row is organized into distinct records:

1. `dataset_row`
2. `assistant_message`
3. `assistant_target_text`
4. `illustrative_bad_outputs`
5. `fabricated_tool_result`
6. `illustrative_post_tool_response`
7. `expected_evaluator_result`
8. `interpretation`

Every illustrative bad output, fabricated tool result, and illustrative post-tool response carries `execution_status: "synthetic_not_executed"`.

The scored boundary is the assistant action, not the later fictional tool result. This example teaches the shape of the interaction without claiming that any external action was actually executed.

## What the example supports, and what it does not

The package supports:

- demonstration of correct tool selection;
- argument fidelity;
- restraint on a no-call row;
- anti-substitution when a plausible substitute tool is not equivalent;
- observability through rendered-prompt and hash records;
- reproducible validation of the fixture contract.

It does not prove model improvement. Improvement would require a separately authorized comparison on frozen evaluation data, aggregate behavior-class results, and an independent interpretation of tradeoffs.

## Why it is excluded from training and evaluation manifests

The example is synthetic and public-facing. It is intentionally excluded from canonical training and evaluation manifests, splits, and promotion-eligible discovery surfaces so that it cannot contaminate future comparisons or become a hidden source of leakage.

The fixture also avoids private datasets, held-out rows, generated outputs, model artifacts, credentials, workstation paths, and unpublished concepts.

## Repository boundary

The implementation path is:

1. originate in the private canonical repository;
2. review and preserve the implementation there;
3. project it into the public checkout through a separately governed operation;
4. publish only from the public checkout after public validation.

It does not authorize changes to canonical training or evaluation data, execution of a study, model promotion, projection or publication outside the governed workflow, tag creation, push, merge, rebase, or amendment.

## Public package shape

The intended bounded package is three files:

1. `docs/framework/examples/public_sanitized_tool_call_worked_example.md`
2. `docs/framework/examples/public_sanitized_tool_call_worked_example.json`
3. `tests/test_public_sanitized_tool_call_worked_example.py`

The public front door updates are limited to:

- `README.md`
- `docs/current/start_here.md`

That keeps the example colocated with the framework documentation and minimizes maintenance overhead.
