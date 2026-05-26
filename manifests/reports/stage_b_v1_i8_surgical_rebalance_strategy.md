# Stage B i8 Surgical Rebalancing Strategy (Recon + Proposal Only)

Generated: 2026-05-26
Scope: read-only reconnaissance + proposal (no dataset mutation executed)

## Inputs Reviewed
- `manifests/reports/stage_b_v1_i8_family_concentration_review.json`
- `manifests/reports/stage_b_v1_i8_family_concentration_review.md`
- `scripts/build_stage_b_v1_i8_family_concentration_review.py`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i8_train.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i8_val.jsonl`

## Objective
Reach approximately the telemetry profile of the existing 12% cap simulation with a surgical trim-only rebalance that preserves:
- ambiguity-remediation gains,
- multi-tool lineage signal,
- tool-routing realism,
- style and prompt coverage,
- hard/edge-case operational prompts.

## Baseline Concentration Facts
- Targeted rows (`read_file` + `rg_search`): `799`
- 12% cap-equivalent absolute ceiling: `floor(0.12 * 799) = 95` rows per family
- Families above that ceiling:
1. `i3_adapt_p0_read_file_1`: 122 rows
2. `i3_adapt_p0_rg_search_4`: 99 rows

## Risk Taxonomy (Explicitly Separated)
### 1) Mass concentration risk
- Main driver: family row share.
- Primary offenders: `i3_adapt_p0_read_file_1`, `i3_adapt_p0_rg_search_4`.

### 2) Semantic clone risk
- Driver: many rows with minimal incremental lexical/semantic variation.
- Evidence: very low effective-diversity ratios (for example `0.115`, `0.098`) and high exact-prompt reuse.

### 3) Template replication risk
- Driver: repeated skeleton families within and across high-mass families.
- Example overrepresented skeletons (tool+id):
1. `rg_search:7bf04fd7509e` (42 rows; spans `rg_search_4` and `rg_search_3`)
2. `rg_search:a195264dd90c` (40 rows; spans `rg_search_4` and `rg_search_3`)
3. `rg_search:49e8a004f19b` (36 rows; spans `rg_search_4` and `rg_search_3`)

### 4) Historical ambiguity-risk residue
- Hard-block ambiguity is clean.
- Residual lineage risk remains concentrated in `i3_adapt_*` families, especially `i3_adapt_p0_read_file_1` (multi-tool + remediation history).

## Surgical Trim Proposal (No Execution Yet)
Total proposed reduction: `31` targeted rows (cap-equivalent to existing 12% simulation).

### Family A: `i3_adapt_p0_read_file_1` (remove 27)
Rationale:
- Largest mass concentration + strongest memorization-risk candidate.
- Remove only low-incremental `read_file` clones from non-remediated imperative-line prompts.
- Preserve all ambiguity-remediated rows and all `rg_search` rows in this family.

Proposed trim clusters (exact prompt groups):
1. `Read /opt/ai-stack/.../service.py line range 1-25 ...` trim `9` (13 -> 4)
2. `Read /opt/ai-stack/.../service.py lines 1-25 ...` trim `6` (10 -> 4)
3. `Show /opt/ai-stack/.../service.py lines 1-25 ...` trim `5` (9 -> 4)
4. `Read /mnt/services/.../service.py line range 1-25 ...` trim `3` (7 -> 4)
5. `Open /mnt/services/.../service.py lines 1-25 ...` trim `3` (6 -> 3)
6. `Show /mnt/services/.../service.py lines 1-25 ...` trim `1` (4 -> 3)

Guarded preservation constraints:
- Preserve `all 55` ambiguity-remediation rows.
- Preserve `all 43` `rg_search` rows (multi-tool lineage evidence retained).
- Preserve all `task_narrative` rows in this family.
- Preserve at least one row per target payload and per skeleton family.

### Family B: `i3_adapt_p0_rg_search_4` (remove 4)
Rationale:
- Second mass-concentration offender.
- Remove from highest-frequency lexical clones only; preserve all operational pattern classes.

Proposed trim clusters:
1. `Use rg_search in /mnt/services/.../agent.py for pattern "tool_calls" ...` trim `3` (15 -> 12)
2. `Find in /opt/ai-stack/.../agent.py for pattern "tool_calls" ...` trim `1` (13 -> 12)

Guarded preservation constraints:
- Preserve both target payload path variants.
- Preserve all 5 skeleton classes.
- Preserve all 10 prompt families (no prompt family elimination).

## Expected Post-Trim Telemetry (Simulated, No Mutation)
Assuming only the proposed 31-row targeted trim:

### Concentration profile
- Targeted rows: `799 -> 768`
- `i3_adapt_p0_read_file_1`: `122 -> 95` (15.269% -> 12.370% post-trim share)
- `i3_adapt_p0_rg_search_4`: `99 -> 95` (12.390% -> 12.370% post-trim share)

### Diversity/concentration deltas
- Family-entropy delta: `+0.02778` bits (matches prior 12% cap simulation envelope).
- Targeted prompt uniqueness ratio: `0.128911 -> 0.134115` (`+0.005204`).
- Top-1 skeleton share (targeted): `0.052566 -> 0.050781` (`-0.001785`).
- `i3_adapt_p0_read_file_1` effective-diversity ratio: `0.115462 -> 0.139779`.
- `i3_adapt_p0_rg_search_4` effective-diversity ratio: `0.097658 -> 0.102960`.

### Semantic-variation note
- Existing nearest-neighbor semantic-variation metric remains `~0` in these families because exact-neighbor duplicates still exist.
- This is a metric limitation, not evidence that all useful variation is absent.

## Why This Is Not Blind Deletion
Deletion priority is deterministic and cluster-aware:
1. only families above 12%-equivalent cap,
2. only high-frequency exact prompt clusters,
3. only rows with lowest incremental diversity contribution,
4. explicit preservation of ambiguity-remediated and multi-tool lineage exemplars,
5. no elimination of rare/edge prompt families.

## Recommendation: Trim Mode Choice
Recommendation: **pure surgical trimming is sufficient for this pass**.

Why:
- Meets the explicit “12% cap-equivalent” concentration objective with low dilution risk.
- Avoids introducing new ambiguity risk via paraphrase/augmentation in a governance-critical phase.
- Preserves existing remediation and edge-case behavior while reducing memorization pressure.

Defer augmentation/paraphrase unless post-trim human review still shows coercive local-template dynamics.

## Proposed Post-Remediation Telemetry Targets
Use these as review targets (not gate changes):
1. Max family size target: `<=95` rows for any targeted family (12%-equivalent absolute cap from baseline targeted cardinality).
2. Effective-diversity ratio floor for high-mass targeted families (`>=70` rows): `>=0.10`, stretch target `>=0.13`.
3. Semantic-variation floor:
- Nearest-neighbor metric: non-degradation (`>=0.0` in current telemetry regime).
- Pairwise lexical variation proxy (`1 - mean_pairwise_jaccard`): maintain `>=0.20` for high-mass targeted families.
4. Acceptable entropy delta range:
- family entropy delta: `+0.02` to `+0.05` bits,
- normalized prompt-entropy delta: `>=0.0` to `+0.01`.

## Governance Limits / Unknowns
What remains unknown even after rebalance:
1. Lexical telemetry does not fully measure intent-level semantic breadth.
2. Concentration reduction does not guarantee parseability/schema coupling improvement under training.
3. Small single-template families (`i3_long_*`, `i3_read_literal_*`, `i3_rg_readstyle_*`) remain clone-prone by design and may still contribute local memorization pressure.
4. No forward evidence yet on whether reduced family mass shifts schema-spill risk versus parse-anchor over-imprinting.

Residual risk after proposed trim:
- latent semantic aliasing may persist,
- local-template coercion can still emerge during training,
- high-share `i3_adapt_*` families remain dominant even after cap-equivalent reduction.

## Final Proposal Summary
- Recommended action: execute a controlled, deterministic 31-row surgical trim exactly as specified above.
- Do not mutate ambiguity-remediated exemplars or multi-tool lineage coverage.
- Re-run concentration telemetry + ambiguity audit + preflight validation immediately after trim before any training review decision.
