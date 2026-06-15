# D0 Acceptance Criteria

## Acceptance Statement

D0 is accepted only when the reconstruction-verification package can certify the frozen `i3`, `H0`, `H1`, and `H2` surfaces without executing reconstruction, modifying datasets, or training.

## Must-Pass Criteria

### Authority

- The authority matrix exists and assigns one primary source per reconstruction surface.
- The authority matrix states a precedence order for conflicts.
- The matrix explicitly rejects inference-based repair of missing reconstruction facts.

### Source Availability

- All source artifacts required by the implementation plan are present.
- No required source artifact is missing in a way that blocks implementation.
- Any absent optional artifact is explicitly marked non-blocking.

### i3 Fidelity

- `i3` train and val hashes match the published values.
- `i3` row identity and ordering match the published summary.
- `i3` is the exact control comparator for H0.

### H0 Fidelity

- H0 is a metadata-only re-expression of the frozen `i3` control bytes.
- H0 config and manifest differences versus `i3` are limited to the certified field lists.
- H0 does not introduce dataset drift.

### H1 Fidelity

- H1 train and val hashes match the published values.
- H1 patch size is exactly `100`.
- H1 replacement positions, patch-row tool distribution, and row counts match the published summary.
- H1 config and manifest differences versus H0 are limited to the certified field lists.

### H2 Fidelity

- H2 train and val hashes match the published values.
- H2 patch size is exactly `100`.
- H2 replacement positions, patch-row tool distribution, and row counts match the published summary.
- H2 config and manifest differences versus H1 are limited to the certified field lists.

### Pairwise Diff Certification

- The final D0 report explicitly enumerates every field-level difference between `i3` and H0.
- The final D0 report explicitly enumerates every field-level difference between H0 and H1.
- The final D0 report explicitly enumerates every field-level difference between H1 and H2.
- No unlisted field delta appears in the certified diff tables.

### Eval-Surface Fidelity

- The canonical eval manifest is frozen and unchanged.
- Decode defaults remain pinned to the frozen manifest.
- The scorer path, metric-spec path, and split hashes remain frozen.
- The executed eval bundles conform to the published canonical comparison surfaces.

### Package Completeness

- The final D0 package contains the authority matrix.
- The final D0 package contains the implementation plan.
- The final D0 package contains the validation checklist.
- The final D0 package contains these acceptance criteria.
- The final D0 package contains a missing-artifact assessment.

## Current Missing-Artifacts Assessment

No blocking repository artifacts are currently missing for D0 implementation.

The following artifact families are present and therefore do not block implementation:

- canonical eval manifest
- `i3` train and val JSONL files
- `H0`, `H1`, and `H2` final config files
- `H0`, `H1`, and `H2` final run-manifest files
- `H1` and `H2` train and val JSONL files
- `H1` and `H2` summary JSON files
- `H1` and `H2` published bundle `package_manifest.json` files
- `H0`, `H1`, and `H2` executed eval summaries and comparison rows
- the required governance and closure documents under `docs/phase_h/` and `docs/phase_i/`

If any of those families were absent, D0 would be blocked.
