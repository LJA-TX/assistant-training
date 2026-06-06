# Push Readiness Checklist

## Purpose

Standardize safe push execution after publication approval.

## Trigger

Use when push is explicitly authorized.

## Checklist

- [ ] Confirm working tree is clean.
- [ ] Confirm no ZIP bundles are tracked or staged.
- [ ] Confirm no unintended files are staged.
- [ ] Confirm current `HEAD` matches reviewed commit or documented intentional descendant.
- [ ] Execute push command to intended remote/branch (for example: `git push origin main`).
- [ ] Verify push completed successfully.
- [ ] Verify local and remote are synchronized (`git rev-list --left-right --count origin/main...main`).
- [ ] Verify no unexpected file changes occurred during push.
- [ ] Report push result, pushed commit hash, sync status, and anomalies.

## Boundary Notes

- This checklist governs push operation safety only.
- It does not define milestone acceptance criteria.
