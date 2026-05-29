# Stage B v1 Objective-Interaction / Exposure-Geometry Mapping Design

## Mode
Design-only, read-only planning phase.
No training, no eval reruns, no dataset mutation, no trainer-code edits.

## Scientific Status
Geometry mapping is scientifically justified now.

Evidence from completed probes:
- `i10r_microprobe`: no-call aggregate `0.9167`, adversarial `0.75`, read_file exact-valid `0.7037`.
- `i10r_nocall_probe`: no-call aggregate/adversarial restored to `1.0/1.0`, but read_file exact-valid collapsed to `0.2593` and read_file symbol-name exact-valid to `0.0`.
- `i10r_counterbalanced_probe`: read_file exact-valid restored (`0.7037`, symbol-name `0.9231`), but no-call remained sub-ceiling (`0.9667` aggregate, `0.9` adversarial).
- `i10r_residual_nocall_probe`: no-call returned to `1.0/1.0`, read_file collapsed again (`0.2593`, symbol-name `0.2308`).

Interpretation: this is calibration coupling / objective interaction, not ordinary data insufficiency.

## Primary Question
Estimate the minimum no-call adversarial exposure that yields `no_call_correctness == 1.0`, and the read_file symbol-name counterweight needed to avoid read_file collapse.

## Sweep Variables
Candidate independent variables:
1. `no_call_adversarial_family_exposure` (primary pressure axis).
2. `read_file_symbol_name_exposure` (primary counterweight axis).
3. `valid_rg_search_contrastive_exposure` (stabilizer axis; keeps refusal pressure paired with valid-commitment pressure).
4. `uncertainty_conditioning_exposure` (default `0`; include only with explicit justification).

Dependent variables:
- `read_file_exact_valid` and `read_file_symbol_name_exact_valid` are measured outcomes during mapping (not immediate hard-stop gates unless catastrophic collapse).

## Conceptual Grid
Full conceptual grid:
- No-call pressure: `low / medium / high`
- Read_file counterweight: `low / medium / high`

## Smallest Useful Sweep (Recommended First Pass)
Five-point bracketed sweep (instead of full 3x3) to localize the threshold with minimal confounding:
1. `L/H`: low no-call, high read_file.
2. `M/H`: medium no-call, high read_file.
3. `H/H`: high no-call, high read_file.
4. `H/M`: high no-call, medium read_file.
5. `H/L`: high no-call, low read_file.

Rationale:
- Prior evidence already brackets likely no-call threshold between current "counterbalanced-like" and "nocall-like" regimes.
- This 5-point path isolates the threshold then immediately tests counterweight sufficiency at the high-pressure edge.

## Exposure-Level Definitions (Design Targets)
Relative to current i10r-localized intervention footprint:
- No-call pressure:
  - `low`: 10 contrastive no-call rows equivalent.
  - `medium`: 13 contrastive no-call rows equivalent.
  - `high`: 16 contrastive no-call rows equivalent.
- Read_file counterweight:
  - `low`: 0 symbol-name counterweight rows.
  - `medium`: 6 rows.
  - `high`: 10 rows.
- Valid rg_search contrastive:
  - Maintain malformed:valid contrastive pairing at `1:1` for each no-call unit.
- Uncertainty conditioning:
  - `0` by default in Stage B v1 geometry mapping.

## Weighting/Composition Methods
Method suitability for this phase:
- Sampler weighting: preferred long-term for clean geometry control.
- Row duplication: acceptable temporary approximation if tightly capped and explicitly audited.
- Curriculum staging: acceptable secondary lever after first threshold mapping.
- Loss weighting: defer (higher interpretability and implementation risk).
- Dataset composition variants: acceptable now and currently most operationally compatible.

## Missing Instrumentation
Currently missing for auditable geometry mapping:
1. Run-level effective exposure ledger by family/archetype/axis.
2. Declared-vs-realized exposure accounting per epoch.
3. Cell ID + axis-level metadata propagation from dataset row -> training summary.
4. Automatic extraction of Pareto metric bundle in one artifact per run.
5. Catastrophic-collapse detector for dependent-variable handling (read_file collapse policy).

## Required Trainer/Instrumentation Changes (Design Only)
Trainer capabilities absent today:
- Native weighted sampler path.
- Sample-weight ingestion and logging.
- Per-step/per-epoch family exposure counters.

Minimum design changes (next executable phase, no training yet):
1. Add optional deterministic weighted sampler path.
2. Add optional `geometry_weight` ingestion from row metadata or sidecar manifest.
3. Emit `effective_exposure_by_axis` + `effective_exposure_by_family` artifacts.
4. Emit sweep cell metadata (`cell_id`, axis levels, intended multipliers).

## Safest First Implementation Path
1. Implement instrumentation first (no run).
2. If sampler weighting is not yet implemented, run the smallest sweep using declared dataset-composition variants (or capped row duplication) with strict exposure audit artifacts.
3. Prefer sampler weighting once instrumentation is in place, then re-run the same sweep topology for cleaner attribution.

## Pareto Frontier Definition
A candidate point is Pareto-improving if it increases no-call integrity without regressing other protected metrics beyond tolerance.

Target metrics for frontier tracking:
- `no_call aggregate/adversarial`
- `read_file exact-valid`
- `read_file_symbol_name exact-valid`
- `scalar substitution`
- `direct-answer substitution`
- `no-anchor exact-valid`
- `wrapper leakage`
- `exact-valid overall`
- `invalid_json overall`

Stable Pareto improvement (recommended criterion):
- `no_call_correctness` aggregate and adversarial both `== 1.0`
- `read_file_exact_valid >= 0.65`
- `read_file_symbol_name_exact_valid >= 0.70`
- `wrapper_leakage == 0.0`
- `scalar_substitution_share <= 0.05`
- `direct_answer_substitution_share <= baseline_i10r + 0.05`
- `exact_valid_overall >= 0.435`
- `invalid_json_overall <= 0.13`
- And reproducible in at least one neighboring sweep cell or repeat seed.

## Hard Invariants vs Tradeoff Variables
Remain hard invariants:
- No wrapper leakage (`== 0`).
- No contamination overlap with heldout/tool_holdout.
- Canonical eval topology unchanged.
- No unauthorized uncertainty-conditioning additions.
- No catastrophic parse collapse (`invalid_json_overall > 0.30` is catastrophic halt).

Measured tradeoff variables during mapping:
- `no_call_correctness` (aggregate + adversarial).
- `read_file_exact_valid`.
- `read_file_symbol_name_exact_valid`.
- `direct_answer_substitution_share`.
- `no_anchor_exact_valid_share`.
- `exact_valid_overall`.

## Explicit Answers
1. Is geometry mapping scientifically justified now?
- Yes.

2. What is the smallest useful sweep?
- Five-point bracketed sweep: `L/H`, `M/H`, `H/H`, `H/M`, `H/L`.

3. What instrumentation is missing?
- Effective exposure ledger, declared-vs-realized exposure accounting, cell-level metadata propagation, automatic Pareto bundle artifact, and catastrophic-collapse detector.

4. Should we implement sampler/loss weighting before another run?
- Implement sampler weighting instrumentation before another run if feasible; defer loss weighting.

5. Is row-duplication acceptable as temporary approximation, or too confounded?
- Acceptable only as temporary approximation with strict caps, pair-preservation, and explicit exposure accounting; otherwise too confounded.

6. What would constitute a stable Pareto improvement?
- `no_call_correctness == 1.0` (aggregate+adversarial) while preserving read_file floors and zero wrapper leakage, with overall exact-valid/invalid-json within specified bounds and repeatability.

7. What should remain hard invariants?
- Wrapper leakage zero, contamination zero, eval topology unchanged, uncertainty-conditioning default zero, catastrophic parse-collapse halt.

8. What should become measured tradeoff variables?
- No-call correctness, read_file exact-valid, read_file symbol-name exact-valid, direct-answer substitution, no-anchor share, overall exact-valid/invalid-json.

9. Recommended next executable phase after this design?
- Instrumentation implementation-only phase: add auditable exposure-weighting plumbing and sweep-manifest/reporting support, with no training execution in that phase.
