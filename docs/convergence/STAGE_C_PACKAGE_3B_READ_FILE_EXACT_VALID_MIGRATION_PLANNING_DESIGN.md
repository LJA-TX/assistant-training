# Stage C Package 3B Read-File Exact-Valid Migration Planning Design

## Scope

This package defines a planning-only migration blueprint for the focus surface:

- `read_file_exact_valid_rate`

This package does not authorize migration implementation.

It does not modify detector authority, threshold authority, migration flags, or historical metric behavior.

## Planning Boundary

Current required posture remains:

1. `authoritative_detector_output=false`
2. `detector_migration_enabled=false`
3. `threshold_profile_migration_enabled=false`

Planning status inherited from Package 3A:

1. `migration-ready`
2. `gate-open`
3. `planning conditionally authorized`

This package uses that planning authorization to describe a possible future migration path for this one surface only.

## Current And Prospective Target State

### Current Legacy Source

Current live source for `read_file_exact_valid_rate`:

1. artifact: `summary.json`
2. metric path: `failure_profile.read_file_exact_valid.rate`
3. construction site: `scripts/eval_canonical_manifest.py::_build_failure_profile`
4. detector consumer path:
   - `scripts/post_eval_collapse_detector.py::_resolve_metric_from_catalog`
   - `scripts/post_eval_collapse_detector.py::_resolve_required_metrics`
   - `scripts/post_eval_collapse_detector.py::_run_detector`
5. threshold consumer path:
   - `manifests/reports/stage_b_v1_threshold_profile.json`
   - catastrophic rule `read_file_exact_valid_rate_lt_0_40`
   - watch rule `read_file_exact_valid_rate_lt_0_70`

### Prospective Authoritative Source

Prospective authoritative source for this one surface:

1. authoritative input facts:
   - `stage_c_row_fact_metadata_artifact.json`
   - `stage_c_family_a_scorer_evidence_artifact.json`
2. authoritative denominator:
   - rows where `membership_markers.family_b1_read_file_eligible == true`
3. authoritative numerator:
   - the authoritative read-file eligible rows whose joined scorer evidence reports `exact_valid == true`
4. authoritative row-identity requirement:
   - `row_id = "{split_id}:{row_index_1based}"`
   - `split_id`
   - manifest-pinned row-set identity
5. authoritative aggregate shape needed for migration:
   - read-file eligible row count
   - read-file exact-valid count
   - read-file exact-valid rate
   - split or population identity
   - comparability marker
   - computability or noncomputability state

The authoritative source described here is aggregate-only detector input.

It is not detector row scanning.

It is not a replacement metric family expansion.

### Intended End-State Architecture For This Surface

Intended end-state for this one surface only:

1. authoritative Stage C facts remain the ownership source;
2. a detector-consumable aggregate-only surface exposes `read_file_exact_valid_rate` using those facts;
3. the detector consumes that aggregate-only authoritative surface rather than the legacy `failure_profile` path;
4. the threshold profile continues to apply the same metric ID, rule IDs, comparators, and threshold values;
5. historical metric identity for `read_file_exact_valid_rate` remains preserved even if source binding later changes.

## Detector Consumption Model

Future detector consumption for this surface should satisfy the already-settled Stage B contract shape:

1. consume an emitted aggregate, not row-level records;
2. receive:
   - eligible row count
   - exact-valid count
   - exact-valid rate
   - split or row-set identity
   - comparability marker when relevant
   - explicit computability state
3. preserve current detector rule evaluation semantics;
4. preserve noncomputable escalation if authoritative inputs are missing, partial, or unstable.

## Threshold Consumption Model

Future threshold consumption for this surface should remain semantically unchanged:

1. threshold profile continues to govern:
   - catastrophic `read_file_exact_valid_rate_lt_0_40`
   - watch `read_file_exact_valid_rate_lt_0_70`
2. comparator and threshold values remain unchanged;
3. rule precedence remains unchanged;
4. only the source binding for the metric may change in a later authorized migration slice;
5. noncomputable handling must remain conservative if authoritative source requirements are not fully met.

## Migration Phase Model

### Phase 1: Preparation

Purpose:

1. freeze the migration reference set for this surface;
2. assemble all authoritative and legacy preservation artifacts;
3. confirm that the focus surface remains the only in-scope migration target.

Required preconditions:

1. Package 3A planning authorization remains active for this surface;
2. Package 2A full-run evidence remains the reference runtime bundle;
3. Package 2B detector and threshold impact review remains current;
4. Package 2C rollback-review record remains current;
5. current migration-disabled flags remain false.

Required validation and preservation:

1. preserve the frozen manifest identity;
2. preserve the latest full-run legacy outputs;
3. preserve the latest authoritative Stage C artifacts;
4. preserve reconciliation and readiness artifacts;
5. preserve row-identity stability evidence.

### Phase 2: Dual-Surface Validation

Purpose:

1. materialize legacy and authoritative views for the same frozen row set;
2. prove that both surfaces stay aligned before any consumer transition is attempted.

Required preconditions:

1. Phase 1 preservation bundle is complete;
2. authoritative row-identity joins remain stable;
3. guardrail status remains clear;
4. authoritative inputs are complete for the focus surface.

Required validation and preservation:

1. dual-surface comparison record for the same frozen row set;
2. exact reconciliation of:
   - eligible row count
   - exact-valid count
   - exact-valid rate
3. preservation of missing-row and join-failure evidence if any exists;
4. preservation of detector and threshold outputs from the unchanged legacy path.

### Phase 3: Detector-Consumption Transition

Purpose:

1. transition detector consumption for this one metric from the legacy source path to the authoritative aggregate-only surface.

Required preconditions:

1. Phase 2 dual-surface validation remains aligned;
2. authoritative detector-input contract is explicit and preserved;
3. noncomputable behavior for missing authoritative inputs is explicit and testable;
4. rollback trigger conditions and rollback artifacts are prepared before any attempt.

Required validation and preservation:

1. pre-transition detector snapshot on the frozen row set;
2. post-transition detector snapshot on the same frozen row set;
3. rule-trigger equivalence for the focus surface;
4. detector status equivalence for the focus surface;
5. preserved evidence for all computability-state decisions.

### Phase 4: Threshold-Consumption Transition

Purpose:

1. transition threshold dependency for this surface so the thresholded metric resolves from the authoritative detector-consumption source rather than the legacy evaluator path.

Required preconditions:

1. Phase 3 detector transition evidence is complete and stable;
2. threshold path mapping is explicit;
3. legacy and authoritative metric identities remain separable and auditable;
4. rollback artifacts remain ready for the threshold boundary as well as the detector boundary.

Required validation and preservation:

1. preserved pre-transition threshold-evaluation outputs;
2. preserved post-transition threshold-evaluation outputs on the same frozen row set;
3. proof that catastrophic and watch rule behavior is unchanged;
4. proof that noncomputable escalation remains conservative.

### Phase 5: Stabilization

Purpose:

1. confirm that the transitioned surface remains stable across repeated full runs.

Required preconditions:

1. detector and threshold transition evidence is complete;
2. authoritative artifact emission remains stable;
3. row identity remains stable across repeated runs on the same frozen row set.

Required validation and preservation:

1. repeated full-run execution on the frozen manifest;
2. repeated reconciliation of legacy-preserved versus authoritative-consumed focus-surface outputs;
3. repeated readiness and guardrail checks;
4. preserved run hashes and semantic digests;
5. preserved rollback readiness record.

### Phase 6: Rollback

Purpose:

1. restore legacy-only detector and threshold consumption immediately if migration conditions fail.

Required preconditions:

1. rollback triggers are explicit before any migration attempt begins;
2. pre-migration snapshots are preserved;
3. post-migration snapshots are preserved;
4. noncomputable failure handling is explicit;
5. failed-attempt preservation artifacts are prepared.

Required validation and preservation:

1. rollback invocation reason record;
2. preserved pre-rollback and post-rollback detector outputs;
3. preserved threshold outputs;
4. preserved noncomputable evidence when rollback was triggered by missing or unstable authoritative inputs;
5. reviewer decision record confirming legacy recoverability.

## Preconditions Inventory

| Phase | Preconditions |
|---|---|
| Preparation | planning conditionally authorized; gate-open; Package 2A evidence current; Package 2B impact review current; Package 2C rollback record current; migration-disabled flags unchanged |
| Dual-surface validation | preparation bundle complete; authoritative artifacts complete; row identity stable; guardrails clear; reconciliation path reproducible |
| Detector-consumption transition | dual-surface alignment proven; authoritative detector-input contract explicit; computability rules explicit; rollback artifacts prepared |
| Threshold-consumption transition | detector transition evidence complete; threshold mapping explicit; metric identity continuity preserved; rollback boundary extended to threshold consumer |
| Stabilization | transitioned surface active for the focus metric only; repeated full-run execution possible; row identity and authoritative artifacts stable |
| Rollback | rollback triggers explicit; pre/post snapshots preserved; failed-attempt preservation set prepared |

## Phase Validation Requirements

| Phase | Required Evidence | Required Artifact Preservation | Required Comparability Checks | Required Rollback Checks |
|---|---|---|---|---|
| Preparation | manifest identity, current Package 2A bundle, current Package 2B review, current Package 2C review | legacy outputs, Stage C artifacts, reconciliation outputs, readiness outputs | confirm focus surface still aligns on frozen manifest | confirm rollback artifact inventory is complete |
| Dual-surface validation | same-run legacy and authoritative surface comparison | dual-surface comparison record, join evidence, detector and threshold outputs | eligible count, exact-valid count, and rate all align | confirm rollback remains possible before any consumer switch |
| Detector-consumption transition | pre/post detector snapshots on same frozen row set | detector outputs, source-binding evidence, computability evidence | rule triggers and detector status unchanged | verify rollback invocation can restore legacy detector behavior |
| Threshold-consumption transition | pre/post threshold-evaluation snapshots on same frozen row set | threshold outputs, rule-trigger evidence, source-binding evidence | catastrophic and watch results unchanged | verify rollback invocation can restore legacy threshold behavior |
| Stabilization | repeated full-run evidence after transition | run hashes, semantic digests, guardrail outputs, readiness outputs | repeated focus-surface agreement and status stability | verify rollback remains viable after stabilization checks |
| Rollback | rollback invocation record and restored outputs | pre/post rollback artifacts, failed-attempt preservation record | confirm restored legacy outputs match pre-migration baseline for the same row set | confirm rollback path preserved noncomputable evidence and audit trail |

## Abort Conditions

The following conditions must halt any future migration attempt immediately:

1. reconciliation failure for eligible row count, exact-valid count, or exact-valid rate;
2. row-identity instability for the same frozen row set;
3. unresolved or unstable `row_id` joins between row facts and scorer evidence;
4. guardrail regression in authoritative artifact emission;
5. missing authoritative row-fact artifact;
6. missing authoritative scorer-evidence artifact;
7. inability to form the authoritative read-file denominator;
8. detector divergence on triggered rules, status, progression, or halt outcome;
9. threshold divergence on catastrophic or watch behavior;
10. unexpected noncomputable escalation or silent computability substitution;
11. mutation of legacy-preservation artifacts during the migration attempt;
12. incomplete rollback artifact set before any consumer transition.

## Rollback Path

### Rollback Trigger Points

Rollback trigger points for this surface:

1. after dual-surface validation if alignment cannot be reproduced;
2. during detector-consumption transition if detector outputs diverge;
3. during threshold-consumption transition if threshold rule behavior diverges;
4. during stabilization if repeated runs show row-identity drift, reconciliation drift, or guardrail regression;
5. immediately on any missing authoritative input or unresolved computability state.

### Rollback Artifact Requirements

Rollback for this surface requires the Package 2C inventory at attempt time:

1. dual-surface comparison record;
2. pre-migration detector snapshot;
3. post-migration detector snapshot;
4. rollback trigger conditions record;
5. noncomputable fallback record;
6. audit preservation manifest;
7. failed-attempt preservation record when rollback is invoked.

### Rollback Verification Requirements

Rollback verification must prove:

1. the legacy detector source path is restored;
2. the threshold profile again resolves the focus surface from the legacy source;
3. detector outputs on the same frozen row set match the preserved pre-migration baseline;
4. threshold-trigger behavior on the same frozen row set matches the preserved pre-migration baseline;
5. noncomputable evidence from the failed attempt remains preserved rather than discarded.

## Migration Hazard Mapping

| Hazard | Mitigation Strategy | Validation Requirement | Rollback Requirement |
|---|---|---|---|
| Detector path coupling to `failure_profile.read_file_exact_valid.rate` | isolate migration to one aggregate-only detector input for one metric | pre/post detector snapshots on the same frozen row set | preserve legacy detector snapshot and restore on divergence |
| Threshold-profile path coupling | preserve rule IDs, comparators, and thresholds while changing only metric source binding in a later authorized slice | pre/post threshold rule-equivalence evidence | preserve legacy threshold outputs and restore on divergence |
| Structural mismatch between flat legacy summary and Stage C fact graph | keep authoritative source aggregate-only and preserve row-identity joins as explicit evidence | dual-surface comparison with join integrity evidence | rollback immediately on join instability or denominator failure |
| Missing or partial authoritative inputs | require explicit computability checks before detector or threshold consumption | missing-artifact and denominator-formation checks | escalate to rollback with preserved noncomputable record |
| Row-identity instability | keep manifest-pinned row set and repeated row-identity digest checks | repeated full-run row-identity stability evidence | rollback on any row-identity drift |
| Guardrail regression | require guardrail-clear status before and during migration attempt | preserved guardrail artifacts for each run | rollback on any guardrail violation |
| Legacy-surface mutation during attempt | preserve old and new outputs as separate artifact classes | pre/post raw hash and semantic digest preservation | rollback and retain both output sets plus decision record |
| Failed-attempt evidence loss | define required audit preservation manifest before transition | verify artifact inventory completeness before phase advance | preserve failed-attempt record and noncomputable evidence |

## Planning Determination

For `read_file_exact_valid_rate`, the repository now has a complete planning blueprint for a future migration attempt that:

1. remains surface-scoped;
2. preserves the active migration-disabled posture;
3. requires aggregate-only authoritative detector consumption;
4. makes dual-surface validation, abort conditions, and rollback evidence explicit before any later implementation request.

This package does not authorize phase entry.

It documents what phase entry would require if a later migration implementation package were separately authorized.

## Boundary Confirmation

This planning design does not:

1. modify detector code;
2. modify threshold profiles;
3. create replacement metrics;
4. alter migration flags;
5. perform migration implementation;
6. perform detector cutover;
7. perform threshold cutover;
8. alter comparability policy.
