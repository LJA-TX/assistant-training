# Publication Readiness Audit

Repository: `assistant-training`
Date: 2026-06-09

## Verdict

Not ready for public release.

The repo is clean on `main`, and a targeted secret-prefix scan did not find obvious credential strings, but the release surface still has structural gaps and multiple public-safety issues:

- required release entrypoints and boundary files are missing
- tracked manifests, configs, and reports contain machine-local absolute paths and loopback URLs
- `.gitignore` does not exclude several runtime-output surfaces that are currently tracked
- `LICENSE` and `SECURITY.md` are missing

## Method

Checks performed:

- `git status --short --branch`
- root inventory and top-level file presence checks
- targeted secret-pattern scan for credential prefixes and private key markers
- local-path and loopback scan for `/opt/ai-stack`, `/home/roy`, `localhost`, and `127.0.0.1`
- ignore-policy verification with `git check-ignore -v`
- review of `README.md`, `.gitignore`, `docs/repo_layout.md`, `data/README.md`, and representative config/manifest files

## Findings

| ID | Severity | Finding | Evidence | Recommended action | Blocking |
|---|---|---|---|---|---|
| F1 | High | `LICENSE` is missing from the repository root. Public release terms are undefined. | Root inventory shows `LICENSE` is absent. | Add a root `LICENSE` with an explicit SPDX-compatible license and confirm provenance. | Yes |
| F2 | Medium | `SECURITY.md` is missing. | Root inventory shows `SECURITY.md` is absent. | Add a public security disclosure policy and contact path. | No |
| F3 | High | The repo does not match the requested monolith release shape. Required root surfaces are absent: `serve.sh`, `config.toml`, `prompts.toml`, `server/`, and `model/`. | Root inventory shows all of these paths are absent. | Add a minimal public-facing launcher/config boundary or narrow the public release scope to a repo that already has this shape. | Yes |
| F4 | High | Tracked release-facing files contain machine-local absolute paths and loopback URLs. | `data/README (data-intake).md:5-9`; `manifests/runs/lora_probe_llama_3_2_3b_instruct_toolcall_v0_2.run_manifest.json:9-29`; `manifests/runs/stage_b_llama31_8b_base_v1_i9.run_manifest.draft.json:9-17`; `configs/lora/stage_b_llama31_8b_base_v1_geometry_probe_lh.config.json:9-154`; `manifests/reports/stage_b_v1_i10r_microprobe_comparison_rows_raw.snapshot.jsonl:187-194`; `evals/data/canonical_v1/tool_holdout.jsonl`; `evals/data/canonical_v1/heldout_validation.jsonl` | Replace machine-local paths with relative paths or environment placeholders in the public tree, or move the raw/internal variants outside the public release set. | Yes |
| F5 | High | `.gitignore` does not exclude several runtime-output surfaces that are present in the tree and tracked. | `.gitignore:17-29` ignores `artifacts/`, caches, logs, `evals/runs/`, and `local_review_bundles/`, but not `reports/`, `manifests/reports/`, `manifests/runs/`, or `staging/`. Tracked files exist under `reports/`, `manifests/reports/`, and `manifests/runs/`. | Add ignore rules for runtime outputs, then decide which tracked outputs are curated public evidence versus internal-only/generated artifacts. | Yes |

## Clean Findings

- No high-confidence secret, token, credential, or private-key prefixes were found in the targeted regex scan.
- `artifacts/` and `local_review_bundles/` are already ignored, which is correct for local-only weights and review bundles.
- `README.md` is present and does not show an obvious secret leak in the reviewed sections.

## Proposed Patch Plan

Keep the cleanup minimal and commit-separated:

1. Add release metadata only.
   - Add `LICENSE`.
   - Add `SECURITY.md`.
   - Keep content changes to documentation only.

2. Add a public-safe boundary skeleton.
   - Add `serve.sh`.
   - Add root config entrypoints or examples (`config.toml`, `prompts.toml`, or `*.example` variants).
   - Add `server/` and `model/` boundary placeholders if this repo is the intended monolith release target.
   - Do not change runtime behavior in this commit.

3. Sanitize machine-local references.
   - Replace absolute paths in public configs/manifests/docs with relative paths or environment variables.
   - Convert raw/internal manifests and report snapshots to redacted or example forms if they must remain visible.

4. Tighten ignore policy and output boundaries.
   - Add ignore rules for `reports/`, `manifests/reports/`, `manifests/runs/`, `staging/`, and other runtime-output paths that should not be tracked.
   - Keep the existing `artifacts/` and `local_review_bundles/` ignores.
   - If curated report files must remain tracked, split them into explicit public-safe allowlists.

5. Re-run the publication audit after the above changes.
   - Confirm no machine-local path matches remain in the public tree.
   - Confirm runtime outputs are either ignored or intentionally curated.
   - Confirm the release tree matches the intended public monolith layout.

## Notes

- This audit intentionally did not make cleanup edits.
- The repo is clean in git, so the current issues are structural and content-based rather than staging-related.
