# Public Snapshot Identity And Versioning Assessment

Status: accepted snapshot identity; public publication and annotated tagging are separately governed

Date: 2026-07-11

## Purpose

Record a durable historical identity for a public publication point without coupling that identity to mutable repository heads or claiming a software-release contract that does not exist.

## Chosen Convention

The repository reuses the existing Publication Lineage Version 2 convention. The machine-readable record identifies a frozen public publication point inside a living curated package. The public and private repositories are governed related lineages, not identical mirrors.

The record is historical: future commits do not invalidate the snapshot, and the recorded commits are not required to equal later `HEAD` values.

## Snapshot Record

The machine-readable source of truth is:

- [docs/publication/public_snapshot.json](../../publication/public_snapshot.json)

The historical record contains:

- Snapshot ID: `publication-lineage-v2-snapshot-v1`
- Snapshot version: `v1`
- Publication date: `2026-07-11`
- Publication lineage: `Publication Lineage Version 2`
- Status: `living curated package with a frozen historical publication snapshot`
- Public snapshot commit: `05634b6a3f47dfd6cf5656d4ab8da7997bf894d1`
- Private lineage commit: `9d88798c506328635200b95b5aff9234dc127079`

The relationship statement explicitly says that the record identifies one frozen public publication point, that future commits do not invalidate it, and that private engineering continues independently.

## Tag Recommendation

Recommend an annotated tag named `publication-lineage-v2-snapshot-v1` in the public repository `LJA-TX/assistant-training`, pointing to public commit `05634b6a3f47dfd6cf5656d4ab8da7997bf894d1`. The JSON record is authoritative for the portable snapshot identity; the annotated tag would provide an independent Git-native corroboration when deliberately created. This implementation remains valid before the tag exists.

This document does not assert that the annotated tag exists; tag presence must be verified independently in Git history.

The current public pre-push guard authorizes only a bounded `refs/heads/main` publication. An ordinary tag push is therefore not authorized by the current guard. Creating the annotated tag requires a separate reviewed and authorized operation, using either a deliberately bounded tag mechanism or another explicitly governed GitHub operation. The JSON record remains authoritative whether or not the tag is later created.

## Original Rejection Reasons

The previous implementation was rejected because its tests required recorded private and public commits to equal live repository `HEAD`, which made later preservation self-invalidating; it hardcoded a workstation-specific public checkout path; and its assessment prematurely declared the work accepted.

## Corrected Semantics

The corrected implementation validates field names, commit syntax, date format, fixed snapshot values, front-door consistency, historical language, and absence of workstation paths. It does not compare recorded commits with mutable `HEAD`. Optional object-existence and ancestry checks run only when explicit repository paths are configured and skip when those paths are unavailable.

## Remaining Review Questions

1. Whether the maintainer wants the recommended annotated public tag created in a separate authorized operation.
2. Whether the publication date should remain the assembly date for future snapshots or be defined as the remote publication date.
3. Whether a future snapshot should increment the snapshot marker or introduce a separate publication event record.

## Validation Boundary

The snapshot identity is accepted. Whether this record is present in a particular checkout or remote is established by that repository's history. Public projection and publication, and annotated-tag creation, remain separately governed operations. The JSON record remains authoritative whether or not a tag exists. Omitted private artifacts are not claimed to be publicly available, and the public package is not claimed to be reproducible from the complete private engineering history.
