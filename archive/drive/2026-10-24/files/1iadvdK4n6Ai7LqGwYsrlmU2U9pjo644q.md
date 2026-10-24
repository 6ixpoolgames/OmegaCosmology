# 5. Futures through time

> **Drafting note (r2, 22 October).**
> - Sol's review of r1, with Sol's second message on the TL;DR (ruling 70).
>   - **Workshop (5.3) reconciled.** The r1 kernel made the step that
>     completes the build also the first use of the new tools, which the
>     description did not say. The model now ends the build in a ready state
>     and starts using the tools on the next step. Offset −40 bits (8 expected
>     steps at 1 bit instead of 6), crossover at 10 steps. Sol's recomputation
>     agrees.
>   - **One law, several closed classes** (TL;DR, 5.5): the claim is now
>     about starts that share a long-run regime. Building apparatus changes
>     the state and the effective dynamics of the parts, not the native law.
>   - **The ordering** (5.4) is a long-run verdict, not a claim about every
>     late horizon; in cycling developments the offset is an average and the
>     profile can keep oscillating; a tie on rate and offset is a tie on the
>     verdict, not identical profiles. The list of cautions is now a
>     paragraph.
>   - **Three kinds of comparison** (5.6): only process comparisons are
>     choices from one present; preparation and mechanism comparisons are
>     evidence of other kinds.
>   - **Tank** (5.5): the engine runs or waits before fuel arrives.
>   - **Ramsey removed** (5.4): whether not discounting is ethically right
>     belongs to Part III; the chapter says only that the measure has no
>     discount factor.
>   - Repeated announcements that rate beats offset are trimmed (5.3, 5.4).
> - Before upload (ruling 71): one line rewrapped, and the tank's "change of
>   law" now distinguishes a different law in the model from a different
>   physical setup in the world, in keeping with 5.5's treatment of
>   apparatus.

> **Drafting note (r1, 22 October).**
> - First draft, following outline r18 (chapter 5) and the concept ladder
>   (profile; rate; offset; crossover horizon). Written to rulings 63–68:
>   the TL;DR states the chapter's claims as takeaways, headline claims are
>   made as strongly as they can be defended, the qualifications are argued
>   in the body, and the examples are physical setups with exact numbers.
> - **Sources:** outline r18; Overview r19, section 4 ("Head starts and
>   rates", definitions 9–11); Appendix A r16, Definition A.3.1 to
>   Corollary A.3.9; v4 chapter 4 (r6), section 4.5, whose investment and
>   ruin examples are rebuilt here as the workshop and the fragile machine.
>   Persistence, hazards and the cost of an early end are left to chapter 6.
> - Script: `analysis/ch5/ch5_numbers.py` computes every number in the
>   chapter. The rate–offset identity holds in the tank model to 4 × 10⁻¹³
>   bits.
> - The drafting notes are working provenance. They are removed at
>   compilation and kept in the revision record (Appendix H).

> **TL;DR**
>
> Given time, a faster rate beats any head start. Within a shared long-run
> regime, a better start buys a lead, not speed.
>
> - **The profile is the comparison.** It is the difference in lushness
>   between two options, horizon by horizon. Its slope is the difference in
>   rate, its settling level the difference in offset, and its zero the
>   crossover horizon.
> - **Rate decides first, offset second.** Over everything that follows, the
>   option that branches faster wins, whatever its deficit. At equal rates,
>   the larger offset wins.
> - **Head starts lose on a schedule.** The crossover comes at the deficit
>   divided by the rate advantage. A workshop that builds tools before using
>   them gives up a 40-bit offset for 4 more bits per step, and overtakes
>   after 10 steps.
> - **A short horizon can rank a collapse first.** A fragile machine whose
>   breakdowns branch leads a robust one for 109 steps, then stops for good.
> - **A stock buys an offset, a supply sets the rate.** A full fuel tank is
>   worth exactly the 16 bits its fuel can run. How fast the engine branches
>   is set by the fuel supply.

Chapter 4 measured how much follows from a present up to a horizon. This
chapter compares two options across every horizon at once, and develops the
first half of [Overview section 4](#overview-4). Every result in it is a
theorem of [Appendix A](#appendix-a), section A.3, stated for finite models,
and each is shown in a model small enough to compute exactly. How long a
regime lasts, and what its end costs, is [chapter 6](#chapter-6).

---

## 5.1 Two ways to be ahead

**One option can be ahead now. Another can be pulling ahead. The profile
shows both at once.**

Take two options from the same present. At any horizon, chapter 4 gives each
a log lushness, and their difference says which keeps more open up to that
horizon. One horizon is one reading. The difference at every horizon, taken
together, is the object of comparison.

> **Plain-English definition 5.1: Profile**
>
> The difference in log lushness between two options from the same present,
> at every horizon.

An option can lead in two ways. It can start ahead and keep a fixed margin,
or it can branch faster and pull further ahead at every step. The profile
separates the two: a fixed margin shows as a level, a faster rate as a slope.

> **In Omega**
>
> The profile compares two parts of Omega that unfold from the same present,
> one section at a time. Every verdict about which option keeps more open is
> a reading of it.

---

## 5.2 Rate and offset

**Every finite process has a long-run rate of branching and a lasting
offset. Its log lushness at every horizon is rate times horizon plus offset,
less the part of the offset not yet realized.**

> **Plain-English definition 5.2: Rate**
>
> The branching a present's futures add per step, in the long run, in bits
> per step.

> **Plain-English definition 5.3: Offset**
>
> The lasting difference a present makes beyond its rate: the lead, in bits,
> that it keeps however long the development runs.

Both are defined for every finite kernel ([Definition A.3.1](#a-3-1)), and
they fix log lushness at every horizon ([Theorem A.3.3](#a-3-3)).

> \[
> \ell_n=n\,h+b-K^n b .
> \]
>
> *In words:* the log lushness of a horizon is the rate times the horizon,
> plus the offset, less the part of the offset not yet realized by then.

The last term is the part of the head start still to be cashed in. Where the
development forgets its start, that term shrinks to zero, and log lushness
becomes a straight line of slope h, raised by b. The identity needs neither
irreducibility nor aperiodicity; where the development cycles, the
unrealized part oscillates and averages to zero.

The rate has a plain source. A development eventually settles into one or
more closed regions of states it cannot leave. Its rate is the average
branching of those regions, weighted by the chance of settling in each
([Corollary A.3.4](#a-3-4)). Whatever happens before settling contributes to
the offset, not to the rate.

> **Primer: Markov processes**
>
> A finite Markov process moves among finitely many states, each step drawn
> from a table of probabilities that depends only on the current state
> (Norris 1997). Some groups of states, once entered, are never left: these
> are closed classes. A process confined to one closed class settles into a
> stationary law, the long-run fraction of time it spends in each state, and
> forgets where it started; how fast it forgets is its mixing time (Levin,
> Peres and Wilmer 2009). A process that cycles through its states in a fixed
> order is periodic: it settles only on average. Every finite process
> eventually enters some closed class (Kemeny and Snell 1960).

---

## 5.3 The crossover horizon

**A head start loses to a faster rate on a schedule: the deficit divided by
the rate advantage.**

When one option starts behind but branches faster, the profile crosses zero.

> **Plain-English definition 5.4: Crossover horizon**
>
> The horizon at which an option that starts behind but branches faster
> draws level, and after which it leads.

> \[
> T_\times=-\frac{\Delta b}{\Delta h} .
> \]
>
> *In words:* the faster option draws level after its starting deficit
> divided by its advantage in rate, up to an error no larger than the offsets
> not yet realized.

The error bound is stated in [Proposition A.3.7](#a-3-7). It is crude; in the
models of this manuscript, the profile changes sign within a step of T× once
the transients have passed.

**Example 5.1: build first or act now.** A workshop has 4 tools and can use
them in any of 4 equally likely ways at each step: 2 bits per step.
- **Act now.** It uses its tools at every step. Rate 2 bits per step, offset
  0.
- **Build first.** At each step it tries to double its tools, and succeeds
  with probability ½; each attempt, succeeding or failing, is itself a
  1-bit branch. On the fourth success it holds 64 tools, and from the next
  step on it uses them in any of 64 equally likely ways: 6 bits per step.
  The expected build takes 8 steps. Rate 6 bits per step, offset −40 bits:
  8 expected steps at 1 bit instead of 6.

The crossover horizon is 40 ÷ 4 = 10 steps, and exact computation agrees:
acting leads at every horizon up to 9 steps, by as much as 4.75 bits at step
6, and building leads from step 10 on.

| Horizon (steps) | Act now (bits) | Build first (bits) | Difference |
|---|---|---|---|
| 1 | 2.00 | 1.00 | −1.00 |
| 4 | 8.00 | 4.00 | −4.00 |
| 8 | 16.00 | 13.47 | −2.53 |
| 10 | 20.00 | 22.38 | +2.38 |
| 12 | 24.00 | 32.96 | +8.96 |
| 100 | 200.00 | 560.00 | +360.00 |

Building narrows the future while it lasts and widens it afterwards. A
comparison that stops before step 10 ranks building below acting; one that
runs past it ranks building above.

---

## 5.4 Rate decides first, offset second

**The long-run verdict orders options by rate, then by offset. A short
horizon can reverse it.**

A change that permanently lowers the rate eventually costs more than any
change whose cost is a finite offset ([Corollary A.3.8](#a-3-8)). The full
verdict reads off the profile ([Corollary A.3.9](#a-3-9)).

> \[
> \Delta_n(a:b)=n\,\Delta h+\Delta b-\bigl[(K_a^n b^a)(x)-(K_b^n b^b)(x)\bigr].
> \]
>
> *In words:* the profile grows by the difference in rate at every step, and
> settles to the difference in offset when the rates are equal. Over
> everything that follows, the option with the higher rate wins; at equal
> rates, the option with the larger offset wins; if both tie, the verdict is
> a tie.

This ordering is not new. It is the overtaking criterion for comparing
infinite programmes of growth (von Weizsäcker 1965), and the ordering by
gain, then bias, of average-reward dynamic programming (Veinott 1966). What
is new is the object it is applied to.

**Example 5.2: a robust machine and a fragile one.** Two machines each start
with 16 tools.
- **The robust machine** never breaks. At every step it uses its tools in any
  of 16 equally likely ways: 4 bits per step, for ever.
- **The fragile machine** breaks with probability 0.1 per step, in any of 64
  distinguishable ways, and loses a tool each time; otherwise it works like
  the robust one with the tools it has left. With no tools left it stops. It
  lasts 160 steps on average.

At first the fragile machine branches more: 4.67 bits in its first step
against 4, because its breakdowns are real branches and the count includes
them. It leads for 109 steps, by up to 22.8 bits at step 62. Then its losses
catch up with it. Its total converges to 569.3 bits and never rises again,
while the robust machine adds 4 bits every step. At 500 steps the robust
machine leads by 1,431 bits, and the gap grows without limit.

| Horizon (steps) | Robust (bits) | Fragile (bits) | Difference |
|---|---|---|---|
| 10 | 40.0 | 46.3 | +6.3 |
| 50 | 200.0 | 221.8 | +21.8 |
| 100 | 400.0 | 408.9 | +8.9 |
| 150 | 600.0 | 524.8 | −75.2 |
| 500 | 2,000.0 | 569.3 | −1,430.7 |

*The difference is fragile minus robust.*

This is the case chapter 4 warned about. Noisy failure looks like breadth
until its consequences arrive. A comparison cut off before step 110 ranks the
collapsing machine first.

**No step is discounted.** The profile weights no horizon above another. A
finite horizon is a truncation: it counts everything before it fully and
everything after it not at all. The measure itself introduces no discount
factor.

**What the ordering does and does not say.** It orders the long-run rate,
then the long-run offset. It is a verdict about everything that follows, not
a claim about every late horizon. In a development that cycles, the offset
is read as an average over the cycle, and the profile can keep oscillating
around it. Two options that tie on rate and offset tie on the verdict; their
profiles need not be identical. Where the state space grows or the law
changes over time, rate and offset may not exist at all, and the profile
itself is the object. And no agent computes the limit: a bounded agent acts
on finite horizons, with bounds on what it cannot see
([Proposition A.12.1](#a-12-1); [chapter 24](#chapter-24)). That is a way of
deciding, not a different comparison.

> **In Omega**
>
> Rate and offset are two features of how a part of Omega grows from its
> present: how fast its branches multiply in the long run, and how far ahead
> it starts.

---

## 5.5 A stock buys an offset; a supply sets the rate

**Where two starts settle into the same long-run regime, the better start
buys a lasting lead and never a faster rate.**

When every development from two presents settles into the same closed class
of one finite law, the two presents have the same rate. Their difference is
an offset, and the offsets average to zero over the long-run law
([Theorem A.3.5](#a-3-5)).

> \[
> h(x)=h(y)=\pi_C\,g .
> \]
>
> *In words:* when every development from both starts settles into the same
> closed class, both branch at that class's rate in the long run, and a
> better start buys only a lead.

**Example 5.3: a full tank and an empty one.** An engine draws on a tank that
holds up to 8 units of fuel. While the tank holds fuel, the engine runs: at
each step it does one of 4 equally likely things and burns one unit. With the
tank empty, it waits. After the engine has run or waited, a unit of fuel
arrives with probability 0.3, if there is room. Compare two presents of the
same engine: tank full and tank empty.
- **Same rate.** Both branch at 1.481 bits per step in the long run. That
  rate is set by the supply: the engine runs 30 per cent of the time, which
  gives 0.3 × 2 = 0.6 bits per step, and the arrival of fuel adds h₂(0.3) =
  0.881 bits.
- **Different offset.** The full tank leads by exactly 16.000 bits: 8 units,
  each running one 2-bit step that the empty tank never gets. The lead is
  2 bits after one step, 14.1 after 10, and 16.000 from about step 20 on. It
  never grows further.

A store of fuel is a head start. A larger tank, with the same supply, buys
a larger head start and nothing more. Only a faster supply, or an engine
that does more with each unit, changes the rate. In the model that is a
different law; in the world it is a different physical setup, which may have
to be built.

**The asterisks.** The theorem needs every development from both starts to
settle into the same closed class. One finite law can contain several closed
classes with different rates, and then a better start can buy a faster rate.
That happens in three ways, each of which the program studies:
- **Different closed classes under one law.** A seed that germinates and one
  that rots settle into different regions of the same physics.
- **Building apparatus.** Construction changes the state, and with it the
  dynamics of everything the apparatus acts on. The native law does not
  change. In the full description, the build moves the development into a
  different closed region; in a coarser description of the parts alone, it
  shows up as a change in their effective law.
- **A growing state space.** A process that keeps adding new kinds of state,
  as a population that builds new kinds of structure does, is not confined to
  a fixed set of closed classes, and its rate need not settle.

Whether organization escapes the theorem in these ways, in models and in
real systems, is the subject of [chapters 13](#chapter-13) and
[15](#chapter-15). This theorem is why the question has to be asked there: an
organized present that settles into the same closed class as its disordered
counterpart can buy an offset, and nothing more.

> **In Omega**
>
> Within one closed region of Omega's law, every present opens the same
> number of new branches per step in the long run. What a better present
> adds there is a lead that stays fixed.

---

## 5.6 Three kinds of comparison

**Two developments can differ in their starts, in the policy a controller
follows, or in the law. Only the second is a choice from one present.**

[Definition A.3.6](#a-3-6) names three ways two developments can differ.

| Kind | What differs | Example | What it can show |
|---|---|---|---|
| **Preparation** | the present, under one law | the full tank and the empty one (5.5) | an offset only, when every start settles into the same closed class |
| **Process** | the policy, in one controlled model | acting now and building first (5.3) | a difference in rate as well as offset |
| **Mechanism** | the law | the robust machine and the fragile one (5.4) | a difference in rate as well as offset |

The profile is computed the same way in all three, but they are different
kinds of evidence.
- **A process comparison is a choice.** Both policies are physically
  available from one present, with their implementation and costs inside the
  model. The options an agent faces, and the tests of the central thesis, are
  comparisons of this kind ([chapter 12](#chapter-12)).
- **A preparation comparison sets two presents side by side.** The full and
  empty tanks are not two options open to one engine. They show what a
  difference in starting state is worth under one law.
- **A mechanism comparison sets two laws side by side.** The robust and
  fragile machines isolate what failure without repair does. A rate
  advantage found this way is a contrast between laws, not evidence that one
  start under a single law is better than another.

Chapters [13](#chapter-13) to [16](#chapter-16) keep the three apart.

---

## 5.7 What the profile gives the rest of the manuscript

- **Persistence.** When a regime ends at a random time, its ending and what
  follows belong to the history law, and the profile of the whole law
  converges. [Chapter 6](#chapter-6) gives its limit, the worth of lasting
  and the cost of an early end.
- **Harm.** A narrowing is a negative profile. Whether it is an offset or a
  rate narrowing decides whether it can be outgrown
  ([chapter 17](#chapter-17)).
- **Resolution.** The profile is read at a declared resolution.
  [Chapter 7](#chapter-7) asks which governs.
- **Decision.** A bounded agent reads the profile to the horizon it can
  resolve, and bounds the rest ([chapter 24](#chapter-24)).

---

## 5.8 What this chapter does not claim

- **That organization raises the rate.** Section 5.5 shows that within one
  closed class it cannot. Whether it does by the routes the theorem excludes
  is tested in [chapters 13](#chapter-13) and [15](#chapter-15).
- **That every profile has a slope and a level.** Where the state space grows
  or the law changes, the profile itself is the object.
- **That a finite horizon gives the verdict.** It gives a reading, which can
  reverse, as both worked examples show.
- **That a faster rate is good.** The profile is a description of Omega. That
  what we recognize as good corresponds to widening the whole field is the
  central thesis ([chapter 11](#chapter-11)).

---

## Status of chapter 5

| Status | Claims |
|---|---|
| **D** (definitions) | profile (5.1); rate, offset (5.2); crossover horizon (5.3); preparation, process and mechanism comparisons, and which of them is a choice from one present (5.6) |
| **T** (results, under their stated assumptions) | rate and offset exist for every finite kernel ([Definition A.3.1](#a-3-1); [Lemma A.3.2](#a-3-2)); the rate–offset identity ([Theorem A.3.3](#a-3-3), proved here); where the rate comes from ([Corollary A.3.4](#a-3-4), proved here); the offset theorem ([Theorem A.3.5](#a-3-5), proved here); the crossover horizon and its bound ([Proposition A.3.7](#a-3-7), proved here); rate outweighs offset ([Corollary A.3.8](#a-3-8), proved here); the profile and the verdict over everything that follows ([Corollary A.3.9](#a-3-9), proved here); the ordering coincides with the overtaking criterion and the gain-then-bias ordering, cited (5.4) |
| **M** | none; Examples 5.1–5.3 are exact computations in specified finite models, illustrating the theorems |
| **E** | none |
| **N** | none |
| **C** | none asserted; whether organization escapes the offset theorem is tested in chapters 13 and 15 |
| **Open** | the profile as the object where rate and offset do not exist (5.4); a single verdict for open-ended fields (Appendix A, section A.15) |

## References cited in chapter 5

*Collected with full details in Appendix G.* Entries marked "to verify" are
not yet checked against their sources.

- Kemeny, J. G., and Snell, J. L. (1960). *Finite Markov Chains.* Princeton:
  Van Nostrand. To verify.
- Levin, D. A., Peres, Y., and Wilmer, E. L. (2009). *Markov Chains and Mixing
  Times.* Providence: American Mathematical Society. To verify.
- Norris, J. R. (1997). *Markov Chains.* Cambridge: Cambridge University
  Press. To verify.
- Veinott, A. F. (1966). On finding optimal policies in discrete dynamic
  programming with no discounting. *Annals of Mathematical Statistics* 37,
  1284–1294. To verify.
- von Weizsäcker, C. C. (1965). Existence of optimal programs of accumulation
  for an infinite time horizon. *Review of Economic Studies* 32(2), 85–104.
  To verify.
