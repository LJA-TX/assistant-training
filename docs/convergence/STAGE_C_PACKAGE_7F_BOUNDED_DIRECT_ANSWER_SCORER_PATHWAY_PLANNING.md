# Stage C Package 7F Bounded Direct-Answer Scorer-Pathway Planning

## Scope

This package defines the first bounded scorer-pathway planning model for:

- `direct_answer_substitution_count`

This is a planning package.

It does not:

1. perform implementation;
2. authorize implementation;
3. authorize migration;
4. modify scorer behavior;
5. modify evaluator behavior;
6. modify detector behavior;
7. modify threshold behavior;
8. alter migration flags;
9. reopen readiness;
10. reopen gate.

## Planning Boundary

Current direct-answer surface state remains unchanged:

1. reconciliation: `requires_future_migration`
2. readiness: `migration-blocked`
3. gate: `gate-blocked`

Current governance posture remains unchanged:

1. `authoritative_detector_output=false`
2. `detector_migration_enabled=false`
3. `threshold_profile_migration_enabled=false`

Planning authorization inherited from Package `7E`:

1. future bounded scorer-pathway planning is conditionally authorized;
2. implementation remains unauthorized;
3. migration remains unauthorized.

This package uses that authorization to define the planning target and boundaries only.

## Planning Target Definition

### Precise Planning Target

The planning target is:

- a bounded scorer-pathway target for the direct-answer and scalar subtype reachability gap inside the current authoritative Family A pathway for `direct_answer_substitution_count`

More precisely, the target is limited to planning around the current handoff between:

1. `_classify(...)`
2. `_stage_c_family_a_declared_subtype(...)`
3. `stage_c1.emit_family_a_scorer_evidence(...)`

The planning target is not:

1. generalized scorer redesign;
2. detector redesign;
3. threshold redesign;
4. migration planning;
5. corpus or metadata redesign;
6. Family A taxonomy redesign.

### Ownership Scope

Planning ownership scope is limited to:

1. scorer-owned direct-answer substitution evidence production
2. scorer-owned scalar substitution evidence production
3. evaluator runtime carrier surfaces that currently translate scorer facts into Family A subtype records

Out of scope ownership domains:

1. dataset metadata ownership
2. detector ownership
3. threshold ownership
4. migration-governance ownership

### Runtime Scope

Runtime scope is limited to the live authoritative path that currently handles non-exact tool-expected rows:

1. parse and schema extraction surfaces
2. tool-attempt and tool-identity failure classification surfaces
3. subtype declaration handoff
4. Family A scorer-evidence emission handoff

Runtime scope explicitly excludes:

1. summary.json legacy metric generation
2. detector metric resolution
3. threshold rule resolution
4. row-fact identity generation
5. non-Family A governance families

### Contract Scope

Contract scope is limited to already-approved doctrine:

1. `direct-answer substitution`
2. `scalar substitution`
3. existing missing-evidence behavior
4. existing non-inference doctrine
5. existing ambiguity handling doctrine

Contract scope explicitly excludes:

1. new subtype creation
2. doctrine expansion
3. alternate ownership models
4. replacement metric creation

### Explicit Exclusions

The following are explicitly excluded from the planning target:

1. any design that requires detector-side classification
2. any design that requires evaluator-side reconstruction from generated text
3. any design that assumes universal subtype assignment
4. any design that collapses the `131` governance-preserving structurally incapable rows
5. any design that collapses the `3` ambiguous rows
6. any design that changes detector or threshold consumers
7. any design that implies migration or implementation authorization

## Pathway Surface Inventory

### Owned Pathway Components

Owned scorer-pathway components relevant to future implementation planning:

1. `_classify(...)`
   - current primary-outcome producer for exact-valid and non-exact tool-call failure classes
2. `_stage_c_family_a_declared_subtype(...)`
   - current authoritative mapping from runtime failure classes to approved Family A subtype or missing-evidence state
3. `_build_stage_c_family_a_record(...)`
   - current handoff builder that packages subtype or missing-evidence state for Stage C1 contract emission
4. `stage_c1.emit_family_a_scorer_evidence(...)`
   - current contract-enforcing output surface for authoritative Family A row evidence

### Handoff Locations

Relevant handoff locations:

1. parse/schema and tool-attempt facts are produced before subtype declaration
2. subtype declaration currently occurs without any emitted answer-like or scalar-like substitution evidence class
3. Stage C1 emission currently accepts approved subtype strings or explicit missing-evidence state
4. downstream governance consumers read the emitted Family A artifact rather than generating subtype facts themselves

### Evidence Production Locations

Current evidence production locations:

1. `_extract_json_payload(...)`
   - parseability framing
2. `_validate_schema(...)`
   - schema validity framing
3. `_looks_like_tool_intent(...)`
   - tool-attempt framing
4. `_classify(...)`
   - current primary-outcome and secondary-failure production
5. `_stage_c_family_a_declared_subtype(...)`
   - approved-subtype-or-missing-evidence production

Relevant current gap:

1. answer-like substitution evidence is not currently produced as a scorer-owned path outcome
2. scalar-like substitution evidence is not currently produced as a scorer-owned path outcome
3. precedence evidence between direct-answer, scalar, malformed output, and missing tool call is not currently surfaced in the authoritative path

### Evidence Consumption Locations

Current evidence consumption locations:

1. `_build_stage_c_family_a_record(...)`
2. `stage_c1.emit_family_a_scorer_evidence(...)`
3. `stage_c_family_a_scorer_evidence_artifact.json`
4. passive governance, reconciliation, and readiness packages that consume the authoritative artifact

Explicitly excluded evidence consumption locations:

1. detector metric resolution
2. threshold resolution
3. migration or cutover consumers

## Preservation-Oriented Planning Model

### Planning Principle

Future work must be planning-preserving before it is ever implementation-oriented.

That means future planning must treat:

1. missingness preservation
2. ambiguity preservation
3. non-inference preservation
4. downstream-consumer independence

as primary constraints, not secondary clean-up tasks.

### Missing-Evidence Preservation Model

Future planning must assume that missing evidence remains a legitimate and possibly permanent outcome for many rows.

Planning expectations:

1. no future target may require universal subtype assignment
2. explicit missing-evidence state must remain available
3. absence of subtype evidence must remain preferable to detector or evaluator guesswork

### Ambiguous-Row Preservation Model

Future planning must preserve the `3` ambiguous rows as ambiguous unless later scorer-owned evidence justifies a narrower outcome.

Planning expectations:

1. ambiguity is preserved by default
2. no planning target may depend on collapsing mixed-output rows into direct-answer or scalar categories
3. ambiguity remains a valid blocker outcome under current doctrine

### Structurally Incapable Row Preservation Model

Future planning must preserve the `131` structurally incapable rows as governance-preserving missingness unless later scorer-owned evidence justifies otherwise.

Planning expectations:

1. these rows are not assumed to become positive subtype assignments
2. these rows are not treated as an optimization target for conversion
3. their continued missingness is consistent with doctrine rather than evidence of planning failure

### Non-Inference Preservation Model

Future planning must preserve:

1. no detector-side generated-text classification
2. no evaluator-side generated-text reconstruction
3. no default promotion of legacy `_failure_subtype(...)` heuristics into authoritative scorer facts

### Detector And Threshold Independence Model

Future planning must preserve:

1. detector independence
2. threshold independence
3. migration-disabled posture

Planning expectations:

1. no detector input contract changes are assumed
2. no threshold profile changes are assumed
3. no migration-path coupling is assumed

## Success-State Planning Definition

Successful future implementation, if it were ever later authorized, would need to demonstrate at a conceptual level:

1. ownership preservation
   - scorer-owned subtype evidence remains scorer-owned
2. bounded evidence production
   - only the direct-answer/scalar pathway gap is addressed
3. contract compliance
   - approved subtypes and missing-evidence states remain within current Family A doctrine
4. preservation compatibility
   - the `131` structurally incapable rows and `3` ambiguous rows remain protected unless scorer-owned evidence justifies otherwise
5. non-inference preservation
   - no detector or evaluator reconstruction is required
6. bounded runtime localization
   - changes remain local to the scorer-pathway handoff rather than spreading across unrelated runtime surfaces

Planning success does not mean:

1. direct-answer count becomes nonzero
2. scalar count becomes nonzero
3. migration becomes authorized
4. readiness or gate state changes

## Failure-State Planning Definition

Future implementation effort would be conceptually invalidated or terminated if planning later shows:

1. detector contamination is required
2. evaluator reconstruction is required
3. doctrine expansion is required before the pathway can even be bounded
4. the `131` structurally incapable rows cannot remain missing
5. the `3` ambiguous rows cannot remain ambiguous
6. the planning target cannot be localized more narrowly than generalized scorer redesign
7. the pathway cannot remain isolated from detector, threshold, or migration work

Any of those findings would mean the current bounded-planning model was too optimistic and the blocker would remain effectively terminal under current governance.

## Hazard Containment Plan

### Scorer Redesign Creep

Containment expectation:

1. keep future work tied to the specific handoff surfaces already localized by Package `7D`
2. exclude unrelated scorer families and unrelated failure taxonomies
3. require explicit justification for any scope expansion

### Detector Contamination

Containment expectation:

1. keep detector systems outside the planning target
2. forbid any planning assumption that detector can resolve prose-versus-scalar evidence
3. require all subtype evidence to remain scorer-owned

### Migration Creep

Containment expectation:

1. preserve all migration-disabled flags
2. forbid planning outputs from implying cutover or source-binding changes
3. keep detector and threshold consumers out of scope

### Planning Scope Expansion

Containment expectation:

1. keep the surface limited to `direct_answer_substitution_count`
2. keep the runtime scope limited to the current scorer-pathway handoff
3. keep exclusions explicit throughout any future planning work

### Ambiguous-Row Collapse Pressure

Containment expectation:

1. treat ambiguity preservation as a planning invariant
2. require scorer-owned evidence before any narrower interpretation is even considered
3. forbid convenience collapse of mixed-output rows into direct-answer or scalar buckets

## Planning Exit Criteria

### Conditions Under Which Planning Should Stop

Planning should stop if:

1. the target expands beyond the bounded scorer-pathway handoff
2. future work requires detector or evaluator inference
3. future work requires doctrine expansion before bounded pathway definition is possible
4. future work depends on collapsing the `131` structurally incapable rows or `3` ambiguous rows
5. future work cannot remain separated from detector, threshold, or migration work

### Conditions Under Which Planning Should Continue

Planning should continue if:

1. the target remains localized to the scorer-pathway handoff
2. ownership remains scorer-centered
3. preservation boundaries remain intact
4. contract interaction remains inside current approved doctrine
5. explicit exclusions remain sufficient to prevent redesign drift

### Conditions Under Which Future Implementation-Authorization Consideration Could Become Meaningful

Future implementation-authorization consideration could become meaningful only if planning later shows:

1. a bounded target remains viable without doctrine change
2. the target remains localized without redesign creep
3. missingness preservation remains intact
4. ambiguous-row preservation remains intact
5. non-inference doctrine remains intact
6. detector and threshold independence remain intact

This package does not authorize implementation.

It defines only what would need to be true before implementation-authorization consideration becomes meaningful.

## Planning Determination

For `direct_answer_substitution_count`, the repository now has a first bounded scorer-pathway planning model that:

1. is narrower than generalized scorer redesign
2. is bounded by existing doctrine and contract
3. is explicit about preserved missingness and ambiguity
4. is explicit about downstream independence
5. is explicit about stop conditions and scope controls

This package does not claim that future implementation should occur.

It documents what future bounded planning is expected to preserve and what would invalidate that planning path.

## Regimen Impact Assessment

Completion of this planning package contributes:

1. the first actual blocker-oriented branch planning record
2. a new post-blocker transition maturity step after:
   - investigation feasibility
   - investigation authorization
   - investigation execution
   - planning authorization
3. stronger reusable-regimen evidence that the blocker-oriented branch can progress from blocked-state characterization into bounded forward planning without violating governance boundaries

This does not yet contribute:

1. a second blocker-oriented surface family
2. implementation authorization
3. migration authorization
4. any reopened surface state

## Boundary Confirmation

This planning package does not:

1. modify scorer behavior
2. modify evaluator behavior
3. modify detector behavior
4. modify threshold behavior
5. alter migration flags
6. create implementation design
7. authorize implementation
8. authorize migration
9. reopen readiness
10. reopen gate
