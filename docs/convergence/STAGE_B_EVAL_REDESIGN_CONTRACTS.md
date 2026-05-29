# Stage B.2A Evaluation Redesign Contracts

## Scope

This document specifies governance-semantic contracts for the four retained Stage B metric concepts that require evaluation redesign:

- `direct_answer_substitution_count`
- `no_anchor_exact_valid_share`
- `read_file_exact_valid_rate`
- `read_file_symbol_name_exact_valid_rate`

This is documentation-only planning. It does not define schema names, output paths, detector mappings, thresholds, or implementation changes.

## Contract Principles

The following constraints govern all contracts in this document:

- No proxy mappings: related aggregate fields are insufficient unless the exact governed concept is explicitly emitted.
- No detector-time inference: the detector may consume declared metric facts, but must not classify prompts, generated text, or row populations itself.
- Stable denominators: every governed rate must declare its eligible population and denominator before it can support gate or watch semantics.
- Baseline comparability first: a metric cannot support trend or delta interpretation unless the row population, scorer semantics, and metadata taxonomy are comparable.
- Noncomputable remains conservative: until these concepts are explicitly emitted by a redesigned evaluator/scorer stack, the current halt behavior remains expected.

## Recommended Family Structure

### Family A: Governed Failure-Subtype Taxonomy

Contains the retained concept currently represented by `direct_answer_substitution_count`.

Recommendation:
- Do not retain as an isolated raw count only.
- Redesign as a governed failure-subtype taxonomy for tool-expected rows.
- Preserve direct-answer substitution as a governed subtype within that taxonomy.
- Emit both count and denominator-bearing rate for review, while leaving future threshold decisions to a later phase.

### Family B1: Read-File Preservation Family

Contains the retained concepts currently represented by:

- `read_file_exact_valid_rate`
- `read_file_symbol_name_exact_valid_rate`

Recommendation:
- Redesign as a read-file preservation family.
- Retain overall read-file exact-valid behavior as the family aggregate concept.
- Merge symbol-name behavior into the family as a required governed sub-slice, not as a retired standalone concern.

### Family B2: Anchor-Generalization Family

Contains the retained concept currently represented by `no_anchor_exact_valid_share`.

Recommendation:
- Redesign as an anchor-generalization family.
- Treat no-anchor exact-valid behavior as a governed sub-slice of prompt generalization.
- Do not leave it as a standalone top-level metric unless future planning rejects the family structure.

## Contract: Direct-Answer Substitution

### Disposition

Redesigned and merged into Family A. Retain the governed concept; do not retire or downgrade to diagnostic-only.

### Purpose

Protect against false procedural progress where a tool-expected row receives direct result prose, scalar output, or other answer-like text instead of the required tool invocation. This metric protects evidence-gathering discipline and prevents aggregate exact-valid or invalid-json movement from hiding a model that bypasses tools.

### Metric Owner

Primary owner: scorer.

Supporting owners:
- evaluator, to aggregate the scorer-emitted subtype over eligible rows;
- dataset metadata, to declare which rows are tool-expected and what canonical tool behavior is expected.

The detector should be a consumer only.

### Required Eval-Row Metadata

Required explicit row facts:

- whether the row expects a tool call;
- canonical expected tool identity and expected arguments;
- scorer primary outcome class;
- scorer parse/schema outcome sufficient to distinguish non-exact tool rows;
- approved failure subtype for non-exact tool-expected rows;
- row inclusion split;
- stable row identity for baseline comparability.

The failure subtype must be emitted as an approved scorer result, not reconstructed from generated prose by the detector.

### Numerator Definition

Number of eligible tool-expected rows where the scorer classifies the non-exact outcome as direct-answer substitution under the approved failure-subtype taxonomy.

### Denominator Definition

Two denominator views are required for a complete contract:

- total eligible tool-expected rows, for run-comparable rate interpretation;
- total non-exact eligible tool-expected rows, for failure-mix interpretation.

The historical count may remain available, but a count alone is insufficient for robust comparison unless row counts are fixed.

### Eligible Population

Rows qualify when all are true:

- the row is part of the approved evaluation population for the run;
- the row expects one or more canonical tool calls;
- the row is not exact-valid under scorer semantics;
- the row has an approved failure subtype.

Rows that expect no call are excluded.

### Split Scope

Eligible tool-positive splits only. Historical usage implies heldout and tool-holdout style tool-positive populations are relevant. Direct-answer/no-call/adversarial rows are excluded unless future evaluation design explicitly creates a tool-expected direct-answer-substitution stress split.

### Baseline Comparability Requirements

Comparisons require:

- same or explicitly versioned evaluation row population;
- same tool-expected eligibility rules;
- same scorer primary-class semantics;
- same failure-subtype taxonomy;
- stable treatment of malformed JSON, scalar output, prose output, wrapper drift, and missing-tool-call cases;
- stable denominator reporting.

Delta interpretation is not meaningful if a future run changes subtype taxonomy or eligible row count without explicit annotation.

### Governance Role

Tradeoff watch. The concept should detect material rebound in answer substitution during interventions. It should not become a catastrophic gate by contract alone; any escalation would require later threshold planning.

### Detector Consumer Requirements

The detector must receive:

- direct-answer substitution count;
- eligible tool-expected denominator;
- non-exact tool-expected denominator;
- rate over tool-expected rows;
- rate over non-exact tool-expected rows;
- taxonomy version or equivalent comparability marker;
- split/population identity used for aggregation;
- baseline value only when delta rules are evaluated.

The detector must not inspect generated text or infer the failure subtype.

### Retirement Criteria

This concept may be removed or merged only if:

- a broader governed failure-subtype taxonomy replaces it and preserves direct-answer substitution visibility;
- empirical evidence shows direct-answer substitution is no longer a distinct failure class across approved eval runs;
- no active threshold, watch rule, readiness review, or human-review package depends on it;
- removal does not weaken detection of tool-bypass behavior.

## Contract: No-Anchor Exact-Valid Generalization

### Disposition

Redesigned and merged into Family B2. Retain the governed concept as an anchor-generalization sub-slice; do not retire. It may be downgraded to diagnostic-only only if future planning rejects anchor-conditioned gating and supplies another governed generalization signal.

### Purpose

Protect against anchor dependence, where exact-valid behavior works primarily when prompts contain literal or paraphrastic tool-call/schema cues. This concept protects procedural generalization on less explicit prompts.

### Metric Owner

Primary owner: dataset metadata or evaluator, depending on where approved anchor classification is declared.

Supporting owners:
- scorer, to provide exact-valid outcome;
- evaluator, to aggregate exact-valid behavior by approved anchor category.

The detector should be a consumer only.

### Required Eval-Row Metadata

Required explicit row facts:

- whether the row belongs to an anchor-generalization eligible population;
- approved prompt anchor category;
- whether the row is tool-expected;
- scorer exact-valid outcome;
- row inclusion split;
- stable row identity for baseline comparability.

The prompt anchor category must be declared before detector consumption. The detector must not classify prompts using string matching.

### Numerator Definition

Number of eligible rows in the no-anchor category that are exact-valid under scorer semantics.

### Denominator Definition

Number of eligible rows in the no-anchor category.

If a future design needs the historical "share of exact-valid rows that are no-anchor" interpretation, it must be separately contracted because it answers a different denominator question.

### Eligible Population

Rows qualify when all are true:

- the row is in an approved evaluation population for anchor-generalization measurement;
- the row has an approved anchor category;
- the row is tool-expected unless future planning explicitly approves no-call anchor-generalization semantics;
- the row is not excluded by contamination, ambiguity, or unsupported metadata.

### Split Scope

Tool-positive evaluation splits that contain approved anchor-category coverage. No-call and direct-answer splits are excluded unless a future contract explicitly defines anchor-generalization for no-call behavior.

### Baseline Comparability Requirements

Comparisons require:

- stable anchor taxonomy;
- stable assignment process for anchor categories;
- stable exact-valid scorer semantics;
- comparable no-anchor row population and denominator;
- comparable prompt distribution or explicit drift annotation;
- stable split inclusion.

No-anchor behavior is not comparable if anchor labels are derived differently across baseline and current runs.

### Governance Role

Tradeoff watch by default. The concept protects generalization and should remain visible in governance review. It should not be used as a catastrophic gate without later threshold planning and denominator validation.

### Detector Consumer Requirements

The detector must receive:

- no-anchor exact-valid count;
- no-anchor eligible row count;
- no-anchor exact-valid rate;
- anchor taxonomy/comparability marker;
- split/population identity used for aggregation;
- optionally, companion counts/rates for other approved anchor categories for interpretation.

The detector must not inspect prompt text or infer anchor category.

### Retirement Criteria

This concept may be removed or merged only if:

- a broader anchor-generalization family replaces it and preserves no-anchor visibility;
- approved eval coverage no longer includes meaningful anchor variation;
- a superior governed generalization signal is adopted without weakening detection of anchor dependence;
- no active governance review depends on no-anchor behavior.

## Contract: Read-File Exact-Valid Preservation

### Disposition

Redesigned and retained as the aggregate concept inside Family B1. Do not retire or downgrade to diagnostic-only.

### Purpose

Protect `read_file` procedural commitment during no-call and geometry interventions. This concept prevents improvements in no-call behavior or mixed-tool aggregates from masking collapse in file-read evidence acquisition.

### Metric Owner

Primary owner: evaluator.

Supporting owners:
- dataset metadata, to declare expected tool identity;
- scorer, to emit exact-valid outcome;
- detector, as consumer only.

### Required Eval-Row Metadata

Required explicit row facts:

- whether the row expects a tool call;
- canonical expected tool identity;
- scorer exact-valid outcome;
- split membership;
- stable row identity for baseline comparability;
- exclusion status for contamination, ambiguity, or unsupported cases.

The evaluator must aggregate by expected tool identity rather than relying on detector-side row filtering.

### Numerator Definition

Number of eligible `read_file` tool-expected rows that are exact-valid under scorer semantics.

### Denominator Definition

Number of eligible `read_file` tool-expected rows.

### Eligible Population

Rows qualify when all are true:

- the row is part of the approved evaluation population;
- the row expects `read_file` as the canonical tool behavior;
- the row has valid expected arguments for scorer comparison;
- the row belongs to an eligible split;
- the row is not excluded by contamination, ambiguity, or unsupported metadata.

Rows for other tools are excluded.

### Split Scope

Tool-positive evaluation splits containing `read_file` rows. Historical governance emphasizes heldout/tool-holdout style populations. Split inclusion must be explicit and stable for each comparison.

### Baseline Comparability Requirements

Comparisons require:

- stable `read_file` row set or explicitly versioned row-set changes;
- stable expected argument semantics;
- stable scorer exact-valid definition;
- stable split inclusion;
- stable denominator and count reporting;
- explicit annotation if prompt archetype mix changes materially.

Mixed-tool exact-valid rates are not comparable substitutes.

### Governance Role

Catastrophic gate and tradeoff watch concept. The existing governance intent treats severe read-file collapse as catastrophic and moderate degradation as watch-level. This document does not set or revise thresholds.

### Detector Consumer Requirements

The detector must receive:

- `read_file` exact-valid count;
- `read_file` eligible row count;
- `read_file` exact-valid rate;
- split/population identity used for aggregation;
- scorer/eval comparability marker;
- baseline value when delta or comparative interpretation is required.

The detector must not compute this by scanning row-level records.

### Retirement Criteria

This concept may be removed or merged only if:

- `read_file` is no longer a governed tool family;
- another governed tool-preservation family includes an equivalent `read_file` aggregate with explicit count, denominator, and rate;
- no active intervention depends on read-file preservation;
- removal does not weaken detection of per-tool collapse hidden by mixed-tool metrics.

## Contract: Read-File Symbol-Name Exact-Valid Preservation

### Disposition

Redesigned and merged into Family B1 as a required governed sub-slice. Do not retire. Do not retain as an isolated top-level metric if the read-file preservation family is adopted.

### Purpose

Protect a harder `read_file` subpopulation where the model must issue the file-read call rather than directly reporting a symbol-like answer. This concept detects sub-slice collapse that can be hidden by overall `read_file` exact-valid recovery.

### Metric Owner

Primary owner: evaluator, with dataset metadata support.

Supporting owners:
- dataset metadata, to declare approved read-file archetype membership;
- scorer, to emit exact-valid outcome;
- detector, as consumer only.

### Required Eval-Row Metadata

Required explicit row facts:

- whether the row expects `read_file`;
- approved read-file archetype or subpopulation membership;
- scorer exact-valid outcome;
- split membership;
- stable row identity for baseline comparability;
- exclusion status for contamination, ambiguity, or unsupported cases.

The archetype must be declared as evaluation metadata. The detector must not infer symbol-name membership from prompt text.

### Numerator Definition

Number of eligible `read_file` symbol-name rows that are exact-valid under scorer semantics.

### Denominator Definition

Number of eligible `read_file` symbol-name rows.

### Eligible Population

Rows qualify when all are true:

- the row is part of the approved evaluation population;
- the row expects `read_file` as the canonical tool behavior;
- the row belongs to the approved symbol-name read-file subpopulation;
- the row has valid expected arguments for scorer comparison;
- the row belongs to an eligible split;
- the row is not excluded by contamination, ambiguity, or unsupported metadata.

### Split Scope

Tool-positive evaluation splits containing approved read-file symbol-name rows. Split inclusion must be explicit because this subpopulation may have a small denominator.

### Baseline Comparability Requirements

Comparisons require:

- stable symbol-name subpopulation definition;
- stable row identities or explicitly versioned additions/removals;
- stable scorer exact-valid semantics;
- stable `read_file` expected-argument semantics;
- stable split inclusion;
- count and denominator visibility due to small-denominator volatility.

Overall read-file exact-valid rate is not a replacement for this sub-slice.

### Governance Role

Catastrophic gate concept as a read-file preservation sub-slice, subject to later threshold planning. It may also be reported diagnostically alongside the aggregate read-file preservation metric.

### Detector Consumer Requirements

The detector must receive:

- symbol-name exact-valid count;
- symbol-name eligible row count;
- symbol-name exact-valid rate;
- subpopulation/archetype comparability marker;
- split/population identity used for aggregation;
- parent read-file aggregate context for interpretation.

The detector must not infer symbol-name membership.

### Retirement Criteria

This concept may be removed or merged only if:

- the read-file preservation family includes an approved replacement sub-slice that captures the same extraction-like behavior;
- symbol-name rows are no longer part of approved governance coverage;
- empirical evidence shows the sub-slice no longer diverges from aggregate read-file behavior across representative runs;
- removal does not weaken detection of read-file subpopulation collapse.

## Cross-Contract Recommendations

### Recommended Retained Metric Concepts

Retain all four concepts:

- direct-answer substitution among tool-expected failures;
- no-anchor exact-valid generalization;
- aggregate read-file exact-valid preservation;
- read-file symbol-name exact-valid preservation.

None should be retired in Stage B.2A.

### Recommended Metric-Family Structure

Recommended structure:

- Family A: governed failure-subtype taxonomy for tool-expected non-exact rows.
- Family B1: read-file preservation family with aggregate and required sub-slice reporting.
- Family B2: anchor-generalization family with no-anchor behavior as a governed sub-slice.

### Concepts Recommended For Merger

Recommended mergers:

- `direct_answer_substitution_count` into Family A as a governed subtype, retaining count and rate visibility.
- `read_file_symbol_name_exact_valid_rate` into Family B1 as a required read-file sub-slice.
- `no_anchor_exact_valid_share` into Family B2 as a no-anchor generalization sub-slice.

`read_file_exact_valid_rate` should remain the aggregate concept inside Family B1.

### Concepts Recommended For Retirement

No concepts are recommended for retirement.

### Diagnostic-Only Downgrade Assessment

No concept should be downgraded to diagnostic-only in this phase.

The no-anchor concept is the closest candidate for diagnostic-only treatment if future planning cannot approve stable anchor metadata. Until then, it remains a governed concern requiring redesign, not a retired or relaxed metric.

## Recommended Stage B.2B Objective

Stage B.2B should define the metric emission design without implementation. It should specify, for each approved family:

- the required information content to appear at row level;
- the required information content to appear in aggregate summaries;
- versioning/comparability markers;
- which component is responsible for emitting each fact;
- detector consumption expectations;
- migration treatment for historical baselines.

Stage B.2B should still avoid threshold redesign and should not implement schema, scorer, evaluator, detector, or manifest changes.
