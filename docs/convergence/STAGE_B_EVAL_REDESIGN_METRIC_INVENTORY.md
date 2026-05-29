# Stage B Evaluation Redesign Metric Inventory

## Scope

This is a bounded, read-only reconnaissance inventory for the four Stage B metrics that remained noncomputable after schema convergence:

- `direct_answer_substitution_count`
- `no_anchor_exact_valid_share`
- `read_file_exact_valid_rate`
- `read_file_symbol_name_exact_valid_rate`

Schema convergence is treated as closed. This document does not modify schemas, detectors, thresholds, or metric mappings, and does not propose proxy or inferred mappings.

## Evidence Summary

Current threshold definitions live in `manifests/reports/stage_b_v1_threshold_profile.json`:

- `direct_answer_substitution_count` maps to `failure_profile.failure_categories_non_exact_tool_rows.direct_answer_substitution`.
- `no_anchor_exact_valid_share` maps to `failure_profile.anchor_exact_share.no_anchor_phrase`.
- `read_file_exact_valid_rate` maps to `failure_profile.read_file_exact_valid.rate`.
- `read_file_symbol_name_exact_valid_rate` maps to `failure_profile.read_file_symbol_name_exact_valid.rate`.

The detector in `scripts/post_eval_collapse_detector.py` is profile-driven. It resolves every metric referenced by threshold rules from `metric_catalog`; unresolved required metrics become noncomputable and, under the current profile, force `halt_progression`.

The current live evaluator, `scripts/eval_canonical_manifest.py`, emits `base`, `adapter`, `per_split`, `aggregate`, and `delta_adapter_minus_base` summaries. It emits aggregate class counts, exact JSON validity, invalid JSON rate, tool-name accuracy, argument accuracy, wrapper leakage, no-call correctness, and tool-expected row counts. It does not emit `failure_profile`, per-tool exact-valid rates, prompt-anchor buckets, symbol-name archetype slices, or direct-answer substitution subtypes.

Historical `failure_profile` data appears in report-layer canonical eval summaries such as:

- `manifests/reports/stage_b_v1_i10r_microprobe_canonical_eval_summary.json`
- `manifests/reports/stage_b_v1_i10r_nocall_probe_canonical_eval_summary.json`
- `manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`
- `manifests/reports/stage_b_v1_i10r_residual_nocall_probe_canonical_eval_summary.json`

No tracked current producer script was found that emits the `failure_profile` object into the live canonical eval summary. Related analysis and dataset-builder code can infer or carry nearby concepts, but doing so for detector mapping would violate the No Proxy Doctrine.

## Current Live-Schema Related Observations

Related live fields exist, but none is a one-to-one equivalent for the four metrics:

- `adapter.aggregate.class_counts.*`
- `adapter.aggregate.exact_json_validity.rate`
- `adapter.aggregate.invalid_json_rate`
- `adapter.aggregate.wrapper_leakage_rate`
- `adapter.aggregate.no_call_correctness.rate`
- `adapter.per_split.tool_holdout.exact_json_validity.rate`
- `adapter.per_split.direct_answer.no_call_correctness.rate`
- `comparison_rows.jsonl` row-level `source_case_id`, `user_prompt`, expected tool fields, generated text, primary class, schema reason, and exact-valid boolean

The `comparison_rows.jsonl` fields are sufficient to support future explicit redesign work, but only if a future evaluator intentionally emits approved first-class metrics. Filtering rows, parsing prompts, or deriving subtype labels from generated text during convergence would be reconstruction, not a safe mapping.

## Metric Inventory

### `direct_answer_substitution_count`

#### Original Purpose

Detect material rebound in tool-expected rows where the model substitutes a direct answer, scalar answer, or result-like prose for the required procedural tool call. The governance concern is false progress: a model can appear helpful while bypassing evidence-gathering behavior.

#### Historical Producer

The metric is present in historical `failure_profile.failure_categories_non_exact_tool_rows.direct_answer_substitution` report fields. Examples:

- `stage_b_v1_i10r_microprobe_canonical_eval_summary.json`: value `12`
- `stage_b_v1_i10r_nocall_probe_canonical_eval_summary.json`: value `29`
- `stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`: value `11`
- `stage_b_v1_i10r_residual_nocall_probe_canonical_eval_summary.json`: value `8`

Related producer logic exists in pre-eval and dataset-builder analysis code. `scripts/build_stage_b_recovery_i10_dataset.py` classifies some `payload_not_parsed` outputs as `direct_answer_substitution`, and `scripts/i10_diagnostics_scaffold.py` emits a `direct_answer_substitution_proxy` for intervention rows. These are related historical analysis surfaces, not current live eval summary producers.

No tracked current script was found that emits this exact `failure_profile` field into `scripts/eval_canonical_manifest.py` output.

#### Historical Consumer

The active threshold profile consumes this metric through tradeoff watch rule `direct_answer_substitution_delta_gt_3`, with `basis: delta_vs_baseline`. The first live probe design also lists `direct_answer_substitution_count` as a required monitored decision metric.

Dataset builders consume related shares as anti-regression context, for example `direct_answer_substitution_share` in `build_stage_b_recovery_i10r_nocall_dataset.py`, `build_stage_b_recovery_i10r_counterbalanced_dataset.py`, and `build_stage_b_recovery_i10r_residual_nocall_dataset.py`.

#### Current Status

Redesign required. The current live summary has direct-answer split no-call correctness and class counts, but these measure correct no-tool behavior on no-call rows. They do not count direct-answer substitution on tool-expected rows.

The row-level comparison output contains generated text and schema reasons that could support future subtype classification. That would require an explicit evaluator redesign, not a mapping update.

#### Governance Impact

Removing this metric entirely would blind governance to a known failure mode where the model answers the user's requested result instead of issuing the required retrieval or search call. Existing no-call correctness metrics do not cover this failure mode. Removal would make direct result substitution easier to hide under aggregate exact-valid or invalid-json changes.

#### Redesign Considerations

- Decide whether the governed object should be a raw count, a rate over tool-expected non-exact rows, or both. The current delta threshold assumes comparable row counts and stable subtype taxonomy across baseline and eval.
- Emit an explicit failure subtype for tool-expected rows from the evaluator rather than deriving it post hoc from prose.
- Consider merging with a broader explicit substitution taxonomy, while preserving direct-answer substitution as a subtype if it remains decision-relevant.
- Keep baseline comparability explicit: a count-based delta requires fixed eval topology or a denominator-aware rule.

Hidden assumptions in the original implementation:

- `failure_profile` exists in every eval summary consumed by the detector.
- Generated-text subtype classification is stable enough to compare across runs.
- A raw count delta is meaningful because the underlying eval row set and denominator are stable.
- Direct-answer substitution is distinct from scalar substitution and wrapper/envelope drift in a repeatable way.

#### Preliminary Recommendation

Still required in concept, redesign required in implementation. Do not map it to direct-answer split no-call correctness. Redesign as an explicit evaluator-emitted tool-expected substitution subtype, preferably with both count and denominator/rate available for governance review.

### `no_anchor_exact_valid_share`

#### Original Purpose

Measure whether exact-valid behavior generalizes beyond prompts that contain overt schema/tool-call anchors. The governance concern is anchor dependence: a model may improve only when prompts include literal or paraphrastic tool-call cues, rather than learning robust procedural commitment.

#### Historical Producer

The metric is present in historical `failure_profile.anchor_exact_share.no_anchor_phrase` fields. Examples:

- `stage_b_v1_i10r_microprobe_canonical_eval_summary.json`: `0.862069`
- `stage_b_v1_i10r_nocall_probe_canonical_eval_summary.json`: `0.8513513513513513`
- `stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`: `0.8369565217391305`
- `stage_b_v1_i10r_residual_nocall_probe_canonical_eval_summary.json`: `0.8148148148148148`

Related anchor-bucket logic exists in `scripts/i9_diagnostics_scaffold.py`, `scripts/i10_diagnostics_scaffold.py`, and dataset builders through `_prompt_anchor_bucket`, which classifies prompt text into buckets such as `literal_tool_calls`, `paraphrastic_tool_call`, `schema_paraphrase`, and `no_anchor_phrase`.

No tracked current live evaluator producer emits anchor buckets or anchor-conditioned exact-valid shares.

#### Historical Consumer

The active threshold profile consumes this metric through tradeoff watch rule `no_anchor_exact_valid_share_lt_0_75`.

The first live probe design lists `no_anchor_exact_valid_share` as a required monitored decision metric. Dataset builders also consume related `no_anchor_exact_share` context in anti-regression reports.

#### Current Status

Redesign required. The current live summary has no anchor taxonomy and no anchor-conditioned exact-valid fields. Prompt text exists in `comparison_rows.jsonl`, but classifying prompt anchors from text would reconstruct a missing metric.

#### Governance Impact

Removing this metric entirely would blind governance to anchor overfitting and cue dependence. A future run could improve exact-valid output by relying on literal `tool_calls` phrasing while failing less explicit prompts, and aggregate exact-valid metrics would not isolate that failure.

#### Redesign Considerations

- Decide whether anchor bucket is an eval-dataset annotation, a scorer-derived first-class label, or a dataset-builder provenance field carried into eval rows.
- Preserve denominator semantics: the historical name says "share", but it is only meaningful if the denominator is explicitly defined as exact-valid rows, tool-expected rows, or anchor-bucket rows.
- Consider moving this into an explicit prompt-generalization or anchor-dependence metric family rather than keeping it as an isolated top-level metric.
- Do not infer anchor buckets from prompt text inside the detector.

Hidden assumptions in the original implementation:

- Prompt-anchor taxonomy is stable and reproducible.
- The string-based bucket logic is acceptable as governance evidence.
- Exact-valid rows and anchor buckets have compatible denominators.
- The absence of anchor phrasing in a prompt is equivalent to procedural generalization.

#### Preliminary Recommendation

Potentially mergeable into a redesigned anchor-generalization metric family. Do not retire without an approved replacement, because the governance concern remains valid. If retained, future evals should emit anchor bucket and anchor-conditioned success fields explicitly.

### `read_file_exact_valid_rate`

#### Original Purpose

Protect `read_file` procedural commitment as a dependent variable during no-call and geometry interventions. The governance concern is that no-call improvements or broad schema behavior can mask collapse in evidence-gathering file-read behavior.

#### Historical Producer

The metric is present in historical `failure_profile.read_file_exact_valid.rate` fields. Examples:

- `stage_b_v1_i10r_microprobe_canonical_eval_summary.json`: `0.703704`
- `stage_b_v1_i10r_nocall_probe_canonical_eval_summary.json`: `0.25925925925925924`
- `stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`: `0.7037037037037037`
- `stage_b_v1_i10r_residual_nocall_probe_canonical_eval_summary.json`: `0.25925925925925924`

The same concept appears in preservation and emergence reports, for example `stage_b_v1_i10r_microprobe_read_file_emergence_analysis.json` and `stage_b_v1_i10r_counterbalanced_probe_read_file_symbol_name_preservation_assessment.json`.

No tracked current live evaluator producer emits per-tool exact-valid rates.

#### Historical Consumer

The active threshold profile consumes this metric through:

- catastrophic rule `read_file_exact_valid_rate_lt_0_40`
- tradeoff watch rule `read_file_exact_valid_rate_lt_0_70`

The first live probe design lists it as a required decision metric. Dataset builders consume related read-file rates as anti-regression context.

#### Current Status

Still required and redesign required. The current live summary has `adapter.per_split.tool_holdout.exact_json_validity.rate`, but that split is mixed-tool and is not a one-to-one read-file metric. `comparison_rows.jsonl` and source eval rows contain enough information to identify read-file rows, but filtering and aggregating those rows would be reconstruction.

#### Governance Impact

Removing this metric entirely would remove the main guard against `read_file` collapse during no-call pressure, geometry sampling, or other interventions. Current aggregate exact-valid, tool-name accuracy, and argument accuracy can hide a per-tool regression if other tools improve or dominate the sample.

#### Redesign Considerations

- Emit per-tool exact-valid summaries from the evaluator, including count, denominator, and rate.
- Decide whether per-tool rates should be emitted for every tool or only governance-critical tools such as `read_file`.
- Preserve split identity: if the governance concern is `tool_holdout` read-file behavior, the metric should specify split and denominator.
- Keep catastrophic and watch thresholds closed until an approved first-class metric exists.

Hidden assumptions in the original implementation:

- The eval summary contains a stable `failure_profile` with read-file-specific rows.
- The read-file row denominator is stable enough for fixed thresholds.
- A single read-file exact-valid rate captures the relevant retrieval behavior.
- Mixed-tool exact validity can be separated elsewhere if needed.

#### Preliminary Recommendation

Still required. Redesign as an explicit evaluator-emitted per-tool slice, not as a path convergence candidate. It should remain a governance metric once re-emitted with clear denominator semantics.

### `read_file_symbol_name_exact_valid_rate`

#### Original Purpose

Protect a harder `read_file` sub-slice where prompts ask the model to read a file and report a symbol name. The governance concern is that overall read-file exact-valid can recover while a semantically important, extraction-like sub-archetype collapses.

#### Historical Producer

The metric is present in historical `failure_profile.read_file_symbol_name_exact_valid.rate` fields for later probe summaries. Examples:

- `stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`: `0.9230769230769231`
- `stage_b_v1_i10r_residual_nocall_probe_canonical_eval_summary.json`: `0.23076923076923078`

Related preservation reports include explicit symbol-name counts and denominators, for example `stage_b_v1_i10r_counterbalanced_probe_read_file_symbol_name_preservation_assessment.json` and `stage_b_v1_i10r_residual_nocall_probe_read_file_preservation_assessment.json`.

No tracked current live evaluator producer emits read-file archetype or symbol-name sub-slice summaries.

#### Historical Consumer

The active threshold profile consumes this metric through catastrophic rule `read_file_symbol_name_exact_valid_rate_lt_0_40`.

The first live probe design lists it as a required decision metric. Dataset builders consume related `read_file_symbol_name_exact_valid_rate` context for residual no-call anti-regression assessment.

#### Current Status

Redesign required. The current live summary has no symbol-name archetype field. The source prompts and some historical metadata can identify symbol-name-like rows, but extracting that set would be inference/reconstruction unless a future evaluator emits the archetype as first-class schema.

#### Governance Impact

Removing this metric entirely would allow a targeted collapse in symbol-name file-read behavior to pass unnoticed if broader `read_file` or mixed-tool metrics remain acceptable. That is especially risky because historical reports show symbol-name preservation and collapse can diverge sharply across probes.

#### Redesign Considerations

- Emit eval-row archetype metadata for `read_file` rows, then summarize exact-valid rate by archetype.
- Define whether this metric belongs as a standalone catastrophic threshold or as a required sub-slice under a broader read-file preservation family.
- Preserve counts and denominators because historical symbol-name rows were small, making rate volatility material.
- Avoid prompt substring matching in detector or threshold mapping.

Hidden assumptions in the original implementation:

- Symbol-name rows are identifiable and stable across eval versions.
- The prompt text or source-case naming convention is a legitimate archetype identifier.
- A small denominator is acceptable for catastrophic governance.
- Overall read-file behavior is insufficient to protect this sub-slice.

#### Preliminary Recommendation

Still justified, but potentially mergeable into a redesigned `read_file` slice family. Keep it separate as a required sub-slice if future planning confirms symbol-name behavior remains a governed dependent variable.

## Cross-Metric Findings

All four metrics are semantically meaningful governance signals, but none currently has a direct live-schema equivalent.

The four metrics fall into two redesign families:

- Failure subtype redesign: `direct_answer_substitution_count`
- Eval slice/metadata redesign: `no_anchor_exact_valid_share`, `read_file_exact_valid_rate`, `read_file_symbol_name_exact_valid_rate`

The detector is behaving consistently with conservative governance. Noncomputability should remain `halt_progression` until explicit redesign is approved and implemented.

Current active computable findings remain separate and valid:

- `no_call_correctness_aggregate` is approximately `0.9333`.
- `wrapper_leakage_overall` is approximately `0.015`.

Those findings should not be obscured by future redesign work for these four metrics.

## Candidate Redesign Themes

1. Emit first-class evaluator slices.
   Add explicit summary dimensions for tool name, split, and approved prompt/archetype labels so per-tool and sub-archetype exact-valid rates are native outputs.

2. Emit explicit failure subtypes.
   Extend the scorer output with approved failure subtypes for tool-expected rows, including direct-answer substitution if it remains governance-relevant.

3. Carry approved eval metadata into comparison rows and summaries.
   Preserve source metadata such as tool family, archetype, and anchor bucket only when those labels are declared evaluation fields, not inferred detector-time text scans.

4. Clarify denominator contracts.
   For every redesigned rate or count, specify numerator, denominator, eligible split(s), and baseline comparability requirements.

5. Separate governance gates from diagnostic context.
   Some current concepts may belong in diagnostic reports until their labels and denominators are strong enough for gating.

## Metrics Potentially No Longer Justified

No metric is currently safe to remove outright based on repository evidence.

`no_anchor_exact_valid_share` is the least justified as an isolated top-level governance metric unless anchor bucket becomes an explicit evaluation field. It remains justified as a governance concern, but may be better merged into an anchor-generalization metric family.

`read_file_symbol_name_exact_valid_rate` may be mergeable into a redesigned read-file preservation family, but removing the sub-slice entirely would lose a historically important collapse signal.

## Next Planning Recommendation

The next Stage B planning step should define a metric redesign contract before implementation. For each retained concept, approve:

- metric owner/purpose,
- numerator and denominator,
- required eval-row metadata,
- summary path shape,
- baseline comparability rule,
- threshold/gating role,
- retirement or merge decision.

Only after that contract is approved should schemas, scorer output, detector mappings, or thresholds be changed.
