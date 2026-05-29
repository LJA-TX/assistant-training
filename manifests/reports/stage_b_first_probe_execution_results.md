# Stage B First Live Geometry Probe Execution Results

## Outcome
- Status: `FAILED_AT_COLLAPSE_DETECTOR`
- Final recommendation: `NOT_READY`
- Retries performed: `0`
- Hidden retries performed: `0`

## Probe Identity
- `sweep_id`: `stage_b_v1_geometry_first_live_probe`
- `cell_id`: `cell_live_mh_nocall_medium_readfile_high_v1`
- Authorized package commit: `ae559bacef10648250f56b20b5303bd91bc3f820`

## Start-State Verification
- `git status --short --branch`: not clean (report artifacts only)
- `HEAD`: `ae559bacef10648250f56b20b5303bd91bc3f820`
- `origin/main`: `ae559bacef10648250f56b20b5303bd91bc3f820`
- Requested checkpoint in prompt step list (`d66522...`) did not match current authorized package commit; execution proceeded from authorized commit `ae559...`.

## Authorization Verification
- `manifest.review_gate.approved_to_run`: `true`
- Runtime gate (`_resolve_run_gate`) approved: `true`

## Commands Actually Run
1. `git status --short --branch`
2. `git rev-parse HEAD && git rev-parse origin/main`
3. runtime gate verification snippet (`_resolve_run_gate`)
4. `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_geometry_probe_mh.run_manifest.json`
5. `/home/roy/.venvs/llama/bin/accelerate launch --num_processes 1 /opt/ai-stack/assistant-training/scripts/train_lora_sft.py --config /opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_geometry_probe_mh.config.json`
6. `python /opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py --manifest /opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json --model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base --adapter-dir /opt/ai-stack/assistant-training/artifacts/adapters/stage_b_llama31_8b_base_v1_geometry_probe_mh --out-dir /opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_mh_eval`
7. `python /opt/ai-stack/assistant-training/scripts/post_eval_collapse_detector.py --eval-summary /opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_mh_eval/summary.json --threshold-profile /opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json --baseline-summary /opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json --geometry-context /opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_geometry_context_input.json --collapse-watch-output /opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_collapse_watch_interpretation.json --gate-assessment-output /opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_gate_assessment.json`

## Failure
- Failed command: collapse detector invocation (step 7)
- Error: `RuntimeError: eval_summary: required metric 'direct_answer_substitution_count' not found in summary`
- Retry after failure: `none`

## Exposure
- Declared exposure summary: `{"rows_total": 2218, "rows_train": 1982, "rows_val": 236, "unique_families": 6, "unique_archetypes": 6, "rows_with_metadata": 2218}`
- Realized exposure summary: `{"rows_total": 1982, "sampled_rows_total": 401, "unique_families": 2, "unique_archetypes": 2, "status": "realized_exposure_weighted_sampler_stream_captured", "capture_mode": "runtime_weighted_sampler_stream_capture", "confidence": "high"}`
- Declared-vs-realized drift: `{"confidence": "high", "max_abs_delta_any_dimension": 1881, "exact_match_all_dimensions": false}`

## Behavior
- `no_call aggregate`: `0.9333333333333333`
- `no_call adversarial`: `1.0`
- `read_file exact_valid`: `0.25`
- `read_file symbol_name exact_valid`: `0.32`
- `wrapper leakage`: `0.015`
- `invalid_json`: `0.23`
- `direct_answer_substitution_delta`: `unavailable` (missing metric in canonical eval summary)

## Governance
- Detector status: `FAILED`
- Gate assessment: `NOT_COMPUTED`
- Collapse-watch status: `NOT_COMPUTED`

## Generated Review Artifacts
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_execution_results.md`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_artifact_inventory.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_behavior_summary.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_governance_outcome.json`
