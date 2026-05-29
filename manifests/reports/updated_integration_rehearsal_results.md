# Updated Integration Rehearsal Results

## Typed Digest Outcome
- Mapping identity digest:
  - `geometry_mapping_identity_digest=1f35b81bfe3dfae09e675361b193620955d2a2c51e6d720ad3b0b8cea4f13348`
- Context input digest:
  - `geometry_context_input_digest=04a286d67a82dbd054ebcdc2c5ca485881534a0674a1241abcc64c4421797e9e`
- Legacy alias behavior:
  - mapping stack: `geometry_context_digest_alias_of=geometry_mapping_identity_digest`
  - detector stack: `geometry_context_digest_alias_of=geometry_context_input_digest`

## Governance Interpretation Update
- Cross-type digest inequality is treated as expected semantic divergence.
- Failure conditions now focus on semantic misuse:
  - wrong alias target
  - missing typed fields
  - cross-stack mismatch within the same digest type

## Rehearsal Validation Snapshot
- Geometry context flow: `PASS`
- Exposure accounting flow: `PASS`
- Weighted sampling flow: `PASS`
- Traceability flow: `PASS`
- Collapse detector flow: `PASS`
- End-to-end reconstruction with typed digests: `PASS`

## Artifact References
- [integration_rehearsal_artifact_graph.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal_artifact_graph.json)
- [updated_artifact_graph_example.json](/opt/ai-stack/assistant-training/manifests/reports/updated_artifact_graph_example.json)
- [integration_rehearsal_validation_results.md](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal_validation_results.md)

## Readiness Recommendation
- `READY_FOR_SINGLE_CELL_PROBE`
- Rationale: digest ambiguity is resolved with explicit typed semantics and backward-compatible aliasing; remaining risks are scientific threshold calibration and drift-governance policy.
