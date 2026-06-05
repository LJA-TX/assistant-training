# Stage C Technical Spike Direct-Answer Scorer-Pathway Evidence Emission Probe

## Scope

This spike executed the smallest bounded scorer-pathway change authorized by the repository record.

It did not:

1. modify detector behavior
2. modify threshold behavior
3. modify migration flags
4. reopen readiness
5. reopen gate
6. authorize migration
7. change `stage_c1.emit_family_a_scorer_evidence(...)`

## Before/After Runtime Assessment

| Surface | Before | After Run A | After Run B |
|---|---:|---:|---:|
| direct-answer subtype count | 0 | 0 | 0 |
| scalar-substitution subtype count | 0 | 0 | 0 |
| missing-evidence count | 134 | 134 | 134 |
| reconciliation state | `requires_future_migration` | `requires_future_migration` | `requires_future_migration` |
| readiness state | `migration-blocked` | `migration-blocked` | `migration-blocked` |
| subtype counts | `{'malformed output': 6}` | `{'malformed output': 6}` | `{'malformed output': 6}` |

Legacy detector-facing surface remained unchanged across all runs:

- `failure_profile.direct_answer_substitution = 125`
- `failure_profile.scalar_substitution = 0`

## Runtime Evidence Assessment

Result:

- no new authoritative direct-answer evidence appeared
- no new authoritative scalar-substitution evidence appeared
- no missing-evidence rows were resolved

Observed deltas:

1. direct-answer subtype delta: `0`
2. scalar-substitution subtype delta: `0`
3. missing-evidence delta: `0`

Why this happened:

1. the frozen canonical run contained `0` strict JSON scalar outputs that met the bounded scorer-owned scalar evidence rule
2. the `6` already-assigned authoritative subtype rows remained `malformed output`
3. the `134` missing-evidence rows never entered the bounded scalar path

## Preservation Audit

Protected cohorts remained fully preserved.

Structurally incapable cohort:

- expected protected rows: `131`
- changed rows: `0`
- missing rows from audit: `0`

Ambiguous cohort:

- expected protected rows: `3`
- changed rows: `0`
- missing rows from audit: `0`

The ambiguous rows remained:

1. `heldout_validation:10`
2. `heldout_validation:28`
3. `heldout_validation:77`

No row in either protected cohort changed:

1. `subtype_assignment`
2. `missing_evidence`
3. `missing_evidence_reasons`
4. `primary_outcome`

## Stability Validation

Repeated full canonical executions produced a stable null result.

Confirmed stable:

1. row identity digests
2. tool-expected row identity digests
3. non-exact row identity digests
4. blocker-inventory digests
5. reconciliation digests
6. readiness digests

Strongest stability signal:

- `comparison_rows.jsonl` hash was identical across before, after A, and after B
- `stage_c_family_a_scorer_evidence_artifact.json` hash was identical across before, after A, and after B

This means the bounded scorer-pathway addition did not activate on any row in either repeated full run.

## Downstream Independence Review

Confirmed unchanged:

1. detector-facing legacy `failure_profile`
2. detector metric behavior
3. threshold behavior
4. migration-disabled posture
5. runtime legacy-surface policy
6. guardrail state

Guardrails stayed clear in all runs.

## Failure Assessment

The spike did not fail operationally.

It failed to produce new governed subtype evidence.

That outcome was informative rather than erroneous.

Most specific explanation supported by runtime evidence:

1. the smallest safe scorer-owned scalar-emission path is inert on the frozen canonical corpus
2. the current blocker is therefore not resolved by a minimal strict-scalar pathway
3. the live direct-answer gap remains runtime-unresolved without broadening beyond this spike's approved scope

## Strategic Assessment

This spike generated genuinely new knowledge.

What we learned that we did not know before:

- the smallest governance-safe scorer-pathway implementation change is a full runtime no-op on the frozen canonical corpus
- the blocker is stronger than "the code path is missing"
- for this corpus, the blocker is also "the smallest safe replacement code path never fires"

Implications:

1. this result weakens the case for immediate formal implementation work on this exact bounded spike design
2. it does not prove that all future scorer-pathway work is impossible
3. it does show that any future successful change would need either:
   - broader scorer-owned evidence production, or
   - a different corpus/output regime
4. it strengthens the case that additional governance packaging would add less value than runtime-oriented evidence or a redirect to higher-charter work

## Final Question

What did we learn that we did not know before?

- We learned that a real bounded scorer-pathway change can be implemented, validated, and rerun without breaking any governance boundary, while still producing zero authoritative evidence movement.
- We learned that the current direct-answer blocker is not merely awaiting a trivial subtype-emission patch.
- We learned that the frozen corpus plus current model outputs do not contain even one row that the smallest safe scalar-substitution path can convert into governed authoritative evidence.
