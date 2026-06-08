Assessment and action authorized if warranted.

# PUBLICATION_ARCHITECTURE_PRESERVATION_ASSESSMENT

## 1. Executive Summary

These publication-architecture artifacts form a coherent decision lineage and should be preserved in the canonical repository.

The set is not a random collection of planning notes. It documents a complete chain of decisions about:
- public repository scope
- public/private authority boundaries
- historical evidence strategy
- rights posture
- curated repository assembly
- version-1 readiness

The correct long-term home remains `docs/research/`. That category is already established as the place for exploratory research, publication-strategy analysis, external-dataset assessment, and provenance-relevant historical analysis. These artifacts fit that role well and do not belong in `docs/housekeeping/` or `docs/current/`.

## 2. Per-Artifact Assessment

| Artifact | Classification | Rationale |
|---|---|---|
| `docs/research/AGENTS_MD_CLASSIFICATION_ASSESSMENT_Grok-Build.md` | Preserve | Supporting decision evidence. It records why `AGENTS.md` belongs in Public Supporting, which fed directly into the curated-repository assembly decisions. It is ancillary, but not disposable. |
| `docs/research/OSS_06_LICENSE_AND_RIGHTS_DECISION.md` | Preserve | Rights posture is a required publication gate. This document anchors the Apache-2.0 recommendation and the public/private rights boundary. |
| `docs/research/OSS_PKG_04_CURATED_HISTORICAL_EVIDENCE_DEFINITION.md` | Preserve | Defines the historical-evidence concept that the later public-repo planning depends on. |
| `docs/research/OSS_PKG_05_PUBLIC_REPOSITORY_PUBLICATION_DOCTRINE.md` | Preserve | Establishes the authority model, category definitions, inclusion/exclusion doctrine, and publication governance. Core decision-lineage artifact. |
| `docs/research/OSS_PKG_06_CURATED_REPOSITORY_IMPLEMENTATION_PLAN.md` | Preserve | Converts doctrine into an implementation-oriented plan. Distinct from doctrine and therefore worth preserving separately. |
| `docs/research/PUBLIC_REPO_01_INITIAL_CONTENT_MANIFEST.md` | Preserve | First candidate definition of curated/public v1 contents. Important decision record. |
| `docs/research/PUBLIC_REPO_02_CURATED_REPOSITORY_ASSEMBLY_PLAN.md` | Preserve | Defines the curated repo structure, reader journey, navigation, and assembly blueprint. Distinct from the content manifest. |
| `docs/research/PUBLIC_REPO_03_HISTORICAL_EVIDENCE_SPINE_DESIGN.md` | Preserve | Specifies how the bounded evidence spine should be presented and kept bounded. |
| `docs/research/PUBLIC_REPO_04_VERSION1_ASSEMBLY_READINESS_DETERMINATION.md` | Preserve | Final readiness determination for beginning Version 1 assembly work. This is the capstone planning gate. |

### Preservation verdict
- Preserve: 9
- Preserve After Adjustment: 0
- Do Not Preserve: 0

## 3. Family Assessment

Yes. Collectively these artifacts form a coherent **Publication Architecture Decision Trail**.

The trail has a clear progression:
1. rights and licensing posture
2. curated historical evidence definition
3. publication doctrine
4. implementation planning
5. initial public content manifest
6. assembly plan
7. historical evidence spine design
8. version-1 assembly readiness

The AGENTS classification note is not a core publication-architecture pillar, but it is still part of the supporting evidence trail because it explains a boundary choice that affected the public repository composition.

## 4. Taxonomy Assessment

`docs/research/` remains the correct long-term home.

Why it fits:
- these files are research and decision-support records
- they are not current authority
- they are not housekeeping governance artifacts
- they are not public-facing curated-repository content
- they are provenance-relevant historical analysis

No better location is required.

## 5. Consolidation Assessment

No artifact should be merged away at this stage.

### Not redundant
- `OSS_PKG_04`, `OSS_PKG_05`, and `OSS_PKG_06` are sequential and distinct.
- `PUBLIC_REPO_01`, `PUBLIC_REPO_02`, `PUBLIC_REPO_03`, and `PUBLIC_REPO_04` are sequential and distinct.
- `OSS_06` is a separate rights gate, not a duplicate of the publication doctrine.
- `AGENTS_MD_CLASSIFICATION_ASSESSMENT_Grok-Build.md` is supporting evidence for a specific supporting-file decision and should remain separate.

### Not superseded
Later artifacts build on earlier ones, but they do not erase them. The later reports depend on the earlier doctrine and evidence decisions, so the chain should remain intact.

### Recommended treatment
- keep all artifacts separate
- preserve them as a documented sequence
- do not compress them into a single summary

## 6. Preservation Recommendation

Preserve the full set.

The publication-architecture effort produced a legitimate decision lineage that belongs in the canonical repository as historical research evidence.

The set is coherent, ordered, and useful for future provenance review, license review, and publication-architecture review.

## 7. Action Taken

Preservation was recommended, so the approved artifacts were staged.

Staged files:
- `docs/research/AGENTS_MD_CLASSIFICATION_ASSESSMENT_Grok-Build.md`
- `docs/research/OSS_06_LICENSE_AND_RIGHTS_DECISION.md`
- `docs/research/OSS_PKG_04_CURATED_HISTORICAL_EVIDENCE_DEFINITION.md`
- `docs/research/OSS_PKG_05_PUBLIC_REPOSITORY_PUBLICATION_DOCTRINE.md`
- `docs/research/OSS_PKG_06_CURATED_REPOSITORY_IMPLEMENTATION_PLAN.md`
- `docs/research/PUBLIC_REPO_01_INITIAL_CONTENT_MANIFEST.md`
- `docs/research/PUBLIC_REPO_02_CURATED_REPOSITORY_ASSEMBLY_PLAN.md`
- `docs/research/PUBLIC_REPO_03_HISTORICAL_EVIDENCE_SPINE_DESIGN.md`
- `docs/research/PUBLIC_REPO_04_VERSION1_ASSEMBLY_READINESS_DETERMINATION.md`
- `docs/research/PUBLICATION_ARCHITECTURE_PRESERVATION_ASSESSMENT.md`

No commits were created.
No pushes were performed.
No repository restructuring was performed.

## 8. Final Recommendation

Keep the publication-architecture decision trail preserved in `docs/research/` as a tracked historical record.

Do not collapse these artifacts into a single note. Their sequence is the value.

The canonical repository now has a coherent preserved lineage for:
- rights posture
- publication doctrine
- historical evidence strategy
- curated repository assembly
- version-1 readiness
