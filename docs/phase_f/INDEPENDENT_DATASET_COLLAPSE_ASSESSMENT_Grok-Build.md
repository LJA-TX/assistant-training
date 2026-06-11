# Independent Assessment: Dataset Collapse Hypothesis

## Executive Summary

**The collapse finding is real.** I independently verified that Dataset v1.0’s train tool-positive slice is 972 identical rows: one prompt, one target, one case ID (`p0_rg_search_3`), one tool (`rg_search`). Phase F did not overstate this.

**But collapse alone does not sufficiently explain the Phase E i3 performance profile.** The i3 adapter evaluated in Phase E was trained on `dataset_v1_0_stage_b_recovery_i3_train.jsonl`, which already remediated the collapse (154 unique prompts, 74 case IDs, 23 tools). i3 still achieved 2.5% exact JSON validity and 3.57% tool-name/argument accuracy. That means other factors — thin-source oversampling, output-mode competition in the training mix, model capacity, and strict eval — are at least co-equal causes.

**Verdict:** The collapse is a project-defining dataset defect for v1.0 and `stage_b_train`, but Phase F overreaches when it maps that defect directly onto the Phase E i3 results. The recommended external-data direction (xLAM/APIGen + When2Call) is sound, with caveats.

---

## Dataset-Collapse Assessment

### 1. Is the finding factually correct?

**Yes.** Direct inspection of `data/v1_0/dataset_v1_0_train.jsonl` confirms:

| Metric | Phase F claim | Independent verification |
|---|---:|---:|
| Train tool-positive rows | 972 | 972 |
| Unique prompts | 1 | 1 |
| Unique targets | 1 | 1 |
| Unique case IDs | 1 (`p0_rg_search_3`) | 1 (`p0_rg_search_3`) |
| Unique tools | 1 (`rg_search`) | 1 (`rg_search`) |

The same collapse propagates into `dataset_v1_0_stage_b_train.jsonl`: **1,404 / 1,404** tool-positive rows are identical (65% of Stage B training).

Val tool-positive is broader (108 rows, 31 prompts, 8 tools), matching Phase F.

### 2. How severe is it?

**Critical for any training path using v1.0 or `stage_b_train`.**

- 45% of top-level train rows (972/2,160) are one exemplar.
- 65% of Stage B train rows (1,404/2,160) are the same exemplar.
- Upstream sources are **not** starved: 144 deduplicated tool rows across 44 case IDs and 26 tools come from three JSONL sources totaling ~1,592 raw rows.
- Eval sets are appropriately diverse: heldout validation has 90 unique prompts and 17 tools; tool holdout has 8 tools across 8 held-out case IDs.

The collapse is a **pipeline artifact**, not an upstream data absence.

### 3. How did it happen?

Replicating `scripts/build_dataset_v1.py` with seed `20260525` reproduces the exact survivor:

```
144 deduped tool rows
  → 8 case IDs held out for tool_holdout eval
  → 136 non-holdout exemplars remain
  → 100 removed for heldout_validation (without replacement)
  → 36 exemplars remain
  → val samples 108 with replacement, capturing 35/36 unique fingerprints
  → train_tool_pool = 1 exemplar (p0_rg_search_3)
  → train samples 972 with replacement from that 1 row
```

The causal chain is:

1. Aggressive deduplication by `(prompt, tool_name, arguments)` fingerprint.
2. Large heldout draw (100 of 136 non-holdout exemplars).
3. Val fingerprint exclusion that removes almost all remaining diversity.
4. With-replacement oversampling of the single survivor.
5. No minimum-diversity guardrail anywhere in the pipeline.

### 4. Was it intentional?

**No.** Nothing in the charter, build script, or summaries indicates deliberate single-exemplar saturation. The script enforces category balance and leakage control, but not tool-positive diversity. This is an emergent defect from eval-isolation logic interacting with a small deduplicated pool.

### 5. Alternative interpretations?

| Interpretation | Assessment |
|---|---|
| “Upstream data lacks tool diversity” | **False.** 26 tools and 44 cases exist before the build pipeline collapses them. |
| “Only train collapsed; val is fine” | **True but incomplete.** Val is more diverse, but Stage B re-samples from the collapsed train pool at 65% tool-positive weight. |
| “Eval diversity masks train collapse” | **Partially true.** Zero train/heldout prompt overlap is good governance, but it also means the model never sees eval-distribution prompts during training. |
| “i3 recovery already fixed this” | **True for i3 training only.** Recovery i3 has 23 tools and 154 prompts. v1.0 and `stage_b_train` remain collapsed. |

---

## Causal Assessment

Phase F argues:

```text
Poor tool-name / argument / exact-JSON metrics
        ↓ caused largely by ↓
Collapsed tool-positive diversity in Dataset v1.0
```

### Rating by training path

| Training corpus | Causal strength | Rationale |
|---|---|---|
| `dataset_v1_0_train.jsonl` / `stage_b_train` | **Strongly Supported** | 1 exemplar cannot teach 17–26 tool families or argument variation. |
| `stage_b_recovery_i3_train` (actual Phase E i3 corpus) | **Plausible But Unproven → Weak** | Diversity was restored, yet i3 still scored 5/140 correct tool rows. |

### Evidence that collapse is necessary but not sufficient

**i3 recovery dataset stats** (`dataset_v1_0_stage_b_recovery_i3_train.jsonl`):

- 1,404 tool-positive rows from 122 curated source rows (heavy oversampling).
- 23 tools; top tools: `rg_search` (470), `read_file` (249).
- Zero prompt/target overlap with heldout eval (by design).

**i3 eval results** (Phase E revalidation):

- 5/200 rows exactly valid; 5/140 tool-expected rows correct.
- Heldout: 5/100 exact (including 52 `rg_search` eval rows).
- Tool holdout: 0/40 exact.
- No-call: 1.0; wrapper leakage: 0.0.
- Dominant failure modes: direct-answer substitution (45), scalar substitution (43), near-canonical wrapper drift (44) — not “wrong tool selected from a diverse menu.”

If collapse were the dominant cause, i3’s 470 `rg_search` training examples should have produced much better `rg_search` exact-match rates. It did not. The model is failing to emit tool-call JSON at all in most cases, not merely picking the wrong tool.

### Overall causal rating

**Plausible But Unproven** as the primary explanation for Phase E i3.

- **Strong** for v1.0 as a training artifact and for explaining why `stage_b_train` is unfit.
- **Insufficient** for explaining i3’s measured profile, because i3 already trained on a diversified recovery corpus and still failed.

---

## Alternative Explanations

Ranked by likely contribution to the Phase E profile:

### 1. Output-mode competition in training mix (High)

Stage B i3 is 65% tool-positive but 35% teaches text responses (`no_call_direct`, `runtime_alignment`, `refusal_policy`, `adversarial_malformed`). The dominant eval failures are text substitutions, not wrong-tool errors. The model learned restraint and no-call discipline (1.0 correctness) more reliably than tool-call commitment.

### 2. Thin-source oversampling despite surface diversity (High)

i3 expands 122 curated rows into 1,404 tool-positive examples via resampling. Surface diversity (154 prompts) masks a shallow pool. Repetition skew (`rg_search` 33%, `read_file` 18%) may not provide enough argument-schema variation for strict exact-JSON eval.

### 3. Model-capability / training-methodology limits (Medium–High)

8B base + QLoRA LoRA (r=16) on structured JSON tool calls is a hard task. i3 improved invalid-JSON rate (base 70% → i3 28% aggregate on tool rows) but exact validity remained near zero. Format recovery and exact canonical compliance appear to be different learning problems.

### 4. v1.0 build-pipeline collapse (High for v1.0; N/A for i3)

Real and severe, but i3 explicitly bypassed it. Still matters because v1.0 remains the canonical dataset manifest (`dataset_v1_0_summary.json` referenced by the eval manifest).

### 5. Evaluation strictness and distribution shift (Medium)

Eval requires exact JSON validity with zero train/heldout prompt overlap. This is appropriate governance, but it sets a high bar that repetition-heavy training cannot clear without broader prompt coverage.

### 6. Runtime-schema mismatch (Medium)

i3 recovery applied canonicalization and compact JSON shaping. Residual `invalid_schema` (51/100 heldout rows) suggests schema conformance — not just tool identity — remains a problem independent of collapse.

### 7. Masking issue (Low)

`assistant_only_loss` + `mask_user_and_system_tokens` is standard and unlikely to be the primary blocker.

### 8. Evaluator bug (Low)

Phase E established a reconciled, reproducible eval contract. Metrics are internally consistent across base and i3 runs.

---

## Dataset Strategy Critique

Phase F recommends xLAM/APIGen (primary), When2Call (co-primary), APIGen-MT and ToolACE (secondary).

### Strengths

- **xLAM/APIGen:** Best match for tool-name, argument, and exact-JSON gaps. CC BY 4.0, verification pipeline, broad API coverage. Directionally correct.
- **When2Call:** Appropriate for preserving no-call strength. No-call is already 1.0; this is insurance, not the primary gap fix.
- **BFCL exclusion:** Correct. Benchmark contamination risk is real.
- **Incremental v1.1 framing:** Preserves working runtime/no-call/refusal structure instead of full redesign.

### Weaknesses and blind spots

1. **Misses the i3 confound.** Phase F attributes the i3 profile to v1.0 collapse, but i3 trained on a recovery dataset that already diversified tool positives. External augmentation may help, but Phase F does not explain why internal recovery was insufficient.

2. **Underweights the build-pipeline defect.** Upstream already has 144 diverse exemplars. A diversity floor in `build_dataset_v1.py` could recover substantial internal signal without external dependencies. Phase F jumps to external corpora without acknowledging this cheaper internal fix.

3. **Oversampling risk persists.** Adding xLAM rows into the same resampling pipeline without diversity guardrails could recreate skew in a larger pool.

4. **When2Call as co-primary may be mis-prioritized.** No-call is already saturated at 1.0. Co-primary weight on When2Call risks reinforcing text-mode responses at the expense of tool-call commitment.

### Licensing, contamination, implementation risks

| Source | Concern | Severity |
|---|---|---|
| APIGen-MT | CC BY-NC 4.0 | Medium–High if downstream distribution is needed |
| xLAM/APIGen | Canonicalization to runtime schema; partial-release constraints | Medium |
| ToolACE | Agentic style drift, wrapper/prose regression | Medium |
| Glaive | Thin provenance, conversational noise | Medium–High |
| ToolBench | Legacy conversational style | High regression risk |
| Any external source | Eval contamination if not leakage-checked against frozen manifest | Medium |

### Superior or complementary alternatives

Phase F’s external-data plan is reasonable, but equally or more urgent:

- **Fix the v1.0 build pipeline** with minimum tool/case/fingerprint diversity floors before heldout/val exclusion.
- **Expand internal alias/paraphrase generation** from the existing 144-row pool (the project already has `allaliases` sources).
- **Ablate output-mode mix** — test whether reducing non-tool slices or adding explicit “must emit tool_calls JSON” contrastives improves commitment rate.
- **Tool-commitment failures first** — the failure profile suggests the model abandons tool-call mode; more tool diversity alone may not fix that.

---

## Recommendation

### Agree With Caveats

| Finding | Verdict |
|---|---|
| Dataset v1.0 train tool-positive collapse is real | **Agree** — independently verified |
| Collapse is severe and pipeline-caused | **Agree** |
| Collapse makes v1.0 / `stage_b_train` unfit for tool-generalization training | **Agree** |
| Collapse sufficiently explains Phase E i3 performance | **Disagree** — i3 used recovery data with 23 tools and still failed |
| External augmentation (xLAM + When2Call) is the right strategic direction | **Agree with caveats** — xLAM is well-targeted; When2Call is lower priority; fix build pipeline too |
| No serious training until dataset evolution | **Agree** — but “evolution” should include internal pipeline repair, not only external ingestion |

---

## Confidence Level

| Claim | Confidence |
|---|---|
| Collapse finding is factually correct | **Very High (95%+)** — reproduced by direct artifact inspection and build-script simulation |
| Collapse is pipeline-caused, not upstream-starved | **Very High (90%+)** |
| Collapse alone explains Phase E i3 profile | **Low–Medium (35%)** — confounded by i3 recovery dataset |
| Collapse explains poor performance on any v1.0/`stage_b_train` training run | **High (85%)** |
| Multi-causal explanation (mode competition + thin pool + model limits + collapse) | **High (80%)** |
| xLAM/APIGen as primary external source is directionally correct | **Medium–High (75%)** |
| Phase F “no-go on training until v1.1” is prudent | **High (85%)** |

---

## Bottom Line

> **Is the dataset-collapse finding real?**
> **Yes.** It is not a summary artifact. It is reproducible, mechanistically explained, and severe.

> **Is it sufficient to explain the observed Phase E performance profile?**
> **No.** Phase E i3 did not train on the collapsed v1.0 tool-positive slice. It trained on a recovery corpus with meaningful tool diversity and still achieved ~3.6% tool accuracy. Collapse is a necessary part of the v1.0 story and a critical defect to fix, but the Phase E profile implicates additional causes — especially tool-call commitment failure, thin-source oversampling, and model/training limits — that external data alone may not resolve without pipeline and curriculum changes.

## Sources Used

- `data/v1_0/dataset_v1_0_train.jsonl`
- `data/v1_0/dataset_v1_0_val.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_train.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json`
- `data/v1_0/dataset_v1_0_summary.json`
- `data/v1_0/dataset_v1_0_leakage_report.json`
- `scripts/build_dataset_v1.py`
- `configs/lora/stage_b_llama31_8b_base_v1_i3.config.json`
- `evals/runs/phase_e_i3_revalidation_20260610_r1/summary.json`
- `docs/phase_f/CURRENT_DATASET_ASSESSMENT.md`
- `docs/phase_f/BEHAVIORAL_GAP_MAPPING.md`
- `docs/phase_f/PHASE_F_CLOSURE_AND_DATASET_EVOLUTION_ASSESSMENT.md`
- `docs/phase_e/I3_ADAPTER_REVALIDATION_REPORT.md`
