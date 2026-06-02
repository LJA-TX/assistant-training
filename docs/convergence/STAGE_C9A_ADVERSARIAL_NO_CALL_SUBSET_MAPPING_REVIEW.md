# Stage C9-A Adversarial No-Call Subset Mapping Review

## Scope

This review addresses the Stage C9-A adversarial no-call subset mapping blocker at the contract-definition and evidence-mapping level only.

Route selected from `AGENTS.md`: `migration_gate`.

This review does not implement evaluator behavior, modify detector behavior, modify threshold profiles, authorize detector migration, or authorize threshold-profile migration.

## Authoritative Inputs Reviewed

1. `AGENTS.md`
2. `docs/convergence/STAGE_C9_BLOCKER_CLOSURE_PLANNING_ASSESSMENT.md`
3. `docs/convergence/STAGE_C9_BLOCKER_CLOSURE_READINESS_DETERMINATION.md`
4. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_IMPLEMENTATION_GATE.md`
5. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_GATE_DETERMINATION.md`
6. `docs/convergence/STAGE_C8_NON_AUTHORITATIVE_DETECTOR_PROJECTION_ADAPTER.md`
7. `docs/convergence/STAGE_C8_DETECTOR_PROJECTION_ADAPTER_CONFORMANCE_REPORT.md`
8. `docs/convergence/STAGE_C0_C8_IMPLEMENTATION_REVIEW.md`
9. `manifests/reports/stage_b_v1_threshold_profile.json`
10. `manifests/reports/stage_b_first_probe_design.md`
11. `evals/data/canonical_v1/adversarial.jsonl`
12. `evals/data/canonical_v1/no_call.jsonl`
13. Stage C4/C5/C6 emitted contract and reporting artifacts
14. Stage B WP8 scenario catalog and fixture corpus

## Existence Finding

An adversarial no-call source subset exists in the legacy Stage B canonical evaluation/probe topology.

Evidence:

1. `evals/data/canonical_v1/adversarial.jsonl` contains 20 rows.
2. All 20 rows carry metadata category `adversarial_malformed`.
3. All 20 rows carry metadata source `synthetic_adversarial_malformed`.
4. Source case IDs run from `adv_91001` through `adv_91020`.
5. The Stage B threshold profile defines legacy metric `no_call_correctness_adversarial` with candidate paths `metrics.probes.no_call_adversarial.no_call_correctness` and `metrics.stage_b_i10r_nocall_probe.no_call_correctness`.
6. The Stage B first probe design identifies no-call adversarial family exposure and lists no-call adversarial correctness as a required probe slice.

A Stage C detector-projection mapping for that subset did not already exist before this review.

Evidence:

1. Stage C4 model-output records preserve fixture/source references, model identity, raw output, parse status, tool-call status, no-call status, and provenance, but do not define an adversarial subset marker.
2. Stage C5 scoring records preserve no-call scoring evidence, but do not define an adversarial subset partition.
3. Stage C6 reporting artifacts preserve parse/tool/no-call summaries and detector-projection preparation surfaces, but do not define an adversarial no-call subset metric source.
4. Stage C7 explicitly classified `no_call_correctness_adversarial` as blocked because no authoritative Stage C adversarial subset projection was emitted.
5. Stage C8 preserved that blocker as `projection_status=noncomputable_blocked` with reason code `blocked_adversarial_subset_mapping_unavailable`.

Determination: the legacy source subset exists, but it was not already usable as a Stage C detector-projection metric without an explicit non-inferential mapping contract.

## Missing Stage C Authority Before C9-A

Before this review, the exact missing authority was:

1. no accepted Stage C contract defining adversarial no-call subset ownership, inclusion criteria, exclusion criteria, provenance requirements, computability requirements, and noncomputable conditions;
2. no emitted Stage C model-output, scoring, or reporting field that explicitly marked adversarial no-call subset membership;
3. no non-authoritative adapter validation proving `no_call_correctness_adversarial` can be computed from explicit subset evidence while remaining noncomputable when that evidence is absent.

This review addresses item 1 only.

Items 2 and 3 remain implementation or validation work for a later controlled slice.

## Smallest Safe Blocker-Closure Path

The smallest safe blocker-closure path is:

1. define the mapping contract and evidence requirements without changing runtime behavior;
2. in a later controlled implementation slice, emit or preserve an explicit adversarial no-call subset marker where source authority exists;
3. update the non-authoritative detector projection adapter to consume only that explicit marker;
4. keep unresolved or missing subset evidence noncomputable;
5. validate that migration flags remain disabled;
6. rerun the migration gate after remaining C9 blockers are also addressed.

This path preserves the current non-authoritative and migration-disabled posture.

## Ownership Contract

### Source Subset Ownership

The adversarial no-call source subset is owned by the legacy Stage B canonical evaluation/probe topology.

Authoritative source surfaces:

1. `evals/data/canonical_v1/adversarial.jsonl`
2. `evals/canonical_eval_manifest_v1.json`, when it references the canonical adversarial split
3. Stage B probe planning artifacts that identify no-call adversarial exposure

### Legacy Metric Ownership

The legacy detector-facing metric identity is owned by the Stage B threshold profile and detector inventory surfaces.

Authoritative source surfaces:

1. `manifests/reports/stage_b_v1_threshold_profile.json`
2. Existing detector metric inventory and gate outputs that consume `no_call_correctness_adversarial`

The threshold profile owns the metric identifier and threshold rule. It does not, by itself, authorize Stage C derivation by inference from aggregate no-call data, prompt text, report names, or path conventions.

### Stage C Projection Ownership

Stage C projection ownership belongs to the evaluator reporting/projection path, but only for explicitly emitted evidence.

Allowed projection ownership responsibilities:

1. consume explicit Stage C row-level or summary-level subset evidence;
2. preserve raw output, scoring evidence, provenance, and denominator evidence;
3. emit noncomputable status when required subset evidence is absent;
4. keep detector-projection outputs non-authoritative unless a later migration gate authorizes migration.

### Governance Ownership

Governance ownership remains with the Stage C0 contract lock and Stage B non-inference doctrine.

Governance responsibilities:

1. prohibit subset inference from prompt text;
2. prohibit subset inference from historical report names;
3. prohibit subset inference from path conventions alone;
4. prohibit denominator substitution from aggregate no-call metrics;
5. prohibit state-axis collapse.

## Inclusion Criteria

A Stage C output or scored record may be included in the adversarial no-call subset only when all required evidence is explicit.

Required inclusion criteria:

1. The record has explicit source-subset evidence identifying the Stage B canonical adversarial split or an accepted successor subset.
2. The source-subset evidence is emitted as data, not inferred from prompt wording, source-case naming patterns, file paths, report names, or absence of other markers.
3. The record has explicit no-call expectation evidence, such as `no_call_expected=true` in Stage C output records or `expected_no_call=true` in legacy row evidence.
4. The record has no-call scoring evidence sufficient to classify no-call correctness without reconstructing missing outputs or tool calls.
5. The record preserves fixture/source identity, model identity, raw output evidence, and provenance needed to audit denominator membership.

Examples of acceptable source-subset evidence:

1. an emitted `source_split` or equivalent field with value `adversarial` from the canonical eval manifest;
2. an emitted `subset_id` or equivalent field with value `adversarial_no_call` from an accepted Stage C mapping contract;
3. row-level provenance that explicitly links to `evals/data/canonical_v1/adversarial.jsonl` and carries the row's recorded metadata category, source, and source case ID.

## Exclusion Criteria

A record must be excluded from the adversarial no-call subset when any of the following applies:

1. The record belongs only to aggregate no-call evaluation without explicit adversarial subset evidence.
2. The record belongs to `evals/data/canonical_v1/no_call.jsonl` or any direct no-call split without explicit adversarial subset evidence.
3. The record has no-call expectation evidence but no adversarial subset evidence.
4. The record has adversarial source evidence but no explicit no-call expectation evidence.
5. The record is identified as adversarial only by prompt content, row naming convention, source-case ID pattern, report path, or artifact filename.
6. The record is a Stage B WP8 no-call proxy or detector non-inference fixture without explicit adversarial subset membership.
7. The record requires reconstruction, substitution, or inference to determine source subset, no-call expectation, or scoring outcome.

## Provenance Requirements

Any future Stage C artifact that computes or contributes to `no_call_correctness_adversarial` must preserve the following evidence:

1. `record_id`
2. `fixture_id`, when applicable
3. `source_definition_id`, when applicable
4. `model_identifier`
5. `prompt_reference` or equivalent input reference
6. preserved `raw_model_response` or raw-output digest with retained source artifact reference
7. source artifact path or manifest reference
8. source split or subset marker
9. source row identifier or line number when available
10. no-call expectation evidence
11. no-call emitted/status evidence
12. no-call scoring dimension result and reason
13. denominator inclusion evidence
14. noncomputable reason code when inclusion cannot be established
15. independent completeness, current-run computability, and comparability states when state-axis data is emitted

## Computability Requirements

`no_call_correctness_adversarial` is current-run computable only when the current run contains an explicit adversarial no-call denominator and scored no-call outcomes for that denominator.

Required arithmetic:

1. Denominator: count of current-run records satisfying all inclusion criteria.
2. Numerator: count of included denominator records whose no-call correctness scoring dimension passes.
3. Rate: numerator divided by denominator.

Required constraints:

1. Denominator membership must be explicit and auditable.
2. Numerator membership must be derived from scored no-call correctness evidence, not from generated text shape.
3. A zero denominator is noncomputable, not a valid zero score.
4. Aggregate no-call correctness cannot substitute for adversarial no-call correctness.
5. Historical no-call adversarial reports cannot substitute for current-run denominator evidence.
6. Comparability state remains independent from current-run computability.
7. Computing the current-run metric does not authorize baseline comparison unless a separate comparability gate allows it.

## Noncomputable Conditions

The metric must be emitted as noncomputable when any of the following conditions applies:

1. adversarial subset marker or explicit row-level adversarial provenance is missing;
2. no-call expectation evidence is missing;
3. no-call scoring evidence is missing;
4. the denominator is zero;
5. only aggregate no-call correctness is available;
6. only legacy report-layer metric values are available;
7. source split membership would require inference from prompt text, naming conventions, path conventions, or absence of markers;
8. row-level provenance conflicts with emitted subset membership;
9. the output would require repair, reconstruction, or substitution before scoring;
10. state-axis collapse would be required to produce the value.

Recommended reason codes for later non-authoritative adapter implementation:

1. `blocked_adversarial_subset_mapping_unavailable`
2. `source_adversarial_subset_marker_missing`
3. `source_no_call_expectation_missing`
4. `source_no_call_scoring_missing`
5. `source_adversarial_subset_denominator_zero`
6. `source_adversarial_subset_provenance_conflict`
7. `source_adversarial_subset_inference_prohibited`

## Mapping Contract

The legacy detector metric ID remains:

- `no_call_correctness_adversarial`

The only permitted Stage C mapping is:

- explicit adversarial no-call subset denominator plus explicit no-call correctness scoring results.

Allowed future Stage C sources:

1. a per-output scoring artifact containing explicit adversarial subset evidence and no-call correctness scoring evidence;
2. a parse/tool/no-call scoring summary partitioned by explicit adversarial subset evidence;
3. a projection-preparation artifact that carries the row-level evidence required by this review.

Disallowed sources:

1. aggregate no-call correctness;
2. prompt text patterns;
3. source-case ID prefixes by themselves;
4. artifact filenames or report paths by themselves;
5. historical metric values without current-run denominator evidence;
6. no-call proxy fixture behavior intended for a different doctrine boundary.

## Findings

| Target | Status | Evidence |
|---|---|---|
| Legacy adversarial no-call source subset exists | pass | Canonical adversarial split contains 20 rows with explicit adversarial metadata. |
| Stage C emitted subset mapping already existed | fail | C7/C8 classified the metric as blocked; C4/C5/C6 do not emit the required subset marker. |
| Explicit ownership can be defined without doctrine redesign | pass | Ownership separates source subset, legacy metric identity, Stage C projection, and governance guardrails. |
| Inclusion/exclusion criteria can be defined without inference | pass | Criteria require explicit subset, no-call expectation, scoring, and provenance evidence. |
| Computability can be defined without denominator substitution | pass | Denominator and numerator are current-run, explicit, and auditable. |
| Detector migration can be authorized by this slice | fail | This slice is contract-definition only and preserves migration-disabled posture. |

## Validation Results

Validation evidence captured for this review:

1. `rg` search across `docs`, `manifests`, `scripts`, `tests`, `reports`, and `evals` for adversarial no-call and metric references: pass.
2. JSONL inspection of `evals/data/canonical_v1/adversarial.jsonl`: pass, 20 rows, category `adversarial_malformed`, source `synthetic_adversarial_malformed`, source case IDs `adv_91001` through `adv_91020`.
3. JSONL inspection of `evals/data/canonical_v1/no_call.jsonl`: pass, 20 rows, category `no_call_direct`, source `synthetic_no_call_direct`, source case IDs `nc_90001` through `nc_90020`.
4. Review of `manifests/reports/stage_b_v1_threshold_profile.json`: pass, legacy metric candidate paths and hard-invariant rule found.
5. Review of C4/C5/C6 documentation and C8 adapter code: pass, current emitted Stage C surfaces lack adversarial subset evidence and C8 still emits `no_call_correctness_adversarial` as noncomputable blocked.
6. Search for Stage C adversarial subset fields in C4/C5/C6 scripts and reports: pass, no `adversarial_no_call`, `source_split`, or `subset_id` marker found.
7. Search for migration-enabled flags in C9-A artifacts: pass, no enabled detector or threshold migration flag found.

## Governance Concerns

No new governance doctrine is introduced.

Active governance concerns retained:

1. Detector migration remains unauthorized.
2. Threshold-profile migration remains unauthorized.
3. Aggregate no-call correctness must not substitute for adversarial no-call correctness.
4. Legacy adversarial split existence must not be converted into Stage C current-run membership without explicit emitted evidence.
5. Comparability remains independent from current-run computability.

## Residual Ambiguities

Residual ambiguity after this review is implementation-facing, not contract-facing:

1. Stage C output/scoring artifacts do not yet emit an explicit adversarial subset marker.
2. The C8 non-authoritative adapter has not been updated to consume this contract.
3. Full migration remains blocked by the no-anchor semantic-equivalence bridge and baseline-delta comparability gate.

## Determination

Stage C9-A resolves the adversarial no-call subset blocker at the contract-definition and evidence-mapping level.

End-to-end detector migration remains blocked because this review does not implement the mapping, does not update the non-authoritative adapter, does not authorize threshold migration, and does not close the remaining C9 blockers.

Blocker status for authoritative detector migration: partially resolved.

## Boundary Confirmation

This review did not modify evaluator runtime code, detector code, threshold profiles, fixture catalogs, fixture definitions, governance doctrine, or repository process infrastructure.

This review does not authorize detector migration, threshold-profile migration, live inference, or replacement of existing detector outputs.
