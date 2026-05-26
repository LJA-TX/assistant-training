# i8 Bounded Implementation Scaffold

- Event: authorized bounded scaffolding for `stage_b_llama31_8b_base_v1_i8` with no dataset/training/eval execution.
- Parent baseline: `stage_b_llama31_8b_base_v1_i3`.
- Objective: test whether parseability can improve without schema-spill regression.

Doctrine notes:
- i4/i5 mechanisms are forbidden because broad/global corrective pressure previously produced overconstraint collapse and semantic flattening.
- Localized intervention is required to isolate movement in `rg_search` and `read_file` while preserving global runtime/eval invariants.
- Diversity preservation is mandatory because hidden local template homogenization can recreate i5-style collapse within targeted families.
- Spill-guard interpretation is co-primary with parseability because i6/i7 showed oscillatory coupling across `payload_not_parsed`, `payload_not_object`, and `missing_tool_calls`.

Boundaries preserved:
- No canonical eval semantic changes.
- No gate/threshold relaxation.
- No dataset generation in this phase.
- No training in this phase.
- Approval gates remain closed.

Implementation-completion additions:
- Builder flow now includes explicit overlap guard, intervention annotation flow, anti-overconstraint scan hooks, and fail-fast pre-generation stop.
- Diagnostics now include style buckets, skeleton concentration, targeted-tool distribution, forbidden-pattern scans, intervention coverage, and prompt-length delta analysis.
- Preflight now validates draft artifacts + doctrine invariants and emits human-review support outputs without opening execution gates.

Ambiguity corrective additions:
- Added hard-block prompt-ambiguity audit for conflicting prompt->target/tool/argument mappings.
- Added explicit artifact output `stage_b_v1_i8_prompt_ambiguity_audit.json`.
- Added bounded remediation pass for targeted-family prompt disambiguation when ambiguity hard-blocks are detected.
