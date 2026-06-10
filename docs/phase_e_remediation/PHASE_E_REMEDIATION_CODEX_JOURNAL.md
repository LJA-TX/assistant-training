# Phase E Remediation Codex Journal

Purpose: record progress on the bounded evaluator-contract drift investigation and remediation assessment.

## 2026-06-10

- Received the Phase E remediation package and confirmed the scope is limited to evaluator-contract drift.
- Verified the live evaluator hash from `scripts/eval_canonical_manifest.py` is `08a5cec22a781193365bed85b709ceebef534846602004bbfa047f4e0b59d738`.
- Verified the canonical manifest still pins `80af75c494e0da59f30f33a910997b5fdff15d4ffa8dca09988cdedc0fc06e3f`.
- Traced the evaluator hash lineage across the relevant commits: `7b694fb`, `9124324`, `19f126d`, `d82e0f0`, `97491ef`, and `325bdb4`.
- Confirmed the manifest pin predates a sequence of intentional evaluator updates, with `325bdb4` producing the current hash.
- Rechecked the fresh Phase E revalidations.
- Found the base revalidation reproduces the old run at the classification level.
- Found the adapter revalidation shifts four `heldout_validation` rows between `invalid_json` and `invalid_schema`, but the aggregate Phase E gate conclusions do not change.
- Confirmed the core canonical scoring functions did not change between the manifest-pinned script and the current evaluator; the drift is in supporting evidence and prompt-trace plumbing.
- Started the remediation documentation bundle under `docs/phase_e_remediation/`.
- Drafted the full assessment bundle and validated it with `git diff --check`.
- Confirmed the only remaining untracked files outside this bundle are the user-supplied work-package prompts.

## Current Focus

- Finish the assessment documents and capture the smallest correct remediation.

## Open Items

- Commit and push the documentation bundle if the tree is clean.
