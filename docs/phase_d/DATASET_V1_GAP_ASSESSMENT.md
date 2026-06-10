# Dataset v1.0 Gap Assessment

## Scope

Compare the repository state against the charter targets for dataset v1.0.
This is an assessment only. It does not acquire new datasets or expand the dataset family set.

## Inputs

- [docs/goal_charter_v5a.md](../goal_charter_v5a.md)
- [docs/appendix_a_operational_execution_contract_v3a.md](../appendix_a_operational_execution_contract_v3a.md)
- [data/v1_0/dataset_v1_0_summary.json](../../data/v1_0/dataset_v1_0_summary.json)
- [data/v1_0/dataset_v1_0_leakage_report.json](../../data/v1_0/dataset_v1_0_leakage_report.json)
- [data/README.md](../../data/README.md)
- [data/README (data-intake).md](<../../data/README (data-intake).md>)

## Known Datasets And Families

- Canonical v1 train and val splits: `data/v1_0/dataset_v1_0_train.jsonl`, `data/v1_0/dataset_v1_0_val.jsonl`
- Stage A splits: `data/v1_0/dataset_v1_0_stage_a_train.jsonl`, `data/v1_0/dataset_v1_0_stage_a_val.jsonl`
- Stage B splits: `data/v1_0/dataset_v1_0_stage_b_train.jsonl`, `data/v1_0/dataset_v1_0_stage_b_val.jsonl`
- Stage B recovery subsets: `dataset_v1_0_stage_b_recovery_i2` through `dataset_v1_0_stage_b_recovery_i10r` variants
- Canonical eval families: `evals/data/canonical_v1/{heldout_validation,tool_holdout,no_call,adversarial,direct_answer}.jsonl`
- Source material referenced by the dataset summary: `data/tool_ft_allaliases_20260525_from_qual_reports*.jsonl` and assistant-runtime report-derived corpora

## Charter Target Comparison

| Target area | Charter target | Current repository state | Gap status |
|---|---|---|---|
| Runtime behavioral alignment | 25% of the balanced mix | Present in canonical v1 at the target proportion, but much of the material is synthetic/template-driven | Met on paper, narrow in provenance |
| Tool-call positives | 45% of the balanced mix | Present at the target proportion in canonical v1; some recovery subsets skew much higher | Met in canonical v1, skewed in recovery subsets |
| No-call / direct-answer behavior | 15% of the balanced mix | Present at the target proportion in canonical v1 | Met, but still narrow in scenario breadth |
| Refusal / policy behavior | 10% of the balanced mix | Present at the target proportion in canonical v1 | Met, but represented by a limited family |
| Adversarial / malformed-request behavior | 5% of the balanced mix | Present at the target proportion in canonical v1 | Met, but diversity is limited |

## Obvious Coverage Deficiencies

- The canonical v1 build does not show evidence of imported external family breadth such as xLAM, APIGen, APIGen-MT, ToolACE, or Glaive in the current manifest chain.
- Runtime behavioral alignment exists, but the v1 summary shows a 0.55 synthetic ratio, which is above the preferred sub-0.50 level.
- No-call and refusal coverage exist, but the families are still compact and template-heavy.
- Adversarial coverage exists at the nominal target rate, but the sample set is small and not obviously diversified.
- Stage B recovery subsets are recovery experiments, not a substitute for broader dataset family coverage.

## Composition Status

- The canonical v1 dataset is compositionally aligned with the charter target mix on paper.
- The gap is not category balance; the gap is provenance diversity and behavioral breadth.
- The biggest practical risk is treating narrow synthetic coverage as if it were full real-world coverage.

## Determination

Dataset v1.0 is sufficient for baseline revalidation and continued controlled work, but it is not yet a broad-diversity dataset family.
The next gap to carry forward is broader coverage, not more category count bookkeeping.

## Boundary Confirmation

This assessment does not authorize new dataset acquisition, dataset expansion, or training changes.
