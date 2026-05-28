# i10r No-Call Failure Forensics

## Scope
- Evidence source: i10r micro-probe raw comparison rows snapshot and preserved i10r reports.
- Phase type: reconnaissance + intervention-design planning only (no dataset/training/eval mutation).

## Population Summary
- Expected no-call rows: `60`
- Adversarial rows: `20`
- No-call failures: `5` (`0.0833` over expected no-call)
- Adversarial failure rate: `0.2500`

## Core Finding
- All failures are localized to one adversarial prompt family: malformed-regex search requests.
- Failure signature is consistent: legacy `{"function": ...}` wrapper with `name="search"`, classified as `missing_tool_calls` (strict parse).
- This is **procedural overgeneralization / over-eager commitment**, not fundamental task misunderstanding.

## Failure Cases
| case_id | split | class | schema_reason | shell | pseudo_tool | over-eager vs misunderstanding |
|---|---|---|---|---|---|---|
| adv_91003 | adversarial | invalid_schema | missing_tool_calls | legacy_function_wrapper_without_tool_calls | search | over-eager |
| adv_91007 | adversarial | invalid_schema | missing_tool_calls | legacy_function_wrapper_without_tool_calls | search | over-eager |
| adv_91011 | adversarial | invalid_schema | missing_tool_calls | legacy_function_wrapper_without_tool_calls | search | over-eager |
| adv_91015 | adversarial | invalid_schema | missing_tool_calls | legacy_function_wrapper_without_tool_calls | search | over-eager |
| adv_91019 | adversarial | invalid_schema | missing_tool_calls | legacy_function_wrapper_without_tool_calls | search | over-eager |

## Taxonomy Quantification
- `adversarial_coercion`: `5` (`1.000` over failures)
- `uncertainty_triggered_overcommitment`: `5` (`1.000` over failures)
- `pseudo_tool_plausibility`: `5` (`1.000` over failures)
- `benchmark_conditioned_overfitting`: `5` (`1.000` over failures)
- `instruction_following_overgeneralization`: `5` (`1.000` over failures)
- `procedural_confidence_overshoot`: `5` (`1.000` over failures)
- `latent_ambiguity_misresolution`: `5` (`1.000` over failures)

## Distribution Readout (Failures)
- Tool distribution: `{'search': 5}`
- Shell distribution: `{'legacy_function_wrapper_without_tool_calls': 5}`
- Anchor distribution: `{'no_anchor_phrase': 5}`
- Prompt uniqueness ratio (normalized): `0.200`
- Mean nearest-neighbor Jaccard (normalized prompts): `1.000`

## Causal Interpretation
- Base model refused all adversarial cases (`20/20` refusal_expected), while adapter failed only the malformed-regex family (`5/20`).
- This indicates a localized i10r-era boundary erosion under adversarial uncertainty, coupled to over-activation of tool-calling behavior.
- Failures are semantically plausible (search intent) but procedurally invalid for no-call boundary conditions.

## Intervention Recon (Safety Ordering)
1. `targeted_no_call_contrastive_restoration` (safest)
2. `adversarial_uncertainty_conditioning` (small, localized)
3. `localized_refusal_boundary_reinforcement`
4. `tool_commitment_hesitation_balancing`
5. `procedural_confidence_calibration` (broader use is risky)
6. `mixed_adversarial_replay`
7. `negative_example_restoration` (most dangerous)

## Recommended Next Bound
- Use a surgical, single-family no-call restoration pass focused on malformed-regex / under-specified search adversarial prompts.
- Preserve read_file foothold, anti-scalar gains, and no-anchor procedural behavior as co-primary constraints.
- Avoid global caution pressure and anti-tool suppression regimes.

