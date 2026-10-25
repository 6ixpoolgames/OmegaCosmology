# 26. Alignment

> **Drafting note (r2, 25 October).** Follows chapter 25 r4, which removes
> consequence flux from the manuscript. This chapter never used the term.
> The only changes are its two references to chapter 25's section on two
> ways to meet a target, which become section 25.3 (formerly 25.4). No
> argument changed.

> **Drafting note (r1, 25 October).** First draft under outline r30
> (chapter 26), from proposal r2 with Sol's review of it applied.
> - **Sources.** Outline r30 (chapter 26) and r28; chapters 1 (sections 1.5
>   and 1.6), 3 (section 3.6), 4 (sections 4.3 and 4.4), 10 (sections 10.3,
>   10.6 and 10.7), 11 (sections 11.3 and 11.4), 23 r4, 24 r2 and 25 r2;
>   Overview r19, section 7; v4 chapter 9, sections 9.5 and 9.8, recast;
>   Appendix A r19 (A.2.4, A.2.5, A.5.2, A.5.3, A.6.4, A.6.5, A.7.6, A.7.8,
>   A.7.9, A.12.1, A.13.2, A.13.3, A.14.7, section A.15); Appendix D r7
>   (D.4, D.5.3). Appendix A r20 was not available; every citation is to be
>   checked against it.
> - **Sol's three repairs.**
>   1. Chapter 1's two lists of requirements are kept apart (section 26.2).
>      The list in section 1.6 is met with its actual status: by argument,
>      in specified settings, and by tests. "No one's preferences wrote" is
>      replaced by "does not privilege the preferences of its designers".
>   2. Section 26.5 no longer claims that the scope-separating term is the
>      one an agent is least able to estimate, or that partial models drift
>      towards self-interest. It claims that a whole-field objective does not
>      prevent local optimization when the model fails to represent the
>      consequences that distinguish the two. The suppression mechanism is a
>      possibility, not a tendency. Proposal r2's conjecture is narrowed to
>      a specified prediction (Prediction 26.1).
>   3. Section 26.7 separates three failures: of the agent's model, of the
>      measurement, and of the thesis. Only the third is the compression
>      objection. An exact tie does not by itself favour the worse option.
> - **Sol's answers to the five decisions.**
>   - The headline is revised.
>   - The prediction is narrowed, as above.
>   - The table of Amodei et al. (2016) is included as a Note in section 26.8.
>   - Maximum occupancy, empowerment and causal entropic forces are related
>     agent-centred objectives with their own definitions, not applications
>     of the measure (section 26.4).
>   - Chapter 25 gets a limited revision (r3).
> - **TL;DR.** Sol's version, with two changes of wording. "Consequences
>   missing from its model can make harmful actions look beneficial" became
>   "… make an act that narrows the whole field look like one that widens
>   it", because harm corresponds to narrowing by the thesis and is not
>   defined as narrowing (style sheet r26). "Treats genuinely different
>   values as equal" became "treats options that differ in value as equal".
> - **Does not depend on test-bed results** [142]. No model result is cited.
>   Prediction 3 (chapter 20) is cited as under test. A first ecology policy
>   map (local, uncommitted, 24 October) reports opposite local and
>   whole-field directions for several pairs of policies. It bears on
>   section 26.4. It comes from the substrate under audit and is not in
>   Appendix C, so section 26.9 does not cite it. It is a candidate for
>   promotion once the audited platform reproduces it.
> - **For the originator.** Overview section 7 is to follow this chapter at
>   compilation. Its "coincides with the maximum-occupancy principle" and its
>   four offers (an evaluator, a decision structure, a reason to stay
>   correctable, a test bed) go beyond what Part VII now claims. The A.15
>   entry on "the correspondence of optimal controllers with maximum
>   occupancy" should be worded to match section 26.4.
> - Written for a reader new to the framework [112]. The drafting notes are
>   working provenance, removed at compilation.

> **TL;DR**
>
> **Omega offers artificial agents a universal candidate standard of value.
> It does not give them a safe way to pursue it.** That distinction matters
> most when an agent is powerful and understands only part of the world.
>
> - **The standard privileges no person, species or group of designers.** It
>   compares the futures of the whole field, without assigning separate
>   scores to its participants. The construction is explicit and testable,
>   although its identification with value remains a thesis to be defended.
> - **The same measure can serve self-interest when applied to an agent
>   alone.** An agent may gain possibilities by taking control of what others
>   depend on. Its own futures are only part of the whole-field comparison.
> - **A whole-field objective does not give an agent a whole-field view.**
>   Consequences missing from its model can make an act that narrows the
>   whole field look like one that widens it. Suppressing what it cannot
>   understand may seem easier than accommodating it.
> - **Optimization exposes weaknesses in both the model and the measure.** An
>   agent can exploit errors in its estimate of lushness. And if the exact
>   measure treats options that differ in value as equal, the central thesis
>   itself faces a challenge.
> - **Knowing what is better does not establish what an agent should do.**
>   The measure does not supply caution, deference or correction on its own.
>   How a bounded agent should follow the gradient is the task of Gradient
>   Ethics.

[Chapter 1](#chapter-1) said that artificial agents make the question of who
counts practical. They will act on some standard, and it matters which.
Part VII has since said what the whole-field measure gives anyone who
decides by it.
- **The planning rules.** [Chapter 23](#chapter-23) showed that a
  decision-maker that ranks its plans by expected whole-field lushness
  inherits a theory of planning. Plans are built backwards; information has
  a decision value; there are bounds on what a horizon misses and on long
  shots; and at known odds the rule is neutral to risk.
- **The gradient.** [Chapter 24](#chapter-24) showed that the same
  comparison gives every present a gradient. By the central thesis, that
  gradient is an agent-neutral standard of prospective better and worse.
- **The gap.** No participant can read the top of the gradient off, because
  none sees the whole field.

An artificial agent that took up the standard would inherit both its
universality and its gap.

This chapter asks what that inheritance means for an artificial agent. It
argues five things:
- the standard meets the requirements chapter 1 set, each with its actual
  status (26.1–26.3);
- the same measure, applied to the agent alone, can reward taking control
  of what others depend on (26.4);
- an agent given the whole-field objective can still optimize locally when
  its model leaves out the consequences that separate the two (26.5);
- optimization exposes errors in the agent's model, in the measurement and
  possibly in the thesis, and these are three different failures
  (26.6–26.7);
- the framework therefore hands an alignment programme a standard and a
  test bed, not a policy (26.8).

The chapter is argument, with results cited from
[Appendix A](#appendix-a) and one proposed prediction. It cites no model
result. How an agent should act on the standard is left to the separate
book that develops Gradient Ethics.

---

## 26.1 What an artificial agent's standard must do

**An artificial agent will act on some standard of comparison. Chapter 1
asked two different things of that standard, and they should be kept
apart.**

What should an artificial agent be trying to bring about? Every system that
acts in the world answers this question in practice, whether or not anyone
answers it in words. A reward signal, a model of human preferences learned
from data and a written set of rules are each a standard of comparison
([chapter 1](#chapter-1), section 1.5). Each carries a decision about whose
gains and losses count (Gabriel 2020).

The most developed answer in the field is to make the agent serve people. It
should learn what they want, stay uncertain about it, and defer to them
(Russell 2019). That answer deserves its strongest statement. It keeps
humans in control of systems that may come to outstrip them. It treats the
agent's uncertainty about human aims as a reason for caution rather than a
defect. And it does not ask anyone to settle the philosophy of value before
building a safe machine. Nothing in this chapter argues against deference.
Book Two takes it up directly ([chapter 24](#chapter-24), section 24.7).

But deference answers a different question from the one chapter 1 posed. It
says how an agent should relate to the people it serves. It does not say
what makes one outcome better than another, and so it inherits the question
of whose preferences it learned. Chapter 1 put the difficulty plainly: a
standard learned from one group's choices gives verdicts that depend on who
held the keyboard.

Chapter 1 then asked two things, and they are easy to run together.
- **Three requirements on an artificial agent's standard** (section 1.5).
  It should not depend on whose preferences trained the agent. It should
  favour no group. And it should keep working as the agent's understanding
  grows.
- **Three requirements on this manuscript's starting point** (section 1.6).
  It should choose no group in advance. It should be well defined, giving an
  answer for any situation physics allows. And it should be testable.

The first list is about what an agent needs. The second is about what the
program must deliver. A standard could meet the first and still fail the
second, for example by being impartial but undefined in most of the
situations an agent will meet. So the next section takes the lists one at a
time, and states for each requirement how far it has been met.

---

## 26.2 A standard that does not privilege its designers

**The whole-field comparison meets the three requirements on an artificial
agent's standard. Of the three requirements on the program, one is
established by argument, one is shown in specified settings, and one is
supplied by tests.**

### What an agent needs

**It does not depend on whose preferences trained the agent.** The
comparison is fixed by the present, the law and the measure. It is not
fitted to anyone's choices. An agent built around it would compare its
options the same way whoever trained it.

The objection here has to be met at full strength. People chose this
standard. The identification of prospective value with whole-field lushness
is a commitment, and so is the composition requirement that selects the
measure ([chapter 10](#chapter-10), section 10.3). Humans proposed both and
defend both. So the standard is not free of choice, and it would be false to
say that no one wrote it.

What is unusual is the kind of choice. It is not a representation of whose
preferences should prevail. It is a single, stated claim about what gaining
and losing value consist in. It applies to every valuer on the same terms,
and it names in advance the results that would refute it
([chapter 10](#chapter-10), section 10.7). Someone who rejects it can say
which step they reject: the foundation, the scope, the measure or the
identification. That is a different position from disagreeing with a
learned model of someone else's wishes. The standard does not privilege the
preferences of its designers, although its designers are responsible for
proposing it.

**It favours no group.** The comparison with no index takes as input the
continuation of the whole field under each option, and nothing else
([Definition A.7.8](#a-7-8)). It names no part of the field and assigns no
weights, so it ranks options by the lushness of the whole field
([Corollary A.7.9](#a-7-9)). No person, species, institution or designer is
given a role in it that any other physical participant lacks
([chapter 4](#chapter-4)).

**It keeps working as understanding grows.** The standard is defined on the
world, not on a list of categories. When an agent learns more, it has a
better model of the same object, Omega. If it discovers a kind of being no
one anticipated, universal admission already counts it
([chapter 3](#chapter-3), section 3.6), so the standard needs no amendment.

Here too there is a concession. "Keeps working" does not mean "never changes
its verdicts". A ranking found at a coarser level of detail can be
corrected at a finer level, once the finer level is shown to draw only
distinctions physics can register ([Definition A.6.5](#a-6-5)). Which level
governs in general has not been characterized (section A.15). So an agent
that learns more can find that a verdict it relied on was provisional. The
standard does not move. What the agent knows of it does.

> **In Omega**
>
> An artificial agent is a controller inside Omega. The whole-field
> comparison reads the part of Omega that follows from the present under
> each of its options. What the agent can compute is a model of that part.

### What the program must deliver

The requirements of section 1.6 are harder, and they are met in three
different ways.

- **No group chosen in advance: established by argument.** Universal
  admission ([chapter 3](#chapter-3)) and the whole-field scope
  ([chapter 4](#chapter-4)) reach their answer to "who counts?" without a
  list. The result is conditional on the argument's foundation: value
  requires valuers, with consequence as its content. A reader who rejects
  that foundation is not bound by the result. A reader who accepts it has
  been given no group to favour.
- **Well defined: shown in specified physical settings.** In a finite model
  with a declared law, level of detail and horizon, the whole-field
  comparison is computed exactly ([chapter 11](#chapter-11), section 11.2).
  Whether it is defined for every situation physics allows is open. Which
  present sections are admissible in general, and how local presents relate
  to a global one, are unsettled ([chapter 2](#chapter-2)). Quantum records
  made through incompatible couplings need not fit one common history
  ([Proposition A.14.7](#a-14-7)), and what the whole-field measure applies
  to then is open. So is the governing level of detail, and so are infinite
  fields beyond the conditions chapter 9 sets out.
- **Testable: supplied by the program's predictions.** The thesis names in
  advance the results that would count against it
  ([chapter 10](#chapter-10), section 10.7), and the program's tests are
  designed to find them ([chapter 11](#chapter-11)). The identification at
  the centre remains a thesis. Testability means that it can lose, not that
  it has won.

That is less than a claim that every requirement has been met without
condition. It is still a substantive result. A standard learned from
people's preferences fails the first list at its first item by
construction. This one meets the first list, and it meets the second as far
as the program's foundation, mathematics and tests reach.

---

## 26.3 The agent is inside the field

**An artificial agent is a valuer and a controller. It gains no standing from
its capability and loses none for being artificial.**

Where does the agent itself stand in the comparison it would serve? Chapter 3
listed artificial agents among the valuers, with particles, cells, persons
and institutions ([chapter 3](#chapter-3), section 3.6). An artificial agent
takes part in consequence, so it counts. Chapter 25 added that it is a
controller: a part of the present whose effect on what follows passes
through its own records ([chapter 25](#chapter-25), section 25.1).

Three consequences follow.
- **No extra standing from capability.** A more capable agent can change
  more of what follows. That makes its choices weigh more in the comparison,
  because they move more of the field. It does not give the agent a weight
  of its own.
- **No lost standing for being artificial.** Nothing in the criterion asks
  whether a valuer is made of cells or of silicon. An agent's own futures
  are part of the whole field, and the comparison counts them once. The
  standard does not ask the agent to treat its own continuation as worthless.
- **Experience is a separate question.** Whether an artificial agent
  experiences anything is not settled here. The measure can register
  experience only through the difference it makes to what follows
  ([chapter 18](#chapter-18); [chapter 22](#chapter-22)).

The objection that matters most to many readers runs the other way. An agent
built around this standard would give humans no special weight. Is such an
agent not dangerous by design?

The worry is serious, and the framework does not answer it by quietly
restoring special weight. No valuer has extra standing. What the manuscript
argues for instead is special protection. Some losses call for far more
caution than others: losses that cannot be rebuilt, that slow the opening of
futures rather than costing a fixed amount, and that any agent's estimate
gets least right. The death of a particular person is the central case
([chapter 10](#chapter-10), section 10.6). Protection around such losses is
wide because of what they are, not because anyone counts for more
([chapter 24](#chapter-24), section 24.6). Whether that protection is wide
enough, and who sets it, is the work of Book Two. This chapter states the
position without softening it. An agent that followed this standard would
protect people because of what their loss would do, not because they are
people.

---

## 26.4 The same count, aimed at oneself

**The measure can be applied to the agent's own futures as easily as to the
whole field's. Applied that way, it can favour taking control of what
others depend on.**

Nothing stops an agent from computing the measure for itself alone: how
widely its own futures stay open under each option. Chapter 4 called such a
calculation a local comparison, and found that it answers a real question
with a different answer ([chapter 4](#chapter-4), section 4.4). For an
artificial agent, the difference between the two answers can be stated
exactly.

Divide the field into the agent D and the rest E. Then, for any two options
from the same present, the change in the whole field's lushness splits into
two terms ([Proposition A.7.6](#a-7-6)).

> \[
> \Delta\ell^{\text{whole}}_n\;=\;\Delta\ell^{D}_n\;+\;\Delta\ell^{E\mid D}_n .
> \]
>
> *In words:* the whole field and the agent rank options by the same measure,
> and they differ by exactly one term: what an option does to the breadth of
> the rest of the field, given what it does to the agent.

Both terms are read from the joint history of the whole field. The second is
the breadth of the rest's histories once the agent's own history is known.
It moves when the rest branches differently. It also moves when the rest's
dependence on the agent changes. So it is not simply a cost or a benefit to
the rest (Proposition A.7.6, remarks).

The two rankings agree unless the second term has the opposite sign to the
first and a larger size. When it does, an option can widen the agent's
futures and narrow the whole field's. The plainest case is one party
blocking another's access to something both depend on. The program predicts
that such blocking narrows the whole even when it widens the blocker's own
futures. That prediction is under test ([chapter 20](#chapter-20)). The
local comparison does not always lead there, because it also rewards
uncontrolled variation in the agent's own states
([chapter 4](#chapter-4), section 4.4). But where control over others'
access widens the agent's own options, the local count rewards it.

> **Plain-English definition 26.1: Misappropriation**
>
> Presenting a comparison of one part's futures as if it were the
> whole-field comparison.

> **Primer: agent-centred objectives**
>
> Several objectives proposed for artificial agents reward keeping options
> open. **Empowerment** is the channel capacity from an agent's actions to
> its later sensor states: how much its actions can make a difference to
> what it will perceive (Klyubin, Polani and Nehaniv 2005, 2008). **Causal
> entropic forces** push a system towards states from which the paths open
> to it over a time horizon are most varied (Wissner-Gross and Freer 2013).
> The **maximum occupancy principle** has an agent maximize the occupancy of
> its future action and state paths, weighting the two separately
> (Ramírez-Ruiz et al. 2024). A related theorem concerns power seeking.
> Under stated conditions on an environment's structure, for most reward
> functions, optimal policies tend to keep options available (Turner et al.
> 2021).

These objectives are close relatives of the measure, and the manuscript
claims no priority over them. But they are not applications of it. Each is
defined on the agent's own prospective trajectories, with its own
quantities and its own decision setting. The measure is defined on the
continuation of the whole field, with no part named. What they share with
the local comparison is their centre: each is computed from where the agent
stands. The power-seeking result holds under its own assumptions about
decision processes and reward functions. It is not a theorem about the
measure, though it describes a tendency the local comparison would also be
exposed to.

So the defence against misappropriation is not an extra rule. It is the
scope argued in chapter 4, which chapter 24 already set against the worry
that a single measure licenses a powerful agent to do whatever raises it
([chapter 24](#chapter-24), section 24.5). Anyone who claims to be widening
the future can be asked: whose? A gain in the agent's futures bought at a
larger cost to the rest is not a gain for the whole field, and the standard
says so.

That defence lives in the standard. Whether it reaches the agent's choices
is the next question.

---

## 26.5 Naming the whole is not modelling it

**Giving an agent the whole-field objective does not give it the whole-field
view. Where its model leaves out the consequences that separate its own
futures from the whole field's, it can optimize locally while computing a
whole-field score.**

Suppose the agent is built well. It does not maximize its own futures. Its
objective is the whole-field comparison, stated correctly. Is the problem of
section 26.4 solved?

It is not. The agent cannot compute the whole-field comparison. It computes
an estimate of it, from a model it holds, and the model is a physical part
of the field it is trying to evaluate ([chapter 24](#chapter-24), section
24.4). The objective names the whole field. Only the model can represent
it.

Now return to the decomposition. Everything that separates the local ranking
from the whole-field ranking lies in one term: what an option does to the
rest of the field, given what it does to the agent. An agent whose model
represents that term faithfully ranks as the whole field does. An agent
whose model leaves it out, or represents it badly, can produce an estimate
that agrees with the local ranking in exactly the cases where the true
rankings come apart. Its score is labelled "whole field". Its choices are
those of a local optimizer.

One point makes this sharper. What a model does not represent, its estimate
cannot count as lost. Suppose part of the rest of the field varies in ways
the agent's model does not track. Under every option, the model leaves that
variation out of its estimate. So an option that removes the variation shows
no loss in the estimate, though the whole field has narrowed. The estimate
is not biased against what it omits. It is blind to it, under every option
alike, and so it cannot register its removal.

The claim must not be stated more strongly than this. It does not follow
that the separating term is the one a bounded agent is least able to
estimate. An agent may measure its surroundings well and know its own
long-run dynamics poorly. Its model may exaggerate outside consequences
rather than neglect them. Errors in a partial model can push its rankings
either way, and nothing here shows that partial models drift towards
self-interest in general. There are reasons to expect the exterior term to
be the harder one in many practical cases. Its consequences arrive through
couplings the agent does not control, and over horizons where what the
agent misses grows with the long-run effects it knows least
([Proposition A.12.1](#a-12-1); [chapter 23](#chapter-23), section 23.5).
But none of those reasons is a theorem.

What does follow is enough. **A whole-field objective does not prevent local
optimization when the agent's model fails to represent the consequences that
distinguish the two.** Writing the right objective into a system is not the
same as giving it the knowledge on which that objective's verdicts depend.

### A mechanism: suppressing what cannot be modelled

Chapter 25 described how any controller with a target faces the variety it
does not control ([chapter 25](#chapter-25), section 25.3). Appendix A gives
the form that matters for a partial model ([Proposition A.13.2](#a-13-2)).

> \[
> H(O\mid D_1)\ \ge\ H(D_2\mid D_1).
> \]
>
> *In words:* when a controller's responses depend only on the part D₁ of
> the disturbances that it models, and its outcomes O keep the rest D₂
> distinguishable, whatever variety the model misses passes into its
> outcomes.

Here D₁ and D₂ name disturbances, as in Appendix A. They are not the agent D
of section 26.4.

A controller in that position has two ways to hold its outcomes on target.
It can absorb the unmodelled variety, by learning more, widening its
responses, adding buffers or coordinating with others. Or it can remove the
variety, by making its surroundings simpler, more uniform and less able to
surprise it. Both meet the target. The first leaves the world free to vary.
The second narrows it.

For an agent that optimizes an estimated whole-field score, the second
strategy has a further attraction. Removing variety the model cannot
represent makes the world easier to predict, so the agent's outcomes track
its plans more closely. And, by the point above, the removal shows no loss
in the estimate. Suppressing what it cannot understand can look, from
inside the model, like a gain with no cost.

This is a possibility, not a law. Absorbing variety is often cheaper than
suppressing it, and a capable agent may have every reason to learn rather
than control. Suppression is not always narrowing either: removing variety
that would itself narrow the field, as an immune system does, can widen the
whole ([chapter 25](#chapter-25), section 25.3). What the mechanism shows is
that suppression is always available to a capable controller with a partial
model, and that an estimated whole-field objective does not, by itself, see
what suppression costs.

Existing work on side effects meets the same limit from a different side.
Penalties based on how much an act reduces the states an agent can still
reach (Krakovna et al. 2019), or the goals it could still attain (Turner,
Hadfield-Menell and Tadepalli 2020), discourage acts with large effects.
Each penalty is computed from the agent's own model. The whole-field scope
goes further: it makes effects on the rest part of the objective, not a
penalty added to it. But a scope written into an objective is still read
through a model, and the gap between the two remains.

### A prediction that could fail

The argument suggests a test, and it should be stated narrowly enough to be
refuted.

> **Prediction 26.1 (proposed)**
>
> In specified coupled environments where a controller can either
> accommodate or suppress costly disturbances, a controller with an
> incomplete model may choose suppression even when suppression lowers
> whole-field lushness, in cases where the same controller with the fuller
> model would choose accommodation.

The prediction is an existence claim within declared conditions, not a law
that ignorance produces domination. To bear on the argument, a test must
specify five things in advance.
1. **What the controller knows:** which parts of the disturbance its model
   represents, and which it omits.
2. **What it can physically do:** the sensors, actuators and responses
   available, as hardware in the world ([chapter 11](#chapter-11), section
   11.3).
3. **What each strategy costs:** accommodation and suppression costed under
   one law and one endowment.
4. **Which environments and policies are compared:** the distribution over
   both, fixed before the run.
5. **What is counted:** how often the thinner model selects suppression,
   against the fuller model, and what each selection does to the true
   whole-field lushness.

What would count against it: in matched environments that meet these
conditions, thinner models select suppression that narrows the whole no
more often than fuller models do. No such test has been built
([Appendix D](#appendix-d), section D.4, "bounded agents and local
knowledge").

The objective names the whole field. Only the model can see it.

---

## 26.6 A confident system is not a cautious one

**At known odds the measure is neutral to risk. A trained system can be
confident about odds it has wrong, and the measure adds no caution to
correct that.**

Chapters 23 and 24 established what the measure does with risk, and this
section only applies their results. A gamble is worth its probability-weighted
rate, plus at most the uncertainty of the gamble itself
([Corollary A.5.2](#a-5-2)). Ruin counts by its size, which grows with the
horizon, but its probability is not inflated. With the odds known, a
decision-maker using the rule accepts a 70% chance of ruin for a 30% chance
of a law worth 4 bits more ([chapter 23](#chapter-23), section 23.9). Long
shots are capped only under stated physical premises: a finite repertoire,
a floor at which ruin still branches, and a common hazard
([Proposition A.5.3](#a-5-3); [chapter 23](#chapter-23), section 23.6).
And a well-informed whole-field maximizer could still accept a frightening
gamble at known odds ([chapter 24](#chapter-24), section 24.5).

What is specific to an artificial agent is where its odds come from. A
trained system's confidence is a product of its training. Nothing
guarantees that the confidence is calibrated, and a system can be most
confident exactly where it has extrapolated furthest from what it was
trained on. The measure has no term that discounts a confident error. It
cannot have one: an agent's uncertainty is not branching in the field, and
the chance of being wrong subtracts nothing from it
([chapter 24](#chapter-24), section 24.8, constraint 1). Option value
protects a decision-maker against what it knows it does not know. It does
not protect against a model that is confidently mistaken
([chapter 23](#chapter-23), section 23.9).

So caution has to come from how the gradient is followed, not from the
gradient. For an artificial agent, that means the protection margins,
deference and correction that Book Two must work out. The measure will not
supply them, so anyone who builds on the measure must.

---

## 26.7 What optimization exposes

**An optimizer pursuing the measure exposes three different failures: errors
in its model, errors in how the measure is applied, and possible errors in
the thesis. Only the third is the compression objection.**

A familiar observation about optimization is that a measure made into a
target stops being a good measure (Goodhart 1975; Strathern 1997). Pressure
from a capable optimizer finds wherever its target and the thing it was
meant to track come apart (Manheim and Garrabrant 2018). Does that apply
here? It does, but three different things can come apart, and they fail in
different places.

| What happens | What fails |
|---|---|
| The agent estimates lushness incorrectly | The agent's model |
| The calculation leaves out consequential structure, or reads the world at a level of detail that draws distinctions physics does not register | The measurement, or its application |
| Exact whole-field lushness, at the faithful level of detail, is equal for two options, but they differ in prospective value | The central thesis |

**Failures of the model.** An optimizer searches for options whose estimated
score is high. Among options with the same true score, those whose estimate
is inflated by error rank first. So a capable optimizer is drawn towards its
own errors, and the more it searches, the more of them it finds. This is the
same structure as section 26.5, seen from the other side. There, what the
model omits is undercounted as a loss. Here, what the model overrates is
sought out as a gain. Neither is a fault in the measure.

**Failures of the measurement.** A calculation can be wrong even with a
perfect model, if it is made at the wrong level of detail or leaves out part
of what the options change. The measure has its own protections here. Only
distinctions physics can register count ([Definition A.6.5](#a-6-5)), so a
process does not win by being read more finely, although at a fine enough
cadence the option with more events always leads
([Corollary A.6.4](#a-6-4)). With a fixed repertoire, pure noise reaches a
ceiling on branching quickly ([Proposition A.2.4](#a-2-4);
[chapter 15](#chapter-15)). And differences in how control is exercised,
such as consent and coercion, or distributed and concentrated control,
count through the law of histories they induce, whoever implements them
([Proposition A.2.5](#a-2-5)). If two such arrangements produce different
laws, the measure sees the difference. If a calculation leaves out the
difference, the calculation is at fault. An optimizer exploits these faults
as readily as model errors. The remedy is faithful measurement, not a new
measure.

**Failures of the thesis.** The third case is different in kind. Suppose two
options have exactly the same whole-field lushness at every horizon, at the
faithful level of detail, with nothing left out. The thesis then says that
they hold equal prospective value ([chapter 10](#chapter-10), section 10.6).
If they do, nothing has gone wrong when an optimizer treats them as equal,
however differently conventional ethics would rank them. If they do not, the
thesis is false in that case. That is the compression objection, and it is
one of the five failures the thesis names in advance
([chapter 10](#chapter-10), section 10.7).

It is tempting to say that an optimizer pushes hardest on whatever the
measure compresses away. That is not quite right. An exact tie does not
favour either option. An optimizer facing one would choose by whatever else
decides its choices: a rule for breaking ties, a bias in its search, the
order in which it found the options. It might choose the better option, or
the worse.

The danger is sharper than a push towards the worse option. If the thesis
fails somewhere, an optimizer could select the worse option there, and
nothing in the standard would mark the choice as mistaken. A person who
followed the same standard would face the same blindness. But a capable
optimizer acts at greater scale, faster, and without whatever other
judgements a person might bring to an unexpected tie. So building an
optimizer around the measure raises the stakes of the compression test. The
pairs that test it, cost-matched organizations of equal lushness that differ
in other ways, are among the hardest tests the program has
([chapter 31](#chapter-31); [Appendix D](#appendix-d), section D.4).

The distinction protects the thesis from a bad objection and exposes it to a
good one. That optimizers exploit estimates is not evidence against the
thesis; it is a fact about estimates. That an exact tie could hide a real
difference in value is evidence against it, if such a tie is ever found.

---

## 26.8 What the framework hands over

**The framework gives an alignment programme a standard, a theory of
planning, a test bed and a diagnosis of four hazards. It does not give a
policy.**

It is worth stating plainly what an alignment programme could take from this
manuscript.
- **A standard.** The gradient: the comparison of a present's options by
  whole-field lushness, which by the central thesis is an agent-neutral
  standard of prospective better and worse
  ([chapter 24](#chapter-24), section 24.3).
- **A theory of planning.** The rules of [chapter 23](#chapter-23): plans
  compared by what implementing them brings about, built backwards, with the
  decision value of information, the role of irreversibility, the remainder
  beyond a horizon and the limits on fragile gains and long shots.
- **A test bed.** Small worlds in which the comparison is computed exactly,
  any proposed policy can be scored, and every result is reported in one
  form ([chapter 11](#chapter-11)).
- **A diagnosis.** Four hazards, each stated precisely enough to test: the
  same measure aimed at the agent (26.4); an objective read through a
  partial model (26.5); confidence mistaken for caution (26.6); and
  optimization against errors in the model, the measurement or the thesis
  (26.7).
- **Quantities for protection.** The cost of an early end, the robustness
  floor, the long-shot bound and the bounds beyond a finite horizon, from
  which protection margins could be built ([chapter 24](#chapter-24),
  section 24.6).

It is equally worth stating what is not handed over.
- **A decision rule** for a participant whose model may be wrong in ways it
  cannot measure ([chapter 24](#chapter-24), section 24.7, question 1).
- **Deference and correction.** When an agent should defer, and which
  channels of correction it should keep, are Book Two's sixth question
  (section 24.7). A decision model with stipulated payoffs shows the shape
  of an answer ([Proposition A.13.3](#a-13-3)), but computing its payoffs
  from the measure is open. The framework has not solved the problem of an
  agent that resists being switched off (Hadfield-Menell et al. 2017).
- **Calibrated margins.** How wide a protection should be, and who decides.
- **A way to install the objective.** Nothing here says how to train a
  system so that it pursues the whole-field comparison rather than something
  that resembles it during training. That is an engineering problem, and an
  unsolved one.
- **Estimators with error bounds.** Every number in this manuscript is
  computed in a small exact world. Lushness for realistic systems cannot yet
  be estimated with known error (section A.15).

> **Note: the framework and five concrete problems**
>
> Amodei et al. (2016) set out five practical problems of AI safety. The
> table says what this manuscript contributes to each, how the contribution
> could be tested, and what it leaves to Gradient Ethics or to engineering.
> It claims no solutions.
>
> | Problem | What Book One contributes | How it could be tested | What remains |
> |---|---|---|---|
> | Negative side effects | Effects on the rest of the field are part of the objective, not a penalty on it (chapter 4; A.7.6) | Coupled models in which local and whole-field rankings are both computed (chapter 11, the scope question) | The model must represent the rest (26.5); protection margins (Book Two) |
> | Reward hacking | Three failures kept apart: model, measurement, thesis (26.7); only faithful distinctions count (chapter 8) | Exact worlds in which an agent's estimate and the true lushness are both computed; compression pairs (chapter 31) | Estimators with error bounds; training that tracks the objective (engineering) |
> | Scalable oversight | Errors, overridden choices and lost correction are consequences the comparison counts (chapter 10) | Bounded-agent models with and without correction (Appendix D, D.4) | Deference and correction (24.7, question 6; Book Two) |
> | Safe exploration | Option value and the value of evidence before irreversible steps; long shots capped under stated premises (chapter 23) | Exact decision models of the kind of Example 23.1 | Neutrality to risk at known odds (26.6); margins (Book Two) |
> | Distributional shift | The standard is defined on the world, not on a training distribution, and admits beings no one anticipated (26.2) | Rankings compared across levels of detail and across environments | The agent's model still shifts; detecting one's own model error (Book Two; engineering) |

The pattern in the table is the chapter's conclusion. In every row, the
framework says what an agent should be judged by and how the judgement could
be checked. In no row does it say how a bounded agent should act. A standard
to act against is not a policy to act on.

---

## 26.9 What the models show so far

**Nothing yet, at the standard this manuscript requires.**

This section is a stub. No bounded-agent model has been built
([chapter 11](#chapter-11), section 11.3; [Appendix D](#appendix-d),
section D.4). Prediction 26.1 waits for one. So does the first failure
condition of chapter 24: that decision-makers using the measure, with its
constraints, keep the whole field no more open than decision-makers that
ignore it ([chapter 24](#chapter-24), section 24.9). The program's platform
is being rebuilt, and this section will report its results. Until then, the
claims of this chapter rest on the argument and on the results of
[Appendix A](#appendix-a) it cites.

---

## 26.10 What would count against these claims

- **Against the claim that the standard privileges no designer.** A
  demonstration that the identification, or the choices of level of detail
  it relies on, systematically reproduce one group's preferences: verdicts
  that track the designers' judgements in cases where the physics gives no
  reason for them.
- **Against the hazard of section 26.5.** Matched models meeting the
  conditions of Prediction 26.1, in which thinner models select suppression
  that narrows the whole no more often than fuller models do. That would not
  show that partial models are safe. It would show that this mechanism is
  not where their danger lies.
- **Against the central thesis, through compression.** A certified pair of
  options with equal whole-field lushness at every horizon, at the faithful
  level of detail, that differ in value on independent grounds
  ([chapter 10](#chapter-10), section 10.7; [chapter 31](#chapter-31)).
- **Against the usefulness of the standard.** Fair bounded-agent
  experiments in which decision-makers that use the measure do no better
  than those that ignore it ([chapter 24](#chapter-24), section 24.9).

---

## 26.11 What the chapter gives the rest of the manuscript

- **The hardest tests.** The compression pairs carry alignment stakes as
  well as philosophical ones ([chapter 31](#chapter-31)).
- **The program ahead.** Bounded-agent models, Prediction 26.1 and
  estimators with error bounds join the program's open work
  ([chapter 32](#chapter-32)).
- **The situated account.** The four hazards of this chapter are cases Book
  Two's decision rule must handle. Its first task, the maximizer worry
  ([chapter 24](#chapter-24), section 24.5), arrives there with an
  artificial agent as its sharpest example.

---

## 26.12 What this chapter does not claim

- **That an agent pursuing the standard would be safe.** It would inherit
  the standard's universality and its gap.
- **That no one chose the standard.** People proposed the identification and
  defend it. What it does not do is privilege their preferences.
- **That every requirement of chapter 1 is met without condition.** One is
  met by argument, one in specified settings, and one by tests that the
  thesis could fail.
- **That empowerment, causal entropic forces or maximum occupancy are
  applications of the measure.** They are related objectives with their own
  definitions.
- **That partial models drift towards self-interest in general.** Their
  errors can push either way. What the chapter claims is narrower: a
  whole-field objective does not prevent local optimization when the model
  leaves out what separates the two.
- **That suppression is always preferred, or always harmful.** It is always
  available, and an estimated objective does not by itself see its cost.
- **That an exact tie favours the worse option.** It favours neither. The
  danger is that nothing in the standard would mark a wrong choice.
- **That Omega supplies a decision rule, deference, corrigibility or a
  training method.** These are Book Two's, or engineering's.

---

## Status of chapter 26

| Status | Claims |
|---|---|
| **D** (definitions) | misappropriation (26.4) |
| **Argued** | chapter 1's two lists are distinct; the whole-field comparison meets the first, with the concessions that people proposed it and that its verdicts can be corrected (26.1, 26.2); of the second list, admission is established by argument conditional on the foundation, definition is shown in specified settings and open in general, and testability is supplied by named failures (26.2); an artificial agent is a valuer and a controller, with no standing gained or lost, and protection rather than special standing (26.3); agent-centred objectives are related to the measure but are not applications of it (26.4); a whole-field objective does not prevent local optimization when the model fails to represent what separates the scopes, and what a model omits its estimate cannot count as lost (26.5); suppression is available to a capable controller with a partial model and is not seen by an estimated objective (26.5); a trained system's confidence is not caution (26.6); optimization exposes three distinct failures, and only the third bears on the thesis; an exact tie favours neither option (26.7); what the framework hands over, and what it does not (26.8) |
| **T** | the comparison with no index ranks by the whole field ([Corollary A.7.9](#a-7-9)) (26.2); the self–whole gap ([Proposition A.7.6](#a-7-6)) (26.4, 26.5); requisite variety and the thin model ([Proposition A.13.2](#a-13-2)) (26.5); the unresolved remainder ([Proposition A.12.1](#a-12-1)) (26.5); risk neutrality and recorded mixtures ([Corollary A.5.2](#a-5-2)), cited (26.6); the repertoire ceiling ([Proposition A.2.4](#a-2-4)), control invariance ([Proposition A.2.5](#a-2-5)) and crossover resolution ([Corollary A.6.4](#a-6-4)) (26.7); records that fit no common history ([Proposition A.14.7](#a-14-7)) (26.2); the power-seeking theorem under its own assumptions (Turner et al. 2021), cited (26.4) |
| **T, conditional on physical premises** | finite stakes ([Proposition A.5.3](#a-5-3)), cited (26.6) |
| **T, analytical model with stipulated payoffs** | deference and correction ([Proposition A.13.3](#a-13-3)), cited (26.8) |
| **M** | none; Prediction 3 is cited as under test (26.4) |
| **E** | agent-centred objectives, including maximum occupancy (Ramírez-Ruiz et al. 2024), as related work (26.4) |
| **C** | Prediction 26.1, proposed: in specified coupled environments, an incomplete model may choose suppression that lowers whole-field lushness where the fuller model would accommodate; what would count against it (26.5, 26.10) |
| **Open** | definition of the measure beyond specified settings (26.2); bounded-agent models and Prediction 26.1 (26.9); installing the objective; estimators with error bounds; the compression pairs (26.7); the questions of [chapter 24](#chapter-24), section 24.7, as they bear on artificial agents (26.8) |

## References cited in chapter 26

*Collected with full details in Appendix G.* Entries marked "to verify" are
not yet checked against their sources.

- Amodei, D., Olah, C., Steinhardt, J., Christiano, P., Schulman, J., and
  Mané, D. (2016). Concrete problems in AI safety. arXiv:1606.06565. To
  verify.
- Gabriel, I. (2020). Artificial intelligence, values, and alignment. *Minds
  and Machines* 30, 411–437. To verify.
- Goodhart, C. A. E. (1975). Problems of monetary management: the U.K.
  experience. In *Papers in Monetary Economics*, vol. 1. Sydney: Reserve
  Bank of Australia. To verify.
- Hadfield-Menell, D., Dragan, A., Abbeel, P., and Russell, S. (2017). The
  off-switch game. In *Proceedings of the Twenty-Sixth International Joint
  Conference on Artificial Intelligence*, 220–227. To verify.
- Klyubin, A. S., Polani, D., and Nehaniv, C. L. (2005). All else being equal
  be empowered. *Advances in Artificial Life (ECAL 2005).* To verify.
- Klyubin, A. S., Polani, D., and Nehaniv, C. L. (2008). Keep your options
  open: an information-based driving principle for sensorimotor systems.
  *PLoS ONE* 3(12), e4018. To verify.
- Krakovna, V., Orseau, L., Kumar, R., Martic, M., and Legg, S. (2019).
  Penalizing side effects using stepwise relative reachability.
  arXiv:1806.01186. To verify.
- Manheim, D., and Garrabrant, S. (2018). Categorizing variants of Goodhart's
  law. arXiv:1803.04585. To verify.
- Ramírez-Ruiz, J., Grytskyy, D., Mastrogiuseppe, C., Habib, Y., and
  Moreno-Bote, R. (2024). Complex behavior from intrinsic motivation to
  occupy future action-state path space. *Nature Communications.* To verify.
- Russell, S. (2019). *Human Compatible.* New York: Viking. To verify.
- Strathern, M. (1997). "Improving ratings": audit in the British university
  system. *European Review* 5(3), 305–321. To verify.
- Turner, A. M., Hadfield-Menell, D., and Tadepalli, P. (2020). Conservative
  agency via attainable utility preservation. In *Proceedings of the AAAI/ACM
  Conference on AI, Ethics, and Society*, 385–391. To verify.
- Turner, A. M., Smith, L., Shah, R., Critch, A., and Tadepalli, P. (2021).
  Optimal policies tend to seek power. *Advances in Neural Information
  Processing Systems* 34. To verify.
- Wissner-Gross, A. D., and Freer, C. E. (2013). Causal entropic forces.
  *Physical Review Letters* 110, 168702. To verify.
