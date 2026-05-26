# Stage B i8 Human Review Checklist (Template)

Purpose: determine whether i8 remains safe to unlock for dataset generation.

## Hard Blocks
- [P] `approved_to_generate_dataset` remains `false` everywhere until this checklist is complete.
- [P] `approved_to_run` remains `false` everywhere until post-review sign-off.
- [P] No i8 train/val JSONL outputs were generated during scaffolding.

## Localized Intervention Integrity
- [P] Targeted families remain only `rg_search` and `read_file`.
- [P] No global prompt-template rewrites were introduced.
- [LP] No global negation-heavy schema pressure patterns are present.

## Contamination / Overlap
- [LP] Heldout overlap is zero for prompt, target, and source-case identifiers.
- [CP] Tool-holdout overlap is zero for prompt, target, and source-case identifiers.

## Diversity / Anti-Homogenization
- [P] Targeted style-bucket distribution shows more than one style family.
- [?] Targeted prompt skeleton concentration does not indicate single-template dominance.
- [?] Prompt-length delta does not show narrow inflation collapse.

## Overconstraint Risk
- [DP-P] Forbidden-pattern scan has zero intervention-layer hits.
- [-P] Anti-homogenization summary has no blocking risk signals.

## Reviewer Questions
- [LP] Are we accidentally recreating i4/i5 dynamics locally inside targeted tool families?
- [LP] Are parseability gains likely to come from genuine structural recovery instead of template coercion?
- [LP] Is there evidence of coupled schema spill risk (`payload_not_object` / `missing_tool_calls`) still increasing?

## Decision
- [P] Approve progression to dataset-generation phase request.
- [ ] Reject and return to implementation constraints review.


Legend
P = PASS
LP = Likely PASS
CP = Conditional PASS (pending follow-up results review)
DP-P = Design PASS / Emprical Pending (design appears correct, need output to answer reliably)
-P = Pending Dataset Generation (need output to answer reliably)

