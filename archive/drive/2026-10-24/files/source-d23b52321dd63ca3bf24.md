# Formal audit of the four new results — r1

**Date:** 16 October 2026.
**Requested by:** Sol (comments on the program review). Each new result needs
five things:
- exact assumptions;
- an exact statement;
- a proof;
- its scope;
- numerical checks, used only as verification.

**Audited:**
- the persistence result;
- the robustness floor;
- the thermal bounds;
- the risk identity.

All four come from the rate-first analysis r3.

**Where the full statements and proofs are:** Appendix A, sections A.3–A.5
(A_FORMAL_CORE_r1). This note records the verdicts and what changed.
**Verification:** `analysis/formal_audit/verify_appendix_a.py`, results in
`verify_appendix_a_results.json`. Checks V1–V9; every one passes.

## Verdicts

| Result (r3) | Verdict | Status in v4.1 | Appendix A |
|---|---|---|---|
| Persistence: ΔL(λ) ≈ Δr/λ + Δb | **Correct to leading order; the constant term was misstated.** Exact form found. Not new mathematics. | Theorem: established in dynamic programming, applied here | Theorems A.4.2–A.4.3, Corollary A.4.4 |
| Robustness floor: ε ≥ μ·\|Δb\| | **Correct to leading order.** The unexplained residual of about 20 bits is identified exactly. | Theorem (corollary of a proved identity) | Proposition A.4.5, Corollary A.4.6 |
| Thermal bounds and the long-shot threshold p ≤ L/(L + U_max) | **Correct as a conditional proposition, to first order in persistence.** Three premises are now named. The inequality must be strict. It unifies with v4's bounded-fanaticism result. | Conditional proposition | Proposition A.5.3, Corollary A.5.4 |
| Risk identity: ℓ(gamble) = h₂(p) + Σ pᵢℓᵢ | **Correct, but not new.** It is the chain rule, already present as v4's recorded-mixture result. It is extended to unrecorded outcomes, as a pair of bounds. | Theorem | Proposition A.5.1, Corollary A.5.2 |

## 1. The persistence result

**What r3 said.** When the differing laws relax at hazard λ,
ΔL(λ) ≈ Δr/λ + Δb.

**What is true.**

1. **The random-horizon identity (exact).** Take the rate–offset identity
   ℓ_n = nh + b − Kⁿb. It holds for every finite kernel, periodic and reducible
   ones included (V1). Taking its expectation over any horizon N independent of
   the development gives
   E[ℓ_N] = h·E[N] + b − E[K^N b] (V2). The last term is bounded by ‖b‖∞.
2. **The geometric horizon (exact).** With E[N] = m, the expected lushness is
   E[ℓ_N] = hm + b − Z(mI + Z)⁻¹b (V9). Expanding in 1/m gives
   E[ℓ_N] = hm + b − Zb/m + O(m⁻²). This is the Laurent expansion of discounted
   value (Blackwell 1962; Veinott 1969; Puterman 1994), proved in the appendix
   in a few lines.
3. **The constant term.** The engine's convention gives
   E[N] = (1 − λ)/λ = 1/λ − 1. So the correct first-order statement is
   ΔE[ℓ_N] = Δh/λ + (Δb − Δh) + O(λ). r3 dropped the −Δh term. It is
   negligible in every r3 case, where Δh ≤ 0.1 against |Δb| of thousands of
   bits, so no number in r3 changes. The convention-free statement is
   **ΔE[ℓ_N] = Δh·E[N] + Δb + O(1/E[N])**.
4. **The tie (new, sharper).** The options tie at an expected persistence
   E[N*] = T× − τ_b + O(1/T×), where τ_b = Δ(Zb)/Δb. τ_b is the mean time
   it takes for the offset difference to be realized. When that difference
   is realized through a single exponential mode, the tie is exactly T× − τ.
   - This explains r3's unexplained drift of λ*·T× up to 1.18. In every case,
     τ_b equals the case's transient time (V5):

     | Cases | τ_b |
     |---|---|
     | C1 and C5 (structure life) | 1,000 |
     | C2 (rebuild delay) | 100 and 1,000 |
     | C4 (rebuild time) | 100 and 10,000 |
   - The second-order error is below 0.6 steps in all nine cases.

**Status.** The mathematics is established; the reading for lushness is the
program's. In the manuscript the result is a theorem with sources, not a
discovery.

## 2. The robustness floor

**What r3 said.** A rate gain ε bought at a finite cost |Δb| is accepted if
ε ≥ μ·|Δb|, where 1/μ is the gain's expected persistence. The exact offsets
differed from ε/μ − |Δb| by "about 20 bits".

**What is true.**

1. **The window decomposition (exact; optional stopping).** The offset of a
   present equals two parts added together:
   - the excess branching, above the rate, accumulated before any stopping
     time τ with E[τ] < ∞;
   - the offset at τ.

   Exact to 1e-12 (V6).
2. **The floor (exact form).** For a gain held at excess ε until it ends at
   hazard μ,
   Δb = ε/μ − c + β, with β = h₂(μ)/μ − (h_F + ε).
3. **The residual explained.** β is the branching of the gain's own ending,
   about log₂(e/μ) bits, less one step of branching. It accounts for the
   r3 residual to within 10⁻⁵ bits (V6):

   | μ | Residual (bits) |
   |---|---|
   | 10⁻³ | 10.8 |
   | 10⁻⁴ | 14.2 |
   | 10⁻⁵ | 17.5 |
   | 10⁻⁶ | 20.8 |

   The ending of a gain is itself an uncertain event, and the measure counts
   it.
4. **The leading-order floor stands:** ε ≥ μ(c − β), and β grows only like
   log(1/μ).

**Status.** Theorem (proposition plus corollary).

**Scope.** Under uncertainty about μ, expected lushness uses the expected
life E[1/μ]. The model-error margin of ruling 22 is a decision-level layer,
not a theorem of the measure; the appendix says so.

## 3. The thermal bounds

**What r3 said.** In a world that relaxes into a shared thermal law with a
capped event rate, upside, downside and persistence are all bounded. A
gamble loses for every U ≤ U_max when p ≤ L/(L + U_max).

**What is true.**

1. **Three premises carry the result, now named:**
   - (F1) a finite repertoire at the declared grain, which caps every rate at
     log₂ M by the repertoire ceiling;
   - (F2) ruin leaves a residual process at rate r_th ≥ 0;
   - (F3) the options' differing regimes relax at a common hazard.

   These are physical hypotheses at the declared grain. The result holds
   given them; they are not proved.
2. **The statement, unified.** The gamble's advantage over a sure gain Δh ≥ 0
   is E[N]·[pu − (1 − p)d − Δh] + B, where |B| ≤ B̄. B̄ includes H(p) and the
   offsets, and does not grow with E[N]. So the gamble loses for every
   available upside whenever **p < (Δh + d)/(u_max + d)**, once E[N] exceeds
   a finite threshold.
   - With Δh = 0, this is r3's long-shot threshold.
   - With d = 0, it is v4's bounded-fanaticism result.
3. **Corrections to r3.**
   - The inequality must be strict. At equality with u = u_max the rates tie,
     and the offsets decide.
   - The result is first order in persistence. In the r3 model the exact tie
     probability is 0.1977 at E[N] = 9, 0.1900 at 99 and 0.18927 at 999,
     approaching 0.18919 with a correction of about 0.08/E[N] (V8).
4. **A nuance r3 did not state.** A higher thermal floor shrinks d, and so
   lowers the threshold. The more the residual process branches, the more ruin
   the measure tolerates.
5. **Margolus and Levitin (1998)** justify (F1) only when steps are physical
   time intervals and energy is bounded. No universal bound on branching is
   claimed.

**Status.** Conditional proposition.

## 4. The risk identity

**What r3 said.** ℓ(gamble) = h₂(p) + Σ pᵢℓᵢ, so the measure is
risk-neutral.

**What is true.**

1. **Recorded outcomes (exact).** When the outcome is recorded in the
   history, the identity holds exactly. It is the chain rule (Theorem A.2.1),
   and v4 already had it as the recorded-mixture result for the agent's own
   randomization.
2. **Unrecorded outcomes (new).** When the outcome is not recorded,
   H(X) = H(p) + Σ pᵢℓᵢ − H(I | X), so
   Σ pᵢℓᵢ ≤ H(X) ≤ H(p) + Σ pᵢℓᵢ (V7).
3. **Risk neutrality, stated precisely.**
   - In rate, the measure is exactly risk-neutral: the rate of a gamble is
     Σ pᵢhᵢ.
   - In total, it is risk-seeking by at most H(p) ≤ log₂ k bits, whatever the
     horizon.
   - Ruin is weighted by its size. An irreversible loss is large because it is
     permanent, not because its probability is inflated.

**Status.** Theorem.

## Consequences for working files

- **Rate-first analysis r3:** needs a short erratum, as an r4 or a note, not
  a rewrite.
  - Restate the persistence result with E[N], or add the −Δh term.
  - Add the τ_b explanation of the λ*·T× drift.
  - Add the β explanation of the 20-bit residual.
  - Make the long-shot inequality strict.
  - Credit the dynamic-programming literature.

  None of its verdicts change.
- **Ledger r10.** The four rows take the statuses above.
- **Not covered by this audit.** These are new claims that are not yet stated
  formally:
  - the subject bounds on marginal histories;
  - the persistence relation Δℓ ≈ −C + g·τ_up;
  - the counterfactual-access principle;
  - the policy-search correspondence with maximum occupancy.

  Each needs the same treatment before its chapter is drafted. The window
  decomposition (Proposition A.4.5) is the natural formal home for the
  persistence relation.

## References

- Blackwell, D. (1962). Discrete dynamic programming. *Annals of Mathematical
  Statistics* 33(2), 719–726.
- Margolus, N., and Levitin, L. B. (1998). The maximum speed of dynamical
  evolution. *Physica D* 120(1–2), 188–195.
- Puterman, M. L. (1994). *Markov Decision Processes: Discrete Stochastic
  Dynamic Programming.* New York: Wiley.
- Veinott, A. F. (1969). Discrete dynamic programming with sensitive discount
  optimality criteria. *Annals of Mathematical Statistics* 40, 1635–1660.
