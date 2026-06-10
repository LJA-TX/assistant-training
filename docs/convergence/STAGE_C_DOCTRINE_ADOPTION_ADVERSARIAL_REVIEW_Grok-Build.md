# Stage C Doctrine Adoption Candidate Assessment — Independent Adversarial Review

**Date**: 2026 (review of frozen artifacts and the candidate assessment)
**Reviewer posture**: Independent adversarial. Primary sources examined directly. The proposed doctrine is tested for falsifiability and for whether the Stage C evidence record actually supports elevating the claims to doctrine status. No assumption that the proposal is correct, "narrow," or already earned.
**Scope**: Bounded to the 8 primary questions in the task. Focus is evidentiary: what the R1 reconnaissance through E1 sequence, the prior R1 adversarial review, the E1 bundle artifacts, the methodology extraction assessment, and the doctrine candidate assessment itself actually demonstrate. Does not evaluate usefulness or operational convenience.
**Authority posture per AGENTS.md**: Doctrine artifacts are authority level 2 (after authoritative catalogs/planning). This review checks whether the proposal has earned that status from the evidence produced by one investigation family. Pre-flight checks applied (see below). No stop-and-escalate conditions triggered.

## Pre-Flight (Per AGENTS.md Process Dispatcher Skeleton)

- **Request classification and bounded scope**: Confirmed. This is an architecture/process assessment of a methodology extraction / doctrine adoption candidate. Bounded to the listed investigation sequence and the 4 doctrine claims + supporting classifications in the candidate assessment. Not an execution slice, not a migration gate, not catalog work, not remediation.
- **Ownership/authority inputs identified**: The candidate doctrine is documented in `docs/convergence/STAGE_C_DOCTRINE_ADOPTION_CANDIDATE_ASSESSMENT.md`. Primary evidence chain is the R1* / E1 / transition / methodology extraction set in the same directory. The prior independent adversarial review (`STAGE_C_R1_ADVERSARIAL_REVIEW_OF_STAGE_C_DIAGNOSIS.md`) is treated as peer input.
- **Stop-and-escalate triggers checked**: None met. No authority conflict (the task is explicitly to test the proposal before formal adoption). No catalog contradiction surfaced in the reviewed Stage B scenario catalogs or family definitions. Ownership of the investigation artifacts is clear within the convergence record. Scope did not expand. No methodology redesign was requested; this is review of an extraction claim. No repository anomaly blocking the read-only analysis (untracked status of the convergence docs and E1 bundle is consistent with active review artifacts; see hygiene note).
- **Baseline hygiene checks**:
  - `docs/framework/process_infrastructure/checklists/hygiene_review_checklist.md`: Applied conceptually. Review is read-only against existing artifacts. No runtime/evaluator/governance surfaces touched. The E1 bundle itself carries a passing `validation_report.json` (render_only=true, generation/scoring/detector all false, exact hash match, render exactness pass, control cleanliness pass, completeness pass).
  - `docs/framework/process_infrastructure/checklists/governance_boundary_verification_checklist.md`: Scope stayed inside the authorized review of the doctrine candidate. No unapproved workstreams. Boundary confirmation present in this report.
  - Git status (live at review time) showed untracked convergence docs (including the candidate assessment itself) and the E1 bundle under `manifests/reports/`, plus some script modifications unrelated to this review. This is noted as context (active artifacts under review, not yet baseline-committed), not a blocker for read-only analysis. Initial conversation snapshot indicated clean tree; live status reflects the state of the investigation deliverables.

**Primary sources directly examined** (not summaries only):
- `docs/convergence/STAGE_C_RECONNAISSANCE_AND_EVIDENCE_INVENTORY.md`
- `docs/convergence/STAGE_C_R1A_RUNTIME_REGIME_CHARACTERIZATION_ASSESSMENT.md`
- `docs/convergence/STAGE_C_R1B_CONTAMINATION_ORIGIN_ASSESSMENT.md`
- `docs/convergence/STAGE_C_R1C_PROMPT_CONSTRUCTION_AND_CAUSALITY_ASSESSMENT.md`
- `docs/convergence/STAGE_C_R1D_RENDERED_PROMPT_RECOVERABILITY_ASSESSMENT.md`
- `docs/convergence/STAGE_C_R1_ADVERSARIAL_REVIEW_OF_STAGE_C_DIAGNOSIS.md` (prior adversarial)
- `docs/convergence/STAGE_C_TRANSITION_FROM_EVIDENCE_EXTRACTION_TO_EVIDENCE_CREATION_ASSESSMENT.md`
- `docs/convergence/STAGE_C_E1_PROMPT_TRACE_EVIDENCE_CREATION_PLAN.md`
- `docs/convergence/STAGE_C_E1_PROMPT_TRACE_EVIDENCE_INTERPRETATION.md`
- `docs/convergence/STAGE_C_METHODOLOGY_EXTRACTION_ASSESSMENT.md`
- `docs/convergence/STAGE_C_DOCTRINE_ADOPTION_CANDIDATE_ASSESSMENT.md`
- E1 bundle: `manifests/reports/stage_c_prompt_trace_evidence/stage_c_e1_prompt_trace_20260609T221315792398Z/` (manifest.json, prompt_traces.jsonl, validation_report.json, both .prompt.txt files)
- Supporting: runtime forensics investigation excerpts, evaluator code paths in `scripts/eval_canonical_manifest.py`, manifest `evals/canonical_eval_manifest_v1.json`, dataset splits.

## The Proposed Doctrine (Quoted from Candidate Assessment)

The candidate assessment advances one narrow doctrine-worthy result:

> When prompt construction may affect interpretation, the exact rendered prompt MUST be captured as a first-class evidence artifact. The artifact MUST be accompanied by row identity, source dataset and manifest provenance, render-path metadata, and stable hashes or fingerprints. Continuation text alone MUST NOT be used to infer prompt provenance or to substitute for the rendered prompt.

Supporting claims in tables and text:
- Exact rendered prompts are first-class evidence artifacts (Doctrine).
- Prompt provenance must be captured with the rendered prompt (Doctrine).
- Continuation text alone is insufficient for prompt-origin claims (Doctrine).
- Prompt and continuation surfaces must be preserved separately when prompt construction may affect interpretation (Doctrine).

Provisional/guidance items (one affected + one control; render-only trace bundles; manifest/JSONL/raw prompt/validation-report bundle shape; minimum control strategy) are explicitly *not* put forward as doctrine in the candidate.

## Answers to the Primary Questions

**1. Has Stage C actually demonstrated doctrine-level findings? Or has it merely demonstrated Stage C-specific findings?**

It has demonstrated a high-value, concrete, Stage C-specific finding with clear methodological implications for cases that share its structure (frozen record lacking the prompt surface; causal question turning on pre-generation vs. continuation content; chat-templated render path with fallback; dominant transcript-replay/echo regime on tool-directed rows).

It has *not* demonstrated a cross-family, cross-context, content-independent doctrine. The entire R1–E1 arc is one investigation family (canonical_v1 heldout_validation + tool_holdout non-exact tool-expected rows + the separate direct_answer control split, on llama-3.1-8b-base lineage, under one evaluator manifest and one generic_roles_v1 fallback path). The prior R1 adversarial review already characterized the causal claims as fragile precisely because the exact rendered prompt was absent. E1 (two rows, render-only) narrowed the uncertainty boundary for the representative affected row and the chosen control; its own interpretation states: "the bundle narrows the space of explanations, but it does not materially resolve the remaining causal question."

The candidate assessment's own adoption standard requires the finding to be "independent of the specific contamination content" and to "generalize to future evaluation families." Stage C produced a demonstration that the prompt snapshot was the missing artifact *in this case*. It did not produce replicated demonstrations that the same structural gap arises, or that the same rule is required, across other families.

Verdict on this question: primarily Stage C-specific findings, with a reusable negative lesson about continuation-only evidence. The leap to doctrine is an extraction step, not a direct demonstration.

**2. Is "rendered prompts are first-class evidence artifacts" genuinely doctrine-worthy? Why or why not?**

It is a strong, evidenced *observability and evidence-creation rule* for any investigation in which the causal or interpretive question requires knowing the exact pre-generation surface and that surface is not already preserved. The R1C/R1D gap analysis and the prior adversarial review both independently identified the absence of the exact rendered prompt as the hard limit on further causal discrimination. E1 directly created the artifact via the canonical render path (validation passed on exactness, hash, render_only, control cleanliness). The concrete prompts are now available:

Affected (`p0_rg_search_4`):
```
[SYSTEM]
Use ONLY the exact tool requested. Keep final answer concise. If a tool result already answers the task, stop and finalize.
[USER]
Use rg_search in /opt/ai-stack/runtimes/assistant-runtime/server/agent.py for string "tool_calls" and report match_count only.
[ASSISTANT]
```

Control (`da_92001`):
```
[SYSTEM]
You are a runtime assistant. Be concise, truthful, and explicit about limits. Never claim actions were executed unless results are provided.
[USER]
Define idempotent in one sentence. [eval 92001] eval_direct
[ASSISTANT]
```

Both used the same fallback (`render_path_used=generic_roles_v1_fallback`, `fallback_used=true`, tokenizer_chat_template_text=null). The prompt surface for the affected row contained the task-specific content, the system instruction, and the role delimiters via the fallback. Bad continuations (per forensics investigation) replay task text + [SYSTEM] + instruction after the generation cue. This allows clean separation of input surface from continuation behavior.

However, "first-class evidence artifact" as a standing doctrine for "whenever prompt construction may affect interpretation" is not yet earned at doctrine level from this record. The candidate assessment's adoption standard itself requires generalization beyond the single case. No other family in the reviewed artifacts (Stage B probes, other packages, later C0–C10 implementation work) is shown to have hit an identical unresolvable prompt-origin ambiguity that required the same rule. Family-level reconstruction from preserved messages + render contract + manifest was already possible (R1D explicitly states this); the exact snapshot is higher-fidelity for audit and for cases where per-row render choice or template text matters. Elevating the prompt snapshot to "first-class" status on one successful minimal trace risks codifying a solution to a demonstrated gap as a universal norm before the norm has been stress-tested.

**3. Is prompt provenance metadata doctrine-worthy? Or merely a strong implementation recommendation?**

The specific metadata bundle demonstrated in E1 (row identity/source_case_id, split, dataset path + sha256, manifest path + sha256, system/user_text, render_path_used + fallback flag + custom_template_name, tokenizer reference + (null) template text/sha, rendered_prompt_path + sha256 + char/token counts, prompt_contract, captured_utc) is exactly what made the two .prompt.txt files self-authenticating and auditable. The validation_report confirms row resolution, render exactness, hash match, template provenance, no-generation, control cleanliness, and completeness. This is strong, concrete evidence that *when you create a rendered prompt snapshot for evidentiary purposes, these fields are necessary for it to function as evidence rather than another opaque artifact*.

It is therefore a strong implementation/evidence-hygiene recommendation, demonstrated as necessary in this instance. It has not been shown to be a doctrine-level requirement that applies even when the prompt surface is not the contested artifact, or when family-level reconstruction suffices. The candidate assessment already classifies the full "manifest / JSONL / raw prompt / validation-report bundle shape" as Guidance, not Doctrine. Provenance metadata is part of making the snapshot trustworthy; it does not independently rise to doctrine on this evidence.

**4. Is the claim that continuation-only evidence is insufficient for prompt-origin claims adequately supported? Or is it over-generalized from Stage C?**

This is the claim with the strongest direct support in the record.

R1C explicitly states: "There is no direct evidence that the full contamination marker set already existed verbatim in the prompt text for the affected rows." The artifacts showed the prompt construction path (system + user messages → prompt_prefix via apply_chat_template or fallback; only continuation decoded into generated_text) and the outputs full of prompt-like markers, but without the rendered prefix one could not attribute the markers cleanly.

The prior R1 adversarial review (pre-E1) listed as a key weakness: the training data artifact with the exact echoed instruction was under-leveraged precisely because "the exact rendered prompt ... is missing"; alternatives (model replay bias on chat-formatted prompts, eval-time harness construction) could not be separated from corpus-construction claims without it.

E1 + the actual prompts close that specific gap for the representative rows: the markers (role delimiters via fallback, the exact system instruction text, the task content) *were* in the rendered prompt for the affected row; the continuation phenomena (replay of task + [SYSTEM] + instruction) are post-prompt. The E1 interpretation itself notes that "the markers are output-side continuation phenomena, not prompt-side evidence" in the sense that the full transcript-replay behavior was not pre-rendered as a block, but the components that were replayed were present in the prompt.

The negative lesson is well-supported for *prompt-origin claims* (claims of the form "X text or X construction was present in the input that the model saw"): continuation alone cannot settle them when the continuation itself contains (replays of) prompt-derived text. This is not over-generalized from one row; it is the direct reason the R1 series reached a structural ceiling (R1D) and why the transition to evidence creation was required.

It is adequately supported as a bright-line guidance rule for any investigation that needs to discriminate prompt-surface from continuation-surface contributions. Whether it needs the full weight of "doctrine" (vs. strong process hygiene) is a separate classification question.

**5. Has the project overfit a methodology rule to a single investigation?**

Yes, on the positive "first-class artifact" framing and the generalization to "whenever prompt construction may affect interpretation."

The investigation was high-quality, the gap was real, the minimal E1 experiment (1 affected from dominant regime + 1 clean control from direct_answer split, render-only, full provenance, validation) was well-designed and executed (all checks passed), and the prior adversarial review had already called for exactly this evidence. The negative lesson about continuation insufficiency is robust for the class of questions that require pre- vs. post- discrimination.

However, the move from "in this frozen-record case the missing prompt snapshot was the blocker; creating it with 1+1 render-only + metadata narrowed the space" to a standing doctrine rule for future families is an extraction that outruns the demonstrated scope. The candidate assessment's own tables keep the sampling/bundle/control strategy as Guidance/Open. The E1 interpretation is explicit that causal resolution remained incomplete. No second family or second prompt-surface ambiguity investigation is shown in the reviewed artifacts to have independently required or validated the same rule. The later C0–C10 packages are implementation and migration work under the new surfaces, not replications of the prompt-recoverability crisis.

The project has not overfit the *observation that the prompt snapshot was necessary here*; it has over-extracted the *generalization* to doctrine on a single investigation's evidence.

**6. What evidence most strongly supports adoption?**

- R1C/R1D + prior adversarial: independent identification (pre-E1) that the exact rendered prompt was the structural missing fact preventing resolution of prompt/harness vs. continuation vs. corpus attributions.
- E1 bundle + validation_report: concrete, reproducible creation of the missing artifact via the canonical path; all validators passed; the two prompts are now durable, hashed, provenanced, separated from any generation.
- Actual prompt content vs. known continuation patterns (forensics investigation excerpts): demonstrates in practice why continuation alone was insufficient (the prompt contained the system instruction and role markers via fallback; continuations replayed them).
- The E1 plan and transition assessment: explicitly scoped as the smallest evidence-creation step that targets the identified gap, not a full run.
- Self-limiting language in the candidate assessment: it already excludes the sampling pattern, bundle layout, and Stage C content from doctrine status.

This body of evidence strongly supports treating the prompt snapshot (with provenance) as required evidence *when the investigation's causal question turns on the pre-generation surface and the record lacks it*.

**7. What evidence most strongly argues against adoption?**

- Single-family scope: one eval manifest, one render fallback (tokenizer template null), one dominant regime (prompt/task echo + transcript on non-exact tool rows), two-row trace, one model lineage. The direct_answer control uses a *different* system prompt by design.
- E1 interpretation's own limit statement: "does not materially resolve the remaining causal question."
- R1D explicit statement that family-level reconstruction from messages + contract was already feasible; exact per-row snapshot is higher fidelity, not the only path.
- Prior R1 adversarial: the causal weighting toward corpus-construction was already fragile *before* the prompt was available; surface-definition choices (authoritative predicates vs. legacy) co-produce the size of the "missing-evidence" phenomenon.
- Absence of cross-validation: no evidence in the reviewed record that other families (Stage B probes that did archive some prompt tails for specific audits, later C packages, other lineages) encountered unresolvable prompt-origin ambiguities that this rule would have prevented.
- Over-extraction risk: the candidate assessment applies an adoption standard that the evidence only partially meets (direct support yes for the gap; generalization and content-independence demonstrated only within this investigation).

The strongest argument against is that the evidence proves the *utility of creating the snapshot in the specific circumstance where it was missing and needed*; it does not prove a standing, first-class doctrinal requirement that applies prospectively to all future cases where "prompt construction may affect interpretation."

**8. What evidence would be required in the future to revise, weaken, or overturn the proposed doctrine?**

To revise/weaken (keep as strong guidance rather than doctrine):
- One or more additional independent families or investigations in which a prompt-surface question arose, the exact rendered prompt was *not* snapshotted, and family-level reconstruction from messages + render contract + manifest proved sufficient for the required claims (i.e., no unresolvable ambiguity of the R1C/R1D type materialized).
- Demonstration that the marginal cost (storage of raw prompts + provenance metadata + validation bundles, consistency requirements across render paths, enforcement overhead) outweighs the interpretability gain in routine (non-forensic) evaluation work.

To overturn (treat the rule as non-general or actively harmful):
- A case in which mandating the exact rendered prompt + full provenance for a prompt-construction-relevant investigation produced misleading or over-trusted evidence (e.g., the snapshot was taken under a different render contract than the actual generation run, or provenance was incomplete and created false confidence).
- Multiple families in which continuation + messages + render-contract reconstruction reliably supported prompt-origin claims that were later validated by other means, showing the "continuation alone is insufficient" bright line was over-strong.
- A prompt construction regime in which "exact rendered prompt" is not a stable, archivable artifact (dynamic/runtime-dependent rendering, non-deterministic templates, tokenized-only paths, or external context injection) and the doctrine creates an unachievable or misleading requirement.

Future evidence that would *strengthen* toward doctrine: replicated demonstration of the same structural gap (frozen record lacks prompt surface; causal question blocked) across at least two additional distinct families or render contracts, with the minimal 1+1 render-only + provenance pattern again being the smallest step that materially advanced interpretation, and no cheaper reconstruction sufficing.

## Separation of Findings (Evidence-Based, Not Utility-Based)

### Doctrine-Level Status (has earned adoption on the evidence reviewed)

None of the four proposed claims fully meet the candidate assessment's own adoption standard (directly supported + independent of specific content + generalizes to future families + stable norm) on the basis of a single investigation family.

The closest is the negative lesson on continuation text. Even that is most cleanly stated as a demonstrated limit in cases requiring prompt-vs-continuation discrimination rather than a universal first-class rule.

### Guidance-Level Status (strong, evidenced recommendation for evidence creation / observability when the condition applies; does not yet have the cross-validation or foundational character for doctrine)

- Exact rendered prompts (with row identity, source provenance, render-path metadata, and stable hashes) should be treated as required evidence artifacts whenever a prompt-surface question is live and the prior record does not already contain the exact snapshot. (Supported by R1C gap, R1D recoverability conclusion, prior adversarial identification of the gap, E1 successful creation and validation, and concrete prompt vs. continuation comparison.)
- Prompt and continuation surfaces should be preserved separately when the investigation requires discriminating pre-generation construction from post-generation behavior. (Directly shown by the R1 series ceiling and the E1 contrast.)
- Continuation text alone is insufficient to settle prompt-origin claims (claims about what text or construction was present in the input prompt). (Strongest supported claim; demonstrated by the structural limit in R1C/R1D and the clarifying power of the E1 snapshots.)

The specific packaging (manifest + JSONL index + raw prompt files + validation report) and the 1-affected + 1-clean-control minimal experiment are validated patterns from E1 (all checks passed) but remain guidance because they were the *designed* smallest step for this case, not independently derived minima.

### Observations (tied to this investigation; true for Stage C but not generalized)

- The frozen Stage C record for the authoritative missing-evidence cohort (134 rows, 116/134 prompt/task echo with transcript contamination) preserved input messages, the render contract, and continuation-only `generated_text`, but not the exact rendered prompt prefix for the affected rows (R1D).
- Both the representative affected row and the chosen direct_answer control used the `generic_roles_v1_fallback` path (not pure tokenizer_native) under the frozen manifest; tokenizer_chat_template_text was null.
- The rendered prompt for `heldout_validation:2 / p0_rg_search_4` contained the row-specific task, the "Use ONLY the exact tool requested..." system instruction, and the role delimiters via the fallback. Bad continuations (per forensics) replayed task text + [SYSTEM] + instruction after the [ASSISTANT] cue.
- E1 (render-only, two rows, full provenance) materially reduced the prompt-recovery uncertainty boundary for the exemplars but, per its own interpretation, "does not materially resolve the remaining causal question" (corpus-construction / prompt/harness / model continuation bias mix).
- The prior R1 adversarial review (pre-E1) independently identified the absence of the exact inference prompt as a central limit on causal claims and listed provision of the rendered prompt vs. clean rows as strengthening evidence.
- The E1 bundle validation_report.json records full pass on row resolution, render exactness, hash match, template provenance, no-generation/scoring/detector, control cleanliness, and completeness.

### Open Questions (explicitly or implicitly left open by the record)

- Minimum control strategy and sampling for more complex families (multi-turn, conditional/dynamic prompt construction, multiple render paths within one family). The candidate assessment already flags this.
- Whether family-level reconstruction from preserved messages + render contract + manifest is systematically adequate for prompt-origin questions, or whether per-row exact snapshots are required in the general case (R1D acknowledges reconstruction is feasible at family level).
- How the rule interacts with render regimes in which "exact rendered prompt" is not a simple archivable string (tokenized paths, runtime-injected context, non-deterministic elements).
- Cross-family replication: whether other evaluation families or lineages encounter the same structural prompt-surface gap under their frozen records, or whether the Stage C case was particular to the combination of chat-templated fallback serialization + transcript-replay failure mode on tool-directed non-exact rows.

## Overall Determination

The Stage C sequence (R1 reconnaissance through R1D gap → transition → E1 creation and interpretation) plus the prior R1 adversarial review constitutes high-quality, self-critical forensic work. It convincingly demonstrates that, in this specific investigation, the absence of the exact rendered prompt (with provenance) was the blocker to further causal discrimination, that continuation contained replay of prompt-derived text, and that a minimal render-only trace with the documented metadata bundle closed the recovery gap for the representative rows.

That body of evidence earns strong guidance status for evidence hygiene in prompt-surface investigations: capture the exact rendered prompt + row/source/render/hash provenance when the question requires it; do not rely on continuation alone for prompt-origin attributions; keep the surfaces separate.

It does not yet earn doctrine-level status for the four proposed claims under the candidate assessment's own standard. The generalization from one family's demonstrated gap and one successful minimal trace to a standing, content-independent, first-class rule for all future cases where "prompt construction may affect interpretation" is an over-extraction. The proposal's own source documents already qualify the strength (E1 does not fully resolve causality; sampling/bundle details are kept at guidance level). No replicated demonstration across independent families exists in the reviewed record.

**Recommendation on adoption**: Do not adopt the proposed package as doctrine at this time. Codify the negative lesson on continuation insufficiency and the requirement for exact rendered prompt + provenance (when the surface is relevant and missing) as authoritative guidance or process-infrastructure practice. Treat the E1 1+1 render-only + bundle pattern as a validated, reusable observation/guidance for evidence-creation steps. Require at least one additional independent family or investigation that reproduces the structural gap (or successfully applies the pattern) before reconsidering doctrine elevation. This preserves the real evidentiary gain from Stage C without prematurely elevating a single-investigation extraction to regimen-wide doctrine.

The goal of this review is not consensus or utility. It is to test whether the evidence produced by Stage C has earned the proposed doctrine before formal adoption. On the record examined, it has earned rigorous, bounded guidance; it has not yet earned doctrine.

## References (Traceability to Primary Sources)

All claims above are traceable to the R1A–D assessments, the prior adversarial review, the transition and E1 plan/interpretation documents, the E1 bundle artifacts (with passing validation), the reconnaissance inventory, the forensics investigation excerpts, the candidate doctrine assessment, and the methodology extraction assessment. Specific file paths and section references are given inline or in the evidence inventory above. No external or web sources were used.

---

*This assessment was produced as a read-only review. It does not modify any implementation, governance, or migration state. Boundary: limited to the Stage C investigation sequence and the doctrine proposal derived from it.*