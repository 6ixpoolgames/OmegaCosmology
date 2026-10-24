# 12. How the thesis is tested

> **Drafting note (r1, 17 October).**
> - First chapter drafted. It sets the chapter template: TL;DR, an opening
>   paragraph stating what the chapter claims and with what status, numbered
>   sections with bold headlines, definitions and "In Omega" boxes, a status
>   table, references.
> - **Template choices to confirm:**
>   - one TL;DR per chapter, with a bold headline opening each numbered
>     section, rather than a TL;DR per numbered section;
>   - definitions numbered provisionally by chapter (12.1, 12.2, …) and
>     renumbered through the manuscript at compilation, since chapters are
>     drafted out of order;
>   - links to the Overview use `#overview-N`.
> - **[P5]** The three rubric rules of ledger r7 (matching includes internal
>   degrees of freedom; resolution; factorial reporting) are proposals that
>   still need the originator's approval. Section 12.4 marks where they are
>   used.
> - Sources: ledger r9 (evidence rubric, reading rule, structural account, two
>   layers, A3, A4, A13, A22, C1a, C3, C23); program review r1; Appendix A r11;
>   standing rulings 4, 6, 7, 12, 13 and 14.

> **TL;DR**
>
> The thesis is tested in small physical models that are solved exactly. Every
> test is a declared contrast: options from the same present, compared at a
> stated resolution and horizon, with everything else held fixed. A result
> counts as evidence only if its model contains what the claim is about, with
> resources matched and nothing building in the answer; otherwise it is a
> diagnostic. Results are read for what they show about the principle, not for
> whether a guessed threshold was met. This chapter develops the method behind
> [Overview section 6](#overview-6).

This chapter states how the program tests the central thesis and what a test
can and cannot show. Its claims are of two kinds. Most are definitions and
methodological stipulations (status D): what a contrast is, what counts as
evidence, how results are read. The rest restate results proved in
[Appendix A](#appendix-a) that decide in advance what some contrasts can show
(status T). The chapter claims nothing about whether the thesis is true. That
is the business of Parts IV to VI, and of [chapters 31](#chapter-31) and
[32](#chapter-32).

---

## 12.1 Why small exact models

**Omega cannot be computed whole. The part of it a comparison needs can be
computed exactly, in a small enough model.**

Most ethical theories cannot be tested at all. They offer principles, and
principles are argued over, not measured. The central thesis is different in
kind. It says that what we recognize as good corresponds to widening the
whole field's futures, and what we recognize as harm to narrowing them. Both
sides of that correspondence can be examined. Our recognition of good and harm
is given in advance. The widening and narrowing are physical quantities.

The difficulty is size. Omega for any realistic system is far beyond
computation, and estimates of lushness for large systems carry errors that no
one yet knows how to bound ([chapter 33](#chapter-33)). The program therefore
works with models small enough to compute exactly. Each is a specified
physical system: a finite set of states, a law that gives the probability of
every step, and the physical bookkeeping (energy, resources, costs) the case
requires. For such a model the lushness of every option at every horizon is
computed without sampling, one step at a time ([Theorem A.2.1](#a-2-1)).

> **Primer: exact, not estimated**
>
> A simulation runs a model many times and averages what it sees, so its
> answers carry sampling error. An exact computation does not run the model at
> all. It carries the whole probability law forward step by step and computes
> the entropy of the histories directly. The answer is the model's answer, to
> the precision of the arithmetic. In the program's runs, energy is conserved
> to within about 10⁻¹¹, and the contributions to each entropy sum to the total
> to within about 10⁻⁹ bits.

What such models can show, and what they cannot, should be said at the start.
- **They can show what lushness ranks** in a specified physical setting, with
  no estimation error, and how the ranking depends on the resolution, the
  horizon and the parameters of the setting.
- **They cannot show that real systems behave the same way.** A model result
  holds within its model. That organized processes outproduce disorder in the
  real world is shown by the published literature (status E), not by the test
  bed, and the literature does not measure lushness.

So each result in this manuscript is reported with its model and its scope,
and how far it bears on the thesis is said every time.

---

## 12.2 Two layers

**One layer asks what lushness ranks. The other asks what an agent inside the
world can know and do.**

The program runs its experiments in two layers.
- **The oracle layer.** The model is known exactly, and the controller, if
  there is one, has the exact model and full information. Experiments in this
  layer show what lushness itself ranks.
- **The bounded-agent layer.** The controller observes only part of the
  world, is uncertain about its law, or holds a model that does not match it.
  Experiments in this layer show what an embedded controller can know and
  implement.

> **Plain-English definition 12.1: Oracle layer**
>
> Experiments in which the model is known exactly and nothing is hidden from
> the controller. They show what the measure ranks.

> **Plain-English definition 12.2: Bounded-agent layer**
>
> Experiments in which the controller is uncertain, partially informed or
> mistaken about its world. They show what an agent inside the world can know
> and do.

> **In Omega**
>
> The oracle layer reads Omega's ordering directly. The bounded-agent layer
> asks how much of that ordering a frame inside Omega can find from its own
> records.

Three rules follow from the split.
1. **Uncertainty belongs to the bounded layer.** Precaution, option value,
   deference and correction all derive from uncertainty
   ([Overview section 5](#overview-5)). An oracle experiment can neither
   confirm nor refute them, because its controller has nothing to be uncertain
   about.
2. **Re-planning is not uncertainty.** A controller that has the exact model
   and re-plans from each new present is still in the oracle layer. Such
   controllers check that a result does not depend on restricting attention to
   fixed policies.
3. **Inspection has two effects, and they are reported separately.** When a
   bounded controller inspects its world, the inspection changes what it does
   later, and the inspection event is itself random. The measure counts both,
   since randomness counts. Only the first is the value of information, and
   reports keep them apart.

---

## 12.3 The declared contrast

**Every test compares options from the same present, and declares everything
that could change the answer.**

A test of the thesis is never a single number. It is a contrast between
options, and the contrast is declared in full before it is read:
1. **the context:** the present from which the options start, and the model's
   law;
2. **the options:** what differs between them;
3. **what is held fixed:** resources, costs, state space and everything else
   that must match;
4. **the resolution:** the grain and the cadence at which futures are told
   apart ([Definition A.6.1](#a-6-1));
5. **the horizon:** how far ahead the comparison runs.

> **Plain-English definition 12.3: Declared contrast**
>
> A comparison between options from the same present that states its context,
> its options, what is held fixed, its resolution and its horizon.

> **Plain-English definition 12.4: Test class**
>
> A family of declared contrasts that bears on one part of the central thesis,
> with positive cases, negative cases and matched controls.

> **In Omega**
>
> A declared contrast picks out two or more sets of futures in Omega, all
> leaving the same present, and fixes how finely and how far they are read.

**What a contrast can show depends on its kind.** There are three kinds
([Definition A.3.6](#a-3-6)).
- **A preparation contrast** compares different presents under one law. If the
  law is finite and every development eventually shares it, the presents
  differ only by an offset, never in rate ([Theorem A.3.5](#a-3-5)). So no such
  contrast can show a lasting difference in rate, and its absence is not a
  gap in the evidence.
- **A process contrast** compares different policies under one controlled
  model. It can differ in rate.
- **A mechanism contrast** compares different laws. A rate advantage found
  here is a contrast between laws. It does not show that one start within a
  law is better than another.

**Every contrast reports the same things.**
- **The profile:** the difference in lushness at every horizon, with its rate,
  offset and crossover ([Corollary A.3.9](#a-3-9)).
- **Narrowing and widening** for the whole field and for any subject the claim
  concerns ([Definition A.9.2](#a-9-2)).
- **Foreclosure,** reported beside narrowing, since either can occur without
  the other ([Definition A.9.3](#a-9-3)).
- **Sign stability:** whether the sign of the difference holds at every
  admissible resolution ([Definition A.6.5](#a-6-5)). A small difference that
  keeps its sign is a ranking. A large one that changes sign is not.
- **Resolved or unresolved.** Where only bounds can be computed, as for a part
  of the field whose own states reveal little, a comparison is resolved only
  if the bounds do not overlap ([Definition A.7.4](#a-7-4)). Where a remainder
  beyond the horizon cannot be bounded, the comparison is unresolved, however
  large the difference so far ([Proposition A.12.1](#a-12-1)). "Unresolved" is
  a report about the bounds, not a tie.

---

## 12.4 What counts as evidence

**A result supports a claim only if its model contains what the claim is
about.**

A model can always support claims about the objects it contains: a theorem
about the measure, a local mechanism, a single-agent result. It supports a
claim about the thesis only if it meets five criteria.
1. **Matching.** Conserved quantities and resources are matched across the
   options.
2. **Presence.** The relation the claim concerns is physically present.
   Claims about domination, appropriation or the whole field need the coupled
   parties in the model.
3. **A stable objective.** The quantity compared was not changed after the
   results were seen.
4. **Accounting.** The physical bookkeeping is sufficient for the claim.
5. **No built-in answer.** No feature of the model predetermines the ranking
   being sought.

A result whose model misses any criterion is a **diagnostic**. It teaches
something about the model, and nothing about the claim. Diagnostics are kept
in the provenance ([Appendix H](#appendix-h)) and never cited as support.

> **Plain-English definition 12.5: Diagnostic**
>
> A result from a model that does not contain what a claim is about, or that
> fails one of the five criteria. It informs the design of the next test, and
> it is not evidence for or against the thesis.

**The rule cuts both ways.** Classification follows the structure of the model,
whatever the result. A favourable result from a model that fails a criterion is
a diagnostic. An unfavourable result can be set aside only by naming the
criterion its model fails.

**Two lessons from the program's own runs** show why each criterion is needed.
- **A permissive control.** One early comparison set an organized, catalysed
  process against an "uncatalysed" control. The control turned out to allow
  the same feedback with no apparatus at all, at the rate the catalysed arm
  reached only when its rare apparatus was present. The control won, by 36.60
  bits against 36.36. That was close to built in: it compared a more
  permissive law with a less permissive one. Under the fifth criterion the
  result is a diagnostic. It shows only that making an available coupling
  depend on rare apparatus reduces access.
- **A simpler comparator.** The first test of the suffering prediction
  compared a valuer that suffers under an obstacle with a calm valuer under the
  same obstacle. It gave two counterexamples, of +0.258 and +0.153 bits. But
  the calm valuer had also lost its inner variation, so the comparison set the
  suffering valuer against a simpler one. With the inner variation matched, the
  prediction held at every point. The two numbers stay on record as the reason
  for the rule below.

**Matching includes a valuer's inner degrees of freedom** [P5]. To compare "the
same valuer without X", keep the same states, the same laws of activation and
relaxation and the same costs, and remove only the coupling that constitutes X.
This is a declared method, not a criterion of identity for valuers.

---

## 12.5 Reading results

**A run is read for what it shows about the principle.**

Predictions and thresholds filed before a run are working guesses. They help
design the run. They are not verdicts on the principle.
- **A missed guess is a bad guess.** A run that demonstrates the principle but
  misses a guessed threshold has shown the principle and refuted the guess.
  In one batch, four predictions about an informed-action model were all made
  for a horizon of 64 steps, while the horizons at which information repaid
  its cost turned out to lie between 220 and 879 time units. The predictions
  were wrong about the horizon. The principle held: informed action had the
  higher rate in all 57 comparisons.
- **Adverse findings bear on the principle itself.** A sign that reverses at
  an admissible grain or horizon is adverse. So is a matched comparison that
  goes the wrong way within its scope.
- **Behaviour the account predicts is not a failure.** Several early reports
  scored a protection policy as failing because the policy that kept the most
  open kept slightly less stock than a protective control. The account says
  to keep channels open, not to maximize stock
  ([Overview section 4](#overview-4)). That behaviour is what it predicts.

**Two-factor contrasts are reported in full** [P5]. Where a contrast varies two
factors, such as information and action, the report gives the exact division of
the difference into what each adds alone and what they add together
([Proposition A.8.3](#a-8-3)), with every absolute score. A winner is reported
only together with where it sits relative to the boundary. Physical bills are
never added to entropy terms, and an interaction term never replaces the
quantity compared.

**Every important number comes with a structural account.** Nine questions
place it in Omega:
1. What changed in Omega?
2. Which channel or dependency caused the change?
3. How robust, repairable or substitutable is that channel?
4. Does using the channel deplete it or maintain it?
5. Do descendants reconstruct or expand it?
6. What remains after it is lost, and what would be available without it?
7. What does finite-horizon lushness report?
8. What does the long-run rate report?
9. Are those results stable across the admissible resolutions?

The structural account explains and predicts. It does not overrule lushness. A
disagreement between the two is evidence about what the measure compresses
away, which is part of the thesis ([chapter 16](#chapter-16)).

---

## 12.6 The gas baseline, and capability

**Everything counts, gas included, so disorder is the baseline every claim
about organization must beat.**

Lushness counts every future, random ones included
([Overview section 3](#overview-3)). The random motion of a gas branches, and
at fine grain it branches enormously. Any claim that organization widens the
future is therefore a claim against a strong opponent, and the program keeps
that opponent in view as a baseline.

Three consequences shape every test of organization.
- **Capability, not proportion.** What has to be shown is that organization
  can raise the rate at which futures open. A large margin over the thermal
  background is not required.
- **Same-law contrasts show offsets.** In a finite model where every
  development eventually shares one law, an organized start cannot beat a
  disordered start in rate ([Theorem A.3.5](#a-3-5)). The comparison can show
  an offset, and that is all it can show. Rate advantages belong to mechanism
  contrasts, and to systems that grow or never settle, where the theorem does
  not apply.
- **The model must contain disorder's advantage.** A comparison means
  organization against disorder only if the model contains the dispersal that
  makes disorder the thermal default: free motion, positions, room to spread.
  A model without positions compares more machinery with less, not organization
  with disorder.

The last point has a practical consequence. Reference outcomes are not
comparable across models. On a spatial lattice, an organized seed beat the full
thermal mixture and lost to an unbound start. In a model of counts without
positions, it beat the unbound start and lost to the thermal mixture. Each
result is read within its own model.

None of this is where the evidence for compounding comes from. That
organization can outrun the thermal background is shown by our own existence
and by the literature ([Overview section 4](#overview-4)). Comparisons with
gas in the test bed check that a model captures the dynamics that matter.

---

## 12.7 Reproducibility

**Every number in the manuscript is produced by a script, from frozen inputs,
and can be recomputed.**
- **Frozen inputs.** Each run starts from a recorded input whose hash is kept
  with the result.
- **Capped execution.** Runs are limited in time and memory, and the limits
  are recorded.
- **Automated reports.** Results are written by the run itself, not
  transcribed.
- **Independent recomputation.** Key figures are recomputed by a second
  implementation, and the checks on conservation and on the decomposition of
  entropy are reported with the result.
- **Scripts.** Every worked example in the manuscript names its script
  ([Appendix B](#appendix-b)), and every model is specified in full
  ([Appendix C](#appendix-c)).

---

## 12.8 The single-model ideal

**Ideally one model would show every property the thesis predicts. Until then,
the models must overlap.**

Each test class is now run in its own model. The ideal is a single model in
which all of Omega's predicted properties appear together, and perhaps others
not yet predicted. Short of that, the models should overlap enough that
conclusions about the thesis as a whole are warranted: shared mechanisms,
shared baselines, and results that agree where the models meet.

The overlap today is partial. The compounding, renewal and protection models
share a chemistry of capture, construction and wear. The domination and
suffering models stand further apart. The next model in the program's order of
work is spatial, with several carriers and a loop that sustains itself. It is
where the comparison against a gas belongs, and it is the first step toward a
single model ([chapter 33](#chapter-33)).

---

## 12.9 What this chapter does not claim

- **That small models represent real systems.** A model result holds within
  its model (status M). How far it bears on the thesis is stated each time.
- **That published correspondences confirm the measure.** They show that a
  mechanism operates in real populations and ecosystems (status E). They never
  show that lushness is the right ranking.
- **That the thesis is true.** The thesis remains a thesis (status C). This
  chapter says how it can be tested, and how a test can count against it.

---

## Status of chapter 12

| Status | Claims |
|---|---|
| **D** (definitions and methodological stipulations) | oracle layer and bounded-agent layer (12.2); the three rules that follow from the split (12.2); the declared contrast and the test class (12.3); what every contrast reports (12.3); the five criteria and the diagnostic (12.4); matching includes inner degrees of freedom [P5] (12.4); reading results for the principle (12.5); factorial reporting [P5] (12.5); the structural account (12.5); capability, not proportion (12.6); reproducibility requirements (12.7) |
| **T** | a preparation contrast under one shared finite law differs only by an offset ([Theorem A.3.5](#a-3-5)); exact computation of lushness ([Theorem A.2.1](#a-2-1)); resolved and unresolved comparisons ([Definition A.7.4](#a-7-4), [Proposition A.12.1](#a-12-1)) |
| **M** | the permissive "uncatalysed" control (36.60 against 36.36 bits) as a diagnostic (12.4); the calm-obstruction counterexamples removed by matching (12.4); informed action's higher rate in 57 of 57 comparisons, with repayment horizons of 220 to 879 time units (12.5); reference outcomes inverting between the lattice and count models (12.6) |
| **E** | organized processes outproducing the thermal background in the real world, as cited in [Overview section 4](#overview-4) (12.6) |
| **N** | none |
| **C** | none asserted; the central thesis is referred to, not argued |

## References cited in chapter 12

No external works are cited in this chapter. The correspondences referred to in
section 12.6 are cited in [Overview section 4](#overview-4) and
[chapter 15](#chapter-15).
