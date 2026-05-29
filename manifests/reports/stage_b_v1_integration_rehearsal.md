# Stage B v1 Instrumentation Integration Rehearsal

## Scope
- Synthetic end-to-end instrumentation rehearsal only.
- No training, eval execution, sweep execution, dataset generation, or dataset mutation.

## Synthetic Geometry Cell
- `sweep_id`: `stage_b_v1_geometry_integration_rehearsal`
- `cell_id`: `cell_synth_nocall_high_readfile_medium_v1`
- `axis_levels`: `{"no_call_pressure": "high", "read_file_counterweight": "medium", "rg_search_contrastive": "low", "uncertainty_conditioning": "zero"}`
- `weighting_mode`: `metadata_weighted_random_sampler_probe`
- `geometry_sampling.enabled`: `true`
- `geometry_sampling.sampler_seed`: `314159`
- `threshold_profile_reference`: `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json`

## Flow Results
1. Geometry Context Flow
- `geometry_context` present in resolved config and all exposure artifacts.
- Mapping stack digest (`geometry_mapping` contract): `1f35b81bfe3dfae09e675361b193620955d2a2c51e6d720ad3b0b8cea4f13348`.
- Detector stack digest (`full geometry_context object`): `04a286d67a82dbd054ebcdc2c5ca485881534a0674a1241abcc64c4421797e9e`.

2. Exposure Accounting Flow
- Declared ledger generated: `/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/exposure_ledger_declared.synthetic.json`.
- Realized ledger generated in weighted captured mode: `/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/exposure_ledger_realized.synthetic.json`.
- Drift ledger generated with runtime captured basis: `/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/exposure_ledger_drift.synthetic.json`.

3. Weighted Sampling Flow
- Deterministic sampler metadata emitted: `/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/sampler_determinism_report.synthetic.json`.
- Sampled stream capture path exercised (`sampled_index_stream_total=12`).
- Weight digest: `cfbb93ebccecec84ab5d8032a0561dc9d124cf2568cc5acc850c096d16ae00f3`.

4. Traceability Flow
- Artifact linkage captured in [integration_rehearsal_artifact_graph.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal_artifact_graph.json).
- Threshold profile digest consistent between collapse watch and gate outputs.

5. Collapse Detection Flow
- Threshold profile ingested by standalone detector.
- Geometry context linked to collapse/gate outputs.
- Detector outputs produced without eval execution:
  - `/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/collapse_watch_interpretation.synthetic.json`
  - `/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/gate_assessment.synthetic.json`

## End-to-End Reconstruction Capability
A reviewer can reconstruct intended geometry, realized geometry, weighting configuration, threshold profile, and lineage chain from emitted artifacts in `manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1` plus the artifact graph.

## Remaining Gaps
- `geometry_context_digest` contract diverges between mapping stack and detector stack.
: Mapping uses reduced digest fields (`schema/sweep/cell/axis_levels/weighting_mode`) while detector digests full geometry context object.
- No first-class shared digest spec object is emitted to disambiguate digest semantics.

## Remaining Scientific Risks
- Drift interpretation sensitivity remains high with small synthetic sample counts.
- Weighted sampling realization bias is visible by design; real probe cells may need declared-vs-realized tolerance policy before gate action.
- Collapse detector thresholds are static; scientific validity still depends on empirically calibrated baseline selection in real runs.

## Readiness Recommendation
- `NOT_READY`
: Rationale: cross-stack `geometry_context_digest` semantics are not yet harmonized, which weakens deterministic lineage reconstruction across mapping and detector artifacts.
