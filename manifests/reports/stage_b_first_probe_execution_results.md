# Stage B First Probe Execution Results

## Probe Identity
- `sweep_id`: `stage_b_v1_geometry_first_live_probe`
- `cell_id`: `cell_live_mh_nocall_medium_readfile_high_v1`
- authorized package commit: `d66522edd64b96acb27aa22b546bd8310efe5ae5`

## Commands Actually Run
1. `git status --short --branch`
2. `git rev-parse HEAD && git rev-parse origin/main && git rev-parse --verify d66522edd64b96acb27aa22b546bd8310efe5ae5`
3. `jq '{review_gate}' manifests/runs/stage_b_llama31_8b_base_v1_geometry_probe_mh.run_manifest.json && jq '{safety}' configs/lora/stage_b_llama31_8b_base_v1_geometry_probe_mh.config.json`
4. runtime gate check snippet via `train_lora_sft._find_manifest_for_config(...)` + `_resolve_run_gate(...)`
5. `python /opt/ai-stack/assistant-training/scripts/preflight_lora_run.py /opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_geometry_probe_mh.run_manifest.json`
6. `/home/roy/.venvs/llama/bin/accelerate launch --num_processes 1 /opt/ai-stack/assistant-training/scripts/train_lora_sft.py --config /opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_geometry_probe_mh.config.json`

## Execution Outcome
- start-state checks: passed (`HEAD == origin/main == authorized commit`)
- authorization checks: passed (`review_gate.approved_to_run=true`, runtime gate `approved=true`)
- preflight: passed
- training: failed on first attempt (exit code `1`)
- retries: none
- hidden retries: none
- eval: not run (stopped after training failure)
- collapse detector: not run (stopped after training failure)

## Failure
Training failed after instrumentation setup and before first train step due trainer integration error:

`TypeError: _GeometrySamplingTrainer._get_train_sampler() takes 1 positional argument but 2 were given`

No retry was performed by policy.

## Exposure Summary
### Declared Exposure
- source: `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/exposure_ledger_declared.json`
- train rows: `1982`
- val rows: `236`
- combined rows: `2218`
- train family counts: `{"malformed_regex_underspecified_search_adversarial_boundary": 8, "read_file_symbol_name_commitment_instability": 5, "semantic_substitution_conversion_pairs_read_file_primary": 52, "semantic_substitution_conversion_pairs_rg_search_scalar_secondary": 28, "uncertainty_conditioned_procedural_continuation_smallscale": 8, "unspecified": 1881}`

### Realized Exposure
- source: `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/exposure_ledger_realized.json`
- status: `realized_exposure_weighted_configured_runtime_not_captured`
- capture_mode: `index_space_inferred_no_sampler_stream_capture`
- confidence: `limited`

### Declared-vs-Realized Drift
- source: `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/exposure_ledger_drift.json`
- status: `declared_vs_realized_comparison_default_path_inferred`
- confidence: `limited`
- max_abs_delta_any_dimension: `None`

## Behavior Metrics
- `no_call aggregate`: unavailable (eval not run)
- `no_call adversarial`: unavailable (eval not run)
- `read_file exact_valid`: unavailable (eval not run)
- `read_file symbol_name exact_valid`: unavailable (eval not run)
- `wrapper leakage`: unavailable (eval not run)
- `invalid_json`: unavailable (eval not run)
- `direct_answer_substitution_delta`: unavailable (eval not run)

## Governance
- detector status: `not_run`
- gate assessment: `not_run`
- collapse-watch status: `not_run`

## Final Recommendation
`NOT_READY`
