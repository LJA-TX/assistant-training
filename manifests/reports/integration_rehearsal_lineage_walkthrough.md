# Integration Rehearsal Lineage Walkthrough (Typed Digests)

1. Intended Geometry Reconstruction
- Read [synthetic_geometry_cell_definition.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/synthetic_geometry_cell_definition.json) for `sweep_id`, `cell_id`, and axis levels.
- Confirm resolved geometry context in [resolved_config.synthetic.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/resolved_config.synthetic.json).

2. Typed Digest Reconstruction
- Mapping identity digest: `geometry_mapping_identity_digest`.
- Detector input digest: `geometry_context_input_digest`.
- Legacy compatibility field: `geometry_context_digest` with `geometry_context_digest_alias_of`.

3. Declared Exposure Reconstruction
- Read [exposure_ledger_declared.synthetic.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/exposure_ledger_declared.synthetic.json).
- Use `declared_exposure_by_split.train` for intended family/archetype/axis distributions.

4. Weighting Configuration Reconstruction
- Read `geometry_sampling` block in resolved config.
- Confirm deterministic weighting metadata in [sampler_determinism_report.synthetic.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/sampler_determinism_report.synthetic.json).

5. Realized Geometry Reconstruction
- Read [exposure_ledger_realized.synthetic.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/exposure_ledger_realized.synthetic.json).
- Verify sampled stream digest matches sampler determinism report.

6. Declared-vs-Realized Divergence Reconstruction
- Read [exposure_ledger_drift.synthetic.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/exposure_ledger_drift.synthetic.json).
- Use `aggregate.max_abs_delta_any_dimension` as drift severity summary.

7. Threshold Profile and Gate Lineage
- Read [stage_b_v1_threshold_profile.json](/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json).
- Read detector outputs:
  - [collapse_watch_interpretation.synthetic.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/collapse_watch_interpretation.synthetic.json)
  - [gate_assessment.synthetic.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/gate_assessment.synthetic.json)
- Confirm `geometry_context_input_digest` equivalence across detector outputs.

8. Chain Completeness Check
- Use [integration_rehearsal_artifact_graph.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal_artifact_graph.json) for directed lineage edges and typed digest relationships.
