# Integration Rehearsal Lineage Walkthrough

1. Intended Geometry Reconstruction
- Read [synthetic_geometry_cell_definition.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/synthetic_geometry_cell_definition.json) for `sweep_id`, `cell_id`, axis levels, and weighting intent.
- Confirm resolved geometry context in [resolved_config.synthetic.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/resolved_config.synthetic.json).

2. Declared Exposure Reconstruction
- Read [exposure_ledger_declared.synthetic.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/exposure_ledger_declared.synthetic.json).
- Use `declared_exposure_by_split.train` for intended family/archetype/axis distributions.

3. Weighting Configuration Reconstruction
- Read `geometry_sampling` block from resolved config.
- Confirm deterministic weighting metadata in [sampler_determinism_report.synthetic.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/sampler_determinism_report.synthetic.json):
  - `sampler_seed`
  - `replacement`
  - `num_samples_policy`
  - `weights_digest_sha256`

4. Realized Geometry Reconstruction
- Read [exposure_ledger_realized.synthetic.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/exposure_ledger_realized.synthetic.json) for runtime sampled-stream realized counts.
- Verify sampled stream digest matches sampler determinism report.

5. Declared-vs-Realized Divergence Reconstruction
- Read [exposure_ledger_drift.synthetic.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/exposure_ledger_drift.synthetic.json).
- Use `aggregate.max_abs_delta_any_dimension=2` for drift severity summary.

6. Threshold Profile and Gate Lineage
- Read threshold profile at [stage_b_v1_threshold_profile.json](/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json).
- Read detector outputs:
  - [collapse_watch_interpretation.synthetic.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/collapse_watch_interpretation.synthetic.json)
  - [gate_assessment.synthetic.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal/cell_synth_nocall_high_readfile_medium_v1/gate_assessment.synthetic.json)
- Confirm profile digest consistency across both outputs.

7. Chain Completeness Check
- Use [integration_rehearsal_artifact_graph.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal_artifact_graph.json) for directed lineage edges from cell definition to gate assessment.
