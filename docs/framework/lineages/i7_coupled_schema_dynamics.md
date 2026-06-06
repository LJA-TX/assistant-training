# i7 Coupled-Schema-Dynamics Finding

- Event: i7 targeted `payload_not_object` in isolation from i3 baseline.
- Result: `payload_not_object` improved vs i6, but `payload_not_parsed` worsened and heldout exact-valid remained failed.
- Key finding: `payload_not_object` did not move independently from `missing_tool_calls`; schema dynamics remained coupled.
- Durable implication: next recovery work should assume coupling among top-level schema failure classes unless disproven.
