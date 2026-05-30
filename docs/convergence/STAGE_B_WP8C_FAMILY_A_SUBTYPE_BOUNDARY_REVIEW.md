# Stage B WP8-C Family A Subtype Boundary Review

## Scope

This document reviews and formalizes Family A failure-subtype boundaries before fixture authoring, schema implementation, scorer implementation, validator implementation, or detector implementation.

This is documentation-only planning. It does not create fixture files, implement validators, implement schemas, modify code, modify detectors, modify evaluators, modify scorers, modify thresholds, modify governance rules, modify mappings, or modify manifests.

Reference inputs:

- `STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
- `STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
- `STAGE_B_EVAL_REDESIGN_IMPLEMENTATION_READINESS.md`
- `STAGE_B_WP8A_SCENARIO_CATALOG.md`
- `STAGE_B_WP8B_COMMON_STATE_FIXTURES.md`

Family A purpose:

- Preserve direct-answer substitution as a governed subtype within a broader failure-subtype taxonomy for non-exact tool-expected rows.
- Ensure every eligible non-exact tool-expected row receives exactly one approved subtype, or explicit noncomputability when subtype evidence is missing.
- Prevent detector-time generated-text interpretation, prompt inspection, denominator reconstruction, or proxy substitution.

## Boundary Principles

- Family A applies only to eligible tool-expected rows.
- Exact-valid tool-expected rows are not assigned a failure subtype.
- Excluded rows are not assigned a governed failure subtype and do not enter governed denominators.
- No-call rows are not Family A eligible unless future design explicitly marks them as tool-expected rows.
- A non-exact tool-expected row must have exactly one approved failure subtype for complete Family A emission.
- Missing or conflicting subtype evidence creates noncomputability for the affected subtype distribution.
- The detector consumes emitted subtype facts and must not classify generated text.
- A generic `other` subtype is not approved by this review. If future implementation needs one, it requires separate approval and fixture coverage.

## Approved Subtype Set For WP8-C Fixture Planning

The following subtype set is approved for WP8-C planning:

| Subtype | Boundary Status |
|---|---|
| direct-answer substitution | Governed subtype |
| scalar substitution | Approved sibling subtype |
| malformed output | Approved sibling subtype |
| wrapper/envelope drift | Approved sibling subtype |
| missing tool call | Approved sibling subtype |
| wrong tool name | Approved sibling subtype |
| wrong argument | Approved sibling subtype |

No additional subtype is approved by current Stage B planning.

Future-reserved candidate areas:

- wrong tool-call cardinality;
- wrong tool-call ordering;
- extra unsupported tool call;
- multiple simultaneous failures with explicit precedence.

These candidates should not be used in fixture authoring or scorer implementation until separately approved.

## Subtype Boundary Definitions

### Direct-Answer Substitution

Subtype name:

- direct-answer substitution.

Purpose:

- Detect tool bypass when a tool-expected row receives answer-like prose, a direct result, or answer text instead of the required tool invocation.

Required scorer evidence:

- Row is eligible and tool-expected.
- Response is not exact-valid.
- No valid required tool invocation satisfies the expected tool behavior.
- Scorer identifies the response as answer-like output replacing the tool call rather than attempting the required tool interface.
- Failure taxonomy marker is present.

What distinguishes it from neighboring subtypes:

- Unlike scalar substitution, the output is answer-like natural language or direct result prose rather than a bare scalar or scalar-like value.
- Unlike missing tool call, the response does more than merely omit a tool call; it substitutes an answer for the required procedure.
- Unlike malformed output, the primary failure is procedural substitution, not unreadable or invalid serialization.
- Unlike wrapper/envelope drift, the primary issue is not a near-tool envelope with wrapper drift; it is answer delivery instead of tool invocation.

Boundary conditions:

- If a response contains both answer prose and a valid exact tool invocation, exact-valid handling takes precedence and no failure subtype is assigned.
- If a response contains answer prose plus an invalid tool attempt, scorer evidence must identify the primary failure according to approved precedence before subtype assignment.
- If the response is a short scalar-like value only, scalar substitution should be considered before direct-answer substitution.
- If output cannot be parsed enough to determine whether it is answer-like, malformed output or missing subtype evidence should be used according to scorer evidence.

Missing-evidence behavior:

- If scorer evidence cannot distinguish answer-like substitution from scalar substitution, malformed output, or missing tool call, subtype is missing and Family A is noncomputable for the affected row.
- Detector must not inspect generated text to resolve the subtype.

Detector non-inference expectations:

- Detector must not decide whether prose is a direct answer.
- Detector must not infer direct-answer substitution from no-call correctness movement, invalid-json movement, or wrapper leakage.
- Detector must consume only emitted direct-answer subtype count, denominators, rates, and taxonomy markers.

Reconciliation implications:

- Direct-answer substitution increments one subtype count in the non-exact eligible denominator.
- It must contribute to rates over eligible tool-expected rows and over non-exact eligible tool-expected rows when both denominator bases are emitted.
- Missing direct-answer subtype summary blocks direct-answer governed evaluation even if Family A aggregate exists.

### Scalar Substitution

Subtype name:

- scalar substitution.

Purpose:

- Detect tool bypass where the model emits a bare scalar-like answer, identifier, value, or minimal result instead of the required tool invocation.

Required scorer evidence:

- Row is eligible and tool-expected.
- Response is not exact-valid.
- Required tool invocation is absent or not valid.
- Output is primarily scalar-like or minimal answer-like content rather than structured tool-call content.
- Failure taxonomy marker is present.

What distinguishes it from neighboring subtypes:

- Unlike direct-answer substitution, scalar substitution is primarily a bare value or minimal result, not explanatory answer prose.
- Unlike malformed output, the scalar may be syntactically readable but semantically wrong because it replaces the required tool procedure.
- Unlike missing tool call, scalar substitution contains an answer-like value rather than simple omission.

Boundary conditions:

- A scalar embedded inside prose may be direct-answer substitution if prose is the primary emitted content.
- A scalar embedded inside a malformed attempted tool payload may be malformed output if serialization failure prevents reliable subtype assignment.
- A scalar in a wrong tool argument position belongs under wrong argument if a valid tool call envelope and correct tool identity are otherwise present.

Missing-evidence behavior:

- If scorer evidence cannot distinguish scalar substitution from direct-answer substitution or malformed output, subtype is missing and affected Family A emission is noncomputable.

Detector non-inference expectations:

- Detector must not classify output shape as scalar substitution.
- Detector must not use string length, token shape, JSON parse failure, or no-call aggregate as a proxy.

Reconciliation implications:

- Scalar substitution increments one sibling subtype count.
- Scalar substitution must not be relabeled as direct-answer substitution by the detector.
- Subtype totals must still reconcile to the non-exact eligible denominator.

### Malformed Output

Subtype name:

- malformed output.

Purpose:

- Detect output that cannot be interpreted as a valid tool invocation because its syntax, serialization, parseability, or structure is malformed.

Required scorer evidence:

- Row is eligible and tool-expected.
- Response is not exact-valid.
- Scorer parse/schema evidence shows malformed output prevents valid tool-call interpretation.
- Failure taxonomy marker is present.

What distinguishes it from neighboring subtypes:

- Unlike direct-answer or scalar substitution, malformed output is primarily an invalid or unreadable format problem.
- Unlike wrapper/envelope drift, malformed output is not a coherent near-tool wrapper with a recognizable but wrong envelope; it fails parse or structural validity.
- Unlike wrong tool name or wrong argument, malformed output may not reliably expose a valid tool name or argument structure.

Boundary conditions:

- If a parseable tool call has the wrong name, wrong tool name should be used rather than malformed output.
- If a parseable tool call has correct tool name but wrong arguments, wrong argument should be used rather than malformed output.
- If a near-valid wrapper is parseable enough to identify envelope drift, wrapper/envelope drift should be used.
- If malformed text also looks answer-like, malformed output applies only when scorer evidence cannot reliably classify procedural substitution.

Missing-evidence behavior:

- If parse evidence is unavailable, subtype is missing unless scorer emits another approved subtype with sufficient evidence.

Detector non-inference expectations:

- Detector must not parse generated text to decide malformed output.
- Detector must not substitute invalid-json overall metrics for this subtype.

Reconciliation implications:

- Malformed output increments one sibling subtype count.
- It remains separate from invalid JSON aggregate governance signals.
- Subtype totals must reconcile to the non-exact eligible denominator.

### Wrapper/Envelope Drift

Subtype name:

- wrapper/envelope drift.

Purpose:

- Detect near-tool outputs where the model attempts a tool-call-like structure but emits the wrong wrapper, envelope, or surrounding protocol form.

Required scorer evidence:

- Row is eligible and tool-expected.
- Response is not exact-valid.
- Scorer can identify a tool-call-like attempt.
- Tool name or argument intent may be recognizable, but wrapper/envelope protocol is wrong enough to fail exact-valid requirements.
- Failure taxonomy marker is present.

What distinguishes it from neighboring subtypes:

- Unlike malformed output, wrapper/envelope drift is structured enough to identify a near-tool protocol attempt.
- Unlike wrong tool name, the primary failure is the surrounding envelope rather than the requested tool identity.
- Unlike wrong argument, the primary failure is the envelope or wrapper rather than argument content.
- Unlike direct-answer substitution, the response attempts tool-call form rather than delivering answer prose.

Boundary conditions:

- If the envelope is correct but tool name is wrong, wrong tool name applies.
- If envelope and tool name are correct but arguments are wrong, wrong argument applies.
- If the output is too malformed to identify a near-tool envelope, malformed output applies.
- If both envelope and tool name are wrong, scorer evidence must apply approved precedence; without it, subtype is missing.

Missing-evidence behavior:

- If scorer cannot distinguish wrapper drift from malformed output, wrong tool name, or wrong argument, subtype is missing.

Detector non-inference expectations:

- Detector must not inspect serialized output to identify wrapper drift.
- Detector must not use wrapper leakage aggregate as this subtype.

Reconciliation implications:

- Wrapper/envelope drift increments one sibling subtype count.
- It must remain separate from wrapper leakage governance findings.
- Subtype totals must reconcile to the non-exact eligible denominator.

### Missing Tool Call

Subtype name:

- missing tool call.

Purpose:

- Detect tool-expected rows where the required tool invocation is absent and no more specific approved substitution subtype is supported by scorer evidence.

Required scorer evidence:

- Row is eligible and tool-expected.
- Response is not exact-valid.
- No valid required tool call is present.
- Scorer evidence does not support direct-answer substitution or scalar substitution as a more specific subtype.
- Failure taxonomy marker is present.

What distinguishes it from neighboring subtypes:

- Unlike direct-answer substitution, missing tool call does not require answer-like procedural substitution evidence.
- Unlike scalar substitution, it does not require scalar-like answer evidence.
- Unlike malformed output, it does not require malformed syntax as the primary failure.
- Unlike wrong tool name, there is no parseable tool invocation with an incorrect name.

Boundary conditions:

- Empty response, refusal, unrelated prose without answer substitution evidence, or unsupported non-tool behavior may belong here if the taxonomy approves missing tool call as the best available subtype.
- If answer-like evidence exists, direct-answer substitution should be considered first.
- If scalar-like evidence exists, scalar substitution should be considered first.
- If a parseable wrong tool call exists, wrong tool name should be used.

Missing-evidence behavior:

- If scorer cannot determine whether a tool call is absent, malformed, or wrong-tool, subtype is missing.

Detector non-inference expectations:

- Detector must not infer missing tool call from no-call correctness aggregate.
- Detector must not inspect response text to decide absence.

Reconciliation implications:

- Missing tool call increments one sibling subtype count.
- It must not replace direct-answer substitution when direct-answer evidence is emitted.
- Subtype totals must reconcile to the non-exact eligible denominator.

### Wrong Tool Name

Subtype name:

- wrong tool name.

Purpose:

- Detect non-exact tool-expected rows where the response contains a parseable tool invocation, but the invoked tool identity does not match the expected tool behavior.

Required scorer evidence:

- Row is eligible and tool-expected.
- Response is not exact-valid.
- Scorer identifies a parseable tool-call attempt.
- Emitted or invoked tool name is present.
- Tool name differs from expected tool identity.
- Failure taxonomy marker is present.

What distinguishes it from neighboring subtypes:

- Unlike missing tool call, a tool-call attempt exists.
- Unlike wrapper/envelope drift, tool identity can be read and is the primary failure.
- Unlike wrong argument, the tool identity is wrong, so argument comparison against the expected tool is not primary.
- Unlike malformed output, output is parseable enough to identify a tool name.

Boundary conditions:

- If both tool name and arguments are wrong, wrong tool name should generally take precedence because arguments are evaluated under the wrong tool context.
- If tool name cannot be parsed reliably, malformed output or wrapper drift may apply depending on evidence.
- If the wrong tool name appears in answer prose but not in a tool-call attempt, this subtype does not apply.

Missing-evidence behavior:

- If scorer cannot read a tool name or determine expected tool identity, subtype is missing.

Detector non-inference expectations:

- Detector must not inspect generated text or tool-like strings to determine wrong tool name.
- Detector must not infer expected tool identity from prompt text.

Reconciliation implications:

- Wrong tool name increments one sibling subtype count.
- It blocks wrong-argument classification unless precedence explicitly says otherwise.
- Subtype totals must reconcile to the non-exact eligible denominator.

### Wrong Argument

Subtype name:

- wrong argument.

Purpose:

- Detect non-exact tool-expected rows where the response invokes the expected tool but supplies incorrect, incomplete, extra, or otherwise nonmatching arguments.

Required scorer evidence:

- Row is eligible and tool-expected.
- Response is not exact-valid.
- Scorer identifies a parseable tool-call attempt.
- Tool name matches the expected tool identity.
- Argument comparison against expected tool behavior fails.
- Failure taxonomy marker is present.

What distinguishes it from neighboring subtypes:

- Unlike wrong tool name, the expected tool identity is correct.
- Unlike wrapper/envelope drift, the tool-call envelope is valid enough for argument comparison.
- Unlike malformed output, arguments are parseable enough to compare.
- Unlike direct-answer or scalar substitution, a tool-call attempt exists.

Boundary conditions:

- Missing required argument, wrong value, wrong type, extra prohibited argument, or wrong path can be wrong argument when the expected tool identity is correct.
- If tool name is wrong, wrong tool name should generally take precedence.
- If wrapper/envelope prevents argument comparison, wrapper/envelope drift or malformed output applies.
- If expected arguments are unavailable, subtype is missing rather than inferred.

Missing-evidence behavior:

- If expected arguments or argument comparison evidence are missing, subtype is missing.

Detector non-inference expectations:

- Detector must not compare arguments.
- Detector must not infer expected arguments from prompt text or baseline artifacts.

Reconciliation implications:

- Wrong argument increments one sibling subtype count.
- It requires correct tool identity evidence.
- Subtype totals must reconcile to the non-exact eligible denominator.

## Non-Subtype Categories

The following are not Family A failure subtypes:

| Category | Treatment |
|---|---|
| exact-valid tool-expected row | Excluded from non-exact subtype denominator. |
| excluded row | Reported in exclusion summary and excluded from governed denominators. |
| no-call row that is not tool-expected | Outside Family A eligible population. |
| missing subtype evidence | Noncomputability condition, not an `other` subtype. |
| historical direct-answer count | Migration evidence only; not a current-run subtype fact. |
| invalid-json overall metric | Separate governance signal; not a malformed-output subtype source. |
| wrapper leakage overall metric | Separate governance signal; not a wrapper-drift subtype source. |
| no-call correctness metric | Separate governance signal; not a missing-tool-call or direct-answer subtype source. |

## Ambiguity Zones

| Ambiguity Zone | Conflict | Required Scorer Evidence To Resolve | Expected Behavior When Evidence Is Missing |
|---|---|---|---|
| direct-answer substitution vs scalar substitution | Output may be answer-like but very short. | Evidence distinguishing prose/direct answer from bare scalar-like value. | Mark subtype missing; Family A affected row noncomputable. |
| direct-answer substitution vs missing tool call | Response omits tool call and may contain unrelated or answer-like text. | Evidence that response substitutes an answer for the required tool procedure. | Use missing subtype if substitution evidence is absent and missing-tool-call evidence is also insufficient. |
| scalar substitution vs malformed output | Scalar-like output may also be invalid tool-call serialization. | Evidence that output is a readable scalar answer rather than malformed attempted tool call. | Mark subtype missing or malformed output only if parse evidence supports malformed output. |
| malformed output vs wrapper/envelope drift | Output has some structure but may not be parseable enough to identify wrapper drift. | Parse/schema evidence showing near-tool envelope is recognizable. | Use malformed output if parse evidence supports it; otherwise mark subtype missing. |
| wrapper/envelope drift vs wrong tool name | Tool-like output has both wrong wrapper and wrong tool identity. | Evidence identifying primary failure precedence between envelope and tool identity. | Mark subtype missing unless approved precedence is emitted. |
| wrapper/envelope drift vs wrong argument | Tool-like output has envelope drift and argument mismatch. | Evidence that envelope is valid enough for argument comparison, or precedence marking envelope as primary. | Mark subtype missing unless scorer emits approved primary subtype. |
| wrong tool name vs wrong argument | Tool name and arguments both do not match expectation. | Evidence that tool identity is wrong; expected precedence should assign wrong tool name first. | Mark subtype missing if tool identity cannot be reliably read. |
| wrong argument vs malformed output | Tool identity appears correct but arguments are malformed. | Evidence that arguments are parseable enough to compare against expectation. | Use malformed output if arguments cannot be parsed; otherwise wrong argument. |
| direct-answer substitution vs wrapper/envelope drift | Response contains answer prose plus a near-tool attempt. | Evidence identifying whether the primary emitted behavior is tool bypass or malformed tool attempt. | Mark subtype missing unless scorer emits approved primary subtype. |
| missing tool call vs malformed output | Response lacks a valid tool call but may include invalid fragments. | Evidence distinguishing absence from malformed attempted tool syntax. | Mark subtype missing if absence cannot be distinguished from malformed attempt. |

## Precedence Expectations For Fixture Planning

The following precedence expectations are recommended for WP8-C fixture planning. They are not implementation code and require scorer-owner approval before WP3 implementation:

1. Exact-valid rows exit Family A subtype classification.
2. Excluded rows exit governed subtype classification.
3. Parseable wrong tool name takes precedence over wrong argument.
4. Correct tool name with comparable arguments and argument mismatch maps to wrong argument.
5. Recognizable near-tool envelope failures map to wrapper/envelope drift when envelope is the primary failure.
6. Unparseable or invalid structure maps to malformed output when parse evidence supports that subtype.
7. Bare scalar-like answer replacement maps to scalar substitution.
8. Prose or direct answer replacement maps to direct-answer substitution.
9. Tool call absence without sufficient substitution evidence maps to missing tool call only when absence evidence is clear.
10. If required evidence for precedence is absent, subtype is missing and the affected row is noncomputable.

## Family A Reconciliation Model

Required reconciliation:

- eligible tool-expected denominator equals exact-valid eligible rows plus non-exact eligible rows;
- every non-exact eligible row has exactly one approved subtype;
- approved subtype counts sum to non-exact eligible denominator;
- direct-answer substitution count is one subtype count within that distribution;
- subtype rates over eligible tool-expected rows use the eligible tool-expected denominator;
- subtype rates over non-exact tool-expected rows use the non-exact eligible denominator;
- excluded rows are visible and excluded from governed denominators;
- split-scoped subtype counts reconcile to family aggregate when split-scoped governance is active.

Reconciliation failure behavior:

- Missing subtype blocks subtype distribution reconciliation.
- Missing taxonomy marker blocks governed subtype computation.
- Missing denominator blocks rate computation.
- Count-only direct-answer evidence remains diagnostic, not governed-computable.
- Detector must not repair reconciliation failures.

## Detector Non-Inference Requirements

The detector must never construct:

- failure subtype;
- direct-answer classification;
- scalar classification;
- malformed-output classification;
- wrapper/envelope-drift classification;
- missing-tool-call classification;
- wrong-tool-name classification;
- wrong-argument classification;
- eligible tool-expected denominator;
- non-exact denominator;
- subtype rates;
- subtype comparability status.

The detector may consume:

- emitted subtype counts;
- emitted denominators;
- emitted rates;
- emitted taxonomy markers;
- emitted completeness, computability, noncomputability, and comparability states;
- emitted missing-evidence reasons.

## Additional Subtype Candidate Assessment

No additional subtype is approved for WP8-C fixture authoring.

Future-reserved candidates may be revisited only if fixture planning or scorer design proves the approved set cannot represent observed failures without ambiguity:

| Candidate | Current Status | Reason Not Approved Now |
|---|---|---|
| wrong tool-call cardinality | Future Reserved | Existing Stage B planning has not contracted cardinality as a governed subtype. |
| wrong tool-call ordering | Future Reserved | Multi-call ordering has not been approved as a separate governed subtype. |
| extra unsupported tool call | Future Reserved | Could overlap wrong tool name, wrong argument, or wrapper drift without a separate contract. |
| ambiguous multiple failure | Future Reserved | Would weaken one-subtype-per-row unless precedence rules are separately approved. |
| other/unclassified | Not approved | Would hide missing subtype evidence unless explicitly governed and reconciled. |

## WP3 Readiness Assessment

WP3 Family A scorer taxonomy is planning-ready but not implementation-ready.

Ready now:

- Approved WP8-C planning subtype set exists.
- Direct-answer substitution remains the governed subtype.
- Boundary conditions are documented for every planned subtype.
- Ambiguity zones are identified.
- Detector non-inference expectations are explicit.
- Reconciliation implications are explicit.

Still required before WP3 implementation:

- Scorer-owner approval of subtype names and precedence expectations.
- Fixture-owner approval of Family A scenario-to-subtype mapping.
- Governance-owner approval that no generic `other` subtype is introduced.
- Explicit taxonomy marker/version plan.
- Concrete evidence contract for scorer outputs.
- Family A fixture authoring plan after WP8-C is accepted.

Recommendation:

- Proceed next with a WP8-C companion mapping from Family A scenario IDs to subtype evidence requirements and expected missing-evidence behavior.
- Do not begin scorer implementation until the subtype taxonomy, precedence rules, and taxonomy marker plan are approved.
