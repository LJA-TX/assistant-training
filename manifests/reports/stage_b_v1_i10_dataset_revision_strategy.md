# Stage B i10 Dataset Revision Strategy (Planning Only)

## Executive Summary
Immediate micro-probe execution remains inadvisable under the current unweighted legacy-dominant exposure mix.  
Recommended next step is a **bounded deterministic dataset revision** (no objective drift) to reduce ritualized legacy pressure while preserving robustness and lineage continuity.

## Reconnaissance Findings
Targeted composition (`972` rows):
- `i3_adapt_*`: `667` (`68.62%`)
- `i3_read_literal_* + i3_rg_readstyle_* + i3_long_rg_*`: `101` (`10.39%`)
- `i9_conv_*`: `102` (`10.49%`)
- `i10_conv_*`: `102` (`10.49%`)

### Procedural / Semantic Health by Family Class
- `i3_read_literal_*`, `i3_rg_readstyle_*`, `i3_long_rg_*`
  - semantic variation: `0.0`
  - mean NN similarity: `1.0`
  - high shell concentration signals
  - classification: **structurally dangerous**
- broader `i3_adapt_*`
  - semantic variation: `0.0`
  - mean NN similarity: `1.0`
  - very low procedural diversity (`unique tool+args ratio ~0.0315`)
  - classification: **weak but useful** (coverage value, but dominant/confounding)
- `i9_conv_*`
  - high prompt/skeleton diversity, moderate semantic variation
  - classification: **healthy bridge**
- `i10_conv_*`
  - strongest healthy profile; primary read_file commitment families
  - classification: **healthy + irreplaceable**

## Revision Philosophy
- Preserve lineage continuity: do not erase legacy classes.
- Preserve thin legacy contrastive stress.
- Preserve uncertainty exposure.
- Preserve no-call robustness and wrapper/no-leak invariants by leaving non-targeted/no-call components untouched.
- Avoid hidden weighting-by-proxy: rules must be deterministic and auditable.

## Recommended Strategy
Strategy: **deterministic family thinning with contrastive floors**

- Keep `i10_conv_*` untouched.
- Keep `i9_conv_*` untouched.
- Thin `i3_read_literal_*`, `i3_rg_readstyle_*`, `i3_long_rg_*` to contrastive-anchor-only representation.
- Thin broader `i3_adapt_*` with explicit per-family caps/floors (retain all families).

### Recommended Planning Scenario (Balanced)
- `i3_adapt`: retain `55%`
- risky legacy (`read_literal/readstyle/long_rg`): retain `30%`
- `i9_conv`: retain `100%`
- `i10_conv`: retain `100%`

Projected targeted mix:
- legacy total: `~66.06%`
- healthy conversion total: `~33.94%`

This is a bounded shift: enough to reduce confounding dominance while avoiding clean-room redesign behavior.

## Minimum Viable Retained Legacy Exposure
Recommended first-revision legacy retention envelope: **~0.64 to 0.69** of targeted rows.

- Above this: likely still heavily confounded.
- Far below this in one pass: over-revision risk rises (lineage comparability + robustness pressure loss).

## Interpretability and Anti-Drift Safeguards
- No semantic rewrites in the revision step.
- No synthetic augmentation in this step.
- Publish pre/post family-retention and diversity telemetry before any training request.
- Maintain canonical eval topology and thresholds unchanged.

## Explicit Conclusions
1. Most dangerous legacy families procedurally:
   - `i3_read_literal_*`, `i3_rg_readstyle_*`, `i3_long_rg_*`, and high-share `i3_adapt_p0_*` families.
2. Legacy families with robustness value:
   - broader `i3_adapt_*` (thinned), especially multi-tool lineage stress slices.
3. Minimum viable retained legacy exposure:
   - roughly `64–69%` targeted share for first bounded revision.
4. Best interpretability-preserving revision strategy:
   - deterministic family thinning with floors/caps and full i9/i10 conversion retention.
5. Best ritualization-pressure reduction strategy:
   - strong thinning of literal/readstyle/long_rg slices to contrastive-anchor-only representation.
6. Cleaner signal expectation vs current unweighted exposure:
   - **Yes**.
7. Principal risk of over-revision:
   - robustness/uncertainty underexposure and weaker lineage comparability.
8. Next step after this planning pass:
   - **bounded dataset revision** (not micro-probe execution yet).

## Go/No-Go
- **Go**: bounded dataset revision execution (deterministic, auditable).
- **No-Go**: immediate micro-probe execution on current unweighted legacy-dominant dataset.
