# Stage B i8 Prompt-Ambiguity Corrective Review

## Scope
Bounded diagnostics/data-hygiene corrective pass for i8 dataset-generation pipeline only.
No training/eval/checkpoint actions executed.

## Pre-Correction Findings (Recon)
Baseline candidate i8 dataset (pre-correction) showed a real ambiguity defect:

- Duplicate prompt groups with identical target payload: `327`
- Duplicate prompt groups with different target payloads: `1`
- Duplicate prompt groups mapped to different tool names: `1`
- Duplicate `(prompt, tool)` groups with materially different argument payloads: `1`

Impact scope:
- Rows in conflicting prompt groups: `55`
- Cross-tool conflict observed explicitly between `read_file` and `rg_search`.

Concrete conflicting prompt family:
- Prompt text: `Read /mnt/services/runtimes/assistant-runtime/server/service.py lines 1-25 and report the first function name. Return strict JSON tool_calls only.`
- Observed tool mapping: both `rg_search` and `read_file`
- Observed arg divergence within `rg_search`: 5 distinct payload variants

## Root Cause Assessment
Primary cause was **source-case reuse + variant expansion inherited from i3 parent data**, not overlap handling and not contamination logic.

- The conflict was already present in i3 (same ambiguity counts), then inherited by i8 generation.
- Anchor injection was not the dominant source; most conflicting rows had existing parse-anchor signal before i8-specific edits.
- Dedupe gap: prior pipeline allowed identical prompt strings to survive while carrying divergent targets/tools/args.

## Corrective Changes Implemented
1. Added hard-block ambiguity audit to diagnostics and builder:
   - reject prompt -> multiple targets
   - reject prompt -> multiple tools
   - reject `(prompt, tool)` -> multiple argument payloads
2. Added explicit artifact:
   - `manifests/reports/stage_b_v1_i8_prompt_ambiguity_audit.json`
3. Added deterministic ambiguity remediation pass (targeted rows only):
   - applied semantic disambiguation clause derived from tool + key args
   - no non-target row mutation allowed
   - fail-fast if non-target mutation would be required
4. Preserved contamination doctrine:
   - heldout/tool_holdout overlap checks unchanged and still blocking

## Post-Correction Results
From `stage_b_v1_i8_prompt_ambiguity_audit.json`:

- `duplicate_prompt_groups_different_target_count = 0`
- `duplicate_prompt_groups_different_tool_count = 0`
- `duplicate_prompt_tool_groups_different_arguments_count = 0`
- hard-block flags all `false`

Remediation stats (from i8 summary):
- conflicting prompt groups corrected: `1`
- rows changed: `55`
- touched by tool: `read_file=12`, `rg_search=43`

## Residual Risks
- High-frequency prompt reuse still exists for some non-conflicting prompts (expected in this lineage).
- Source-case reuse remains high; now surfaced explicitly in ambiguity diagnostics.
- Ongoing risk is local-template concentration, monitored by existing skeleton/style diagnostics.

## Safety Assessment
Current corrected i8 candidate is acceptable for **bounded training review preparation**:
- ambiguity hard blocks clear,
- contamination overlaps remain zero,
- approval gates remain closed.

