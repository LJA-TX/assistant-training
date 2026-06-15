# D0 Historical Code Resolution Plan

## Scope

This document defines a read-only historical-code-resolution layer for D0 dry-run and future certification runs.

It applies only to code artifacts whose live repository bytes may differ from the published canonical eval claim:

- `scripts/train_lora_sft.py`
- `scripts/build_dataset_v1.py`

This is a design and implementation plan only.

- No reconstruction is executed here.
- No manifest hashes are edited here.
- No published hash claims are updated here.
- No datasets, configs, or manifests are modified here.
- No advisory override is introduced here.

## Goal

D0 must distinguish four evidence states for each code artifact:

1. the current live repository hash
2. the canonical manifest published hash claim
3. an optional historical git resolution
4. an unresolved provenance gap

The historical path exists only to explain and, when valid, resolve stale code pins.
It does not replace the canonical manifest, and it does not weaken fail-closed behavior.

## Authority Order

Historical resolution follows the existing D0 authority chain:

1. canonical contracts and governance artifacts
2. machine-readable source artifacts in the current repository snapshot
3. explicit historical source-map inputs
4. git object database evidence reachable from the repository
5. narrative or advisory notes

When artifacts disagree, the higher-precedence evidence wins for classification, but the disagreement is still recorded.

## Accepted Historical References

D0 dry-run should accept one or more of the following optional inputs.

### 1. Commit reference

Shape:

- artifact id
- repo-relative path
- commit oid

Example:

```json
{
  "artifact_id": "dataset_builder",
  "reference_kind": "git_commit",
  "repo_path": "scripts/build_dataset_v1.py",
  "commit_oid": "7b694fbd8df5e7bbc5073127732ff9283992b085"
}
```

Resolution rule:

- materialize `repo_path` from `commit_oid` using git plumbing only
- compute SHA-256 from the raw bytes
- compare the result to the published claim

### 2. Blob reference

Shape:

- artifact id
- repo-relative path
- blob oid

Example:

```json
{
  "artifact_id": "training_script",
  "reference_kind": "git_blob",
  "repo_path": "scripts/train_lora_sft.py",
  "blob_oid": "<git blob oid>"
}
```

Resolution rule:

- read the blob bytes from the git object database
- verify the supplied repo-relative path matches the artifact registry entry
- compute SHA-256 from the blob bytes
- compare the result to the published claim

### 3. Explicit historical source-map JSON

Recommended canonical input:

`docs/continuity/d0_historical_source_map.json`

Schema intent:

- one entry per required artifact
- each entry names the repo-relative path and the historical reference kind
- source-map entries may provide commit or blob references
- CLI overrides may supersede the JSON entries on a per-artifact basis

The source map is the preferred machine-readable input because it is deterministic, reviewable, and easy to preserve for provenance audits.

## Resolution Sequence

For each code artifact, D0 must evaluate evidence in this order:

1. Read the current working-tree bytes and compute the live SHA-256.
2. Read the published SHA-256 from `evals/canonical_eval_manifest_v1.json`.
3. If the live SHA-256 matches the published claim, mark the artifact `current_match`.
4. If the live SHA-256 differs, look for an explicit historical reference.
5. If a historical reference is present, validate its path association and materialize the historical bytes.
6. If the historical bytes match the published claim, mark the artifact `stale_but_resolvable`.
7. If the historical bytes materialize but do not match the published claim, mark the artifact `hash_mismatch`.
8. If no valid historical reference exists, mark the artifact `stale_unresolved` or `missing_required_source` depending on whether any authoritative bytes could be materialized.

This sequence is read-only. D0 must never checkout historical content into the working tree.

## Status Taxonomy

Use one provenance status field with the following values:

| Status | Meaning | Blocking behavior |
|---|---|---|
| `current_match` | Current live bytes match the published claim. | Non-blocking. |
| `stale_but_resolvable` | Current live bytes differ, but a valid historical reference resolves to the published claim. | Non-blocking. |
| `stale_unresolved` | Current live bytes differ, but no valid historical reference resolves the claim. | Fatal/blocking. |
| `missing_required_source` | Neither current bytes nor a valid historical source can be materialized. | Blocking. |
| `hash_mismatch` | Bytes were materialized, but the computed hash does not match the published claim. | Fatal/blocking. |

### Status interpretation

- `current_match` means the live tree is aligned with the canonical claim.
- `stale_but_resolvable` means the live tree has drifted, but the canonical bytes are still recoverable from a verified historical source.
- `stale_unresolved` means the drift cannot be tied back to a verified historical source.
- `missing_required_source` means the artifact cannot be materialized from either the live tree or the supplied historical evidence.
- `hash_mismatch` means a concrete byte source exists and can be hashed, but the bytes do not satisfy the canonical claim.

### Failure-code mapping

Keep failure codes orthogonal to provenance status.

- `HISTORICAL_REFERENCE_PATH_MISMATCH`
- `HISTORICAL_REFERENCE_UNRESOLVABLE`
- `HISTORICAL_REFERENCE_HASH_MISMATCH`
- `MISSING_REQUIRED_SOURCE_ARTIFACT`
- `HASH_MISMATCH`

Path mismatches should be treated as provenance failures, not silently coerced into a match.

## Exit Semantics

### Dry-run

Dry-run remains read-only and non-reconstructive.

Recommended behavior:

- exit `0` when every required code artifact is `current_match` or `stale_but_resolvable`
- exit `1` when any required code artifact is `stale_unresolved`, `missing_required_source`, or `hash_mismatch`
- exit `2` for malformed input, unsafe paths, or other internal verification errors

Dry-run should surface `stale_but_resolvable` separately from fatal mismatch so reviewers can see that the provenance gap is explainable.

### Certification mode

Certification remains fail-closed.

It may pass only when every required historical code artifact is either:

- `current_match`
- `stale_but_resolvable`

Any `stale_unresolved`, `missing_required_source`, or `hash_mismatch` result keeps certification blocked.

## Recommended CLI/API Shape

### CLI

Extend `scripts/d0_verify.py` with optional historical inputs:

```bash
scripts/d0_verify.py \
  --mode dry-run \
  --output-root /opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification \
  --historical-source-map docs/continuity/d0_historical_source_map.json
```

Optional per-artifact override form:

```bash
--historical-reference training_script=git_commit:97491ef0a9556dd9357cc87fe0f788bc21b1dd73:scripts/train_lora_sft.py
--historical-reference dataset_builder=git_commit:7b694fbd8df5e7bbc5073127732ff9283992b085:scripts/build_dataset_v1.py
```

Recommended precedence:

1. explicit `--historical-reference` overrides
2. `--historical-source-map`
3. no historical reference

### Python API

Extend the dry-run entrypoint with explicit historical inputs:

```python
run_dry_run(
    *,
    repo_root: Path | None = None,
    output_root: Path | None = None,
    run_id: str | None = None,
    historical_source_map: Path | None = None,
    historical_references: dict[str, HistoricalReference] | None = None,
)
```

The API should be read-only and deterministic.

## Output Schema Additions

### `ledgers/hash_ledger.json`

Add these fields per code artifact entry:

- `current_live_sha256`
- `published_sha256`
- `selected_evidence_kind`
- `selected_evidence_ref`
- `selected_evidence_sha256`
- `historical_reference`
- `provenance_status`
- `resolution_error`
- `hash_status`

Recommended meaning:

- `current_live_sha256` is the SHA-256 of the working-tree bytes.
- `published_sha256` is the canonical manifest claim.
- `selected_evidence_sha256` is the SHA-256 of the evidence used to explain the classification, when a historical reference is available.
- `selected_evidence_kind` is `current`, `git_commit`, or `git_blob`.
- `provenance_status` is one of the five values above.
- `resolution_error` records why a historical reference failed, if it did.

### `reports/dry_run_summary.json`

Add these summary fields:

- `provenance_status_counts`
- `current_match_count`
- `stale_but_resolvable_count`
- `stale_unresolved_count`
- `missing_required_source_count`
- `hash_mismatch_count`
- `historical_reference_count`
- `historical_resolution_success_count`
- `historical_resolution_failure_count`
- `blocked_artifact_ids`

The summary should make it obvious whether the run is blocked by an unresolvable provenance gap or merely exhibits explainable drift.

### `reports/eval_surface_fidelity_report.json`

Add these fields for future certification:

- `code_artifacts`
- `code_artifact_status_counts`
- `historical_resolution_mode`
- `current_live_sha256`
- `published_sha256`
- `selected_evidence_sha256`
- `provenance_status`
- `resolution_error`
- `blocked_artifact_ids`

The eval-surface report should explicitly identify whether code comparability is based on current live bytes or on historical resolution.

## Inventory and Ledger Implications

The source inventory should carry the same provenance classification so downstream reports do not need to infer it from the hash ledger.

Recommended inventory additions:

- `current_live_sha256`
- `published_sha256`
- `provenance_status`
- `historical_reference`
- `resolution_error`

This keeps the inventory, hash ledger, and summary aligned.

## Test Matrix

Add tests that cover the following cases.

### 1. Current hash matches published claim

Test name:

- `test_current_hash_matches_published_claim`

Expected result:

- `provenance_status == "current_match"`
- `hash_status == "match"`
- dry-run remains non-blocking

Fixture style:

- a synthetic temp file or a known current-match artifact

### 2. Current hash differs but historical blob matches

Test name:

- `test_current_hash_differs_but_historical_blob_matches`

Expected result:

- `provenance_status == "stale_but_resolvable"`
- `selected_evidence_kind in {"git_commit", "git_blob"}`
- `selected_evidence_sha256 == published_sha256`
- dry-run reports the artifact separately from fatal mismatches

Recommended fixture:

- `scripts/build_dataset_v1.py` with a historical reference to the baseline commit that still matches the published builder hash

### 3. Current hash differs and no historical blob matches

Test name:

- `test_current_hash_differs_and_no_historical_blob_matches`

Expected result:

- `provenance_status == "stale_unresolved"`
- `hash_status == "mismatch"`
- run is blocked

Recommended fixture:

- `scripts/train_lora_sft.py`

### 4. Provided historical reference path does not match expected artifact path

Test name:

- `test_historical_reference_path_mismatch_is_rejected`

Expected result:

- provenance classification is not promoted to `stale_but_resolvable`
- `resolution_error == "path_mismatch"` or equivalent
- failure is recorded as a provenance failure

### 5. Provenance gap remains fatal

Test name:

- `test_provenance_gap_remains_fatal`

Expected result:

- `stale_unresolved` or `missing_required_source` remains blocking
- exit status remains non-zero
- summary includes the blocking artifact id

## Implementation Constraints

- Historical resolution must use git plumbing only.
- No checkout, rebase, reset, or file mutation is allowed.
- Current live bytes always remain the first comparison surface.
- Historical evidence may explain drift, but it must never overwrite the published claim.
- If multiple historical references are supplied, D0 must record the full set and choose the first valid resolution by the documented precedence order.

## Residual Risks

1. A commit reference may be reachable in git history but not byte-identical to the intended archival state if the wrong path is paired with the commit oid. The path check must therefore be explicit.
2. A blob oid without a matching path can explain bytes, but not artifact identity. The path association must still be recorded.
3. A historical source-map JSON can become stale if it points to an object that later disappears from a shallow clone or pruned object database. That condition must be classified as unresolved, not repaired.
4. `train_lora_sft.py` currently demonstrates the unresolved provenance-gap case; this is expected to remain fatal until an actual historical source is provided.

## Decision

This plan preserves the fail-closed boundary and adds a historical-resolution path only for provenance explanation.

It does not add any advisory override.
