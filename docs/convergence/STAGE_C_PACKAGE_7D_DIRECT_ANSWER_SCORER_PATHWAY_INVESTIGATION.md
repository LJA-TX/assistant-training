# Stage C Package 7D Direct Answer Scorer-Pathway Investigation

## Scope

This package executes the first authorized blocker-oriented branch transition investigation for:

- `direct_answer_substitution_count`

This is an investigation package.

It does not:

1. reassess authorization;
2. begin planning;
3. begin implementation;
4. modify scorer behavior;
5. modify evaluator behavior;
6. modify detector behavior;
7. modify threshold behavior;
8. alter migration flags;
9. reopen readiness;
10. reopen gate;
11. authorize planning or implementation.

## Inputs

Prior blocker-branch and transition inputs:

1. `docs/convergence/STAGE_C_PACKAGE_5C_DIRECT_ANSWER_SUBTYPE_COMPLETENESS_INVESTIGATION.md`
2. `docs/convergence/STAGE_C_PACKAGE_5D_SCORER_COMPLETENESS_VERSUS_GOVERNANCE_PRESERVATION_ASSESSMENT.md`
3. `docs/convergence/STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md`
4. `docs/convergence/STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md`
5. `docs/convergence/STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md`
6. `docs/convergence/STAGE_C_PACKAGE_7B_DIRECT_ANSWER_POST_BLOCKER_TRANSITION_FEASIBILITY_ASSESSMENT.md`
7. `docs/convergence/STAGE_C_PACKAGE_7C_POST_BLOCKER_TRANSITION_AUTHORIZATION_ASSESSMENT.md`

Doctrine and contract inputs:

8. `docs/convergence/STAGE_B_WP3_FAMILY_A_SCORER_EVIDENCE_CONTRACT.md`
9. `docs/convergence/STAGE_B_WP8C_SCENARIO_TO_SUBTYPE_MAPPING.md`
10. `docs/convergence/STAGE_B_WP8C_FAMILY_A_SUBTYPE_BOUNDARY_REVIEW.md`
11. `docs/convergence/STAGE_B_EVAL_REDESIGN_CONTRACTS.md`

Read-only implementation inputs:

12. `scripts/eval_canonical_manifest.py`
13. `scripts/stage_c1_evaluator_foundation.py`

Prior repeated-run evidence inputs:

14. `manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_a.json`
15. `manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_b.json`
16. `manifests/reports/stage_c_package5b_direct_answer_blocker_persistence_assessment.json`

## Current Context

Current direct-answer surface state remains unchanged:

1. reconciliation: `requires_future_migration`
2. readiness: `migration-blocked`
3. gate: `gate-blocked`

Current preserved blocker facts from Packages `5C` and `5D`:

1. `134` authoritative missing-evidence rows
2. `131` governance-preserving structurally incapable rows
3. `3` ambiguous mixed-output rows
4. `0` clean direct-answer-only rows
5. `0` clean scalar-only rows

Package `7C` already conditionally authorized this bounded scorer-pathway investigation.

This package answers the next narrower question:

1. where exactly does the live authoritative pathway fail to support the approved direct-answer and scalar subtype concepts;
2. who owns that gap;
3. whether the gap is theoretically closable without violating preservation boundaries.

## Scorer-Pathway Inventory

### Current Emitted Subtype Set

The Stage C1 contract layer allows the following approved Family A subtype set:

1. `direct-answer substitution`
2. `scalar substitution`
3. `malformed output`
4. `wrapper/envelope drift`
5. `missing tool call`
6. `wrong tool name`
7. `wrong argument`

The current live authoritative evaluator pathway emits only the following non-exact subtype outcomes:

1. `wrong tool name`
2. `wrong argument`
3. `missing tool call`
4. `wrapper/envelope drift`
5. `malformed output`
6. explicit missing-evidence state

The live pathway does not emit:

1. `direct-answer substitution`
2. `scalar substitution`

### Current Subtype Eligibility Logic

The active authoritative handoff is:

1. `_classify(row, prediction_text)`
2. `_stage_c_family_a_declared_subtype(classified)`
3. `_build_stage_c_family_a_record(stage_c1, row, classified)`
4. `stage_c1.emit_family_a_scorer_evidence(...)`

Observed live classifier behavior:

1. `_classify(...)` produces exact-valid or a protocol/tool-call failure class.
2. The non-exact class vocabulary is limited to:
   - `invalid_json`
   - `invalid_schema`
   - `wrapper_leakage`
   - `missing_tool_call`
   - `wrong_tool_name`
   - `wrong_arguments`
3. `_classify(...)` does not emit any scorer-owned evidence concept or primary class for:
   - answer-like substitution
   - scalar-like substitution

Observed subtype-mapping behavior:

1. `_stage_c_family_a_declared_subtype(...)` maps `wrong_tool_name`, `wrong_arguments`, `missing_tool_call`, and `wrapper_leakage` directly to approved Family A subtypes.
2. It maps `invalid_json` and some `invalid_schema` cases to:
   - `malformed output` when output still looks like a tool attempt; or
   - explicit missing-evidence when the output does not look like a tool attempt.
3. It contains no branch that returns:
   - `direct-answer substitution`
   - `scalar substitution`

### Current Missing-Evidence Handling

The live pathway currently uses explicit missing-evidence states rather than fallback subtype synthesis.

Observed missing-evidence reasons in the authoritative mapping layer:

1. `current canonical evaluator does not emit approved direct-answer or scalar substitution evidence`
2. `current canonical evaluator cannot distinguish schema-invalid tool omission from governed substitution categories`
3. `current canonical evaluator lacks approved Family A subtype evidence for this non-exact tool-expected row`

Observed repeated-run runtime behavior from Package `5B`:

1. the `134` blocked rows all carried reason `1`;
2. no direct-answer or scalar subtype was emitted;
3. the missing-evidence row set was stable across repeated full runs.

### Current Ownership Boundaries

Current authoritative ownership chain remains:

1. dataset metadata owns row identity, split, and tool-expected eligibility context;
2. scorer-owned Family A evidence owns subtype assignment or explicit missing-evidence state;
3. evaluator runtime carries the current scorer-pathway implementation and aggregates emitted facts;
4. detector and threshold consumers remain downstream legacy consumers only.

The evaluator is not authorized to reconstruct subtype evidence from generated text when scorer-owned evidence is absent.

### Current Handoff Points

The active handoff points are:

1. metadata and expected-tool facts enter `_classify(...)`
2. `_classify(...)` produces exact/non-exact and protocol/tool-attempt facts
3. `_stage_c_family_a_declared_subtype(...)` translates those facts into approved subtype or missing-evidence state
4. `stage_c1.emit_family_a_scorer_evidence(...)` enforces the contract-locked Family A output structure
5. downstream governance and reconciliation packages consume the emitted Family A artifact

The direct-answer completeness gap therefore sits before or inside subtype declaration, not in downstream consumption.

## Pathway-Level Completeness Investigation

### Repository-Supported Explanation

The strongest repository-supported explanation is:

- the subtype contract exists, but the live authoritative scorer pathway never emits the evidence required to reach `direct-answer substitution` or `scalar substitution`

This is more precise than a generic statement of incompleteness.

The gap is specifically:

1. the contract layer is capable of carrying both subtypes;
2. the live classifier does not produce answer-like or scalar-like substitution evidence classes;
3. the live subtype mapper therefore cannot emit those subtypes;
4. the pathway falls back to explicit missing-evidence rather than legacy heuristic classification.

### Contract Support Exists

Contract and doctrine evidence already support the subtype concepts:

1. WP3 contract requires answer-like substitution evidence for `direct-answer substitution`.
2. WP3 contract requires scalar-like substitution evidence for `scalar substitution`.
3. WP8-C boundary review preserves both as approved Family A subtypes.
4. WP8-C mapping defines complete, partial, missing, and non-inference scenarios for both subtype areas.
5. Stage C1 contract validation allows both subtype strings as approved outputs.

So the gap is not:

1. a missing schema field;
2. a prohibited subtype name;
3. a doctrine-level ban on direct-answer or scalar subtype emission.

### Live Path Is Unreachable For These Subtypes

The live authoritative path is currently unreachable for direct-answer and scalar subtype emission because:

1. `_classify(...)` partitions failures by parse, schema, tool-call presence, tool identity, and argument match.
2. It does not represent:
   - answer-like substitution evidence;
   - scalar-like substitution evidence;
   - precedence evidence between direct-answer, scalar, malformed output, and missing tool call.
3. `_stage_c_family_a_declared_subtype(...)` only consumes the limited protocol/tool-call class vocabulary above.
4. When a response is invalid or schema-invalid without a recognizable tool attempt, the pathway emits missing-evidence rather than a governed substitution subtype.

The most accurate characterization is:

- the approved subtypes are representable but currently unreachable in the live authoritative path

### Legacy Heuristic Exists But Is Not Part Of The Authoritative Path

The repository still contains legacy heuristic classification in `_failure_subtype(...)`.

That legacy path:

1. classifies bare numeric or boolean-like invalid outputs as `scalar_substitution`;
2. classifies other non-tool invalid outputs as `direct_answer_substitution`.

But that logic is used only for legacy preaggregation labels and `failure_profile`, not for authoritative Family A scorer evidence.

This distinction matters because the current blocker is not:

1. absence of any repository logic touching the concept;
2. inability to name the concept;
3. inability to represent the concept in schema.

The blocker is that the authoritative Stage C pathway intentionally does not reuse the legacy generated-text heuristic as scorer-owned subtype evidence.

### Gap Classification

The pathway-level completeness gap is best classified as:

1. contract-path mismatch;
2. subtype representability without live reachability;
3. scorer-owned evidence-production gap rather than detector, threshold, or metadata gap.

## Ownership And Authority Investigation

### Scorer Ownership

Resolution authority for the missing capability is scorer-owned.

Why scorer-owned:

1. WP3 contract assigns answer-like substitution evidence and scalar-like substitution evidence to the scorer.
2. WP8-C boundary doctrine requires scorer evidence to distinguish direct-answer, scalar, malformed output, and missing tool call.
3. Detector is explicitly forbidden from generated-text classification for these subtypes.

### Evaluator Ownership

The current evaluator implementation owns the runtime carrier site of the scorer pathway, but not the governance authority to invent missing subtype evidence.

The evaluator currently owns:

1. active classifier structure;
2. active subtype mapping function;
3. aggregation of emitted Family A records.

The evaluator does not own:

1. detector-side fallback classification;
2. permission to reconstruct scorer evidence from generated text;
3. authority to collapse ambiguous rows into direct-answer or scalar subtypes without scorer-supported evidence.

### Metadata Ownership

Dataset metadata does not own the missing capability.

Reason:

1. row identity, split membership, and tool-expected eligibility are already present;
2. the current gap is not absence of denominator ownership;
3. the current gap is subtype-specific evidence production, not row-population declaration.

### Contract And Doctrine Ownership

Contract and doctrine already define the permissible shape of the capability:

1. approved subtype set exists;
2. missing-evidence handling exists;
3. detector non-inference rules exist;
4. ambiguity handling rules exist.

So contract ownership does not currently appear to be the blocking missing authority.

The blocking missing capability is inside the live scorer-pathway realization of those already-approved concepts.

## Preservation Compatibility Investigation

### Governance-Preserving Missingness

The identified gap could theoretically be closed without violating governance-preserving missingness, but only if any future work remains limited to scorer-owned evidence production and approved subtype declaration.

Why compatible in principle:

1. the Family A contract already allows explicit missing-evidence states when subtype evidence is insufficient;
2. the approved subtype taxonomy already distinguishes direct-answer and scalar substitution from neighboring subtypes;
3. the contract does not require every current missing-evidence row to become classifiable.

So future closure of the pathway gap does not inherently require elimination of missingness.

### Non-Inference Doctrine

Any future closure must preserve non-inference doctrine.

That means:

1. no detector-side prose interpretation;
2. no evaluator-side generated-text reconstruction in place of scorer evidence;
3. no reuse of legacy `_failure_subtype(...)` as authoritative subtype assignment without scorer-owned evidence justification.

Compatibility conclusion:

- a legitimate pathway could exist only if it remains scorer-owned and does not convert detector or evaluator into inference engines

### Ambiguous-Row Preservation

The current `3` ambiguous rows remain preserved.

This investigation found no repository evidence that justifies reclassifying them now.

Any future pathway would still need to preserve:

1. subtype missingness when answer-like and transcript/tool-attempt evidence remain mixed;
2. noncomputability when scorer evidence cannot resolve direct-answer versus scalar versus malformed versus missing-tool-call precedence.

### Governance-Preserving Structurally Incapable Rows

The current `131` structurally incapable rows also remain preserved.

This investigation found no repository evidence that converts them into clean direct-answer or scalar positives.

So theoretical pathway closure is preservation-compatible only if it allows:

1. some rows to remain missing forever;
2. the current `131` rows to remain governance-preserving missing unless scorer-owned evidence materially changes;
3. the `3` ambiguous rows to remain ambiguous unless scorer-owned evidence materially changes.

## Investigation Success Criteria

Before a future planning-authorization package could be justified, the following would need to be true:

1. the target gap is bounded to the direct-answer/scalar scorer-pathway rather than broad detector or evaluator redesign;
2. ownership is clear that any missing capability is scorer-owned, with evaluator acting only as the runtime carrier;
3. contract compatibility is clear that direct-answer and scalar subtypes are already approved and representable;
4. preservation compatibility is clear that future work can leave the `131` structurally incapable rows and `3` ambiguous rows missing unless new scorer-owned evidence supports otherwise;
5. the future target can be described without relying on detector inference, evaluator reconstruction, or legacy fallback promotion;
6. the expected outcome of any future work remains investigation-to-planning scoped rather than implicit migration work.

## Investigation Failure Criteria

The following findings would indicate that no legitimate forward pathway exists or that planning would remain unjustified:

1. the only way to produce direct-answer or scalar subtype records would be detector-side or evaluator-side generated-text inference;
2. the pathway would require doctrine expansion before even bounded planning could be described;
3. the pathway would require forced relabeling of the `131` governance-preserving rows or `3` ambiguous rows absent new scorer-owned evidence;
4. the gap cannot be localized more narrowly than a generalized scorer redesign with no bounded target;
5. future investigation cannot produce any additional decision-relevant evidence beyond what Packages `5C`, `5D`, `7B`, and `7C` already established.

## Handoff Determination

Handoff determination:

- future planning-authorization consideration appears justified

Why this threshold is met:

1. a bounded target now exists at the scorer-pathway handoff level;
2. ownership is clear enough to distinguish scorer responsibility from evaluator, metadata, detector, and threshold responsibilities;
3. contract and doctrine already support the subtype concepts;
4. preservation constraints are understood and appear maintainable;
5. the live gap is now localized enough to investigate or plan without reopening readiness, gate, or migration questions.

This package does not authorize planning.

It only determines that future planning-authorization consideration is now meaningful rather than premature.

## First Post-Blocker Transition Record Assessment

This package does constitute the repository's first actual blocker-oriented branch transition investigation record.

Why:

1. Package `7C` authorized a bounded investigation class;
2. Package `7D` is the first package to execute that authorization rather than reassess it;
3. the package moves beyond blocker persistence and characterization into pathway localization and ownership analysis.

### New Evidence Obtained

New evidence established here:

1. the live authoritative gap is localized to the scorer-pathway handoff between `_classify(...)` and `_stage_c_family_a_declared_subtype(...)`;
2. the Stage C1 contract layer already supports `direct-answer substitution` and `scalar substitution`;
3. legacy direct-answer/scalar logic exists, but only in the non-authoritative legacy preaggregation path;
4. the current blocker is therefore not a doctrine prohibition or schema deficiency;
5. a theoretically preservable forward path exists only through scorer-owned pathway completeness, not detector or evaluator reconstruction.

### What Remains Unknown

Still unknown:

1. whether any future scorer-owned pathway on the current frozen corpus would emit a non-zero governed direct-answer or scalar population;
2. whether the `3` ambiguous rows could ever become classifiable under approved scorer evidence;
3. whether any future bounded pathway target would remain narrow enough for planning without broad scorer redesign concerns.

## Regimen Impact Assessment

This investigation contributes the following new regimen evidence:

1. blocker-oriented branch now has an actual post-blocker transition investigation record, not only feasibility and authorization records;
2. the blocker-oriented branch is now evidenced through:
   - entry;
   - persistence;
   - characterization;
   - preservation-versus-completeness attribution;
   - transition-feasibility review;
   - transition-authorization review;
   - transition-execution investigation;
3. reusable-regimen maturity improves because the repository now has one example of blocker-branch movement beyond static blocked-state preservation.

This does not close the branch-level evidence gap for:

1. a second blocker-oriented surface family; or
2. a realized post-blocker planning or implementation transition.

But it materially strengthens the blocker-oriented branch as a reusable regimen component by showing that transition investigation can occur without violating preservation boundaries.

## Investigation Conclusion

The direct-answer completeness gap is best explained as:

1. contract-level support exists;
2. live authoritative pathway support is incomplete;
3. the incomplete portion is scorer-owned and currently unreachable in the runtime mapping path;
4. preservation-compatible forward consideration is plausible, but only under later explicit planning authorization.

That makes the current blocker:

- still blocked for migration purposes;
- newly localized for future planning-authorization consideration;
- and now supported by the repository's first actual post-blocker transition investigation record.
