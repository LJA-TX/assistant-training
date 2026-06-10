# Dataset Evolution Strategy

## Recommendation

**Strategy A: Incremental Dataset v1.1 expansion**

## Why This Strategy

The current dataset is already structurally aligned with the charter at the category level. The problem is not the broad mix. The problem is that the tool-positive training signal is too concentrated. A full redesign would risk breaking the parts that already work, especially no-call correctness and runtime restraint.

An incremental v1.1 expansion lets us preserve the working balance while replacing the narrow tool-positive saturation with broader tool-call coverage.

## Evidence

- Train and val already match the charter's category balance.
- The train tool-positive slice is a single repeated case and a single tool.
- No-call correctness is already strong, so the next iteration should not destabilize that advantage.
- The external survey produced several viable supplementation candidates, with xLAM / APIGen and When2Call standing out as the strongest primary additions.

## What v1.1 Should Change

- Broaden the tool-positive corpus so the model sees multiple tools, prompts, and argument shapes.
- Keep runtime-alignment, no-call, and refusal coverage near the current ratios.
- Use high-verification external data first.
- Canonicalize every external source into the runtime schema before ingestion.
- Preserve the current evaluation contract and leakage checks.

## Suggested Source Priorities

1. xLAM / APIGen as the primary tool-positive source family.
2. When2Call as the primary no-call / follow-up supplement.
3. APIGen-MT as a secondary multi-turn supplement if licensing is acceptable.
4. ToolACE as a later diversity supplement after filtering.
5. Glaive only as a filtered broad-format fallback.
6. BFCL-related assets for evaluation only, not training.
7. ToolBench only if a broader fallback corpus is still needed after the higher-quality families.

## Why Not a Full v2 Redesign

- The current balance already matches the charter.
- The current no-call behavior is not the problem.
- A redesign would add more moving parts than the evidence justifies.

## Why Not Targeted Augmentation Only

- The tool-positive collapse is large enough that the next step should be versioned as a proper expansion, not as a handful of isolated examples.
- The dataset needs broader tool diversity, not only a small patch on top of the current shape.

## Sources Used

- `CURRENT_DATASET_ASSESSMENT.md`
- `EXTERNAL_DATASET_SURVEY.md`
- `DATASET_COMPATIBILITY_ASSESSMENT.md`
- `DATASET_RISK_ASSESSMENT.md`
- `docs/goal_charter_v5a.md`
- `docs/appendix_a_operational_execution_contract_v3a.md`
