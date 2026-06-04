# Stage C Package 5C Direct Answer Subtype Completeness Investigation

## Scope

This package investigates the authoritative subtype incompleteness affecting:

- `direct_answer_substitution_count`

The goal is blocker characterization only.

It does not:

1. assign new subtype labels;
2. modify scorer behavior;
3. modify evaluator behavior;
4. perform readiness reassessment;
5. perform gate reassessment;
6. alter migration flags;
7. create replacement metrics;
8. begin migration planning.

## Inputs

Existing doctrine and surface-state inputs:

1. `docs/convergence/STAGE_C_PACKAGE_1C_RUNTIME_VALIDATION_REPORT.md`
2. `docs/convergence/STAGE_C_PACKAGE_1D_MIGRATION_READINESS_TAXONOMY_RATIONALE.md`
3. `docs/convergence/STAGE_C_PACKAGE_1E_CURRENT_SURFACE_GATE_ASSESSMENT.md`
4. `docs/convergence/STAGE_C_PACKAGE_5A_DIRECT_ANSWER_SUBSTITUTION_SURFACE_ENTRY_ASSESSMENT.md`
5. `docs/convergence/STAGE_C_PACKAGE_5B_DIRECT_ANSWER_SUBSTITUTION_BLOCKER_PERSISTENCE_ASSESSMENT.md`
6. `docs/convergence/STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
7. `docs/convergence/STAGE_B_WP3_FAMILY_A_SCORER_EVIDENCE_CONTRACT.md`
8. `docs/convergence/STAGE_B_WP8A_SCENARIO_CATALOG.md`
9. `docs/convergence/STAGE_B_WP8C_SCENARIO_TO_SUBTYPE_MAPPING.md`
10. `docs/convergence/STAGE_B_WP8C_FAMILY_A_SUBTYPE_BOUNDARY_REVIEW.md`
11. `docs/convergence/STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`

Runtime and evidence inputs:

1. `evals/canonical_eval_manifest_v1.json`
2. `/tmp/stage_c_package5b_full_run_a/*`
3. `/tmp/stage_c_package5b_full_run_b/*`
4. `manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_a.json`
5. `manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_b.json`
6. `manifests/reports/stage_c_package5b_direct_answer_blocker_persistence_assessment.json`

Implementation inputs reviewed read-only:

1. `scripts/eval_canonical_manifest.py`
2. `scripts/stage_c1_evaluator_foundation.py`

## Current Surface Posture

Current state remains unchanged:

1. reconciliation: `requires_future_migration`
2. readiness: `migration-blocked`
3. gate: `gate-blocked`

Package 5B already established that this blocker is strongly reproducible.

Package 5C addresses the next question:

1. what kind of subtype incompleteness is present;
2. whether the missing subtype evidence is primarily doctrinal, evidentiary, implementation-driven, or mixed.

## Missing-Evidence Population Inventory

### Stable Population Counts

Observed from both repeated full runs:

| Surface slice | Count |
|---|---:|
| tool-expected population | 140 |
| non-exact tool-expected population | 140 |
| subtype-assigned population | 6 |
| authoritative direct-answer subtype population | 0 |
| authoritative missing-evidence population | 134 |
| legacy direct-answer count | 125 |

### Split Distribution

Observed missing-evidence split distribution:

| Split | Missing-evidence rows |
|---|---:|
| `heldout_validation` | 94 |
| `tool_holdout` | 40 |

No blocker rows were observed in:

1. `adversarial`
2. `direct_answer`
3. `no_call`

Those splits are not tool-positive Family A denominator members for this surface.

### Row-Family Distribution

Observed missing-evidence distribution by expected primary tool:

| Expected primary tool | Missing-evidence rows |
|---|---:|
| `rg_search` | 46 |
| `read_file` | 27 |
| `find_files` | 12 |
| `debug_tools` | 7 |
| `check_service_health` | 6 |
| `get_system_datetime` | 6 |
| `archive_create` | 4 |
| `write_file` | 3 |
| `run_command` | 3 |
| `copy_path` | 3 |
| `archive_extract` | 3 |
| `stat_path` | 2 |
| `apply_unified_diff` | 2 |
| each of `list_tools`, `service_control`, `git_status`, `git_diff`, `test_run`, `get_system_version`, `json_edit`, `sha256_file`, `http_request`, `list_active_ports` | 1 each |

The blocker is therefore not a single-tool anomaly.

### Relevant Scorer-Owned Characteristics

Every missing-evidence row shared the same authoritative scorer-evidence pattern:

1. `tool_expected_eligibility = true`
2. `non_exact_tool_expected = true`
3. `exact_valid = false`
4. `primary_outcome = invalid_json`
5. `missing_evidence = true`
6. `missing_evidence_reason = current canonical evaluator does not emit approved direct-answer or scalar substitution evidence`

Observed parse-side characteristics in the paired comparison rows:

1. `parse_mode = invalid`
2. `schema_reason = payload_not_parsed`

No missing-evidence row carried:

1. `direct-answer substitution`
2. `scalar substitution`
3. `missing tool call`
4. `wrong tool name`
5. `wrong argument`
6. `wrapper/envelope drift`

The only assigned subtype on non-exact tool-expected rows was `malformed output`, and only for `6` rows that contained explicit tool-attempt markers.

## Subtype Opportunity Analysis

This section is investigative only.

It does not create new governed subtypes.

It classifies the observed missing-evidence outputs by whether their current emitted structure appears capable of supporting approved direct-answer or scalar evidence under the current doctrine.

### Investigative Opportunity Counts

| Investigative category | Count | Rationale |
|---|---:|---|
| structurally capable of clean direct-answer substitution | 0 | no missing-evidence row emitted a clean answer-only prose response without transcript or instruction echo |
| structurally capable of clean scalar substitution | 0 | no missing-evidence row emitted a bare numeric / boolean / null / scalar-only payload |
| structurally incapable under current doctrine | 131 | rows were prompt echo, transcript echo, or tool/instruction repetition rather than readable substitution evidence |
| ambiguous boundary | 3 | rows began with an answer-like line and then spilled into transcript echo, leaving subtype boundaries mixed rather than explicit |

### Observed Structural Shapes

Observed first-line structural distribution inside the `134` missing-evidence rows:

| First-line shape | Count |
|---|---:|
| instructional echo first | 100 |
| transcript marker first (`[SYSTEM]` / `[USER]`) | 9 |
| answer-like first | 3 |
| other echoed imperative / policy text first | 22 |

Representative structurally incapable rows:

1. `heldout_validation:1`
   - starts by repeating the task prompt, then emits transcript markers
2. `heldout_validation:11`
   - repeats `Tool: python` rather than emitting a readable substitution answer
3. `heldout_validation:50`
   - repeats the tool instruction payload and then spills into transcript text

Representative ambiguous rows:

1. `heldout_validation:10`
2. `heldout_validation:28`
3. `heldout_validation:77`

All three ambiguous rows begin with:

- `The first function name is: main`

but then continue with `[SYSTEM]` and `[USER]` transcript echo.

Under the approved Family A boundary doctrine, these rows are not clean direct-answer facts.

They are mixed outputs whose governing subtype cannot be safely assigned without scorer-owned approved evidence.

### Implication

The missing-evidence population is not primarily a suppressed set of clean direct answers or clean scalar substitutions.

It is primarily a population of:

1. prompt/transcript echo artifacts; plus
2. a very small mixed-output ambiguity slice.

## Blocker Taxonomy

### Category A: Scorer-Output Incompleteness

Observed blocker category:

1. the current Stage C Family A pathway emits `malformed output` when invalid JSON still looks like a tool attempt;
2. otherwise it emits explicit missing evidence rather than governed direct-answer or scalar subtypes.

This behavior is implemented in the current authoritative emission path in `scripts/eval_canonical_manifest.py`.

Affected rows:

1. all `134` missing-evidence rows

Owner of resolution authority:

1. scorer implementation under the approved Family A contract

### Category B: Doctrine-Prohibited Detector Inference

Observed blocker category:

1. doctrine explicitly forbids converting prose appearance, scalar appearance, no-call movement, or generated-text shape into detector-owned direct-answer or scalar subtype facts.

Affected rows:

1. all `134` missing-evidence rows
2. especially the legacy `125` direct-answer counts that are not scorer-emitted governed facts

Owner of resolution authority:

1. governance doctrine
2. scorer doctrine / Family A subtype contract

### Category C: Mixed-Output Ambiguity

Observed blocker category:

1. a small row subset begins with answer-like text but then spills into transcript echo;
2. this creates ambiguity between answer substitution, malformed output, and generic transcript leakage.

Affected rows:

1. `3`

Owner of resolution authority:

1. scorer doctrine for subtype boundary rules
2. scorer implementation for whether approved distinguishing evidence is emitted

### Category D: Legacy Fallback Overclassification

Observed blocker category:

1. the legacy evaluator maps many non-exact invalid-json plaintext rows to `direct_answer_substitution` by fallback;
2. the authoritative Stage C path intentionally does not preserve that as a governed fact.

Affected rows:

1. legacy-only `125` direct-answer counts

Owner of resolution authority:

1. legacy evaluator implementation for the current fallback behavior
2. migration governance for whether that legacy behavior can ever be bridged

### Category E: Evaluator-Consumption Limitation

Observed category:

1. no separate downstream evaluator-consumption failure was found;
2. the Stage C consumer surfaces preserve scorer-emitted missingness rather than overwriting it.

Conclusion:

1. the decisive blocker is upstream subtype-emission incompleteness, not downstream consumption corruption.

## Legacy-To-Authoritative Gap Review

### Count-Level Gap

Observed full-run gap:

| Surface | Count |
|---|---:|
| legacy `direct_answer_substitution_count` | 125 |
| authoritative `direct-answer substitution` count | 0 |
| authoritative missing-evidence population | 134 |

### Gap Attribution

The gap is not a simple missing-count delta.

It is a mismatch between:

1. a legacy fallback classification regime; and
2. an authoritative scorer-owned governed-subtype regime that preserves missingness.

Investigative attribution of the `125` legacy-only direct-answer counts:

| Apparent contributing factor | Investigative count | Notes |
|---|---:|---|
| doctrine-exposed legacy fallback | 125 | every legacy direct-answer count in this run depends on a legacy fallback that current doctrine forbids as governed subtype evidence |
| prompt / instruction / transcript echo rather than clean substitution evidence | 122 | these rows do not look like clean direct-answer or scalar replacements under the current evidence record |
| mixed-output ambiguity | 3 | answer-like first line followed by transcript echo |
| clean scalar-only opportunity | 0 | none observed |
| clean direct-answer-only opportunity | 0 | none observed |

These counts are investigative, not authoritative subtype replacements.

### Proportion Interpretation

The observed gap appears attributable primarily to:

1. doctrine plus implementation interaction:
   - the legacy path classifies by fallback;
   - the authoritative path refuses to convert output shape into governed subtype fact;
2. evidence insufficiency in the current scorer output:
   - no approved direct-answer or scalar evidence is emitted for the `134` blocked rows;
3. a small ambiguity slice:
   - `3` rows present answer-like text mixed with transcript echo.

The record does not support a conclusion that the blocked population mainly consists of clean direct-answer or scalar substitutions waiting to be turned on.

## Ownership Review

### Governance Doctrine

Owns:

1. whether detector-side or consumer-side text classification is prohibited;
2. whether missing subtype remains missing;
3. whether historical or legacy fallback counts can stand in for current-run governed subtype facts.

### Scorer Doctrine

Owns:

1. approved Family A subtype taxonomy;
2. precedence between direct-answer substitution, scalar substitution, malformed output, wrapper/envelope drift, and missing tool call;
3. missing-evidence behavior when subtype boundaries cannot be resolved.

### Scorer Implementation

Owns:

1. emission of approved direct-answer or scalar subtype evidence;
2. emission of explicit missing evidence when subtype evidence is insufficient;
3. emission of `malformed output` when tool-attempt evidence is sufficient.

This is the primary practical locus of the current blocker.

### Evaluator Implementation

Owns:

1. preserving emitted authoritative subtype vs missing-evidence state into Stage C artifacts;
2. preserving row identity and denominator membership.

Current assessment:

1. evaluator consumption is conservative and aligned with doctrine;
2. it is not independently inventing the missing subtype problem.

### Dataset Metadata

Owns:

1. row identity and population metadata;
2. not the missing direct-answer subtype evidence for this surface.

Current assessment:

1. dataset metadata is not the limiting actor for this blocker.

## Regimen Impact Assessment

### Readiness Implications

Current `migration-blocked` posture remains meaningful because:

1. the authoritative surface is present;
2. the blocker is explicit and stable;
3. the blocker concerns subtype completeness, not missing population coverage.

### Future Evidence Requirements

Future lifecycle work would need evidence about:

1. whether the scorer pathway can emit approved direct-answer substitution on the frozen corpus at all;
2. whether the scorer pathway can emit approved scalar substitution on the frozen corpus at all;
3. whether mixed answer-plus-transcript outputs remain missing by doctrine or can become disambiguated by approved scorer evidence.

### Future Blocker-Focused Investigations

The next blocker-focused investigations are now clearly scorer-centered:

1. subtype boundary applicability under current emitted evidence;
2. scorer implementation completeness for direct-answer vs scalar evidence;
3. whether the `3` ambiguous rows are intrinsically noncomputable or only currently under-evidenced.

No further corpus-coverage qualification is indicated by the current record.

## Recommendation

Recommended blocker classification:

- `mixed`

### Rationale

The blocker is not purely doctrinal, purely evidentiary, or purely implementation-driven.

It is mixed because:

1. doctrine forbids rescuing the gap through detector-side or evaluator-side text inference;
2. the current scorer implementation does not emit approved direct-answer or scalar evidence for the blocked rows;
3. most blocked rows do not present clean substitution evidence anyway;
4. a small remainder is genuinely ambiguous rather than clearly classifiable.

More specifically:

1. the blocker manifests operationally as implementation-driven missing subtype emission;
2. it remains governance-hard because doctrine intentionally preserves that missingness;
3. the underlying row shapes suggest the missingness is often evidentially justified rather than merely accidental.

## Determinations

1. The current blocker population is `134` authoritative missing-evidence rows on a stable `140`-row non-exact denominator.
2. The missing-evidence population is concentrated in `heldout_validation` and `tool_holdout` and spans many expected tools.
3. No clean direct-answer-only or scalar-only missing-evidence rows were observed in the repeated full-run record.
4. `131` rows appear structurally incapable of supporting governed direct-answer or scalar subtype assignment under the current doctrine and current emitted evidence.
5. `3` rows are mixed-output ambiguous rather than clearly classifiable.
6. The legacy-to-authoritative count gap is mainly a legacy fallback vs governed-subtype mismatch, not a hidden pool of clean authoritative direct-answer rows.
7. Resolution authority lies primarily with scorer doctrine plus scorer implementation, not dataset metadata and not downstream evaluator consumption.
8. Future lifecycle progression should stay focused on scorer subtype completeness rather than on further corpus-coverage work.
