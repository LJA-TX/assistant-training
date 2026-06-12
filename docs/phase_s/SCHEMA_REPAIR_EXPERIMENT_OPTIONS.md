# Schema Repair Experiment Options

## Scope

This phase is documentation only. No dataset construction, training, evaluation reruns, or governance changes are authorized here.

The question is whether exact tool-call envelope realization can be repaired through a small schema-focused patch while preserving the existing Stage B recovery scaffold.

## Evidence Base

The relevant pattern is consistent across the repository:

- H1 and H2 were small patch runs on a frozen 2160-row scaffold, each adding 100 tool-positive rows.
- H1 and H2 reached exact JSON validity of `0.44` and `0.48`, with tool-name accuracy of `0.7143` and `0.7714`, and argument accuracy of `0.6286` and `0.6929`.
- Phase Q on Dataset v1.2 collapsed to exact JSON validity `0.03` while producing `94` near-canonical wrapper or envelope drift failures.
- Of those `94` wrapper-drift failures, `59` landed on the core anchors `rg_search`, `read_file`, `find_files`, `debug_tools`, and `run_command`.
- v1.1 flattened the core-anchor share to `0.1937`.
- v1.2 restored anchor concentration to `0.5212`, but it still failed to recover exact envelope realization.

Sources:

- [Phase R completion report](/opt/ai-stack/assistant-training/docs/phase_r/PHASE_R_COMPLETION_REPORT.md)
- [Schema realization analysis](/opt/ai-stack/assistant-training/docs/phase_r/SCHEMA_REALIZATION_ANALYSIS.md)
- [Phase Q execution review](/opt/ai-stack/assistant-training/docs/phase_q/PHASE_Q_EXECUTION_REVIEW.md)
- [H1 checkpoint report](/opt/ai-stack/assistant-training/docs/phase_ix/H1_EXCEPTION_CHECKPOINT_REPORT.md)
- [H2 checkpoint report](/opt/ai-stack/assistant-training/docs/phase_i/H2_CHECKPOINT_REPORT.md)

## Candidate Options

| Candidate | Row count | Tool concentration | Prompt regime | Schema targets | Expected effects | Primary risks |
|---|---:|---|---|---|---|---|
| Schema-repair micro-patch | 60 tool-positive rows | 12 rows each on `rg_search`, `read_file`, `find_files`, `debug_tools`, `run_command` | Narrow exact-tool / strict-JSON regime only | Canonical `tool_calls` envelope, one call per row, no bare `function` / `type` wrapper | Best chance of improving exact JSON validity and reducing wrapper drift while leaving safety rows untouched | Underpowered if envelope learning needs more exposure; may overfit to five anchors |
| Anchor-only patch | 60 tool-positive rows | Same five anchors, same exposure count | Same semantic prompts, but without extra schema pressure | Tool semantics only; no explicit envelope repair emphasis | Should test whether anchor concentration alone can recover capability | Likely improves tool selection more than envelope realization; weak attribution on schema hypothesis |
| Prompt-regime patch | 60 tool-positive rows | Same five anchors, same exposure count | Broader prompt wording, more instruction variety | Exact envelope target retained, but prompt wording is the variable under test | Tests whether wording and prompt style drive realization more than data shape | Can improve coverage while still diluting exact envelope commitment |
| Full dataset redesign | 2160-row rebuild or larger | Broad tool mix and broad anchor set | Broad prompt regime and broader safety calibration | Multiple objectives at once | May be best for final production readiness | Lowest information value for the schema hypothesis; too many variables move together |

## Interpretation

The minimum intervention that directly tests schema realization is the schema-repair micro-patch.

It changes the smallest number of moving parts while still targeting the observed failure surface:

- exact JSON validity,
- wrapper drift,
- and the `tool_calls` envelope itself.

The other options are useful as ablations, but they are not as direct a test of the Phase R hypothesis.

