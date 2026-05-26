# Potential Skill Proposal: `canonical-eval-stage-ab`

## Purpose
Codify the charter-governed workflow for:
1. Resolving and pinning `canonical_eval_manifest_v1.json` from template.
2. Running canonical baseline eval on `Llama-3.1-8B-base`.
3. Building dataset v1.0 under Appendix A composition and leakage rules.
4. Executing Stage A and Stage B LoRA iterations with canonical re-eval.
5. Applying binding promotion gates and autonomous budget limits.

## Trigger Conditions
Use this skill when requests include any of:
- "execute charter v5a" / "Appendix A" / "metric spec v1a"
- "pin canonical eval manifest"
- "run baseline + stage A/B"
- "promotion gates" / "budget limits"

## Binding Authorities
- `docs/goal_charter_v5a.md`
- `docs/appendix_a_operational_execution_contract_v3a.md`
- `docs/metric_specification_v1a.md`

## Canonical Target
- Base model: `Llama-3.1-8B-base`
- Canonical path in this environment:
  - `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base`

## Required Inputs
- Eval manifest template and canonical manifest path.
- Runtime commit + tool schema hash.
- Dataset split paths and SHA256 hashes.
- Scorer script path + hash.
- Training/eval script hashes.
- Environment snapshot (torch/transformers/PEFT/CUDA + pip freeze hash).

## Workflow
1. Pin runtime and evaluation contract.
2. Resolve and fully pin canonical eval manifest.
3. Run canonical baseline eval (base-only).
4. Build dataset v1.0 with composition/leakage reports.
5. Launch Stage A run, capture summary, run canonical eval.
6. Launch Stage B run, capture summary, run canonical eval.
7. Compare base vs Stage A vs Stage B deltas.
8. Enforce promotion gates and budget checks.
9. Emit final promotion recommendation with rationale.

## Promotion Gate Checks (Appendix A v3a)
Minimum promising threshold (vs canonical base baseline):
- exact JSON validity delta >= +10 percentage points
- tool-name accuracy delta >= +5 percentage points
- invalid_json rate must decrease
- wrapper leakage must not worsen by >5 percentage points
- no-call correctness must not degrade by >10 percentage points

Suggested strong-candidate thresholds:
- exact JSON validity >= 50%
- tool-name accuracy >= 35%
- argument accuracy >= 25%

## Budget and Escalation Checks
Per Appendix A defaults:
- max 5 serious runs per stage before escalation
- max 3 consecutive no-progress serious runs
- max 24 GPU-hours/day autonomous usage
- max 20% dataset-size growth per iteration unless justified

## Required Artifacts Per Serious Run
- run config + run manifest
- resolved config + masking audit
- training summary
- canonical eval summary and class distributions
- comparison rows/logs
- gate decision and promotion/rejection rationale

## Non-Negotiables
- Do not change tool schema/eval semantics mid-cycle without new versioning.
- Keep canonical decode settings fixed for promotion scoring.
- Treat safety/no-call regressions as blocking risks.
- Do not promote on loss-only improvements.

## Packaging Plan (Next Step)
When converting this proposal into an active Codex skill:
1. Create skill folder `canonical-eval-stage-ab`.
2. Move this workflow into `SKILL.md` frontmatter + imperative steps.
3. Add optional helper scripts for hash capture and gate scoring.
4. Validate with `quick_validate.py` and forward-test on a fresh run.
