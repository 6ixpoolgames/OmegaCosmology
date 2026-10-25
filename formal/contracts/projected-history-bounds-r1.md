# Finite observed-history bounds from a known full present

25 October 2026. Classical finite Markov adapter. This is an ordinary argument
with numerical reference tests, not a proof-assistant result or a physical
faithfulness certificate. It does not change the lushness definition.

Let X be a full sufficient Markov state sampled at a fixed cadence, with known
X_0=x, and let Y_k=f(X_k) be a passive projection. Its history entropy is

H(Y_1,...,Y_n | X_0=x) = sum_k H(Y_k | Y_1,...,Y_(k-1), X_0=x).

For r=min(m,k-1), let Z denote Y_(k-r),...,Y_(k-1). Then

H(Y_k | Z, X_(k-r-1), X_0=x)
<= H(Y_k | Y_1,...,Y_(k-1), X_0=x)
<= H(Y_k | Z, X_0=x).

The upper inequality drops observations from the conditioning. For the lower,
add the hidden boundary X_(k-r-1) to the complete observed past; given this
Markov state, older observations do not affect the future block. Summing gives
a finite-history interval. At m=0 the lower reduces to sum H(Y_k | X_(k-1)).
At m>=n-1 both bounds equal the exact finite-history entropy, since the boundary
is the known X_0 and every earlier observed coordinate is retained. More memory
tightens the lower as well as the upper: the more recent full hidden boundary
contains at least the predictive information of an older boundary plus the
intervening observation, by the same Markov separation argument.

Word operators P D_y1 ... P D_yr 1 give the joint observation law conditional on
each boundary state. The lower averages its conditional row entropy over the
actual boundary distribution. The upper mixes those rows before taking the
conditional entropy. Thus hidden correlations and observation memory stay in
the computation. An observed-Markov assumption is unnecessary.

The upper can also be capped by the complete full-state history entropy under
the same known root, because deterministic projection cannot increase entropy.
An injective projection has exactly that full-state value.

Implementation: `src/omega_cosmology/testbed/projections.py`, integrated as
optional `projected_histories` in `finite_study.py`. Observation coordinates,
known-full-present conditioning, cadence/horizon and model/generator hashes are
reported. Mixtures and own-present conditioning are explicitly rejected by this
assay entry point rather than being silently averaged. Full-present averaging
could be implemented by evaluating each known root separately and averaging
its intervals; this is different from an unobserved-root mixture.

The inequalities are analytic. Matrix/entropy operations use float64 and do not
produce rigorous numerical intervals. Any ranking must respect a validated
numerical tolerance as well as interval overlap. Word/workspace caps reject the
requested query instead of changing the grain, memory or horizon.

[Independent tests](../../tests/test_projection_bounds.py) compare all memory
depths against exhaustive finite hidden-Markov word laws, verify monotonic
tightening, lumpable and injective cases, constant projections, explicit caps,
and the typed shared-assay output. No large-horizon subject ranking is certified
solely because a short engineering smoke passes.
