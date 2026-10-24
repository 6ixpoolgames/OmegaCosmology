# 12. How the thesis is tested

> **Drafting note (r4, 18 October).**
> - Sol's second pass, folded in at the originator's instruction:
>   - **Failure is defined by what the theory requires.** A claim fails when a
>     fair comparison contradicts what the theory requires at the stated
>     horizons and levels of detail. A reversal over time is not by itself a
>     failure, since the theory predicts crossovers.
>   - **Guesses and claims are told apart by where they come from**, not by
>     their form: a theorem can require a threshold, and a sign can be a guess.
>     Either can be revised; the original and the reason stay on record.
>   - **Suffering result.** Distinguished as a ranking at the finest level of
>     detail tested, not yet certified across every admissible level.
>   - **Real systems** are physical correspondences that motivate the rate
>     hypothesis; the comparison of rates of opening futures in real systems
>     is open. The activity-matched comparison is "tested", not "decided", in
>     chapter 16.

> **Drafting note (r3, 18 October).**
> - Sol's review of r2, integrated with the originator's rulings 37 and 38:
>   - **Theory follows evidence** (ruling 37). Section 12.7 separates design
>     guesses (thresholds, horizons, sizes) from claims drawn from the
>     principle (signs, required consequences). A failed claim stays on record
>     with what it shows, and the theory changes to fit the evidence.
>   - **Rate, not totals** (ruling 38). Sections 12.2 and 12.8 no longer say
>     that our existence and the published record show organization outrunning
>     the thermal background. Real systems show organized processes raising
>     rates; whether that raises the rate at which futures open in real systems
>     needs tests of its own (chapter 15).
>   - **Suffering result** stated at the level of detail where it holds
>     (ledger r9, C16).
>   - **Other ethical theories.** The opening no longer says they cannot face
>     the question; it says they make no claim that can be computed in a
>     physical model.
> - Approved by the originator on 18 October (Sol item 8): one sentence in
>   section 12.5 joining the two tests: a ranking holds only when it is
>   resolved, with the same sign, at every admissible level of detail.
> - Template: one TL;DR per chapter, on trial (ruling 40). In the markdown it
>   stays at the top; in the PDF it may become a box within the chapter.
>   Chapter-numbered definitions and `#overview-N` links remain provisional.

> **Drafting note (r2, 17 October).**
> - Changes from r1:
>   - **Voice.** Rewritten in the Overview's voice: each rule is explained
>     through the case that taught it. Status labels appear only in the table
>     at the end.
>   - **Plain terms.** "Comparison" replaces "declared contrast". Resolved and
>     unresolved, and two-factor reporting, are explained in the text, with a
>     new definition (12.5).
>   - **The three rubric rules** (inner degrees of freedom, resolved and
>     unresolved, two-factor reporting) are stated plainly, as accepted for
>     this version (ruling 36). The [P5] markers are removed.
> - Template choices still to confirm: one TL;DR per chapter; definitions
>   numbered by chapter until compilation; links to the Overview as
>   `#overview-N`.
> - Sources: ledger r9 (evidence rubric, reading rule, structural account, two
>   layers, A3, A4, A22, C1a, C3, C23); program review r1; Appendix A r11;
>   standing rulings 4, 6, 7, 12, 13, 14, 36, 37 and 38.

> **TL;DR**
>
> The thesis is tested in small physical worlds that are computed exactly.
> Each test compares options from the same present, with everything else held
> fixed, at a stated level of detail and over a stated time. A result counts
> only if its model contains what the claim is about; otherwise it is a
> diagnostic, useful for building the next test and nothing more. Results
> are read for what they show about the principle, not for whether a guess
> made beforehand came true, and when a claim drawn from the principle fails,
> the theory changes. This chapter develops the method behind
> [Overview section 6](#overview-6).

How do you test an ethics? Most ethical theories make no claim that can be
computed in a physical model, so for them the question does not arise. The
central thesis makes one. This chapter explains how the program tests
it, and what its tests can and cannot show. The verdicts themselves come later,
in Parts IV to VI and in [chapters 31](#chapter-31) and [32](#chapter-32).

---

## 12.1 What there is to test

**Both sides of the thesis can be examined: what we recognize as good and
harmful, and what happens to the futures.**

The thesis says that what we recognize as good corresponds to widening the
whole field's futures, and what we recognize as harm to narrowing them. One
side of that correspondence is given in advance. We already recognize
domination, suffering and waste as harms, and building, cooperation and repair
as goods, whatever any theory says about them. The other side is physical: how
much a present keeps open, measured by lushness.

So the thesis can be put at risk. Take a class of cases in which our
judgements are clear. Build physical models of them. Measure what the options
do to the futures. If what we recognize as harm turns out to widen the whole
field's futures, and the model is a fair one, the thesis has lost a case.

> **Plain-English definition 12.1: Test class**
>
> A family of cases that bears on one part of the central thesis, with cases
> where it should hold, cases where it should fail, and matched controls.

---

## 12.2 Small worlds, computed exactly

**Omega cannot be computed whole. The part of it a comparison needs can be
computed exactly, in a small enough world.**

For any realistic system, Omega is far beyond computation, and estimates of
lushness for large systems carry errors no one yet knows how to bound
([chapter 33](#chapter-33)). So the program builds small worlds instead. Each
is a specified physical system: a finite set of states, a law giving the
probability of every step, and whatever bookkeeping the case needs, such as
energy, resources and costs. In a world that small, the lushness of every
option at every horizon can be computed exactly, one step at a time
([Theorem A.2.1](#a-2-1)).

> **Primer: exact, not estimated**
>
> A simulation runs a model many times and averages what it sees, so its
> answers carry sampling error. An exact computation does not run the model at
> all. It carries the whole probability law forward step by step and computes
> the entropy of the histories directly. The answer is the model's answer, to
> the precision of the arithmetic. In the program's runs, energy is conserved
> to within about 10⁻¹¹, and the contributions to each entropy add up to the
> total to within about 10⁻⁹ bits.

Small worlds have a clear reach, and a clear limit.
- **They show what lushness ranks** in a specified physical setting, with no
  estimation error, and how the ranking changes with the level of detail, the
  horizon and the parameters.
- **They do not show that real systems behave the same way.** A model result
  holds within its model. Published studies show organized processes raising
  rates of energy capture and of adaptation in real systems. They do not
  measure lushness.

So every result in this manuscript comes with its model and its scope, and
with a sentence saying how far it bears on the thesis.

---

## 12.3 Two questions

**One kind of experiment asks what the measure ranks. Another asks what an
agent inside the world can find out and do.**

The two questions need different experiments.
- **What does lushness rank?** Here the model is known exactly, and any
  controller in it has the exact model and sees everything. We call these
  oracle experiments.
- **What can an agent inside the world know and do?** Here the controller sees
  only part of the world, is unsure of its law, or holds the wrong model. We
  call these bounded-agent experiments.

> **Plain-English definition 12.2: Oracle layer**
>
> Experiments in which the model is known exactly and nothing is hidden from
> the controller. They show what the measure ranks.

> **Plain-English definition 12.3: Bounded-agent layer**
>
> Experiments in which the controller is uncertain, partially informed or
> mistaken about its world. They show what an agent inside the world can know
> and do.

> **In Omega**
>
> An oracle experiment reads Omega's ordering directly. A bounded-agent
> experiment asks how much of that ordering a frame inside Omega can find from
> its own records.

Keeping the two apart settles three things.
- **Claims about uncertainty need the bounded layer.** Precaution, option
  value, deference and correction all come from uncertainty
  ([Overview section 5](#overview-5)). An oracle experiment cannot confirm or
  refute them, because its controller has nothing to be uncertain about.
- **Re-planning is not uncertainty.** A controller that has the exact model
  and re-plans at every step is still an oracle. Such controllers are useful as
  a check that a result does not depend on fixing the policy in advance.
- **Looking has two effects.** When a bounded controller inspects its world,
  the inspection changes what it does next, and the inspection itself is a
  random event. Lushness counts both, since randomness counts. Only the first
  is the value of information, so the two are reported separately.

---

## 12.4 Comparing like with like

**Every test compares options from the same present, and says in advance
everything that could change the answer.**

A test of the thesis is never a single number. It is a comparison, and before
it is read, it states five things:
1. **where it starts:** the present, and the world's law;
2. **what the options are:** what differs between them;
3. **what is held fixed:** resources, costs, the set of states, and anything
   else that must match;
4. **the level of detail:** which states count as different, and how often the
   system is read ([Definition A.6.1](#a-6-1));
5. **how far ahead:** the horizon.

> **In Omega**
>
> A comparison picks out two or more sets of futures in Omega, all leaving the
> same present, and fixes how finely and how far they are read.

**What a comparison can show depends on what it varies**
([Definition A.3.6](#a-3-6)).
- **Different starting points, one law.** If the law is finite and every
  development eventually shares it, the starting points can differ only by a
  head start, never in rate ([Theorem A.3.5](#a-3-5)). So no such comparison
  can show a lasting difference in rate, and finding none is not a gap in the
  evidence.
- **Different policies, one world.** These can differ in rate.
- **Different laws.** A rate advantage found here is an advantage of one law
  over another. It does not show that one start within a law beats another.

---

## 12.5 What every comparison reports

**The same five things, every time, so that no result can be read selectively.**
- **The profile.** The difference in lushness at every horizon, with its rate,
  its head start and the point where one overtakes the other
  ([Corollary A.3.9](#a-3-9)).
- **Narrowing or widening,** for the whole field and for any part of it the
  claim concerns ([Definition A.9.2](#a-9-2)).
- **Foreclosure:** which futures one option makes impossible. It is reported
  beside narrowing, because either can happen without the other
  ([Definition A.9.3](#a-9-3)).
- **Whether the sign holds.** A ranking counts only if it keeps its sign at
  every admissible level of detail ([Definition A.6.5](#a-6-5)). A small
  difference that keeps its sign is a ranking. A large one that flips is not.
- **Whether it is resolved.**

The last needs explaining. Sometimes a quantity cannot be computed exactly,
only bounded. This happens for one part of a world whose own states reveal
little about the rest ([Definition A.7.4](#a-7-4)), and for whatever lies
beyond the horizon ([Proposition A.12.1](#a-12-1)).
- **Resolved:** the ranges for the two options do not overlap, so we know which
  is larger. In the domination model of [Overview section 6](#overview-6),
  the blocker's own gain lies between +4.85 and +14.06 bits. The whole range is
  above zero, so the blocker gained.
- **Unresolved:** the ranges overlap, so at that level of detail we cannot say
  which is larger. In an earlier domination model, the blocker's own lushness
  stayed unresolved at every setting.

An unresolved comparison is not a tie. It is a question the computation has not
yet settled, and it supports no ranking either way. The same holds for a
ranking whose sign flips between admissible levels of detail. Put together:
**a ranking holds only when it is resolved, with the same sign, at every
admissible level of detail.**

> **Plain-English definition 12.4: Resolved and unresolved**
>
> A comparison is resolved when the computed ranges for its options do not
> overlap, so which is larger is known. It is unresolved when they overlap.
> Unresolved is not a tie.

---

## 12.6 When a result counts

**A result counts only if its model contains what the claim is about.**

A model can always teach us about what it contains: a fact about the measure, a
local mechanism, how a single agent behaves. It bears on the thesis only if
five conditions hold.
1. **Matched.** What is conserved, and the resources available, are the same
   across the options.
2. **Present.** The relation the claim is about is physically in the model. A
   claim about domination needs a dominator and a dominated party, coupled.
3. **Stable.** The quantity compared was not changed after the results were
   seen.
4. **Accounted.** The physical bookkeeping is complete enough for the claim.
5. **Not built in.** Nothing in the model settles the answer in advance.

A result whose model fails any of the five is a **diagnostic**. It tells us
something about the model, which helps build the next one. It tells us nothing
about the thesis, and it is never cited as support. Diagnostics are kept on
record in [Appendix H](#appendix-h).

> **Plain-English definition 12.5: Diagnostic**
>
> A result from a model that does not contain what a claim is about, or that
> fails one of the five conditions. It informs the next test. It is not
> evidence for or against the thesis.

**The rule cuts both ways.** A favourable result from a flawed model is a
diagnostic too. An unfavourable result can be set aside only by naming the
condition its model fails.

Two of the program's own runs show why the conditions are needed.
- **The control that was a better law.** An early test set an organized,
  catalysed process against an "uncatalysed" control. The control turned out to
  allow the same feedback with no apparatus at all, at the rate the catalysed
  process reached only when its rare apparatus happened to be present. The
  control won, 36.60 bits to 36.36. It was bound to: it was a more permissive
  law. The answer was built in, so the result is a diagnostic. All it shows is
  that making an open path depend on rare apparatus reduces access.
- **The calm valuer that was a simpler one.** The first test of the suffering
  prediction compared a valuer that struggles against an obstacle with a calm
  valuer facing the same obstacle. It found two counterexamples, of +0.258 and
  +0.153 bits. But the calm valuer had lost its inner variation as well as its
  distress, so the test compared the suffering valuer with a simpler one. Once
  the inner variation was matched, the prediction held at all 18 primary
  points at the finest level of detail tested, and no comparison was shown to
  reverse at a coarser one. Coarser levels leave many comparisons unresolved,
  so until those levels are resolved or shown to be inadmissible, this is a
  ranking at the finest level tested, not one certified across every
  admissible level ([chapter 19](#chapter-19)).

The second case gives a rule of its own. **"The same valuer without X" keeps
everything about the valuer except X**: the same states, the same laws by which
it changes, the same costs. Only the coupling that makes X is removed. That is
a rule about how to run the comparison, not a theory of what a valuer is.

---

## 12.7 Reading what a run shows

**A run is read for what it shows about the principle, not for whether a guess
came true. The theory answers to what it shows.**

Before a run, the program writes down what it expects, and the expectations
are of two kinds.
- **Design guesses:** what was anticipated in order to design the run, such as
  where a crossover will fall or how large an effect will be. A run that misses
  one has refuted the guess, not the principle.
- **Claims drawn from the principle:** what the theory requires, whether a
  sign, a threshold or a crossover. A fair comparison that contradicts one
  counts against the principle.

What separates the two is where an expectation came from, not its form. A
theorem can require a threshold, and a sign can be a guess. Either kind can be
revised when the evidence warrants, and the original expectation and the reason
for revising it stay on record.

In one batch, four predictions about informed action were all made for a
horizon of 64 steps. The horizons at which information actually repaid its
cost turned out to lie between 220 and 879 time units. The predictions were
wrong about time. The principle held: informed action had the higher rate in
all 57 comparisons.

When a claim fails, the record keeps the failure and what it shows about
where the theory went wrong, and the theory changes to fit the evidence. The
program is after what is true, not after keeping its first statement of it. A
claim fails when a fair comparison contradicts what the theory requires at the
stated horizons and levels of detail. A reversal over time is not by itself a
failure: the theory predicts crossovers ([Overview section 4](#overview-4)), and
a crossover where one was predicted is a success. Behaviour the account
predicts is not a failure, however it looked to whoever filed the guess. Several early reports scored a protection
policy as failing because the policy that kept the most open kept slightly
less stock than a cautious control. The account says to keep channels open, not
to hoard stock ([Overview section 4](#overview-4)). That is the behaviour it
predicts.

**Some experiments vary two things at once, and then the whole picture is
reported.** The main case asks two questions about an inner register: does it
carry information about the world, and can it act on the world? That makes
four versions. The difference between "informed and acting" and "random and
idle" splits exactly into three parts: what information adds alone, what action
adds alone, and what they add only together
([Proposition A.8.3](#a-8-3)). All three are reported, with every raw score,
and a winner is never reported on its own.

The reason is that the answer often lives in the third part. In the renewal
model, informed action beat random action in all 57 comparisons. Yet
information alone and action alone each beat the idle version in none of them.
Reporting only the winner would hide that the whole advantage comes from
putting the two together.

**Every important number is placed in Omega.** Alongside each result, the
program answers nine questions:
1. What changed in Omega?
2. Which channel or dependency caused the change?
3. How robust, repairable or replaceable is that channel?
4. Does using it wear it down or keep it up?
5. Do later structures rebuild or extend it?
6. What remains after it is lost, and what would be there without it?
7. What does lushness over the finite horizon say?
8. What does the long-run rate say?
9. Do the answers hold at every admissible level of detail?

These answers explain a result and help predict the next one. They never
overrule lushness. Where they disagree with it, that disagreement is evidence
about what the measure compresses away, which is part of the thesis
([chapter 16](#chapter-16)).

---

## 12.8 Gas is the opponent

**Lushness counts everything, gas included, so disorder is the baseline every
claim about organization has to beat.**

The random motion of a gas branches, and at fine detail it branches
enormously. Lushness counts that branching ([Overview section 3](#overview-3)).
So any claim that organization widens the future is made against a strong
opponent, and the program keeps the opponent in view.

Three things follow.
- **Capability, not margin.** What has to be shown is that organization can
  raise the rate at which futures open. It does not have to beat the thermal
  background by a large margin.
- **Under one law, only head starts.** In a finite world where every
  development eventually shares one law, an organized start cannot beat a
  disordered start in rate ([Theorem A.3.5](#a-3-5)). The comparison can show
  a head start, and that is all it can show. Rate advantages belong to
  comparisons between laws, and to worlds that grow or never settle down.
- **Disorder's advantage must be in the model.** A comparison means
  organization against disorder only if the model contains what makes disorder
  the default: free motion, positions, room to spread. A model without
  positions compares more machinery with less, not organization with disorder.

So the baseline is read within its own model. On a spatial lattice, an
organized seed beat the full thermal mixture and lost to an unbound start. In a
model that counts molecules without positions, it beat the unbound start and
lost to the thermal mixture. Neither result transfers to the other model.

Real systems offer physical correspondences: organized processes raising the
rate of energy capture and of adaptation by building on what they have built
([Overview section 4](#overview-4)). They motivate the hypothesis that
organization raises the rate at which futures open. They do not test it, and
that comparison in real systems is still open ([chapter 15](#chapter-15)).
Whether the measure prefers organization to disorder doing as much is tested
in [chapter 16](#chapter-16). Comparisons
with a gas in the test bed check that a model captures the dynamics that
matter.

---

## 12.9 Anyone can check

**Every number in this manuscript comes from a script, run on recorded inputs,
and can be computed again.**
- **Recorded inputs.** Each run starts from an input whose fingerprint is kept
  with the result.
- **Limited runs.** Time and memory are capped, and the caps are recorded.
- **Results written by the run.** Nothing is copied out by hand.
- **Second checks.** Key figures are recomputed by a second implementation,
  and the checks on energy and on the entropy totals are reported with the
  result.
- **Everything specified.** Every worked example names its script
  ([Appendix B](#appendix-b)), and every model is specified in full
  ([Appendix C](#appendix-c)).

---

## 12.10 Toward one model

**Ideally one world would show everything the thesis predicts. Until then, the
models have to overlap.**

Each test class now runs in its own model. The ideal is one model in which all
of Omega's predicted properties appear together, and perhaps others nobody has
predicted. Short of that, the models should share enough (mechanisms,
baselines, results that agree where they meet) to support conclusions about
the thesis as a whole.

The overlap so far is partial. The compounding, renewal and protection models
share mechanisms of capture, construction and wear. The domination and
suffering models stand further apart. The next model in the program's order of
work is spatial, with several carriers and a loop that keeps itself going. That
is where the comparison against a gas belongs, and it is the first step toward
one model ([chapter 33](#chapter-33)).

---

## 12.11 What this chapter does not claim

- **That small worlds stand in for real ones.** A model result holds within its
  model, and how far it bears on the thesis is said every time.
- **That published studies confirm the measure.** They show that a mechanism
  operates in real populations and ecosystems. They never show that lushness is
  the right ranking.
- **That the thesis is true.** This chapter says how the thesis can be tested,
  and how a test can count against it.

---

## Status of chapter 12

| Status | Claims |
|---|---|
| **D** (definitions and rules of method) | test class (12.1); oracle and bounded-agent layers, and the three rules that follow (12.3); what a comparison states (12.4); what every comparison reports (12.5); resolved and unresolved (12.5); the five conditions and the diagnostic (12.6); "the same valuer without X" (12.6); a ranking holds only when resolved with the same sign at every admissible level of detail (12.5); reading results for the principle; design guesses and claims, told apart by where they come from; a claim fails when a fair comparison contradicts what the theory requires; revising the theory when a claim fails (12.7); reporting two-factor experiments in full (12.7); the nine questions (12.7); capability, not margin (12.8); reproducibility (12.9) |
| **T** | exact computation of lushness ([Theorem A.2.1](#a-2-1)); starting points under one shared finite law differ only by a head start ([Theorem A.3.5](#a-3-5)); bounds and resolved rankings ([Definition A.7.4](#a-7-4), [Proposition A.12.1](#a-12-1)); the three-part split of a two-factor difference ([Proposition A.8.3](#a-8-3)) |
| **M** | the permissive "uncatalysed" control, 36.60 against 36.36 bits, as a diagnostic (12.6); the calm-valuer counterexamples removed by matching, and the matched result as a ranking at the finest level tested (12.6); the blocker's resolved gain of +4.85 to +14.06 bits (12.5); informed action's higher rate in 57 of 57 comparisons, with repayment horizons of 220 to 879 time units (12.7); information alone and action alone beating the idle version in none of the 57 (12.7); baselines inverting between the lattice and count models (12.8) |
| **E** | organized processes raising rates of energy capture and of adaptation, as physical correspondences that motivate the rate hypothesis, as cited in [Overview section 4](#overview-4) (12.8) |
| **N** | none |
| **C** | none asserted; the central thesis is referred to, not argued |

## References cited in chapter 12

No outside works are cited in this chapter. The published studies referred to
in section 12.8 are cited in [Overview section 4](#overview-4) and
[chapter 15](#chapter-15).
