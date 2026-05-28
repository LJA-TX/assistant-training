# Stage B v1 Checkpoint Execution Plan (No-Execution Draft)

## Scope
This plan defines exact staging boundaries for a disciplined two-commit checkpoint. It does not execute commits.

## Preconditions
1. Confirm no new training/eval/dataset mutation occurred since readiness report generation.
2. Confirm approved draft cleanup already applied.
3. Confirm current branch remains `main` and remote tracking is intact.

## Commit 1
### Name
`checkpoint_core_execution_and_forensics`

### Intent
Preserve reproducibility-critical datasets/configs/manifests and all finalized probe/forensic outputs.

### Staging commands
```bash
git add data/v1_0/dataset_v1_0_stage_b_recovery_i10r_*
git add configs/lora/stage_b_llama31_8b_base_v1_i10r_*
git add manifests/runs/stage_b_llama31_8b_base_v1_i10r_*
git add manifests/reports/stage_b_v1_i10r_*probe*
git add manifests/reports/stage_b_v1_i10r_*forensics*
git add manifests/reports/stage_b_v1_i10r_*taxonomy*
git add manifests/reports/stage_b_v1_i10r_*causal*
git add manifests/reports/stage_b_v1_i10r_*stability*
git add manifests/reports/stage_b_v1_i10r_*rollback*
git add manifests/reports/stage_b_v1_i10r_*next_step*
```

### Proposed commit message
`checkpoint: preserve i10r probe execution and forensic lineage`

### Validation before commit
```bash
git diff --cached --name-only
```
Verify staged set contains only core execution/forensic artifacts.

## Commit 2
### Name
`checkpoint_governance_and_design_context`

### Intent
Preserve convergence-housekeeping reports, governance artifacts, dataset-generation diagnostics, and builder lineage context.

### Staging commands
```bash
git add scripts/build_stage_b_recovery_i10r_*
git add manifests/reports/stage_b_v1_convergence_*
git add manifests/reports/stage_b_v1_i10r_*design*
git add manifests/reports/stage_b_v1_i10r_*dataset_plan*
git add manifests/reports/stage_b_v1_i10r_*readiness_criteria*
git add manifests/reports/stage_b_v1_i10r_*risk_assessment*
git add manifests/reports/stage_b_v1_i10r_*diagnostics*
git add manifests/reports/stage_b_v1_i10r_*preflight_validation*
git add manifests/reports/stage_b_v1_i10r_*contamination_audit*
git add manifests/reports/stage_b_v1_i10r_*prompt_ambiguity_audit*
git add manifests/reports/stage_b_v1_i10r_*localized_diff_verification*
git add manifests/reports/stage_b_v1_i10r_*human_review_package*
```

### Proposed commit message
`docs: preserve i10r governance context and convergence checkpoint planning`

### Validation before commit
```bash
git diff --cached --name-only
```
Verify staged set is governance/design context only.

## Ordering Rationale
1. Commit 1 establishes replay/reproducibility and behavioral evidence baseline.
2. Commit 2 adds doctrine/context on top, making rollback and review clearer.

## Rollback Guidance (If Boundaries Are Wrong)
- Unstage all currently staged paths:
```bash
git restore --staged .
```
- Re-stage by commit group using the pathspecs above.
- Re-run `git diff --cached --name-only` after each group.

## Files That Must Remain Untracked
- **Mandatory untracked set: none**.

Optional defer-to-later (if scope minimization is desired) should be explicitly approved before exclusion:
- `manifests/reports/stage_b_v1_i10r_*training_execution_readiness.json`
- duplicate/derived summaries flagged in `stage_b_v1_convergence_cleanup_candidates.json`

## Execution Safety Notes
- Do not auto-delete duplicate/derived artifacts during checkpoint execution.
- Do not run any training/eval/dataset commands during checkpointing.
