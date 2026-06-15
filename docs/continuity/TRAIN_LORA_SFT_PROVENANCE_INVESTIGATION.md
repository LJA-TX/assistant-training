# `scripts/train_lora_sft.py` Provenance Investigation

## Scope

This review searched the current repository contents and reachable git history for:

- `28900accae3d6abf05ddb9e86b41c03ad3c812a683f3af343bffa94281e14c8b`
- `training_script_sha256`
- `scripts/train_lora_sft.py`

It also checked preserved verification/journal artifacts for any byte-preserving source that could explain the canonical manifest claim.

## Conclusion

The canonical hash claim for `training_script_sha256` is anchored in the committed canonical eval manifest, but no reachable git blob for `scripts/train_lora_sft.py` reproduces that SHA-256.

The evidence supports this interpretation:

- the claim originated as a committed manifest field, not as a reproducible script blob in the current repository history;
- the script has since diverged through a sequence of legitimate commits; and
- the preserved verification artifacts only corroborate the current live hash, not the canonical one.

## Evidence Chain

| Evidence | Result |
|---|---|
| `evals/canonical_eval_manifest_v1.json` added in commit `82c6b32` | First surviving committed artifact containing `training_script_sha256 = 28900accae3d6abf05ddb9e86b41c03ad3c812a683f3af343bffa94281e14c8b` |
| Reachable git history search for `training_script_sha256` | Only the canonical manifest contains the field in committed history |
| Reachable git history search for the exact canonical hash | Only the canonical manifest contains the literal in committed history |
| Script blob history for `scripts/train_lora_sft.py` | Six reachable versions were found; none hash to the canonical value |
| Phase I control-surface verification | Records the current live script hash as `faf6cd4b676e230c5d2797392bc2fca204752d012f3e80e71c0af4ced7288432`, confirming the live bytes differ from the canonical claim |
| Phase I journal | Records the verification command used to snapshot hashes, but not a preserved blob matching the canonical value |

## Timeline

| Date | Commit | Artifact | Observation |
|---|---|---|---|
| 2026-05-26 | `82c6b32` | `evals/canonical_eval_manifest_v1.json` | Canonical hash claim introduced in a committed manifest |
| 2026-05-26 | `7b694fb` | `scripts/train_lora_sft.py` | Initial reachable script blob hashes to `17382b1a615ced26c76a16c712aaa5c49472715d04e133218134afbfbc4b7b70`, not the canonical hash |
| 2026-05-29 | `b19acb7` | `scripts/train_lora_sft.py` | Instrumentation foundation changed the script; new hash `dd98cdf4b34d9fc969c4624528d84300d84e41d314c600a4fe0d99627af4bb93` |
| 2026-05-29 | `7669f1b` | `scripts/train_lora_sft.py` | Typed geometry digest contract changed the script; new hash `dc5e2d9df7aa40ca6c2ceff7e0fb2d4dd72da83e97ed1b0ee2ee9d1fe9c63a5d` |
| 2026-05-29 | `3b4812e` | `scripts/train_lora_sft.py` | First live geometry probe package changed the script; new hash `63cb9b622725192f1afd89374a3d17d7b6e68a54b69a794bd366f168287c1b17` |
| 2026-05-29 | `ae559ba` | `scripts/train_lora_sft.py` | Weighted-sampler hook signature fix changed the script; new hash `e68efd5639c46d1049b40128dd753e0c4226a6dd5b7951360a62e979380cb936` |
| 2026-06-06 | `97491ef` | `scripts/train_lora_sft.py` | Compatibility path decoupling changed repo-root/config resolution; current live hash `faf6cd4b676e230c5d2797392bc2fca204752d012f3e80e71c0af4ced7288432` |
| 2026-06-11 | `9edc154` | `docs/phase_i/CONTROL_SURFACE_VERIFICATION.md` | Verification doc records the current live script hash, not the canonical manifest hash |

## Candidate Explanations

1. The canonical hash was copied from an external or lost historical snapshot that is not preserved in reachable git history.
2. The canonical hash came from a generated publication bundle, archived evaluation package, or sidecar that is no longer present in the repository.
3. The canonical hash was captured from an intermediate script state that predates the current reachable history.
4. The canonical hash is simply stale or incorrect relative to the preserved repository state.

## Confidence Assessment

- High confidence: no reachable git blob for `scripts/train_lora_sft.py` reproduces the canonical hash.
- High confidence: the committed canonical manifest is the earliest surviving artifact that states the hash.
- Medium confidence: the true source, if it exists, is outside the current reachable repository history.
- Low confidence: any preserved in-repo artifact other than the canonical manifest can reproduce the claimed bytes.

## Recommendation

Keep D0 fail-closed.

Do not edit the manifest or hash claim to match the current repository state.

If a later investigation finds an archived bundle, publication artifact, or historical snapshot with the canonical bytes, register it as the authoritative historical reference instead of rewriting the published claim. Until then, treat `scripts/train_lora_sft.py` as a provenance gap, not a tooling problem.
