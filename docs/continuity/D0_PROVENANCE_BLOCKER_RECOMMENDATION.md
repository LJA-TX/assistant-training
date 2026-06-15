# D0 Provenance Blocker Recommendation

## Recommendation

Adopt **Option 1: strict resolution required before certification**.

Keep D0 fail-closed until the canonical `training_script_sha256` claim is explained by preserved bytes or until a later governance decision explicitly re-scopes D0 away from canonical-byte certification.

## Rationale

- Scientific integrity: the current repository does not contain a reachable `scripts/train_lora_sft.py` blob that reproduces the canonical hash claim.
- Reproducibility: certifying against the current tree would no longer mean certifying the published canonical bytes.
- Publication integrity: the manifest is the published authority surface and should not be rewritten to fit the live tree.
- Governance clarity: current-tree comparability is a different question and requires explicit authority change before it can replace canonical certification.

## Immediate Stance On Other Options

- Option 2 may be used only if a new external archive or publication bundle is identified. It is evidence discovery, not a substitute certification mode.
- Option 3 should not be adopted under the current authority set.
- Option 4 should not be adopted unless governance explicitly accepts the ambiguity of parallel reference regimes.
- Option 5 should be rejected because it converts an unresolved provenance gap into a permanent exception.

## Decision Text

Recommended decision:

> D0 remains blocked on `scripts/train_lora_sft.py` provenance. Certification may resume only after a byte-preserving authoritative source for the canonical hash claim is identified or after a separate governance decision formally re-scopes D0 to current-tree comparability.

## Boundary

No manifest edits, no hash-claim edits, no certification, and no reconstruction are authorized by this recommendation.
