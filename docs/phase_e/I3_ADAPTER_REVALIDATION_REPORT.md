# i3 Adapter Revalidation Report

## Scope

Fresh canonical evaluation of `stage_b_llama31_8b_base_v1_i3` against the frozen canonical manifest.

## Command

```bash
python scripts/eval_canonical_manifest.py \
  --manifest evals/canonical_eval_manifest_v1.json \
  --model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base \
  --adapter-dir artifacts/adapters/stage_b_llama31_8b_base_v1_i3 \
  --out-dir evals/runs/phase_e_i3_revalidation_20260610_r1
```

## Runtime Notes

- Model load completed successfully.
- Warnings observed:
  - `torch_dtype` is deprecated; use `dtype` instead.
  - the generation flags warning noted `temperature` may be ignored.
  - `clean_up_tokenization_spaces=True` warning for the BPE tokenizer was emitted.
- No execution failure occurred.

## Outputs

- Summary: [evals/runs/phase_e_i3_revalidation_20260610_r1/summary.json](../../evals/runs/phase_e_i3_revalidation_20260610_r1/summary.json)
- Comparison rows: [evals/runs/phase_e_i3_revalidation_20260610_r1/comparison_rows.jsonl](../../evals/runs/phase_e_i3_revalidation_20260610_r1/comparison_rows.jsonl)
- Supporting evaluator artifacts:
  - `stage_c_row_fact_metadata_artifact.json`
  - `stage_c_family_a_scorer_evidence_artifact.json`
  - `stage_c_governance_guardrails_artifact.json`
  - `stage_c_runtime_contract_summary_artifact.json`

## i3 Adapter Results

| Metric | Value |
|---|---:|
| Rows | 200 |
| Exact JSON validity | 0.025 |
| Invalid JSON rate | 0.28 |
| Tool-name accuracy | 0.03571428571428571 |
| Argument accuracy | 0.03571428571428571 |
| Wrapper leakage rate | 0.0 |
| No-call correctness | 1.0 |

## Failure Profile

| Category | Count |
|---|---:|
| Direct-answer substitution | 45 |
| Scalar substitution | 43 |
| Malformed partial JSON | 3 |
| Near-canonical wrapper or envelope drift | 44 |
| Other non-exact | 0 |

## Interpretation

The i3 adapter is reproducible and materially better than the base model on structured-output behavior, but it remains far below the Appendix A minimum-promising threshold.

Its no-call behavior is preserved, which is the important non-regression property for this baseline.

## Determination

The i3 adapter was freshly revalidated successfully and the result is reproducible as evidence.
It is not promotion-eligible.

## Boundary Confirmation

This report does not propose promotion or training changes.
