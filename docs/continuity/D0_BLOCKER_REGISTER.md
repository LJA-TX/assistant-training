# D0 Blocker Register

## Blocker Entry

| Field | Value |
|---|---|
| blocker_id | `D0-BLK-TRAINING-SCRIPT-PROVENANCE-001` |
| affected_artifact | `scripts/train_lora_sft.py` |
| canonical_hash_claim | `28900accae3d6abf05ddb9e86b41c03ad3c812a683f3af343bffa94281e14c8b` |
| current_live_hash | `faf6cd4b676e230c5d2797392bc2fca204752d012f3e80e71c0af4ced7288432` |
| earliest_surviving_source_of_claim | `evals/canonical_eval_manifest_v1.json` first committed in `82c6b32` (`evals: add canonical eval manifest and canonical_v1 data`) |
| investigation_result | No reachable git blob for `scripts/train_lora_sft.py` reproduces the canonical hash. The claim is documented in the canonical manifest, but the preserved repository history does not explain the claimed bytes. |
| certification_impact | D0 certification remains fail-closed and blocked on unresolved training-script provenance. Row-ledger and full certification work must not proceed while this blocker is open. |
| allowed_resolution_paths | Locate an archived byte-preserving copy matching the canonical hash; locate an external/publication bundle containing the canonical bytes; prove the manifest claim was generated from a specific non-git source artifact; explicitly re-scope D0 to current-tree comparability in a later governance decision. |
| prohibited_resolution_paths | Edit `evals/canonical_eval_manifest_v1.json` to match current bytes; downgrade the block to advisory without authority change; infer bytes from prose; continue certification as though the hash matched. |

## Status

This blocker is active until a documented authority update or preserved byte source resolves the canonical training-script hash claim.
