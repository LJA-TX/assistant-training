# Llama 3.1 Project-Wide Comparison

This table is the canonical first-screen comparison for the curated Llama 3.1 evidence package.

## Comparison Table

| Regime | Class | Exact JSON | Invalid JSON | Tool-name | Arg | Wrapper leakage | No-call | Adversarial no-call | Reading |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Base | Canonical baseline | `0.0` | `0.7` | `0.0` | `0.0` | `0.0` | `1.0` | `1.0` | Authoritative Base revalidation; non-tool baseline with intact no-call behavior. |
| Instruct | Canonical baseline | `0.0` | `0.69` | `0.0` | `0.0` | `0.0` | `1.0` | `1.0` | Direct-load external reference baseline at the frozen-contract floor. |
| NVFP4 | Canonical baseline | `0.0` | `0.695` | `0.0` | `0.0` | `0.0` | `1.0` | `1.0` | Service-backed external reference baseline that matches Instruct on aggregate behavior. |
| H1 | Internal reference regime | `0.44` | `0.1` | `0.7142857142857143` | `0.6285714285714286` | `0.0` | `0.9` | `0.7` | Diversity-lift regime with real capability signal and safety regression. |
| H2 | Internal reference regime | `0.48` | `0.085` | `0.7714285714285715` | `0.6928571428571428` | `0.005` | `0.8` | `0.4` | Strongest exact-call regime in the repo; still non-promotional because safety regresses more sharply. |

## Bundle Roles

- Base, Instruct, and NVFP4 are published under `canonical_baselines/`.
- H1 and H2 are published under `internal_reference_regimes/`.

That distinction is intentional:

- canonical baselines are public reference points for the frozen contract
- internal reference regimes are report-only scientific comparators

## Interpretation

- Base, Instruct, and NVFP4 all confirm the same baseline reality: no-call behavior is preserved, but exact tool-call realization is absent.
- H1 and H2 remain the only strong capability regimes in the repository.
- H1 and H2 split the metric families rather than producing a single clean, safety-preserving winner.

## Supporting Surfaces

- Package root: [../../../evals/baselines/llama31/README.md](../../../evals/baselines/llama31/README.md)
- Machine-readable index: [../../../evals/baselines/llama31/canonical_baseline_index.json](../../../evals/baselines/llama31/canonical_baseline_index.json)
- Machine-readable comparison table: [../../../evals/baselines/llama31/project_wide_comparison_table.json](../../../evals/baselines/llama31/project_wide_comparison_table.json)
- H1 checkpoint: [../../phase_ix/H1_EXCEPTION_CHECKPOINT_REPORT.md](../../phase_ix/H1_EXCEPTION_CHECKPOINT_REPORT.md)
- H1 interpretation: [../../phase_ix/H1_EXCEPTION_SCIENTIFIC_INTERPRETATION.md](../../phase_ix/H1_EXCEPTION_SCIENTIFIC_INTERPRETATION.md)
- H2 checkpoint: [../../phase_i/H2_CHECKPOINT_REPORT.md](../../phase_i/H2_CHECKPOINT_REPORT.md)

