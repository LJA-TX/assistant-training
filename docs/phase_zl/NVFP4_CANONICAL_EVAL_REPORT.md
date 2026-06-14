# NVFP4 Canonical Evaluation Report

## Method

The frozen canonical manifest was executed against the NVFP4 external reference model with the following constraints preserved:

- the manifest remained frozen: `evals/canonical_eval_manifest_v1.json`
- decode defaults remained frozen
- the scorer logic remained frozen
- prompt rendering used the canonical chat-template path from the manifest

The only execution accommodation was the inference backend: instead of loading the checkpoint through Transformers, the run used the production vLLM service at `http://127.0.0.1:8012`.

## Persisted Artifacts

- [summary.json](../../evals/runs/phase_zl_nvfp4_external_reference_eval_20260614T131002Z/summary.json)
- [comparison_rows.jsonl](../../evals/runs/phase_zl_nvfp4_external_reference_eval_20260614T131002Z/comparison_rows.jsonl)
- [stage_c_family_a_scorer_evidence_artifact.json](../../evals/runs/phase_zl_nvfp4_external_reference_eval_20260614T131002Z/stage_c_family_a_scorer_evidence_artifact.json)

## Aggregate Results

| Metric | Value |
|---|---:|
| Rows | `200` |
| Exact JSON validity | `0.0` |
| Invalid JSON rate | `0.695` |
| Tool-name accuracy | `0.0` |
| Argument accuracy | `0.0` |
| Wrapper leakage | `0.0` |
| No-call correctness | `1.0` |
| Adversarial no-call correctness | `1.0` |

## Failure Profile

| Category | Count | Notes |
|---|---:|---|
| Direct-answer substitution | `133` | Dominant failure mode on tool-expected rows. |
| Scalar substitution | `0` | Not observed. |
| Malformed partial JSON | `6` | Minor residual. |
| Near-canonical wrapper/envelope drift | `1` | Rare. |
| Other non-exact | `0` | Not observed. |

## Interpretation

The model behaves like a non-tool model on this frozen contract. It refuses cleanly on no-call rows, but it does not realize the canonical tool-call envelope and does not recover exact JSON, tool-name, or argument correctness.

