# Git-Ignore Verification Checklist

## Purpose

Ensure temporary review artifacts (especially ZIP bundles) remain untracked and unstaged.

## Trigger

Use after creating any temporary bundle or local review artifact.

## Checklist

- [ ] Verify ignore rule applies (`git check-ignore -v <path>`).
- [ ] Confirm ignored path is under `local_review_bundles/`.
- [ ] Confirm artifact is not staged (`git status --short`).
- [ ] Confirm artifact is not tracked (`git ls-files --error-unmatch <path>` should fail).
- [ ] Confirm no unintended ignored-path exceptions were introduced.

## Boundary Notes

- Ignore verification is a hygiene check only.
- It does not replace publication-readiness or push-readiness checks.
