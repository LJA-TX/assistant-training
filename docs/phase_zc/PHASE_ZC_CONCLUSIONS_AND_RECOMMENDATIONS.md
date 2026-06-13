# Phase ZC Conclusions And Recommendations

## Promotion Conclusion

**Do Not Promote**

Treatment C is the best capability result in the preservation sweep, but it still fails to recover the H1/H2 capability floor and it loses adversarial no-call safety.

## Attribution Conclusion

Anchor concentration is **not a sufficient explanation** for H1/H2-style capability recovery.

The sweep shows that anchor concentration matters, but the effect is:

- incomplete,
- non-monotonic,
- and entangled with safety regression.

The evidence therefore supports a mixed-cause interpretation rather than a single anchor-density explanation.

## Operational Conclusion

The execution was successful:

- preflight passed
- training completed
- canonical evaluation completed
- contamination stayed clean
- the frozen framework remained unchanged

## Evidence-Based Recommendations

1. Do not promote the Treatment C adapter under the frozen Phase L contract.
2. Do not treat anchor concentration alone as the final causal explanation for H1/H2 success.
3. Reuse the ablation evidence as a boundary condition for later analysis:
   - anchor concentration helps exact-call realization,
   - but it does not preserve the full safety/capability balance by itself.
4. Shift future investigation toward the remaining factors that were preserved in H1/H2 but not isolated by this sweep:
   - prompt regime structure,
   - schema realization details,
   - scaffold interaction,
   - and any tool-family composition effects that co-varied with the successful runs.

## Final Determination

The preservation ablation is complete.

Anchor concentration is a viable contributor, but not a sufficient primary explanation for H1/H2-style capability recovery.
