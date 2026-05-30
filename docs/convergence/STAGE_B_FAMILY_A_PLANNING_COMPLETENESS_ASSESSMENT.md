# Stage B Family A Planning Completeness Assessment

## Scope

This document assesses whether Family A planning has reached implementation-planning readiness.

This is a review exercise only. It does not modify code, schemas, fixtures, validators, detectors, scorers, thresholds, governance rules, mappings, or manifests.

Reference inputs:

- `STAGE_B_WP8C_FAMILY_A_SUBTYPE_BOUNDARY_REVIEW.md`
- `STAGE_B_WP8C_SCENARIO_TO_SUBTYPE_MAPPING.md`
- `STAGE_B_WP3_FAMILY_A_SCORER_EVIDENCE_CONTRACT.md`

## Summary Determination

Family A planning has reached implementation-planning readiness.

The remaining work is approval, concrete scorer evidence output design, taxonomy marker/version design, and later schema/fixture implementation. Additional Family A planning is unlikely to materially change the taxonomy, boundary model, missing-evidence behavior, detector boundary, or reconciliation model.

Recommendation: A. Family A planning complete; proceed to implementation planning.

## 1. Architectural Unknowns

No architectural unknowns remain.

Settled architectural decisions:

- Family A is the Governed Failure-Subtype Taxonomy.
- Direct-answer substitution is retained as a governed subtype.
- Family A applies to eligible tool-expected rows.
- Exact-valid rows exit failure subtype assignment.
- Excluded rows exit governed subtype assignment and do not enter denominators.
- Every eligible non-exact tool-expected row requires exactly one approved subtype, or an explicit missing-evidence state.
- Missing or ambiguous subtype evidence creates noncomputability.
- Detector consumes emitted subtype facts and states only.
- A generic `other` subtype is not approved.

Unresolved items:

| Item | Classification | Assessment |
|---|---|---|
| Concrete storage location for scorer evidence outputs | implementation-planning | Needed before implementation, but does not change Family A architecture. |
| Concrete schema representation for taxonomy markers and subtype facts | implementation-planning | Belongs to schema/output design, not taxonomy architecture. |
| Concrete rollback mechanism for unstable subtype evidence | implementation-planning | Needed for implementation planning, not architecture redesign. |

## 2. Taxonomy Unknowns

No taxonomy-design unknowns remain.

Approved planning subtype set:

- direct-answer substitution;
- scalar substitution;
- malformed output;
- wrapper/envelope drift;
- missing tool call;
- wrong tool name;
- wrong argument.

Additional subtype candidates remain future-reserved and are not approved for current implementation planning:

- wrong tool-call cardinality;
- wrong tool-call ordering;
- extra unsupported tool call;
- ambiguous multiple failure;
- other/unclassified.

Unresolved items:

| Item | Classification | Assessment |
|---|---|---|
| Formal scorer-owner approval of subtype names | governance approval | Approval gate only; not expected to change taxonomy unless rejected. |
| Formal scorer-owner approval of precedence expectations | governance approval | Approval gate only; current precedence model is documented. |
| Future-reserved subtype disposition | implementation | Can remain out of scope unless implementation reveals unclassifiable observed failures. |

## 3. Evidence-Contract Unknowns

The conceptual evidence contract is complete.

Shared evidence dependencies have been identified:

- tool-expected eligibility;
- exclusion state;
- exact-valid outcome;
- primary scorer outcome;
- non-exact tool-expected status;
- parse/schema evidence;
- emitted tool-call attempt detection;
- expected and emitted tool identity;
- expected and emitted argument evidence;
- answer-like substitution evidence;
- scalar-like substitution evidence;
- tool-call absence evidence;
- wrapper/envelope evidence;
- approved subtype assignment;
- failure taxonomy marker;
- scorer semantics marker;
- missing-evidence reason.

Unresolved items:

| Item | Classification | Assessment |
|---|---|---|
| Concrete scorer evidence outputs | implementation-planning | Required before scorer implementation; does not change evidence contract semantics. |
| Evidence-output ownership handoff to evaluator aggregation | implementation-planning | Needed for packet sequencing and schema/output design. |
| Exact marker/version encoding | implementation-planning | Required before implementation; current marker semantics are settled. |
| Evidence precision for answer-like and scalar-like classification | implementation-planning | Requires scorer-owner review, but missing evidence already maps to noncomputability. |

## 4. Detector-Boundary Unknowns

No detector-boundary design unknowns remain.

Settled detector boundaries:

- Detector must not infer subtype from generated text.
- Detector must not inspect prompt text to infer expected tool behavior.
- Detector must not compare arguments.
- Detector must not infer tool identity.
- Detector must not infer scalar or prose substitution from output shape.
- Detector must not infer malformed output from invalid-json aggregate.
- Detector must not infer wrapper drift from wrapper leakage aggregate.
- Detector must not infer missing tool call from no-call correctness aggregate.
- Detector must not use historical direct-answer counts as current-run facts.
- Detector must not create an `other` subtype.
- Detector must not reconstruct denominators or rates.

Unresolved items:

| Item | Classification | Assessment |
|---|---|---|
| Detector-owner acceptance of non-inference boundary | governance approval | Approval gate; not a design unknown. |
| Concrete detector-facing projection | implementation-planning | Needed later, but detector ownership semantics are settled. |
| Negative fixture implementation proving non-inference | implementation | Covered by WP8 planning; not needed to decide readiness for implementation planning. |

## 5. Fixture-Coverage Unknowns

Family A fixture coverage is sufficient for implementation planning.

Settled coverage:

- Every approved subtype has at least one positive complete-emission scenario.
- Direct-answer substitution has additional partial, missing, historical, and detector non-inference coverage.
- Scalar substitution has positive and missing-evidence coverage.
- Malformed output, wrapper/envelope drift, missing tool call, wrong tool name, and wrong argument have positive complete-emission coverage.
- Boundary ambiguity is covered by the boundary review and scenario-to-subtype mapping.
- Missing evidence maps to noncomputability.

Unresolved items:

| Item | Classification | Assessment |
|---|---|---|
| Concrete fixture files | implementation | Not part of planning readiness; later implementation artifact. |
| Validator behavior for Family A fixtures | implementation | Requires fixture implementation and validators later. |
| Whether ambiguity-zone fixture count should be expanded beyond positive subtype coverage | implementation-planning | Desirable before fixture authoring, but not expected to change taxonomy. |
| Fixture-owner approval of scenario coverage | governance approval | Approval gate before implementation. |

## 6. Remaining Approval Requirements

The following approvals remain:

| Approval | Classification | Required Before |
|---|---|---|
| Scorer-owner approval of subtype names | governance approval | Scorer implementation planning completion. |
| Scorer-owner approval of precedence expectations | governance approval | Scorer implementation planning completion. |
| Scorer-owner approval of concrete evidence outputs | governance approval | Scorer implementation. |
| Schema owner approval of later evidence representation | governance approval | Schema/output implementation. |
| Validation owner approval of Family A fixture expectations | governance approval | Fixture implementation. |
| Governance owner confirmation that no generic `other` subtype is introduced | governance approval | Scorer implementation. |
| Taxonomy marker/version plan approval | governance approval | Schema/output implementation. |
| Detector owner acceptance of non-inference boundary | governance approval | Detector consumption implementation. |
| Rollback behavior approval for unstable subtype evidence | governance approval | Implementation sequencing. |

These approvals are required, but they do not justify additional broad Family A planning unless an approver rejects a core premise.

## 7. Risks Remaining Before Implementation

### Architectural Risks

No material architectural risk remains for Family A planning.

Residual architectural risk:

- A future implementation could attempt to introduce a generic `other` subtype to avoid missing-evidence noncomputability.

Classification: governance approval.

Mitigation:

- Keep `other/unclassified` not approved unless separately contracted and fixture-covered.

### Taxonomy Risks

Risk:

- Missing tool call may become over-broad if used as a fallback for uncertain failures.

Classification: implementation-planning.

Mitigation:

- Require clear tool-call absence evidence and absence of stronger direct-answer/scalar evidence.

Risk:

- Multiple simultaneous failures may pressure the one-subtype-per-row model.

Classification: implementation-planning.

Mitigation:

- Use documented precedence rules; if precedence evidence is missing, mark subtype missing/noncomputable.

### Evidence Risks

Risk:

- Scorer output may not preserve enough evidence to distinguish answer-like prose, scalar output, malformed output, and missing tool call.

Classification: implementation-planning.

Mitigation:

- Require concrete scorer evidence output design before implementation.

Risk:

- Expected tool identity or argument evidence may be unavailable at scorer time.

Classification: implementation-planning.

Mitigation:

- Verify dataset metadata and scorer input contract before scorer implementation.

### Detector Risks

Risk:

- Detector implementation may attempt to repair missing subtype evidence by inspecting generated text or aggregate metrics.

Classification: implementation.

Mitigation:

- Implement negative fixtures for generated-text classification, no-call proxy rejection, invalid-json proxy rejection, and wrapper-leakage proxy rejection.

### Fixture Risks

Risk:

- Positive coverage exists for every subtype, but ambiguity-zone fixture coverage may need expansion during fixture authoring.

Classification: implementation-planning.

Mitigation:

- Add ambiguity-zone fixture expansion as the first Family A fixture-authoring planning step if fixture owner requests it.

## Recommendation

Recommendation: A. Family A planning complete; proceed to implementation planning.

Rationale:

- No remaining architectural unknowns are open.
- Taxonomy design is settled for implementation planning.
- Evidence contract semantics are complete.
- Detector non-inference boundaries are explicit.
- Fixture coverage is sufficient for implementation planning.
- Remaining work is approval, concrete evidence output design, taxonomy marker/version design, and later implementation.
- Additional Family A planning is expected to mostly restate existing decisions unless an approver rejects the subtype set, precedence model, or evidence contract.

This recommendation does not authorize scorer implementation, schema changes, fixture implementation, validator implementation, detector changes, or threshold changes.

## Completion Findings

### Remaining Architectural Unknowns

None.

### Remaining Implementation-Planning Unknowns

- Concrete scorer evidence outputs.
- Concrete evidence-output handoff to evaluator aggregation.
- Taxonomy marker/version output design.
- Evidence precision for answer-like and scalar-like classification.
- Whether ambiguity-zone fixture scenarios should be expanded before fixture files are authored.
- Rollback behavior for unstable subtype evidence.

### Remaining Governance Approvals

- Scorer-owner approval of subtype names and precedence.
- Scorer-owner approval of concrete evidence outputs.
- Schema owner approval of later evidence representation.
- Validation owner approval of Family A fixture expectations.
- Governance owner approval that no generic `other` subtype is introduced.
- Taxonomy marker/version plan approval.
- Detector owner acceptance of non-inference boundary.

### Expected Value Of Additional Planning

Low for broad Family A planning.

Additional planning may be useful only if narrowly scoped to implementation-entry artifacts, such as scorer evidence output design or ambiguity-zone fixture expansion. It is not expected to change the Family A design.

### Confidence Level

Confidence level: high.

Basis:

- The subtype boundary review, scenario-to-subtype mapping, and scorer evidence contract converge on the same taxonomy and noncomputability model.
- All approved subtypes have evidence requirements.
- All known ambiguity zones have explicit missing-evidence behavior.
- Detector non-inference boundaries are explicit and consistent across artifacts.
