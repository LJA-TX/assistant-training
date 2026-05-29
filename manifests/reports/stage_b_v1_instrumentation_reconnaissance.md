# Stage B v1 Geometry Instrumentation Reconnaissance

## Mode / Scope
- Phase: implementation planning + bounded code reconnaissance only.
- Confirmed in this phase: no training, no eval reruns, no dataset mutation/generation, no sweep execution.

## Environment Snapshot
- Repo: `/opt/ai-stack/assistant-training`
- Trainer stack observed: `transformers==5.9.0`, `torch==2.12.0+cu130`, `peft==0.19.1`

## 1) Exposure Accounting

### Current-State Observations
1. Dataset rows enter the training pipeline in two code paths:
- `scripts/train_lora_sft.py:547-548` (`--masking-audit-only` path) via `_load_jsonl(train_jsonl/val_jsonl)`.
- `scripts/train_lora_sft.py:651-652` (full training path) via `_load_jsonl(train_jsonl/val_jsonl)`.

2. Row-level metadata is currently partially consumed but not propagated end-to-end:
- `_encode_with_explicit_masking` writes only `source_case_id` and `tool` into per-row audit (`scripts/train_lora_sft.py:308-326`).
- `_TokenizedDataset.__getitem__` drops metadata and returns only tensors (`scripts/train_lora_sft.py:353-359`).

3. Existing artifacts contain no declared-vs-realized exposure ledger:
- `resolved_config.json` currently stores gate + prompt-template + full config (`scripts/train_lora_sft.py:642-649`).
- `masking_audit.json` currently stores only first 3 train / first 2 val audits (`scripts/train_lora_sft.py:384-388`, `681-683`).
- `training_summary.json` stores row counts and trainer metrics only (`scripts/train_lora_sft.py:743-754`).

4. The repo already has analysis utilities that can be reused conceptually for counting distributions:
- `scripts/i8_diagnostics_scaffold.py` / `scripts/i10_diagnostics_scaffold.py` compute tool/style/family-like coverage and collapse-watch telemetry for dataset analysis (not training-time realized sampling).

### Recommendations (Smallest Safe Changes)
1. Add a non-behavioral exposure-accounting layer before trainer creation:
- Compute `declared_exposure_by_family/archetype/axis` from loaded `train_rows` metadata.
- Emit to new artifact: `exposure_ledger_declared.json`.
- Complexity: Low.

2. Add realized exposure accounting at dataloader/sampler boundary:
- Record sampled index stream per epoch (or per global step bucket) and aggregate into `realized_exposure_by_family/archetype/axis`.
- Emit to new artifact: `exposure_ledger_realized.json`.
- Complexity: Medium (depends on sampler strategy).

3. Keep tensor payload unchanged:
- Preserve current `__getitem__` tensor contract.
- Use sidecar maps (`idx -> metadata summary`) for accounting.
- Complexity: Low.

### Reproducibility Risks
- If realized exposure is inferred indirectly (instead of captured sampler-side), drift can go undetected.
- If metadata keys vary by dataset iteration (`intervention_i10_*`, `i10r_counterbalanced_*`, `i10r_residual_nocall_*`), aggregation can be inconsistent unless normalized.

### Doctrine Concerns
- Hidden/unlogged exposure manipulation violates auditable geometry doctrine.
- Non-normalized family keys risk false attribution of coupling effects.

## 2) Cell Traceability

### Current-State Observations
1. Training artifacts have insertion points for sweep metadata:
- `resolved_config.json` assembly (`scripts/train_lora_sft.py:642-649`).
- `masking_audit.json` assembly (`scripts/train_lora_sft.py:384-388`).
- `training_summary.json` assembly (`scripts/train_lora_sft.py:743-754`).

2. Eval outputs currently lack run-level geometry context:
- `scripts/eval_canonical_manifest.py` writes `summary.json` with manifest/model/decode/base/adapter/delta (`686-698`) but no training cell metadata.

3. Run manifests already carry rich provenance structure and can host geometry references:
- `manifests/runs/*` include `inputs`, `outputs_reports`, gate state, and checkpoint lineage.

### Recommendations (Smallest Safe Changes)
1. Add `geometry_context` object in config/manifest and copy verbatim into resolved artifacts.
2. Add `cell_trace` block to masking audit and training summary:
- `cell_id`, axis levels, weighting mode, declared exposure declaration hash.
3. Add optional CLI input in `eval_canonical_manifest.py` for run-context sidecar (non-breaking):
- e.g., `--run-context-json`.
- Include selected fields in eval `summary.json`.
4. Keep gate logic external; traceability should be write-only metadata in this phase.

### Reproducibility Risks
- If eval artifacts are disconnected from training cell IDs, Pareto/frontier comparisons become ambiguous.
- If cell metadata can be edited post-hoc without hash linkage to config/manifest, lineage trust degrades.

### Doctrine Concerns
- Geometry experiments require deterministic, attributable cell lineage; missing traceability undermines objective-interaction claims.

## 3) Weighted Sampling Feasibility (No Implementation)

### Current-State Observations
1. Trainer integration currently uses default `Trainer` with random sampler behavior:
- `Trainer(...)` creation in `scripts/train_lora_sft.py:725-732`.
- No weighted sampler hook in local trainer script.

2. Installed `transformers==5.9.0` has extension seams:
- `Trainer._get_train_sampler(...)` and `Trainer.get_train_dataloader(...)` are overridable.
- Default `_get_train_sampler` returns grouped/sequential/random only.

### Feasibility Assessment
- Deterministic weighted sampler is feasible with bounded code changes by subclassing `Trainer` and overriding `_get_train_sampler`.
- Single-process complexity: Medium.
- Distributed-safe complexity: Medium-High (sampler sharding / rank-consistent effective exposure accounting).

### Reproducibility Risks
- Seed scope mismatch (Python/Torch/sampler generator) can change realized exposure.
- Weighted sampling with replacement can alter effective epoch semantics versus row-count assumptions.
- Multi-rank duplication/skew risk if sampler is not distribution-aware.

### Doctrine Concerns
- Weighting without declared-vs-realized audit is non-compliant.
- Loss weighting as first move is higher-confound and weaker for attribution than sampler weighting.

## 4) Geometry Metadata Schema

### Current-State Observations
- Current row metadata is iteration-specific and heterogeneous; no canonical geometry schema exists.
- Config and run manifests have no dedicated geometry section.
- Training/eval artifacts do not carry normalized geometry identifiers.

### Recommendations (Minimal Schema)
1. Row-level (metadata, non-breaking, additive):
- `geometry_cell_id`
- `geometry_axes` (`no_call_pressure`, `read_file_counterweight`, `rg_contrastive`, `uncertainty_conditioning`)
- `geometry_family`
- `geometry_archetype`
- `geometry_declared_weight`
- `geometry_pair_id` (for contrastive-pair integrity)

2. Manifest/config-level:
- `geometry_mapping`: `sweep_id`, `cell_id`, axis levels, weighting mode, declared exposure units, invariants.

3. Artifact-level:
- `resolved_config`: geometry declaration + hash.
- `masking_audit`: geometry sample echo + dataset-level geometry counts.
- `training_summary`: declared exposure summary + realized exposure summary + drift flags.
- `eval summary`: geometry context echo + link to exposure ledger artifacts.

### Reproducibility Risks
- Flat ad-hoc keys per iteration recreate the current heterogeneity problem.
- Missing pair IDs can break no-call/valid-contrastive coupling audits.

### Doctrine Concerns
- Schema must be stable and versioned (`geometry_schema_version`) to support convergence-era comparability.

## 5) Collapse Detection (Architecture + Reporting Only)

### Current-State Observations
1. Collapse-watch logic exists as distributed threshold artifacts and interpretation JSONs, but not as a unified reusable post-eval engine.
2. `eval_canonical_manifest.py` currently emits raw eval metrics and class counts; it does not enforce collapse policy.

### Recommendations (Smallest Safe Path)
1. Add a standalone post-eval collapse-detector script (new reporter, no eval behavior changes):
- Inputs: canonical eval `summary.json`, optional baseline summary, thresholds file.
- Output: standardized `collapse_watch_interpretation.json` + `gate_assessment.json`.

2. Keep detector policy external and explicit:
- Threshold profiles versioned in JSON.
- Detector only reports triggers and recommendation state; does not mutate trainer/eval behavior.

3. Include catastrophic thresholds aligned to geometry mapping doctrine:
- `invalid_json_overall`, `wrapper_leakage`, `read_file_exact_valid`, `read_file_symbol_name_exact_valid`.

### Reproducibility Risks
- Embedding thresholds directly in multiple ad-hoc scripts causes policy drift.
- Implicit baseline selection can silently change trigger outcomes.

### Doctrine Concerns
- Read_file during geometry mapping must be measured dependent variable by default; hard-stop only on catastrophic collapse.
- Hard invariants (wrapper leakage, contamination, eval topology) remain non-negotiable.

## Consolidated Complexity View
- Exposure ledger (declared only): Low.
- Cell-trace propagation into existing artifacts: Low.
- Weighted sampler (single-process deterministic): Medium.
- Weighted sampler (distributed-safe + auditable): Medium-High.
- Unified post-eval collapse detector reporter: Medium.

## Recommended Next Executable Phase
- Stage B v1 instrumentation implementation-only:
1. Add metadata/schema plumbing + artifact trace fields.
2. Add declared exposure ledger first.
3. Add weighted sampler hook and realized exposure ledger second.
4. Add standalone collapse-detector reporter third.
- Keep training/eval execution out of this phase.
