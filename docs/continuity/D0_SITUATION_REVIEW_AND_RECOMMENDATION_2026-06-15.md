# D0 Situation Review and Independent Recommendation

**Date:** 2026-06-15
**Context:** Independent assessment of the current Stage D / D0 situation following implementation and execution of D0 dry-run tooling (commit 4896d0f).
**Scope:** Review of the unresolved `scripts/train_lora_sft.py` provenance gap, D0 blocker status, and options for moving forward on H1/H2 mechanism isolation.
**Constraints observed:** No files were modified, no code implemented, and no manifests or hash claims edited during this assessment.

---

## Key Facts (Established from Repository Evidence)

- Stage D originated as H1/H2 mechanism isolation work. D0 was intended to verify reconstruction fidelity of the frozen `i3`/`H0`/`H1`/`H2` surfaces before authorizing causal experiments (A1/A2/A3).
- D0 dry-run tooling was added in commit `4896d0f` ("Add D0 reconstruction verification dry-run tooling").
- D0 dry-run findings:
  - `build_dataset_v1.py`: `stale_but_resolvable` (historical resolution via git commit reference exists).
  - `train_lora_sft.py`: `stale_unresolved`.
- Canonical hash claim (from `evals/canonical_eval_manifest_v1.json`):
  - `training_script_sha256`: `28900accae3d6abf05ddb9e86b41c03ad3c812a683f3af343bffa94281e14c8b`
- Current live hash:
  - `faf6cd4b676e230c5d2797392bc2fca204752d012f3e80e71c0af4ced7288432`
- Focused provenance investigation (see `docs/continuity/TRAIN_LORA_SFT_PROVENANCE_INVESTIGATION.md`): No reachable git blob for `scripts/train_lora_sft.py` reproduces the canonical hash. GitHub serves as the effective backup; the bytes are treated as likely unrecoverable absent new evidence.
- Script history timeline (from investigation):
  - Canonical claim introduced ~2026-05-26 (commit `82c6b32`).
  - Reachable script versions exist from `7b694fb` onward.
  - Final change: 2026-06-06 (`97491ef` — "Adopt compatibility path decoupling slice"): repo-root/config resolution hardening only. No meaningful change to training logic.
  - H1/H2 runs executed 2026-06-11 using the post-06-06 script.
- Current documented state (from `docs/continuity/D0_BLOCKER_REGISTER.md`, `D0_DRY_RUN_PROVENANCE_FINDING.md`, `D0_PROVENANCE_BLOCKER_*` series, and `D0_ACCEPTANCE_CRITERIA.md`):
  - D0 canonical-byte certification is blocked (fail-closed).
  - No manifest/hash claim edits are allowed.
  - No reconstruction or A1/A2/A3 experiments have been authorized.
  - Historical H1/H2 remain preserved as observational evidence.
  - Pre-existing D0 governance artifacts uniformly recommend keeping the block under "strict resolution required" (Option 1) until preserved bytes or explicit governance re-scope.

The D0 tooling (see `docs/continuity/D0_HISTORICAL_CODE_RESOLUTION_PLAN.md`, `scripts/d0_verification/`, `D0_IMPLEMENTATION_ARCHITECTURE.md`, etc.) is explicitly designed to distinguish `stale_but_resolvable` from `stale_unresolved` and to keep certification fail-closed on unresolved provenance gaps.

---

## Options Evaluated

1. Continue trying to resolve D0 canonical-byte certification?
2. Re-scope D0 into a dual-track path?
3. Freeze D0 certification and start a fresh current-tree mechanism-isolation program using H1/H2 as clues rather than byte-perfect reconstruction targets?
4. Do something else?

---

## Assessment

### 1. Continue trying to resolve D0 canonical-byte certification
- **Scientific integrity**: High *if successful*, but the pinned hash predates the actual script used to generate the H1/H2 surfaces that motivate the science.
- **Reproducibility**: Strong for the manifest claim; low relevance to the H1/H2 results actually observed.
- **Implementation cost**: Low-to-medium for passive search; potentially very high for deep archival work with uncertain yield. Investigation already concludes "likely unrecoverable."
- **Publication risk**: Low while blocked; increases with deadlock.
- **Risk of contaminating future causal conclusions**: Low (remains blocked).
- **Key issue**: Even recovery would tie future work to a trainer state that was not the one used for the key results.

### 2. Re-scope D0 into a dual-track path (historical + current-tree)
- **Scientific integrity**: Defensible only with extreme rigor and labeling.
- **Reproducibility**: Creates a split story; high interpretive burden.
- **Implementation cost**: High (parallel ledgers, reports, sustained review overhead).
- **Publication risk**: High (fragile narratives, easy mis-citation or confusion).
- **Risk of contaminating future causal conclusions**: High. Future claims become vulnerable to "which trainer version?" attacks.
- Existing D0 governance documents already classify dual-track as high-risk and requiring explicit authority change.

### 3. Freeze D0 certification and start a fresh current-tree mechanism-isolation program
- **Scientific integrity**: Strongest practical option. H1/H2 are the real observed high-capability regimes (H2: 48% exact JSON). They were produced with the June-6+ (current live) script. The actual mechanism carriers are the preserved H1/H2 100-row patch surfaces (JSONL data + summaries + configs + eval contract). These are fully preserved, hash-verifiable, and independent of the trainer script bytes. The trainer is implementation scaffolding, not the causal object.
- **Reproducibility**: Excellent. All necessary artifacts (preserved data patches, row identities via existing plans, configs, frozen canonical eval manifest, current stabilized script) are in the current tree.
- **Implementation cost**: Lowest viable path. Avoids chasing unrecoverable bytes. Existing D0 row-ledger, diff-certification, and surface-fidelity machinery can still be applied to the *data*, *config*, *manifest*, and *eval* surfaces.
- **Publication risk**: Manageable with precise scoping language in any preregistration or paper (e.g., "H1/H2 treated as fixed observational reference regimes from the 2026-06-11 snapshot; mechanism isolation executed on current stabilized tooling against the same preserved data surfaces").
- **Risk of contaminating future causal conclusions**: Lowest. Enables clean separation between "observational H1/H2 evidence" and "current-tree controlled reproduction + mechanism tests." Avoids any implication that we byte-replayed a non-existent early trainer.
- Alignment: The `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md` already plans to use published H1/H2 runs as frozen R0/R1/R2 references and to reconstruct surfaces from preserved JSONL/summaries rather than requiring trainer replay.

### 4. Something else (hybrid)
A clean, low-risk hybrid is viable:
- Formally scope-limit the training-script canonical-byte requirement inside D0 (document the gap as a closed historical anomaly for the early manifest claim).
- Complete the remainder of D0 verification focused on the fully preserved data/config/manifest/eval surfaces using the existing authority matrix, implementation plan, validation checklist, and acceptance criteria.
- Proceed with current-tree mechanism isolation, treating H1/H2 as fixed references.
- Continue passive, low-cost archival search in parallel without blocking progress.

This extracts the maximum value from the D0 investment without being permanently hostage to an unresolvable early hash claim.

---

## Recommendation

**Primary recommendation: Option 3 (Freeze D0 canonical-byte certification for the training script and initiate a current-tree H1/H2 mechanism-isolation program), supplemented by completing the non-code portions of D0 reconstruction verification on the preserved data/config/eval surfaces.**

Do not pursue aggressive resolution of the missing training-script bytes as a prerequisite for mechanism work. Do not adopt dual-track certification. Do not edit manifests or hash claims.

Treat the confirmed `stale_unresolved` status for `train_lora_sft.py` as a documented, closed provenance gap specific to the early (2026-05-26) manifest claim. The D0 tooling has already performed its intended function by making the distinction visible.

**Rationale summary**:
- The D0 framework correctly surfaced an unresolved gap. Governance should now act on that information.
- The H1/H2 signal worth isolating was generated under the *current* script. The data surfaces (patches) are the objects that carried the capability improvement; those surfaces are independently verifiable today.
- Continuing to block all progress on an unresolvable early trainer hash harms the ability to capitalize on the actual empirical result (H1/H2) more than it protects long-term integrity.
- Current-tree work on preserved surfaces maximizes reproducibility and cleanly bounds future attribution.
- This approach is consistent with the direction already outlined in the 2026-06-14 H1/H2 continuity note and leverages (rather than discards) the substantial D0 planning and tooling artifacts.

---

## Best Next Step

Produce a short, authoritative governance/continuity note that:
1. Records the confirmed `stale_unresolved` finding for the training script and the timing mismatch relative to H1/H2 execution.
2. Explicitly scopes the remaining actionable value of D0 to data-surface / row-identity / config / manifest / eval-contract fidelity verification (using the pre-existing `D0_RECONSTRUCTION_AUTHORITY_MATRIX.md`, implementation plan, validation checklist, and acceptance criteria for non-code artifacts).
3. Authorizes (under appropriate future process) a current-tree, preregistered H1/H2 mechanism-isolation program that:
   - Uses the published H1/H2 runs and their preserved output artifacts as fixed reference regimes (R1/R2).
   - Defines A1 (H2-like positive control), A2 (matched semantic control with weaker outer-envelope), A3 (anchor step-down under preserved envelope), etc., against the current stabilized script + builder.
4. Preserves the fail-closed rule for any future claim that would require the missing canonical trainer bytes.

This note should be placed alongside the existing D0 continuity package and the H1/H2 post-publication continuity document.

This path protects long-term credibility while enabling the project to advance on the highest-value remaining scientific question.

---

## References (Key Supporting Artifacts)

- `docs/continuity/D0_BLOCKER_REGISTER.md`
- `docs/continuity/D0_DRY_RUN_PROVENANCE_FINDING.md`
- `docs/continuity/D0_PROVENANCE_BLOCKER_RECOMMENDATION.md`
- `docs/continuity/D0_PROVENANCE_BLOCKER_RISK_ASSESSMENT.md`
- `docs/continuity/D0_PROVENANCE_BLOCKER_GOVERNANCE_OPTIONS.md`
- `docs/continuity/TRAIN_LORA_SFT_PROVENANCE_INVESTIGATION.md`
- `docs/continuity/D0_HISTORICAL_CODE_RESOLUTION_PLAN.md`
- `docs/continuity/D0_ACCEPTANCE_CRITERIA.md`
- `docs/continuity/D0_RECONSTRUCTION_AUTHORITY_MATRIX.md`
- `docs/continuity/D0_IMPLEMENTATION_ARCHITECTURE.md`
- `docs/continuity/post-publication_h1_h2_mechanism_isolation_continuity_2026-06-14.md`
- `docs/current/status/TRAINING_RUN_HISTORY.md` (H1/H2 results)
- `evals/canonical_eval_manifest_v1.json` (source of the hash claim)
- `scripts/d0_verification/` and `scripts/d0_verify.py` (dry-run implementation)
- `docs/phase_d/` (earlier Phase D roadmap reconciliation context)

---

*This document was created by capturing the independent review and recommendation delivered in response to the 2026-06-15 query on the Stage D / D0 situation. It contains no changes to code, manifests, hashes, or any other repository state beyond the creation of this continuity artifact.*
