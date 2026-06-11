# Dataset V1.2 Recommendation

## Recommendation

Build Dataset v1.2 as an **anchor-weighted hybrid with modest density restoration**.

That is the best-supported design for recovering H1/H2 tool-call capability while preserving Phase L safety.

## Why This Is The Best Option

The evidence says:

- pure density restoration is probably not enough,
- pure anchor weighting risks safety regression,
- pure curriculum depends on sampler behavior that the current trainer does not guarantee,
- the hybrid is the only option that addresses both the density problem and the flattening problem.

## Recommended Shape

### 1. Preserve An Explicit Safety Block

Keep the exact no-call and adversarial no-call calibration slices.

Do not remove them.
They are the reason Phase L safety improved.

### 2. Restore More Tool-Positive Exposure

Move tool-positive density back toward the H1/H2 range rather than leaving it at the Phase L floor.

The data-supported target is:

- more tool-positive rows than Dataset v1.1,
- fewer safety rows than the Phase L over-calibrated adversarial tail, or else a modest dataset expansion that keeps the safety block intact.

### 3. Reintroduce Anchor Concentration

The repeated core should not be flat.

At minimum, the v1.2 tool-positive core should give the following tools materially more exposure than the long tail:

- `rg_search`
- `read_file`
- `find_files`
- `debug_tools`
- `run_command`

The v1.2 design should also keep the H1 breadth-restoration tools:

- `list_dir`
- `list_models`
- `move_path`

### 4. Keep All 26 Tools Represented

Do not revert to a narrow H2-style tool set.
H1 proved that breadth matters.
The right answer is breadth with structure, not breadth with uniformity.

## Concrete Design Targets

| Target | Recommended range |
|---|---:|
| Tool-positive density | `63%` to `65%` of train rows |
| Core anchor share (`rg_search`, `read_file`, `find_files`, `debug_tools`, `run_command`) | `45%` to `55%` of tool-positive rows |
| `rg_search + read_file` share | `30%` to `40%` of tool-positive rows |
| Unique tool families | `26` |
| Minimum per-tool exposure | Enough to remain auditable; do not flatten to near-uniform counts |
| Safety rows | Preserve explicit no-call and adversarial calibration; do not let safety rows dominate the tool-call signal |

## If The Budget Must Stay Fixed

If total row budget cannot expand, reallocate rows away from the overrepresented adversarial no-call calibration slice first.

Do not steal from:

- the core no-call rows,
- the direct refusal calibration rows,
- or the anchor core too aggressively.

The goal is to reduce over-calibration, not to remove safety.

## If The Budget Can Expand

If a modest expansion is feasible, prefer expansion over pure reallocation.

That keeps the Phase L safety block intact while restoring more tool-positive signal.

## Why Not A Pure Curriculum

The current trainer samples randomly by default.
A pure file-order curriculum is therefore not reliable enough to be the primary answer.

Curriculum-like behavior is only worth using if it is implemented as weighted or staged sampling, not as simple row ordering.

## Final Recommendation In One Sentence

Build a **hybrid, anchor-weighted Dataset v1.2** that restores more tool-positive density, restores anchor concentration, preserves breadth across all 26 tools, and keeps the explicit safety block that made Phase L refusal behavior exact.

## Sources Used

- `docs/phase_m/DATASET_SHAPE_ANALYSIS.md`
- `docs/phase_m/TOOL_FREQUENCY_ANALYSIS.md`
- `docs/phase_l/PHASE_L_EXECUTION_REVIEW.md`
- `scripts/train_lora_sft.py`
