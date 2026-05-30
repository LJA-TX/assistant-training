# Stage B Implementation Planning Phase 1: Work Packet Decomposition

## Scope

This document decomposes Stage B Evaluation Redesign implementation into reviewable work packets before any schema or code changes occur.

This is documentation-only implementation planning. It does not modify schemas, code, detectors, evaluators, scorers, thresholds, governance rules, mappings, manifests, or runtime behavior.

Reference inputs:

- `STAGE_B_EVAL_REDESIGN_METRIC_INVENTORY.md`
- `STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
- `STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
- `STAGE_B_EVAL_REDESIGN_IMPLEMENTATION_READINESS.md`
- `STAGE_B_EVAL_REDESIGN_SCHEMA_READINESS.md`
- `STAGE_B_EVAL_REDESIGN_SCHEMA_PROPOSAL.md`
- `STAGE_B_PLANNING_COMPLETENESS_ASSESSMENT.md`

Planning baseline:

- Stage B architecture planning is complete.
- No critical architectural unknowns remain.
- Implementation has not begun.
- Threshold redesign remains out of scope.

## Implementation Doctrine

- Implementation work must preserve the no-proxy, no-inference, no-detector-reconstruction doctrine.
- Current-run computability and baseline comparability must remain separate.
- Missing required facts must remain noncomputable.
- Detector behavior must remain consumer-only.
- Parent family aggregates must not substitute for governed sub-slices.
- Historical baselines must remain comparison-blocked unless migration review explicitly allows comparison.
- Active computable governance findings must remain visible during transition.

## 1. Work Packet Inventory

### WP0: Implementation Entry Gate

Purpose:

- Convert completed Stage B planning into an approved implementation-entry package.
- Confirm branch hygiene, review ownership, packet sequence, and non-threshold scope.

Primary owner:

- Governance/release owner.

Output type:

- Review checkpoint, not runtime artifact.

Required decisions:

- Approve the Stage B.5 schema proposal as the implementation target.
- Approve the packet sequence in this document.
- Confirm that threshold review is excluded.
- Confirm that implementation work starts from a clean branch.

### WP1: Schema Authoring

Purpose:

- Create the concrete schema representation for the approved family model.

Primary owner:

- Schema/evaluator interface owner.

Required future work:

- Encode the top-level containers approved in Stage B.5.
- Encode the common governed-family envelope.
- Encode family aggregate and governed sub-slice structure.
- Encode completeness, current-run computability, noncomputability, and comparability states.
- Encode detector-facing projection boundaries.
- Preserve audit and coverage representation without creating detector reconstruction paths.

Out of scope:

- Threshold design.
- Detector policy changes.
- New metric semantics beyond approved Stage B families.

### WP2: Dataset Metadata

Purpose:

- Supply declared row facts required before scoring and aggregation.

Primary owner:

- Dataset metadata owner.

Required future work:

- Preserve stable row identity and split membership.
- Declare tool-expected eligibility and expected tool behavior.
- Declare read-file family eligibility.
- Declare symbol-name sub-slice membership after WP4 approval.
- Declare anchor-generalization eligibility and anchor category after WP5 approval.
- Declare exclusions before aggregation.
- Provide row-set, population, split, and exclusion evidence for migration review.

Out of scope:

- Detector-side row filtering.
- Prompt-text inference for metadata labels.

### WP3: Family A Scorer Taxonomy

Purpose:

- Define and implement deterministic failure-subtype classification for non-exact tool-expected rows.

Primary owner:

- Scorer owner.

Required future work:

- Approve the failure-subtype set.
- Preserve direct-answer substitution as a governed subtype.
- Distinguish direct-answer substitution from scalar substitution, malformed output, wrapper drift, missing tool call, wrong tool name, wrong arguments, and other approved subtypes.
- Emit scorer facts required for evaluator aggregation.
- Emit taxonomy and scorer semantics comparability evidence.

Out of scope:

- Detector-time generated-text review.
- Reinterpreting no-call correctness or invalid-json metrics as direct-answer substitution.

### WP4: Family B1 Symbol-Name Ownership

Purpose:

- Define non-detector ownership and declaration rules for the read-file symbol-name governed sub-slice.

Primary owner:

- Dataset metadata owner, with evaluator review.

Required future work:

- Approve the symbol-name subpopulation definition.
- Decide where symbol-name membership is declared.
- Confirm membership exists before evaluator aggregation.
- Define parent read-file context required for sub-slice interpretation.
- Define small-denominator visibility requirements for validation and reporting.

Out of scope:

- Detector-side prompt inspection.
- Substituting aggregate read-file behavior for symbol-name behavior.

### WP5: Family B2 Anchor Ownership

Purpose:

- Define non-detector ownership and declaration rules for anchor categories, including no-anchor membership.

Primary owner:

- Dataset metadata owner or approved anchor-assignment owner.

Required future work:

- Approve anchor taxonomy.
- Assign ownership for anchor category classification.
- Ensure no-anchor membership is declared before aggregation.
- Emit anchor taxonomy and ownership comparability evidence.
- Define how excluded or unsupported anchor rows are represented.

Out of scope:

- Detector-side prompt classification.
- Reconstructing no-anchor membership from generated text or prompt strings.

### WP6: Evaluator Aggregation

Purpose:

- Aggregate declared dataset metadata and scorer facts into approved family summaries.

Primary owner:

- Evaluator owner.

Required future work:

- Emit Family A failure-subtype aggregate and direct-answer governed subtype summary.
- Emit Family B1 read-file aggregate and symbol-name governed sub-slice summary.
- Emit Family B2 anchor-generalization aggregate and no-anchor governed sub-slice summary.
- Emit counts, denominators, rates, split-scoped summaries when active, exclusions, coverage summaries, and reconciliation evidence.
- Emit completeness and current-run computability state without detector inference.
- Preserve noncomputability when required facts are missing.

Out of scope:

- Reconstructing metadata from prompt text or generated text.
- Treating mixed-tool or parent-family aggregates as governed sub-slice substitutes.

### WP7: Detector Consumption

Purpose:

- Consume emitted family facts, state, and comparability status after evaluator emission is validated.

Primary owner:

- Detector owner.

Required future work:

- Read only the detector-facing projection or approved emitted aggregate facts.
- Treat missing required facts as noncomputable.
- Treat missing markers or unapproved migration status as comparison-blocking.
- Preserve conservative behavior for partial emissions.
- Report noncomputability reasons without reconstructing metrics.

Out of scope:

- Threshold redesign.
- Detector-side row filtering.
- Detector-side denominator or rate construction.
- Detector-side migration bridge decisions.

### WP8: Validation Fixtures

Purpose:

- Provide fixture coverage proving complete, partial, missing, noncomputable, and comparison-blocked behavior across all approved families.

Primary owner:

- Validation owner, with dataset, scorer, evaluator, and detector reviewers.

Required future work:

- Define complete-emission fixtures for every family.
- Define partial-emission fixtures.
- Define missing-family, missing-sub-slice, missing-marker, and missing-denominator fixtures.
- Define Family A subtype boundary fixtures.
- Define Family B1 symbol-name and non-symbol-name fixtures.
- Define Family B2 anchor and no-anchor fixtures.
- Define detector non-inference fixtures.
- Define reconciliation fixtures for counts, denominators, rates, coverage, and split summaries.
- Define migration-status fixtures for comparison-allowed, bridge-required, reference-only, and comparison-blocked.

Out of scope:

- Threshold tuning.
- Relaxing current governance behavior to make fixtures pass.

### WP9: Migration Review

Purpose:

- Classify historical baselines for comparison eligibility after future emissions exist.

Primary owner:

- Migration/governance review owner.

Required future work:

- Identify historical artifacts for each governed family and sub-slice.
- Determine whether historical values were emitted, inferred, reconstructed, or report-layer only.
- Compare population, denominator, split, scorer semantics, taxonomy, subpopulation, and provenance evidence.
- Classify each concept as comparison-allowed, bridge-required, reference-only, or comparison-blocked.
- Preserve approval rationale for detector consumption.

Out of scope:

- Allowing detector to infer baseline comparability.
- Applying family-level migration approval automatically to governed sub-slices.

### WP10: Integration And Audit Review

Purpose:

- Confirm the full implementation preserves Stage B doctrine before any later threshold review.

Primary owner:

- Governance/release owner.

Required future work:

- Verify component outputs reconcile end to end.
- Verify rollback paths remain available.
- Verify active computable governance findings remain visible.
- Verify detector does not consume inferred or proxy facts.
- Verify audit artifacts are retained without becoming alternate metric sources.

Out of scope:

- Threshold review.
- Governance relaxation.

## 2. Dependency Graph

### Dependency Table

| Work Packet | Prerequisites | Downstream Dependents | Blocking Relationships |
|---|---|---|---|
| WP0 Implementation Entry Gate | Clean branch; Stage B planning package committed; architecture accepted for implementation planning | All packets | Blocks all implementation work until scope, sequence, and no-threshold boundary are approved. |
| WP1 Schema Authoring | WP0; Stage B.5 schema proposal accepted; initial WP8 fixture matrix outline | WP2, WP3, WP6, WP7, WP8, WP9, WP10 | Blocks component emission work that depends on concrete schema shape. |
| WP2 Dataset Metadata | WP0; WP1 schema direction; WP4 and WP5 ownership decisions for sub-slices | WP3, WP6, WP8, WP9, WP10 | Blocks scorer/evaluator aggregation for rows requiring declared metadata. |
| WP3 Family A Scorer Taxonomy | WP0; WP1 schema direction; WP2 tool-expected metadata; WP8 subtype fixtures | WP6, WP7, WP8, WP9, WP10 | Blocks Family A aggregation and detector consumption. |
| WP4 Family B1 Symbol-Name Ownership | WP0; WP2 metadata ownership review; WP8 symbol-name fixtures | WP2, WP6, WP7, WP8, WP9, WP10 | Blocks symbol-name sub-slice emission and validation. |
| WP5 Family B2 Anchor Ownership | WP0; WP2 metadata ownership review; WP8 anchor fixtures | WP2, WP6, WP7, WP8, WP9, WP10 | Blocks no-anchor sub-slice emission and validation. |
| WP6 Evaluator Aggregation | WP1 schema; WP2 metadata; WP3 scorer taxonomy; WP4 symbol-name ownership; WP5 anchor ownership; WP8 aggregation fixtures | WP7, WP9, WP10 | Blocks detector consumption and migration classification based on future emissions. |
| WP7 Detector Consumption | WP1 schema; WP6 evaluator emission; WP8 detector non-inference fixtures; initial WP9 status model | WP10; later threshold review | Blocks full governance verification of redesigned emissions. |
| WP8 Validation Fixtures | WP0; Stage B contracts; Stage B.5 schema proposal; input from WP3, WP4, WP5 | WP1, WP2, WP3, WP6, WP7, WP9, WP10 | Blocks implementation acceptance when fixture gaps exist. |
| WP9 Migration Review | WP1 comparability model; WP6 validated emissions; WP8 migration fixtures | WP7, WP10; later threshold review | Blocks historical comparison and comparative detector behavior. |
| WP10 Integration And Audit Review | WP1 through WP9 completed or explicitly deferred where allowed | Later threshold review | Blocks any threshold review or governance promotion. |

### Critical Blocking Chain

Critical path:

1. WP0 Implementation Entry Gate.
2. WP8 Validation Fixtures, at least as an approved fixture matrix.
3. WP1 Schema Authoring.
4. WP4 Family B1 Symbol-Name Ownership and WP5 Family B2 Anchor Ownership.
5. WP2 Dataset Metadata.
6. WP3 Family A Scorer Taxonomy.
7. WP6 Evaluator Aggregation.
8. WP7 Detector Consumption.
9. WP9 Migration Review.
10. WP10 Integration And Audit Review.

Reasoning:

- Schema and fixtures define the target contract.
- Metadata and scorer facts create the facts available for aggregation.
- Evaluator aggregation creates the first governed family emissions.
- Detector consumption and migration review depend on validated emissions.

### Parallelizable Work

The following work can proceed in parallel after WP0:

- WP1 schema authoring draft and WP8 fixture matrix draft.
- WP4 symbol-name ownership and WP5 anchor ownership review.
- WP3 taxonomy definition work, as long as implementation waits for schema and metadata alignment.

The following work should not proceed in parallel as implementation:

- WP7 detector consumption before WP6 emits validated aggregate facts.
- WP9 comparison allowance before future emissions and markers exist.
- Threshold review before WP10 passes.

## 3. Acceptance Criteria

### WP0 Acceptance Criteria

- Branch and worktree are clean at implementation start.
- Stage B.5 schema proposal is accepted as the target architecture.
- Work-packet dependency order is approved.
- No threshold redesign is included.
- Rollback and review checkpoints are assigned.

### WP1 Acceptance Criteria

- Concrete schema representation covers the approved top-level containers.
- Common governed-family envelope is represented.
- Family A, Family B1, and Family B2 aggregate and sub-slice structures are represented.
- Completeness, current-run computability, noncomputability, and comparability states are represented separately.
- Detector-facing projection contains emitted facts and states only.
- Missing required facts cannot be represented as zero values.
- Review confirms no proxy, alias, or detector-reconstruction path is introduced.

### WP2 Acceptance Criteria

- Required row identity, split membership, tool-expected eligibility, expected tool behavior, read-file eligibility, anchor eligibility, exclusions, and population markers are declared where applicable.
- Symbol-name and anchor ownership decisions are integrated after WP4 and WP5 approval.
- Coverage review confirms eligible rows have required metadata.
- Missing metadata scenarios are explicitly represented for downstream noncomputability.
- Detector remains unable to construct metadata labels.

### WP3 Acceptance Criteria

- Approved failure-subtype taxonomy exists.
- Direct-answer substitution is a governed subtype.
- Fixture review proves direct-answer substitution is distinct from scalar substitution, malformed output, wrapper drift, missing tool call, wrong tool name, wrong arguments, and other approved subtypes.
- Every non-exact tool-expected governed row receives exactly one approved subtype or explicit noncomputability state.
- Scorer semantics and taxonomy markers are emitted for downstream aggregation and migration review.

### WP4 Acceptance Criteria

- Symbol-name sub-slice definition is approved.
- Symbol-name membership ownership is non-detector and explicit.
- Parent read-file context requirement is approved.
- Missing symbol-name marker scenarios produce sub-slice noncomputability.
- Fixture review covers symbol-name, non-symbol-name read-file, non-read-file, excluded, and missing-marker rows.

### WP5 Acceptance Criteria

- Anchor taxonomy is approved.
- Anchor assignment ownership is explicit and non-detector.
- No-anchor membership is declared before aggregation.
- Missing anchor category, missing anchor taxonomy, and conflicting ownership scenarios produce noncomputability or comparison blockage as appropriate.
- Fixture review covers no-anchor, other anchor categories, excluded rows, missing category, and missing marker cases.

### WP6 Acceptance Criteria

- Family A aggregate, direct-answer governed subtype, and sibling subtype summaries reconcile.
- Family B1 read-file aggregate and symbol-name sub-slice reconcile.
- Family B2 anchor aggregate and no-anchor sub-slice reconcile.
- Counts, denominators, rates, split summaries, exclusions, and coverage summaries reconcile.
- Partial or missing emissions remain noncomputable for affected governed concepts.
- Evaluator does not infer from prompt text, generated text, artifact names, or detector logic.

### WP7 Acceptance Criteria

- Detector consumes only approved emitted facts, state, and comparability status.
- Missing families, missing sub-slices, missing denominators, and missing markers remain noncomputable or comparison-blocking.
- Detector does not construct row populations, sub-slices, denominators, rates, failure subtypes, anchor categories, or migration status.
- Partial-emission fixtures do not pass silently.
- Existing active computable governance findings remain visible.

### WP8 Acceptance Criteria

- Fixture matrix covers every governed family and governed sub-slice.
- Fixtures cover complete, partial, missing, current-run noncomputable, comparison-allowed, bridge-required, reference-only, and comparison-blocked states.
- Fixtures cover Family A subtype boundaries.
- Fixtures cover Family B1 symbol-name small-denominator behavior.
- Fixtures cover Family B2 no-anchor and anchor taxonomy behavior.
- Fixture expected outputs are defined before implementation acceptance.
- Fixtures include negative cases for proxy, inferred, reconstructed, and parent-aggregate substitution behavior.

### WP9 Acceptance Criteria

- Historical artifacts are inventoried by governed family and sub-slice.
- Each historical concept is classified as comparison-allowed, bridge-required, reference-only, or comparison-blocked.
- Approval rationale identifies population, denominator, split, scorer semantics, taxonomy, subpopulation, row-set, and provenance evidence.
- Family-level approval does not automatically approve sub-slices.
- Detector receives migration status rather than inferring it.

### WP10 Acceptance Criteria

- End-to-end validation confirms schema, metadata, scorer, evaluator, detector, fixtures, and migration review align.
- Rollback can independently disable unvalidated emissions or detector consumption.
- Audit artifacts are preserved.
- No implementation path relaxes governance or thresholds.
- Threshold review remains blocked until redesigned emissions validate and migration review completes.

## 4. Rollback Boundaries

### Independently Revertible Packets

The following packets should be designed to be independently revertible when their downstream consumers have not yet been enabled:

- WP1 schema authoring, if no component emits or consumes the new schema yet.
- WP2 metadata additions, if evaluator aggregation does not require them yet.
- WP3 scorer taxonomy changes, if evaluator aggregation and detector consumption are not enabled.
- WP4 symbol-name ownership metadata, if read-file sub-slice aggregation is not enabled.
- WP5 anchor ownership metadata, if anchor aggregation is not enabled.
- WP8 fixture additions, because validation fixtures should not change runtime behavior.
- WP9 migration review records, if detector comparison remains disabled.

### Packets That Must Move Together

The following packets should move together once runtime consumption begins:

- WP1 schema representation and WP6 evaluator aggregation for emitted family summaries.
- WP2 metadata facts and WP6 evaluator aggregation for any family using those facts.
- WP3 scorer taxonomy and WP6 Family A aggregation.
- WP4 symbol-name ownership and WP6 Family B1 symbol-name aggregation.
- WP5 anchor ownership and WP6 Family B2 no-anchor aggregation.
- WP6 evaluator aggregation and WP7 detector consumption for any active governed decision surface.
- WP7 detector consumption and WP9 migration status for historical comparison behavior.

### Rollback Rules

- If a required row fact is incomplete, roll back or disable dependent aggregation rather than inferring the fact.
- If a scorer subtype is unstable, roll back Family A subtype emission and keep the governed concept noncomputable.
- If denominator reconciliation fails, roll back affected family or sub-slice emission.
- If detector consumes inferred or proxy facts, roll back detector consumption before changing governance rules.
- If migration status is wrong or incomplete, block comparison rather than changing thresholds.
- If partial emissions are unavoidable, represent them explicitly and keep dependent governed rules noncomputable.

## 5. Recommended Execution Order

### Phase 1: Implementation Entry And Review Setup

Work packets:

- WP0 Implementation Entry Gate.
- WP8 Validation Fixtures, fixture matrix only.

Objective:

- Establish implementation boundaries, review ownership, fixture expectations, and clean-start conditions.

Exit criteria:

- Work-packet sequence approved.
- Fixture matrix approved at least at scenario level.
- No threshold scope included.

### Phase 2: Schema And Ownership Foundations

Work packets:

- WP1 Schema Authoring.
- WP4 Family B1 Symbol-Name Ownership.
- WP5 Family B2 Anchor Ownership.

Objective:

- Define concrete representation and settle the highest-impact metadata ownership questions before component implementation.

Exit criteria:

- Schema review passes.
- Symbol-name ownership approved.
- Anchor ownership approved.
- Fixture matrix updated to match ownership decisions.

### Phase 3: Source Fact Emission

Work packets:

- WP2 Dataset Metadata.
- WP3 Family A Scorer Taxonomy.

Objective:

- Emit the row-level and scorer facts required by evaluator aggregation.

Exit criteria:

- Metadata coverage validates.
- Scorer subtype fixtures pass.
- Missing fact scenarios produce expected noncomputability.

### Phase 4: Family Aggregation

Work packets:

- WP6 Evaluator Aggregation.
- WP8 Validation Fixtures, aggregation and reconciliation coverage.

Objective:

- Emit and validate family summaries, governed sub-slice summaries, completeness state, current-run computability state, and noncomputability state.

Exit criteria:

- Family A, Family B1, and Family B2 summaries reconcile.
- Governed sub-slices cannot be replaced by parent aggregates.
- Partial and missing emissions are represented explicitly.

### Phase 5: Detector Consumption

Work packets:

- WP7 Detector Consumption.
- WP8 Validation Fixtures, detector non-inference coverage.

Objective:

- Enable detector consumption of emitted facts and states without detector-side reconstruction.

Exit criteria:

- Detector consumes only approved facts and states.
- Noncomputable and comparison-blocked states behave conservatively.
- Current active governance findings remain visible.

### Phase 6: Migration And Integration Review

Work packets:

- WP9 Migration Review.
- WP10 Integration And Audit Review.

Objective:

- Classify historical baselines, verify end-to-end behavior, and confirm readiness for later threshold-review eligibility.

Exit criteria:

- Migration classifications are recorded.
- Audit artifacts are preserved.
- Rollback paths are verified.
- Later threshold review remains separately gated.

## Critical-Path Work Packets

Critical-path packets:

- WP0 Implementation Entry Gate.
- WP8 Validation Fixtures.
- WP1 Schema Authoring.
- WP4 Family B1 Symbol-Name Ownership.
- WP5 Family B2 Anchor Ownership.
- WP2 Dataset Metadata.
- WP3 Family A Scorer Taxonomy.
- WP6 Evaluator Aggregation.
- WP7 Detector Consumption.

WP9 and WP10 become critical before historical comparison or threshold-review eligibility, but they do not block current-run family emission planning.

## Highest-Risk Work Packet

Highest-risk work packet: WP3 Family A Scorer Taxonomy.

Reason:

- Direct-answer substitution must remain a governed subtype without detector-time generated-text interpretation.
- The taxonomy must distinguish several close failure classes deterministically.
- Ambiguous subtype boundaries would undermine Family A aggregation and could recreate proxy behavior.

Secondary high-risk packets:

- WP5 Family B2 Anchor Ownership, because anchor classification can drift into prompt-text inference.
- WP4 Family B1 Symbol-Name Ownership, because small-denominator sub-slices are easy to obscure with parent aggregates.

## Earliest Implementation Candidate

Earliest implementation candidate: WP8 Validation Fixtures, followed by WP1 Schema Authoring.

Rationale:

- Fixtures can be authored without changing runtime behavior and can encode acceptance expectations before components emit new facts.
- Schema authoring should follow or proceed alongside fixture matrix approval so implementation has a stable target.
- Dataset, scorer, evaluator, and detector code should wait until the fixture and schema boundary is accepted.

## Recommendation For First Actual Implementation Phase

Recommended first actual implementation phase:

- Implement the Stage B validation fixture matrix and schema acceptance tests before modifying evaluator, scorer, detector, or threshold behavior.

Scope for that first phase:

- Add fixture scenarios for all approved families and states.
- Add validation expectations for complete, partial, missing, noncomputable, and comparison-blocked behavior.
- Keep runtime behavior unchanged.
- Do not enable detector consumption of redesigned metrics.
- Do not change thresholds or governance rules.

This creates the acceptance harness required for later schema and component implementation without weakening current conservative governance.
