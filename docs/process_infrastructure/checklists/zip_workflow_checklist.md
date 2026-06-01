# ZIP Workflow Checklist

## Purpose

Standardize review-bundle creation for bounded slices without polluting tracked repository paths.

## Trigger

Use when a slice requires a review ZIP bundle.

## Checklist

- [ ] Identify exact assets created or modified in the current slice.
- [ ] Confirm each selected asset path exists and is readable.
- [ ] Create a timestamped ZIP filename that is slice-specific.
- [ ] Write the ZIP only under `local_review_bundles/`.
- [ ] Verify ZIP contents (`unzip -l <zip_path>` or equivalent).
- [ ] Capture and report:
  - ZIP filename
  - full ZIP path
  - clickable path form (if environment supports clickable local paths)
- [ ] Confirm ZIP creation did not alter tracked artifact locations.

## Boundary Notes

- ZIP bundles are transport/review artifacts only.
- Canonical artifacts remain in their original repository paths.
