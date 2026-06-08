# PUBLIC_ALPHA_05_ALPHA_ASSEMBLY_VALIDATION

## 1. Executive Summary

The repository is **ready with minor findings** to begin local alpha assembly.

The accepted alpha baseline in `PUBLIC_ALPHA_01` remains intact in scope and intent, and the alpha-preparation remediation reported in `PUBLIC_ALPHA_04` is supported by the current tree state:

- the public front door and current-state surfaces now align with the accepted alpha package;
- the doctrine and manifest surfaces are normalized to repository-relative or logical references;
- the lineage index matches the curated evidence spine;
- the evaluator and targeted tests are decoupled from external runtime fixtures and passed.

Validation evidence reviewed for this package:

- `docs/research/PUBLIC_ALPHA_01_ALPHA_REPOSITORY_ASSEMBLY_MANIFEST.md`
- `docs/research/PUBLIC_ALPHA_02_ALPHA_ASSEMBLY_PREPARATION_ASSESSMENT.md`
- `docs/research/PUBLIC_ALPHA_03_ALPHA_PREPARATION_REMEDIATION_PLAN.md`
- `docs/research/PUBLIC_ALPHA_04_EXECUTION_REPORT.md`
- the modified alpha-preparation surfaces listed in `PUBLIC_ALPHA_04`
- the legacy roadmap record `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md`

Corrective actions taken during this validation pass:

- none.

## 2. Manifest Conformance Review

`PUBLIC_ALPHA_01` still defines the accepted alpha assembly boundary, and the current tree conforms to that boundary at the level that matters for assembly:

- the included alpha-facing surfaces are the same family set the manifest expected;
- the excluded canonical-only families remain excluded from the alpha package;
- the curated historical evidence spine still centers on the accepted, bounded set of lineage and method records;
- the public-core and public-supporting surfaces now read as a coherent curated package rather than a machine-specific working tree.

The main residual issue is not a scope deviation. It is link hygiene inside preserved historical artifacts. Several accepted historical documents still contain absolute links to excluded canonical-only families such as `docs/convergence/`. That is consistent with the decision to preserve those records unchanged, but it remains the primary minor finding to document.

Representative examples:

- `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md`
- `docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md`
- `docs/framework/methodology/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md`

These are preserved historical records, not front-door or runtime surfaces, so the issue is a publication-hygiene residual rather than a manifest violation.

## 3. Remediation Completion Verification

The remediation described in `PUBLIC_ALPHA_02` and `PUBLIC_ALPHA_03` is supported by the current repository state.

Verified outcomes:

- front-door alignment: `README.md`, `docs/current/start_here.md`, `docs/current/current_status.md`, `docs/current/framework_vs_history.md`, and `docs/current/housekeeping_status.md` now point at the accepted alpha package instead of the broader canonical working tree;
- doctrine and manifest normalization: `docs/goal_charter_v5a.md`, `docs/appendix_a_operational_execution_contract_v3a.md`, and `evals/canonical_eval_manifest_v1.json` were normalized to repository-relative or logical references;
- evidence-spine alignment: `docs/framework/lineages/README.md` now presents the bounded curated spine and follow-on context instead of an open-ended lineage archive;
- evaluator/test decoupling: `scripts/stage_c1_evaluator_foundation.py` and the targeted tests now use self-contained or repo-root-relative inputs instead of external runtime checkout assumptions.

Targeted validation results:

- `git diff --cached --check`: PASS
- `git diff --check`: PASS
- trailing-whitespace / final-newline check on `docs/research/PUBLIC_ALPHA_05_ALPHA_ASSEMBLY_VALIDATION.md`: PASS
- `pytest tests/test_dataset_contract.py tests/test_eval_canonical_manifest.py tests/test_eval_adapter_toolcalls.py tests/test_repo_paths.py tests/test_stage_c1_evaluator_foundation.py tests/test_compatibility_path_resolution.py tests/test_masking_behavior.py`: PASS, 40 passed

## 4. Scope-Control Verification

`PUBLIC_ALPHA_04` did not widen the alpha scope.

Observed scope behavior:

- only files already identified by `PUBLIC_ALPHA_02` and `PUBLIC_ALPHA_03` were modified for remediation;
- the preservation report `docs/research/PUBLIC_ALPHA_04_EXECUTION_REPORT.md` was added as documentation of the remediation pass;
- no alpha-assembly step was performed;
- no public-repository population step was performed;
- no new architecture was introduced.

The remaining historical-link residue is confined to preserved historical artifacts and to canonical-only records that are outside the alpha package. That does not constitute an alpha-boundary violation.

## 5. Validation Review

The validation evidence is sufficient for local alpha-assembly readiness.

Why it is sufficient:

- documentation hygiene passed;
- path hygiene passed on the modified alpha-preparation surfaces;
- targeted tests covered the path-sensitive surfaces that had been decoupled;
- the remaining known references to excluded families live in preserved historical artifacts or canonical-only records that the manifest already treats as out of scope for alpha assembly.

The current validation set does not indicate a hidden assembly blocker. It does show one residual publication-hygiene risk: preserved historical records still carry absolute links into excluded canonical-only content. That risk is acceptable for now because those records are intentionally preserved historical evidence rather than active navigation surfaces.

## 6. Readiness Risk Assessment

### High Risks

- None identified.

### Medium Risks

- Preserved historical artifacts still contain absolute links to excluded canonical-only families, especially `docs/convergence/`.
- The legacy roadmap record `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md` retains historical absolute links, but it is not a blocker because it was intentionally left outside the remediation set.

### Low Risks

- Canonical-only lineage notes outside the alpha package still contain historical run-path references, for example `docs/framework/lineages/i10r_microprobe_checkpoint_lineage_note.md`. These do not affect alpha readiness because the file is excluded from the accepted alpha assembly boundary.

## 7. Assembly Readiness Determination

**Ready with minor findings**

Rationale:

- the accepted alpha manifest still matches the current preparation state;
- the remediation boundary was respected;
- the targeted validation suite passed;
- the only remaining issues are preserved historical-link residues, not alpha-scope defects.

## 8. Assembly Preconditions

No blocking preconditions remain before local alpha assembly begins.

The only follow-up worth tracking is optional future normalization of historical links inside preserved evidence records if a later publication pass decides that archival link hygiene should be tightened.

## 9. Recommended Next Boundary

**Alpha Assembly Execution**

The repository is ready to move from preparation validation into the actual local alpha assembly phase.

## 10. Final Recommendation

Proceed with local alpha assembly.

Keep the preserved historical-link residue documented as a known, non-blocking publication-hygiene issue rather than as a readiness blocker.
