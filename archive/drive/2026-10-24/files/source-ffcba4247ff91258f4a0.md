# 11 — Evidence and research program

The program is built so that it can fail. This chapter records what has been
shown, how strongly, and what remains to be shown, and it sets out the research
that would decide the open questions. Its centre is the Gradient Ethics project:
the work needed to establish whether lushness, the measure of chapter 4, ranks
the world the way the ethics of chapters 5 to 9 requires, and to make that
ranking usable by real systems.

The chapter reaches four conclusions. First, the evidence so far is of three
kinds, which must not be confused: established mathematics, exact worked
examples under stipulated laws, and finite probes of physical models. The first
is secure; the second shows that the measure can register the distinctions the
ethics cares about; the third shows that physical organization changes weighted
breadth in some models and not in others. None of them yet shows that the
measure selects generativity over noise and pathology in the complex, coupled
systems the ethics concerns. Second, the decisive tests are adversarial:
searches for worlds in which high lushness and recognizable badness coincide,
run under a protocol fixed in advance. Third, the most promising route to the
program's central hypothesis now runs through established mathematics of
transport networks, which shows how organization across scales changes the cost
of supplying distributed activity; what remains is to carry that change through
to weighted continuation. Fourth, the alignment framework needs engineering
before it can be applied rather than only specified, and the work has a
definite order: reproducible benchmarks, exact adversarial comparisons, one
resource-accounted mechanism, and then estimators of lushness validated against
those exact cases.

---

## 11.1 How to read the evidence

Claims in this manuscript carry one of several statuses, and the evidence for
each is of a different kind.

- **Established mathematics and physics.** Results proved or measured
  independently of the program: the chain rule of information theory, the
  uniqueness of Shannon entropy within its class, decoherence, the Bellman
  recursion. These are secure, and the program's contribution is to apply them.
- **Exact worked examples.** Small models with stated laws, computed exactly by
  the chain rule, each built to isolate one mechanism. They show what the
  measure does under laws stipulated to contain that mechanism. They do not show
  that the world's laws contain it.
- **Finite probes.** Stylized physical models — lattice gases, reaction
  networks, small quantum circuits — in which the program's quantities were
  computed. They test whether organization changes weighted breadth under laws
  closer to physics, and they have produced negative results as well as positive
  ones.
- **Hypotheses and the central wager.** Claims the program stakes but has not
  shown, each paired with the test that would decide it.

Three rules govern all of the work. Organization enters only through the native
law: no model may award a bonus to structure, cooperation or complexity, and any
advantage must come from the dynamics. Comparisons are made against matched
references: same law, same material and energy, same declared resolution, with
construction, transport and maintenance charged. And the strength of a claim is
fixed before the result is seen, so that a favourable frame cannot be chosen
afterwards.

---

## 11.2 What the exact examples show

Fifteen exact examples appear in chapters 4 to 10. Each is computed by a script
that accompanies the manuscript, and each reproduces its reported values to the
stated precision.

| Example | Chapter | Question | Result under its stated model |
| --- | --- | --- | --- |
| E1 | 4 | Does building beat acting? | Building loses at short horizons and wins after a crossover; the best investment grows with the horizon. |
| E2 | 4 | Maintenance, ruin or disruption? | Ruin leads for ten steps or more, then falls behind; a disruption built to reopen growth leads in the limit. |
| E3 | 4 | Does lushness see hidden structure? | It registers a three-way correlation exactly when the dynamics use it. |
| E4 | 4 | What does a closed system allow? | The equilibrium identity holds; a good start leaves a lasting offset of +0.42 bits. |
| E5 | 4 | Is quantum breadth unique? | No: an idle qubit has breadth 1 in one basis and 2 in another. |
| E6 | 6 | What shapes can harm take? | A wound costs a fixed 59.5 bits; an amputation costs rate; destroying repair is invisible at first and worst in the end. |
| E7 | 6 | Is turnover loss or maintenance? | Loss for the individual; maintenance for the niche, whose rate peaks at moderate turnover. |
| E8 | 6 | Does aversive signalling help? | An accurate signal gives the lushest life; a constant one the poorest; the ranking depends on withdrawal having a cost. |
| E9 | 6 | Is obstructed suffering less lush? | Yes against the matched awake arm, by its developmental trace; against anaesthesia the comparison is delicate. |
| E10 | 7 | When does sharing a commons pay? | Crisis priority and rotation lead domination for millions of steps; with fixed capacity domination leads narrowly in the limit; a channel-opening wager reverses this above a break-even probability. |
| E11 | 8 | Contain or remove an uncertain process? | Short horizons favour leaving it; reliable containment wins in the long run; removal is licensed above a credence threshold. |
| E12 | 8 | Many lives or few? | The population optimum is interior, set by subsistence cost, in a model without interaction. |
| E13 | 9 | How strongly to commit? | The recursion over beliefs values evidence still to come; caution emerges without a separate reward. |
| E14 | 9 | Keep oversight or act alone? | Reliable, cost-free oversight is worth keeping short of certainty; its value falls with cost and unreliability. |
| E15 | 10 | Does choice matter if everything happens? | Two policies with identical support differ by 1,123.3 bits at 1,000 steps. |

Read together, the examples show that the measure registers the distinctions the
ethics depends on: investment against noise, recoverable against irreversible
loss, accurate against decoupled signalling, sharing against domination,
containment against removal, evidence against haste, and weight against mere
occurrence. They also record where the measure's verdict depends on a modelling
choice: E2's short-horizon preference for ruin, E8's reversal when withdrawal is
free, E9's delicate comparison with anaesthesia, and E10's dependence on whether
new channels can open. Those dependences are results, not loose ends. Each marks
a place where a stronger model, or a closer look at physics, has to decide.

What the examples cannot show is that real dynamics have the shape the examples
stipulate. That is the work of the finite probes and of the research program
below.

### The scripts

| Examples | Folder | Entry point |
| --- | --- | --- |
| E1–E5 | `ch4_examples/` | `ch4_examples.py` |
| E6–E9 | `ch6_examples/` | `ch6_examples.py`, with `e8_valence.py` and `e9_obstructed.py` |
| E10 | `ch7_examples/` | `ch7_examples.py`, calling the `e10_*.py` modules |
| E11–E12 | `ch8_examples/` | `ch8_examples.py`, calling `e11_excision.py` and `e12_population.py` |
| E13–E14 | `ch9_examples/` | `ch9_examples.py`, calling `e13_commitment.py` and `e14_deference.py` |
| E15 | `ch10_examples/` | `ch10_examples.py`, calling `e15_choice.py` |

Each entry point runs its examples and writes the results to a JSON file in the
same folder. The scripts are written in Python, with NumPy and SciPy where
linear algebra is needed and exact rational arithmetic where precision demands
it. Each folder runs in under three minutes on an ordinary computer. The scripts
and a record of their verification are to be published together as the
benchmark package of section 11.6.

---

## 11.3 What the finite probes show

Before this manuscript, the program ran a series of finite probes of physical
models. Their reports are kept in the program's research notes. The results
that bear on the argument are these.

**Information is not access.** Probes with matched information content showed
arrangements that differ in how cheaply they can be decoded and repaired, and
laws with identical event counts that differ in how records couple to responses.
In exhaustive surveys of small model worlds, most pairs of arrangements holding
equal information differed in what they later made accessible (chapter 2). This
is the finite basis for treating access, not information, as the locus of
difference between options.

**Placement changes breadth in a reaction network.** In a closed two-compartment
reaction model with an autocatalytic channel, adapted from published reactive
lattice-gas chemistry (Boon et al. 1996), two preparations with the same
molecules, occupancy and stationary probability placed the enabling molecules
differently. Over a window of four time units, after four units of development,
the preparation ready for catalysis exceeded the separated one by 4.34 bits of
expected fresh history entropy, the stationary reference by 3.29 bits and a
matched-composition reference by 1.37 bits. The advantage has boundaries:
transport rate and observation interval can reverse the ranking, and the runs
did not show sustained autocatalytic multiplication.

**Matching can change the answer.** In a lattice-gas model, some organized
preparations exceeded a broad stationary reference, but an audit found
additional conserved quantities on the tested lattices. Comparisons that crossed
those conserved sectors could not establish a matched thermal advantage. The
lesson is methodological: a reference that is not matched on every conserved
quantity can manufacture an advantage.

**Production can outlast its producer.** A catalytic model showed descendant
structures continuing to catalyze after the initiating structure had gone. In
that model, stronger catalysis also accelerated reversal, so the extra
descendant continuation largely offset shorter original survival, and there was
no overall gain in persistence.

**Quantum readouts are not unique.** Finite quantum tests showed that an idle
qubit has different breadths in different bases, that a convenient reference
construction can suppress the growth being measured, and that discarding
coherent cross terms needs a physical justification. These are obstructions to
proposed readouts, and they define what a general quantum construction must
satisfy (chapter 4, section 4.8).

**Negative results.** An earlier decision prototype scored 5 of 6 on a test
suite where direct optimization under the same guards scored 35 of 36; it is
recorded as evidence against that candidate, not as validation of the present
theory (chapter 9). An earlier cellular-automaton pilot did not establish a
preferred ranking, because signed responses could cancel and its invariant
assumptions needed correction. A reported toy model of tools enabling tools,
supplied from outside the program, has not been reproduced.

Together, these probes support links in a chain: organization changes how
information can be used and repaired; production changes later enabling; and in
at least one reaction model, placement changes weighted breadth. They do not
connect those links in a single resource-accounted model, and they do not show
that the chain compounds in nature.

---

## 11.4 The Gradient Ethics project

The operational heart of the framework is the claim that lushness, assessed at
the furthest resolvable horizon, ranks the world as Gradient Ethics requires:
that the breadth which dominates over long horizons is generative rather than
pathological. Establishing or refuting that claim is the program's main work.
It has four parts.

### Adversarial search

The central wager (chapter 5) is decided adversarially. The task is to build
models of the structure and search them for configurations in which high
lushness and recognizable badness coincide. Six targets are decisive.

- **Equal-breadth, different-consequence pairs.** Physically different
  developments with equal lushness over the declared comparison, but with
  independently identified differences in harm, recovery or agency. Lushness
  compresses a structure into one number, and this is the most direct test of
  what the compression leaves out.
- **The isomorphic pair.** The strongest case of the first target: two worlds
  with identical branching structure at every resolution, one recognizably good
  and one recognizably bad.
- **Noisy failure.** A lawful variant in which failure modes multiply and
  outscore maintenance. E2 shows this happening at short horizons and reversing
  in the limit; the target is a case in which it does not reverse.
- **Breadth-neutral domination.** Concentration of access in a few at no cost to
  total lushness (chapters 5 and 7).
- **Obstructed suffering.** Suffering decoupled from narrowing that does not
  lose to the same obstruction without suffering. E9 settles the comparison with
  an awake agent under its model; the comparison with unconsciousness, once
  trauma and lasting harm are modelled, is still open (chapter 6).
- **The thin world and the monster.** A thin existence, or a single dominant
  valuer, that extracts more lushness from the same gradient than a plural
  ecology does (chapter 8).

The search must be run under a protocol fixed in advance, because a search that
chooses its frame after seeing the results can find whatever it wants.

> **Preregistered rejection criterion.** Before computing any breadth, declare
> the physical frame, the range of horizons, how resources are matched, and the
> independent grounds for judging a development worse, such as increased
> preventable suffering or reduced recovery and agency of the valuers affected,
> with any compensating opportunities included. Then compare a maintained
> arrangement with a lawful variant. If the variant robustly increases lushness
> while worsening those independently judged consequences throughout the
> declared comparison, reject the unrestricted rule that greater lushness is
> better.

The evidence a rejection needs depends on the scope of the claim under test, and
the burden is declared in advance with the rest of the protocol.

- **A claim about a bounded horizon** is refuted by a sound counterexample
  within that horizon.
- **A claim about a complete finite development** requires the development to
  be followed to its end.
- **A claim about the long run** requires the limiting comparison to be
  established, or the unresolved remainder of the comparison to be bounded
  (chapter 8).

E2 shows why this matters: ruin leads maintenance for ten steps or more and
loses in the limit. Without a declared burden, either side could move the
goalposts — a proponent by appealing indefinitely to a later reversal, a critic
by treating an early reversal as decisive.

One sound counterexample within the declared scope defeats the unrestricted rule
there. What fails is the central wager in that regime: the claim that, because
no one knows where on the structure value lies, ranking the structure by its
lushness is the prudent course. Lushness remains a physical measure. Repeated
failures across representative cases would retire that prudential ranking as the
program's general default. A narrower claim, made after a failure, must state
its domain and face new tests rather than selecting a favourable frame after the
fact. The criterion tests the ranking and its declared scope; it does not test
the premise that value depends on the conditions that support valuers.

One further caution applies to every comparison. Matching complete path entropy
in advance would force equal lushness by definition, so it cannot test whether
one arrangement exceeds another. What is matched must be the inputs: law,
resources, resolution and, where needed, an early-time control. The later
development is then allowed to differ.

### When organization beats noise

The ethics needs organized, generative processes to beat thermal noise and thin
existence over long horizons. The program has calibrated this only in stylized
models. The general question is now sharp, because the chain rule reduces it to
a single inequality.

> **When a preparation beats its matched reference**
>
> \[
> \ell_T(\text{org})-\ell_T(\text{ref})
> =\sum_{t=0}^{T-1}\Bigl(\mathbb E_{\rm org}[g(X_t)]
> -\mathbb E_{\rm ref}[g(X_t)]\Bigr)>0
> \]
>
> ℓ_T is log lushness over T steps, g(x) the branching in one step from state x
> under the common law, and the expectations are taken along the two
> developments.
>
> *In words: an organized preparation beats its matched reference exactly when,
> summed over the horizon, the states it leads to branch more than the states
> the reference leads to.*

The identity is established (formal note F11.1). What it leaves open is why any
class of physical arrangements should make the sum positive. That has to be
derived from what the arrangements do — deliver resources, persist, enable
further transformations — not assumed by giving organized states a higher g.

Two considerations shape the answer. The first is finite mixing. Under a common
law on a finite state space that eventually forgets its starting point, initial
organization can buy only a lasting offset, never a different long-run rate
(chapter 4). A sustained rate advantage therefore requires escape from those
common-forgetting conditions. A fixed law with dynamically separated regimes,
in which different preparations settle into different closed classes, is one
route; resource-accounted growth is another. Neither guarantees an advantage,
and the program investigates both. Finite construction and compounding remain
worth studying even where no indefinite advantage is possible.

The second consideration is activity. Organization that sustains more lawful
activity from the same resources may be exactly how it generates greater
lushness, so activity is a mechanism to be explained, not an effect to be
subtracted. Two comparisons are therefore needed. The primary comparison
matches physical inputs and lets activity, persistence and breadth emerge. A
mechanism control compares against an alternative matched in activity, to
determine how much of an advantage comes through activity and how much through
other changes. An advantage that comes through activity remains an advantage;
the control explains it rather than removing it. Activity also does not add
branching by itself: deterministic activity adds none.

### Organization across scales

Chapter 8 conjectured that organization nested across scales extracts more
generativity from a gradient than organization confined to one scale. There is
now a concrete route to that conjecture through established mathematics.

West, Brown and Enquist (1997) derived how the metabolic rate of organisms
scales with body mass from the geometry of the networks that supply them. Their
model rests on three assumptions: the network branches so as to fill the space
it serves; its terminal units, such as capillaries, have the same size in every
organism; and the network minimizes the energy spent on transport. From these it
predicts that metabolic power B grows with body mass M as M to the power 3/4.
The mathematics connects physical geometry to the cost of delivering resources
and maintaining the activity they support, and later work has generalized it to
asymmetric networks, showing how the scaling depends on network geometry and
flow (Brummer, Savage and Enquist 2017). The program uses this as a starting
family of physical constraints, not as a foundational constant.

The route from such a network to lushness runs through four links:

> network geometry → resource delivery → enabled physical transitions →
> weighted continuation breadth

Transport mathematics supplies the first two links. The last two require a model
of what the supplied sites actually do. A network feeding deterministic clocks
and a network feeding stochastic chemistry can have identical transport
properties and very different breadth, so transport efficiency alone cannot
settle the question.

The scaling law also contains a trade-off that the program has to resolve rather
than assume away.

> **Splitting a body under the three-quarter law**
>
> \[
> N\,B\!\left(\frac{M}{N}\right)=N^{1/4}\,B(M)
> \]
>
> *In words: under the idealized law, dividing a total mass into N separate
> organisms raises total metabolic demand by a factor of N to the one-quarter;
> the integrated organism is cheaper to run per unit of mass.*

Distributed arrangements have greater total throughput; integrated ones have
cheaper maintenance (formal note F11.2). Greater throughput may support more
activity, and cheaper maintenance may free resources for construction or longer
persistence. Neither advantage alone determines lushness. It follows that the
transport mathematics cannot by itself establish that a plural ecology defeats
a single dominant valuer: a single organism can already contain an elaborate
network spanning many scales. The relevant distinction is physical architecture
and its consequences, not how many individuals are named.

The program's hypothesis contains two mechanisms, and they should be tested
separately:

- **Distribution across space and scale.** Hierarchical networks reach sites
  that would otherwise be inaccessible, at manageable transport cost. The
  transport mathematics applies directly here.
- **Complementary use of resources.** One process makes materials or remaining
  free energy accessible to another, enabling further processes. This needs a
  model of transformations and exchange as well as transport, with energy fully
  accounted for, since the same available work cannot be spent twice.

Three things must be fixed before the first result can be meaningful.

1. **The exchange mechanism.** Delivering nutrients, conducting heat,
   distributing power and passing reaction products impose different
   constraints. The first model should use one established local mechanism; a
   general "coupled surface" does not determine the equations.
2. **The comparison class.** Beating an unorganized reference with the same
   resources is an existence result. Beating every equally resourced arrangement
   confined to one scale is much stronger. Beating every concentrated
   arrangement is stronger still and may be false. The three claims should be
   pursued in that order.
3. **The horizon and growth regime.** A finite network can show construction
   paying for itself, repeated enabling and substantial gains in breadth. Under
   a common finite mixing law, it cannot keep a different long-run rate, so an
   open-ended claim needs dynamically separated regimes or resource-accounted
   growth, declared in advance.

The first result the program aims for has this shape:

> Under specified transport and reaction laws, a hierarchy serving complementary
> resource niches produces greater complete-development lushness than a matched
> reference, over a stated range of scales and horizons, after accounting for
> construction and maintenance.

That would establish a mechanism by which generativity drives lushness, without
claiming that every hierarchy, every form of biodiversity or every cooperation
must win. The demanding part is showing that the result survives reasonable
changes of geometry, rates and reference. The aim is first a robust conditional
theorem, and then to find out whether its conditions describe a narrow exception
or a broad physical tendency.

### Norms, commitments and channels

Chapters 6 to 9 derived familiar norms from the measure in small models:
weigh lost rate above lost offset, protect recovery, cooperate where coupling
widens joint access, forgive under noise, contain rather than excise, commit as
far as the evidence supports, keep reliable correction. Each derivation should
be repeated in models with richer dynamics, so that the norms are tested rather
than illustrated. Two questions from chapter 7 are central: what physical
processes supply new channels of generativity, at what cost, and how a bounded
agent should estimate both their chance and their value. The answer decides,
in cases like E10, whether sustaining several agents beats protecting the
commons.

---

## 11.5 Engineering for alignment

The alignment framework of chapter 9 specifies what an aligned system should
protect, prefer and correct. Applying it requires engineering that does not yet
exist.

- **Estimators of lushness with stated error.** Realistic systems cannot compute
  complete path entropy. They need estimators whose errors are known, so that a
  system can say how much of a comparison it has actually resolved. Error has
  several sources that must be reported separately: numerical approximation,
  sampling, coarse-graining, truncation of the horizon and mismatch between the
  model and the world. A tight numerical interval is not a bound on omitted
  physics.
- **World models adequate to the decision.** Chapter 1 set the standard: a model
  is adequate only if it preserves the joint relations the decision depends on,
  under the operations the system might perform. Tests should check whether a
  system treats separately feasible commitments as jointly feasible, a permitted
  transformation as a ready one, or a summary as if it fixed what follows.
- **Horizon-adequacy audits.** Comparisons of a system's planning horizon with
  the persistence of its actions' effects, as E13 does in miniature.
- **Oversight tests.** Measurements of whether a system keeps reliable channels
  of correction intact when it could cheaply degrade them, and how it responds
  when it judges a channel defective.
- **Better correction channels.** Correction that is reliable, cheap and hard to
  compromise, since corrigibility is only as valuable as the correction
  available.
- **Shared benchmarks.** Comparison with existing measures of side effects and
  preserved capability, such as relative reachability (Krakovna et al. 2019) and
  attainable utility preservation (Turner, Hadfield-Menell and Tadepalli 2020),
  which are close to the harm signature of chapter 6.
- **Decision theory under physical models.** A justified matching rule, or a
  precise obstruction, and its interface with the decision recursion; Newcomb's
  problem stated as an explicit physical model.

One problem lies beyond all of these: **installation**. Specifying a standard is
not the same as making a system hold it. The program does not claim to have
solved installation.

---

## 11.6 The order of work

The projects of sections 11.4 and 11.5 depend on one another, and the order in
which they are done matters.

1. **A reproducible benchmark package.** Every example and probe, linked to its
   exact source, its version and a record of its verification, so that anyone
   can rerun it and check the reported values.
2. **Adversarial comparisons where lushness can be computed exactly.** The
   targets of section 11.4, first in models small enough to calculate without
   approximation.
3. **One resource-accounted mechanism.** The conditional theorem of section
   11.4, linking transport and complementary resource use to lushness, with
   construction and maintenance charged and activity controls in place.
4. **Estimators.** Developed and validated against the exact cases of the first
   three steps, then extended to physical systems where exact computation is
   impossible.

Estimators come last not because they matter less, but because an estimator can
only be trusted once it has been checked against cases where the answer is
known.

---

## 11.7 Foundations and the long range

Several questions concern the foundations of the program rather than its
immediate use.

- **A general quantum construction.** Fix the native physical process and test
  any proposed quantum lushness against equivalent descriptions, analytical
  checkpoints, actual record formation, inert ancillas, independent copies and
  erasure. Either exhibit a construction that survives those tests or show
  precisely which requirements conflict (chapters 1 and 4).
- **A field-theoretic model.** A small regulated field model with stated
  resolution, cutoffs, boundaries and environment, built when a specific
  question requires it (chapter 1).
- **Resolution.** Whether a single ranking holds across resolutions, and whether
  durable records select a privileged coarse-graining (chapter 4).
- **Similarity between futures.** Whether the full structure needs a measure
  that registers how different two futures are, with lushness as its limiting
  case (chapter 4).
- **The ultimate frame.** A mathematical construction of the closure at which
  comparisons across frames are justified (chapters 2 and 10).
- **A universal bound on branching.** Whether any physical ceiling limits the
  branching rate of the universal continuation, connecting clock, region, growth
  and quantum description (chapter 9).
- **Orientation and observers.** A measure over orientations, and whether
  weighting oriented developments by the trajectories they support predicts the
  extent of our low-entropy past; whether a separate account of situated
  expectation is needed (chapter 10).
- **Perspective and experience.** How physical limits of integration and access
  correspond to distinct subjects, where one perspective ends and another
  begins, and what the strong sense of experience would require (chapter 10).
- **Identity across substrates.** Whether a reconstruction on a different
  substrate can reproduce an original's generative capacity (chapter 8).
- **Dense organization.** The originator's conjecture of a singularity-like
  limit of densely organized identity needs definitions of density, vortex and
  singularity before it can yield predictions (chapter 8).

---

## 11.8 What success and failure would look like

Success need not take the form of a single universal number. A transferable
physical representation of the structure, a valid partial comparison, a finite
mechanism for compounding breadth with its conditions stated, or an
impossibility theorem showing that two of the program's demands conflict would
each be real progress. Additional machinery that only renames an existing
difficulty would not.

Failure is also defined. If the adversarial search finds bad high-lushness
worlds in some regime, the central wager fails there. Lushness would remain a
well-defined physical measure; what would fail is the prudential ranking of the
structure by lushness in that regime, and Gradient Ethics would have to restrict
its claim or identify what the measure misses. If organization does not beat
matched references under any reasonable physical mechanism, the generativity
hypothesis fails, and with it the program's account of why the familiar norms
follow from the measure. The program is built so that these outcomes are
possible, and the protocol of section 11.4 is how it would find out.

Some of the payoff does not depend on the ethics at all. Characterizing how
organization reshapes physical possibility — how structure changes what can
follow, at what cost, and over what horizon — is valuable science even if the
unrestricted ethical ranking fails.

---

## Formal notes

*Written for readers who want the definitions in full.*

### F11.1 The matched-reference criterion

For a finite Markov law K with step entropy g(x) = H(K(x, ·)) and a preparation
μ, two quantities must be distinguished. The complete joint entropy is
H_μ(X_{0:T}) = H(μ) + Σ_{t=0}^{T−1} E_{μK^t}[g], by the chain rule (F4.2). The
conditional entropy is H_μ(X_{1:T} | X_0) = Σ_{t<T} E_{μK^t}[g]. Omitting X_0
from the recorded sequence is not the same as conditioning on it, so a
comparison must declare which quantity it uses. From an exact present x the two
coincide, since H(δ_x) = 0. A physically randomized preparation contributes
H(μ) as real branching; an analyst's uncertainty about the starting state does
not, and enters the comparison rather than the measure (chapter 9). Under the
conditional form, ℓ_T(μ) − ℓ_T(ν) = Σ_{t<T} (E_{μK^t}[g] − E_{νK^t}[g]). If K
is irreducible and aperiodic on a finite space, μK^t and νK^t converge to the
same stationary law geometrically, so the difference converges to a finite
limit: initial organization buys an offset, not a rate (F4.3). A different
long-run rate requires escape from these conditions: different closed classes
under a fixed law, a growing state space, or a law that is not
time-homogeneous, each of which must be declared and resource-accounted, and
none of which guarantees an advantage. Matching ℓ_T itself in advance makes the
comparison vacuous; matching law, resources, resolution and, where needed, an
early-time window does not.

### F11.2 Scaling under the three-quarter law

If B(M) = cM^{3/4} over the range considered, with c fixed, then for N equal
parts N·B(M/N) = N·c·M^{3/4}N^{−3/4} = N^{1/4}B(M), and metabolic demand per
unit mass is B(M)/M = cM^{−1/4}, decreasing with M. Both statements assume the
same prefactor and that M/N stays within the scaling range. The West–Brown–
Enquist derivation assumes space-filling branching, size-invariant terminal
units and minimized transport energy (West, Brown and Enquist 1997); the
exponent depends on network geometry and flow assumptions when these are
relaxed (Brummer, Savage and Enquist 2017). Metabolic power, thermodynamic
entropy production and path entropy are distinct quantities, and no relation
among them is assumed.

---

## For alignment

This chapter is itself largely for alignment. Its practical content is the list
in section 11.5, taken in the order of section 11.6. The end point of that order
is an estimator of lushness with stated, validated error. Without one, a system
can be told what to protect and prefer but cannot know how much of the relevant
comparison it has resolved, which is exactly the quantity that chapters 8 and 9
make decisive for its licence to act and its reason to seek correction.

---

## Status

| Status | Claims in this chapter |
| --- | --- |
| **Established** | The chain-rule identity for matched comparisons. Under a common finite mixing law, initial organization buys an offset, not a rate. Metabolic scaling from space-filling networks, under its assumptions. |
| **Exact worked examples** | E1 to E15, under their stated models, with scripts. |
| **Finite evidence** | Information is not access. Placement-dependent breadth in a reaction model, with regimes of reversal. Matching on conserved quantities can remove apparent advantages. Descendant production offsetting shorter survival. Obstructions to proposed quantum readouts. A decision prototype recorded as a negative result. |
| **Research program** | Adversarial search under a preregistered rejection criterion, with six targets including equal-breadth, different-consequence pairs and noisy failure, and a burden of evidence fixed by the scope of the claim. A derivation of when organization beats matched references. A conditional theorem linking organization across scales to lushness through transport and complementary resource use. Activity treated as a mechanism, explained by controls rather than subtracted. Norms tested in richer models. Estimators, audits, oversight tests and benchmarks for alignment, in a stated order of work. |
| **Open** | Whether the breadth that dominates is generative rather than pathological. Whether organization across scales beats matched references, and over what comparison class. A general quantum construction. Installation. The foundational questions of section 11.7. |

---

## References cited in this chapter

*Collected with full details in chapter 13.*

- Boon, J. P., Dab, D., Kapral, R., and Lawniczak, A. (1996). Lattice gas
  automata for reactive systems. *Physics Reports* 273(2), 55–147.
- Brummer, A. B., Savage, V. M., and Enquist, B. J. (2017). A general model for
  metabolic scaling in self-similar asymmetric networks. *PLoS Computational
  Biology* 13(3), e1005394.
- Krakovna, V., Orseau, L., Kumar, R., Martic, M., and Legg, S. (2019).
  Penalizing side effects using stepwise relative reachability.
  arXiv:1806.01186.
- Turner, A. M., Hadfield-Menell, D., and Tadepalli, P. (2020). Conservative
  agency via attainable utility preservation. In *Proceedings of the AAAI/ACM
  Conference on AI, Ethics, and Society*, 385–391.
- West, G. B., Brown, J. H., and Enquist, B. J. (1997). A general model for the
  origin of allometric scaling laws in biology. *Science* 276(5309), 122–126.
