# OSS_PKG_03A_CODEX_FOR_OSS_REASSESSMENT

## 1. Executive Summary

OSS-PKG-03 remains broadly correct, but it was optimized for a minimal public package more than for a Codex-for-OSS reviewer. Under a reviewer lens, the repository should still stay lean at the core, but it should also retain a small, deliberate layer of historical evidence showing project evolution, assessment cycles, governance maturity, and sustained work.

The main adjustment is not to reopen the archive wholesale. It is to introduce a narrow middle category, `Curated Historical Evidence`, for a selected subset of historical files. That category is meant to strengthen reviewer confidence without turning the curated repository into a full archive mirror.

Recommended high-level shift:
- keep the core method surface public,
- keep the bulk of data-bearing and generated artifact surfaces canonical-only,
- include a small amount of selected historical evidence,
- keep the public repo readable and inspection-friendly.

## 2. Areas Where OSS-PKG-03 Remains Correct

OSS-PKG-03 is still correct on the main architectural boundaries:

- The curated repository should still center on the regimen, doctrine, methodology, code, tests, and current-state docs.
- The public repo should still avoid bulk `data/`, `evals/data/`, `reports/`, `manifests/runs/`, `manifests/reports/`, `local_review_bundles/`, and `manifests/environment/`.
- The canonical/private repository should remain the full source of truth.
- Compatibility aliases should remain optional, not the driver of the public design.
- The public repo should not try to mirror every operational artifact or historical execution record.

Those recommendations remain correct because they keep the reviewer-facing surface readable and avoid dragging mixed-provenance artifacts into the public default.

## 3. Areas Potentially Over-Pruned

The main over-pruning risk is in treating the historical layer as uniformly canonical-only.

That is too aggressive for a Codex-for-OSS reviewer because the reviewer is not just asking, “Is this clean?” but also, “Does this repo show evidence of serious, sustained, disciplined work?”

The files most likely over-pruned by OSS-PKG-03 are:

- `docs/convergence/`
- `docs/housekeeping/`
- to a lesser extent `docs/continuity/`

These families contain evidence of:
- milestone progression,
- closure and readiness decisions,
- governance evolution,
- preservation policy,
- architecture/protocol transitions,
- and iterative improvement over time.

That evidence is valuable to a reviewer even if the full archive remains private.

## 4. Historical Evidence Assessment

A Codex-for-OSS reviewer benefits from selected historical evidence, not the full history dump.

The useful evidence categories are:
- project evolution,
- assessment cycles,
- governance evolution,
- major milestones,
- and controlled transitions.

That evidence helps a reviewer assess:
- seriousness,
- maintenance quality,
- methodological maturity,
- technical rigor,
- reproducibility,
- and usefulness to the broader ecosystem.

The key constraint is selectivity:
- the curated repo should not carry the entire historical archive,
- but it should carry enough historical evidence to show that the project was built through controlled, reviewed, and documented phases.

## 5. Convergence Assessment

`docs/convergence/` is the strongest candidate for a new middle category.

Why it matters:
- it contains many stage closure and transition records,
- it documents how the regimen was shaped,
- it shows evolution from Stage B through later methodology work,
- it provides direct evidence of disciplined review and closure practices.

Why the whole family should not simply be public core:
- it is very large,
- much of it is repetitive closure/package material,
- it adds explanation burden,
- and it can dominate the public narrative if included wholesale.

Recommended treatment:
- introduce `Curated Historical Evidence` for a selected subset of convergence records,
- keep the bulk of `docs/convergence/` canonical-only.

Representative examples that are reviewer-valuable:
- `STAGE_B_COMPLETION_DETERMINATION.md`
- `STAGE_B_CLOSURE_ASSESSMENT.md`
- `STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md`
- `STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md`
- `STAGE_B_WP8_STAGE_B_MILESTONE_READINESS_DETERMINATION.md`
- `PHASE1_FREEZE_SUMMARY_2026-06-01.md`

Those kinds of files show that the project did not simply appear finished; it was iterated into a controlled state.

## 6. Housekeeping Assessment

`docs/housekeeping/` is also a strong candidate for a curated evidence subset, but not for wholesale inclusion.

Why it matters:
- it captures governance and preservation decisions,
- it shows boundary enforcement,
- it records compatibility and path-decoupling work,
- it documents public-front-door refinement,
- and it preserves review artifacts that demonstrate process seriousness.

Why the whole family should remain mostly canonical-only:
- it is a mixed bag of authority docs, review artifacts, execution reports, preservation records, and process history,
- much of it is internal housekeeping rather than reviewer-facing narrative,
- it adds maintenance and explanation burden,
- and it can overwhelm the curated public repository.

Recommended treatment:
- include a small, intentional subset as `Curated Historical Evidence`,
- keep the rest canonical-only.

Representative reviewer-valuable examples:
- `HOUSEKEEPING_PRESERVATION_INDEX.md`
- `HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md`
- `HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md`
- `OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md`
- `OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md`
- `W1-13_WAVE_1_CLOSURE_REPORT.md`

These files show governance evolution, preservation posture, and bounded public-facing refinement.

## 7. Continuity Assessment

`docs/continuity/` is small and high-signal. Under a Codex-for-OSS reviewer lens, it is better treated as `Public Supporting` than as canonical-only.

Why it matters:
- it captures current project continuity,
- it records operational doctrine snapshots,
- it preserves the state of the project across phases,
- and it is compact enough that inclusion cost is low.

Why it should be public supporting:
- only a few files exist,
- the burden is low,
- the reviewer value is high,
- and it helps connect the public method to the project’s continuity story.

Representative files:
- `project_state_continuity_v1.md`
- `operational_doctrine_snapshot_v1.md`
- `experimental_topology_summary_v1.md`

These are exactly the kind of concise continuity records that help a reviewer understand how the project evolved without opening the full archive.

## 8. Revised Classification Recommendations

A new category is justified:

- `Curated Historical Evidence`

Definition:
- a narrow, reviewer-facing subset of historical documents that demonstrates project evolution, assessment cycles, governance maturity, and major milestones,
- without importing the full archive into the public repo.

### Revised family classifications

| Asset family | OSS-PKG-03 position | Revised position | Rationale |
|---|---|---|---|
| `README.md` | Public Core | Public Core | Front door remains essential. |
| `AGENTS.md` | Public Supporting | Public Supporting | Helpful process guidance. |
| `docs/current/` | Public Core | Public Core | Still the best public orientation layer. |
| `docs/framework/` | Public Core | Public Core | Still core methodology backbone. |
| `docs/convergence/` | Canonical Only | Curated Historical Evidence | Too valuable to hide entirely from a reviewer, but too large for full public inclusion. |
| `docs/continuity/` | Canonical Only or Optional | Public Supporting | Small, compact, and high reviewer value. |
| `docs/housekeeping/` | Canonical Only | Curated Historical Evidence | Selected authority/governance/preservation docs are useful evidence. |
| `docs/deprecated/` | Canonical Only | Canonical Only | Low-value history for the curated repo. |
| `scripts/` | Public Core | Public Core | Core executable regimen. |
| `tests/` | Public Core | Public Core | Essential for rigor and trust. |
| `configs/` | Canonical Only | Canonical Only | Path-heavy and stage-specific; low public value. |
| `evals/` | Mixed | Public Core for the manifest, Canonical Only for data/runs | Keep the canonical eval contract visible; keep corpus/runs private. |
| `evals/data/` | Canonical Only | Canonical Only | Mixed provenance and high burden. |
| `data/` | Canonical Only | Canonical Only | Mixed provenance, high burden. |
| `reports/` | Canonical Only | Canonical Only | Derived artifacts, low public-package value. |
| `manifests/runs/` | Canonical Only | Canonical Only | Operational record. |
| `manifests/reports/` | Canonical Only | Canonical Only | Derived archive. |
| `local_review_bundles/` | Canonical Only | Canonical Only | Preservation bundles, not reviewer-facing. |
| `pyproject.toml` | Public Core | Public Core | Required project metadata. |
| `.gitignore` | Public Supporting | Public Supporting | Low-cost hygiene. |
| `repo_paths.py` | Public Core | Public Core | Useful portability helper. |

## 9. Codex-for-OSS Reviewer Perspective

A Codex-for-OSS reviewer is likely to ask whether the repository is:
- serious,
- stable,
- disciplined,
- reproducible,
- and useful to the broader ecosystem.

A lean repo with no historical evidence can look too polished or too thin.

A curated repo with selected historical evidence signals:
- the work was sustained,
- the methodology was not accidental,
- major decisions were reviewed and closed,
- and the project evolved through controlled stages.

That is especially important for a repository like this one, where the value is the regimen itself. The reviewer should be able to see both:
- the current method,
- and the path by which it got there.

The right balance is:
- public core first,
- supported by a small historical evidence layer,
- with the bulk archive remaining canonical-only.

## 10. Final Recommendation

Retain OSS-PKG-03’s core guidance, but adjust it for a Codex-for-OSS reviewer:

- keep the public repo lean at the core,
- add a new `Curated Historical Evidence` category,
- move `docs/continuity/` to `Public Supporting`,
- include a small curated subset from `docs/convergence/` and `docs/housekeeping/`,
- keep the bulk of the archive canonical-only,
- and continue excluding bulk data, reports, manifests, and review bundles from the curated public default.

In short:
- OSS-PKG-03 was right about minimalism,
- but for a reviewer-grade public repository, minimalism should be moderated by selected evidence of serious, sustained work.
