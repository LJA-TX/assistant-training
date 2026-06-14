# Commit And Push Procedure

Status: reusable operational note.

Use this procedure when a controlled phase is complete and the work should be committed and pushed.

## Preconditions

- All intended phase files are in place.
- Required validations have passed.
- The change set has been reviewed for scope and boundary compliance.
- If the work includes a canonical run or probe, update `docs/current/status/TRAINING_RUN_HISTORY.md` before closeout.

## Procedure

1. Run `git diff --check`.
2. Inspect `git status --short --branch`.
3. Review the pending diff and confirm only intended files are included.
4. Stage the intended files.
5. Create one logical commit for the completed phase work.
6. Push the commit to `origin/main`.
7. Record the commit hash, push result, and validation outcome in the phase closeout note or journal.

## Closeout Expectations

- Final git status should be reported.
- Boundary confirmations should state what was not changed.
- The phase closeout should remain concise and factual.
