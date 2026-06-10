# Dataset Compatibility Assessment

## Criteria

Compatibility is judged against four things:

1. the goal charter's runtime-oriented assistant behavior,
2. Appendix A's frozen evaluation and dataset-composition rules,
3. the canonical evaluation framework,
4. the need to preserve strong no-call behavior while improving weak tool-call metrics.

## Assessment

### Salesforce xLAM / APIGen

**Fit: HIGH**

- Strong alignment with strict tool-call JSON, tool-name accuracy, and argument accuracy.
- The APIGen verification pipeline and xLAM release history provide the best quality signals in the survey.
- The family is compatible with runtime-oriented behavior after canonicalization into the assistant-runtime schema.

### Salesforce APIGen-MT

**Fit: MEDIUM**

- Good for multi-turn follow-up behavior and policy/domain interaction.
- Smaller scale and NC licensing reduce flexibility.
- Best treated as a supplement, not the core corpus.

### ToolACE

**Fit: MEDIUM**

- Good breadth and strong tool-learning relevance.
- More agentic and synthetic than the current runtime-oriented dataset wants to be.
- Useful after filtering, but not the cleanest primary source.

### Glaive function-calling v2

**Fit: MEDIUM**

- Useful breadth and function-call format exposure.
- Provenance detail is thinner than the strongest candidates.
- Likely helpful only after filtering for wrapper/prose reduction.

### BFCL-related public datasets

**Fit: LOW**

- Excellent benchmark material, but not appropriate as a training corpus.
- High contamination risk if the benchmark is folded into training.
- Best reserved for evaluation and diagnostic use.

### When2Call

**Fit: HIGH**

- Directly targets the no-call, follow-up, and admit-limits boundary that Appendix A cares about.
- Complements the current dataset's already-strong no-call behavior without threatening the objective.
- Very good fit as a targeted supplement.

### ToolBench

**Fit: LOW**

- Large and historically useful, but older and noisier than the best candidates.
- More likely to import conversational padding and wrapper leakage than the higher-quality families.
- Better treated as a fallback reference than a primary ingredient.

## Compatibility Conclusions

- **Best primary training fit:** xLAM / APIGen
- **Best boundary-behavior supplement:** When2Call
- **Best secondary diversity supplements:** APIGen-MT and ToolACE
- **Best optional broad-format supplement:** Glaive
- **Evaluation-only family:** BFCL-related public datasets
- **Lowest-priority fallback:** ToolBench

## Sources Used

- `docs/goal_charter_v5a.md`
- `docs/appendix_a_operational_execution_contract_v3a.md`
- External dataset survey sources listed in `EXTERNAL_DATASET_SURVEY.md`
