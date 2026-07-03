# Llama 3.1 Baseline Package

This directory is the curated public evidence package for the repository's Llama 3.1 baseline and reference-regime results.

Use the package in this order:

1. [canonical_baseline_index.json](canonical_baseline_index.json)
2. [project_wide_comparison_table.json](project_wide_comparison_table.json)
3. [../../../docs/current/baselines/README.md](../../../docs/current/baselines/README.md)
4. [../../../docs/current/baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md](../../../docs/current/baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md)

## Layout

- `canonical_baselines/`: authoritative external or raw-model reference bundles
- `internal_reference_regimes/`: strongest observed internal capability regimes published for scientific interpretation, not deployment recommendation

## Bundle Classes

- `canonical_baseline`: published reference point for the frozen canonical evaluation contract
- `internal_reference_regime`: report-only reference regime used to explain the repository's strongest capability signals

H1 and H2 are intentionally published under `internal_reference_regimes/` because both are scientifically central and both remain non-promotional under the repository's own safety and stop-rule framing.

## Naming Legend

- Timestamped or phase-scoped bundle directory names preserve provenance from the executed run naming.
- The stable interpretation surface is the `package_manifest.json` inside each bundle, not the directory name alone.
- `base_revalidation_20260610_r1` is the authoritative published Base baseline.
- `base_original_20260526T0044Z` is preserved as historical provenance.

## Evidence Policy

- Primary benchmark evidence in this package is preserved verbatim from executed repository artifacts.
- Environment-specific literals are intentionally preserved rather than sanitized.
- Newly authored package files such as indexes, manifests, and README surfaces use repo-relative paths and explanatory labels.

## Environment-Specific Literals

Some published benchmark artifacts contain literals such as:

- local filesystem paths under `/mnt/services/...` or `/mnt/mirrors/...`
- loopback URLs such as `http://127.0.0.1:8100/...`

Those literals are part of the executed benchmark evidence or the author runtime environment. They are preserved to keep the published artifacts audit-faithful to the executed runs. They do not change the reported metrics or the comparison conclusions in this package.

## Verification

- Evaluation contract: [../../canonical_eval_manifest_v1.json](../../canonical_eval_manifest_v1.json)
- Evaluator entrypoint: [../../../scripts/eval_canonical_manifest.py](../../../scripts/eval_canonical_manifest.py)
- Current public comparison landing page: [../../../docs/current/baselines/README.md](../../../docs/current/baselines/README.md)

