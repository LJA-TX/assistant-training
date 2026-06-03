# Stage B Independent Methodology Review

**Repository:** `/opt/ai-stack/assistant-training`  
**Date of Review:** 2026-06 (independent synthesis from current artifacts)  
**Reviewer Posture:** Direct evidence review only. Codex execution logs, prior lessons-learned summaries, and closure determinations were read as artifacts but not treated as presumptively correct. Conclusions were formed or revised against primary sources: run artifacts, ledgers, eval summaries, detector outputs, scripts, package/reconciliation docs, and governance reviews. No redesign of geometry, no new probe proposals.

**Primary Evidence Sources Reviewed (non-exhaustive):**
- Live probe artifacts and assessments: `manifests/reports/stage_b_first_probe_scientific_assessment.md`, `stage_b_successor_probe_scientific_assessment.md`, `stage_b_*_probe_gate_assessment.json`, `stage_b_*_probe_behavior_interpretation.json`, `stage_b_v1_i10r_*_canonical_eval_summary.json` (microprobe, nocall_probe, counterbalanced_probe, residual_nocall_probe), `stage_b_v1_geometry_*` design/sweep/ledgers.
- Geometry and exposure: `artifacts/stage_b_llama31_8b_base_v1_geometry_probe_{mh,lh}/` (training_summary.json, exposure_ledger_{declared,realized,drift}.json, exposure_row_identity_sidecar.json, sampler_determinism_report.json), `manifests/reports/stage_b_v1_geometry_mapping_design.md`, `stage_b_v1_geometry_sweep_matrix.json`, `stage_b_successor_probe_weights_sidecar.json`, `stage_b_*_probe_design.md`.
- Detector/governance/observability: `scripts/post_eval_collapse_detector.py`, `manifests/reports/stage_b_first_probe_detector_noncomputable_fix_summary.md`, `stage_b_first_probe_detector_noncomputable_validation.json`, `stage_b_v1_threshold_profile.json`, `stage_b_schema_convergence_recommendation.md`, `stage_b_successor_probe_readiness_determination.md`.
- Evaluator: `scripts/eval_canonical_manifest.py` (_build_failure_profile and row metadata), `evals/canonical_eval_manifest_v1.json`, i10r canonical summaries containing `failure_profile`.
- WP8 / governance doctrine: `docs/convergence/STAGE_B_WP8A_SCENARIO_CATALOG.md`, `STAGE_B_B1_NI_SCENARIO_RECONCILIATION_REVIEW.md`, `STAGE_B_WP8_B2_EXIT_REVIEW.md` (and B2C/B2M/B2P/B2NI sub-slices), `STAGE_B_B1_PARENT_CONTEXT_AND_DENOMINATOR_REVIEW.md`, `STAGE_B_B2_*_REVIEW.md`, `STAGE_B_CLOSURE_ASSESSMENT.md`, `STAGE_B_COMPLETION_DETERMINATION.md`, `STAGE_B_LESSONS_LEARNED_SUMMARY.md` (read for comparison only).
- Process/evidence preservation: `local_review_bundles/` (e.g. `stage_b_evaluator_implementation_readiness_review_*.zip`, wp8 slice zips), package/coverage/reconciliation artifacts under `docs/convergence/STAGE_B_WP8_*`, `manifests/reports/stage_b_*_package_review.md`, `*_coverage_summary.md`, `*_reconciliation_summary.md`.
- Regimen implementation: `scripts/train_lora_sft.py` (_GeometrySamplingTrainer, exposure ledger builders, geometry digests), `scripts/provision_geometry_probe_weights.py`, `scripts/build_stage_b_recovery_i10r*.py`, preflight/validate scaffolds, `evals/runs/stage_b_*_eval/`.
- Supporting: `docs/convergence/STAGE_B_EVAL_REDESIGN_*` (contracts, metric inventory, emission design), `STAGE_B_WP8_*` execution and midpoint artifacts, dataset v1_0 stage_b_recovery jsonl/summaries.

**Distinction Framework Used:**
- **Model-specific findings:** Numeric behavioral outcomes, deltas, archetype robustness, and hypothesis results tied to the llama-3.1-8b-base + this dataset/intervention distribution. Not portable as method.
- **Regimen findings:** How probes, geometry cells, instrumentation, baselines, and bounded execution were executed and audited.
- **Governance findings:** Authority, non-inference, noncomputability, invariants, reconciliation, and doctrine enforcement.
- **Evaluator findings:** What the scorer/evaluator must emit, row metadata contracts, and why proxies are disallowed.

---

## 1. What methodological lessons appear validated?

Evidence directly supports these as durable:

- **Small, targeted, rollback-first live probes efficiently map objective-interaction surfaces.** The i10r quartet (microprobe → nocall_probe → counterbalanced_probe → residual_nocall_probe) plus two geometry cells (M/H then L/H) used minimal additions (EXPECTED_NOCALL_CONTRASTIVE_ROWS ~10-16, read_file_symbol ~0-10) on a stable i10r parent. They produced clear, attributable deltas across no_call (agg/adv), read_file (overall + symbol-name), wrapper, invalid_json, direct_answer_substitution, and no_anchor without full retrains or multi-epoch runs. See `build_stage_b_recovery_i10r_*.py` EXPECTED_* constants, i10r canonical_eval_summary.json metrics/failure_profile, and the two scientific_assessment.md (Part A findings + hypothesis evaluation). The L/H successor was explicitly designed as "smallest informative follow-up" and delivered a decisive negative.

- **Exposure geometry with declared/realized/drift accounting + digests is required for attribution.** Without it, first probe showed "partial/confounded" axis activation (no clean valid_rg_search_contrastive_family in realized) and large raw drift (1881) that had to be manually explained as sampling artifact. Post-plumbing (lh/mh), geometry_context (sweep_id, cell_id, axis_levels, declared_exposure_units) propagated to training_summary, ledgers, sampler report, detector gate/collapse outputs, and weights sidecar. Digests (geometry_mapping_identity_digest, geometry_context_input_digest, row_identity_digest) enable cell reproducibility and audit. See `artifacts/.../training_summary.json` geometry_context + realized_exposure, `exposure_ledger_realized.json` family_counts (only 2 families realized from 13 weighted rows), `post_eval_collapse_detector.py` _build_*_digest functions, and successor scientific assessment "Sampler validity is not the open question anymore."

- **Non-inference + explicit noncomputable handling restores governance observability.** First probe (M/H) left 8 metrics + 9 rules noncomputable due to stale threshold paths vs live eval schema (pre-full failure_profile emission); detector crashed or was blind. Repair in `post_eval_collapse_detector.py` (record unresolved with reason/catalog/affected_rules, status="noncomputable", noncomputable_policy_applied, conservative halt under profile) plus eval emission of `failure_profile.*` made successor fully computable (0 noncomputable). Gate now surfaces hard/catastrophic/watch distinctly. See `stage_b_first_probe_detector_noncomputable_fix_summary.md`, successor gate_assessment.json (noncomputable_* empty), threshold_profile.json (noncomputable_status: "halt_progression"), and scientific "Scientific observability is restored, but the measured behavior is still unacceptable."

- **Bounded slices + package/reconciliation/zip discipline improves control and auditability.** WP8 delivered 99/99 scenarios (Family A 25, B1 24, B2 23, X 27) with per-slice (B2C/B2M/B2P/B2NI, X1/X2a etc) then cumulative package_review + coverage_summary + reconciliation_summary + fixture_index, plus zip bundles in local_review_bundles/. B1-NI and B2 exit reviews explicitly checked authority contradictions, catalog fidelity, and doctrine drift. See `STAGE_B_CLOSURE_ASSESSMENT.md` (quantitative 99/99 table, governance check table), `STAGE_B_WP8_B2_EXIT_REVIEW.md` (sub-slice coverage + doctrine preservation), and AGENTS.md route for slice_execution/readiness_or_closure_review. No unresolved authority/catalog/governance drift at closure.

- **Protected behaviors require first-class evaluator support with stable denominators and archetype slices.** Read_file procedural commitment, symbol-name sub-slice, no-anchor, and direct_answer_substitution cannot be reliably recovered from aggregates or post-hoc comparison_rows parsing. Redesign contract required explicit emission + row metadata (symbol_name_membership, anchor_bucket, failure_subtype, expected_primary_tool_name). See `STAGE_B_EVAL_REDESIGN_CONTRACTS.md` (Family B1 read-file preservation, "Protect `read_file` procedural commitment during no-call and geometry interventions"), `eval_canonical_manifest.py` _build_failure_profile (exact counts/rows/rates per archetype), and i10r canonical summaries vs early live summaries.

- **Hard invariants vs catastrophic vs tradeoff-watch separation, plus fixed reference baseline, enables interpretable gates.** Threshold profile and gates distinguish no_call==1.0 absolute (hard, even if other metrics improve), read_file <0.40 (catastrophic), <0.70 (watch), wrapper==0, etc. All gates used the same i10r_counterbalanced_probe_canonical_eval_summary.json as baseline for deltas. See successor and first gate_assessment.json (active_rule_ids broken out), threshold_profile.json (hard_invariants, catastrophic_thresholds, tradeoff_watch_thresholds, basis delta_vs_baseline), and scientific assessments.

---

## 2. What methodological lessons appear invalidated?

Direct evidence shows these did not hold or required revision:

- **The specific L/H geometry hypothesis (low no-call pressure + high read_file counterweight would materially restore read_file procedural commitment while preserving adversarial/aggregate no_call at ceiling) was not supported.** L/H produced no_call agg 0.733 / adv 0.650 (worse than both baseline 0.967/1.0 and prior M/H 0.933/1.0), read_file exact-valid 0.222 (worse than M/H 0.370 and baseline 0.704), with other read_file archetypes at 0/14. Symbol-name held ~0.46 but insufficient. Hypothesis evaluation in `stage_b_successor_probe_scientific_assessment.md` explicitly marks "Unsupported" for both no_call preservation and read_file restoration. "The cell did not reduce overall invalid-json failure pressure." Decisive negative; "Next geometry cell recommendation: None warranted from the current line."

- **Clean independent axis activation and family label alignment cannot be assumed without explicit taxonomy work.** Declared geometry axes (no_call_adversarial_family, read_file_symbol_name_family, valid_rg_search_contrastive_family) vs realized family_counts in ledgers only partially matched (e.g., "malformed_regex_underspecified_search_adversarial_boundary" and "read_file_symbol_name_commitment_instability"; no distinct valid_rg_search in realized for first probe). Assessments repeatedly flag "Geometry-axis activation is partial/confounded." See realized ledgers, first scientific assessment, geometry_context in training_summary vs family/archetype_counts.

- **"More no-call pressure always strengthens no_call without unacceptable cost" (or simple pressure-threshold model) was falsified by the probe series.** Nocall_probe achieved 1.0/1.0 no_call but read_file collapsed to 0.259/0.0 symbol; counterbalanced restored read_file to baseline levels but no_call only to 0.967/0.9; geometry cells did not find a compensating point in tested L/H or M/H. See the four i10r canonical_eval_summary metrics + hard_stop_evaluation, restoration assessments, and scientific hypothesis sections. This directly motivated (and then terminated) geometry mapping.

- **Stale metric paths or missing first-class surfaces would be minor or auto-resolvable.** First probe showed hard runtime/governance blockage (noncomputable) until explicit detector repair + eval emission expansion. "Prior behavior: unresolved required metric caused hard runtime failure." No silent pass-through was allowed post-repair. See detector_noncomputable_fix_summary and schema_convergence_recommendation (hybrid path required; profile-only left blind spots on read_file/anchor/direct_answer).

- **Row duplication or un-instrumented composition would be sufficient for geometry.** Design explicitly preferred sampler weighting for "clean geometry control" and required ledgers/digests/sampler capture; duplication noted as "acceptable temporary approximation if tightly capped and explicitly audited" but "otherwise too confounded." Implemented path used deterministic_weighted_sampler_sidecar_overlay with capture. See geometry_mapping_design.md (weighting methods, missing instrumentation list) and lh training_summary (sampler_class, weights_summary with 1969 zero-weight rows, 13 positive).

---

## 3. Which Stage B outputs should become permanent parts of the training regimen?

**Regimen (execution + audit):**
- Geometry sampling support (`_GeometrySamplingTrainer`, sidecar overlay, `geometry_sampling` + `geometry_mapping` config blocks), exposure ledger builders (declared/realized/drift), row_identity_sidecar, sampler_determinism_report, and full geometry_context + digest propagation. All appear in training_summary, ledgers, detector outputs, and reports. Permanent for any objective-interaction calibration. Evidence: `train_lora_sft.py` (geometry functions + trainer subclass + _build_*_ledger), `provision_geometry_probe_weights.py`, lh/mh artifacts, successor design/readiness.
- Bounded package construction + package_review + coverage_summary + reconciliation_summary + readiness_determination + launch_blocker + go_no_go + success_criteria + preflight validation artifacts before any probe/iteration run. See manifests/reports/stage_b_*_probe_* (design, package_review, readiness, blocker, success_criteria), AGENTS.md slice routes, and wp8 equivalents.
- Fixed reference baseline snapshot discipline (i10r_counterbalanced_probe_canonical_eval_summary as the stable "counterbalanced" reference for all deltas, gates, and restoration assessments). Used across i10r probes and both geometry cells.
- Zip bundle workflow for external review slices (local_review_bundles/*) without polluting git. Validated by volume of wp8 and evaluator readiness zips + AGENTS.md.

**Governance:**
- Threshold profile contract (hard_invariants with absolute ==1.0 for no_call, catastrophic, tradeoff_watch, noncomputable_status=halt, missing_baseline_policy). See `stage_b_v1_threshold_profile.json`, gate_assessments, detector.
- Noncomputable-safe detector with explicit reporting (noncomputable_metrics/rules, reasons, affected, policy_applied) + geometry digest fields. See `post_eval_collapse_detector.py` (full _run_detector and noncomputable paths), first_probe fix summary + validation.
- Authority precedence (catalog > execution prompt for scenario IDs, expected states, detector treatment) + reconciliation checks on contradiction. See B1-NI reconciliation review, B2 exit review, closure assessment.
- Explicit "missing means missing", non-substitution, current-run facts only, denominator provenance, comparability-state distinctions (comparison-blocked, bridge-required, reference-only). Codified in B* reviews and fixture matrix.

**Evaluator:**
- First-class `failure_profile` emission (read_file_exact_valid {count,rows,rate}, read_file_symbol_name_exact_valid, failure_categories_non_exact_tool_rows, anchor_exact_share, tool_expected_rows, non_exact...) plus supporting row metadata (symbol_name_membership, anchor_bucket, failure_subtype, expected_primary_tool_name, source_case_id for comparability). See `eval_canonical_manifest.py` _build_failure_profile + _tool_expected_rows etc, STAGE_B_EVAL_REDESIGN_CONTRACTS.md and METRIC_INVENTORY, i10r canonical summaries (which had it) vs early live summaries.
- No-proxy doctrine: detector consumes only declared emitted facts; comparison_rows and aggregates insufficient for governed concepts.

**Evidence preservation cross-cutting:**
- All ledger/digest/sidecar/sampler artifacts + cross-references in training_summary and detector outputs.
- Fixture indexes + human review packages where used.
- Per-iteration resolved_config + run manifests + approval_state.

These are now embedded in scripts, manifest/report templates, and doctrine; removing them would regress observability and auditability for future work.

---

## 4. Which Stage B outputs should remain experimental?

- The specific 5-point bracketed sweep matrix and cell definitions (L/H, M/H, H/H, H/M, H/L with exact exposure units 10/13/16 and 0/6/10). Only L/H + M/H executed; hypothesis space terminated early. Future work may choose different axes, weighting, or non-bracketed designs. See `stage_b_v1_geometry_sweep_matrix.json` and mapping_design.md (smallest_useful_sweep section).
- Exact decomposition granularity of WP8 validation authoring into per-subslice packages (B2C/B2M/B2P/B2NI + X1/X2a/X2b/X3/X4 separate full coverage/package/reconcil cycles before cumulative). Produced high artifact volume for 99 scenarios. Family-level + targeted sub-slice tests may suffice; the per-slice loop was execution-specific. Evidence: count of STAGE_B_WP8_B2* and X* files vs cumulative.
- The i10r_*_specific recovery dataset builders, concentration reviews, and preflight/validate scaffolds (i8/i9/i10 variants). These were episode-specific rollback instruments from i10r parent; superseded by counterbalanced + geometry approach. See scripts/build_stage_b_recovery_i{8,9,10,10r}*.py and i*_diagnostics_scaffold.py.
- Detailed per-probe launch_blocker_inventory.md, filesystem_readiness_audit.json, go_no_go_summary, and resolved_config snapshots for every micro-experiment. Necessary hygiene, but some repetition once process stabilized (cf. later stage c conformance).
- The precise 4 "retained Stage B metrics" as standalone detector keys (now integrated into family redesign contracts). Their exact paths and catastrophic/watch thresholds were tuned to this geometry episode.

These were valuable for this Stage B but are not core reusable contracts.

---

## 5. Which Stage B activities generated the highest information value per unit effort?

- **i10r probe series (micro/nocall/counterbalanced/residual) + associated restoration/no_call assessments and canonical summaries.** ~4 small dataset builds (10-16 added contrastive rows + 0-6 symbol rows), 4 evals on 0.2-epoch-ish runs, produced the full observed coupling surface, showed read_file as dependent variable under no-call pressure, and directly motivated (then bounded) geometry. High signal: clear before/after rates, hard_stop triggers, residual failure taxonomy. Low unit cost vs full i* iterations. See build scripts EXPECTED_*, four canonical_eval_summary.json (metrics + failure_profile + hard_stop_evaluation + deltas), counterbalanced no_call_restoration_assessment and next_step_assessment.
- **Detector noncomputable repair + synthetic/live validation (single targeted change in post_eval_collapse_detector.py + one validation run).** Unblocked all subsequent governance for probes and beyond. Turned 8+ noncomputable metrics/rules from crash/blind into explicit halt with audit fields. See fix_summary.md (root cause, implementation, validation results), noncomputable sections in successor gate (0 count), and how first probe gate was still "halt_progression" but post-repair successor was substantive.
- **Geometry context + ledger + digest + sampler determinism + sidecar plumbing (trainer + provisioner + detector + reports).** One-time implementation enabled clean attribution, cell isolation, drift explanation, and reproducibility for the two live probes (and future). Evidence value: assessments could state "sampler-valid", "declared vs realized is sampling artifact not execution failure", "axis activation partial", and propagate digests. See training_summary geometry_sampling + realized_exposure_summary (401 sampled, 13 unique), realized ledger family_counts, sampler report status, detector _build_*_digest, and scientific assessments.
- **Two live geometry probes (M/H then L/H) + scientific/gate/behavior assessments.** Low effective exposure (13 rows weighted, 0.2 epoch), sampler seed fixed, produced decisive hypothesis falsification, behavioral numbers, governance outcome (catastrophic_halt on no_call invariants + read_file/invalid_json), and "no further cells warranted." Wrapper and das showed partial independence. Highest decision value per training cost in the record.

These activities had outsized impact on "what we now know about the surface, what governance can see, and what is reproducible."

---

## 6. Which activities generated the lowest information value per unit effort?

- **Granular WP8 sub-slice execution/review cycles (B2C/B2M/B2P/B2NI + X1/X2a/X2b/X3/X4 + per-family package/coverage/reconcil + cumulative).** ~30+ STAGE_B_WP8_* md files + multiple zips for 99 scenarios (B2 alone 23 scenarios split 4 ways). Each sub-slice produced full fixture_index + package_review + coverage_summary; then exit reviews re-checked the same doctrine. Once family coverage and authority/consistency checks passed, marginal incremental signal per additional slice review was low relative to documentation and reconciliation volume. See count of B2* and X* files vs STAGE_B_CLOSURE_ASSESSMENT 99/99 table and B2 exit review (which still had to re-verify all sub-slices).
- **Iteration-specific scaffold repetition (i8/i9/i10 family concentration reviews, build/validate_stage_b_recovery_i*.py variants, i*_diagnostics_scaffold).** These supported early i* recovery but were largely superseded by the i10r counterbalanced + geometry approach. Concentration reviews repeated similar family-mix analysis patterns. Evidence: multiple near-identical build_stage_b_recovery_i*.py and validate_*_preflight.py, plus concentration_review.md for i8/i9/i10/i10r.
- **Boilerplate per-probe hygiene artifacts (launch_blocker_inventory, filesystem_readiness_audit, go_no_go, resolved_config, cleanup plans) for every micro cell.** Necessary for the two geometry probes and i10r, but high repetition once the package/review pattern stabilized. See manifests/reports/stage_b_first/successor_probe_* (blocker, audit, go_no_go, etc).
- **Exploratory schema convergence option matrices and phase2 inventory when hybrid path was selected early.** Useful for decision but not all branches exercised post-recommendation. See stage_b_schema_convergence_option_matrix.json, phase2_* artifacts.

These were not valueless (completeness and hygiene matter), but the ratio of new decision-relevant information to effort (docs, scripts, reviews) was lower than the probe/instrumentation cluster.

---

## 7. Did Stage B successfully create reusable post-training methodology, independent of model-specific outcomes?

**Yes, with clear boundaries.**

Reusable methodology (embodied in code, contracts, and process, portable to other models/data/protected behaviors):

- **Probe-based objective-interaction calibration regimen:** small rollback additions, weighted sampler + sidecar for controlled exposure, explicit geometry_context/cell/axis, full declared/realized/drift + row identity + sampler determinism + digest audit trail, fixed reference baseline, hypothesis + success criteria + scientific/gate assessment, bounded package/readiness/launch before run. Independent of whether any cell "succeeds." See trainer/eval/detector scripts, lh/mh artifacts (all geometry_context present even on failure), i10r-to-geometry progression, probe package/review artifacts.
- **Governance engine and doctrine:** profile-driven detector (hard/catastrophic/watch + explicit noncomputable with policy), non-inference contract (no prompt/history/aggregate substitution for governed slices), authority (catalog authoritative), missing=noncomputable, denominator integrity + current-run facts, explicit comparability states. Codified in threshold profile, detector, B1-NI/B2 reconcil reviews, eval redesign contracts, closure. Survives model outcomes.
- **Evaluator contract for governed observability:** first-class failure_profile with archetype rates + denoms + metadata (symbol_name_membership etc), no-proxy rule, stable row identity for comparability. See eval_canonical_manifest.py, redesign docs, i10r summaries (the emission), successor "restored detector-facing metric contract."
- **Evidence-preservation and process infrastructure:** ledgers/digests/sidecars, package+coverage+reconciliation+readiness+zip bundle workflow, slice discipline, hygiene checklists, authority precedence in AGENTS.md. Used for both probes and 99-scenario WP8 closure. See local_review_bundles, wp8 artifacts, convergence docs, train/detector code.

Model-specific / episode-specific (do not carry as methodology):
- The numeric surface for this 8b (no sweet spot in L/H or M/H for 1.0 no_call + preserved read_file; symbol-name more robust than p0_read_file_1/3; L/H actually regressed no_call more on adversarial).
- The exact 5-cell bracket + exposure units chosen for this geometry mapping.
- The precise failure thresholds and 4 retained metrics as they stood mid-episode (now generalized into families).
- The per-subslice decomposition depth used for WP8 validation authoring.
- Any one-off scaffold or concentration review tied to i8-i10r rollback sequence.

Stage B therefore extracted a portable "post-training calibration + governed observability + evidence-auditable intervention" methodology whose core contracts and instrumentation are independent of the specific llama-3.1-8b outcomes (which were, correctly, treated as falsification data rather than portable claims). Later stage c work (evaluator foundation, detector projection, etc.) built on these surfaces, confirming the extraction.

---

## 8. What are the three most important lessons that should survive into future projects?

1. **Evidence-preservation instrumentation (ledgers, digests, row identity, sampler capture, explicit geometry_context, archetype metadata) must be built in before probe or geometry work, not after.** Without it, first probe outcomes were partially confounded (axis activation, drift explanation required manual forensics) and governance was noncomputable. With it, successor could cleanly state sampler validity, attribute regressions, restore full gate computability, and produce a decisive negative with attribution. This is regimen + evidence + governance. Direct evidence: contrast between first and successor scientific assessments + gate outputs + lh/mh ledgers vs pre-plumbing state; geometry_mapping_design missing-instrumentation list; NI reviews rejecting historical/prompt inference.

2. **Governance for protected behaviors must be non-inference by construction and noncomputable-safe by design.** Detector must consume only explicitly emitted facts (failure_profile rates with stable denoms, row metadata markers); unresolved or schema-mismatched metrics must halt visibly and conservatively (never crash, never silent pass, never proxy). "Missing means missing"; no prompt-text, path-name, historical, or parent-aggregate substitution for sub-slices like symbol-name or no-anchor. This survived the first-probe breakage and enabled substantive (not blocked) rejection of L/H. Governance + evaluator. Evidence: B1-NI-003 ("do not infer symbol-name from prompt text"), B2 exit review doctrine preservation list, detector_noncomputable_fix + successor 0-noncomputable gate, eval redesign contracts ("no proxy mappings", "detector may consume declared metric facts, but must not classify prompts..."), threshold noncomputable_status.

3. **Small, instrumented, reference-baselined live probes with explicit hypotheses, success criteria, and bounded package discipline are the efficient way to map tradeoffs and falsify assumptions in post-training.** The i10r series + 2 geometry cells (low effective exposure) mapped the no_call / read_file coupling, showed symbol-name vs other read_file divergence, falsified the L/H restoration hypothesis, and stopped further cells with clear rationale ("behaviorally unsuccessful and governance-rejected"). Negative results are high-value when attribution and reproducibility are engineered in. This is regimen + distinction of model-specific vs method. Evidence: i10r canonical summaries + restoration assessments, geometry design hypothesis, two scientific assessments (supported/unsupported/unexpected sections + final determination "L/H probe failed"), package/readiness artifacts, and "no further geometry cell recommendation."

These three are directly extractable from the contrast between early Stage B (pre-instrumentation, blocked governance, untested hypotheses) and late Stage B (auditable cells, computable substantive gates, doctrine-consistent closure), and they are portable beyond this model and this specific geometry.

---

**Appendix: Key File Map for Verification**

- Probes + geometry outcomes: `manifests/reports/stage_b_*_probe_scientific_assessment.md`, `*_gate_assessment.json`, i10r `*_canonical_eval_summary.json`, `artifacts/stage_b_llama31_8b_base_v1_geometry_probe_{lh,mh}/` (all ledgers + training_summary + sampler).
- Instrumentation: `scripts/train_lora_sft.py` (geometry sections), `provision_geometry_probe_weights.py`, `post_eval_collapse_detector.py`.
- Evaluator: `scripts/eval_canonical_manifest.py` (_build_failure_profile), `evals/canonical_eval_manifest_v1.json`, STAGE_B_EVAL_REDESIGN_* in convergence/.
- Governance doctrine: `docs/convergence/STAGE_B_B1_NI_SCENARIO_RECONCILIATION_REVIEW.md`, `STAGE_B_WP8_B2_EXIT_REVIEW.md` (and sub), `STAGE_B_CLOSURE_ASSESSMENT.md`, `stage_b_v1_threshold_profile.json`.
- Process: `local_review_bundles/*.zip`, `docs/convergence/STAGE_B_WP8_*_PACKAGE_REVIEW.md` etc, AGENTS.md.
- Redesign contracts: `docs/convergence/STAGE_B_EVAL_REDESIGN_CONTRACTS.md`, `METRIC_INVENTORY.md`.

All claims above are traceable to these artifacts. No claim relies on unverified prior narrative.

**End of Independent Review.**