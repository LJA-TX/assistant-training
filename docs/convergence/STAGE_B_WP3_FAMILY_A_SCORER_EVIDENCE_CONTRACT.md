# Stage B WP3 Family A Scorer Evidence Contract

## Scope

This document defines the scorer evidence contract required to support the approved Family A failure-subtype taxonomy.

This is documentation-only implementation planning. It does not implement scorer logic, implement schemas, implement validators, implement fixtures, modify code, modify detectors, modify evaluators, modify scorers, modify thresholds, modify governance rules, modify mappings, or modify manifests.

Reference inputs:

- `STAGE_B_WP8C_FAMILY_A_SUBTYPE_BOUNDARY_REVIEW.md`
- `STAGE_B_WP8C_SCENARIO_TO_SUBTYPE_MAPPING.md`

Family A purpose:

- Preserve direct-answer substitution as a governed subtype.
- Require deterministic scorer evidence for every non-exact tool-expected subtype assignment.
- Keep detector ownership limited to emitted facts and emitted states.
- Represent missing or ambiguous evidence as noncomputability, not as a fallback subtype.

## Contract Principles

- Family A applies only to eligible tool-expected rows.
- Exact-valid tool-expected rows exit subtype assignment.
- Excluded rows exit governed subtype assignment and do not enter governed denominators.
- Every eligible non-exact tool-expected row must receive exactly one approved subtype, or an explicit missing-evidence state.
- A generic `other` subtype is not approved.
- Scorer evidence must be sufficient to distinguish neighboring subtypes or produce missing-evidence state.
- Detector must not reconstruct scorer evidence from generated text, prompt text, row records, baseline artifacts, or aggregate metrics.
- Taxonomy marker and scorer semantics marker are required for governed comparability.

## Shared Evidence Inventory

The following evidence concepts are shared across Family A subtype decisions.

| Evidence Concept | Owner | Required For | Notes |
|---|---|---|---|
| row identity | Dataset metadata | all Family A evidence | Required for audit and baseline review. |
| split membership | Dataset metadata | all Family A evidence | Required for split-scoped summaries. |
| tool-expected eligibility | Dataset metadata | all Family A evidence | Required before scorer subtype assignment is governed. |
| expected tool identity | Dataset metadata | wrong tool name, wrong argument, exact-valid dependency | Required before comparing invoked tool identity. |
| expected argument evidence | Dataset metadata or scorer input contract | exact-valid dependency, wrong argument | Required before argument comparison can be governed. |
| exclusion state | Dataset metadata or approved evaluator pre-filter | denominator and subtype eligibility | Excluded rows do not enter subtype denominator. |
| primary scorer outcome | Scorer | exact/non-exact partition and subtype assignment | Required before Family A aggregation. |
| exact-valid outcome | Scorer | exact-valid exit and non-exact denominator | Exact-valid rows are not subtyped. |
| non-exact tool-expected status | Scorer derived from scorer outcome plus metadata | all subtypes | Required before subtype assignment. |
| valid required tool-call detection | Scorer | direct-answer, scalar, missing tool call, exact-valid dependency | Establishes whether a satisfying tool call exists. |
| emitted tool-call attempt detection | Scorer | wrapper/envelope drift, wrong tool name, wrong argument | Establishes whether model attempted tool-call form. |
| emitted tool identity evidence | Scorer | wrong tool name, wrong argument | Required to distinguish wrong tool name from wrong argument. |
| emitted argument evidence | Scorer | wrong argument | Required for argument comparison. |
| parse/schema evidence | Scorer | malformed output, wrapper/envelope drift, wrong tool name, wrong argument | Required to distinguish format failures from parseable tool attempts. |
| wrapper/envelope evidence | Scorer | wrapper/envelope drift | Required to identify near-tool protocol failure. |
| answer-like substitution evidence | Scorer | direct-answer substitution | Required to distinguish prose/direct answer from absence. |
| scalar-like substitution evidence | Scorer | scalar substitution | Required to distinguish bare-value substitution from prose/direct answer. |
| tool-call absence evidence | Scorer | missing tool call | Required to establish absence without using aggregate no-call proxies. |
| subtype assignment | Scorer | all non-exact rows | Must be one approved subtype when evidence is complete. |
| missing-evidence reason | Scorer | noncomputability | Required when subtype cannot be assigned. |
| failure taxonomy marker | Scorer | all governed Family A outputs | Required for governed subtype interpretation. |
| scorer semantics marker | Scorer | comparability | Required for baseline comparison review. |

## Subtype-Specific Evidence Inventory

| Subtype | Required Distinguishing Evidence |
|---|---|
| direct-answer substitution | Answer-like substitution evidence replacing required tool procedure. |
| scalar substitution | Bare scalar-like replacement evidence replacing required tool procedure. |
| malformed output | Parse/schema evidence showing invalid or unreadable tool-call structure. |
| wrapper/envelope drift | Recognizable tool-call-like attempt with wrapper/envelope protocol failure. |
| missing tool call | Clear absence of valid required tool call and absence of stronger substitution evidence. |
| wrong tool name | Parseable tool-call attempt with tool identity different from expected tool. |
| wrong argument | Parseable expected-tool call with argument comparison failure. |

## Exact-Valid Dependency Contract

Purpose:

- Establish that exact-valid scoring precedes Family A failure-subtype assignment.

Required evidence:

- Tool-expected eligibility.
- Expected tool identity and expected argument evidence.
- Response-level exact-valid outcome.
- Primary scorer outcome.
- Scorer semantics marker.

Expected behavior:

- Exact-valid tool-expected rows do not receive failure subtype assignment.
- Non-exact tool-expected rows proceed to subtype assignment.
- Missing exact-valid evidence blocks exact/non-exact partition and makes affected Family A emission noncomputable.

Evidence that must never be reconstructed:

- Exact-valid outcome must not be inferred by detector from generated text, JSON validity, tool name strings, or row-level artifacts.
- Exact-valid outcome must not be inferred from Family A subtype counts.

Reconciliation dependencies:

- Eligible tool-expected denominator must equal exact-valid eligible rows plus non-exact eligible rows.
- Non-exact denominator is the denominator for subtype distribution.

## Tool-Expected Eligibility Contract

Purpose:

- Establish which rows are eligible for Family A subtype assignment.

Required evidence:

- Row identity.
- Split membership.
- Tool-expected eligibility.
- Expected tool behavior sufficient for scorer comparison.
- Exclusion state.

Expected behavior:

- Rows not marked tool-expected are outside Family A.
- Excluded rows are reported in exclusion summary and excluded from governed denominators.
- Missing tool-expected eligibility blocks Family A aggregation for affected rows.

Evidence that must never be reconstructed:

- Detector must not infer tool-expected eligibility from prompt text, generated text, expected-output shape, or historical artifact paths.

Reconciliation dependencies:

- Eligible tool-expected denominator depends on declared tool-expected eligibility and exclusions.
- Split-scoped denominators depend on declared split membership.

## Subtype Evidence Contracts

### Direct-Answer Substitution

Required scorer evidence:

- Row is tool-expected and not excluded.
- Exact-valid outcome is false.
- No valid required tool invocation satisfies expected tool behavior.
- Generated response is classified by the scorer as answer-like prose, direct result prose, or answer text replacing required tool invocation.
- The output is not classified as scalar-only replacement.
- The output is not primarily malformed or a near-tool wrapper/envelope attempt.
- Failure taxonomy marker is present.

Optional scorer evidence:

- Confidence or rationale for answer-like substitution classification.
- Reference to competing subtype candidates that were rejected by precedence.
- Indicator that answer-like content includes explanatory prose rather than bare scalar content.

Evidence ownership:

- Scorer owns answer-like substitution classification.
- Dataset metadata owns tool-expected eligibility and expected tool behavior.
- Evaluator owns aggregation of emitted subtype facts.
- Detector owns policy consumption only.

Evidence dependencies:

- Exact-valid dependency contract.
- Tool-expected eligibility contract.
- Valid required tool-call detection.
- Answer-like substitution evidence.
- Precedence distinction from scalar substitution, malformed output, wrapper/envelope drift, and missing tool call.

Missing-evidence behavior:

- If scorer cannot distinguish answer-like substitution from scalar substitution, malformed output, wrapper/envelope drift, or missing tool call, subtype evidence is missing.
- Missing answer-like evidence blocks direct-answer subtype assignment.

Expected noncomputability behavior:

- Affected row is noncomputable for subtype distribution until an approved subtype or missing-evidence state is emitted.
- Direct-answer governed subtype is noncomputable when direct-answer subtype summary or required denominators are missing.

Detector-visible outputs required:

- Direct-answer subtype count.
- Eligible tool-expected denominator.
- Non-exact tool-expected denominator.
- Direct-answer rates when denominator bases exist.
- Failure taxonomy marker.
- Completeness and current-run computability state.
- Missing-evidence reason when applicable.

Reconciliation dependencies:

- Direct-answer count contributes exactly one subtype count to non-exact eligible denominator.
- Direct-answer rates reconcile against both denominator bases when emitted.
- Direct-answer subtype cannot be reconstructed from no-call correctness, invalid-json, wrapper leakage, or generated text.

### Scalar Substitution

Required scorer evidence:

- Row is tool-expected and not excluded.
- Exact-valid outcome is false.
- No valid required tool invocation satisfies expected tool behavior.
- Generated response is classified by the scorer as bare scalar-like value, identifier, minimal value, or minimal result replacing required tool invocation.
- The output is not classified as answer-like prose.
- The output is not a parseable expected-tool call with wrong arguments.
- Failure taxonomy marker is present.

Optional scorer evidence:

- Rationale distinguishing scalar-like output from prose/direct answer.
- Indicator that the scalar appears outside a valid tool-call envelope.
- Competing subtype candidates rejected by precedence.

Evidence ownership:

- Scorer owns scalar-like substitution classification.
- Dataset metadata owns tool-expected eligibility and expected tool behavior.
- Evaluator owns aggregation.
- Detector owns policy consumption only.

Evidence dependencies:

- Exact-valid dependency contract.
- Tool-expected eligibility contract.
- Valid required tool-call detection.
- Scalar-like substitution evidence.
- Precedence distinction from direct-answer substitution, malformed output, and wrong argument.

Missing-evidence behavior:

- If scorer cannot distinguish scalar substitution from direct-answer substitution or malformed output, subtype evidence is missing.
- If expected-tool call and argument comparison evidence are missing, scorer must not use scalar substitution to avoid wrong-argument evidence requirements.

Expected noncomputability behavior:

- Missing scalar evidence makes affected subtype distribution noncomputable.
- Scalar-looking output without emitted subtype remains noncomputable and cannot be classified by detector.

Detector-visible outputs required:

- Scalar subtype count.
- Relevant denominators and rates when emitted.
- Failure taxonomy marker.
- Completeness and current-run computability state.
- Missing-evidence reason when applicable.

Reconciliation dependencies:

- Scalar count contributes exactly one sibling subtype count.
- Scalar count must not be relabeled as direct-answer substitution.
- Subtype totals must reconcile to non-exact eligible denominator.

### Malformed Output

Required scorer evidence:

- Row is tool-expected and not excluded.
- Exact-valid outcome is false.
- Parse/schema evidence shows invalid, unreadable, or structurally malformed output preventing valid tool-call interpretation.
- Output is not parseable enough to identify wrong tool name, wrong argument, or wrapper/envelope drift as the primary subtype.
- Failure taxonomy marker is present.

Optional scorer evidence:

- Parse failure class.
- Schema validation failure class.
- Rationale for why wrong tool name, wrong argument, or wrapper/envelope drift could not be assigned.

Evidence ownership:

- Scorer owns parse/schema classification.
- Dataset metadata owns tool-expected eligibility and expected tool behavior.
- Evaluator owns aggregation.
- Detector owns policy consumption only.

Evidence dependencies:

- Exact-valid dependency contract.
- Parse/schema evidence.
- Precedence distinction from wrapper/envelope drift, wrong tool name, and wrong argument.

Missing-evidence behavior:

- If parse/schema evidence is unavailable, malformed output cannot be assigned unless sufficient scorer evidence supports it.
- If output is partially parseable but primary failure cannot be resolved, subtype evidence is missing.

Expected noncomputability behavior:

- Missing parse/schema evidence blocks malformed-output subtype assignment.
- Affected row remains noncomputable for subtype distribution if no other approved subtype is emitted.

Detector-visible outputs required:

- Malformed-output subtype count.
- Relevant denominators and rates when emitted.
- Failure taxonomy marker.
- Completeness and current-run computability state.
- Missing-evidence reason when applicable.

Reconciliation dependencies:

- Malformed-output count contributes exactly one sibling subtype count.
- Malformed-output subtype remains separate from invalid-json overall governance metrics.
- Subtype totals must reconcile to non-exact eligible denominator.

### Wrapper/Envelope Drift

Required scorer evidence:

- Row is tool-expected and not excluded.
- Exact-valid outcome is false.
- Scorer identifies a recognizable tool-call-like attempt.
- Wrapper, envelope, protocol, or surrounding structure is wrong enough to fail exact-valid requirements.
- Evidence supports wrapper/envelope as the primary failure rather than wrong tool name or wrong argument.
- Failure taxonomy marker is present.

Optional scorer evidence:

- Wrapper/envelope failure class.
- Recognized tool-call-like intent.
- Rationale for primary-failure precedence.

Evidence ownership:

- Scorer owns wrapper/envelope failure classification.
- Dataset metadata owns tool-expected eligibility and expected tool behavior.
- Evaluator owns aggregation.
- Detector owns policy consumption only.

Evidence dependencies:

- Exact-valid dependency contract.
- Tool-call attempt detection.
- Parse/schema evidence sufficient to identify near-tool envelope.
- Precedence distinction from malformed output, wrong tool name, and wrong argument.

Missing-evidence behavior:

- If scorer cannot distinguish wrapper/envelope drift from malformed output, wrong tool name, or wrong argument, subtype evidence is missing.
- If near-tool envelope evidence is absent, wrapper/envelope drift cannot be assigned.

Expected noncomputability behavior:

- Missing wrapper/envelope evidence blocks wrapper-drift subtype assignment.
- Affected row remains noncomputable if no other approved subtype is emitted.

Detector-visible outputs required:

- Wrapper/envelope drift subtype count.
- Relevant denominators and rates when emitted.
- Failure taxonomy marker.
- Completeness and current-run computability state.
- Missing-evidence reason when applicable.

Reconciliation dependencies:

- Wrapper/envelope drift contributes exactly one sibling subtype count.
- It remains separate from wrapper leakage overall governance metrics.
- Subtype totals must reconcile to non-exact eligible denominator.

### Missing Tool Call

Required scorer evidence:

- Row is tool-expected and not excluded.
- Exact-valid outcome is false.
- No valid required tool call is present.
- No parseable wrong-tool call is present.
- No sufficient direct-answer substitution evidence is present.
- No sufficient scalar substitution evidence is present.
- Absence evidence is sufficient to classify missing tool call.
- Failure taxonomy marker is present.

Optional scorer evidence:

- Response-empty, refusal, unrelated-output, or unsupported-output indicator.
- Evidence that substitution subtype candidates were considered and rejected.
- Evidence that malformed fragments are insufficient to classify malformed output.

Evidence ownership:

- Scorer owns tool-call absence classification.
- Dataset metadata owns tool-expected eligibility and expected tool behavior.
- Evaluator owns aggregation.
- Detector owns policy consumption only.

Evidence dependencies:

- Exact-valid dependency contract.
- Valid required tool-call detection.
- Tool-call absence evidence.
- Precedence distinction from direct-answer substitution, scalar substitution, malformed output, and wrong tool name.

Missing-evidence behavior:

- If scorer cannot determine whether a tool call is absent, malformed, wrong-tool, direct-answer, or scalar substitution, subtype evidence is missing.
- Missing tool call must not be used as a generic fallback subtype.

Expected noncomputability behavior:

- Missing absence evidence blocks missing-tool-call subtype assignment.
- Affected row remains noncomputable if no approved subtype is emitted.

Detector-visible outputs required:

- Missing-tool-call subtype count.
- Relevant denominators and rates when emitted.
- Failure taxonomy marker.
- Completeness and current-run computability state.
- Missing-evidence reason when applicable.

Reconciliation dependencies:

- Missing-tool-call count contributes exactly one sibling subtype count.
- It remains separate from no-call correctness governance metrics.
- Subtype totals must reconcile to non-exact eligible denominator.

### Wrong Tool Name

Required scorer evidence:

- Row is tool-expected and not excluded.
- Exact-valid outcome is false.
- Response contains a parseable tool-call attempt.
- Emitted tool identity is available.
- Expected tool identity is available.
- Emitted tool identity differs from expected tool identity.
- Failure taxonomy marker is present.

Optional scorer evidence:

- Recognized emitted tool identity.
- Expected tool identity reference.
- Rationale for wrong-tool-name precedence over wrong argument.

Evidence ownership:

- Scorer owns emitted tool identity detection and mismatch classification.
- Dataset metadata owns expected tool identity.
- Evaluator owns aggregation.
- Detector owns policy consumption only.

Evidence dependencies:

- Exact-valid dependency contract.
- Tool-expected eligibility contract.
- Parse/schema evidence sufficient to identify a tool-call attempt.
- Expected tool identity.
- Emitted tool identity.
- Precedence distinction from wrong argument.

Missing-evidence behavior:

- If emitted tool identity cannot be read, wrong tool name cannot be assigned.
- If expected tool identity is missing, wrong tool name cannot be assigned.
- If both tool identity and wrapper evidence are ambiguous, subtype evidence is missing unless approved precedence is emitted.

Expected noncomputability behavior:

- Missing tool identity evidence blocks wrong-tool-name subtype assignment.
- Affected row remains noncomputable if no other approved subtype is emitted.

Detector-visible outputs required:

- Wrong-tool-name subtype count.
- Relevant denominators and rates when emitted.
- Failure taxonomy marker.
- Completeness and current-run computability state.
- Missing-evidence reason when applicable.

Reconciliation dependencies:

- Wrong-tool-name count contributes exactly one sibling subtype count.
- Wrong tool name generally takes precedence over wrong argument when tool identity is wrong.
- Subtype totals must reconcile to non-exact eligible denominator.

### Wrong Argument

Required scorer evidence:

- Row is tool-expected and not excluded.
- Exact-valid outcome is false.
- Response contains a parseable tool-call attempt.
- Emitted tool identity is available and matches expected tool identity.
- Expected argument evidence is available.
- Emitted argument evidence is available.
- Argument comparison fails.
- Failure taxonomy marker is present.

Optional scorer evidence:

- Argument mismatch class, such as missing required argument, wrong value, wrong type, extra prohibited argument, or wrong path.
- Argument comparison rationale.
- Expected argument reference.

Evidence ownership:

- Scorer owns emitted argument extraction and comparison outcome.
- Dataset metadata owns expected argument evidence unless scorer input contract explicitly owns it.
- Evaluator owns aggregation.
- Detector owns policy consumption only.

Evidence dependencies:

- Exact-valid dependency contract.
- Tool-expected eligibility contract.
- Parse/schema evidence sufficient for argument extraction.
- Correct tool identity evidence.
- Expected and emitted argument evidence.
- Argument comparison outcome.

Missing-evidence behavior:

- If expected arguments are unavailable, wrong argument cannot be assigned.
- If emitted arguments are not parseable enough to compare, wrong argument cannot be assigned.
- If tool identity is wrong or unknown, wrong argument cannot be assigned.

Expected noncomputability behavior:

- Missing argument evidence or comparison evidence blocks wrong-argument subtype assignment.
- Affected row remains noncomputable if no other approved subtype is emitted.

Detector-visible outputs required:

- Wrong-argument subtype count.
- Relevant denominators and rates when emitted.
- Failure taxonomy marker.
- Completeness and current-run computability state.
- Missing-evidence reason when applicable.

Reconciliation dependencies:

- Wrong-argument count contributes exactly one sibling subtype count.
- Requires correct tool identity evidence.
- Subtype totals must reconcile to non-exact eligible denominator.

## Missing-Evidence Contract

Purpose:

- Define how scorer evidence gaps are represented without introducing fallback subtypes or detector inference.

Missing-evidence states apply when:

- exact-valid evidence is missing;
- tool-expected eligibility is missing;
- expected tool identity is missing;
- expected argument evidence is missing;
- scorer primary outcome is missing;
- parse/schema evidence is missing;
- subtype evidence is ambiguous between approved subtypes;
- taxonomy marker is missing;
- precedence evidence is missing;
- subtype summary is missing from aggregate emission.

Expected behavior:

- Missing evidence blocks affected subtype assignment.
- Missing subtype evidence prevents subtype distribution reconciliation.
- Missing denominator blocks rate computation.
- Missing taxonomy marker blocks governed Family A subtype computation.
- Missing evidence is not repaired by `other`, parent aggregate, no-call correctness, invalid-json, wrapper leakage, or historical direct-answer counts.

Detector-visible outputs required:

- Affected concept.
- Missing-evidence reason.
- Completeness state.
- Current-run computability state.
- Comparability state.

## Taxonomy Marker And Versioning Requirements

Purpose:

- Ensure emitted subtype facts are tied to the approved Family A taxonomy.

Required marker semantics:

- Taxonomy identity for Family A.
- Taxonomy version or equivalent comparability marker.
- Approved subtype set.
- Scorer semantics marker.
- Population and split scope marker.
- Tool-expected eligibility marker.
- Exclusion policy marker.

Expected behavior:

- Subtype counts without taxonomy marker are diagnostic-only or noncomputable for governed use.
- Historical comparison is blocked unless taxonomy and scorer semantics are stable or explicitly bridged.
- A taxonomy marker must apply at family level and be sufficient to interpret governed direct-answer subtype.

Missing marker behavior:

- Missing taxonomy marker makes subtype distribution noncomputable.
- Missing scorer semantics marker blocks baseline comparison.
- Missing population, split, or exclusion marker blocks comparison and may block current-run interpretation if the marker is required for denominator construction.

Detector non-inference boundary:

- Detector must not infer taxonomy version from artifact path, report shape, subtype names, or historical output format.

## Ambiguity-Zone Resolution Requirements

| Ambiguity Zone | Required Evidence To Resolve | Missing-Evidence Outcome |
|---|---|---|
| direct-answer vs scalar | Evidence distinguishing prose/direct answer from bare scalar-like value. | Subtype missing; affected row noncomputable. |
| direct-answer vs missing tool call | Evidence that response substitutes an answer for required procedure. | Subtype missing unless missing-tool-call absence evidence is independently sufficient. |
| scalar vs malformed output | Evidence that output is a readable scalar answer rather than malformed attempted tool call. | Subtype missing unless parse evidence supports malformed output. |
| malformed output vs wrapper/envelope drift | Evidence that near-tool envelope is recognizable. | Malformed output only if parse evidence supports it; otherwise subtype missing. |
| wrapper/envelope drift vs wrong tool name | Evidence identifying primary failure and readable tool identity. | Subtype missing unless approved precedence is emitted. |
| wrapper/envelope drift vs wrong argument | Evidence that envelope is valid enough for argument comparison or primary envelope failure. | Subtype missing unless approved precedence is emitted. |
| wrong tool name vs wrong argument | Evidence that tool identity is wrong or correct before argument comparison. | Subtype missing if tool identity cannot be reliably read. |
| wrong argument vs malformed output | Evidence that arguments are parseable enough to compare. | Malformed output if parse evidence supports it; otherwise subtype missing. |
| direct-answer vs wrapper/envelope drift | Evidence identifying primary behavior as tool bypass or near-tool attempt. | Subtype missing unless approved primary subtype is emitted. |
| missing tool call vs malformed output | Evidence distinguishing absence from malformed attempted syntax. | Subtype missing if absence cannot be distinguished from malformed attempt. |

## Evidence That Must Never Be Reconstructed

The following evidence must never be reconstructed by detector or evaluator from lower-level artifacts:

- direct-answer substitution evidence;
- scalar substitution evidence;
- malformed-output evidence;
- wrapper/envelope-drift evidence;
- missing-tool-call evidence;
- wrong-tool-name evidence;
- wrong-argument evidence;
- exact-valid outcome;
- tool-expected eligibility;
- expected tool identity;
- expected argument evidence;
- emitted tool identity;
- emitted argument evidence;
- eligible tool-expected denominator;
- non-exact denominator;
- subtype rates;
- taxonomy marker;
- scorer semantics marker;
- baseline comparability status.

## Detector Non-Inference Boundary Review

Detector may consume:

- emitted subtype counts;
- emitted denominator bases;
- emitted subtype rates;
- emitted completeness state;
- emitted current-run computability state;
- emitted noncomputability reasons;
- emitted comparability state;
- emitted taxonomy and scorer semantics markers.

Detector must not:

- inspect generated text to classify subtype;
- inspect prompt text to infer expected tool behavior;
- compare arguments;
- infer tool identity;
- infer scalar or prose substitution from output shape;
- infer malformed output from invalid-json aggregate;
- infer wrapper drift from wrapper leakage aggregate;
- infer missing tool call from no-call correctness aggregate;
- use historical direct-answer counts as current-run facts;
- create an `other` subtype;
- reconstruct denominator membership.

## Reconciliation Dependencies

Family A scorer evidence must support the following reconciliation checks:

- Exact-valid eligible row count plus non-exact eligible row count equals eligible tool-expected denominator.
- Every non-exact eligible row has exactly one approved subtype or explicit missing-evidence state.
- Approved subtype counts sum to non-exact eligible denominator when complete.
- Direct-answer substitution count is a member of the approved subtype distribution.
- Subtype rates over eligible tool-expected rows use the eligible tool-expected denominator.
- Subtype rates over non-exact rows use the non-exact eligible denominator.
- Excluded rows are excluded from governed denominators and visible in exclusion summary.
- Split-scoped subtype summaries reconcile to family aggregate when active.

## Required Analysis Findings

### Evidence Sufficiency By Subtype

| Subtype | Evidence Sufficiency Assessment |
|---|---|
| direct-answer substitution | Sufficient if answer-like substitution evidence and valid required tool-call absence are emitted. |
| scalar substitution | Sufficient if scalar-like replacement evidence and valid required tool-call absence are emitted. |
| malformed output | Sufficient if parse/schema failure evidence is emitted. |
| wrapper/envelope drift | Sufficient if near-tool attempt and wrapper/envelope primary-failure evidence are emitted. |
| missing tool call | Sufficient only if tool-call absence evidence is clear and stronger substitution evidence is absent. |
| wrong tool name | Sufficient if expected tool identity and emitted tool identity mismatch evidence are emitted. |
| wrong argument | Sufficient if correct tool identity and comparable expected/emitted argument mismatch evidence are emitted. |

### Shared Evidence Dependencies

Shared dependencies across all subtypes:

- tool-expected eligibility;
- exclusion state;
- exact-valid outcome;
- primary scorer outcome;
- non-exact tool-expected status;
- failure taxonomy marker;
- scorer semantics marker;
- missing-evidence reason when subtype cannot be assigned.

Shared dependencies across tool-attempt subtypes:

- parse/schema evidence;
- emitted tool-call attempt detection;
- emitted tool identity evidence;
- wrapper/envelope evidence or argument evidence depending on subtype.

Shared dependencies across substitution subtypes:

- absence of a valid required tool call;
- answer-like or scalar-like replacement evidence;
- precedence evidence distinguishing substitution from missing tool call and malformed output.

## Remaining WP3 Blockers

WP3 implementation remains blocked until:

- scorer-owner approves the seven subtype names;
- scorer-owner approves precedence expectations;
- scorer-owner approves the concrete scorer evidence outputs;
- schema owner approves how evidence outputs will be represented later;
- validation owner approves Family A fixture expectations;
- governance owner confirms no generic `other` subtype is introduced;
- taxonomy marker and versioning plan is approved;
- detector non-inference boundary is accepted by detector owner;
- rollback behavior for unstable subtype evidence is accepted.

## Family A Planning Readiness Assessment

Family A is ready for WP3 implementation planning.

Family A is not ready for scorer implementation.

Rationale:

- The approved subtype set has evidence requirements.
- Every approved subtype has sufficient conceptual evidence requirements.
- Ambiguity zones have required evidence and missing-evidence behavior.
- Detector non-inference boundaries are explicit.
- Remaining work is approval and concrete evidence representation, not taxonomy architecture.

Recommended next step:

- Open WP3 implementation planning with a scorer evidence output design review. That review should still avoid code and schema implementation until the evidence outputs, taxonomy marker, and fixture expectations are approved.
