# Stage B i10 Micro-Probe Execution Plan (Bounded)

## Executive Summary
This plan prepares one minimal viable micro-LoRA probe to answer:

> Are we improving generalized procedural commitment, or just producing more sophisticated shell ritualization?

Current evidence supports **conditional forward movement** only. i10 data quality and governance gates are clean, but legacy-family exposure remains dominant and scalar substitution is still the primary collapse-watch risk.

## Current Evidence Snapshot
- i10 intervention rows: `102` (read_file `60`, rg_search `42`)
- Ambiguity hard blocks: clean
- Heldout/tool_holdout contamination: zero overlap
- Diversity + anti-homogenization: pass
- Anchor dominance ratio: `0.215686` (below threshold)
- Scalar rebound proxy delta vs i9: `+0.05098` (flagged)
- Targeted composition still legacy-heavy: `i3_*` ~`79%` of targeted rows; `i9+i10 conv` ~`21%`

## Micro-Probe Design (Single Run)
- Parent checkpoint: `stage_b_llama31_8b_base_v1_i9`
- Dataset: i10 train/val unchanged
- Budget: `0.20` epochs (single bounded probe)
- Eval topology: canonical manifest unchanged
- Decode defaults: unchanged
- Retry policy: none (no hidden retries)
- Rollback unit: discard probe adapter and return to parent checkpoint

## Weighted Exposure Strategy Assessment
### Scientific
Weighted exposure control is justified. It directly addresses legacy ritualized dominance while preserving contrastive stress pressure.

### Operational
Weighted exposure is **not natively supported** in the current trainer implementation (`scripts/train_lora_sft.py` has no weighted sampler hook).

### Practical Consequence
If weighted exposure remains unavailable, the probe signal will likely be confounded by legacy-family dominance. In that case, run readiness should shift to **dataset revision before execution**.

## Telemetry-First Doctrine
Primary telemetry to decide success/failure:
- `read_file` exact-valid emergence (`>0` required)
- anti-scalar delta (scalar/direct substitution vs i9 must decrease)
- paraphrastic + no-anchor exact-valid behavior
- unseen-shell exact-valid behavior
- no-call correctness and wrapper leakage invariants

First-class failure mode:
- **high lexical diversity with low procedural diversity**

This must be treated as false progress even if exact-valid rises.

## Halt and Rollback Conditions
Immediate halt:
- `no_call_correctness < 1.0`
- `wrapper_leakage > 0`
- collapse-watch trigger activation

Rollback/invalid-progress:
- exact-valid gains concentrated in literal shell bucket
- read_file exact-valid remains zero
- scalar/direct substitution rebounds
- unseen-shell exact-valid remains near-zero

## Acceptable Regression Envelope
- no-call correctness: exactly `1.0`
- wrapper leakage: exactly `0.0`
- heldout exact-valid: not worse than i9 by more than `-0.02` absolute
- heldout invalid_json: not worse than i9 by more than `+0.03` absolute
- scalar/direct substitution: must not increase vs i9 baseline

## Explicit Conclusions
1. Weighted exposure is scientifically justified: **Yes**.
2. Weighted exposure is operationally safe today: **Not yet** (no native support path in current trainer).
3. Weighted exposure likely improves procedural diversity: **Yes**, if auditable and deterministic.
4. Safest viable micro-probe: **single 0.20 epoch run from i9 checkpoint, strict telemetry-first gates, no retries**.
5. Best telemetry for generalization vs ritualization:
   - unseen-shell exact-valid
   - read_file exact-valid emergence
   - anti-scalar delta
   - anchor-bucket independence
   - successful procedural diversity ratio
6. Genuine success vs false success:
   - Genuine: read_file foothold + scalar decrease + non-literal transfer + invariants preserved.
   - False: exact-valid up but shell concentration or scalar substitution unchanged/worse.
   - Immediate rollback: any invariant breach or collapse-watch trigger.
7. Recommended next step after this planning pass:
   - **dataset revision or weighting instrumentation before micro-probe execution**.

## Go/No-Go Recommendation
- **Conditional GO** only if weighted exposure is made auditable (or equivalent non-mutating exposure control exists).
- **No-GO** for immediate execution under the current unweighted legacy-dominant exposure mix.
