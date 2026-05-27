# i10r Micro-Probe Checkpoint Lineage Note

- Generated UTC: 2026-05-27T14:02:12Z
- Run: `stage_b_llama31_8b_base_v1_i10r_microprobe`
- Parent checkpoint: `stage_b_llama31_8b_base_v1_i9`
- Dataset: `dataset_v1_0_stage_b_recovery_i10r_*`
- Canonical eval run: `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_i10r_microprobe_eval_20260527T134117Z`

## Outcome Summary
- Heldout exact-valid improved from i9 (`0.150` -> `0.660`).
- Read-file exact-valid emergence: `19/27` (`0.704`).
- Scalar substitution share delta vs i9: `-0.400`.
- No-call correctness (aggregate expected-no-call): `0.916667`.
- Wrapper leakage: `0.000000`.

## Governance Result
- Hard-stop triggers: `no_call_correctness_lt_1`.
- Progression status: `halt_progression_report_only`.
- Promotion/canonization: not authorized.
