# 23. Choosing inside the structure

> **Drafting note (r4, 25 October).** Sol's review of outline r29 and
> chapters 23 r3 and 24 r1. The rules arise from properties of the measure
> that defines the gradient, not from the gradient as an ordering: an
> ordering alone carries no additive composition, value of information,
> horizon bound or cost threshold, and a strictly increasing transformation
> of lushness would keep the order and lose them. The opening list now says
> "the measure", and two of its lines are brought into line with the body.
> Information is worth to a decision-maker what it lets it do, while
> producing it is a physical event counted regardless (section 23.3). A
> finite repertoire bounds the branching rate at a declared level of detail;
> the caps on fragile gains and long shots need further physical premises
> (section 23.6).

> **Drafting note (r3, 25 October).** Outline r29 [143], [144]. Part VII is
> *Deciding without the whole view*, and chapter 24 is *The gradient*. The
> opening now shows that each decision rule takes its shape from a property
> of the ranking, and that these properties are the gradient chapter 24
> sets up. Gradient Ethics is named in the text as what deciding within the
> structure entails. The TL;DR headline adds the rules' source; the last
> bullet names Gradient Ethics by what it is. The other bullets are Sol's,
> unchanged.

> **Drafting note (r2, 25 October).** Sol's review of r1, applied.
> - **Organizing idea.** Omega yields conditional decision mathematics, not
>   permission to optimize. The opening now says so, and brings forward the
>   gap that r1 left to section 23.9: a ranking made with complete knowledge
>   can license tradeoffs that no situated agent could responsibly presume to
>   make.
> - **TL;DR.** Sol's version, adopted with bold lines added. The standard,
>   agreed in the review: the TL;DR must be independently sufficient to
>   understand the chapter's argument; the body establishes the results,
>   states their conditions and answers objections. The infinite rate family
>   and the no-cycle result stay out of it. (For the style sheet at its next
>   revision.)
> - **The rule is conditional** (23.1). The chain rule fixes how lushness
>   composes. Adopting expected whole-field lushness as a decision rule, with
>   expectation over credences, is a further step. Every result is stated as
>   what a decision-maker using that rule would do. The In Omega box now says
>   that implemented control policies alter the continuation process, and
>   keeps the determinism limit of chapter 3.
> - **Admissible actions** (23.2). Implementable randomizing mechanisms are
>   actions, with their devices' branching and costs. Time consistency holds
>   given a correct state, a fixed objective and horizon, and the capacity to
>   carry out the contingent continuations.
> - **Information and its use** (23.3). Three quantities kept apart: the
>   test's physical contribution, the decision value of the information, and
>   the net value of testing. The value-of-information inequality concerns
>   the second, for information available at no extra cost and free to be
>   ignored. Example 23.1 reports the net value of testing, with the signals'
>   own branching shown separately.
> - **Reversibility** (23.4). No longer stated as universal. The harder a
>   mistake is to undo, the more useful evidence can be worth; waiting has
>   consequences too, and other variables enter. The example's results are
>   scoped to the example. Section 23.5: reversing an act returns the options
>   to a common law only if undoing restores dynamics that forget the act.
> - **Long shots** (23.6). The comparison with a sure gain and the
>   comparison with doing nothing are separated.
> - **No cycles** (23.8). Shortened, and stated without assuming that a loss
>   of resources is bad in itself. Appendix A's Proposition A.13.4 carries
>   that premise and should be restated the same way at its next revision.
> - **Verification.** `analysis/ch23/test_ch23_numbers.py` enumerates every
>   history of recorded chance events under the optimal plan, for horizons of
>   6, 10 and 14 steps and all four reversibility settings, and computes the
>   history entropy directly. It agrees with the recursion and with the
>   script's forward evaluation to 5 × 10⁻¹³ bits, so each chance event is
>   counted once. The check found one boundary inconsistency in the first
>   version of the test, not in the script: the script records whether a bad
>   intervention can be undone in the step after its revelation, and the test
>   now does the same. The example's text says so.

> **Drafting note (r1, 25 October).** First draft under outline r28
> (chapter 23), opening Part VII, *From value to action*.
> - **Sources.** Outline r28 (Part VII, chapter 23) and r22 (former chapter
>   24); v4 chapter 9, sections 9.1–9.4 (decision lineage, implementation
>   and conditioning, the strength of commitment, bounded fanaticism),
>   recast for v4.1; chapters 6 (sections 6.3–6.4), 7 (sections 7.3–7.6),
>   10 (section 10.6), 11 (sections 11.3, 11.5) and 13; Appendix A r20
>   (A.4.6, A.5.2–A.5.4, A.9.5, A.9.6, A.12.1, A.12.2, A.13.1, A.13.4,
>   A.13.5).
> - **Does not depend on test-bed results** [142]. Every claim is a theorem
>   of Appendix A or an exact computation in a specified finite model. The
>   worked example of section 23.4 is new, with its own script
>   (`analysis/ch23/ch23_numbers.py`, to be listed in Appendix B). It
>   replaces v4's Example E13, whose script is not in the archive; the
>   parameters follow E13, and every chance event a step records (signal,
>   revelation, whether a bad step can be undone) is counted by the chain
>   rule rather than folded into stipulated totals.
> - **Book Two boundary** [130], [134]. The margin for model error,
>   deference, correction and the decision rule for situated agents are
>   named and passed to chapter 24. Option value (A.9.6) is here, as the
>   outline moves it. Precautionary protection (A.9.5) appears once, as the
>   expected-value form of precaution, with protection margins left to
>   chapter 17.
> - **Pointers to fix elsewhere.** Chapter 7, sections 7.8 and 7.9, point to
>   chapter 24 for the robustness floor, the long-shot bound and the window
>   applied; under r28 that is this chapter. Appendix A's remarks to A.4.6,
>   A.5.2, A.9.6 and A.13.3 point to chapter 24 for the margin for model
>   error, which r28 keeps there as a question passed to Book Two. Fix at
>   the next revision of each.
> - Written for a reader new to the framework [112]. The drafting notes are
>   working provenance, removed at compilation.

> **TL;DR**
>
> Omega can rank what different plans would bring about. It cannot, by
> itself, authorize anyone to act on that ranking. A decision-maker is part
> of the world it changes. If it compares physically possible plans by their
> expected contribution to whole-field lushness, a theory of planning
> follows. Its rules are not added from outside. Each arises from a
> property of the measure itself.
>
> - **Only plans that can actually be carried out belong in the
>   comparison.** Waiting, testing, committing and reversing course all use
>   time and resources. Their consequences count. Wished-for outcomes do not.
> - **A plan must account for what happens after its first step.** The
>   measure allows a chooser to compare each action together with the best
>   responses available afterwards. The resulting plans remain consistent as
>   events unfold, provided the model and objective stay fixed.
> - **Learning can make waiting worthwhile, especially before irreversible
>   decisions.** Information helps a chooser when it allows better
>   decisions. But obtaining evidence has costs, and waiting can close
>   opportunities too. Both sides belong in the comparison.
> - **How long consequences last can change which plan is better.** Effects
>   that eventually fade leave a limited gain or loss. Changes to a lasting
>   rate accumulate over time. A short horizon can miss the difference.
> - **Fragile gains and unlikely windfalls must earn their place.** A
>   temporary gain must repay its cost before it disappears. A sufficiently
>   unlikely gain with a physical ceiling can lose to a smaller, certain one.
>   These results follow from the consequences, without adding a separate
>   penalty for risk.
> - **The measure does not protect a chooser from being confidently
>   wrong.** At known odds, it does not impose extra caution. Real
>   decision-makers have incomplete models, can misjudge distant
>   consequences and can destroy opportunities for correction. How they
>   should act under those conditions, on a gradient they can only partly
>   see, is what deciding within the structure entails: the problem the
>   manuscript calls Gradient Ethics.

Parts IV to VI test what the whole-field comparison ranks. Part VII asks
what that ranking means for someone who has to decide without the whole
view. The answer has two halves, and this chapter keeps them apart from the
start.

The first half is a result. A decision-maker that compares the plans it can
carry out by the expected lushness of what they bring about inherits a
working theory of planning. Its rules are not chosen for their convenience
or borrowed from another theory. Each arises from a property of the measure,
and an ordering of futures without those properties would not give them.
- **The measure composes.** The lushness of a history is the branching of
  its first step plus the expected lushness of what follows. So the best
  plan is built backwards, one step and its best continuations at a time
  (section 23.2).
- **It counts every physical consequence.** So only plans that can be
  carried out are compared, and a test counts as a physical process, whether
  or not anyone uses its result (sections 23.1 and 23.3).
- **It keeps information apart from its use.** Producing information is a
  physical event, counted like any other. What the information is worth to
  a decision-maker lies in the choices it changes. So evidence is worth what
  it could change, and irreversibility can raise that worth (sections 23.3
  and 23.4).
- **It weighs how long consequences last.** So a short horizon misses most
  where an act changes a lasting rate (section 23.5).
- **A finite repertoire bounds its rate.** At a declared level of detail, no
  step branches more than the repertoire allows. With further physical
  premises, a residual floor, a common hazard and a finite window, fragile
  gains and long shots have limits (section 23.6).

Comparing the continuations a present makes available, by this measure,
gives every present a direction in which the whole field widens.
[Chapter 24](#chapter-24) sets up that gradient, and argues that by the
central thesis its best move corresponds to a universal ethics.

The second half is a limit. The theory is conditional mathematics, not
permission to optimize. It is only as good as the model the decision-maker
holds, and the model is held by a physical participant in the field it is
trying to evaluate. A ranking made with complete knowledge can favour a
tradeoff that no situated agent could responsibly presume to make. At known
odds the measure accepts, for example, a 70% chance of ruin for a 30% chance
of something better. [Chapter 10](#chapter-10) said that a ranking does not
by itself give authority to act. This chapter shows how much the ranking
does supply, and where it stops. Every result is a theorem of
[Appendix A](#appendix-a) or an exact computation in a specified model.

---

## 23.1 The chooser is part of what it chooses among

**A decision-maker is a physical process inside the world it acts on. Its
options are the plans it can physically carry out. If it ranks them by
expected whole-field lushness, it compares the complete developments that
carrying each one out would bring about.**

An organism's motor system, a trained habit, a planning program and an
institution's rules are all physical organizations. The same laws carry
them forward as everything else. When one of them chooses, it does not
stand outside the structure and pick a branch. It is part of the present,
and its choice is one of the events by which the present continues
([chapter 2](#chapter-2)).

That fixes what an option is.

> **Plain-English definition 23.1: Plan**
>
> A way of responding to what the decision-maker will observe that it can
> physically carry out from the present, with its apparatus, delays,
> resources and costs included: committing, waiting, investigating,
> delegating, or changing how it decides.

Three consequences follow. Each repeats a rule the manuscript has already
stated for comparisons in general.
- **Options must be implementable.** A plan counts only if some physical
  process available from the present can carry it out. A list of policies
  that no hardware in the world could execute is not a set of options.
  Switching between plans is itself a physical act, with its own costs
  ([chapter 11](#chapter-11), sections 11.3 and 11.5).
- **Options are implemented, not selected.** Picking out the histories in
  which an action happened to occur gives a conditional law. That law need
  not describe what carrying out the action would do. Let an unobserved
  coin Z be fair, let an action C agree with Z nine times in ten, and let an
  outcome Y equal Z. Among histories in which C = 1, Y = 1 has probability
  0.9. An actuator that sets C = 1 without touching Z leaves Y = 1 at
  probability 0.5 (Pearl 2009). Selecting histories by the action has
  selected its common cause. The comparison always uses the implemented
  action ([Theorem A.13.1](#a-13-1), remarks).
- **Costs act through the futures they remove.** The time a plan takes, the
  energy it uses and the apparatus it occupies are part of the development
  it produces. Nothing is subtracted afterwards ([chapter 12](#chapter-12),
  section 12.2).

**The rule is a choice, not a consequence of the measure.** The measure
fixes how lushness composes: the lushness of a history is the branching of
its first step plus the expected lushness of what follows
([chapter 5](#chapter-5)). It does not tell anyone to maximize it. A
decision-maker that does adopt expected whole-field lushness as its rule
makes two further commitments. It takes the whole-field comparison as its
objective. And, since it seldom knows its world exactly, it averages over
its credences about which law holds. This chapter studies what follows from
that rule. Its results have the form "a decision-maker using this rule
would …". They are not instructions.

The decision-maker's uncertainty belongs to the comparison, not to the
measure. Each way the world might be has its own law of histories and its
own lushness, and the decision-maker averages across them. Not knowing which
future will occur adds no branching to the field, and the chance of being
wrong subtracts none ([chapter 10](#chapter-10), section 10.6).

> **In Omega**
>
> A decision-maker is a part of the present whose physical state helps set
> the law by which the present continues. A plan is a physically
> implemented control policy, and different policies alter the continuation
> process. Where the full present fixes what follows, there is one
> continuation and nothing to compare ([chapter 3](#chapter-3)). The
> decision-maker's uncertainty is a spread of credence over which
> continuation law holds.

---

## 23.2 The best plan is built backwards

**A decision-maker using the rule values its best choice now as the
branching it produces at once, plus the expected value of the best choices
afterwards. Plans built this way stay best as events unfold, provided the
model and the objective stay fixed.**

Suppose a decision-maker can take one of several actions at each step, each
with its own transition law. The best lushness any plan can reach over n
steps from a state x is given by a recursion ([Theorem A.13.1](#a-13-1)).

> \[
> V_n(x)=\max_a\Bigl[g_a(x)+\sum_y K_a(x,y)\,V_{n-1}(y)\Bigr],\qquad V_0=0 .
> \]
>
> *In words:* the value of the best choice now is the branching that action
> produces at this step, plus the expected value of choosing best from
> wherever it leads.

Here g_a(x) is the branching of action a at state x, and K_a(x, y) the
probability that it leads to y. This is the recursion of dynamic programming
(Bellman 1957), with log lushness as the quantity maximized. It is exact
because the measure composes. The same property that selected the measure
makes planning with it consistent over time: a plan judged best from the
present is still best when judged again from any state it reaches.

Three conditions go with that consistency, and with the recursion itself.
- **The action set must be the implementable one.** If the decision-maker
  can randomize, the randomizing mechanisms it can build are actions in
  their own right. Each comes with the branching of its random device and
  the device's costs. A maximum over deterministic actions alone can miss
  them, because a recorded random choice adds branching. The gain is small:
  at most one bit over the better of two plans, when the two are equally
  good, and almost nothing when one is far better
  ([Corollary A.5.2](#a-5-2)). Flipping a coin cannot rescue a poor plan.
- **The state must be represented correctly.** The recursion is exact for
  the model it is run on. A decision-maker whose state description leaves
  out something that matters gets the best plan for the wrong world.
- **The objective, the horizon and the capacity to follow through must stay
  fixed.** A plan stays best when judged again only if it is judged by the
  same rule, over the same horizon, and only if the decision-maker can still
  carry out the responses the plan calls for.

When the decision-maker is unsure which of several laws holds, and updates
its credences from what it observes, the same recursion run over its
credences gives the plan with the highest expected lushness
([Theorem A.13.1](#a-13-1), remarks). Each possible law keeps its own
lushness. The plan is chosen by the average.

---

## 23.3 What information is worth, and what testing costs

**Information has decision value only when it can change what is done.
Producing it is a physical process, with consequences of its own. The
comparison counts both.**

A plan can include looking before acting: running a test, waiting for news,
asking someone who knows. Three quantities are involved, and they need to be
kept apart.
- **The physical contribution of the test.** A test is a physical process.
  It takes time, uses resources, creates correlations, and its outcome is a
  chance event that adds branching of its own. The measure counts all of
  this whether or not anyone acts on the result
  ([chapter 11](#chapter-11), section 11.3).
- **The decision value of the information.** This is the improvement the
  decision-maker gets by letting its later actions depend on the result,
  with the process that produces the result held fixed.
- **The net value of testing.** This is the whole difference between a plan
  that tests and one that does not: the decision value, plus the test's own
  branching, less the futures its costs and delays remove.

> **Plain-English definition 23.2: Decision value of information**
>
> The improvement in expected lushness a decision-maker gets by letting its
> later actions depend on a signal, with the process that produces the
> signal held fixed. It is zero when no possible reading of the signal would
> change what is done.

The decision value has a simple property. Suppose the information is
available at no additional cost, and the decision-maker is free to ignore
it. Then having it cannot make the best plan worse
([Proposition A.9.6](#a-9-6)).

> \[
> \mathbb E_Z\Bigl[\max_a \mathbb E[\ell\mid a, Z]\Bigr]\ \ge\ \max_a \mathbb E[\ell\mid a].
> \]
>
> *In words:* choosing after seeing a signal Z is worth at least as much as
> choosing without it, and worth more exactly when, with some chance, the
> signal would make a different action best.

The inequality matters most before a step that cannot be undone. There, the
chance to learn first is worth something even when acting now looks best.

> **Plain-English definition 23.3: Option value**
>
> The decision value of keeping a choice open until something has been
> learned, rather than committing now to a step that cannot be undone.

This is the irreversibility effect of environmental economics (Arrow and
Fisher 1974; Henry 1974), stated in the measure's terms. It is also
[chapter 13](#chapter-13)'s principle: information widens the future only
through what it changes. A signal that could not change the choice has no
decision value, however accurate it is. Producing it may still have physical
consequences, and the comparison counts them.

A small case shows the decision value alone. A structure matters with
credence 0.1. If it matters, destroying it costs 1,000 bits; preserving it
costs 50 bits. With no signal, the best choice is to preserve it, at an
expected cost of 50 bits. A costless signal that reveals for certain whether
it matters lets the decision-maker destroy it when it does not. The expected
cost falls to 5 bits, so the signal's decision value is 45 bits. A costless
signal that is right only six times in ten has no decision value, because
neither of its readings would make destroying the structure the better
choice ([Appendix A](#appendix-a), verification V13).

Real tests are not costless. A decision-maker using the rule tests only when
the net value of testing is positive. Waiting to learn can also close
opportunities, and that loss belongs in the same comparison.

---

## 23.4 Irreversibility can raise the value of evidence

**The harder a mistake is to undo, the more useful evidence can be worth.
But waiting has consequences too, and how strongly to commit depends on
both.**

The recursion over credences says how much evidence a commitment needs in a
given case. A worked example shows how reversibility enters.

**Example 23.1: Commit, test or give up.** A decision-maker can adopt an
intervention whose type it does not know. It holds credence 0.5 that the
intervention is good.
- **The regimes.** Under the status quo the system branches 4 bits a step.
  If the intervention is good, committing to it gives 6 bits a step; if it
  is bad, 2.
- **Testing.** Each step, before committing, the decision-maker can run a
  small pilot instead. The pilot regime branches 3 bits a step, and it
  returns a signal that is right three times in four.
- **Giving up.** It can abandon the intervention for good and keep the
  status quo.
- **After committing.** The intervention's type shows itself with
  probability 0.2 a step. In the step after a bad intervention is revealed,
  it turns out to be undoable with probability u, a chance fixed by the
  physics of the case. Undoing takes that step, with no branching, and then
  the status quo resumes. If it cannot be undone, the bad regime continues.

Every chance event a step records adds its own branching, and the measure
counts it once, by the chain rule: the pilot's signal, the revelation, and
whether undoing is possible. The best plan over 1,000 steps is computed
exactly by the recursion over credences (script
`analysis/ch23/ch23_numbers.py`). An independent check enumerates every
history of recorded events for short horizons and computes its entropy
directly; the two agree to 10⁻¹² bits. Each signal changes the odds by a
factor of three, so the credence depends only on how many more signals have
favoured the intervention than opposed it.

| Chance a revealed bad commitment can be undone | First action | Commit after net favourable signals (credence) | Expected pilots, good / bad | Net value of testing | Of which, the signals' own branching | Loss of a 20-step planner |
|---|---|---|---|---|---|---|
| 1 | pilot | 1 (0.75) | 2.0 / 10.0 | 0.2 bits | 4.9 bits | 7.5 bits |
| 0.5 | pilot | 5 (0.996) | 10.0 / 15.9 | 486.6 bits | 10.5 bits | 56.0 bits |
| 0.2 | pilot | 5 (0.996) | 10.0 / 15.9 | 783.4 bits | 10.5 bits | 87.4 bits |
| 0 | pilot | 6 (0.9986) | 12.0 / 16.0 | 982.1 bits | 11.3 bits | 108.9 bits |

*The net value of testing is the best plan's expected lushness minus the
better of committing at once and abandoning at once. It includes the pilot
regime, the delay and the signals' branching, shown separately. The 20-step
planner chooses, at every step, the plan that is best over the next 20
steps, and is scored over the full 1,000. In every case the best plan
abandons the intervention after eight more unfavourable signals than
favourable ones, at a credence of about 0.00015.*

In this example, four things happen.
- **When a mistake can always be undone, committing tests itself.** One
  favourable signal is enough. The net value of testing is a fifth of a bit,
  and the signals' own branching, 4.9 bits, is larger than that. So the
  decision value of the pilots does not cover their other costs: here,
  committing is nearly as good a way to learn as testing.
- **When undoing may fail, evidence becomes worth much more.** The plan
  tests until its credence passes 0.996, or 0.9986 when undoing is
  impossible. The net value of testing rises to almost a thousand bits, and
  nearly all of it is decision value. Nothing in the recursion rewards
  caution. The caution is the value of the evidence still to come.
- **Giving up is a commitment too.** Abandoning forecloses the good outcome
  for good, so the plan holds it to a standard of its own. It gives up only
  when its credence that the intervention is good has fallen to about
  0.00015. Protection and opportunity are weighed in one comparison.
- **A short look ahead costs most where acts last.** A decision-maker that
  plans only 20 steps ahead, re-planning as it goes, loses 7.5 bits when the
  commitment can be undone and 109 bits when it cannot. A short planner
  underrates how long its acts persist. Section 23.5 bounds that error in
  general.

**The pattern is not a general law.** Reversibility is one variable among
several. The others include the time available to learn, the cost of
waiting, the reliability of the evidence, and the consequences of doing
nothing. Two cases show the pattern failing.
- **A closing window.** An irreversible step that must be taken now or not
  at all leaves no time to learn. Waiting for evidence then forecloses the
  opportunity, and that loss can outweigh the risk of acting.
- **A costly reversal.** A step that can be undone, but whose first hours
  carry a heavy and lasting cost, is not cheap to try. Its reversibility does
  not make it its own experiment.

What the example does show is how the comparison handles all of these at
once. How strongly to commit is set by the evidence in hand, the evidence
still obtainable, what waiting costs and how recoverable the commitment is.
None of these needs a place of its own in the measure.

---

## 23.5 What a finite horizon leaves out

**A decision-maker that looks only so far ahead misses a remainder. If the
world comes to forget the act, the remainder is bounded. If the act changes
a lasting rate, the remainder grows with the horizon, and its sign is set by
the long-run effect the decision-maker knows least well.**

No physical decision-maker computes everything that follows. It compares
options over some horizon n̄ and acts. The true difference between two
options over a longer horizon n is the difference it computed plus a
remainder: the branching the options would add, or remove, beyond n̄. How
large can that remainder be? [Proposition A.12.1](#a-12-1) answers in two
cases.

> \[
> \text{(i)}\ \ \lvert R\rvert\ \le\ \frac{4C\,\lVert g\rVert_\infty\, r^{\bar n-\tau}}{1-r};
> \qquad
> \text{(ii)}\ \ R=(n-\bar n)(h_a-h_b)+O(1).
> \]
>
> *In words:* if, after the act, both options come under the same dynamics,
> and those dynamics forget where they started, what the decision-maker
> cannot see is bounded and shrinks the further it looks. If the act's
> effects persist, so that the options settle at different rates, what it
> cannot see grows in proportion to how far beyond its horizon the
> consequences run.

In case (i), the options converge after some time τ to one law that mixes at
a geometric rate r. The constants C and r, and the largest step branching
‖g‖∞, set the bound. In case (ii), the options settle into regimes with
rates h_a and h_b that differ. The remainder is the long-run gap times the
unseen time, up to a bounded correction.

Three points follow.
- **Persistence, not size, defeats a short horizon.** A large act whose
  effects fade costs a finite amount, which a longer horizon can see. A
  small act that changes a rate costs more and more the further its
  consequences run ([chapter 6](#chapter-6), section 6.4).
- **The sign of the remainder is set by what is least known.** In case (ii)
  the remainder is dominated by the long-run difference in rate. That is the
  quantity a decision-maker can estimate least well, because it depends on
  how the world develops long after the act ([chapter 10](#chapter-10),
  section 10.3).
- **Undoing helps only if it restores a common law.** An act that can be
  reversed once its effects are seen can return the options to case (i). It
  does so only if undoing actually restores dynamics that forget the
  intervention. A reversal that leaves lasting traces downstream leaves the
  options in case (ii).

The bound in case (i) is only as useful as the estimates of C and r that go
into it. A decision-maker that cannot estimate how fast its world forgets
cannot certify what its horizon misses.

---

## 23.6 Fragile gains, long shots and acts that cannot be undone

**A gain must repay its cost within its expected life, and no gain outlasts
the window in which it operates. In a finite world, a small enough chance of
a capped gain loses to a smaller, certain one. Removing something that might
matter is right only when the expected loss from leaving it outweighs the
expected loss from destroying it.**

[Chapter 7](#chapter-7) priced persistence, early ends and gambles. For a
decision-maker using the rule, its results become limits. None of them adds
a penalty for risk. Each follows from the consequences.

**Fragile gains.** A gain in rate of ε bits a step, ending at hazard μ, is
worth giving up a finite c bits only if it repays them within its expected
life of about 1/μ steps ([Corollary A.4.6](#a-4-6)).

> \[
> \varepsilon>\frac{\mu\,(c+h_F)-h_2(\mu)}{1-\mu}.
> \]
>
> *In words:* the more fragile a gain, the larger it must be to be worth
> what it costs; the residual rate h_F and the branching of the gain's own
> uncertain end adjust the threshold.

When the hazard is uncertain, the expected life is an average of 1/μ over the
possibilities, and the most optimistic possibility dominates it. A
decision-maker that is unsure how long a gain will last is pulled towards
the most hopeful estimate. The generative window limits that pull. If the
conditions that support the gain last an expected T_G steps, the gain can
contribute at most about T_G steps' worth. A gain bought at cost c is then
worth taking only if it exceeds about c/T_G a step
([Corollary A.5.4](#a-5-4)). With a cost of 3,538 bits, and the gain equally
likely to end at a hazard of 10⁻⁴ or 10⁻⁶, the floor is 0.007 bits a step with
no window and 0.071 bits a step within a window of 100,000 steps
([chapter 7](#chapter-7), section 7.6).

**Long shots.** An expected-value maximizer can be offered an enormous
payoff at a tiny probability, and led to give up something real for almost
nothing (Bostrom 2009). A decision-maker using the rule resists this where
the possible gain has a physical ceiling. Three premises are needed: a
finite repertoire, so that no gain in rate exceeds some u_max; a floor at
which ruin still branches, so that the downside d is finite; and a common
hazard for the options' regimes ([Proposition A.5.3](#a-5-3)). Given them,
once the regimes last long enough, a gamble with chance of success p loses
to a sure gain of Δh a step whenever

> \[
> p<\frac{\Delta h+d}{u_{\max}+d}.
> \]
>
> *In words:* if the chance of success is smaller than the sure gain plus
> the downside, divided by the largest possible upside plus the downside,
> the gamble loses to the sure gain, whatever it promises.

Two comparisons need to be kept apart.
- **Against a sure gain.** The condition above is a comparison with the
  sure gain Δh. A gamble can lose to a sure gain and still beat doing
  nothing. With no downside, a 0.1% chance of a 100-bit gain is worth
  0.1 bits in expectation: it loses to a sure 1-bit gain and beats a sure
  zero.
- **Against doing nothing.** Setting Δh = 0 gives the comparison with the
  status quo: a long shot loses to doing nothing when p < d/(u_max + d). A
  gamble that fails this test also loses to every sure gain. With no
  downside, d = 0, and no long shot loses to doing nothing.

With no downside, the first comparison is a bound on fanaticism for finite
systems: a long shot loses to a sure gain whenever its probability times the
largest gain physically available falls short of the sure gain. The bound
limits particular gambles. It is not a general prohibition on risky choices,
and it does not say that a probability above the threshold may be taken at
face value. Its premises carry it: the repertoire is a property of the
declared level of detail, and grows as the description is refined
([chapter 7](#chapter-7), section 7.5).

**Acts that cannot be undone.** Suppose a process inside a host might be
generative, adding Δh_X to the host's rate, or might be destructive,
consuming the host if it escapes. The decision-maker has credence p that it
is destructive. Each step, either its type is read, with probability q, or
it escapes, with probability ε, or neither happens. Removing it destroys
whatever it would have added. Containing it risks escape. Comparing
long-run rates, removal is better exactly when the expected loss from an
escape outweighs the expected loss from destroying something generative
([Proposition A.12.2](#a-12-2)).

> \[
> p\,(1-s)\,h_{\text{host}}\ >\ (1-p)\,\Delta h_X,\qquad s=\frac{q}{q+\varepsilon}.
> \]
>
> *In words:* remove only when the chance that the process is destructive,
> times the chance it escapes before it is understood, times what the host
> would lose, exceeds the chance that it is generative times what it would
> add.

Here s is the chance that the type is read before an escape. Take a host
branching 4 bits a step, a process that would add 2, and a reading chance of
0.05 a step. Removal is never better if escape is impossible. It is better
above a credence of 0.75 when the escape chance is 0.01, and above 0.5 when
it is 0.05 ([Appendix A](#appendix-a), verification V14). The result is a
race. What makes removal right is not the danger alone but the danger of
acting too late to learn.

Its mirror image is precaution. Suppose an act would irreversibly destroy
something a valued development might depend on, with credence p. Preserving
it is better when p, times the rate it would sustain, times the expected
life of the regime, exceeds the cost of preserving it
([Proposition A.9.5](#a-9-5)). [Chapter 17](#chapter-17) builds protection
margins from quantities of this kind.

---

## 23.7 When ranking by rate cannot choose

**Ranking options by rate first and head start second is the verdict over
everything that follows, but it can fail to choose at all. A comparison over
a finite expected persistence still chooses.**

[Chapter 6](#chapter-6) showed that, over everything that follows, a higher
rate beats any head start. As a rule for choosing, that has a gap. Suppose
there is an infinite family of options, each with a higher rate than the
last, approaching a limit that none reaches. Then every option is beaten on
rate by another, and ranking by rate selects nothing
([Proposition A.13.5](#a-13-5)).

A decision-maker in a world where regimes end does not face this problem.
Suppose option k waits a mean of 10k steps and then runs at 2 − 1/k bits a
step. Every option is outranked on rate by the next. But over a finite
expected persistence there is a best one: k = 8 when regimes end at a hazard
of 10⁻³, and k = 70 at a hazard of 10⁻⁵.

So ranking by rate gives the right choice only under three conditions.
1. **The window condition.** Regimes must be expected to last longer than
   the horizon at which the options' profiles cross
   ([Corollary A.4.4](#a-4-4)).
2. **The existence condition.** Some option must reach the highest rate on
   offer.
3. **The replacement condition.** A loss that will be replaced after a mean
   time R costs a head start realized over about R steps. Ranking by rate
   treats such a loss as free however long R is, so it is right only if
   regimes outlast R.

When these fail, the decision-maker compares totals over the expected
persistence, which is what the measure ranks in any finite world.

---

## 23.8 A fixed evaluation cannot be led in a circle

**A decision-maker that revises its plan only towards plans it ranks
strictly higher, by an evaluation that stays fixed, can never return to a
plan it ranks lower than where it started.**

An agent with inconsistent preferences can be exploited. Offered a series
of trades, each of which it prefers, it can end where it started, worse
off. A fixed scalar evaluation rules this out. Each strict improvement
raises the evaluation, so a chain of them can never come back to the
starting plan, or to any plan the evaluation ranks below it
([Proposition A.13.4](#a-13-4)). Nothing here assumes that losing a
resource is bad in itself. A loss counts against a plan only if it lowers
the plan's expected lushness, and some losses do not.

The protection assumes that the evaluation stays fixed. A decision-maker
that learns changes its credences, and with them its evaluation, between
revisions. Whether a learning agent can be led round such a cycle needs a
further analysis, which this manuscript does not give.

---

## 23.9 What the measure does not supply

**The planning theory of this chapter is conditional mathematics, carried
out by a physical participant on a model of the field. At known odds it is
neutral to risk, and nothing in it protects a decision-maker from a model
that is confidently wrong.**

Everything in this chapter follows from expectation over a model the
decision-maker holds. That is a strength, because none of it needed a rule
added from outside. It also marks the limit.
- **Neutral to risk at known odds.** A gamble is worth its
  probability-weighted rate, plus at most the uncertainty of the gamble
  itself ([Corollary A.5.2](#a-5-2)). Ruin counts by its size, which grows
  with the horizon, but its probability is not inflated. With the odds
  known, the measure accepts a 70% chance of ruin for a 30% chance of a law
  worth 4 bits more ([Appendix D](#appendix-d), section D.5.3). Many readers
  will find that reckless. The measure does not supply the caution they
  want.
- **The model may be wrong.** Option value protects a decision-maker
  against what it knows it does not know. It does not protect against a
  model that is confidently mistaken. A margin for the chance that one's
  own model is wrong is a policy for acting, not a theorem of the measure.
- **Others may know better.** When to defer to another decision-maker, and
  when to keep a channel open through which one's own mistakes can be
  corrected, depend on how reliable each party is and what deferring costs.
  [Appendix A](#appendix-a) gives a decision model of this, with stipulated
  payoffs ([Proposition A.13.3](#a-13-3)). Computing its payoffs from the
  measure is open.
- **A thin model may suppress what it cannot see.** A regulator that must
  hold its outcomes on target, and can neither model nor absorb some source
  of variation, has suppressing that variation as one way to succeed
  ([Proposition A.13.2](#a-13-2)). That is a hazard of capable
  decision-makers with partial models, taken up in
  [chapters 25](#chapter-25) and [26](#chapter-26).

A whole-field comparison made with complete knowledge can favour a
tradeoff that no situated agent could responsibly presume to make. That gap
is real, and it is not a defect to hide. It is why deciding within the
structure cannot be read off the measure. [Chapter 24](#chapter-24) sets up
the gradient the rules of this chapter follow, names what deciding on it
entails for a participant who sees only part of the field, and states the
questions that remain.

---

## 23.10 What the chapter gives the rest of the manuscript

- **The gradient.** Comparing a present's options by the measure that
  shapes these rules gives every present a direction of widening.
  [Chapter 24](#chapter-24) sets it up, and starts from what this chapter
  leaves open.
- **Protection.** Option value, the cost of an early end and the precaution
  of section 23.6 are the quantities from which [chapter 17](#chapter-17)
  builds protection margins.
- **Controllers.** A decision-maker that changes the processes generating
  further decision-makers is the subject of [chapter 25](#chapter-25).
- **Alignment.** An artificial agent that compares plans this way inherits
  the recursion, the value of information, the bounds on long shots and the
  neutrality to risk at known odds ([chapter 26](#chapter-26)).

---

## 23.11 What this chapter does not claim

- **That the measure tells an agent what to do.** It ranks the developments
  that plans would bring about. Adopting that ranking as a decision rule is
  a further step. How a participant should act on it, with a partial model,
  is what deciding within the structure entails, and it is developed in a
  separate book.
- **That caution is valuable in itself.** Caution in this chapter is the
  value of evidence still to come. It vanishes when nothing more can be
  learned, and waiting can cost more than it gains.
- **That less reversible steps always need more evidence.** Irreversibility
  can raise the value of evidence. Whether it does depends on the time
  available, the cost of waiting and the consequences of doing nothing.
- **That information has no physical consequences unless it is used.** Its
  decision value depends on use. The process that produces it is counted
  regardless.
- **That long shots above the threshold should be taken at face value, or
  that risky choices are ruled out.** The bound limits particular gambles,
  and only given its premises.
- **That the measure supplies prudence beyond expectation.** At known odds
  it is neutral to risk.
- **That Example 23.1 describes a real decision.** It is an exact
  computation in a specified finite model, chosen to show how the
  comparison handles evidence, cost and reversibility together.

---

## Status of chapter 23

| Status | Claims |
|---|---|
| **D** (definitions) | plan (23.1); decision value of information; option value; the physical contribution of a test and the net value of testing (23.3) |
| **Argued** | each decision rule arises from a property of the measure, not from an ordering alone (opening); the decision-maker is part of the structure, so its options are implementable plans compared by what implementing them brings about; adopting expected whole-field lushness as a decision rule is a further step; uncertainty enters the comparison, not the measure (23.1); the conditions on the action set and on time consistency (23.2); reversibility is one variable among several (23.4); undoing returns options to a common law only if it restores forgetting dynamics (23.5); what the measure does not supply (23.9) |
| **T** (established elsewhere) | the decision recursion ([Theorem A.13.1](#a-13-1); Bellman 1957) (23.2); option value ([Proposition A.9.6](#a-9-6); Arrow and Fisher 1974; Henry 1974), with verification V13 (23.3) |
| **T** (proved here) | risk neutrality and recorded mixtures ([Corollary A.5.2](#a-5-2)) (23.2, 23.9); the unresolved remainder ([Proposition A.12.1](#a-12-1)) (23.5); the robustness floor ([Corollary A.4.6](#a-4-6)) (23.6); when removal is licensed ([Proposition A.12.2](#a-12-2)), with verification V14 (23.6); precautionary protection ([Proposition A.9.5](#a-9-5)) (23.6); when the faster option wins ([Corollary A.4.4](#a-4-4)) and when ranking by rate can choose ([Proposition A.13.5](#a-13-5)) (23.7); coherence of plan revision ([Proposition A.13.4](#a-13-4)), restated without its resource-loss premise (23.8) |
| **T, conditional on physical premises** | finite stakes ([Proposition A.5.3](#a-5-3)), with the comparisons against a sure gain and against doing nothing separated; the persistence cap ([Corollary A.5.4](#a-5-4)) (23.6) |
| **T, analytical model with stipulated payoffs** | deference and correction ([Proposition A.13.3](#a-13-3)), cited (23.9) |
| **M** | none; Example 23.1 is an exact computation in a specified finite model, checked by enumeration |
| **E, N, C** | none |
| **Open** | plan revision with learning (23.8); computing the payoffs of deference and correction from the measure (23.9); estimates of mixing that certify a finite horizon (23.5) |

## References cited in chapter 23

*Collected with full details in Appendix G.* Entries marked "to verify" are
not yet checked against their sources.

- Arrow, K. J., and Fisher, A. C. (1974). Environmental preservation,
  uncertainty, and irreversibility. *Quarterly Journal of Economics* 88(2),
  312–319.
- Bellman, R. (1957). *Dynamic Programming.* Princeton: Princeton University
  Press.
- Bostrom, N. (2009). Pascal's mugging. *Analysis* 69(3), 443–445. To verify.
- Henry, C. (1974). Investment decisions under uncertainty: the
  "irreversibility effect". *American Economic Review* 64(6), 1006–1012.
- Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.).
  Cambridge: Cambridge University Press.
