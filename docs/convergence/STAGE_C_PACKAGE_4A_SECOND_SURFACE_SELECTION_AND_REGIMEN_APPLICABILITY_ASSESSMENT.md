# Stage C Package 4A Second Surface Selection And Regimen Applicability Assessment

## Scope

This package selects the best second compatibility-bearing surface for validating reuse of the migration regimen extracted in Package 3C.

This is selection and applicability assessment only.

It does not:

1. authorize migration implementation;
2. modify detector behavior;
3. modify threshold behavior;
4. alter migration flags;
5. reopen current readiness, gate, or planning-authorization determinations;
6. begin a new migration lifecycle.

## Inputs

Primary surface-state artifacts reviewed:

1. `docs/convergence/STAGE_C_PACKAGE_1C_RUNTIME_VALIDATION_REPORT.md`
2. `docs/convergence/STAGE_C_PACKAGE_1D_RUNTIME_VALIDATION_REPORT.md`
3. `docs/convergence/STAGE_C_PACKAGE_1E_CURRENT_SURFACE_GATE_ASSESSMENT.md`
4. `docs/convergence/STAGE_C_PACKAGE_3C_REGIMEN_RETROSPECTIVE_AND_REUSABILITY_ASSESSMENT.md`
5. `docs/convergence/STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md`
6. `docs/convergence/STAGE_C9D_NO_ANCHOR_METRIC_DISPOSITION_CLOSURE_DETERMINATION.md`
7. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_IMPLEMENTATION_GATE.md`
8. `docs/convergence/STAGE_B_EVAL_REDESIGN_METRIC_INVENTORY.md`
9. `docs/convergence/STAGE_B_WP8_B1_FIXTURE_INDEX.md`
10. `docs/convergence/STAGE_B_WP8C_FAMILY_A_SUBTYPE_BOUNDARY_REVIEW.md`
11. `manifests/reports/stage_b_v1_threshold_profile.json`

## Compatibility-Bearing Surface Inventory

Repository evidence identifies four active compatibility-bearing legacy surfaces:

1. `read_file_exact_valid_rate`
2. `read_file_symbol_name_exact_valid_rate`
3. `direct_answer_substitution_count`
4. `no_anchor_exact_valid_share`

This package evaluates the remaining three surfaces after the completed traversal of `read_file_exact_valid_rate`.

No additional active compatibility-bearing legacy surfaces were identified in repository evidence.

Other thresholded detector metrics remain active in the threshold profile, but the Stage C package series and Stage B metric inventory consistently treat the compatibility-bearing migration set as these four surfaces only.

## Current State Inventory

| Surface | Current reconciliation status | Current readiness status | Current gate status | Known blockers | Known evidence gaps |
|---|---|---|---|---|---|
| `read_file_symbol_name_exact_valid_rate` | `requires_future_migration` | `insufficient-evidence` | `gate-not-open` | no declared authoritative symbol-membership rows in the bounded runtime sample; governed B1 sub-slice coverage not yet demonstrated | full-run authoritative governed-membership coverage review; reconciliation stability on real governed rows; all later gate evidence absent |
| `direct_answer_substitution_count` | `requires_future_migration` | `migration-blocked` | `gate-blocked` | explicit Family A subtype missing-evidence rows; active baseline-delta comparability blocker; detector-gate doctrine still records blocked delta rule | full-run blocker persistence review; stronger scorer-owned subtype completeness evidence; later gate evidence beyond blocker review absent |
| `no_anchor_exact_valid_share` | `not_comparable` | `not-comparable` | `not-gate-eligible` | semantic mismatch is authority-resolved; authoritative noncomputable preservation selected; replacement and retirement both unsupported in current scope | no migration-gate evidence task exists in current scope; only a later authority-level disposition change could reopen candidacy |

## Surface Notes

### `read_file_symbol_name_exact_valid_rate`

Current evidence shows absence, not failure.

The bounded runtime sample in Package 1D emitted:

1. `declared_symbol_membership_row_ids = []`
2. reconciliation reason `authoritative_declared_symbol_membership_unavailable`
3. readiness `insufficient-evidence`

The gate assessment explicitly treats this as a coverage problem rather than a semantic blocker.

WP8 B1 fixtures show that the governed sub-slice contract is already formalized for:

1. complete emission;
2. partial emission;
3. missing emission;
4. detector non-inference.

That makes the surface under-evidenced, not under-specified.

### `direct_answer_substitution_count`

Current evidence shows an explicit authoritative blocker.

The bounded runtime sample preserved:

1. `missing_evidence_row_ids`
2. reconciliation reason `authoritative_family_a_subtype_surface_incomplete`
3. readiness `migration-blocked`

In addition, detector-gate doctrine still records the active baseline-delta rule as blocked because baseline compatibility, comparability, and migration status are missing.

This surface is therefore governed by both:

1. scorer-owned subtype completeness; and
2. baseline-delta comparability.

### `no_anchor_exact_valid_share`

Current evidence shows doctrinal non-applicability for migration reuse.

Authority already determined:

1. semantic equivalence is unsupported;
2. authoritative replacement is unsupported in current scope;
3. authoritative retirement is unsupported in current scope;
4. authoritative noncomputable preservation is the selected disposition.

This means the surface remains visible but blocked by design rather than merely under-evidenced.

## Regimen Applicability Assessment

### Applicability Table

| Surface | Regimen reuse unchanged | Special handling required | New governance challenge level | Applicability assessment |
|---|---|---|---|---|
| `read_file_symbol_name_exact_valid_rate` | high | governed-membership coverage qualification; B1 child-slice denominator completeness; explicit non-inference around symbol-name membership | medium | cleanest second-surface reuse candidate |
| `direct_answer_substitution_count` | medium | scorer subtype completeness; baseline-delta comparability; denominator compatibility; explicit blocked-state persistence review | high | useful but materially more complex than the first surface |
| `no_anchor_exact_valid_share` | low | authority-level semantic disposition change would be required before ordinary migration gating could even apply | very high | not a clean regimen-reuse candidate under current scope |

### `read_file_symbol_name_exact_valid_rate`

Most of the extracted regimen can be reused unchanged:

1. authoritative fact emission and row identity remain the same;
2. passive governance consumption remains applicable;
3. passive reconciliation remains applicable;
4. readiness assessment remains applicable;
5. gate assessment remains applicable;
6. later impact, rollback, authorization, and planning layers would all remain structurally familiar.

Special handling required:

1. prove that declared symbol-name governed rows exist in the full frozen row set without reconstruction;
2. preserve the B1 child-slice denominator independently from the parent read-file aggregate;
3. preserve detector non-inference around symbol-like prompt text and parent-slice substitution.

New governance challenge:

1. the regimen must now operate over a governed sub-slice rather than a parent aggregate.

That is a meaningful but bounded expansion of the first surface.

### `direct_answer_substitution_count`

The regimen remains conceptually reusable, but not cleanly reusable unchanged.

Reusable pieces:

1. authoritative emission and row identity discipline;
2. passive governance consumption;
3. passive reconciliation;
4. readiness and gate taxonomy.

Special handling required:

1. scorer-owned subtype completeness rather than simple exact-valid aggregation;
2. preservation of explicit missing-evidence states;
3. baseline-delta comparability gate handling;
4. concept-scoped baseline compatibility.

New governance challenges:

1. detector must never classify generated text;
2. subtype boundaries must remain scorer-owned and complete enough to migrate;
3. delta-vs-baseline introduces a regime element not exercised by `read_file_exact_valid_rate`.

This surface is therefore high-value but not low-risk.

### `no_anchor_exact_valid_share`

The extracted regimen does not currently apply cleanly.

Reusable pieces remain limited to:

1. visibility preservation;
2. blocked-state reporting;
3. noncomputable preservation discipline.

Ordinary migration-regimen reuse does not apply because:

1. the surface is not gate-eligible;
2. current doctrine forbids substitution of Stage C B2 governed-rate evidence into the legacy share metric;
3. the selected disposition is preserved noncomputability rather than migratable equivalence.

This makes the surface a doctrine exception, not a reusable next candidate.

## Candidate Ranking

### Overall Suitability Ranking

1. `read_file_symbol_name_exact_valid_rate`
2. `direct_answer_substitution_count`
3. `no_anchor_exact_valid_share`

### Lowest-Risk Candidate

`read_file_symbol_name_exact_valid_rate`

Why:

1. it stays within Family B1;
2. it uses absolute-threshold semantics rather than baseline-delta semantics;
3. current evidence gap is absence of governed coverage, not an explicit doctrinal blocker;
4. WP8 B1 fixtures already formalize the missing/partial/non-inference cases that matter.

### Highest Information-Value Candidate

`direct_answer_substitution_count`

Why:

1. it would test the regimen against scorer-owned subtype completeness rather than simple exact-valid aggregation;
2. it would test the regimen against baseline-delta comparability, which the first surface never exercised;
3. it would show whether the extracted process can handle an explicitly blocked surface rather than merely an under-evidenced surface.

### Most Difficult Candidate

`no_anchor_exact_valid_share`

Why:

1. the surface is not-gate-eligible under current doctrine;
2. semantic equivalence is already rejected;
3. authoritative noncomputable preservation is already the selected disposition.

Difficulty here is not implementation complexity alone.

It is that current doctrine does not present an ordinary migration path for the surface at all.

## Recommended Next Surface

Recommended next surface:

- `read_file_symbol_name_exact_valid_rate`

### Rationale

This is the best second-surface candidate because it is:

1. the nearest structural neighbor to the already-completed `read_file_exact_valid_rate` path;
2. still within Family B1, which reduces cross-family methodological jump risk;
3. blocked by insufficient evidence rather than by a settled doctrinal exclusion;
4. capable of testing whether the regimen generalizes from a parent aggregate to a governed sub-slice without yet introducing baseline-delta complexity.

Why not `direct_answer_substitution_count` first:

1. it introduces two new hard problems at once:
   - scorer subtype completeness
   - baseline-delta comparability
2. failure on that surface would be less informative about whether the regimen itself is reusable versus whether the surface is still blocker-bound.

Why not `no_anchor_exact_valid_share`:

1. current doctrine already places it outside clean migration-regimen reuse in current scope.

## Regimen Validation Assessment

Successful traversal of `read_file_symbol_name_exact_valid_rate` would materially strengthen confidence in the extracted regimen.

It would test new aspects not exercised by `read_file_exact_valid_rate`:

1. governed sub-slice coverage qualification rather than parent-aggregate coverage only;
2. denominator completeness for a child B1 slice;
3. stronger non-inference requirements around sub-slice membership;
4. transition from `insufficient-evidence` to either:
   - a stronger reusable readiness state, or
   - a stable evidence-based blocker state without reconstruction;
5. reuse of the same reconciliation, readiness, gate, impact, rollback, authorization, and planning structure on a second but structurally related surface.

It would therefore test whether the regimen is:

1. reusable beyond one exact-valid aggregate metric; and
2. still disciplined when governed-membership coverage itself is the first unresolved evidence issue.

## Determination

Package 4A determines that:

1. the extracted regimen is most cleanly reusable next on `read_file_symbol_name_exact_valid_rate`;
2. `direct_answer_substitution_count` is the highest-value stress test after that;
3. `no_anchor_exact_valid_share` should not be treated as the next reuse candidate under current doctrine.

## Boundary Confirmation

This package does not:

1. authorize migration implementation;
2. modify detector behavior;
3. modify threshold behavior;
4. alter migration flags;
5. reopen current gate determinations;
6. begin a new migration lifecycle.
