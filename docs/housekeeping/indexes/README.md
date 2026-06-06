# Canonical Index Infrastructure

This directory contains the Wave 0 index infrastructure defined by `W0-01`.

The goal is to establish canonical registry and family-index files before any repository-wide population or structural movement begins.

## Files

- `index_schema.json`
  - machine-readable field and ID specification
- `index_registry.json`
  - top-level registry for the family indexes
- `convergence_history_index.json`
- `reports_index.json`
- `manifests_index.json`
- `fixture_index.json`
- `sample_artifact_index.json`
- `archive_index.json`

## Validation

Run:

```bash
python scripts/validate_housekeeping_indexes.py
```

Validation checks:

- required fields
- stable ID uniqueness
- basic schema compliance
- registry-to-family cross-reference integrity

## Scope Boundary

This is seed infrastructure only.

It does not populate repository-wide indexes, move content, create archives, or change doctrine.
