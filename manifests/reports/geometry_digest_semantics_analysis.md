# Geometry Digest Semantics Analysis

## Scope
Read-only analysis of Stage B instrumentation + integration rehearsal digest semantics.

Reviewed:
- [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py)
- [post_eval_collapse_detector.py](/opt/ai-stack/assistant-training/scripts/post_eval_collapse_detector.py)
- [stage_b_v1_integration_rehearsal.md](/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_integration_rehearsal.md)
- [integration_rehearsal_validation_results.md](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal_validation_results.md)
- [integration_rehearsal_artifact_graph.json](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal_artifact_graph.json)
- [integration_rehearsal_lineage_walkthrough.md](/opt/ai-stack/assistant-training/manifests/reports/integration_rehearsal_lineage_walkthrough.md)

## 1) Mapping Stack Digest
Constructor:
- `_build_geometry_context_digest` in [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py:60)

Included fields:
- `geometry_schema_version`
- `sweep_id`
- `cell_id`
- `axis_levels`
- `weighting_mode`

Not included:
- `declared_exposure_units`
- any run-level paths, model/trainer settings, gate/eval metadata

Observed semantics:
- Stable **geometry configuration identity** for mapping cell coordinates.
- Digest is intentionally tied to core geometry axes + weighting mode, not to declared budgets or downstream evaluation context.

## 2) Detector Stack Digest
Constructor:
- `geometry_digest = _sha256_text(_canonical_json_text(geometry_context))` in [post_eval_collapse_detector.py](/opt/ai-stack/assistant-training/scripts/post_eval_collapse_detector.py:506)

Included fields:
- Entire provided `geometry_context` object (all keys present in input file).

Semantics:
- **Detector input context digest** (not explicitly constrained to mapping identity fields).
- If additional keys are present in detector geometry context input, digest changes.

## 3) Consumer Inventory Summary
Detailed machine-readable inventory:
- [geometry_digest_consumer_inventory.json](/opt/ai-stack/assistant-training/manifests/reports/geometry_digest_consumer_inventory.json)

Key finding:
- Most code paths **emit** digest but do not enforce cross-system digest equivalence.
- Rehearsal validation/reporting artifacts explicitly treat mapping-vs-detector digest divergence as a gap (human governance assumption of equivalence).

## 4) Semantic Interpretation
Mapping digest currently best matches:
- Geometry identity: **Yes**
- Geometry configuration identity: **Yes**
- Geometry lineage identity: **Partial** (insufficient alone for full lineage)
- Experiment identity: **No**

Detector digest currently best matches:
- Geometry context identity: **Yes (full object)**
- Detector context identity: **Yes (if geometry_context includes detector-relevant keys)**
- Evaluation context identity: **Partial** (only geometry-context slice)
- Gate context identity: **Partial**

## 5) Primary Question Assessment (A/B/C)
Assessment:
- **B is true**: these are two valid differently scoped digests.
- **C is also true**: using one field name (`geometry_context_digest`) for two scopes creates a lineage-modeling ambiguity.
- Therefore this is not purely a bug in hashing logic; it is a semantic-contract issue.

Conclusion to primary question:
- Best characterization: **C (broader lineage-modeling issue), with B as the immediate technical state**.

## 6) Option Analysis and Migration Impact
Detailed option matrix:
- [geometry_digest_option_matrix.json](/opt/ai-stack/assistant-training/manifests/reports/geometry_digest_option_matrix.json)

High-level:
- Option A (mapping canonical): improves cell identity stability; may lose detector-context fidelity.
- Option B (detector canonical): broad context fidelity; weakens strict cell identity stability unless normalized.
- Option C (split digest types): preserves both semantics and removes ambiguity with explicit contracts.

## Final Recommendation
See:
- [geometry_digest_recommendation.md](/opt/ai-stack/assistant-training/manifests/reports/geometry_digest_recommendation.md)

Recommended outcome:
- `SPLIT_INTO_DISTINCT_DIGEST_TYPES`
