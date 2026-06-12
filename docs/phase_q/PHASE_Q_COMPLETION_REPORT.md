# Phase Q Completion Report

## Executive Summary

The first governed Dataset v1.2 run completed end to end. Training finished, the frozen canonical evaluation contract ran, contamination remained zero, and the repository now has a complete execution record.

The result is **Do Not Promote**.

Phase Q recovered a small amount of exact JSON behavior relative to Phase L v1.1, but it did not recover H1/H2-level tool-call capability and it regressed safety on the no-call surfaces.

## Dataset Summary

| Item | Value |
|---|---|
| Dataset | `data/v1_2/` |
| Rows | `2400` total, `2160` train, `240` val |
| Categories | `tool_positive=1548`, `runtime_alignment=360`, `no_call_direct_calibration=240`, `refusal_calibration=180`, `adversarial_no_call_calibration=72` |
| Tool families | `26` represented |
| Train tool-positive density | `0.6449074074074074` |
| Core anchor share | `0.5200258397932817` |
| `rg_search + read_file` share | `0.31330749354005166` |

## Validation Results

- `git diff --check`: PASS
- `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid.run_manifest.json`: PASS

## Contamination Results

Contamination validation remains clean.

- Zero overlap for prompt, target, and case-id checks across heldout validation, tool holdout, no-call, adversarial, and direct-answer splits.
- The training run did not mutate the dataset.
- The canonical eval contract remained frozen.

## Execution Results

| Item | Value |
|---|---|
| Training runtime | `161.7761s` |
| Training loss | `0.7323995166354709` |
| Internal eval loss | `0.43417230248451233` |
| Exact JSON validity | `0.03` |
| Invalid JSON rate | `0.2` |
| Tool-name accuracy | `0.07142857142857142` |
| Argument accuracy | `0.04285714285714286` |
| Wrapper leakage | `0.0` |
| No-call correctness | `0.7666666666666667` |
| Adversarial no-call correctness | `0.3` |

## Readiness Determination

The run completed successfully, but the candidate is **not ready for promotion**.

Reasons:

1. Safety is not preserved.
2. Tool-call capability remains materially below the H1/H2 baselines.
3. The dataset reform did not recover the diversity tail.
4. The frozen Phase L promotion criteria are not met.

## Risks

- Safety regression on the no-call surfaces is the dominant blocker.
- Tool-call capability is still mostly schema-adjacent rather than exact.
- The candidate still does not recover the H1 read-file lift or the H2 broader realization lift.
- Canonical evaluation required an explicit local mirror override for the base model path in this workspace.

## Recommended Next Phase

Return to design-stage investigation rather than authorizing another governed run immediately.

The next phase should focus on the specific failure surface that remains dominant here:

- schema realization is still too weak,
- direct-answer substitution is still too common,
- and safety calibration is no longer intact.
