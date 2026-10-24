# 1 — The physical possibility structure

Ethics usually begins with persons, preferences or rules. The Omega program
begins with something prior to all of them: what can follow from the way the
world is now. This chapter defines that object precisely, shows that physics
already supplies it, and identifies the properties of it that the rest of the
manuscript depends on.

The claim of the chapter is modest in one sense and ambitious in another. It is
modest because nothing here goes beyond established physics: the object is the
state of the world, its laws, and the developments they generate. It is
ambitious because we take that object, rather than any summary of it, as what
ethics is ultimately about. Every later chapter is an inquiry into features of
this one structure.

---

## 1.1 What follows from a present

A **present** is the physical state of the world on a spacelike slice of
spacetime: the state of everything, across space, at one moment in some
admissible frame of reference. Relativity allows many such slices through any
event; none is privileged, and the account below does not need one to be.

A present, together with the laws, determines what can follow. Two ingredients
are needed and both must be complete.

**The present must be sufficient.** It must contain everything the laws need to
carry the world forward: positions and momenta, fields, chemical stocks,
records, correlations with the environment, and the state of any apparatus that
will act. An effective model may legitimately omit microscopic detail, but it
must retain whatever its own law of motion requires. A description of a
subsystem alone is usually not sufficient, because its future depends on
correlations it shares with its surroundings.

**The law must be native.** It is the actual dynamics of the physical model —
not a list of tasks, a menu of actions, or a set of scenarios someone finds
interesting. Choices, controllers and agents enter only as physical processes
governed by the same law.

Given both, the **physical possibility structure** from that present is the
complete set of developments the law permits, each with its weight, together
with all the relations among them: which developments share a beginning, which
reconverge, which enable or exclude which.

### The classical form

In a classical model with a finite set of states, the law is a transition kernel
K, where K(x, y) is the probability of moving from state x to state y in one
step. The probability of a complete history from a sufficient present x is the
product of these one-step probabilities.

> \[
> P_x(x_1,\dots,x_n)=\prod_{t=0}^{n-1}K(x_t,x_{t+1}),\qquad x_0=x.
> \]
>
> The structure from x is this probability law over complete histories, for
> every horizon n.

What matters is the law at every state the system might reach, not just the
first step. Two models can agree on what happens next from x and disagree
entirely one step later. Continuous-time models work the same way with rates in
place of step probabilities; sampling such a process at fixed intervals
describes it at that resolution and can miss events between samples.

### The quantum form

In quantum mechanics the present is a quantum state and the law is unitary
evolution: the state is carried forward by a family of operators that preserve
all its information. Alternatives carry complex amplitudes rather than
probabilities, and amplitudes can reinforce or cancel. A quantum structure is
therefore not simply a list of weighted branches. Paths through it can
interfere, and drawing them as separate worlds to be counted misdescribes them.
Probabilities appear when distinctions become recorded in the environment, a
process developed in section 1.5.

### What the structure is not

The structure adds no substance and no force. Catalysts, reservoirs, interfering
amplitudes and deliberating organisms shape it through their ordinary physical
relations. No additional principle steers the world toward greater possibility;
the question of how possibility grows is answered later from the dynamics
themselves.

Nor is the structure a space of everything describable. It contains what the
physical model actually permits. Three questions stay distinct throughout the
manuscript: what a formal model admits, what physical reality realizes, and where
experience occurs.

---

## 1.2 Complete developments

The structure contains complete developments, not just where they end.

Consider a system that stays idle, and the same system making an excursion and
returning. The end states agree. The developments do not: during the excursion,
the system coupled to its surroundings, consumed resources and occupied
apparatus that something else might have used. A description that keeps only
end states treats the two as identical. The structure keeps both.

This matters ethically before any ethics has been stated. A construction that
later dissolved still occurred. A delay that made a rescue impossible is part of
what happened, even if the eventual state is the same as with a timely rescue. A
loss followed by recovery is not the same development as no loss at all.

### Reconvergence and re-rooting

Different histories can arrive at the same later state. Suppose x → a → c and
x → b → c. From the original present x, these are two distinct developments
with their own weights. From c, what follows is the same in both cases.

Both statements are true, and they answer different questions. Asking about the
structure from x keeps both routes. Asking about the structure from c — taking c
as a new present — asks what follows from there. The two are linked by ordinary
conditioning on reaching c. Neither deletes the other, and re-rooting adds no
hidden label recording which route was taken. The past bears on the future only
through the state it produced.

### Ending versus not knowing

A development can terminate: a process halts, an organism dies, a reaction
stops. Termination is a real outcome and keeps its weight. An unfinished
calculation is different: it marks the edge of what has been computed, not an
end of what follows. Confusing the two manufactures false certainty at the
boundary of a model.

---

## 1.3 Joint structure and composition

What matters about several processes is how they behave together.

Two fair coins can be independent, or perfectly correlated copies of each other.
Each coin, alone, is a fair coin in both cases. Now compute the XOR of the two,
which is 1 when they differ and 0 when they agree. It is a fair coin in the
first case and always 0 in the second. Identical parts, different futures. The
structure is a property of the joint state, and summaries of the parts can
discard exactly what determines what follows.

### Sequential composition

Processes leave things behind: stocks depleted or replenished, apparatus
occupied or freed, records written somewhere, correlations available to later
interactions. These residual conditions are how one stage of a development
shapes the next, and so how organization enters the future without any special
credit.

To compose two stages correctly, the first stage's description must carry both
its outcome and the state it leaves. The second stage then acts on that residual
state. Time, energy and material consumed by the first stage are no longer
available to the second. Failures and unfinished outcomes keep their actual
residual states and costs.

### Parallel composition and joint feasibility

Running processes side by side requires their actual joint law. Two repairs,
each individually possible, may compete for the same unit of fuel. Any two of
three processes may fit within a resource budget while all three together do
not. **Joint feasibility** — the existence of one physical development in which
several requirements hold at once — does not follow from each requirement being
feasible separately, or even from every pair being feasible.

Independence is a special case and needs a physical reason. Independently
prepared, non-interacting systems compose as products. Correlated preparations
or interacting dynamics require the joint description, even when each part's
readings agree with the independent case.

---

## 1.4 What can actually be done

Agents, controllers and institutions are physical processes inside the
structure. A **controlled** process is one whose development depends on
physically available records and physically implemented operations: a
thermostat reading a temperature and switching a heater, a cell sensing a
nutrient and expressing an enzyme, an engineer reading a design and building a
machine.

Control has two physical requirements. The controller can respond only to
records it actually has, not to facts an analyst knows about the system's hidden
state. And an operation is available only if something physically implements
it. Naming a chemical reaction does not make it a selectable action; it remains
part of the native dynamics until some process controls it.

A **realization witness** connects an operational claim to the physics that
supports it: the controller, the preparation, the resources consumed, the
boundary conditions and the resulting law. It separates three different things:

- a transformation the laws **permit**;
- an apparatus **ready** to perform it reliably;
- a **route** by which such an apparatus can actually be obtained.

If preparing the apparatus succeeds with probability p and using it then
succeeds with probability q, the whole route succeeds with probability pq.
Readiness and the route to readiness are different physical facts, and both
belong to the structure.

---

## 1.5 Quantum structure and records

Quantum developments combine through amplitudes, and amplitudes interfere. Two
consequences shape everything later.

**A drawn path is not a world.** A diagram of quantum alternatives can be useful,
but its paths cannot be counted as independent outcomes. Where paths interfere,
coarse alternatives must be combined at the level of amplitudes before any
probability is assigned. Intermediate stages in such a diagram are not physical
measurements unless the corresponding interactions are part of the model.

**Probabilities arise from records.** When a distinction becomes correlated with
the environment — when a record of it forms — interference between the
alternatives is suppressed for every process that cannot access the whole
environment. This is **decoherence**. Families of alternatives that have
decohered behave like ordinary classical outcomes, with probabilities given by
the quantum weights.

Two cautions follow, and both recur in chapter 4.

First, decoherence does not by itself select a unique way of dividing the world
into alternatives. An idle qubit prepared in a definite state can be described
by questions in different bases; each description is internally consistent, and
they assign different numbers of effective alternatives. What selects a
description physically is actual record formation: which distinctions the
dynamics copy into the environment, durably and redundantly.

Second, records can be undone. If the only record of a distinction is reversed
by a later interaction, the alternatives recombine and interference returns. If
a redundant record survives elsewhere, the split persists. The intervening
evolution remains part of the structure in either case. Global purity of the
universal state does not make the structure trivial: the whole can be in a pure
state while the relations within it are rich.

---

## 1.6 Faithful descriptions

No one computes with the whole structure. Every model compresses it. A
compression is faithful for a purpose when it preserves the relations that
purpose depends on.

The standard of faithfulness is predictive. Two descriptions are equivalent
relative to a family of physical tests if every test in the family produces the
same outcome law from both. Enlarging the family can separate descriptions that
were equivalent; it never merges descriptions already separated. Equivalence
for isolated outputs is not enough when a part will be embedded in a larger
process: the tests must include the contexts it will be composed into.

A small example shows why summaries fail. Take three signs X, Y, Z, each +1 or
−1, with joint law

> \[
> P_\theta(x,y,z)=\tfrac18\,(1+\theta\,xyz),\qquad -1\le\theta\le1.
> \]

For every θ, each sign has mean zero and the three are pairwise uncorrelated.
Means and covariances cannot tell the values of θ apart. Now apply the
reversible transformation that replaces Z by the product XYZ. The new third sign
has mean θ. The same transformation applied to inputs with identical summaries
produces different outputs. A summary that discards the triple correlation
cannot predict what follows under an operation the physics allows.

Faithful compression is a tool, not a verdict. It does not identify physical
copies, histories or individuals, and a distinction outside a description's
tests remains in the structure. Approximate compression needs an error
statement, and approximate equivalence is not transitive: two descriptions each
close to a third can be twice as far from each other.

---

## 1.7 The futuresfield and Omega

Two names are useful for two ways of looking at the same object.

The **futuresfield** is the physical possibility structure seen forward from a
particular present: what that present supports, at every horizon. It is the
object assessed in decisions, comparisons and ethical judgments, all of which
are made from somewhere.

**Omega** is the structure taken whole: every development of every present,
considered together as one completed object. Its role in the main argument is
as the reference against which local descriptions are complete or incomplete,
developed in chapter 2 as the ultimate frame. Its role in the wider
interpretation of the program is taken up in chapter 10.

---

## 1.8 The physical setting

Quantum field theory is the best current description of matter and its
interactions, and it is the preferred physical setting for the structure.
Fields, their local interactions, symmetries and causal constraints supply
propagation, binding, record formation and recombination before any measure of
breadth is chosen.

The program's finite models — classical chains, chemical networks and small
quantum circuits — are exact calibration cases for the structure, not claims
about its ultimate form. The next physical step is a small regulated field
model, with its spatial resolution, cutoffs, boundary conditions and
environment stated, built when a specific question requires it.

---

## Formal notes

*These notes state the constructions of the chapter precisely. They are written
for readers who want the definitions in full.*

### F1.1 Finite quantum specification

A finite closed quantum model is specified by

\[
\mathsf P=(\mathcal H,\{\mathcal A(R)\},\mathscr G,H(t)),\qquad
\rho_\Sigma\ge0,\quad\operatorname{Tr}\rho_\Sigma=1,
\]

where \(\mathcal H\) is the Hilbert space, \(\mathcal A(R)\) the observables
associated with physical regions R, \(\mathscr G\) the constraints and
physical identifications, and H(t) the Hamiltonian. Propagation satisfies

\[
i\hbar\,\partial_tU(t,s)=H(t)U(t,s),\qquad
\rho_t=U(t,0)\rho_\Sigma U(t,0)^\dagger .
\]

The structure from Σ over horizon T is

\[
\Omega_{\Sigma,T}=\bigl[\mathsf P,\rho_\Sigma,
\{U(t,s):0\le s\le t\le T\}\bigr]_{\sim},
\]

with ∼ a declared physical equivalence. A passive change of description must
transform state, law, observable structure and readout together; rotating the
state alone while holding the apparatus fixed changes the physics. The full
propagator family, not only U(T, 0), is retained, so that idle and
out-and-back developments with equal endpoints remain distinct.

### F1.2 Composition with residual states

At a classical interface, a stage is described by a subnormalized kernel
J_r(x, y): the probability of record r and residual state y from x. A physically
implemented second stage composes as

\[
J_{s\circ r}(x,z)=\sum_y J_r(x,y)\,J_s(y,z).
\]

When time and resources are resolved, composition also sums over their
compatible splits, with the second stage's deadline and budget reduced by what
the first consumed. A second stage may depend on the record r but not on the
residual y except through physically available records. Failed and unfinished
outcomes retain their mass and residual state.

### F1.3 Predictive equivalence

For a declared family 𝒯 of admissible physical tests,

\[
p\equiv_{\mathcal T}q
\iff
\operatorname{Law}(\tau[p])=\operatorname{Law}(\tau[q])
\ \ \text{for all }\tau\in\mathcal T,
\]

and

\[
d_{\mathcal T}(p,q)=\sup_{\tau\in\mathcal T}
\operatorname{TV}\bigl(\operatorname{Law}(\tau[p]),\operatorname{Law}(\tau[q])\bigr)
\]

is a pseudometric. Enlarging 𝒯 refines ≡. The relation d ≤ ε is not
transitive; the triangle inequality bounds the separation of two laws each
within ε of a third by 2ε. A deterministic encoding q with update F is faithful
when an abstract update F̄ satisfies q∘F = F̄∘q; stochastic and quantum versions
are analogous, and resource costs and accessible records must factor through
the same quotient.

### F1.4 Histories and decoherence

For exhaustive orthogonal projector families at declared times, the class
operators and decoherence functional are

\[
C_\alpha=P^{(n)}_{a_n}U_{n,n-1}\cdots P^{(1)}_{a_1}U_{1,0},\qquad
D_{\alpha\beta}=\operatorname{Tr}\bigl(C_\alpha\rho_\Sigma C_\beta^\dagger\bigr).
\]

A coarse alternative A has C_A = Σ_{α∈A} C_α and weight
D(A, A) = Σ_{α,β∈A} D_{αβ}; off-diagonal terms make this weight non-additive in
general. Medium decoherence, D_{αβ} = 0 for α ≠ β, makes the family classical
with probabilities D_{αα}, but does not select the family. In an exact
pure-state model, orthogonal record projections R_h certify a history family
through R_h ψ_T = C_h ψ_Σ; physical provenance still requires the recording
interactions to belong to the model.

### F1.5 Field theory

In local quantum field theory a state is a normalized positive functional on the
algebra of observables, more general than a density matrix. Typical local
algebras are of von Neumann type III, so a finite matrix trace does not carry
over to the continuum. Real-time (Schwinger–Keldysh) methods and process tensors
are representation tools for this setting; their slots for hypothetical
operations do not add physical alternatives unless the operations are
implemented.

---

## For alignment

An AI system's world model is a compression of this structure. Section 1.6 gives
the standard such a model must meet: it is adequate for a decision only if it
preserves the joint relations that decision depends on, under the operations the
system might actually perform. Sections 1.3 and 1.4 name the failures a capable
optimizer can exploit when that standard is not met: treating separately
feasible commitments as jointly feasible, treating a permitted transformation as
a ready one, and treating a summary as if it determined what follows.

---

## Status

| Status | Claims in this chapter |
| --- | --- |
| **Established** | The structure as the state, law and developments of a physical model. Classical path laws and quantum unitary evolution. Decoherence and record formation. Failure of summaries under the three-sign example. Non-transitivity of approximate equivalence. |
| **Adopted** | The physical possibility structure as the object of ethics. Field theory as the preferred physical setting. |
| **Open** | A general relativistic quantum construction of the structure. Physical selection of history families beyond finite models. |
