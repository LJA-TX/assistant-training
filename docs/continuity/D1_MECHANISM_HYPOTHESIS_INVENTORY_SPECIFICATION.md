# D1 Mechanism-Hypothesis Inventory Specification

Date: 2026-06-16

## Status

- Governance-only.
- No experimental design.
- No arm design.
- No execution planning.
- No training authorization.
- No preregistration creation.
- D0 blocker `D0-BLK-TRAINING-SCRIPT-PROVENANCE-001` remains active and unchanged.
- H1 and H2 remain observational reference regimes, not replay targets.
- A mechanism-hypothesis inventory is a catalog of candidate explanations, not evidence that any explanation is correct.

This specification defines the structure, standards, and acceptance requirements for a future D1 mechanism-hypothesis inventory. It does not create the inventory itself.

## 1. Purpose And Scope

The purpose of a D1 mechanism-hypothesis inventory is to catalog candidate explanations for observed current-tree and H-series behavior in a read-only governance form.

The inventory exists to:

- name candidate explanations explicitly
- classify those explanations by evidentiary status
- record the admissible evidence supporting or weakening each candidate
- preserve confound awareness
- support later governance review before any experimental design is considered

The inventory does not:

- authorize training
- authorize evaluation execution
- authorize experimental design
- authorize arm design
- authorize arm-specific run planning
- create preregistration
- prove that a candidate explanation is true

The inventory is a governance artifact, not an execution artifact.

## 2. Relationship To D0 And D1 Governance

This specification is subordinate to the approved [D1 Governance Foundation Package](./D1_GOVERNANCE_FOUNDATION_PACKAGE.md).

It inherits the D0 blocker and the D1 boundary rules already established there:

- D0 canonical-byte certification remains blocked.
- No manifest edits are authorized.
- No hash-claim edits are authorized.
- No training runs are authorized.
- No experimental arm execution is authorized.
- H1 and H2 are observational reference regimes, not replay targets.
- Current-tree review is distinct from canonical-byte certification.

The inventory specification operationalizes the D1 permission for read-only mechanism-hypothesis inventory and classification. It does not expand that permission into design, execution, or preregistration.

Relationship rules:

1. D0 continuity and blocker documents remain higher-order authority for canonical-byte and provenance questions.
2. The D1 Governance Foundation Package remains the authority for D1 boundary setting.
3. This specification only defines how a future inventory is structured and reviewed.
4. If a hypothesis requires experimental design to become meaningful, that design belongs to a later separately authorized process.

## 3. Admissible Evidence Sources

The future inventory may use only the following evidence classes:

### 3.1 D0 and D1 governance documents

- `docs/continuity/D0_TO_CURRENT_TREE_MECHANISM_ISOLATION_GOVERNANCE.md`
- `docs/continuity/D0_BLOCKER_REGISTER.md`
- `docs/continuity/D0_DRY_RUN_PROVENANCE_FINDING.md`
- `docs/continuity/D0_PROVENANCE_BLOCKER_RECOMMENDATION.md`
- `docs/continuity/D0_PROVENANCE_BLOCKER_RISK_ASSESSMENT.md`
- `docs/continuity/D0_SITUATION_REVIEW_AND_RECOMMENDATION_2026-06-15.md`
- `docs/continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md`
- `docs/current/framework_vs_history.md`
- `docs/current/status/TRAINING_RUN_HISTORY.md`

### 3.2 Current-tree operational surfaces

- `scripts/train_lora_sft.py`
- `scripts/build_dataset_v1.py`
- `scripts/eval_canonical_manifest.py`
- `tests/test_eval_canonical_manifest.py`
- `docs/current/baselines/README.md`
- `docs/current/baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md`

### 3.3 Frozen control and observational reference surfaces

- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json`
- `configs/lora/stage_b_llama31_8b_base_v1_i3.config.json`
- `manifests/runs/stage_b_llama31_8b_base_v1_i3.run_manifest.json`
- `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.json`
- `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.run_manifest.json`
- `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_val.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json`
- `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_val.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json`
- `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.config.json`
- `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.config.json`
- `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.run_manifest.json`
- `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.run_manifest.json`
- `evals/runs/stage_b_v1_phase_i_h0_control_i3_micro_eval_20260611T103048Z/summary.json`
- `evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/summary.json`
- `evals/runs/stage_b_v1_phase_i_h2_commitment_patch_eval_20260611T120228Z/summary.json`
- `evals/baselines/llama31/internal_reference_regimes/`

### 3.4 Frozen evaluation contract surfaces

- `evals/canonical_eval_manifest_v1.json`
- `docs/goal_charter_v5a.md`
- `docs/appendix_a_operational_execution_contract_v3a.md`
- `docs/metric_specification_v1a.md`

Admissible evidence is read-only evidence only. It may support classification, comparison, or confound tracking, but it may not be used to authorize execution or to infer truth by convenience.

## 4. Prohibited Evidence Sources

The future inventory may not use the following as evidence:

- any training output from an unauthorized run
- any evaluation output from an unauthorized run
- any comparison row, summary, or bundle created outside authorized boundaries
- any manifest edit or hash-claim edit
- any inferred, reconstructed, or heuristically completed provenance
- any arm design
- any arm-specific run plan
- any execution plan
- any preregistration artifact created for the purpose of launching a study
- any downstream artifact used as upstream evidence without authority
- any source that contradicts higher-order D0 or D1 authority

If a source is not expressly admissible above, it must be treated as prohibited for inventory purposes unless a higher-order governance document separately authorizes it.

## 5. Required Hypothesis Structure

Each inventory entry must represent exactly one candidate explanation.

Required fields:

| Field | Requirement |
|---|---|
| `hypothesis_id` | Stable, unique identifier. |
| `label` | Short human-readable name. |
| `classification` | One of the approved classification categories in Section 6. |
| `confidence_level` | One of the approved confidence levels in Section 7. |
| `candidate_explanation` | Plain-language statement of the explanation being cataloged. |
| `observed_pattern` | The observed behavior or regularity the hypothesis is meant to explain. |
| `evidence_refs` | Explicit references to admissible evidence sources only. |
| `comparison_class` | The comparison class used for the explanation. |
| `control_class` | The control or reference class used for contrast. |
| `relationship_type` | One of the permitted relationship types in Section 6, or `none` for a standalone entry. |
| `related_hypothesis_ids` | Ordered list of linked hypothesis IDs; empty only when `relationship_type` is `none`. |
| `fixed_surfaces` | Surfaces treated as fixed in the comparison. |
| `confounds` | Confound records linked to the hypothesis. |
| `status` | Catalog status such as `candidate`, `provisional`, `confounded`, `duplicate`, or `out_of_scope`. |
| `notes` | Optional clarifying notes. |

Required structural rules:

1. One entry, one explanation. Do not bundle multiple mechanisms into a single hypothesis.
2. The candidate explanation must be phrased as a cataloged explanation, not as a proof.
3. The entry must state what is being explained before stating how it is believed to work.
4. The entry must identify the comparison and control classes explicitly.
5. The entry must identify every fixed surface it relies on.
6. The entry must list confounds rather than hiding them in prose.
7. The entry must not include arm design, run planning, or execution instructions.

## 6. Hypothesis Relationship Rules

Relationship metadata is descriptive only. It does not constitute evidence, proof, prioritization, or execution guidance.

Permitted relationship types:

- `duplicate_of`
- `derivative_of`
- `parent_of`
- `child_of`
- `competing_with`
- `composite_of`
- `component_of`

Sentinel value:

- `none` indicates a standalone entry with no declared relationship.
- `none` is not a relationship type and carries no inferential weight.

Relationship rules:

1. `relationship_type` and `related_hypothesis_ids` are required for every entry.
2. If `relationship_type` is `none`, `related_hypothesis_ids` must be empty.
3. If `relationship_type` is not `none`, `related_hypothesis_ids` must be non-empty.
4. Every `related_hypothesis_ids` value must refer to an existing hypothesis entry in the same inventory.
5. `duplicate_of` and `derivative_of` entries must reference their source entry or entries explicitly.
6. `duplicate_of` and `derivative_of` are directional and do not imply proof of equivalence.
7. `parent_of` and `child_of` are directional and must be reciprocally consistent when both entries are present.
8. `composite_of` and `component_of` are directional and must be reciprocally consistent when both entries are present.
9. `competing_with` is symmetric and must be mirrored by the related entry when both entries are present.
10. Relationships may be used to record catalog structure only. They may not be used as evidence, proof, prioritization, or execution guidance.
11. Any entry classified as `duplicate_or_derivative` must use `duplicate_of` or `derivative_of` as its `relationship_type`.

## 7. Hypothesis Classification Categories

The inventory may classify entries using the following categories:

| Category | Meaning | Admissible status |
|---|---|---|
| `observational_pattern` | Describes a repeated pattern or regularity without committing to a mechanism. | Admissible. |
| `mechanistic_candidate` | Proposes a plausible mechanism that could explain the observed pattern. | Admissible. |
| `control_or_null` | Proposes preservation, null, or non-effect explanation for a pattern. | Admissible. |
| `confounded_candidate` | Candidate explanation with unresolved confounds that materially limit interpretation. | Admissible, but must be labeled clearly. |
| `duplicate_or_derivative` | Restates or partially restates an existing hypothesis entry. | Admissible only as a cross-reference, not as a primary entry. |
| `out_of_scope` | Does not belong in the inventory as a candidate explanation. | Not admissible as an active entry. |

Classification rules:

1. Classification is descriptive, not promotional.
2. Classification does not establish truth.
3. A high-confidence candidate can still be false.
4. A confounded candidate can still be worth cataloging if the confound is explicit.
5. Duplicates must be cross-referenced, not inflated into separate claims.

## 8. Confidence-Level Definitions

Confidence is a cataloging judgment about support quality, not a truth verdict.

| Level | Definition | Typical evidence posture |
|---|---|---|
| `low` | Limited admissible support; substantial ambiguity remains. | One surface or weakly connected sources. |
| `moderate` | Multiple admissible sources point in the same direction, but important gaps remain. | Cross-surface support with explicit confounds. |
| `high` | Several admissible sources converge and the candidate is internally coherent under the recorded constraints. | Strong convergence, but still not proof. |
| `undetermined` | The evidence is insufficient to rate the candidate responsibly. | Missing or incomplete admissible support. |

Confidence rules:

1. Confidence is about support quality, not certainty.
2. High confidence does not convert the inventory into evidence of correctness.
3. Confidence may be lowered by unresolved confounds even when a candidate remains catalog-worthy.
4. Undetermined confidence is an acceptance failure for the inventory entry until resolved or downgraded.

## 9. Confound Documentation Requirements

Every hypothesis entry must document its confounds explicitly.

Required confound fields:

- `confound_id`
- `description`
- `affected_hypothesis_ids`
- `evidence_ref`
- `direction_of_bias`
- `impact_scope`
- `resolution_status`
- `residual_risk`
- `notes`

Confound rules:

1. Confounds must be named, not implied.
2. The likely direction of distortion must be stated when known.
3. Shared confounds must be identified as shared.
4. Confounds that could alter the interpretation materially must be marked clearly.
5. A missing confound record is not a neutral omission; it is a structural defect.
6. Confound documentation is descriptive only and does not itself authorize mitigation work.

## 10. Comparison And Control Requirements

Each hypothesis entry must state how it is compared and what it is compared against.

Required comparison and control elements:

- at least one explicit comparison class
- at least one explicit control or reference class
- explicit fixed surfaces
- explicit statement of what is held constant
- explicit statement of what is varying only at the level of catalog description

Approved comparison classes may include:

- current-tree baseline comparisons
- frozen `i3` / `H0` control comparisons
- H1 observational comparisons
- H2 observational comparisons
- frozen evaluation contract comparisons

Approved control classes may include:

- `i3` control scaffold
- `H0` control comparator
- `H1` observational reference regime
- `H2` observational reference regime
- frozen evaluation contract

Control rules:

1. Controls must be named from admissible evidence only.
2. Controls may not be invented ad hoc to strengthen a narrative.
3. A hypothesis entry without a named control class is incomplete.
4. A hypothesis entry may not use a future or hypothetical output as its control.
5. Comparison must remain read-only and descriptive.

## 11. Inventory Acceptance Criteria

The inventory is acceptable only when the catalog is structurally complete and boundary-compliant.

Acceptance criteria:

- Every entry has a unique `hypothesis_id`.
- Every entry includes the required fields in Section 5.
- Every entry uses only admissible evidence sources.
- Every entry has a classification and confidence level.
- Every entry has a valid `relationship_type` and `related_hypothesis_ids` value.
- Every entry documents comparison and control classes.
- Every entry documents confounds.
- No entry includes arm design, execution planning, training authorization, or preregistration creation.
- No entry treats H1 or H2 as replay targets or canonical-byte proof.
- Every referenced hypothesis ID exists in the inventory.
- Relationship declarations are internally consistent with Section 6.
- Duplicate and derivative entries reference their source entries explicitly and use a matching `relationship_type`.
- The inventory as a whole remains clearly a catalog of candidate explanations.
- The inventory does not imply that any candidate explanation is correct.

Acceptance of the inventory means the catalog is usable for later governance review. It does not mean the cataloged explanations are validated.

## 12. Failure Taxonomy

### Severity classes

- `fatal`: stop inventory review immediately and escalate.
- `blocking`: stop the affected inventory entry or section.
- `advisory`: record and continue, but do not treat the issue as resolved.

| Code | Trigger | Severity | Stop action |
|---|---|---|---|
| `AUTHORITY_CONFLICT` | The inventory conflicts with D0 continuity or D1 foundation authority. | fatal | Stop all review and resolve the authority chain. |
| `D0_BLOCKER_REINTERPRETATION` | The blocker is weakened, relabeled, or treated as advisory. | fatal | Stop immediately and preserve the original blocker status. |
| `REFERENCE_REGIME_MISLABEL` | H1 or H2 is treated as a replay target, proof target, or execution target. | fatal | Stop immediately and correct the label. |
| `PROHIBITED_SOURCE_USE` | A prohibited evidence source is used as supporting evidence. | fatal | Stop immediately and remove the source from the inventory. |
| `INFERENCE_CONTAMINATION` | Missing evidence is filled by heuristic inference or unsupported completion. | fatal | Stop immediately and mark the missing evidence as missing. |
| `RELATIONSHIP_SCHEMA_VIOLATION` | `relationship_type` or `related_hypothesis_ids` is missing, malformed, or uses an unsupported value. | blocking | Stop the affected entry until the schema is corrected. |
| `MISSING_REFERENCED_HYPOTHESIS` | A related hypothesis ID does not exist in the inventory. | blocking | Stop the affected entry until the reference is resolved. |
| `RELATIONSHIP_INCONSISTENCY` | Relationship direction, reciprocity, or duplicate/derivative source reference is internally inconsistent. | blocking | Stop the affected entry until the relationship is corrected. |
| `MISSING_REQUIRED_FIELD` | A hypothesis entry lacks a required field. | blocking | Stop the affected entry until the field is supplied. |
| `CONTROL_CLASS_ABSENT` | A hypothesis entry lacks a named control class. | blocking | Stop the affected entry until the control is named. |
| `CONFIDENCE_OVERCLAIM` | Confidence language is used as if it were proof. | blocking | Stop the affected entry and downgrade the wording. |
| `SCHEMA_DRIFT` | The inventory structure deviates from this specification. | blocking | Stop the affected section and restore the schema. |
| `EXECUTION_LEAKAGE` | Arm design, run planning, execution planning, or training authorization appears. | fatal | Stop immediately and remove the leaked content. |
| `BOUNDARY_BREACH` | The inventory is used to imply preregistration or experiment authorization. | fatal | Stop immediately and restore governance-only framing. |

## 13. Boundary Confirmation

- No training authorization is granted.
- No evaluation execution is authorized.
- No experimental design is introduced.
- No arm design is introduced.
- No arm-specific run planning is introduced.
- No execution planning is introduced.
- No preregistration is created.
- The D0 blocker remains unchanged.
- H1 and H2 remain observational reference regimes.
- The inventory remains a catalog of candidate explanations, not evidence that any explanation is correct.
