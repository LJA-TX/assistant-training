# D0 Tooling Construction Plan

## Status

Pre-code design only.

- No reconstruction execution.
- No dataset modification.
- No config modification.
- No manifest modification.
- No training.
- No certification output generation yet.

This plan implements the verification framework described by:

- [D0_IMPLEMENTATION_ARCHITECTURE.md](/opt/ai-stack/assistant-training/docs/continuity/D0_IMPLEMENTATION_ARCHITECTURE.md)
- [D0_OUTPUT_ARTIFACT_SPECIFICATION.md](/opt/ai-stack/assistant-training/docs/continuity/D0_OUTPUT_ARTIFACT_SPECIFICATION.md)
- [D0_FAILURE_TAXONOMY.md](/opt/ai-stack/assistant-training/docs/continuity/D0_FAILURE_TAXONOMY.md)
- [D0_HASH_AUTHORITY_VERIFICATION.md](/opt/ai-stack/assistant-training/docs/continuity/D0_HASH_AUTHORITY_VERIFICATION.md)
- [D0_EXECUTION_SEQUENCE.md](/opt/ai-stack/assistant-training/docs/continuity/D0_EXECUTION_SEQUENCE.md)

## Objective

Build a read-only D0 verification toolkit that can:

1. resolve authority for every reconstruction surface
2. inventory every required source artifact
3. compute and record authoritative hashes
4. generate row and diff evidence during full certification
5. stop closed on any failure category defined in the taxonomy
6. run a dry-run mode that exercises authority resolution, inventory generation, and hash ledger generation without full certification

## Tooling Architecture

### Layer 1: CLI entrypoint

One primary CLI should orchestrate all D0 modes:

- `scripts/d0_verify.py`

Expected responsibilities:

- parse command-line options
- resolve repository root
- select `dry-run` or `certify` mode
- enforce output-root restrictions
- dispatch into the verification pipeline
- emit a final run summary and exit code

Suggested CLI shape:

```bash
python scripts/d0_verify.py \
  --mode dry-run \
  --run-id d0_YYYYMMDDThhmmssZ \
  --output-root /opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification
```

### Layer 2: Verification library package

Use a small Python package under `scripts/` so the top-level entrypoint stays thin:

```text
scripts/d0_verification/
  __init__.py
  cli.py
  authority.py
  artifacts.py
  hashing.py
  inventory.py
  row_ledger.py
  diff_certifier.py
  eval_surface.py
  reports.py
  schemas.py
  failures.py
  paths.py
  models.py
```

Design principles:

- read-only by default
- deterministic ordering
- raw-byte hashing only
- explicit field-path diffing
- no inference-based repair
- no write access outside the declared output root

### Layer 3: Shared path resolution

The toolkit should reuse `scripts/repo_paths.py` for repository-root detection and canonical path resolution.

That avoids a second, divergent path registry and keeps the D0 tooling aligned with existing repository conventions.

### Layer 4: Stage pipeline

The full certification pipeline should be decomposed into stage functions:

1. authority resolution
2. source inventory generation
3. hash ledger generation
4. row ledger generation
5. dataset integrity certification
6. patch accounting certification
7. tool-family distribution certification
8. config diff certification
9. manifest diff certification
10. eval-surface fidelity certification
11. missing-artifact reporting
12. acceptance summarization

The dry-run path terminates after stage 3.

## Implementation Plan

### Phase 1: Scaffold the package

Deliverables:

- CLI entrypoint
- package directory under `scripts/d0_verification/`
- shared dataclasses and enum-like constants
- read-only path guards
- run-id and output-root validation

Key design choices:

- keep the CLI thin
- keep artifact serialization in `reports.py`
- keep failure classification in `failures.py`
- keep path constants in `paths.py`

### Phase 2: Implement authority resolution

Deliverables:

- parse the D0 authority matrix
- load the approved implementation plan
- resolve the precedence order
- build the authoritative source map for `i3`, `H0`, `H1`, and `H2`
- emit a machine-readable authority resolution payload for dry-run output

Core outputs:

- `authority_resolution.json` in dry-run mode
- authority metadata attached to all downstream artifacts

### Phase 3: Implement artifact inventory and hash ledger

Deliverables:

- enumerate all required source artifacts
- classify each artifact as primary, corroborating, derived, or missing
- compute raw-byte SHA-256 values
- compare raw hashes to published claims
- record source provenance and conflict handling

Core outputs:

- `inventory/source_artifact_inventory.json`
- `ledgers/hash_ledger.json`

This phase is the full extent of the requested dry-run mode.

### Phase 4: Implement row-ledger and certification surfaces

Deliverables:

- row-level identity extraction
- row-order preservation
- patch-slot tracking
- tool-family counting
- dataset integrity reporting
- patch accounting reporting
- tool-family distribution reporting

Core outputs:

- `ledgers/row_ledger.jsonl`
- `reports/dataset_integrity_report.json`
- `reports/patch_accounting_report.json`
- `reports/tool_family_distribution_report.json`

### Phase 5: Implement diff certification

Deliverables:

- field-level diff extraction for configs
- field-level diff extraction for manifests
- exact pair coverage for:
  - `i3 -> H0`
  - `H0 -> H1`
  - `H1 -> H2`
- unexpected-delta rejection

Core outputs:

- `diffs/config_diff_certification.json`
- `diffs/manifest_diff_certification.json`

### Phase 6: Implement eval-surface fidelity checks

Deliverables:

- canonical eval manifest validation
- scorer and metric-spec validation
- split-hash validation
- bundle-manifest validation
- executed-summary and comparison-row presence checks

Core outputs:

- `reports/eval_surface_fidelity_report.json`

### Phase 7: Implement acceptance aggregation

Deliverables:

- surface-by-surface pass/fail aggregation
- failure taxonomy mapping
- blocked/fatal/advisory status rollup
- missing-artifact report
- final acceptance summary

Core outputs:

- `reports/missing_artifact_report.json`
- `reports/acceptance_summary.json`

## File Layout

### Source code layout

```text
scripts/
  d0_verify.py
  d0_verification/
    __init__.py
    cli.py
    authority.py
    artifacts.py
    hashing.py
    inventory.py
    row_ledger.py
    diff_certifier.py
    eval_surface.py
    reports.py
    schemas.py
    failures.py
    paths.py
    models.py
```

### Test layout

```text
tests/
  test_d0_verify.py
  test_d0_verify_dry_run.py
  test_d0_verification_authority.py
  test_d0_verification_inventory.py
  test_d0_verification_hashing.py
  test_d0_verification_row_ledger.py
  test_d0_verification_diff_certifier.py
  test_d0_verification_eval_surface.py
  test_d0_verification_schemas.py
  test_d0_verification_failures.py
```

### Runtime output layout

Certification runs remain under:

```text
/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/
```

Dry runs should use a separate namespace so they never masquerade as certified reconstruction evidence:

```text
/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/dry_runs/<run_id>/
```

Recommended dry-run layout:

```text
/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/dry_runs/<run_id>/
  authority/
    authority_resolution.json
  inventory/
    source_artifact_inventory.json
  ledgers/
    hash_ledger.json
  reports/
    dry_run_summary.json
  logs/
    dry_run.log
```

Dry runs do not emit:

- row ledger
- patch accounting report
- tool-family distribution report
- config diff certification
- manifest diff certification
- eval-surface fidelity report
- acceptance summary

## Proposed Modules

### `cli.py`

Responsibilities:

- parse `--mode`, `--run-id`, `--output-root`, and `--strict`
- validate mutually exclusive options
- dispatch into `dry-run` or `certify`
- convert structured failures into exit codes

### `paths.py`

Responsibilities:

- resolve repository root through `scripts/repo_paths.py`
- define canonical input and output paths
- enforce output-root containment

### `authority.py`

Responsibilities:

- load the approved D0 authority documents
- apply precedence ordering
- resolve authoritative sources for each surface
- produce an explicit authority-resolution record

### `artifacts.py`

Responsibilities:

- define artifact records and roles
- classify required vs corroborating artifacts
- attach source provenance

### `hashing.py`

Responsibilities:

- compute raw-byte SHA-256 values
- compare computed values to published claims
- format hash-claim evidence

### `inventory.py`

Responsibilities:

- build the source artifact inventory
- determine presence and size
- record claim source and corroborators
- flag missing required artifacts

### `row_ledger.py`

Responsibilities:

- load JSONL rows without normalization
- extract explicit identity keys
- compute row digests
- preserve source ordering

### `diff_certifier.py`

Responsibilities:

- compute structured field diffs
- certify the approved pairwise deltas
- reject any unexpected field change

### `eval_surface.py`

Responsibilities:

- validate canonical eval manifest fields
- validate score, metric, split, and bundle references
- record the fidelity status for each eval surface

### `reports.py`

Responsibilities:

- serialize JSON and JSONL artifacts
- maintain schema versioning
- build the final summary payloads

### `schemas.py`

Responsibilities:

- define the machine-readable schemas
- validate required fields
- keep schema version strings centralized

### `failures.py`

Responsibilities:

- map verifier findings to the D0 failure taxonomy
- classify severity and stop conditions
- format blocked/fatal/advisory outcomes

### `models.py`

Responsibilities:

- hold dataclasses for inventories, hash entries, row entries, and diff records
- avoid ad hoc dict construction in the core pipeline

## Dry-Run Workflow

Dry run is a bounded, read-only exercise of the first three stages.

### Inputs

- D0 authority matrix
- D0 implementation plan
- D0 validation checklist
- D0 acceptance criteria
- D0 hash authority verification doc
- all required source artifacts referenced by the implementation plan

### Steps

1. resolve authority precedence
2. determine the authoritative source for each surface
3. enumerate required source artifacts
4. verify file presence
5. compute raw-byte SHA-256 hashes
6. record published claim vs computed value
7. emit the dry-run inventory
8. emit the dry-run hash ledger
9. emit the dry-run summary

### Expected outputs

- authority resolution payload
- source artifact inventory
- hash ledger
- dry-run summary
- optional logs

### What dry-run must not do

- generate row ledger entries
- compare configs or manifests
- evaluate bundle fidelity
- certify patch accounting
- certify tool-family distributions
- produce final acceptance summaries
- touch datasets, configs, manifests, or training code

## Validation Strategy

Validation must prove two things:

1. the tooling is read-only
2. the tooling is faithful to the D0 authority and artifact contracts

### Unit-level validation

Recommended coverage:

- authority precedence resolution
- path resolution and output-root containment
- SHA-256 computation
- artifact presence classification
- inventory ordering and serialization
- dry-run exit behavior
- failure taxonomy mapping

### Schema validation

Every emitted JSON artifact should be checked against its required field set.

Validation rules:

- required keys must exist
- array membership must be exhaustive where mandated
- pair sets must match the approved pair list exactly
- unexpected keys should be rejected unless explicitly allowed

### Dry-run integration validation

The dry-run workflow should be exercised against the repository snapshot with a test output root.

Validation goals:

- confirm only dry-run artifacts are emitted
- confirm the source inventory covers the approved source set
- confirm the hash ledger reproduces known published values
- confirm no source file is modified

### Full-mode validation

After dry-run passes, full certification mode should be validated in stages:

- row ledger creation from JSONL inputs
- pairwise config diff certification
- pairwise manifest diff certification
- eval-surface fidelity
- acceptance aggregation

### Negative testing

At least one test should exercise each of these failure families:

- missing required artifact
- hash mismatch
- row identity mismatch
- unexpected diff field
- invalid schema
- unauthorized output path

### Determinism checks

The same dry-run execution should produce byte-stable JSON output when run twice against the same snapshot.

Useful assertions:

- identical hash ledger entries
- identical inventory ordering
- stable JSON serialization
- unchanged source file hashes

## Read-Only Enforcement

The implementation must enforce read-only behavior at three layers:

1. code paths only open inputs for read access
2. output writes are restricted to the declared output root
3. the tests fail if any source file hash or timestamp changes unexpectedly

This is not optional. It is part of the verification contract.

## Risks And Assumptions

Known risks to carry into implementation:

- a path helper drift would silently break source resolution if the CLI reimplements repo-root logic
- diff certification can drift if nested field paths are not canonicalized
- row identity can drift if JSONL parsing normalizes bytes before hashing
- dry-run can be mistaken for certified output unless it uses its own namespace
- stale corroborating docs can disagree with raw bytes; the code must fail closed, not reconcile

Assumptions that should remain explicit:

- the approved D0 docs remain the controlling authority
- raw bytes remain authoritative for hash computation
- certification artifacts are generated only under the declared output root
- dry-run artifacts are not treated as certified evidence

## Deliverable Boundary

This plan is the pre-code implementation package for D0-T.

The next step, after approval, is to implement the CLI and library package exactly once, then cover it with read-only tests before any full certification run is attempted.
