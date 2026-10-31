# Finite full-state profiles and independent endings

30 October 2026. An implemented finite classical contract, not a declaration
of conformance to an unavailable newer Appendix A.

For a finite stochastic matrix P and row-entropy reward g, let Pi be its
ergodic projector (the Cesaro limit). Set r = Pi g and normalize the Poisson
bias b by Pi b = 0:

    (I - P)b = g - r.

For a known initial root or an average of individually known roots mu, the
complete conditional sampled-history entropy satisfies exactly in real
arithmetic:

    ell_n = sum_(k=0)^(n-1) mu P^k g
          = n mu r + mu b - mu P^n b.

The second equality telescopes and uses Pr = r. It applies to reducible and
periodic finite kernels. It does not imply convergence of the remainder for
a periodic chain. Mixture uncertainty in an unobserved initial state is not
silently included. Projected histories generally have memory, so a quotient
Markov kernel is not an implementation of this contract for those histories.

For a contrast of profiles with coefficients c_j, let Delta r and Delta b be
the corresponding initial-state averages and M = sum_j |c_j| ||b_j||_infinity.
Then

    |Delta ell_n - n Delta r - Delta b| <= M.

If Delta r > 0, n Delta r + Delta b > M suffices for positive difference at
that and every later horizon. The analogous condition holds with reversed
sign. This is an eventual bound, not proof of a single crossing. Earlier
steps must also be checked for an all-horizon claim. Delta r = 0 requires
separate tail reasoning; equality of rate and bias need not mean equal profiles.

For an independent ending N on nonnegative integers with finite mean,

    E[ell_N] = E[N] mu r + mu b - mu E[P^N]b.

For geometric N with mean m, rho = m/(m+1) and

    E[P^N] = (1-rho)(I-rho P)^(-1),
    E[ell_N] = rho mu (I-rho P)^(-1)g.

The remainder magnitude is bounded by ||b||_infinity. A uniform ending on
0,...,L replaces E[P^N] by the mean of the first L+1 matrix powers. Physical
duration is n times cadence; holding expected duration fixed requires scaling
the mean number of steps with cadence.

Profile dominance over the support of an independent ending distribution
implies dominance of E[ell_N]. Strictness requires positive mass on a horizon
where the gap is strict. An equal endpoint alone proves neither dominance nor
strictness. Random stopping is not a license to use ell_(E[N]) or E[2^ell_N].

For pre-transition, state-dependent stopping probability h_i, let
K = diag(1-h)P and require eventual stopping. The expected transition
surprisal is mu (I-K)^(-1) diag(1-h)g. Entropy of the stopped record, which
includes termination, additionally contains mu (I-K)^(-1) H_binary(h).
These are distinct from applying an independent-ending law to an unchanged
process. State-dependent stopping changes the selected development law.

Implementation: [profile_analysis.py](../../src/omega_cosmology/testbed/profile_analysis.py).
Independent reference tests: [test_profile_analysis.py](../../tests/test_profile_analysis.py).
All implementation values are float64 equation checks, not verified rounding
enclosures. Structural support for CTMC inputs comes from the native graph;
underflowed matrix entries do not define impossibility. Synthetic discrete
reference kernels do not claim thermodynamic embodiment or normative status.
