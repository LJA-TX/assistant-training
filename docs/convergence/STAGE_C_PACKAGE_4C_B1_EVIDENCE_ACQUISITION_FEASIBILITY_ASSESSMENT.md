# Stage C Package 4C B1 Evidence Acquisition Feasibility Assessment

## Scope

This package evaluates whether a doctrine-compliant path exists by which authoritative Family B1 symbol-name governed-membership evidence could exist in a future authorized corpus revision for:

- `read_file_symbol_name_exact_valid_rate`

This is feasibility assessment only.

It does not:

1. modify the frozen corpus;
2. create metadata;
3. perform readiness reassessment;
4. perform gate reassessment;
5. begin migration planning;
6. infer governed membership from prompt content.

## Inputs

Doctrine and contract inputs:

1. `docs/convergence/STAGE_B_B1_SYMBOL_NAME_OWNERSHIP_REVIEW.md`
2. `docs/convergence/STAGE_B_B1_PARENT_CONTEXT_AND_DENOMINATOR_REVIEW.md`
3. `docs/convergence/STAGE_B_B1_READINESS_CLOSURE_ASSESSMENT.md`
4. `docs/convergence/STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
5. `docs/convergence/STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
6. `docs/convergence/STAGE_B_EVAL_REDESIGN_SCHEMA_PROPOSAL.md`
7. `docs/convergence/STAGE_B_WP8_B1_FIXTURE_INDEX.md`
8. `docs/convergence/STAGE_C_PACKAGE_4A_SECOND_SURFACE_SELECTION_AND_REGIMEN_APPLICABILITY_ASSESSMENT.md`
9. `docs/convergence/STAGE_C_PACKAGE_4B_B1_GOVERNED_MEMBERSHIP_COVERAGE_QUALIFICATION.md`

Corpus and workflow inputs:

1. `evals/canonical_eval_manifest_v1.json`
2. `evals/data/canonical_v1/*.jsonl`
3. `data/tool_ft_allaliases_20260525_from_qual_reports_freq.jsonl`
4. `/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_aug_rebalanced_20260417T104659Z.jsonl`
5. `/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_aug_focus_rebalanced_20260417T104747Z.jsonl`
6. `scripts/build_dataset_v1.py`
7. `scripts/eval_canonical_manifest.py`
8. `scripts/stage_c1_evaluator_foundation.py`
9. `data/v1_0/dataset_v1_0_summary.json`

## Current Surface Constraint

Package 4B established:

1. authoritative B1 governed-membership coverage on the frozen canonical corpus is `absent`;
2. explicit symbol-membership declarations in the frozen canonical row set: `0`;
3. explicit archetype declarations in the frozen canonical row set: `0`;
4. current `insufficient-evidence` remains justified.

The question in Package 4C is narrower:

1. is the surface merely missing evidence that could exist under current doctrine; or
2. is the surface effectively unreachable under current doctrine and corpus governance?

## Evidence Requirements Inventory

### Minimum Governed Evidence Required

Under existing B1 doctrine and contracts, `read_file_symbol_name_exact_valid_rate` becomes meaningfully assessable only when all of the following exist:

1. explicit read-file family eligibility
2. explicit symbol-name governed-membership or explicit approved archetype declaration
3. explicit ownership marker for the declared symbol-name membership when membership is declared
4. stable row identity
5. explicit split membership
6. scorer exact-valid outcome
7. parent read-file context
8. symbol-name denominator visibility
9. symbol-name numerator visibility
10. comparability markers sufficient for later migration review

### Required Marker Classes

Required marker classes, grouped by owner:

Dataset metadata or evaluator-owned metadata preparation:

1. expected tool identity
2. read-file family eligibility
3. symbol-name governed-sub-slice membership or approved read-file archetype
4. explicit non-membership for read-file rows outside the sub-slice when represented
5. split membership
6. stable row identity
7. pre-scoring exclusion status when applicable

Scorer:

1. exact-valid outcome
2. scorer semantics marker

Evaluator:

1. symbol-name count
2. symbol-name denominator
3. symbol-name rate
4. parent read-file aggregate context
5. sub-slice comparability markers
6. current-run computability and noncomputability state

### Minimum Meaningful Assessability Threshold

The surface is not meaningfully assessable merely because one or two rows happen to be tagged.

Meaningful assessability requires at least:

1. explicit governed rows in the approved evaluation population;
2. enough emitted denominator visibility to distinguish absence, missingness, and small-denominator volatility;
3. parent-context completeness so the governed sub-slice can be interpreted without substitution from the aggregate read-file metric.

## Potential Evidence Sources

### Doctrinally Acceptable Source Types

Repository doctrine permits only the following kinds of upstream source for the missing evidence:

1. dataset metadata
2. evaluator-owned metadata preparation upstream of aggregation
3. approved read-file archetype declarations emitted as evaluation metadata
4. upstream evaluation-data tooling that writes explicit membership before aggregation

Repository doctrine does not permit:

1. prompt-derived inference
2. generated-text-derived inference
3. detector-time classification
4. parent-aggregate substitution
5. historical report-layer values as current-run membership evidence

### Current Repository Workflow Evidence

The current repository already has a place where evaluation rows are normalized and metadata is written:

1. `scripts/build_dataset_v1.py` normalizes tool rows into canonical rows;
2. each normalized canonical tool row receives a `metadata` object;
3. the frozen manifest then binds the resulting jsonl files as the evaluation row set;
4. `scripts/eval_canonical_manifest.py` already knows how to consume explicit:
   - `symbol_name_membership`
   - `membership_owner`
   - `symbol_name_membership_owner`
   - `read_file_archetype`
   - `eval_read_file_archetype`
   - `intervention_i10_query_archetype`

That means a doctrinally acceptable carrier path already exists in the repository architecture:

1. upstream evaluation metadata row fields;
2. emitted row-fact membership markers;
3. downstream governed aggregation.

### Current Upstream Source Limitation

Current upstream tool sources do not currently provide the missing evidence.

Observed current upstream metadata for read-file rows in the tool sources:

1. `case_id`
2. `source`
3. `tool`

Observed current normalized canonical metadata for read-file rows:

1. `category`
2. `source`
3. `source_case_id`
4. `source_file`
5. `tool`
6. `synthetic`

So the doctrine-compatible carrier path exists, but the currently populated source metadata does not supply symbol-membership evidence.

## Doctrine Compatibility Review

### Compatibility Classification

Future acquisition of the missing evidence is:

- `doctrine-constrained`

### Rationale

It is not `doctrine-prohibited` because current doctrine explicitly allows:

1. dataset metadata to own symbol-name membership;
2. evaluator-owned metadata preparation upstream of aggregation;
3. approved archetype declarations as evaluation metadata;
4. future explicit current-run symbol-name evidence when emitted before detector consumption.

It is not unconstrainedly `doctrine-compatible` because doctrine imposes hard boundaries:

1. membership must be explicit before aggregation;
2. prompt text must not become membership evidence;
3. generated text must not become membership evidence;
4. parent read-file aggregate must not substitute for child symbol-name membership;
5. missing membership must remain noncomputable;
6. detector must consume emitted facts only.

So the future path is allowed, but only under strict ownership and non-inference constraints.

## Corpus-Revision Feasibility Assessment

### Feasibility Determination

A future authorized corpus revision could theoretically provide the missing evidence without violating current doctrine.

Feasibility classification:

- feasible with authorized upstream corpus revision

### Why Feasible

The repository already contains the structural elements needed for a doctrine-compliant path:

1. a canonical evaluation row metadata carrier;
2. a dataset builder that writes canonical metadata;
3. a live evaluator that consumes explicit membership fields without needing prompt inference;
4. a row-fact contract that validates declared membership and ownership markers;
5. WP8 B1 fixtures that define acceptable complete, partial, missing, and non-inference states.

### Why A Corpus Revision Is Still Required

The current frozen evaluation row set and its upstream tool sources do not contain the evidence.

Therefore a future authorized revision would have to change at least one upstream stage:

1. enrich upstream evaluation-source metadata with explicit symbol-name membership or explicit archetype declarations; or
2. add an evaluator-owned metadata-preparation step that writes explicit membership into the evaluation rows before aggregation; or
3. revise the canonical dataset builder so those explicit upstream fields are preserved into the canonical evaluation jsonl outputs.

Without one of those authorized upstream changes, the current architecture cannot produce the missing evidence.

### Doctrine Boundary For Such A Revision

A future revision would remain doctrine-compliant only if:

1. membership is written explicitly into evaluation metadata before aggregation;
2. ownership markers remain upstream of detector consumption;
3. rows explicitly outside the symbol-name sub-slice remain representable;
4. parent read-file context remains visible;
5. count and denominator visibility are preserved;
6. no inference from prompt or generated content is used to manufacture membership.

## Surface Viability Determination

Surface viability classification:

- `viable with corpus revision`

### Rationale

The surface is not doctrinally blocked because:

1. B1 doctrine preserves it as a required governed sub-slice;
2. B1 doctrine explicitly allows explicit upstream membership or approved archetype declarations;
3. Stage C artifact emission already has slots for that declared evidence.

The surface is not currently viable on the frozen corpus because:

1. the evidence is absent today;
2. the current source files do not provide it;
3. the current normalized canonical corpus does not preserve it.

So the correct classification is neither:

1. `viable` now; nor
2. `doctrinally blocked`.

It is viable only if a later authorized corpus revision supplies explicit upstream governed evidence.

## Regimen Implications

### Recommendation

Regimen recommendation:

- defer this surface in active reuse planning until doctrine-compliant governed membership evidence exists in an authorized corpus revision.

### Why Defer Rather Than Switch Automatically

The surface remains the best doctrinally aligned second-surface candidate in structural terms, as Package 4A established.

But after Package 4B and Package 4C, the blocker is now better defined:

1. it is not a missing review problem;
2. it is not a doctrinal impossibility;
3. it is an upstream evidence-availability problem.

That means the regimen should not immediately switch surfaces on the basis that this surface is impossible.

It should instead recognize:

1. this surface remains strategically valuable;
2. current reuse cannot proceed on the frozen corpus;
3. progress requires an authorized corpus-evidence path first.

### Newly Clarified Regimen Boundary

Package 4C clarifies a reusable boundary in the extracted regimen:

1. before second-surface reuse begins, the candidate surface must be checked not only for readiness state but also for evidence-acquisition feasibility under current doctrine and corpus governance.

That boundary was not fully exercised by `read_file_exact_valid_rate`, because its governing evidence already existed in the frozen corpus.

## Determination

Package 4C determines that:

1. `read_file_symbol_name_exact_valid_rate` is not unreachable under current doctrine;
2. a doctrine-compliant future path for authoritative B1 governed-membership evidence does exist in principle;
3. that path requires an authorized upstream corpus revision or metadata-preparation revision;
4. the surface is therefore `viable with corpus revision`;
5. until such evidence exists, active regimen reuse on this surface should be deferred rather than treated as ready.

## Boundary Confirmation

This package does not:

1. modify the frozen corpus;
2. create metadata;
3. perform readiness reassessment;
4. perform gate reassessment;
5. begin migration planning;
6. infer governed membership from prompt content.
