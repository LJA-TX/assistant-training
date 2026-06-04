# Stage C Package 1B Passive Governance Consumer Rationale

## Scope

This artifact records the design rationale for the first passive governance consumer over authoritative Stage C Package 1/1A artifacts.

This is a consumption-only slice. It does not migrate detector authority, threshold authority, comparability policy, or historical metric identities.

## Available Authoritative Inputs

Package 1/1A makes the following authoritative Stage C artifacts available in the live canonical evaluator path:

1. `stage_c_row_fact_metadata_artifact.json`
2. `stage_c_family_a_scorer_evidence_artifact.json`
3. `stage_c_governance_guardrails_artifact.json`
4. `stage_c_runtime_contract_summary_artifact.json`

These artifacts already provide:

1. dataset-owned Family A tool-expected eligibility and row identity;
2. scorer-owned Family A exact-valid / non-exact / subtype / missing-evidence state;
3. evaluator-emitted guardrail state;
4. evaluator-emitted legacy-surface preservation policy.

## Candidate Governance Questions

### Candidate 1

Question:

- Can the authoritative Family A tool-expected population already be consumed directly for governed subtype analysis, and where does explicit missing evidence remain?

Why it is viable:

1. Family A tool-expected eligibility is already present in row-fact metadata.
2. Family A subtype assignment and missing-evidence state are already present in scorer evidence.
3. The question is governance-relevant because missing-evidence handling is an explicit Stage B / Stage C governance concern.
4. The answer requires no reconstruction and no detector/threshold migration.

### Candidate 2

Question:

- Are B1 symbol-name and B2 anchor governed sub-slice ownership markers complete enough for direct governance use?

Why it is less suitable as the first consumer:

1. Current live Package 1/1A runtime outputs often contain no declared B1 or B2 governed memberships.
2. A B1/B2-only first consumer would mostly prove absence of emitted facts rather than demonstrating active scorer-evidence consumption.
3. It would be a weaker demonstration of the post-reconstruction ownership model than a Family A coverage consumer.

### Candidate 3

Question:

- Can a detector-facing projection be consumed directly from Stage C artifacts?

Why it is out of scope for Package 1B:

1. Detector-facing projection already belongs to later Stage C migration-preparation surfaces.
2. Even a non-authoritative detector-shaped consumer risks blurring the boundary between passive governance analysis and detector cutover preparation.
3. The package objective is governance consumption, not detector consumption.

## Selected Governance Question

Selected question:

- For the authoritative Family A tool-expected population, how much scorer evidence is directly consumable for governed subtype analysis, how much remains explicit missing evidence, and are any declared governed ownership markers absent or conflicting?

## Selection Rationale

This question is the smallest defensible first passive governance consumer because:

1. it is governance-relevant;
2. it uses only authoritative Stage C facts already emitted by the live evaluator;
3. it exercises both dataset-owned and scorer-owned facts;
4. it keeps missingness visible rather than repaired;
5. it requires no detector migration, threshold migration, comparability cutover, or legacy-metric replacement.

## Ownership Model Used By The Consumer

The consumer is constrained to consume facts under the existing ownership model:

1. dataset metadata ownership:
   - `row_id`
   - `split_id`
   - `family_a_tool_expected_eligible`
   - declared B1 membership markers
   - declared B2 ownership/category markers
2. scorer ownership:
   - `exact_valid`
   - `non_exact_tool_expected`
   - `subtype_assignment`
   - `missing_evidence`
   - `missing_evidence_reasons`
3. evaluator ownership:
   - guardrail artifact
   - runtime contract summary

The consumer does not infer or replace any owned fact.

## Consumer Output Shape

The consumer emits one governance-facing report:

- `stage_c_package1b_passive_governance_report.json`

The report contains:

1. the governance question and selection rationale;
2. input artifact references;
3. reported values with:
   - originating artifact,
   - owning authority,
   - consumption path;
4. supporting row-ID sets for explicit gaps;
5. integrity checks over authoritative artifact linkage.

## Boundary Confirmation

This design intentionally does not:

1. read or modify `summary.json`;
2. read or modify `failure_profile`;
3. consume detector metric catalogs;
4. consume threshold profiles;
5. compute replacement historical metrics;
6. introduce comparability-policy decisions.
