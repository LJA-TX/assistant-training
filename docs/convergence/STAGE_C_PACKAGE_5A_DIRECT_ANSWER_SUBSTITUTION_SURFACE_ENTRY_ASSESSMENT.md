# Stage C Package 5A Direct Answer Substitution Surface Entry Assessment

## Scope

This package assesses whether:

- `direct_answer_substitution_count`

is positioned to become the next active surface for reuse of the extracted Stage C migration regimen on the current frozen canonical corpus.

This is an entry assessment only.

It does not:

1. perform readiness reassessment;
2. perform gate reassessment;
3. modify detector behavior;
4. modify threshold behavior;
5. alter migration flags;
6. begin migration planning.

## Inputs

Current surface-state and regimen inputs:

1. `docs/convergence/STAGE_C_PACKAGE_1A_RUNTIME_VALIDATION_REPORT.md`
2. `docs/convergence/STAGE_C_PACKAGE_1C_RUNTIME_VALIDATION_REPORT.md`
3. `docs/convergence/STAGE_C_PACKAGE_1C_PASSIVE_RECONCILIATION_RATIONALE.md`
4. `docs/convergence/STAGE_C_PACKAGE_1D_RUNTIME_VALIDATION_REPORT.md`
5. `docs/convergence/STAGE_C_PACKAGE_1D_MIGRATION_READINESS_TAXONOMY_RATIONALE.md`
6. `docs/convergence/STAGE_C_PACKAGE_1E_CURRENT_SURFACE_GATE_ASSESSMENT.md`
7. `docs/convergence/STAGE_C_PACKAGE_3C_REGIMEN_RETROSPECTIVE_AND_REUSABILITY_ASSESSMENT.md`
8. `docs/convergence/STAGE_C_PACKAGE_4A_SECOND_SURFACE_SELECTION_AND_REGIMEN_APPLICABILITY_ASSESSMENT.md`
9. `docs/convergence/STAGE_C_PACKAGE_4B_B1_GOVERNED_MEMBERSHIP_COVERAGE_QUALIFICATION.md`
10. `docs/convergence/STAGE_C_PACKAGE_4C_B1_EVIDENCE_ACQUISITION_FEASIBILITY_ASSESSMENT.md`
11. `manifests/reports/stage_c_package2a_read_file_exact_valid_gate_evidence_run_a.json`
12. `manifests/reports/stage_c_package2a_read_file_exact_valid_gate_evidence_run_b.json`

Doctrine, contract, and migration-gate inputs:

1. `docs/convergence/STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
2. `docs/convergence/STAGE_B_EVAL_REDESIGN_METRIC_INVENTORY.md`
3. `docs/convergence/STAGE_B_WP3_FAMILY_A_SCORER_EVIDENCE_CONTRACT.md`
4. `docs/convergence/STAGE_B_WP8C_FAMILY_A_SUBTYPE_BOUNDARY_REVIEW.md`
5. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_IMPLEMENTATION_GATE.md`
6. `docs/convergence/STAGE_C9C_BASELINE_DELTA_COMPARABILITY_CLOSURE_DETERMINATION.md`
7. `docs/convergence/STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md`

Runtime and corpus-carrier inputs:

1. `manifests/reports/stage_b_v1_threshold_profile.json`
2. `scripts/post_eval_collapse_detector.py`
3. `scripts/eval_canonical_manifest.py`
4. `scripts/stage_c1_evaluator_foundation.py`
5. `scripts/stage_c8_non_authoritative_detector_projection_adapter.py`
6. `evals/canonical_eval_manifest_v1.json`
7. `evals/data/canonical_v1/heldout_validation.jsonl`
8. `evals/data/canonical_v1/tool_holdout.jsonl`
9. `evals/data/canonical_v1/no_call.jsonl`
10. `evals/data/canonical_v1/adversarial.jsonl`
11. `evals/data/canonical_v1/direct_answer.jsonl`

## Current Surface Inventory

### Current State Table

| Surface field | Current repository state |
|---|---|
| Metric identity | `direct_answer_substitution_count` |
| Legacy metric path | `failure_profile.failure_categories_non_exact_tool_rows.direct_answer_substitution` |
| Detector consumption | profile-driven legacy detector resolves `metric_id = direct_answer_substitution_count` from the threshold profile metric catalog |
| Threshold consumption | tradeoff watch rule `direct_answer_substitution_delta_gt_3` |
| Threshold basis | `delta_vs_baseline` |
| Baseline policy | `missing_baseline_policy = fail_fast` |
| Current reconciliation status | `requires_future_migration` |
| Current readiness status | `migration-blocked` |
| Current gate status | `gate-blocked` |
| Current authoritative detector wiring | not wired; only legacy detector path is authoritative |
| Current Stage C detector preparation | non-authoritative adapter path exists, but authoritative migration remains disabled |

### Surface Notes

The repository evidence is consistent on one point that matters for entry assessment:

1. the surface remains blocked for migration;
2. the blocker is explicit and preserved in authoritative artifacts;
3. the blocker is not caused by missing corpus coverage in the way that blocked B1 symbol-membership reuse.

Package 1C records:

1. reconciliation status `requires_future_migration`;
2. authoritative value:
   - `direct_answer_substitution_count = 0`
   - `non_exact_tool_expected_row_count = 6`
   - `missing_evidence_row_ids = 5`
3. reason: `authoritative_family_a_subtype_surface_incomplete`.

Package 1D carries that forward as:

1. readiness `migration-blocked`;
2. blocker class: preserved scorer missing-evidence rows.

Package 1E then classifies the surface as:

1. `gate-blocked`;
2. with the additional active baseline-delta migration concern still present in detector-gate doctrine.

## Evidence Availability Review

### Frozen Corpus Eligibility Shape

The frozen canonical corpus contains:

1. `100` tool-positive rows in `heldout_validation`;
2. `40` tool-positive rows in `tool_holdout`;
3. `20` `no_call_direct` rows in `no_call`;
4. `20` `adversarial_malformed` rows in `adversarial`;
5. `20` `direct_answer_eval` rows in `direct_answer`.

Only the `heldout_validation` and `tool_holdout` tool-positive rows carry canonical assistant tool-call targets.

That means the current frozen row set already contains:

1. `140` tool-expected rows for Family A governed subtype review;
2. a complete current-run tool-positive population on which the direct-answer substitution concept can be assessed;
3. direct-answer-named split rows that are not part of the governed Family A eligible denominator.

This last point is surface-specific and important:

1. the governed concept represented by `direct_answer_substitution_count` is not computed from the `direct_answer` split;
2. under current doctrine, direct-answer/no-call/adversarial rows remain outside Family A unless explicitly marked tool-expected in a future design;
3. the current governed population is the non-exact subset of the `140` tool-positive rows.

### Scorer Evidence Availability

Scorer-evidence availability is present.

The live Stage C artifact path already emits Family A scorer evidence records with:

1. `row_id`;
2. `tool_expected_eligibility`;
3. `primary_outcome`;
4. `exact_valid`;
5. `non_exact_tool_expected`;
6. `subtype_assignment`;
7. `missing_evidence`;
8. `missing_evidence_reasons`;
9. `failure_taxonomy_marker`;
10. `scorer_semantics_marker`.

The current full-run evidence in the Package 2A bundles shows that this emission is stable on the frozen manifest:

1. run A `family_a_tool_expected_population_count = 140`;
2. run B `family_a_tool_expected_population_count = 140`;
3. run A `family_a_missing_evidence_count = 134`;
4. run B `family_a_missing_evidence_count = 134`;
5. row-identity uniqueness and Family A row-to-row-fact linkage both remain true in runs A and B.

### Subtype Evidence Availability

Subtype evidence availability is partial rather than absent.

The approved subtype set exists in doctrine and in the Stage C contract validator, including:

1. `direct-answer substitution`;
2. `scalar substitution`;
3. `malformed output`;
4. `wrapper/envelope drift`;
5. `missing tool call`;
6. `wrong tool name`;
7. `wrong argument`.

But the current live canonical evaluator intentionally emits conservative subtype coverage.

Current evaluator behavior:

1. wrong tool name, wrong argument, missing tool call, wrapper/envelope drift, and some malformed-output cases can be emitted;
2. invalid-json or schema-invalid outputs that do not support an approved governed distinction remain `missing_evidence`;
3. the evaluator explicitly does not emit approved direct-answer or scalar substitution evidence from generated text heuristics.

This means the surface has subtype infrastructure now, but not subtype completeness now.

### Denominator Visibility

Denominator visibility exists and is sufficient to begin the lifecycle.

The Family A contract already requires visibility over:

1. total eligible tool-expected rows;
2. total non-exact eligible tool-expected rows.

The current authoritative artifact stack exposes those views:

1. Package 1B governance consumption reports Family A tool-expected population;
2. Package 1C and Package 1D expose `non_exact_tool_expected_row_count` in direct-answer surface support;
3. missing-evidence rows remain individually visible rather than being silently excluded.

The current legacy surface is weaker:

1. it is a raw count consumed through a delta-vs-baseline threshold rule;
2. denominator meaning is implicit in the legacy path and explicit in the Stage C path.

That is a later migration hazard, but it is not an entry blocker.

### Ownership Visibility

Ownership visibility is present.

Current doctrine and current artifacts already preserve:

1. dataset metadata ownership of tool-expected eligibility and expected tool behavior;
2. scorer ownership of subtype assignment or missing-evidence state;
3. evaluator ownership of aggregation;
4. detector consumer-only posture.

This is the key difference from the deferred B1 surface:

1. B1 lacked the governed source evidence itself;
2. this Family A surface already has the governed ownership chain in place on the frozen corpus;
3. what is missing is subtype completeness, not ownership provenance.

### Noncomputable And Missing-State Handling

Noncomputable and missing-state handling is already live and doctrine-compliant.

Observed current behavior:

1. no fallback subtype synthesis;
2. ambiguous direct-answer/scalar/malformed boundaries remain `missing_evidence`;
3. readiness consumes that blocker directly and marks the surface `migration-blocked`;
4. gate assessment consumes that blocker directly and marks the surface `gate-blocked`.

This means the surface already exercises one of the key regimen behaviors:

1. preserved missingness;
2. preserved blocked state;
3. no detector-time repair.

## Lifecycle Entry Assessment

### Entry Classification

- `ready for regimen entry`

### Rationale

This classification does not mean:

1. `migration-ready`;
2. `gate-open`;
3. planning-authorized;
4. migration-authorized.

It means the minimum authoritative infrastructure needed to start the regimen on the current frozen corpus already exists.

Why the surface is entry-ready:

1. the frozen corpus already contains the relevant governed evaluation population;
2. authoritative Stage C row identity is stable on that row set;
3. scorer-evidence artifacts already emit the governed Family A fields needed for lifecycle assessment;
4. ownership boundaries are explicit and already preserved;
5. missingness and blocked states are already directly observable;
6. the current blocker is explicit authoritative evidence, not missing source coverage.

Why the surface is not `evidence-constrained` for entry:

1. unlike the deferred B1 symbol-membership surface, the required authoritative artifact classes already exist on the frozen corpus;
2. the problem is not that the corpus fails to instantiate the governed concept at all;
3. the problem is that the current authoritative scorer surface preserves incomplete subtype evidence, which is precisely a lifecycle-valid blocker state.

Why the surface is not `doctrine-constrained` for entry:

1. doctrine already defines the Family A subtype taxonomy;
2. doctrine already defines scorer ownership and missing-evidence handling;
3. doctrine already permits the governed concept on the current tool-positive population.

Why the surface is not `blocked` for entry:

1. the surface is blocked for migration;
2. it is not blocked from entering the regimen as a blocker-oriented stress test.

## Hazard Inventory

### Hazard 1: Subtype Completeness

Current authoritative evidence still preserves large missing-evidence coverage for Family A.

This is the primary surface hazard because:

1. `direct-answer substitution` is a scorer-owned governed subtype;
2. the current live evaluator does not emit approved direct-answer or scalar-substitution evidence for ambiguous answer-like outputs;
3. the surface therefore begins from an explicit completeness blocker rather than an aligned authoritative count.

### Hazard 2: Scorer-Authority Strictness

Detector and threshold consumers must not classify generated text to repair subtype gaps.

This hazard is unique relative to the completed `read_file_exact_valid_rate` path because:

1. the completed surface depended on exact-valid aggregation;
2. this surface depends on scorer-owned subtype interpretation;
3. any attempt to shortcut scorer completeness would violate ownership doctrine immediately.

### Hazard 3: Surface Name Versus Eligible Population

The surface name suggests the `direct_answer` split, but the governed concept currently lives on tool-positive non-exact rows.

This creates a lifecycle hazard because:

1. readers can incorrectly assume the dedicated `direct_answer` split supplies the governed numerator or denominator;
2. under current doctrine, it does not;
3. split-scope and denominator documentation therefore matter more here than on the completed read-file aggregate surface.

### Hazard 4: Baseline-Delta Coupling

This is the only active compatibility-bearing surface consumed by a delta-vs-baseline threshold rule.

Repository evidence records:

1. one active delta rule: `direct_answer_substitution_delta_gt_3`;
2. basis: `delta_vs_baseline`;
3. baseline policy: `fail_fast`;
4. current detector-gate doctrine: contract-defined but still blocked in the current run.

This makes baseline comparability part of the surface lifecycle much earlier than it was for `read_file_exact_valid_rate`.

### Hazard 5: Count Versus Denominator Semantics

The legacy detector consumes a raw count, while the redesigned Family A contract requires both:

1. eligible tool-expected denominator;
2. non-exact eligible denominator.

This is not a doctrinal mismatch, but it is a migration hazard because:

1. historical detector semantics are count-and-delta oriented;
2. authoritative Stage C semantics are concept-and-denominator aware;
3. later migration work would need to preserve the count concept while respecting the richer denominator-bearing authoritative surface.

### Hazard 6: Detector Coupling

Current authoritative Stage C evidence is not wired into the authoritative detector path.

Only the following exist now:

1. legacy detector consumption through `failure_profile`;
2. non-authoritative Stage C adapter preparation;
3. a blocked baseline-delta gate record.

This means the surface can enter the regimen now, but the detector-facing portion of the lifecycle is expected to remain blocked for longer than it did on the first surface.

## Regimen Applicability Review

### Reusable Regimen Components

The following regimen elements should reuse cleanly without doctrine redesign:

1. authoritative row identity discipline from Package 1A;
2. passive governance consumption from Package 1B;
3. passive reconciliation framing from Package 1C;
4. readiness taxonomy from Package 1D;
5. gate taxonomy from Package 1E;
6. detector-impact and threshold-impact review structure;
7. rollback review structure;
8. authorization review structure;
9. migration-planning blueprint structure, if the surface ever reaches that point.

### Surface-Specific Treatment Likely Required

The following parts are expected to require direct-answer-specific handling:

1. Family A subtype completeness review;
2. direct-answer versus scalar versus malformed boundary evidence review;
3. explicit blocked-state persistence review rather than immediate alignment search;
4. baseline-delta comparability and baseline artifact requirements;
5. split-scope clarification showing that the dedicated `direct_answer` split is not the governed eligible population.

### New Regimen Behaviors This Surface Would Exercise

If this surface becomes active, the extracted regimen would be tested on behaviors that the completed read-file aggregate path did not cover:

1. scorer-owned governed subtype completeness rather than simple exact-valid aggregation;
2. preserved missing-evidence rows as a primary lifecycle input;
3. blocked-state traversal rather than near-aligned traversal;
4. delta-vs-baseline detector coupling instead of absolute-threshold-only coupling.

## Recommendation

Recommended next active regimen-validation surface:

- `direct_answer_substitution_count`

### Recommendation Rationale

The recommendation is yes.

This surface should become the next active regimen-validation surface because:

1. the originally preferred B1 symbol-name surface is currently deferred by genuinely absent governed corpus evidence;
2. the direct-answer surface already has a live authoritative artifact path on the frozen corpus;
3. the current blocker is explicit, preserved, and doctrine-compliant;
4. advancing to this surface would test whether the regimen is reusable not only for near-aligned surfaces, but also for blocker-heavy scorer-owned surfaces.

Recommended interpretation of that decision:

1. treat the surface as an active blocker-oriented stress test, not as a near-term migration candidate;
2. expect early regimen work to focus on blocker persistence, subtype completeness evidence, and baseline-delta coupling;
3. do not treat entry readiness as any change to current `migration-blocked` or `gate-blocked` state.

## Boundary Confirmation

This assessment does not:

1. perform readiness reassessment;
2. perform gate reassessment;
3. modify detector behavior;
4. modify threshold behavior;
5. alter migration flags;
6. begin migration planning.
