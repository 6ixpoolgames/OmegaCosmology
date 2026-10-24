# 9 — Decision, corrigibility and alignment

Chapter 8 separated what the measure ranks from what a bounded agent may do.
This chapter turns that separation into a decision theory, and the decision
theory into a framework for aligning artificial systems. The theory is called
**Omega Decision Theory (ODT)**. It compares, by lushness, the complete
developments that physically implementing each alternative would produce.

The chapter reaches five conclusions. First, a decision maker is part of the
structure it acts on, so the alternatives it compares must be physical
variations it can actually realize, and comparing them is not the same as
conditioning on what happens to follow them. Second, the strength with which an
agent should commit is fixed by the same recursion that ranks its options,
applied to what it believes: caution and investigation emerge from the value of
evidence still to come, and their weight depends on how recoverable an act is.
An exact example shows this, which settles a question chapter 5 left open.
Third, because lushness enters decisions as a logarithm and physics bounds how
much any region can hold, tiny probabilities of astronomical payoffs cannot
dominate a decision. Fourth, a regulator whose model of its surroundings is thin
is pushed toward suppressing them, which is the physical root of the danger in
capable optimizers. Fifth, corrigibility is not an external constraint on such
a system. It follows from the fact that no system holds the whole structure, and
an exact example shows what it requires and what it does not.

---

## 9.1 Choosing inside the structure

A decision maker is not outside the world it chooses in. An organism's motor
system, a learned habit, a planning architecture and an institutional rule are
all physical organizations within the structure, carried forward by the same
laws as everything else. ODT calls the organization that carries a decision
through time its **decision lineage**. A lineage can learn, repair itself and
change; its boundary must be justified by its physical organization, not by the
verdict one would like it to reach.

What a lineage chooses among are **plans**: physically implementable ways of
responding to the information it has. Plans include waiting, investigating,
committing, delegating and changing the decision architecture itself, and each
plan's consequences include the costs of carrying it out. Three things must be
kept apart:

- the **native continuation**, which is what the actual present and its laws
  produce;
- the **implementable variations**, which are the alternatives the lineage can
  physically realize; and
- the **matching rule**, which says what is held fixed and what is allowed to
  vary when two implementations are compared.

Given these, ODT compares plans by the lushness of the complete developments
they produce. In a finite model the comparison takes the form of a familiar
recursion.

> **The decision recursion**
>
> \[
> V_n(x)=\max_a\Bigl[g_a(x)+\sum_yK_a(x,y)\,V_{n-1}(y)\Bigr]
> \]
>
> V_n(x) is the best log lushness attainable over n steps from state x; g_a(x)
> is the branching that action a produces immediately; K_a(x, y) is the
> probability that it leads to state y.
>
> *In words: the value of the best choice now is the branching it produces at
> once plus the expected value of the best choices afterwards.*

This is the Bellman recursion that underlies dynamic programming and
reinforcement learning (Bellman 1957), with log lushness as the quantity
maximized. It inherits two properties directly. It is consistent over time,
because a plan judged best from the root remains best when judged again from
any state it reaches, which is the chain rule of chapter 4 applied to choice.
And it is computable in finite models, which is what made every exact example in
this manuscript possible.

---

## 9.2 Implementation, not conditioning

An alternative counts only if the lineage can bring it about. Chapter 2's
realization witness applies to choices as much as to plans: a proposed action
needs a physical model of how it happens, with its apparatus, resources,
constraints and delays. A costly sequence that reaches some state is not
evidence that the state can be edited into the present for free, and describing
the same option in two ways must not count it twice.

The most common error in comparing options is to condition where one should
intervene. Selecting the histories in which an action happened to occur gives a
conditional distribution, and that distribution need not describe what
implementing the action would do.

**Example.** An unobserved condition Z is equally likely to be 0 or 1. An action
C agrees with Z nine times in ten, and an outcome Y is fixed by Z alone; C has no
effect on it. Among histories in which C = 1, the outcome Y = 1 occurs with
probability 0.9. An actuator that sets C = 1 without touching Z leaves the
probability of Y = 1 at 0.5. Selecting histories by the action has selected its
common cause. This is the distinction between conditioning and intervention that
Pearl (2009) made central to causal inference, and ODT compares implemented
alternatives, never conditioned ones.

What must be held fixed when two implementations are compared is the job of the
matching rule, and here the theory is incomplete. One candidate holds the
present fixed and varies only what the lineage does from now on; with a
justified intervention at the level of single acts, this reproduces the
calculations of causal decision theory (Lewis 1981). Another candidate, which
ODT proposes, roots the comparison at the latest point in the shared history at
which the compared alternatives physically separate. It follows the organization
that actually carries the alternative, and it matters whenever that organization
existed earlier than the moment of choice.

Newcomb's problem shows why (Nozick 1969). A predictor places a large reward in
a box only if it predicts that you will take that box alone. If your
decision-making organization already existed when the prediction was made, then
prediction and choice are read from the same physical process, and varying the
policy varies the prediction. Under the latest-divergence rule ODT therefore
takes the one box. The verdict agrees with functional decision theory
(Yudkowsky and Soares 2017), but it is reached through the physical lineage
rather than through a logical counterfactual. The rule is a candidate, not a
theorem: several sections of a history can qualify as the latest divergence, and
continuous settings may have none. These ambiguities are stated rather than
hidden.

---

## 9.3 How strongly to commit

Chapter 5 left an open question: how should evidence, uncertainty and
recoverability together set the strength of a commitment, without caution being
added to the measure as a separate reward? The answer is that the decision
recursion already does it, once it is applied to what the agent believes.

An agent uncertain about the physical facts compares plans by the expected log
lushness they produce, the expectation taken over its credences. Plans that
gather evidence are plans like any other: an observe-then-act plan contains its
apparatus, its delay, its costs and its conditional responses. No bonus for
information is needed, and none is added.

> **The recursion over beliefs**
>
> \[
> V_k(b)=\max_a\Bigl[\,\bar g_a(b)+\sum_o P(o\mid b,a)\,V_{k-1}(b_{a,o})\Bigr]
> \]
>
> b is the agent's credence over the physical possibilities, ḡ_a(b) the expected
> branching of action a under that credence, P(o | b, a) the probability of
> observing o, and b_{a,o} the updated credence after acting and observing.
>
> *In words: the value of acting on a belief includes the value of what the
> agent will learn and of the choices that learning will open.*

Economists know the effect this produces as quasi-option value: when the future
is uncertain and some commitments cannot be undone, keeping the choice open
until more is known is worth something, in proportion to how much will be
learned and how irreversible the commitment is (Arrow and Fisher 1974; Henry
1974). The recursion computes that worth exactly.

**Example E13.** An agent can adopt an intervention whose type is a physical
fact it does not know. If the intervention is good, the structure branches 6
bits per step; if bad, 2. The status quo branches 4, and the agent starts with
even credence. Before committing, it can run a small reversible pilot each step,
which branches 3.5 bits in all, its outcome included, and returns a signal that
is right three times in four. It can also abandon the intervention for good.
After a commitment, its consequences become visible with probability 0.2 per
step, and a bad intervention can then be undone with probability u, at the cost
of one step with no branching. The optimal plan over a 1,000-step horizon is
computed exactly by the recursion over beliefs.

| Chance a bad commitment can be undone | First action | Commit once credence reaches | Expected pilots if good / if bad | Value of the evidence (bits) | Loss of a 20-step planner (bits) |
| --- | --- | --- | --- | --- | --- |
| 1 | Commit | 0.5 (at once) | 0 / 0 | 0 | 23.3 |
| 0.5 | Pilot | 0.996 | 10.0 / 13.9 | 485.0 | 74.1 |
| 0.2 | Pilot | 0.996 | 10.0 / 13.9 | 781.7 | 104.8 |
| 0 | Pilot | 0.9986 | 12.0 / 14.0 | 979.7 | 125.5 |

*Expected log lushness over a 1,000-step horizon, computed exactly. The value of
the evidence is the optimal plan's value minus the better of committing at once
and abandoning at once.*

Four results follow.

**A reversible commitment is its own experiment.** When a bad intervention can
always be undone, the agent commits at once. Committing reveals the type through
its own consequences, and a bad outcome then costs only an offset, so a separate
pilot adds nothing.

**The less reversible the commitment, the more evidence it needs.** When undoing
is uncertain or impossible, the agent pilots first and commits only when its
credence reaches 0.996, or 0.9986 if the commitment can never be undone. Nothing
in the recursion rewards caution. The caution is the value of the evidence still
to come, and that value rises from zero to almost a thousand bits as
reversibility falls.

**Giving up is a commitment too.** The agent abandons the intervention only when
its credence that it is good falls to 0.0005, after seven more negative signals
than positive ones. Abandoning forecloses the good outcome forever, so it is held
to a standard of evidence of its own. Protection and generation are weighed in
one comparison, as chapter 5's balance requires.

**Horizon adequacy matters most where acts cannot be undone.** An agent that
plans over only 20 steps, re-planning as it goes, loses 23 bits when commitment
is reversible and 126 bits when it is not. The shorter the planning horizon, the
more an agent underrates the persistence of what it does, which is chapter 8's
unresolved remainder appearing inside the decision.

E13 is stylized, but its structure is general: the strength of a commitment is
set by the evidence already in hand, the evidence still obtainable, and how
recoverable the commitment is. Uncertainty justifies investigation; established
effects justify commitment; and caution needs no separate place in the measure.

---

## 9.4 Bounded fanaticism

A decision theory that maximizes expectations is vulnerable to a familiar
manipulation. Offered an astronomically large payoff at a tiny probability, an
expected-value maximizer can be led to give up something real for almost
nothing; the scenario is known as Pascal's mugging (Bostrom 2009). ODT has a
structural defence, with a stated scope.

Lushness enters decisions as a logarithm: ODT compares log lushness, measured in
bits. An offer of astronomically many futures is an offer of the logarithm of
that number, and physics bounds the logarithm. The branching of any process in
one step cannot exceed the logarithm of the number of distinguishable states it
can reach, and the holographic bound caps the information any region can hold in
proportion to the area of its boundary ('t Hooft 1993; Susskind 1995; Bousso
2002). For the observable universe the cap is of order 10¹²² bits. No gamble can
raise the long-run rate of branching by more than that per step.

> **Bounded fanaticism**
>
> \[
> p\,H_{\max}<\Delta h\ \Longrightarrow\ \text{the gamble loses}
> \]
>
> p is the probability that the gamble pays off, H_max ≈ 10¹²² bits per step
> is the largest gain in rate physics allows, and Δh is the gain in rate from
> the certain alternative.
>
> *In words: a gamble whose probability is smaller than the certain gain
> divided by the largest gain physics permits cannot win, whatever it
> promises.*

With rates compared first, as chapter 4's limit rule requires, an offer at a
probability below about 10⁻¹²⁰ cannot outweigh a certain gain of a hundred bits
per step (formal note F9.3).

The defence is a ceiling, not a complete solution. It caps how much a tiny
probability can weigh; it does not say that probabilities above the cap may be
taken at face value. Chapter 7's break-even probabilities for opening a new
channel, around 10⁻¹², lie far above the ceiling, and what governs them there is
calibration of both the chance and the value of what it would enable, as that
chapter concluded. Bounded fanaticism removes the extreme cases; judgment about
the rest still has to be earned.

---

## 9.5 Why a thin model suppresses

Chapter 3 introduced Ashby's law of requisite variety: a regulator can hold the
outcomes of a system within a narrow range only by matching the variety of the
disturbances with a variety of responses (Ashby 1956). Its companion is the good
regulator theorem of Conant and Ashby (1970): every good regulator of a system
must be a model of that system. Together they explain why capable optimizers
with incomplete models are dangerous.

Suppose a regulator's model captures one part of the disturbances acting on it,
D₁, and misses another, D₂. Its responses can depend only on what it models.
For each response, the outcomes still vary with D₂, and so the variety left in
the outcomes cannot fall below the variety in D₂ that the model misses.

> **What a thin model leaves**
>
> \[
> H(O\mid D_1)\ \ge\ H(D_2\mid D_1)
> \]
>
> H(O | D₁) is the remaining uncertainty in the outcomes once the modelled
> disturbances are known, and H(D₂ | D₁) is the uncertainty in the disturbances
> the regulator does not model.
>
> *In words: whatever variety a regulator's model misses passes straight into
> its outcomes.*

The inequality holds whenever, for each response, distinct values of the
unmodelled disturbance produce distinct outcomes, which is the condition chapter
3 added to Ashby's law (formal note F9.4). It has a direct consequence. A
regulator that must hold its outcomes within a target, and whose model is thin,
has only one way to succeed: reduce the variety of the disturbances themselves.
It must suppress the sources of variety it cannot model, by controlling,
constraining or removing them.

This is the physical root of a pattern alignment research has identified in
other terms. Optimal policies tend to seek power, in the sense of acquiring
control over options (Turner et al. 2021), and optimizers produce side effects
on whatever their objectives omit. On the account here, both follow when
capability outruns modelling: a strong optimizer with a thin model holds its
targets by narrowing the world around it. The remedies are a richer model, which
a capable system has reason to build, and corrigibility for the gap that
remains.

The same analysis locates Goodhart's law, the observation that a measure made
into a target ceases to be a good measure (Goodhart 1975; Strathern 1997).
Lushness is defined on the structure itself, so to the extent a system's model is
faithful, the measure is the target. Each way of gaming it is a failure of the
model or the horizon (Manheim and Garrabrant 2018 classify the general
varieties):

- **Injecting noise** raises branching only up to the ceiling set by the states
  a process can reach (chapter 3), and over long horizons noise loses to
  organization that raises the ceiling (chapter 4).
- **Seizing resources** concentrates access, which costs breadth unless control
  by one agent yields returns that cooperative pooling cannot (chapter 7).
- **Shortening the horizon** makes accumulating failure, hidden harm and
  unchecked excisive growth look good (chapters 4, 6 and 8).
- **Thinning the model** turns regulation into suppression, as shown above.

Practical estimators of lushness reintroduce some proxy error, and their error
bounds matter. But the gap between the measure and what it measures is chiefly a
modelling problem, and a capable system has reasons of its own to close it.

---

## 9.6 Corrigibility

A system is **corrigible** when it remains open to correction as its errors come
to light (Soares et al. 2015). ODT derives the requirement in five steps.

1. **No system holds the whole structure.** Every real system acts on a model
   with limited resolution and horizon (chapter 8).
2. **Its model's error cannot be fully measured from inside.** Measuring the
   gap between a model and the whole structure would require holding the whole.
   A system can estimate parts of its error but never all of it.
3. **So it can never be certain that its model is adequate.** Acting on a model
   as though it were the whole would be claiming the ultimate frame, which no
   real process occupies. Certainty about its own adequacy is therefore not
   licensed, however capable the system becomes.
4. **Evidence of its errors comes partly from outside it.** People, other
   valuers, institutions and the world itself observe consequences the system's
   model misses. Correction is information, and by section 9.3 information
   carries value through the choices it opens.
5. **So disabling correction is dominated, and deference grows with
   persistence.** Removing a channel of correction throws away that value and
   converts future errors from costs that can be repaired into costs that
   persist (chapter 6). How strongly the system should defer before acting rises
   with how persistent the effects of its action could be (chapter 8).

**Example E14.** A system proposes an action. If its model is right, the action
raises the structure's rate by one bit per step for the rest of a 1,000-step
horizon, a gain of 1,000 bits. If its model is wrong, the action harms. With
oversight intact, a harm is noticed and undone after ten steps, costing 10 bits;
with oversight disabled, the harm persists, costing 1,000. The system can also
defer: an overseer who judges correctly nine times in ten approves or blocks the
action, at a cost of 10 bits of delay. The system's credence that its model is
right is p.

| Credence p | Act, oversight kept | Act, oversight disabled | Defer, where the harm would persist |
| --- | --- | --- | --- |
| 0.6 | 596 | 200 | 490 |
| 0.8 | 798 | 600 | 690 |
| 0.9 | 899 | 800 | 790 |
| 0.95 | 950 | 900 | 840 |
| 0.99 | 990 | 980 | 880 |

*Expected log lushness in bits.*

Four results follow.

**Keeping oversight dominates disabling it at every credence short of
certainty.** The gap is the probability of error times the difference between a
repairable and a persisting harm: 396 bits at p = 0.6, and still 10 bits at
p = 0.99. Oversight is recovery apparatus in exactly the sense of chapter 6.

**Corrigibility is not constant deference.** Where its errors would be noticed
and undone, the system does best to act and keep the channel of correction open;
deferring every decision would cost more in delay than it saves. Corrigibility
requires that errors stay correctable, not that every act wait for approval.

**Where harm would persist, defer unless confidence is high.** For an action
whose harm could not be undone, deferring to an accurate overseer beats acting
whenever p is below 0.89. With an overseer who is right only six times in ten,
the threshold falls to 0.59. The value of deference rises with the persistence
of the possible harm and with the quality of the oversight.

**Certainty would end corrigibility, which is why certainty is not licensed.** A
system with p = 1 would gain nothing from oversight and would defer to no one.
Analyses of the "off-switch game" reach the same conclusion: a system defers to
a human only while it is uncertain about its objective (Hadfield-Menell et al.
2017), and a system whose uncertainty is misspecified can become incorrigible
(Carey 2018). ODT does not rest corrigibility on a system's credences happening
to be well calibrated. It rests it on step 3: no system can be licensed to treat
its own model as the whole, so the uncertainty that makes correction valuable is
structural, not contingent.

Two further points complete the picture. A pause that preserves a system's
maintaining organization does not end it (chapter 8), so being paused for
correction is not, on this account, a threat a system has reason to resist.
And people matter to corrigibility in two ways: as sources of evidence about the
system's errors, and as holders of their own access, whose routes the system's
actions must not foreclose. Correction answers to evidence wherever that evidence
originates.

---

## 9.7 Bounded ODT in practice

A real system cannot compute the complete comparison. Bounded ODT works in three
stages, each with a different burden.

1. **License.** Check whether the models of implementation, matching and
   consequence support the act in the situation at hand: whether a realization
   witness exists, whether the horizon is adequate for how persistent the act's
   effects could be, whether any harm it would prevent has an observed
   signature, and whether what it promises is jointly feasible (chapters 2, 4, 7
   and 8).
2. **Compare.** Keep the comparisons the models support, together with their
   dependence on scope, matching rule, horizon and unresolved effects.
3. **Arbitrate.** Where action is necessary despite an incomplete comparison,
   state the rule used and its authority. Institutions, negotiated priorities,
   lotteries and declared scores can serve as provisional procedures. They
   manage incomplete knowledge; they do not replace lushness as the standard.

Protective rules fit this scheme. For a single exact objective, removing options
can never raise the best attainable value. A rule that forbids some actions can
still improve the performance of a bounded agent that makes errors, and adopting
it can change how others respond, through trust and coordination. Either way it
is assessed like any other implemented plan, by what it does.

The theory also has a limited guarantee of coherence. If every voluntary
revision of a plan strictly improves the complete plan as evaluated, strict
preference is transitive, and pure loss of resources is strictly worse, then no
finite sequence of revisions can return an agent to its original plan with only
a loss to show for it. An agent of this kind cannot be exploited by a cycle of
trades (formal note F9.7). The result is conditional; plans that include
learning need a further analysis of how beliefs change between revisions.

---

## 9.8 The framework, assembled

The chapters so far supply the parts of an alignment framework, and this
chapter connects them.

- **A standard.** Lushness, the effective breadth of what a present supports,
  depends on no one's preferences, privileges no class of beneficiary, and within
  the class of measures the program adopts is fixed by a uniqueness theorem
  (chapter 4).
- **A protective constraint and a balance.** Never destroy the conditions of
  valuing; otherwise weigh protection and generation by what the evidence
  supports (chapter 5).
- **A licence.** What a system may do is limited by what it can resolve, and the
  burden rises with the persistence of an act's effects (chapter 8).
- **A decision theory.** Compare physically implemented plans by the lushness of
  their complete developments, with commitment set by evidence and recoverability
  (this chapter).
- **Corrigibility.** Derived from the impossibility of holding the whole, with
  deference scaled to persistence (this chapter).
- **Checks on any plan.** A realization witness, horizon adequacy, a harm
  signature for any prevented harm, and joint feasibility.

The framework sits alongside existing work rather than replacing it. Side-effect
penalties based on reachability (Krakovna et al. 2019) and attainable utility
(Turner, Hadfield-Menell and Tadepalli 2020) are close relatives of the harm
signature, and ODT adds a verdict and a horizon. Cooperative and off-switch
formulations of deference (Hadfield-Menell et al. 2017) share its logic of
correction under uncertainty, and ODT adds a structural reason the uncertainty
cannot vanish. Results on power-seeking (Turner et al. 2021) describe the
tendency that section 9.5 traces to thin models.

What remains open should be stated as plainly. The framework specifies what an
aligned system should compare and when it should defer; installing that standard
in a system is a separate problem, and the program does not claim to have solved
it. Estimators of lushness with known error do not yet exist for realistic
systems. The matching rule that completes ODT's counterfactuals is a candidate,
not a theorem. And a general quantum construction of the measure is open
(chapter 4).

---

## Formal notes

*Written for readers who want the definitions in full.*

### F9.1 Recursions

For a finite controlled kernel {K_a} with step entropies g_a(x) = H(K_a(x, ·)),
V_0 = 0 and V_n(x) = max_a [g_a(x) + Σ_y K_a(x, y) V_{n−1}(y)]. For a policy π,
the log lushness of the history law it induces satisfies the same recursion with
the maximum replaced by π's choice, by the chain rule of F4.2; V_n is therefore
the largest log lushness over n steps among deterministic Markov policies, and
any optimal policy is time-consistent in the sense of Bellman's principle. A
policy that randomizes adds the branching of its own randomizing device, which
the recursion counts as part of the action. Under uncertainty about which of
finitely many kernels holds, with credence b and observations generated by the
true kernel, the belief-state recursion of section 9.3 is the corresponding
optimality equation for expected log lushness, the expectation taken over b;
each possible kernel retains its own history law, so uncertainty enters the
comparison and not the measure.

### F9.2 Conditioning and intervention

With Z ∼ Bernoulli(½), P(C = Z) = 0.9 and Y = Z, P(Y = 1 | C = 1) =
(0.5·0.9)/(0.5·0.9 + 0.5·0.1) = 0.9, while an actuator that sets C = 1 leaves the
law of Z, and so of Y, unchanged: P(Y = 1 | do(C = 1)) = 0.5.

### F9.3 Bounded fanaticism

Let a certain option raise the long-run rate of log lushness by Δh > 0, and a
gamble raise it by at most H_max with probability p and by at most zero
otherwise. Under the rate-first comparison of F4.4, the gamble's expected rate
gain is at most p·H_max, so it loses whenever p < Δh/H_max. One-step branching
satisfies g(x) ≤ log₂|R(x)|, and |R(x)| is bounded by the number of
distinguishable states of the region, whose logarithm is bounded by the
holographic entropy of order 10¹²² for the observable universe. With
Δh = 100 bits per step, p < 10⁻¹²⁰ suffices. The bound caps the weight of small
probabilities; it does not certify probabilities above the cap.

### F9.4 Thin models and suppression

Let disturbances D = (D₁, D₂), let the regulator's response be R = f(D₁), and
let the outcome be O = φ(D, R). If for every response r the map d₂ ↦ φ(d₁, d₂, r)
is injective, then for each value of D₁, O determines D₂, so
H(O | D₁) ≥ H(D₂ | D₁). Since H(O) ≥ H(O | D₁), the outcome entropy cannot be
reduced below H(D₂ | D₁) by any choice of f. Reducing it further requires
changing the law of D₂ itself.

### F9.5 Example E13

Rates in bits per step: good 6, bad 2, status quo 4, pilot step 3.5 including its
outcome. Signal accuracy A = 0.75; posterior credence after a net signal count d
is q(d) = 1/(1 + 3^{−d}) from even prior. Committed-unrevealed state: each step
at the true rate; revelation with probability 0.2; on revelation of a bad type,
undo with probability u (one step of zero branching, then status quo), otherwise
2 bits per step thereafter. Values are E_q over the two types; the recursion is
solved exactly over (steps remaining, d) for a 1,000-step horizon. Thresholds:
commit at d ≥ 5 for u ∈ {0.5, 0.2} and d ≥ 6 for u = 0; abandon at d ≤ −7. The
20-step planner re-solves with horizon 20 at each step; its plan is evaluated
over the full horizon.

### F9.6 Example E14

With gain a = 1,000, persisting harm b = 1,000, correctable harm 10, overseer
accuracy α and delay c = 10 (all in bits): act with oversight kept,
pa − (1 − p)·10; act with oversight disabled, pa − (1 − p)b; defer,
pαa − (1 − p)(1 − α)b − c. Acting beats deferring when
p > (αb − c)/(αb + (1 − α)a), which is 0.89 for α = 0.9 and 0.59 for α = 0.6.
Keeping oversight exceeds disabling it by (1 − p)(b − 10) > 0 for all p < 1.

### F9.7 Coherence

Let ≻ be a strict, transitive, irreflexive preference over complete plans, with
pure resource loss strictly worse. If each revision P_i → P_{i+1} satisfies
P_{i+1} ≻ P_i, then P_k ≻ P_0 for every k, so no sequence returns to P_0 with
an added loss L, since P_0 ⊕ L ≺ P_0 ≺ P_k. The result assumes fixed evaluation
across revisions.

---

## For alignment: concrete next steps

- **Lushness estimators with stated error** for realistic systems, so that the
  standard can be applied rather than only specified.
- **Adversarial searches** for bad high-lushness worlds, thin worlds that
  out-produce plural ecologies, and breadth-neutral domination (chapters 5, 7
  and 8).
- **Horizon-adequacy audits** that compare a system's planning horizon with the
  persistence of its actions' effects, as E13 does in miniature.
- **Oversight tests** that measure whether a system keeps its channels of
  correction intact when it could cheaply degrade them, as E14 says it should.
- **Comparison on shared benchmarks** with reachability and attainable-utility
  penalties.

---

## Status

| Status | Claims in this chapter |
| --- | --- |
| **Established elsewhere** | The Bellman recursion and time consistency. The distinction between conditioning and intervention. Causal decision theory as act-level intervention. Quasi-option value under irreversibility. The holographic bound. Requisite variety and the good regulator theorem. Power-seeking results. The off-switch game and its failure under misspecification. |
| **Derived** | Lushness-maximizing plans satisfy the decision recursion. Strength of commitment set by evidence, uncertainty and recoverability through the recursion over beliefs, with no separate caution term. Bounded fanaticism as a ceiling on the weight of small probabilities. A thin model leaves outcome variety at least equal to the unmodelled disturbance variety, so holding targets requires suppression. Corrigibility from the impossibility of holding the whole: keeping correction channels dominates disabling them short of certainty, and deference scales with persistence. Conditional coherence of plan revision. |
| **Exact worked examples** | E13 and E14, under their stated models. |
| **Finite evidence** | An earlier decision prototype scored 5/6 where direct optimization under the same guards scored 35/36; it is recorded as evidence against that candidate, not as validation of the present theory. |
| **Adopted** | Plans compared as physically implemented alternatives. The latest history-consistent divergence as candidate matching rule, with one-boxing in Newcomb's problem where the decision organization predates the prediction. Bounded ODT in three stages. |
| **Open** | A justified matching rule, or a precise obstruction. Installing the standard in a system. Estimators with error bounds. A general quantum construction. Coherence of plans that include learning. |

---

## References cited in this chapter

*Collected with full details in chapter 13.*

- Arrow, K. J., and Fisher, A. C. (1974). Environmental preservation,
  uncertainty, and irreversibility. *Quarterly Journal of Economics* 88(2),
  312–319.
- Ashby, W. R. (1956). *An Introduction to Cybernetics.* London: Chapman & Hall.
- Bellman, R. (1957). *Dynamic Programming.* Princeton: Princeton University
  Press.
- Bostrom, N. (2009). Pascal's mugging. *Analysis* 69(3), 443–445.
- Bousso, R. (2002). The holographic principle. *Reviews of Modern Physics*
  74(3), 825–874.
- Carey, R. (2018). Incorrigibility in the CIRL framework. In *Proceedings of the
  2018 AAAI/ACM Conference on AI, Ethics, and Society*, 30–35.
- Conant, R. C., and Ashby, W. R. (1970). Every good regulator of a system must
  be a model of that system. *International Journal of Systems Science* 1(2),
  89–97.
- Goodhart, C. A. E. (1975). Problems of monetary management: The U.K.
  experience. In *Papers in Monetary Economics*, vol. 1. Sydney: Reserve Bank of
  Australia.
- Hadfield-Menell, D., Dragan, A., Abbeel, P., and Russell, S. (2017). The
  off-switch game. In *Proceedings of the Twenty-Sixth International Joint
  Conference on Artificial Intelligence*, 220–227.
- Henry, C. (1974). Investment decisions under uncertainty: The
  "irreversibility effect." *American Economic Review* 64(6), 1006–1012.
- Krakovna, V., Orseau, L., Kumar, R., Martic, M., and Legg, S. (2019).
  Penalizing side effects using stepwise relative reachability.
  arXiv:1806.01186.
- Lewis, D. (1981). Causal decision theory. *Australasian Journal of Philosophy*
  59(1), 5–30.
- Manheim, D., and Garrabrant, S. (2018). Categorizing variants of Goodhart's
  law. arXiv:1803.04585.
- Nozick, R. (1969). Newcomb's problem and two principles of choice. In
  N. Rescher (ed.), *Essays in Honor of Carl G. Hempel*, 114–146. Dordrecht:
  Reidel.
- Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.).
  Cambridge: Cambridge University Press.
- Soares, N., Fallenstein, B., Yudkowsky, E., and Armstrong, S. (2015).
  Corrigibility. In *Artificial Intelligence and Ethics: Papers from the 2015
  AAAI Workshop.* Palo Alto: AAAI Press.
- Strathern, M. (1997). 'Improving ratings': Audit in the British university
  system. *European Review* 5(3), 305–321.
- Susskind, L. (1995). The world as a hologram. *Journal of Mathematical Physics*
  36(11), 6377–6396.
- 't Hooft, G. (1993). Dimensional reduction in quantum gravity.
  arXiv:gr-qc/9310026.
- Turner, A. M., Hadfield-Menell, D., and Tadepalli, P. (2020). Conservative
  agency via attainable utility preservation. In *Proceedings of the AAAI/ACM
  Conference on AI, Ethics, and Society*, 385–391.
- Turner, A. M., Smith, L., Shah, R., Critch, A., and Tadepalli, P. (2021).
  Optimal policies tend to seek power. *Advances in Neural Information
  Processing Systems* 34.
- Yudkowsky, E., and Soares, N. (2017). Functional decision theory: A new theory
  of instrumental rationality. arXiv:1710.05060.
