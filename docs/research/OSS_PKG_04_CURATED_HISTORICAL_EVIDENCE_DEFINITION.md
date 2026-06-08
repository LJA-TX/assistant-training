No repository changes were made.

# OSS_PKG_04_CURATED_HISTORICAL_EVIDENCE_DEFINITION

## 1. Executive Summary

`Curated Historical Evidence` should be a narrow, reviewer-facing evidence layer, not a second archive. The public reader should see just enough history to understand how the methodology evolved, how major gates were crossed, and why the repository looks the way it does today.

The strongest source for this layer is not `docs/convergence/` itself, but the distilled surfaces that already exist under `docs/framework/lineages/` and selected files under `docs/framework/methodology/` and `docs/current/`. `docs/continuity/` is useful supporting evidence. `docs/housekeeping/` contributes a small number of governance and publication-architecture milestones. `docs/research/` is mostly canonical/private historical record only.

Best overall shape:
- essential historical evidence: compact, decision-bearing, distilled
- supporting historical evidence: compact context that strengthens the narrative
- canonical historical record only: bulk archive, exploratory memos, generated artifacts, and detailed internal records

Publication form recommendation:
- hybrid, not summaries-only and not archive-dump wholesale

## 2. Definition of Curated Historical Evidence

`Curated Historical Evidence` is the smallest intentional set of historically significant documents that a public reader should be shown because they directly evidence how the methodology, governance, or publication stance evolved, and because they can be understood without consulting the full canonical archive.

It is:
- a selection rule
- a presentation layer
- a reviewer-aid

It is not:
- an authority layer
- a doctrine layer
- a replacement for the canonical historical record
- a bulk archive category

## 3. Inclusion Criteria

A document qualifies as `Curated Historical Evidence` if it meets most of the following:
- it marks a major methodological pivot
- it captures a major architectural or governance decision
- it records a closure, freeze, readiness, or milestone determination
- it shows an independent review that materially influenced direction
- it explains a publication-architecture or preservation decision
- it is concise enough to read without the rest of the archive
- it is decision-bearing rather than merely descriptive
- it helps answer “why does the current method look like this?”

Good examples of qualifying content:
- contamination discipline and anti-overlap enforcement
- isolated-variable methodology pivots
- schema-coupling discoveries
- freeze/closure and migration-gate decisions
- public-front-door refinement
- preservation and compatibility governance

## 4. Exclusion Criteria

A document does not qualify if it is primarily:
- routine housekeeping
- operational log material
- generated report output
- an intermediate draft
- a compatibility alias page
- a repetitive package review
- a bulk run manifest or artifact bundle
- a dense research memo that requires archive context to interpret
- a path-heavy or machine-specific execution surface
- something already fully captured by a concise lineage or methodology summary

Specific exclusions by family:
- `docs/convergence/` bulk package records and alias shells
- `docs/research/` exploratory memos by default
- `reports/`, `manifests/reports/`, `manifests/runs/`, `data/`, and similar generated or data-bearing surfaces
- verbose implementation summaries that do not add a new decision point

## 5. Historical Classification Framework

| Tier | Meaning | Best sources | Public treatment |
|---|---|---|---|
| Essential Historical Evidence | Minimal spine that explains the project’s evolution and major inflection points | `docs/framework/lineages/` and a few selected files under `docs/framework/methodology/` and `docs/current/` | Public-facing and easy to reach |
| Supporting Historical Evidence | Helpful context that strengthens confidence and fills in the narrative, but is not required to understand the method | Selected `docs/continuity/` docs and a very small subset of governance/publication docs | Public if space permits |
| Canonical Historical Record Only | Full archive, exploratory memos, generated artifacts, detailed reviews, and compatibility scaffolding | Bulk `docs/convergence/`, bulk `docs/housekeeping/`, `docs/research/`, and data/report/manifests surfaces | Private canonical only by default |

Practical rule:
- if a document already exists as a distilled lineage or methodology record, prefer that form
- if a document is still a detailed archive record, keep it canonical-only unless there is a strong reviewer need

## 6. Candidate Artifact Assessment

| Artifact | Assessment | Recommended tier |
|---|---|---|
| [docs/framework/lineages/](/opt/ai-stack/assistant-training/docs/framework/lineages/) | This is the clearest evidence spine: compact, durable, and already distilled into major inflection points. | Essential Historical Evidence |
| [docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md](/opt/ai-stack/assistant-training/docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md) | Shows how the process architecture was formed and why the regimen was extracted the way it was. | Essential Historical Evidence |
| [docs/framework/methodology/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/framework/methodology/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md) | Documents methodology extraction from the convergence arc into framework structure. | Essential Historical Evidence |
| [docs/framework/methodology/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/framework/methodology/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md) | Marks a major transition and is directly useful for explaining how the current structure emerged. | Essential Historical Evidence |
| [docs/framework/methodology/STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/framework/methodology/STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md) | Useful for showing methodological generalization, but more specific than the core spine. | Supporting Historical Evidence |
| [docs/framework/methodology/STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/framework/methodology/STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md) | Shows a governance/method shift that a reviewer can use to assess maturity. | Supporting Historical Evidence |
| [docs/framework/methodology/STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md](/opt/ai-stack/assistant-training/docs/framework/methodology/STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md) | Completes the blocker-oriented branch narrative; useful context, not the first thing a reader needs. | Supporting Historical Evidence |
| [docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md](/opt/ai-stack/assistant-training/docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md) | Compact marker of a major state transition. | Supporting Historical Evidence |
| [docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md](/opt/ai-stack/assistant-training/docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md) | Shows forward movement after the freeze point and helps explain the current trajectory. | Supporting Historical Evidence |
| [docs/continuity/project_state_continuity_v1.md](/opt/ai-stack/assistant-training/docs/continuity/project_state_continuity_v1.md) | Compact handoff snapshot; high signal and low burden. | Supporting Historical Evidence |
| [docs/continuity/operational_doctrine_snapshot_v1.md](/opt/ai-stack/assistant-training/docs/continuity/operational_doctrine_snapshot_v1.md) | A small, direct summary of binding doctrine and operating rules. | Supporting Historical Evidence |
| [docs/continuity/experimental_topology_summary_v1.md](/opt/ai-stack/assistant-training/docs/continuity/experimental_topology_summary_v1.md) | Useful historical context, but more specific and somewhat more technical than the continuity snapshots above. | Supporting Historical Evidence |
| [docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md](/opt/ai-stack/assistant-training/docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md) | Independent review evidence is valuable to a reviewer because it shows external scrutiny and reconciliation. | Supporting Historical Evidence |
| [docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md](/opt/ai-stack/assistant-training/docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md) | Shows the public-facing refinement pass and why the front door improved. | Supporting Historical Evidence |
| [docs/housekeeping/W1-13_WAVE_1_CLOSURE_REPORT.md](/opt/ai-stack/assistant-training/docs/housekeeping/W1-13_WAVE_1_CLOSURE_REPORT.md) | Important as a closure record, but more archival than essential once the core history is already distilled elsewhere. | Supporting Historical Evidence |
| [docs/housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md](/opt/ai-stack/assistant-training/docs/housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md) | Strong governance index, but mostly an internal authority/preservation artifact. | Canonical Historical Record Only unless selectively summarized |
| [docs/housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md](/opt/ai-stack/assistant-training/docs/housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md) | Useful internal architecture trail, but too plan-heavy to be default public evidence. | Canonical Historical Record Only unless selectively summarized |
| [docs/housekeeping/HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md](/opt/ai-stack/assistant-training/docs/housekeeping/HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md) | Good provenance for path cleanup, but more of an internal implementation-governance record. | Canonical Historical Record Only unless selectively summarized |
| [docs/research/model_fine_tuning_research_assessment.md](/opt/ai-stack/assistant-training/docs/research/model_fine_tuning_research_assessment.md) | Exploratory, dataset-specific, and provenance-relevant, but too research-heavy for the public evidence spine. | Canonical Historical Record Only |
| [docs/research/OSS_PKG_03_CURATED_REPOSITORY_DEFINITION.md](/opt/ai-stack/assistant-training/docs/research/OSS_PKG_03_CURATED_REPOSITORY_DEFINITION.md) | Publication-architecture research. Important for decision trail, but too meta for the public evidence set. | Canonical Historical Record Only |
| [docs/research/OSS_PKG_03A_CODEX_FOR_OSS_REASSESSMENT.md](/opt/ai-stack/assistant-training/docs/research/OSS_PKG_03A_CODEX_FOR_OSS_REASSESSMENT.md) | Reviewer reassessment of publication architecture; useful privately, but not public evidence of methodology evolution. | Canonical Historical Record Only |
| [docs/research/DOCS_TAXONOMY_01_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/research/DOCS_TAXONOMY_01_ASSESSMENT.md) | Taxonomy analysis is valuable context, but it is still a meta-research artifact. | Canonical Historical Record Only |
| Bulk [docs/convergence/](/opt/ai-stack/assistant-training/docs/convergence/) compatibility/closure records | Important archive, but mostly too detailed and repetitive for curated public evidence. | Canonical Historical Record Only |

## 7. Publication Form Assessment

### Option A: Original documents
Strengths:
- preserves authenticity
- preserves the actual decision trail
- makes it easy to cite exact records

Weaknesses:
- too much detail if used wholesale
- can recreate archive noise in the public repo

### Option B: Curated summaries
Strengths:
- readable
- compact
- easy to orient newcomers and reviewers

Weaknesses:
- weaker provenance signal if used alone
- can feel detached from the actual record

### Option C: Hybrid approach
Recommended.

Why:
- use original documents for the small essential spine
- use curated summaries or short indexes when a historical cluster is too large or repetitive
- preserve the real record, but expose only the parts a reviewer needs to see

This is the best fit for a Codex-for-OSS reviewer because it keeps the audit trail real without making the public repository feel like an archive dump.

## 8. Codex-for-OSS Reviewer Perspective

For a reviewer looking for seriousness, sustained work, methodology maturity, governance discipline, technical rigor, and reproducibility, enough historical evidence is:
- enough to explain the major inflection points
- enough to show that the project evolved through reviewed gates
- enough to demonstrate that the current method did not appear accidentally

A good target is:
- one small evidence spine
- 1 to 2 docs per major inflection point
- about 6 to 12 curated documents total, plus one small index if needed

That is enough to answer:
- how contamination discipline evolved
- how the isolated-variable methodology emerged
- how freeze/closure and transition decisions were made
- how governance and publication framing changed over time

If the reader has to browse the bulk archive to understand the story, the curated evidence set is too large.

## 9. Recommended Curated Historical Evidence Set

Recommended default set for a future public repository:
- [docs/framework/lineages/](/opt/ai-stack/assistant-training/docs/framework/lineages/)
- [docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md](/opt/ai-stack/assistant-training/docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md)
- [docs/framework/methodology/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/framework/methodology/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md)
- [docs/framework/methodology/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/framework/methodology/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md)
- [docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md](/opt/ai-stack/assistant-training/docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md)
- [docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md](/opt/ai-stack/assistant-training/docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md)
- [docs/continuity/project_state_continuity_v1.md](/opt/ai-stack/assistant-training/docs/continuity/project_state_continuity_v1.md)
- [docs/continuity/operational_doctrine_snapshot_v1.md](/opt/ai-stack/assistant-training/docs/continuity/operational_doctrine_snapshot_v1.md)
- [docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md](/opt/ai-stack/assistant-training/docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md)
- [docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md](/opt/ai-stack/assistant-training/docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md)

Not part of the default public evidence set:
- bulk [docs/convergence/](/opt/ai-stack/assistant-training/docs/convergence/)
- bulk [docs/housekeeping/](/opt/ai-stack/assistant-training/docs/housekeeping/)
- all of [docs/research/](/opt/ai-stack/assistant-training/docs/research/)
- bulk generated surfaces such as [reports/](/opt/ai-stack/assistant-training/reports/), [manifests/reports/](/opt/ai-stack/assistant-training/manifests/reports/), [manifests/runs/](/opt/ai-stack/assistant-training/manifests/runs/), and [data/](/opt/ai-stack/assistant-training/data/)

## 10. Final Recommendation

Adopt `Curated Historical Evidence` as a narrow, hybrid-backed, reviewer-facing selection layer.

In practice:
- make `docs/framework/lineages/` the primary historical evidence spine
- surface a few selected canonicalized methodology and current-state docs
- keep a tiny number of housekeeping governance/review summaries available if they materially explain the evolution
- keep `docs/research/` and the bulk archive surfaces canonical-only by default

That gives a public reader enough history to understand the method’s evolution without turning the curated repository into an archive.
