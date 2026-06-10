# Contract Integrity Assessment

## Question

Is the manifest hash stale, did the evaluator change materially, or did both happen?

## Evidence

- The manifest pins `80af75c494e0da59f30f33a910997b5fdff15d4ffa8dca09988cdedc0fc06e3f`.
- The current evaluator file hashes to `08a5cec22a781193365bed85b709ceebef534846602004bbfa047f4e0b59d738`.
- The hash lineage shows a sequence of intentional evaluator updates, with `325bdb4` producing the current hash.
- The classification logic in `scripts/eval_canonical_manifest.py` is unchanged in the canonical scoring section.
- The added code paths are prompt-trace, row-identity, and supplemental evidence plumbing.

## Scenario Test

### Scenario 1: Manifest hash is stale

- Supported by the evidence.
- The manifest still points to an older script hash.
- The current evaluator is the one now present on `main`.

### Scenario 2: Evaluator changed materially

- Not supported for the canonical scoring contract.
- No scoring-rule change was found in the canonical class assignment path.

### Scenario 3: Both

- Not supported by the evidence collected here.
- The evaluator changed, but the material drift is in diagnostics and evidence surfaces, not in the canonical scoring contract.

## Determination

Scenario 1 is the supported scenario.
The contract problem is a stale manifest pin, not a broken canonical scorer.
