# D0 Failure Taxonomy

## Purpose

This taxonomy defines how the D0 verification machinery classifies failures, when it stops, and what must be recorded when it does.

The taxonomy applies only to reconstruction-verification work. It does not authorize repair, inference, or execution.

## Severity Levels

- `fatal`: stop the run immediately. No later surface may be evaluated.
- `blocking`: stop the affected surface family and mark the run blocked. No repair or retry is allowed.
- `advisory`: record the condition and continue.

## Stop Rules

1. The first `fatal` failure stops the run immediately.
2. A `blocking` failure stops the current surface family and any downstream dependent checks.
3. `advisory` findings never change certification status by themselves.
4. If a higher-precedence source conflicts with a lower-precedence source, the lower-precedence source is discarded and the conflict is still recorded as a failure.

## Failure Categories

| Code | Trigger | Severity | Stop condition | Required response |
|---|---|---:|---|---|
| `AUTHORITY_CONFLICT` | The authority matrix, implementation plan, validation checklist, acceptance criteria, or raw source artifacts disagree on what is authoritative. | fatal | Stop immediately. | Record both authorities, the precedence chain, and the unresolved conflict. |
| `MISSING_REQUIRED_SOURCE_ARTIFACT` | A required source artifact listed in the implementation plan is absent from the snapshot. | blocking | Stop the affected surface family. | Mark the artifact missing and do not infer its contents. |
| `MISSING_CORROBORATING_ARTIFACT` | A corroborating artifact is absent, but the primary artifact is present. | advisory | Continue. | Record the missing corroborator and the surviving primary evidence. |
| `HASH_MISMATCH` | The computed raw-byte SHA-256 does not match the published hash claim. | fatal | Stop immediately. | Record the artifact path, published value, computed value, and claim source. |
| `ROW_IDENTITY_MISMATCH` | A row cannot be mapped to the required identity keys or the identity keys disagree with the published row ledger. | fatal | Stop immediately. | Record the row index, surface, identity keys, and mismatch reason. |
| `ROW_DUPLICATION_OR_GAP` | The row ledger reveals duplicated rows, skipped rows, or count mismatches. | fatal | Stop immediately. | Record the duplicate or missing indices and the affected surface. |
| `PATCH_ACCOUNTING_DRIFT` | The patch size, patch-slot coverage, or replacement positions differ from the published summary. | fatal | Stop immediately. | Record expected and observed patch positions and counts. |
| `TOOL_FAMILY_DRIFT` | Recomputed tool-family counts do not match the published distribution. | fatal | Stop immediately. | Record expected and observed counts by tool family. |
| `CONFIG_DIFF_DRIFT` | The field-level config diff contains an unexpected field change or omits a certified change. | fatal | Stop immediately. | Record the full field-diff set and the unapproved delta. |
| `MANIFEST_DIFF_DRIFT` | The field-level manifest diff contains an unexpected field change or omits a certified change. | fatal | Stop immediately. | Record the full field-diff set and the unapproved delta. |
| `EVAL_SURFACE_DRIFT` | The canonical eval manifest, scorer, metric spec, split hash, bundle manifest, comparison rows, or summary evidence disagrees with the frozen contract. | blocking | Stop the eval-surface family. | Record the mismatched eval contract element and the affected bundle. |
| `OUTPUT_SCHEMA_DRIFT` | A generated artifact does not match the required machine-readable schema or omits required fields. | fatal | Stop immediately. | Record the file path and schema violation. |
| `FILESYSTEM_MUTATION` | An input artifact is modified, or any unauthorized path is written. | fatal | Stop immediately. | Record the path, the mutation type, and the time observed. |
| `EXECUTION_LEAKAGE` | A reconstruction output appears before its stage is authorized, or a downstream artifact is used as upstream evidence. | fatal | Stop immediately. | Record the leaked path and the leaked dependency chain. |
| `INFERENCE_CONTAMINATION` | A missing row, field, or diff is filled by heuristic inference instead of source evidence. | fatal | Stop immediately. | Record the inferred element and the missing source evidence. |
| `UNAUTHORIZED_RECONSTRUCTION_OUTPUT` | Any A1, A2, A3, training, or reconstructed output is generated during D0. | fatal | Stop immediately. | Record the unauthorized path and the process that created it. |

## Additional Classification Rules

- Hash failures are never downgraded to advisory.
- Row identity failures are never repaired by ordering heuristics.
- Config and manifest diffs are certified only by explicit field paths; any hidden delta is a fatal failure.
- Future outputs that do not yet exist are not failures by themselves.
- A missing optional mirror report is advisory only if the canonical machine-readable artifact is present.

## Surface Stop Semantics

The following units are treated as surface families for stop purposes:

- `i3` control family
- `H0` control family
- `H1` replacement family
- `H2` replacement family
- config diff certification
- manifest diff certification
- eval-surface fidelity

If a fatal failure occurs in one family, all later families remain unverified and must be reported as such.

## Examples Of Non-Fail Conditions

These conditions are expected and must not be misclassified as failures:

- The `H0`, `H1`, and `H2` control-val hash matching the `i3` control-val hash.
- Missing future-generated outputs before execution.
- Human-readable mirror files that are absent while the canonical JSON or JSONL artifact is present.
- A lower-precedence narrative report that disagrees with a higher-precedence machine-readable artifact.

## Recording Requirement

Every failure record must include, at minimum:

- `failure_code`
- `severity`
- `surface_id`
- `artifact_path`
- `observed_value`
- `expected_value`
- `precedence_source`
- `stop_action`
- `notes`
