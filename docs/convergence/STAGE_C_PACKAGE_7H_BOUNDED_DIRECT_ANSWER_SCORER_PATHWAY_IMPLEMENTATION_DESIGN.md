# Stage C Package 7H Bounded Direct-Answer Scorer-Pathway Implementation Design

## Scope

This package defines the first bounded implementation design for:

- `direct_answer_substitution_count`

This is a design package.

It does not:

1. perform implementation;
2. authorize implementation execution;
3. authorize migration;
4. modify scorer behavior;
5. modify evaluator behavior;
6. modify detector behavior;
7. modify threshold behavior;
8. alter migration flags;
9. reopen readiness;
10. reopen gate.

## Design Boundary

Current direct-answer surface state remains unchanged:

1. reconciliation: `requires_future_migration`
2. readiness: `migration-blocked`
3. gate: `gate-blocked`

Current governance posture remains unchanged:

1. `authoritative_detector_output=false`
2. `detector_migration_enabled=false`
3. `threshold_profile_migration_enabled=false`

Implementation authorization inherited from Package `7G`:

1. future bounded scorer-pathway implementation is conditionally authorized;
2. migration remains unauthorized;
3. detector and threshold independence remain mandatory.

This package uses that authorization to define a prospective implementation design only.

## Implementation Target Design

### Exact Bounded Implementation Target

The implementation target is:

- bounded realization of scorer-owned direct-answer and scalar substitution evidence production inside the current authoritative Family A scorer-pathway handoff

More precisely, the target is limited to the runtime handoff around:

1. `_classify(...)`
2. `_stage_c_family_a_declared_subtype(...)`
3. `_build_stage_c_family_a_record(...)`
4. `stage_c1.emit_family_a_scorer_evidence(...)` as the unchanged contract-enforcing receiver

The target is not:

1. generalized scorer redesign;
2. detector redesign;
3. threshold redesign;
4. evaluator redesign outside the current scorer carrier surfaces;
5. migration design;
6. taxonomy redesign;
7. metadata redesign.

### Runtime Surfaces Involved

Runtime surfaces inside scope:

1. `_extract_json_payload(...)`
   - parseability framing for the candidate output
2. `_validate_schema(...)`
   - schema validity framing for tool-call structure
3. `_looks_like_tool_intent(...)`
   - tool-attempt framing
4. `_classify(...)`
   - current primary outcome production and the natural insertion point for scorer-owned substitution-evidence production
5. `_stage_c_family_a_declared_subtype(...)`
   - current subtype-or-missing-evidence mapping surface
6. `_build_stage_c_family_a_record(...)`
   - authoritative handoff into Stage C1 contract emission

### Ownership Boundaries

The design preserves the following ownership boundaries:

1. scorer ownership
   - answer-like substitution evidence
   - scalar-like substitution evidence
   - precedence evidence between direct-answer, scalar, malformed output, and missing tool call
2. evaluator ownership
   - runtime carriage and aggregation of scorer-owned outputs only
3. dataset metadata ownership
   - row identity, split, tool-expected eligibility, expected tool facts
4. detector ownership
   - downstream consumption only, unchanged
5. threshold ownership
   - downstream consumption only, unchanged

### Contract Boundaries

The design stays inside current approved doctrine:

1. `direct-answer substitution` remains an approved Family A subtype
2. `scalar substitution` remains an approved Family A subtype
3. explicit missing-evidence remains an approved Family A outcome
4. non-inference doctrine remains binding
5. ambiguity preservation remains binding

The design does not require:

1. new subtype creation
2. new doctrine
3. relaxed missing-evidence handling
4. detector-visible proxy classification

### Explicit Exclusions

The design explicitly excludes:

1. detector-side generated-text classification
2. evaluator-side reconstruction from generated text outside scorer-owned evidence production
3. promotion of legacy `_failure_subtype(...)` into authoritative scorer evidence
4. any change to `summary.json`
5. any change to `failure_profile`
6. any change to detector inputs or detector logic
7. any change to threshold profiles or threshold logic
8. any migration or cutover work

## Proposed Runtime Flow Design

### Conceptual Flow

The bounded conceptual runtime flow is:

1. parse and schema framing remains as today
2. exact-valid and existing tool-attempt failure classification remains as today
3. for eligible non-exact tool-expected rows that do not already resolve to a decisive approved subtype from existing tool-attempt evidence, a scorer-owned substitution-evidence stage produces structured direct-answer/scalar/precedence evidence
4. subtype declaration consumes:
   - existing protocol/tool-attempt evidence
   - new scorer-owned substitution evidence when present
5. Stage C1 receives either:
   - an approved subtype assignment; or
   - explicit missing-evidence state

### Evidence Production Points

Conceptual evidence production points:

1. parse/schema evidence
   - existing
2. tool-attempt evidence
   - existing
3. answer-like substitution evidence
   - new scorer-owned conceptual evidence point
4. scalar-like substitution evidence
   - new scorer-owned conceptual evidence point
5. precedence evidence
   - new scorer-owned conceptual evidence point used only to resolve direct-answer versus scalar versus malformed versus missing-tool-call boundaries when possible

### Evidence Handoff Points

Conceptual handoff points:

1. `_classify(...)` hands forward current protocol/tool-attempt facts plus scorer-owned substitution evidence when available
2. `_stage_c_family_a_declared_subtype(...)` consumes those facts to produce:
   - `direct-answer substitution`
   - `scalar substitution`
   - existing approved sibling subtype
   - or explicit missing-evidence
3. `_build_stage_c_family_a_record(...)` packages the declared subtype or missing-evidence result without downstream reinterpretation
4. `stage_c1.emit_family_a_scorer_evidence(...)` enforces contract compliance

### Evidence Consumption Points

Conceptual evidence consumption points inside scope:

1. subtype declaration logic
2. authoritative Family A record construction
3. Stage C1 contract emission

Explicitly out-of-scope evidence consumers:

1. detector metric resolution
2. threshold rule evaluation
3. migration or cutover consumers

### Missing-Evidence Handling

Missing-evidence handling remains preservation-first:

1. if scorer-owned substitution evidence is insufficient, missing-evidence remains the outcome
2. if precedence between neighboring subtypes cannot be resolved, missing-evidence remains the outcome
3. missing-evidence is preferred over speculative direct-answer or scalar assignment

The design therefore does not depend on count movement.

It remains valid even if a future bounded implementation produces:

1. zero direct-answer subtype assignments on the frozen corpus
2. zero scalar subtype assignments on the frozen corpus

## Preservation Design Review

### Governance-Preserving Missingness

The design preserves governance-preserving missingness by requiring that scorer-owned evidence be explicit before subtype assignment occurs.

Preservation consequences:

1. rows without sufficient substitution evidence remain missing
2. missingness remains a valid success-path outcome for implementation
3. no future implementation success criterion depends on eliminating missingness

### Non-Inference Doctrine

The design preserves non-inference doctrine because:

1. detector remains out of scope
2. threshold consumers remain out of scope
3. downstream packages continue consuming emitted facts only
4. authoritative subtype assignment remains inside the scorer-owned pathway rather than detector-side prose interpretation

### Ambiguous-Row Preservation

The design preserves the `3` ambiguous rows by making ambiguity a stable allowed outcome.

Preservation requirement:

1. mixed-output rows remain missing unless scorer-owned evidence resolves them under existing doctrine
2. no convenience collapse into `direct-answer substitution`
3. no convenience collapse into `scalar substitution`

### Detector Independence

Detector independence is preserved because:

1. no detector code path is touched
2. no detector input contract is changed
3. no detector proxy or heuristic is introduced

### Threshold Independence

Threshold independence is preserved because:

1. no threshold profile path changes
2. no threshold semantics changes
3. no threshold dependency changes

### The `131` Structurally Incapable Rows

The design explicitly preserves the `131` governance-preserving structurally incapable rows.

Preservation expectation:

1. implementation must not target them for forced subtype conversion
2. implementation must tolerate their continued missingness as valid
3. any changed treatment would require scorer-owned evidence under current doctrine, not design convenience

### The `3` Ambiguous Rows

The design explicitly preserves the `3` ambiguous rows.

Preservation expectation:

1. they remain ambiguous by default
2. they are not used to justify broader subtype-collapse behavior
3. their continued ambiguity is consistent with design success

## Validation Design

### Contract Validation

Future implementation validation should include:

1. approved subtype-set validation
2. prohibition of `other`
3. explicit missing-evidence validation
4. contract-marker validation
5. unchanged detector-visible Family A record shape validation

### Runtime Validation

Future implementation validation should include:

1. targeted runtime execution through the live canonical evaluator
2. row-level inspection of affected Family A records
3. verification that downstream detector and threshold artifacts remain unchanged

### Frozen-Manifest Validation

Future implementation validation should include:

1. frozen manifest execution on the current canonical row set
2. validation that row identity remains unchanged
3. validation that the `131` structurally incapable row cohort remains preserved unless scorer-owned evidence justifies otherwise
4. validation that the `3` ambiguous row cohort remains preserved unless scorer-owned evidence justifies otherwise

### Repeated-Run Stability Validation

Future implementation validation should include:

1. repeated full canonical runs on the same frozen manifest
2. repeated row-level scorer-evidence comparisons
3. repeated validation that unchanged preserved cohorts remain unchanged
4. repeated validation that no downstream detector or threshold behavior changes appear

### Preservation Validation

Future implementation validation should explicitly validate:

1. no detector contamination
2. no threshold contamination
3. no migration-flag changes
4. no readiness or gate mutation
5. no collapse of missingness into fallback subtype counts

### Validation Output Expectation

The accompanying future validation package should be able to distinguish:

1. valid bounded-pathway realization
2. preserved-zero-change behavior
3. constrained positive subtype movement when scorer-owned evidence justifies it
4. boundary-violating behavior that requires halt or rollback

## Rollback Design

### Artifact Preservation

A future implementation package should preserve, at minimum:

1. pre-implementation authoritative Stage C artifacts
2. pre-implementation legacy artifacts
3. row-level Family A scorer-evidence snapshots
4. affected-row preservation manifests for the `131` and `3` protected cohorts
5. post-implementation authoritative artifacts
6. separable failed-attempt evidence if rollback is triggered

### Failure Isolation

Rollback design assumes failure isolation at the scorer-pathway boundary.

That means:

1. rollback should be able to restore pre-implementation authoritative behavior without touching detector or threshold systems
2. rollback should isolate scorer-pathway failures from downstream governance consumers
3. rollback should preserve row-level audit evidence for any changed Family A records

### Rollback Triggers

Conceptual rollback triggers include:

1. contract validation failure
2. detector or threshold behavior drift
3. violation of preserved treatment for the `131` structurally incapable rows
4. violation of preserved treatment for the `3` ambiguous rows
5. doctrine boundary violation
6. scope-expansion into detector, threshold, or migration surfaces

### Audit Requirements

Audit preservation should include:

1. pre/post artifact hashes
2. pre/post row-level scorer-evidence diffs
3. preserved missing-evidence reason diffs
4. explicit reviewer record explaining why rollback was or was not invoked

## Hazard Mitigation Design

### Scorer Redesign Creep

Mitigation expectation:

1. keep implementation limited to the scorer-pathway handoff surfaces
2. forbid unrelated scorer-family or taxonomy changes
3. require explicit justification for any scope extension

### Detector Contamination

Mitigation expectation:

1. detector stays untouched
2. detector outputs are preserved and revalidated
3. any implementation dependency on detector heuristics is a stop condition

### Migration Creep

Mitigation expectation:

1. preserve all migration-disabled flags
2. forbid any source-binding or consumer changes
3. keep all migration questions explicitly out of scope

### Scope Expansion

Mitigation expectation:

1. keep surface limited to `direct_answer_substitution_count`
2. keep runtime limited to the authorized scorer-pathway handoff
3. keep explicit exclusions active throughout implementation and validation

### Doctrine Expansion Pressure

Mitigation expectation:

1. stay within existing Family A doctrine
2. stay within existing missing-evidence doctrine
3. treat any need for new doctrine as a hard stop

### Ambiguous-Row Collapse Pressure

Mitigation expectation:

1. ambiguity preservation remains a design invariant
2. row collapse is disallowed unless scorer-owned evidence supports it under current doctrine
3. preserved-cohort validation makes collapse visible immediately

## Design Success Criteria

A future implementation would need to demonstrate, at a high level:

1. bounded runtime realization inside the authorized scorer-pathway scope
2. contract-compliant Family A emission
3. preserved missing-evidence handling
4. preserved ambiguity handling
5. preserved treatment of the `131` structurally incapable rows unless scorer-owned evidence justifies otherwise
6. preserved treatment of the `3` ambiguous rows unless scorer-owned evidence justifies otherwise
7. unchanged detector and threshold behavior
8. unchanged migration-disabled posture

Success does not require:

1. nonzero direct-answer counts
2. nonzero scalar counts
3. readiness reopening
4. gate reopening
5. migration authorization

## Design Failure Criteria

The design implies that future implementation should not proceed, should be halted, or should trigger rollback if:

1. detector or evaluator inference becomes necessary
2. doctrine expansion becomes necessary
3. preserved missingness cannot be maintained
4. the `131` structurally incapable rows cannot remain protected
5. the `3` ambiguous rows cannot remain protected
6. implementation scope expands toward generalized scorer redesign
7. downstream detector, threshold, or migration surfaces become implicated
8. ownership boundaries cannot be preserved in runtime behavior

Any such finding indicates that the blocker may remain effectively terminal under current governance.

## Implementation Readiness Assessment

Implementation readiness consideration:

- justified

Why:

1. the target is now bounded at design level, not only at authorization level
2. runtime surfaces, ownership boundaries, contract boundaries, and exclusions are explicit
3. preservation expectations are explicit for both the `131` structurally incapable rows and the `3` ambiguous rows
4. validation and rollback expectations are explicit enough to govern a bounded implementation slice

This is not implementation authorization.

It is a readiness judgment that no additional design package appears necessary before a later bounded implementation package is considered.

## Regimen Impact Assessment

This design package contributes:

1. the first actual blocker-oriented branch implementation-design record
2. another post-blocker transition maturity step after:
   - investigation
   - planning authorization
   - bounded planning
   - implementation authorization
3. stronger reusable-regimen evidence that the blocker-oriented branch can progress from blocked-state assessment into bounded implementation design while preserving governance boundaries

This package does not contribute:

1. implementation execution
2. migration authorization
3. readiness or gate state change
4. a second blocker-oriented surface family

## Boundary Confirmation

This design package does not:

1. perform implementation
2. modify scorer behavior
3. modify evaluator behavior
4. modify detector behavior
5. modify threshold behavior
6. alter migration flags
7. reopen readiness
8. reopen gate
9. authorize implementation
10. authorize migration
