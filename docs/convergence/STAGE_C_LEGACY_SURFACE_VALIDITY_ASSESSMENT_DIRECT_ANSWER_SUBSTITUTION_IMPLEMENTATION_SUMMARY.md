# Stage C Legacy Surface Validity Assessment Direct-Answer Substitution Implementation Summary

## Scope

This slice adds a read-only semantic-validity analyzer for the legacy:

- `direct_answer_substitution_count`

surface.

It does not change runtime behavior.

## Files Added

1. [stage_c_legacy_surface_validity_direct_answer_assessment.py](/opt/ai-stack/assistant-training/scripts/stage_c_legacy_surface_validity_direct_answer_assessment.py:1)
2. [test_stage_c_legacy_surface_validity_direct_answer_assessment.py](/opt/ai-stack/assistant-training/tests/test_stage_c_legacy_surface_validity_direct_answer_assessment.py:1)
3. [stage_c_legacy_surface_validity_direct_answer_assessment.json](/opt/ai-stack/assistant-training/manifests/reports/stage_c_legacy_surface_validity_direct_answer_assessment.json:1)
4. [STAGE_C_LEGACY_SURFACE_VALIDITY_ASSESSMENT_DIRECT_ANSWER_SUBSTITUTION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_LEGACY_SURFACE_VALIDITY_ASSESSMENT_DIRECT_ANSWER_SUBSTITUTION.md:1)
5. [STAGE_C_LEGACY_SURFACE_VALIDITY_ASSESSMENT_DIRECT_ANSWER_SUBSTITUTION_ACCEPTANCE_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_LEGACY_SURFACE_VALIDITY_ASSESSMENT_DIRECT_ANSWER_SUBSTITUTION_ACCEPTANCE_ASSESSMENT.md:1)

## Exact Change

The analyzer:

1. inventories the legacy `direct_answer_substitution` population from `comparison_rows.jsonl`
2. resolves every legacy-counted row to authoritative scorer evidence and row facts
3. classifies the actual emitted runtime outputs into artifact-derived behavior categories
4. measures the population against the live authoritative predicates
5. emits a machine-readable validity assessment

## Why This Change

The prior runtime-forensics slice explained the authoritative missing-evidence population.

This slice answers the complementary question:

1. what the legacy surface itself is actually counting
2. whether that counted population matches the surface's intended semantic meaning
