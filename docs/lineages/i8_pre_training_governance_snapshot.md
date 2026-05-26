# i8 Pre-Training Governance Snapshot

## A) Current State

- Iteration: `stage_b_llama31_8b_base_v1_i8`
- Objective: recover parseability in a localized way (targeted families: `rg_search`, `read_file`) while preventing schema spill and runtime-discipline regressions.
- Parent lineage baseline: `stage_b_llama31_8b_base_v1_i3` dataset lineage (`dataset_v1_0_stage_b_recovery_i3_{train,val}.jsonl`).
- Current dataset status:
  - `dataset_v1_0_stage_b_recovery_i8_train.jsonl`: 2160 rows
  - `dataset_v1_0_stage_b_recovery_i8_val.jsonl`: 240 rows
  - `dataset_v1_0_stage_b_recovery_i8_summary.json` generated with diagnostics/audit references.
- Ambiguity remediation status: completed.
  - Initial hard-block conflict family detected and remediated by bounded prompt disambiguation on targeted rows.
  - Final ambiguity hard-block counts are all zero.
- Approval state: all gates remain closed.
  - `approved_to_generate_dataset = false`
  - `approved_to_run = false`
  - `approved_to_train = false`
  - `approved_to_promote = false`

## B) Major Governance Improvements

- Prompt ambiguity hard-block invariants are now enforced in builder + diagnostics:
  - identical prompt -> multiple targets: reject
  - identical prompt -> multiple tool names: reject
  - identical `(prompt, tool)` -> divergent argument payloads: reject
- Fail-fast protections preserved and tightened:
  - explicit generation unlock flags required
  - contamination overlap remains blocking
  - ambiguity hard-block violations terminate generation
- Anti-homogenization diagnostics expanded and preserved:
  - style buckets, skeleton concentration, prompt-length deltas
  - targeted prompt samples and risk rollups
- Contamination governance remains unchanged:
  - heldout/tool_holdout prompt/target/source_case overlap must remain zero
- Spill-guard interpretation posture remains co-primary:
  - structural validity improvements are interpreted jointly with schema-coupling risk indicators.

## C) Key Findings

- Original defect:
  - duplicate prompt groups with different targets: 1
  - duplicate prompt groups with different tools: 1
  - duplicate `(prompt, tool)` groups with different args: 1
  - concrete cross-tool conflict observed (`read_file` vs `rg_search`) for one high-frequency prompt family.
- Remediation scope:
  - 55 targeted rows disambiguated (`rg_search`: 43, `read_file`: 12).
- Current overlap status:
  - heldout overlap: zero (train/val/combined; prompt/target/source_case)
  - tool_holdout overlap: zero (train/val/combined; prompt/target/source_case)
- Current diversity/concentration status:
  - targeted style buckets: 3
  - dominant targeted style share: 0.484355
  - targeted unique skeletons: 54
  - targeted top-1 skeleton share: 0.052566
  - anti-homogenization risk flags: none
- Current ambiguity status:
  - different-target prompt groups: 0
  - different-tool prompt groups: 0
  - `(prompt, tool)` different-args groups: 0

## D) Remaining Risks

- Source-case family concentration:
  - several high-frequency source-case families remain and require ongoing monitoring.
- Latent semantic aliasing:
  - near-equivalent user intents can still drift toward neighboring tool families if not continuously audited.
- Local-template convergence risk:
  - repeated localized corrective clauses may gradually narrow prompt-surface diversity.
- Parse-anchor over-imprinting risk:
  - parse-safety language can become over-represented and potentially reduce semantic flexibility.
- Semantic narrowing despite structural gains:
  - stronger structural consistency does not guarantee equivalent semantic breadth.

## E) Current Recommendation State

- i8 is currently **safe for bounded training review** from governance/data-hygiene posture.
- i8 is **not approved for promotion**.
- i8 is **not canonized**.
- Training has **not** been executed.
- Canonical evals have **not** been executed in this checkpoint operation.
