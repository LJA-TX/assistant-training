# AGENTS.md Classification Assessment

**Repository:** `/opt/ai-stack/assistant-training` (canonical)
**Public target:** `LJA-TX/assistant-training`
**Request:** Independent classification of `AGENTS.md` as Public Core, Public Supporting, or Exclude.
**Constraints:** Assessment only. No repository modifications. No commits. No implementation.

**Date of assessment:** Current baseline (post-Wave 1, post-compatibility adoption, Phase 1 process infrastructure closed).

---

## 1. Executive Summary

`AGENTS.md` is a thin, intentionally route-oriented **process dispatcher skeleton (Phase 1)**. It provides:

- An authority precedence order.
- Mandatory pre-flight checks for all routes.
- A route selection table that maps trigger intents (slice execution, readiness/closure review, conformance slice, migration gate, publication checkpoint, push checkpoint, milestone determination, architecture/process assessment) to specific checklists and templates under `docs/framework/process_infrastructure/`.
- Explicit stop-and-escalate triggers.
- Hard boundaries stating what it must *not* contain (doctrine, scenario catalogs, migration semantics/procedures, protocol bodies, template bodies, checklist bodies).

In actual operation, it functions as the top-level execution control surface for recurring Stage B/C process work. Nearly every convergence artifact since its adoption begins with a line of the form: `Route selected from 'AGENTS.md': 'migration_gate'` (or equivalent).

**Classification recommendation:** **Public Supporting**.

It improves navigation, maintainability, automation, and agent/contributor guidance for the process layer. It is not required for a technically sophisticated reviewer to understand the methodology, the operating model, the primary value proposition, or how the regimen actually works at the substantive level. Prior internal publication-architecture work (PUBLIC_REPO_02, OSS_PKG_03, OSS_PKG_03A, PUBLIC_REPO_03) reached the same conclusion.

---

## 2. Operational Role Assessment

In actual practice, `AGENTS.md` serves as:

| Role | Strength | Evidence |
|------|----------|----------|
| **Process dispatcher / execution router** | Primary | Route table + repeated "Route selected from `AGENTS.md`" usage in convergence artifacts (e.g., STAGE_C9_POST_BLOCKER_REASSESSMENT.md:7, multiple C9/C10 migration-gate and conformance artifacts). |
| **Workflow governance surface** | Strong | Authority order (5 levels), pre-flight checks (scope, ownership, stop-and-escalate, hygiene/governance/git-ignore checklists), stop-and-escalate triggers (authority conflict, catalog contradiction, undefined ownership, scope expansion, methodology redesign, repository anomaly). |
| **Automation / agent contract** | Strong | Explicit contract for agents performing recurring work; live hard consumer of process asset paths (17 route references validated and rollback-protected during Wave 1 housekeeping). |
| **Navigation / maintainability aid** | Moderate-to-strong | Listed in README.md, docs/current/start_here.md, and docs/current/framework_vs_history.md as part of the reusable framework surface. Critical preservation priority in HOUSEKEEPING_PRESERVATION_INDEX.md ("Thin dispatcher, authority order, stop-and-escalate rules, and route map for recurring work. Preserve unchanged semantics."). |
| **Methodology definition** | None | Explicitly prohibited from containing doctrine, scenario content, migration semantics, or protocol bodies. The architecture proposal and extraction assessment treat it as the *control plane* above the actual process assets. |
| **Process infrastructure** | Core to the extracted infrastructure | Phase 1 closure determination treats the dispatcher + the referenced checklists/templates as the extracted unit. |

**Classification of role:** Primarily **process infrastructure + workflow governance + execution contract**. It is the thin routing and pre-flight layer for the reusable process asset library (`docs/framework/process_infrastructure/`).

It is not a passive README or contributor guide. It is an operational component that is actively consulted (by agents and by the historical record) to determine *which* reusable assets govern a given piece of work.

---

## 3. Dependency Analysis

**Question:** If `AGENTS.md` were removed from the future public repository, would a technically sophisticated reviewer lose an important understanding of how the project operates, how work is performed, how methodology is executed, or how governance is applied?

**Answer:** Partial loss, not critical loss for methodology understanding.

**What would still be intelligible:**

- The substantive methodology (non-inference discipline, bounded slice execution, package/reconciliation/zip hygiene, evidence preservation, blocker-oriented branch model, governance boundary enforcement) is documented in:
  - Doctrine (`docs/goal_charter_v5a.md`, `docs/appendix_a_operational_execution_contract_v3a.md`, `docs/metric_specification_v1a.md`).
  - `docs/current/framework_vs_history.md` and `docs/current/start_here.md`.
  - `docs/framework/lineages/` (distilled inflection points).
  - Selected `docs/framework/methodology/` retrospectives (especially STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md and STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md).
  - The executable regimen (`scripts/`, `evals/canonical_eval_manifest_v1.json`, core tests).
- The *intent* and *rationale* for the hybrid process architecture (dispatcher + protocols + templates + checklists) is fully explained in the architecture proposal and extraction assessment.
- The actual substance of recurring process work (what a package review must contain, what hygiene checks are required, what a readiness or closure determination must address) lives in the checklists and templates themselves, which would remain under `docs/framework/process_infrastructure/`.
- Historical usage traces would still exist in the convergence record (the artifacts that say "Route selected from `AGENTS.md`" would remain, even if the dispatcher file itself is absent).

**What would be lost or degraded:**

- The single, authoritative, thin surface that encodes the current operational classification of recurring work and the mandatory pre-flight + escalation contract.
- Immediate legibility of *why* a given convergence artifact used a particular route and asset set (the "Route selected..." line would become a dangling reference without the source table).
- Direct evidence of the authority hierarchy and stop-and-escalate discipline as a standing, machine- and agent-readable rule set.
- The precise mapping from intent to asset that was used to produce the body of process work that demonstrates the methodology in practice.

**Net effect:** A sophisticated reviewer would still understand *what* the regimen is and *how it works* at the level that defines the project's value proposition. They would have a modestly harder time reconstructing the exact operational mechanics of how the project organized and governed its own recurring process work. The loss is real for operational transparency and agent workflow reproducibility, but it is not a loss of the methodology itself.

---

## 4. Methodology vs Infrastructure Assessment

**Is `AGENTS.md` primarily:**

### A. Repository navigation / process infrastructure

**or**

### B. Part of the methodology itself

**Assessment: Primarily A.**

**Rationale:**

- The project's own architecture documents treat the dispatcher as the *control surface* above the process assets, not as a carrier of methodological content. STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md:26–33 and STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md:152–154 are explicit: the dispatcher classifies requests, enforces pre-flights, routes to protocol/template/checklist references, and defines the override hierarchy. The substance (decision sequences, evidence structures, operational steps) belongs in protocols, templates, and checklists.
- `AGENTS.md` itself declares its boundaries (lines 58–65): it must not contain doctrine specifics, scenario catalog content, migration semantics or procedures, protocol bodies, template bodies, or checklist bodies. It is self-defined as thin and route-oriented.
- The Phase 1 closure determination (STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md) validates the dispatcher precisely on the criteria of remaining thin, having correct route references, and not embedding prohibited content.
- The actual methodology of the regimen (how training/evaluation is performed, how non-inference is enforced, how evidence is preserved, how blockers are managed, how reproducibility is achieved) is carried by doctrine, the canonical evaluation contract, the core scripts, the lineages, and the selected methodology retrospectives — not by the route table.
- `AGENTS.md` is grouped with "framework assets" in preservation and navigation docs because it is part of the *active operational surface* of the canonical repository. That is a different classification axis from "is this part of the reusable methodology that defines the project's public value proposition."

It is infrastructure that makes the extracted process layer usable in a repeatable, governable, agent-friendly way. It is not the methodology the infrastructure supports.

---

## 5. Codex-for-OSS Perspective

**Question:** Would `AGENTS.md` materially strengthen the case for maintenance discipline, governance maturity, operational rigor, and agent-assisted workflow maturity?

**Answer: Yes.**

**Why it strengthens the case:**

- It is visible proof of deliberate extraction. The project did not leave recurring process work as long prompt boilerplate. It extracted a bounded dispatcher with explicit authority ordering, pre-flight hygiene/governance checks, and hard boundaries against scope creep into doctrine or protocol content.
- The stop-and-escalate triggers and authority precedence order are direct, legible signals of governance culture. A Codex-for-OSS reviewer looking for "serious project" indicators will see a small but non-trivial investment in making governance and process control surfaces explicit rather than implicit in individual execution prompts.
- It is the contract for agent-assisted workflow. Multiple independent reviews (including this one) and the historical record itself were produced under routes selected from this file. Retaining it lets a reviewer inspect the exact operational rules that agents were given for slice execution, migration gates, publication checkpoints, etc.
- During housekeeping, `AGENTS.md` was treated as a first-class hard consumer of repository paths (17 route-asset references required inventory, update, validation, and rollback protection). That treatment itself is evidence of maintenance discipline.
- Prior internal reviews (OSS_01, various housekeeping assessments) explicitly call out `AGENTS.md` + `docs/framework/process_infrastructure/` as providing "a lightweight but effective governance dispatcher."

**Limits of the signal:**

It is a small file. Its value as a maturity signal is real but modest in isolation. It is stronger in combination with the actual checklists/templates it routes to, the architecture and extraction assessments that motivated it, and the body of convergence artifacts produced under its routes.

**Conclusion under this lens:** For a reviewer whose evaluation criteria include operational rigor and agent-assisted workflow maturity, `AGENTS.md` is positive evidence worth having in the public surface. It is not, however, core methodological content.

---

## 6. Classification Decision

**Recommendation: Public Supporting**

**Detailed rationale:**

1. **Alignment with project definitions**
   - Public Core is material *required* to understand the methodology, operating model, primary value proposition, and how the regimen actually works.
   - Public Supporting is material that improves navigation, maintainability, automation, and contributor/agent guidance but is not essential to understanding the methodology itself.
   - `AGENTS.md` meets the Supporting criteria. The methodology and operating model are carried by doctrine, the evaluation contract + scripts, lineages, framework_vs_history, and selected methodology retrospectives. The dispatcher improves how one *navigates and executes* the process layer that supports that methodology.

2. **Consistency with prior publication architecture work**
   - PUBLIC_REPO_02_CURATED_REPOSITORY_ASSEMBLY_PLAN.md (section 6): "AGENTS.md belongs in Public Supporting, not Public Core." Rationale: helpful for process routing and agentic inspection; supports maintainability and automation; does not define the public method itself.
   - OSS_PKG_03_CURATED_REPOSITORY_DEFINITION.md (multiple matrices): "Public Supporting — Helpful process dispatcher and authority-order note, but not essential to the public understanding of the regimen." "Supporting — Helpful process routing, but not central to the regimen itself." "Useful history — A small process record, but not a core archive layer."
   - OSS_PKG_03A_CODEX_FOR_OSS_REASSESSMENT.md: retains "Public Supporting" classification even after adjusting other categories for reviewer value.
   - PUBLIC_REPO_03_HISTORICAL_EVIDENCE_SPINE_DESIGN.md: "Reference AGENTS.md only as a supporting navigation pointer, not as a historical evidence item."

3. **Self-description and design intent**
   - The file opens by calling itself a "minimal routing skeleton... intentionally thin and route-oriented."
   - Its boundaries and Phase 1 status statement make clear that the real protocol and process substance is elsewhere (or deferred).

4. **Operational reality in the canonical repo does not dictate publication classification**
   - In the full canonical repository, `AGENTS.md` has Critical preservation priority and is grouped with framework assets because the *operational* surface needs the dispatcher to function. Publication classification applies a different filter: what does a public reader need to understand the *regimen* (the project's public value), not what does the private operational team need to continue executing work.

5. **Marginal value for different public audiences**
   - Strictly minimal human-only public repo: could be omitted without material harm to a first-time reader's understanding.
   - Agent-friendly or "inspect the project's operational discipline" public repo: high value as supporting material. The project has already invested in making its process execution legible to agents; exposing that contract publicly is consistent with the "serious, disciplined, reproducible" signal the curated repo is trying to send.

**Exclude from public repository** is not recommended. The cost is low (small, stable file) and the supporting value for agent workflow transparency and governance signaling is positive.

**Public Core** is not recommended. It would overstate the file's role relative to doctrine, the executable regimen, the evaluation contract, and the distilled methodology records.

---

## 7. Confidence Assessment

**Recommendation:** Public Supporting

**Confidence level:** High (≈ 82/100)

**Strongest supporting evidence:**

- Convergence of multiple prior artifacts written specifically to define the Public Core / Public Supporting / Curated Historical Evidence boundary for this exact repository (PUBLIC_REPO_02, OSS_PKG_03, OSS_PKG_03A, PUBLIC_REPO_03). These assessments directly addressed `AGENTS.md` and placed it in Supporting.
- The file's own text and the design artifacts that produced it (architecture proposal, extraction assessment, Phase 1 closure determination) consistently describe it as a thin dispatcher/router, not a carrier of methodological content.
- Concrete operational usage pattern ("Route selected from `AGENTS.md`") demonstrates it is real process infrastructure, while the content of the routes demonstrates that the actual process knowledge lives in the referenced assets.
- The preservation index gives it Critical priority for *canonical* purposes while the publication research gives it Supporting priority for *public* purposes — a coherent distinction once the two classification axes are separated.

**Strongest counterargument:**

- `AGENTS.md` is listed in `docs/current/start_here.md` and `docs/current/framework_vs_history.md` as part of the reusable framework surface, and it is the actual entry point used to produce the body of process work (slices, packages, gates, closures) that demonstrates the methodology in practice. A reviewer could reasonably argue that "how the project actually performs and governs its recurring work under the regimen" is part of understanding the operating model, and that the dispatcher is the most compact expression of that "how."
- In a strictly agent-centric public inspection scenario, the absence of the dispatcher slightly obscures the provenance of the process artifacts a reviewer is looking at.

The counterargument is legitimate on the "operational transparency" axis but does not, in the assessor's judgment, rise to the level of "required to understand the methodology itself" under the definitions provided.

---

## 8. Final Recommendation

**Classify `AGENTS.md` as Public Supporting** in the curated public repository (`LJA-TX/assistant-training`).

Include it in the root alongside `README.md` (and any other supporting hygiene files such as `.gitignore` if retained). Do not place it in the primary "understand the methodology and regimen" reading path; treat it as an operational-support and agent-guidance artifact that strengthens the maturity signal without being a prerequisite for grasping the project's public value.

This classification is consistent with the project's own prior publication-architecture analysis, with the file's self-described scope and boundaries, and with the distinction between (a) what is needed to understand the regimen and (b) what improves the legibility and reproducibility of how the project operates that regimen.

---

**End of assessment.** No changes were made to any repository content. This document is the sole deliverable.
