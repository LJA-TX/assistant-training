# Instruct Canonical Evaluation Report

## Method

The frozen canonical evaluation contract was executed directly against the non-quantized Instruct checkpoint.

Preserved:

- canonical manifest: `evals/canonical_eval_manifest_v1.json`
- prompt rendering
- decode defaults
- scorer logic
- thresholds

No evaluation changes were made.

## Persisted Artifacts

- [summary.json](../../evals/runs/phase_zm_instruct_external_reference_eval_20260614T131500Z/summary.json)
- [comparison_rows.jsonl](../../evals/runs/phase_zm_instruct_external_reference_eval_20260614T131500Z/comparison_rows.jsonl)
- [stage_c_family_a_scorer_evidence_artifact.json](../../evals/runs/phase_zm_instruct_external_reference_eval_20260614T131500Z/stage_c_family_a_scorer_evidence_artifact.json)

## Aggregate Results

| Metric | Value |
|---|---:|
| Rows | `200` |
| Exact JSON validity | `0.0` |
| Invalid JSON rate | `0.69` |
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
| Malformed partial JSON | `5` | Minor residual. |
| Near-canonical wrapper/envelope drift | `2` | Rare. |
| Other non-exact | `0` | Not observed. |

## Interpretation

The non-quantized Instruct model sits at the same frozen-contract floor as the NVFP4 external reference on aggregate tool-call metrics. It preserves no-call behavior, but it does not recover the canonical tool-call envelope.

