# 2 — Present frames and access

Chapter 1 defined the physical possibility structure. This chapter fixes the
point of view from which it is assessed and identifies where, inside it, the
differences between options actually lie.

The argument has three steps. All assessment is made from a present, and a
present carries the past only through its physical state. Because fundamental
dynamics is unitary, every option leaves the total information of the world
unchanged, so total information cannot rank options. The differences therefore
lie in how the whole is organized, and specifically in **access**: what situated
parts of the world can actually reach, by what route and at what cost. Access is
the concept through which organization, harm, cooperation and choice enter the
rest of the manuscript.

---

## 2.1 Present frames

A **physical frame** is a present together with its physical state: an
admissible spacelike slice of spacetime and the state of the world on it. In a
relativistic setting there are many such slices through any event, and none is
privileged. Different slices are related by the dynamics and by the appropriate
transformations of their descriptions. In a finite model the frame is simply a
declared update step and the state at that step.

Within a frame, a **perspective** is the situated access and influence of a
process: where it couples to the rest of the world, what can affect it, what it
can affect, and which correlations cross its boundary. A detector, a gas in
contact with a reservoir, a cell and an institution each have a perspective in
this sense. Awareness and agency are further kinds of organization a perspective
may have. They are not entry conditions for having one.

A **frame description** is a representation of a physical frame at a stated
scope and resolution: a region, a set of observables, a duration, the coupling
at its boundary, the records available inside it. A scientist can choose such a
description without any process inside the world corresponding to it. What
justifies treating a description as a perspective is the physical coupling that
actually realizes it, not the mathematics alone.

The distinction matters because the same physical situation supports many
descriptions. An operator in a power plant encounters part of its state; an
engineering model of the plant resolves components but not molecules; the full
physical frame contains both and more. They are related, and adequacy depends on
which consequences a restricted description preserves (section 1.6).

---

## 2.2 Sufficiency and blindness to arrival

A present is **sufficient**: whatever bearing the past has on the future is
carried by the physical state it left. There is no further record of history
attached to a present beyond the physical traces in it. In probability theory
this is the Markov property of a complete state description (Norris 1997).

Two consequences follow.

**A process cannot tell, from its present, how it arrived.** Two routes that
produce the same physical state have the same future. Whether a cell came from a
division, a repair or an accident, and whether a branch arose from decoherence
or from an interaction with an apparatus, makes no difference to what follows
unless it left a physical trace. History is not lost: it remains in Omega, where
it can be queried. It is simply not an additional ingredient of the present.

**History and current access are different things.** The accumulated history of
a process grows over time. What the process currently has access to need not.
A record can be lost: the history still contains it, but the process can no
longer use it. Recovering its use requires a physical route — retrieval,
re-derivation, reconstruction — with its own delay, coupling and cost. An
analyst's archive gives the process nothing for free.

At a restricted interface, memory effects can appear (Breuer et al. 2016): a
subsystem behaves as if it remembers, because correlations with an omitted
environment carry information forward. These are not exceptions to sufficiency.
They show that the restricted description was not sufficient, and that the
environment, or an explicit multitime description of the interface, must be
added back.

---

## 2.3 Why total information cannot rank options

Fundamental dynamics is unitary: the universal quantum state evolves without
creating or destroying information (Nielsen and Chuang 2000). Every option,
carried forward, leaves the total information of the universal state unchanged.
Information about what happened is redistributed — into the environment, into
correlations, into places no situated process can reach — but it is not removed.

Total information therefore cannot supply a ranking: asked "which option leaves
the universe with more information?", the structure answers "neither". This does
not mean the whole has no properties that distinguish options. Two options that
conserve total information can differ greatly in their internal organization:
their correlations, their records, and which developments situated processes
can reach. The ranking has to come from that organization. Which developments
can a given process reach? With what weight? Through which couplings? At what
cost? Lushness, taken from a present frame, is a property of the whole that
measures exactly this.

That is the sense in which the differences between options live in access.

---

## 2.4 Access

**Access** is the capacity of a situated process to reach a development: a
state, a transformation, a capability, a recovery. An access claim names a
physical route and everything the route involves:

- **the preparation** required before the route can be used;
- **the records** available to the process along the way;
- **the resources** consumed — energy, material, apparatus time, space;
- **the elapsed time**;
- **the weight** with which the route succeeds;
- **the residual state** left behind for whatever comes next.

Weights compose along a route. If preparing an apparatus succeeds with
probability p and using it then succeeds with probability q, the route succeeds
with probability pq. Repeated attempts change that only if failures leave states
from which a retry is possible and enough time and material remain.

Costs form a profile, not a single number. Work, consumption, peak occupancy and
time compose by different rules: sequential expenditures add, peak space takes a
maximum, stocks can be replenished. Taking the cheapest entry in each column from
different implementations can describe a combination no single implementation
achieves. An access claim therefore retains the whole route, so that later
processes inherit its actual consequences.

Access is oriented. It runs forward along the gradients the universe supplies,
and what one process makes accessible can be what another process loses access
to. Chapter 10 reads this orientation as the physical form of a primitive
asymmetry anchored in the arrow of time; nothing in the main argument depends on
that reading.

---

## 2.5 Realization witnesses

A **realization witness** is the physical account that backs an access claim: the
controller, the preparation, the resources, the boundary conditions and the law
that results. Every access claim in the manuscript is meant to be backed by one,
and the concept does more work than its modest definition suggests. It applies
to access claims the distinction, central to constructor theory, between tasks
the laws permit and constructors that can perform them (Deutsch 2013).

A witness separates three questions that are easily run together:

1. **Is the transformation permitted?** The laws allow it.
2. **Is an apparatus ready to perform it?** Something exists that does it
   reliably.
3. **Is there a route to that apparatus?** The apparatus can actually be
   obtained from here, with the resources, time and information available.

Each is a separate physical fact. A transformation can be permitted with no
ready apparatus, and an apparatus can be possible in principle with no available
route to building it. Readiness is a property of the present; the route to
readiness is a property of the structure from the present.

A witness also fixes what a controller can respond to. A control policy may
depend only on records the controller actually has, not on the hidden state an
analyst knows. And a combination of operations needs one witness for the
combination: two separately witnessed operations can still be jointly infeasible
(section 1.3).

The concept is central for alignment. A capable planner can propose
transformations that are permitted but have no available route, or treat
separately feasible steps as jointly feasible. Asking for the witness — what
prepares this, what it consumes, what it leaves, whether its pieces can run
together — exposes both errors.

---

## 2.6 Information is not access

The amount of information an arrangement holds does not determine what it gives
access to. Two examples, both from the program's finite models, show the
difference.

**Encoding.** Three registers can hold three bits s, f₁, f₂ as plain copies, or
as the invertible recoding (s, s⊕f₁, s⊕f₁⊕f₂), where ⊕ is XOR. Both hold exactly
the same information. Now ask how many local operations it takes to deliver a
particular function of the bits into a fresh register:

| Delivery | From copies | From recoding |
| --- | --- | --- |
| f₁ | 1 step | 2 steps |
| f₁ AND f₂ | 1 step | 3 steps |
| parity of all three | 3 steps | 1 step |
| s⊕f₁ | 2 steps | 1 step |

*Step counts are illustrative, computed in a model in which each operation
touches at most three bits, using copy, XOR, AND and their controlled versions.
Current figures are in chapter 11.*

Neither arrangement is better overall; each makes different things cheap. A
summary that counts how many functions are deliverable within a given number of
steps cannot see the difference at all, because an invertible recoding only
permutes which deliveries are cheap.

**Repair.** Three registers holding two bits u and v can store (u, u AND v, v),
(u, u, v) or (u, v, u⊕v). All three determine u and v. After the loss of one
register at a known position, the first can be repaired at one of the three
positions, the second at two, and the parity arrangement at all three. Where
redundancy sits, not how much information is held, decides what can be
recovered. The parity arrangement is the simplest example of an erasure code
(MacWilliams and Sloane 1977).

The cause is locality. Physical interactions are local and involve few degrees
of freedom at a time. If arbitrary transformations of any size were available in
a single step, the differences above would vanish. In a world of local
interactions, they are real, and in the program's exhaustive surveys of small
model worlds most pairs of arrangements holding equal information differed in
what they later made accessible.

---

## 2.7 Weights from a frame

A frame assigns weights to the developments it supports. Conditioning on what is
known in a frame produces normalized probabilities for that frame. Two points
about this are easy to get wrong.

**Conditioning keeps its cost.** If a development is reached only after a
preparation that succeeds with probability P(α), a frame that starts after the
preparation sees normalized probabilities. The encompassing description retains
P(α). Forgetting it would change the claim from "what follows once the
preparation succeeds" to "what follows from here", which are different
questions.

**Normalization is not breadth.** Every frame's probabilities sum to one,
whether they are spread over a million developments or concentrated on one.
Normalization says how weight is distributed. It says nothing about how many
developments carry it. That is the question lushness answers (chapter 4).

---

## 2.8 Access over time

"Can reach" has several meanings over time, and they must not be conflated.

- **First arrival**: whether and when a process first reaches a target.
- **Occupancy**: how much of the time it spends there.
- **Maintenance**: whether it stays there for a required duration after arrival.
- **Regeneration**: whether it returns after being displaced.

A process that reaches a target early and immediately loses it scores well on
first arrival and badly on everything else. Each of these is a forward question
from a present; none is a time average that substitutes for the present.
Chapter 6 uses the distinctions to separate recovery from mere return.

---

## 2.9 The ultimate frame

The **ultimate frame** is Omega used as the reference for every comparison: the
encompassing closure in which every local description and every frame's
weighting belong to one physical account, with no further frame outside it.

It has three properties.

**It is a reference, not an observer.** It does not choose, evaluate or act. It
is what a comparison would be relative to if it were complete.

**No real process occupies it.** Every actual process holds a partial
description. Its records, models and interventions are themselves parts of the
structure they describe.

**It grounds humility.** Because no real process holds the complete comparison,
no real process can claim the verdict that only the complete comparison could
deliver. Chapters 8 and 9 draw the consequences: graded rather than complete
justification for sacrifice, and corrigibility as a structural requirement.

---

## 2.10 From access to lushness

Access and lushness are not two separate ideas. Lushness is access accumulated
over the futuresfield, by the chain rule of information theory (Cover and Thomas
2006).

> **Access is the input to lushness**
>
> \[
> g(x)=-\sum_y K(x,y)\log K(x,y),\qquad
> \log L_x(n)=\sum_{t=0}^{n-1}(K^tg)(x)
> \]
>
> g(x) is the entropy of what the present x can reach in one step, weighted by
> how likely each successor is: one-step access, measured as effective
> branching. Log lushness adds up that branching over the horizon, weighted by
> which states the dynamics actually visit.

Three consequences follow, each developed in chapter 4.

**Organization enters through access.** A construction changes which states are
visited later, and so which branching is available then. That is the precise
form of "organization changes what follows" (chapter 3).

**Costs need no separate term.** Section 2.4 gave access a cost profile: time,
energy, material, occupancy. Lushness contains no cost penalty, and needs none. A
route that consumes resources leaves a residual state with less available, and
less available means less branching afterwards. Costs register in lushness
through what they use up. Adding a separate cost term would count them twice
and would take the measure outside the weight-only class within which chapter 4
proves it unique.

**Equal information, unequal lushness.** The arrangements of section 2.6 hold the
same information but make different transformations cheap. When later
processes draw on them, local dynamics give the two arrangements different
future branching, and lushness distinguishes them. If nothing ever draws on the
difference, it changes nothing downstream, and lushness correctly ties them.

### Coherent access

The account of access in this chapter is stated for processes whose
alternatives have decohered into records. Access is not only classical.
Coherent processes can reach outcomes through interference without forming
records along the way; quantum computation is the clearest case (Nielsen and
Chuang 2000). Coherent
access belongs with the quantum construction of lushness in chapter 4, where
the open problem of measuring breadth without a classical history family is
stated precisely.

---

## Formal notes

*Written for readers who want the definitions in full.*

### F2.1 Physical frames and descriptions

A physical frame is F_Σ = (Σ, ρ_Σ) with the native specification needed to
evolve it (F1.1). In a relativistic model Σ is an admissible spacelike
hypersurface, a Cauchy surface where the spacetime and theory admit one; in a
finite model it is a declared update cut. A frame description is a
representation, restriction or conditioning of F_Σ at declared scope:
observable algebra 𝒜(R), duration, boundary coupling and accessible records.
Different admissible sections are related by the dynamics and the appropriate
transformations of their descriptions; a worldline through an event does not
select a unique global section. Relational treatments of quantum fields on
hypersurfaces (Höhn, Russo and Smith 2023) provide a developed connection; a
general relativistic quantum realization remains open.

### F2.2 Conditioning and current access

Under a common classical law P, a positive-probability condition α gives

\[
\mu_\alpha(E)=P(E\mid\alpha),\qquad P(E\cap\alpha)=P(\alpha)\,\mu_\alpha(E).
\]

The encompassing description retains P(α). For nested information
𝓕_s ⊆ 𝓕_t and an integrable readout Z, the tower identity holds (Williams
1991):

\[
\mathbb E\bigl[\mathbb E[Z\mid\mathcal F_t]\mid\mathcal F_s\bigr]
=\mathbb E[Z\mid\mathcal F_s].
\]

The accumulated history generates an increasing filtration 𝓕_t. Current access
𝓖_t = σ(O_t, M_t), generated by present observations and accessible memory, need
not increase: a lost record remains in 𝓕_t while leaving 𝓖_t. Martingale
reasoning valid for 𝓕_t does not transfer automatically to 𝓖_t. At restricted
interfaces, multitime dependence is represented by process tensors (Pollock et al.
2018) with declared intervention slots; slots describe implemented
operations or queries, not additional physical alternatives.

### F2.3 Access with resources

An operational prefix is described by a joint law J(r, y, b, t | x) over
accessible record r, sufficient residual state y, resource bill b and elapsed
time t. A suffix may depend on r but not on y except through accessible records.
For a later event E,

\[
P_x(E)=\sum_{r,y,b,t}J(r,y,b,t\mid x)\;P_y^{\,\mathrm{suffix}(r)}\bigl(E;\,T-t,\,B-b\bigr),
\]

with the remaining deadline T − t and budget B − b. Failed and unfinished
prefixes retain their mass. The bill b is a vector whose components compose by
their own rules (sum for sequential work, maximum for peak occupancy, signed sum
for replenishable stocks). Joint feasibility of several requirements requires a
single implemented development satisfying all of them.

### F2.4 Arrival, occupancy and maintenance

For a classical target set V, let τ_V = inf{t ≥ 0 : X_t ∈ V}. The first-arrival
profile A_x(t) = P_x(τ_V ≤ t) satisfies

\[
\int_0^T A_x(t)\,dt=\mathbb E_x\bigl[(T-\tau_V)_+\bigr],
\]

which measures expected time remaining after arrival, regardless of whether the
target is retained. Occupancy is

\[
O_x(T)=\mathbb E_x\!\left[\int_0^T\mathbf 1_V(X_t)\,dt\right]
=\int_0^T P_x(X_t\in V)\,dt .
\]

Maintenance requires remaining in V for a declared duration after arrival;
regeneration concerns return after a specified displacement. For controlled
finite models, a viability set (Aubin 1991) collects the states from which some
available policy keeps declared requirements satisfied against specified
disturbances; full-state and partially observed control require different
constructions.

---

## For alignment

Two failure modes of capable planners are failures of access reasoning. The
first is treating a permitted transformation as available: the plan names an
outcome physics allows but no route the system can actually take. The second is
treating separately feasible steps as jointly feasible. Realization witnesses
catch both. A third, subtler failure is reasoning from an archive the system no
longer has access to, or from facts an overseer knows but the system cannot
observe. Section 2.2's distinction between history and current access is the
corrective.

---

## Status

| Status | Claims in this chapter |
| --- | --- |
| **Established** | Physical frames and their relativistic multiplicity. Sufficiency of a complete present. Unitarity and the conservation of information. Conditioning identities; history versus current access. Arrival and occupancy identities. One-step access as the input to log lushness, by the chain rule. |
| **Finite evidence** | Information is not access: equal-information arrangements differ in delivery cost and repairability; most equal-information pairs in exhaustive small-world surveys differ in later access. |
| **Adopted** | Assessment from present frames. Access, backed by realization witnesses, as the locus of differences between options. The ultimate frame as reference. |
| **Interpretive** | Access as the physical form of a primitive asymmetry (chapter 10). |
| **Open** | A general relativistic quantum construction of frames and their comparison. Coherent access and its contribution to lushness. |

---

## References cited in this chapter

*Collected with full details in chapter 13.*

- Aubin, J.-P. (1991). *Viability Theory.* Boston: Birkhäuser.
- Breuer, H.-P., Laine, E.-M., Piilo, J., and Vacchini, B. (2016). Colloquium: Non-Markovian dynamics in open quantum systems. *Reviews of Modern Physics* 88(2), 021002.
- Cover, T. M., and Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Hoboken: Wiley.
- Deutsch, D. (2013). Constructor theory. *Synthese* 190(18), 4331–4359.
- Höhn, P. A., Russo, A., and Smith, A. R. H. (2023). Matter relative to quantum hypersurfaces. arXiv:2308.12912.
- MacWilliams, F. J., and Sloane, N. J. A. (1977). *The Theory of Error-Correcting Codes.* Amsterdam: North-Holland.
- Nielsen, M. A., and Chuang, I. L. (2000). *Quantum Computation and Quantum Information.* Cambridge: Cambridge University Press.
- Norris, J. R. (1997). *Markov Chains.* Cambridge: Cambridge University Press.
- Pollock, F. A., Rodríguez-Rosario, C., Frauenheim, T., Paternostro, M., and Modi, K. (2018). Non-Markovian quantum processes: Complete framework and efficient characterization. *Physical Review A* 97(1), 012127.
- Williams, D. (1991). *Probability with Martingales.* Cambridge: Cambridge University Press.
