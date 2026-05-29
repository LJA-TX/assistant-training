# Stage B Weight Provisioning Validation Results

## Validation Scope
No training, no evals, no probe execution.
Validation used static checks and deterministic in-process resolution harnesses only.

## Commands Run
1. Compile checks
```bash
python -m py_compile scripts/train_lora_sft.py scripts/provision_geometry_probe_weights.py
```
Result: `PASS`

2. Provision first-probe sidecar
```bash
python scripts/provision_geometry_probe_weights.py \
  --train-jsonl /opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i10r_counterbalanced_train.jsonl \
  --declared-exposure /opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_declared_exposure.json \
  --geometry-context /opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_geometry_context_input.json \
  --output-sidecar /opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_weights_sidecar.json \
  --default-weight 0.0 \
  --min-positive-rows 13
```
Result: `PASS`

3. Determinism/fail-fast/ledger compatibility harness
- Artifact: [stage_b_weight_provisioning_validation_runtime.json](/opt/ai-stack/assistant-training/manifests/reports/stage_b_weight_provisioning_validation_runtime.json)
Result: `PASS`

## Assertions and Outcomes

### A) Positive-weight coverage supplied
- `positive_weight_rows = 13`
- `weights_sum = 36.0`
- Sidecar summary at [stage_b_first_probe_weights_sidecar.json](/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_weights_sidecar.json)
- Status: `PASS`

### B) Deterministic resolution
- Two independent `_resolve_geometry_sampling_plan(...)` resolutions produced identical:
  - weight vector
  - weight digest
  - weight summary
- Status: `PASS`

### C) Missing weights fail fast
- Removed one row from sidecar `rows` list.
- Loader raised: `geometry_sampling sidecar missing 1 row weights`
- Status: `PASS`

### D) Row identity mismatch fail fast
- Corrupted one sidecar `row_hash_sha256`.
- Loader raised mismatch at the expected index.
- Status: `PASS`

### E) Row identity lineage reconstructable
- Sidecar `row_identity_reference.rows_digest_sha256` matched reconstructed training row-identity digest.
- Status: `PASS`

### F) Exposure accounting compatibility preserved
- Default pre-train realized ledger path emitted weighted-configured/inferred status:
  - `realized_exposure_weighted_configured_runtime_not_captured`
- Drift ledger remained computable and consistent.
- Status: `PASS`

### G) No tensor/loss/default-sampler regressions
- No changes to tensor payload contract (`_TokenizedDataset`, collator, model input construction unchanged).
- No changes to loss-path logic.
- No changes to default sampler behavior when `geometry_sampling.enabled=false`.
- Changes are confined to sidecar weight resolution and source-detail reporting.
- Status: `PASS`

## Additional Note: Hash Collisions
- Dataset contains repeated row hashes (`row_hash_collision_count = 157`).
- Implemented collision-aware row-hash mode and recommended explicit row-identity `rows` mode as canonical first-probe path.
