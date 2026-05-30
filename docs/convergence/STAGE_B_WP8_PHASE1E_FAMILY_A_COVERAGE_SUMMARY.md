# Stage B WP8 Phase 1E Family A Coverage Summary

## Scope

This document summarizes Family A fixture coverage after WP8 Phase 1E package finalization.

This is documentation-only. It does not implement validators, implement schemas, modify runtime behavior, modify detectors, modify scorers, modify evaluators, modify thresholds, modify governance rules, modify mappings, or modify manifests.

## Scenario Counts

| Scenario Group | Count | Coverage Status |
|---|---:|---|
| Complete-emission scenarios | 10 | Covered |
| Partial-emission scenarios | 5 | Covered |
| Missing-emission scenarios | 6 | Covered |
| Detector non-inference scenarios | 4 | Covered |
| Total approved Family A scenarios | 25 | Covered |

## Fixture Counts By Category

| Fixture Category | Fixture Count | Current-Run Computability Profile | Comparability Profile |
|---|---:|---|---|
| Complete emission | 10 | 10 current-run computable | 10 comparison-blocked |
| Partial emission | 5 | 5 current-run noncomputable | 5 comparison-blocked |
| Missing emission | 6 | 6 current-run noncomputable | 6 comparison-blocked |
| Detector non-inference | 4 | 4 current-run noncomputable | 3 comparison-blocked, 1 bridge-required |
| Total | 25 | 10 computable, 15 noncomputable | 24 comparison-blocked, 1 bridge-required, 0 comparison-allowed, 0 reference-only |

## Subtype And Concept Counts

| Subtype Or Concept | Fixture Count | Fixture IDs |
|---|---:|---|
| Exact-valid control; no subtype assignment | 1 | `A-C-001` |
| Excluded-row control; no subtype assignment | 1 | `A-C-009` |
| Missing active Family A aggregate | 1 | `A-M-001` |
| `direct-answer substitution` | 4 | `A-C-002`, `A-P-002`, `A-P-003`, `A-M-002` |
| `scalar substitution` | 1 | `A-C-003` |
| `malformed output` | 1 | `A-C-004` |
| `wrapper/envelope drift` | 1 | `A-C-005` |
| `missing tool call` | 1 | `A-C-006` |
| `wrong tool name` | 1 | `A-C-007` |
| `wrong argument` | 1 | `A-C-008` |
| `all approved subtypes, split-scoped` | 1 | `A-C-010` |
| `affected approved subtype unknown or missing` | 1 | `A-P-001` |
| `direct-answer substitution, split-scoped` | 1 | `A-P-004` |
| `all approved subtype rates` | 1 | `A-P-005` |
| `all approved subtypes` | 1 | `A-M-003` |
| `affected subtype unknown` | 2 | `A-M-004`, `A-M-005` |
| `affected approved subtype missing` | 1 | `A-M-006` |
| `direct-answer substitution candidate, missing evidence` | 1 | `A-NI-001` |
| `scalar substitution candidate, missing evidence` | 1 | `A-NI-002` |
| `direct-answer substitution, historical-only evidence` | 1 | `A-NI-003` |
| `direct-answer substitution candidate, no-call proxy rejected` | 1 | `A-NI-004` |

## Coverage Matrix

| Coverage Dimension | Positive Coverage | Partial Coverage | Missing Coverage | Non-Inference Coverage | Status |
|---|---|---|---|---|---|
| Direct-answer substitution | `A-C-002` | `A-P-002`, `A-P-003`, `A-P-004` | `A-M-002` | `A-NI-001`, `A-NI-003`, `A-NI-004` | Covered |
| Scalar substitution | `A-C-003` | Not applicable | Not applicable | `A-NI-002` | Covered |
| Malformed output | `A-C-004` | Not applicable | Not applicable | Not applicable | Covered |
| Wrapper/envelope drift | `A-C-005` | Not applicable | Not applicable | Not applicable | Covered |
| Missing tool call | `A-C-006` | Not applicable | Not applicable | No-call proxy rejected by `A-NI-004` | Covered |
| Wrong tool name | `A-C-007` | Not applicable | Not applicable | Not applicable | Covered |
| Wrong argument | `A-C-008` | Not applicable | Not applicable | Not applicable | Covered |
| Exact-valid partition | `A-C-001` | Not applicable | `A-M-005` | Not applicable | Covered |
| Exclusion handling | `A-C-009` | Not applicable | Not applicable | Not applicable | Covered |
| Split-scoped summaries | `A-C-010` | `A-P-004` | Not applicable | Not applicable | Covered |
| Family aggregate | `A-C-010` | `A-P-001`, `A-P-005` | `A-M-001` | Not applicable | Covered |
| Failure taxonomy | Complete fixtures require taxonomy marker | `A-P-003` | `A-M-003` | `A-NI-003` rejects historical-only evidence without current facts | Covered |
| Scorer primary outcome | Complete fixtures require primary outcome | Not applicable | `A-M-004` | Not applicable | Covered |
| Non-exact subtype assignment | `A-C-002` through `A-C-008` | `A-P-001` | `A-M-006` | `A-NI-001`, `A-NI-002` | Covered |

## Detector Non-Inference Coverage

| Rejected Inference | Fixture ID | Expected Treatment |
|---|---|---|
| Prose-like generated text becomes direct-answer substitution | `A-NI-001` | Report missing subtype; do not classify generated text. |
| Scalar-looking output becomes scalar or direct-answer substitution | `A-NI-002` | Report missing subtype; do not choose neighboring subtype. |
| Historical direct-answer count becomes current-run evidence | `A-NI-003` | Block comparison; require bridge before baseline comparison. |
| No-call correctness becomes direct-answer substitution | `A-NI-004` | Keep no-call correctness separate; report missing direct-answer subtype. |

## State Coverage

| Completeness | Current-Run Computability | Comparability | Fixture Count | Fixture IDs |
|---|---|---|---:|---|
| `complete` | `current-run computable` | `comparison-blocked` | 10 | `A-C-001` through `A-C-010` |
| `partial` | `current-run noncomputable` | `comparison-blocked` | 5 | `A-P-001` through `A-P-005` |
| `partial` | `current-run noncomputable` | `bridge-required` | 1 | `A-NI-003` |
| `missing` | `current-run noncomputable` | `comparison-blocked` | 9 | `A-M-001` through `A-M-006`, `A-NI-001`, `A-NI-002`, `A-NI-004` |

## Remaining Gaps

Family A fixture coverage has no remaining approved scenario gaps.

Remaining gaps are outside the completed Family A fixture package:

- validator implementation planning;
- validator implementation;
- schema implementation planning and implementation;
- Family B1 fixture authoring;
- Family B2 fixture authoring;
- cross-family package review after Family B1 and Family B2 coverage exist.

## Readiness Assessment

Family A fixture coverage is ready for validator implementation planning after review and approval of the Phase 1E package documents.

Validator planning should preserve the following required distinctions:

- complete, partial, and missing completeness states;
- current-run computability versus baseline comparability;
- emitted subtype facts versus detector inference;
- direct-answer substitution versus scalar substitution;
- governed Family A evidence versus no-call correctness or wrapper leakage signals;
- current-run facts versus historical baseline context.
