# Stage D Continuity Handoff: D1 Complete, D2 Not Yet Authorized

Date: 2026-06-16

This document is authoritative handoff material for a new ChatGPT thread and a new Codex thread.
It summarizes the published D1 package, the preserved D0 blocker, and the boundary that must remain in place before any D2 mechanism-isolation planning could begin.
This document does not authorize execution, training, experimental design, arm design, run planning, preregistration creation, manifest edits, or hash-claim edits.

## 1. Repository State

- `main` is synchronized with `origin/main`.
- The working tree was clean at the time this handoff was prepared.
- The Stage D package set is published on `origin/main`.
- No D2 governance artifacts exist yet.

## 2. Latest Published Commit

- `bf6b4fb0df7b73e9f220298c993f4a77ff17deeb`
- Commit message: `Add D1 closure and D2 readiness assessment`
- This is the current published tip on `main`.

## 3. D0 Outcome

- D0 reconstruction framework is complete.
- Canonical-byte certification remains blocked.
- The unresolved `scripts/train_lora_sft.py` provenance gap remains a blocked provenance issue, not a repaired claim.
- D0 remains useful for non-training-script surfaces such as dataset identity, row identity, patch accounting, config diffs, manifest diffs, and eval-contract fidelity.

## 4. D0 Blocker Status

- D0 blocker `D0-BLK-TRAINING-SCRIPT-PROVENANCE-001` remains active and unchanged.
- No manifest edits are authorized.
- No hash-claim edits are authorized.
- No canonical-byte certification, row-ledger, or full certification execution is authorized.

## 5. Governance Transition Outcome

- Stage D transitioned from `Reconstruction-first` to `Current-tree mechanism isolation`.
- The transition preserved provenance integrity and scientific honesty.
- D1 formalized the working boundary for that transition: current stabilized implementation surfaces are the operative D1 baseline, and H1/H2 remain observational reference regimes, not replay targets.
- The transition preserved D1-only scope and did not open D2 planning or execution.

## 6. D1 Accomplishments

- Established the D1 governance foundation that preserves the D0 blocker and separates current-tree authority from canonical-byte certification.
- Published a D1 inventory specification that requires typed evidence references, structured confounds, relationship metadata, and explicit acceptance criteria.
- Published a D1 mechanism-hypothesis inventory that catalogs plausible candidate explanations for H1/H2-class behavior in read-only form.
- Normalized the inventory confound records so shared confounds are explicit, reusable, and structurally consistent.
- Published the D1 closure and D2 readiness assessment as the current handoff status note.

## 7. D1 Published Artifacts

Core D1 artifacts:

- [`docs/continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md`](./D1_GOVERNANCE_FOUNDATION_PACKAGE.md)
  Commit: `e2f7abe` `Add D1 governance foundation package`
- [`docs/continuity/D1_MECHANISM_HYPOTHESIS_INVENTORY_SPECIFICATION.md`](./D1_MECHANISM_HYPOTHESIS_INVENTORY_SPECIFICATION.md)
  Commit: `7c1eb2c` `Add D1 mechanism hypothesis inventory specification`
- [`docs/continuity/D1_MECHANISM_HYPOTHESIS_INVENTORY.md`](./D1_MECHANISM_HYPOTHESIS_INVENTORY.md)
  Commit: `9a40c15` `Add D1 mechanism hypothesis inventory`
- Normalization commit for the inventory confounds: `1819629` `Normalize D1 inventory confound records`

Supporting publication and handoff artifact:

- [`docs/current/status/D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md`](../current/status/D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md)
  Commit: `bf6b4fb` `Add D1 closure and D2 readiness assessment`

## 8. D1 Methodological Outcomes

- Evidence is typed by role. Only `behavioral_evidence` is direct support for a behavior claim.
- `governance_boundary_evidence`, `provenance_authority_evidence`, `evaluation_contract_evidence`, and `continuity_context_evidence` are not direct behavioral proof.
- Relationship metadata is descriptive only; it is not evidence, proof, prioritization, or execution guidance.
- Confounds are structured records, and shared confounds are reused across affected hypotheses instead of being restated as free text.
- The inventory remains a catalog of candidate explanations, not evidence that any explanation is correct.
- H1 and H2 remain observational reference regimes, not replay targets.
- The current stabilized trainer, dataset-builder, evaluation, and associated current-tree framework components remain the operative D1 baseline.

## 9. Current Authority Order

When D1 or D1-adjacent materials conflict, use the highest-precedence source available and treat lower-precedence material as subordinate context only.

1. D0 continuity and blocker documents
2. D1 Governance Foundation Package
3. D1 inventory specification
4. D1 mechanism-hypothesis inventory
5. D1 closure and D2 readiness assessment, plus current status notes
6. Any future D2 governance material, only after separate authorization

Lower levels must not override higher levels.

## 10. Current Non-Authorizations

This handoff does not authorize:

- D2 governance artifact creation
- D2 planning
- execution
- training
- experimental design
- arm design
- arm-specific run planning
- preregistration creation
- manifest edits
- hash-claim edits
- canonical-byte certification
- any reinterpretation of the D0 blocker as advisory

## 11. D2 Readiness Status

- D2 mechanism-isolation planning is not ready yet.
- A separate D2 governance decision is required before any planning begins.
- The D1 boundary remains intact, including the active D0 blocker and the no-manifest-edit and no-hash-claim-edit rules.
- H1 and H2 remain fixed observational reference regimes.
- No D2 execution path is authorized by this handoff.

## 12. Recommended Next Governance Action

- Keep D1 closed and published.
- Do not begin D2 planning yet.
- If future D2 work is desired, first obtain a separate D2 governance decision that states the authority order, scope, and boundary controls.

## 13. Recommended First D2 Activity If Later Authorized

If D2 is later authorized, the first activity should be a read-only authority and surface confirmation review that:

1. restates the D1 boundary in D2 terms,
2. confirms the fixed current-tree surfaces and observational reference regimes,
3. confirms the prohibited intervention classes remain prohibited,
4. identifies the minimum scope that any future D2 planning must preserve.

This should happen before any D2 arm concepts, run concepts, or execution concepts are discussed.
