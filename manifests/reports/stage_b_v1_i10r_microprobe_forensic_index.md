# Stage B i10r Micro-Probe Forensic Index

## Purpose
Preserve historically significant i10r micro-probe evidence in commit-eligible paths, including previously gitignored raw eval and runtime artifacts.

## Critical Artifact Map

| Artifact | Why it matters | Path | Gitignored at source? | Commit-eligible snapshot? | Role |
|---|---|---|---|---|---|
| Raw canonical eval summary | Canonical split/aggregate metrics and hard-stop context | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_eval_summary_raw.snapshot.json` | Yes (`evals/runs/*`) | Yes | Interpretability + replay |
| Raw comparison rows | Row-level behavioral evidence for substitution, drift, refusal behavior | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_comparison_rows_raw.snapshot.jsonl` | Yes (`evals/runs/*`) | Yes | Interpretability |
| Resolved training config (runtime) | Actual resolved training parameters used at execution | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_resolved_training_config_raw.snapshot.json` | Yes (`artifacts/*`) | Yes | Replay |
| Masking audit (runtime) | Assistant-only masking enforcement evidence | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_masking_audit_raw.snapshot.json` | Yes (`artifacts/*`) | Yes | Replay + governance |
| Training summary | Runtime/training telemetry and resolved artifact pointers | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_training_summary.json` | Source yes (`artifacts/*`) | Yes | Replay |
| Finalized config | Declared bounded-run contract | `/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_i10r_microprobe.config.json` | No | Yes | Replay |
| Run manifest | Run boundary/governance and lineage trace | `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_i10r_microprobe.run_manifest.json` | No | Yes | Replay + governance |
| Canonical eval interpretation summary | i9 vs i10r and gate/halt interpretation | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_canonical_eval_summary.json` | No | Yes | Interpretability |
| Scalar substitution delta | Primary residual-failure trajectory evidence | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_scalar_substitution_delta_analysis.json` | No | Yes | Interpretability |
| read_file emergence analysis | Key scientific win (first foothold) | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_read_file_emergence_analysis.json` | No | Yes | Interpretability |
| Procedural generalization assessment | Anchor dependence and no-anchor evidence | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_procedural_generalization_assessment.json` | No | Yes | Interpretability |
| Collapse-watch interpretation | Explicit hard-stop trigger and halt rationale | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_collapse_watch_interpretation.json` | No | Yes | Governance |
| Forensic integrity snapshot | Hashes/row counts across dataset + raw eval + runtime snapshots | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_reproducibility_snapshot.json` | N/A | Yes | Replay + audit |
| Behavioral evidence hash bundle | Integrity hashes for key behavior artifacts | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_behavioral_evidence_snapshot.json` | N/A | Yes | Audit |
| Runtime binary hash manifest | Verifiable identities for gitignored adapter/checkpoint binaries | `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_runtime_hash_manifest.json` | Source yes (`artifacts/*`) | Yes | Replay + audit |
| i10r checkpoint narrative | Human-readable checkpoint interpretation | `/opt/ai-stack/assistant-training/docs/lineages/i10r_microprobe_checkpoint.md` | No | Yes | Governance + continuity |

## Minimum Viable Replay Set
- Finalized run config and run manifest.
- i10r train/val/summary dataset artifacts.
- Resolved training config snapshot.
- Masking audit snapshot.
- Training summary.
- Raw eval summary snapshot.
- Reproducibility snapshot (hashes/row counts).
- Runtime binary hash manifest.

## Minimum Viable Interpretability Set
- Raw comparison rows snapshot.
- Canonical eval summary (interpreted).
- Scalar substitution delta analysis.
- read_file emergence analysis.
- Procedural generalization assessment.
- Collapse-watch interpretation.
- i10r checkpoint narrative.

## Optional Extended Forensic Set
- i10r family concentration review (json + md).
- i10r dataset diagnostics.
- i10r exposure projection.
- i10r human review package (json + md).
- i10r prompt ambiguity audit and contamination audit.
- Runtime binary hash manifest (if full binary retention is intentionally avoided).

## Reproducibility/Interpretability Notes
- Raw eval and runtime sources remain in gitignored locations (`evals/runs/*`, `artifacts/*`).
- Commit-eligible snapshots in `manifests/reports/` now preserve those sources without altering underlying evidence.
- Snapshot integrity is verifiable via `stage_b_v1_i10r_microprobe_reproducibility_snapshot.json` and `stage_b_v1_i10r_microprobe_behavioral_evidence_snapshot.json`.
