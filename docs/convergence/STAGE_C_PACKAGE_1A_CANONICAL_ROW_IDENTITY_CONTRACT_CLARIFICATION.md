# Stage C Package 1A Canonical Row Identity Contract Clarification

## Scope

This artifact clarifies authoritative row-identity instantiation for Stage C Package 1A in the live canonical evaluator path.

Clarified scope only:

1. why `source_case_id` is not authoritative row identity;
2. why duplicate `source_case_id` values are expected in the canonical corpus;
3. the canonical evaluator row-identity instantiation rule;
4. the relationship between `row_id`, `split_id`, and row-set identity.

Out of scope:

1. detector migration;
2. threshold-profile migration;
3. comparability cutover;
4. historical metric identity replacement;
5. Package 2 implementation.

## Authoritative Inputs

This clarification is anchored to:

- `STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
- `STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
- `STAGE_B_WP3_FAMILY_A_SCORER_EVIDENCE_CONTRACT.md`
- `STAGE_B_WP3_SCORER_EVIDENCE_OUTPUT_DESIGN_REVIEW.md`
- `STAGE_C0_EVALUATOR_IMPLEMENTATION_ENTRY_CONTRACT_LOCK.md`
- `scripts/stage_c1_evaluator_foundation.py`
- `scripts/build_dataset_v1.py`
- `scripts/eval_canonical_manifest.py`
- `evals/canonical_eval_manifest_v1.json`
- canonical corpus files under `evals/data/canonical_v1/*.jsonl`

## Contract Requirements

Stage B and Stage C already lock the row-identity concept even though the canonical corpus does not yet ship a dedicated `row_id` field.

Required contract properties:

1. dataset metadata owns row identity and split membership (`STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`, `STAGE_B_WP3_FAMILY_A_SCORER_EVIDENCE_CONTRACT.md`);
2. row identity must be stable enough for baseline comparison (`STAGE_B_EVAL_REDESIGN_CONTRACTS.md`, `STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`);
3. row identity and split membership are separate required row-fact concepts (`STAGE_C0_EVALUATOR_IMPLEMENTATION_ENTRY_CONTRACT_LOCK.md`, `scripts/stage_c1_evaluator_foundation.py`);
4. missing row identity is governance-significant because it blocks audit and reconciliation (`STAGE_B_WP3_SCORER_EVIDENCE_OUTPUT_DESIGN_REVIEW.md`);
5. row identity sources must not be inferred from prompt text, naming conventions, or filesystem paths (`STAGE_B_EVALUATOR_ARCHITECTURE_DISCOVERY_AND_GAP_ANALYSIS.md`).

## Why `source_case_id` Is Not Row Identity

`source_case_id` is a provenance label carried through corpus construction. Repository evidence does not support treating it as a globally unique row key.

Evidence:

1. `scripts/build_dataset_v1.py` preserves `source_case_id` from upstream metadata and only synthesizes a fallback when source metadata omits it. This behavior is provenance preservation, not row-identity minting.
2. The same builder groups normalized tool rows into `rows_by_case` keyed by `source_case_id` before holdout selection. A single `source_case_id` is therefore expected to back multiple rows.
3. `tool_holdout` is sampled from the holdout pool with replacement. Exact repeated rows sharing the same `source_case_id` are therefore valid by construction.
4. Tool-row deduplication is keyed on `(user_text, tool_name, arguments)`, not `source_case_id`, which further shows that `source_case_id` is not the corpus row key.

Concrete corpus evidence:

1. `data/v1_0/dataset_v1_0_summary.json` records `8` holdout case IDs but `40` `tool_holdout` rows, which implies repeated case IDs inside that split.
2. `evals/data/canonical_v1/heldout_validation.jsonl` contains materially different rows with the same `source_case_id` `p0_read_file_2`, including different prompts and different expected tools.
3. `evals/data/canonical_v1/tool_holdout.jsonl` contains exact duplicated rows sharing `source_case_id` `p0_find_files_1`, matching with-replacement sampling semantics.

Determination:

- `source_case_id` remains authoritative provenance metadata.
- `source_case_id` is not authoritative row identity.

## Why Duplicate `source_case_id` Values Are Expected

Duplicate `source_case_id` values are a normal corpus property, not a repository anomaly.

Evidence chain:

1. normalized source tool rows retain their upstream `source_case_id` values;
2. holdout case selection operates over case pools rather than unique output rows;
3. `tool_holdout` sampling allows replacement;
4. non-holdout selection also allows multiple normalized rows originating from the same case pool when those rows differ structurally.

This means two different duplication patterns are expected:

1. one case ID may correspond to multiple distinct evaluation rows;
2. one case ID may correspond to repeated identical evaluation rows when a split samples with replacement.

## Canonical Evaluator Row-Identity Instantiation Rule

For the current frozen canonical evaluator corpus, authoritative logical row identity is:

1. row-set identity;
2. `split_id`;
3. `row_index_1based`.

Package 1A instantiates emitted Stage C `row_id` as:

- `"{split_id}:{row_index_1based}"`

This rule is the smallest defensible instantiation because:

1. the live evaluator already loads split membership and ordinal row position during canonical row construction;
2. the live evaluator already uses `(split, row_index_1based)` as the structural key for legacy comparison-row alignment;
3. split-plus-ordinal distinguishes both repeated `source_case_id` rows and exact duplicated rows without reinterpreting provenance labels;
4. the rule does not require prompt-derived inference, content-derived reconstruction, or path-derived heuristics.

## Relationship Between `row_id`, `split_id`, And Row-Set Identity

The three identity layers are related but distinct.

### `row_id`

- Per-row emitted Stage C identifier.
- Package 1A value: `"{split_id}:{row_index_1based}"`.
- Must be unique within a frozen canonical row set.

### `split_id`

- Separate row-fact field required by contract.
- Identifies split membership for split-scoped aggregation and reporting.
- Must remain independently visible; it is not collapsed into provenance only.

### Row-Set Identity

- Run-level evaluation-context identity for the frozen collection of rows under evaluation.
- In the canonical evaluator path this is anchored by the manifest and its split metadata, including manifest version and split hashes in `evals/canonical_eval_manifest_v1.json`.
- Row-set identity is not a replacement for per-row identity. It scopes the meaning of `row_id` and `split_id` across reruns and baseline review.

Operational interpretation:

- authoritative logical row reference = `(row-set identity, split_id, row_index_1based)`
- emitted Stage C row reference = `row_id` plus separate `split_id`

## Governance Alignment

This clarification preserves Stage B / Stage C governance requirements:

1. missing or duplicated provenance labels do not force evaluator reconstruction of identity;
2. provenance remains preserved because `source_case_id` continues to travel in emitted evidence payloads;
3. no prompt text, path text, or detector-time inference is used to synthesize row identity;
4. exact duplicated corpus rows remain audit-distinguishable because ordinal row slots remain distinct.

## Boundary Confirmation

This clarification does not change:

1. detector authority;
2. threshold authority;
3. comparability policy;
4. legacy metric identities;
5. governed ownership of Family A, Family B1, or Family B2 facts outside canonical row identity instantiation.
