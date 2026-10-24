# Finite quantum continuation — verification

**Status:** passed. **Arithmetic:** exact Gaussian rationals; no floating-point tolerance.

233 named checks completed. These verify the worked instances, not the general proofs.

| Quantity | Exact result |
| --- | --- |
| Actuator-only observation effect dimension | 2 |
| All source instruments with actuator output | 8 |
| Full joint output effect dimension | 16 |
| Coherent/dephased processes at restricted output | Equal |
| Coherent/dephased processes at full output | Different |
| Recovery outcome, coherent preparation | 1 |
| Recovery outcome, dephased preparation | 1/2 |
| Record kept / flipped: actuator-1 probability | 1/2 / 0 |
| Stationary observable closure dimensions | 2 → 4 → 8 → 12 → 16 → 16 |
| Qutrit orthogonal-projection determinant | −1/27 |

The effect dimensions measure retained predictive coordinates in this model. They are not lushness scores.

The process matrices satisfy exact causal trace constraints and have independently checked positive Gram decompositions. Sixteen physically realizable measure/prepare operations span the intervention Choi space; direct circuit and process-matrix outputs agree on all sixteen. Backward effect propagation agrees with forward probabilities.

## Reproduce

Run with Python 3.10 or newer; no third-party packages are required.

```bash
python3 10_FINITE_QUANTUM_CONTINUATION_VERIFY.py
```

Complete check names and sparse process matrices: [10_FINITE_QUANTUM_CONTINUATION_RESULTS.json](10_FINITE_QUANTUM_CONTINUATION_RESULTS.json).

Script SHA-256: `63f5e556778d990ca3dfb818e42f34c8431ca7e27b658e157b519887633eef32`

## Boundaries

- No Planck cutoff or quantum-gravity model is derived.
- No valuerhood, phenomenal correspondence, lushness measure, or ordering is supplied.
- Boundaries, permitted operations, and causal schedule are declared model inputs.
- Finite closure is algebraic predictive completeness for the declared controls, not a minimum physical length.
- This is not a Lean proof or a re-execution of the existing Omega repository suite.
