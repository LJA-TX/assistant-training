# D0 Provenance Blocker Risk Assessment

## Summary

The unresolved `scripts/train_lora_sft.py` provenance gap is a high-severity governance risk because it blocks certification at the authority surface where D0 must distinguish published claims from current-tree bytes.

This is not a tooling defect. The dry-run machinery already demonstrated the difference between:

- a resolvable stale pin,
- an unresolved provenance gap, and
- a live hash that no longer matches the canonical claim.

## Risk Domains

| Risk domain | Current exposure | Consequence if unresolved | Severity | Primary mitigation |
|---|---|---|---|---|
| Canonical provenance integrity | Active | The published hash claim cannot be explained from reachable repository bytes. | High | Preserve the block until a byte-preserving authoritative source is found. |
| Scientific attribution | Active | Later D0/H1/H2 comparisons may mix historical canon with current-tree behavior. | High | Require strict resolution or a formally re-scoped authority. |
| Reproducibility | Active | Reviewers cannot reproduce the canonical claim from the live tree alone. | High | Locate preserved bytes or a preserved source-map to the canonical bytes. |
| Publication integrity | Active | Editing the manifest would rewrite the historical record rather than explain it. | High | Keep the manifest unchanged and preserve the published claim. |
| Governance drift | Active | Pressure may build to downgrade the block or treat the mismatch as advisory. | Medium to high | Keep the fail-closed rule until authority changes. |
| Audit complexity | Active | Current-tree, historical, and dual-track narratives can become conflated. | Medium | Keep a single authoritative resolution path unless governance explicitly re-scopes D0. |

## Option-Specific Risk Notes

### 1. Strict resolution required before certification

Lowest risk overall. It preserves the chain of authority and avoids contaminating the certification record.

### 2. External archive / publication bundle search

Low to medium risk. The main downside is schedule delay and the possibility that no preserved bytes are found.

### 3. Current-tree reconstruction certification path

High risk. It changes the question from canonical fidelity to current-tree comparability and can invalidate historical cross-run analysis.

### 4. Dual-track certification

High risk. It may be scientifically defensible only with precise labeling, but it increases the chance of interpretive error and publication ambiguity.

### 5. Permanent documented exception

Very high risk. It removes the blocker without resolving the underlying authority problem and would weaken the meaning of the canonical manifest.

## Bottom Line

The unresolved training-script hash claim is a provenance risk, not a computation risk. The safe posture is to keep certification blocked until the claim is resolved by preserved bytes or by a later formal governance re-scope.
