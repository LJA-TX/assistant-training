# Navigation And Discovery Assessment

## Scope

Assess whether the repository needs additional navigation surfaces because searchability is unreliable.
Prefer concise, high-value index artifacts over broad catalog generation.

## Inputs

- [docs/current/start_here.md](../current/start_here.md)
- [docs/current/current_status.md](../current/current_status.md)
- [docs/current/framework_vs_history.md](../current/framework_vs_history.md)
- [docs/framework/lineages/README.md](../framework/lineages/README.md)
- [docs/continuity/STAGE_C_CLOSURE_CONTINUITY_PACKAGE.md](../continuity/STAGE_C_CLOSURE_CONTINUITY_PACKAGE.md)
- [docs/continuity/post-publication_transition_return_to_stage_c_continuity_2026-06-09.md](../continuity/post-publication_transition_return_to_stage_c_continuity_2026-06-09.md)
- [scripts/repo_paths.py](../../scripts/repo_paths.py)
- [scripts/eval_canonical_manifest.py](../../scripts/eval_canonical_manifest.py)
- [tests/test_repo_paths.py](../../tests/test_repo_paths.py)
- [docs/phase_d/README.md](README.md)

## Current Navigation Surfaces

- `docs/current/start_here.md` is still the fastest front door into the curated package.
- `docs/current/current_status.md` is the current-state summary.
- `docs/current/framework_vs_history.md` cleanly separates reusable framework from curated history.
- `docs/framework/lineages/README.md` provides the bounded evidence spine.
- `docs/continuity/STAGE_C_CLOSURE_CONTINUITY_PACKAGE.md` preserves the Stage C closure handoff.
- `scripts/repo_paths.py` now gives the repo an explicit role registry for script and artifact discovery, including the E1 prompt-trace creator.

## Discovery Problem

GitHub search is not a reliable way to navigate this repository because there are many similarly named convergence, continuity, research, and report files.
That makes a compact index more useful than a broad search strategy.

## Assessment

- The repository already has the right kind of front-door docs.
- The missing piece is a bounded phase-local index for the current work package.
- A large generated catalog would add noise instead of value.
- The new role registry in `scripts/repo_paths.py` improves code-side discovery, but it does not replace human-readable navigation.

## Recommended Supporting Index Artifact

- Keep `docs/phase_d/README.md` as the only new navigation surface needed for this phase.

Why this is enough:

- It is small.
- It points to all Phase D deliverables.
- It keeps the journal discoverable.
- It avoids creating another broad taxonomy.

## Determination

A single bounded Phase D index is justified and sufficient.
No broad catalog generation is warranted.
No additional navigation tree is needed at this time.

## Boundary Confirmation

This assessment does not change repo taxonomy, authority order, or release policy.
