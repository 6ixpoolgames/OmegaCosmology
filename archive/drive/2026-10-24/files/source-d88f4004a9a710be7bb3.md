# 6. How long things last

> **Drafting note (r1, 22 October).**
> - First draft, following outline r18 (chapter 6) and the concept ladder
>   (persistence; hazard; regeneration; robustness floor; generative
>   window), in the form of rulings 63–69: a headline and takeaways, claims
>   stated as strongly as they can be defended, qualifications argued in the
>   body, and physical examples where they help.
> - **Sources:** outline r18; Overview r19, section 4 ("What lasting is
>   worth", "What an early end costs"); Appendix A r16, sections A.4 and A.5.
>   The metavalue, and why persistence matters for value at all, are left to
>   chapter 9; option value and precaution to chapters 18 and 25.
> - Script: `analysis/ch6/ch6_numbers.py` computes the workshop, machine,
>   mixture, long-shot and window numbers, and checks each closed form
>   against an exact computation on the full chain (agreement to the
>   precision shown). The structure of section 6.4 (3,538.4 bits) and its
>   tie are Appendix A's worked example (Corollaries A.4.4 and A.4.6,
>   verifications V5 and V6).
> - The drafting notes are working provenance. They are removed at
>   compilation and kept in the revision record (Appendix H).

> **TL;DR**
>
> Lasting is worth exactly what it keeps open beyond whatever would replace
> it. An early end costs most when nothing can rebuild what was lost.
>
> - **Persistence has no worth of its own in the measure.** Each extra step a
>   regime is expected to last is worth its rate minus its successor's: about
>   2 bits a step for a workshop replaced by a poorer one, about −1 for one
>   replaced by a richer one.
> - **An early end costs the excess, divided by the hazards.** A machine that
>   fails at 1 per cent a step costs 106 bits to lose if it is never rebuilt,
>   and 87 if it is rebuilt after a mean of 500 steps.
> - **Fragile gains must pay for themselves.** Giving up a 3,538-bit structure
>   for a faster rate needs a gain of 0.35 bits a step if the gain lasts about
>   10,000 steps, and 0.035 if it lasts about 100,000.
> - **The measure is neutral to risk in rate.** A gamble is worth its
>   probability-weighted rate, plus at most the uncertainty of the gamble.
> - **A finite world caps long shots.** With a bounded repertoire, a long
>   shot with a real downside loses once regimes last long enough, and no
>   gain outlasts the window it operates in.

Chapter 5 compared options as if their regimes ran for ever. None does. This
chapter lets regimes end at a random time and asks what their lasting is
worth, what an early end costs, and how fragile a gain can be and still be
worth taking. It develops the second half of
[Overview section 4](#overview-4). Every result is a theorem of
[Appendix A](#appendix-a), sections A.4 and A.5; those of section 6.5 and
6.6 are conditional on named physical premises. Why the persistence of
valuing matters for value at all is argued in [chapter 9](#chapter-9).

---

## 6.1 Regimes end

**A regime that ends at a random time is worth its rate times its expected
duration, plus its offset, less a bounded remainder.**

Machines break, populations die out, institutions dissolve. A regime is a
law that holds for a while: a machine running, a population thriving. Its
end is a physical event like any other, with a probability at each step.

> **Plain-English definition 6.1: Hazard**
>
> The probability, at each step, that a regime ends.

> **Plain-English definition 6.2: Expected persistence**
>
> The number of steps a regime is expected to complete before it ends. Under
> a constant hazard λ, it is (1 − λ)/λ: about 99 steps at a hazard of 1 per
> cent.

What a regime adds over its random life follows from chapter 5's identity,
averaged over when the end comes ([Theorem A.4.2](#a-4-2)).

> \[
> \mathbb E[\ell_N]=h\,\mathbb E[N]+b-\mathbb E[K^N b],\qquad
> \bigl\lvert\mathbb E[K^N b]\bigr\rvert\le\lVert b\rVert_\infty .
> \]
>
> *In words:* a regime that lasts a random time adds its rate times its
> expected persistence, plus its offset, less the part of the offset not yet
> realized when it ends, and that last part stays bounded however long the
> regime lasts.

Under a constant hazard the remainder has a closed form, and it shrinks in
inverse proportion to the expected persistence ([Theorem A.4.3](#a-4-3)).
This is the Laurent expansion of discounted value in dynamic programming
(Blackwell 1962; Veinott 1969; Puterman 1994), summed exactly and read for
lushness.

Holding the law fixed, lasting longer never lowers what a regime accrues:
each added step adds the branching expected at that step, and branching is
never negative ([Corollary A.4.7](#a-4-7)). That is about the regime's own
count. What its lasting does to everything else is the subject of the next
section.

> **Primer: expected value**
>
> When an outcome is uncertain, its expected value is the average of its
> possible values, each weighted by its probability. A regime that ends at
> step 10 with probability ½ and at step 30 with probability ½ has an
> expected duration of 20 steps. Expected values add: the expected total of a
> sum is the sum of the expected parts. Decision theory compares uncertain
> options by expected value, or by expected utility when the stakes are not
> linear; the measure here needs only the first, because log lushness is
> already the quantity being added.

> **In Omega**
>
> A regime's end belongs to Omega like any other event: the futures in which
> it ends early and the futures in which it lasts are both branches of the
> same structure, each with its probability.

---

## 6.2 What lasting is worth

**Each step a regime is expected to last is worth its rate minus the rate of
whatever replaces it.**

When a regime ends, something follows: a successor law. Over a long horizon,
the whole development's log lushness grows at the successor's rate, and the
regime's contribution is a lasting offset on top of it. Its value is given
in closed form ([Proposition A.4.8](#a-4-8)).

> \[
> \frac{d}{dm}\Bigl[\lim_{T\to\infty}\bigl(\ell_T-h'T\bigr)\Bigr]
> =h-h'+\log_2\!\Bigl(1+\frac1m\Bigr)+\bigl[Z(mI+Z)^{-2}b\bigr]
> =h-h'+O(1/m).
> \]
>
> *In words:* one more step of expected persistence is worth the regime's
> rate less its successor's, plus two terms that fade as the regime lasts
> longer: the branching of its uncertain ending, and the share of its offset
> it realizes.

**Example 6.1: a workshop and what replaces it.** A workshop uses 16 tools in
any of 16 equally likely ways: 4 bits a step. It closes at a constant hazard,
and the site passes to a successor.
- **Replaced by a poorer successor** that uses 4 tools (2 bits a step), each
  extra step of expected persistence is worth 2.14 bits at an expected
  persistence of 10 steps, 2.01 at 100, and 2.001 at 1,000. Over everything
  that follows, a workshop expected to last 1,000 steps leaves the whole
  development 2,009 bits ahead of the successor's line.
- **Replaced by a richer successor** that uses 32 tools (5 bits a step), each
  extra step is worth −0.86 bits at 10 steps, −0.99 at 100, and −0.999 at
  1,000. The workshop narrows the whole by lasting.

Exact computation on the full chain agrees with the closed form to the
precision shown.

Three things follow.
- **Persistence has no worth of its own.** In the measure, lasting is worth
  exactly what the regime adds, step for step, over its successor. A
  structure whose replacement would keep more open narrows the whole by
  surviving. That is the sense in which persistence is instrumental. Why the
  persistence of valuing nonetheless underlies every value still to come is
  a different claim, argued in [chapter 9](#chapter-9).
- **Ending is itself a branch.** When something ends is uncertain, and the
  measure counts that uncertainty. A regime expected to last 1,000 steps
  carries 11.4 bits in the timing of its end. That grows only with the
  logarithm of the expected persistence, while the rate term grows in
  proportion to it.
- **The policy is to keep channels open, not to preserve stock.** What lasts
  is worth what it keeps open. The program's test-bed models behave this way
  ([model](#c-channels)).

> **In Omega**
>
> How long a structure lasts is part of the futures that contain it. What
> its lasting is worth is how much more those futures branch than the
> futures in which it has been replaced.

---

## 6.3 What an early end costs

**Ending a regime early costs the difference between what it adds each step
and what its successor adds, divided by the hazard of ending plus the hazard
of being rebuilt.**

Some losses are repaired. A machine that breaks may be rebuilt; a population
that dies out in one valley may recolonize it from the next. Others are
never repaired.

> **Plain-English definition 6.3: Regeneration**
>
> The rebuilding of a regime after it has ended, at a hazard of its own: the
> probability, at each step, that what was lost is restored.

Let a regime add s_R bits a step and its successor s_S, ending and rebuilding
included. An early end moves the development from the regime to the
successor now ([Proposition A.4.9](#a-4-9)).

> \[
> C=\frac{s_R-s_S}{\lambda+\gamma} .
> \]
>
> *In words:* the cost of an early end is the regime's excess over its
> successor, per step, divided by the hazard of ending plus the hazard of
> being rebuilt. When nothing can rebuild it, the cost is the whole excess
> over the regime's expected remaining life.

**Example 6.2: a machine that breaks.** A machine uses 4 tools in any of 4
ways, 2 bits a step, and fails at a hazard of 1 per cent a step. A broken
machine is scrap that settles into one of 2 states each step: 1 bit.

| Rebuilt at hazard | Mean time to rebuild | Cost of breaking it now |
|---|---|---|
| 0 | never | 106.08 bits |
| 0.002 | 500 steps | 86.83 bits |
| 0.01 | 100 steps | 49.50 bits |

If instead the broken machine's parts feed a process that branches 3 bits a
step, breaking it now widens the future: the cost is −93.92 bits if the
machine is never rebuilt. The sign is the sign of the excess. Exact
computation on the full chain agrees with the formula in every case.

Three consequences carry through the manuscript.
- **Irreversibility is the case γ = 0.** Where nothing can rebuild what an
  early end removes, the difference is permanent, and the cost is as large
  as it can be for the given hazard of ending. Precaution and option value
  take their force from this case ([chapter 18](#chapter-18);
  [chapter 25](#chapter-25)).
- **Regeneration shrinks the stakes, whichever their sign.** A world that
  rebuilds quickly makes early ends cheap and makes them gain little.
- **Where neither hazard is positive,** an early end changes the rate, and
  its cost grows without bound with the horizon (chapter 5).

The formula takes the hazard of regeneration as given. Why our world rebuilds
so little of what is lost, the alignment of irreversibility with the order of
time, is the subject of [chapter 28](#chapter-28).

> **In Omega**
>
> An early end moves the development into the futures in which the regime
> has stopped. What that costs depends on how readily Omega's law leads back
> to the futures in which it runs again.

---

## 6.4 Fast but fragile

**A gain in rate is worth what it costs only if, spread over its expected
life, it repays what is given up.**

Chapter 5 found that a faster rate eventually beats any head start. That
assumed the faster regime lasts. A regime that may end has to repay its
deficit before it does.

**When the faster option wins.** Two options trade a head start against a
rate. The faster one wins when its regime is expected to last longer than
the crossover horizon, less the mean time it takes for the head start to be
realized ([Corollary A.4.4](#a-4-4)). In Appendix A's worked example, one
option keeps a structure with 16 equally likely states for a mean of 1,000
steps before settling into a residual process that branches 0.469 bits a
step; over that residual, the structure is worth 3,538.4 bits. The other
option destroys it at once, for a residual 0.1 bits a step faster. The
crossover horizon is 35,384 steps, and the options tie at an expected
persistence of 34,384 steps.

**The floor on a fragile gain.** Now let the faster rate itself end, at a
hazard μ. Then it must repay the finite branching it gives up within its
expected life of about 1/μ steps ([Corollary A.4.6](#a-4-6)).

> \[
> \varepsilon>\frac{\mu\,(c+h_F)-h_2(\mu)}{1-\mu}.
> \]
>
> *In words:* a gain of ε bits a step, ending at hazard μ, is worth giving up
> c bits only if it exceeds the cost spread over its expected life, adjusted
> for the residual rate and for the branching of its own uncertain end.

> **Plain-English definition 6.4: Robustness floor**
>
> The smallest gain in rate that is worth what it costs, given how long the
> gain is expected to last.

For the 3,538-bit structure, set against a gain on the 0.469-bit residual:

| Hazard of the gain ending | Expected life | Gain needed |
|---|---|---|
| 10⁻³ | 1,000 steps | 3.53 bits a step |
| 10⁻⁴ | 10,000 steps | 0.352 bits a step |
| 10⁻⁵ | 100,000 steps | 0.0352 bits a step |
| 10⁻⁶ | 1,000,000 steps | 0.00352 bits a step |

The floor rises with the hazard. Strict priority of rate, chapter 5's
long-run verdict, is the limit in which every gain is assumed to last for
ever. One asterisk matters in practice: when the hazard is uncertain, the
expected life is an average of 1/μ over the possibilities, and that average
is dominated by the most optimistic of them. Section 6.6 shows what caps it.

---

## 6.5 Gambles and long shots

**The measure is neutral to risk in rate. In a finite world, a long shot with
a real downside loses once the stakes last long enough.**

A gamble splits the future: with some probability one development follows,
otherwise another. Its value is the probability-weighted value of its
outcomes, plus a bonus no larger than the uncertainty of the gamble itself,
the bonus being whole when the outcome is recorded
([Proposition A.5.1](#a-5-1)). In the long run it is worth exactly its
probability-weighted rate ([Corollary A.5.2](#a-5-2)).

> \[
> h(\text{gamble})=\sum_i p_i\,h_i .
> \]
>
> *In words:* in the long run, a gamble branches at the average of its
> outcomes' rates, weighted by their probabilities.

So the measure gives no weight to the spread of outcomes as such. Ruin counts
by its size: a loss that lowers the rate grows without bound with the
horizon, and so outweighs any finite gain. Its probability is not inflated.
A gamble an actor runs on itself, choosing at random between two policies,
gains at most one bit over the better of them, and almost nothing when one
policy is far better.

| Gap between the two policies | Best mixture's gain over the better |
|---|---|
| 0 bits | 1.000 bit |
| 2 bits | 0.322 bits |
| 5 bits | 0.044 bits |
| 10 bits | 0.001 bits |

**Long shots.** A long shot promises a large gain with small probability and
risks ruin otherwise. Three physical premises bound it
([Proposition A.5.3](#a-5-3)):
1. **finite repertoire:** at the declared level of detail, no state can reach
   more than M states in one step, so no rate exceeds log₂ M;
2. **a residual floor:** ruin leaves a process that still branches at some
   rate;
3. **a common relaxation:** both options' regimes end at the same hazard.

Given these, a gamble whose chance of success falls below a definite
threshold loses, both to doing nothing and to any sure gain, once the regimes
last long enough. For a system branching 1 bit a step, a ruined floor of 0.3
bits and a repertoire of 16, the threshold is 0.189: any long shot less likely
than that loses to doing nothing, however large its promised upside. With
no downside, the condition becomes the bound on fanaticism for finite
systems: a long shot loses to a sure gain whenever its probability times the
largest gain physically available falls short of the sure gain.

The premises carry the result. The repertoire is a property of the declared
description, and grows as the description is refined. That every faithful
level of detail of a finite physical system is finite is conjectured, with
physical information bounds (Margolus and Levitin 1998; Bekenstein 1981) as
the proposed justification; turning those bounds into a bound on the
histories counted here needs an argument still to be made
([chapter 33](#chapter-33)).

---

## 6.6 The generative window

**No gain outlasts the window in which it operates, and that caps the
optimistic tail of every uncertain estimate.**

> **Plain-English definition 6.5: Generative window**
>
> The span of time over which the conditions that support a family of
> regimes last: in the models, the expected time before the whole system
> relaxes.

If the world itself relaxes at a hazard of 1/T_G, no gain can contribute for
longer than about T_G steps, however robust it is, and a gain bought at a
finite cost c is worth taking only if it exceeds about c/T_G a step
([Corollary A.5.4](#a-5-4)). The window cuts off the optimistic tail that
dominates the robustness floor under uncertainty. With a cost of 3,538 bits,
and the gain equally likely to end at a hazard of 10⁻⁴ or 10⁻⁶, the floor built
on the expected life is 0.007 bits a step with no window, and 0.071 bits a
step within a window of 100,000 steps.

---

## 6.7 A finite regime still counts

**Transience does not zero worth. What a regime adds before it ends stays
added.**

One response to impermanence is that nothing lasts, so nothing matters. The
measure gives a precise reply in its own terms. A regime that ends adds its
branching to the futures that contain it, and that addition is not undone by
the end. Two finite histories still differ in total lushness, and over
everything that follows the verdict between them is finite and definite
([Corollary A.3.9](#a-3-9)). The structure is not flat because it ends.
Whether that ordering is value is the central thesis; [chapter 30](#chapter-30)
takes up the nihilist's case in full.

---

## 6.8 What the chapter gives the rest of the manuscript

- **Harm.** An early end, priced by its excess and its hazards, is the model
  of irreversible harm ([chapter 17](#chapter-17)).
- **Protection.** Keeping channels open, not preserving stock, is the
  measure's version of protection ([chapter 18](#chapter-18)).
- **Persistence and compounding.** Whether organized structure lasts long
  enough to raise the rate is tested in [chapter 15](#chapter-15).
- **Acting under uncertainty.** The robustness floor, the long-shot bound and
  the window are applied in [chapter 25](#chapter-25).

---

## 6.9 What this chapter does not claim

- **That persistence is valuable in itself.** In the measure it is worth what
  it keeps open beyond its replacement. Why the persistence of valuing
  matters for value is argued in [chapter 9](#chapter-9).
- **That everything that exists should be preserved.** A structure whose
  replacement keeps more open narrows the whole by lasting.
- **That the long-shot bound holds without its premises.** It is conditional
  on a finite repertoire, a residual floor and a common relaxation.
- **That the measure supplies prudence beyond expectation.** A margin for the
  actor's own model error is a policy for acting under uncertainty, not a
  theorem of the measure ([chapter 25](#chapter-25)).

---

## Status of chapter 6

| Status | Claims |
|---|---|
| **D** (definitions) | hazard, expected persistence (6.1); regeneration (6.3); robustness floor (6.4); generative window (6.6) |
| **T** (results, under their stated assumptions) | the random-horizon identity ([Theorem A.4.2](#a-4-2), proved here); the constant-hazard expansion ([Theorem A.4.3](#a-4-3), established elsewhere); persistence and accrual ([Corollary A.4.7](#a-4-7), proved here); what persistence is worth ([Proposition A.4.8](#a-4-8), proved here); the cost of an early end ([Proposition A.4.9](#a-4-9), proved here); when the faster option wins ([Corollary A.4.4](#a-4-4), proved here); the robustness floor ([Corollary A.4.6](#a-4-6), proved here); gambles ([Proposition A.5.1](#a-5-1)) and risk neutrality in rate ([Corollary A.5.2](#a-5-2)), proved here |
| **T, conditional on physical premises** | finite stakes ([Proposition A.5.3](#a-5-3)); the persistence cap ([Corollary A.5.4](#a-5-4)) |
| **M** | none; Examples 6.1 and 6.2 and the tables are exact computations in specified finite models; the test-bed's channel-keeping policy is cited (6.2) |
| **E** | none |
| **N** | none |
| **C** | that every faithful level of detail of a finite physical system is finite, the justification proposed for premise 1 of the long-shot bound (6.5) |
| **Open** | turning physical information bounds into a bound on counted histories (6.5) |

## References cited in chapter 6

*Collected with full details in Appendix G.* Entries marked "to verify" are
not yet checked against their sources.

- Bekenstein, J. D. (1981). Universal upper bound on the entropy-to-energy
  ratio for bounded systems. *Physical Review D* 23(2), 287–298. To verify.
- Blackwell, D. (1962). Discrete dynamic programming. *Annals of Mathematical
  Statistics* 33(2), 719–726. To verify.
- Margolus, N., and Levitin, L. B. (1998). The maximum speed of dynamical
  evolution. *Physica D* 120(1–2), 188–195. To verify.
- Puterman, M. L. (1994). *Markov Decision Processes: Discrete Stochastic
  Dynamic Programming.* New York: Wiley. To verify.
- Veinott, A. F. (1969). Discrete dynamic programming with sensitive discount
  optimality criteria. *Annals of Mathematical Statistics* 40, 1635–1660. To
  verify.
