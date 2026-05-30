# Stage B WP8 B1 Coverage Summary

## Scope

This document summarizes Family B1 fixture coverage after completion of the Family B1 package.

This is documentation-only. It does not implement validators, schemas, runtime behavior, detectors, scorers, evaluators, thresholds, governance rules, mappings, or manifests.

## Scenario Counts

| Scenario Group | Count | Coverage Status |
|---|---:|---|
| Complete-emission scenarios | 9 | Covered |
| Partial-emission scenarios | 5 | Covered |
| Missing-emission scenarios | 6 | Covered |
| Detector non-inference scenarios | 4 | Covered |
| Total approved Family B1 scenarios | 24 | Covered |

## Fixture Counts By Category

| Fixture Category | Fixture Count | Current-Run Computability Profile | Comparability Profile |
|---|---:|---|---|
| Complete emission | 9 | 9 current-run computable | 9 comparison-blocked |
| Partial emission | 5 | 5 current-run noncomputable | 5 comparison-blocked |
| Missing emission | 6 | 6 current-run noncomputable | 6 comparison-blocked |
| Detector non-inference | 4 | 4 current-run noncomputable | 3 comparison-blocked, 1 bridge-required |
| Total | 24 | 9 computable, 15 noncomputable | 23 comparison-blocked, 1 bridge-required, 0 comparison-allowed, 0 reference-only |

## Governed Concept Counts

| Governed Concept | Fixture Count | Fixture IDs |
|---|---:|---|
| Read-file aggregate | 9 | `B1-C-001`, `B1-C-002`, `B1-C-006`, `B1-M-001`, `B1-M-002`, `B1-M-003`, `B1-M-006`, `B1-NI-001`, `B1-P-004` |
| Symbol-name governed sub-slice | 10 | `B1-C-003`, `B1-C-004`, `B1-C-008`, `B1-M-004`, `B1-NI-002`, `B1-NI-003`, `B1-NI-004`, `B1-P-001`, `B1-P-002`, `B1-P-003` |
| Read-file aggregate and symbol-name sub-slice | 2 | `B1-C-005`, `B1-M-005` |
| Split-scoped read-file and symbol-name summaries | 1 | `B1-C-009` |
| Split-scoped symbol-name summary | 1 | `B1-P-005` |
| Exclusion handling | 1 | `B1-C-007` |

## Coverage Matrix

| Coverage Dimension | Positive Coverage | Partial Coverage | Missing Coverage | Non-Inference Coverage | Status |
|---|---|---|---|---|---|
| Read-file aggregate | `B1-C-001`, `B1-C-002`, `B1-C-005`, `B1-C-006`, `B1-C-009` | `B1-P-004` | `B1-M-001`, `B1-M-002`, `B1-M-003`, `B1-M-006` | `B1-NI-001` | Covered |
| Symbol-name governed sub-slice | `B1-C-003`, `B1-C-004`, `B1-C-005`, `B1-C-008`, `B1-C-009` | `B1-P-001`, `B1-P-002`, `B1-P-003`, `B1-P-005` | `B1-M-004`, `B1-M-005` | `B1-NI-002`, `B1-NI-003`, `B1-NI-004` | Covered |
| Parent read-file context | `B1-C-003`, `B1-C-004`, `B1-C-008`, `B1-C-009` | `B1-P-003` | Not applicable | `B1-NI-002` rejects parent aggregate substitution | Covered |
| Denominator visibility | `B1-C-001` through `B1-C-005`, `B1-C-008`, `B1-C-009` | `B1-P-002` | `B1-M-006` | `B1-NI-001`, `B1-NI-002` | Covered |
| Expected-tool and read-file eligibility markers | `B1-C-001`, `B1-C-002`, `B1-C-006`, `B1-C-009` | `B1-P-004` | `B1-M-002`, `B1-M-003` | Not applicable | Covered |
| Exact-valid scorer fact | `B1-C-001`, `B1-C-003` | Not applicable | `B1-M-005` | Not applicable | Covered |
| Non-exact partition | `B1-C-002`, `B1-C-004` | Not applicable | `B1-M-005` blocks partitioning | Not applicable | Covered |
| Exclusion handling | `B1-C-007` | Not applicable | Not applicable | Not applicable | Covered |
| Split-scoped summaries | `B1-C-009` | `B1-P-005` | Not applicable | Not applicable | Covered |
| Small denominator visibility | `B1-C-008` | `B1-P-002` | Not applicable | Not applicable | Covered |
| Historical baseline context | Not applicable | Not applicable | Not applicable | `B1-NI-004` rejects historical rate as current-run evidence | Covered |

## Detector Non-Inference Coverage

| Rejected Inference | Fixture ID | Expected Treatment |
|---|---|---|
| Mixed-tool exact-valid aggregate becomes read-file aggregate | `B1-NI-001` | Report missing read-file aggregate; do not substitute mixed-tool totals. |
| Parent read-file aggregate becomes symbol-name sub-slice | `B1-NI-002` | Report missing symbol-name sub-slice; do not substitute parent aggregate. |
| Symbol-like prompt text creates symbol-name membership | `B1-NI-003` | Report missing symbol-name marker; do not inspect prompt text for membership. |
| Historical symbol-name rate becomes current-run evidence | `B1-NI-004` | Block comparison, require bridge, and do not use historical rate as emitted current-run evidence. |

## State Coverage

| Completeness | Current-Run Computability | Comparability | Fixture Count | Fixture IDs |
|---|---|---|---:|---|
| `complete` | `current-run computable` | `comparison-blocked` | 9 | `B1-C-001` through `B1-C-009` |
| `partial` | `current-run noncomputable` | `comparison-blocked` | 5 | `B1-P-001` through `B1-P-005` |
| `partial` | `current-run noncomputable` | `bridge-required` | 1 | `B1-NI-004` |
| `missing` | `current-run noncomputable` | `comparison-blocked` | 9 | `B1-M-001` through `B1-M-006`, `B1-NI-001`, `B1-NI-002`, `B1-NI-003` |

## Scenario-Catalog Reconciliation

| Source Scenario Range | Catalog Count | Authored Fixture Count | Reconciliation Status |
|---|---:|---:|---|
| `B1-C-001` through `B1-C-009` | 9 | 9 | Reconciled |
| `B1-P-001` through `B1-P-005` | 5 | 5 | Reconciled |
| `B1-M-001` through `B1-M-006` | 6 | 6 | Reconciled |
| `B1-NI-001` through `B1-NI-004` | 4 | 4 | Reconciled against authoritative B1-NI review |
| Total | 24 | 24 | Reconciled |

## Remaining Gaps

Family B1 fixture coverage has no remaining approved scenario gaps.

Remaining gaps are outside the completed Family B1 fixture package:

- Family B2 anchor-generalization fixture readiness and authoring;
- cross-family package review after Family B2 exists;
- fixture validator implementation planning;
- fixture validator implementation;
- schema implementation planning and implementation;
- runtime evaluator, scorer, and detector implementation.

## Readiness Assessment

Family B1 fixture coverage is ready for validator implementation planning after review and approval of the B1 package documents.

Validator planning should preserve the following required distinctions:

- aggregate read-file preservation versus symbol-name governed sub-slice preservation;
- parent aggregate facts versus sub-slice facts;
- current-run computability versus baseline comparability;
- emitted ownership and membership facts versus detector inference;
- counts versus denominators and rates;
- current-run facts versus historical baseline context;
- missing, partial, and complete completeness states.
