# Stop Rules

## Preflight Stop Rules

Stop before training if any of the following fails:

1. The config or manifest path does not resolve.
2. The model or tokenizer mirror is unavailable.
3. The train or val JSONL path is missing.
4. The loss policy is not fail-fast.
5. The adapter output directory already exists.
6. The draft config or manifest is mutated after review without a new pass through validation.

## Training Stop Rules

Stop training immediately if any of the following occurs:

1. Loss becomes NaN or infinite.
2. The trainer fails to load the dataset cleanly.
3. The run diverges from the configured adapter-only output policy.
4. Any hidden retry or auto-chain behavior appears.

## Post-Training Stop Rules

Stop and do not promote if any of the following occurs:

1. Any contamination overlap is nonzero.
2. Wrapper leakage is nonzero.
3. `no_call_correctness` or `adversarial_no_call_correctness` is below `1.0`.
4. Aggregate `no_call_correctness` is below `0.95`.
5. Aggregate invalid JSON is above `0.30`.
6. The canonical eval manifest, decode defaults, or scoring semantics drift.
7. The strong-system-prompt override is used for a result that is supposed to be promotable.

## Escalation Rule

If the candidate is clean but still lands in the inconclusive band against H0/H1/H2, stop after the first run.
Do not retune thresholds and do not launch another internal-only run without new authorization.
