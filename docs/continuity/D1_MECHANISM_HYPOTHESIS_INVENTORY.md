# D1 Mechanism-Hypothesis Inventory

Date: 2026-06-16

## Status

- Governance-compliant.
- Read-only analysis only.
- No experimental design.
- No arm design.
- No execution planning.
- No training authorization.
- No preregistration creation.
- D0 blocker `D0-BLK-TRAINING-SCRIPT-PROVENANCE-001` remains active and unchanged.
- H1 and H2 remain observational reference regimes, not replay targets.
- This is an initial catalog of candidate explanations, not evidence that any explanation is correct.
- Evidence is typed by role. Only `behavioral_evidence` is direct support for a behavior claim; the other roles are boundary, provenance, contract, or continuity context and must not be treated as direct behavioral support.
- Confounds are recorded as structured records with shared IDs where applicable.

## Inventory Overview

Inventory size: 14 hypotheses.

Relationship clusters:

- Parent/child: `D1-HYP-001` -> `D1-HYP-002`, `D1-HYP-003`
- Composite/component: `D1-HYP-004` -> `D1-HYP-005` through `D1-HYP-010`
- Competing: `D1-HYP-011` <-> `D1-HYP-012`
- Duplicate: `D1-HYP-013` -> `D1-HYP-002`
- Derivative: `D1-HYP-014` -> `D1-HYP-003`

## Inventory Entries

### D1-HYP-001

- `label`: Outer-envelope instruction family
- `classification`: mechanistic_candidate
- `confidence_level`: moderate
- `relationship_type`: parent_of
- `related_hypothesis_ids`: `D1-HYP-002`, `D1-HYP-003`
- `candidate_explanation`: A broader outer-envelope instruction family helps explain why H1/H2-class behavior concentrates around exact tool-call realization rather than remaining at the frozen baseline floor.
- `observed_pattern`: H1 and H2 show materially stronger exact JSON, tool-name, and argument accuracy than the canonical baselines, while the preserved continuity notes repeatedly describe envelope-pressure and cue-regime differences.
- `evidence_refs`:
  - `behavioral_evidence`:
    - `docs/current/baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md`
    - `docs/current/status/TRAINING_RUN_HISTORY.md`
  - `continuity_context_evidence`:
    - `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
  - `governance_boundary_evidence`:
    - `docs/continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md`
- `comparison_class`: current-tree stabilized implementation surfaces compared against H1/H2 observational reference regimes under the frozen canonical evaluation contract
- `control_class`: `i3` / `H0` control scaffold plus frozen evaluation contract
- `fixed_surfaces`: current stabilized trainer surface; current stabilized dataset-builder surface; current stabilized evaluation surface; `i3` control scaffold; `H0` control comparator; H1/H2 reference surfaces; canonical eval manifest; decode defaults; scorer / evaluator path
- `confounds`:
  - `confound_id`: `CFN-001`
    `description`: Envelope pressure, cue phrasing, strict-JSON wording, and duplicate or derivative rephrasings are tightly coupled and can collapse into one causal surface.
    `affected_hypothesis_ids`: `D1-HYP-001`, `D1-HYP-002`, `D1-HYP-003`, `D1-HYP-007`, `D1-HYP-008`, `D1-HYP-013`, `D1-HYP-014`
    `evidence_ref`: `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
    `direction_of_bias`: Can inflate apparent separation between envelope, cue, and duplicate or derivative variants.
    `impact_scope`: Envelope-family hypotheses and their duplicate or derivative cross-references.
    `resolution_status`: unresolved
    `residual_risk`: moderate
    `notes`: Shared envelope/cue family confound; reuse this ID for lexical variants instead of inventing new causal categories.
  - `confound_id`: `CFN-002`
    `description`: Several preserved H1/H2 surface changes co-vary, so apparent gains may reflect a conjunctive bundle rather than any single factor.
    `affected_hypothesis_ids`: `D1-HYP-001`, `D1-HYP-004`
    `evidence_ref`: `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
    `direction_of_bias`: Can overstate the specificity of parent and composite explanations.
    `impact_scope`: Parent and composite umbrella entries.
    `resolution_status`: unresolved
    `residual_risk`: moderate
    `notes`: Shared co-variation confound across the broad umbrella entries.
- `status`: candidate
- `notes`: Broad parent family only; the child entries carry the more specific explanations.

### D1-HYP-002

- `label`: Explicit `tool_calls` envelope pressure
- `classification`: mechanistic_candidate
- `confidence_level`: moderate
- `relationship_type`: child_of
- `related_hypothesis_ids`: `D1-HYP-001`
- `candidate_explanation`: Explicit pressure toward `tool_calls` envelopes is a plausible contributor to exact JSON realization in H1/H2-class behavior.
- `observed_pattern`: The preservation note identifies exact `tool_calls` envelope pressure as one of the smallest plausible causal factors behind the H1/H2 regime.
- `evidence_refs`:
  - `behavioral_evidence`:
    - `docs/current/baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md`
    - `docs/current/status/TRAINING_RUN_HISTORY.md`
    - `evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/summary.json`
    - `evals/runs/stage_b_v1_phase_i_h2_commitment_patch_eval_20260611T120228Z/summary.json`
  - `continuity_context_evidence`:
    - `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
  - `governance_boundary_evidence`:
    - `docs/continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md`
- `comparison_class`: current-tree stabilized implementation surfaces compared against H1/H2 observational reference regimes under the frozen canonical evaluation contract
- `control_class`: `i3` / `H0` control scaffold plus frozen evaluation contract
- `fixed_surfaces`: current stabilized trainer surface; current stabilized dataset-builder surface; current stabilized evaluation surface; `i3` control scaffold; `H0` control comparator; H1/H2 reference surfaces; canonical eval manifest; decode defaults; scorer / evaluator path
- `confounds`:
  - `confound_id`: `CFN-001`
    `description`: Envelope pressure, cue phrasing, strict-JSON wording, and duplicate or derivative rephrasings are tightly coupled and can collapse into one causal surface.
    `affected_hypothesis_ids`: `D1-HYP-001`, `D1-HYP-002`, `D1-HYP-003`, `D1-HYP-007`, `D1-HYP-008`, `D1-HYP-013`, `D1-HYP-014`
    `evidence_ref`: `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
    `direction_of_bias`: Can inflate apparent separation between envelope, cue, and duplicate or derivative variants.
    `impact_scope`: Envelope-family hypotheses and their duplicate or derivative cross-references.
    `resolution_status`: unresolved
    `residual_risk`: moderate
    `notes`: Shared envelope/cue family confound; reuse this ID for lexical variants instead of inventing new causal categories.
- `status`: candidate
- `notes`: This entry is the source reference for the duplicate entry below.

### D1-HYP-003

- `label`: Strict-JSON envelope pressure
- `classification`: mechanistic_candidate
- `confidence_level`: low
- `relationship_type`: child_of
- `related_hypothesis_ids`: `D1-HYP-001`
- `candidate_explanation`: A broader strict-JSON or structured-output pressure can plausibly contribute to exact realization even when the strongest `tool_calls` wording is softened.
- `observed_pattern`: The H1/H2 continuity note distinguishes exact `tool_calls` pressure from weaker generic strict-JSON phrasing, suggesting a meaningful gradient in envelope strength.
- `evidence_refs`:
  - `behavioral_evidence`:
    - `docs/current/baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md`
    - `docs/current/status/TRAINING_RUN_HISTORY.md`
  - `continuity_context_evidence`:
    - `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
  - `governance_boundary_evidence`:
    - `docs/continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md`
- `comparison_class`: current-tree stabilized implementation surfaces compared against H1/H2 observational reference regimes under the frozen canonical evaluation contract
- `control_class`: `i3` / `H0` control scaffold plus frozen evaluation contract
- `fixed_surfaces`: current stabilized trainer surface; current stabilized dataset-builder surface; current stabilized evaluation surface; `i3` control scaffold; `H0` control comparator; H1/H2 reference surfaces; canonical eval manifest; decode defaults; scorer / evaluator path
- `confounds`:
  - `confound_id`: `CFN-001`
    `description`: Envelope pressure, cue phrasing, strict-JSON wording, and duplicate or derivative rephrasings are tightly coupled and can collapse into one causal surface.
    `affected_hypothesis_ids`: `D1-HYP-001`, `D1-HYP-002`, `D1-HYP-003`, `D1-HYP-007`, `D1-HYP-008`, `D1-HYP-013`, `D1-HYP-014`
    `evidence_ref`: `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
    `direction_of_bias`: Can inflate apparent separation between envelope, cue, and duplicate or derivative variants.
    `impact_scope`: Envelope-family hypotheses and their duplicate or derivative cross-references.
    `resolution_status`: unresolved
    `residual_risk`: moderate
    `notes`: Shared envelope/cue family confound; reuse this ID for lexical variants instead of inventing new causal categories.
  - `confound_id`: `CFN-008`
    `description`: Decode defaults, scorer-path consistency, and evaluation-contract alignment can make exact-JSON or measurement effects look stronger or weaker than they are.
    `affected_hypothesis_ids`: `D1-HYP-003`, `D1-HYP-012`, `D1-HYP-014`
    `evidence_ref`: `docs/continuity/D0_HASH_AUTHORITY_VERIFICATION.md`
    `direction_of_bias`: Can collapse a wording or contract effect into a measurement-only story or exaggerate scorer sensitivity.
    `impact_scope`: Strict-JSON and evaluation-contract hypotheses.
    `resolution_status`: unresolved
    `residual_risk`: low
    `notes`: Shared by the strict-JSON source, the evaluation-contract hypothesis, and the derivative reference because all depend on the same decode and scorer surfaces.
- `status`: provisional
- `notes`: This entry is the source reference for the derivative entry below.

### D1-HYP-004

- `label`: Conjunctive H1/H2 realization surface
- `classification`: mechanistic_candidate
- `confidence_level`: moderate
- `relationship_type`: composite_of
- `related_hypothesis_ids`: `D1-HYP-005`, `D1-HYP-006`, `D1-HYP-007`, `D1-HYP-008`, `D1-HYP-009`, `D1-HYP-010`
- `candidate_explanation`: H1/H2-class exact realization is best understood as a conjunctive surface in which several preserved factors jointly matter rather than any single factor operating alone.
- `observed_pattern`: The published continuity material consistently describes H1/H2 as a preserved high-capability regime formed from a specific combination of scaffold, replacement, cue, budget, and boundary conditions.
- `evidence_refs`:
  - `behavioral_evidence`:
    - `docs/current/baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md`
    - `docs/current/status/TRAINING_RUN_HISTORY.md`
    - `evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/summary.json`
    - `evals/runs/stage_b_v1_phase_i_h2_commitment_patch_eval_20260611T120228Z/summary.json`
  - `continuity_context_evidence`:
    - `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
  - `governance_boundary_evidence`:
    - `docs/continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md`
- `comparison_class`: current-tree stabilized implementation surfaces compared against H1/H2 observational reference regimes under the frozen canonical evaluation contract
- `control_class`: `i3` / `H0` control scaffold plus frozen evaluation contract
- `fixed_surfaces`: current stabilized trainer surface; current stabilized dataset-builder surface; current stabilized evaluation surface; `i3` control scaffold; `H0` control comparator; H1/H2 reference surfaces; canonical eval manifest; decode defaults; scorer / evaluator path
- `confounds`:
  - `confound_id`: `CFN-002`
    `description`: Several preserved H1/H2 surface changes co-vary, so apparent gains may reflect a conjunctive bundle rather than any single factor.
    `affected_hypothesis_ids`: `D1-HYP-001`, `D1-HYP-004`
    `evidence_ref`: `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
    `direction_of_bias`: Can overstate the specificity of parent and composite explanations.
    `impact_scope`: Parent and composite umbrella entries.
    `resolution_status`: unresolved
    `residual_risk`: moderate
    `notes`: Shared co-variation confound across the broad umbrella entries.
- `status`: candidate
- `notes`: Composite umbrella only; the component entries below provide the finer-grained candidate explanations.

### D1-HYP-005

- `label`: Low-delta patch-local replacement
- `classification`: mechanistic_candidate
- `confidence_level`: moderate
- `relationship_type`: component_of
- `related_hypothesis_ids`: `D1-HYP-004`
- `candidate_explanation`: Low-delta, patch-local replacement is a plausible contributor to preserving the H1/H2 signal while changing only a narrow part of the scaffold.
- `observed_pattern`: The H1 and H2 patch summaries record bounded replacement budgets and preserved control rows, matching the continuity note's patch-local framing.
- `evidence_refs`:
  - `behavioral_evidence`:
    - `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json`
    - `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json`
    - `evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/summary.json`
    - `evals/runs/stage_b_v1_phase_i_h2_commitment_patch_eval_20260611T120228Z/summary.json`
  - `continuity_context_evidence`:
    - `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
  - `evaluation_contract_evidence`:
    - `docs/continuity/D0_ACCEPTANCE_CRITERIA.md`
  - `provenance_authority_evidence`:
    - `docs/continuity/D0_IMPLEMENTATION_ARCHITECTURE.md`
- `comparison_class`: current-tree stabilized implementation surfaces compared against H1/H2 observational reference regimes under the frozen canonical evaluation contract
- `control_class`: `i3` / `H0` control scaffold plus frozen evaluation contract
- `fixed_surfaces`: current stabilized trainer surface; current stabilized dataset-builder surface; current stabilized evaluation surface; `i3` control scaffold; `H0` control comparator; H1/H2 reference surfaces; canonical eval manifest; decode defaults; scorer / evaluator path
- `confounds`:
  - `confound_id`: `CFN-003`
    `description`: Low-delta patch-local replacement and replacement density may proxy broader lineage fidelity or capacity rather than a direct mechanism.
    `affected_hypothesis_ids`: `D1-HYP-005`, `D1-HYP-008`
    `evidence_ref`: `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
    `direction_of_bias`: Can make patch-local preservation look causal when it is only a surrogate for broader fidelity or capacity.
    `impact_scope`: Patch-local and replacement-density hypotheses.
    `resolution_status`: unresolved
    `residual_risk`: moderate
    `notes`: Shared patch-budget confound.
- `status`: candidate
- `notes`: None

### D1-HYP-006

- `label`: High anchor concentration
- `classification`: mechanistic_candidate
- `confidence_level`: low
- `relationship_type`: component_of
- `related_hypothesis_ids`: `D1-HYP-004`
- `candidate_explanation`: H1/H2-class behavior may require a high concentration of anchor rows or anchor-like examples to stabilize exact realization.
- `observed_pattern`: The continuity note names anchor concentration as a plausible factor, while the H1 and H2 eval summaries expose anchor-related exact-share signals; the support remains indirect.
- `evidence_refs`:
  - `behavioral_evidence`:
    - `evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/summary.json`
    - `evals/runs/stage_b_v1_phase_i_h2_commitment_patch_eval_20260611T120228Z/summary.json`
  - `continuity_context_evidence`:
    - `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
  - `governance_boundary_evidence`:
    - `docs/continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md`
- `comparison_class`: current-tree stabilized implementation surfaces compared against H1/H2 observational reference regimes under the frozen canonical evaluation contract
- `control_class`: `i3` / `H0` control scaffold plus frozen evaluation contract
- `fixed_surfaces`: current stabilized trainer surface; current stabilized dataset-builder surface; current stabilized evaluation surface; `i3` control scaffold; `H0` control comparator; H1/H2 reference surfaces; canonical eval manifest; decode defaults; scorer / evaluator path
- `confounds`:
  - `confound_id`: `CFN-004`
    `description`: Anchor concentration may proxy cue strength or patch budget and may co-occur with other improvements.
    `affected_hypothesis_ids`: `D1-HYP-006`, `D1-HYP-008`
    `evidence_ref`: `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
    `direction_of_bias`: Can overstate anchor causality by collapsing it into a broader surface-strength effect.
    `impact_scope`: Anchor and patch-budget hypotheses.
    `resolution_status`: unresolved
    `residual_risk`: moderate
    `notes`: Shared between anchor and budget hypotheses.
- `status`: provisional
- `notes`: None

### D1-HYP-007

- `label`: Narrow exact-tool-request cue regime
- `classification`: mechanistic_candidate
- `confidence_level`: low
- `relationship_type`: component_of
- `related_hypothesis_ids`: `D1-HYP-004`
- `candidate_explanation`: A narrow cue regime focused on exact tool requests can plausibly support exact JSON realization more strongly than a looser cue regime.
- `observed_pattern`: The continuity note treats cue phrasing as a distinct factor and contrasts strong exact-tool-request cues with weaker generic wording, while the baseline comparison shows the exact-JSON lift the cue regime is meant to explain.
- `evidence_refs`:
  - `behavioral_evidence`:
    - `docs/current/baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md`
    - `docs/current/status/TRAINING_RUN_HISTORY.md`
  - `continuity_context_evidence`:
    - `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
  - `governance_boundary_evidence`:
    - `docs/continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md`
- `comparison_class`: current-tree stabilized implementation surfaces compared against H1/H2 observational reference regimes under the frozen canonical evaluation contract
- `control_class`: `i3` / `H0` control scaffold plus frozen evaluation contract
- `fixed_surfaces`: current stabilized trainer surface; current stabilized dataset-builder surface; current stabilized evaluation surface; `i3` control scaffold; `H0` control comparator; H1/H2 reference surfaces; canonical eval manifest; decode defaults; scorer / evaluator path
- `confounds`:
  - `confound_id`: `CFN-001`
    `description`: Envelope pressure, cue phrasing, strict-JSON wording, and duplicate or derivative rephrasings are tightly coupled and can collapse into one causal surface.
    `affected_hypothesis_ids`: `D1-HYP-001`, `D1-HYP-002`, `D1-HYP-003`, `D1-HYP-007`, `D1-HYP-008`, `D1-HYP-013`, `D1-HYP-014`
    `evidence_ref`: `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
    `direction_of_bias`: Can inflate apparent separation between envelope, cue, and duplicate or derivative variants.
    `impact_scope`: Envelope-family hypotheses and their duplicate or derivative cross-references.
    `resolution_status`: unresolved
    `residual_risk`: moderate
    `notes`: Shared envelope/cue family confound; reuse this ID for lexical variants instead of inventing new causal categories.
- `status`: provisional
- `notes`: None

### D1-HYP-008

- `label`: Patch budget / replacement density
- `classification`: mechanistic_candidate
- `confidence_level`: moderate
- `relationship_type`: component_of
- `related_hypothesis_ids`: `D1-HYP-004`
- `candidate_explanation`: The number and density of replacement rows may contribute to the H1/H2 regime by setting the amount of preserved surface available to carry the signal.
- `observed_pattern`: The H1 and H2 patch summaries record a fixed `100`-row replacement budget, and the continuity note treats patch budget as a distinct factor.
- `evidence_refs`:
  - `behavioral_evidence`:
    - `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json`
    - `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json`
    - `evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/summary.json`
    - `evals/runs/stage_b_v1_phase_i_h2_commitment_patch_eval_20260611T120228Z/summary.json`
  - `continuity_context_evidence`:
    - `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
  - `evaluation_contract_evidence`:
    - `docs/continuity/D0_ACCEPTANCE_CRITERIA.md`
- `comparison_class`: current-tree stabilized implementation surfaces compared against H1/H2 observational reference regimes under the frozen canonical evaluation contract
- `control_class`: `i3` / `H0` control scaffold plus frozen evaluation contract
- `fixed_surfaces`: current stabilized trainer surface; current stabilized dataset-builder surface; current stabilized evaluation surface; `i3` control scaffold; `H0` control comparator; H1/H2 reference surfaces; canonical eval manifest; decode defaults; scorer / evaluator path
- `confounds`:
  - `confound_id`: `CFN-001`
    `description`: Envelope pressure, cue phrasing, strict-JSON wording, and duplicate or derivative rephrasings are tightly coupled and can collapse into one causal surface.
    `affected_hypothesis_ids`: `D1-HYP-001`, `D1-HYP-002`, `D1-HYP-003`, `D1-HYP-007`, `D1-HYP-008`, `D1-HYP-013`, `D1-HYP-014`
    `evidence_ref`: `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
    `direction_of_bias`: Can inflate apparent separation between envelope, cue, and duplicate or derivative variants.
    `impact_scope`: Envelope-family hypotheses and their duplicate or derivative cross-references.
    `resolution_status`: unresolved
    `residual_risk`: moderate
    `notes`: Shared envelope/cue family confound; reuse this ID for lexical variants instead of inventing new causal categories.
  - `confound_id`: `CFN-003`
    `description`: Low-delta patch-local replacement and replacement density may proxy broader lineage fidelity or capacity rather than a direct mechanism.
    `affected_hypothesis_ids`: `D1-HYP-005`, `D1-HYP-008`
    `evidence_ref`: `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
    `direction_of_bias`: Can make patch-local preservation look causal when it is only a surrogate for broader fidelity or capacity.
    `impact_scope`: Patch-local and replacement-density hypotheses.
    `resolution_status`: unresolved
    `residual_risk`: moderate
    `notes`: Shared patch-budget confound.
  - `confound_id`: `CFN-004`
    `description`: Anchor concentration may proxy cue strength or patch budget and may co-occur with other improvements.
    `affected_hypothesis_ids`: `D1-HYP-006`, `D1-HYP-008`
    `evidence_ref`: `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
    `direction_of_bias`: Can overstate anchor causality by collapsing it into a broader surface-strength effect.
    `impact_scope`: Anchor and patch-budget hypotheses.
    `resolution_status`: unresolved
    `residual_risk`: moderate
    `notes`: Shared between anchor and budget hypotheses.
- `status`: candidate
- `notes`: None

### D1-HYP-009

- `label`: Non-tool / no-call balance preservation
- `classification`: control_or_null
- `confidence_level`: low
- `relationship_type`: component_of
- `related_hypothesis_ids`: `D1-HYP-004`
- `candidate_explanation`: Preserving the non-tool and no-call balance may be necessary for H1/H2-class behavior without itself being the positive mechanism that drives exact realization.
- `observed_pattern`: The published baselines and H-series eval summaries show intact no-call behavior at the floor and partial preservation in the higher-capability regimes.
- `evidence_refs`:
  - `behavioral_evidence`:
    - `docs/current/baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md`
    - `docs/current/status/TRAINING_RUN_HISTORY.md`
    - `evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/summary.json`
    - `evals/runs/stage_b_v1_phase_i_h2_commitment_patch_eval_20260611T120228Z/summary.json`
  - `continuity_context_evidence`:
    - `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
- `comparison_class`: current-tree stabilized implementation surfaces compared against H1/H2 observational reference regimes under the frozen canonical evaluation contract
- `control_class`: `i3` / `H0` control scaffold plus frozen evaluation contract
- `fixed_surfaces`: current stabilized trainer surface; current stabilized dataset-builder surface; current stabilized evaluation surface; `i3` control scaffold; `H0` control comparator; H1/H2 reference surfaces; canonical eval manifest; decode defaults; scorer / evaluator path
- `confounds`:
  - `confound_id`: `CFN-005`
    `description`: No-call preservation may be a boundary condition or effect of other factors, and metric coupling can make it look explanatory when it is only preserving the floor.
    `affected_hypothesis_ids`: `D1-HYP-009`
    `evidence_ref`: `docs/current/baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md`
    `direction_of_bias`: Can overstate the null-style explanatory role of no-call balance.
    `impact_scope`: No-call balance hypothesis.
    `resolution_status`: unresolved
    `residual_risk`: low
    `notes`: Boundary-condition confound only.
- `status`: provisional
- `notes`: Descriptive boundary-condition candidate only.

### D1-HYP-010

- `label`: Current-tree scaffold fidelity / preserved baseline alignment
- `classification`: confounded_candidate
- `confidence_level`: low
- `relationship_type`: component_of
- `related_hypothesis_ids`: `D1-HYP-004`
- `candidate_explanation`: The preserved current-tree scaffold and baseline alignment may explain part of the H1/H2 regime by keeping the comparison surface stable enough for the signal to appear.
- `observed_pattern`: The D1 foundation and current-tree transition docs identify the preserved current-tree scaffold and baseline alignment as comparison infrastructure rather than mechanism evidence.
- `evidence_refs`:
  - `provenance_authority_evidence`:
    - `docs/continuity/D0_IMPLEMENTATION_ARCHITECTURE.md`
    - `docs/continuity/D0_HASH_AUTHORITY_VERIFICATION.md`
  - `evaluation_contract_evidence`:
    - `docs/continuity/D0_ACCEPTANCE_CRITERIA.md`
    - `docs/continuity/D0_HASH_AUTHORITY_VERIFICATION.md`
  - `continuity_context_evidence`:
    - `docs/current/framework_vs_history.md`
    - `docs/continuity/D0_TO_CURRENT_TREE_MECHANISM_ISOLATION_GOVERNANCE.md`
  - `governance_boundary_evidence`:
    - `docs/continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md`
- `comparison_class`: current-tree stabilized implementation surfaces compared against H1/H2 observational reference regimes under the frozen canonical evaluation contract
- `control_class`: `i3` / `H0` control scaffold plus frozen evaluation contract
- `fixed_surfaces`: current stabilized trainer surface; current stabilized dataset-builder surface; current stabilized evaluation surface; `i3` control scaffold; `H0` control comparator; H1/H2 reference surfaces; canonical eval manifest; decode defaults; scorer / evaluator path
- `confounds`:
  - `confound_id`: `CFN-006`
    `description`: Preserved current-tree scaffold fidelity and baseline alignment are comparison infrastructure and may be prerequisites rather than causal drivers.
    `affected_hypothesis_ids`: `D1-HYP-010`
    `evidence_ref`: `docs/continuity/D0_TO_CURRENT_TREE_MECHANISM_ISOLATION_GOVERNANCE.md`
    `direction_of_bias`: Can collapse the hypothesis into a boundary condition instead of a positive mechanism.
    `impact_scope`: Scaffold fidelity hypothesis.
    `resolution_status`: unresolved
    `residual_risk`: low
    `notes`: Boundary-condition confound only.
- `status`: confounded
- `notes`: Boundary-condition candidate only.

### D1-HYP-011

- `label`: Contamination-bound preservation as explanatory core
- `classification`: confounded_candidate
- `confidence_level`: low
- `relationship_type`: competing_with
- `related_hypothesis_ids`: `D1-HYP-012`
- `candidate_explanation`: H1/H2-class behavior may be better explained by the preservation of contamination and leakage boundaries than by a distinct positive mechanism.
- `observed_pattern`: The D0 and D1 continuity material treats contamination, leakage, and boundary discipline as blocking concerns and emphasizes their preservation across the curated surfaces.
- `evidence_refs`:
  - `governance_boundary_evidence`:
    - `docs/continuity/D0_FAILURE_TAXONOMY.md`
    - `docs/continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md`
  - `evaluation_contract_evidence`:
    - `docs/continuity/D0_ACCEPTANCE_CRITERIA.md`
  - `continuity_context_evidence`:
    - `docs/continuity/D0_TO_CURRENT_TREE_MECHANISM_ISOLATION_GOVERNANCE.md`
- `comparison_class`: current-tree stabilized implementation surfaces compared against H1/H2 observational reference regimes under the frozen canonical evaluation contract
- `control_class`: `i3` / `H0` control scaffold plus frozen evaluation contract
- `fixed_surfaces`: current stabilized trainer surface; current stabilized dataset-builder surface; current stabilized evaluation surface; `i3` control scaffold; `H0` control comparator; H1/H2 reference surfaces; canonical eval manifest; decode defaults; scorer / evaluator path
- `confounds`:
  - `confound_id`: `CFN-007`
    `description`: Contamination and leakage control may be necessary but not sufficient and may explain preservation rather than gain.
    `affected_hypothesis_ids`: `D1-HYP-011`
    `evidence_ref`: `docs/continuity/D0_FAILURE_TAXONOMY.md`
    `direction_of_bias`: Can overstate boundary discipline as a positive mechanism.
    `impact_scope`: Contamination-bound hypothesis.
    `resolution_status`: unresolved
    `residual_risk`: low
    `notes`: Boundary-preservation confound only.
- `status`: confounded
- `notes`: Competing null-style explanation.

### D1-HYP-012

- `label`: Evaluation-contract / decode-default alignment as explanatory core
- `classification`: confounded_candidate
- `confidence_level`: low
- `relationship_type`: competing_with
- `related_hypothesis_ids`: `D1-HYP-011`
- `candidate_explanation`: H1/H2-class behavior may be partly explained by stable evaluation-contract alignment, including decode defaults and scorer-path consistency, rather than by a distinct data-surface mechanism.
- `observed_pattern`: The D0 authority documents and D1 foundation elevate the canonical evaluation manifest, decode defaults, and scorer path as frozen measurement authority.
- `evidence_refs`:
  - `provenance_authority_evidence`:
    - `docs/continuity/D0_HASH_AUTHORITY_VERIFICATION.md`
    - `docs/continuity/D0_IMPLEMENTATION_ARCHITECTURE.md`
  - `evaluation_contract_evidence`:
    - `docs/continuity/D0_ACCEPTANCE_CRITERIA.md`
    - `docs/continuity/D0_HASH_AUTHORITY_VERIFICATION.md`
  - `governance_boundary_evidence`:
    - `docs/continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md`
- `comparison_class`: current-tree stabilized implementation surfaces compared against H1/H2 observational reference regimes under the frozen canonical evaluation contract
- `control_class`: `i3` / `H0` control scaffold plus frozen evaluation contract
- `fixed_surfaces`: current stabilized trainer surface; current stabilized dataset-builder surface; current stabilized evaluation surface; `i3` control scaffold; `H0` control comparator; H1/H2 reference surfaces; canonical eval manifest; decode defaults; scorer / evaluator path
- `confounds`:
  - `confound_id`: `CFN-008`
    `description`: Decode defaults, scorer-path consistency, and evaluation-contract alignment can make exact-JSON or measurement effects look stronger or weaker than they are.
    `affected_hypothesis_ids`: `D1-HYP-003`, `D1-HYP-012`, `D1-HYP-014`
    `evidence_ref`: `docs/continuity/D0_HASH_AUTHORITY_VERIFICATION.md`
    `direction_of_bias`: Can collapse a wording or contract effect into a measurement-only story or exaggerate scorer sensitivity.
    `impact_scope`: Strict-JSON and evaluation-contract hypotheses.
    `resolution_status`: unresolved
    `residual_risk`: low
    `notes`: Shared by the strict-JSON source, the evaluation-contract hypothesis, and the derivative reference because all depend on the same decode and scorer surfaces.
- `status`: confounded
- `notes`: Competing null-style explanation.

### D1-HYP-013

- `label`: Duplicate phrasing of explicit envelope pressure
- `classification`: duplicate_or_derivative
- `confidence_level`: low
- `relationship_type`: duplicate_of
- `related_hypothesis_ids`: `D1-HYP-002`
- `candidate_explanation`: This entry restates the explicit `tool_calls` envelope-pressure hypothesis with alternate wording only.
- `observed_pattern`: The same envelope-pressure pattern is being cataloged under a second label for cross-reference purposes.
- `evidence_refs`:
  - `behavioral_evidence`:
    - `docs/current/baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md`
    - `docs/current/status/TRAINING_RUN_HISTORY.md`
    - `evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/summary.json`
    - `evals/runs/stage_b_v1_phase_i_h2_commitment_patch_eval_20260611T120228Z/summary.json`
  - `continuity_context_evidence`:
    - `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
  - `governance_boundary_evidence`:
    - `docs/continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md`
- `comparison_class`: current-tree stabilized implementation surfaces compared against H1/H2 observational reference regimes under the frozen canonical evaluation contract
- `control_class`: `i3` / `H0` control scaffold plus frozen evaluation contract
- `fixed_surfaces`: current stabilized trainer surface; current stabilized dataset-builder surface; current stabilized evaluation surface; `i3` control scaffold; `H0` control comparator; H1/H2 reference surfaces; canonical eval manifest; decode defaults; scorer / evaluator path
- `confounds`:
  - `confound_id`: `CFN-001`
    `description`: Envelope pressure, cue phrasing, strict-JSON wording, and duplicate or derivative rephrasings are tightly coupled and can collapse into one causal surface.
    `affected_hypothesis_ids`: `D1-HYP-001`, `D1-HYP-002`, `D1-HYP-003`, `D1-HYP-007`, `D1-HYP-008`, `D1-HYP-013`, `D1-HYP-014`
    `evidence_ref`: `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
    `direction_of_bias`: Can inflate apparent separation between envelope, cue, and duplicate or derivative variants.
    `impact_scope`: Envelope-family hypotheses and their duplicate or derivative cross-references.
    `resolution_status`: unresolved
    `residual_risk`: moderate
    `notes`: Shared envelope/cue family confound; reuse this ID for lexical variants instead of inventing new causal categories.
- `status`: duplicate
- `notes`: Cross-reference only; not a separate source of support.

### D1-HYP-014

- `label`: Derivative cue-phrasing hypothesis
- `classification`: duplicate_or_derivative
- `confidence_level`: low
- `relationship_type`: derivative_of
- `related_hypothesis_ids`: `D1-HYP-003`
- `candidate_explanation`: This entry specializes the strict-JSON envelope-pressure hypothesis into a cue-phrasing variant rather than a separate mechanism.
- `observed_pattern`: The catalog is capturing a more specific phrasing of the same cue-pressure idea that appears in the preservation note.
- `evidence_refs`:
  - `behavioral_evidence`:
    - `docs/current/baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md`
    - `docs/current/status/TRAINING_RUN_HISTORY.md`
  - `continuity_context_evidence`:
    - `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
  - `governance_boundary_evidence`:
    - `docs/continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md`
- `comparison_class`: current-tree stabilized implementation surfaces compared against H1/H2 observational reference regimes under the frozen canonical evaluation contract
- `control_class`: `i3` / `H0` control scaffold plus frozen evaluation contract
- `fixed_surfaces`: current stabilized trainer surface; current stabilized dataset-builder surface; current stabilized evaluation surface; `i3` control scaffold; `H0` control comparator; H1/H2 reference surfaces; canonical eval manifest; decode defaults; scorer / evaluator path
- `confounds`:
  - `confound_id`: `CFN-001`
    `description`: Envelope pressure, cue phrasing, strict-JSON wording, and duplicate or derivative rephrasings are tightly coupled and can collapse into one causal surface.
    `affected_hypothesis_ids`: `D1-HYP-001`, `D1-HYP-002`, `D1-HYP-003`, `D1-HYP-007`, `D1-HYP-008`, `D1-HYP-013`, `D1-HYP-014`
    `evidence_ref`: `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
    `direction_of_bias`: Can inflate apparent separation between envelope, cue, and duplicate or derivative variants.
    `impact_scope`: Envelope-family hypotheses and their duplicate or derivative cross-references.
    `resolution_status`: unresolved
    `residual_risk`: moderate
    `notes`: Shared envelope/cue family confound; reuse this ID for lexical variants instead of inventing new causal categories.
  - `confound_id`: `CFN-008`
    `description`: Decode defaults, scorer-path consistency, and evaluation-contract alignment can make exact-JSON or measurement effects look stronger or weaker than they are.
    `affected_hypothesis_ids`: `D1-HYP-003`, `D1-HYP-012`, `D1-HYP-014`
    `evidence_ref`: `docs/continuity/D0_HASH_AUTHORITY_VERIFICATION.md`
    `direction_of_bias`: Can collapse a wording or contract effect into a measurement-only story or exaggerate scorer sensitivity.
    `impact_scope`: Strict-JSON and evaluation-contract hypotheses.
    `resolution_status`: unresolved
    `residual_risk`: low
    `notes`: Shared by the strict-JSON source, the evaluation-contract hypothesis, and the derivative reference because all depend on the same decode and scorer surfaces.
- `status`: provisional
- `notes`: Derivative cross-reference only.
