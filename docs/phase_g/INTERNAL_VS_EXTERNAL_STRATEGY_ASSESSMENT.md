# Internal vs External Strategy Assessment

## Executive Summary

Internal-first is the better next move for causal clarity.

External-first is the better next move for maximum eventual upside.

Those are not the same question.

For the specific Phase G mission, the preferred sequence is:

1. run one bounded internal-first proving slice,
2. stop if it does not break the i3 ceiling,
3. then move to external-first dataset expansion.

## Comparison Table

| Dimension | Internal-first | External-first |
|---|---|---|
| Expected effort | Low to medium | Medium to high |
| Main work | Rebuild internal diversity floors, recover omitted internal signal, rebalance internal recovery | Review, filter, canonicalize, and decontaminate external corpora |
| Main risk | False confidence from shallow internal gains | Contamination, style drift, schema mismatch, licensing review |
| Expected upside | Moderate | High |
| Expected learning value | Very high | Medium |
| Best use | Causal attribution and low-risk proof | Mainline performance expansion |

## Internal-First Assessment

### Expected effort

Internal-first work is relatively cheap because:

- the upstream sources already exist locally,
- the build scripts already exist,
- the failure profile is already pinned by Phase E,
- and the collapse mechanism is now understood precisely.

### Expected risk

Internal-first has lower contamination and license risk, but it has one major scientific risk:

- the project may spend more time extracting small gains from a corpus that is still fundamentally thin.

### Expected upside

The upside is real but bounded.

Why it should help:

- v1.0 collapse can be repaired directly,
- i3 omitted some upstream signal from the final training distribution,
- many tools can be balanced more intelligently than they were in either v1.0 or i3.

Why the upside is capped:

- `15` tool families in the i3 source pool still have exactly one source exemplar,
- tool-holdout exact-valid remains `0 / 40`,
- and the dominant residual failure is commitment / schema realization rather than simple absence of tool names.

### Learning value

Internal-first is the best way to answer the Phase G question itself because it isolates what the repository can already teach without confounding from external data.

## External-First Assessment

### Expected effort

External-first requires more front-loaded work:

- source review,
- contamination checks,
- canonicalization,
- schema normalization,
- quality filtering,
- and license interpretation.

### Expected risk

The risks are higher and already documented in Phase F:

- contamination if benchmark-adjacent data leaks in,
- style drift toward conversational or wrapper-heavy outputs,
- mismatched tool schemas,
- and licensing constraints on some candidates.

### Expected upside

External-first has the highest expected upside because it directly addresses the current bottleneck: shallow source depth per tool and per argument family.

The present internal corpus does not provide enough independent exemplars to assume strong heldout generalization across tool families or prompt forms. External tool-call corpora can change that if filtered well.

### Learning value

External-first improves the training asset base, but it answers the Phase G causal question less cleanly because any improvement would mix internal repair with new external supervision.

## Recommended Sequence

### Recommendation

Use an internal-first bounded proving slice before committing the mainline dataset program to external-first expansion.

### Why this sequence fits Phase G

- Phase G is an attribution phase, not a v1.1 implementation phase.
- The internal signal is strong enough to justify one clean proof slice.
- The internal signal is also weak enough in source depth that it should not justify repeated open-ended internal-only iterations.

### Proposed stop rule

The internal-first slice should stop and hand off to external-first if it fails to do at least one of the following:

- break the literal-anchor dependence seen in Phase E,
- produce nonzero exact-valid performance on tool-holdout,
- or produce a clear lift beyond the current i3 neighborhood on tool-expected rows.

If none of those happen, further internal-only iteration is more likely to consume time than to close the Appendix A gap.

## Determination

For Phase G:

- Preferred next assessment move: `internal-first`
- Preferred mainline dataset direction after that bounded proof: `external-first`

That is the most defensible combination of effort, risk, upside, and learning value supported by the repository evidence.

## Sources Used

- `docs/phase_f/DATASET_EVOLUTION_STRATEGY.md`
- `docs/phase_f/DATASET_RISK_ASSESSMENT.md`
- `docs/phase_f/EXTERNAL_DATASET_SURVEY.md`
- `docs/phase_f/INDEPENDENT_DATASET_COLLAPSE_ASSESSMENT_Grok-Build.md`
- `docs/phase_g/INTERNAL_SIGNAL_INVENTORY.md`
- `docs/phase_g/RECOVERY_CORPUS_ANALYSIS.md`
- `docs/phase_g/FAILURE_ATTRIBUTION_ANALYSIS.md`
- `docs/phase_g/COUNTERFACTUAL_ASSESSMENT.md`
