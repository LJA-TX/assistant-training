# D0 Implementation Architecture

## Scope

This document defines the read-only implementation architecture for the D0 reconstruction-verification package covering:

- `i3`
- `H0`
- `H1`
- `H2`

It is design only.

- No reconstruction is executed here.
- No datasets are modified here.
- No configs are modified here.
- No manifests are modified here.
- No training is launched here.
- No new experimental arms are introduced here.

## Design Goals

The implementation must:

1. Certify source-artifact fidelity from raw bytes.
2. Preserve row identity and ordering as first-class evidence.
3. Produce deterministic, machine-readable certification outputs.
4. Fail closed on any authority, integrity, or diff conflict.
5. Avoid inference, normalization, or repair when evidence is missing.

## Authority Flow

The implementation resolves authority in the following order:

1. `docs/continuity/D0_RECONSTRUCTION_AUTHORITY_MATRIX.md`
2. `docs/continuity/D0_RECONSTRUCTION_IMPLEMENTATION_PLAN.md`
3. `docs/continuity/D0_VALIDATION_CHECKLIST.md`
4. `docs/continuity/D0_ACCEPTANCE_CRITERIA.md`
5. Raw source artifacts under `data/`, `configs/`, `manifests/`, `evals/`, and `docs/phase_*`

If a lower-precedence artifact disagrees with a higher-precedence artifact, the higher-precedence source wins and the discrepancy is recorded as a failure, not reconciled by inference.

## Architecture Overview

The D0 implementation is a deterministic, read-only pipeline with seven logical subsystems.

### 1. Authority resolver

Responsibilities:

- Load the authority matrix and the approved implementation plan.
- Resolve the authoritative source for each reconstruction surface.
- Resolve precedence when artifacts disagree.
- Emit a machine-readable authority summary used by later stages.

### 2. Source artifact inventory builder

Responsibilities:

- Enumerate every required source artifact path.
- Capture presence, size, byte hash, and authority tier.
- Classify each artifact as primary, corroborating, derived, or missing.
- Produce the source inventory report used by later validators.

### 3. Hash ledger builder

Responsibilities:

- Compute raw-byte SHA-256 hashes for all inventoried artifacts.
- Record the published hash claim, computed hash, source path, and claim origin.
- Flag any mismatch as a closed failure.

### 4. Row ledger builder

Responsibilities:

- Read JSONL rows in byte order.
- Assign stable row identities from explicit metadata keys.
- Record row position, row digest, message digest, and identity keys.
- Preserve one ledger line per row without reshaping row content.

### 5. Surface verifiers

Responsibilities:

- Verify the `i3` scaffold against the published control hashes and row ledger.
- Verify `H0` as a metadata-only re-expression of the `i3` control bytes.
- Verify `H1` and `H2` against their published dataset hashes, patch accounting, and tool-family distributions.
- Verify that no surface requires reconstruction of missing evidence.

### 6. Diff certifier

Responsibilities:

- Compare `i3` vs `H0` configs and manifests field by field.
- Compare `H0` vs `H1` configs and manifests field by field.
- Compare `H1` vs `H2` configs and manifests field by field.
- Emit the exact certified deltas and reject any extra field change.

### 7. Acceptance aggregator

Responsibilities:

- Collect all verification outputs.
- Map failures to the taxonomy.
- Determine surface-level and run-level completion.
- Emit the final acceptance summary.

## Canonical Output Root

Future D0 certification runs must write only to:

`/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/`

The output tree is treated as generated evidence, not as a source of truth.

## Data Flow

The pipeline is strictly ordered:

1. Lock authority.
2. Snapshot source artifacts.
3. Build the source inventory.
4. Build the hash ledger.
5. Build the row ledger.
6. Verify `i3`.
7. Verify `H0`.
8. Verify `H1`.
9. Verify `H2`.
10. Certify config diffs.
11. Certify manifest diffs.
12. Verify eval-surface fidelity.
13. Emit the missing-artifact report.
14. Emit the acceptance summary.

No later step may overwrite or reinterpret earlier evidence.

## Reconstruction Surfaces

### `i3` scaffold

The `i3` surface is the control scaffold. It anchors row identity, control-byte hashes, and downstream comparison semantics.

### `H0`

`H0` is a metadata-only control comparator. Its dataset bytes are the `i3` control bytes, while its config and manifest are separately certified by field-level diff.

### `H1`

`H1` is the first replacement-patch surface. Its reconstruction must be certified from the published train/val bytes, patch accounting, and tool-family distribution evidence.

### `H2`

`H2` is the second replacement-patch surface. Its certification rules match `H1`, with pairwise comparison against `H1` rather than `H0`.

## Row Identity Model

Row identity must never be inferred from prose or from generated outputs. The implementation must require explicit row identity metadata.

Canonical row identity keys:

- `source_case_id`
- `phase_i_parent_case_id`
- `phase_i_variant`
- `phase_i_patch_slot`
- `category`
- `tool`

Required row-identity checks:

- row count matches the published surface summary
- row ordering matches the published JSONL order
- row digests match the row ledger
- identity keys are stable and unambiguous
- patch rows map to the published patch slot positions
- inherited control rows remain unchanged where they are expected to be unchanged

## Dataset Integrity Model

Dataset integrity is certified from raw JSONL bytes, not from summaries.

Required integrity checks:

- raw-byte SHA-256 matches the published hash
- row count matches the published count
- JSONL line count matches the row ledger
- row ordering is identical to the source file ordering
- no duplication or omission is detected
- no contamination appears in holdout or adversarial surfaces

## Patch Accounting Model

Patch accounting is a direct row-level reconciliation between the published summary and the actual JSONL train surface.

Required checks:

- patch size equals the published size
- replacement positions match exactly
- each replacement row is accounted for once
- the patch slot map is total and non-overlapping
- tool-family counts match the published distribution

## Tool-Family Distribution Model

Tool-family distribution is a derived report, but the row ledger must preserve the direct evidence needed to recompute it.

Required checks:

- tool counts are recomputed from row payloads
- counts match the published summary exactly
- no hidden tool-family source is used
- inherited control rows and patch rows are separated in the report

## Config and Manifest Certification Model

Config and manifest certification is field-level, not hash-only.

Rules:

- Parse the final config and manifest as structured objects.
- Compare paths and values at field granularity.
- Enumerate every added, removed, or changed field.
- Reject any delta not listed in the approved diff surface.
- Do not infer intent from neighboring fields.

This rule is especially important for `i3 -> H0`, `H0 -> H1`, and `H1 -> H2` because each pair has a fixed certified delta set.

## Eval-Surface Fidelity Model

The eval surface is certified from frozen manifest and bundle evidence.

Required checks:

- canonical eval manifest hash matches the published value
- scorer path and metric-spec path match the frozen contract
- comparison rows and summary outputs are present for the executed bundles
- bundle manifests identify the correct bundle class and role
- split hashes match the published values

## Failure Handling

The implementation must stop on the first authoritative failure in a surface family.

Examples:

- authority conflict
- missing required artifact
- hash mismatch
- row identity mismatch
- patch accounting drift
- tool-family drift
- config diff drift
- manifest diff drift
- eval-surface drift
- unexpected output generation

No retry, normalization, or data repair is allowed.

## Implementation Risks and Hidden Assumptions

The following assumptions must be treated as explicit and checked, not implicit:

- Raw bytes are authoritative for every SHA-256 claim.
- JSONL byte order is authoritative for row identity.
- Published summary prose is corroborating evidence only.
- Control val bytes are intentionally shared across `i3`, `H0`, `H1`, and `H2`.
- Final config and manifest certification depends on field-level diffs, not on a hash claim alone.
- Any future generated output is absent by design before execution and is not itself a failure.
- Missing evidence must be reported as missing, not reconstructed.
- No causal attribution may be inferred from evaluation prose when a row-level or field-level source exists.

## Non-Goals

This architecture does not define reconstruction algorithms, model training procedures, or artifact repair logic. It only defines the verification machinery that will be used later to certify D0 reconstruction fidelity.
