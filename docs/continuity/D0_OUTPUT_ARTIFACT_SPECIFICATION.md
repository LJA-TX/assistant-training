# D0 Output Artifact Specification

## Canonical Output Root

All future D0 certification outputs must be written beneath:

`/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/`

Each run must use a dedicated run directory:

`/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/`

Recommended run-id format:

`d0_YYYYMMDDThhmmssZ`

The run directory is the only location authorized for generated D0 evidence.

## Directory Layout

```text
/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/
  runs/
    <run_id>/
      inventory/
        source_artifact_inventory.json
      ledgers/
        hash_ledger.json
        row_ledger.jsonl
      reports/
        dataset_integrity_report.json
        patch_accounting_report.json
        tool_family_distribution_report.json
        eval_surface_fidelity_report.json
        missing_artifact_report.json
        acceptance_summary.json
      diffs/
        config_diff_certification.json
        manifest_diff_certification.json
```

Optional human-readable mirrors may be added next to the JSON artifacts, but they are never authoritative.

## Serialization Rules

- JSON files must be UTF-8 encoded.
- JSON files must use LF line endings.
- JSONL files must contain exactly one object per line.
- Output generation must be deterministic.
- Key order must be stable within each emitted JSON object.
- Relative references in the package must resolve from the run directory.

## Common Envelope

All JSON artifacts should include the same top-level envelope fields where applicable:

```json
{
  "schema_version": "1.0",
  "run_id": "d0_YYYYMMDDThhmmssZ",
  "generated_utc": "2026-06-15T00:00:00Z",
  "authority_matrix_path": "/opt/ai-stack/assistant-training/docs/continuity/D0_RECONSTRUCTION_AUTHORITY_MATRIX.md",
  "status": "pass",
  "notes": []
}
```

The exact `generated_utc` value is runtime-dependent. `status` must be one of `pass`, `warn`, `fail`, or `blocked`.

## Required Artifacts

| Relative path | Type | Purpose |
|---|---|---|
| `inventory/source_artifact_inventory.json` | JSON | Inventory of every source artifact used or checked by D0. |
| `ledgers/hash_ledger.json` | JSON | Raw-byte hash ledger for source and authoritative reference artifacts. |
| `ledgers/row_ledger.jsonl` | JSONL | One line per row across the certified row surfaces. |
| `reports/dataset_integrity_report.json` | JSON | Dataset hash, count, order, and contamination certification. |
| `reports/patch_accounting_report.json` | JSON | Patch-size and replacement-position certification. |
| `reports/tool_family_distribution_report.json` | JSON | Tool-family count certification. |
| `diffs/config_diff_certification.json` | JSON | Field-level config diff certification for `i3 -> H0`, `H0 -> H1`, and `H1 -> H2`. |
| `diffs/manifest_diff_certification.json` | JSON | Field-level manifest diff certification for `i3 -> H0`, `H0 -> H1`, and `H1 -> H2`. |
| `reports/eval_surface_fidelity_report.json` | JSON | Eval-manifest, scorer, metric, and bundle fidelity certification. |
| `reports/missing_artifact_report.json` | JSON | Explicit list of missing required or corroborating artifacts. |
| `reports/acceptance_summary.json` | JSON | Final run-level acceptance or rejection decision. |

## `source_artifact_inventory.json`

Purpose: identify every artifact that participates in D0 certification and record the evidence needed to classify it.

```json
{
  "schema_version": "1.0",
  "run_id": "d0_YYYYMMDDThhmmssZ",
  "generated_utc": "2026-06-15T00:00:00Z",
  "authority_matrix_path": "/opt/ai-stack/assistant-training/docs/continuity/D0_RECONSTRUCTION_AUTHORITY_MATRIX.md",
  "artifacts": [
    {
      "artifact_id": "i3_train",
      "surface_id": "i3",
      "role": "primary",
      "path": "/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl",
      "required": true,
      "present": true,
      "size_bytes": 0,
      "sha256": "c19dbab14d930c39b90f85de8f7bf820f1ac37035756a9ca5063f823369e3f9a",
      "claim_source": "docs/continuity/D0_RECONSTRUCTION_AUTHORITY_MATRIX.md",
      "corroborators": [],
      "authority_tier": 3,
      "status": "present",
      "notes": []
    }
  ]
}
```

Required inventory fields:

- `artifact_id`
- `surface_id`
- `role`
- `path`
- `required`
- `present`
- `size_bytes`
- `sha256`
- `claim_source`
- `corroborators`
- `authority_tier`
- `status`

## `hash_ledger.json`

Purpose: record the published hash claim and the computed raw-byte hash for each authoritative source artifact.

```json
{
  "schema_version": "1.0",
  "run_id": "d0_YYYYMMDDThhmmssZ",
  "entries": [
    {
      "hash_id": "i3_train_sha256",
      "artifact_path": "/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl",
      "algorithm": "sha256",
      "published_value": "c19dbab14d930c39b90f85de8f7bf820f1ac37035756a9ca5063f823369e3f9a",
      "computed_value": "c19dbab14d930c39b90f85de8f7bf820f1ac37035756a9ca5063f823369e3f9a",
      "authoritative_source": "data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl",
      "corroborators": [
        "docs/continuity/D0_RECONSTRUCTION_AUTHORITY_MATRIX.md",
        "docs/continuity/D0_RECONSTRUCTION_IMPLEMENTATION_PLAN.md"
      ],
      "match_status": "match",
      "conflict_status": "none",
      "notes": []
    }
  ]
}
```

Required hash-ledger fields:

- `hash_id`
- `artifact_path`
- `algorithm`
- `published_value`
- `computed_value`
- `authoritative_source`
- `corroborators`
- `match_status`
- `conflict_status`

## `row_ledger.jsonl`

Purpose: preserve a row-by-row reconstruction trace that can be recomputed from raw JSONL input.

Each line must follow this schema:

```json
{
  "schema_version": "1.0",
  "run_id": "d0_YYYYMMDDThhmmssZ",
  "surface_id": "H1_train",
  "split": "train",
  "row_index_0based": 0,
  "row_index_1based": 1,
  "source_case_id": "case-000123",
  "phase_i_parent_case_id": "case-000007",
  "phase_i_variant": "H1",
  "phase_i_patch_slot": 42,
  "category": "replacement",
  "tool_name": "search",
  "row_json_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
  "messages_sha256": "1111111111111111111111111111111111111111111111111111111111111111",
  "metadata_sha256": "2222222222222222222222222222222222222222222222222222222222222222",
  "identity_keys": {
    "source_case_id": "case-000123",
    "phase_i_parent_case_id": "case-000007",
    "phase_i_variant": "H1",
    "phase_i_patch_slot": 42
  },
  "status": "ok",
  "notes": []
}
```

Required row-ledger fields:

- `surface_id`
- `split`
- `row_index_0based`
- `row_index_1based`
- `source_case_id`
- `phase_i_parent_case_id`
- `phase_i_variant`
- `phase_i_patch_slot`
- `category`
- `tool_name`
- `row_json_sha256`
- `messages_sha256`
- `metadata_sha256`
- `identity_keys`
- `status`

## `dataset_integrity_report.json`

Purpose: certify that the raw dataset bytes, row count, row order, and contamination profile match the published evidence.

```json
{
  "schema_version": "1.0",
  "run_id": "d0_YYYYMMDDThhmmssZ",
  "surfaces": {
    "i3_train": {
      "artifact_path": "/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl",
      "expected_sha256": "c19dbab14d930c39b90f85de8f7bf820f1ac37035756a9ca5063f823369e3f9a",
      "observed_sha256": "c19dbab14d930c39b90f85de8f7bf820f1ac37035756a9ca5063f823369e3f9a",
      "expected_row_count": 0,
      "observed_row_count": 0,
      "row_order_status": "match",
      "identity_status": "match",
      "contamination": {
        "heldout_validation": 0,
        "tool_holdout": 0,
        "no_call": 0,
        "adversarial": 0
      },
      "status": "pass",
      "notes": []
    }
  }
}
```

Required integrity fields:

- `artifact_path`
- `expected_sha256`
- `observed_sha256`
- `expected_row_count`
- `observed_row_count`
- `row_order_status`
- `identity_status`
- `contamination`
- `status`

The `surfaces` object must include every in-scope train/val surface:

- `i3_train`
- `i3_val`
- `H0_train`
- `H0_val`
- `H1_train`
- `H1_val`
- `H2_train`
- `H2_val`

## `patch_accounting_report.json`

Purpose: certify that patch rows are fully and exactly accounted for.

```json
{
  "schema_version": "1.0",
  "run_id": "d0_YYYYMMDDThhmmssZ",
  "surfaces": {
    "H1": {
      "parent_surface_id": "H0",
      "patch_size_expected": 100,
      "patch_size_observed": 100,
      "replacement_positions_expected": [],
      "replacement_positions_observed": [],
      "replacement_position_status": "match",
      "patch_slot_coverage_status": "match",
      "status": "pass",
      "notes": []
    }
  }
}
```

Required patch-accounting fields:

- `parent_surface_id`
- `patch_size_expected`
- `patch_size_observed`
- `replacement_positions_expected`
- `replacement_positions_observed`
- `replacement_position_status`
- `patch_slot_coverage_status`
- `status`

The `surfaces` object must include at least `H1` and `H2`.

## `tool_family_distribution_report.json`

Purpose: certify the tool-family counts derived from patch rows and control rows.

```json
{
  "schema_version": "1.0",
  "run_id": "d0_YYYYMMDDThhmmssZ",
  "surfaces": {
    "H2": {
      "tool_family_expected": {
        "search": 0,
        "browse": 0
      },
      "tool_family_observed": {
        "search": 0,
        "browse": 0
      },
      "tool_family_status": "match",
      "status": "pass",
      "notes": []
    }
  }
}
```

Required tool-family fields:

- `tool_family_expected`
- `tool_family_observed`
- `tool_family_status`
- `status`

The `surfaces` object must include at least `H1` and `H2`.

## `config_diff_certification.json`

Purpose: enumerate the exact field-level config differences for:

- `i3 -> H0`
- `H0 -> H1`
- `H1 -> H2`

```json
{
  "schema_version": "1.0",
  "run_id": "d0_YYYYMMDDThhmmssZ",
  "pairs": [
    {
      "pair_id": "i3__H0",
      "left_surface_id": "i3",
      "right_surface_id": "H0",
      "left_path": "/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_i3.config.json",
      "right_path": "/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.json",
      "expected_delta_count": 9,
      "observed_delta_count": 9,
      "field_deltas": [
        {
          "field_path": "name",
          "change_type": "changed",
          "left_value": "i3",
          "right_value": "H0",
          "status": "certified"
        }
      ],
      "unexpected_deltas": [],
      "status": "certified",
      "notes": []
    }
  ]
}
```

Required config-diff fields:

- `pair_id`
- `left_surface_id`
- `right_surface_id`
- `left_path`
- `right_path`
- `expected_delta_count`
- `observed_delta_count`
- `field_deltas`
- `unexpected_deltas`
- `status`

Each `field_deltas` entry must include:

- `field_path`
- `change_type`
- `left_value`
- `right_value`
- `status`

The `pairs` array must include exactly:

- `i3__H0`
- `H0__H1`
- `H1__H2`

## `manifest_diff_certification.json`

Purpose: enumerate the exact field-level manifest differences for the same three surface pairs.

```json
{
  "schema_version": "1.0",
  "run_id": "d0_YYYYMMDDThhmmssZ",
  "pairs": [
    {
      "pair_id": "i3__H0",
      "left_surface_id": "i3",
      "right_surface_id": "H0",
      "left_path": "/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_i3.run_manifest.json",
      "right_path": "/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.run_manifest.json",
      "expected_delta_count": 18,
      "observed_delta_count": 18,
      "field_deltas": [
        {
          "field_path": "name",
          "change_type": "changed",
          "left_value": "i3",
          "right_value": "H0",
          "status": "certified"
        }
      ],
      "unexpected_deltas": [],
      "status": "certified",
      "notes": []
    }
  ]
}
```

Required manifest-diff fields are the same as the config-diff fields, with manifest paths substituted.

The `pairs` array must include exactly:

- `i3__H0`
- `H0__H1`
- `H1__H2`

## `eval_surface_fidelity_report.json`

Purpose: certify that the eval surface used by D0 matches the frozen contract and the published run bundles.

```json
{
  "schema_version": "1.0",
  "run_id": "d0_YYYYMMDDThhmmssZ",
  "canonical_eval_manifest_path": "/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json",
  "canonical_eval_manifest_sha256": "a5035f41e89764519df3079d8786392b8c6d21dd2da487d00748dd595ec3d9a0",
  "scorer_path": "/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py",
  "scorer_sha256": "08a5cec22a781193365bed85b709ceebef534846602004bbfa047f4e0b59d738",
  "metric_spec_path": "/opt/ai-stack/assistant-training/docs/metric_specification_v1a.md",
  "metric_spec_sha256": "793a884bbd783c3559828ab2cf84e4ceccc2aab256a80cf360c624dd8a549a3d",
  "split_hashes": {
    "heldout_validation": "78d47d4fb974f0f3245eaf81a17a847febc2667da5926bd372f625cd00b127a5",
    "tool_holdout": "ca492290645cdf3e374bdd456b9488500c594b080180caae9b3b73fe288d0f45",
    "no_call": "0584f529d86b8b319b2abaaa2410e504d614243f32a56a3a1eae44e8f8768fa7",
    "adversarial": "c500b8195722355b54dc7ddb612690daa9ef530ba4b030bcd04c7c2b2b50c5cc",
    "direct_answer": "969d1d5dde3b17515c45c9a5f4b69beb1d908063f61ce470f778d625b1b1afbd"
  },
  "bundles": [
    {
      "bundle_id": "H1_eval",
      "bundle_manifest_path": "/opt/ai-stack/assistant-training/evals/baselines/llama31/internal_reference_regimes/h1_diversity_patch_20260611T125835Z/package_manifest.json",
      "bundle_manifest_sha256": "<computed_at_runtime>",
      "comparison_rows_path": "/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/comparison_rows.jsonl",
      "summary_path": "/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/summary.json",
      "status": "pass",
      "notes": []
    }
  ],
  "status": "pass",
  "notes": []
}
```

Required eval-fidelity fields:

- `canonical_eval_manifest_path`
- `canonical_eval_manifest_sha256`
- `scorer_path`
- `scorer_sha256`
- `metric_spec_path`
- `metric_spec_sha256`
- `split_hashes`
- `bundles`
- `status`

The `bundles` array must include every executed bundle that D0 certifies, at minimum the `H0`, `H1`, and `H2` comparison bundles.

## `missing_artifact_report.json`

Purpose: record any required or corroborating artifact that is absent from the repository snapshot or from the run package.

```json
{
  "schema_version": "1.0",
  "run_id": "d0_YYYYMMDDThhmmssZ",
  "missing": [
    {
      "artifact_path": "/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json",
      "required": true,
      "surface_id": "eval_surface",
      "reason": "absent from snapshot",
      "severity": "blocking",
      "status": "missing",
      "notes": []
    }
  ],
  "status": "pass"
}
```

Required missing-artifact fields:

- `artifact_path`
- `required`
- `surface_id`
- `reason`
- `severity`
- `status`

## `acceptance_summary.json`

Purpose: provide the final run-level decision and pointers to all other outputs.

```json
{
  "schema_version": "1.0",
  "run_id": "d0_YYYYMMDDThhmmssZ",
  "overall_status": "blocked",
  "surface_statuses": {
    "i3": "pass",
    "H0": "pass",
    "H1": "pass",
    "H2": "pass"
  },
  "certified_diffs": {
    "i3__H0": "certified",
    "H0__H1": "certified",
    "H1__H2": "certified"
  },
  "output_artifacts": [
    "inventory/source_artifact_inventory.json",
    "ledgers/hash_ledger.json",
    "ledgers/row_ledger.jsonl",
    "reports/dataset_integrity_report.json",
    "reports/patch_accounting_report.json",
    "reports/tool_family_distribution_report.json",
    "diffs/config_diff_certification.json",
    "diffs/manifest_diff_certification.json",
    "reports/eval_surface_fidelity_report.json",
    "reports/missing_artifact_report.json"
  ],
  "blocking_failures": [],
  "advisory_findings": [],
  "status": "blocked",
  "notes": []
}
```

Required acceptance-summary fields:

- `overall_status`
- `surface_statuses`
- `certified_diffs`
- `output_artifacts`
- `blocking_failures`
- `advisory_findings`
- `status`

## Schema Consistency Rules

- Every machine-readable artifact must reference the same `run_id`.
- Every artifact must point back to the authoritative authority matrix.
- Every diff report must enumerate field paths explicitly.
- Every failure report must use the failure taxonomy names exactly.
- Every missing artifact must remain listed until the run is re-executed.
