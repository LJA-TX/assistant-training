# Published Baselines

This page is the front door for the curated Llama 3.1 baseline evidence package.

Start here:

1. [LLAMA31_PROJECT_WIDE_COMPARISON.md](LLAMA31_PROJECT_WIDE_COMPARISON.md)
2. [../../../evals/baselines/llama31/README.md](../../../evals/baselines/llama31/README.md)
3. [../../../evals/baselines/llama31/canonical_baseline_index.json](../../../evals/baselines/llama31/canonical_baseline_index.json)
4. [../../../evals/baselines/llama31/project_wide_comparison_table.json](../../../evals/baselines/llama31/project_wide_comparison_table.json)

## What Is Published Here

- canonical baselines for `Llama-3.1-8B-Base`, `Llama-3.1-8B-Instruct`, and `Llama-3.1-8B-Instruct-NVFP4`
- internal reference regimes for H1 and H2, published because they are the strongest observed capability regimes in the repository
- machine-readable evidence bundles copied verbatim from executed repository artifacts
- human-readable comparison surfaces that distinguish baseline reference points from report-only internal regimes

## Canonical Vs Internal

- `canonical_baselines/` contains published reference points for the frozen canonical evaluation contract.
- `internal_reference_regimes/` contains H1 and H2 as scientific comparison regimes.

H1 and H2 are not deployment recommendations. They are published because the repository's main scientific claims about capability emergence and failure tradeoffs depend on them.

## Current Reading

- Base, Instruct, and NVFP4 all sit at the exact-call floor on the frozen contract.
- H1 and H2 are the only clear high-capability regimes in the repository.
- H1 and H2 both remain non-promotional because they regress safety surfaces even while materially improving tool-call realization.

## Evidence Policy

- Published benchmark artifacts are preserved verbatim.
- Environment-specific literals in those artifacts are documented, not redacted.
- Curated package metadata and comparison surfaces are repo-relative and explanatory.

