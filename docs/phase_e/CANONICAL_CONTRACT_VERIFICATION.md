# Canonical Contract Verification

## Scope

Verify whether the frozen canonical evaluation contract still reproduces cleanly.

## Inputs

- [evals/canonical_eval_manifest_v1.json](../../evals/canonical_eval_manifest_v1.json)
- [scripts/eval_canonical_manifest.py](../../scripts/eval_canonical_manifest.py)
- [scripts/stage_c1_evaluator_foundation.py](../../scripts/stage_c1_evaluator_foundation.py)
- [evals/data/canonical_v1/](../../evals/data/canonical_v1/)
- [evals/runs/phase_e_base_revalidation_20260610_r1/summary.json](../../evals/runs/phase_e_base_revalidation_20260610_r1/summary.json)
- [evals/runs/phase_e_i3_revalidation_20260610_r1/summary.json](../../evals/runs/phase_e_i3_revalidation_20260610_r1/summary.json)

## Verification Results

| Contract element | Status | Basis |
|---|---|---|
| Manifest integrity | Pass | Manifest file exists and its split hashes match the canonical datasets |
| Split integrity | Pass | All five evaluation splits exist and the row counts in the manifest match the canonical assets |
| Decode defaults | Pass | Both fresh runs used `temperature=0.0`, `top_p=1.0`, `do_sample=false`, `repetition_penalty=1.0`, `max_new_tokens=64`, `seed=1234` |
| Dataset references | Pass | All dataset paths in the manifest resolve to existing files |
| Model references | Pass | The canonical model path exists and the adapter path exists |
| Scorer references | Fail with caveat | The manifest pins scorer hash `80af75c494e0da59f30f33a910997b5fdff15d4ffa8dca09988cdedc0fc06e3f`, but the current script hash is `08a5cec22a781193365bed85b709ceebef534846602004bbfa047f4e0b59d738` |

## Fresh Execution Evidence

- Base revalidation completed successfully against the frozen manifest and produced `summary.json` plus `comparison_rows.jsonl`.
- i3 revalidation completed successfully against the same frozen manifest and produced `summary.json` plus `comparison_rows.jsonl`.
- Both runs also emitted the Stage C evidence artifacts expected by the evaluator chain:
  - `stage_c_row_fact_metadata_artifact.json`
  - `stage_c_family_a_scorer_evidence_artifact.json`
  - `stage_c_governance_guardrails_artifact.json`
  - `stage_c_runtime_contract_summary_artifact.json`

## Determination

The canonical evaluation contract is operationally reproducible, but it is not strictly hash-stable without acknowledging the scorer-script drift.

In practical terms:

- the manifest, datasets, model path, and decode defaults remain usable
- the current evaluator script can still execute the canonical process successfully
- the manifest’s pinned scorer hash is stale relative to the current repository tip

So the answer is:

- **reproducible in practice, with caveats**
- **not strictly reproducible without reconciling the scorer hash pin**

## Required Controls

- Keep the frozen manifest fixed for baseline comparison work.
- Keep the model path fixed at `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base`.
- Keep the dataset assets fixed to the canonical v1 split set.
- Treat the scorer hash mismatch as a contract drift item, not as a silent non-event.

## Boundary Confirmation

This verification does not change the manifest, the scorer semantics, or the dataset assets.
