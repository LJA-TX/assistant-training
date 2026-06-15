# D0 Validation Checklist

## Preflight

- [ ] Confirm the package is located under `docs/continuity/` and not under the existing `docs/phase_d/` roadmap family.
- [ ] Confirm the request is still planning-only.
- [ ] Confirm no dataset file, config file, or manifest file has been modified as part of D0 preparation.
- [ ] Confirm no training or reconstruction execution has started.

## Authority And Inventory

- [ ] The authority matrix names a primary source for every reconstruction surface.
- [ ] The authority matrix includes an explicit precedence order for conflicts.
- [ ] Every required source artifact is listed in the implementation plan inventory.
- [ ] Every listed source artifact is present in the repository snapshot.
- [ ] Every listed source artifact has a recorded path and hash or a clear note explaining why it is not needed.

## i3 Control Checks

- [ ] `data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl` hash matches `c19dbab14d930c39b90f85de8f7bf820f1ac37035756a9ca5063f823369e3f9a`.
- [ ] `data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl` hash matches `d1bde5c675e22a88df250ac91e13522bb4d9ff8685d86e3b885f6d8d106d661f`.
- [ ] The `i3` row ledger matches the published summary exactly.
- [ ] The `i3` scaffold is treated as the control comparator for H0.

## H0 Control Checks

- [ ] H0 resolves to the exact `i3` control bytes.
- [ ] H0 config and manifest are compared only against the certified `i3 -> H0` diff paths.
- [ ] H0 does not introduce any dataset mutation.
- [ ] H0 does not change the canonical eval contract or decode defaults.

## H1 Reconstruction Checks

- [ ] H1 train hash matches `fb488f828b9ff42f2c067031ae4e7d65edecd791420c2d6daf79e27422e4e947`.
- [ ] H1 val hash matches the control val hash `d1bde5c675e22a88df250ac91e13522bb4d9ff8685d86e3b885f6d8d106d661f`.
- [ ] H1 patch size is exactly `100`.
- [ ] H1 replacement positions match the published summary exactly.
- [ ] H1 patch-row tool distribution matches the published summary exactly.
- [ ] H1 config and manifest diffs versus H0 are limited to the certified field list.

## H2 Reconstruction Checks

- [ ] H2 train hash matches `41834b7dd1b06bf90bfdb38b77c15f67a3dfdab802d164b0edddfcc686a75fd5`.
- [ ] H2 val hash matches the control val hash `d1bde5c675e22a88df250ac91e13522bb4d9ff8685d86e3b885f6d8d106d661f`.
- [ ] H2 patch size is exactly `100`.
- [ ] H2 replacement positions match the published summary exactly.
- [ ] H2 patch-row tool distribution matches the published summary exactly.
- [ ] H2 config and manifest diffs versus H1 are limited to the certified field list.

## Pairwise Diff Certification

### i3 -> H0

- [ ] The config diff enumerates exactly 9 field-level changes.
- [ ] The manifest diff enumerates exactly 18 field-level changes.
- [ ] No extra config field changes are present.
- [ ] No extra manifest field changes are present.

### H0 -> H1

- [ ] The config diff enumerates exactly 8 field-level changes.
- [ ] The manifest diff enumerates exactly 8 field-level changes.
- [ ] No extra config field changes are present.
- [ ] No extra manifest field changes are present.

### H1 -> H2

- [ ] The config diff enumerates exactly 8 field-level changes.
- [ ] The manifest diff enumerates exactly 8 field-level changes.
- [ ] No extra config field changes are present.
- [ ] No extra manifest field changes are present.

## Distribution And Integrity Checks

- [ ] Row order matches the published ledgers.
- [ ] Row identity checks use the explicit metadata keys for the surface under review, including `source_case_id`, `phase_i_parent_case_id`, `phase_i_variant`, and `phase_i_patch_slot` where present.
- [ ] Row identity checks use message-payload hashes and row order, not prompt inference.
- [ ] Tool-family distributions match the published summaries.
- [ ] Patch accounting matches the published replacement-position lists.
- [ ] `heldout_validation` contamination remains zero for H1 and H2.
- [ ] `tool_holdout` contamination remains zero for H1 and H2.
- [ ] The inherited `no_call` and `adversarial` overlap profile matches the published control profile.

## Eval-Surface Checks

- [ ] The canonical eval manifest is unchanged.
- [ ] Decode defaults match the frozen manifest.
- [ ] Scorer path and metric-spec path match the frozen manifest.
- [ ] The published eval bundles use the same `comparison_rows.jsonl` and `summary.json` surface set expected for the run.
- [ ] The published bundle manifests identify the correct bundle class, role, and artifact list.

## Package Completeness

- [ ] The final D0 package includes the authority matrix.
- [ ] The final D0 package includes the implementation plan.
- [ ] The final D0 package includes this validation checklist.
- [ ] The final D0 package includes the acceptance criteria.
- [ ] The final D0 package includes a missing-artifact assessment.
