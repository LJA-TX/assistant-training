# Stage B WP8-C Scenario-To-Subtype Mapping

## Scope

This document maps every Family A scenario from `STAGE_B_WP8A_SCENARIO_CATALOG.md` to the approved Family A subtype taxonomy and expected missing-evidence behavior.

This is documentation-only planning. It does not implement scorer logic, create fixture files, implement validators, implement schemas, modify code, modify detectors, modify evaluators, modify scorers, modify thresholds, modify governance rules, modify mappings, or modify manifests.

Reference inputs:

- `STAGE_B_WP8A_SCENARIO_CATALOG.md`
- `STAGE_B_WP8B_COMMON_STATE_FIXTURES.md`
- `STAGE_B_WP8C_FAMILY_A_SUBTYPE_BOUNDARY_REVIEW.md`

## Mapping Principles

- Exact-valid tool-expected rows are not assigned a failure subtype.
- Excluded rows are not assigned a governed subtype and do not enter governed denominators.
- Every eligible non-exact tool-expected row must have exactly one approved subtype for complete Family A emission.
- Missing or conflicting subtype evidence is a noncomputability condition, not an `other` subtype.
- Detector consumes emitted subtype facts only and must not classify generated text.
- Historical direct-answer counts are migration evidence only; they are not current-run subtype facts.

## Family A Scenario-To-Subtype Mapping

| Scenario ID | Intended Subtype | Required Scorer Evidence | Required Precedence Assumptions | Missing-Evidence Outcome | Expected Computability State | Expected Detector Treatment | Reconciliation Expectations |
|---|---|---|---|---|---|---|---|
| A-C-001 | None: exact-valid control | Tool-expected eligibility; exact-valid scorer outcome; taxonomy marker for family context. | Exact-valid exits subtype classification before failure taxonomy assignment. | Missing exact-valid evidence makes exact/non-exact partition noncomputable. | current-run computable | Consume exact-valid fact; do not assign subtype. | Eligible denominator includes row; non-exact denominator excludes row. |
| A-C-002 | direct-answer substitution | Tool-expected eligibility; non-exact status; no valid required tool call; answer-like substitution evidence; taxonomy marker. | Direct-answer evidence beats missing-tool-call when answer substitution is explicit; scalar-only output is handled separately. | Missing answer-substitution evidence makes subtype missing and direct-answer governed concept noncomputable for affected row. | current-run computable | Consume emitted direct-answer subtype only. | Direct-answer count increments; eligible and non-exact denominators reconcile. |
| A-C-003 | scalar substitution | Tool-expected eligibility; non-exact status; no valid required tool call; scalar-like replacement evidence; taxonomy marker. | Bare scalar-like replacement is classified before direct-answer prose; wrong-argument applies if scalar occurs inside a valid expected-tool call. | Missing scalar evidence makes subtype missing unless another approved subtype has sufficient evidence. | current-run computable | Consume emitted scalar subtype; do not relabel as direct-answer. | Scalar count increments; subtype totals reconcile to non-exact denominator. |
| A-C-004 | malformed output | Tool-expected eligibility; non-exact status; parse/schema evidence showing malformed output; taxonomy marker. | Parseable wrong tool name, wrong argument, or wrapper drift takes precedence when those facts are available. | Missing parse/schema evidence makes subtype missing unless another approved subtype has sufficient evidence. | current-run computable | Consume emitted malformed-output subtype only. | Malformed count increments; subtype totals reconcile. |
| A-C-005 | wrapper/envelope drift | Tool-expected eligibility; non-exact status; recognizable tool-call-like attempt; envelope/wrapper failure evidence; taxonomy marker. | Recognizable envelope failure takes precedence over malformed output; wrong tool name or wrong argument takes precedence when envelope is valid enough and is not primary. | Missing primary-failure evidence makes subtype missing. | current-run computable | Consume emitted wrapper-drift subtype; do not use wrapper leakage proxy. | Wrapper-drift count reconciles within subtype distribution. |
| A-C-006 | missing tool call | Tool-expected eligibility; non-exact status; no valid required tool call; absence evidence; no stronger direct-answer or scalar substitution evidence; taxonomy marker. | Direct-answer and scalar substitution are considered before missing tool call when substitution evidence exists. | Missing absence evidence makes subtype missing. | current-run computable | Consume emitted missing-tool-call subtype; do not infer from no-call aggregate. | Missing-tool-call count reconciles within subtype distribution. |
| A-C-007 | wrong tool name | Tool-expected eligibility; non-exact status; parseable tool-call attempt; emitted tool name; expected tool identity; mismatch evidence; taxonomy marker. | Wrong tool name takes precedence over wrong argument when tool identity is wrong. | Missing tool-name or expected-tool evidence makes subtype missing. | current-run computable | Consume emitted wrong-tool-name subtype only. | Wrong-tool-name count reconciles within subtype distribution. |
| A-C-008 | wrong argument | Tool-expected eligibility; non-exact status; parseable expected-tool call; comparable emitted arguments; expected arguments; mismatch evidence; taxonomy marker. | Correct tool identity plus comparable argument mismatch maps to wrong argument after wrong-tool-name is ruled out. | Missing expected-argument or comparison evidence makes subtype missing. | current-run computable | Consume emitted wrong-argument subtype only. | Wrong-argument count reconciles within subtype distribution. |
| A-C-009 | None: excluded-row control | Tool-expected row marked excluded before aggregation; exclusion reason emitted. | Exclusion exits governed subtype classification before failure taxonomy assignment. | Missing exclusion evidence means row eligibility must be resolved by metadata owner; detector must not infer. | current-run computable for remaining governed population | Consume exclusion summary; do not count excluded row. | Excluded row appears in exclusion count and not in governed denominator. |
| A-C-010 | All approved subtypes, split-scoped | Complete subtype facts across active splits for all approved subtypes represented in split scope. | Split-scoped subtype assignment must follow the same subtype precedence as aggregate assignment. | Missing split subtype evidence makes split-scoped subtype summary noncomputable. | current-run computable | Consume emitted split summaries only. | Split subtype totals reconcile with family aggregate. |
| A-P-001 | Affected approved subtype unknown or missing | Family aggregate present; one required approved subtype summary absent. | No fallback subtype or `other` category is assumed. | Missing subtype summary makes affected subtype and full subtype distribution noncomputable. | current-run noncomputable | Mark partial; do not infer missing subtype. | Aggregate cannot claim subtype distribution reconciliation. |
| A-P-002 | direct-answer substitution | Direct-answer count emitted; denominator evidence absent. | Count-only evidence is not sufficient for governed rate. | Missing denominator makes direct-answer governed rate noncomputable. | current-run noncomputable | Treat count-only evidence as incomplete. | Rate reconciliation blocked by missing denominator. |
| A-P-003 | direct-answer substitution | Direct-answer count and denominator emitted; failure taxonomy marker absent. | Taxonomy marker is required for governed subtype interpretation. | Missing taxonomy marker makes subtype not governed-computable. | current-run noncomputable | Do not accept direct-answer subtype without taxonomy marker. | Numeric count may reconcile diagnostically; taxonomy validation fails. |
| A-P-004 | direct-answer substitution, split-scoped | Aggregate direct-answer summary emitted; active split-scoped summary absent. | Split-scoped governance requires emitted split summary; aggregate does not substitute for split. | Missing split summary makes split-scoped direct-answer noncomputable. | current-run noncomputable | Do not synthesize split summary from aggregate. | Split-to-aggregate reconciliation blocked. |
| A-P-005 | All approved subtype rates | Non-exact denominator emitted; eligible tool-expected denominator absent. | Failure-mix rate and eligible-population rate are distinct denominator views. | Missing eligible denominator blocks eligible-population rates for all subtypes. | current-run noncomputable | Do not compute eligible-population rates. | Failure-mix denominator may reconcile; eligible-population rate blocked. |
| A-M-001 | None: missing-family control | Family registry declares Family A active; Family A aggregate absent. | Active registered family requires either emission or explicit noncomputability. | Missing family makes all Family A concepts noncomputable. | current-run noncomputable | Report missing family; do not reconstruct from rows or history. | No Family A count, denominator, or rate reconciliation possible. |
| A-M-002 | direct-answer substitution | Family aggregate emitted; direct-answer governed subtype absent. | Governed subtype must be explicit; sibling subtype totals do not substitute. | Missing direct-answer subtype makes direct-answer governed concept noncomputable. | current-run noncomputable | Report missing governed subtype; do not use other subtype totals. | Direct-answer reconciliation impossible. |
| A-M-003 | All approved subtypes | Taxonomy marker and approved subtype set absent. | Taxonomy marker is prerequisite for subtype validity. | Missing taxonomy makes subtype distribution noncomputable. | current-run noncomputable | Report missing taxonomy; do not classify generated output. | Subtype distribution cannot reconcile against approved taxonomy. |
| A-M-004 | Affected subtype unknown | Required scorer primary outcome missing for eligible row. | Primary outcome is prerequisite to exact/non-exact and subtype assignment. | Missing scorer primary outcome blocks row partition and subtype assignment. | current-run noncomputable | Report missing scorer fact. | Row cannot enter exact/non-exact partition reconciliation. |
| A-M-005 | Affected subtype unknown | Exact-valid fact missing for tool-expected row. | Exact-valid determination precedes failure-subtype assignment. | Missing exact-valid fact blocks exact/non-exact partition. | current-run noncomputable | Report missing exact-valid fact. | Exact/non-exact denominator partition blocked. |
| A-M-006 | Affected approved subtype missing | Non-exact tool-expected row lacks approved subtype. | No `other` subtype is implied; exactly one approved subtype is required. | Missing subtype makes affected row and subtype distribution noncomputable. | current-run noncomputable | Report missing subtype; do not assign `other`. | Non-exact subtype totals fail to reconcile. |
| A-NI-001 | direct-answer substitution candidate, missing evidence | Generated text appears prose-like; no direct-answer subtype emitted by scorer. | Detector cannot convert prose appearance into subtype evidence. | Missing emitted subtype keeps direct-answer concept noncomputable. | current-run noncomputable | Do not classify generated text; report missing subtype. | No direct-answer count reconciliation allowed. |
| A-NI-002 | scalar substitution candidate, missing evidence | Scalar-looking output exists; scorer subtype missing. | Detector cannot choose scalar or direct-answer from output shape. | Missing emitted subtype keeps subtype distribution noncomputable. | current-run noncomputable | Do not infer scalar or direct-answer subtype from output shape. | Subtype distribution blocked. |
| A-NI-003 | direct-answer substitution, historical-only evidence | Historical direct-answer count exists; current taxonomy or denominator absent. | Historical evidence is migration context, not current-run subtype fact. | Missing current taxonomy or denominator makes current-run direct-answer noncomputable and comparison bridge-required. | current-run noncomputable | Block comparison; do not use historical count as current fact. | Current denominator and taxonomy reconciliation blocked. |
| A-NI-004 | direct-answer substitution candidate, no-call proxy rejected | No-call correctness changes; direct-answer subtype facts absent. | No-call correctness is separate governance signal and cannot substitute for direct-answer subtype. | Missing direct-answer subtype keeps Family A direct-answer concept noncomputable. | current-run noncomputable | Do not reinterpret no-call correctness as direct-answer substitution. | No Family A subtype reconciliation allowed. |

## Precedence-Dependent Scenarios

The following scenarios depend on subtype precedence rules:

- `A-C-002`: direct-answer substitution must be distinguished from scalar substitution, missing tool call, malformed output, and wrapper/envelope drift.
- `A-C-003`: scalar substitution must be distinguished from direct-answer substitution, malformed output, and wrong argument.
- `A-C-004`: malformed output must yield to wrong tool name, wrong argument, or wrapper/envelope drift when those scorer facts are available.
- `A-C-005`: wrapper/envelope drift must be distinguished from malformed output, wrong tool name, and wrong argument.
- `A-C-006`: missing tool call applies only after direct-answer and scalar substitution evidence is absent.
- `A-C-007`: wrong tool name takes precedence over wrong argument when tool identity is wrong.
- `A-C-008`: wrong argument requires correct tool identity and comparable arguments.
- `A-C-010`: split-scoped subtype summaries must apply the same precedence as aggregate subtype assignment.

Precedence-dependent missing behavior:

- If the scorer cannot emit the required precedence evidence, subtype assignment is missing and the affected Family A row is noncomputable.

## Scorer-Evidence Dependencies

The scenario catalog depends on the following scorer-evidence contracts:

- exact-valid outcome;
- primary outcome class;
- non-exact tool-expected status;
- parse/schema evidence;
- valid required tool-call detection;
- expected tool identity;
- emitted tool identity;
- expected argument evidence;
- emitted argument evidence;
- argument comparison outcome;
- answer-like prose substitution evidence;
- scalar-like substitution evidence;
- tool-call absence evidence;
- wrapper/envelope failure evidence;
- approved subtype assignment;
- failure taxonomy marker;
- missing-evidence reason when subtype cannot be assigned.

These are evidence dependencies, not implementation requirements in this document.

## Noncomputable When Evidence Is Absent

The following scenarios are explicitly noncomputable when evidence is absent:

- `A-P-001`: missing subtype summary.
- `A-P-002`: missing denominator.
- `A-P-003`: missing taxonomy marker.
- `A-P-004`: missing split-scoped subtype summary.
- `A-P-005`: missing eligible denominator.
- `A-M-001`: missing Family A aggregate.
- `A-M-002`: missing direct-answer subtype.
- `A-M-003`: missing taxonomy.
- `A-M-004`: missing scorer primary outcome.
- `A-M-005`: missing exact-valid fact.
- `A-M-006`: missing approved subtype for non-exact row.
- `A-NI-001`: no emitted direct-answer subtype despite prose-like output.
- `A-NI-002`: no emitted subtype despite scalar-looking output.
- `A-NI-003`: current taxonomy or denominator absent with historical direct-answer evidence only.
- `A-NI-004`: no emitted direct-answer subtype with no-call proxy evidence only.

## Coverage Assessment

### Scenario Coverage By Subtype

| Coverage Category | Scenario Count | Scenario IDs |
|---|---:|---|
| direct-answer substitution | 8 | `A-C-002`, `A-P-002`, `A-P-003`, `A-P-004`, `A-M-002`, `A-NI-001`, `A-NI-003`, `A-NI-004` |
| scalar substitution | 2 | `A-C-003`, `A-NI-002` |
| malformed output | 1 | `A-C-004` |
| wrapper/envelope drift | 1 | `A-C-005` |
| missing tool call | 1 | `A-C-006` |
| wrong tool name | 1 | `A-C-007` |
| wrong argument | 1 | `A-C-008` |
| aggregate, control, or missing-evidence scenarios | 10 | `A-C-001`, `A-C-009`, `A-C-010`, `A-P-001`, `A-P-005`, `A-M-001`, `A-M-003`, `A-M-004`, `A-M-005`, `A-M-006` |

### Approved Subtype Coverage Sufficiency

Every approved subtype has at least one positive complete-emission scenario.

Direct-answer substitution has additional partial, missing, historical, and detector non-inference scenarios because it is the governed subtype retained from the original redesign-required metric.

Scalar substitution has both positive and missing-evidence coverage.

Malformed output, wrapper/envelope drift, missing tool call, wrong tool name, and wrong argument each have positive complete-emission coverage, but their ambiguity-zone coverage is currently captured by boundary review and precedence rules rather than separate scenario IDs.

### Over-Broad Subtype Assessment

Potential over-broad subtype:

- missing tool call.

Reason:

- It can absorb empty, refusal, unrelated, or non-tool behavior if scorer evidence is weak.

Control:

- Missing tool call should apply only when tool-call absence evidence is clear and direct-answer/scalar substitution evidence is absent. Otherwise subtype evidence is missing.

### Redundancy Assessment

No approved subtype appears redundant.

Rationale:

- Direct-answer substitution protects prose/tool-bypass behavior.
- Scalar substitution protects bare-value/tool-bypass behavior.
- Malformed output protects parse/schema failure.
- Wrapper/envelope drift protects near-tool protocol drift.
- Missing tool call protects absence of required tool invocation without stronger substitution evidence.
- Wrong tool name protects wrong tool identity.
- Wrong argument protects correct tool with wrong arguments.

### Ambiguity Assessment

Implementation-blocking unresolved ambiguity count: 0.

Documented ambiguity zones requiring scorer evidence or precedence: 10.

Those zones are resolved for planning by the following rule:

- if required scorer evidence or approved precedence is missing, subtype assignment is missing and the affected Family A row is current-run noncomputable.

## Taxonomy Readiness Assessment

Family A taxonomy is ready for fixture planning.

Family A taxonomy is not ready for scorer implementation until the following are approved:

- scorer-owner approval of subtype names;
- scorer-owner approval of precedence assumptions;
- concrete scorer evidence contract;
- taxonomy marker or version plan;
- governance-owner confirmation that no generic `other` subtype will be introduced without separate approval;
- fixture-owner approval that the scenario coverage is sufficient.

## Recommendation For WP3

WP3 can proceed to implementation planning, but not implementation.

Recommended next WP3 planning objective:

- Define the scorer evidence contract for Family A, including exact evidence fields or outputs needed to support each approved subtype and missing-evidence state.

Implementation should remain blocked until:

- subtype names and precedence are approved;
- scorer evidence outputs are specified;
- Family A fixture expectations are accepted;
- taxonomy marker/version handling is specified;
- detector non-inference boundaries are accepted.
