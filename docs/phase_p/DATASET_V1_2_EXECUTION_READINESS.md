# Dataset V1.2 Execution Readiness

## Status

**Ready**

## Verification Summary

Dataset v1.2 satisfies the structural readiness conditions from Phase N and Phase O.

| Check | Result | Evidence |
|---|---|---|
| Contamination status | PASS | Zero overlap on prompt, target, and source-case ID across `heldout_validation`, `tool_holdout`, `no_call`, `adversarial`, and `direct_answer`. |
| Structural targets | PASS | Train rows `2160`, val rows `240`, total rows `2400`. |
| Anchor targets | PASS | Core anchor share `0.5200` and `rg_search + read_file` share `0.3133`. |
| Density targets | PASS | Train tool-positive density `0.6449`. |
| Safety-block preservation | PASS | Runtime alignment, no-call direct, refusal, and adversarial slices are all present. |
| Tool-family representation | PASS | All `26` tool families remain represented. |

## Dataset Facts

| Item | Value |
|---|---:|
| Tool-positive rows | `1548` |
| Runtime alignment rows | `360` |
| No-call direct rows | `240` |
| Refusal rows | `180` |
| Adversarial no-call rows | `72` |
| Train tool-positive rows | `1393` |
| Train tool-positive density | `0.6449` |
| Core anchor share | `0.5200` |
| `rg_search + read_file` share | `0.3133` |

## Consistency With Phase N

The observed v1.2 composition stays inside the Phase N target bands:

- tool-positive density: target `0.63` to `0.65`, observed `0.6449`;
- core anchor share: target `0.45` to `0.55`, observed `0.5200`;
- `rg_search + read_file` share: target `0.30` to `0.40`, observed `0.3133`;
- tool families: target `26`, observed `26`.

That is the intended anchor-weighted hybrid shape.

## Readiness Conclusion

Dataset v1.2 is ready as a governed-execution candidate.

The dataset itself is not the blocker.
The remaining caveat is operational promotion of the checked-in Phase L run assets to reference `data/v1_2/`.
