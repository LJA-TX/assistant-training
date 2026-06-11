# Phase J Lessons Learned Inventory

## Context

Phase IX completed the missing H1 datapoint, but the formal project determination remains `inconclusive_external_first`.
The current scientific interpretation is `Combined Bottleneck (E)`, so this inventory records what the repository actually demonstrated and what it still did not settle.

## Inventory

| Area | Conclusion | Confidence | Supporting evidence | Unresolved questions |
|---|---|---|---|---|
| What H0 demonstrated | H0 is a valid control comparator, but it is not safety-clean and does not establish usable tool-call competence. | High | `H0_control_i3_micro` completed training and canonical eval, but recorded `exact_json_validity = 0.045`, `tool_holdout_exact_valid = 0.0`, `heldout_validation_exact_valid = 0.09`, `no_call_correctness = 0.9166666666666666`, and `adversarial_no_call_correctness = 0.75`. | The row-level split between commitment loss, schema drift, and prompt-form dependence is still not fully resolved in the control checkpoint itself. |
| What H2 demonstrated | Commitment pressure is a real capability lever, but it introduces safety regressions. | High | `H2_commitment_patch` reached `exact_json_validity = 0.48`, `tool_name_accuracy = 0.7714285714285715`, `argument_accuracy = 0.6928571428571428`, `tool_holdout_exact_valid = 0.525`, `heldout_validation_exact_valid = 0.75`, and `no_anchor_exact_valid = 0.84375`, but also tripped `wrapper_leakage = 0.005`, `no_call_correctness = 0.8`, and `adversarial_no_call_correctness = 0.4`. | It remains unknown whether those gains can be preserved in a safety-clean variant that keeps no-call and adversarial correctness at `1.0`. |
| What H1 demonstrated | Diversity restoration is also a real capability lever, and it can outperform H2 on the tool-holdout slice, but it still fails safety invariants. | High | `H1_diversity_patch` reached `exact_json_validity = 0.44`, `tool_name_accuracy = 0.7142857142857143`, `argument_accuracy = 0.6285714285714286`, `tool_holdout_exact_valid = 0.6`, `heldout_validation_exact_valid = 0.64`, `no_anchor_exact_valid = 0.8636363636363636`, `wrapper_leakage = 0.0`, `no_call_correctness = 0.9`, and `adversarial_no_call_correctness = 0.7`. | It remains unknown whether a diversity-heavy design can keep the H1 tool-holdout lift while also becoming safety-clean. |
| What remains unknown | The repository still does not show a schema-dominant or methodology-dominant explanation, and it does not yet show a safety-clean combined solution. | Medium | H3 and H4 were not executed; H1 and H2 split the metric families rather than producing a single clean winner; all three runs fail at least one safety invariant. | The main unresolved questions are whether schema realization is independently dominant, whether methodology matters once content is balanced, and whether a v1.1 design can combine H1 and H2 gains without reintroducing wrapper leakage or no-call regressions. |

## Bottom Line

The evidence now supports a two-lever content story with a separate safety gate.
H2 proved that commitment matters.
H1 proved that diversity matters.
Neither run solved the safety problem, and no repository evidence justifies collapsing the bottleneck to a single lever.

## Sources Used

- `docs/phase_i/H0_CHECKPOINT_REPORT.md`
- `docs/phase_i/H2_CHECKPOINT_REPORT.md`
- `docs/phase_ix/H1_EXCEPTION_CHECKPOINT_REPORT.md`
- `docs/phase_ix/H1_EXCEPTION_SCIENTIFIC_INTERPRETATION.md`
- `docs/phase_i/PHASE_I_FINAL_COMPLETION_REPORT.md`

