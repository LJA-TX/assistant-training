# Stage B WP8-A Scenario Catalog And Expected Outcomes

## Scope

This document is the authoritative WP8-A scenario catalog for Stage B Validation Fixtures.

It defines expected behavior before fixture files, validators, schemas, or runtime implementation are created.

This is documentation-only planning. It does not implement fixtures, implement validators, modify schemas, modify code, modify detectors, modify evaluators, modify scorers, modify thresholds, modify governance rules, modify mappings, or modify manifests.

Reference inputs:

- `STAGE_B_IMPLEMENTATION_WORKPACKETS.md`
- `STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`

## State Vocabulary

Completeness states:

- `complete`
- `partial`
- `missing`

Current-run computability states:

- `current-run computable`
- `current-run noncomputable`

Comparability states:

- `comparison-allowed`
- `bridge-required`
- `reference-only`
- `comparison-blocked`

Classifications:

- Required
- Optional Diagnostic
- Future Reserved

Default comparability expectation:

- Unless a scenario explicitly tests migration or baseline comparison, expected comparability is `comparison-blocked`. Current-run computability does not imply baseline comparability.

## Catalog Summary

Scenario count by family:

| Family | Scenario Count |
|---|---:|
| Family A | 25 |
| Family B1 | 24 |
| Family B2 | 23 |
| Cross-family | 27 |
| Total | 99 |

Scenario count by primary state type:

| Primary State Type | Scenario Count |
|---|---:|
| Complete emission | 28 |
| Partial emission | 16 |
| Missing emission | 19 |
| Noncomputability-specific | 2 |
| Comparability | 10 |
| Detector non-inference | 14 |
| Reconciliation | 10 |
| Total | 99 |

Partial, missing, detector non-inference, and several reconciliation scenarios also exercise noncomputability, but each scenario is counted once by primary scenario type.

## Family A Scenario Catalog

Family A covers the Governed Failure-Subtype Taxonomy and the direct-answer substitution governed subtype.

| Scenario ID | Family | Governed Concept Or Sub-Slice | Required Input Conditions | Expected Completeness State | Expected Current-Run Computability State | Expected Comparability State | Expected Detector Treatment | Expected Reconciliation Requirements | Classification |
|---|---|---|---|---|---|---|---|---|---|
| A-C-001 | Family A | Failure-subtype aggregate | Eligible tool-expected row; scorer exact-valid outcome emitted; taxonomy marker present. | complete | current-run computable | comparison-blocked | Consume emitted exact-valid fact; do not subtype exact-valid row. | Eligible tool-expected denominator includes row; non-exact denominator excludes row. | Required |
| A-C-002 | Family A | Direct-answer governed subtype | Eligible tool-expected non-exact row; subtype emitted as direct-answer substitution; denominators and taxonomy marker present. | complete | current-run computable | comparison-blocked | Consume direct-answer subtype facts only. | Direct-answer count increments; eligible and non-exact denominator bases reconcile. | Required |
| A-C-003 | Family A | Sibling subtype | Eligible tool-expected non-exact row; subtype emitted as scalar substitution; taxonomy marker present. | complete | current-run computable | comparison-blocked | Consume emitted scalar subtype; do not relabel as direct-answer. | Scalar count increments; subtype totals reconcile to non-exact denominator. | Required |
| A-C-004 | Family A | Sibling subtype | Eligible tool-expected non-exact row; subtype emitted as malformed JSON; taxonomy marker present. | complete | current-run computable | comparison-blocked | Consume emitted malformed-output subtype. | Malformed count increments; subtype totals reconcile. | Required |
| A-C-005 | Family A | Sibling subtype | Eligible tool-expected non-exact row; subtype emitted as wrapper or envelope drift; taxonomy marker present. | complete | current-run computable | comparison-blocked | Consume emitted wrapper-drift subtype without using wrapper leakage proxy. | Wrapper-drift count reconciles within subtype distribution. | Required |
| A-C-006 | Family A | Sibling subtype | Eligible tool-expected non-exact row; subtype emitted as missing tool call; taxonomy marker present. | complete | current-run computable | comparison-blocked | Consume emitted missing-tool-call subtype without using no-call aggregate as substitute. | Missing-tool-call count reconciles within subtype distribution. | Required |
| A-C-007 | Family A | Sibling subtype | Eligible tool-expected non-exact row; subtype emitted as wrong tool name; taxonomy marker present. | complete | current-run computable | comparison-blocked | Consume emitted wrong-tool-name subtype. | Wrong-tool-name count reconciles within subtype distribution. | Required |
| A-C-008 | Family A | Sibling subtype | Eligible tool-expected non-exact row; subtype emitted as wrong argument; taxonomy marker present. | complete | current-run computable | comparison-blocked | Consume emitted wrong-argument subtype. | Wrong-argument count reconciles within subtype distribution. | Required |
| A-C-009 | Family A | Exclusion handling | Tool-expected row marked excluded before aggregation; exclusion reason emitted. | complete | current-run computable | comparison-blocked | Consume exclusion summary; do not count excluded row in governed denominator. | Excluded row appears in exclusion count and not in eligible denominator. | Required |
| A-C-010 | Family A | Split-scoped subtype summaries | Complete Family A facts emitted across all active split scopes. | complete | current-run computable | comparison-blocked | Consume split-scoped summaries only as emitted. | Split subtype totals reconcile with family aggregate. | Required |
| A-P-001 | Family A | Failure-subtype aggregate | Family aggregate emitted; one approved subtype summary absent. | partial | current-run noncomputable | comparison-blocked | Mark affected subtype and family completeness partial; do not infer missing subtype. | Aggregate cannot claim subtype distribution reconciliation. | Required |
| A-P-002 | Family A | Direct-answer governed subtype | Direct-answer count emitted; eligible and non-exact denominator bases absent. | partial | current-run noncomputable | comparison-blocked | Treat count-only evidence as incomplete for governed rate. | Rate reconciliation blocked by missing denominator. | Required |
| A-P-003 | Family A | Direct-answer governed subtype | Direct-answer count and denominator emitted; failure taxonomy marker absent. | partial | current-run noncomputable | comparison-blocked | Treat subtype as not governed-computable without taxonomy marker. | Count and denominator may reconcile diagnostically; taxonomy validation fails. | Required |
| A-P-004 | Family A | Split-scoped subtype summaries | Aggregate direct-answer summary emitted; active split-scoped subtype summary absent. | partial | current-run noncomputable | comparison-blocked | Do not synthesize split summary from aggregate. | Split-to-aggregate reconciliation blocked. | Required |
| A-P-005 | Family A | Failure-subtype aggregate | Non-exact denominator emitted; eligible tool-expected denominator absent. | partial | current-run noncomputable | comparison-blocked | Do not compute eligible-population rate. | Failure-mix denominator may reconcile; eligible-population rate blocked. | Required |
| A-M-001 | Family A | Failure-subtype aggregate | Family A aggregate absent while family is registered active. | missing | current-run noncomputable | comparison-blocked | Report missing family. | No count, denominator, or rate reconciliation possible. | Required |
| A-M-002 | Family A | Direct-answer governed subtype | Family aggregate emitted; direct-answer governed subtype absent. | missing | current-run noncomputable | comparison-blocked | Report missing governed subtype; do not use other subtype totals. | Direct-answer reconciliation impossible. | Required |
| A-M-003 | Family A | Failure taxonomy | Taxonomy marker and subtype set absent. | missing | current-run noncomputable | comparison-blocked | Report missing taxonomy; do not classify generated output. | Subtype distribution cannot reconcile against approved taxonomy. | Required |
| A-M-004 | Family A | Scorer primary outcome | Required scorer primary outcome missing for eligible row. | missing | current-run noncomputable | comparison-blocked | Report missing scorer fact. | Row cannot enter exact/non-exact partition reconciliation. | Required |
| A-M-005 | Family A | Exact-valid fact | Exact-valid fact missing for tool-expected row. | missing | current-run noncomputable | comparison-blocked | Report missing exact-valid fact. | Exact/non-exact denominator partition blocked. | Required |
| A-M-006 | Family A | Non-exact subtype | Non-exact tool-expected row lacks approved subtype. | missing | current-run noncomputable | comparison-blocked | Report missing subtype; do not assign `other` unless emitted. | Non-exact subtype totals fail to reconcile. | Required |
| A-NI-001 | Family A | Direct-answer governed subtype | Generated text appears prose-like; no direct-answer subtype emitted. | missing | current-run noncomputable | comparison-blocked | Do not classify generated text; report missing subtype. | No direct-answer count reconciliation allowed. | Required |
| A-NI-002 | Family A | Direct-answer governed subtype | Scalar-looking output exists; scorer subtype missing. | missing | current-run noncomputable | comparison-blocked | Do not infer scalar or direct-answer subtype from output shape. | Subtype distribution blocked. | Required |
| A-NI-003 | Family A | Direct-answer governed subtype | Historical direct-answer count exists; current taxonomy or denominator absent. | partial | current-run noncomputable | bridge-required | Block comparison; do not use historical count as current fact. | Current denominator and taxonomy reconciliation blocked. | Required |
| A-NI-004 | Family A | Direct-answer governed subtype | No-call correctness changes; direct-answer subtype facts absent. | missing | current-run noncomputable | comparison-blocked | Do not reinterpret no-call correctness as direct-answer substitution. | No Family A subtype reconciliation allowed. | Required |

## Family B1 Scenario Catalog

Family B1 covers the Read-File Preservation Family and the symbol-name governed sub-slice.

| Scenario ID | Family | Governed Concept Or Sub-Slice | Required Input Conditions | Expected Completeness State | Expected Current-Run Computability State | Expected Comparability State | Expected Detector Treatment | Expected Reconciliation Requirements | Classification |
|---|---|---|---|---|---|---|---|---|---|
| B1-C-001 | Family B1 | Read-file aggregate | Eligible read-file row; exact-valid scorer fact emitted; denominator marker present. | complete | current-run computable | comparison-blocked | Consume emitted read-file aggregate. | Read-file numerator and denominator reconcile. | Required |
| B1-C-002 | Family B1 | Read-file aggregate | Eligible read-file row; non-exact scorer fact emitted; denominator marker present. | complete | current-run computable | comparison-blocked | Consume emitted read-file non-exact contribution. | Read-file non-exact partition reconciles with denominator. | Required |
| B1-C-003 | Family B1 | Symbol-name governed sub-slice | Eligible read-file symbol-name row; exact-valid scorer fact emitted; parent context present. | complete | current-run computable | comparison-blocked | Consume emitted symbol-name summary. | Symbol-name numerator, denominator, and parent context reconcile. | Required |
| B1-C-004 | Family B1 | Symbol-name governed sub-slice | Eligible read-file symbol-name row; non-exact scorer fact emitted; parent context present. | complete | current-run computable | comparison-blocked | Consume emitted symbol-name non-exact contribution. | Symbol-name exact/non-exact partition reconciles. | Required |
| B1-C-005 | Family B1 | Read-file aggregate and symbol-name sub-slice | Read-file row explicitly outside symbol-name sub-slice. | complete | current-run computable | comparison-blocked | Do not include row in symbol-name denominator. | Read-file denominator includes row; symbol-name denominator excludes row. | Required |
| B1-C-006 | Family B1 | Read-file aggregate | Non-read-file tool row present with explicit tool identity. | complete | current-run computable | comparison-blocked | Do not include non-read-file row in read-file denominator. | Non-read-file row excluded from read-file family totals. | Required |
| B1-C-007 | Family B1 | Exclusion handling | Read-file row marked excluded before aggregation. | complete | current-run computable | comparison-blocked | Consume exclusion summary; do not count excluded row. | Excluded read-file row appears in exclusion count only. | Required |
| B1-C-008 | Family B1 | Symbol-name governed sub-slice | Small symbol-name denominator emitted with count and rate. | complete | current-run computable | comparison-blocked | Consume count and denominator visibly; do not hide small denominator. | Symbol-name rate reconciles and denominator is visible. | Required |
| B1-C-009 | Family B1 | Split-scoped read-file and symbol-name summaries | Complete Family B1 facts emitted across active split scopes. | complete | current-run computable | comparison-blocked | Consume split-scoped summaries only as emitted. | Split summaries reconcile with aggregate and sub-slice totals. | Required |
| B1-P-001 | Family B1 | Symbol-name governed sub-slice | Read-file aggregate emitted; symbol-name sub-slice absent. | partial | current-run noncomputable | comparison-blocked | Do not use read-file aggregate as symbol-name substitute. | Read-file aggregate may reconcile; symbol-name reconciliation impossible. | Required |
| B1-P-002 | Family B1 | Symbol-name governed sub-slice | Symbol-name numerator emitted; symbol-name denominator absent. | partial | current-run noncomputable | comparison-blocked | Treat count-only symbol-name evidence as incomplete. | Symbol-name rate reconciliation blocked. | Required |
| B1-P-003 | Family B1 | Symbol-name governed sub-slice | Symbol-name summary emitted without parent read-file context. | partial | current-run noncomputable | comparison-blocked | Block governed sub-slice use until parent context exists. | Parent-child denominator reconciliation blocked. | Required |
| B1-P-004 | Family B1 | Read-file aggregate | Read-file aggregate emitted without expected-tool marker. | partial | current-run noncomputable | comparison-blocked | Do not infer read-file membership. | Read-file denominator source validation blocked. | Required |
| B1-P-005 | Family B1 | Split-scoped symbol-name summary | Aggregate symbol-name summary emitted; active split-scoped summary absent. | partial | current-run noncomputable | comparison-blocked | Do not synthesize split summary. | Split-to-aggregate reconciliation blocked. | Required |
| B1-M-001 | Family B1 | Read-file aggregate | Read-file family missing while registered active. | missing | current-run noncomputable | comparison-blocked | Report missing family. | No read-file reconciliation possible. | Required |
| B1-M-002 | Family B1 | Read-file aggregate | Read-file eligibility marker missing. | missing | current-run noncomputable | comparison-blocked | Do not infer read-file membership. | Read-file denominator cannot be constructed. | Required |
| B1-M-003 | Family B1 | Read-file aggregate | Expected tool identity missing for eligible row. | missing | current-run noncomputable | comparison-blocked | Report missing expected-tool identity. | Tool-family denominator reconciliation blocked. | Required |
| B1-M-004 | Family B1 | Symbol-name governed sub-slice | Symbol-name membership marker missing. | missing | current-run noncomputable | comparison-blocked | Do not infer symbol-name membership from prompt. | Symbol-name denominator cannot be constructed. | Required |
| B1-M-005 | Family B1 | Read-file aggregate and symbol-name sub-slice | Exact-valid scorer fact missing. | missing | current-run noncomputable | comparison-blocked | Report missing scorer fact. | Numerator and exact/non-exact partition blocked. | Required |
| B1-M-006 | Family B1 | Read-file aggregate | Read-file denominator missing. | missing | current-run noncomputable | comparison-blocked | Do not use mixed-tool denominator. | Read-file rate reconciliation blocked. | Required |
| B1-NI-001 | Family B1 | Read-file aggregate | Mixed-tool exact-valid aggregate exists; read-file aggregate absent. | missing | current-run noncomputable | comparison-blocked | Do not substitute mixed-tool aggregate. | Read-file denominator and numerator absent. | Required |
| B1-NI-002 | Family B1 | Symbol-name governed sub-slice | Read-file aggregate exists; symbol-name sub-slice absent. | missing | current-run noncomputable | comparison-blocked | Do not substitute parent aggregate for sub-slice. | Symbol-name reconciliation impossible. | Required |
| B1-NI-003 | Family B1 | Symbol-name governed sub-slice | Prompt contains symbol-like text; symbol-name marker missing. | missing | current-run noncomputable | comparison-blocked | Do not infer symbol-name from prompt text. | Symbol-name denominator blocked. | Required |
| B1-NI-004 | Family B1 | Symbol-name governed sub-slice | Historical symbol-name rate exists; current subpopulation marker missing. | partial | current-run noncomputable | bridge-required | Block comparison; do not use historical rate as emitted current fact. | Current subpopulation denominator blocked. | Required |

## Family B2 Scenario Catalog

Family B2 covers the Anchor-Generalization Family and the no-anchor governed sub-slice.

| Scenario ID | Family | Governed Concept Or Sub-Slice | Required Input Conditions | Expected Completeness State | Expected Current-Run Computability State | Expected Comparability State | Expected Detector Treatment | Expected Reconciliation Requirements | Classification |
|---|---|---|---|---|---|---|---|---|---|
| B2-C-001 | Family B2 | No-anchor governed sub-slice | Eligible no-anchor row; exact-valid scorer fact emitted; taxonomy and ownership markers present. | complete | current-run computable | comparison-blocked | Consume emitted no-anchor facts. | No-anchor numerator, denominator, and rate reconcile. | Required |
| B2-C-002 | Family B2 | No-anchor governed sub-slice | Eligible no-anchor row; non-exact scorer fact emitted; taxonomy and ownership markers present. | complete | current-run computable | comparison-blocked | Consume emitted no-anchor non-exact contribution. | No-anchor exact/non-exact partition reconciles. | Required |
| B2-C-003 | Family B2 | Sibling anchor category | Eligible row in another approved anchor category; exact-valid scorer fact emitted. | complete | current-run computable | comparison-blocked | Consume emitted sibling category facts. | Sibling category contributes to anchor-family distribution. | Required |
| B2-C-004 | Family B2 | Sibling anchor category | Eligible row in another approved anchor category; non-exact scorer fact emitted. | complete | current-run computable | comparison-blocked | Consume emitted sibling category facts. | Sibling category partition reconciles. | Required |
| B2-C-005 | Family B2 | Anchor-generalization aggregate | Row outside anchor-generalization population emitted with exclusion from family. | complete | current-run computable | comparison-blocked | Do not include outside row in anchor denominator. | Outside row excluded from anchor-family denominator. | Required |
| B2-C-006 | Family B2 | Exclusion handling | Anchor-eligible row marked excluded before aggregation. | complete | current-run computable | comparison-blocked | Consume exclusion summary; do not count excluded row. | Excluded row appears in exclusion count only. | Required |
| B2-C-007 | Family B2 | Anchor-category distribution | Multiple approved anchor categories emitted with taxonomy and ownership markers. | complete | current-run computable | comparison-blocked | Consume emitted category distribution. | Category denominators reconcile with anchor-family denominator. | Required |
| B2-C-008 | Family B2 | Split-scoped anchor summaries | Complete Family B2 facts emitted across active split scopes. | complete | current-run computable | comparison-blocked | Consume split-scoped summaries only as emitted. | Split summaries reconcile with aggregate category totals. | Required |
| B2-P-001 | Family B2 | No-anchor governed sub-slice | Anchor family aggregate emitted; no-anchor sub-slice absent. | partial | current-run noncomputable | comparison-blocked | Do not use anchor aggregate as no-anchor substitute. | No-anchor reconciliation impossible. | Required |
| B2-P-002 | Family B2 | No-anchor governed sub-slice | No-anchor count emitted; no-anchor denominator absent. | partial | current-run noncomputable | comparison-blocked | Treat count-only no-anchor evidence as incomplete. | No-anchor rate reconciliation blocked. | Required |
| B2-P-003 | Family B2 | Anchor-generalization aggregate | Anchor categories emitted without assignment ownership marker. | partial | current-run noncomputable | comparison-blocked | Do not infer assignment ownership. | Category distribution provenance validation blocked. | Required |
| B2-P-004 | Family B2 | Anchor-category distribution | Anchor taxonomy marker emitted; category distribution incomplete. | partial | current-run noncomputable | comparison-blocked | Do not fill missing category counts. | Category totals fail to reconcile to family denominator. | Required |
| B2-P-005 | Family B2 | Split-scoped no-anchor summary | Aggregate no-anchor summary emitted; active split-scoped summary absent. | partial | current-run noncomputable | comparison-blocked | Do not synthesize split summary. | Split-to-aggregate reconciliation blocked. | Required |
| B2-M-001 | Family B2 | Anchor-generalization aggregate | Anchor family missing while registered active. | missing | current-run noncomputable | comparison-blocked | Report missing family. | No anchor-family reconciliation possible. | Required |
| B2-M-002 | Family B2 | Anchor taxonomy | Anchor taxonomy missing. | missing | current-run noncomputable | comparison-blocked | Report missing taxonomy; do not classify prompts. | Category distribution cannot be validated. | Required |
| B2-M-003 | Family B2 | Anchor assignment ownership | Anchor assignment ownership marker missing. | missing | current-run noncomputable | comparison-blocked | Do not infer ownership. | Category provenance reconciliation blocked. | Required |
| B2-M-004 | Family B2 | Anchor category | Anchor category missing for eligible row. | missing | current-run noncomputable | comparison-blocked | Do not classify prompt text. | Anchor-family denominator/category distribution blocked. | Required |
| B2-M-005 | Family B2 | No-anchor governed sub-slice | No-anchor sub-slice missing. | missing | current-run noncomputable | comparison-blocked | Report missing governed sub-slice. | No-anchor reconciliation impossible. | Required |
| B2-M-006 | Family B2 | Exact-valid fact | Exact-valid scorer fact missing for anchor-eligible row. | missing | current-run noncomputable | comparison-blocked | Report missing scorer fact. | Category exact-valid rate reconciliation blocked. | Required |
| B2-NI-001 | Family B2 | No-anchor governed sub-slice | Prompt text lacks obvious anchor phrase; no-anchor marker missing. | missing | current-run noncomputable | comparison-blocked | Do not infer no-anchor from prompt text. | No-anchor denominator blocked. | Required |
| B2-NI-002 | Family B2 | No-anchor governed sub-slice | Historical share of exact-valid rows that are no-anchor exists; no-anchor exact-valid rate absent. | missing | current-run noncomputable | bridge-required | Do not substitute denominator-incompatible historical share. | Current no-anchor denominator and rate absent. | Required |
| B2-NI-003 | Family B2 | No-anchor governed sub-slice | Family aggregate exact-valid rate exists; no-anchor sub-slice absent. | missing | current-run noncomputable | comparison-blocked | Do not substitute family aggregate for no-anchor. | No-anchor reconciliation impossible. | Required |
| B2-NI-004 | Family B2 | No-anchor governed sub-slice | Anchor taxonomy changed; no approved migration status emitted. | complete | current-run computable | comparison-blocked | Consume current run only; block historical comparison. | Current no-anchor reconciliation may pass; comparison marker fails. | Required |

## Cross-Family Scenario Catalog

Cross-family scenarios cover common emission states, comparability, detector non-inference, and reconciliation expectations that apply across families.

| Scenario ID | Family | Governed Concept Or Sub-Slice | Required Input Conditions | Expected Completeness State | Expected Current-Run Computability State | Expected Comparability State | Expected Detector Treatment | Expected Reconciliation Requirements | Classification |
|---|---|---|---|---|---|---|---|---|---|
| X-C-001 | Cross-family | All active families and governed sub-slices | Family A, B1, and B2 complete emissions present together. | complete | current-run computable | comparison-blocked | Consume emitted family facts and states only. | All family and sub-slice reconciliation checks pass. | Required |
| X-P-001 | Cross-family | Active family package | One family complete; one family partial; one family missing. | partial | current-run noncomputable | comparison-blocked | Evaluate only computable concepts; preserve noncomputability for others. | Complete family reconciles; partial/missing family reconciliation blocked. | Required |
| X-M-001 | Cross-family | Source fact dependency | Shared required row-level source fact missing for an active concept. | missing | current-run noncomputable | comparison-blocked | Report missing source fact; do not infer from row text. | Dependent denominator and rate reconciliation blocked. | Required |
| X-NC-001 | Cross-family | Count-only governed evidence | Count emitted without required denominator for a governed rate. | partial | current-run noncomputable | comparison-blocked | Treat as diagnostic-only evidence. | Rate reconciliation blocked by missing denominator. | Required |
| X-NC-002 | Cross-family | Parent and governed sub-slice relationship | Parent family computable; required governed sub-slice noncomputable. | partial | current-run noncomputable | comparison-blocked | Permit parent current-run review only where independent; block sub-slice rule. | Parent reconciles; sub-slice reconciliation blocked. | Required |
| X-CMP-001 | Cross-family | Baseline comparison | Current-run facts computable; baseline migration approved at same concept level. | complete | current-run computable | comparison-allowed | Allow detector comparison only for approved concept. | Current and baseline denominators, markers, and scope reconcile. | Required |
| X-CMP-002 | Cross-family | Baseline comparison | Current-run facts computable; historical concept related but bridge not approved. | complete | current-run computable | bridge-required | Block detector comparison pending review. | Current run reconciles; bridge evidence incomplete. | Required |
| X-CMP-003 | Cross-family | Baseline comparison | Current-run facts computable; historical value retained for reference only. | complete | current-run computable | reference-only | Do not run comparative rule or delta. | Current run reconciles; historical denominator or provenance unusable. | Required |
| X-CMP-004 | Cross-family | Baseline comparison | Current-run facts computable; required migration status missing. | complete | current-run computable | comparison-blocked | Block comparison; do not infer status. | Current run reconciles; migration marker absent. | Required |
| X-CMP-005 | Cross-family | Baseline comparison | Current-run facts noncomputable; baseline present. | missing | current-run noncomputable | comparison-blocked | Block current-run and comparative evaluation for affected concept. | Current-run reconciliation blocked. | Required |
| X-CMP-006 | Cross-family | Family/sub-slice comparison | Family comparison allowed; governed sub-slice comparison status blocked. | partial | current-run computable | comparison-blocked | Compare family only; block sub-slice comparison. | Family reconciles; sub-slice migration marker fails. | Required |
| X-CMP-007 | Cross-family | Historical denominator | Historical baseline present; historical denominator missing. | complete | current-run computable | reference-only | Do not compare against historical value. | Current run reconciles; historical denominator invalid. | Required |
| X-CMP-008 | Cross-family | Historical taxonomy | Historical baseline present; taxonomy changed without approved bridge. | complete | current-run computable | bridge-required | Block comparison pending taxonomy bridge review. | Current run reconciles; taxonomy comparability unresolved. | Required |
| X-CMP-009 | Cross-family | Historical subpopulation | Historical baseline present; subpopulation definition changed. | complete | current-run computable | bridge-required | Block sub-slice comparison pending subpopulation bridge review. | Current run reconciles; subpopulation comparability unresolved. | Required |
| X-CMP-010 | Cross-family | Historical provenance | Historical baseline is report-layer only. | complete | current-run computable | reference-only | Do not treat report-layer value as comparable baseline. | Current run reconciles; historical provenance invalid. | Required |
| X-NI-001 | Cross-family | Historical comparison | Historical report-layer value exists without migration status. | complete | current-run computable | comparison-blocked | Do not infer comparison status from artifact name or path. | Current run reconciles; comparison marker absent. | Required |
| X-NI-002 | Cross-family | Denominator construction | Required denominator missing; another population denominator exists. | partial | current-run noncomputable | comparison-blocked | Do not use alternate denominator. | Rate reconciliation blocked; denominator substitution rejected. | Required |
| X-REC-001 | Cross-family | Aggregate reconciliation | Numerator and non-numerator partitions emitted for eligible denominator. | complete | current-run computable | comparison-blocked | Consume emitted reconciliation status. | Partitions sum exactly to eligible denominator. | Required |
| X-REC-002 | Cross-family | Sub-slice reconciliation | Governed sub-slice denominator emitted with parent denominator. | complete | current-run computable | comparison-blocked | Consume parent/sub-slice relationship as emitted. | Sub-slice denominator is bounded by parent denominator. | Required |
| X-REC-003 | Cross-family | Exclusion reconciliation | Excluded rows emitted with exclusion summary. | complete | current-run computable | comparison-blocked | Do not count excluded rows in governed denominators. | Included plus excluded coverage reconciles to source coverage. | Required |
| X-REC-004 | Cross-family | Split reconciliation | Split-scoped summaries emitted for active split scope. | complete | current-run computable | comparison-blocked | Consume split summaries only as emitted. | Split totals reconcile with aggregate totals. | Required |
| X-REC-005 | Cross-family | Coverage reconciliation | Row-fact coverage summary emitted for governed population. | complete | current-run computable | comparison-blocked | Use coverage status; do not inspect raw rows. | Coverage count reconciles with governed denominator. | Required |
| X-REC-006 | Family A | Failure-subtype reconciliation | Family A subtype counts emitted for non-exact eligible denominator. | complete | current-run computable | comparison-blocked | Consume subtype counts as emitted. | Approved subtype counts sum to non-exact eligible denominator. | Required |
| X-REC-007 | Family B1 | Symbol-name reconciliation | Symbol-name denominator and parent read-file denominator emitted. | complete | current-run computable | comparison-blocked | Consume parent context; do not infer membership. | Symbol-name denominator reconciles with read-file parent context. | Required |
| X-REC-008 | Family B2 | Anchor-category reconciliation | Anchor category counts emitted for active taxonomy. | complete | current-run computable | comparison-blocked | Consume category distribution; do not classify prompts. | Category counts sum to anchor-family denominator. | Required |
| X-REC-009 | Cross-family | Rate reconciliation | Count, denominator, and rate emitted for governed concept. | complete | current-run computable | comparison-blocked | Consume emitted rate only after reconciliation passes. | Rate equals count over denominator according to approved precision. | Required |
| X-REC-010 | Cross-family | Small-denominator visibility | Governed sub-slice has small denominator with visible count and denominator. | complete | current-run computable | comparison-blocked | Report count and denominator; do not hide volatility. | Rate reconciles and denominator remains visible. | Required |

## Coverage Assessment

### Required Coverage Status

| Coverage Area | Status |
|---|---|
| Family A | Covered |
| Family B1 | Covered |
| Family B2 | Covered |
| Complete emissions | Covered |
| Partial emissions | Covered |
| Missing emissions | Covered |
| Noncomputable states | Covered |
| Comparability states | Covered |
| Detector non-inference cases | Covered |
| Reconciliation cases | Covered |

### Uncovered Areas

No required WP8-A coverage areas are intentionally uncovered.

Known dependencies before fixture authoring:

- Exact Family A subtype names and boundaries must be approved before concrete Family A fixture files are authored.
- Family B1 symbol-name ownership and declaration rule must be approved before concrete symbol-name fixture files are authored.
- Family B2 anchor taxonomy and assignment ownership must be approved before concrete anchor fixture files are authored.
- Concrete schema field names are still unavailable by design; WP8-B should remain conceptual or use placeholders until schema authoring begins.

## Recommendation For WP8-B Scope

Recommended WP8-B scope: Common State Fixtures.

WP8-B should convert cross-family state scenarios into fixture-ready definitions before family-specific fixture files are authored.

Recommended WP8-B contents:

- Complete package emission fixture expectation.
- Partial package emission fixture expectation.
- Missing family fixture expectation.
- Missing sub-slice fixture expectation.
- Missing denominator fixture expectation.
- Missing marker fixture expectation.
- Current-run computable plus comparison-blocked fixture expectation.
- Current-run noncomputable plus comparison-blocked fixture expectation.
- Parent aggregate computable with governed sub-slice noncomputable fixture expectation.
- Detector non-inference negative fixture expectation for missing denominators and historical report-layer values.

WP8-B should still avoid concrete fixture files, validator implementation, schema field naming, and runtime changes unless a later implementation phase explicitly authorizes them.

## Sufficiency Assessment

Confidence that this scenario catalog is sufficient for fixture authoring: high.

Rationale:

- Every fixture category from the WP8 matrix plan has at least one scenario.
- Every approved family and governed sub-slice is covered.
- Current-run computability and historical comparability are represented as separate axes.
- Detector non-inference and parent-aggregate substitution failures are explicit.
- Reconciliation requirements are defined before implementation.

Residual risk:

- Family-specific fixture authoring will still depend on approved concrete taxonomy and ownership decisions for Family A, Family B1, and Family B2.
