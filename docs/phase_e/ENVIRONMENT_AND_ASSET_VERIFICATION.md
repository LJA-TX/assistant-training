# Environment And Asset Verification

## Scope

Verify the current repository state and the canonical assets required for Phase E baseline revalidation.

## Inputs

- [docs/goal_charter_v5a.md](../goal_charter_v5a.md)
- [docs/appendix_a_operational_execution_contract_v3a.md](../appendix_a_operational_execution_contract_v3a.md)
- [docs/metric_specification_v1a.md](../metric_specification_v1a.md)
- [evals/canonical_eval_manifest_v1.json](../../evals/canonical_eval_manifest_v1.json)
- [data/v1_0/dataset_v1_0_summary.json](../../data/v1_0/dataset_v1_0_summary.json)
- [data/v1_0/dataset_v1_0_leakage_report.json](../../data/v1_0/dataset_v1_0_leakage_report.json)
- [manifests/runs/stage_b_llama31_8b_base_v1_i3.run_manifest.json](../../manifests/runs/stage_b_llama31_8b_base_v1_i3.run_manifest.json)
- [artifacts/stage_b_llama31_8b_base_v1_i3/training_summary.json](../../artifacts/stage_b_llama31_8b_base_v1_i3/training_summary.json)

## Environment Verification Results

| Check | Result | Evidence |
|---|---|---|
| Current branch | Pass | `main` |
| HEAD | Pass | `325bdb4a38286180cf5c6d7ab36fa2ed642a2178` |
| origin alignment | Pass | `HEAD == origin/main` |
| Working tree cleanliness | Fail with expected local work | Untracked local files are present: `docs/Phase_D_Work_packages.md`, `docs/Phase_E_Work_packages.md`, `docs/phase_d/`, and `docs/phase_e/`. No unexpected tracked edits were introduced by this phase. |
| Canonical model path | Pass | `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base` exists |
| i3 adapter path | Pass | `artifacts/adapters/stage_b_llama31_8b_base_v1_i3` exists |

## Asset Verification Results

| Asset | Result | Evidence |
|---|---|---|
| Canonical eval manifest | Pass | `evals/canonical_eval_manifest_v1.json` exists |
| Canonical eval datasets | Pass | `evals/data/canonical_v1/{heldout_validation,tool_holdout,no_call,adversarial,direct_answer}.jsonl` all exist |
| Dataset manifest | Pass | `data/v1_0/dataset_v1_0_summary.json` exists |
| Leakage report | Pass | `data/v1_0/dataset_v1_0_leakage_report.json` exists |
| Evaluator script | Pass | `scripts/eval_canonical_manifest.py` exists |
| Scorer script hash pinned in manifest | Fail | Manifest expects `80af75c494e0da59f30f33a910997b5fdff15d4ffa8dca09988cdedc0fc06e3f`; current script hash is `08a5cec22a781193365bed85b709ceebef534846602004bbfa047f4e0b59d738` |
| Dataset split hashes | Pass | All five split hashes match the manifest exactly |
| Dataset manifest hash | Pass | `86f68710d7257bb43793fb6a47245a232a3d390e55890604e8926676e6a2b4fd` matches the manifest |

## Hash Comparison

- `heldout_validation`: pass
- `tool_holdout`: pass
- `no_call`: pass
- `adversarial`: pass
- `direct_answer`: pass
- `dataset_v1_0_summary.json`: pass
- `eval_canonical_manifest.py`: fail, because the current script hash differs from the manifest pin

## Determination

The required assets are present and the canonical datasets match the frozen manifest.
The only verification failure is scorer hash drift between the manifest pin and the current evaluator script.

## Boundary Confirmation

This verification does not alter datasets, manifests, or scoring semantics.
