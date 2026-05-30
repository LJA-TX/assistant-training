# Stage B WP3 Scorer Evidence Output Design Review

## Scope

This document defines the scorer evidence outputs required to support the approved Family A scorer evidence contract.

This is implementation planning only. It does not implement scorer logic, implement schemas, implement validators, create fixture files, modify code, modify detectors, modify evaluators, modify scorers, modify thresholds, modify governance rules, modify mappings, or modify manifests.

Reference inputs:

- `STAGE_B_WP8C_FAMILY_A_SUBTYPE_BOUNDARY_REVIEW.md`
- `STAGE_B_WP8C_SCENARIO_TO_SUBTYPE_MAPPING.md`
- `STAGE_B_WP3_FAMILY_A_SCORER_EVIDENCE_CONTRACT.md`
- `STAGE_B_FAMILY_A_PLANNING_COMPLETENESS_ASSESSMENT.md`

Design boundaries:

- These are conceptual output requirements, not schema field names.
- Scorer output must support evaluator aggregation without detector inference.
- Missing required scorer evidence remains noncomputable.
- Direct-answer substitution remains a governed subtype inside Family A.
- A generic `other` subtype remains unapproved.

## Output Design Principles

- Every eligible non-exact tool-expected row must have one approved Family A subtype or an explicit missing-evidence state.
- Exact-valid rows exit Family A failure-subtype assignment.
- Excluded rows exit governed denominators before subtype assignment.
- The scorer owns subtype evidence and subtype assignment.
- Dataset metadata owns row identity, split membership, tool-expected eligibility, expected tool behavior, and exclusions unless a later approved contract assigns part of that ownership elsewhere.
- The evaluator owns aggregation, denominator construction from emitted facts, reconciliation, completeness state, and current-run computability state.
- The detector owns policy consumption only and must not reconstruct scorer evidence.

## 1. Evidence Output Inventory

The following output inventory is the concrete planning target for WP3. Output IDs are planning labels only and are not schema names.

| Output ID | Output Concept | Requirement | Primary Owner | Required For | Detector Visibility | Notes |
|---|---|---|---|---|---|---|
| FA-OUT-001 | Row identity reference | Mandatory | Dataset metadata, carried through scorer handoff | audit, reconciliation, comparability | Hidden from detector ownership | Required to trace row-level evidence to aggregate coverage. |
| FA-OUT-002 | Split membership reference | Mandatory | Dataset metadata, carried through scorer handoff | split aggregation, comparability | Summary only | Required for split-scoped Family A summaries. |
| FA-OUT-003 | Tool-expected eligibility reference | Mandatory | Dataset metadata | eligible population, denominator basis, noncomputability | Summary only | Detector must not infer eligibility from prompt or response text. |
| FA-OUT-004 | Exclusion state reference | Mandatory | Dataset metadata or approved evaluator pre-filter | denominator basis, reconciliation | Summary only | Excluded rows do not receive governed subtype assignment. |
| FA-OUT-005 | Expected tool identity availability | Mandatory for tool-comparison rows | Dataset metadata | wrong tool name, wrong argument, exact-valid partition | Hidden from detector ownership | Absence blocks affected subtype assignment. |
| FA-OUT-006 | Expected argument evidence availability | Mandatory for argument-comparison rows | Dataset metadata or scorer input contract | wrong argument, exact-valid partition | Hidden from detector ownership | Absence blocks wrong-argument assignment. |
| FA-OUT-007 | Primary scorer outcome | Mandatory | Scorer | exact/non-exact partition, reconciliation | Summary only | Missing primary outcome blocks Family A row partition. |
| FA-OUT-008 | Exact-valid outcome | Mandatory | Scorer | exact-valid exit, non-exact denominator | Summary only | Must not be reconstructed from JSON validity, subtype counts, or generated text. |
| FA-OUT-009 | Non-exact tool-expected status | Mandatory | Scorer from metadata and scorer outcome | subtype eligibility | Summary only | This is the row population that requires subtype assignment or missing evidence. |
| FA-OUT-010 | Valid required tool-call detection | Mandatory | Scorer | exact-valid dependency, missing tool call, substitutions | Hidden from detector ownership | Establishes whether a satisfying required invocation exists. |
| FA-OUT-011 | Emitted tool-call attempt status | Mandatory when response may be tool-like | Scorer | malformed output, wrapper drift, wrong tool name, wrong argument | Hidden from detector ownership | Required to distinguish absence from attempted tool form. |
| FA-OUT-012 | Parse/schema status | Mandatory | Scorer | malformed output, wrapper drift, identity and argument extraction | Hidden from detector ownership | Missing parse evidence blocks malformed or parse-dependent assignment. |
| FA-OUT-013 | Emitted tool identity status | Mandatory when tool-call attempt is parseable | Scorer | wrong tool name, wrong argument precedence | Hidden from detector ownership | Missing identity evidence blocks wrong-tool-name assignment. |
| FA-OUT-014 | Emitted argument status and comparison outcome | Mandatory when expected-tool call is parseable | Scorer | wrong argument | Hidden from detector ownership | Missing comparable argument evidence blocks wrong-argument assignment. |
| FA-OUT-015 | Answer-like substitution evidence | Mandatory for direct-answer subtype | Scorer | direct-answer substitution | Hidden from detector ownership | Required to distinguish direct-answer from scalar and missing tool call. |
| FA-OUT-016 | Scalar-like substitution evidence | Mandatory for scalar subtype | Scorer | scalar substitution | Hidden from detector ownership | Required to prevent relabeling scalar output as direct-answer. |
| FA-OUT-017 | Wrapper/envelope evidence | Mandatory for wrapper drift subtype | Scorer | wrapper/envelope drift | Hidden from detector ownership | Required to distinguish near-tool protocol drift from malformed output. |
| FA-OUT-018 | Tool-call absence evidence | Mandatory for missing-tool-call subtype | Scorer | missing tool call | Hidden from detector ownership | Must not be a fallback for ambiguous failures. |
| FA-OUT-019 | Precedence resolution evidence | Mandatory for ambiguity zones | Scorer | one-subtype assignment, reconciliation | Hidden from detector ownership | Missing precedence evidence creates missing-evidence state. |
| FA-OUT-020 | Approved subtype assignment | Mandatory for every eligible non-exact row with complete evidence | Scorer | subtype counts, governed direct-answer concept | Aggregate/subtype summary only | Must be one approved subtype, not `other`. |
| FA-OUT-021 | Missing-evidence state | Mandatory when subtype assignment cannot be emitted | Scorer | noncomputability | Summary only | Required instead of fallback subtype assignment. |
| FA-OUT-022 | Missing-evidence reason | Mandatory when evidence is missing | Scorer | noncomputability, audit, reconciliation | Summary only | Must identify affected evidence class. |
| FA-OUT-023 | Failure taxonomy marker | Mandatory | Scorer, approved by governance | governed interpretation, comparability | Visible as marker | Required before subtype facts are governance-computable. |
| FA-OUT-024 | Scorer semantics marker | Mandatory | Scorer | comparability, migration review | Visible as marker | Required before historical comparison can be allowed. |
| FA-OUT-025 | Population and exclusion comparability references | Mandatory for comparison review | Dataset metadata and evaluator, carried through handoff | comparability | Visible as marker summary | Required to keep current-run computability separate from baseline comparability. |
| FA-OUT-026 | Optional subtype rationale | Optional diagnostic | Scorer | review and debugging | Hidden from detector ownership | Cannot substitute for mandatory evidence outputs. |
| FA-OUT-027 | Optional rejected-candidate notes | Optional diagnostic | Scorer | ambiguity review | Hidden from detector ownership | Useful for audit, not a governed metric input. |
| FA-OUT-028 | Optional parse or mismatch class | Optional diagnostic | Scorer | fixture debugging and review | Hidden from detector ownership | Examples include parse failure class or argument mismatch class. |

Mandatory output summary:

- Eligibility and denominator basis outputs: `FA-OUT-001` through `FA-OUT-006`.
- Scorer partition outputs: `FA-OUT-007` through `FA-OUT-010`.
- Tool-attempt and subtype evidence outputs: `FA-OUT-011` through `FA-OUT-019` when applicable to the row.
- Subtype or missing-evidence outputs: `FA-OUT-020` through `FA-OUT-022`.
- Taxonomy, scorer, and comparability marker outputs: `FA-OUT-023` through `FA-OUT-025`.

Optional output summary:

- `FA-OUT-026` through `FA-OUT-028` are review aids only.
- Optional outputs must never repair missing mandatory evidence.
- Optional outputs must not become detector-owned evidence unless a later approved contract makes them governed.

## 2. Shared Evidence Outputs

### Applicability Output Bundle

Purpose:

- Establish whether a row belongs in the governed Family A population.

Mandatory outputs:

- Row identity reference.
- Split membership reference.
- Tool-expected eligibility reference.
- Exclusion state reference.
- Expected tool identity availability when tool comparison is required.
- Expected argument evidence availability when argument comparison is required.

Required for reconciliation:

- Eligible tool-expected denominator.
- Excluded-row accounting.
- Split-to-aggregate reconciliation.

Required for noncomputability:

- Missing eligibility, exclusion, split, or expected-behavior evidence must produce an explicit missing-evidence or metadata-missing state.

Required for comparability:

- Population, split, tool-expected eligibility, expected-behavior, and exclusion-policy markers.

### Scorer Partition Output Bundle

Purpose:

- Separate exact-valid rows from non-exact rows before subtype assignment.

Mandatory outputs:

- Primary scorer outcome.
- Exact-valid outcome.
- Non-exact tool-expected status.
- Valid required tool-call detection.

Required for reconciliation:

- Eligible tool-expected denominator must reconcile with exact-valid eligible rows, non-exact eligible rows, and exclusions.
- Non-exact eligible rows must reconcile with subtype assignment or missing-evidence state.

Required for noncomputability:

- Missing primary scorer outcome or exact-valid outcome blocks Family A partitioning.

Required for comparability:

- Scorer semantics marker and exact-valid semantics marker.

### Tool-Attempt Output Bundle

Purpose:

- Distinguish malformed output, wrapper drift, wrong tool name, wrong argument, missing tool call, and substitution behavior.

Mandatory outputs when applicable:

- Emitted tool-call attempt status.
- Parse/schema status.
- Emitted tool identity status.
- Emitted argument status and comparison outcome.
- Valid required tool-call detection.

Required for reconciliation:

- Parseable tool-call attempts must resolve to exact-valid, wrong tool name, wrong argument, wrapper drift, malformed output, or missing evidence.

Required for noncomputability:

- Missing parse, identity, argument, or attempt evidence blocks affected subtype assignment when no other approved subtype has complete evidence.

Required for comparability:

- Scorer semantics marker covering parse, identity, and argument comparison behavior.

### Substitution And Absence Output Bundle

Purpose:

- Distinguish tool bypass and absence classes without detector text review.

Mandatory outputs when applicable:

- Answer-like substitution evidence.
- Scalar-like substitution evidence.
- Tool-call absence evidence.
- Precedence resolution evidence for direct-answer, scalar, malformed, wrapper, and missing-tool-call ambiguity zones.

Required for reconciliation:

- Direct-answer, scalar, and missing-tool-call counts must each contribute exactly one subtype count when assigned.

Required for noncomputability:

- Missing substitution or absence evidence blocks assignment of the affected subtype.

Required for comparability:

- Failure taxonomy marker and scorer semantics marker covering substitution and absence classification.

### Taxonomy And Missing-Evidence Output Bundle

Purpose:

- Tie every Family A fact to the approved taxonomy and preserve noncomputability when required evidence is absent.

Mandatory outputs:

- Approved subtype assignment or missing-evidence state.
- Missing-evidence reason when subtype assignment is absent.
- Failure taxonomy marker.
- Scorer semantics marker.

Required for reconciliation:

- Every eligible non-exact row must reconcile to exactly one approved subtype or one missing-evidence state.
- Subtype totals must reconcile to the non-exact eligible denominator only when missing-evidence states are absent or explicitly accounted for as noncomputable.

Required for noncomputability:

- Missing subtype, missing reason, missing taxonomy marker, or missing scorer marker blocks governed Family A computation.

Required for comparability:

- Taxonomy and scorer semantics markers are prerequisites for baseline comparison review.

## 3. Subtype-Specific Evidence Outputs

| Subtype | Mandatory Outputs | Optional Outputs | Missing-Evidence Behavior | Reconciliation Role |
|---|---|---|---|---|
| direct-answer substitution | Tool-expected eligibility; exact-valid false; no valid required tool call; answer-like substitution evidence; precedence evidence distinguishing scalar, malformed, wrapper drift, and missing tool call; failure taxonomy marker; subtype assignment. | Rationale for answer-like classification; rejected-candidate notes; prose-vs-scalar diagnostic. | Missing answer-like or precedence evidence makes direct-answer subtype noncomputable for the affected row. | Direct-answer count contributes one subtype count and supports the retained governed subtype. |
| scalar substitution | Tool-expected eligibility; exact-valid false; no valid required tool call; scalar-like substitution evidence; precedence evidence distinguishing direct-answer, malformed, and wrong argument; failure taxonomy marker; subtype assignment. | Scalar-form diagnostic; rejected-candidate notes. | Missing scalar or precedence evidence makes scalar subtype assignment noncomputable. | Scalar count contributes one sibling subtype count and must not be relabeled as direct-answer. |
| malformed output | Tool-expected eligibility; exact-valid false; parse/schema status showing malformed output; precedence evidence ruling out wrapper drift, wrong tool name, and wrong argument when available; failure taxonomy marker; subtype assignment. | Parse failure class; schema validation failure class; rationale for why parseable subtypes were unavailable. | Missing parse/schema evidence blocks malformed-output assignment unless another approved subtype has complete evidence. | Malformed count contributes one sibling subtype count and remains separate from invalid-json aggregate metrics. |
| wrapper/envelope drift | Tool-expected eligibility; exact-valid false; recognizable tool-call-like attempt; wrapper/envelope evidence; primary-failure or precedence evidence; failure taxonomy marker; subtype assignment. | Wrapper failure class; recognized tool-call-like intent; primary-failure rationale. | Missing near-tool or precedence evidence blocks wrapper-drift assignment. | Wrapper-drift count contributes one sibling subtype count and remains separate from wrapper leakage metrics. |
| missing tool call | Tool-expected eligibility; exact-valid false; no valid required tool call; tool-call absence evidence; absence of sufficient direct-answer and scalar evidence; absence of parseable wrong-tool evidence; failure taxonomy marker; subtype assignment. | Response-empty, refusal, unrelated-output, or unsupported-output indicator; rejected substitution candidates. | Missing absence evidence blocks missing-tool-call assignment. Missing tool call must not be used as a fallback. | Missing-tool-call count contributes one sibling subtype count and remains separate from no-call correctness metrics. |
| wrong tool name | Tool-expected eligibility; exact-valid false; parseable tool-call attempt; expected tool identity availability; emitted tool identity status; mismatch evidence; failure taxonomy marker; subtype assignment. | Recognized emitted tool identity; expected tool identity reference; precedence rationale over wrong argument. | Missing expected or emitted tool identity blocks wrong-tool-name assignment. | Wrong-tool-name count contributes one sibling subtype count and generally precedes wrong argument when tool identity is wrong. |
| wrong argument | Tool-expected eligibility; exact-valid false; parseable expected-tool call; emitted tool identity matches expected tool identity; expected argument evidence availability; emitted argument evidence; failed argument comparison; failure taxonomy marker; subtype assignment. | Argument mismatch class; comparison rationale; expected argument reference. | Missing expected argument, emitted argument, comparison, or correct-tool evidence blocks wrong-argument assignment. | Wrong-argument count contributes one sibling subtype count and requires correct tool identity evidence. |

Subtype-specific mandatory outputs are required for governed subtype assignment. Optional subtype diagnostics may support review, but they must not be used to compute governed counts unless promoted through a later approved contract.

## 4. Evaluator Handoff Requirements

The scorer-to-evaluator handoff must provide enough emitted evidence for aggregation without requiring evaluator or detector reconstruction.

Mandatory handoff content:

- Family A applicability output bundle.
- Scorer partition output bundle.
- Tool-attempt output bundle when applicable.
- Substitution and absence output bundle when applicable.
- Approved subtype assignment for each eligible non-exact row when evidence is complete.
- Missing-evidence state and reason for each eligible non-exact row when evidence is incomplete.
- Failure taxonomy marker.
- Scorer semantics marker.
- Population, split, exclusion, and expected-behavior comparability references.

Evaluator responsibilities after handoff:

- Build Family A aggregate summaries from emitted row-level facts.
- Emit direct-answer governed subtype summary.
- Emit sibling subtype summaries needed for reconciliation.
- Emit counts, denominators, and rates only when denominator basis is complete.
- Emit completeness state and current-run computability state.
- Preserve missing-evidence states as noncomputability.
- Preserve split-scoped summaries only when split evidence is complete.
- Preserve comparability status separately from current-run computability.

Evaluator must not:

- Infer subtype from generated text.
- Infer tool-expected eligibility from prompt text.
- Repair missing scorer facts from sibling subtype totals.
- Convert optional diagnostics into governed evidence.
- Use invalid-json, wrapper leakage, no-call correctness, or historical direct-answer counts as Family A subtype facts.

Handoff blocking conditions:

- Missing row identity, split membership, tool-expected eligibility, or exclusion evidence for rows needed by the governed population.
- Missing primary scorer outcome or exact-valid outcome.
- Missing subtype assignment and missing missing-evidence state for eligible non-exact rows.
- Missing failure taxonomy marker.
- Missing scorer semantics marker.
- Missing denominator basis needed for governed rates.

## 5. Missing-Evidence Output Requirements

Missing-evidence outputs are mandatory whenever the scorer cannot emit an approved subtype for an eligible non-exact row.

Required missing-evidence content:

- Affected family or subtype concept.
- Evidence class that is missing.
- Whether the missing evidence blocks subtype assignment, denominator construction, current-run computability, comparability, or reconciliation.
- Whether the row remains eligible, excluded, or unresolved.
- Whether the family aggregate is partial or missing as a consequence.

Required missing-evidence categories:

| Category | Expected Treatment |
|---|---|
| Missing row identity | Block audit and reconciliation for affected row. |
| Missing split membership | Block split-scoped aggregation and comparison. |
| Missing tool-expected eligibility | Block Family A eligibility and denominator construction. |
| Missing exclusion state | Block denominator construction for affected row. |
| Missing expected tool identity | Block wrong-tool-name and wrong-argument assignment when identity comparison is needed. |
| Missing expected argument evidence | Block wrong-argument assignment. |
| Missing primary scorer outcome | Block exact/non-exact partition. |
| Missing exact-valid outcome | Block exact-valid exit and non-exact denominator. |
| Missing valid required tool-call detection | Block exact-valid dependency and absence/substitution decisions. |
| Missing tool-call attempt evidence | Block attempted-tool versus absent-tool distinction. |
| Missing parse/schema evidence | Block malformed, wrapper, wrong-tool, and wrong-argument decisions when parse evidence is required. |
| Missing emitted tool identity | Block wrong-tool-name and wrong-argument decisions. |
| Missing emitted argument evidence | Block wrong-argument decision. |
| Missing answer-like substitution evidence | Block direct-answer subtype assignment. |
| Missing scalar-like substitution evidence | Block scalar subtype assignment. |
| Missing wrapper/envelope evidence | Block wrapper-drift subtype assignment. |
| Missing tool-call absence evidence | Block missing-tool-call subtype assignment. |
| Missing precedence resolution evidence | Block subtype assignment in ambiguity zones. |
| Missing approved subtype assignment | Block subtype distribution reconciliation unless explicit missing-evidence state is emitted. |
| Missing failure taxonomy marker | Block governed Family A subtype computation. |
| Missing scorer semantics marker | Block baseline comparison and migration review. |
| Missing denominator basis | Block governed rate computation. |

Noncomputability requirements:

- Missing mandatory scorer evidence must produce current-run noncomputability for the affected concept.
- Missing denominator basis must block rates even if counts exist.
- Missing taxonomy marker must block governed interpretation even if numeric subtype counts reconcile.
- Missing scorer semantics marker must block historical comparison even if current-run computation is otherwise complete.
- Missing evidence must not be repaired by `other`, parent aggregate totals, sibling subtype totals, generated text review, prompt inspection, or historical artifacts.

## 6. Taxonomy Marker Output Requirements

Taxonomy marker outputs are mandatory for governed Family A interpretation.

Required taxonomy marker content:

- Family A taxonomy identity.
- Taxonomy version or equivalent governed comparability marker.
- Approved subtype set.
- Direct-answer governed subtype identification.
- Precedence model or precedence semantics marker.
- Scorer semantics marker.
- Exact-valid semantics marker.
- Tool-expected eligibility semantics marker.
- Exclusion policy marker.
- Split and population scope references.

Required for reconciliation:

- The approved subtype set must match the subtype assignment domain.
- The non-exact eligible denominator must reconcile to approved subtype counts when evidence is complete.
- Missing-evidence states must be excluded from successful subtype distribution reconciliation and reported as noncomputability.

Required for noncomputability:

- Missing taxonomy marker blocks governed Family A computation.
- Missing approved subtype set blocks subtype distribution interpretation.
- Missing precedence marker blocks ambiguity-zone subtype assignment when precedence matters.

Required for comparability:

- Taxonomy version, scorer semantics, exact-valid semantics, population, split, eligibility, and exclusion markers must be stable or explicitly bridged.
- Historical direct-answer substitution artifacts remain reference-only or bridge-required until migration review permits comparison.
- Current-run computability does not imply comparison-allowed status.

## 7. Detector-Visible Output Requirements

The detector receives only the approved detector-facing projection after evaluator aggregation. It does not receive ownership of raw scorer evidence.

Detector-visible outputs:

- Family A active or missing status.
- Family A completeness state.
- Family A current-run computability state.
- Family A noncomputability reasons.
- Eligible tool-expected denominator when emitted.
- Non-exact tool-expected denominator when emitted.
- Exact-valid count or rate when emitted as part of the approved aggregate.
- Approved subtype counts, denominators, and rates when computable.
- Direct-answer governed subtype count, denominator, and rate when computable.
- Missing-evidence summary when Family A is partial or noncomputable.
- Failure taxonomy marker.
- Scorer semantics marker.
- Population, split, exclusion, and comparability markers.
- Comparison status: comparison-allowed, bridge-required, reference-only, or comparison-blocked.
- Reconciliation status for aggregate, split, and subtype totals.

Information intentionally outside detector ownership:

- Raw generated text.
- Prompt text.
- Row-level dataset records.
- Raw expected tool arguments.
- Raw emitted tool arguments.
- Raw parse trees or serialization details.
- Scorer-internal rationale.
- Optional rejected-candidate diagnostics.
- Historical report-layer counts as current-run facts.

Detector must not:

- Infer direct-answer substitution from answer-like text.
- Infer scalar substitution from output shape.
- Infer malformed output from invalid-json aggregate metrics.
- Infer wrapper drift from wrapper leakage metrics.
- Infer missing tool call from no-call correctness metrics.
- Infer wrong tool name or wrong argument by inspecting tool payloads.
- Reconstruct denominators from rows, historical reports, sibling totals, or aggregate rates.
- Create an `other` subtype.

## 8. Rollback And Stability Considerations

Rollback boundaries:

- Scorer evidence output planning can be revised independently before schema representation or evaluator aggregation is implemented.
- Scorer evidence emission can be rolled back independently only while evaluator aggregation and detector consumption do not depend on it.
- Once evaluator aggregation consumes Family A scorer outputs, scorer and evaluator changes must roll back together for Family A.
- Once detector consumption depends on Family A aggregate projection, scorer, evaluator, and detector-facing projection changes must roll back together.

Stability requirements before implementation:

- Mandatory scorer outputs must be approved by scorer and evaluator owners.
- Taxonomy and scorer semantics markers must be approved before governed comparison is considered.
- Missing-evidence categories must be fixture-covered before runtime use.
- Detector non-inference negatives must be fixture-covered before detector consumption.
- Direct-answer subtype output must be stable enough to support the retained governed concept without no-call, invalid-json, wrapper-leakage, or historical-count proxies.

Rollback behavior for unstable evidence:

- If subtype evidence proves unstable before detector consumption, Family A subtype emission should remain disabled or marked noncomputable rather than partially governed.
- If one subtype is unstable, dependent subtype distribution and direct-answer governed interpretation must remain noncomputable unless the approved contract still reconciles without that subtype.
- If taxonomy marker emission is unstable, numeric subtype outputs may be retained for audit only but must not be treated as governed-computable.
- If scorer semantics change without an approved bridge, historical comparison must remain blocked.

Governance boundaries:

- Rollback must not relax existing governance rules.
- Rollback must not convert missing evidence into passing state.
- Rollback must not hide active computable governance findings outside Family A.
- Rollback must preserve the distinction between current-run noncomputability and baseline comparison blockage.

## Required Analysis Summary

Mandatory outputs:

- Eligibility, split, exclusion, expected-behavior, scorer outcome, exact-valid, non-exact status, tool-attempt, parse/schema, subtype evidence, subtype assignment or missing-evidence state, missing-evidence reason, taxonomy marker, scorer semantics marker, and comparability references.

Optional outputs:

- Subtype rationale, rejected-candidate diagnostics, parse failure class, wrapper failure class, argument mismatch class, and other review-only evidence details.

Outputs required for reconciliation:

- Row identity reference, split membership, eligibility, exclusion state, exact-valid outcome, non-exact status, approved subtype assignment, missing-evidence state, denominator basis, and taxonomy marker.

Outputs required for noncomputability:

- Missing-evidence state, missing-evidence reason, affected concept, completeness impact, current-run computability impact, missing denominator basis, missing taxonomy marker, and missing scorer semantics marker.

Outputs required for comparability:

- Failure taxonomy marker, scorer semantics marker, exact-valid semantics marker, population marker, split marker, eligibility marker, exclusion-policy marker, and migration status emitted by later migration review.

## Remaining Blockers Before Scorer Implementation Planning Completion

- Scorer-owner approval of the mandatory output inventory.
- Evaluator-owner approval that the handoff content is sufficient for Family A aggregation and reconciliation.
- Governance-owner approval of taxonomy marker and scorer semantics marker requirements.
- Detector-owner acceptance of the detector-visible projection and non-inference boundaries.
- Validation-owner approval that WP8 fixtures cover every mandatory output, missing-evidence category, and detector non-inference negative.
- Schema-owner review of how these conceptual outputs will later be represented without collapsing current-run computability and baseline comparability.
- Explicit approval that no generic `other` subtype will be introduced in scorer implementation without a separate contract and fixture coverage.
