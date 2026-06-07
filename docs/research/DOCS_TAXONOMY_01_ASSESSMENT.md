# DOCS_TAXONOMY_01_ASSESSMENT
Assessment only. No repository changes were made as part of the assessment itself.

## 1. Executive Summary

The current documentation taxonomy is broadly sound and should be preserved. `docs/research/` is a legitimate long-term category and should be recognized formally alongside `docs/framework/`, `docs/current/`, `docs/continuity/`, `docs/convergence/`, `docs/housekeeping/`, and `docs/deprecated/`.

The taxonomy is strongest when each category has a narrow purpose:
- `framework` for authoritative methodology and process structure
- `current` for present-state guidance and navigation
- `continuity` for compact handoff snapshots
- `convergence` for closed-stage and closure-history evidence
- `housekeeping` for repository governance, preservation authority, and boundary records
- `research` for exploratory research, dataset acquisition strategy, comparative analysis, and provenance-oriented historical analysis
- `deprecated` for superseded content retained only for reference

`docs/research/` fills a gap that none of the other categories covers cleanly. It is the right place for historical research assessments such as `model_fine_tuning_research_assessment.md`, and it is also the best home for publication-strategy and external-dataset evaluation notes that are not current authority and not housekeeping governance.

## 2. Current Taxonomy Assessment

Each category has a distinct purpose, and the overlap is manageable if the boundaries are kept explicit.

| Category | Purpose | Overlap risk |
|---|---|---|
| `docs/framework/` | Canonical methodology, process infrastructure, and lineage | Low |
| `docs/current/` | Active status, parked work, and reading order | Low |
| `docs/continuity/` | Short continuity snapshots across threads/phases | Moderate, mostly with `convergence` |
| `docs/convergence/` | Closed work-package history, assessments, and closure evidence | Moderate, mostly with `housekeeping` |
| `docs/housekeeping/` | Repository governance, preservation, boundaries, compatibility, and architectural decisions | Moderate, mostly with `research` |
| `docs/research/` | Exploratory research and historical analysis of datasets, acquisition strategy, and provenance | Moderate, mostly with `housekeeping` and `convergence` |
| `docs/deprecated/` | Superseded or retired content | Low |

The current taxonomy supports preservation and discoverability better than a single undifferentiated archive would. It also supports public curation by making it easier to exclude exploratory or archive-heavy material from a future curated repository.

## 3. Research Category Assessment

`docs/research/` is a legitimate long-term category.

It should contain:
- external dataset research
- acquisition strategy notes
- comparative literature or dataset reviews
- provenance-relevant historical analysis
- exploratory research assessments
- taxonomy or publication-architecture research notes
- subject-matter memos that inform future governance, but are not themselves governance authority

It should not contain:
- current-state guidance
- authoritative doctrine
- repository governance authority
- closure/phase-completion records
- generated reports or operational manifests
- deprecated material

The category is most useful when it stays research-oriented rather than becoming a catch-all archive.

## 4. Category Boundary Review

The best boundaries are:

- `framework`: what the project believes and how it operates now
- `current`: what a newcomer should read first
- `continuity`: what was handed forward between phases or threads
- `convergence`: what was closed, decided, or archived as part of the project’s evolution
- `housekeeping`: what governed repository structure, preservation, compatibility, and boundary management
- `research`: what was explored, compared, or analyzed as part of strategy or provenance work
- `deprecated`: what was superseded

The main overlap to avoid is mixing `research` into `housekeeping`.
Housekeeping should remain authority-leaning and boundary-oriented.
Research should remain exploratory and analytical.

## 5. Artifact Placement Review

### `docs/research/model_fine_tuning_research_assessment.md`

This file is appropriately placed in `docs/research/`.

Why it fits:
- it is a historical research assessment
- it focuses on training-data acquisition strategy and external dataset evaluation
- it is provenance-relevant, but not authoritative doctrine
- it is not current methodology and not public-curated content

It should remain in `docs/research/`.

### `docs/housekeeping/OSS_PKG_03_CURATED_REPOSITORY_DEFINITION.md`

This file should be preserved, but it does not belong in `docs/housekeeping/`.

Why:
- it is publication-strategy research, not housekeeping authority
- it materially documents the reasoning behind the canonical/private plus curated/public architecture
- it is better classified as research history than as repository housekeeping

Recommended home: `docs/research/`.

### `docs/housekeeping/OSS_PKG_03A_CODEX_FOR_OSS_REASSESSMENT.md`

This file should be preserved, but it also does not belong in `docs/housekeeping/`.

Why:
- it is a reassessment of publication architecture through a Codex-for-OSS reviewer lens
- it belongs with the research trail that informed repository-publication decisions
- it is decision-support history, not housekeeping authority

Recommended home: `docs/research/`.

## 6. OSS-PKG-03 Preservation Review

Both OSS-PKG documents should be preserved and tracked.

They materially contribute to the decision trail that produced the canonical/private + curated/public architecture:
- they explain why the curated repository should be lean
- they document the review cycle that refined that decision
- they provide provenance for later publication decisions
- they help explain why certain archive-heavy surfaces remain canonical-only

They should not be surfaced in the future curated/public repository by default.

They should be preserved in the canonical/private repository only.

## 7. Recommended Taxonomy

Recommended official taxonomy:

- `docs/framework/`
- `docs/current/`
- `docs/continuity/`
- `docs/convergence/`
- `docs/housekeeping/`
- `docs/research/`
- `docs/deprecated/`

Recommended role of `docs/research/`:
- official long-term category
- canonical/private by default
- used for exploratory research, dataset evaluation, acquisition strategy, and provenance analysis
- not a substitute for `framework`, `current`, or `housekeeping`

## 8. Recommended Actions

1. Recognize `docs/research/` as an official category.
2. Keep `docs/research/model_fine_tuning_research_assessment.md` where it is.
3. Move `docs/housekeeping/OSS_PKG_03_CURATED_REPOSITORY_DEFINITION.md` into `docs/research/`.
4. Move `docs/housekeeping/OSS_PKG_03A_CODEX_FOR_OSS_REASSESSMENT.md` into `docs/research/`.
5. Preserve those files as tracked canonical/private historical research artifacts.
6. Do not surface them in the future curated/public repository by default.

## 9. Final Recommendation

Adopt `docs/research/` as a recognized long-term documentation category.
It improves preservation, discoverability, and historical analysis without blurring the boundaries of current methodology or repository governance.

The two OSS_PKG documents should be preserved and relocated into `docs/research/`.
`model_fine_tuning_research_assessment.md` is already correctly located there and should remain.
