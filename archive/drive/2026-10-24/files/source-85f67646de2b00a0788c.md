# 4 — Lushness

Chapters 1 to 3 described an object and a mechanism: the physical possibility
structure, the access it supports from each present, and the organization that
changes that access. This chapter supplies the measure. **Lushness** is the
effective breadth of the futuresfield: how many distinct futures a present
supports, each weighted by its probability.

The chapter has five tasks. It defines lushness and shows how organization
enters it. It shows that lushness is the unique measure meeting the framework's
own requirements. It settles which horizon the comparison should use. It states
what lushness can and cannot see, including at the quantum level. And it works
five exact examples, so that the claims of chapter 3 become measurable rather
than merely compatible with the measure.

One distinction runs through all of it. The structure is the object; lushness is
its magnitude, not a representation of it. Two structures can have the same
lushness and differ in every other respect. The structure carries the explanation of
what happens; lushness carries the verdict on how much is supported. Which
structural configurations raise lushness, and there will be many, is what the
program studies.

---

## 4.1 Definition

For a classical development described at a stated resolution, lushness is the
exponentiated entropy of complete future histories.

> **Lushness**
>
> \[
> L_x(n)=\exp H(p_x),\qquad H(p)=-\sum_h p(h)\log p(h)
> \]
>
> p_x is the probability distribution over complete histories h of length n
> starting from state x. H is its Shannon entropy, the standard measure of how
> widely probability is spread. Exponentiating turns entropy into an effective
> number of futures.

The calibration is easy to check:

- N equally likely futures give L = N.
- n independent fair binary events give 2ⁿ, although the probabilities sum to
  one.
- A certain future gives 1.
- Weights (0.9, 0.05, 0.05) give about 1.48: three possibilities, effectively
  fewer than two.

Lushness is neither a count of possibilities nor a measure of probability. A
development with a million possible futures, nearly all of whose weight falls on
one, has lushness close to one. Support and weight are both in the definition.
In ecology the same quantity is the Hill number of order one, used to measure
the effective diversity of a community (Hill 1973; Jost 2006). In language
modelling it is the perplexity of a predictive distribution (Jelinek et al.
1977).

Everything counts. Construction and collapse, cooperation and competition,
success and failure, organization and noise all contribute their branches. The
measure does not decide in advance which developments matter. That is what
allows it to judge between them, and it is also what exposes it to the tests of
section 4.9.

### Independent and coupled systems

For independent systems, lushness multiplies: L_AB = L_A · L_B, because the
entropies of independent histories add. Coupled systems use their actual joint
law. Shared resources, correlations and interactions change both the parts and
the whole, and composition is represented in that joint law rather than by any
added term.

One consequence matters for the ethics. Independent copies of a stochastic
process multiply lushness exactly as independent processes of different kinds
with the same breadth do. Under lushness, plurality is not valuable because
variety is valuable in itself. It is valuable through interaction: complementary
processes opening joint transformations that copies cannot.

---

## 4.2 How organization enters

The chain rule of information theory (Cover and Thomas 2006) decomposes the entropy of a whole history
into the entropy of each step, given what came before. For a Markov process this
gives a direct formula.

> **How organization enters**
>
> \[
> \log L_x(n)=\sum_{t=0}^{n-1}(K^tg)(x),\qquad
> g(x)=-\sum_y K(x,y)\log K(x,y)
> \]
>
> g(x) is the branching of the next step from state x: one-step access,
> measured as effective branching (section 2.10). Kᵗg(x) is its expected value t
> steps ahead. Log lushness is the sum of expected branching over the horizon.

The present configuration sets the first term; the dynamics decide which
configurations, and therefore which branching, come next. Catalysis,
construction, damage and repair all change lushness through this sum and in no
other way. There is no bonus for organization and no penalty for cost. A route
that consumes resources leaves a residual state with less available, and that
state branches less afterwards. Costs register through what they use up.

The formula also makes chapter 3's repertoire ceiling quantitative. Since
g(x) ≤ log|R(x)|, where R(x) is the set of states reachable from x in one step,
lushness is bounded by the logarithms of the repertoires the dynamics visit.
Noise can bring g(x) up to that bound. Only changing which states are visited,
or enlarging R itself, can raise it.

---

## 4.3 Why this measure

Comparing states of the structure by magnitude requires a measure. There are
many candidates: free energy, number of organisms, number of reachable states,
or variants of entropy. Two commitments the framework already holds narrow the
choice to one.

**Impartiality.** The measure may depend only on the weights of the alternatives,
not on what the alternatives are. Relabelling futures cannot change it. No kind
of thing and no recipient is privileged.

**Consistency over time.** All assessment is from a present (chapter 2).
Assessing a development whole, from its root, must therefore agree with
assessing it step by step: first the branching at the root, then the expected
branching from each successor, weighted by its probability. This is precisely
the chain rule, sometimes called the grouping property.

Add two natural requirements: N equally weighted alternatives count as N, and
small changes in the weights produce small changes in the measure.

Shannon's characterization of entropy (Shannon 1948), made rigorous by Khinchin
(1957) and by Faddeev (1956), shows that exactly one function satisfies symmetry, continuity, grouping and a
normalization: Shannon entropy. Exponentiating it gives the calibration to an
effective count. Other entropy-like measures — the Rényi family (Rényi 1961), for example —
are additive for independent systems but fail the full grouping property. They
would make the verdict from a root disagree with the verdict assembled from its
successors, which is exactly the inconsistency the framework's present-rooted
assessment rules out.

Lushness is therefore not chosen. It is the unique measure meeting the
framework's own requirements. The result is conditional in the honest sense: a
reader who rejects impartiality or consistency over time can reject the measure.
What the theorem establishes is what follows from accepting them.

---

## 4.4 What lushness sees

Because lushness is a magnitude rather than a representation, a natural worry
is that it discards the structure chapters 1 to 3 insisted on: joint
correlations, composition, residual states, latent capabilities.

It does not discard them where they matter. Lushness is computed over complete
histories generated by the full joint dynamics. A correlation, a capability or a
latent structure changes lushness exactly when the dynamics draw on it, because
that is when it changes what follows. If nothing ever draws on a difference, it
changes nothing downstream, and lushness correctly ties the two cases.

**Example E3** makes this exact. Take three signs with joint law
P_θ(x,y,z) = (1 + θxyz)/8. For every θ the signs have zero means and are
pairwise uncorrelated; a model built from means and covariances cannot tell the
values of θ apart. Let a preparation sample the signs, and let a later module
branch four ways per step for k steps when an exposed sign is +1, and idle
otherwise.

| θ | Exposed: dynamics read XYZ | Unexposed: dynamics read X | Summary-based prediction |
| --- | --- | --- | --- |
| −1 | 2.0 | 22.0 | 23.0 |
| −0.5 | 12.8 | 22.8 | 23.0 |
| 0 | 23.0 | 23.0 | 23.0 |
| 0.5 | 32.8 | 22.8 | 23.0 |
| 1 | 42.0 | 22.0 | 23.0 |

*Log lushness in bits for k = 20 downstream steps.*

When the dynamics expose the triple correlation, lushness separates θ by 40
bits. When they do not, the only difference is the entropy of the preparation
itself, at most one bit. The summary-based model, which cannot see θ, predicts
the same value throughout and errs by up to 21 bits.

Where lushness genuinely loses information is at coarse resolution and short
horizons: a coarse description can merge futures the dynamics would later
separate, and a short horizon can stop before the separation happens. Those are
the subjects of sections 4.5 and 4.7.

---

## 4.5 Which horizon

Lushness is defined for a horizon n. Which horizon should a comparison use?

### Lushness is cumulative

By the chain rule, log lushness at horizon n contains all the branching of every
shorter horizon. Long-horizon lushness does not ignore early branches; it
includes them. Every shorter horizon is a truncation of the same object.

Truncation is a choice, and a privileging one. Cutting the assessment at a
horizon N weights the future fully up to N and not at all afterwards: a hidden
discount, shaped as a step. Lushness carries no discount factor, consistent with Ramsey's
argument that discounting later welfare merely because it is later has no
ethical justification (Ramsey 1928). Every step of the future counts, and the object the program cares about is the complete
development. The furthest horizon is therefore not one privileged choice among
others. It is the least truncated view of the one object.

Requiring an option to win at every horizon does not work as a substitute. Two
options can lead at different horizons, and dominance across truncations then
returns "incomparable" where the complete development gives a clear answer.
Example E2 shows exactly this.

### Example E2: maintenance, ruin and productive disruption

Start from a repertoire of 16 transformations, used uniformly (4 bits per step).
Compare three continuations:

- **Maintenance.** The repertoire stays at 16.
- **Ruin.** Each step, with probability f, a failure occurs in one of m failure
  modes and the repertoire loses one transformation. A repertoire of zero is
  dead. Otherwise the process acts.
- **Productive disruption.** The repertoire is cut to 8, but growth beyond the old
  ceiling is reopened: each step, with probability 0.2, the process builds and
  doubles its repertoire, up to 256; otherwise it acts.

Across a sweep of failure rate f from 0.05 to 0.4 and failure modes m from 4 to
256:

- **At short horizons ruin leads.** In every case swept, ruin exceeds maintenance
  for the first ten steps or more. Failure modes are real branches, and lushness
  counts them.
- **Ruin then falls behind.** Ruin drops below maintenance between 20 and 200
  steps, depending on f and m.
- **Productive disruption trails, then leads.** It is behind maintenance for the
  first steps, overtakes it at 20, and leads every case from 50 steps on.

In the limit the picture is unambiguous. Maintenance grows at 4 bits per step and
productive disruption at 7.1. Every path of ruin eventually ends, so its total is
bounded — between 137 and 1,060 bits across the sweep, however rare or varied
its failures. The complete-development ordering is productive disruption, then
maintenance, then ruin, in every case.

The short-horizon reversal is the lesson, not a loose end. Noisy failure looks
good until its consequences arrive. A short-horizon estimate of lushness can
prefer ruin.

### Comparing in the limit

When totals grow without bound, the limit comparison has a natural form: compare
long-run growth rates first, then lasting offsets.

> **Comparison in the limit**
>
> \[
> \log L_x(n)=n\,h(x)+c(x)+o(1)
> \]
>
> h(x) is the long-run rate of branching from x; c(x) is the lasting offset.
> Higher rate wins; at equal rates, higher offset wins.

The form holds for every finite process (formal note F4.4). Ruin has rate zero
and a bounded total. Maintenance and disruption have positive rates. In a closed
system that eventually forgets its starting point, all starting points share one
rate, and the comparison falls to the offset (section 4.6).

### Example E1: investment

The rate-then-offset form also explains investment. Compare a process that acts
uniformly over a fixed repertoire of 4 (2 bits per step) with one that first
spends k steps building — zero branching while it builds — and then acts over
the enlarged repertoire.

| Horizon | Noise in fixed repertoire | Best linear building | Best compounding building |
| --- | --- | --- | --- |
| 4 | 8 | 8 (k = 0) | 9 (k = 1) |
| 16 | 32 | 36 (k = 3) | 81 (k = 7) |
| 64 | 128 | 208 (k = 14) | 648 (k = 10) |
| 128 | 256 | 501 (k = 26) | 1,416 (k = 10) |

*Log lushness in bits. Linear building adds one transformation per step;
compounding doubles the repertoire, up to 4,096.*

Building always loses at short horizons, because a reliable constructor
concentrates weight. It wins after a crossover — for a single step of
investment, at 8 steps with linear growth and 4 with compounding — and the best
amount of investment grows with the horizon. This is chapter 3's reliable
constructor, made exact: concentration first, breadth later.

### The resolvable horizon

A bounded process cannot resolve the limit. Its model of the structure becomes
less reliable the further ahead it looks. In practice it compares options at the
furthest horizon it can resolve with acceptable error. Three levels follow.

- **The truest test** is the limit: the complete development, Omega.
- **The practical test** is the furthest horizon the process can resolve.
- **The gap between them** is where corrigibility lives. An action whose
  consequences extend beyond the resolvable horizon cannot be fully justified
  by a comparison that stops short of them. The less reversible the action, the
  more that matters (chapter 9).

Short-termism now has a precise definition: treating the resolvable horizon, or
a still shorter convenient one, as if it were the whole. Example E2 shows what
that error looks like.

---

## 4.6 Better than equilibrium, and the generative window

Thermal equilibrium is the stationary distribution π that a closed system's
dynamics approach when left alone. Compare a starting state x with it.

> **States better than equilibrium exist**
>
> \[
> \Delta\ell_n(x)=\log L_x(n)-\sum_y\pi(y)\log L_y(n),\qquad
> \sum_x\pi(x)\,\Delta\ell_n(x)=0
> \]
>
> The excess of starting at x over the equilibrium average, weighted by
> equilibrium itself, is exactly zero, because the dynamics leave equilibrium
> unchanged. Unless every starting state ties, some are strictly better than
> equilibrium.

That better-than-equilibrium states exist is a theorem. That the best of them
are organized, generative states is the program's hypothesis.

In a closed, finite system that forgets its starting point, the excess
converges: Δℓₙ(x) approaches a constant c(x). A good starting state buys a
lasting offset, not a faster long-run rate, and its advantage over each fresh
window decays as the system forgets. How large the offset can be depends on how
long forgetting takes, and forgetting times can grow enormously with system
size.

**Example E4.** On a randomly generated six-state chain, the equilibrium-weighted
sum of excess lushness is zero to machine precision at every horizon. The best
starting state keeps a lasting offset of +0.42 bits and the worst −0.76; the
offsets settle within about ten steps, because this small chain forgets quickly.

The universe is not such a system. It is far from equilibrium, open to the
growth of structure, and nowhere near forgetting its initial conditions. The
**generative window** is the interval before forgetting. Within it, offsets are
the phenomenon, and compounding generativity — growth of the repertoire itself —
is how a process escapes the closed-system bound by changing which states can be
reached at all.

---

## 4.7 Resolution

Every calculation of lushness declares a resolution: which distinctions between
states count as different. Coarse resolutions merge futures; fine ones separate
them. Rankings can change with resolution, and this is one of the program's main
open problems.

The program's position has three parts.

**The object is the profile.** Lushness at a single resolution is one view. The
full object is lushness across every resolution and horizon.

**The target is dominance across resolutions.** The program's headline physical
hypothesis is that generative organization beats the thermal reference at every
resolution within the generative window. Dominance across the whole profile
would settle a comparison without choosing a resolution.

**Where dominance fails, the resolution is fixed in advance.** When options are
incomparable across resolutions, a practical comparison uses a resolution chosen
before the comparison by a stated rule, never after seeing the result. Physics
offers a candidate privileged resolution: the distinctions that decoherence
copies durably and redundantly into the environment (Zurek 2009), which are the ones
situated processes can actually access. Whether that candidate suffices in
general is open, and a single ranking across resolutions remains a research
goal.

---

## 4.8 Quantum lushness

Quantum developments combine through amplitudes, which can interfere, so a
quantum structure is not simply a distribution over histories. Where a family of
alternatives has decohered, its histories carry ordinary probabilities, and
lushness applies to them directly. The open problem is breadth where no
classical family has been selected.

**Example E5.** An idle qubit prepared in a definite state can be described by a
question in the Z basis or in the X basis. Both descriptions are internally
consistent, and both families are decoherent. The Z question gives breadth 1;
the X question gives breadth 2. No single number can agree with both while also
ignoring which question was asked. A quantum lushness therefore needs either a
physical rule for selecting the family — such as actual record formation — or an
explicit dependence on the physically realized interface. The difficulty is a
known feature of decoherent-histories formulations of quantum mechanics, often
called the set-selection problem (Dowker and Kent 1996).

A satisfactory construction must meet several requirements at once:

- equivalent descriptions of the same physical process give the same value;
- inserting an analytical checkpoint, with no physical interaction, changes
  nothing;
- independent systems compose correctly;
- actual record formation, which makes new distinctions accessible, can change
  the value;
- the classical limit reproduces the classical calibration.

For a fixed, physically justified family with weights p, a natural requirement
is that quantum lushness lie between one effective direction and the fully
distinguishable classical case: 1 ≤ L_Q ≤ exp H(p). Bounds alone do not choose a
value. Finite tests in the program have ruled out several candidates, each of
which failed one requirement or another. The deliverable is a construction that
passes all of them, a demonstration that the requirements are incompatible, or a
precise statement of the missing physical input.

Coherent access (section 2.10) belongs here as well: processes that reach
outcomes through interference without forming records contribute to the
structure in ways a classical history family does not capture.

None of this changes the classical results above, which hold wherever
developments carry ordinary probabilities.

---

## 4.9 What the measure shows, and what it must still show

The examples answer the question chapter 3 left open: does lushness measure the
distinctions the mechanism describes, or merely sound compatible with them?

- **Construction versus noise (E1).** A reliable constructor loses at short
  horizons and wins after a crossover, by a margin that grows with compounding.
- **Ruin versus disruption (E2).** In the limit, productive disruption beats
  maintenance, which beats ruin, in every case swept. At short horizons, ruin can
  lead.
- **Hidden structure (E3).** Lushness sees a correlation exactly when the dynamics
  use it.
- **Equilibrium (E4).** Better-than-equilibrium states exist, and their advantage
  in a closed system is a lasting offset.
- **Quantum family selection (E5).** Breadth depends on the question asked,
  unless physics selects it.

These are stylized models with stated parameters, chosen to isolate one
mechanism each. They show that the measure behaves as the framework requires
where the mechanism is clear. They do not yet show that it does so in the
complex, coupled systems the ethics concerns.

The program's central wager (chapter 5) depends on that further step. Its two
decisive tests are a pair of worlds with identical branching structure at every
resolution, one recognizably good and one recognizably bad, and a world of
breadth-neutral domination, in which access is concentrated in a few at no cost
to total lushness. E2's short-horizon reversal shows why both must be assessed
at the furthest resolvable horizon. A test that stops early can be won by ruin.

---

## Formal notes

*Written for readers who want the definitions in full.*

### F4.1 Uniqueness

Let H be defined on finite probability vectors and satisfy: symmetry under
permutation; continuity of H(p, 1−p) in p; the grouping property

\[
H(p_1,\dots,p_n)=H(p_1+p_2,p_3,\dots,p_n)+(p_1+p_2)\,
H\!\left(\tfrac{p_1}{p_1+p_2},\tfrac{p_2}{p_1+p_2}\right);
\]

and normalization H(½, ½) = 1. Then H = −Σ pᵢ log₂ pᵢ (Faddeev 1956; see also
Shannon 1948 and Khinchin 1957). Exponentiation gives L(uniform on N) = N.
Rényi entropies of order α ≠ 1 satisfy additivity for independent systems but
not grouping, so the root assessment of a history tree does not equal the
probability-weighted assessment of its subtrees.

### F4.2 Chain rule and recurrence

For a Markov kernel K and exact root x₀, with
p(x₁,…,x_n) = ∏ K(x_t, x_{t+1}) and g(x) = H(K(x,·)),

\[
\ell_n=\sum_{t=0}^{n-1}K^tg,\qquad \ell_{n+1}=g+K\ell_n,\qquad \ell_0=0,
\]

computing complete-history entropy without enumerating the tree. A terminal
outcome with a deterministic self-loop keeps its weight and adds no branching.
For independent histories L_AB = L_A L_B; for a coupled joint law
H(A, B) = H(A) + H(B) − I(A; B).

### F4.3 The equilibrium identity and finite forgetting

For a stationary π (πK = π),

\[
\sum_x\pi(x)\Delta\ell_n(x)=\sum_{t=0}^{n-1}(\pi K^t-\pi)g=0.
\]

If K is finite, irreducible and aperiodic, then
sup_x ‖δ_xKᵗ − π‖_TV ≤ C rᵗ for some C < ∞ and 0 < r < 1 (Levin, Peres and
Wilmer 2009, Theorem 4.9), so

\[
\Delta\ell_n(x)\to c(x)=\sum_{t=0}^{\infty}(\delta_xK^t-\pi)g,\qquad
|\Delta\ell_n(x)-c(x)|\le\frac{2C\,\|g\|_\infty\,r^n}{1-r},
\]

and ℓ_n(x) = n·πg + c(x) + O(rⁿ). Fresh-window advantage decays:
|K^mℓ_n(x) − n·πg| ≤ 2C‖g‖_∞ r^m/(1 − r). The constants depend on K and need
not stay bounded as system size grows.

### F4.4 Comparison in the limit

For any finite kernel, the Cesàro limit h(x) = lim ℓ_n(x)/n exists and equals
Σ_C P_x(absorbed in C)·π_C g over the closed classes C reachable from x, with
π_C the stationary law of C; transient states and absorbing terminal states
contribute rate zero. Within an aperiodic closed class, ℓ_n(x) − n h(x)
converges to a finite offset; periodic classes give bounded oscillation. The
limit order compares h first and the offset second. For growing or
non-stationary systems, rates are defined along the realized growth and must be
stated with the model.

### F4.5 Worked examples

All values are exact, computed by the recurrence of F4.2 in bits; the script is
listed in chapter 11.

- **E1.** Repertoire r₀ = 4 acted on uniformly; build-first policies spend k
  deterministic steps building (r_k = r₀ + k, or min(r₀·2ᵏ, 4096)), then act
  uniformly for n − k steps.
- **E2.** R = 16. Ruin: g(r) = h(f) + f log₂m + (1 − f) log₂r, with r → r − 1 on
  failure and r = 0 absorbing; f ∈ {0.05, 0.1, 0.2, 0.4}, m ∈ {4, 16, 64, 256}.
  Disruption: r₀ = 8, g(r) = h(0.2) + 0.8 log₂r, r → min(2r, 256) on building.
  Maintenance: g = 4. Limit rates 4, 7.12 and 0 bits per step.
- **E3.** P_θ(x,y,z) = (1 + θxyz)/8; after sampling, k steps of four-way branching
  when the exposed sign is +1.
- **E4.** A six-state chain generated with a fixed seed; offsets reported at
  n = 200.
- **E5.** |ψ⟩ = |0⟩, one cut, projective families in the Z and X bases.

### F4.6 Quantum histories

For exhaustive projector families at declared times, with class operators
C_α and decoherence functional D_{αβ} = Tr(C_α ρ C_β†) (F1.4), a decoherent
family has probabilities D_{αα} and classical lushness exp H(diag D). For the
idle qubit with H = 0 and ρ = |0⟩⟨0|, D_Z = diag(1, 0) and D_X = diag(½, ½) are
both decoherent and give 1 and 2. Any family-independent scalar that equals
classical perplexity on every decoherent family is therefore impossible. A
candidate quantum lushness must specify its physical family selection or its
interface dependence and satisfy the requirements of section 4.8.

---

## For alignment

Example E2 identifies a concrete failure mode for any system that optimizes an
estimate of lushness: at short horizons, adding failure modes raises the
estimate. A system evaluating its options over too short a horizon would
therefore prefer ruin to maintenance, and its errors would look like success
until their consequences arrived. The correction is structural, not a patch.
Lushness carries no discount, so options must be compared at the furthest
horizon the system can resolve, and the gap between that horizon and the
complete development is where corrigibility is required. Horizon adequacy belongs
alongside realization witnesses as a check on any plan.

---

## Status

| Status | Claims in this chapter |
| --- | --- |
| **Established** | Lushness as exponentiated entropy; its calibration; the chain rule and recurrence; product rule for independent systems. Uniqueness of Shannon entropy under symmetry, continuity, grouping and normalization. The equilibrium identity. Finite forgetting and the lasting offset. The rate-then-offset form of the limit. Family dependence of decoherent breadth. |
| **Exact worked examples** | E1 to E5, under their stated models. |
| **Adopted** | Lushness as the benchmark of the structure. No temporal discount; comparison at the furthest resolvable horizon, with the limit as the truest test. Resolution fixed in advance where dominance fails. |
| **Hypotheses** | Generative organization dominates the thermal reference at every resolution within the generative window. The breadth that dominates over long horizons is generative rather than pathological. |
| **Open** | A single ranking across resolutions. A general quantum construction. Estimators with error bounds for realistic systems. |

---

## References cited in this chapter

*Collected with full details in chapter 13.*

- Cover, T. M., and Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Hoboken: Wiley.
- Dowker, F., and Kent, A. (1996). On the consistent histories approach to quantum mechanics. *Journal of Statistical Physics* 82(5–6), 1575–1646.
- Faddeev, D. K. (1956). On the concept of entropy of a finite probabilistic scheme. *Uspekhi Matematicheskikh Nauk* 11(1), 227–231. (In Russian.)
- Hill, M. O. (1973). Diversity and evenness: A unifying notation and its consequences. *Ecology* 54(2), 427–432.
- Jelinek, F., Mercer, R. L., Bahl, L. R., and Baker, J. K. (1977). Perplexity — a measure of the difficulty of speech recognition tasks. *Journal of the Acoustical Society of America* 62(S1), S63.
- Jost, L. (2006). Entropy and diversity. *Oikos* 113(2), 363–375.
- Khinchin, A. I. (1957). *Mathematical Foundations of Information Theory.* New York: Dover.
- Levin, D. A., Peres, Y., and Wilmer, E. L. (2009). *Markov Chains and Mixing Times.* Providence: American Mathematical Society.
- Ramsey, F. P. (1928). A mathematical theory of saving. *Economic Journal* 38(152), 543–559.
- Rényi, A. (1961). On measures of entropy and information. In *Proceedings of the Fourth Berkeley Symposium on Mathematical Statistics and Probability*, vol. 1, 547–561. Berkeley: University of California Press.
- Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal* 27, 379–423 and 623–656.
- Zurek, W. H. (2009). Quantum Darwinism. *Nature Physics* 5(3), 181–188.
