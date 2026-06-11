# Failure Attribution Analysis

## Executive Summary

The dominant Phase E i3 failure is not wrong tool choice. It is failure to stay in canonical tool-call mode.

- On the `140` tool-expected rows, i3 produced only `5` exact-valid outputs.
- The remaining `135` failures are dominated by commitment loss and schema drift, not by evaluator-scored `wrong_tool_name` or `wrong_arguments` outcomes.
- Every exact-valid success came from the `literal_tool_calls` anchor bucket, which indicates severe prompt-form dependence even after recovery.

## Inputs

- `evals/runs/phase_e_i3_revalidation_20260610_r1/summary.json`
- `evals/runs/phase_e_i3_revalidation_20260610_r1/comparison_rows.jsonl`
- `evals/runs/phase_e_base_revalidation_20260610_r1/summary.json`
- `docs/phase_e/I3_ADAPTER_REVALIDATION_REPORT.md`
- `docs/phase_e/BASE_MODEL_REVALIDATION_REPORT.md`

## Evaluator-Class View

### i3 aggregate results

| Class | Count |
|---|---:|
| `exact_valid` | 5 |
| `invalid_json` | 56 |
| `invalid_schema` | 79 |
| `refusal_expected` | 60 |

The `60` `refusal_expected` rows are the no-call and adversarial non-tool rows. The tool-attribution question is therefore concentrated in the `140` tool-expected rows.

### Tool-expected split view

| Split | Rows | Exact valid | Invalid JSON | Invalid schema |
|---|---:|---:|---:|---:|
| `heldout_validation` | 100 | 5 | 44 | 51 |
| `tool_holdout` | 40 | 0 | 12 | 28 |
| Total tool-expected | 140 | 5 | 56 | 79 |

The zero-exact result on `tool_holdout` is the clearest sign that internal recovery did not produce robust unseen-tool generalization.

## Requested Attribution Taxonomy

The Phase E summary already contains a non-exact tool-row failure profile. Mapping that profile into the Phase G attribution question gives the following distribution.

| Phase G attribution bucket | Count | Share of non-exact tool rows |
|---|---:|---:|
| Tool-call commitment failure | 88 | 65.2% |
| Schema failure / wrapper or envelope drift | 44 | 32.6% |
| Malformed JSON | 3 | 2.2% |
| Wrong tool selection | 0 | 0.0% |
| Wrong arguments | 0 | 0.0% |
| Other | 0 | 0.0% |

### Bucket definitions used here

- Tool-call commitment failure: the model emits plain text, a scalar, or some other non-tool-call substitute instead of entering canonical tool-call JSON mode.
- Schema failure / wrapper drift: the model emits near-tool-call structure, but the payload lands in `missing_tool_calls` or `payload_not_object` rather than the canonical schema.
- Malformed JSON: partial or broken JSON that never reaches strict parseability.

## What The Row-Level Evidence Shows

### 1. Commitment failure dominates

The summary breakdown for the `135` non-exact tool rows is:

| Failure subtype from Phase E summary | Count |
|---|---:|
| Direct-answer substitution | 45 |
| Scalar substitution | 43 |
| Near-canonical wrapper or envelope drift | 44 |
| Malformed partial JSON | 3 |
| Other non-exact | 0 |

The first two buckets together are the dominant problem: `88 / 135` non-exact tool rows (`65.2%`).

### 2. Pure tool confusion is not the main observed failure

At the row level:

- `predicted_tool_names` appear only on the `5` exact-valid rows.
- Those `5` rows are all `rg_search`.
- There are no evaluator-scored `wrong_tool_name` rows.
- There are no evaluator-scored `wrong_arguments` rows.

The model usually fails before it reaches a state where wrong-tool or wrong-argument evaluation would even matter.

### 3. Schema drift is real but secondary

The dominant schema reasons on tool-expected rows are:

| Schema reason | Count |
|---|---:|
| `payload_not_parsed` | 56 |
| `missing_tool_calls` | 44 |
| `payload_not_object` | 35 |
| `ok` | 5 |

This means many i3 failures are close to tool-call mode without being canonical. Typical surfaces include:

- wrong envelope keys such as `tool_functions`
- scalar outputs such as `1` or `True`
- file-content literals or terse answers instead of tool-call JSON

### 4. Exact success is literal-anchor-bound

The exact-valid anchor distribution is:

| Anchor bucket | Exact-valid share |
|---|---:|
| `literal_tool_calls` | 1.0 |
| `paraphrastic_tool_call` | 0.0 |
| `schema_paraphrase` | 0.0 |
| `no_anchor_phrase` | 0.0 |

All exact successes come from the most explicit prompt family. None come from paraphrastic or anchor-light prompts.

## Base Versus i3

The i3 adapter is better than the base model, but the kind of improvement matters.

| Failure subtype | Base | i3 |
|---|---:|---:|
| Direct-answer substitution | 125 | 45 |
| Scalar substitution | 0 | 43 |
| Near-canonical wrapper or envelope drift | 0 | 44 |
| Malformed partial JSON | 15 | 3 |
| Exact-valid outputs | 0 | 5 |

i3 converts many base-model direct-answer failures into near-tool-call attempts. That is meaningful progress, but it is not the same thing as robust tool execution competence.

## Determination

The dominant remaining deficit after internal recovery is mode commitment and schema realization, not broad menu confusion.

The evidence supports this attribution:

1. Collapse repair helped enough to reduce malformed plain-text behavior.
2. Most residual failures still occur before canonical tool selection and argument scoring can even be evaluated.
3. Internal recovery did not remove literal-anchor dependence or unseen-tool brittleness.

## Sources Used

- `evals/runs/phase_e_i3_revalidation_20260610_r1/summary.json`
- `evals/runs/phase_e_i3_revalidation_20260610_r1/comparison_rows.jsonl`
- `evals/runs/phase_e_base_revalidation_20260610_r1/summary.json`
- `docs/phase_e/I3_ADAPTER_REVALIDATION_REPORT.md`
- `docs/phase_f/INDEPENDENT_DATASET_COLLAPSE_ASSESSMENT_Grok-Build.md`
