# 4. Counting futures

> **Drafting note (r7, 23 October).**
> - Ruling 79: section 4.2's pointer to chapter 7 states matched resolution
>   and that the finer level governs once shown faithful.

> **Drafting note (r6, 23 October).**
> - Timing, after chapter 7 r2 and Appendix A r17 (ruling 76): what counts
>   is the timing information a system's records can register; a sharp floor
>   on cadence is one possible result, not an assumption, and a reading made
>   by a physical recorder is part of the development, not a finer
>   description of it. Section 4.2 and the status table's open item
>   are reworded; nothing else changes.

> **Drafting note (r5, 22 October).**
> - **Sol's review of r4**, applied.
>   - **Restructured** into the sequence Sol identified: what can be
>     distinguished (4.2, merging resolution and the continuation
>     structure), how much it amounts to (4.3), how breadth is generated
>     (4.4, merging the step and branch forms with randomness, control
>     invariance and accessible possibility), how it accumulates (4.5), and
>     what the number leaves out (4.6). Sections 4.7 and 4.8 are the old
>     4.11 and 4.12, shortened. The naming section becomes a Note in 4.3.
>     Cautions are consolidated in 4.6, and the other sections point there.
>   - **The composition rule.** The physical probabilities are fixed, and
>     several summaries of them are possible; the third requirement selects
>     one because of what an effective breadth is meant to be. The claim that
>     power weighting treats branches as more or less likely than they are is
>     withdrawn.
>   - **Similarity** (4.3): kept out of the count, but relations between
>     histories are physical, stay in Omega, and can be unseen by the count;
>     they join the list in 4.6.
>   - **Resolution** (4.2): the measure is established at a declared
>     resolution. Which faithful level governs, including levels neither of
>     which refines the other, and the floor on cadence, are chapter 7's.
> - TL;DR: "the resolution that governs" becomes "which distinctions count".
> - Definitions 4.1–4.5 keep their numbers. Earlier drafting notes cite
>   the r1–r4 section numbers.

> **Drafting note (r4, 22 October).**
> - The TL;DR becomes a two-sentence headline (ruling 65) and six
>   takeaways, after Sol's proposal: each bullet a
>   conclusion, no reasons. Changes to Sol's text: "not itself value" added
>   to the first bullet (ruling 56); the horizon dropped from "physics
>   determines what counts", since the verdict concerns everything that
>   follows; "physically resolved" replaced, because "resolved" keeps the
>   meaning of Definition A.7.4; "remains open" replaced by the central
>   thesis. The pointer to the Overview moves from the TL;DR to the opening
>   paragraph. The body is otherwise unchanged.

> **Drafting note (r3, 22 October).**
> - The TL;DR is tightened (ruling 64): the result first, then four
>   consequences. The body is unchanged.

> **Drafting note (r2, 21 October).**
> - **The TL;DR states the point and its consequences** (ruling 63), and the
>   body develops them.
> - **Astra's review of r1**, applied:
>   - **The composition rule is stated before the theorem** (4.4): divide the
>     future at any stage, and log lushness is the log lushness of the
>     branches plus the probability-weighted average of the log lushness
>     within them. It is named as the requirement that selects the measure,
>     with its reasons. Other composition rules are coherent; Rényi entropy
>     composes with escort weights and a power mean, and fails only the
>     probability-weighted rule. The decision-recursion reason is narrowed to
>     what Theorem A.13.1 uses.
>   - **The physical continuation structure and what the count takes from
>     it** are distinguished (4.3). The count of one horizon sees the
>     weighted set of histories; prefixes, timing and which part varies stay
>     in Omega.
>   - **Cadence** (4.2, 4.11): timing no record can register does not count,
>     so no process wins merely by being read more often; whether busy
>     processes outrank enabling structure at the cadence that governs is
>     tested in chapter 16. Deriving the floor for a given model is open.
>   - **Finite scope** of the theorem stated (4.3).
>   - **Signs are computed, not assumed:** consumption changes the residual
>     state (4.5); a possibility adds at every probability when what follows
>     its taking has at least as much lushness over the horizon (4.8, by the
>     concavity of entropy); continuity is not what makes a new-support gain
>     positive (4.8); slope and level decide where they exist (4.6).
>   - **"Carried" replaced** (4.10): timing and access enter through the
>     history law; the number need not distinguish every physical difference.
>   - Smaller: an exact tie (½, ⅛, ⅛, ⅛, ⅛ against four equal futures); the
>     similarity measures reduce to the Hill numbers; language-model
>     perplexity is per token, from cross-entropy; the gas note no longer
>     says futures narrow with the horizon.
> - **Knock-on items, not yet made:** the reason given for condition 3 in
>   Theorem A.2.3, the "higher rate" sentence in the scope of Proposition
>   A.2.7, the word "same" in Definition A.1.1, and "carried" in section
>   32.8 of chapter 32 need the same corrections.

> **Drafting note (r1, 21 October).**
> - First draft, following outline r17 (chapter 4) and the concept ladder
>   (resolution, continuation structure, lushness). Chapter 7 keeps faithful
>   distinctions, the level that governs and certified rankings; this chapter
>   says only that physics decides and points there. Chapter 5 defines the
>   profile; this chapter uses the word once, with a pointer.
> - **Sources:** outline r17; Overview r19, section 3 (its wording on
>   resolution predates rulings 51 and 52, so "admissible" and "accept only
>   robust verdicts" are not carried over); v4 chapter 4 (r6), whose "adopted
>   class" framing is superseded by the derivation in Appendix A r15, section
>   A.2; Appendix A r15, sections A.1, A.1.1–A.1.2 and A.2.1–A.2.7.
> - Calibration numbers (sections 4.1 and 4.4) give lushness itself, with log
>   lushness in bits beside it, because calibration is what they show. Every
>   other number is log lushness in bits.
> - Script: `analysis/ch4/ch4_numbers.py` computes every number in the
>   chapter not already in Appendix A.
> - Lushness is said not to be value, and the reasons the count bears on value
>   are left to Part III (ruling 56; Overview sections 2, 4 and 5).
> - The drafting notes are working provenance. They are removed at
>   compilation and kept in the revision record (Appendix H).

> **TL;DR**
>
> How much can follow from a present has exactly one measure. The program
> calls it lushness, and physics supplies everything it counts.
>
> - **Lushness measures future breadth.** It is the effective number of
>   physically distinguishable continuation histories from a present. It is
>   not itself value; Part III argues why it bears on value.
> - **The measure is uniquely determined.** Four counting requirements select
>   Shannon perplexity: L = 2^H(P).
> - **Physics determines what counts.** The histories, their probabilities
>   and which distinctions count come from physics, not from preference.
> - **Access is already included.** Organization, resources, control and
>   repair shape the continuation law. No additional weight is needed.
> - **Randomness counts too.** Every continuation physics can distinguish
>   contributes, noise included. Possibilities no route can reach do not.
> - **Lushness is not all of Omega.** Different continuation structures can
>   have equal lushness. Whether ethics needs what that leaves out is part of
>   the central thesis.

Chapter 3 built Omega and showed that, once the law is fixed, what can follow
from a present is fixed by the present. This chapter measures how much
follows, and develops [Overview section 3](#overview-3). It takes five steps:
what can be distinguished (section 4.2), how much it amounts to (4.3), how
that breadth is generated (4.4), how it accumulates over time (4.5), and
what the number leaves out (4.6). The measure is established at a declared
resolution; which resolution governs is the subject of
[chapter 7](#chapter-7). The chapter makes no ethical claim. Lushness
measures how much can follow from a present, and why that bears on value is
argued in Part III, from value requires valuers.

---

## 4.1 Two problems before any count

**To count futures, we must first say which futures are different, and how
much an unlikely one counts. Every attempt to count possibility has stumbled
on one or both.**

The first problem is grain. A count depends on which differences it attends
to. Economists who rank freedom by counting options must decide whether two
nearly identical options are one option or two, and the decision settles the
verdict. The entropy of a gas depends on which microscopic differences are
counted; Gibbs's paradox about mixing gases made that dependence famous
(Jaynes 1992). Measures of how many options an artificial agent has depend on
how the states of its world are represented. Time raises the same problem
again: how often a process is read changes the count, and a process read
often enough shows a new branch at every small event.

The second problem is weighting. With sameness settled, the natural next step
is to count the distinct futures. That is how freedom of choice has been
ranked: Pattanaik and Xu (1990) showed that three plausible axioms force a
ranking by the number of options. For futures, counting fails. Take a present
with a million distinct futures, one with probability 99.9 per cent and the
rest sharing the remaining 0.1 per cent equally. A count says a million. The
measure this chapter derives says 1.02, or 0.031 bits: in effect, one future.
Physics says not only which futures are possible but how likely each is, and
a count that ignores the likelihoods discards that.

Section 4.2 answers the first problem in principle. Section 4.3 answers the
second in full.

---

## 4.2 What can be distinguished

**Every count of futures is made at a declared resolution. At that
resolution, what follows from a present is a set of histories with their
probabilities, and a count of futures responds to those alone.**

### Resolution

A future is a history: a sequence of states passed through (chapter 3). To
say when two histories are the same, a comparison declares two things.
- **The grain.** Which states count as different. A gas described by its
  pressure and temperature has few states; described molecule by molecule, it
  has an astronomical number.
- **The cadence.** How often the development is read. A history read once a
  second and the same history read once a nanosecond are different sequences.

> **Plain-English definition 4.1: Resolution**
>
> The level of detail at which futures are counted: its grain, meaning which
> states count as different, and its cadence, meaning how often the
> development is read.

Formally, a resolution is a pair: a cadence, and a map from the states of a
finer description onto the states counted ([Definition A.6.1](#a-6-1)).

Choosing a level of detail and saying nothing about it, or choosing the level
that gives the wanted answer, lets the choice decide the verdict. The
program's rule is that physics decides which distinctions count. A
distinction between states, or between the times at which changes occur,
counts only if physics can register it: if a physical record of it can form,
or if it changes the law of later records. Relabelling histories, splitting
one history into duplicates, or inserting checkpoints that change nothing
draws no distinction at all. The same rule applies to time: a timing
distinction that no record can register does not count, so no process wins
merely by being read more often.

That rule says which distinctions count. Which of several faithful levels of
detail governs a comparison is a second problem. Options are compared at
one level. Of two levels, one refining the other, the finer governs once its
extra detail is shown to be faithful, and a ranking at the coarser level is
checked against it ([Definition A.6.5](#a-6-5); [Proposition A.6.6](#a-6-6)). Levels
that keep different information, neither refining the other, need a
further step, and how finely a system's records can register timing has
still to be derived for any given model. [Chapter 7](#chapter-7) takes up both. This chapter establishes
the measure at a declared resolution.

> **Note: lushness is not the entropy of heat**
>
> Thermodynamic entropy counts the microscopic arrangements consistent with a
> system's state at one moment. Lushness counts the futures a present
> supports over time, at a declared resolution, weighted by their
> probabilities. They are different quantities and need not move together. A
> gas at equilibrium has the largest thermodynamic entropy its constraints
> allow. Described by its pressure and temperature, it has essentially one
> future; described molecule by molecule, it has an astronomical number.

### The continuation structure

Fix a present, a resolution and a horizon. The histories that can follow, read
at that resolution, form a set, and the law gives each a probability.

> **Plain-English definition 4.2: Continuation structure**
>
> The histories that can follow from a present, read at a declared resolution
> up to a horizon, together with their probabilities. Histories with no
> chance of occurring are not part of it.

Each history is a sequence, so the continuation structure keeps which
histories share a beginning, where they branch, and which parts of the world
vary along the way. A count of how many futures follow needs less. Two
continuation structures whose histories can be matched one to one, each pair
with the same probability, give the same count, whatever the histories are
called and however they branch along the way
([Definition A.1.1](#a-1-1)). So, for any count of futures, names do not
matter, and adding a history that cannot happen changes nothing
([Proposition A.1.2](#a-1-2)). The rest of the structure stays in Omega,
where other quantities read it (section 4.6).

**Finite scope.** The theorem of section 4.3 concerns finite continuation
structures: finitely many histories, each with a positive probability. In
continuous time, or with continuous outcomes, a single exact history can have
probability zero without being impossible. Such cases enter as limits of
finite resolutions ([Theorem A.6.3](#a-6-3); [chapter 7](#chapter-7)).

**Quantum frames.** The same construction applies to a frame's records. A
frame's couplings fix what it records, and quantum theory gives the
probabilities of the recorded histories
([Proposition A.14.3](#a-14-3)). They form a continuation structure like any
other, and everything in this chapter applies to them unchanged
([chapter 29](#chapter-29)).

> **In Omega**
>
> A resolution fixes which futures in Omega count as the same; it changes how
> finely Omega is read, not Omega itself. The continuation structure is the
> part of Omega that unfolds from one present, read at one resolution, up to
> one horizon.

---

## 4.3 How much it amounts to

**The measure is derived. Four requirements leave exactly one count of
distinct futures: their perplexity. The requirement that selects it is the
rule for composing stages.**

We want a number that says how many futures a continuation structure amounts
to. Any such number should meet four requirements.
1. **It depends only on the futures and their probabilities.** Renaming
   futures changes nothing, and futures that cannot happen do not count.
2. **It responds continuously to the probabilities.** A small change in how
   likely the futures are makes only a small change in the count.
3. **It composes by stages, each later stage weighted by the probability of
   reaching it.** Divide the future at any stage. The logarithm of the count
   of the whole equals the logarithm of the count of the branches at that
   stage, plus the average of the logarithms of the counts within the
   branches, each weighted by the probability of reaching it.
4. **It counts plainly.** A number of equally likely futures counts as that
   number.

> \[
> \log_2 L(\text{whole})=\log_2 L(\text{branches})+\sum_i q_i\log_2 L(\text{within branch } i) .
> \]
>
> *In words:* the log count of a future divided at any stage is the log count
> of the branches at that stage, plus the log counts within the branches,
> averaged with the probability of reaching each branch as its weight.

The first and fourth requirements are definitional: the first says the count
is a count of the futures, the fourth says what an effective number of
futures means. The second is required by measurement: physical laws are known
to finite precision, and a count that jumped under arbitrarily small changes
in the probabilities would let differences no measurement can detect decide
verdicts.

The third is where the commitment lies. The physical probabilities are fixed,
and more than one mathematical summary of them is possible. The third
requirement selects one, because of what an effective breadth of futures is
meant to be.
- **Counting the whole and counting by stages must agree.** Grouping the
  histories at an intermediate stage is bookkeeping, and it should not change
  how much follows. Two equally likely branches, each followed by four
  equally likely continuations, are eight equally likely futures, whether
  counted whole or as two times four.
- **Each branch contributes in proportion to how often it is reached.** A
  branch reached half the time contributes half of its log breadth. That is
  the sense in which the count is an effective number of the futures that
  actually follow, each as likely as physics makes it.
- **It is the form that assessment one stage at a time needs.** The decision
  recursion computes the largest lushness a finite controlled model can reach
  as the branching of the next step plus the expected lushness of what
  follows, and that form rests on this rule ([Theorem A.13.1](#a-13-1)).

Given the four requirements, exactly one measure meets them
([Theorem A.2.3](#a-2-3)).

> \[
> L=2^{H(p)},\qquad H(p)=-\sum_i p_i\log_2 p_i .
> \]
>
> *In words:* any count of distinct futures that depends only on the futures
> and their probabilities, varies continuously with them, composes by stages
> with each later stage weighted by the probability of reaching it, and
> counts equally likely futures plainly, is two raised to the Shannon entropy
> of the futures' probabilities.

The theorem is Faddeev's (1956) sharpening of Shannon's characterization of
entropy (Shannon 1948; Khinchin 1957). Its premises map onto the four
requirements one for one: symmetry, continuity, grouping and normalization.
What belongs to the program is the object it is applied to, the continuation
structure of a present, and the reasons each requirement holds there.

The number 2^H already has a name: **perplexity**. It was introduced to
measure how hard a speech-recognition task is (Jelinek et al. 1977), and in
ecology it is the Hill number of order one, the effective number of species
in a community (Hill 1973; Jost 2006).

> **Plain-English definition 4.3: Perplexity**
>
> The effective number of equally likely alternatives that a set of
> probabilities amounts to. Over k equally likely alternatives it is k. When
> probability is spread unevenly, it is less.

> **Plain-English definition 4.4: Lushness**
>
> The perplexity of a present's futures: the effective number of distinct
> futures that follow from it, at a declared resolution and horizon. It
> equals the number of futures when they are equally likely, and falls
> towards one as a single future comes to dominate. Log lushness is its
> logarithm in base two, measured in bits.

Four worked numbers, from `analysis/ch4/ch4_numbers.py`:
- Four equally likely futures give a lushness of 4: log lushness 2 bits.
- The same four futures with probabilities of 97, 1, 1 and 1 per cent give
  1.18: 0.24 bits, in effect little more than one.
- Probabilities of 90, 5 and 5 per cent give 1.48: three futures, effectively
  fewer than two.
- The million futures of section 4.1 give 1.02.

Lushness and log lushness rank continuation structures identically, so the
manuscript uses "lushness" for comparisons and quotes numbers as log
lushness, in bits.

> **Primer: entropy and perplexity**
>
> The Shannon entropy of a probability law, H(p) = −Σ p_i log₂ p_i, measures
> how widely probability is spread, in bits. A fair coin has one bit; a coin
> that always lands heads has none; eight equally likely outcomes have three.
> Entropy has a chain rule: the entropy of two outcomes taken together is the
> entropy of the first plus the average entropy of the second given the first
> (Cover and Thomas 2006). That chain rule is the third requirement.
> Perplexity is two raised to the entropy: one bit is two alternatives, three
> bits are eight, and ten fair coins have perplexity 2¹⁰ = 1,024.

> **Note: other names, and one usage to avoid**
>
> Log lushness is the path entropy of the futures, conditioned on the full
> present; the entropy of future paths over a horizon is also called causal
> path entropy (Wissner-Gross and Freer 2013). Lushness is the effective
> number of distinct continuation histories (Jost 2006). In language
> modelling, perplexity is usually reported per token, from a model's
> cross-entropy on text. The counterpart here is per step, two raised to the
> rate of [chapter 5](#chapter-5), and is never called lushness: one fair
> binary choice at each of 100 steps has a per-step perplexity of 2 and a
> lushness of 2¹⁰⁰.

### Other summaries of the same probabilities

Other entropy-like measures summarize the same probabilities differently,
and they are coherent on their own terms. The Rényi entropies of order other
than one (Rényi 1961) are additive for independent systems, and each composes
by stages under its own rule, in which later stages enter through powers of
the probabilities of reaching them and a different mean. Take three futures
with probabilities ½, ¼ and ¼: a fair first choice, followed on one branch by
a second fair choice. The Rényi entropy of order two gives 1.415 bits,
whether computed whole or by its own rule. Composed as the third requirement
asks, the stages give 1 + ½ × 1 = 1.5 bits, which Shannon entropy matches
both ways. The Rényi entropies fail the third requirement, not consistency in
general.

### Why similar futures are not counted as partly the same

Some measures of diversity count two similar alternatives as partly the same,
using a matrix of similarities between them (Leinster and Cobbold 2012). A
similarity matrix is not given by the futures and their probabilities, so a
count that used it would fail the first requirement. When every pair of
distinct futures is treated as fully dissimilar, those measures reduce to the
Hill numbers, whose member of order one is perplexity.

That keeps similarity out of the count. It does not make relations between
histories unimportant. Where a similarity makes a difference to what follows,
through different recoveries, capacities or interactions, the histories and
their probabilities already differ, and the count registers the difference
as far as entropy separates it. Two developments can also share every
probability while their histories stand in very different physical
relations: one set differing by microscopic rearrangements, the other by
large-scale changes of structure. Those relations are physical, and they
remain part of Omega. The count does not separate them. Whether ethics needs
them is the question of section 4.6.

> **In Omega**
>
> Lushness is a measurement of Omega at one present: how many distinct
> futures leave it, each weighted by its probability, at a declared
> resolution and horizon.

---

## 4.4 How breadth is generated

**Lushness accrues step by step and branch by branch. Organization, access
and cost enter through the law that generates the branches. Randomness counts
like any other branching, and possibility no route can reach adds nothing.**

### Step by step

In a finite classical model, where the law is a table of step probabilities
K (chapter 3), the branching of one step from a state x is the entropy of
the next state, g(x). Log lushness over n steps is that branching, expected
at each step and summed ([Theorem A.2.1](#a-2-1)).

> \[
> \ell_n(x)=\sum_{t=0}^{n-1}(K^t g)(x),\qquad
> g(x)=-\sum_y K(x,y)\log_2 K(x,y) .
> \]
>
> *In words:* the log lushness of a horizon is the branching expected at
> each step, summed over the horizon, each step's branching taken from the
> states the development can have reached by then.

Three consequences follow ([Corollary A.2.2](#a-2-2);
[Proposition A.2.4](#a-2-4)).
- **Independent processes add.** Their log lushness adds, and their lushness
  multiplies. Coupled processes have the sum less the information their
  histories share. Coupling, correlation and shared resources enter through
  the actual joint law, not through any added term.
- **A state that cannot change adds nothing.** A development that has reached
  a state it can never leave branches no further, and keeps its weight.
- **A step cannot branch more than its repertoire.** Its branching is at most
  the logarithm of the number of states it can reach. Raising that bound
  requires reaching different states.

### Branch by branch

Read at any intermediate stage, the third requirement is the branch form.
Group the futures by how they stand at some stage. Then lushness is the
effective number of groups, times the geometric mean of the lushness within
the groups, each weighted by its probability ([Corollary A.2.6](#a-2-6)).

> \[
> L=2^{H(E)}\prod_e L_{\mid e}^{\,P(E=e)} .
> \]
>
> *In words:* the effective breadth of a future is the effective number of
> branches through any intermediate stage, times the geometric mean of the
> breadths within them, each branch continuing from where it actually stands.

A worked case. A present has two equally likely first steps. One leads to
eight equally likely continuations, the other to two. There are ten distinct
histories. The lushness is 2 × √(8 × 2) = 8, or 3 bits: one bit for the first
choice, plus the average of three bits and one bit for what follows it. The
first branch contributes more because more can follow from it, and the count
records exactly how much more.

Each branch continues from its full residual state. What a branch has spent,
recorded and changed in its surroundings goes with it, and what follows from
that state is counted as it is. Consuming a resource can narrow what follows,
or unlock reactions and construction that widen it. The sign is computed from
the law, never assumed, and no separate cost term is needed. Inserting a
stage that only groups histories already distinguished changes nothing;
distinguishing new physical events changes the histories themselves, which is
a change of resolution.

This is where organization, access and harm enter the measure. Machinery,
records, resources and couplings change the law, and through it which
branches occur, how likely each is, and how much follows from each. Nothing
multiplies or divides the count afterwards (chapter 3, section 3.8).

### Randomness counts

Lushness decides nothing in advance about which variations matter.
Construction and collapse, cooperation and competition, success and failure,
organization and noise all contribute their branches, and the random motion
of molecules is counted with the rest. What earns a future its weight is how
likely it is and what can follow from it, not what kind of variation it is.
That keeps the count free of any prior view about what matters. It also
raises the strongest objection, that a measure which counts everything must
prefer noise to structure. [Chapter 16](#chapter-16) states that objection
at full strength and tests it.

Who implements the law makes no difference to the count. Two implementations
that induce the same law on the histories have the same lushness
([Proposition A.2.5](#a-2-5)). A difference between consent and coercion, or
between distributed and concentrated control, can matter to lushness only
through a difference in the law, and that is where any difference it makes
must appear.

### Accessible and inaccessible possibility

Chapter 3 said that a transformation no route can reach opens no future, and
that an accessible one opens futures even when it is unlikely to be used. The
count makes this exact ([Proposition A.2.7](#a-2-7)). Suppose a possibility
is taken with some probability, and compare the law with it against the law
without it.
- **Inaccessible possibility adds nothing.** If the probability of taking it
  is zero, the law is unchanged, and so is the count.
- **Accessible possibility that opens otherwise impossible futures adds, once
  it is unlikely enough.** Take a present with two equally likely futures,
  and a possibility that, if taken, leads to a third. Taken with probability
  0.1, it adds 0.369 bits; with probability 0.01, 0.071 bits; with
  probability 0.001, 0.010 bits. The gain shrinks with the probability, and
  stays positive.
- **How unlikely is enough depends on where it leads.** If what follows its
  taking has at least as much lushness over the horizon as what follows when
  it is not taken, the possibility adds at every probability, because the
  entropy of a mixture is at least the weighted average of the entropies
  mixed (Cover and Thomas 2006). If what follows has less, it must be unlikely
  enough. If every future it leads to is new, and half a bit per step is lost
  after it is taken, then over 4,096 steps the probability must be below
  about 2⁻²⁰⁴⁷.
- **Possibility that only redirects among futures already possible can add or
  subtract.** A possibility that leads, when taken, to one of the two existing
  futures in the example makes their probabilities unequal, and subtracts
  0.007 bits at probability 0.1.

---

## 4.5 How it accumulates

**Lushness is measured to a horizon, a later section along the orientation.
It is cumulative, and where what follows has no end, the object is the whole
sequence of values over later horizons.**

Every count runs from a present to a horizon. In general the horizon is a
later section along the orientation; in a finite model with a declared
cadence, it is a number of steps ([section A.1](#a-1)).

> **Plain-English definition 4.5: Horizon**
>
> The later section, along the orientation, up to which the futures of a
> present are counted. In a finite model it is a number of steps.

- **Lushness is cumulative.** By the chain rule, the count to a later horizon
  contains all the branching of every earlier one.
- **A horizon is a truncation, not a discount.** Counting to a horizon weights
  everything before it fully and everything after it not at all. No future
  step is worth less for being later. The program's object is everything
  that follows, and every finite horizon is a partial view of it.
- **Where the field has no end, the sequence is the object.** The values over
  successive horizons form a sequence. [Chapter 5](#chapter-5) calls the
  difference between two such sequences the profile. Where the profile has a
  long-run slope and level, they give the verdict over everything that
  follows ([Corollary A.3.9](#a-3-9)). Where it has neither, as when the
  state space grows or the law changes, the profile itself is the object.

A short horizon can mislead. Failure modes are real branches, and a process
that can fail in many ways branches widely at first. Whether its failures
close what would otherwise follow appears only later, so a comparison that
stops before the consequences arrive can rank a collapse above maintenance.
[Chapters 5](#chapter-5) and [6](#chapter-6) work through this with exact
models.

> **In Omega**
>
> A horizon is a later section of Omega. Counting to it reads the part of
> Omega between the present and that section.

---

## 4.6 What the number leaves out

**Lushness is not one to one. Different continuation structures can have the
same lushness. Whether ethics needs anything the number leaves out is part of
the central thesis.**

Lushness compresses a continuation structure into one number, and distinct
structures can share it. Four equally likely futures have log lushness 2
bits. So do five futures, one with probability ½ and four with probability ⅛
each. The two structures tie at every horizon when built in two steps: a fair
first choice, followed either by a second fair choice on both branches, or by
a four-way fair choice on one branch and none on the other. Both have 1 bit
after one step and 2 bits after two.

What the number leaves out comes in several kinds.
- **Timing and arrangement.** When futures open, how long a structure lasts
  and how fast it is rebuilt change the counts at successive horizons
  ([chapters 5](#chapter-5) and [6](#chapter-6)). The counts need not
  distinguish every difference. One fair choice made at the first step and
  the same choice made at the last tie at the last step, with 1 bit, and
  differ before it. The example above ties at every horizon.
- **Access.** Machinery, records, resources, couplings and repair change
  which histories occur and how likely each is (section 4.4). Their effects
  can change lushness, but the number need not distinguish every physical
  difference they make. A multiplier for access would count the same effect
  twice, and would break the uniqueness of the count.
- **Relations between histories.** Histories that differ by microscopic
  rearrangements and histories that differ by large-scale changes of
  structure can carry the same probabilities (section 4.3).
- **Where the branching sits.** Two options can give the whole world the same
  count at every horizon while the branching sits in different parts of it:
  in one, one part varies and the rest is fixed; in the other, the reverse.
  Counting each part's own futures separates them ([chapter 8](#chapter-8)).

All of these are in Omega. Some are read by other quantities: the counts at
each horizon, and the counts of each part. Being in the continuation
structure is still not the same as being separated by its entropy. That is
the **compression boundary**: the line between what the count registers and
what it leaves out.

Whether ethics needs anything on the far side of it is part of the central
thesis ([chapter 11](#chapter-11)), and [chapter 32](#chapter-32) states the
cases that would show that it does. If one does, Omega is still the object,
and its reading has to change. The count itself cannot be repaired by a
weight chosen after the result, because it is the only count that meets the
four requirements.

---

## 4.7 What the count gives the rest of the manuscript

**Of chapter 2's four problems, weighting is answered and grain is answered
in principle. Subject and busyness have their place.**

- **Weighting: answered.** Probability decides how much each future counts,
  and the four requirements leave one count (section 4.3).
- **Grain: answered in principle.** Physics decides which distinctions count
  (section 4.2). [Chapter 7](#chapter-7) says which faithful level governs.
- **Subject: placed.** The count applies to the futures of any frame. How a
  part's count relates to the whole world's is [chapter 8](#chapter-8).
- **Busyness: placed.** Randomness counts, and timing no record can register
  does not, so no process wins merely by being read more often. Whether busy
  processes outrank enabling structure at the cadence that governs is tested
  in [chapter 16](#chapter-16).

[Chapter 5](#chapter-5) follows the count through time and compares options
by the whole profile of their difference. [Chapter 6](#chapter-6) asks what
lasting is worth, and what an early end costs.

---

## 4.8 What this chapter does not claim

- **That lushness is value.** Why it bears on value is argued in Part III.
- **That no other summary of the probabilities is coherent.** Others are; the
  third requirement selects among them (section 4.3).
- **That the resolution that governs is settled here.** The measure is
  established at a declared resolution; [chapter 7](#chapter-7) says which
  governs.
- **That a short horizon gives the verdict.** The verdict concerns everything
  that follows ([chapter 5](#chapter-5)).
- **That the count misses nothing.** See section 4.6.
- **That a single number can be estimated for realistic systems.** Every
  number here is computed exactly in a small model. Estimators with error
  bounds for realistic systems are open ([chapter 33](#chapter-33)).

---

## Status of chapter 4

| Status | Claims |
|---|---|
| **D** (definitions) | resolution, grain and cadence; continuation structure, and when two give the same count (4.2); perplexity; lushness and log lushness (4.3); horizon (4.5); the compression boundary (4.6) |
| **T** (results, under their stated assumptions) | what any count of futures respects ([Proposition A.1.2](#a-1-2), proved here); the unique effective count, given its four requirements ([Theorem A.2.3](#a-2-3), established elsewhere: Faddeev 1956), with the reasons for each requirement argued in 4.3; the Rényi entropies of order other than one fail the probability-weighted composition rule (4.3, with a worked case); the chain rule and its consequences ([Theorem A.2.1](#a-2-1); [Corollary A.2.2](#a-2-2), established elsewhere); the repertoire ceiling ([Proposition A.2.4](#a-2-4), established elsewhere); control invariance ([Proposition A.2.5](#a-2-5), proved here); branch volume ([Corollary A.2.6](#a-2-6), established elsewhere); accessible possibility ([Proposition A.2.7](#a-2-7), proved here); the entropy of a mixture is at least the average of the entropies mixed (4.4, cited); a frame's records have an ordinary probability law ([Proposition A.14.3](#a-14-3), established elsewhere) |
| **E** | perplexity in speech recognition and language modelling, and the Hill number of order one in ecology, as the same quantity (4.3), cited; ranking freedom by counting options (4.1), cited |
| **M** | none |
| **N** | none |
| **C** | none asserted; whether anything on the far side of the compression boundary matters ethically is part of the central thesis, referred to, not argued (4.6) |
| **Open** | which faithful level of detail governs, including levels neither of which refines the other, and how much timing information a given model's records can carry (4.2; chapter 7); estimators with error bounds for realistic systems (4.8) |

## References cited in chapter 4

*Collected with full details in Appendix G.* Entries marked "to verify" are
not yet checked against their sources.

- Cover, T. M., and Thomas, J. A. (2006). *Elements of Information Theory*
  (2nd ed.). Hoboken: Wiley. To verify.
- Faddeev, D. K. (1956). On the concept of entropy of a finite probabilistic
  scheme. *Uspekhi Matematicheskikh Nauk* 11(1), 227–231. (In Russian.) To
  verify.
- Hill, M. O. (1973). Diversity and evenness: a unifying notation and its
  consequences. *Ecology* 54(2), 427–432. To verify.
- Jaynes, E. T. (1992). The Gibbs paradox. In C. R. Smith, G. J. Erickson and
  P. O. Neudorfer (eds.), *Maximum Entropy and Bayesian Methods*, 1–21.
  Dordrecht: Kluwer. To verify.
- Jelinek, F., Mercer, R. L., Bahl, L. R., and Baker, J. K. (1977).
  Perplexity: a measure of the difficulty of speech recognition tasks.
  *Journal of the Acoustical Society of America* 62(S1), S63. To verify.
- Jost, L. (2006). Entropy and diversity. *Oikos* 113(2), 363–375. To verify.
- Khinchin, A. I. (1957). *Mathematical Foundations of Information Theory.*
  New York: Dover. To verify.
- Leinster, T., and Cobbold, C. A. (2012). Measuring diversity: the importance
  of species similarity. *Ecology* 93(3), 477–489. To verify.
- Pattanaik, P. K., and Xu, Y. (1990). On ranking opportunity sets in terms of
  freedom of choice. *Recherches Économiques de Louvain* 56(3–4), 383–390. To
  verify.
- Rényi, A. (1961). On measures of entropy and information. In *Proceedings
  of the Fourth Berkeley Symposium on Mathematical Statistics and
  Probability*, vol. 1, 547–561. Berkeley: University of California Press. To
  verify.
- Shannon, C. E. (1948). A mathematical theory of communication. *Bell System
  Technical Journal* 27, 379–423 and 623–656. To verify.
- Wissner-Gross, A. D., and Freer, C. E. (2013). Causal entropic forces.
  *Physical Review Letters* 110(16), 168702. To verify.
