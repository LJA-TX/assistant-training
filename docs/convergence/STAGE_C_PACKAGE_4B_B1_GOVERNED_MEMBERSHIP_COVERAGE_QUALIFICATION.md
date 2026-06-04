# Stage C Package 4B B1 Governed Membership Coverage Qualification

## Scope

This package determines whether authoritative Family B1 symbol-name governed-membership coverage exists in the frozen canonical corpus used by Stage C work.

This is a coverage-qualification assessment only.

It does not:

1. perform reconciliation changes;
2. perform readiness reassessment;
3. perform gate reassessment;
4. perform migration planning;
5. modify detector behavior;
6. modify threshold behavior;
7. create replacement metrics;
8. infer governed membership from prompt content.

## Inputs

Doctrine and contract inputs:

1. `docs/convergence/STAGE_B_B1_SYMBOL_NAME_OWNERSHIP_REVIEW.md`
2. `docs/convergence/STAGE_B_B1_PARENT_CONTEXT_AND_DENOMINATOR_REVIEW.md`
3. `docs/convergence/STAGE_B_B1_READINESS_CLOSURE_ASSESSMENT.md`
4. `docs/convergence/STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
5. `docs/convergence/STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
6. `docs/convergence/STAGE_B_WP8_B1_FIXTURE_INDEX.md`
7. `docs/convergence/STAGE_C_PACKAGE_1C_RUNTIME_VALIDATION_REPORT.md`
8. `docs/convergence/STAGE_C_PACKAGE_1D_RUNTIME_VALIDATION_REPORT.md`
9. `docs/convergence/STAGE_C_PACKAGE_1D_MIGRATION_READINESS_TAXONOMY_RATIONALE.md`
10. `docs/convergence/STAGE_C_PACKAGE_1E_CURRENT_SURFACE_GATE_ASSESSMENT.md`

Frozen-corpus and emission inputs:

1. `evals/canonical_eval_manifest_v1.json`
2. `evals/data/canonical_v1/heldout_validation.jsonl`
3. `evals/data/canonical_v1/tool_holdout.jsonl`
4. `evals/data/canonical_v1/no_call.jsonl`
5. `evals/data/canonical_v1/adversarial.jsonl`
6. `evals/data/canonical_v1/direct_answer.jsonl`
7. `scripts/eval_canonical_manifest.py`
8. `scripts/stage_c1_evaluator_foundation.py`

## Current Surface State

Current repository state for `read_file_symbol_name_exact_valid_rate`:

1. reconciliation: `requires_future_migration`
2. readiness: `insufficient-evidence`
3. gate: `gate-not-open`

Current known blocker from Package 4A:

1. authoritative governed symbol-membership coverage has not yet been demonstrated on the frozen canonical row set.

## B1 Membership Source Inventory

### Source Inventory Table

| Source | Ownership authority | Emission authority | Declared membership fields | Non-inference requirement |
|---|---|---|---|---|
| `STAGE_B_B1_SYMBOL_NAME_OWNERSHIP_REVIEW.md` | dataset metadata or evaluator-owned metadata preparation upstream of detector | upstream evaluation metadata preparation | explicit symbol-name sub-slice membership; explicit non-membership for read-file rows outside the sub-slice | detector must not infer membership from prompt text, generated text, paths, history, or neighboring rows |
| `STAGE_B_B1_PARENT_CONTEXT_AND_DENOMINATOR_REVIEW.md` | dataset metadata for parent read-file context and symbol-name membership; scorer for exact-valid; evaluator for denominators and rates | evaluator after explicit membership exists | explicit symbol-name membership bounded by explicit read-file family context | parent read-file aggregate must not substitute for missing symbol-name membership or denominator |
| `STAGE_B_EVAL_REDESIGN_CONTRACTS.md` | evaluator with dataset metadata support; detector consumes only | evaluator- or metadata-emitted first-class metric inputs | explicit approved read-file archetype or explicit symbol-name membership; split membership; stable row identity | detector must not infer symbol-name membership from prompt text |
| `scripts/eval_canonical_manifest.py` | consumes only explicit metadata for Stage C row-fact emission | live canonical evaluator Stage C artifact emission | `symbol_name_membership`, `membership_owner`, `symbol_name_membership_owner`, `read_file_archetype`, `eval_read_file_archetype`, `intervention_i10_query_archetype` | if those fields are absent, emitted `family_b1_symbol_name_member` remains `null`; no prompt-derived reconstruction is allowed in Stage C artifacts |
| `scripts/stage_c1_evaluator_foundation.py` | contract validator for emitted row-fact ownership and membership markers | validates the emitted row-fact contract | `membership_markers.family_b1_symbol_name_member`; `ownership_markers.symbol_name_membership_owner` | declared membership requires owner; detector-side repair is outside contract |
| `evals/data/canonical_v1/*.jsonl` | frozen canonical corpus metadata | upstream row metadata carrier for live canonical evaluation | only whatever explicit membership metadata is stored in each row’s `metadata` object | absence remains absence; prompt text is not an authoritative membership source |

### Source Interpretation

The authoritative source chain for B1 symbol-name membership is:

1. explicit upstream evaluation metadata in the frozen corpus;
2. live evaluator Stage C row-fact emission that copies only explicit declared membership or declared archetype evidence;
3. downstream consumers that consume emitted row facts only.

There is no doctrine-supported path where detector-time or evaluator-time prompt inspection creates current-run symbol-name membership.

## Frozen Corpus Coverage Review

### Corpus-Level Findings

Frozen manifest row set:

1. total rows: `200`
2. read-file rows: `27`
3. rows with any explicit symbol-membership or archetype declaration field: `0`

Scanned explicit fields:

1. `symbol_name_membership`
2. `membership_owner`
3. `symbol_name_membership_owner`
4. `read_file_archetype`
5. `eval_read_file_archetype`
6. `intervention_i10_query_archetype`

Result:

1. none of these fields appear in any frozen canonical eval row;
2. none of the `27` read-file rows carry explicit symbol-membership evidence;
3. all `27` read-file rows carry only:
   - `category`
   - `source`
   - `source_case_id`
   - `source_file`
   - `synthetic`
   - `tool`

### Split Distribution

Read-file rows by split:

1. `heldout_validation`: `27`
2. `tool_holdout`: `0`
3. `no_call`: `0`
4. `adversarial`: `0`
5. `direct_answer`: `0`

### Provenance Distribution

Read-file rows originate from three repeated source-case labels:

1. `p0_read_file_1`: `7` rows
2. `p0_read_file_2`: `13` rows
3. `p0_read_file_3`: `7` rows

Read-file source labels:

1. `contrastive_positive`: `14`
2. `canonical_case_template`: `7`
3. `corrective_tool_choice`: `6`

Read-file source files:

1. `/opt/ai-stack/assistant-training/data/tool_ft_allaliases_20260525_from_qual_reports_freq.jsonl`: `14`
2. `/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_aug_rebalanced_20260417T104659Z.jsonl`: `13`

### Explicit Versus Inferred Membership

Explicit membership review result:

1. explicit governed symbol-membership rows: `0`
2. explicit governed symbol-nonmembership rows: `0`
3. explicit archetype-declared rows that would emit symbol membership: `0`
4. inferred-only candidate rows: not counted and not used

Because no explicit symbol-membership or archetype declaration fields exist in the frozen corpus, any positive coverage conclusion would require prompt- or content-based inference.

That is prohibited by current B1 doctrine and out of scope for this package.

## Runtime Emission Implication

Current Stage C runtime emission for B1 symbol membership is constrained by `scripts/eval_canonical_manifest.py`:

1. emit `family_b1_symbol_name_member = true` only from declared `symbol_name_membership=true` or declared `read_file_archetype == "read_file_symbol_name"`;
2. emit `family_b1_symbol_name_member = false` only from explicit declared non-membership or a declared non-symbol archetype;
3. emit `family_b1_symbol_name_member = null` when no explicit declared source exists.

Given the frozen-corpus findings above, the frozen canonical row set can currently emit:

1. read-file eligibility for `27` rows;
2. symbol-name membership for `0` rows;
3. symbol-name population provenance for `0` rows.

This matches prior bounded runtime evidence:

1. Package 1C reconciliation reported authoritative `rows = 0` for `read_file_symbol_name_exact_valid_rate`;
2. Package 1D reported `declared_symbol_membership_row_ids = []`.

## WP8 Alignment Review

### WP8 Category Comparison

| WP8 B1 fixture category | Represented in frozen corpus? | Assessment |
|---|---|---|
| Complete emission | No | No row carries explicit symbol-name membership plus required ownership/context fields |
| Partial emission | No | No row carries partial symbol-name governed facts such as count without denominator or child summary without parent context |
| Missing emission | Partially | The corpus demonstrates global absence of symbol-name membership markers on all `27` read-file rows, but it does not contain an explicitly declared symbol-name row whose membership marker is then missing |
| Detector non-inference | No direct corpus demonstration | The doctrine and fixtures exist, but the frozen corpus does not by itself certify a non-inference case without prompt interpretation, which this package does not perform |

### Required WP8 Coverage Questions

Current frozen corpus evidence exercises:

1. complete membership: not observed
2. partial membership: not observed
3. missing membership: only at the coarse corpus-wide “no marker exists anywhere” level
4. detector non-inference: not positively exercised by explicit corpus metadata alone

### WP8 Alignment Interpretation

WP8 B1 remains highly relevant because it defines exactly the cases the frozen corpus does not currently instantiate for symbol-name coverage:

1. explicit positive membership;
2. explicit negative membership within the read-file family;
3. partial and missing governed sub-slice fact patterns;
4. explicit detector non-inference scenarios.

The frozen corpus is therefore aligned with WP8 as a detection target, but not as a complete exercise of the B1 symbol-name fixture space.

## Coverage Qualification Assessment

Coverage classification:

- `absent`

### Rationale

The authoritative B1 symbol-name governed-membership coverage in the frozen canonical corpus is `absent` because:

1. there are `27` read-file rows and `0` explicit symbol-membership declarations;
2. there are `0` declared archetype fields that would authoritatively emit symbol membership;
3. the current live evaluator is intentionally reconstruction-free for Stage C membership emission;
4. the only way to produce positive symbol-membership coverage from the frozen corpus would be prompt-based or content-based inference, which doctrine forbids.

This means the current `insufficient-evidence` state is caused by missing governed evidence in the frozen corpus, not merely by unexamined evidence.

## Readiness-Impact Assessment

This package does not reassess readiness.

It only assesses whether the current `insufficient-evidence` state remains justified.

Determination:

1. the current `insufficient-evidence` state remains justified;
2. current evidence now shows that the insufficiency comes from absent governed membership coverage, not from an incomplete review of the existing corpus.

Future readiness work would require, at minimum:

1. explicit symbol-name membership or explicit approved archetype declarations in the frozen evaluation row set;
2. ownership markers for the declared symbol-name membership;
3. parent read-file context preserved alongside the child sub-slice;
4. denominator-complete emitted symbol-name coverage on the frozen row set;
5. only after that, renewed reconciliation and readiness review in a separate package.

This package does not recommend that next package.

It only records what evidence would be necessary before such a package could be meaningful.

## Regimen Reuse Assessment

Because coverage is absent, the extracted regimen cannot yet be fully reused on `read_file_symbol_name_exact_valid_rate`.

If authoritative B1 governed membership coverage were later demonstrated, the following regimen elements would become newly testable on a second surface:

1. parent aggregate to governed child-slice reuse within the same Family B1 framework;
2. governed sub-slice denominator completeness rather than parent aggregate denominator only;
3. reuse of reconciliation and readiness structure on a small-denominator governed sub-slice;
4. reuse of detector-impact and threshold-impact review on a second absolute-threshold B1 surface;
5. reuse of rollback and planning gates on a surface where the primary challenge is governed-membership completeness rather than baseline-delta or semantic non-equivalence.

At current repository state, those regimen elements remain potential rather than active because the required governed membership evidence is absent in the frozen corpus.

## Determination

Package 4B determines that:

1. authoritative B1 symbol-name governed-membership coverage does not currently exist in the frozen canonical corpus;
2. the current `insufficient-evidence` state is justified by genuinely missing governed evidence rather than by unexamined existing evidence;
3. future second-surface regimen reuse for `read_file_symbol_name_exact_valid_rate` would require new explicit governed membership evidence before reconciliation or readiness work can advance meaningfully.

## Boundary Confirmation

This package does not:

1. perform reconciliation changes;
2. perform readiness reassessment;
3. perform gate reassessment;
4. perform migration planning;
5. modify detector behavior;
6. modify threshold behavior;
7. create replacement metrics;
8. infer governed membership from prompt content.
