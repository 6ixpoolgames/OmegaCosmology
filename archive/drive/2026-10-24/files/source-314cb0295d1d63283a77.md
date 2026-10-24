# 12 — Formal core

The chapters state their mathematics where the argument needs it, and their
formal notes give the definitions in full. This chapter collects the results on
which the argument depends and proves each of them once, in a single notation.
It adds no new claim. Where a chapter relies on a result, the result is here
with its assumptions stated; where a result belongs to the established
literature, it is stated with its source and the proof is outlined rather than
reproduced.

The chapter is organized in the order the argument uses the results: the
measure and its chain rule; why the measure is unique within its class; the
ceiling on branching; equilibrium, forgetting and the limit comparison; harm and
protection; cooperation and concentration; bounded comparison; decision and
correction; and the comparisons used in chapters 10 and 11. A final section
lists what the formal core does not yet contain.

---

## 12.1 Setting and notation

Unless stated otherwise, results concern a **finite classical model**: a finite
state space S and a stochastic kernel K on S, with K(x, y) the probability of a
step from x to y. Together S and K are the adapter of chapter 10, and the step
index carries the orientation. A **present** is a state x ∈ S, or a probability
distribution μ on S when the preparation is itself physically randomized.

The **history law** from x over n steps is

\[
P_x(x_1,\dots,x_n)=\prod_{t=0}^{n-1}K(x_t,x_{t+1}),\qquad x_0=x .
\]

The **step entropy** is g(x) = H(K(x, ·)) = −Σ_y K(x, y) log K(x, y). The **log
lushness** over n steps is ℓ_n(x) = H(P_x), and **lushness** is
L_x(n) = exp ℓ_n(x). Logarithms are taken to base 2 throughout, so entropies are
in bits and L_x(n) = 2^{ℓ_n(x)}. Kᵗg denotes the function
x ↦ Σ_y Kᵗ(x, y) g(y), and for a distribution μ, μg = Σ_y μ(y) g(y).

A **controlled model** has a family of kernels {K_a} indexed by actions a, with
step entropies g_a. Where a result needs time and resource accounting, it uses
the joint law of record, residual state, bill and elapsed time of formal note
F2.3; nothing below depends on more than the stated finite structure.

Quantum models are specified in formal note F1.1, and a decoherent history
family carries ordinary probabilities through the diagonal of its decoherence
functional (F1.4). Results proved here for classical models apply to such a
family once it is fixed. Section 12.10 states why fixing it is not innocent.

---

## 12.2 The chain rule and its consequences

### Theorem 1 (chain rule for lushness)

For a finite classical model and a present x,

> \[
> \ell_n(x)=\sum_{t=0}^{n-1}(K^tg)(x),\qquad
> \ell_{n+1}=g+K\ell_n,\qquad \ell_0=0 .
> \]
>
> *In words: log lushness is the expected branching of each step, summed over
> the horizon, and it can be computed one step at a time without enumerating
> the tree of histories.*

**Proof.** By the chain rule for entropy (Cover and Thomas 2006, Theorem 2.5.1),
H(X_1, …, X_n | X_0 = x) = Σ_{t=0}^{n−1} H(X_{t+1} | X_0 = x, X_1, …, X_t). By the
Markov property the t-th term equals H(X_{t+1} | X_t) under the law of X_t from
x, which is Σ_y Kᵗ(x, y) g(y) = (Kᵗg)(x). The recurrence follows by splitting
off the first step: ℓ_{n+1}(x) = g(x) + Σ_y K(x, y) ℓ_n(y). ∎

Three consequences are used repeatedly.

**Product rule.** If two processes evolve independently, the entropy of their
joint history is the sum of their separate entropies, so L_AB = L_A · L_B. For
a coupled joint law, H(A, B) = H(A) + H(B) − I(A; B), with I(A; B) ≥ 0 the
mutual information (Cover and Thomas 2006, Theorem 2.4.1).

**Absorbing outcomes.** A state y with K(y, y) = 1 has g(y) = 0. A development
absorbed into such a state keeps its weight and adds no further branching.

**Preparations.** For a randomized preparation μ, the complete joint entropy is
H_μ(X_0, …, X_n) = H(μ) + Σ_{t<n} μKᵗg, while the entropy conditional on the
starting state omits H(μ). A comparison must declare which it uses. From an
exact present the two coincide (formal note F11.1).

---

## 12.3 Why this measure

### Theorem 2 (uniqueness within the class)

Let H be defined on finite probability vectors and satisfy:

1. **symmetry**: H is unchanged by permuting the entries;
2. **continuity**: H(p, 1 − p) is continuous in p;
3. **grouping**:
   H(p_1, …, p_n) = H(p_1 + p_2, p_3, …, p_n)
   + (p_1 + p_2) H(p_1/(p_1 + p_2), p_2/(p_1 + p_2));
4. **normalization**: H(½, ½) = 1.

> \[
> H(p)=-\sum_i p_i\log_2p_i,\qquad L(\text{uniform on }N)=2^{\log_2N}=N .
> \]
>
> *In words: among measures that depend only on the weights of alternatives and
> give the same verdict whether a development is assessed whole or step by step,
> exactly one has the right calibration and continuity, and lushness is its
> exponential.*

**Source and outline.** The theorem is Faddeev's (1956), refining Shannon's
characterization (Shannon 1948) and Khinchin's (1957). The outline: grouping and
symmetry make F(n) = H(1/n, …, 1/n) additive on the positive integers,
F(mn) = F(m) + F(n); continuity of H(p, 1 − p) gives F(n + 1) − F(n) → 0; and an
additive function with that property is c·log n, so F(n) = log₂ n under the
normalization. Grouping then fixes H on vectors with rational entries, and
continuity extends it to all vectors. ∎

Two remarks fix the scope.

**Grouping fails for the alternatives.** The Rényi entropies
H_α(p) = (1 − α)⁻¹ log₂ Σ pᵢ^α, α ≠ 1, are additive for independent systems
(Rényi 1961) but do not satisfy grouping. For example, for p = (½, ¼, ¼),
H₂(p) = −log₂(0.375) = 1.415 bits, while grouping the last two entries gives
H₂(½, ½) + ½H₂(½, ½) = 1.5 bits. Applied to a history tree, the root assessment
and the probability-weighted assessment of its subtrees would disagree.

**The theorem does not choose the class.** That H depends on the probability
vector alone is part of the definition of the class. Similarity-sensitive
diversity of order one (Leinster and Cobbold 2012),
D^Z(p) = exp(−Σ pᵢ log(Zp)ᵢ) for a similarity matrix Z with unit diagonal, lies
outside it and reduces to exp H(p) when Z is the identity. Chapter 4 states the
choice of class as the program's.

---

## 12.4 The ceiling on branching

### Proposition 3 (repertoire ceiling)

With R(x) = {y : K(x, y) > 0} the set of states reachable in one step,

> \[
> g(x)\le\log_2\lvert R(x)\rvert,\qquad
> \ell_n(x)\le\sum_{t=0}^{n-1}\mathbb E_x\bigl[\log_2\lvert R(X_t)\rvert\bigr].
> \]
>
> *In words: a step cannot branch more than the logarithm of the number of states
> it can reach, and randomness can bring a process up to that ceiling but not
> beyond it.*

**Proof.** The entropy of a distribution supported on m points is at most
log₂ m, with equality exactly for the uniform distribution (Cover and Thomas
2006, Theorem 2.6.4). Applying this to K(x, ·) gives the first inequality;
summing its expectation along the development, by Theorem 1, gives the second.
∎

A change of K that leaves every R(x) unchanged can raise ℓ_n only up to this
bound. Raising the bound requires changing which states are visited, so that
later repertoires are larger, or changing R itself (formal note F3.2).

---

## 12.5 Equilibrium, forgetting and the limit comparison

Let π be a stationary distribution of K, so that πK = π, and define the excess
of a starting state over the equilibrium average,
Δℓ_n(x) = ℓ_n(x) − Σ_y π(y) ℓ_n(y).

### Theorem 4 (equilibrium identity)

> \[
> \sum_x\pi(x)\,\Delta\ell_n(x)=0\qquad\text{for every }n .
> \]
>
> *In words: averaged over equilibrium itself, the excess lushness of a starting
> state is exactly zero, so unless every state ties, some lie above the
> average.*

**Proof.** By Theorem 1, Δℓ_n(x) = Σ_{t<n} (δ_xKᵗ − π)g, where δ_x is the point
mass at x. Averaging over π gives Σ_{t<n} (πKᵗ − π)g = 0, since πKᵗ = π. ∎

The identity is a property of averages. The program's substantive claim, that a
specified organized state beats a properly matched stationary reference, is a
hypothesis (chapter 4) and is not proved here.

### Theorem 5 (finite forgetting and the lasting offset)

Suppose K is finite, irreducible and aperiodic. Then there are constants C < ∞
and 0 < r < 1 with sup_x ‖δ_xKᵗ − π‖_TV ≤ C rᵗ (Levin, Peres and Wilmer 2009,
Theorem 4.9), and

> \[
> \Delta\ell_n(x)\to c(x)=\sum_{t=0}^{\infty}(\delta_xK^t-\pi)g,\qquad
> \lvert\Delta\ell_n(x)-c(x)\rvert\le\frac{2C\,\lVert g\rVert_\infty\,r^n}{1-r}.
> \]
>
> *In words: in a closed finite system that forgets its starting point, a good
> start buys a fixed lasting offset, not a faster long-run rate.*

**Proof.** For distributions μ, ν and bounded g,
|μg − νg| ≤ 2‖μ − ν‖_TV ‖g‖_∞. Hence the t-th term of the series is bounded by
2C‖g‖_∞ rᵗ, the series converges absolutely, and the tail from n onwards is at
most 2C‖g‖_∞ rⁿ/(1 − r). ∎

It follows that ℓ_n(x) = n·πg + c(x) + O(rⁿ). The advantage of a good start over
a fresh window decays: |K^mℓ_n(x) − n·πg| ≤ 2C‖g‖_∞ r^m/(1 − r), because
K^mℓ_n(x) − n·πg = Σ_{t<n} (δ_xK^{m+t} − π)g. The constants depend on K and need
not stay bounded as the system grows, which is why forgetting times, and so the
size of attainable offsets, can be enormous.

### Proposition 6 (rate and offset in the limit)

For any finite kernel K the Cesàro limit Π = lim_n n⁻¹ Σ_{t<n} Kᵗ exists
(Kemeny and Snell 1960), and

> \[
> h(x)=\lim_{n\to\infty}\frac{\ell_n(x)}{n}
> =\sum_{C}P_x(\text{absorbed in }C)\,\pi_Cg ,
> \]
>
> where the sum runs over the closed communicating classes C reachable from x
> and π_C is the stationary law of C.
>
> *In words: the long-run rate of branching from a present is the average of the
> rates of the closed regions the development can settle into, weighted by the
> chance of settling in each.*

**Proof.** By Theorem 1, ℓ_n(x)/n = (n⁻¹ Σ_{t<n} Kᵗg)(x) → (Πg)(x). The rows of
Π are mixtures of the stationary laws of the closed classes, weighted by the
absorption probabilities from x; transient states carry no weight in Π. ∎

Within an aperiodic closed class, ℓ_n(x) − n h(x) converges to a finite offset
by Theorem 5; periodic classes give a bounded oscillation, and transient
excursions contribute a bounded amount because the expected number of visits to
transient states is finite.

**The comparison rule.** The program adopts the rule: compare long-run rates
first, then offsets (chapter 4). Where ℓ_n = n h + c + o(1) holds for both
developments and they differ in h or c, the rule coincides with the overtaking
criterion: a is preferred to b if ℓ_n^a > ℓ_n^b for all sufficiently large n
(von Weizsäcker 1965). Where offsets oscillate with overlapping ranges, the
overtaking criterion leaves the pair incomparable, and the rule must report
that rather than force a ranking. The rule is adopted, not proved; Proposition
6 shows only that the quantities it compares exist.

---

## 12.6 Harm and protection

### Corollary 7 (rate outweighs offset)

Let two developments satisfy ℓ_n^a − ℓ_n^b = nΔh + Δc + o(1) with Δh < 0. Then
for every finite c₀ there is N with ℓ_n^a − ℓ_n^b < −c₀ for all n ≥ N.

> \[
> \Delta h<0\ \Longrightarrow\ \ell_n^a-\ell_n^b\to-\infty .
> \]
>
> *In words: a harm that permanently lowers the rate eventually outweighs any harm
> whose cost is a finite offset.*

**Proof.** nΔh + Δc + o(1) → −∞ when Δh < 0. ∎

The corollary is stated in terms of rate and offset, not the words recoverable
and irreversible. In growing or non-stationary systems an irreversible change
need not lower the rate, and a recovered one need not leave a bounded deficit;
the categories must then be restated along the realized growth (formal note
F6.2). **Permanent recovery** into a recovered set C is entry into the largest
subset of C closed under the dynamics, and a first recovery with probability one
is compatible with permanent recovery of probability zero (F6.3).

### Proposition 8 (strict protection)

Let 𝓗 be a set of hypotheses about where value is realized, V_h(a) the realized
value of action a under h, and S* the conditions of valuing. Suppose the valued
end requires that some valuer exist and ranks the absence of all valuers lowest.

> \[
> V_h(d)\le V_h(a)\quad\text{for every }h\in\mathcal H
> \text{ and every }S^*\text{-preserving action }a .
> \]
>
> *In words: whichever hypothesis about value is true, destroying the conditions
> of valuing is never better than preserving them, so it is dominated without
> any probabilities over the hypotheses.*

**Proof.** Under any h, d produces a world without valuers, which the end ranks
lowest; so V_h(d) is the minimum value under h, and V_h(a) ≥ V_h(d). Strict
dominance holds wherever some S*-preserving action has positive value under
some h. ∎

The argument does not extend to a particular substructure P, since for a given P
there are in general hypotheses under which destroying it makes no difference to
the valued end. Ends that rank some world with valuers below a world without
them, as negative utilitarianism permits (Smart 1958), violate the ranking
condition and fall outside the proposition (chapter 5).

### Proposition 9 (precautionary protection)

Let d_P irreversibly destroy a particular structure P, let preservation cost a
finite offset c in log lushness, let p > 0 be the credence that a valued
development depends on P, and suppose that under that dependence d_P lowers the
long-run rate by Δh > 0.

> \[
> p\,(n\Delta h+O(1))>c\quad\text{for all }n>\frac{c}{p\,\Delta h}+O(1).
> \]
>
> *In words: for destruction that cannot be undone, even a modest credence that
> the destroyed structure matters comes to outweigh a bounded cost of preserving
> it, once the horizon is long enough to see the consequence.*

**Proof.** The expected loss from d_P is at least p times the rate loss
accumulated over n steps, by Corollary 7, and the inequality is linear in n. ∎

The conclusion holds within the furthest resolvable horizon n̄ only when n̄
exceeds the threshold, and it reverses when preserving P itself lowers the rate.
It is graded in p, Δh, c and n̄, and it does not apply to credences too small to
outweigh the largest physically available gain (Proposition 15).

---

## 12.7 Cooperation and concentration

### Proposition 10 (coupling at fixed marginals)

For processes A and B with fixed marginal history laws,

> \[
> H(A,B)=H(A)+H(B)-I(A;B)\le H(A)+H(B),
> \]
>
> with equality exactly under independence.
>
> *In words: coupling two processes while leaving each one's own breadth unchanged
> makes the whole narrower, so cooperation pays only by changing what the parties
> can reach.*

**Proof.** Mutual information is non-negative and vanishes exactly under
independence (Cover and Thomas 2006, Theorem 2.6.3). ∎

A gain in joint lushness from cooperation must therefore come from changes in
the marginal laws, enlarging the support or evening the weights of what each
process reaches, or from joint outcomes outside the product of the separate
supports (chapter 7).

### Proposition 11 (division and concentration)

Let a resource R > 0 be divided as r₁, …, r_N > 0 among independent processes,
each acting uniformly over f(rᵢ) transformations, and let φ = log₂ f. Joint log
lushness per step is Φ(r) = Σᵢ φ(rᵢ).

> \[
> \varphi\ \text{concave}\Rightarrow\Phi\text{ maximal at }r_i=R/N;\quad
> \varphi\ \text{linear}\Rightarrow\Phi\text{ constant};\quad
> \varphi\ \text{convex}\Rightarrow\Phi\text{ maximal under concentration}.
> \]
>
> *In words: whether sharing or concentrating a resource gives more breadth depends
> only on whether the logarithm of the returns bends down, stays straight or bends
> up.*

**Proof.** A sum of concave functions of the coordinates is Schur-concave and so
is maximized at the equal division, by Jensen's inequality; a sum of convex
functions is Schur-convex and is maximized at an extreme point of the simplex
(Marshall, Olkin and Arnold 2011). If φ is linear, Φ is linear with constant
sum. For f(r) = c·r^k with c, k > 0, φ(r) = log₂ c + k log₂ r is concave on
r > 0. Maximizing Φ is maximizing the product Π f(rᵢ), which is the Nash
product (Nash 1950) and, when f is throughput, proportional fairness (Kelly
1997). ∎

The proposition assumes independent processes and uniform repertoires; coupled
processes use Proposition 10.

---

## 12.8 Bounded comparison

### Proposition 12 (the unresolved remainder)

Let options a and b generate kernels K_a and K_b from a common present, with step
entropies g_a and g_b, and let Δ_n = ℓ_n^a − ℓ_n^b. For any n̄ < n,
Δ_n = Δ_{n̄} + Σ_{t=n̄}^{n−1} δ_t with δ_t = E_a[g_a(X_t)] − E_b[g_b(X_t)].

> \[
> \text{(i)}\ \Bigl\lvert\sum_{t\ge\bar n}\delta_t\Bigr\rvert
> \le\frac{4C\lVert g\rVert_\infty\,r^{\bar n-\tau}}{1-r};
> \qquad
> \text{(ii)}\ \sum_{t=\bar n}^{n-1}\delta_t=(n-\bar n)(h_a-h_b)+O(1).
> \]
>
> *In words: if after the act both options come under the same forgetting
> dynamics, what the agent cannot see is bounded; if the act's effects persist,
> what it cannot see grows with the horizon, with a sign fixed by the long-run
> effect it knows least well.*

**Proof.** The decomposition is Theorem 1 applied to each option. (i) Suppose
both options follow one finite, irreducible, aperiodic kernel K with step
entropy g after some τ ≤ n̄, and let μ_a, μ_b be their distributions at τ. Then
δ_t = (μ_aK^{t−τ} − μ_bK^{t−τ})g, and each of μ_aK^s and μ_bK^s lies within
C r^s of π in total variation, so |δ_t| ≤ 4C‖g‖_∞ r^{t−τ}; summing the
geometric tail gives the bound. (ii) If the options settle into closed classes
with rates h_a ≠ h_b, then δ_t → h_a − h_b with a summable error by Theorem 5,
which gives the stated form. ∎

The condition in (i) concerns the dynamics after the act, not whether the act
itself was reversible, and the bound is informative only with usable estimates
of C and r. Reversibility enters as an option: an act that can be undone gives
the agent a route from case (ii) back to case (i) once its effects are seen
(chapter 8).

### Proposition 13 (when removal is licensed)

In the model of formal note F8.2, with credence p that a process X is excisive,
probability r = q/(q + ε) that containment reads its type before it escapes,
host rate h_host and rate Δh_X lost by removing a generative X, removal beats
containment in the long-run comparison exactly when

> \[
> p\,(1-r)\,h_{\text{host}}>(1-p)\,\Delta h_X .
> \]
>
> *In words: remove only when the expected loss from an escape outweighs the
> expected loss from destroying something generative.*

**Proof.** By Proposition 6 the long-run rates are: removal h_host; containment
(1 − p)(h_host + Δh_X) + p·r·h_host, since an excisive X is removed if read in
time and otherwise consumes the host. Removal wins iff
h_host > (1 − p)(h_host + Δh_X) + p r h_host, which rearranges to the stated
condition. In the model h_host = 4 and Δh_X = 2 bits per step, and the
thresholds for ε = 0, 0.01 and 0.05 with q = 0.05 are never, p > 0.75 and
p > 0.5. ∎

---

## 12.9 Decision and correction

### Theorem 14 (the decision recursion)

For a finite controlled model with kernels {K_a} and step entropies g_a, define
V_0 = 0 and

> \[
> V_n(x)=\max_a\Bigl[g_a(x)+\sum_yK_a(x,y)\,V_{n-1}(y)\Bigr].
> \]
>
> Then V_n(x) is the largest log lushness over n steps attainable from x by any
> deterministic policy, and a policy that chooses a maximizing action at each
> state and number of remaining steps attains it.
>
> *In words: the value of the best choice now is the branching it produces at
> once plus the expected value of the best choices afterwards, and plans built
> this way remain best when judged again from any state they reach.*

**Proof.** By induction on n. For any deterministic policy σ, possibly depending
on the history, the action at the root is fixed, say a, and the chain rule gives
ℓ_n^σ(x) = g_a(x) + Σ_y K_a(x, y) ℓ_{n−1}^{σ_y}(y), where σ_y is the policy σ
continues with after reaching y. By the inductive hypothesis
ℓ_{n−1}^{σ_y}(y) ≤ V_{n−1}(y), so ℓ_n^σ(x) ≤ V_n(x), with equality for the
maximizing policy. Time consistency is Bellman's principle of optimality
(Bellman 1957). ∎

A policy that randomizes adds the branching of its randomizing device, which
the recursion counts as part of the action. Under uncertainty about which of
finitely many kernels holds, with credence b updated by observations generated
by the true kernel, the recursion over beliefs of section 9.3 is the optimality
equation for expected log lushness; each possible kernel keeps its own history
law, so uncertainty enters the comparison and not the measure. The results
assume independent choice of action at every state; comparisons under the
latest-divergence matching rule need not satisfy that assumption (chapter 9).

**Conditioning is not intervention.** With Z ∼ Bernoulli(½), P(C = Z) = 0.9 and
Y = Z, P(Y = 1 | C = 1) = 0.45/0.5 = 0.9, while setting C = 1 by an actuator
leaves P(Y = 1) = 0.5 (Pearl 2009). The decision recursion compares implemented
actions, never conditioned ones.

### Proposition 15 (bounded fanaticism)

Let a certain option raise the long-run rate by Δh > 0, and a gamble raise it by
at most G_max with probability p and by at most zero otherwise.

> \[
> p\,G_{\max}<\Delta h\ \Longrightarrow\ \text{the gamble loses},\qquad
> G_{\max}\le\log_2M .
> \]
>
> *In words: where the gain a gamble could bring is bounded, as it is for any
> finite system, a small enough probability cannot win however much the gamble
> promises.*

**Proof.** Under the rate-first comparison the gamble's expected rate gain is at
most p·G_max, which is less than Δh. For a finite classical system with at most
M distinguishable states, g(x) ≤ log₂|R(x)| ≤ log₂ M by Proposition 3, so no
rate exceeds log₂ M. ∎

No extension to the universal continuation is claimed. Holographic bounds
concern the information associated with specified regions and surfaces; a
universal ceiling on the branching rate would require fixing clock, region,
growth and quantum description (chapter 9). The bound caps the weight of small
probabilities and does not certify probabilities above the cap.

### Proposition 16 (requisite variety and the thin model)

Let disturbances D, responses R and outcomes O = f(D, R) satisfy, for every
response r, that d ↦ f(d, r) is injective. Then H(O) ≥ H(D) − H(R) (Ashby 1956).
If D = (D₁, D₂) and the regulator's response depends only on what it models,
R = f(D₁), and d₂ ↦ φ(d₁, d₂, r) is injective for every d₁ and r, then

> \[
> H(O\mid D_1)\ \ge\ H(D_2\mid D_1).
> \]
>
> *In words: under the stated condition, whatever variety a regulator's model
> misses passes into its outcomes, so holding outcomes in a target requires
> accommodating that variety or suppressing it.*

**Proof.** For Ashby's inequality: injectivity in each column gives
H(D | R, O) = 0, so H(D | R) = I(D; O | R) ≤ H(O | R) ≤ H(O), and
H(D) ≤ H(R) + H(D | R). For the thin model: for each value of D₁ the response is
fixed and O determines D₂, so H(O | D₁ = d₁) ≥ H(D₂ | D₁ = d₁); average over D₁. ∎

The injectivity condition is necessary. Without it, shielding, buffering or
redundancy can make several disturbances produce the same outcome, which is
accommodation; changing the law of D₂ is suppression (formal note F9.4). The good
regulator theorem (Conant and Ashby 1970) is cited, not proved here.

### Proposition 17 (deference)

In the decision model of formal note F9.6, with gain a, persisting harm b,
correctable harm b_c, overseer accuracy α, delay c, and credence p that the
system's model is right:

> \[
> \text{act}\succ\text{defer}\iff p>\frac{\alpha b-c}{\alpha b+(1-\alpha)a},
> \qquad
> \text{keep}-\text{disable}=(1-p)(b-b_c)-k .
> \]
>
> *In words: where harm would persist, a system should defer unless its confidence
> is high, and a channel of correction is worth keeping by the expected harm it
> converts from persisting to repairable, minus what it costs.*

**Proof.** Acting with oversight disabled yields pa − (1 − p)b, and deferring
yields pαa − (1 − p)(1 − α)b − c. The first exceeds the second iff
p[a(1 − α) + αb] > αb − c. Keeping a channel that costs k yields
pa − (1 − p)b_c − k against pa − (1 − p)b for disabling it. ∎

With a = b = 1,000, b_c = c = 10 bits, the thresholds are 0.89 for α = 0.9 and
0.59 for α = 0.6. The gains and losses in this model are stipulated net
consequences, not a lushness calculation over complete histories.

### Proposition 18 (coherence of plan revision)

Let ≻ be a strict, transitive, irreflexive preference over complete plans, with
pure resource loss strictly worse. If each revision P_i → P_{i+1} satisfies
P_{i+1} ≻ P_i, no finite sequence of revisions returns to P_0 with an added loss
L.

> \[
> P_0\oplus L\prec P_0\prec P_k\quad\text{for every }k\ge1 .
> \]
>
> *In words: an agent that revises a fixed evaluation only to strictly better
> plans cannot be led around a cycle that leaves it worse off.*

**Proof.** Transitivity gives P_k ≻ P_0, and P_0 ≻ P_0 ⊕ L by assumption, so
P_k ≠ P_0 ⊕ L by irreflexivity. ∎

The result assumes the evaluation is fixed across revisions; plans that include
learning need a further analysis.

---

## 12.10 Comparisons for chapters 10 and 11

### Proposition 19 (the matched-reference criterion)

For preparations μ (organized) and ν (reference) under a common finite law K,
using entropy conditional on the starting state,

> \[
> \ell_T(\mu)-\ell_T(\nu)=\sum_{t=0}^{T-1}\bigl(\mu K^tg-\nu K^tg\bigr).
> \]
>
> If K is irreducible and aperiodic, the difference converges to a finite limit.
>
> *In words: an organized preparation beats its matched reference exactly when the
> states it leads to branch more, summed over the horizon; under a common law that
> forgets, it can buy only a lasting offset.*

**Proof.** The identity is Theorem 1 applied to each preparation. Convergence
follows as in Theorem 5, since μKᵗ and νKᵗ approach π geometrically. ∎

A different long-run rate requires escape from these conditions: different
closed classes under a fixed law, a growing state space or a law that is not
time-homogeneous, each declared and resource-accounted. Matching ℓ_T itself in
advance makes the comparison vacuous; what is matched must be the inputs
(chapter 11).

### Proposition 20 (matched transients)

Let A and B be preparations under the same Markov law, with
ℓ_k(·) = log₂ L(k). If P_A(X_m) = P_B(X_m), then

> \[
> \ell_{m+n}(A)-\ell_{m+n}(B)=\ell_m(A)-\ell_m(B)\qquad\text{for every }n .
> \]
>
> *In words: once two developments reach the same distribution over states, their
> lushness never separates further, whatever they passed through on the way.*

**Proof.** By the chain rule and the Markov property,
ℓ_{m+n}(A) = ℓ_m(A) + Σ_y P_A(X_m = y) λ_n(y), with λ_n(y) the log lushness of n
further steps from y, and likewise for B. The second terms coincide when the
distributions do. ∎

If the distributions at m differ by total variation ε, the second terms differ
by at most ε·max_y λ_n(y), since λ_n ≥ 0, and the conclusion is approximate, at
a rate set by how quickly the residual difference decays (formal note F10.4).

### Proposition 21 (recorded mixture of policies)

Let a recorded random choice select policy A with probability q and policy B
otherwise, with log lushness ℓ_A and ℓ_B over the horizon. Then

> \[
> \ell_{\text{mix}}(q)=h_2(q)+q\,\ell_A+(1-q)\,\ell_B,\qquad
> \max_q\ell_{\text{mix}}=\log_2\bigl(2^{\ell_A}+2^{\ell_B}\bigr),
> \]
>
> attained at q* = L_A/(L_A + L_B), where h₂ is the binary entropy.
>
> *In words: randomizing between two policies adds at most about one bit when they
> are close, and almost nothing when one is far better, so a mixture cannot rescue
> a much worse policy.*

**Proof.** The chain rule splits the entropy of (choice, history) into the
entropy of the choice plus the expected entropy of the history given the
choice. ℓ_mix is concave in q, and its derivative log₂((1 − q)/q) + ℓ_A − ℓ_B
vanishes at q*; substituting gives log₂(L_A + L_B). ∎

The gain over the better fixed policy is log₂(1 + 2^{−|ℓ_A − ℓ_B|}). For an
equal-weight mixture, ℓ_mix(½) = 1 + ½(ℓ_A + ℓ_B), which loses to the better
policy exactly when |ℓ_A − ℓ_B| > 2. The result requires the choice to be
recorded; an unrecorded choice whose alternatives interfere combines at the
level of amplitudes (chapter 1).

### Proposition 22 (family dependence of quantum breadth)

Let an idle qubit have Hamiltonian zero and state ρ = |0⟩⟨0|, and consider
single-time projective families in the Z and X bases. Both are decoherent, with

> \[
> D_Z=\operatorname{diag}(1,0),\qquad D_X=\operatorname{diag}(\tfrac12,\tfrac12),
> \qquad \exp H(\operatorname{diag}D_Z)=1,\quad \exp H(\operatorname{diag}D_X)=2 .
> \]
>
> *In words: the same quantum state has breadth 1 under one question and 2 under
> another, so no single number can agree with classical lushness on every
> decoherent family while ignoring which family was chosen.*

**Proof.** A single-time family is trivially decoherent, since distinct
orthogonal projectors at one time give D_{αβ} = Tr(P_α ρ P_β) = 0 for α ≠ β. The
diagonals are ⟨0|P_α|0⟩, which are (1, 0) in the Z basis and (½, ½) in the X
basis. ∎

A quantum lushness therefore needs a physical rule for selecting the family,
such as actual record formation, or an explicit dependence on the realized
interface. This is the set-selection problem of decoherent histories (Dowker and
Kent 1996; Gell-Mann and Hartle 1993), and chapter 4 states the requirements a
construction must meet.

---

## 12.11 What the formal core does not contain

The results above are proved under their stated assumptions. Several things the
argument needs are not among them, and they are listed so that no reader
mistakes their absence for an oversight.

- **The central wager.** No theorem shows that greater lushness is better, or
  that the breadth that dominates is generative rather than pathological. That
  is decided by adversarial search (chapters 5 and 11).
- **Organization against matched references.** Proposition 19 states when an
  organized preparation wins; no theorem yet derives that any class of physical
  arrangements makes the sum positive (chapter 11).
- **The cross-scale conjecture.** That organization nested across scales
  extracts more lushness from a gradient than organization confined to one scale
  is a hypothesis with a stated route, not a result (chapters 8 and 11).
- **A single ranking across resolutions.** Results are stated at a declared
  resolution; dominance across resolutions is a research target (chapter 4).
- **A quantum construction.** Proposition 22 is an obstruction, not a
  construction (chapter 4).
- **A justified matching rule.** The latest-divergence rule for comparing
  alternatives that differ in earlier architecture is a candidate, and its
  interface with Theorem 14 is unformalized (chapter 9).
- **Estimators with error bounds.** Every number in the manuscript is computed
  exactly or to stated precision in a small model; no estimator for realistic
  systems is analysed here (chapter 11).
- **A universal bound on branching.** Proposition 15 holds for finite systems
  only (chapter 9).

---

## Status

| Status | Claims in this chapter |
| --- | --- |
| **Established elsewhere** | The entropy chain rule and the non-negativity of mutual information. Faddeev's characterization of Shannon entropy. Geometric convergence of finite irreducible aperiodic chains. Existence of the Cesàro limit for finite chains. Schur-concavity of separable concave sums. Bellman's principle of optimality. Ashby's law of requisite variety, under its injectivity condition. The good regulator theorem. |
| **Proved here, under stated assumptions** | The lushness recurrence. The repertoire ceiling. The equilibrium identity. The lasting offset and its bound. The rate formula in the limit. Rate outweighs offset. Strict and precautionary protection. Coupling at fixed marginals. Division and concentration. The unresolved remainder. The removal and deference thresholds. The decision recursion. Bounded fanaticism for finite systems. The thin-model bound. Coherence of plan revision. The matched-reference criterion. Matched transients. The recorded mixture bound. Family dependence of decoherent breadth. |
| **Adopted** | The class of weight-only measures with the grouping rule. Rate-then-offset as the comparison rule. |
| **Not proved** | The items of section 12.11. |

---

## References cited in this chapter

*Collected with full details in chapter 13.*

- Ashby, W. R. (1956). *An Introduction to Cybernetics.* London: Chapman & Hall.
- Bellman, R. (1957). *Dynamic Programming.* Princeton: Princeton University
  Press.
- Conant, R. C., and Ashby, W. R. (1970). Every good regulator of a system must
  be a model of that system. *International Journal of Systems Science* 1(2),
  89–97.
- Cover, T. M., and Thomas, J. A. (2006). *Elements of Information Theory* (2nd
  ed.). Hoboken: Wiley.
- Dowker, F., and Kent, A. (1996). On the consistent histories approach to
  quantum mechanics. *Journal of Statistical Physics* 82(5–6), 1575–1646.
- Faddeev, D. K. (1956). On the concept of entropy of a finite probabilistic
  scheme. *Uspekhi Matematicheskikh Nauk* 11(1), 227–231. (In Russian.)
- Gell-Mann, M., and Hartle, J. B. (1993). Classical equations for quantum
  systems. *Physical Review D* 47(8), 3345–3382.
- Kelly, F. P. (1997). Charging and rate control for elastic traffic. *European
  Transactions on Telecommunications* 8(1), 33–37.
- Kemeny, J. G., and Snell, J. L. (1960). *Finite Markov Chains.* Princeton, NJ:
  Van Nostrand.
- Khinchin, A. I. (1957). *Mathematical Foundations of Information Theory.* New
  York: Dover.
- Leinster, T., and Cobbold, C. A. (2012). Measuring diversity: the importance
  of species similarity. *Ecology* 93(3), 477–489.
- Levin, D. A., Peres, Y., and Wilmer, E. L. (2009). *Markov Chains and Mixing
  Times.* Providence: American Mathematical Society.
- Marshall, A. W., Olkin, I., and Arnold, B. C. (2011). *Inequalities: Theory of
  Majorization and Its Applications* (2nd ed.). New York: Springer.
- Nash, J. F. (1950). The bargaining problem. *Econometrica* 18(2), 155–162.
- Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.).
  Cambridge: Cambridge University Press.
- Rényi, A. (1961). On measures of entropy and information. In *Proceedings of
  the Fourth Berkeley Symposium on Mathematical Statistics and Probability*,
  vol. 1, 547–561. Berkeley: University of California Press.
- Shannon, C. E. (1948). A mathematical theory of communication. *Bell System
  Technical Journal* 27, 379–423 and 623–656.
- Smart, R. N. (1958). Negative utilitarianism. *Mind* 67(268), 542–543.
- von Weizsäcker, C. C. (1965). Existence of optimal programs of accumulation
  for an infinite time horizon. *Review of Economic Studies* 32(2), 85–104.
