# Stage B v1 Instrumentation Integration Rehearsal

## Scope
- Synthetic end-to-end instrumentation rehearsal only.
- No training, eval execution, sweep execution, dataset generation, or dataset mutation.

## Synthetic Geometry Cell
- `sweep_id`: `stage_b_v1_geometry_integration_rehearsal`
- `cell_id`: `cell_synth_nocall_high_readfile_medium_v1`
- `axis_levels`: `{"no_call_pressure":"high","read_file_counterweight":"medium","rg_search_contrastive":"low","uncertainty_conditioning":"zero"}`
- `weighting_mode`: `metadata_weighted_random_sampler_probe`
- `geometry_sampling.enabled`: `true`
- `geometry_sampling.sampler_seed`: `314159`
- `threshold_profile_reference`: `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json`

## Flow Results
1. Geometry Context Flow
- `geometry_mapping_identity_digest`: `1f35b81bfe3dfae09e675361b193620955d2a2c51e6d720ad3b0b8cea4f13348`
- `geometry_context_input_digest`: `04a286d67a82dbd054ebcdc2c5ca485881534a0674a1241abcc64c4421797e9e`
- Legacy alias behavior:
  - mapping artifacts: `geometry_context_digest_alias_of=geometry_mapping_identity_digest`
  - detector artifacts: `geometry_context_digest_alias_of=geometry_context_input_digest`

2. Exposure Accounting Flow
- Declared ledger generated.
- Realized ledger generated in weighted captured mode.
- Drift ledger generated with runtime captured basis.

3. Weighted Sampling Flow
- Deterministic sampler metadata emitted.
- Sampled stream capture path exercised (`sampled_index_stream_total=12`).
- Weight digest emitted and linked.

4. Traceability Flow
- Artifact linkage captured in [integration_rehearsal_artifact_graph.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal_artifact_graph.json).
- Typed digests and legacy alias semantics are explicit in the graph.

5. Collapse Detection Flow
- Threshold profile ingested by standalone detector.
- Detector outputs include typed digests and legacy alias semantics.
- No eval execution occurred.

## End-to-End Reconstruction Capability
A reviewer can reconstruct intended geometry, realized geometry, weighting configuration, threshold profile, and lineage chain from emitted artifacts under:
- `/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1`
- [integration_rehearsal_artifact_graph.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal_artifact_graph.json)

## Remaining Gaps
- No runtime enforcement yet that detector `geometry_context_input_digest` must match a supplied mapping-side `geometry_context_input_digest` when both are present.
- Governance checks remain report-level (not hard runtime gate) for semantic misuse.

## Remaining Scientific Risks
- Synthetic rehearsal confirms instrumentation and lineage semantics, not behavioral robustness under full train/eval noise.
- Drift tolerance policy still requires governance calibration for live probe decisions.

## Readiness Recommendation
- `READY_FOR_SINGLE_CELL_PROBE`
: Rationale: typed digest semantics are explicit, deterministic, and backward-compatible; residual risk is now governance calibration, not digest ambiguity.
