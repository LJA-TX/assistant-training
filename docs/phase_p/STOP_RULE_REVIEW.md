# Stop Rule Review

## Verdict

The existing Phase L stop rules remain appropriate for Dataset v1.2 without modification.

## Review

### Preflight Stops

The preflight gates are still correct:

- config or manifest path must resolve;
- model and tokenizer mirrors must be available;
- train and val JSONL paths must exist;
- loss policy must remain fail-fast;
- the adapter output directory must not already exist;
- the draft config or manifest must not be mutated after review without revalidation.

These are still the right operational checks before a governed v1.2 launch.

### Training Stops

The training stops are still correct:

- NaN or infinite loss;
- dataset load failure;
- divergence from adapter-only output policy;
- hidden retry or auto-chain behavior.

None of those should be relaxed because the candidate improved structurally.

### Post-Training Stops

The post-training stops remain the correct promotion barriers:

- any contamination overlap;
- any wrapper leakage;
- `no_call_correctness < 1.0`;
- `adversarial_no_call_correctness < 1.0`;
- aggregate `no_call_correctness < 0.95`;
- aggregate invalid JSON above `0.30`;
- any canonical eval manifest, decode default, or scoring drift;
- any strong-system-prompt override for promotion.

Dataset v1.2 does not reduce the need for these checks.

### Escalation Rule

The escalation rule remains appropriate:

- if the candidate is clean but lands in an inconclusive band against H0/H1/H2, stop after the first run;
- do not retune thresholds;
- do not launch another internal-only run without new authorization.

That rule is still scientifically correct because the question remains whether the combined bottleneck is resolved, not whether one more exploratory run might be informative.

## Conclusion

No stop-rule changes are needed.
The current rule set is still the right guardrail package for the first governed Dataset v1.2 run.
