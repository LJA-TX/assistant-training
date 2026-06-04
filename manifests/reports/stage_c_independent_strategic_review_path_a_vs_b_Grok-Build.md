# Independent Strategic Review — Path A vs Path B

**Repository:** /opt/ai-stack/assistant-training  
**Assessment Date:** 2026-06 (independent, direct evidence review)  
**Posture:** All conclusions formed from direct inspection of artifacts, code, reports, fixtures, ledgers, scientific outputs, process docs, and review bundles. No reliance on external narrative; Codex package outputs, determinations, and summaries were read as part of the record but not granted presumptive correctness. The task is strictly assessment: what the completed Stage C record (through Package 6A and subsequent C9/C10 activity) justifies as the next step for the blocker-oriented branch. No implementation performed. No files edited. Focus: evidence sufficiency, risks, and recommendation between governance formalization (Path A) and additional evidence gathering (Path B).

**Primary Evidence Sources (direct review, non-exhaustive):**
- Stage B closure and foundation: `docs/convergence/STAGE_B_CLOSURE_AND_STAGE_C_TRANSITION_ASSESSMENT_Grok-Build.md`, `STAGE_B_COMPLETION_DETERMINATION.md`, `STAGE_B_WP8_*` package reviews / coverage / reconciliation summaries / fixture indexes, `manifests/reports/stage_b_wp8_validation/fixtures/`, WP8 99-scenario catalog, Stage B contracts (EVAL_REDESIGN_CONTRACTS, WP3_FAMILY_A_SCORER_EVIDENCE_CONTRACT, etc.), `stage_b_independent_methodology_review_Grok-Build.md`, probe artifacts (geometry ledgers, digests, scientific assessments, gates).
- Regimen extraction and branch demonstrations: `docs/convergence/STAGE_C_PACKAGE_3C_REGIMEN_RETROSPECTIVE_AND_REUSABILITY_ASSESSMENT.md` (and supporting 1x/2x packages), `STAGE_C_PACKAGE_4A_SECOND_SURFACE_SELECTION_AND_REGIMEN_APPLICABILITY_ASSESSMENT.md`, `STAGE_C_PACKAGE_4B_B1_GOVERNED_MEMBERSHIP_COVERAGE_QUALIFICATION.md`, `STAGE_C_PACKAGE_4C_B1_EVIDENCE_ACQUISITION_FEASIBILITY_ASSESSMENT.md`, `STAGE_C_PACKAGE_5A_DIRECT_ANSWER_SUBSTITUTION_SURFACE_ENTRY_ASSESSMENT.md` (and acceptance), `STAGE_C_PACKAGE_5B_DIRECT_ANSWER_SUBSTITUTION_BLOCKER_PERSISTENCE_ASSESSMENT.md` (and bundle runs + persistence assessment), `STAGE_C_PACKAGE_5C_DIRECT_ANSWER_SUBTYPE_COMPLETENESS_INVESTIGATION.md`, `STAGE_C_PACKAGE_5D_SCORER_COMPLETENESS_VERSUS_GOVERNANCE_PRESERVATION_ASSESSMENT.md`, `STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md` (and acceptance + summary), `STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md` (and acceptance + implementation summary).
- Evidence bundles and runtime artifacts: `manifests/reports/stage_c_package2a_read_file_exact_valid_gate_evidence_run_*.json`, `stage_c_package5b_direct_answer_blocker_bundle_run_a.json`, `stage_c_package5b_direct_answer_blocker_bundle_run_b.json`, `stage_c_package5b_direct_answer_blocker_persistence_assessment.json`, canonical eval summaries, evaluator emission in `scripts/eval_canonical_manifest.py` (failure_profile, read_file_*_exact_valid, direct_answer_substitution, symbol_name_membership, anchor_bucket, subtype logic).
- Process and governance infrastructure: `AGENTS.md` (dispatcher routes including migration_gate, architecture_or_process_assessment, slice_execution, readiness_or_closure_review), `docs/process_infrastructure/` (all checklists and templates), `docs/convergence/STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md`, `docs/appendix_a_operational_execution_contract_v3a.md`, `docs/goal_charter_v5a.md`.
- Later Stage C activity (post-6A context): `local_review_bundles/` (STAGE_C9_BLOCKER_CLOSURE_PLANNING_ASSESSMENT_REVIEW.zip containing `STAGE_C9_BLOCKER_CLOSURE_PLANNING_ASSESSMENT.md` + readiness determination; `stage_c9_post_blocker_reassessment_review.zip` containing `STAGE_C9_POST_BLOCKER_REASSESSMENT.md` + migration readiness determination; C9-A/B/C slice reviews; stage_c10* bundles; STAGE_C0_EVALUATOR_IMPLEMENTATION_ENTRY_CONTRACT_LOCK artifacts; C7/C8 detector projection and non-authoritative adapter artifacts), `reports/stage_c6/`, related manifests.
- Current state signals: absence of any post-6A synthesized regimen document, absence of "blocker-oriented" or "conditionally adopt" references outside the 5A–6A package set, unchanged migration-disabled posture and prior surface states in later artifacts, fixture coverage of direct_answer subtypes (e.g., `a_c_002_direct_answer_substitution.json`, `a_m_002_missing_direct_answer_subtype.json`).

**Distinction Framework (applied throughout):**  
- **Scientific outcomes:** Behavioral results, deltas, hypothesis tests, archetype differences, reproducibility, negative or blocker characterizations tied to this model + data + corpus.  
- **Methodology outcomes:** How work was executed, instrumented, audited, reviewed, extracted (bounded packages, evidence bundles, persistence comparisons, retrospective generalization, scientific+gate process).  
- **Governance outcomes:** Doctrine (non-inference, authority of catalog/fixtures over prompts, "missing means missing", denom integrity, comparability states), preservation of boundaries, explicit attribution of governance-preserving missingness vs. implementation-path incompleteness.  
- **Infrastructure outcomes:** Code emission, fixtures, contracts, process dispatcher/templates/checklists, review bundles, reports.

---

## Project Context and Objective

The project objective evolved from an initial function-calling post-training effort to the development of a **reusable, scientifically governed post-training / evaluation / migration regimen**.

Stage A addressed runtime behavioral alignment on Llama-3.1-8B base.  
Stage B (Tool-Call Specialization) is complete and closed on its approved scope (WP8 99/99 fixture authoring and reconciliation across Family A/B1/B2 + cross-family, contracts, evidence-preservation discipline, probe scientific execution and critique). See `STAGE_B_COMPLETION_DETERMINATION.md` and the independent closure assessment. The largest Stage B deliverable — the governed fixture corpus and redesign contracts — exists precisely to drive and validate subsequent measurement and migration work.

Stage C exercises the reusable regimen on compatibility-bearing surfaces using the frozen corpus and Stage B fixtures as acceptance ground truth. Three distinct outcome branches have now been demonstrated:

1. **Alignment Branch** — Surface: `read_file_exact_valid_rate`. Outcome: full lifecycle traversal (authoritative foundation → passive governance/reconciliation → readiness `migration-ready` → gate evidence with repeated full runs + impact/rollback reviews → `gate-open` → planning authorization). Extracted as reusable template in Package 3C.
2. **Evidence-Availability Branch** — Surface: `read_file_symbol_name_exact_valid_rate`. Outcome: lifecycle entry legitimate but blocked upstream by absent governed membership declarations in the frozen corpus (0 explicit symbol_name_membership or archetype declarations); determined `viable with corpus revision`; deferred rather than abandoned. Packages 4A–4C.
3. **Blocker-Oriented Branch** — Surface: `direct_answer_substitution_count`. Outcome: lifecycle entry established on current corpus and ownership chain (5A), blocker persistence and strong reproducibility established across repeated full runs (5B, stable row identities / counts / reasons / states), blocker characterization completed (5C: 131/134 structurally incapable under current doctrine/evidence, 3 ambiguous), governance-preserving missingness separated from scorer-pathway incompleteness (5D), retrospective generalization and branch recommendation (5E). Package 6A performed the formal sufficiency assessment for regimen branch adoption.

Most recent state per Stage C Package 6A (the dedicated formal blocker-oriented regimen branch adoption assessment):
- Repository evidence is sufficient to support blocker-oriented branch formalization **at the recommendation level**.
- Best-supported recommendation = `conditionally adopt`.
- No adoption decision has been made.
- No doctrine changes have been made.
- The branch has only been exercised on one active blocker surface (Family A, direct-answer subtype incompleteness + governance-preserving missingness).
- No blocker-oriented surface has yet proceeded into later scorer-pathway planning or post-blocker state transition.

Later Stage C work (C0 contract lock, C7–C8 non-authoritative detector projection and adapter integration, C9 blocker resolution for migration artifacts, C9 post-blocker reassessment, C10 slices) continues to operate under migration-disabled posture, references the direct_answer surface in legacy delta contexts (e.g., `direct_answer_substitution_delta_gt_3`), and exercises the process infrastructure (migration_gate route, conformance and implementation summaries), but does not enact the 6A recommendation or update the standing regimen description.

---

## 1. Recommended Path

**A (Governance formalization)**

Proceed toward formal recognition of the blocker-oriented branch within the reusable Stage C regimen at the level justified by the evidence (high-level, conditional adoption). This includes an adoption decision recorded via existing process routes (e.g., `milestone_determination` or `architecture_or_process_assessment`), minimal regimen structure updates (a synthesized branch model document cross-referencing the source packages), and light integration into process documentation — all while preserving the "conditional" qualifier, the common-trunk model, and all current doctrine / migration-disabled boundaries.

Path B (pure additional evidence gathering with no formal recognition) is not recommended as the immediate next step.

---

## 2. Why

Package 6A exists specifically to answer the question "is the evidence base now sufficient for formalization of the blocker-oriented branch?" It performed the cross-package retrospective (3C success-path extraction + 4-series evidence-availability demonstration + 5A–5E blocker lifecycle), stability assessment, structure analysis, impact assessment, risk/hazard analysis, and criteria proposal. Its determinations are:

- Repository evidence is sufficient to justify high-level formalization.
- The blocker-oriented branch is a reusable regimen component, not a one-off anomaly.
- The overall regimen is best represented as a common lifecycle trunk with conditional branches (alignment / evidence-availability / blocker-oriented).
- The best-supported recommendation is `conditionally adopt` (adopt is too strong due to single-surface/family limitation and lack of post-blocker transitions; defer adoption is too weak because the branch is no longer speculative and already adds governance clarity; reject is unsupported).
- Formal adoption would improve governance clarity and future-surface evaluation discipline without requiring current doctrine changes.
- Package 6A itself performed no adoption and altered no governance or migration posture.

The 5A–5E sequence materially changed understanding at every step (entry legitimacy despite blocked readiness/gate; strong persistence/reproducibility; quantitative characterization; explicit attribution of governance-preserving vs. implementation incompleteness) without any state change on the surface. 5E explicitly recommended formal branch treatment and identified core reusable steps. The three surfaces together demonstrate that the regimen (as exercised) already handles success, evidence-absence, and stable blocked cases.

The project pattern supports formalization now:
- Stage B used closure assessment → completion determination → transition (even though scientific tool-call specialization success was not achieved; the governance infrastructure was the deliverable).
- Process infrastructure uses explicit slice execution → package review/reconciliation → readiness/closure/milestone determinations.
- 3C itself was a retrospective extraction after one successful surface; the project then deliberately tested the regimen on a second surface (4A) and a blocker surface (5A) precisely to generalize.

6A is the analogous retrospective + sufficiency gate for the now-expanded branch set. Leaving the recommendation at "justified at the recommendation level" with no decision or integration keeps the primary reusable-regimen document (3C) success-path biased and the blocker work as an implicit special case. This weakens the "reusable, scientifically governed" objective.

Path B (more surfaces / post-blocker transitions / scorer work before any formalization) can and should occur, but it does not require withholding recognition. 6A already scoped the adoption as conditional precisely to account for limited diversity and missing post-blocker evidence. Formal high-level recognition provides the governance scaffolding under which additional evidence can be gathered more consistently (future surfaces classified early as alignment / evidence-availability / blocker-oriented; mandatory steps applied explicitly).

Post-6A C9/C10 activity demonstrates that implementation-layer and migration-gate work is advancing (contracts locked, non-authoritative adapters, specific migration blockers resolved or partially resolved via C9-A/B/C, post-blocker reassessment performed). The assessment-layer understanding of how surfaces legitimately reach blocked states should be brought into equivalent explicit, reviewable, carry-forward state.

---

## 3. What Evidence Is Already Sufficient

**Multi-branch demonstration (cross-surface):**
- Alignment success path fully exercised and retrospectively extracted as reusable (3C + 1x/2x packages, repeated full-run gate evidence, impact reviews, rollback review, authorization, planning design). Surface reached `migration-ready`, `gate-open`, `planning conditionally authorized`.
- Evidence-availability constrained path (4A–4C): surface lifecycle-eligible on corpus but upstream governed membership absent (0 explicit declarations); viability assessment performed; `insufficient-evidence` / `viable with corpus revision`; explicit recommendation to defer active reuse and check evidence-acquisition feasibility for future surfaces.
- Blocker-oriented path (5A–5E): entry qualification on current authoritative artifacts/ownership (5A, "treat as active blocker-oriented stress test, not near-term migration candidate"); persistence validated with two full-run bundles showing identical row identity, blocker inventory (134 missing_evidence out of 140 tool-expected), reasons, readiness/reconciliation/guardrail states, legacy surface snapshot (`failure_profile_direct_answer_substitution_count` stable); characterization (5C: 131/134 structurally incapable under doctrine and emitted evidence, 3/134 ambiguous mixed); attribution (5D: most missingness is governance-preserving and performing intended function; real pathway-level scorer incompleteness for direct-answer/scalar subtypes remains); retrospective generalization (5E) showing the sequence is reusable and recommending formal branch.

**Reproducibility and stability:**
- 5B persistence assessment: "strongly reproducible"; manifest identity, runtime config, row-fact semantic digest, row identity, tool-expected row identity, direct_answer row ids, missing_evidence reasons, focus reconciliation/readiness, legacy surface all stable or appropriately compared. Hash equality on comparison_rows_jsonl and key governed artifacts.

**Doctrine and governance alignment:**
- All work preserved non-inference (consume emitted facts only), authority (catalog/fixtures > prompt inference), "missing means missing" (noncomputable preserved), denom integrity, comparability state separation.
- 5D explicitly separated governance-preserving missingness (do not "fix" by reconstruction) from scorer-completeness gap (future work target). This distinction is a core governance outcome.
- Direct grounding in Stage B WP8 fixtures (Family A direct_answer scenarios under all emission states, NI tests, sub-slice rules) and contracts.

**Process and infrastructure validation:**
- The 5A–5E + 6A sequence itself used the established slice/package/review/reconciliation/implementation-summary + acceptance + determination pattern.
- AGENTS.md routes, process_infrastructure templates (package_review, implementation_summary, readiness_determination, milestone_determination, closure_determination, etc.) and checklists were exercised.
- Phase 1 process infrastructure closed.
- Evidence bundles (5B) and gate-evidence bundles (2A for the alignment surface) demonstrate repeatable full-run evidence practice.

**6A synthesis:**
- Explicit sufficiency determination, one-off vs. recurring pattern analysis, single-linear vs. common-trunk-with-branches model evaluation, adoption impact (governance clarity, future-surface classification discipline, compatibility with existing branches), risk assessment (over-generalization, premature formalization, insufficient diversity, doctrine ambiguity, governance drift — all deemed manageable under conditional high-level adoption), proposed high-level adoption criteria (when to enter, minimum evidence, mandatory steps, conditional steps, exit conditions).

**Current surface state for the exemplar (stable across bundles):**
- `reconciliation: requires_future_migration`
- `readiness: migration-blocked`
- `gate: gate-blocked`
- No reopening of these states occurred or was claimed.

This body of evidence is broader and more structured than what supported the 3C reusable-regimen extraction (which was accepted as sufficient for reuse guidance on future surfaces).

---

## 4. What Evidence Is Still Missing

- **Surface diversity for the blocker branch:** Only one active blocker-oriented surface (`direct_answer_substitution_count`, Family A scorer-subtype) has been exercised end-to-end through entry, persistence, characterization, and attribution. No equivalent on Family B1 (symbol-name or other read_file archetypes), Family B2 (no-anchor), or additional Family A subtypes.
- **Post-blocker transitions:** No blocker-oriented surface has advanced from "sufficiently characterized / preserve blocked posture pending future pathway work" (5E determination) into an authorized scorer/evaluator planning package, a clean deferral, or a stop. The proposed exit taxonomy remains untested in practice.
- **Second independent validation of branch steps:** No second blocker surface has reached the decision point to confirm that 5A/5B/5C-like steps are reliably mandatory and 5D-like attribution is reliably conditional across different blocker etiologies.
- **Formal adoption decision and integration:** No milestone, architecture assessment, or equivalent determination records the `conditionally adopt` decision. No synthesized "Stage C Regimen Branch Model" or equivalent standing document exists that consolidates the common trunk + conditional branches (3C remains the most prominent reusable extraction and is success-path centered). No updates appear in AGENTS.md, process_infrastructure templates, or continuity docs that reflect the three-branch model.
- **Application in downstream contexts:** The blocker branch has not yet been explicitly applied or referenced in scorer-pathway planning, detector projection migration decisions, or threshold work (C9 references direct_answer_substitution in a legacy delta rule context, but the assessment-layer branch classification is not carried forward in the reviewed C9 artifacts).
- **Broader corpus or model variation:** All work is on the current frozen canonical corpus + Llama-3.1-8B base + specific dataset lineage. Generalization claims are appropriately scoped.

These gaps are exactly why 6A recommended *conditional* rather than unconditional adoption and why it scoped Package 6A as recommendation-only.

---

## 5. Risks of Acting Too Early (Path A — Formalization Now)

- **Over-generalization from limited diversity:** Formalizing a branch structure derived primarily from one Family A direct-answer subtype case risks later surfaces (especially B-family denominator or archetype cases) exposing the need for different entry criteria, additional conditional steps, or revised exit options. Revisions after formalization create governance churn.
- **Untested post-blocker exits:** The most important future use of a blocker branch is guiding *what happens after* characterization (scorer-pathway authorization, evidence-acquisition deferral, or clean stop). Without observing at least one such transition, the branch model may over- or under-specify the decision point.
- **Single-family / single-taxonomy bias:** direct_answer_substitution is a scorer-evidence / subtype-completeness blocker. B1 symbol-name cases are evidence-absence (already separated). B2 no-anchor cases involve denominator semantics and semantic-equivalence questions (visible in C9-B). A branch tuned on one may not travel well.
- **Perception / boundary erosion (even if scoped):** Explicit "conditional", "high-level only", "no doctrine change", and "migration remains disabled" language exists in 5A–6A artifacts. Nonetheless, formal recognition in standing docs could be misread by future work as license to treat blocked surfaces more permissively or to collapse readiness/gate boundaries. The project has repeatedly demonstrated scrupulous boundary preservation; early formalization slightly increases the surface area for future drift.
- **Premature rigidity in a scientific regimen:** The ethos favors evidence-driven iteration. Codifying too early could reduce adaptability before the pattern has been pressure-tested on a second blocker surface or a post-blocker handoff.

These risks are real and were explicitly enumerated in 6A itself. They are mitigated (but not eliminated) by keeping any formalization high-level, explicitly conditional, recommendation-scoped, and accompanied by clear "no change to current posture" language.

---

## 6. Risks of Waiting Too Long (Path B — No Formalization Until More Evidence)

- **Implicit special-case status for already-demonstrated value:** The 5A–5E sequence delivered concrete governance improvements (clearer surface classification, explicit persistence proof, quantitative characterization, governance-vs-implementation attribution). Without formal recognition, this remains a per-package retrospective rather than part of the reusable regimen. Future surfaces lose the scaffolding.
- **Inconsistent or reinvented process for future blockers:** Absent a formal branch, the next blocked surface that is not evidence-absent will either repeat the full 5A–5D analysis ad hoc (duplication, variable rigor) or be shoehorned into the 3C success-path template (mismatch). This directly undermines "reusable" and "scientifically governed."
- **Loss of context for the direct_answer surface itself:** 5E determined it is "sufficiently characterized" and should "remain blocked pending future scorer pathway work." When (or if) scorer-pathway or planning work is authorized for direct_answer or analogous surfaces, the disciplined characterization history and the branch context may not be systematically referenced.
- **Success-path bias in the primary regimen document:** 3C is the most developed reusable-regimen extraction. It was produced before the second and third branches were exercised. The documented "reusable migration regimen" therefore over-represents the alignment case. Delaying codification of the generalization keeps the authoritative extraction incomplete relative to what the repository has actually demonstrated.
- **Drift between assessment layer and implementation layer:** C0–C10 work (contract lock, detector projection adapters, C9 migration-blocker contracts and resolutions, post-blocker reassessments) is actively using and extending governed surfaces, including references to direct_answer_substitution in delta rules and noncomputable handling. The assessment-layer branch model that explains *why* such surfaces legitimately sit in blocked states is not yet carried forward in standing form. This creates a form of process debt.
- **Opportunity cost on governance clarity:** 6A identified specific benefits (early classification of future surfaces into alignment / evidence-availability / blocker-oriented; prevention of conflating blocker work with readiness/gate work; preservation of the missingness vs. incompleteness distinction). These benefits are deferred for every subsequent surface analyzed while the branch remains at "recommendation" status only.

Additional evidence is valuable and should be gathered, but the sufficiency threshold for *high-level conditional formal recognition* has already been crossed per the project's own 6A assessment.

---

## 7. Confidence Level

**70**

- High confidence (80–85) on factual reconstruction: the three branches, the content and determinations of 5A–5E and 6A, the reproducibility data in the 5B bundles, the fixture grounding, the process infrastructure state, the post-6A C9/C10 activity, and the absence of any adoption or synthesized branch document outside the 5A–6A set. All claims are traceable to direct file contents, bundle extractions, and code inspection.
- Medium confidence (60–65) on the strategic recommendation weighting: the repository demonstrates both "test with additional surfaces before generalizing" (deliberate choice to run 4-series and 5-series after 3C) *and* "execute determinations and closures once sufficiency is reached within bounded scope" (Stage B fixture completion, BC Phase 1 closure, C9 blocker closure determinations). The "conditionally adopt" language in 6A is the critical mitigator that makes scoped Path A lower-risk than it would otherwise be. Reasonable reviewers could weight the "gather one more surface first" consideration more heavily; 70 reflects that the balance favors formalization now under explicit conditions.

Confidence would rise with a second blocker surface reaching characterization or with an observed post-blocker transition. It is not binary; the hybrid alternative below is offered partly because it hedges the remaining uncertainty.

---

## 8. Alternative Path Not Captured by Pure A or Pure B

**Hybrid: "Conditional Adoption Gate + Evidence Acceleration under Formal Recognition" (recommended over pure A or pure B)**

Execute one bounded governance-formalization package (using the existing `milestone_determination` or `architecture_or_process_assessment` dispatcher route from AGENTS.md). Scope is deliberately narrow and recommendation-enacting rather than expansive:

- Record the formal `conditionally adopt` decision, including the exact conditions stated in 6A (continued evidence from future surfaces; single active Family A surface to date; no post-blocker transition yet observed; adoption remains high-level only).
- Produce a minimal synthesized carry-forward artifact (e.g., `STAGE_C_REGIMEN_BRANCH_MODEL_V1.md` or equivalent in convergence/ or manifests/reports/) that:
  - Describes the common foundation trunk + three conditional branches.
  - Extracts entry criteria, mandatory steps (5A/5B/5C-like), conditionally mandatory steps (5D-like when governance-preserving vs. completeness ambiguity exists), and exit options directly from 5E/6A.
  - Cross-references all source packages (3C, 4A–4C, 5A–5E, 6A) and the WP8 fixture grounding.
  - Explicitly reaffirms unchanged doctrine, non-inference, migration-disabled posture, and prior surface states.
- Make the smallest justified updates to standing process assets (e.g., a short note or optional branch-classification field in readiness_determination or package_review templates; a one-line addition under the migration_gate or architecture route in AGENTS.md). Do *not* create new mandatory checklists, new doctrine, or scorer-pathway semantics.
- Explicitly authorize (but do not require) immediate application of the now-recognized blocker-oriented branch to any newly selected candidate surfaces. This turns Path B evidence gathering into an *output* of the formalization step rather than a prerequisite, ensuring new blocker work follows the disciplined sequence under explicit branch governance.
- Schedule or note a future lightweight re-assessment (e.g., after one additional blocker surface or first post-blocker transition) to review whether the branch model requires refinement.

**Why this hybrid is superior here:**
- It enacts the governance formalization that 6A determined is justified (Path A benefit) while preserving the conditional nature and the explicit call for more evidence (Path B concern).
- It follows the project's established pattern: assessment package(s) → determination/closure artifact that authorizes bounded next work while locking boundaries.
- It provides immediate scaffolding for the next surfaces (future work will have a documented branch to classify against and steps to follow) without over-committing the model.
- It keeps implementation-layer work (ongoing C9/C10) and assessment-layer understanding in better sync.
- Risks of pure early formalization are contained by narrow scope and explicit conditionality language in the new artifact.
- Risks of waiting are reduced because the value already produced is captured in a reusable, citable form.

A lighter variant of the hybrid is to treat branch formalization as an ongoing "regimen retrospective" practice (analogous to 3C after the first success path) rather than a one-time adoption event, with 6A as the first such retrospective and a standing expectation of periodic re-assessment as the surface set grows.

Pure "defer all formal recognition until a second full blocker surface or observed post-blocker transition" is a coherent conservative alternative but forgoes the governance-clarity and consistency benefits that the project's own 6A analysis already judged to be supported by current evidence.

---

## Branch Comparison Summary (Repository Evidence)

| Dimension                  | Alignment Branch (`read_file_exact_valid_rate`) | Evidence-Availability Branch (`read_file_symbol_name_exact_valid_rate`) | Blocker-Oriented Branch (`direct_answer_substitution_count`) |
|----------------------------|--------------------------------------------------|--------------------------------------------------------------------------|-------------------------------------------------------------|
| Lifecycle entry on frozen corpus | Yes (authoritative + legacy reconciled)         | Yes (but upstream governed membership absent)                           | Yes (authoritative artifacts + ownership chain sufficient) |
| Primary blocker type       | None (proceeded)                                | Absent governed source evidence (0 declarations)                        | Mixed: governance-preserving missingness (dominant population) + scorer-pathway incompleteness |
| Key packages               | 1–3C (full traversal + retrospective)           | 4A–4C (qualification + feasibility)                                     | 5A (entry), 5B (persistence), 5C (characterization), 5D (attribution), 5E (generalization) |
| Reproducibility evidence   | Repeated full-run gate bundles                  | N/A (deferred)                                                          | Two full-run blocker bundles + persistence assessment ("strongly reproducible") |
| Current surface state      | migration-ready, gate-open, planning conditionally authorized | insufficient-evidence; viable with corpus revision; deferred           | requires_future_migration; migration-blocked; gate-blocked (stable) |
| Regimen extraction         | 3C (primary reusable template)                  | Demonstrated need for evidence-acquisition feasibility check            | 5E + 6A (reusable sequence + branch recommendation) |
| Post-6A activity           | Foundation for later migration planning         | Deferred                                                                | Referenced in C9 delta-rule and migration-blocker contexts (no branch formalization) |

---

## Process Infrastructure and Later Stage C Context

The process dispatcher (`AGENTS.md`) and `docs/process_infrastructure/` (8 checklists, 9 templates, Phase 1 closure determination) were used to execute the 5A–6A packages and continue to be used for C9/C10 migration-gate and conformance work. C9 planning and post-blocker reassessment explicitly cite Stage B closure artifacts and C0–C8 contracts as inputs. This shows the infrastructure is live and that "blocker" language in later slices refers to migration-contract blockers (adversarial no-call subset mapping, no-anchor semantic-equivalence, baseline-delta comparability gate), some of which reference the same direct_answer_substitution surface in legacy rules. The regimen assessment-layer branch model (how a surface legitimately becomes and remains a governed blocker at the evaluation surface level) has not been integrated into these later slices.

No evidence was found of any post-6A document that enacts, references, or synthesizes the blocker-oriented branch outside the original 5A–6A package set.

---

## Determinations

1. Repository evidence (through Package 6A) is sufficient to support formal recognition of the blocker-oriented branch at the high level with a `conditionally adopt` recommendation.
2. The blocker-oriented branch is a reusable regimen component (entry qualification, persistence validation, characterization, conditional attribution, explicit decision point) rather than a one-off exception.
3. The best current representation of the Stage C migration regimen is a common lifecycle trunk with conditional branches (alignment / evidence-availability / blocker-oriented), not a single linear success path.
4. The recommended immediate next step is a bounded governance formalization action (adoption decision + minimal synthesized branch model + light process integration) that preserves the conditional scoping, all current doctrine, and the migration-disabled posture.
5. Additional evidence gathering (further blocker surfaces, post-blocker transitions, scorer-pathway application) should be accelerated *under* the now-recognized branch rather than treated as a prerequisite to any recognition.
6. This review performed no adoption, no doctrine change, no implementation, and no alteration of any surface state or migration flag.

---

## Boundary Confirmation

This assessment:
- Did not adopt the blocker-oriented branch or any other branch.
- Did not modify doctrine, governance rules, scorer behavior, evaluator behavior, detector authority, threshold authority, migration flags, or prior surface determinations.
- Did not implement code, author new fixtures, or alter contracts.
- Did not reopen any readiness, gate, or planning state.
- Performed no edits to any repository file.
- Is strictly an independent strategic review based on direct artifact inspection.

All package artifacts reviewed (5A–6A and supporting) were themselves documentation-only within their declared scopes and preserved identical boundaries.

---

## Traceability

Every material claim above is traceable to one or more of the primary evidence sources listed at the top of this document (full paths under `/opt/ai-stack/assistant-training/`). Key cross-checks performed via direct `read_file`, `grep`, directory listings, and `unzip -p` extraction of review bundles. No external sources or unverified Codex narrative were used as authority.

**End of Report.**

All claims traceable to cited repository evidence. No assumptions beyond what the artifacts support. Assessment only.