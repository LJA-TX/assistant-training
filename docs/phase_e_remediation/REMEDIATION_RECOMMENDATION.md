# Remediation Recommendation

## Recommendation

**Option A: Update manifest hash only**

## Why This Is the Smallest Correct Remediation

- The manifest pin is stale relative to the current evaluator file.
- The current evaluator changes are diagnostic and infrastructure oriented, not canonical scoring changes.
- The fresh revalidation results remain usable and preserve the Phase E conclusion.
- There is no evidence that restoring the prior evaluator is required.
- There is no evidence that a new canonical evaluation generation is required.

## Required Action

Update `evals/canonical_eval_manifest_v1.json` so `scoring.scorer_sha256` points to:

`08a5cec22a781193365bed85b709ceebef534846602004bbfa047f4e0b59d738`

## Not Recommended

- Restoring the prior evaluator would roll back accepted evidence plumbing without a scoring-contract need.
- Creating a new canonical evaluation generation would be disproportionate to the observed drift.
- Any other remediation would expand scope beyond the contract mismatch.
