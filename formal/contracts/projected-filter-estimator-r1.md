# Predictive-entropy filtering estimator

25 October 2026. Classical finite hidden-Markov projection, known full present.
This is an analysis method, not a new physical law, objective or record grain.

For Y=f(X), let b_k be the exact filtering distribution of X_k given the observed
prefix and the known full root. The distribution of the next observation is
q_k(y)=sum_i,j b_k(i) P_ij 1[f(j)=y]. Update b by ordinary conditioning on the
drawn next observation. Then the chain rule gives

H(Y_1,...,Y_n | X_0=x) = E[sum_(k=0)^(n-1) H(q_k)].

The estimator samples independent observation histories and averages this
predictive-entropy sum. It does not forget the prefix, assume the projection is
Markov, sample a fictitious prior over policies, or add the sampling randomness
to the physical entropy. The filtering belief is analysis memory, not a scored
state. A passive projection needs no physical sensor in the law.

Two laws can share iid uniforms to couple their observation draws. Each law's
marginal is unchanged. Candidate-minus-reference is estimated from paired path
sums, retaining the covariance. Independent paths, not individual timesteps,
are the observations used to calculate standard errors. State enumeration and
hidden-block padding are bookkeeping only; padding has probability zero.

An optional control variate uses g_k(y)=H(Y_(k+1)|Y_k=y,X0), whose unconditional
mean is computed exactly from the propagated full distribution. For each path
let G=sum g_k(Y_k) and U=E[G]. Replace the path sum Z by Z-G+U. Its expectation
is still H(Y_1,...,Y_n|X0), regardless of how far the memory1 approximation is
from the full-history law. The fixed coefficient is1, never fitted to obtain a
desired sign. The full-history filter remains in Z; it is not replaced by G.
This subtracts estimation noise and restores its known mean, not physical
entropy. The implementation reports both controlled and raw standard errors;
variance reduction is not guaranteed for every law.

## Uncertainty

The paired mean is unbiased under exact kernels/filtering and ideal iid draws.
The paired Student t interval uses the sample variance of independent paired
path sums. Its coverage is approximate; small variance, a favorable sign or
short-reference agreement does not establish rigorous long-horizon coverage.
No sign selected by this interval is called an analytically resolved ranking.
Intervals are pointwise per horizon, not simultaneous across a report.

Each path sum lies in [0,n log2(M)], for M observable values. The paired
difference lies in [-n log2(M),n log2(M)]. A distribution-free Hoeffding interval
therefore has radius

2 n log2(M) sqrt(log(2/alpha)/(2N)).

It is intentionally also reported, even when far too wide to decide anything.
With the optional control, each residual Z-G is in [-n log2(M),n log2(M)], so
the paired range is4 n log2(M), and the Hoeffding radius doubles. The known
mean shift is deterministic. Uncontrolled and controlled intervals are distinct.
These statistical bounds assume ideal samples and exact arithmetic; float64
and pseudorandom evaluation is not rigorous interval arithmetic. Analytic
observation-memory bounds remain independent retained evidence. Do not insert
an approximate interval into their `lower_bits`/`upper_bits` schema.

Sample count, seed, batch size, horizons, scopes and confidence are declared
before each run. No stopping when an interval first becomes favorable. A later
larger sample is a separate documented refinement; do not pool selectively or
count repeated seeded runs as independent replication.

## Validation and resource limits

[Reference tests](../../tests/test_filtering.py) independently enumerate a tiny
non-Markov observation law and sum all filter branches to verify the expectation
identity. They check paired cancellation for identical laws, permutations,
reproducible seeds, exact small-world differences, conditioning and caps.
Before interpreting E1 estimates, compare short actual E1 histories against
full-prefix exact values and profile a declared small sampling job.

The implementation uses dense small sampled kernels and observation-indexed
hidden blocks. Predeclared workspace and sample-step caps reject requests;
they never prune low-probability physical transitions, lower the scientific
horizon or change the represented state grain. Known-root mixtures, own-present
conditioning, arbitrary huge hidden blocks and quantum histories remain outside
this adapter. Rate estimates and irreversible closure are not implemented here.

Code: `src/omega_cosmology/testbed/filtering.py`; capped frozen runner:
`scripts/run_projection_filter.py`.
