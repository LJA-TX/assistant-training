# OSS_PKG_03_CURATED_REPOSITORY_DEFINITION
Assessment only. No repository changes were made.

## 1. Executive Summary

The curated/public repository should be a lean, methodology-first derivative of `assistant-training-private`, not a second archive. Its job is to make the regimen easy to understand, easy to inspect, and easy to trust without importing the full historical, data-bearing, or operational record into the public default.

The public repository should therefore center on:
- the front door,
- current-state orientation,
- the doctrine and methodology docs,
- the executable scripts,
- the verification tests,
- the canonical evaluation manifest,
- and a small amount of light-weight support metadata.

The public repository should not carry:
- the mixed-provenance data surfaces,
- generated reports,
- run manifests,
- artifact caches,
- local review bundles,
- or the long historical closure/continuity/housekeeping archive.

Compatibility aliases and small support files can be retained if they materially improve discoverability, but they are optional. The public repo should prioritize clarity over exhaustive preservation.

## 2. Curated Repository Purpose Statement

`LJA-TX/assistant-training` should present the public-facing regimen: a compact, inspectable repository that explains the project’s purpose, shows the current governing doctrine, exposes the core execution and verification code, and publishes the canonical evaluation contract without dragging the private archive into the public surface.

## 3. Asset Family Classification Matrix

| Asset family | Category | Rationale |
|---|---|---|
| [README.md](/opt/ai-stack/assistant-training/README.md) | Public Core | The front door. It is the first public explanation of what the repository is, why it exists, and how to orient quickly. |
| Root doctrine docs: [docs/goal_charter_v5a.md](/opt/ai-stack/assistant-training/docs/goal_charter_v5a.md), [docs/appendix_a_operational_execution_contract_v3a.md](/opt/ai-stack/assistant-training/docs/appendix_a_operational_execution_contract_v3a.md), [docs/metric_specification_v1a.md](/opt/ai-stack/assistant-training/docs/metric_specification_v1a.md), [docs/evaluation_manifest_v1.md](/opt/ai-stack/assistant-training/docs/evaluation_manifest_v1.md), [docs/repo_layout.md](/opt/ai-stack/assistant-training/docs/repo_layout.md) | Public Core | These files define the regime, the operational contract, the metric framing, the evaluation framing, and the layout/orientation model. |
| [docs/current/](/opt/ai-stack/assistant-training/docs/current/) | Public Core | This is the public orientation layer for current state, parked work, and quick inspection. |
| [docs/framework/](/opt/ai-stack/assistant-training/docs/framework/) | Public Core | This is the methodology backbone, including the current framework, process infrastructure, and lineage notes that explain how the regimen evolved. |
| [scripts/](/opt/ai-stack/assistant-training/scripts/) | Public Core | The executable regimen. The public repo should keep the stable training/evaluation helpers and the scripts needed to inspect the method. |
| [tests/](/opt/ai-stack/assistant-training/tests/) | Public Core | Verification is part of the public value proposition. The tests show the contracts and keep the regimen inspectable. |
| [pyproject.toml](/opt/ai-stack/assistant-training/pyproject.toml) | Public Core | Basic packaging, dependency, and test configuration belongs in the public repo. |
| [repo_paths.py](/opt/ai-stack/assistant-training/repo_paths.py) | Public Core | Small, central portability helper; useful for scripts and path discipline. |
| [evals/canonical_eval_manifest_v1.json](/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json) | Public Core | The canonical evaluation contract is part of the public method and should be visible by default. |
| [AGENTS.md](/opt/ai-stack/assistant-training/AGENTS.md) | Public Supporting | Helpful process dispatcher and authority-order note, but not essential to the public understanding of the regimen. |
| [.gitignore](/opt/ai-stack/assistant-training/.gitignore) | Public Supporting | Low-cost hygiene metadata that helps avoid accidental noise in the public repo. |
| [docs/process_infrastructure/](/opt/ai-stack/assistant-training/docs/process_infrastructure/) | Optional | Compatibility pointer only. Useful if link preservation matters, but not required for the curated public surface. |
| [docs/lineages/](/opt/ai-stack/assistant-training/docs/lineages/) | Optional | Compatibility alias only. Small and discoverability-friendly, but duplicative. |
| [docs/potential_skills/](/opt/ai-stack/assistant-training/docs/potential_skills/) | Optional | Small supplemental note; useful, but not central to the public method. |
| [docs/convergence/](/opt/ai-stack/assistant-training/docs/convergence/) | Canonical Only | Large closure and transition archive. High noise, high explanation burden, not needed for the curated public repo. |
| [docs/continuity/](/opt/ai-stack/assistant-training/docs/continuity/) | Canonical Only | Useful continuity record, but still archive material rather than public-front-door material. |
| [docs/housekeeping/](/opt/ai-stack/assistant-training/docs/housekeeping/) | Canonical Only | Internal review, preservation, and process history. Valuable privately, too heavy publicly. |
| [docs/history/](/opt/ai-stack/assistant-training/docs/history/) | Canonical Only | Deprecated material is not part of the clean public narrative. |
| Transitional/historical root docs: [docs/migration_checklist.md](/opt/ai-stack/assistant-training/docs/migration_checklist.md), [docs/assistant_training_goal_documents_and_artifacts_index.md](/opt/ai-stack/assistant-training/docs/assistant_training_goal_documents_and_artifacts_index.md), [docs/assistant_training_initial_ChatGPT_thread_summary.md](/opt/ai-stack/assistant-training/docs/assistant_training_initial_ChatGPT_thread_summary.md), [docs/repository_establishment_plan_v1.md](/opt/ai-stack/assistant-training/docs/repository_establishment_plan_v1.md) | Canonical Only | These are useful internal history and index material, but they are not necessary for the curated public package. |
| [configs/](/opt/ai-stack/assistant-training/configs/) | Canonical Only | Stage-specific, path-heavy configuration material. Useful privately; too costly for the public default. |
| [evals/data/](/opt/ai-stack/assistant-training/evals/data/) | Canonical Only | Mixed-provenance evaluation corpus. Important privately, but not appropriate for the clean public boundary. |
| [evals/runs/](/opt/ai-stack/assistant-training/evals/runs/) | Canonical Only | Generated evaluation run outputs. Better kept in the canonical repo. |
| [data/](/opt/ai-stack/assistant-training/data/) | Canonical Only | Mixed-provenance training data and lineage material; high burden and not required for the public repo’s core value. |
| [reports/](/opt/ai-stack/assistant-training/reports/) | Canonical Only | Derived reporting artifacts. Useful as evidence, but too noisy for the curated public repo. |
| [manifests/runs/](/opt/ai-stack/assistant-training/manifests/runs/) | Canonical Only | Operational run records and machine-local traces. |
| [manifests/reports/](/opt/ai-stack/assistant-training/manifests/reports/) | Canonical Only | Derived report/manifests archive. Valuable privately, not part of the public front door. |
| [manifests/environment/](/opt/ai-stack/assistant-training/manifests/environment/) | Canonical Only | Environment snapshots are machine-specific and not needed in the public package. |
| [artifacts/](/opt/ai-stack/assistant-training/artifacts/) | Canonical Only | Generated training/execution artifacts. High burden, low public-package value. |
| [local_review_bundles/](/opt/ai-stack/assistant-training/local_review_bundles/) | Canonical Only | Dense preservation bundles. Keep these in the canonical repository. |

## 4. Methodology Value Matrix

| Asset family | Methodology value | Why |
|---|---|---|
| [README.md](/opt/ai-stack/assistant-training/README.md) | Core | Establishes the project identity and the first explanation of the regimen. |
| Root doctrine docs | Core | These are the project’s rule-set, contract, metric framing, and layout guide. |
| [docs/current/](/opt/ai-stack/assistant-training/docs/current/) | Core | Gives the current state, reading order, and boundary conditions. |
| [docs/framework/](/opt/ai-stack/assistant-training/docs/framework/) | Core | Contains the methodology and lineage material that explains the regimen itself. |
| [scripts/](/opt/ai-stack/assistant-training/scripts/) | Core | The runtime embodiment of the method. |
| [tests/](/opt/ai-stack/assistant-training/tests/) | Important | Shows the verification discipline and the observable contracts. |
| [pyproject.toml](/opt/ai-stack/assistant-training/pyproject.toml) | Important | Captures the execution and test configuration needed to understand and run the code. |
| [repo_paths.py](/opt/ai-stack/assistant-training/repo_paths.py) | Important | Important portability and path-resolution helper. |
| [evals/canonical_eval_manifest_v1.json](/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json) | Important | Makes the canonical evaluation setup inspectable and reproducible. |
| [AGENTS.md](/opt/ai-stack/assistant-training/AGENTS.md) | Supporting | Helpful process routing, but not central to the regimen itself. |
| [.gitignore](/opt/ai-stack/assistant-training/.gitignore) | Supporting | Hygiene aid, useful but not method-defining. |
| [docs/process_infrastructure/](/opt/ai-stack/assistant-training/docs/process_infrastructure/) | Supporting | Compatibility alias; helps discoverability but duplicates canonical paths. |
| [docs/lineages/](/opt/ai-stack/assistant-training/docs/lineages/) | Supporting | Compatibility alias; adds discoverability, not core method content. |
| [docs/potential_skills/](/opt/ai-stack/assistant-training/docs/potential_skills/) | Supporting | Small supplemental concept note. |
| [docs/convergence/](/opt/ai-stack/assistant-training/docs/convergence/) | Important | Rich history of methodological transitions and closures, though too heavy for the default public surface. |
| [docs/continuity/](/opt/ai-stack/assistant-training/docs/continuity/) | Supporting | Useful continuity context, but not core to understanding the method. |
| [docs/housekeeping/](/opt/ai-stack/assistant-training/docs/housekeeping/) | Minimal | Mostly internal process and review history rather than methodology itself. |
| [docs/history/](/opt/ai-stack/assistant-training/docs/history/) | Minimal | Deprecated material is historically interesting but not necessary for the curated public method. |
| Transitional/historical root docs | Supporting | Useful for provenance and internal continuity, but not necessary for the public method. |
| [configs/](/opt/ai-stack/assistant-training/configs/) | Important | Configuration records help explain how the regimen was run, but they are too stage-specific for the public default. |
| [evals/data/](/opt/ai-stack/assistant-training/evals/data/) | Important | The evaluation corpus is method-relevant, but its provenance burden is too high for the curated public repo. |
| [evals/runs/](/opt/ai-stack/assistant-training/evals/runs/) | Supporting | Helpful for traceability, but not required to understand the method. |
| [data/](/opt/ai-stack/assistant-training/data/) | Important | Training data lineage matters to the regimen, but not to the public front door. |
| [reports/](/opt/ai-stack/assistant-training/reports/) | Supporting | Shows outputs and evaluation summaries, but not the core method itself. |
| [manifests/runs/](/opt/ai-stack/assistant-training/manifests/runs/) | Supporting | Operational evidence, not method definition. |
| [manifests/reports/](/opt/ai-stack/assistant-training/manifests/reports/) | Supporting | Derived evidence archive, not core method. |
| [manifests/environment/](/opt/ai-stack/assistant-training/manifests/environment/) | Supporting | Reproducibility evidence, but machine-specific. |
| [artifacts/](/opt/ai-stack/assistant-training/artifacts/) | Supporting | Useful operational evidence, but not core to the method narrative. |
| [local_review_bundles/](/opt/ai-stack/assistant-training/local_review_bundles/) | Minimal | Preservation bundles add little to understanding the regimen. |

## 5. Publication Cost Matrix

| Asset family | Publication cost | Why |
|---|---|---|
| [README.md](/opt/ai-stack/assistant-training/README.md) | Low | Small, stable, and portable. |
| Root doctrine docs | Moderate | Need some explanation, but are still relatively compact and core. |
| [docs/current/](/opt/ai-stack/assistant-training/docs/current/) | Moderate | Helpful but requires keeping current-state language aligned. |
| [docs/framework/](/opt/ai-stack/assistant-training/docs/framework/) | Moderate | Methodology-rich; not noisy, but detailed enough to require careful orientation. |
| [scripts/](/opt/ai-stack/assistant-training/scripts/) | High | Path cleanup, stability, and explanation burden are significant. |
| [tests/](/opt/ai-stack/assistant-training/tests/) | Moderate | Useful, but still adds upkeep and explanation surface. |
| [pyproject.toml](/opt/ai-stack/assistant-training/pyproject.toml) | Low | Small and mostly stable. |
| [repo_paths.py](/opt/ai-stack/assistant-training/repo_paths.py) | Low | Small and highly portable. |
| [evals/canonical_eval_manifest_v1.json](/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json) | Moderate | Valuable, but needs care because it references evaluation structure and provenance. |
| [AGENTS.md](/opt/ai-stack/assistant-training/AGENTS.md) | Low | Small and lightweight. |
| [.gitignore](/opt/ai-stack/assistant-training/.gitignore) | Low | Small hygiene file. |
| [docs/process_infrastructure/](/opt/ai-stack/assistant-training/docs/process_infrastructure/) | Low | Small compatibility alias. |
| [docs/lineages/](/opt/ai-stack/assistant-training/docs/lineages/) | Low | Small compatibility alias. |
| [docs/potential_skills/](/opt/ai-stack/assistant-training/docs/potential_skills/) | Low | Small and peripheral. |
| [docs/convergence/](/opt/ai-stack/assistant-training/docs/convergence/) | High | Large, historically dense, and explanation-heavy. |
| [docs/continuity/](/opt/ai-stack/assistant-training/docs/continuity/) | Moderate | Useful context, but still a historical layer to explain. |
| [docs/housekeeping/](/opt/ai-stack/assistant-training/docs/housekeeping/) | High | Large internal process/archive layer. |
| [docs/history/](/opt/ai-stack/assistant-training/docs/history/) | Moderate | Historical/deprecated material still requires context and maintenance. |
| Transitional/historical root docs | Moderate | Useful context, but not worth carrying into the lean public package by default. |
| [configs/](/opt/ai-stack/assistant-training/configs/) | High | Stage-specific, path-heavy, and likely to require ongoing cleanup if public. |
| [evals/data/](/opt/ai-stack/assistant-training/evals/data/) | High | Mixed provenance and corpus explanation burden. |
| [evals/runs/](/opt/ai-stack/assistant-training/evals/runs/) | High | Large generated output surface. |
| [data/](/opt/ai-stack/assistant-training/data/) | High | Mixed provenance, path cleanup, and explanation burden. |
| [reports/](/opt/ai-stack/assistant-training/reports/) | High | Generated artifacts and derived summaries are noisy to publish. |
| [manifests/runs/](/opt/ai-stack/assistant-training/manifests/runs/) | High | Operational records are path-heavy and maintenance-heavy. |
| [manifests/reports/](/opt/ai-stack/assistant-training/manifests/reports/) | High | Derived archive with high review burden. |
| [manifests/environment/](/opt/ai-stack/assistant-training/manifests/environment/) | High | Machine-specific snapshots and provenance burden. |
| [artifacts/](/opt/ai-stack/assistant-training/artifacts/) | High | Dense generated artifacts and run outputs. |
| [local_review_bundles/](/opt/ai-stack/assistant-training/local_review_bundles/) | High | Archive bundles are heavy and not needed in the public surface. |

## 6. Historical Significance Matrix

| Asset family | Historical significance | Why |
|---|---|---|
| [README.md](/opt/ai-stack/assistant-training/README.md) | Essential history | The public record of what the repository is. |
| Root doctrine docs | Essential history | They record the project’s governing doctrine and the current authoritative framing. |
| [docs/current/](/opt/ai-stack/assistant-training/docs/current/) | Essential history | The current-state record and the project’s present boundary conditions. |
| [docs/framework/](/opt/ai-stack/assistant-training/docs/framework/) | Essential history | The curated methodology history and lineage record. |
| [scripts/](/opt/ai-stack/assistant-training/scripts/) | Essential history | The executable record of the regimen. |
| [tests/](/opt/ai-stack/assistant-training/tests/) | Essential history | The verification record for the regimen. |
| [pyproject.toml](/opt/ai-stack/assistant-training/pyproject.toml) | Essential history | The live configuration record for the project’s execution model. |
| [repo_paths.py](/opt/ai-stack/assistant-training/repo_paths.py) | Essential history | A small but important portability record. |
| [evals/canonical_eval_manifest_v1.json](/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json) | Essential history | The canonical public evaluation record. |
| [AGENTS.md](/opt/ai-stack/assistant-training/AGENTS.md) | Useful history | A small process record, but not a core archive layer. |
| [.gitignore](/opt/ai-stack/assistant-training/.gitignore) | Useful history | Hygiene metadata with little archival weight, but still part of the repository’s operational record. |
| [docs/process_infrastructure/](/opt/ai-stack/assistant-training/docs/process_infrastructure/) | Low-value history | Compatibility pointer only; useful for old links, not a history layer worth preserving publicly by default. |
| [docs/lineages/](/opt/ai-stack/assistant-training/docs/lineages/) | Low-value history | Compatibility alias only. |
| [docs/potential_skills/](/opt/ai-stack/assistant-training/docs/potential_skills/) | Low-value history | Small supplemental note, not a meaningful archive layer. |
| [docs/convergence/](/opt/ai-stack/assistant-training/docs/convergence/) | Useful history | It records important methodological transitions, closures, and retrospective decisions. |
| [docs/continuity/](/opt/ai-stack/assistant-training/docs/continuity/) | Useful history | It preserves continuity context for the project’s evolution. |
| [docs/housekeeping/](/opt/ai-stack/assistant-training/docs/housekeeping/) | Generated history | Mostly generated review/preservation/process artifacts. |
| [docs/history/](/opt/ai-stack/assistant-training/docs/history/) | Low-value history | Deprecated content is mainly historical residue. |
| Transitional/historical root docs | Useful history | They capture internal genesis, migration, and index material that is helpful privately but not necessary publicly. |
| [configs/](/opt/ai-stack/assistant-training/configs/) | Generated history | Operational configuration artifacts from specific stages and runs. |
| [evals/data/](/opt/ai-stack/assistant-training/evals/data/) | Generated history | Generated/curated corpora with provenance complexity. |
| [evals/runs/](/opt/ai-stack/assistant-training/evals/runs/) | Generated history | Generated evaluation run history. |
| [data/](/opt/ai-stack/assistant-training/data/) | Generated history | Mixed-provenance dataset history and derived splits. |
| [reports/](/opt/ai-stack/assistant-training/reports/) | Generated history | Derived reporting artifacts. |
| [manifests/runs/](/opt/ai-stack/assistant-training/manifests/runs/) | Generated history | Operational run logs/manifests. |
| [manifests/reports/](/opt/ai-stack/assistant-training/manifests/reports/) | Generated history | Derived report archive. |
| [manifests/environment/](/opt/ai-stack/assistant-training/manifests/environment/) | Generated history | Environment snapshots and freeze records. |
| [artifacts/](/opt/ai-stack/assistant-training/artifacts/) | Generated history | Run artifacts and output records. |
| [local_review_bundles/](/opt/ai-stack/assistant-training/local_review_bundles/) | Generated history | Bundled preservation material, useful privately but not a public history layer. |

## 7. Public Core Recommendation

Include these in the curated repository by default:
- [README.md](/opt/ai-stack/assistant-training/README.md)
- Root doctrine docs: [docs/goal_charter_v5a.md](/opt/ai-stack/assistant-training/docs/goal_charter_v5a.md), [docs/appendix_a_operational_execution_contract_v3a.md](/opt/ai-stack/assistant-training/docs/appendix_a_operational_execution_contract_v3a.md), [docs/metric_specification_v1a.md](/opt/ai-stack/assistant-training/docs/metric_specification_v1a.md), [docs/evaluation_manifest_v1.md](/opt/ai-stack/assistant-training/docs/evaluation_manifest_v1.md), [docs/repo_layout.md](/opt/ai-stack/assistant-training/docs/repo_layout.md)
- [docs/current/](/opt/ai-stack/assistant-training/docs/current/)
- [docs/framework/](/opt/ai-stack/assistant-training/docs/framework/)
- [scripts/](/opt/ai-stack/assistant-training/scripts/)
- [tests/](/opt/ai-stack/assistant-training/tests/)
- [pyproject.toml](/opt/ai-stack/assistant-training/pyproject.toml)
- [repo_paths.py](/opt/ai-stack/assistant-training/repo_paths.py)
- [evals/canonical_eval_manifest_v1.json](/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json)

## 8. Public Supporting Recommendation

Recommend these as public supporting files if the goal is a slightly richer but still clean curated repo:
- [AGENTS.md](/opt/ai-stack/assistant-training/AGENTS.md)
- [.gitignore](/opt/ai-stack/assistant-training/.gitignore)
- [docs/process_infrastructure/](/opt/ai-stack/assistant-training/docs/process_infrastructure/) as a compatibility alias if link preservation is valued
- [docs/lineages/](/opt/ai-stack/assistant-training/docs/lineages/) as a compatibility alias if link preservation is valued
- [docs/potential_skills/](/opt/ai-stack/assistant-training/docs/potential_skills/) if a small supplemental note is desired

## 9. Canonical-Only Recommendation

Keep these only in `assistant-training-private`:
- [docs/convergence/](/opt/ai-stack/assistant-training/docs/convergence/)
- [docs/continuity/](/opt/ai-stack/assistant-training/docs/continuity/)
- [docs/housekeeping/](/opt/ai-stack/assistant-training/docs/housekeeping/)
- [docs/history/](/opt/ai-stack/assistant-training/docs/history/)
- Transitional/historical root docs: [docs/migration_checklist.md](/opt/ai-stack/assistant-training/docs/migration_checklist.md), [docs/assistant_training_goal_documents_and_artifacts_index.md](/opt/ai-stack/assistant-training/docs/assistant_training_goal_documents_and_artifacts_index.md), [docs/assistant_training_initial_ChatGPT_thread_summary.md](/opt/ai-stack/assistant-training/docs/assistant_training_initial_ChatGPT_thread_summary.md), [docs/repository_establishment_plan_v1.md](/opt/ai-stack/assistant-training/docs/repository_establishment_plan_v1.md)
- [configs/](/opt/ai-stack/assistant-training/configs/)
- [evals/data/](/opt/ai-stack/assistant-training/evals/data/)
- [evals/runs/](/opt/ai-stack/assistant-training/evals/runs/)
- [data/](/opt/ai-stack/assistant-training/data/)
- [reports/](/opt/ai-stack/assistant-training/reports/)
- [manifests/runs/](/opt/ai-stack/assistant-training/manifests/runs/)
- [manifests/reports/](/opt/ai-stack/assistant-training/manifests/reports/)
- [manifests/environment/](/opt/ai-stack/assistant-training/manifests/environment/)
- [artifacts/](/opt/ai-stack/assistant-training/artifacts/)
- [local_review_bundles/](/opt/ai-stack/assistant-training/local_review_bundles/)

## 10. Candidate Curated Repository Layout

```text
assistant-training/
├── README.md
├── AGENTS.md
├── .gitignore
├── pyproject.toml
├── repo_paths.py
├── docs/
│   ├── goal_charter_v5a.md
│   ├── appendix_a_operational_execution_contract_v3a.md
│   ├── metric_specification_v1a.md
│   ├── evaluation_manifest_v1.md
│   ├── repo_layout.md
│   ├── current/
│   ├── framework/
│   ├── potential_skills/                (optional)
│   ├── process_infrastructure/          (optional alias)
│   └── lineages/                        (optional alias)
├── evals/
│   └── canonical_eval_manifest_v1.json
├── scripts/
└── tests/
```

Not part of the default curated repo:
- [docs/convergence/](/opt/ai-stack/assistant-training/docs/convergence/)
- [docs/continuity/](/opt/ai-stack/assistant-training/docs/continuity/)
- [docs/housekeeping/](/opt/ai-stack/assistant-training/docs/housekeeping/)
- [docs/history/](/opt/ai-stack/assistant-training/docs/history/)
- [docs/migration_checklist.md](/opt/ai-stack/assistant-training/docs/migration_checklist.md)
- [docs/assistant_training_goal_documents_and_artifacts_index.md](/opt/ai-stack/assistant-training/docs/assistant_training_goal_documents_and_artifacts_index.md)
- [docs/assistant_training_initial_ChatGPT_thread_summary.md](/opt/ai-stack/assistant-training/docs/assistant_training_initial_ChatGPT_thread_summary.md)
- [docs/repository_establishment_plan_v1.md](/opt/ai-stack/assistant-training/docs/repository_establishment_plan_v1.md)
- [configs/](/opt/ai-stack/assistant-training/configs/)
- [evals/data/](/opt/ai-stack/assistant-training/evals/data/)
- [evals/runs/](/opt/ai-stack/assistant-training/evals/runs/)
- [data/](/opt/ai-stack/assistant-training/data/)
- [reports/](/opt/ai-stack/assistant-training/reports/)
- [manifests/runs/](/opt/ai-stack/assistant-training/manifests/runs/)
- [manifests/reports/](/opt/ai-stack/assistant-training/manifests/reports/)
- [manifests/environment/](/opt/ai-stack/assistant-training/manifests/environment/)
- [artifacts/](/opt/ai-stack/assistant-training/artifacts/)
- [local_review_bundles/](/opt/ai-stack/assistant-training/local_review_bundles/)

## 11. Open Questions

- Should the curated repo keep the compatibility alias trees (`docs/process_infrastructure/` and `docs/lineages/`), or should it standardize entirely on the canonical paths under `docs/framework/`?
- Should `AGENTS.md` stay in the public repo, or remain private-only since the curated repo is not intended to be community-developed?
- Should `docs/potential_skills/` travel to the curated repo, or is it too peripheral to justify inclusion?
- Should the canonical eval manifest be the only file under `evals/` in the public repo, or should the public repo also carry a tiny evaluation README later if that becomes necessary?
- Should `docs/framework/lineages/` be treated as the only public historical layer, with the larger archive families remaining private-only?

## 12. Final Recommendation

The curated/public repository should be a lean, inspectable public interface to the regimen, not a mirror of the private canonical repository. Keep the public core centered on the front door, current-state guidance, doctrine, framework, scripts, tests, and the canonical evaluation manifest. Treat the archive-heavy history, data-bearing surfaces, generated reports, manifests, artifacts, and review bundles as canonical-only. Optional compatibility aliases are acceptable, but they should remain optional rather than driving the curated repository design.
