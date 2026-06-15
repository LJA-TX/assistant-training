# D0 to Current-Tree Mechanism Isolation Governance

## Decision

Stage D is transitioned away from canonical-byte replay as the primary scientific path and toward a current-tree mechanism-isolation program.

This transition does **not** remove the D0 blocker. Canonical-byte D0 certification remains blocked by `D0-BLK-TRAINING-SCRIPT-PROVENANCE-001`.

## Authority Position

1. Canonical-byte D0 certification remains blocked by `D0-BLK-TRAINING-SCRIPT-PROVENANCE-001`.
2. The unresolved `training_script_sha256` claim is treated as a documented, closed provenance gap unless new byte-preserving evidence appears.
3. No manifest or hash-claim edits are authorized.

## Scope Preserved for D0

D0 remains valuable for non-training-script surfaces and should continue to be treated as the verification authority for:

- dataset identity
- row identity
- patch accounting
- config diffs
- manifest diffs
- eval-contract fidelity

These surfaces remain useful for reconstruction fidelity, provenance checking, and compare/contrast work even though the canonical training-script bytes are unresolved.

## H1/H2 Treatment

H1 and H2 are preserved as observational reference regimes.

They are not byte-perfect replay targets. They are fixed historical evidence surfaces that can be compared against current-tree behavior, but they should not be repurposed as a reconstruction mandate for the missing canonical trainer bytes.

## Future Current-Tree Mechanism Isolation Program

A future current-tree mechanism-isolation program may be planned using:

- current stabilized `scripts/train_lora_sft.py`
- current stabilized `scripts/build_dataset_v1.py`
- preserved H1/H2 data, config, and eval surfaces
- preregistered A1/A2/A3-style arms

That future program should treat the preserved H1/H2 surfaces as reference regimes for mechanism discovery and comparability analysis, not as byte-perfect historical replay targets.

## Non-Authorization List

This governance note does **not** authorize:

- canonical-byte certification
- row-ledger or full certification execution
- A1/A2/A3 experiments
- training
- manifest edits
- hash-claim edits

## Labeling Requirement

Any future current-tree mechanism-isolation work must be labeled clearly as:

- current-tree comparability, or
- mechanism discovery

It must not be described as historical byte-perfect reconstruction.

## Status

The D0 blocker remains active. The repository may now pursue current-tree mechanism-isolation planning on preserved H1/H2 reference surfaces, but only under later authorization and only with explicit scope separation from canonical-byte D0 certification.
