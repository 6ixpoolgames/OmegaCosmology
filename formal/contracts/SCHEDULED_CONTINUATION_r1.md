# Finite scheduled continuation contract

26 October 2026. Classical finite engineering extension of complete conditional
history entropy (Appendix A r19 A.1 and chain rule A.2.1). This is not a claim of
conformance to an unavailable later Appendix A revision.

Let a prescribed deterministic boundary schedule select native generators Q_j
on one common physical state space, with unchanged Hamiltonian and inventory.
Let each interval at the declared cadence lie inside one phase. Its transition
kernel is P_k = exp(cadence Q_j). From a known full root x_0,

    H(X_1,...,X_n | X_0=x_0, schedule)
      = sum_{k=1}^n sum_x Pr(X_{k-1}=x | x_0,schedule) H(P_k(x,.)),
    mu_k = mu_{k-1} P_k.

No term for selecting the schedule is included: no prior over commands was
introduced. No boundary root is re-selected. A phase boundary is an ordinary
sample, with no duplicate state or reset. H(mu_n) is endpoint entropy and cannot
replace the complete-history expression. Phase durations that do not align with
cadence are rejected in this implementation; a composed within-interval kernel
requires a separate explicit observation contract.

The schedule is an exterior prescription. The modeled state is sufficient for
the time-dependent law once that prescription is given; it is not asserted to
be an autonomous stationary Markov system. If a controller selects the schedule
internally, its registers, sensing, bills and transitions must enter the native
model. A Hamiltonian switch requires a quench-work adapter and is rejected here.

For Y_k = projection(X_k), the projected process need not be Markov. The existing
memory bounds extend to nonhomogeneous kernels: at step k, let L=min(m+1,k),
Z=X_{k-L}, and W=(Y_{k-L+1},...,Y_{k-1}). Then

    H(Y_k | W,Z,schedule) <= H(Y_k | Y_1,...,Y_{k-1},x_0,schedule)
                         <= H(Y_k | W,x_0,schedule).

The first inequality uses conditional independence of the past before Z and the
future after Z under the declared Markov law; the second drops conditioning.
The window operators multiply the actual chronological kernels, including a
window straddling the switch. The hidden-boundary distribution is propagated
from the original root. Summing independent restarted projection entropies is
not this calculation. The implemented inequalities use float64 arithmetic,
not rigorous interval certificates.

Continuous occupation composes independently through the phases. For fixed
energy E, the first law telescopes without a boundary impulse:

    E[ E(X_T)-E(X_0) ] = expected net work - exported heat.

Physical state-changing event counts sum over the native ledger. Parallel
channels with the same represented target are aggregated in Q for history
entropy and the finite coefficient F; their mechanism labels are not additional
observed alternatives. Nbar and F sum over the occupations of each phase and
are fine-cadence diagnostics only. Matching Nbar and gross accepted work at one
horizon does not match event ordering, timing, correlations or projected paths.

The finite scheduled profile has no stationary generator. A common irreducible
recovery phase of unlimited duration would eventually impose its common entropy
rate; the finite pulse can leave an offset. No rate is substituted for the
finite profile in this engineering assay.

Executable checks: `tests/test_phases.py`, especially explicit history-word
enumeration, cross-boundary projection bounds, unchanged-law split invariance,
common state order, quench rejection and native energy/monitor marginal checks.
