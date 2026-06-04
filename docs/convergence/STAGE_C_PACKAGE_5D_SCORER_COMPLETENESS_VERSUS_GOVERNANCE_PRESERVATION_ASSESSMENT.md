# Stage C Package 5D Scorer Completeness Versus Governance Preservation Assessment

## Scope

This package assesses whether the current direct-answer subtype blocker for:

- `direct_answer_substitution_count`

is best explained as:

1. scorer implementation incompleteness;
2. governance-preserving missingness;
3. or a mixed condition.

This is explanatory assessment only.

It does not:

1. modify scorer behavior;
2. modify evaluator behavior;
3. assign new subtype labels;
4. perform readiness reassessment;
5. perform gate reassessment;
6. alter migration flags;
7. begin migration planning.

## Inputs

Existing doctrine and prior-surface inputs:

1. `docs/convergence/STAGE_C_PACKAGE_5A_DIRECT_ANSWER_SUBSTITUTION_SURFACE_ENTRY_ASSESSMENT.md`
2. `docs/convergence/STAGE_C_PACKAGE_5B_DIRECT_ANSWER_SUBSTITUTION_BLOCKER_PERSISTENCE_ASSESSMENT.md`
3. `docs/convergence/STAGE_C_PACKAGE_5C_DIRECT_ANSWER_SUBTYPE_COMPLETENESS_INVESTIGATION.md`
4. `docs/convergence/STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
5. `docs/convergence/STAGE_B_WP3_FAMILY_A_SCORER_EVIDENCE_CONTRACT.md`
6. `docs/convergence/STAGE_B_WP8C_FAMILY_A_SUBTYPE_BOUNDARY_REVIEW.md`
7. `docs/convergence/STAGE_B_WP8C_SCENARIO_TO_SUBTYPE_MAPPING.md`
8. `docs/convergence/STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`

Runtime and evidence inputs:

1. `evals/canonical_eval_manifest_v1.json`
2. `/tmp/stage_c_package5b_full_run_a/*`
3. `/tmp/stage_c_package5b_full_run_b/*`
4. `manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_a.json`
5. `manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_b.json`
6. `manifests/reports/stage_c_package5b_direct_answer_blocker_persistence_assessment.json`

Read-only implementation inputs:

1. `scripts/eval_canonical_manifest.py`
2. `scripts/stage_c1_evaluator_foundation.py`

## Current Surface Posture

Current state remains unchanged:

1. reconciliation: `requires_future_migration`
2. readiness: `migration-blocked`
3. gate: `gate-blocked`

Relevant Package 5C findings:

1. authoritative missing-evidence rows: `134`
2. structurally incapable rows under current doctrine and current emitted evidence: `131`
3. ambiguous mixed-output rows: `3`
4. clean direct-answer-only candidates: `0`
5. clean scalar-only candidates: `0`

## Missingness Justification Review

### Population-Level Justification

The current missing-evidence population is not uniform.

It separates into three explanatory slices:

| Slice | Count | Best explanation |
|---|---:|---|
| structurally incapable rows | 131 | governance-preserving missingness is justified by current doctrine and current emitted evidence |
| ambiguous mixed-output rows | 3 | missingness is justified today, but whether it is intrinsically required or only currently under-evidenced remains unresolved |
| clean dropped direct-answer / scalar rows | 0 | no runtime row shows an obvious missed governed subtype under current evidence |

### Justified Missingness

The `131` structurally incapable rows are justified as missing because the emitted outputs are primarily:

1. prompt echo;
2. transcript echo;
3. tool-label repetition;
4. imperative or policy-text repetition.

Those outputs do not provide clean scorer-owned evidence for:

1. answer-like substitution;
2. scalar-like substitution;
3. or clear missing-tool-call precedence over neighboring substitution categories.

Under the Family A doctrine, that is a valid reason to preserve missingness rather than fabricate subtype certainty.

### Missingness Attributable To Missing Scorer-Emitted Evidence

No row in the repeated full-run record demonstrates a clear dropped direct-answer-only or scalar-only subtype.

So current runtime evidence does not support the strong claim:

1. “the scorer had clean direct-answer evidence and failed to emit it”; or
2. “the scorer had clean scalar evidence and failed to emit it.”

However, code inspection shows a distinct pathway-level incompleteness:

1. the live authoritative emission function `_stage_c_family_a_declared_subtype` returns:
   - `wrong tool name`
   - `wrong argument`
   - `missing tool call`
   - `wrapper/envelope drift`
   - `malformed output`
   - or missing-evidence state
2. it contains no branch that emits:
   - `direct-answer substitution`
   - `scalar substitution`

This means there is implementation incompleteness at the subtype-path level even though the current frozen-corpus rows do not provide clean positive examples that would prove row-level false negatives.

### Unresolved Portion

The unresolved slice is the `3` ambiguous rows:

1. `heldout_validation:10`
2. `heldout_validation:28`
3. `heldout_validation:77`

Each begins with:

- `The first function name is: main`

and then spills into transcript echo.

Those rows do not justify detector-side or evaluator-side subtype inference.

But they also do not conclusively prove that missingness is the only possible scorer outcome under a richer approved scorer evidence pathway.

## Doctrine Preservation Review

### Detector-Side Inference Prevention

Current missingness is performing an intended governance function.

The doctrine requires:

1. detector must not inspect generated text to decide whether prose is a direct answer;
2. detector must not infer direct-answer substitution from no-call movement, invalid-json movement, or wrapper leakage;
3. detector must not classify scalar-looking output by shape alone.

Observed behavior is aligned:

1. authoritative Stage C artifacts preserve missing subtype evidence;
2. direct-answer counts are not reconstructed from generated output;
3. the legacy direct-answer count remains separate rather than being adopted as an authoritative scorer fact.

### Evaluator-Side Inference Prevention

The current evaluator-side Stage C path also preserves doctrine:

1. it emits `malformed output` only when invalid JSON still looks like a tool attempt;
2. otherwise it emits explicit missing evidence;
3. it does not use the legacy `direct_answer_substitution` heuristic to populate authoritative scorer evidence.

That is governance-preserving even when it is migration-blocking.

### Noncomputable-State Preservation

The current behavior preserves noncomputable states intentionally:

1. `134` non-exact tool-expected rows remain explicitly missing rather than being reassigned to a fallback subtype;
2. no `other` subtype is introduced;
3. authoritative direct-answer reconciliation therefore remains blocked instead of being fabricated.

### Ownership Boundary Preservation

Current ownership boundaries are preserved:

1. dataset metadata owns denominator and row identity facts;
2. scorer evidence owns subtype assignment or missing-evidence state;
3. evaluator aggregates emitted facts;
4. detector consumes legacy surfaces only and does not reinterpret missing scorer evidence.

## Scorer Completeness Review

### Contract Expectation

The Family A contract requires:

1. every eligible non-exact tool-expected row receives exactly one approved subtype or an explicit missing-evidence state;
2. direct-answer substitution and scalar substitution remain approved governed subtypes;
3. scorer evidence must be sufficient to distinguish neighboring subtypes or produce missing-evidence state.

### What The Current Scorer Path Supports

The current live authoritative emission path supports:

1. `wrong tool name`
2. `wrong argument`
3. `missing tool call`
4. `wrapper/envelope drift`
5. `malformed output`
6. explicit missing-evidence state

The Stage C1 contract layer can carry any approved subtype, including:

1. `direct-answer substitution`
2. `scalar substitution`

So the schema and contract are not the limiting factor.

### Apparent Completeness Gap

The completeness gap is that the current live emitter has no explicit direct-answer or scalar emission branch.

That supports the claim that at least one documented subtype pathway is currently unimplemented in the live authoritative scorer pathway.

Specifically:

1. the contract and doctrine require those subtypes to exist as governed possibilities;
2. the current live emission function never returns them;
3. instead, non-tool-attempt invalid outputs become missing-evidence rows.

### What Cannot Be Claimed From Current Evidence

Current evidence does not prove:

1. that the frozen corpus contains clean rows which the scorer should already have labeled direct-answer or scalar;
2. that the current scorer path is misclassifying an obvious direct-answer population.

So the current evidence supports:

1. pathway-level scorer incompleteness;
2. but not a demonstrated row-level false-negative population on this corpus.

## Ambiguous Row Review

### Observed Shape

The `3` ambiguous rows all:

1. expect `rg_search`;
2. begin with an answer-like statement;
3. then spill into transcript echo;
4. are counted by the legacy evaluator as `direct_answer_substitution`;
5. remain authoritative missing-evidence rows in Stage C.

### Attribution

The ambiguity appears:

1. doctrinal, because doctrine requires explicit evidence distinguishing answer substitution from neighboring failures before subtype assignment;
2. evidential, because the emitted outputs are mixed rather than clean;
3. secondarily implementation-related, because the current scorer path does not emit richer approved evidence that might separate primary failure modes.

### Assessment

These rows do not justify detector-side or evaluator-side subtype rescue.

But they do remain the best candidate slice for later scorer-completeness investigation, because they are the only rows that exhibit any answer-like content at all.

## Root-Cause Attribution

Recommended attribution:

- `mixed`

### Rationale

The blocker is not primarily implementation-driven in a simple sense because:

1. `131/134` blocked rows are well explained by governance-preserving missingness under the current evidence;
2. `0` clean direct-answer-only rows and `0` clean scalar-only rows were observed.

The blocker is not purely governance-preserving either because:

1. the approved direct-answer and scalar subtype pathways exist in doctrine and contract;
2. the live authoritative emission function does not currently emit either subtype;
3. the `3` ambiguous rows leave open the possibility that richer scorer evidence could matter.

So the correct explanation is mixed:

1. primarily governance-preserving at the observed row-population level;
2. but with a real scorer-completeness gap at the subtype-pathway level.

## Regimen Impact Assessment

### Immediate Implication

Future lifecycle work should remain focused on scorer completeness rather than on:

1. migration governance;
2. corpus coverage;
3. detector-side interpretation.

### Recommended Focus Order

The current evidence points to this future investigation order:

1. scorer completeness for direct-answer and scalar subtype pathways;
2. ambiguity handling for the `3` mixed-output rows;
3. only then any renewed readiness or gate work.

### What Does Not Need Reopening

Current evidence does not justify reopening:

1. denominator ownership doctrine;
2. detector non-inference doctrine;
3. evaluator missingness preservation behavior.

Those parts are functioning as intended.

## Determinations

1. Most current missingness is performing an intended governance-preserving function.
2. The current blocker is not explained by missing corpus coverage.
3. The live authoritative scorer pathway nonetheless appears incomplete for the approved direct-answer and scalar subtype branches.
4. The ambiguous-row slice is small, stable, and appropriate for future scorer-centered investigation.
5. Root-cause attribution is `mixed`, with governance preservation dominating the observed runtime population and scorer incompleteness remaining the decisive pathway-level limitation.
