# 8. Parts and wholes

> **Drafting note (r3, 23 October).**
> - Sol's review of r2. Structure, examples and the short TL;DR kept.
>   - **The rest-given-the-part term is not a cost** (8.6). It moves when the
>     rest branches differently or when its tie to the part changes, and
>     Example 8.4 shows the second alone. It fixes the gap between the two
>     rankings, not harm to the rest. In the domination model the blocked
>     party's own count also narrows, which is stated.
>   - **Log lushness where counts are added** (8.2). The identity is in bits;
>     in lushness it is a product. "Lushness" stays the ordinary term where
>     only order matters (Sol's third message).
>   - **Independence is sufficient, not necessary** for an unchanged region
>     to cancel (8.7).
>   - **A perfect copy adds no independent branching** replaces "a record
>     adds nothing" (8.8), after chapter 7's physical records.
>   - **TL;DR:** the second, fourth and fifth bullets made precise (the
>     lower bound also uses an earlier state of the world).
> - Appendix A carries the same two phrasings in remarks: Proposition A.7.6
>   ("That term is the cost the dominator places on everything else") and
>   Proposition A.7.10 ("Independence is needed"). Both are corrected in
>   Appendix A r19.

> **Drafting note (r2, 23 October).**
> - TL;DR trimmed (originator: "bloated"): a two-sentence headline and five
>   one-line takeaways. "Any part can be measured the same way" folded into
>   the headline. Body unchanged.

> **Drafting note (r1, 23 October).**
> - First draft, following outline r21 (chapter 8), in the form of rulings
>   63–69 and 72: a headline and takeaways with no toy results, claims stated
>   as strongly as they can be defended, qualifications argued in the body.
>   No mention of Alpha (rulings 77 and 78): nothing in the chapter needs it.
> - **Sources:** outline r21; Overview r19, section 2 ("Whose futures
>   count", "The comparison that singles out no one"); Appendix A r18,
>   section A.7 (Definition A.7.1 to Proposition A.7.7, and Proposition
>   A.7.10); chapter 2's four stall points, of which this chapter takes the
>   subject.
> - **Scope kept to measurement.** The chapter says how the measure applies
>   to a part and how a part's count relates to the whole's. Which parts are
>   valuers is chapter 9; why ethical judgement would follow the whole
>   (Definition A.7.8, Corollary A.7.9) and the infinite exterior
>   (Proposition A.7.11) are chapter 10. The chapter points to both and
>   argues neither.
> - **One Overview sentence not carried over.** Overview section 2 says
>   that the more the futures of a self and its world are intertwined, the
>   more often prudence and ethics agree. No numbered result states it.
>   Section 8.6 gives the exact condition for agreement and leaves the claim
>   about frequency to chapter 10. Added to the held r20 list for a decision.
> - **Examples 8.1–8.4** are exact enumerations of all histories in small,
>   fully specified models. Script: `analysis/ch8/ch8_numbers.py`. The
>   domination numbers in 8.6 are Appendix A's V21 (chapter 21's model); the
>   own-present numbers in 8.1 are V11b.
> - The drafting notes are working provenance. They are removed at
>   compilation and kept in the revision record (Appendix H).

> **TL;DR**
>
> One measure counts the futures of the whole world and of any part of it.
> A part and the whole differ by exactly one term.
>
> - **No part has more lushness than the whole.** Branching the parts share
>   is counted once.
> - **The term is how far the rest of the world can still vary, given the
>   part's history.** Part and whole agree unless it points the other way and
>   outweighs the part's own change.
> - **So what is best for a part can be worse for the whole.** This is where
>   self-interest and the whole come apart.
> - **Untouched, independent parts drop out.** Dependence can make an
>   untouched part count. No list of subjects is needed.
> - **A part's ranking can be bounded with a few steps of the past.** Bounds
>   that overlap mean unresolved, not tied.

Chapter 2 named four points at which earlier attempts to build on
possibility stalled. One was the subject: whose possibilities are being
compared. [Overview section 2](#overview-2) gave the program's answer, that
the comparison which singles out no one is made for the whole field, and
that a part and the whole differ by one term. This chapter builds the
measurement that answer rests on. It shows how lushness applies to a part
(8.1), how the parts' counts add up to the whole's (8.2–8.3), how a part's
count can be bracketed when it cannot be computed exactly (8.4), how a part
and the whole can disagree and by how much (8.5–8.6), and why parts an act
cannot touch can be left out (8.7). Which parts are valuers is
[chapter 9](#chapter-9)'s question. Why ethical judgement would follow the
whole and not the part is [chapter 10](#chapter-10)'s. The results are
definitions and theorems of [Appendix A](#appendix-a), section A.7.

---

## 8.1 Following a part

**Lushness applies to any part of the world without change: follow the
part's history, and count its futures.**

The futures counted so far have been futures of a whole system: every state
it can be in, read at a declared resolution (chapters 4 and 7). A part of
the system is picked out by a map that takes each state of the whole to a
state of the part: the position of one molecule in a gas, the setting of one
switch in a circuit, the state of one cell in a tissue. As the whole moves
through its history, the part moves through a history of its own, and that
history has a law, fixed by the law of the whole. Its lushness is the
entropy of that law, two to the power of which is the effective number of
the part's distinct futures, exactly as for the whole
([Definition A.7.1](#a-7-1)).

> **Plain-English definition 8.1: Part, and the lushness of a part**
>
> A part is what a map from states of the world to states of a piece of it
> picks out. The lushness of a part is the lushness of its own history:
> the effective number of different ways that history can go, from the
> present of the world.

The whole is a part too: the part picked out by the map that changes
nothing. Parts can overlap, and one can sit inside another, since a map can
take any piece of the state. In what follows the **subject** is whichever
part a comparison follows. [Chapter 9](#chapter-9) says which parts are
valuers. Every result in this chapter holds for any part, so nothing here
waits on that answer.

**The present has to be declared.** A part's futures are counted from the
present of the whole world, because that present is what fixes how the part
can go on. A part can also be assessed from its own present alone, and the
two counts are different quantities. Averaged over all the presents of the
world that agree with the part's own, the count from the part's own present
is never smaller, since knowing less about where things start cannot narrow
what can follow. For one particular present of the world, it can be larger
or smaller. In a small test model, a part's count from its own present is
3.50 bits, against 2.58, 3.62 and 3.34 bits from the three presents of the
world that agree with it. A comparison says which of the two it uses. The
program's default is the present of the whole, and every result below uses
it.

> **In Omega**
>
> A part's futures are Omega read through a map. Two branches that differ
> only outside the part look the same to it, and the part's count merges
> them. Nothing is added to Omega and nothing is taken away; the part sees
> less of it.

---

## 8.2 The whole and its parts

**The log lushness of the whole is the log lushness of its parts, less
what their futures share. No part has more lushness than the whole.**

Split the state of the world into a part D and the rest, E. Each has a
history, and the whole history is the pair. The count of the whole is tied
to the counts of the two by an identity
([Proposition A.7.2](#a-7-2)):

> \[
> \ell^{\text{whole}}_n=\ell^D_n+\ell^E_n-I_n(D;E)\ \ge\ \max\bigl(\ell^D_n,\ell^E_n\bigr).
> \]
>
> *In words:* in bits, the log lushness of the whole is that of the part
> plus that of the rest, less what their histories share; and since a part's
> history is a summary of the whole's, no part has more lushness than the
> whole.

In lushness itself, the effective number of futures, the identity is a
product: the whole's number is the part's times the rest's, divided by two
to the power of what they share.

The term subtracted is the mutual information between the two histories,
given the present. It is zero when the part and the rest go their own ways,
and it is as large as the smaller of the two counts when either history
fixes the other.

> **Primer: mutual information**
>
> The mutual information between two random quantities is the amount by
> which knowing one reduces the uncertainty of the other, measured in bits.
> It is symmetric: D tells as much about E as E tells about D. It is zero
> exactly when the two are independent, and it is never larger than the
> entropy of either. The entropy of the pair is the sum of the two entropies
> less the mutual information, which is the identity above applied to
> histories (Cover and Thomas 2006, chapter 2).

> **Plain-English definition 8.2: Intertwining**
>
> How far the futures of a part and of the rest of the world go together:
> the mutual information between their histories, given the present. Fully
> intertwined futures move as one; untwined futures are independent.

**Example 8.1: a relay and a lamp.** A relay is open or closed at each step,
each with probability one half, independently of the steps before. A lamp
sits beside it. The present is relay open, lamp off. Two arrangements:
- **Wired.** The lamp is on exactly when the relay is closed.
- **Unwired.** The lamp is on or off at each step with probability one
  half, independently of the relay and of its own past.

| Over 8 steps | Relay | Lamp | Shared | Whole |
|---|---|---|---|---|
| Wired | 8 bits | 8 bits | 8 bits | 8 bits |
| Unwired | 8 bits | 8 bits | 0 bits | 16 bits |

The relay and the lamp have the same counts in both arrangements. What
differs is how far their futures are intertwined. Wired, the lamp's
history repeats the relay's, the two share everything, and the whole has
no more futures than either part. Unwired, they share nothing, and the
whole has as many futures as the two together. The parts' own counts do
not decide the whole's; the joint law does.

**Nested and overlapping parts need no rule.** A family and its members, a
tissue and its cells, an institution and the people in it all overlap. If
each part's count were added up, what they share would be counted more than
once. The identity shows why the whole's count never does this: it is
computed from the joint law of all the parts, and the joint law already
contains what they share. There is nothing to apportion, and nothing to
correct for afterwards.

---

## 8.3 A part that loses nothing

**A part has as much lushness as the whole only if following it loses no
distinction between the whole's futures. Such a part is, for the measure,
the whole.**

Following a part merges any two histories of the world that differ only
outside it. The part's count falls short of the whole's by exactly the
uncertainty of the whole history given the part's history. The shortfall is
zero exactly when no two possible histories of the world give the part the
same history ([Proposition A.7.7](#a-7-7)):

> \[
> \ell^D_n(x)\le\ell^{\text{whole}}_n(x),
> \]
>
> with equality if and only if the part's history fixes the whole history
> on every history that can occur.
>
> *In words:* a part has the whole's lushness only when everything the rest
> of the world can do shows up in the part.

In the wired arrangement of Example 8.1, the relay is such a part. The lamp
does whatever the relay does, so following the relay alone loses nothing,
and the relay's 8 bits are the whole's 8 bits. Unwired, the relay misses the
lamp's own variation, and its 8 bits fall short of the whole's 16.

A part that loses nothing under every option being compared ranks those
options exactly as the whole does. That agreement is guaranteed by
construction. Any other part leaves something out, its agreement with the
whole has to be checked, and the next three sections say what follows.

---

## 8.4 Bracketing a part's lushness

**A part's count can be pinned between two bounds that use only a few steps
of the past, and the bounds close in from both sides as more of the past is
used.**

The history of the whole is Markov: given the present, the past adds
nothing about what follows (chapter 3). The history of a part is in general
not. What the rest of the world is doing, which the part does not show,
carries information from one step to the next, so the part's own past can
keep telling something about its future. That is why a part's count can be
harder to compute than the whole's, which needs only the step-by-step law.
It can still be bracketed ([Theorem A.7.3](#a-7-3)). Write c_t for the new
branching the part adds at step t + 1, given everything it has done so far.
For any number k of steps looked back,

> \[
> H\bigl(D_{t+1}\mid D_{t-k+1},\dots,D_t,\,X_{t-k}\bigr)\ \le\ c_t\ \le\
> H\bigl(D_{t+1}\mid D_{t-k+1},\dots,D_t\bigr),
> \qquad \ell^D_n=\sum_{t<n}c_t .
> \]
>
> *In words:* the part's new branching at each step lies between two
> numbers. The upper one uses only the part's own last k states. The lower
> one adds the full state of the world k steps back. The part's lushness is
> the sum of its branching over the horizon, and looking further back
> narrows the bracket from both sides.

The upper bound forgets the part's older past, and forgetting can only make
the next step look less certain. The lower bound supplies the full state of
the world at one earlier step, and since the world is Markov, nothing
before that step matters; knowing more can only make the next step look
more certain. Both bounds become exact when k reaches back to the present.
These are the standard bounds for functions of Markov chains (Cover and
Thomas 2006, section 4.5), here at a finite horizon from a given present.

> **Plain-English definition 8.3: Resolved and unresolved for a part**
>
> Two options are resolved for a part, at a given depth of looking back, if
> their brackets, summed over the horizon, do not overlap. Otherwise the
> part's ranking is unresolved at that depth. Unresolved is a report about
> the bounds, not a tie.

**Example 8.2: a thermometer in a heated room.** A heater is on or off. At
each step it keeps its state with probability 1 − q and switches with
probability q. At each step, given the heater's state at that step, the
room reads warm with probability 0.9 when the heater is on and 0.1 when it
is off. The part followed is the thermometer, which shows
only warm or cold; the heater is part of the rest. The present is heater on,
room warm. Two options set how often the heater switches: q = 0.05 and
q = 0.1.

| Over 8 steps | q = 0.05 | q = 0.1 | Ranking |
|---|---|---|---|
| Looking back 0 steps | 4.67 to 6.29 bits | 5.44 to 7.16 bits | unresolved |
| Looking back 1 step | 5.10 to 5.47 bits | 5.94 to 6.18 bits | resolved |
| Looking back 2 steps | 5.20 to 5.28 bits | 6.01 to 6.05 bits | resolved |
| Exact | 5.23 bits | 6.03 bits | |

With no look-back, the brackets overlap and the thermometer's ranking is
unresolved. One step back separates them, and the heater that switches more
often gives the thermometer more futures. In a model this small the exact
counts can be computed directly; the bounds matter where they cannot, and
the depth needed to resolve a ranking is then reported with it.

The bounds are wide when the part's own states reveal little about the
rest of the world. In models where the part sees little of what drives it,
its rankings are often unresolved at the depths that can be computed
([chapter 21](#chapter-21) reports such cases). The whole's count has no such
gap: its step-by-step law is what the model specifies.

---

## 8.5 Subjects can disagree

**What is best for a part's own futures can be worse for the futures of the
whole.**

The identity of section 8.2 does not make the part's ranking follow the
whole's. A part can gain while the whole loses ([Proposition A.7.5](#a-7-5)).

**Example 8.3: one supply, three machines.** A single power supply can run
either the subject's machine or two machines elsewhere, not both. A running
machine takes one of two settings at random at each step, each with
probability one half; an idle machine holds its setting. The present is
every machine at its first setting.

| Over 8 steps | Subject's machine | Whole |
|---|---|---|
| Power to the subject's machine | 8 bits | 8 bits |
| Power to the other two | 0 bits | 16 bits |

The subject's own count prefers the first option by 8 bits. The whole's
prefers the second by 8 bits. Neither count is mistaken: they measure
different things, and here they point in opposite directions.

The example has no intertwining at all, but intertwining does not remove
the possibility. [Chapter 21](#chapter-21) reports a model of a dominating
subsystem in a coupled world, where the dominator's futures widen while the
futures of what it governs, and of the whole, narrow. Which of the two
rankings ethical judgement tracks is not a question about the measure, and
[chapter 10](#chapter-10) takes it up.

---

## 8.6 The self–whole gap

**A part and the whole rank options by the same measure, and they differ by
exactly one term: what an option does to the futures of the rest of the
world, given what it does to the part.**

The chain rule splits the whole's count into the part's count and the count
of the rest given the part's history. Under each option, the two add up to
the whole. Subtracting one option from the other gives the gap between the
part's verdict and the whole's ([Proposition A.7.6](#a-7-6)):

> \[
> \Delta\ell^{\text{whole}}_n=\Delta\ell^D_n+\Delta\ell^{E\mid D}_n .
> \]
>
> *In words:* the change in the whole's lushness between two options is the
> change in the part's lushness plus the change in the lushness of the rest
> of the world, given what the part does.

> **Plain-English definition 8.4: The rest given the part**
>
> The lushness of everything outside a part, counted once the part's own
> history is known: the futures the rest of the world can still take that
> the part's history does not already fix.

**The condition for agreement.** The part and the whole rank two options the
same way unless the second term points the other way and is larger in size
than the first. When the second term is small, or points the same way, the
part's interest and the whole's coincide. When it points the other way and
outweighs the part's own change, they part, and the second term sets the
size of the gap.

**What the second term measures.** It is the rest's branching given the
part's history, and it can change in two ways: because the rest branches
more or less, or because the rest's history becomes more or less tied to the
part's. Example 8.4 (section 8.7) shows the second alone. When a recorder
copies the weather instead of tossing its own coin, the weather's own count
stays at 8 bits and the recorder's stays at 8, while the rest given the
recorder falls from 8 bits to 0. Nothing in the weather's own futures
narrowed. So the term fixes the sign and size of the gap between the part's
ranking and the whole's, but on its own it does not measure harm to the
rest.

In Example 8.3, giving the power to the subject's machine changes the whole
by −8 bits. The part gains 8 bits. The rest, given the part, loses 16 bits.
Here the change is in the rest's own branching: the first option fixes the
two other machines' futures. The identity
holds exactly: −8 = 8 − 16.

**A model case.** In the domination model of [chapter 21](#chapter-21)
([model C.14](#c-domination)), one party can block another's access to a
shared resource, paying from an energy bank of its own. At the model's
reference horizon and cadence, blocking changes the whole by −13.637 bits.
The blocker's own count changes by between +4.849 and +14.059 bits; it is
bracketed, not computed exactly, by the bounds of section 8.4. The identity
carries the bracket over: the rest of the world, given the blocker, changes
by between −27.696 and −18.486 bits. The blocker's gain is real, and the
second term is larger and points the other way. The blocked party's own
count narrows as well, by between 14.176 and 25.778 bits, so in this model
the term reflects lost branching, not only a change in what the parties
share.

**The gap can be computed with the part's bounds.** The part's count is
conditional on the present of the whole, so the bounds of section 8.4 apply
to it, and the identity transfers them to the gap. A gap that the bounds
leave straddling zero is reported as unresolved.

---

## 8.7 Unaffected parts cancel

**A part of the world whose futures no option changes, and whose futures
are independent of those the options do change, adds the same to every
option and drops out of the comparison.**

A comparison of options for the whole does not have to survey the whole.
Split the world into a region R that the options affect and a region U
whose history has the same law under every option. If U's history is
independent of R's under both options, the whole's law under each option is
the product of R's law and U's, and U's count is the same in both
([Proposition A.7.10](#a-7-10)):

> \[
> \Delta\ell^{\text{whole}}_n=H(Q_a)-H(Q_b),
> \]
>
> where Q_a and Q_b are the laws of R's histories under the two options.
>
> *In words:* the difference between two options, for the whole, is the
> difference for the region they affect, as long as the rest is unchanged
> and independent of that region.

**Independence is what the result uses.** It is sufficient, not necessary:
a region tied to the one the options change still cancels if what the two
share comes out the same under both options. But a region the options leave
unchanged can also move the difference, through the mutual information of
section 8.2, and then it does not drop out.

**Example 8.4: a recorder and the weather.** The weather is rain or dry at
each step with probability one half, independently of earlier steps, and no
option changes it. A recorder beside it can be set three ways: to record the
weather, to toss its own fair coin at each step, or to hold still. The
present is dry, and the recorder at its first state.

| Over 8 steps | Recorder | Weather | Shared | Whole |
|---|---|---|---|---|
| Records the weather | 8 bits | 8 bits | 8 bits | 8 bits |
| Tosses its own coin | 8 bits | 8 bits | 0 bits | 16 bits |
| Holds still | 0 bits | 8 bits | 0 bits | 8 bits |

Comparing the coin with holding still, the weather is independent of the
recorder under both, and it drops out: the whole's difference, 8 bits, is
the recorder's difference. Comparing the coin with recording, the weather is
just as unchanged, and the recorder's own count is 8 bits in both. Yet the
whole differs by 8 bits, because under recording the recorder's history
repeats the weather's and adds nothing to it. The unchanged region did not
drop out, because under one option it was not independent of the region the
option changed.

**Causal reach.** A region outside the causal future of a decision cannot
have its law changed by any option. It drops out if, in addition, its
futures are independent of those of the regions the options do reach.
Within reach, the test is what the options change, not what the actor
depends on: a region the actor does not rely on still counts whenever the
options affect it.

**No list of subjects.** Together with section 8.2, this is why no list of
subjects has to be drawn up, weighed or kept. Overlaps are handled by the
joint law; regions outside reach and independent of what is reached cancel;
everything else is in the count already.

---

## 8.8 What the chapter gives the rest of the manuscript

- **Valuers.** The measure applies to any part, so the question of which
  parts are valuers is a question about frames, not about the measure
  ([chapter 9](#chapter-9)).
- **The comparison that singles out no one.** The self–whole gap and the
  absence of a list of subjects are the measurement side of
  [chapter 10](#chapter-10)'s argument that a comparison which names no part
  measures the whole field. Chapter 10 also takes up an unchanged exterior
  that is infinite.
- **The test bed.** Rankings for a part are reported with their bounds and
  the depth that resolves them, or as unresolved ([chapter 12](#chapter-12)).
- **Domination.** The model of a subsystem that gains while the whole loses
  is tested in [chapter 21](#chapter-21).
- **Information.** A perfect copy adds no independent branching
  (Example 8.4). What recording does afterwards belongs to the physical law
  that follows it; what a register adds, and when it pays, is
  [chapter 14](#chapter-14)'s.
- **The program ahead.** What makes a part a physically instantiated frame
  is open ([chapter 33](#chapter-33)).

---

## 8.9 What this chapter does not claim

- **That a part's count is irrelevant.** It is the same measure, applied to
  the part, and it ranks options by what they do to the part's futures.
- **That a part and the whole always disagree.** They agree unless the
  rest-given-the-part term points the other way and outweighs the part's own
  change. How often that happens is not settled here.
- **That the whole must be surveyed.** Regions outside reach, and
  independent of what is reached, cancel.
- **That everything an act cannot change drops out.** A region the options
  leave unchanged still counts if its futures are intertwined with those the
  options change.
- **That which ranking ethical judgement tracks follows from the measure.**
  The measure gives both rankings and the exact gap between them. Which one
  ethics follows is part of the central thesis ([chapter 10](#chapter-10)).
- **That which parts are valuers is settled.** Every result here holds for
  any part; the criterion for a physically instantiated frame is open.

---

## Status of chapter 8

| Status | Claims |
|---|---|
| **D** (definitions) | a part, the lushness of a part, and the declared present ([Definition A.7.1](#a-7-1)) (8.1); intertwining (8.2); resolved and unresolved for a part ([Definition A.7.4](#a-7-4)) (8.4); the rest given the part (8.6) |
| **T** (results, under their stated assumptions) | the whole and its parts ([Proposition A.7.2](#a-7-2), proved here) (8.2); a part that loses nothing ([Proposition A.7.7](#a-7-7), established elsewhere) (8.3); bounds on a part's lushness ([Theorem A.7.3](#a-7-3), established elsewhere) (8.4); subjects can disagree ([Proposition A.7.5](#a-7-5), proved here) (8.5); the self–whole gap ([Proposition A.7.6](#a-7-6), proved here) (8.6); unaffected parts cancel ([Proposition A.7.10](#a-7-10), proved here) (8.7) |
| **M** | the domination model's whole-field change and the blocker's bracket ([model C.14](#c-domination); Appendix A's verification V21) (8.6); the own-present comparison, V11b (8.1); Examples 8.1–8.4 are exact computations in specified finite models |
| **E** | none |
| **N** | none |
| **C** | none |
| **Open** | what makes a part a physically instantiated frame (8.1); how often a part's ranking and the whole's agree (8.6) |

## References cited in chapter 8

*Collected with full details in Appendix G.* Entries marked "to verify" are
not yet checked against their sources.

- Cover, T. M., and Thomas, J. A. (2006). *Elements of Information Theory.*
  2nd edition. Hoboken: Wiley. To verify.
