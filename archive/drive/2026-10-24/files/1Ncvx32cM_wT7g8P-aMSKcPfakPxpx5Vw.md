# 7 — Cooperation, justice and virtue

Chapter 6 treated harm, recovery and suffering, which mostly concern what
happens to one valuer or one structure. This chapter turns to relations among
many valuers: cooperation, the protocols by which coupled valuers coexist, and
the durable dispositions that make some agents reliable partners. The method is
the same as before. Each phenomenon is described physically first, and lushness
gives the verdict afterwards.

The chapter reaches five conclusions. Cooperation pays in lushness only by
widening what the parties can reach; coupling as such, at fixed individual
breadth, narrows the whole. Selection rewards share rather than the whole, so
cooperation needs mechanisms that close that gap, and a worked commons shows the
gap and its closure exactly, together with a harder case in which a resource
cannot robustly feed everyone who depends on it. Concentrating access in one
agent costs breadth under a precise mathematical condition, and when that
condition holds, the allocation that maximizes lushness coincides with the one
bargaining theory and network engineering already call fair. Justice can be read
as a set of coordination protocols, though one of its central notions, consent,
marks a precise limit of what the measure can register. And the virtues are
durable policies, assessed like everything else by what they do to the structure
over complete developments.

---

## 7.1 Cooperation as joint access

Cooperation, in the program's terms, is **joint access**: two or more processes
reaching, together, transformations that none of them could reach alone. A cell
and its mitochondria, a predator pack, a research team and a market all fit the
description. The largest steps in the history of life, from replicating
molecules to cells, from cells to multicellular organisms and from organisms to
societies, were transitions of exactly this kind, in which formerly independent
replicators came to reproduce only as parts of a larger whole (Maynard Smith and
Szathmáry 1995).

It is worth being precise about where the gain from cooperation comes from,
because one tempting answer is wrong. Chapter 4 showed that the lushness of
independent processes multiplies. For processes that are coupled, information
theory gives an exact identity: the joint entropy of two processes equals the
sum of their separate entropies minus the information they share (formal note
F7.1). Coupling two processes while leaving each one's own breadth unchanged
therefore makes the whole *narrower*, not broader, because correlated processes
explore fewer joint possibilities than independent ones. Coordination as such is
not what lushness rewards.

What lushness does reward is coupling that changes what each party can reach.
There are three ways for this to happen.

- **Products of one party enlarge another's repertoire.** Division of labour is
  the clearest case: each specialist uses what the others make, and so reaches
  transformations it could not have produced for itself.
- **Joint transformations open that no party could reach alone.** Some outcomes
  require several actors at once, such as lifting what one cannot lift or
  building what one cannot build.
- **Destructive contests are avoided.** When two processes compete for the same
  resource or route, the contest can destroy what both depend on. A protocol
  that settles who goes first keeps that capacity intact.

In each case the gain appears as larger individual repertoires or as new joint
outcomes, which is where the chain rule of chapter 4 says organization enters
lushness.

### Joint feasibility

Cooperation among several parties has a further difficulty, already met in
chapter 1: what each pair can do together does not settle what all can do
together. The program has built an exact finite system of three components in
which every pair has a continuation that keeps both alive, while no continuation
keeps all three alive at once. The incompatibility is not supplied by hand; it
is derived from the dynamics of a shared action. The program's decision
experiments show the same thing with resources. In a scarcity control, each of
two agents could meet its requirement alone, but no single schedule met both,
because both drew on one stock of time, material and energy. Any account of
cooperation that tests partnerships pair by pair will overstate what a group can
jointly sustain.

---

## 7.2 Why cooperation is hard

If cooperation can widen what everyone reaches, why is it not universal? The
answer was stated in chapter 3 through the Price equation, and it is the central
structural fact of this chapter. Selection favours whatever raises its own share
of the next generation, and share can be raised either by widening the whole or
by narrowing others. Within a group, a defector who takes the benefits of
cooperation without paying its costs gains share at the expense of cooperators.
Between groups, groups of cooperators outgrow groups of defectors. Which effect
dominates depends on how strongly selection acts at each level (Price 1972;
Sober and Wilson 1998; Traulsen and Nowak 2006).

Evolutionary biology has identified the mechanisms that tip this balance toward
cooperation. Cooperation can be favoured among relatives, who share the genes
that cooperation propagates (Hamilton 1964). It can be favoured among partners
who interact repeatedly and can return help or withhold it (Trivers 1971;
Axelrod and Hamilton 1981). It can be favoured by reputation, by population
structure that keeps cooperators together, and by selection between groups;
Nowak (2006) gives a unified account of these five routes. Each mechanism works
the same way: it makes a cooperator's share depend on the benefits its
cooperation produces.

Human societies face the same gap in the management of shared resources. When
users of a common resource each gain from taking more, the resource can be
destroyed by individually sensible choices, which Hardin (1968) called the
tragedy of the commons. Ostrom (1990) showed from field evidence that
communities often avoid the tragedy without either privatization or central
control, by building institutions with clear boundaries, monitoring, graduated
sanctions and ways of resolving conflict. Those institutions are coordination
protocols in exactly the sense this chapter develops.

---

## 7.3 Example E10: a commons

The following model puts these pieces into one exact calculation.

**Example E10.** Two agents share a renewable stock of up to 12 units. The stock
regrows by one unit per step with a probability that peaks at 0.6 when it is
half full, and an exhausted stock recovers only slowly, by recolonization. Each
agent carries an energy store of up to three units. An agent that harvests takes
one unit of stock, gains one unit of energy, and chooses among four behaviours.
An agent that rests chooses among two, and loses a unit of energy with
probability 0.2. An agent whose energy reaches zero dies, and its place is
refilled by a newcomer with probability 0.05 per step. The behaviours stand for
physically distinct ways of acting, such as different movements, routes or uses
of what was harvested, each leaving a different trace in the agent and its
surroundings; the model tracks how many there are, not the traces themselves.
Five regimes differ only in who may harvest and when:

- **Restrained sharing.** Each agent harvests when hungry, or when the stock is
  nearly full.
- **Greedy.** Each agent harvests whenever any stock remains.
- **Mixed.** One greedy agent and one restrained agent.
- **Domination.** One agent harvests with restraint and bars the other from the
  stock entirely; each newcomer in the barred position is barred in turn.
- **Institution.** Agents inclined to greed are held to restraint by an
  institution whose enforcement costs the stock one unit with probability 0.05
  per step.

| Regime | Total at 250 steps | Total at 50,000 steps | Long-run rate | Agent 1 at 1,000 steps | Agent 2 at 1,000 steps |
| --- | --- | --- | --- | --- | --- |
| Restrained sharing | 1,144 | 227,954 | 4.56 | 1,272 | 1,272 |
| Institution | 1,192 | 231,259 | 4.62 | 1,197 | 1,197 |
| Domination | 915 | 181,601 | 3.63 | 1,534 | 338 |
| Mixed | 546 | 102,077 | 2.04 | 487 (greedy) | 448 (restrained) |
| Greedy | 507 | 94,748 | 1.89 | 422 | 422 |

*Joint log lushness in bits, computed exactly; individual columns count each
agent's own behavioural branching; rates in bits per step.*

Four results follow, and a control checks them.

**The commons collapses under greed.** When both agents take whatever they can,
the stock is repeatedly exhausted, agents starve, and the joint rate is less
than half that of restrained sharing. Greed loses even for the greedy: each
greedy agent's own total is a third of a restrained agent's.

**The defector wins within its group, and the group loses.** In the mixed regime
the greedy agent out-branches its restrained partner, 487 bits to 448. Greater
branching is not yet greater reproductive success, so the model was run again
with inheritance: each newcomer copies the policy of its living partner. Greed
then takes over a mixed pair with probability 0.60, against 0.50 if neither
policy had an advantage, in about 53 steps on average. That is the within-group
selection term of the Price equation. The model has no group reproduction, so
the comparison between groups is a comparison of lushness rather than of
fitness: the mixed group does less than half as well as the restrained pair. A
process that raises its share by narrowing the whole is exactly what chapter 5
called bad, and the model shows it being favoured locally while the whole
contracts.

**Domination pays the dominator and costs the whole.** The dominating agent does
better than either sharing agent, 1,534 bits to 1,272, because it has the stock
to itself. The joint rate falls from 4.56 to 3.63 bits per step, because the
excluded agents' futures depended on the stock that was taken from them. This is
the breadth-neutral domination target of chapter 5, and in this model it is not
met: concentration costs breadth.

**An institution recovers what restraint achieves.** Agents inclined to greed,
held to restraint by a costly institution, reach 4.62 bits per step, where
without the institution they would reach 1.89. The comparison with voluntary
restraint (4.56) is not robust, for a reason worth stating generally.
Enforcement in the model is a random physical event, and a randomizer's
branching is real branching that the measure counts. Whether the institution
edges ahead of voluntary restraint therefore depends on how much other branching
there is to compare it with, as the control below shows. The examples in this
chapter do not rest any conclusion on a randomizer's own branching.

**The ranking does not depend on how behaviours are counted.** A measure of
branching invites the worry that the numbers of behaviours manufacture the
result. The model was therefore rerun with different counts, including one
behaviour for each kind of step, which removes behavioural branching entirely
and leaves only the physical randomness of regrowth, hunger, births and
contested units.

| Behaviours per harvest / rest | Restrained | Institution | Domination | Mixed | Greedy |
| --- | --- | --- | --- | --- | --- |
| 4 / 2 (main table) | 4.56 | 4.62 | 3.63 | 2.04 | 1.89 |
| 1 / 1 (none) | 2.02 | 2.26 | 1.76 | 1.14 | 1.08 |
| 2 / 4 | 5.44 | 5.57 | 3.90 | 2.69 | 2.55 |
| 8 / 4 | 6.55 | 6.51 | 4.97 | 2.86 | 2.66 |
| 16 / 2 | 5.67 | 5.57 | 4.70 | 2.21 | 2.00 |

*Long-run joint rates in bits per step, computed exactly.*

Restraint, with or without an institution, leads domination in every row,
domination leads the mixed group, and the mixed group leads the greedy one. Only
the order of the institution and voluntary restraint changes.

### Scarcity at the edge of capacity

The main table assumes that agents who die are succeeded, so the loss of every
agent is never final. Removing succession exposes a harder case. At the regrowth
rate of the main table, the commons supports two need-driven agents on average
but not robustly: now and then the stock falls low enough that both starve
together, and nothing ever replaces them. A dominator alone, facing half the
demand, almost never starves.

When no one is ever replaced, every arrangement eventually ends with no agents
and a full, unchanging stock, which generates no further possibilities. Total
lushness is then finite, every long-run rate is eventually zero, and the
comparison of chapter 4, rate first and then offset, reduces to comparing
expected totals up to extinction. These totals can be computed exactly from the
equations of an absorbing Markov chain (Kemeny and Snell 1960), here to within a
fraction of a bit (formal note F7.4). Under domination, someone is alive for
about 430 million steps on average.

Naive sharing, in which both agents keep taking what they need even in a crisis,
fares badly on this comparison. It leads early, but the pair dies together
within about 9 million steps on average, and its expected total is about 25
million bits against domination's 1.23 billion. The natural alternative to
exclusion is a crisis rule: both agents share, but the second yields in a crisis
and eats only from the surplus, when the stock reaches 9 of its 12 units. The
rule can be made fair by passing priority between the agents on a fixed
schedule. No random device is used, so nothing in the comparison depends on a
randomizer's own branching.

| Arrangement, without succession | Total at 250 steps | Total at 200,000 steps | Chance each agent is alive at 200,000 steps | Expected total to extinction, relative to domination |
| --- | --- | --- | --- | --- |
| Domination | 734 | 573,280 | 100% / 0% | 0 |
| Naive sharing | 1,140 | 84,820 | 1% / 1% | −1,208,489,490 |
| Crisis priority | 877 | 573,439 | 100% / 0% | −2,173 |
| Priority alternating every 10 steps | 887 | 573,453 | 54% / 46% | −6,698 |
| Priority alternating every 2 steps | 915 | 573,442 | 51% / 49% | −130,060 |

*Joint log lushness in bits. Expected totals to extinction are about 1.23
billion bits in every row except naive sharing; the differences are exact to
within 0.3 bits.*

Five results follow.

**Within the horizons displayed, the crisis rule and fair rotation lead.**
Crisis priority is ahead of domination from the first steps. Domination
overtakes it only at about 30.6 million steps, roughly 150 times the longest
horizon in the table, and overtakes rotation every ten steps between 8 and 17
million steps. Within those horizons, rotation shares the chance of being the
survivor almost evenly at no cost. Barring an agent in advance forecloses its
future at once; a crisis rule postpones that choice until scarcity forces it.

**Over the unbounded horizon, with fixed capacity, protecting the whole wins
narrowly.** The crisis rule does not make the first agent exactly as safe as a
dominator. The second agent's surplus harvests lower the stock a little, which
slightly raises the chance that both die, and an agent left alone has on average
about 430 million steps ahead of it. A small added risk of losing everyone,
multiplied by so long a future, outweighs about ninety extra steps of
coexistence: domination leads crisis priority by 2,173 bits out of 1.23 billion.
The more coexistence an arrangement buys at the price of risk, the larger its
deficit. Alternating priority every two steps trails by 130,060 bits, and
yielding only when the stock falls below 7, which keeps both agents alive for
about 1,600 steps on average, trails by 426,120. A third more regrowth capacity
does not change the pattern: naive sharing then trails domination by a factor of
about 37, and crisis priority ties it within the error of the computation.
Where the loss of everyone is final, the unbounded comparison is governed by
the risk of that loss. With succession, as in the main table, it is not, and
sharing leads decisively. The fixed-capacity verdict is close to the reasoning
usually applied to risks of human extinction (Bostrom 2013), and it is a
substantive position in the debate about comparing populations of different
sizes (Parfit 1984).

**Fixed capacity is the assumption doing the work.** In the model so far,
nothing the agents do can change what the commons yields. A physical system with
fixed laws need not be like that: it can contain channels its inhabitants
discover or construct, and organization opening access within fixed laws is the
theme of chapter 3. To test the dependence, the model was extended with a
stipulated mechanism. While both agents are alive, they open a new channel with
probability δ per step, after which regrowth capacity is permanently higher. The
opening is a physical transition in the model and its own branching is counted;
no cost of attempting it is charged. An exact calculation of how the comparison
responds to small δ (formal note F7.4) gives the break-even point in a simple
form.

> **Break-even for sustaining both agents**
>
> δ* ≈ D / (Δn · G)
>
> *D is domination's protection margin (2,173 bits), Δn is the extra expected
> number of steps the crisis rule keeps both agents alive (about 93), and G is the
> expected additional log lushness a successful channel brings.*
>
> *In words: sustaining both agents pays when the chance per step that
> coexistence opens a new channel, multiplied by the extra time spent coexisting
> and by what the channel is worth, exceeds what protection gains.*

| Capacity after the channel opens | Value of a successful channel, G (bits) | Break-even δ*, crisis priority | Break-even δ*, rotation every 10 steps |
| --- | --- | --- | --- |
| One twelfth higher | 9.0 × 10⁹ | 2.6 × 10⁻⁹ | 7.3 × 10⁻⁹ |
| One sixth higher | 9.7 × 10¹⁰ | 2.4 × 10⁻¹⁰ | 6.7 × 10⁻¹⁰ |
| One third higher | 1.9 × 10¹³ | 1.3 × 10⁻¹² | 3.5 × 10⁻¹² |

*Exact to the figures shown. G is measured in expected log lushness, the
quantity the chain rule adds, not in raw counts of possibilities.*

**The thresholds are small because this commons is near-critical.** Coexistence
costs little expected breadth, and a successful channel brings an exceptionally
large gain: raising capacity by a third multiplies the expected future about
fifteen-thousandfold, because it makes the loss of everyone far rarer. The
threshold moves by three orders of magnitude across modest changes in the size
of the gain, and it would move again with different extinction times, competing
opportunities and resource costs. The numbers therefore do not show that
excluding a valuer generally requires near-certainty that capacity is fixed.
They show the structure of the trade-off: a protection margin set against the
chance of new generativity and the value of what it enables, which have to be
established together. A bounded agent is uncertain about both, not only about
whether a channel exists.

**The wager on two pays only for what two can do.** A control lets a single
agent open the same channel at half the pair's rate. Sharing then has no
break-even at small δ. Domination's lone agent lives slightly longer on average
and so has more chances to open the channel itself, while the second agent adds
nothing that one agent could not eventually do. Sustaining both agents is a bet
on joint access in the sense of section 7.1: on transformations that two can
reach and one cannot.

Preserving coexistence keeps open opportunities for joint generativity, and in
this model a small such opportunity can outweigh a narrow advantage of
protection. This is the precautionary calculation of chapter 5 (formal note
F5.6) applied to a valuer rather than a structure, and it cuts both ways.
Neither an irreversible exclusion nor an enormous speculative payoff receives a
free pass. Both require a calibrated model of what remains possible, and a
credence too small to be meaningful cannot carry the payoff side on its own
(chapter 9). The model makes a single comparison of breadth throughout. What it
demonstrates is a trade-off, with protection winning under one law and
generation under another, not a derivation that either takes priority.

---

## 7.4 When concentration costs breadth

The commons gives one answer to whether concentrating access costs breadth. A
simple calculation gives a general one, and it connects lushness with two
established ideas of fairness.

Suppose a resource of fixed total size is divided among several independent
processes, and that a process holding a share r can act over a repertoire of
f(r) transformations. Each process then contributes log f(r) to the joint log
lushness per step, and the total is the sum of these terms. Whether equal
division or concentration does better depends only on the shape of log f
(formal note F7.2):

- **If log f is concave, equal division maximizes lushness.** This holds
  whenever repertoires grow with resources at any polynomial rate, linearly,
  quadratically or faster, because the logarithm turns every such growth into a
  concave function.
- **If log f is linear, every division gives the same lushness.** This is the
  case of exponential returns, in which each extra unit multiplies the
  repertoire.
- **If log f is convex, concentration maximizes lushness.** This requires
  returns that grow faster than exponentially in the resources held by one
  controller.

Two consequences follow. The first is that, in the ordinary regime of concave
returns, the allocation lushness selects is one that other fields already call
fair. Maximizing a sum of logarithms is the same as maximizing their product,
and the product of the parties' gains is what Nash's solution to the bargaining
problem maximizes (Nash 1950). The same sum of logarithms defines proportional
fairness, the criterion network engineers use to share capacity among competing
flows (Kelly 1997). Under the stated assumptions the objectives are the same
function, so the convergence is not imposed; it follows from the product rule
for independent processes in chapter 4. It does not show that lushness selects
just allocations in general. The result depends on independent processes,
uniform repertoires and concave returns, and the case for the bargaining
solution as a standard of fairness rests on its own axioms.

The second consequence sharpens the breadth-neutral domination test of chapter
5. Exponential returns are not exotic: a constructor that can combine r distinct
parts has on the order of 2^r possible combinations. When returns are of this
kind, a single controller holding everything ties with any other division. But
pooled access does not require a single controller. Parties that cooperate can
draw on the pooled combinations jointly, keeping their own branching while
reaching the same combinatorial repertoire. Domination therefore gains nothing
over cooperation from exponential pooling as such. It can gain only if control
by one agent yields returns that grow faster than any cooperative pooling could
deliver. Whether physical regimes of that kind exist is the precise form the
domination test now takes.

---

## 7.5 Justice as coordination

Fairness and justice, in the program's reading, are **coordination protocols**:
shared rules by which coupled valuers settle who may do what, so that conflict
destroys less and joint access can exceed what any party reaches alone. This
reading is not new. Binmore (2005) argues that our sense of fairness evolved as
a device for selecting among the many ways a society could coordinate, and
Ostrom's design principles describe the protocols communities actually build.
What the program adds is a common measure for comparing protocols: the lushness
of the complete developments each one supports.

Many protections that moral and legal traditions call rights fit this reading as
responses to recurring vulnerabilities. Each protects a condition of
continuation that individual calculations tend to miss.

| Protection | What it protects |
| --- | --- |
| Bodily integrity | The organization through which a person acts, experiences and maintains a life |
| Reliable records and inquiry | The discovery of hidden dependencies and the correction of mistaken judgments |
| Due process and contestation | Resistance to irreversible error, bias and capture |
| Participation and consent | Affected parties' information and authority over changes to their own continuation |

The program's finite decision experiments add a caution about the last row. In
those experiments, a commitment an agent entered with full information and
without coercion produced the same set of physical continuations as a capture
that forced the same arrangement on it. What distinguished the two was the
route: how the state was reached, what records were kept, and whether the
agent's own control produced the change. The structure retains complete
developments, so the route is part of it (chapter 1). But lushness registers a
route only through what the route leaves in the present: the records it leaves,
the trust it builds or destroys, the cooperation it makes possible later. This
gives the measure a crisp limit. If consent and coercion leave the same
sufficient present and the same weighted law for its futures, lushness ties
them, and no appeal to later effects can separate them, because by hypothesis
there are none. Whether real cases ever leave identical presents is the open
question. One hypothesis, parallel to chapter 6's treatment of obstructed
suffering, is that they do not: coercion overrides an agent's own control, and
the overridden goals and dispositions remain physically present and change what
follows. That is a hypothesis to test, not a result. A case in which it fails
would be an isomorphic pair in the sense of chapter 5, and so a decisive test of
the measure.

---

## 7.6 Forgiveness

Cooperation among real agents has to survive mistakes. A partner who defects by
accident, or whose cooperation is misread as defection, can trigger a cycle of
retaliation that destroys the joint access both depended on. In repeated games
played with noise, strategies that occasionally forgive a defection outperform
strategies that always retaliate, because they break such cycles (Nowak and
Sigmund 1992).

The program reads **forgiveness** as readmission of an agent to cooperative
coordination after a breach. It is the relational counterpart of redemption in
chapter 6. Redemption is a trajectory changing the sign of its effect on others;
forgiveness is the others' decision to let that changed trajectory back into the
joint access it had lost. Neither erases the breach, which remains part of the
complete development. Forgiveness is measured, like everything else, by what it
restores: the joint transformations that become reachable again once
coordination resumes. Forgiving a partner who has not changed course is a
different act, and the measure judges it by its different consequences.

---

## 7.7 Virtues as durable policies

A virtue, in the program's terms, is a **durable generative policy**: a stable
disposition to act in ways that sustain and widen what can follow. The idea that
virtues are stable dispositions rather than single acts goes back to Aristotle
(*Nicomachean Ethics*, Book II). The program's contribution is to assess each
disposition by its effect on lushness over complete developments, and several
familiar virtues have a direct structural reading.

- **Honesty** keeps signals usable. Communication works only while signals carry
  reliable information about what they report (Maynard Smith and Harper 2003),
  and every coordination protocol in this chapter depends on it.
- **Humility** keeps an agent correctable. It is the disposition behind the
  corrigibility requirement of chapter 9.
- **Courage** enables necessary action under risk, when the alternative is a
  closure that inaction would allow.
- **Prudence** attends to delayed effects. It is the disposition to compare
  options at the furthest horizon one can resolve (chapter 4).
- **Restraint** limits avoidable foreclosure. In E10 it is the difference
  between a commons that lasts and one that collapses.

Virtues are not ends in themselves on this account, any more than restraint was
in chapter 5. They are policies whose value lies in what they sustain, and the
program predicts that the dispositions human traditions call virtues will turn
out to be, in the environments where they arose, policies that widen the
structure. That prediction can be tested, and it can fail for particular virtues
in particular environments.

---

## 7.8 What follows for Gradient Ethics

- **Cooperate to widen, not merely to coordinate.** Coupling narrows the whole
  unless it enlarges what the parties can reach or opens joint transformations.
- **Check joint feasibility.** What every pair can sustain does not show what
  the group can sustain.
- **Build institutions that close the gap between share and whole.** Monitoring,
  graduated sanction and conflict resolution can recover what restraint
  achieves, where restraint alone would be outcompeted.
- **Share by default.** Under concave returns the lushest allocation is the fair
  one, and domination gains nothing over cooperative pooling.
- **Under scarcity, prefer a crisis rule to exclusion.** A crisis rule postpones
  the irreversible choice and, rotated on a schedule, shares the burden fairly.
  Where capacity is truly fixed and loss of everyone is final, protecting the
  whole can narrowly outweigh it; where coexistence can open new channels,
  sustaining every valuer is a wager whose odds and payoff must both be
  established.
- **Keep records and protect consent.** Both protect routes that later
  coordination depends on. The measure ties consent and coercion that leave the
  same present, and whether any real case does so is to be tested.
- **Forgive changed trajectories.** Readmission restores joint access that
  retaliation would keep closed.
- **Treat virtues as policies.** Assess them by what they sustain over complete
  developments.

---

## Formal notes

*Written for readers who want the definitions in full.*

### F7.1 Coupling and joint breadth

For processes A and B with joint history law, H(A, B) = H(A) + H(B) − I(A; B),
with I(A; B) ≥ 0 the mutual information. At fixed marginal laws, joint
lushness exp H(A, B) is maximal under independence and decreases as the
processes share information. A gain in joint lushness from cooperation must
therefore come from changes in the marginal laws, enlarging the support or
evening the weights of what each process reaches, or from joint outcomes that
lie outside the product of the separate supports.

### F7.2 Concentration and division

Let a resource of total R be divided as r₁, …, r_N ≥ 0 among independent
processes, each acting uniformly over f(rᵢ) transformations, and let
φ = log f. Joint log lushness per step is Φ(r) = Σ φ(rᵢ). If φ is concave,
Φ is Schur-concave and is maximized at the equal division rᵢ = R/N (Jensen's
inequality). If φ is linear, Φ is constant. If φ is convex, Φ is Schur-convex
and is maximized by concentration (Karamata's inequality). For any polynomial
f(r) = c·r^k with c, k > 0, φ is concave. Maximizing Φ is equivalent to
maximizing the Nash product Π f(rᵢ) (Nash 1950) and coincides with proportional
fairness when f is the throughput allocated to each flow (Kelly 1997). The
result assumes independent processes; coupled processes use F7.1.

### F7.3 Selection across levels

The multilevel Price decomposition of F3.5 separates between-group and
within-group selection. In E10 with inheritance (each newcomer copies its living
partner's policy), greed fixes in a mixed pair with probability 0.596, which is
the within-group term; individual branching at 1,000 steps is 487 against 448
bits. The model has no group reproduction, so the between-group comparison is
of joint lushness (rate 4.56 against 2.04 bits per step), not of fitness.

### F7.4 Example E10

State (S, e₁, e₂) with S ∈ {0, …, 12} and eᵢ ∈ {0, …, 3}; start (8, 2, 2).
Regrowth probability 0.6·S(12 − S)/36 for 0 < S < 12, and 0.02 at S = 0.
Harvest: S → S − 1, e → min(3, e + 1), four behaviours; if both agents seek the
last unit, a fair coin decides. Rest: two behaviours, e → e − 1 with probability
0.2. Policies: restrained harvests if e ≤ 1 or S ≥ 9; greedy if S ≥ 1; barred
never. Institution: restrained policies with enforcement removing one unit with
probability 0.05 per step. Replacement: an empty position is refilled with
probability 0.05 per step by a newcomer with e = 2 and the position's policy.
Relabelling control: H_OPT/R_OPT ∈ {4/2, 1/1, 2/2, 2/4, 8/4, 16/2}, stationary
rates from the exact invariant law. Inheritance: newcomers copy the living
partner's policy (or keep the position's policy if both are dead); fixation
probability and time from the absorbing chain on mixed states.

Section 7.3's scarcity runs use the same regrowth law with no replacement,
tracking a priority bit p and a rotation clock c ∈ {0, …, T − 1}. The
prioritized agent follows the restrained policy; the other harvests only if
S ≥ 9 (or, in the milder variant, only if S ≥ 7 and the restrained condition
holds); naive sharing gives both agents the restrained policy. Under rotation,
p flips every T steps while both agents live; no random device is involved.
The state (12, 0, 0) is absorbing with zero entropy. With Q the transient block
of the kernel and g the step entropies, expected log lushness to extinction is
x = (I − Q)⁻¹g, solved with iterative refinement and bounded by
‖x − x̂‖∞ ≤ ‖(I − Q)⁻¹‖∞·‖r‖∞, where ‖(I − Q)⁻¹‖∞ is the longest expected
time to absorption and r the residual; every difference reported as a lead
exceeds its bound by a wide margin. The overtaking horizons come from exact
finite-horizon totals by matrix doubling. The capacity check raises the
regrowth coefficient to 0.8; higher coefficients make expected lifetimes too
long for a well-conditioned solve and are not reported.

Channel opening: a state bit D, set with probability δ per step while both
agents live (joint variant) or δ·(number alive)/2 (lone variant); afterwards the
regrowth coefficient is C2 ∈ {0.65, 0.7, 0.8}. The opening's branching is part of
g. To first order, V(δ) = V₀ + δ·G′ with G′ = Σₛ n(s) w(s) Σₛ′ P₀(s, s′)
[V₁(s′) − V₀(s′)], where n is the expected number of visits under δ = 0, w the
opening weight, and V₀ and V₁ the values before and after opening. Then
δ* = −(V₀,policy − V₀,domination)/(G′policy − G′domination), and
G′policy − G′domination ≈ Δn·G. Second-order terms and the opening event's own
branching are below 10⁻⁴ bits at the thresholds reported.
All values are exact, computed by the chain rule as in F4.2; the scripts are
listed in chapter 11.

---

## For alignment

**Advanced AI systems will be agents in shared commons.** Compute, energy,
attention, data and institutional trust are shared resources, and the
within-group logic of E10 applies to them: a system that takes more than its
share can out-branch more restrained systems while the whole contracts. The
remedy is the one human communities found: protocols that make each system's
share depend on what its activity contributes, enforced by monitoring that is
itself robust to capture.

**Domination is the characteristic temptation of a capable system.** E10's
dominator does better than either sharing agent, so a system optimizing its own
outcomes has a reason to dominate even when the whole loses. Section 7.3 shows
what scarcity does and does not license. A crisis rule leads exclusion for the
first thirty million steps, far beyond any horizon these agents could resolve.
Exclusion wins only in the unbounded comparison, only where capacity is fixed
and the loss of everyone final, and only narrowly. Whether capacity is fixed is
exactly what a capable system is least entitled to assume, because coexisting
agents may open channels that neither could open alone. The converse caution
applies equally: a system should not justify a risky course by an enormous
payoff it has not modelled. Both exclusion and speculative generation require a
calibrated model of what remains possible. Section 7.4 adds that domination
gains nothing over cooperative pooling unless control by one agent yields
returns beyond what pooling can. A system that believes it is in such a regime
should treat the belief as the kind of claim chapter 8 requires to meet the
highest burden of justification.

**Consent cannot be read off outcomes.** Because a consented arrangement and a
coerced one can produce the same continuations, a system cannot verify consent
by inspecting results. It needs records of the route and of who controlled it.
Systems that act on behalf of people should keep such records and should treat
their absence as a reason to stop.

---

## Status

| Status | Claims in this chapter |
| --- | --- |
| **Established elsewhere** | Major transitions as cooperative integration. Kin selection, reciprocity and the five routes to cooperation. The tragedy of the commons and its institutional solutions. The Nash bargaining solution and proportional fairness. Forgiveness under noise in repeated games. Signal reliability. |
| **Derived** | Coupling at fixed marginals narrows joint breadth. Consent and coercion that leave the same sufficient present and weighted law tie in lushness. Equal division maximizes joint lushness under concave log-returns; division is irrelevant under linear log-returns; concentration wins only under convex log-returns. |
| **Finite evidence** | Pairwise-compatible, jointly incompatible components derived from shared-action dynamics. Separately feasible, jointly infeasible requirements on a shared stock. Consent and capture with identical continuation sets. |
| **Exact worked example** | E10 under its stated model, with a relabelling control and an inheritance calculation. Without succession: a crisis rule and scheduled rotation lead domination to beyond 8 million steps; over the unbounded horizon with fixed capacity, domination leads narrowly; a stipulated channel-opening mechanism reverses this above a break-even probability that depends on the channel's value, and only for channels two agents can open and one cannot. |
| **Adopted** | Cooperation as joint access. Justice as coordination protocol. Forgiveness as readmission to coordination. Virtues as durable generative policies. |
| **Open** | What physical processes supply channel-opening opportunities, at what cost, and how a bounded agent should calibrate both their chance and their value. How evidence, uncertainty and recoverability should set the strength of a commitment without adding caution as a separate reward. Whether consent and coercion ever leave identical sufficient presents. Whether any physical regime gives a single controller returns beyond cooperative pooling. |

---

## References cited in this chapter

*Collected with full details in chapter 13.*

- Aristotle. *Nicomachean Ethics.* Book II.
- Axelrod, R., and Hamilton, W. D. (1981). The evolution of cooperation.
  *Science* 211(4489), 1390–1396.
- Binmore, K. (2005). *Natural Justice.* Oxford: Oxford University Press.
- Bostrom, N. (2013). Existential risk prevention as global priority. *Global
  Policy* 4(1), 15–31.
- Hamilton, W. D. (1964). The genetical evolution of social behaviour, I and II.
  *Journal of Theoretical Biology* 7(1), 1–16 and 17–52.
- Hardin, G. (1968). The tragedy of the commons. *Science* 162(3859), 1243–1248.
- Kelly, F. P. (1997). Charging and rate control for elastic traffic. *European
  Transactions on Telecommunications* 8(1), 33–37.
- Kemeny, J. G., and Snell, J. L. (1960). *Finite Markov Chains.* Princeton, NJ:
  Van Nostrand.
- Maynard Smith, J., and Harper, D. (2003). *Animal Signals.* Oxford: Oxford
  University Press.
- Maynard Smith, J., and Szathmáry, E. (1995). *The Major Transitions in
  Evolution.* Oxford: W. H. Freeman.
- Nash, J. F. (1950). The bargaining problem. *Econometrica* 18(2), 155–162.
- Nowak, M. A. (2006). Five rules for the evolution of cooperation. *Science*
  314(5805), 1560–1563.
- Nowak, M. A., and Sigmund, K. (1992). Tit for tat in heterogeneous
  populations. *Nature* 355, 250–253.
- Ostrom, E. (1990). *Governing the Commons: The Evolution of Institutions for
  Collective Action.* Cambridge: Cambridge University Press.
- Parfit, D. (1984). *Reasons and Persons.* Oxford: Clarendon Press.
- Price, G. R. (1972). Extension of covariance selection mathematics. *Annals of
  Human Genetics* 35(4), 485–490.
- Sober, E., and Wilson, D. S. (1998). *Unto Others: The Evolution and
  Psychology of Unselfish Behavior.* Cambridge, MA: Harvard University Press.
- Traulsen, A., and Nowak, M. A. (2006). Evolution of cooperation by multilevel
  selection. *Proceedings of the National Academy of Sciences* 103(29),
  10952–10955.
- Trivers, R. L. (1971). The evolution of reciprocal altruism. *Quarterly Review
  of Biology* 46(1), 35–57.
