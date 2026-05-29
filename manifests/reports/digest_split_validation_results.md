# Digest Split Validation Results

## Validation Scope
- Synthetic fixtures and static artifact inspection only.
- No training, eval execution, or sweep execution.

## Checks
1. Mapping identity stability
- Setup: recomputed digests with identical geometry identity fields and mutated `declared_exposure_units`.
- Result:
  - base mapping digest: `1f35b81bfe3dfae09e675361b193620955d2a2c51e6d720ad3b0b8cea4f13348`
  - mutated-context mapping digest: `1f35b81bfe3dfae09e675361b193620955d2a2c51e6d720ad3b0b8cea4f13348`
  - `PASS` (`geometry_mapping_identity_digest` stable)

2. Detector context fidelity
- Setup: same mutation as above.
- Result:
  - base context-input digest: `04a286d67a82dbd054ebcdc2c5ca485881534a0674a1241abcc64c4421797e9e`
  - mutated-context input digest: `5ea6eb96fd0cffd286c1181a27ed86296bae2cbdc6447dd4838a10b68c958b89`
  - `PASS` (`geometry_context_input_digest` changes with full context)

3. Backward compatibility behavior
- Mapping artifacts:
  - `geometry_context_digest_alias_of=geometry_mapping_identity_digest`
  - `geometry_context_digest == geometry_mapping_identity_digest`
  - `PASS`
- Detector artifacts:
  - `geometry_context_digest_alias_of=geometry_context_input_digest`
  - `geometry_context_digest == geometry_context_input_digest`
  - `PASS`

4. Detector emitter validation
- Executed detector script with synthetic integration-rehearsal fixtures and geometry context input.
- `collapse_watch_interpretation` and `gate_assessment` both emitted:
  - `geometry_mapping_identity_digest`
  - `geometry_context_input_digest`
  - legacy alias fields
- `PASS`

5. Artifact graph correctness
- Updated graph includes typed digests and alias relationships.
- Integrity summary confirms:
  - mapping identity consistency across stacks: `true`
  - context input consistency across stacks: `true`
  - typed divergence expected: `true`
  - semantic misuse detected: `false`
- `PASS`

6. Rehearsal governance semantics
- Updated synthetic validation artifact:
  - `mapping_identity_digest_consistent=true`
  - `context_input_digest_consistent=true`
  - `typed_digest_scope_valid=true`
  - `legacy_alias_behavior_consistent=true`
- No failure on cross-type digest inequality.
- `PASS`

## Overall Validation Outcome
- `PASS`
- Typed digest split behaves as designed, preserves backward compatibility, and resolves prior governance false-failure mode.
