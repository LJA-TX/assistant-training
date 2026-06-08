Assessment only. No repository changes were made.

Below is the report content for `OSS_PKG_05_PUBLIC_REPOSITORY_PUBLICATION_DOCTRINE.md`.

# OSS_PKG_05_PUBLIC_REPOSITORY_PUBLICATION_DOCTRINE

## 1. Executive Summary

The publication doctrine should establish a one-way authority model:

- `assistant-training-private` is the canonical source of truth.
- `assistant-training` is a curated public derivative, not a mirror and not a second authority center.

The curated repository should be selective, reviewable, and intentionally incomplete relative to the canonical repository. It must present the public method clearly, preserve a small amount of historical evidence, and exclude bulk operational and provenance-heavy material that does not improve public understanding.

The core doctrine is:

- canonical/private owns truth;
- curated/public owns presentation;
- canonical wins on conflict;
- public content is derived and reviewable;
- bulk archive, data, generated artifacts, and research notes remain canonical-only by default.

## 2. Repository Relationship Doctrine

### Canonical Repository
The canonical repository must be the authoritative source for:
- substantive content
- methodology changes
- governance decisions
- provenance records
- historical archive material
- publication decisions that affect meaning or policy

### Curated Repository
The curated repository is a public-facing derivative that should:
- expose the public method
- surface selected historical evidence
- remain readable to a technically competent outsider
- avoid becoming an archive mirror

### Authority
- Canonical/private is authoritative for content, policy, and historical record.
- Curated/public is authoritative only for its own presentation layer and selection choices within the published package.
- The curated repository must not redefine doctrine, methodology, or source-of-truth semantics.

### Ownership
- Canonical/private owns the underlying record.
- Curated/public owns the public package form, not the underlying truth.
- Public-facing artifacts may be authored for the curated repository, but only as derived publication artifacts and never as competing authority.

### Precedence
- If the two repositories differ, canonical/private prevails.
- Any public divergence is a publication defect unless it is a narrowly defined presentation-only variation that does not alter substance.
- The curated repository must be regenerated or corrected to match canonical truth.

### Conflict Resolution
- Treat divergence as stale publication state, not as alternative truth.
- Correct by re-deriving the curated view from canonical-approved material.
- If the discrepancy changes meaning, the canonical repository must be corrected first, then the curated repository republished from it.

## 3. Publication Category Definitions

| Category | Formal definition | Intended purpose |
|---|---|---|
| Public Core | Must be present in the curated repository. Defines the public method and makes the repository inspectable. | Present the regimen, doctrine, current-state guidance, executable core, and canonical evaluation contract. |
| Public Supporting | Useful to include. Improves onboarding, navigation, or review quality, but is not strictly required for understanding the method. | Reduce friction without expanding the public surface into an archive. |
| Curated Historical Evidence | A small, reviewer-facing subset of historical material that directly shows methodology evolution, governance maturity, or major milestones. | Help reviewers understand how the current method came to be without exposing the full archive. |
| Canonical Only | Must remain only in the canonical/private repository unless explicitly reclassified later. | Preserve bulk history, data lineage, generated artifacts, and provenance-heavy material without adding public noise. |

### Primary purpose of each category
- Public Core: answer “what is this and how do I inspect it?”
- Public Supporting: answer “what helps a reviewer or newcomer without adding clutter?”
- Curated Historical Evidence: answer “how did this method evolve?”
- Canonical Only: answer “what must remain preserved privately because it is too heavy, too sensitive, or too noisy for the curated repo?”

## 4. Inclusion Doctrine

### Qualifies for publication when it:
- directly explains the methodology
- defines or documents current doctrine
- supports the reusable framework
- helps a public reader inspect the regimen
- validates current behavior or canonical evaluation
- shows a major historical inflection point without requiring the full archive
- is stable enough to survive public inspection without constant churn

### Methodology
Include if the document:
- explains the regimen
- captures a reusable process
- clarifies behavior, contracts, or evaluation logic
- is not just a project-local experiment log

### Doctrine
Include if the document:
- defines binding rules or current operating policy
- is part of the authoritative method surface
- is necessary to understand the public package

### Framework
Include if the document:
- is reusable
- is part of the current method stack
- helps a reader inspect the core regimen
- is not merely historical residue

### Current-State Material
Include if the document:
- orients a newcomer
- identifies the current boundary
- explains what is active, parked, or preserved
- is part of the public inspection path

Exclude if it is:
- a local execution snapshot
- a machine-specific note
- a private working memo
- an internal-only operational trace

### Tests
Include if the test:
- protects a public contract
- validates current method behavior
- demonstrates reproducibility or evaluation discipline

Exclude if the test is:
- one-off diagnostics
- recovery-only
- tightly coupled to private archive mechanics
- noisy enough that it obscures the public method

### Scripts
Include if the script:
- implements core training, evaluation, dataset construction, path resolution, or preflight logic
- is part of the reusable regimen
- is stable enough to be reviewed publicly

Exclude if the script is:
- a one-off recovery tool
- a transient diagnostic
- a local-only investigation helper
- too tied to private artifacts to be understandable in the public repo

### Historical Evidence
Include only if the document:
- captures a major inflection point
- records a closure, freeze, or gate decision
- shows a governance or publication decision
- helps explain why the current method looks the way it does
- is compact enough to read without archive context

Historical evidence must be selected, not bulk-imported.

## 5. Exclusion Doctrine

The following must remain canonical-only by default:

- `data/`
- `evals/data/`
- `reports/`
- `manifests/runs/`
- `manifests/reports/`
- `manifests/environment/`
- generated artifacts of any kind
- bulk archives
- research artifacts
- provenance-sensitive material
- local review bundles
- machine-specific operational residue

### Specific exclusions
- `data/`: mixed-provenance training and lineage material; too heavy for the public default.
- `reports/`: generated analysis, scoring, and output summaries; useful privately, noisy publicly.
- `manifests/`: operational run manifests and report manifests remain private unless a specific canonical contract artifact is explicitly included.
- `generated artifacts`: do not publish by default.
- `bulk archives`: do not publish by default.
- `research artifacts`: exploratory or publication-strategy memos remain canonical-only unless distilled into a framework or historical evidence record.
- `provenance-sensitive material`: anything whose main value is internal traceability rather than public inspection.

### Important nuance
The canonical evaluation manifest is an exception to the general `manifests/` exclusion rule when it functions as the public evaluation contract. Operational manifests remain canonical-only.

## 6. Authority and Conflict Resolution Doctrine

### Which repository is authoritative?
`assistant-training-private` is authoritative.

### What happens when differences exist?
- Differences are treated as publication defects in the curated repository.
- Canonical/private prevails.
- The curated repository must be corrected or re-derived.

### May public-repository edits originate independently?
- Not for content-bearing authority.
- Presentation-only artifacts may be authored for the curated repository if they are clearly derivative, traceable, and non-authoritative.
- No public-only edit may introduce a new normative claim or override canonical meaning.

### How should publication errors be corrected?
- Correct the canonical source if the underlying substance is wrong.
- Otherwise, regenerate or patch the curated repository from canonical-approved material.
- Treat unapproved public divergence as stale publication state, not as a parallel truth.

### Operating rule
The curated repository is a publication product, not an authority source.

## 7. Curated Historical Evidence Doctrine

`Curated Historical Evidence` is a bounded evidence layer for public reviewers. It exists to show evolution, not to recreate the archive.

### Selection criteria
A document qualifies if it:
- marks a major methodological pivot
- captures a major architectural or governance decision
- records a closure, readiness, or freeze point
- shows an independent review that influenced direction
- explains a publication-architecture decision
- shows how the current public method emerged

### Growth limits
- The set must remain small and bounded.
- Every addition must justify its unique reviewer value.
- Repetitive or redundant documents should not be added simply because they are historically interesting.
- If a document’s value is mostly archival, keep it canonical-only.

### Archival pressure
As the evidence set grows, it should be pruned, not allowed to become a secondary archive. If a new historical doc does not add a new question/answer pair for the reviewer, it should not be included.

### Reviewer value
The curated historical evidence should let a reviewer understand:
- methodology evolution
- governance maturity
- major milestone transitions
- publication and preservation decisions
- why the current regimen has the shape it does

### Recommended source families
- `docs/framework/lineages/`
- selected `docs/framework/methodology/` records
- selected `docs/current/` milestone or boundary docs
- selected `docs/continuity/` snapshots
- a small number of governance/publication documents from `docs/housekeeping/`

### Not part of the default curated evidence set
- bulk `docs/convergence/`
- bulk `docs/research/`
- bulk `docs/housekeeping/`
- generated artifacts and run records

## 8. Publication Principles

The publication process should follow these principles:

- intentional: every public artifact has a reason to exist
- selective: not everything canonical should be public
- derived: the curated repository is produced from canonical-approved material
- reviewable: every public artifact can be justified to a reviewer
- traceable: public artifacts should map back to canonical origin
- bounded: the historical evidence layer must not expand into a second archive
- explainable: a technically competent reader should be able to understand why each artifact is public
- non-mirrored: the curated repository is not a full copy of the canonical repository

## 9. Codex-for-OSS Assessment

This doctrine would help:
- public reviewers, by making the public package legible and bounded
- researchers, by showing the method and selected evolution without archive overload
- future maintainers, by clarifying what belongs where and why
- Codex-for-OSS evaluators, by making authority, selection, and provenance rules explicit

It improves reviewer confidence because it shows:
- the public repo is intentional, not accidental
- the historical layer is evidence-driven, not archival sprawl
- the canonical/private repository remains the authority
- publication is a controlled act, not a broad mirror of internal work

## 10. Final Recommendation

Adopt this doctrine as the governing policy for future publication decisions.

In practice:
- keep `assistant-training-private` as the source of truth
- keep `assistant-training` as a selective public derivative
- make Public Core the stable inspection surface
- keep Public Supporting small and helpful
- maintain a bounded Curated Historical Evidence spine
- keep bulk data, reports, manifests, generated artifacts, and research artifacts canonical-only by default

The curated repository should help a reviewer understand the project, not overwhelm them with the full archive.
