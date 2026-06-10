# Evaluator Contract Drift Final Determination

## Executive Summary

The canonical manifest pins an older evaluator hash than the one currently present on `main`.
The current evaluator hash is the result of intentional, landed updates that add prompt-trace provenance and supplemental Stage C evidence plumbing.
The canonical scoring path did not materially change.
The fresh Phase E revalidation remains usable.

## Root Cause

The manifest pin was not repointed after the evaluator file evolved through a sequence of intentional commits.
The last hash-changing commit in the current line is `325bdb4` (`Support E1 prompt trace and path registry`), which produces the current SHA-256 hash.

## Semantic Impact

The changes are Category B/C:

- diagnostics-only for prompt-trace and supplemental evidence output
- infrastructure-only for row identity and path registry support

No Category D or E evidence was found in the canonical scoring path.

## Contract Status

Scenario 1 is supported: the manifest hash is stale.

The evaluator is not the problem.
The contract pin is.

## Recommended Remediation

Apply Option A: update the manifest hash only.

The manifest should point to `08a5cec22a781193365bed85b709ceebef534846602004bbfa047f4e0b59d738`.

## Effect On Phase E Results

The Phase E results remain usable.

- Base revalidation reproduces the prior classification pattern exactly.
- Adapter revalidation has a narrow row-level variance in `heldout_validation`, but the aggregate conclusions and gate outcomes do not change.
- There is no evidence that the evaluator scoring contract drifted in a way that invalidates the Phase E evidence set.

## Go / No-Go Determination

**No-Go** for proceeding into Phase F while the manifest remains pinned to the stale scorer hash.

**Go** once the manifest is repinned to the current evaluator hash and the bundle is recorded as the authoritative contract state.
