# D0 Dry-Run Provenance Finding

Current D0 dry-run status: `blocked`.

## Findings

- `dataset_builder` is classified as `stale_but_resolvable`.
- `training_script` is classified as `stale_unresolved`.
- The blocking condition remains the unresolved provenance gap for `training_script`.

## Why D0 Remains Blocked

D0 certification is fail-closed by design. A required artifact may be stale only if its historical provenance can be resolved read-only against an authoritative historical reference. `dataset_builder` satisfies that condition. `training_script` does not, so certification must remain blocked.

## Why This Is Not A Tooling Failure

The dry-run machinery is behaving correctly:

- it computes the current live hash,
- compares that hash to the published claim,
- resolves a historical reference when one is available and valid,
- and leaves unresolved provenance gaps fatal.

That behavior distinguishes a resolvable stale pin from a real unresolved contract gap. The remaining failure is provenance, not verifier malfunction.

## Why No Manifest Or Hash Claim Should Be Edited

The manifest hash claims are the published authority surface. Editing them to match the current repository state would convert a provenance finding into a rewrite of the historical record. The correct action is to preserve the published claims and resolve provenance through authoritative history, not to normalize the claims retroactively.

## Certification Boundary

Certification must remain fail-closed until `training_script` provenance is resolved. No row-ledger or full certification work should proceed from this state.
