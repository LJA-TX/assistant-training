**Adversarial Governance & Failure-Mode Review: Stage B `i8` Pre-Training Checkpoint**  
**Repository**: `LJA-TX/assistant-training` @ commit `d5852295f8c8f56a9398eb3d2e756ef73d3b8245` ("docs: finalize i8 pre-training governance checkpoint")  
**Date of review**: 2026-05-26 (artifacts current as of this commit)  
**Scope**: External adversarial review only — no implementation, refactoring, or pipeline changes. Focus on hidden risks that could survive current governance.

I read the core artifacts directly:
- `docs/lineages/i8_pre_training_governance_snapshot.md`
- `docs/lineages/i8_bounded_implementation_scaffold.md`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i8_summary.json`
- `manifests/reports/stage_b_v1_i8_prompt_ambiguity_audit.json`
- `manifests/reports/stage_b_v1_i8_contamination_audit.json`
- Supporting reports (preflight_validation, human_review_package, intervention_declaration templates, prior lineage docs for i3–i7 context)

Training has **not** executed. All gates remain closed (`approved_to_train = false`). Ambiguity remediation is complete and passes hard-block audits.

### 1. Source-Case Family Concentration Risk

**Yes — this risk is real, explicitly exposed by diagnostics, and only partially mitigated.**

From `stage_b_v1_i8_prompt_ambiguity_audit.json` (source_case_divergence_groups):

- `i3_adapt_p0_read_file_1`: **122 rows**, 7 distinct targets, **2 distinct tools**, 15 distinct prompts, 7 distinct tool-argument pairs.
- `i3_adapt_p0_rg_search_4`: 99 rows, 2 targets, 1 tool...
- Multiple other `i3_adapt_p0_*` families in the 70–99 row range with similar multi-target/tool divergence pre-remediation.

The summary confirms 2160 train rows total; targeted intervention touched only 719 rows (with 51 prompt changes for ambiguity). The 122-row family alone is ~5.6% of the train set and was part of the single conflicting prompt group that triggered remediation (55 rows changed, mostly `rg_search`).

**Severity**: Medium-High for *localized* overfitting.  
**Likely behavioral consequences**:
- Latent memorized routing: the model learns source_case-specific surface patterns (or even implicit family IDs) rather than pure semantic intent for `rg_search` vs `read_file`.
- Brittle generalization: strong performance on high-frequency i3_adapt variants, degraded or unstable behavior on novel but semantically similar prompts outside these families.
- Subtle coupling risk: even with ambiguity hard-blocks now at zero, gradient updates during training could re-amplify the pre-remediation divergence signals if the families remain heavily over-represented.

**Do current diagnostics sufficiently expose it?** Partially. The ambiguity audit and source_case_divergence_groups are excellent and directly surface the problem (this is a governance strength). However, they are *static counts*. They do not yet include:
- Intent clustering / embedding-based effective diversity within these families.
- Family-specific holdout performance projections.
- Memorization probes (e.g., repeated near-identical variants).

The anti-homogenization metrics (targeted top-1 skeleton share **0.052566**, top-3 **0.147685**, dominant style **0.484355**) pass cleanly, which is reassuring for *global* flattening but insufficient for *family-local* memorization.

### 2. Local-Template Coercion Risk

**Challenging the assumption aggressively: the risk is plausible and under-measured.**

The parse-anchor strategy (mostly "existing_anchor_signal" on 629/719 targeted train rows, with bounded append/prepend on others) + style-bucket/skeleton/prompt-length diagnostics are in place and currently passing. Intervention was deliberately localized and diversity-preserving modes were used.

However:
- 51 prompt changes were still required for ambiguity remediation (append_clause dominant).
- Dominant style share in targeted rows is already ~48.4%.
- The design explicitly adds "parse-safety language" and corrective clauses.

**Core assumption under challenge**: "Structural parse improvements + low skeleton concentration = genuine semantic tool selection is preserved."

This is brittle. Parse anchors and repeated corrective clauses can train the model to prefer *safe serialization habits* (explicit tool names, rigid JSON structures, anchor-triggered formatting) over deep semantic inference about user intent. Because the intervention is localized to `rg_search`/`read_file`, this coercion risk is concentrated exactly where we are trying to recover behavior — creating a potential local minimum that looks good on structural metrics but narrows inferential flexibility.

The low top-1 skeleton share is positive, but skeleton metrics are coarse proxies. They do not directly measure whether the model is still doing *intent reasoning* vs. pattern-matching to anchor patterns.

**Verdict**: Current shaping *could* unintentionally reward safe serialization. The governance correctly flags "parse-anchor over-imprinting risk" in the snapshot, but the diagnostics do not yet include ablation or semantic-drift telemetry to quantify it.

### 3. Evaluation Blind Spots

Current topology is strong on:
- Parseability / schema correctness
- Overlap/contamination (zero on heldout/tool_holdout for prompt/target/source_case)
- Concentration/homogenization (style buckets, skeletons)
- Ambiguity hard-blocks (now zero)

**Major blind spots that could still slip through**:
- **Semantic narrowing / reduced inferential flexibility**: Stronger structural consistency on targeted tools does not guarantee preserved (or improved) semantic breadth. The model could become a better *dispatcher* for `rg_search`/`read_file` while losing nuance on edge cases, compositional use, or novel phrasings.
- **Tool over-selection or argument rigidity**: Especially if parse anchors bias toward explicit/structured outputs.
- **Prompt brittleness outside concentrated families**: High reuse in `i3_adapt_p0_*` families means low-frequency or out-of-family prompts are under-tested.
- **Subtle spill or re-coupling**: i6/i7 showed oscillatory parse/schema dynamics. Localized intervention + training dynamics could reintroduce this even if pre-train audits pass.
- **No canonical eval execution yet** for this i8 checkpoint (explicitly noted in governance snapshot).
- **Long-context / compositional / multi-turn tool use** not stressed in current structural metrics.
- **Post-remediation semantic aliasing**: Near-equivalent intents that are no longer *identical* prompts could still drift.

These are classic "structural metrics pass, behavioral regression hides" failure modes.

### 4. Ambiguity Doctrine

**The current doctrine is correct and appropriate for this stage.**

Forbidding:
- identical prompt → multiple tools/targets
- identical `(prompt, tool)` → multiple argument payloads

...is the right hard constraint here. Prior lineage (i4/i5 overconstraint collapse + semantic flattening; i6/i7 oscillatory coupled schema-failure) demonstrates that ambiguous training signals are destabilizing and lead to parse/schema regressions.

**Tradeoffs**:
- *Risk of overly deterministic dispatcher*: Real, especially if doctrine is applied too broadly or if remediation over-corrects. A pure semantic router benefits from some controlled ambiguity to learn robust intent boundaries.
- *Benefit at this stage*: Clean training signal for parseability recovery without reintroducing the exact failure modes that collapsed earlier iterations. Remediation was bounded (only 55 rows, targeted families only).

**Verdict**: Keep the doctrine for i8. It can (and should) be relaxed in later stages *after* stability is proven on canonical evals and generalization probes. The current approach avoids the worse failure mode (unstable/collapsing training).

### 5. Governance / Diagnostics Adequacy

**Overall**: Genuinely robust for a pre-training hygiene and gate system, not overly complex given the failure history, but still has brittle assumptions and telemetry gaps.

**Most valuable existing diagnostics**:
- `source_case_divergence_groups` in the ambiguity audit (directly surfaces concentration + pre-remediation divergence).
- Targeted intervention tracking (rows changed, anchor modes, ambiguity remediation details).
- Overlap/contamination audits (strict zero on key evals).
- Style-bucket + skeleton concentration metrics (currently passing cleanly).
- Explicit remaining risks section in the governance snapshot.

**Brittle assumptions**:
- Localized intervention will not produce global side-effects or re-coupled dynamics (history of i6/i7 suggests coupling is easy to re-trigger under training).
- Structural diversity metrics (style/skeletons) are sufficient proxies for "genuine semantic tool selection."
- Zero post-remediation ambiguity hard-blocks + passing concentration metrics = low latent memorization/overfitting risk.
- Pre-train structural audits will catch behavioral regressions that only appear under gradient descent or on canonical evals.

**Additional diagnostics I would add** (prioritized):
1. **Source-family intent clustering / effective diversity** (embedding-based within high-row source_cases like `i3_adapt_p0_read_file_1`).
2. **Pre/post-intervention semantic drift analysis** (prompt embedding similarity or nearest-neighbor shifts for remediated rows).
3. **Family-specific holdout confusion / generalization probes** (targeted tool performance on held-out variants of the high-concentration families).
4. **Parse-anchor impact ablation** (measure behavioral delta on non-targeted tools/behaviors when anchors are present vs removed).
5. **Memorization / repeated-variant probes** in the review package.
6. **Projected spill / re-coupling telemetry** (even if lightweight) before training authorization.

### 6–8. Synthesis & Recommendation

**1. Overall assessment of i8 readiness for bounded training review**  
**Safe to proceed to bounded training review** from a governance and data-hygiene perspective. The checkpoint correctly documents remaining risks, all hard gates (ambiguity, contamination, diversity) are passing or explicitly flagged, and the localized bounded design reflects hard lessons from i4–i7. Training has not begun; approvals remain closed.

**2. Most serious remaining risks**  
- High source-case family concentration (e.g., 122-row `i3_adapt_p0_read_file_1` with multi-target/tool history) creating latent memorized routing or local semantic overfitting in the exact tools being recovered.
- Subtle parse-anchor / local-template coercion narrowing semantic flexibility even while structural metrics pass.

**3. Hidden failure modes likely still possible**  
- Re-emergence of coupled parse/schema oscillatory dynamics under actual training (even localized).
- Semantic narrowing or reduced inferential flexibility on edge/ novel prompts.
- Prompt brittleness and degraded performance outside the high-frequency i3_adapt families.
- Over-deterministic tool selection that looks like improved parseability but is actually shallower routing.

**4. Evaluation blind spots**  
Lack of semantic/intent-based metrics, embedding drift, family-specific generalization probes, and executed canonical evals for this checkpoint. Structural metrics are necessary but not sufficient for behavioral robustness.

**5. Governance strengths**  
Fail-fast multi-layer audits, explicit exposure of source-case concentration, bounded localized intervention doctrine, co-primary spill-guard interpretation, and transparent documentation of remaining risks in the governance snapshot.

**6. Governance weaknesses**  
Reliance on structural proxies that may not catch semantic coercion or latent memorization; high family concentration tolerated without further mitigation (subsampling/augmentation); heavy pre-train focus with limited projection of training dynamics or post-train telemetry.

**7. Additional telemetry/diagnostics recommended**  
See section 5 above — especially family intent clustering, semantic drift, family holdout probes, and parse-anchor ablation.

**8. Recommendation**  
**Proceed toward bounded training review**, with targeted light revisions before execution:
- Consider modest diversification or row capping on the highest-concentration source_cases (e.g., `i3_adapt_p0_read_file_1`) to reduce memorization surface.
- Integrate the additional semantic/family-specific diagnostics into the preflight/review package.

**Do not pause for deeper redesign** — the bounded localized approach is the correct lesson from prior iterations. The governance system is strong enough to support controlled execution with enhanced monitoring. Execute canonical evals early in the bounded phase and maintain tight spill/parse telemetry.

This is a serious, high-quality checkpoint. The remaining risks are visible and manageable rather than hidden. The primary threat vector is over-reliance on the current structural metrics masking localized overfitting or coercion during actual training. Bounded execution with the recommended additions is the rational next step.
