# Repository Establishment Plan v1

## Scope
Establish `/opt/ai-stack/assistant-training` as a disciplined Git repository focused on reproducibility, governance traceability, and portability to future GitHub mirroring.

## Reconnaissance Summary (read-only)
- Top-level size profile:
  - `artifacts/` ~3.5G (dominant, generated)
  - `data/` ~17M (datasets + summaries)
  - `evals/` ~3.7M (manifest/spec + run dumps)
  - `scripts/` ~644K
  - `docs/` ~248K
  - `manifests/` ~176K
- Major churn/sludge sources:
  - checkpoints/adapters in `artifacts/`
  - repeated eval outputs in `evals/runs/`
  - Python/runtime caches (`__pycache__`, `.pytest_cache`)
- Provenance-critical assets exist in:
  - governance docs (`docs/goal_charter_v5a.md`, `docs/appendix_a_operational_execution_contract_v3a.md`, `docs/metric_specification_v1a.md`)
  - run + report manifests (`manifests/runs/`, `manifests/reports/`, `manifests/environment/`)
  - canonical eval contract (`evals/canonical_eval_manifest_v1.json`)
  - training/eval scripts and configs (`scripts/`, `configs/`)

## Recommended Tracked Directories and Files
- `docs/`
  - Rationale: governance authority, contracts, lineage interpretation, future reproducibility context.
- `manifests/`
  - Rationale: structured provenance (run manifests, gate assessments, intervention declarations, environment snapshots).
- `configs/`
  - Rationale: training reproducibility and run intent.
- `scripts/`
  - Rationale: executable pipeline logic and evaluation procedures.
- `tests/`
  - Rationale: contract/regression safety.
- `evals/canonical_eval_manifest_v1.json`
  - Rationale: canonical evaluation contract.
- `evals/data/canonical_v1/`
  - Rationale: canonical evaluation dataset inputs.
- `data/README.md`, `data/README (data-intake).md`
  - Rationale: data handling documentation.
- `data/v1_0/*summary.json`, `data/v1_0/dataset_v1_0_leakage_report.json`
  - Rationale: compact provenance metadata.
- `data/v1_0/*.jsonl` (current v1.0 lineage sets)
  - Rationale: deterministic reproducibility for completed lineage; current footprint is modest.
- Root project files: `README.md`, `pyproject.toml`, `.gitignore`

## Recommended Ignored Directories and Patterns
- `artifacts/`
  - Rationale: very large generated model outputs/checkpoints; not suitable for standard Git.
- `evals/runs/`
  - Rationale: high-churn run dumps; summaries are already captured in `manifests/reports/`.
- `**/__pycache__/`, `*.pyc`, `.pytest_cache/`
  - Rationale: runtime cache noise.
- virtualenv/environment noise: `.venv/`, `venv/`, `.env`, `.env.*`
  - Rationale: machine-local state.
- model binaries/checkpoints: `*.pt`, `*.bin`, `*.safetensors`
  - Rationale: prevent accidental heavyweight commits.
- temp/log output: `*.log`, `tmp/`, `.cache/`
  - Rationale: non-deterministic transient artifacts.

## Artifact Retention Policy
- Keep generated heavy artifacts outside Git (`artifacts/`, `evals/runs/`).
- Preserve reproducibility via:
  - run manifests
  - canonical eval summaries/gate reports in `manifests/reports/`
  - environment snapshot artifacts in `manifests/environment/`
- If needed for handoff, archive heavy artifacts externally with immutable naming and checksums referenced from manifests.

## Checkpoint Retention Policy
- In-repo: none (ignore all checkpoint/adapters/binaries).
- Out-of-repo retention recommendation:
  - Keep only promotion candidates and immediate predecessor for rollback.
  - Retain full training logs for promoted candidates.
  - Garbage-collect non-promoted checkpoint trees on a fixed cadence.

## Dataset Retention Policy
- Track canonical and lineage-critical v1.0 datasets currently referenced by manifests.
- Future policy:
  - track versioned, release-grade datasets and summaries;
  - ignore scratch/intermediate dataset builds unless promoted to a versioned release path.
- Ensure each tracked dataset revision has matching summary/leakage metadata.

## Proposed Branch Strategy
- `main`: protected source of truth for governance + reproducible pipeline code.
- `exp/<lineage-or-iteration>`: short-lived experimentation branches (e.g., `exp/stage-b-i8`).
- `ops/repo-hygiene-*`: maintenance branches for ignore/structure hygiene updates.
- Merge policy:
  - fast-forward or squash allowed;
  - require artifact/report presence for experiment merges into `main`.

## Proposed Commit Hygiene Rules
- One intent per commit group (docs, manifests, scripts, configs, dataset metadata).
- No generated binaries/checkpoints/eval run dumps in commits.
- Commit message convention:
  - `docs: ...`
  - `manifests: ...`
  - `scripts: ...`
  - `configs: ...`
  - `data: ...`
- Include provenance references in commit body when touching lineage outputs (run id / manifest path).

## Future GitHub Mirroring Considerations
- Keep repository free of large generated files to avoid GitHub limits and clone bloat.
- If binary model assets must be mirrored later, use an external artifact store or Git LFS with explicit policy.
- Maintain stable relative paths for manifests/scripts/configs to support orchestrator portability.
- Add mirror-safe metadata only (checksums/URIs) instead of embedding bulky run outputs.

## Initial Establishment Sequencing
1. Finalize `.gitignore` to block known sludge classes.
2. Initialize Git repository.
3. Inspect `git status` and classify tracked/untracked inventory.
4. Stage-only proposal by logical commit groups (no commit execution yet).
