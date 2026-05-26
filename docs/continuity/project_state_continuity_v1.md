# Project State Continuity v1

## Snapshot
- Repository: `assistant-training`
- Branch: `main`
- Head: `85ba267`
- Governance authority: Charter v5a + Appendix A v3a + Metric Spec v1a + canonical eval manifest contract.

## Current Experimental State
- Tuning-lineage experimentation is paused.
- Most recent isolated-variable run completed: i7.
- Current best clean baseline checkpoint: `stage_b_llama31_8b_base_v1_i3`.

## Durable Findings
- Runtime discipline remained stable across late iterations:
  - no-call correctness preserved at 100%
  - wrapper leakage preserved at 0%
- Post-i3 dominant failures shifted to schema-layer classes, not broad semantic collapse.
- i7 isolated intervention improved `payload_not_object` vs i6, but did not recover overall exact-valid heldout performance.

## Immediate Next-Thread Starting Point
- Start from i3 clean baseline for new recovery work.
- Keep overlap/contamination controls unchanged.
- Use single-primary-objective intervention declarations for each new iteration.
