# Stage B.2B Metric Emission Design

## Scope

This document defines how approved Stage B governance concepts should flow through a future evaluator/scorer stack as emitted information. It is documentation-only planning.

This document does not define schema field names, output paths, implementation details, detector redesign, threshold redesign, mappings, manifests, or governance relaxation.

Approved families:

- Family A: Governed Failure-Subtype Taxonomy
- Family B1: Read-File Preservation Family
- Family B2: Anchor-Generalization Family

## Recommended Emission Architecture

Future emission should use a four-layer ownership model:

1. Dataset metadata declares stable row facts before scoring.
2. Scorer emits behavioral outcome facts for each evaluated response.
3. Evaluator aggregates declared row facts and scorer facts into family summaries.
4. Detector consumes only emitted aggregate facts and comparability markers.

The detector must remain a policy consumer. It must not classify row populations, inspect generated text, infer prompt categories, infer archetypes, infer failure subtypes, or reconstruct denominators.

## Global Information-Flow Rules

- Row-level facts must exist before aggregation.
- Aggregates must include counts, denominators, and rates when a governed concept is rate-like.
- Family summaries must expose both aggregate concepts and governed sub-slices when approved.
- Comparability markers must travel with emitted facts.
- Historical baselines are comparable only when population, taxonomy, scorer semantics, and split scope are explicitly aligned or bridged by approved review.
- Missing required emitted facts should remain a governance noncomputability condition until redesign is implemented and approved.

## Family A: Governed Failure-Subtype Taxonomy

### Required Row-Level Facts

Each eligible row must carry or receive the following facts before aggregation:

- row identity stable across baseline comparison;
- split membership;
- whether the row expects a tool call;
- expected tool behavior sufficient for scorer correctness;
- scorer primary outcome;
- whether the response is exact-valid;
- whether the row is a non-exact tool-expected row;
- approved failure subtype for non-exact tool-expected rows;
- taxonomy marker for the failure subtype set;
- exclusion state for rows that should not enter governance aggregation.

Direct-answer substitution must be emitted as one approved subtype in this taxonomy. It must not be derived by detector-time text review.

### Required Aggregate Facts

Family-level aggregates must include:

- total eligible tool-expected row count;
- total exact-valid eligible tool-expected row count;
- total non-exact eligible tool-expected row count;
- count for each approved failure subtype;
- rate for each approved failure subtype over eligible tool-expected rows;
- rate for each approved failure subtype over non-exact eligible tool-expected rows;
- direct-answer substitution count;
- direct-answer substitution rate over eligible tool-expected rows;
- direct-answer substitution rate over non-exact eligible tool-expected rows;
- split-scoped versions of the same facts when split-specific governance is requested;
- summary of excluded rows, if exclusions exist.

The direct-answer substitution count may remain visible for continuity, but it should be emitted with denominators and rates.

### Ownership

Dataset metadata owns:

- row identity;
- split membership;
- tool-expected eligibility;
- expected tool behavior;
- approved exclusion annotations where known before scoring.

Scorer owns:

- primary behavioral outcome;
- exact-valid determination;
- failure subtype assignment for non-exact tool-expected rows;
- failure taxonomy marker.

Evaluator owns:

- eligibility filtering from declared facts;
- aggregation of counts, denominators, and rates;
- split-scoped summaries;
- family summary emission.

Detector owns:

- policy interpretation of emitted aggregate facts only.

### Comparability Markers

Required markers:

- failure taxonomy marker;
- scorer semantics marker;
- evaluation population marker;
- split identity marker;
- row-set marker;
- tool-expected eligibility marker;
- exclusion policy marker.

Direct-answer substitution comparisons require the same failure taxonomy and scorer semantics, or an approved migration bridge.

### Detector Consumption Requirements

The detector receives:

- direct-answer substitution count;
- direct-answer substitution denominators;
- direct-answer substitution rates;
- failure taxonomy marker;
- scorer and population comparability markers;
- split/population scope used for aggregation;
- baseline facts when a comparative rule is active.

The detector must not infer:

- failure subtype from generated text;
- whether prose is a direct answer;
- whether scalar output belongs to direct-answer substitution;
- denominator membership;
- split inclusion;
- row exclusion status.

### Historical Baseline Treatment

Historical baselines that contain only legacy failure-profile reports may be used as historical evidence, not automatically as comparable baselines.

Baseline comparison is allowed only when:

- the historical direct-answer substitution concept is matched to the approved failure subtype by documented review;
- eligible tool-expected population is stable or explicitly bridged;
- denominator differences are known;
- scorer and subtype semantics are stable enough for comparison;
- split scope matches or is explicitly annotated.

If these conditions are not met, historical values should be treated as reference-only.

### Migration Readiness Criteria

Implementation planning may begin only when:

- the approved failure subtype set is documented;
- direct-answer substitution has an approved subtype definition;
- row eligibility and denominator definitions are final;
- ownership boundaries are accepted by dataset, scorer, evaluator, and detector reviewers;
- historical baseline comparability rules are documented;
- expected emitted aggregate information is approved without relying on detector inference.

## Family B1: Read-File Preservation Family

### Required Row-Level Facts

Each eligible row must carry or receive the following facts before aggregation:

- row identity stable across baseline comparison;
- split membership;
- whether the row expects a tool call;
- expected tool identity;
- expected tool behavior sufficient for scorer correctness;
- whether the expected tool belongs to the read-file governed family;
- approved read-file subpopulation or archetype membership, when applicable;
- scorer exact-valid outcome;
- scorer semantics marker;
- exclusion state for rows that should not enter governance aggregation.

The symbol-name sub-slice must be declared before aggregation. It must not be inferred by the detector from prompt text.

### Required Aggregate Facts

Read-file family aggregate facts must include:

- total eligible read-file row count;
- exact-valid eligible read-file row count;
- read-file exact-valid rate;
- split-scoped read-file counts and rates when split-specific governance is requested;
- excluded read-file row count, if exclusions exist;
- read-file family comparability markers.

Symbol-name sub-slice facts must include:

- total eligible read-file symbol-name row count;
- exact-valid eligible read-file symbol-name row count;
- read-file symbol-name exact-valid rate;
- split-scoped symbol-name counts and rates when split-specific governance is requested;
- parent read-file aggregate context for interpretation;
- sub-slice comparability markers.

Additional read-file sub-slices may be emitted for diagnostics or future governance, but symbol-name remains a required governed sub-slice under this family.

### Ownership

Dataset metadata owns:

- row identity;
- split membership;
- expected tool identity;
- read-file family eligibility;
- read-file subpopulation or archetype annotations;
- pre-scoring exclusion annotations where applicable.

Scorer owns:

- exact-valid determination;
- scorer semantics marker.

Evaluator owns:

- aggregation by expected tool family;
- aggregation by approved read-file subpopulation;
- counts, denominators, rates, and family summaries;
- split-scoped summaries;
- population and subpopulation comparability markers.

Detector owns:

- policy interpretation of emitted read-file aggregate and sub-slice facts only.

### Comparability Markers

Required markers:

- scorer semantics marker;
- evaluation population marker;
- split identity marker;
- row-set marker;
- expected tool identity marker;
- read-file family marker;
- read-file subpopulation/archetype marker;
- exclusion policy marker.

Symbol-name comparisons require stable subpopulation membership or an approved migration bridge.

### Detector Consumption Requirements

The detector receives:

- read-file exact-valid count;
- read-file denominator;
- read-file exact-valid rate;
- symbol-name exact-valid count;
- symbol-name denominator;
- symbol-name exact-valid rate;
- parent family context for symbol-name interpretation;
- comparability markers;
- baseline facts when comparative interpretation is active.

The detector must not infer:

- whether a row is a read-file row;
- whether a row is a symbol-name row;
- exact-valid status;
- denominator membership;
- split inclusion;
- row exclusion status.

### Historical Baseline Treatment

Historical read-file preservation reports may be used for comparison only when:

- read-file eligibility matches the approved future population or is explicitly bridged;
- symbol-name sub-slice membership matches or is explicitly bridged;
- scorer exact-valid semantics are comparable;
- denominators are known;
- split scope is known;
- small-denominator volatility is surfaced with counts.

Historical values without clear denominator and subpopulation evidence should remain reference-only.

The symbol-name sub-slice requires stricter baseline handling than the aggregate read-file concept because small row counts can make rates volatile.

### Migration Readiness Criteria

Implementation planning may begin only when:

- read-file family eligibility is approved;
- symbol-name sub-slice definition is approved;
- required row-level ownership is accepted;
- aggregate count, denominator, and rate requirements are approved;
- comparability markers are agreed;
- historical baseline treatment is documented;
- detector consumption remains aggregate-only and inference-free.

## Family B2: Anchor-Generalization Family

### Required Row-Level Facts

Each eligible row must carry or receive the following facts before aggregation:

- row identity stable across baseline comparison;
- split membership;
- whether the row belongs to anchor-generalization measurement;
- approved anchor category;
- whether the row expects a tool call;
- scorer exact-valid outcome;
- scorer semantics marker;
- exclusion state for rows that should not enter governance aggregation.

No-anchor membership must be declared before aggregation. It must not be inferred by detector-side prompt scanning.

### Required Aggregate Facts

Anchor-generalization family facts must include:

- total eligible rows by approved anchor category;
- exact-valid eligible rows by approved anchor category;
- exact-valid rate by approved anchor category;
- no-anchor eligible row count;
- no-anchor exact-valid count;
- no-anchor exact-valid rate;
- split-scoped anchor-category summaries when split-specific governance is requested;
- family-level distribution of eligible rows by anchor category;
- exclusion summary, if exclusions exist;
- anchor taxonomy and population comparability markers.

The no-anchor governed sub-slice must be emitted as a rate over no-anchor eligible rows. If another denominator interpretation is desired in the future, it must be separately approved.

### Ownership

Dataset metadata owns:

- row identity;
- split membership;
- anchor-generalization eligibility;
- approved anchor category when category is assigned before scoring;
- tool-expected status;
- pre-scoring exclusion annotations where applicable.

Evaluator owns:

- anchor category only if category assignment is explicitly approved as evaluator-owned before scoring;
- aggregation by anchor category;
- family and no-anchor sub-slice summaries;
- population and anchor-taxonomy comparability markers.

Scorer owns:

- exact-valid determination;
- scorer semantics marker.

Detector owns:

- policy interpretation of emitted no-anchor and family facts only.

### Comparability Markers

Required markers:

- anchor taxonomy marker;
- anchor assignment owner marker;
- evaluation population marker;
- split identity marker;
- row-set marker;
- scorer semantics marker;
- tool-expected eligibility marker;
- exclusion policy marker.

No-anchor comparisons require stable anchor taxonomy and stable assignment ownership. A dataset-owned category and evaluator-owned category are not automatically comparable unless approved.

### Detector Consumption Requirements

The detector receives:

- no-anchor exact-valid count;
- no-anchor denominator;
- no-anchor exact-valid rate;
- anchor-category counts, denominators, and rates for contextual review;
- anchor taxonomy and assignment markers;
- population and split markers;
- baseline facts when comparative interpretation is active.

The detector must not infer:

- anchor category from prompt text;
- no-anchor membership;
- denominator membership;
- exact-valid status;
- split inclusion;
- row exclusion status.

### Historical Baseline Treatment

Historical no-anchor reports may be used for comparison only when:

- the anchor taxonomy is known and stable;
- the assignment process is known and comparable;
- no-anchor denominator is known;
- eligible row population is stable or explicitly bridged;
- exact-valid scorer semantics are comparable;
- split scope is known.

Historical values should remain reference-only if they are derived from prompt string heuristics that cannot be reproduced or approved under the future ownership model.

### Migration Readiness Criteria

Implementation planning may begin only when:

- anchor taxonomy is approved;
- anchor assignment ownership is approved;
- no-anchor denominator definition is approved;
- split scope is approved;
- aggregate family facts are approved;
- historical baseline comparability requirements are documented;
- detector consumption remains free of prompt-text inference.

## Cross-Family Ownership Boundaries

Recommended boundaries:

- Dataset metadata owns stable row identity, split membership, expected behavior, declared populations, declared subpopulations, declared anchor categories when preassigned, and pre-scoring exclusions.
- Scorer owns behavioral correctness, exact-valid status, primary outcome, failure subtype assignment, and scorer semantics markers.
- Evaluator owns aggregation, family summaries, denominator construction from declared facts, split-scoped summaries, and emitted comparability markers.
- Detector owns only policy interpretation of emitted facts and noncomputability handling when required facts are missing.

The detector must never become the owner of taxonomy assignment, row filtering, prompt classification, generated-text classification, or denominator construction.

## Required Comparability And Version Markers

Before any governed metric can be compared against a baseline, the emission stack must expose markers for:

- evaluation population;
- row set;
- split identity;
- scorer semantics;
- exact-valid semantics;
- failure subtype taxonomy;
- expected tool identity and tool-family eligibility;
- read-file subpopulation/archetype;
- anchor taxonomy;
- anchor assignment ownership;
- exclusion policy;
- aggregation population.

The markers do not need names in this planning phase. They must be explicit enough for a reviewer or detector-side policy layer to decide whether comparison is allowed, blocked, or reference-only.

## Historical-Baseline Migration Concerns

Historical reports remain valuable evidence, but they are not automatically compatible with future emitted metrics.

Key concerns:

- legacy reports may contain report-layer summaries not emitted by the live evaluator;
- denominator definitions may be implicit or incomplete;
- prompt-anchor classification may have used heuristic string logic;
- symbol-name sub-slice membership may depend on prompt text or source-case conventions;
- direct-answer substitution may have been classified with historical subtype logic;
- split inclusion may differ across reports;
- count-based deltas assume stable row populations.

Recommended baseline treatment:

- use historical values as reference-only until comparability markers are approved;
- allow comparison only after documented review of population, scorer semantics, taxonomy, denominator, and split scope;
- require explicit bridge notes when historical and future populations are not identical;
- preserve current active computable governance findings separately from redesign migration work.

## Migration Readiness Checklist

Stage B should not proceed to implementation planning until all are true:

- approved family ownership boundaries are documented;
- required row-level facts are approved for each family;
- required aggregate facts are approved for each family;
- comparability markers are approved;
- historical-baseline treatment is approved;
- detector consumption remains aggregate-only and inference-free;
- missing facts remain noncomputable rather than silently inferred;
- no threshold or governance relaxation is bundled into emission design.

## Recommended Stage B.3 Objective

Stage B.3 should produce an implementation-readiness plan, still before code changes, that maps these emission requirements to concrete work packets and validation gates.

Stage B.3 should define:

- implementation boundaries by component;
- review gates for dataset metadata, scorer semantics, evaluator aggregation, and detector consumption;
- fixture and validation expectations;
- baseline migration review procedure;
- noncomputability behavior for partial emission;
- rollback and audit expectations.

Stage B.3 should not change thresholds or relax governance. Threshold redesign, if needed, should remain a later governed phase after emitted metrics are available and validated.
