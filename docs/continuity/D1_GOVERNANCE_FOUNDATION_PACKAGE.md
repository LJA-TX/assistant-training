# D1 Governance Foundation Package

Date: 2026-06-15

## Status

- Stage D0 blocker `D0-BLK-TRAINING-SCRIPT-PROVENANCE-001` remains active.
- Canonical-byte certification remains blocked.
- No manifest edits are authorized.
- No hash-claim edits are authorized.
- No training runs are authorized.
- No experimental arm execution is authorized.
- H1 and H2 are observational reference regimes, not replay targets.
- The current stabilized implementation surfaces are the operative D1 baseline for review, including trainer, dataset-builder, evaluation, and associated current-tree framework components.

This package is governance and methodology only. It defines the review boundary for later current-tree mechanism-isolation design work. It does not authorize execution, training, or experimental design.

## Authority Order

When D1 materials conflict, use the highest-precedence source available and treat lower-precedence material as subordinate context only.

1. D0 continuity and blocker documents
2. Current-tree framework and live implementation surfaces
3. Frozen control and observational reference surfaces
4. Frozen evaluation contract and current status history
5. Future D1 preregistration artifacts, once approved

Lower levels must not override higher levels.

## 1. Authoritative Evidence Surfaces

### 1.1 Governance and boundary surfaces

These surfaces define what D1 is allowed to be.

- `docs/continuity/D0_TO_CURRENT_TREE_MECHANISM_ISOLATION_GOVERNANCE.md`
- `docs/continuity/D0_BLOCKER_REGISTER.md`
- `docs/continuity/D0_DRY_RUN_PROVENANCE_FINDING.md`
- `docs/continuity/D0_PROVENANCE_BLOCKER_RECOMMENDATION.md`
- `docs/continuity/D0_PROVENANCE_BLOCKER_RISK_ASSESSMENT.md`
- `docs/continuity/D0_SITUATION_REVIEW_AND_RECOMMENDATION_2026-06-15.md`
- `docs/current/framework_vs_history.md`
- `docs/current/start_here.md`
- `docs/current/status/TRAINING_RUN_HISTORY.md`

Use these surfaces to preserve the D0 blocker, separate framework from curated history, and prevent D1 from being recast as a canonical-byte certification effort.

### 1.2 Current-tree operational surfaces

These surfaces define the operative current-tree baseline for D1 reasoning.

- `scripts/train_lora_sft.py`
- `scripts/build_dataset_v1.py`
- `scripts/eval_canonical_manifest.py`
- `tests/test_eval_canonical_manifest.py`
- `docs/current/baselines/README.md`
- `docs/current/baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md`

These are authoritative for D1 because D1 is a current-tree question. They are not authority for the blocked D0 canonical-byte claim.

### 1.3 Frozen control scaffold surfaces

These surfaces anchor the control comparator and row-identity baseline.

- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json`
- `configs/lora/stage_b_llama31_8b_base_v1_i3.config.json`
- `manifests/runs/stage_b_llama31_8b_base_v1_i3.run_manifest.json`
- `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.json`
- `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.run_manifest.json`

Use these as frozen control evidence only. They are not to be repurposed as mutable inputs.

### 1.4 Observational reference regime surfaces

These surfaces are the preserved H-series reference regimes.

- `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_val.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json`
- `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_val.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json`
- `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.config.json`
- `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.config.json`
- `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.run_manifest.json`
- `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.run_manifest.json`
- `evals/runs/stage_b_v1_phase_i_h0_control_i3_micro_eval_20260611T103048Z/summary.json`
- `evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/summary.json`
- `evals/runs/stage_b_v1_phase_i_h2_commitment_patch_eval_20260611T120228Z/summary.json`
- `evals/baselines/llama31/internal_reference_regimes/`

Use these only for compare-and-contrast reasoning. They are observational reference regimes, not replay targets and not approval targets for future execution.

### 1.5 Frozen evaluation contract surfaces

These surfaces define the measurement contract that D1 must preserve.

- `evals/canonical_eval_manifest_v1.json`
- `docs/goal_charter_v5a.md`
- `docs/appendix_a_operational_execution_contract_v3a.md`
- `docs/metric_specification_v1a.md`

Use these surfaces as immutable measurement authority unless a separate governance action explicitly changes the contract.

## 2. Frozen Artifacts And Invariants

| Artifact or invariant | D1 status | Required rule |
|---|---|---|
| D0 blocker `D0-BLK-TRAINING-SCRIPT-PROVENANCE-001` | Active | Do not reopen, downgrade, or reinterpret as advisory. |
| Canonical eval manifest and metric contract | Frozen | Do not edit, normalize, or relax. |
| Current stabilized trainer lineage | Authoritative for D1 | Use as the operative current-tree baseline only. |
| `i3` and `H0` control scaffold | Frozen | Preserve as control comparator evidence only. |
| H1 and H2 reference regimes | Frozen observational evidence | Compare only; do not replay or relabel as canonical targets. |
| Current status and run history | Append-only evidence | Cite for context; do not rewrite history. |

Additional invariants:

- No manifest edits.
- No hash-claim edits.
- No dataset mutation.
- No training launch.
- No experimental arm launch.
- No reclassification of H1 or H2 into replay targets.
- No use of current-tree outputs as proof of blocked canonical bytes.

## 3. Admissible Intervention Classes

The following classes are admissible for D1 governance work once the package is approved. They are read-only, review-oriented, or preregistration-oriented only.

| Class | Allowed scope | Boundary |
|---|---|---|
| Evidence inventory | Classify the available current-tree, control, and observational surfaces. | No data or config mutation. |
| Mechanism-hypothesis inventory | List, categorize, and compare candidate mechanism hypotheses in read-only governance form. | No experimental arms, no run planning, no execution. |
| Surface reconciliation | Compare current-tree surfaces against frozen control and observational references. | No inference-based repair. |
| Hypothesis framing | Draft candidate mechanism questions in governance language. | No execution plan, no arm launch. |
| Preregistration drafting | Define the future questions, controls, stopping rules, and acceptance thresholds. | No hidden variables or post-hoc additions. |
| Claim-format design | Specify how a future mechanism claim must be worded and evidenced. | No overclaiming beyond the evidence tier. |
| Boundary review | Test proposed D1 language against D0 blocker and current-tree authority. | No authority overrides. |

If an action changes repository state, launches work, or depends on unapproved execution, it is not admissible under this package.

## 4. Prohibited Intervention Classes

| Class | Why prohibited |
|---|---|
| Training or evaluation execution | This package is governance-only and authorizes no runtime activity. |
| Dataset, config, or manifest mutation | Would alter source evidence and violate the frozen-artifact boundary. |
| Canonical-byte repair or hash-claim rewriting | Would replace provenance with revisionism. |
| Experimental arm design, arm-specific run planning, or execution | These are not authorized under a governance-only package and belong to a later review. |
| H1/H2 replay targeting | H1 and H2 are observational reference regimes, not replay targets. |
| Heuristic completion of missing evidence | Missing provenance must remain missing until resolved by authoritative source. |
| Unpreregistered variable changes | Post-hoc changes destroy attribution integrity. |
| Authority downgrades without higher-order approval | D0 blocker status must remain unchanged. |
| Claiming canonical-byte continuity from current-tree outputs | Current-tree authority is not a substitute for unresolved D0 provenance. |

## 5. Causal Attribution Standards

A mechanism claim is not accepted unless it can be stated at the correct evidentiary tier.

| Claim tier | Permitted wording | Minimum evidence |
|---|---|---|
| Descriptive | `X changed while Y was held fixed.` | Read-only surface comparison and invariant check. |
| Associative | `X is associated with Y under the current-tree baseline.` | Frozen contract, comparison class, and no boundary violation. |
| Mechanistic candidate | `X plausibly contributes to Y.` | Preregistered contrast, negative controls, and an explicit confound list. |
| Accepted mechanism claim | `X is a mechanism for Y under conditions C.` | Reproducible evidence, no unaccounted confound, and formal review acceptance. |

Required standards:

1. Name the exact surface or intervention being attributed.
2. State the comparison class explicitly.
3. State every surface held fixed.
4. Distinguish observation from intervention.
5. Treat H1 and H2 as reference regimes only.
6. Do not infer causality from metric movement alone.
7. Do not infer causality from a single run, a single split, or a single favorable artifact.
8. Do not use unresolved D0 provenance as a substitute for D1 evidence.
9. If the evidence only supports association, the claim must stay at association level.

## 6. Acceptance Criteria For Mechanism Claims

Mechanism claims may be accepted only if all of the following are true:

- The claim was preregistered before any execution or analysis that could influence the result.
- The claim names the current-tree baseline and the frozen reference regime(s) used for comparison.
- The frozen evaluation contract was unchanged throughout the study.
- All declared fixed surfaces remained fixed.
- All declared negative controls remained negative.
- All declared contamination or leakage checks passed.
- The result is reproducible under the preregistered replication rule.
- The result is reported with effect direction, effect size, and uncertainty.
- The claim does not depend on an unapproved execution path or a prohibited intervention class.
- The claim language matches the strength of the evidence, not the ambition of the hypothesis.

If any criterion fails, the result may remain a hypothesis or a provisional observation, but it is not an accepted mechanism claim.

## 7. Experiment Preregistration Requirements

Any future mechanism-isolation study must be preregistered before design implementation begins.

Required preregistration elements:

1. Study name and version.
2. Scientific objective and null hypothesis.
3. Mechanism being tested, stated in operational terms.
4. Current-tree baseline artifacts to be used.
5. Frozen reference regimes to be used.
6. Surfaces held fixed.
7. Variables allowed to vary.
8. Outcome metrics and acceptance thresholds.
9. Negative controls and contamination checks.
10. Stopping rules and failure taxonomy mapping.
11. Analysis plan, including exclusion rules.
12. Replication rule.
13. Required output artifacts.
14. Approval authority and sign-off date.

Preregistration rules:

- No unlisted variable may be introduced after approval.
- No hidden comparison may be added after approval.
- No metric may be changed after approval without a separate authority update.
- No study may begin execution until preregistration is complete and reviewed.

## 8. Failure Taxonomy

### Severity classes

- `fatal`: stop all D1 work immediately and escalate.
- `blocking`: stop the affected claim or design line.
- `advisory`: record and continue, but do not promote the claim without review.

| Code | Trigger | Severity | Stop action |
|---|---|---|---|
| `AUTHORITY_CONFLICT` | D0 and D1 sources disagree on scope or precedence. | fatal | Stop all work and resolve the authority chain. |
| `D0_BLOCKER_REOPENING_ATTEMPT` | Any attempt to weaken, relabel, or bypass `D0-BLK-TRAINING-SCRIPT-PROVENANCE-001`. | fatal | Stop immediately and preserve the original blocker status. |
| `REFERENCE_REGIME_MISLABEL` | H1 or H2 is treated as a replay target or as canonical-byte proof. | fatal | Stop immediately and correct the label. |
| `CONTRACT_DRIFT` | Metric spec, scorer, decode defaults, or split hashes drift without approval. | blocking | Stop the affected claim line. |
| `SURFACE_DRIFT` | A pinned current-tree or reference artifact no longer matches the expected bytes or identity. | blocking | Stop the affected comparison and record the drift. |
| `MISSING_REQUIRED_EVIDENCE` | A required source surface is absent from the review set. | blocking | Stop the affected claim and do not infer the missing evidence. |
| `UNPREREGISTERED_INTERVENTION` | A variable, contrast, or control appears after preregistration. | fatal | Stop the study definition and restart governance review. |
| `CONTAMINATION_OR_LEAKAGE` | A non-target surface changes or downstream output is used as upstream evidence. | fatal | Stop immediately and quarantine the claim. |
| `CAUSAL_ATTRIBUTION_OVERREACH` | Association is stated as mechanism without the required evidence tier. | fatal | Stop the claim and downgrade the wording. |
| `REPLICATION_FAILURE` | The preregistered replication rule is not met. | blocking | Stop promotion of the claim. |
| `UNAUTHORIZED_EXECUTION` | Training, dataset mutation, or experimental arm launch occurs under this package. | fatal | Stop immediately and escalate. |
| `OUTPUT_SCHEMA_DRIFT` | A governed report cannot be emitted in the approved structure. | blocking | Stop the affected review artifact and repair the schema. |

## 9. Escalation Criteria

Escalate and pause D1 review if any of the following occurs:

- The authority order is unclear or internally contradictory.
- A request appears to modify the D0 blocker, the canonical manifest, or any hash claim.
- A proposal moves from governance into execution without separate authorization.
- H1 or H2 is described as a replay target, a reconstruction mandate, or a substitute canonical record.
- A required surface is missing, ambiguous, or contradicted by a higher-precedence source.
- A design change appears after preregistration and would alter the claim space.
- A claimed mechanism requires unresolved provenance to interpret.
- A repository anomaly suggests the evidence spine is incomplete or inconsistent.

Escalation response:

1. Stop the affected line of work.
2. Record the conflicting authority or missing evidence.
3. Preserve the current boundary.
4. Seek higher-order governance review before continuing.

## 10. Recommended D1 Execution Sequence

This sequence is a governance review sequence, not an execution plan.

1. Confirm the D0 blocker remains unchanged.
2. Confirm H1 and H2 remain observational reference regimes only.
3. Confirm the current-tree trainer lineage is the operative D1 baseline.
4. Inventory the authoritative evidence surfaces and classify them by role.
5. Freeze the invariant list for current-tree comparison work.
6. Draft the admissible and prohibited intervention classes.
7. Draft the causal attribution standards and claim tiers.
8. Draft the preregistration requirements and failure taxonomy.
9. Run a boundary review against the D0 authority chain and current status docs.
10. Approve the governance package before any mechanism-isolation design work begins.

## Boundary Confirmation

- No training behavior changed.
- No dataset behavior changed.
- No manifest or hash-claim edits were made.
- No experimental arm was proposed for execution.
- No current-tree or historical surface was mutated.
- No D0 blocker status changed.
- H1 and H2 remain observational reference regimes, not replay targets.

## Deferred Items

The following are intentionally deferred until this governance package is approved and a separate design review is authorized:

- concrete mechanism hypotheses
- arm structure and arm naming
- execution sequencing
- run manifests
- analysis implementation details
