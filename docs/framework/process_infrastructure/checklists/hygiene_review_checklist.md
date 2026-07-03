# Hygiene Review Checklist

## Purpose

Provide a repeatable repository hygiene check for slice boundaries and review checkpoints.

## Trigger

Use at minimum before final slice reporting, and before publication/push checkpoints.

## Checklist

- [ ] Review branch and repository status (`git status --short --branch`).
- [ ] Confirm all changed files align with authorized scope.
- [ ] Confirm no unexpected runtime, evaluator, or governance surfaces were modified.
- [ ] Confirm untracked files are expected and documented for the current slice.
- [ ] Confirm temporary artifacts remain in intended local-only locations.
- [ ] Confirm no unintended staging state exists.
- [ ] Confirm final report fields can be populated from verified command evidence.

## Boundary Notes

- Hygiene review detects operational drift.
- It does not replace domain-specific reconciliation or conformance validation.
