# Independent Validation: Evaluator Reconstruction Claim

**Repository:** /opt/ai-stack/assistant-training  
**Review Date:** 2026-06  
**Scope:** Pure evidentiary analysis of the claim that the authoritative evaluation path reconstructs facts in the evaluator layer when source metadata is absent, in conflict with Stage B doctrine ("missing data remains missing", "no inference", "no reconstruction", "governance consumes emitted facts only").  
**Constraints observed:** No redesign, no fixes, no migration plans, no recommendations. All conclusions cite exact files, functions, paths, and logic. Codex claim treated as hypothesis only; verified/falsified from repo evidence. Authoritative path determined from current manifests, configs, run records, and execution packages (not historical docs).

**Final Verdict:** **Claim validated**

The authoritative evaluation path does perform reconstruction/derivation of governed sub-slice facts (anchor category, read_file symbol-name membership/archetype) and failure subtype classifications inside the evaluator when source dataset metadata does not explicitly declare them. These derived values are used to compute the `failure_profile` (including `read_file_symbol_name_exact_valid`, `anchor_exact_share`, `failure_categories_non_exact_tool_rows.direct_answer_substitution`, etc.) that is emitted in the summary and consumed by governance (detector, thresholds, gates, reports). The current canonical evaluation data (the data used by the authoritative path) systematically lacks the explicit Stage B metadata markers, causing consistent fallback to prompt-text and output-text heuristics in the evaluator. This creates a governance gap vs. the doctrine that membership/ sub-slice facts for governed concepts must be declared/emitted (not inferred from prompt), that prompt text is not valid membership evidence, and that reconstruction should not occur for missing metadata.

---

## 1. Authoritative Evaluation Path

The current authoritative evaluation path is:

- **Manifest:** `evals/canonical_eval_manifest_v1.json` (defines `scoring.scorer_script`, datasets/splits, tokenizer, decode defaults, legacy reference).
- **Scorer/Evaluator script:** `scripts/eval_canonical_manifest.py` (the `scorer_script` value; invoked with `--manifest` pointing to the json; produces `summary.json` containing `failure_profile`, `metrics`, and `comparison_rows.jsonl`).
- **Execution examples (current runs/probes):** 
  - `manifests/reports/stage_b_successor_probe_execution_package.md`: `python /opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py --manifest /opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json --model-name-or-path ... --adapter-dir ... --out-dir ...`
  - `manifests/reports/stage_b_first_probe_execution_results.md` and `stage_b_first_probe_artifact_inventory.json`: same invocation for M/H probe eval.
  - `manifests/runs/stage_b_llama31_8b_base_v1_geometry_probe_lh.run_manifest.json`, `configs/lora/stage_b_llama31_8b_base_v1_geometry_probe_lh.config.json`, `artifacts/.../resolved_config.json`: reference `"canonical_eval_manifest_path": "/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json"`
  - `manifests/reports/stage_b_v1_i10r_counterbalanced_probe_training_execution_readiness.json` and similar for other i10r: `"evaluator_script": "/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py"`
  - `evals/runs/stage_b_v1_geometry_probe_lh_eval/summary.json` (and other recent probe evals): `"manifest_path": "/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json"`
- **Downstream consumers of outputs:** `scripts/post_eval_collapse_detector.py` (loads summary for metric resolution and gate/collapse_watch), probe scientific assessments/gates, canonical eval summaries in `manifests/reports/`, training readiness/execution packages, reports/stage_c* contract artifacts (for baselines), tests/test_eval_canonical_manifest.py.
- **Legacy (non-authoritative):** `scripts/eval_adapter_toolcalls.py` is listed as `legacy_eval_script` in the manifest and referenced in old README/docs/index, but all Stage B probe execution packages, run manifests, configs, and recent eval runs use the canonical script. The canonical manifest's `scoring.scorer_script` points to `eval_canonical_manifest.py`.

**Flow (from `scripts/eval_canonical_manifest.py` main + helpers):**
1. Load manifest (`evals/canonical_eval_manifest_v1.json`).
2. For each split (heldout_validation, tool_holdout, no_call, adversarial, direct_answer): `_load_jsonl(dataset path)` → `_build_rows(...)` (extracts `messages`, `metadata` from source jsonl; derives `expected_*` from reference assistant message in data via `_expected_from_row`; stores `metadata=dict(meta)`).
3. `_eval_one_side(...)`: `_infer(...)` (model generation) → for each: `_classify(row, output_text)` (parse/validate/match to expected) → `labels = _build_preaggregation_labels(row, classified)` → build row dict with `**labels` + "eval": classified.
4. `_build_failure_profile(detector_rows)` (uses the labels: `failure_subtype`, `symbol_name_membership`, `anchor_bucket`, `expected_primary_tool_name`, `eval["exact_valid"]` etc. to compute rates/counts).
5. Write `summary.json` (includes `"failure_profile"`, `"metrics"`, `"detector_summary_side"`) + `comparison_rows.jsonl` (rows carry the derived labels).
6. Later: detector loads summary, resolves paths like `failure_profile.read_file_symbol_name_exact_valid.rate` (and similar for anchor, direct_answer_substitution, no_anchor_phrase) per `threshold_profile.json` metric_catalog.

This path is used for all recent probe evals (M/H, L/H, i10r baselines) whose summaries feed the gates/thresholds in Stage B record.

**Data sources for authoritative path:** `evals/data/canonical_v1/*.jsonl` (heldout_validation, tool_holdout, no_call, adversarial, direct_answer). These contain `{"messages": [...], "metadata": {...}}`. Metadata is minimal (e.g., `{"category": "...", "source": "...", "source_case_id": "p0_read_file_2", "tool": "read_file", "synthetic": False}`); **no `symbol_name_membership`, `read_file_archetype`, `anchor_bucket`, `anchor_assignment_owner`, `failure_subtype` etc.**

---

## 2. Evaluator Behavior Examination

The evaluator (`scripts/eval_canonical_manifest.py`) adds/derives facts in `_build_preaggregation_labels` (called for every row in `_eval_one_side`, lines ~800) and uses them in `_build_failure_profile` (lines 382-430) and row emission. Key sites:

### 2.1 Sub-slice Membership / Archetype Labels (anchor, read_file symbol-name)

**Functions:**
- `_anchor_assignment_labels(row: EvalRow)` (lines 254-274):
  ```python
  meta = row.metadata
  explicit_bucket = None
  for key in ("anchor_bucket", "eval_anchor_bucket", "intervention_i10_anchor_bucket"):
      value = meta.get(key)
      if isinstance(value, str) and value.strip():
          explicit_bucket = value.strip()
          break
  ...
  if explicit_bucket is not None:
      return (explicit_bucket, explicit_owner or DATASET_METADATA_OWNER, ...)
  return (
      _prompt_anchor_bucket(row.user_text),
      explicit_owner or EVALUATOR_PREAGGREGATION_OWNER,
      ...
  )
  ```
- `_prompt_anchor_bucket(prompt: str)` (lines 220-228):
  ```python
  lowered = prompt.lower()
  if "tool_calls" in lowered: return "literal_tool_calls"
  if "tool call" in lowered or ... : return "paraphrastic_tool_call"
  if "json object" in lowered or ... : return "schema_paraphrase"
  return "no_anchor_phrase"
  ```
- `_read_file_membership_labels(row: EvalRow)` (lines 277-311):
  ```python
  ... check meta for "read_file_archetype", "symbol_name_membership", "symbol_name_membership_owner" ...
  if explicit_archetype is not None:
      ...
  if explicit_membership is not None:
      ...
  derived_archetype = _read_file_archetype(row.user_text)
  return (derived_archetype, derived_archetype == "read_file_symbol_name", explicit_owner or EVALUATOR_PREAGGREGATION_OWNER)
  ```
- `_read_file_archetype(prompt: str)` (lines 231-239):
  ```python
  lowered = prompt.lower()
  if "report whether" in lowered and "appears" in lowered: return "read_file_boolean_presence"
  if "first function name" in lowered: return "read_file_first_function_name"
  if "symbol name" in lowered: return "read_file_symbol_name"
  return "read_file_other"
  ```

**Call site (line 800 in `_eval_one_side`):**
```python
labels = _build_preaggregation_labels(row, classified)
...
"**labels**,  # includes failure_subtype, anchor_bucket, ..., symbol_name_membership, ...
"eval": classified,
```
(See `_build_preaggregation_labels` lines 344-355, which calls the above.)

**Usage in emitted facts ( `_build_failure_profile`, lines 393-429, using detector_rows that carry the labels):**
```python
read_file_rows = [row for row in tool_rows if str(row.get("expected_primary_tool_name") or "") == "read_file"]
...
symbol_rows = [row for row in read_file_rows if row.get("symbol_name_membership") is True]
...
anchor_counts... for row in exact_tool_rows: bucket = str(row.get("anchor_bucket") or "")
...
"read_file_symbol_name_exact_valid": { "count": ..., "rows": ..., "rate": ... },
"anchor_exact_share": { bucket: rate for bucket in LEGACY_ANCHOR_BUCKETS },
"failure_categories_non_exact_tool_rows": { key: count for key in FAILURE_SUBTYPE_KEYS },
```
These go into `result["failure_profile"]` (line 961) in the summary.json that feeds governance.

**Evidence that source metadata is absent in authoritative data:**
- `evals/data/canonical_v1/heldout_validation.jsonl` (and other splits): rows have `metadata` with keys like `category, source, source_file, source_case_id, tool, synthetic` (e.g., `{"source_case_id": "p0_read_file_2", "tool": "read_file"}`). No `anchor_*`, `symbol_name_membership`, `read_file_archetype`, `intervention_*_archetype` etc. (verified by direct inspection of jsonl + sampling in runs).
- Even in probe training data used to produce the adapters (`data/v1_0/dataset_v1_0_stage_b_recovery_i10r_counterbalanced_train.jsonl`): added read_file symbol rows have intervention fields but **no `symbol_name_membership` or `read_file_archetype`** key; membership is still derived at eval time via prompt match on the eval data (canonical splits, not the train data).
- In emitted comparison_rows/summary rows from actual runs (e.g., `evals/runs/stage_b_v1_geometry_probe_lh_eval/comparison_rows.jsonl`): for p0_read_file_2 case: `"anchor_bucket": "no_anchor_phrase", "anchor_assignment_owner": "evaluator_pre_aggregation_v1"`, `"read_file_archetype": "read_file_symbol_name", "symbol_name_membership": true, "membership_owner": "evaluator_pre_aggregation_v1"`. (The "owner" explicitly marks evaluator derivation.)

### 2.2 Failure Subtype Classification

**Function `_failure_subtype(row: EvalRow, classified: dict[str, Any])` (lines 314-341):**
```python
if not row.expected_tool or bool(classified.get("exact_valid", False)):
    return None
generated = str(classified.get("generated_text") or "").strip()
lowered = generated.lower()
parse_mode = str(classified.get("parse_mode") or "")
schema_reason = str(classified.get("schema_reason") or "")
primary_class = str(classified.get("primary_class") or "")
if primary_class in {"wrong_tool_name", ...}: return "near_canonical_wrapper_or_envelope_drift"
if schema_reason == "missing_tool_calls": return ...
if parse_mode in {"invalid", "empty"} or ...:
    if _is_number_token... : return "scalar_substitution"
    if ... or _looks_like_tool_intent(generated): return "malformed_partial_json"
    return "direct_answer_substitution"
... other rules ...
return "other_non_exact"
```
Always returns a subtype (or None for exact); no source metadata key for it in data. Used directly in labels and `failure_categories_non_exact_tool_rows` in `failure_profile`.

**Call:** Same as above, injected into rows and profile.

### 2.3 Other Derivations (for context)
- `source_case_id` fallback (line 514 in `_build_rows`): `str(meta.get("source_case_id") or meta.get("case_id") or f"{split}_{idx}")` — minor normalization.
- `expected_*` (tool/no_call/payload/names/args): derived in `_expected_from_row` (lines 445-460) by inspecting the *reference assistant message* in the source jsonl `messages[2]`. This is definitional for the test case (the data "emits" the ground truth by containing the target assistant content); not reconstruction of "missing" governance facts.
- `exact_valid`, `primary_class`, `schema_reason`, `parse_mode`, etc.: in `_classify` (lines 608+), based on parsing generated vs. the expected (from data) + internal rules. Standard scoring.

These are the core sites of potential reconstruction for governed concepts.

---

## 3. Categorized Findings

**Finding 1: Derivation of `anchor_bucket` (and owner/taxonomy) from prompt text.**
- **Category:** Proven Reconstruction
- **Why:** When `row.metadata` lacks explicit `anchor_bucket`/`eval_anchor_bucket`/`intervention_i10_anchor_bucket` (always true for canonical_v1 data and most recovery data), `_anchor_assignment_labels` (lines 270-274) explicitly calls `_prompt_anchor_bucket(row.user_text)` (string matching on prompt) and assigns owner `EVALUATOR_PREAGGREGATION_OWNER`. The value is injected into every row and used to compute `anchor_exact_share` in `_build_failure_profile` (the value emitted for governance consumption in summary "failure_profile"). Source artifacts (dataset jsonl) emit only basic metadata + full prompt; they do not emit the anchor category fact. This is exactly "reconstructs facts when source metadata is absent" inside the evaluator layer. Matches the Codex claim verbatim. (Evidence: canonical data samples, comparison_rows from lh eval, code paths above.)

**Finding 2: Derivation of `read_file_archetype` + `symbol_name_membership` (and owner) from prompt text.**
- **Category:** Proven Reconstruction
- **Why:** Identical structure in `_read_file_membership_labels` (lines 298-311): if no explicit `read_file_archetype`/`symbol_name_membership` in meta, derives via `_read_file_archetype(row.user_text)` (string match for "symbol name", "first function name", etc.) and sets membership bool + `EVALUATOR_PREAGGREGATION_OWNER`. Used in `_build_failure_profile` for `read_file_symbol_name_exact_valid` rate/count (core governed metric for Family B1 read-file preservation sub-slice). Source data lacks the keys (see inspections); prompt text is used as proxy. Per Stage B fixtures (e.g., B1-NI-003), "prompt text is not membership evidence" and "infer_symbol_name_membership_from_prompt_text": false. The evaluator is performing the inference that doctrine reserves for explicit emission. Owner mark acknowledges derivation but does not prevent it from feeding the emitted profile. Proven in authoritative path (canonical eval runs for probes use this for all read_file rates in their summaries/gates).

**Finding 3: Derivation of `failure_subtype` (including direct_answer_substitution etc.).**
- **Category:** Proven Reconstruction (for governed taxonomy)
- **Why:** `_failure_subtype` (lines 314-341) has no source metadata input for the subtype; it synthesizes entirely from `classified` (generated_text, parse_mode, schema_reason, primary_class — all from model output + internal parse rules in `_classify`/`_extract_json_payload` etc.) + `row.expected_tool`. Result injected and aggregated into `failure_categories_non_exact_tool_rows.direct_answer_substitution` (and others) in `failure_profile`. This is the "governed failure-subtype taxonomy" (Family A) from redesign. No "emitted" subtype fact in source data; evaluator creates the label. Used directly in detector metrics/gates. (Governance-significant because direct_answer_substitution is one of the 4 explicitly retained governed concepts in redesign contracts.)

**Finding 4: Fallbacks and normalizations for source_case_id, expected_*, exact_valid, etc.**
- **Category:** Harmless Normalization (for core eval) / No Reconstruction (for governance sub-slices)
- **Why:** `source_case_id` fallback and `expected_*` derivation are from the reference assistant message in the source jsonl `messages` (the data *is* the test case definition; it "emits" the ground truth). `exact_valid`/`primary_class` etc. are standard scorer logic matching prediction to reference. These are not "when source metadata is absent" for the Stage B governed sub-slices (anchor/symbol/failure taxonomy); they are the definition of the eval. Not the reconstruction of missing governance facts. (Contrast with Findings 1-3, which specifically target the redesign concepts and fall back to prompt/output heuristics.)

**Finding 5: Injection of derived labels into comparison_rows and summary (for downstream use).**
- **Category:** Proven (enables the above in governance)
- **Why:** Rows emitted to `comparison_rows.jsonl` and used for `detector_rows` in summary always carry the evaluator-derived labels (with owner). No separate "raw source marker" vs. "derived" distinction is preserved in the profile itself (profile just uses the final values). This means governance (e.g., probe gates using i10r_counterbalanced or geometry summaries) sees rates computed from reconstructed values without the "metadata absent" case surfacing as noncomputable for the subslice.

No other reconstruction sites found in the main path that affect the governed metrics in `failure_profile` (the ones tied to the Codex claim and Stage B doctrine).

---

## 4. Evidence Citations (Exact)

- **Authoritative script + flow:** `scripts/eval_canonical_manifest.py:856` (main), `879-890` (build rows from canonical data), `796-823` (_eval_one_side + labels), `943-961` (select detector side + failure_profile + write summary), `961` (result["failure_profile"] = _build_failure_profile(detector_rows)).
- **Derivation logic (anchor):** `scripts/eval_canonical_manifest.py:254-274` (_anchor_assignment_labels + fallback to _prompt_anchor_bucket:220-228).
- **Derivation logic (symbol/read_file):** `scripts/eval_canonical_manifest.py:277-311` (_read_file_membership_labels + fallback to _read_file_archetype:231-239).
- **Subtype synthesis:** `scripts/eval_canonical_manifest.py:314-341` (_failure_subtype) + `344-355` (_build_preaggregation_labels) + `800` (call site).
- **Use in emitted governance facts:** `scripts/eval_canonical_manifest.py:393-429` (_build_failure_profile, using row.get("symbol_name_membership"), row.get("anchor_bucket"), row.get("failure_subtype"), etc. for the exact rates in redesign contracts: read_file_symbol_name_exact_valid_rate, no_anchor_exact_valid_share, direct_answer_substitution_count, read_file_exact_valid_rate).
- **Source data lacks markers:** `evals/data/canonical_v1/heldout_validation.jsonl` (and siblings): metadata samples (e.g., p0_read_file_2: only category/source/source_file/source_case_id/tool/synthetic); confirmed via direct `python -c` sampling + `evals/runs/.../comparison_rows.jsonl` outputs from authoritative runs (labels present with "evaluator_pre_aggregation_v1" owner, no raw meta in emitted rows).
- **Probe execution uses this path:** `manifests/reports/stage_b_successor_probe_execution_package.md:88`, `stage_b_first_probe_execution_results.md:30`, `manifests/runs/stage_b_llama31_8b_base_v1_geometry_probe_lh.run_manifest.json:11`, `evals/canonical_eval_manifest_v1.json:79` (scorer_script), `evals/runs/stage_b_v1_geometry_probe_lh_eval/summary.json:3`.
- **Downstream governance consumption:** `scripts/post_eval_collapse_detector.py` (metric resolution from summary paths matching threshold_profile "failure_profile.*"), `manifests/reports/stage_b_*_probe_gate_assessment.json` + scientific_assessments (use the resulting rates for hard invariants/catastrophic/watch on exactly these), `manifests/reports/stage_b_v1_i10r_*_canonical_eval_summary.json` (baselines with failure_profile).
- **Doctrine references (for conflict assessment):** `manifests/reports/stage_b_wp8_validation/fixtures/family_b1/b1_ni_003_symbol_like_prompt_rejected.json` ("infer_symbol_name_membership_from_prompt_text": false, "prompt_text_valid_membership_input": false, "membership_owner": "dataset metadata or evaluator-owned metadata preparation", "detector_role": "consumer only"); `docs/convergence/STAGE_B_EVAL_REDESIGN_CONTRACTS.md` (primary owner "evaluator, with dataset metadata support" for symbol; "The prompt anchor category must be declared before detector consumption. The detector must not classify prompts using string matching."; "Protect `read_file` procedural commitment"; no proxy/reconstruction); `STAGE_B_B1_NI_SCENARIO_RECONCILIATION_REVIEW.md`, `STAGE_B_WP8_B2_EXIT_REVIEW.md` (non-inference, catalog authority, prompt not evidence); `STAGE_B_EVAL_REDESIGN_SCHEMA_PROPOSAL.md` / `METRIC_INVENTORY.md` (explicit emission required for governed concepts).

---

## 5. Evaluation Against Stage B Doctrine

**Governance-significant violations (yes):**
- **"Missing data remains missing" / noncomputable for subslice when marker absent:** Violated in effect. Because canonical source data has no marker, evaluator always derives a value (via prompt match). The emitted `failure_profile.read_file_symbol_name_exact_valid` etc. always has a computable rate based on derivation; there is no path where "missing symbol_name_membership marker" produces noncomputable subslice rate in the summary (as required by B1-NI-004, B1-M-004 fixtures, matrix plan). The "absent metadata" case is hidden by reconstruction.
- **"No inference" / "no reconstruction" from prompt text:** Violated. `_prompt_anchor_bucket` and `_read_file_archetype` + conditional logic are string matching / classification on `row.user_text` (prompt). Doctrine (B1-NI-003 fixture, contracts): "prompt text is not membership evidence", "infer ... from prompt text": false, "The detector must not classify prompts using string matching" (and by extension, the pre-emission layer for governed facts should not either when metadata is the declared source). The evaluator is doing what the NI fixtures and contracts prohibit.
- **"Governance consumes emitted facts only":** Partially violated in spirit. The facts in `failure_profile` (the ones consumed by detector via summary paths in threshold/gates) are *not* emitted by the source dataset artifacts; they are synthesized in the evaluator from prompt + output. Even with "evaluator_pre_aggregation_v1" owner mark, the profile does not carry a "source_declared" vs. "reconstructed" distinction that would allow governance to treat reconstructed as noncomputable/missing. Detector is a pure consumer of the (reconstructed) profile.
- **"Detector_role: consumer only" / no prompt access for membership:** The reconstruction is upstream (evaluator), so detector doesn't see the prompt. But the *emitted fact* it consumes was produced by forbidden inference. This shifts (but does not eliminate) the governance gap: the "source of truth" for the rate is now the evaluator's heuristic instead of declared metadata.

**Observability-only behavior (partial):**
- The owner marking (`EVALUATOR_PREAGGREGATION_OWNER` vs. `DATASET_METADATA_OWNER`) provides *some* audit trail in the row data (visible in comparison_rows). This is better than silent reconstruction. However, it is not propagated into the `failure_profile` rates themselves (the governance surface), so detectors/gates see clean numbers without the "reconstructed" flag affecting computability.

**Benign implementation details (no):**
- Core scoring (`_classify`, exact_valid, expected from reference assistant message in data): These are the definition of "what the test case expects" (data emits the ground truth via its assistant message content). Not reconstruction of absent governance metadata. Not in conflict with Stage B (the redesign targets the *additional* sub-slice labels on top of basic exact-valid/tool matching).
- Fallbacks for source_case_id: Benign, not tied to governed sub-slices.

**Overall against doctrine:** The behavior for the 4 explicitly retained governed metrics (from redesign contracts + metric inventory + fixtures) conflicts with "missing data remains missing", "no inference", "no reconstruction", and "governance consumes emitted facts only" when the (current) source metadata is absent — which it systematically is in the authoritative canonical data path. The "evaluator-owned metadata preparation" allowance in some docs/fixtures appears to be a pragmatic interim for data that lacks declarations, but it directly implements the reconstruction the claim describes and that the NI fixtures were written to prohibit. This is a meaningful Stage B governance concern (not just observability), because it means the probe gates, thresholds, and future governance on read_file preservation / no-anchor / direct_answer substitution / symbol sub-slice are operating on facts that were reconstructed rather than declared, undermining the non-inference and missing=noncomp guarantees that the WP8 fixtures and B1/B2 reviews were meant to enforce.

The reconstruction is *in the evaluator layer* (as claimed), not (primarily) in the detector.

---

## 6. Final Verdict

**Claim validated.**

The Codex claim is directly supported by the code paths, data contents, and emitted artifacts in the authoritative evaluation path (`evals/canonical_eval_manifest_v1.json` + `scripts/eval_canonical_manifest.py`). When source metadata is absent (the normal case for the canonical eval data used in all Stage B probe evals and baselines), the evaluator reconstructs anchor_bucket, read_file symbol-name membership/archetype, and failure subtypes via prompt/output heuristics; these feed the failure_profile rates that governance consumes. This is in conflict with the Stage B doctrine as expressed in the WP8 fixtures (explicit "infer from prompt text: false"), redesign contracts ("no reconstruction", "declared before detector consumption", "prompt text is not membership evidence"), and related reviews. The owner marking and "evaluator preparation" language mitigate but do not eliminate the gap for the authoritative path and current data.

Evidence is exhaustive from the cited files/functions/rows/outputs; no external assumptions required.

**End of Assessment.** (All analysis used only live repo contents at the time of inspection; no prior conclusions adopted.)