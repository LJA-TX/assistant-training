# Gen-2 Program Charter

Date: 2026-06-21

**Status:** Draft. Documentation-only synthesis of prior Gen-2 strategic assessments. This charter does not authorize D2 planning, D2 execution, experiment design, treatment-arm design, run planning, preregistration creation, manifest edits, hash-claim edits, training, evaluation execution, or governance reinterpretation.

`Gen-2` is used here as a strategic program label only. It does not replace the repository's existing stage, family, or blocker terminology.

## Scope

This charter establishes the authoritative identity, boundaries, objectives, governance expectations, success criteria, and constraints for a prospective second-generation evidence program ("Gen-2").

It synthesizes:

- [GEN2_PROSPECTIVE_EVIDENCE_PROGRAM_ASSESSMENT.md](./GEN2_PROSPECTIVE_EVIDENCE_PROGRAM_ASSESSMENT.md)
- [GEN2_STRATEGIC_DIRECTION_OPTIONS_ASSESSMENT.md](./GEN2_STRATEGIC_DIRECTION_OPTIONS_ASSESSMENT.md)
- [GEN2_SCOPE_BOUNDARY_ASSESSMENT.md](./GEN2_SCOPE_BOUNDARY_ASSESSMENT.md)

Supporting context includes the published Gen-1 state: Stage B complete; Stage C complete and closed as historical work with retained guidance; D1 complete and published; the curated Llama 3.1 baseline evidence package; `D0-BLK-TRAINING-SCRIPT-PROVENANCE-001` remains active; D2 mechanism-isolation planning is not authorized; the public repository remains a bounded curated package.

This document is documentation-only. It does not constitute authorization for any execution, design, or planning activity.

## 1. Purpose

Gen-2 exists to convert Gen-1's strongest outputs from descriptive and governance-rich evidence into durable explanatory knowledge with first-class provenance and observability.

Gen-2 should answer the questions Gen-1 deliberately left open:

- what actually explains the strongest observed tool-call capability regimes;
- which tradeoffs are intrinsic versus incidental;
- which lessons are family-specific versus method-general; and
- what evidence must be captured from day one so future conclusions do not depend on retrospective reconstruction.

## 2. Program Identity

Gen-2 is framed as an **explanatory-comparability and observability program** for strong structured tool-calling behavior and its tradeoffs.

The preferred combined shape is:
- primary identity: explanatory-comparability;
- required foundation: observability-first;
- explicit analytical lens: tradeoff-characterization;
- bounded sub-question: mechanism isolation.

The safer, generalized framing is:

"Gen-2 explains strong tool-calling behavior and its tradeoffs in a reusable, evidence-disciplined way, using H1/H2 as the strongest current anchor comparators."

Gen-2 is not:
- a reconstruction-completion program;
- a broad performance-chase program;
- a reopening of Stage C;
- a public-package expansion exercise; or
- an implicit D2 execution program.

The central strategic move is to treat Gen-1 as a completed first-generation evidence program and orient future work around explanatory comparability, observability discipline, and mechanism-quality evidence under preserved governance boundaries.

## 3. Objectives

1. Clarify the explanatory surfaces behind strong structured tool-calling behavior and its associated safety, no-call, and runtime-discipline tradeoffs, using H1/H2 as high-signal observational reference regimes rather than as replay targets or the sole definition of success.
2. Distinguish descriptive observations, associative findings, candidate mechanisms, and accepted mechanism claims at the correct evidentiary tier.
3. Determine which observability and provenance requirements are mandatory when prompt construction, render path, dataset composition, or evaluation contract materially affect interpretation.
4. Separate durable methodology lessons from one-family historical artifacts.
5. Strengthen the bridge between offline canonical evaluation findings and runtime-behavior interpretation without assuming they are interchangeable.
6. Produce reusable methodological assets (evidence-role taxonomies, claim formats, confound schemas, surface-declaration protocols, comparison rules) that support later authorized work.

Valuable Gen-2 question classes (in-scope):
- Mechanism questions: what minimal current-tree surfaces plausibly explain strong tool-calling behavior and its tradeoffs.
- Comparability questions: how preserved historical reference regimes should constrain present-day interpretation without becoming replay mandates.
- Observability questions: what must be captured so prompt, dataset, configuration, and evaluation surfaces are interpretable from first principles.
- Generalization questions: which Gen-1 lessons survive across additional families, render contracts, or model baselines.
- Claim-quality questions: how evidence tiers, fixed-surface declarations, and confound handling should bound acceptable conclusions.

## 4. Non-Goals

Gen-2 should explicitly **not** be defined by:
- clearing the D0 blocker or recovering missing canonical trainer bytes;
- replaying H1 or H2 as success targets;
- reopening Stage C as an active runtime-output investigation;
- broad dataset redesign without a bounded explanatory question;
- benchmark or leaderboard chasing detached from mechanism and safety interpretation;
- public-package front-door polish as a scientific objective;
- experiment design, treatment-arm design, run planning, preregistration, or execution authorization;
- governance rewrite, metric reinterpretation, or blocker weakening.

Question classes that should not define Gen-2 include historical certification cleanup, front-door refinement as substitute for evidence generation, re-litigation of closed Stage C findings, unbounded optimization sweeps, any attempt to weaken the D0 blocker or relabel H1/H2, and any implicit transition from strategic framing into treatment-arm design, run planning, or execution.

## 5. Scope Boundaries

Gen-2 uses a three-part scope model:

### 5.1 Work That Naturally Belongs Inside Gen-2
- Core explanatory work: explanatory analysis of strong structured tool-calling behavior and its tradeoffs; compare-and-contrast across current-tree baselines, frozen controls, and observational reference regimes; interpretation at the correct tier; joint treatment of capability, safety, no-call, runtime-discipline, and wrapper-behavior tradeoffs.
- Core comparability work: preservation and clarification of comparison classes, control classes, and fixed surfaces; analysis of legitimate comparisons under the frozen contract; boundary-setting for historical surfaces; regime-specific vs. method-general identification.
- Core observability work: definition of evidence that must be captured at source; prompt-surface observability rules; provenance framing for claim-bearing artifacts; preservation of evidence-creation machinery when part of the reproducibility boundary.
- Core evidence-quality work: claim-tier discipline; explicit confound handling; evidence-role separation; overclaim prevention; contamination and drift awareness.
- Core methodological inheritance work: carrying forward durable lessons from Stage C and D1; refining inheritance for future families; clarifying what is ready to generalize versus local.

### 5.2 Work Adjacent To Gen-2 But Outside Its Identity
- General repository support work (public-package front-door maintenance, publication architecture, housekeeping, path compatibility, generic infrastructure).
- General execution-preparation work (future D2 governance packaging, study-design templates, generic validation/reporting scaffolds).
- Broad capability-development work (model-improvement aimed primarily at raising metrics, broad dataset redesign not anchored to explanatory question, training optimization, deployment/productization refinements).

These may support or be informed by Gen-2 but are not Gen-2's scientific identity.

### 5.3 Work That Actively Conflicts With The Gen-2 Identity (Out-of-Bounds)
- Replay and reconstruction identity: historical replay framing; byte-perfect reconstruction as main agenda; treating H1/H2 as targets to be recovered; using current-tree outputs as proof of blocked canonical-byte continuity.
- Capability-chasing identity: benchmark-maximization as primary success criterion; execution-first optimization sweeps; treating exact JSON gains as sufficient without tradeoff interpretation; allowing output volume to substitute for explanatory clarity.
- Revisionist evidence practices: heuristic repair of missing evidence; silent contract drift; implicit evidence-tier mixing; post-hoc reinterpretation that weakens provenance discipline.
- Boundary-breaking governance behavior: D0 blocker downgrades; reclassification of H1/H2 into replay targets; manifest or hash-claim edits without separate authority; design or execution drift under the cover of strategic framing.

In-scope question classes are listed in Objectives. Out-of-scope question classes include selection of specific treatment arms, execution of specific runs, authoring of manifests or preregistrations, operational replay of H1/H2, recovery of blocked canonical bytes, fastest path to better benchmark scores independent of explanation quality, and deployment/productization paths.

## 6. Non-Negotiable Principles

Foundational prerequisites (required for any activity claiming to belong inside the Gen-2 identity):
- Preserved authority order.
- Preserved D0 blocker and D1 boundary.
- Frozen-contract discipline.
- Explicit separation between current-tree baseline and historical reference surfaces.
- H1/H2 compare-only treatment.
- Explicit evidence-role framing.
- Explicit claim-tier discipline.
- Observability at source.
- Provenance preservation.
- Tradeoff-aware interpretation.

Durable lessons from Gen-1 that remain non-negotiable:
1. Strong offline evaluation gains do not, by themselves, explain runtime behavior or safety behavior.
2. Exact rendered prompts and their provenance are first-class evidence when prompt construction affects interpretation.
3. Missing evidence must remain missing; substitution, backfill, or inference-based repair damages credibility.
4. Capability improvement and safety/no-call regression must be interpreted together rather than as separate scoreboards.
5. Frozen contracts, pinned surfaces, structured validation, and append-only evidence history are part of the scientific method, not clerical overhead.
6. Candidate-mechanism work requires typed evidence roles and structured confounds or it will drift into narrative overclaim.
7. Evidence-creation mechanisms matter when they are the minimal reproducibility path and should be preserved alongside the resulting evidence objects.

Day-one observability, provenance, and evidence-capture requirements for any future Gen-2 work:
- Exact rendered prompt capture whenever prompt construction materially affects interpretation.
- Row identity, source provenance, render-path metadata, template identity, and hashes attached to prompt-surface evidence.
- Explicit recording of fixed surfaces, comparison class, control/reference class, and allowed-to-vary surfaces for every claim-bearing artifact.
- Preservation of configs, dataset versions, script identities, seeds, environment pinning, training summaries, and evaluation summaries.
- Strict separation of behavioral evidence from governance, provenance, contract, and continuity-context evidence.
- Structured confound records attached to claim-bearing artifacts.
- Preservation of evidence-creation code and validation outputs when they are the minimal reproducibility path.
- Append-only history and explicit versioning for prompt, render, and evaluation-contract changes.

Necessary scope boundaries to preserve the explanatory-comparability doctrine:
1. Comparison must remain distinct from replay.
2. Explanation must remain distinct from optimization.
3. Observability must be captured at source rather than reconstructed later.
4. Provenance gaps must remain visible rather than repaired narratively.
5. Evidence tiers must remain explicit.
6. Tradeoffs must be interpreted jointly rather than selectively.
7. Historical reference regimes must remain compare-only.
8. Frozen measurement contracts must remain stable unless separately re-governed.
9. Strategic framing must remain distinct from operational authorization.

## 7. Governance Framework

Gen-2 operates under a minimal governance framework intended to sustain coherence over multiple years:

- A maintained charter (this document) that states identity, non-goals, success/failure criteria, and boundary rules. Revisions require explicit governance action.
- Mandatory pre-activity surface for any claim-bearing work: documented comparison class, fixed/varying surfaces, evidence-role typing, claim tier, and observability checklist.
- Published authority order (see section 11) that places D0 blocker, frozen contract, D1 governance foundation, and this charter above new work.
- Append-only history for Gen-2 framing decisions and boundary reviews.
- Periodic identity and boundary audits (time- or milestone-based) that test activity against the charter and publish outcomes.
- Explicit rule: movement from analysis or framing into design, arm definition, run planning, or execution requires a separate authorization package.
- Stable outsider-facing description (section 13) and explicit statement of what Gen-2 will never measure itself by.
- Prohibition on reclassifying reference regimes as targets without higher-order authority.

Gen-2 work must follow the same spirit of admissible vs. prohibited interventions established in the D1 governance foundation (read-only/review-oriented/preregistration-oriented only; no mutation, no execution, no authority overrides).

## 8. Success Criteria

Success is distinguished across four dimensions.

### Program Success
The Gen-2 program produces a coherent, bounded, reusable explanatory methodology whose outputs remain trustworthy and transferable over multiple years and families. The repository can explain its strongest observed capability regimes and their tradeoffs without depending on retrospective narrative repair. Future conclusions are stated at the correct evidentiary tier. Observability failures do not recur. H1/H2 and other reference regimes are treated as well-understood scientific comparators. The program definition is broad enough to support later authorized work without being captive to one historical anomaly. The program produces reusable methodological assets that later work can adopt directly.

Program success is measured in durability and transferability of the method, not volume of findings or proximity to any historical peak.

### Scientific Success
Explanatory claims are correctly tiered (descriptive, associative, mechanistic candidate, or accepted) with named comparison classes, fixed surfaces, and structured confounds. Differences are interpreted as explanatory, descriptive, or too confounded. Tradeoffs are characterized as structural, incidental, or unresolved. Generalizable lessons are separated from regime-specific artifacts. Offline and runtime interpretations are bridged only where evidence supports it. The evidence threshold for elevating any candidate mechanism or retained guidance is explicit and met only when warranted.

### Operational Success
New evidence slices (when authorized) attach required metadata at creation time. Append-only history and frozen-contract discipline are visibly preserved. Surfaces remain inspectable and coherent. No unintended drift occurs in comparison classes, hashes, or contracts. Evidence-creation mechanisms are preserved when they constitute the reproducibility boundary. Hygiene, path resolution, and publication boundaries are maintained.

### Governance Success
Authority order is preserved. The D0 blocker remains active and unchanged. H1/H2 remain compare-only. Claim discipline is enforced. No scope creep into execution, replay, or optimization occurs under strategic framing. Strategic documents do not imply execution authority. Boundary reviews occur and are documented before drift can take hold. The charter itself remains the controlling document for Gen-2 identity.

## 9. Failure Modes

Gen-2 fails at the program level when:
- It becomes, in practice, a vehicle for replaying or recovering H1/H2-class behavior.
- Explanatory language justifies capability maximization or benchmark improvement detached from joint tradeoff analysis and tier discipline.
- Observability and provenance gaps are routinely discovered only after interpretation begins.
- High activity and local findings are generated but no durable, adoptable methodology is produced.
- Governance boundaries erode (D0 blocker softened, reference regimes relabeled, framing treated as execution authority, evidence tiers mixed for convenience).
- The repository's face shifts from disciplined explanatory work to historical reconstruction or gap-closing stories.

Principal risks of repeating Gen-1 mistakes include allowing observability gaps post-interpretation, collapsing correlation into mechanism claims, confusing current-tree comparability with historical certification, chasing gains without joint safety accounting, mixing evidence tiers, and letting strategic framing drift into unauthorized design or execution.

## 10. Drift Indicators

**Identity drift:**
- Framing increasingly centers "recovering or explaining the strongest observed regime" as the program's core.
- H1/H2 migrate from "anchor comparators" to "the thing we are trying to do again."
- Success language is dominated by capability metrics without joint tradeoff accounting.
- Work expands to any explanatory question without bounding to the core charter.

**Governance drift:**
- Strategic documents contain arm concepts, run sequencing, or "next steps" that imply authorization.
- The D0 blocker is described as legacy or advisory.
- The D1 inventory is treated as an execution backlog.
- Authority order is inverted.

**Evidence-discipline drift:**
- Missing surfaces are inferred or narratively repaired.
- Behavioral scores support mechanism claims without proper tier, preregistration, or controls.
- Surfaces are compared without explicit verification or declarations.
- Confounds appear only in prose.

**Leading indicators (monitor before serious drift):**
- Language such as "closing the gap," "reproducing the H1/H2 regime," or "recovering the strong behavior."
- Proposals for "quick comparisons" without prior surface declarations and checklists.
- Rising ratio of new behavioral artifacts to governance/observability artifacts.
- Questions about relaxing the frozen contract or D0 boundary for practicality.
- Framing success in terms of volume, speed, or metric movement rather than explanatory clarity or methodological inheritance.

Any leading indicator should trigger a boundary review.

## 11. Authority Relationships

When Gen-2 materials conflict, use the highest-precedence source and treat lower-precedence material as subordinate context only.

1. D0 continuity and blocker documents (including `D0-BLK-TRAINING-SCRIPT-PROVENANCE-001`).
2. D1 Governance Foundation Package and D1 closure/handoff materials.
3. Frozen evaluation contract and canonical evaluation manifest.
4. This Gen-2 Program Charter.
5. Current status, project outcomes, training run history, and baselines (as context).
6. Any future Gen-2 preregistration or planning artifacts (only after separate authorization).

Lower levels must not override higher levels.

Gen-2 does not supersede the D0 blocker, D1 boundary, or frozen contract. This charter defines the framing boundary for Gen-2 work; it does not authorize execution. Any D2 planning requires a separate D2 governance authorization package that restates boundaries and authority order. If such a package is later authorized, it becomes the governing authority for D2-scoped work rather than a subordinate planning artifact under this charter.

The D1 mechanism-hypothesis inventory is a read-only starting catalog of candidate explanations, not an execution backlog or proof of any mechanism.

## 12. Treatment of H1/H2

H1 and H2 are treated as:
- high-signal observational reference regimes;
- anchor comparators for explanatory work;
- preserved historical evidence surfaces;
- scientific inputs, not scientific destiny.

H1 and H2 must **not** be treated as:
- replay targets;
- success targets;
- canonical targets;
- the sole definition of Gen-2;
- substitute proof for current-tree or canonical-byte claims.

H1/H2 remain published under internal reference regimes (distinct from canonical baselines) precisely because they exhibit capability gains accompanied by safety/no-call regressions. They are report-only scientific comparators.

This boundary exists because H1/H2 are central evidence objects but not legitimate identity monopolists. Generalization and additional reference regimes are optional extensions, not prerequisites.

## 13. Outsider-Facing Description of Gen-2

Gen-2 is a second-generation evidence program for tool-calling assistants that moves beyond baseline publication and historical closure into explanation. It uses the repository's published baselines, Stage C observability lessons, D0/D1 governance boundaries, and D1 hypothesis inventory as fixed inputs. It focuses on identifying which current-tree conditions actually produce strong structured tool-calling behavior, which tradeoffs accompany those conditions, and what provenance and observability must be captured from the start so later conclusions are reproducible, inspectable, and not dependent on retrospective reconstruction.

Gen-2 treats H1/H2 as anchor comparators and preserved evidence surfaces, not as targets to be recovered or definitions of success. Success is defined in terms of durable explanatory power, evidence discipline, and reusable methodology rather than local capability maxima.

## 14. Conditions Under Which the Charter Should Be Reconsidered

This charter should be reconsidered (via explicit governance process, not incremental editing) when any of the following occur:
- D2 is separately authorized and a D2 governance package is published that requires integration or boundary adjustment.
- The D0 blocker status changes (downgrade, resolution by new authoritative evidence, or formal reinterpretation).
- The frozen evaluation contract or canonical manifest is re-governed.
- Significant new cross-family or cross-contract evidence materially changes the durability of Gen-1 lessons or the threshold for generalization.
- The program has produced a sufficient body of reusable methodology that a successor framing (Gen-3 or equivalent) is warranted.
- Authority conflicts arise that cannot be resolved under the existing order.
- The assumptions in the Current Basis section of this charter no longer hold.

In all cases, reconsideration must preserve the core non-negotiable principles and the distinction between strategic framing and operational authorization.

## Foundational Inputs (Preserved)

Gen-2 treats the following as fixed starting inputs (not optional background):
- Measurement and doctrine surfaces (goal charter, Appendix A, metric specification, frozen canonical evaluation manifest, published Llama 3.1 baseline package).
- Closure and boundary determinations (Stage B completion, Stage C closure continuity package, D0-to-current-tree governance transition, D1 governance foundation and closure/handoff, D1 mechanism-hypothesis inventory specification and inventory).
- Explanatory starting corpus (living training run history, D1 inventory with typed roles and structured confounds).

## Gen-1 Assumptions Challenged

Gen-2 challenges or discards:
- Byte-perfect reconstruction as the right organizing question.
- Exact-call improvement alone as sufficient to define success.
- Single-family or single-regime evidence as sufficient for doctrine or strong mechanism claims.
- H1/H2 as replay targets rather than observational reference regimes.
- Broader or later modifications as automatically more informative.
- Interchangeable mixing of behavioral, governance, provenance, and continuity evidence.

## Boundary Confirmation

This charter is documentation-only.

It does not authorize:
- D2 planning or D2 execution;
- experiment design;
- treatment-arm design;
- run planning;
- manifests;
- preregistrations;
- training or evaluation execution; or
- governance reinterpretation.

All future work claiming to operate inside the Gen-2 identity must be tested against this charter for scope, principle, and drift compliance before proceeding.

---

**End of charter draft.** This document should be reviewed against the hygiene review checklist, governance boundary verification checklist, and publication readiness checklist prior to any integration or push. No execution surfaces, manifests, or design artifacts were modified or created in the preparation of this charter.
