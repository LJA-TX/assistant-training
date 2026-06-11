# Dataset V1.2 Design Options

## Evaluation Frame

The design must satisfy two goals at once:

1. recover H1/H2 tool-call capability, and
2. keep the Phase L safety gains.

The evidence says the right answer is not a single lever.
It is a combined design that restores tool-call repetition without removing the explicit no-call calibration that worked.

## Options

| Option | Expected advantages | Expected risks | Likely failure mode | Evidence basis |
|---|---|---|---|---|
| Anchor-weighted design | Best chance to recover exact-validity, schema adherence, and tool-call realization. | Can overfit anchor prompts and ignore the long tail; if overdone, may reintroduce safety regressions. | H2-like capability with a return of refusal leakage or wrapper leakage. | H1/H2 both show strong performance on repeated anchor tools such as `rg_search`, `read_file`, `find_files`, and `debug_tools`. |
| Density-restoration design | Raises the tool-call signal floor while keeping a broad tool set. | If the family distribution stays flat, the model may still underfit canonical envelopes. | Partial recovery only; safety remains clean but capability stays below H1/H2. | Phase L reduced tool-positive density from `65%` to `60%`. |
| Hybrid design | Best combined-bottleneck candidate. Preserves breadth, restores density, and reintroduces anchor repetition. | More complex to specify and validate. | If the anchor weights are too weak, it behaves like density-restoration; if too strong, it behaves like H2. | H1/H2 split the metric families; Phase L failed by flattening the tool core. |
| Curriculum-style design | Could help the model learn canonical tool-call behavior before safety calibration if the training stack honors the schedule. | In this repo the trainer uses random sampling by default, so a pure order curriculum is weak unless sampling/weighting is adjusted. | The curriculum effect is washed out by shuffling or insufficient exposure. | `scripts/train_lora_sft.py` uses a sampler path that is random/weighted-random rather than order-aware. |

## Option Notes

### Anchor-Weighted Design

Use this if the main concern is exact-validity recovery.

Recommended shape:

- a repeated anchor core,
- moderate long-tail support,
- all 26 tools preserved,
- safety rows kept explicit.

This is the best way to recover the `rg_search` / `read_file` / `find_files` style canonical envelope learning.

### Density-Restoration Design

Use this if the main concern is that the model simply did not see enough tool-positive examples.

Recommended shape:

- restore tool-positive density toward the H1/H2 level,
- avoid flattening the tool families further,
- keep the safety rows explicit.

This is the smallest change, but it is also the least likely to fully recover the H1/H2 capability surface by itself.

### Hybrid Design

Use this if the goal is the highest-probability combined fix.

Recommended shape:

- restore some tool-positive density,
- restore anchor concentration,
- preserve the breadth restored in v1.1,
- keep the Phase L safety block intact.

This is the most evidence-consistent option.

### Curriculum-Style Design

Use this only if the training pipeline can actually honor staged exposure.

If the sampler shuffles, pure curriculum order is mostly symbolic.
If the sampler is weighted or staged, a curriculum can help the model learn tool-call structure before the safety block exerts its full influence.

## Ranking

1. Hybrid design.
2. Anchor-weighted design.
3. Density-restoration design.
4. Curriculum-style design.

The ranking is evidence-based, not proof-based.
It reflects the smallest design set that stays consistent with both the Phase L safety result and the H1/H2 capability result.

## Sources Used

- `docs/phase_m/FAILURE_CHARACTERIZATION.md`
- `docs/phase_m/JSON_AND_SCHEMA_FAILURE_ANALYSIS.md`
- `docs/phase_m/ROOT_CAUSE_ASSESSMENT.md`
- `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json`
- `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json`
- `data/v1_1/dataset_v1_1_summary.json`
- `scripts/train_lora_sft.py`
