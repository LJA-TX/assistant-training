# Stage C Legacy Surface Validity Assessment Direct-Answer Substitution Acceptance Assessment

## Determination

Accepted.

The slice establishes the true runtime-behavior composition of the legacy `direct_answer_substitution_count` population and supports a concrete semantic-validity judgment from direct artifacts.

## What Was Established

1. the legacy surface counts `125` rows on the frozen runtime corpus
2. all `125` rows are authoritative missing-evidence rows
3. `116/125` rows are prompt/task echo with transcript contamination
4. `0/125` rows present clean governed direct-answer evidence
5. the surface is materially misaligned with its claimed semantic meaning

## Validation Coverage

1. read-only analyzer added and exercised against the frozen technical-spike run directory
2. synthetic unit test covers:
   - full authoritative missing-evidence overlap
   - mixed contamination categories
   - materially-misaligned classification
3. no runtime behavior changed

## Boundary Confirmation

Confirmed unchanged:

1. scorer behavior
2. evaluator behavior
3. detector behavior
4. threshold behavior
5. migration flags
6. governance doctrine
7. readiness state
8. gate state

## Residual Boundary

This slice explains the semantic meaning and validity of the legacy surface.

It does not:

1. retire the surface
2. modify detector use
3. modify threshold use
4. authorize implementation
5. authorize migration
