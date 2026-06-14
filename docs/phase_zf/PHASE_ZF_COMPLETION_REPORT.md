# Phase ZF Completion Report

## Executive Summary

Phase ZF constructed a contamination-clean topology-ablation package with four arms:

- compact local control,
- two-cluster treatment,
- four-cluster treatment,
- fully dispersed treatment.

The frozen scaffold is the phase_y control surface, and only patch-local replacement topology varies.

## Dataset Summary

All four arms share the same core counts:

- `2160` train rows
- `240` validation rows
- `1393` tool-positive rows
- `767` safety rows
- `726` anchor rows
- `667` long-tail rows

The fixed patch content is anchor-only and identical across arms:

- `20` `rg_search`
- `20` `read_file`
- `20` `find_files`
- `20` `debug_tools`
- `20` `run_command`

## Validation Results

- `python -m py_compile scripts/build_phase_zf_topology_ablation_datasets.py`: PASS
- `python scripts/build_phase_zf_topology_ablation_datasets.py`: PASS
- `git diff --check`: PASS
- Exact tool cue retained on all tool-positive rows.
- Canonical single-call `tool_calls` envelope retained.
- Frozen non-tool scaffold preserved.
- All 26 tool families represented.

## Contamination Results

All four arms report zero overlap against:

- heldout validation
- tool holdout
- no-call
- adversarial
- direct answer

## Readiness Determination

All four arms are scientifically admissible and ready for governed execution review.

## Risks

- The topology arms differ only in row placement, so any later signal must be attributed carefully to locality rather than content.
- Treatment B and Treatment C are both broad-footprint arms, so any future execution should compare them against Control and Treatment A as a sweep, not as isolated pairwise anecdotes.

## Recommended Next Phase

Proceed to governed execution review for the Control arm first, then continue the low-to-high topology sweep if the execution gate remains open.
