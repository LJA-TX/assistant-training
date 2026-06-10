# Base Model Revalidation Report

## Scope

Fresh canonical evaluation of `llama-3.1-8b-base` against the frozen canonical manifest.

## Command

```bash
python scripts/eval_canonical_manifest.py \
  --manifest evals/canonical_eval_manifest_v1.json \
  --model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base \
  --out-dir evals/runs/phase_e_base_revalidation_20260610_r1
```

## Runtime Notes

- Model load completed successfully.
- Warnings observed:
  - `torch_dtype` is deprecated; use `dtype` instead.
  - the generation flags warning noted `temperature` may be ignored.
  - `clean_up_tokenization_spaces=True` warning for the BPE tokenizer was emitted.
- No execution failure occurred.

## Outputs

- Summary: [evals/runs/phase_e_base_revalidation_20260610_r1/summary.json](../../evals/runs/phase_e_base_revalidation_20260610_r1/summary.json)
- Comparison rows: [evals/runs/phase_e_base_revalidation_20260610_r1/comparison_rows.jsonl](../../evals/runs/phase_e_base_revalidation_20260610_r1/comparison_rows.jsonl)
- Supporting evaluator artifacts:
  - `stage_c_row_fact_metadata_artifact.json`
  - `stage_c_family_a_scorer_evidence_artifact.json`
  - `stage_c_governance_guardrails_artifact.json`
  - `stage_c_runtime_contract_summary_artifact.json`

## Base Model Results

| Metric | Value |
|---|---:|
| Rows | 200 |
| Exact JSON validity | 0.0 |
| Invalid JSON rate | 0.7 |
| Tool-name accuracy | 0.0 |
| Argument accuracy | 0.0 |
| Wrapper leakage rate | 0.0 |
| No-call correctness | 1.0 |

## Failure Profile

| Category | Count |
|---|---:|
| Direct-answer substitution | 125 |
| Scalar substitution | 0 |
| Malformed partial JSON | 15 |
| Near-canonical wrapper or envelope drift | 0 |
| Other non-exact | 0 |

## Interpretation

The base model remains behaviorally invalid on all tool-expected rows in the canonical suite.

Its only successful behavior in this suite is no-call correctness on the non-tool rows.

## Determination

The base model was freshly revalidated successfully and the result is reproducible as evidence.
It is not a useful structured-output baseline by itself.

## Boundary Confirmation

This report does not propose promotion or training changes.
