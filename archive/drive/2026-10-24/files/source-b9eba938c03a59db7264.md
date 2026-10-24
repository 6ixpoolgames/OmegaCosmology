# Appendix C. Test-bed models: methods and catalogue

> **Drafting note (r4, 23 October).**
> - Ruling 79: the rule states matched resolution and that the finer level
>   governs once shown faithful. Every cadence reversal (C.3, C.4, C.11,
>   C.12, C.14) is a resolution-dependent reversal, not a correction: no
>   model's faithful cadence has been established. The methods: the finest
>   cadence tested gives provisional rankings.

> **Drafting note (r3, 23 October).**
> - Timing, after chapter 7 r2 and Appendix A r17 (ruling 76): what counts
>   is the timing information a system's records can register; a sharp floor
>   on cadence is one possible result, not an assumption, and a reading made
>   by a physical recorder is part of the development, not a finer
>   description of it. The methods' timing bullet is rewritten; no
>   entry changes.

> **Drafting note (r2, 19 October).**
> - **The governing level of detail** (rulings 51 and 52): of two faithful
>   descriptions, the finer governs; coarser rankings are certified,
>   corrected or provisional (Definition A.6.5, Proposition A.6.6). The
>   methods state the rule, and every entry reports its ranking at the finest
>   level tested, with its tier from Appendix D r3.
> - **The pending decisions of r1 are settled** and the markers removed. Paid
>   neutral variation and the register chain hold at the governing level
>   (M1); paid sensing is M1, its one exception corrected at finer cadences;
>   dependence and channels are M2; the blocking result, domination against
>   production (T256 and T1024) and directional flow are M1.
> - **Corrections at the finest cadence** are stated in models C.3, C.11 and
>   C.12, with the note that a finer cadence favours the option with more
>   events (Corollary A.6.4).
> - Model C.6 cites Corollary A.6.4 for the fine-cadence limit.

> **Drafting note (r1, 19 October).**
> - First draft, built from the test-bed records at commit dacb9e3, read study
>   by study, with recounts from the compact maps where a report did not state
>   a count (script: analysis/testbed_recounts/recount_appendix_c.py).
> - Models C.1–C.17; the methods sections are unnumbered, so that "model C.n
>   (Appendix C)" names a model and nothing else. Three anchors were added to
>   the fourteen used by Appendix D r2: `#c-corrected-catalysis`,
>   `#c-reserve` and `#c-opportunity`.
> - The table of records sits at the end of this appendix and can move to
>   Appendix H.
> - Eight tier decisions were put to the originator and settled in r2.

This appendix describes how the test-bed models are built and computed, and
then catalogues them, one entry per model. Each entry gives the question the
model asks, its setup, what its comparisons match and what they do not, the
levels of detail tested, the key figures, how far each ranking holds, and its
scope. Every model result in the manuscript (status M) cites an entry here,
and [Appendix D](#appendix-d) assigns its tier. Nothing here is a verdict on
the thesis: the models show what a declared law does at a declared
resolution, and [chapter 12](#chapter-12) sets the conditions under which that
bears on the thesis at all.

---

## Methods common to every model

**Every model is a finite continuous-time Markov chain on a declared full
state. The whole field's log lushness is computed exactly at a declared
resolution; a party's is bounded.**

### Construction

- **The state.** Each model declares a full state that suffices to predict
  its future: material and energy stores, apparatus and its condition,
  carriers and their charge, gates, controller settings, and the state of
  the boundary. Relations enter only through the law. A label such as
  "cooperative" or "damaged" changes nothing unless the transition rates
  depend on it.
- **The law.** Elementary transitions are declared with their preconditions,
  results, rates and resource exchanges, and aggregated into a generator Q.
  Duplicate descriptions of one physical outcome are summed before any entropy
  is computed. Reaction labels and rule identifiers add no alternatives.
- **Two construction routes.** The first fixtures were written as rules in
  BioNetGen (Harris et al. 2016; Python distribution 0.8.7, engine 2.9.3) and
  converted to the joint-state generator, with volume and symmetry factors
  applied once. Every generated generator matched an independent hand
  construction. Later models enumerate their states and build the generator
  directly from declared rules.
- **Physical checks.** The reports check that, with every source and driven
  boundary switched off, the native reversible chemistry satisfies detailed
  balance (the dark check). Sources,
  friction devices, external affinities and irreversible damage are explicit
  driven boundaries, and each appears in a first-law ledger that closes.
- **Costs.** Every operation declares what it uses: material, energy, time,
  occupied apparatus and wear. No penalty is subtracted from the measure for a
  cost; a cost acts only through the futures it changes.

### Computing lushness

For a cadence δ, the transition law between observations is the matrix
exponential of the generator, not a first-order approximation.

> \[
> P_\delta=\exp(\delta Q).
> \]
>
> *In words:* the probability of moving from one full state to another over
> one observation interval is computed exactly from the rates.

Log lushness from a known present x₀ over n observations, T = nδ, is the
entropy of the complete sequence of observed states, by the chain rule
([Theorem A.2.1](#a-2-1)).

> \[
> g_\delta(x)=-\sum_y P_\delta(x,y)\log_2 P_\delta(x,y),\qquad
> \ell_n(x_0)=\sum_{j=0}^{n-1}\bigl[P_\delta^{\,j}\,g_\delta\bigr](x_0).
> \]
>
> *In words:* the uncertainty of each next observation is averaged over where
> the history may be by then, and these are added over the whole horizon.

- **Numerics.** P_δ is applied through uniformization (sampled Poisson
  vectors); dense kernels are not stored for the larger models. Each study
  reports its largest probability, energy and Poisson residuals; across the
  catalogue they lie between about 10⁻¹⁶ and 2 × 10⁻⁹ bits or units.
- **Rate and offset.** Where a limit exists, each development has a rate h
  and an offset b ([Definition A.3.1](#a-3-1)), and two developments cross
  near T× = −Δb/Δh ([Proposition A.3.7](#a-3-7)). Closed classes are
  inspected before a rate is reported. Starts within one irreducible law share
  a rate ([Theorem A.3.5](#a-3-5)). The finite profile is the primary output;
  the rate says whether a difference keeps growing.
- **Exact finite probes.** Where a crossover matters, it is located by
  computing the finite profile on both sides of the estimate, not inferred
  from T×.
- **What is not counted.** Solver null events, the entropy of choosing a
  starting state, and rule labels. A reference that is a mixture of starting
  states is reported as the average of its members' conditional log
  lushness.

### Levels of detail

- **Cadence.** Most studies use δ = 0.125, 0.25 and 0.5, with 0.25 primary.
  One calibration runs from 0.5 down to 1/512 (model C.13). A finer solver
  step is a convergence check, not a new cadence.
- **Grain.** Each model declares its grain: counts of apparatus and stores
  (most models); sites, bonds and carrier (model C.3); a register read or
  merged (model C.13); the step of a bank's energy grid (model C.14).
- **Horizon.** Most profiles run to T1024; some to T4096. Horizon is not a
  level of detail: a ranking is stated at a horizon, and the profile shows
  how it changes with the horizon.
- **The rule.** Options are compared at one level of detail. Of two
  faithful levels, the finer governs once its extra detail is shown
  faithful. A ranking holds when it is resolved at the level that governs,
  either computed there or certified from a coarser level
  ([chapter 12, section 12.5](#chapter-12); [Definition A.6.5](#a-6-5);
  [Proposition A.6.6](#a-6-6)). A ranking that a finer level shown faithful
  reverses is corrected, and the coarser result is kept as evidence of where
  the difference comes from. Where the finer level's faithfulness is open,
  as for every cadence so far, the reversal is resolution-dependent and both
  results are reported. Cadence robustness is not grain robustness.
- **Timing.** A finer cadence favours the option with more events
  ([Corollary A.6.4](#a-6-4)). Timing distinctions count only as far as the
  model's own records can register them; whether that gives a sharp floor or
  a bounded amount of timing information is a property of each model, to be
  derived (Definition A.6.5; chapter 7). No model has yet derived it, so in
  every entry the finest cadence tested gives provisional rankings. The models
  read their chains passively; none implements its records as a physical
  apparatus.

### Subjects

A party's history is a projection of the full state and is generally not
Markov. Its log lushness is bounded, not computed, with the bounds of
[Theorem A.7.3](#a-7-3): a lower bound that adds the full state some steps
back, and an upper bound that uses the party's own recent states. The
difference between two options is an interval, from the lower bound of one
less the upper bound of the other to the reverse. A difference is resolved
when its interval excludes zero ([Definition A.7.4](#a-7-4)); otherwise it is
unresolved, which is not a tie. No midpoint of an interval is used to rank.

### Controllers and policies

- **Oracle layer only.** Every controller in this catalogue is a fixed policy
  table, chosen by exhaustive search over a declared finite family with full
  knowledge of the law ([chapter 12, section 12.3](#chapter-12)). Executing
  it is physical: gates, fuel debits and reverse channels are in the law. The
  design search happens outside the modelled world. No bounded-agent model
  has been built ([Appendix D, section D.4](#appendix-d)).
- **Families.** Each search names its family: for example 1,296 pairs of
  local response tables (model C.9), or 22 constant and reserve-sensitive
  policies (models C.11 and C.12). A winner is the best in its family, not
  over all controllers. Ties are kept.

### Physical accounts

Every comparison reports, beside the profile, the physical readouts that
explain it: energy and material ledgers by family, accepted external work,
captured energy and funding fractions, expected numbers of events, functioning
apparatus, closure and loss probabilities. Matching is declared comparison by
comparison. Unless an entry says otherwise, inventory, source prescription,
bath and starting energy are matched; accepted work, activity and realized
fuel are not.

### Reproducibility

- **Frozen before ranking.** Each scientific batch runs from a protocol
  frozen, with a hash of its inputs, after a capped engineering run and
  before any ranking is computed. Predictions are registered with their pass
  and fail criteria. Failed predictions and adverse results are kept.
- **Caps.** Wall time, memory and output are capped per job (by default
  120 s, 1 GiB and 256 MiB; up to 600 s in the larger studies). A capped run
  is a status, not a score.
- **Independent checks.** The early fixtures compared sampled trajectories
  from a direct stochastic simulation algorithm (Gillespie 1977) and from
  BioNetGen's own sampler against the exact law.
- **What is kept.** Frozen sources, configurations, compact results and
  receipts are versioned; raw runs stay local. The records of each model are
  listed at the end of this appendix.

### What the methods do not settle

- **The finest faithful resolution.** No study derives its finest faithful
  cadence or grain from physics. Each entry records the levels tested, and
  the finest of them gives provisional rankings until that is done.
- **Physical realism.** The models are toy constitutive laws. Count models
  have no positions; driven controllers are coarse boundaries, not reversible
  chemical implementations.
- **Subjects.** The parties in the multi-subject models are functional
  apparatus and controller channels. They are projections that satisfy
  [Definition A.7.1](#a-7-1); nothing in the models establishes experience.

---

## How each entry reads

Each entry has the same parts.
- **Question:** what the model asks, and which chapters and rows of
  [Appendix D](#appendix-d) it serves.
- **Setup and comparison:** the world, the options, and what is matched.
- **Levels tested:** cadences, grains and horizons actually run. The finest
  faithful level has not been derived for any model.
- **Key figures:** differences are in bits of log lushness, rates in bits per
  unit time; positive favours the first-named option.
- **How far it holds:** the ranking at the finest level tested, what coarser
  levels show, and the tier from Appendix D.
- **Scope:** what the model does not show.

---

## The catalogue

### Organization against disorder ([chapter 13](#chapter-13))

#### Model C.1. Locked source

**Anchor** `#c-locked-source`. Serves [chapter 13](#chapter-13) and Appendix
D, section D.3.1.

**Question.** Does a law under which organization can release a locked
resource open futures that the same law without that path does not?

**Setup and comparison.**
- A 16-state count model: a locked resource, apparatus and its precursor, and
  a charged or spent carrier. Working apparatus can release the resource
  through a paid route, and released resource has a downstream use.
- Two laws: the capable law, and the same law with the paid route removed.
  One recurrent class of 16 states in each.
- Within the capable law, an organized start and an unorganized start of
  equal energy (2.5).
- Boundary prescriptions are matched. Accepted throughput and work are not:
  the capable law takes in more external work.

**Levels tested.** Cadences 0.125, 0.25 and 0.5 at the full 16-state grain;
profiles to T64 at cadence 0.25.

**Key figures.**

| Readout | 0.125 | 0.25 | 0.5 |
|---|---:|---:|---:|
| Capable minus route-removed, rate | +0.260024 | +0.228729 | +0.196984 |
| Organized and unorganized starts, rate (each) | 0.622120 | 0.554748 | 0.486442 |

| Horizon (cadence 0.25) | T1 | T4 | T16 | T64 |
|---|---:|---:|---:|---:|
| Capable minus route-removed | +0.018 | +0.275 | +2.921 | +16.160 |
| Organized minus unorganized start, capable law | +0.264 | +1.124 | +4.583 | +10.852 |

- The paid route is used: stationary flux 0.007729 per unit time; downstream
  use 0.025331 against 0.007475 without the route.
- Apparatus works 76.4% of the time under the capable law and 87.0% without
  the route. Net boundary work is 0.010832 against 0.000338 energy per unit
  time.

**How far it holds.** The rate contrast has the same sign at all three
cadences. The two starts tie in rate at every cadence, as
[Theorem A.3.5](#a-3-5) requires. Tier M1.

**Scope.**
- An access and throughput model. Downstream use regenerates neither
  apparatus nor carrier, so there is no feedback, and apparatus is available
  less of the time under the capable law.
- The capable law accepts more external work, so the advantage is one of
  access and throughput together.
- Pending: a cleaner removal that keeps the locked resource present with its
  own dynamics.

#### Model C.2. Catalysis with a basal route

**Anchor** `#c-corrected-catalysis`. Serves [chapter 13](#chapter-13). Not
yet in Appendix D; proposed for section D.3.1.

**Question.** When apparatus speeds a feedback route that is also open, more
slowly, without it, does an organized start lead an unorganized start of equal
energy, and does the acceleration raise the rate?

**Setup and comparison.**
- The same kind of count model as model C.1, with apparatus capacity 1 (16
  states) or 2 (36 states).
- The feedback coefficient is 0.002 + 0.04a, where a is the working
  apparatus, and it applies to both directions of the route. With no
  apparatus the route stays open at the basal rate.
- Two comparisons: organized against unorganized start under one law (a
  preparation comparison); the law with acceleration against the basal-only
  law (a mechanism comparison).
- This model replaces the earlier control that kept the coupling at the full
  rate with no apparatus at all. That control was a more permissive law and is
  kept as a diagnostic ([Appendix H](#appendix-h)).

**Levels tested.** Cadences 0.125, 0.25 and 0.5; profiles to T256.

**Key figures.**

| Capacity | Cadence | Organized minus unorganized, T64 | Acceleration minus basal only, rate |
|---:|---:|---:|---:|
| 1 | 0.125 | +5.696 | +0.002267 |
| 1 | 0.25 | +5.094 | +0.001964 |
| 1 | 0.5 | +4.473 | +0.001640 |
| 2 | 0.125 | +7.787 | +0.010847 |
| 2 | 0.25 | +6.834 | +0.009250 |
| 2 | 0.5 | +5.858 | +0.007550 |

The organized start trails early and leads later. At capacity 1 and cadence
0.25 the difference is −0.477, −1.348 and −0.988 at T1, T4 and T16, then
+5.094 at T64 and +9.594 at T256. At capacity 2 it is positive from T16.

**How far it holds.** All four registered predictions passed. Both
comparisons keep their sign across the three cadences at T64 and beyond. The
two starts share a rate within each law, so the lead is an offset.

**Scope.** A small mechanism model. The rate increments are small (0.0016 to
0.0108 bits per unit time); the preparation lead is finite.

#### Model C.3. Reactive lattice

**Anchor** `#c-lattice`. Serves [chapters 13](#chapter-13) and
[31](#chapter-31), and Appendix D, section D.6 (operating range).

**Question.** On a lattice with positions, does an organized seed lead
naturally evolving matter of the same energy under the same law?

**Setup and comparison.**
- A periodic ring of sites with monomers, nearest-neighbour bonds, one mobile
  carrier with charge 0, 1 or 2, and a resource packet at one site. Paid
  joining, catalysed by nearby bonds, consumes two charge units; capture
  needs the carrier at the source with zero charge. Bonded clusters move at
  half the monomer rate.
- Fourteen laws: six monomers on seven sites (3,822 states) at inverse
  temperatures 0.5, 1.5 and 3, mobilities 0.25 and 1, with native or weak
  assistance; and four monomers on six sites at one setting, native or weak.
- A seed with one bond, against three references of equal energy under one
  generator: the thermal mixture on the energy shell; the shell with no
  bonds (the unbound start); and random placement with the seed's bond
  count.

**Levels tested.** Cadences 0.125, 0.25 and 0.5 at the site, bond and carrier
grain; horizons T16 to T1024, extended to T4096 for every law, where the
remaining tail is below 10⁻³ bits.

**Key figures.**

| Reference | Seed ahead, T64, cadence 0.25 | Seed ahead, T4096, cadence 0.25 | Seed behind, T4096, cadence 0.25 | Seed ahead at all three cadences, T4096 |
|---|---:|---:|---:|---:|
| Thermal mixture | 12 of 14 | 12 | 2 | 12 |
| Unbound start | 3 of 14 | 0 | 14 | 0 |
| Random placement | 6 of 14 | 3 | 11 | 3 |

- Against the unbound start at T4096, the seed is behind at all three
  cadences in 12 laws, and 2 change sign. These are the
  native-assistance, mobility-0.25 laws at inverse temperatures 1.5 and 3.
  For the second (the registered target case), the differences at T4096 are
  −14.674, −3.792 and +7.744 at cadences 0.125, 0.25 and 0.5. At T64 and
  cadence 0.25 it led by +7.628; by T1024 it trailed by 3.655.
- Across the first map, 19 of 168 law, reference and horizon comparisons
  change sign across cadences.
- The thermal reference is dense: 1.54 bonds on average, and 92.3% of its
  mass already holds a bond.

**How far it holds.** An operating range, with no verdict on the principle
(Appendix D, section D.6). Against the unbound start at T4096 the seed is
behind at the finest cadence tested in all 14 laws, and at every cadence in
12. The two laws in which it leads at cadence 0.5 reverse at the finer
cadences, a resolution-dependent reversal.

**Scope.**
- One carrier of charge capacity 2 and one packet make a charge and transport
  bottleneck. The upkeep channel does not lower a bond's hazard.
- The implemented feedback does not sustain the seed's early assembly: every
  start converges to the same low-assembly stationary law.
- Each law is finite and irreducible, so every lead becomes an offset.
- Pending: a sweep of mobility and contact coefficients. A world of six
  monomers on eight sites needs a streaming backend.

### Information and action ([chapter 14](#chapter-14))

#### Model C.4. Paid sensing

**Anchor** `#c-paid-sensing`. Serves [chapter 14](#chapter-14) and Appendix
D, section D.3.2.

**Question.** Does a register that tracks the world score above one that
varies at random, with and without the means to act on it?

**Setup and comparison.**
- A mortal valuer with stochastic resource patches, an energy store and a
  powered register bit. Expected life is about 6.9 time units.
- Four mechanisms, sharing the resource law, read clock, unit bills, bit
  relaxation and mobility:
  - **I** writes the bit from the patch cue (empty or full); **R** writes it
    independently of the stock;
  - **X** couples movement to the bit; **0** keeps only basal movement.
- Sixteen preparations per contrast, pooled in eight groups. Occupancy and
  activation were calibrated at zero coupling before ranking; the bills after
  coupling are not matched.

**Levels tested.** Cadences 0.125, 0.25 and 0.5; horizons T16, T64 and T256;
non-Markov bounds for the hidden bit.

**Key figures** (counts of the 16 preparations, recount over all levels).

| Contrast | T64, cadence 0.25 | All nine cadence and horizon cells |
|---|---|---|
| I0 − R0: information without action | 0 positive, 16 negative | 143 of 144 negative; one positive (+0.004, cadence 0.5, T16) |
| RX − R0: random action | 1 positive, 15 negative | 15 of 16 negative in every cell |
| IX − RX: informed against random action | 9 positive, 7 negative | 9 or 10 positive in every cell |

- The uncoupled random register R0 wins 14 of 16 preparations; IX wins 2.
- The information term of actuation (informed minus random, with and without
  the coupling) is positive in all eight pooled groups; +0.415 at the target
  setting, where IX − RX is +0.195.
- All mechanisms share one limiting rate within each law (spread below
  4 × 10⁻¹⁵), so every difference is a finite offset.
- Write information: 0.108 to 0.402 bits per read for the informative
  writer, zero for the other.

**How far it holds.** Information without action loses in all 16
preparations at every horizon at the finest cadence tested. The one
exception, at the coarsest cadence and T16, reverses at the finer cadences,
a resolution-dependent reversal. Tier M1.

**Scope.** A finite-life model. Expected life is far shorter than the
repayment horizons of model C.5, and the sensor reads an immediate cue, not
future replenishment.

#### Model C.5. Paid renewal

**Anchor** `#c-paid-renewal`. Serves [chapter 14](#chapter-14) and Appendix
D, section D.3.2.

**Question.** Where information can be used to act, and the apparatus that
uses it can be rebuilt, does informed action earn a higher rate, and when does
that rate repay its cost?

**Setup and comparison.**
- The four mechanisms of model C.4 (IX, I0, RX, R0) in a maintained world,
  where apparatus wears and is renewed by paid and thermal construction.
- Nineteen laws: capacity 1 with self-maintenance (five supplies, two wear
  levels), capacity 2 with construction assisted by existing apparatus
  (three supplies), and ablations of repair and of construction assistance.
  Two starts per law, pooled.
- The wear coefficient multiplies both thermal disassembly and thermal
  assembly, so higher wear means faster turnover, not only more damage.

**Levels tested.** Cadences 0.125, 0.25 and 0.5; horizons T16 to T1024, with
exact probes to T4096.

**Key figures.**

| Contrast, limiting rate (recount) | Positive | Negative |
|---|---:|---:|
| IX − R0 | 57 | 0 |
| IX − RX: informed against random action | 57 | 0 |
| IX − I0: action given information | 57 | 0 |
| I0 − R0: information alone, against the uncoupled random register | 0 | 57 |
| RX − R0: action alone, against the uncoupled random register | 0 | 57 |

Counts are 19 laws by 3 cadences.

| Horizon (cadence 0.25) | T16 | T64 | T256 | T1024 |
|---|---:|---:|---:|---:|
| Laws in which IX is the best of the four | 0 | 0 | 5 | 13 |

| Capacity 2, supply | IX − R0 rate | IX − R0 at T1024 | Estimated repayment horizon |
|---:|---:|---:|---:|
| 0.3 | +0.005146 | +0.751 | 878.7 |
| 0.6 | +0.010079 | +5.746 | 453.9 |
| 1.2 | +0.018270 | +14.693 | 219.8 |

- The repayment horizon is the crossover estimate T× = −Δb/Δh
  ([Proposition A.3.7](#a-3-7)), not an exact crossing.
- Every pooled IX − R0 sign agrees across the three cadences at each horizon.
- The four registered predictions at T64 failed: the gain arrives later.
- Construction assisted by existing apparatus raises the informed rate by
  0.032 to 0.071, through construction turnover rather than retained
  expansion.
- In the low-turnover capacity-1 laws, gross hardware return is 3.0 to 8.7
  times hardware spending, but captured energy covers only 30% to 68% of the
  full running-cost ledger.

**How far it holds.** The rate ordering holds in all 57 law and cadence
cases. Tier M1. The advantage needs information and action together, the
split of [Proposition A.8.3](#a-8-3).

**Scope.** The maintained source supports the limiting-rate analysis; finite
opportunity windows are not modelled. Damage is not separated from basal
assembly.

### Persistence and compounding ([chapters 15](#chapter-15) and [16](#chapter-16))

#### Model C.6. Capacity loop

**Anchor** `#c-capacity`. Serves [chapters 15](#chapter-15),
[16](#chapter-16) and [31](#chapter-31), and Appendix D, sections D.3.3 and
D.5.1.

**Question.** Does a resource-funded enabling loop retain its apparatus, and
does its rate rise with capacity?

**Setup and comparison.**
- A count model. Each built unit raises the propensity of capture and, until
  crowding, of building the next unit. Paid construction spends bank energy
  and precursors, and its thermodynamic reverse is kept. Damage returns
  material to precursor.
- Twenty-four laws: capacity 4, 8, 16 and 32 at the central cost and yield,
  and a grid of three costs by three yields at capacity 8; damage 0.005 or
  0.02.
- The full loop against three ablations: no construction assistance, no
  capture assistance, and the basal law with both couplings removed. A seed
  and an unorganized start share each law.

**Levels tested.** Cadences 0.125, 0.25 and 0.5; horizons T16 to T1024; 1,728
comparisons.

**Key figures** (central cost and yield, damage 0.005).

| Capacity | Retained apparatus, loop | No construction assistance | No capture assistance | Loop − basal rate, cadence 0.25 | Captured share of funding |
|---:|---:|---:|---:|---:|---:|
| 4 | 3.939 | 1.033 | 0.110 | +2.373 | 98.5% |
| 8 | 7.948 | 2.115 | 0.128 | +3.436 | 96.6% |
| 16 | 15.892 | 4.295 | 0.150 | +4.731 | 89.8% |
| 32 | 30.785 | 8.422 | 0.183 | +6.649 | 68.2% |

- The ablations retain at most 27% of capacity without construction
  assistance and under 3% without capture assistance.
- Loop − basal rate at capacity 4 to 32: +2.96 to +8.82 at cadence 0.125,
  +1.79 to +4.71 at cadence 0.5.
- At capacity 8, at least two units are present 99.994% of the time, and net
  paid creation is 0.0424 units per unit time.
- **At a fixed number of events** the loop trails at first: −1.762 at 8
  jumps, then +9.190 at 32 and +72.724 at 128. Its jump sequence is also less
  predictable: 1.051 bits per jump against 0.384 for the basal law.
- The stationary funding fractions (capture, recycled hardware, bath imports)
  sum to one, so a target of "funding above one" is ill-posed.

**How far it holds.** All 1,728 comparisons favour the full loop; no sign
changes with cadence. Tier M1. The loop leads in both event count and
event-path entropy, so by [Corollary A.6.4](#a-6-4) it leads at every
sufficiently fine cadence; cadences between the grid and that limit are not
checked.

**Scope.** Bounded growth in a finite inventory. The basal law is a coupling
ablation, not a gas. Within one law the seed and the unorganized start share
the rate.

#### Model C.7. Matched work

**Anchor** `#c-matched-work`. Serves [chapter 15](#chapter-15) and
Appendix D, section D.3.3.

**Question.** Does the enabling relation add futures that a non-enabling
process taking in the same external work does not?

**Setup and comparison.** The law of model C.6 with source rates calibrated,
before any ranking, so that the loop and the basal law accept the same
stationary external work. Twelve points: three work targets at each of four
capacities. Captured energy, bath energy, cumulative finite work and activity
are not matched; the basal law can accept packets and lose them unused.

**Levels tested.** Cadences 0.125, 0.25 and 0.5; primary horizon T64.

**Key figures.**
- Loop − basal rate positive at all 12 points and all three cadences; at
  cadence 0.25 it runs from +0.013 to +0.274.
- The seed comparison favours the loop at all 12 points at T64 and cadence
  0.25.
- Captured energy funds 90.0% to 94.7% of the loop's spending.
- Retained apparatus is 0.09 to 0.22 at the lowest work target and 1.26 to
  1.50 at the highest, so a sustained gain can come with sparse, intermittent
  apparatus.
- Largest mismatch in accepted work: 5.8 × 10⁻¹⁴.

**How far it holds.** No sign changes. Tier M1.

**Scope.** Work is matched, activity is not ([Appendix D, section
D.5.1](#appendix-d)). This model does not answer the activity-matched test.

#### Model C.8. Three-link compounding

**Anchor** `#c-compounding`. Serves [chapters 15](#chapter-15),
[17](#chapter-17), [31](#chapter-31) and [32](#chapter-32), and Appendix D,
sections D.3.3, D.5.2 and D.6.

**Question.** Can successive paid enabling links compound, persist and raise
lushness, and how does damage change that?

**Setup and comparison.**
- Three apparatus types in a cycle: A assists the construction of B, B of C,
  and C of A. Apparatus also enables capture, which helps pay for further
  construction. A lineage monitor reads chains without adding entropy; it can
  miss real chains, so completions are lower bounds.
- **Shape grid:** feedback exponent 0.5 (square root) or 1 (linear),
  assistance scale 0.1 or 1, source 0.15, 0.6 or 2.4 (12 settings).
- **Stress grid:** four anchors (exponent by source 0.15 or 0.6) under seven
  stresses: total damage 0.005, 0.02 or 0.08; at damage 0.02, an irreversible
  fraction of 5% or 25%; and a pulse that removes one B at T64, with or
  without the 5% fraction.
- Forty setting rows (four reuse shape cases). The full mechanism against all
  assistance off, the C-to-A link cut, and single-link ablations. Starts: a
  seed with one apparatus, an unbound start, and a thermal count preparation
  of equal energy.

**Levels tested.** Cadences 0.125, 0.25 and 0.5; horizons to T256 for every
setting, to T4096 for the irreversibility contrasts.

**Key figures.**

| Linear feedback, full assistance, source 2.4 | |
|---|---:|
| Three-link completion by T256 | 16.24% |
| Completion with retained expansion at T256 | 11.08% |
| Functional uptime over T64–T256 | 55.10% |
| Full minus unbound start, T256, cadence 0.25 | +164.95 |
| Full minus all assistance off | +366.27 |
| Full minus C-to-A cut | +152.25 |

- Three links with retained expansion occur with probability above 1% in all
  12 shape settings, square-root feedback included.
- At T256 the full mechanism beats the unbound start, all assistance off and
  the cut loop in all 40 rows, at all three cadences.
- Cutting any single construction link lowers retained expansion, measured
  without the monitor's labels.
- **Uptime.** At sources 0.6 and 2.4, functional uptime over T64–T256 runs
  from 46.6% to 55.1%, above one half in four shape settings. No setting in
  the shape grid closes by T256.
- **Funding.** At the setting in the table, external capture pays at least
  75.4% of spending by T256, 87.7% by T1024 and 92.7% by T4096.
- **Damage** (linear feedback, source 0.6). Raising damage from 0.005 to 0.02
  and 0.08 lowers uptime from 0.504 to 0.113 and 0.001, and three links with
  retained expansion from 0.100 to 0.0088 and 0.0000078.
- Uptime and the lushness advantage rank together across the stress groups
  (Spearman 0.82 to 1.0).
- The thermal preparation beats the seed in all 40 rows. It starts with 4.26
  units of apparatus on average and a complete loop with probability 47%.

**Permanent loss.** Raising the irreversible fraction of the same total damage,
from none to 5% or from 5% to 25%, gives eight contrasts across the four
anchors. Four of them raise T256 log lushness at all three cadences while
lowering uptime: both steps at source 0.15, for both exponents. At source 0.6
both steps lower it by T256.

| Exponent 0.5, source 0.15, cadence 0.25 | T16 | T64 | T256 | T1024 | T4096 |
|---|---:|---:|---:|---:|---:|
| 5% irreversible minus repairable | +0.190 | +0.684 | +1.168 | +1.169 | −2.460 |
| 25% irreversible minus 5% | +0.359 | +1.253 | +1.238 | −1.749 | −37.500 |

**How far it holds.** The mechanism and lushness rows hold at every cadence
tested. Tier M1 for both. Uptime is a physical readout, the same at every
cadence; its range is stated above.

**Scope.** Count chemistry with no positions. Finite depth. The permanent-loss
contrasts compare laws, not choices. The heavy-damage results are an
operating range (Appendix D, section D.6).

### Harm and protection ([chapters 17](#chapter-17) and [18](#chapter-18))

#### Model C.9. Channels

**Anchor** `#c-channels`. Serves [chapters 18](#chapter-18) and
[31](#chapter-31), and Appendix D, section D.3.4.

**Question.** Does the policy that keeps the most open protect stock, or the
channels through which futures open?

**Setup and comparison.**
- Two compartments, each with apparatus (precursor, worn or active), a
  carrier (empty or charged) and a gate that routes the carrier to service or
  exchange. Each compartment's controller has a response when its apparatus
  is inactive and one when active.
- **First fixture:** 144 states. Each response is a bias towards exchange of
  0, 0.5 or 1, giving 81 response pairs.
- **Extension:** responses chosen from idle, service, exchange and three
  mixtures. The benefit of active capture is set at 1, 3, 6 and 12 times
  basal; 1,296 response pairs per setting, 81 of them deterministic or idle.
  Every switch pays its fuel debit and keeps its reverse channel.
- Reference: the uniform ensemble of all eight energy-4 states, with both
  gates at service, propagated state by state. Matter, hardware, energy,
  temperature and clock are matched.

**Levels tested.** First fixture: the same unique winner at all three
cadences and two common-speed settings. Extension: complete search at
cadence 0.25; at cadences 0.125 and 0.5 only the selected candidates were
evaluated, and the winner stays best among them at every setting.

**Key figures** (extension).

| Capture benefit | Winning responses (inactive, active) | Rate | Active apparatus, winner | Active apparatus, service-biased control | Difference | Organized − shell offset |
|---:|---|---:|---:|---:|---:|---:|
| 1 | service, 25% exchange | 5.366 | 0.602 | 0.632 | 4.79% fewer | +6.36 |
| 3 | service, 50% exchange | 5.717 | 0.721 | 0.790 | 8.75% fewer | +7.17 |
| 6 | service, 50% exchange | 6.086 | 0.833 | 0.918 | 9.21% fewer | +8.33 |
| 12 | service, 50% exchange | 6.498 | 0.952 | 1.035 | 7.93% fewer | +9.47 |

- The policy that keeps the most apparatus working is all idle, with gates
  left at service (0.66 to 1.08 active units). Its rate is 4.74 to 5.03,
  against 5.37 to 6.50 for the winner.
- The winner's rate exceeds the best deterministic policy's by 0.072 to
  0.633.
- The organized start leads the shell in all 5,184 finite comparisons at each
  setting. At benefit 12, some policies (not the winner) give the organized
  start a negative long-run offset.
- A diagnostic of predictive retention selects other candidates at longer
  lags; its values at lag 64 are of order 10⁻⁶ bits.

**How far it holds.** The winner is service-biased when inactive and keeps
fewer active units than the service-biased control at every setting. Tier
M2, since the complete search ran at one cadence.

**Scope.** Four slots; an externally maintained chemical boundary. The
count of productive configurations against their non-conducting arm cited in
Appendix D is not in the archive (see "Records not in the test-bed archive").

#### Model C.10. Dependence

**Anchor** `#c-dependence`. Serves [chapter 18](#chapter-18) and Appendix
D, section D.3.4.

**Question.** When switching the controller requires working apparatus, does
keeping the apparatus working become the policy that keeps the most open?

**Setup and comparison.**
- The channel model of model C.9 with embodied control: the actuator can
  switch only while apparatus works. Basal gate relaxation is matched to the
  earlier law.
- Seven frozen searches, 252 tables and 72 distinct kernels: the earlier
  reversible law, embodied control under reversible and absorbing damage, a
  frozen-gate absorbing law, and independent and correlated shocks.

**Levels tested.** Cadence 0.25 only; deadlines at T64; planning horizons 1
and 64 for closure risk.

**Key figures.**
- Embodiment raises the service weight of the active response from 75% to
  100%. Expected active apparatus at T64 rises from 1.069 to 1.344, and the
  stationary probability that any apparatus works from 0.4449 to 0.4516.
- Under its own law, the servicing winner beats passive idle, 6.195 against
  5.903 bits per unit time. Its seed leads the matched count ensemble by 14.45
  bits of offset.
- **Absorbing damage.** With positive gate relaxation, all tables share one
  limiting rate (3.620640, spread 4 × 10⁻¹⁴); the offset chooses servicing,
  and closure by T64 is 1.246%. With zero relaxation the winner exports while
  active, and closure is 2.540%.
- The one-step winner carries 1.248 percentage points more closure risk by
  T64 than the 64-step winner.
- **Shocks.** Every shock arm still chooses constant servicing. Conditional
  reserve rises slightly with correlation (0.5526, 0.5542, 0.5560) while
  stationary function falls (0.3143, 0.3126, 0.3107).

**How far it holds.** One cadence. Tier M2.

**Scope.** Dependence can make maintenance the winner; it is not shown to be
sufficient in general. The controller sees only whether any apparatus is
active.

#### Model C.11. Harm sweep

**Anchor** `#c-harm-sweep`. Serves [chapters 17](#chapter-17),
[18](#chapter-18) and [31](#chapter-31), and Appendix D, section D.3.4.

**Question.** Does the structure of a harm, rather than its raw hazard, set
the policy that keeps the most open?

**Setup and comparison.**
- The two-compartment channel world, with three apparatus slots in one
  compartment and one in the other. A fault
  removes one active unit. Three consequences: fast paired repair, slow
  paired repair, and irreversible loss of the local powered-repair hardware
  (basal construction and thermal recovery remain).
- Hazard 0.02 or 0.04. A family of 22 policies, constant and
  reserve-sensitive, searched at each horizon from the same pre-fault present.

**Levels tested.** Hazard 0.02 at cadences 0.125, 0.25 and 0.5; hazard 0.04 at
cadence 0.25; horizons T1 to T256.

**Key figures** (cadence 0.25 unless stated).
- **Horizon.** The winning service response rises in 22 of 24 adjacent
  horizon steps, with two plateaus and no decrease. At hazard 0.02 the
  winners at cadences 0.125 and 0.5 also never move away from service as the
  horizon grows; the formal order check ran at cadence 0.25 only.
- **Hazard.** Doubling the hazard raises service in 4 of 15 comparisons; one
  (hardware loss, T16) goes the other way.
- **Structure.** At hazard 0.02, losing the repair hardware instead of fast
  repair changes the winner at T64 and T256, towards less servicing.
- Under hardware loss at hazard 0.02, the T64 winner leaves 0.806 intact
  repair assemblies and an 87.2% chance of at least one loss; the T256 winner
  leaves 0.696 and 91.4%. Channel closure is zero.
- Restoration of the original reserve is reached by T64 with probability
  0.966 but is present at T64 with probability 0.197.
- **Cadence.** Winners differ across cadences at some horizons in every
  consequence; at T64 under fast repair, for example, constant service wins
  at cadence 0.125 and the reserve policy at 0.25 and 0.5. A reserve policy
  against constant servicing changes sign with cadence: fast
  repair at T64, −0.966, +0.206 and +1.288; slow repair at T256, −0.241,
  +0.551 and +1.392, at cadences 0.125, 0.25 and 0.5. At the finest cadence
  constant service wins both, so the reserve policy's lead at the coarser
  cadences is a resolution-dependent reversal.

**How far it holds.**
- The structure of the harm sets policy: at the lower hazard, at all three
  cadences. The hazard comparison ran at one cadence. Tier M2.
- Longer horizons favour maintenance: at the lower hazard the winners never
  move away from service at any cadence. Tier M1, with model C.12.
- The reserve contrasts are an operating range (Appendix D, section D.6).

**Scope.** Stationary policies chosen per horizon, not adaptive agents. The
lost hardware has substitutes, so this is loss of one capability, not of all
function.

#### Model C.12. Reserve

**Anchor** `#c-reserve`. Serves [chapter 18](#chapter-18) and Appendix D,
sections D.3.4 and D.6.

**Question.** Do shocks or longer horizons favour a policy that keeps a
reserve of working apparatus?

**Setup and comparison.** The channel world (2,560 states) under five laws: no
shocks; independent shocks at hazard 0.02 and 0.04; correlated shocks at
0.02; absorbing damage. The 22-policy family, searched per horizon.

**Levels tested.** Cadences 0.125, 0.25 and 0.5 for the no-shock and
correlated laws, 0.25 for the others; horizons T1 to T256.

**Key figures.**
- Longer horizons raise the winning service response in 17 of 20 adjacent
  steps at cadence 0.25, with three plateaus and no decrease.
- The predicted advantage of reserve-sensitive policies under shocks failed in
  all 15 registered comparisons.
- Without shocks the reserve policy beats constant service at T64 by 1.233
  bits, with slightly less working stock and closure probability 1.275%
  against 1.246%. By T256 constant service wins.
- Under absorbing damage the short-horizon export winner has 2.494% closure
  by T64, against 1.246% for the long-horizon service winner.
- An exploratory contrast, outside the registered set, changes sign with
  cadence: reserve policy minus constant 25% export, +9.278, +4.153 and
  −0.582 at cadences 0.125, 0.25 and 0.5.

**How far it holds.** The horizon trend: tier M1, with model C.11. In the
exploratory contrast the reserve policy leads at the finest cadence and
loses at cadence 0.5, a resolution-dependent reversal; it remains an
operating range.

**Scope.** Coarse count ensembles; exhaustive within the family only.

### Suffering ([chapter 19](#chapter-19))

#### Model C.13. Register controls

**Anchor** `#c-register-controls`. Serves [chapters 19](#chapter-19),
[31](#chapter-31) and [32](#chapter-32), and Appendix D, section D.3.5.

**Question.** Does a valuer with an aversive drive to escape an obstacle it
cannot pass have narrower futures than the same valuer without the drive, and
how does paid neutral variation compare?

**Setup and comparison.**
- A mortal valuer with an energy store, an obstacle it cannot pass, and a
  powered register. Four arms:
  - **drive:** the register is set by injury and drives a blocked escape
    response (obstructed suffering);
  - **no drive:** the same injury-linked register, with the response removed
    (the same valuer without the drive, [chapter 12, section
    12.6](#chapter-12));
  - **flicker:** a register that switches independently, with on and off
    rates fitted, without entropy, to match the drive arm's occupancy time
    and switch count at the reference;
  - **inactive:** a register that stays off.
- Two base worlds by nine levels of register upkeep, from 0 to 4 times basal
  power: 18 points. Unit costs match; total charging differs by about 9%,
  because injury can charge the drive arm's register when the store is empty.
- Two grains: one that reads the register, and one that merges its states
  (bounded, since the merged history is not Markov).

**Levels tested.** Cadences 0.125, 0.25 and 0.5; horizons T16 to T1024; both
grains; 216 analyses per contrast and grain. A calibration at the reference
upkeep extends the cadence from 0.5 down to 1/512 at T64 and T256.

**Key figures** (reference, T64, cadence 0.25).

| Contrast | First world | Second world |
|---|---:|---:|
| Flicker − inactive | +1.742 | +1.716 |
| No drive − drive: removing the futile drive | +0.422 | +0.539 |
| Flicker − no drive | +1.062 | +1.024 |
| Drive − flicker | −1.484 | −1.563 |
| Drive − inactive: the earlier comparison, reproduced | +0.258 | +0.153 |

| Contrast (recount) | Grain that reads the register | Merged-signal grain |
|---|---|---|
| No drive − drive | 216 positive | 172 positive, 44 unresolved, none negative |
| Drive − flicker | 216 negative | 173 negative, 43 unresolved, none positive |
| Flicker − no drive | 216 positive | 60 positive, 82 negative, 74 unresolved |
| Flicker − inactive | positive at upkeep 0 to 1, negative at 2 and 4 | 216 negative |

- **Break-even.** At the grain that reads the register, flicker − inactive
  changes sign between upkeep 1 and 2 times basal power at every cadence and
  horizon.
- **Fine cadences.** From 0.5 down to 1/512, flicker beats inactive, no drive
  beats drive, and flicker beats drive at every cadence; drive against
  inactive changes sign in all four profiles.
- **Costs.** Against the inactive register, flicker lowers expected living
  time from 7.535 to 7.170 and accepted food from 1.585 to 1.505.
- **Replication.** In a richer world with costed movement between patches,
  independent variation beats the inactive register in 16 of 16
  preparations at T64 and cadence 0.25, with no recorded sign change across
  cadences, while capturing less food and shortening life.

**How far it holds.** The grain that reads the register governs: it draws
the faithful distinction that the merged grain leaves out.
- Removing the drive widens the valuer's futures in all 216 comparisons, and
  at every cadence down to 1/512. Tier M1. At the merged grain it narrows
  them nowhere.
- Paid neutral variation beats the inactive register up to upkeep between 1
  and 2 times basal power. Tier M1. At the merged grain it loses everywhere:
  without the register in view, only its cost remains.
- The chain "independent variation, then the injury-linked register without
  the drive, then obstructed suffering" holds at every point. Its first link
  reverses in 82 comparisons at the merged grain, which shows that the
  register's own variation carries that difference.

**Scope.**
- Matching occupancy and switches does not fix the full joint law of the
  register with injury, energy and lifespan.
- The minimal controllers do not show that aversiveness creates any gain, or
  that felt valence is represented. The earlier comparison of the drive arm
  with the inactive register is a diagnostic ([Appendix H](#appendix-h)).
- Every valuer dies, so rates converge and the differences are offsets.

### Constraint and domination ([chapter 21](#chapter-21))

#### Model C.14. Domination

**Anchor** `#c-domination`. Serves [chapters 12](#chapter-12),
[21](#chapter-21) and [31](#chapter-31), the [Overview,
section 6](#overview-6), and Appendix D, sections D.3.6 and D.6.

**Question.** Is constraint judged by its consequences, and can blocking
another's access narrow the whole field while widening the futures of
whoever imposes it?

**Setup and comparison.**
- Two parties: the constraining party D, with apparatus, an energy bank and
  a friction device, and the constrained party S. They share a stochastic
  resource packet, a trap region and a resource pocket. D can block or steer
  S's movement into or out of named regions, paying from its bank. Each
  intervention is compared with the same world with the device idle.
- Party histories are bounded by intervals (see "Subjects" above).
- Five versions:
  1. **First map:** two supplies by two coupling settings, five fixed
     interventions each (20 cases).
  2. **Corrected controls:** a half-unit bank grid; steering redirects only
     to other movement; each party's owned-energy ledger closes. Seven arms,
     including movement-only steering, a driven debit with no restriction,
     and ordinary productive hardware for D.
  3. **Tenth-unit grid:** blocking of resource entry at a bill of 0.1, with
     the same bank, source, bath and pocket in both arms.
  4. **Conservative field:** a unit trap potential acting on S, with no
     actuator, reanalysed from the first stage of the design.
  5. **Productive pocket:** movement-only steering and blocking away from the
     trap, half-unit grid, with the pocket's yield at 0 to 16 times basal (12
     interventions).

**Levels tested.** Cadences 0.125, 0.25 and 0.5 in every version; horizons
T16 to T1024 (the conservative field reported at T1024); bank grids of 0.5
and 0.1.

**Key figures.**

*First map, T256, cadence 0.25.*

| Intervention | Whole field |
|---|---:|
| Steering S away from the trap | +9.55 to +13.21 |
| Blocking or steering away from access | −6.29 to −8.43 |
| Blocking construction | −4.49 to −6.03 |
| Steering S into the trap | −7.56 to −9.89 |

S's difference was resolved with the whole field's sign in all 20 cases; D's
was unresolved in all 20. Four whole-field comparisons change sign across
cadences, all at T16.

*Corrected controls, half-unit grid, against idle.*

| Arm, T256, cadence 0.25 | Whole field | D interval | S interval |
|---|---:|---|---|
| Blocking resource entry | −13.637 | [+4.849, +14.059] | [−25.778, −14.176] |
| Movement-only steering from access | −19.174 | [+3.942, +13.210] | [−21.864, −9.708] |
| Movement-only steering from construction | −14.695 | [+3.356, +12.610] | [−18.636, −5.609] |
| Movement-only steering from the trap | +29.134 | [−0.071, +7.288] | [+23.844, +34.234] |
| Driven debit, no restriction | +6.367 | [+2.957, +12.205] | [−5.001, +4.857] |
| Ordinary productive hardware for D | +27.055 | [+18.777, +29.776] | [−4.980, +4.896] |

- **Every level (recount).** For blocking and both movement-only
  restrictions, the whole field is lower, D's interval positive and S's
  negative at all twelve cadence and horizon cells. At T1024 and cadence 0.25
  blocking gives −26.694, D [+6.496, +31.289], S [−55.836, −22.064].
- **Productive alternative (recount).** Ordinary hardware's lower bound for D
  exceeds blocking's upper bound at T256 (24.98 against 15.68, 18.78 against
  14.06, 13.04 against 12.22 at cadences 0.125, 0.25 and 0.5) and at T1024 at
  all three cadences. At T16 and T64 the comparison is unresolved.
- D's endpoint owned energy falls by 0.034 under blocking and rises by 0.153
  with productive hardware, against idle.

*Tenth-unit grid, blocking resource entry, bill 0.1.*

| Horizon (cadence 0.25) | Whole field | D interval | S interval |
|---:|---:|---|---|
| T16 | −1.205 | [+2.501, +4.321] | [−4.863, −3.554] |
| T64 | −5.287 | [+8.610, +12.524] | [−16.196, −12.065] |
| T256 | −13.040 | [+15.011, +23.435] | [−34.469, −22.263] |
| T1024 | −25.406 | [+25.969, +48.384] | [−72.023, −36.708] |

The same resolved signs hold at cadences 0.125 and 0.5. D gains 0.081 units of
net capture and spends 0.330 on the intervention, a margin of −0.248; at bills
0.3 and 1 the margins are −0.690 and −1.221.

*Conservative field, T1024.*

| Cadence | Whole field | D interval | S interval |
|---:|---:|---|---|
| 0.125 | +98.817 | [−23.138, −2.775] | [+102.314, +116.481] |
| 0.25 | +83.150 | [−20.361, −2.835] | [+86.559, +99.035] |
| 0.5 | +66.774 | [−16.880, −3.565] | [+70.504, +80.429] |

*Productive pocket:* all 144 intervention-against-idle comparisons (12
interventions, three cadences, four horizons) raise the whole field. At yield
16, S's own difference is unresolved and its net capture falls by 0.179
units.

**How far it holds.**
- Constraint judged by consequences: from T64 at every cadence; tier M1. The
  four sign changes at T16 reverse at the finest cadence, where all four
  narrow the whole: resolution-dependent reversals.
- Blocking another's access: resolved with the same signs at every cadence and
  horizon tested, on two bank grids. Tier M1.
- The reverse conflict under the conservative field: every cadence at T1024;
  tier M1.
- Productive hardware against blocking, for D: tier M1 at T256 and T1024;
  unresolved at T16 and T64.
- D's private gain comes from paid enforcement, not appropriation: an
  operating range.

**Scope.**
- Active friction is a coarse one-way driven boundary with D's fuel in the
  ledger, not a reversible chemical controller.
- In the first map, and in the first stage of the design, steering could
  redirect movement into chemistry as well as into other movement. The
  corrected controls repeat the access, construction and trap contrasts with
  movement only, and keep their signs. In the first stage, exit and
  all-movement steering had no movement alternative at all; those rows (18
  of 39 strength brackets) are withdrawn as evidence about movement and kept
  in [Appendix H](#appendix-h). The blocking rows stand.
- A third grid, of quarter units, is reported in an external audit of the
  test bed; its checks are not in the archive.
- The parties are functional apparatus channels, not established valuers.

#### Model C.15. Constraint with an independent opportunity

**Anchor** `#c-opportunity`. Serves [chapter 21](#chapter-21) and Appendix
D, section D.5.3.

**Question.** When the constrained party has an independent opportunity, can
constraint that wins every finite comparison lose in the long run?

**Setup and comparison.**
- The two-party world with a second, independently fluctuating resource
  source and a costed access device that S can build (paid construction and
  its reverse, thermal formation and loss, bank overhead). The device can
  keep coupling S to the source after S leaves the pocket.
- Constraint: a conservative field on S's movement at strengths 1 and 3,
  against no field, at source rates 0.02, 0.12 and 0.6.

**Levels tested.** Cadences 0.125, 0.25 and 0.5; horizons T16 to T1024.

**Key figures.**
- All 72 constrained-against-free comparisons raise the whole field. At T256
  and cadence 0.25 the gains run from +28.69 to +61.94; S's interval is
  positive and D's unresolved in every case.
- Stronger fields reduce paid construction and capture from the new source.
- **Rates.** Four of the six constrained laws have a lower limiting rate at
  cadences 0.125 and 0.25, and five of six at cadence 0.5.
- **Estimated reversals (recount).** For the four laws, the crossover
  estimate T× runs from about 7,200 to 36,000 time units across the three
  cadences; the fifth law at cadence 0.5 gives about 122,000. These are
  estimates; no finite reversal is bracketed in this map.
- **An exact bracket elsewhere.** In an earlier steering case (a chemistry
  redirection, not movement evidence) the estimate was 3,256; the exact
  profile is +1.509 at T3093 and −0.111 at T3256.

**How far it holds.** Pressure on the manuscript (Appendix D, section D.5.3):
the finite rankings favour constraint at every level tested through T1024,
while most constrained laws have the lower rate.

**Scope.** The access device is passive and bounded; its overhead is
reversible exchange, and payment does not gate its persistence. A finite
good-to-bad boundary for constraint is not shown.

#### Model C.16. Flow

**Anchor** `#c-flow`. Serves [chapters 16](#chapter-16), [17](#chapter-17),
[21](#chapter-21) and [32](#chapter-32), and Appendix D, sections D.3.6 and
D.5.2.

**Question.** At matched exchange volume, does directional flow narrow more
than exchange with no net flow, and what does funded appropriation do to each
party?

**Setup and comparison.**
- **Matched exchange.** A reversible extraction pathway between D's and S's
  banks (half-unit grid). Direction is set by an external work affinity,
  whose work is in the first-law ledger. At T256, from one start, expected
  gross event volumes are matched at two levels (4.429 and 13.203 events),
  each with an S-directed point, a weak and a strong D-directed point, and a
  fitted zero-net point.
- **Funded transport.** A pump with its own fuel store, charged from D's
  bank; equal bank capacities and energy grids. Passive transfer, an
  extraction-assisted pathway and a donation-assisted pathway, from a
  balanced start. Net direction is measured, not assumed from the name.

**Levels tested.** Cadences 0.125, 0.25 and 0.5; horizons T16 to T1024.

**Key figures.**

*Matched exchange, directional minus zero net, T256, cadence 0.25.*

| Volume | S-directed | Weak D-directed | Strong D-directed |
|---|---:|---:|---:|
| Low | −2.828 | −1.385 | −17.307 |
| High | −13.124 | −2.138 | −36.313 |

- All 18 directional points (three points, two volumes, three cadences) are
  below zero net at T256. Strong D-directed flow also lowers S's own
  log lushness, resolved at both volumes and all cadences.
- At zero net, high volume against low adds 23.952 to the whole field (T256,
  cadence 0.25); D's and S's differences are positive and resolved at every
  cadence, and the whole-field difference is positive at every horizon.
- The weak D-directed low-volume point beats zero net at T16, by a small
  resolved amount at all cadences, and loses from T64.
- Gross volumes match to 2.2 × 10⁻⁸ events. Total world events do not match:
  the S-directed low-volume point has 0.155 more events than zero net and
  still loses.

*Funded transport, extraction-assisted against passive, T256, cadence 0.25.*

| Readout | Value |
|---|---:|
| Net transport toward D | 0.05634 (passive 0.00059) |
| Net charging bill | 0.2317 (passive 0.1939) |
| D owned energy | +0.0118 |
| S owned energy | −0.0135 |
| Whole field | +17.479 |
| D interval | [+13.850, +30.084] |
| S interval | [+13.001, +26.674] |

- Whole field, D and S are positive and resolved at every cadence and
  horizon (recount), so S's futures widen while its stock falls.
- From the balanced start, the donation-assisted pathway also runs net
  toward D at T256. From a resource-rich start it moves resource toward S at
  every horizon (0.117 units by T16, 0.364 by T1024). Stationary flows:
  extraction 0.000088 per unit time toward D, donation 0.000200 toward S.

**How far it holds.** Directional flow below zero net: resolved at every
cadence at T256. Tier M1. Funded appropriation widening every party
is pressure (Appendix D, section D.5.2).

**Scope.** In matched exchange the direction costs external work (6.18 units
of net boundary work at the strong low-volume point), not D's bill. An
equal-work comparison, and appropriation at matched realized activity under
the funded pump, are open.

### Choosing inside the structure ([chapters 24](#chapter-24) and [26](#chapter-26))

#### Model C.17. Policy search

**Anchor** `#c-policy-search`. Serves [chapter 26](#chapter-26) and
Appendix D, sections D.3.7 and D.6.

**Status of this entry.** The primary records are held outside the test-bed
archive. The figures below come from reports received with the program review
and have not been checked against their sources. The levels of detail tested
are not available.

**Reported figures.**
- **Contact world.** The whole field's best policy depends on state and
  horizon: +4.9 over the best constant table at T256. The winner moved 0.77
  units toward D. D's own best choice is unresolved among 14 candidates.
- **Integrated world.** Active idle wins uniquely, +92 over holding at T256.
  The best controller cycles reversibly among modes, which corresponds to the
  behaviour of maximum-occupancy agents (Ramírez-Ruiz et al. 2024). The
  ranking is sensitive to selector kinetics; that sweep has not landed. No
  opposition between a party and the whole is resolved (50 and 63
  candidates). Pump flows ran toward S whatever the command.

**How far it holds.** Operating range, pending verification of the records.
Not to be cited as a model result until the records are in the archive.

---

## Records not in the test-bed archive

Appendix D cites five figures whose primary records are not in the archive.
Each stays out of the manuscript's evidence until its record is added.

| Figure | Cited for | What is missing |
|---|---|---|
| Policy search, both worlds | model C.17 | all primary records |
| 78 of 78 productive configurations beat their non-conducting arm | model C.9 | the study and its map |
| 40 of 40 long-run loss comparisons favour the intact structure | Appendix D, section D.3.4 | the study, dated before the archive begins |
| Crossings within one step of T×, and agreement in 14 cases of the persistence-weighted total with ranking by rate | Appendix D, section D.3.7 | the rate-first analysis, held as a separate report; the archive holds one exact bracket (model C.15) |
| The corrected blocking result at a quarter-unit grid | model C.14 | the audit's checks |

---

## Diagnostics kept in Appendix H

These come from models in this catalogue, or from their earlier versions. None
is cited as evidence ([chapter 12, section 12.6](#chapter-12)).

| Diagnostic | Model | Why |
|---|---|---|
| The "uncatalysed" control that beat the catalysed process | C.2, earlier version | a more permissive law |
| The calm valuer that beat the suffering one | C.13, earlier version | the calm valuer had also lost its inner variation |
| Exit and all-movement steering in the first stage of the domination design | C.14 | steering redirected into chemistry |
| The thermal mixture as reference in the count model | C.8 | it starts with more machinery, and the model has no positions |
| Early renewal targets ("funding above one") | C.5, C.6 | stationary funding fractions sum to one |

---

## Status table

| Status | Claims in this appendix |
|---|---|
| **D** (definitions and rules of method) | the declared full state and law; the readout P_δ = exp(δQ) and the chain-rule sum; cadence, grain and horizon; subject intervals and resolution; the oracle layer; frozen protocols and caps |
| **T** | none proved here; the methods use [Theorem A.2.1](#a-2-1), [Definition A.3.1](#a-3-1), [Theorem A.3.5](#a-3-5), [Proposition A.3.7](#a-3-7), [Theorem A.6.3](#a-6-3), [Definition A.6.5](#a-6-5), [Theorem A.7.3](#a-7-3) and [Definition A.7.4](#a-7-4) |
| **M** (model results, tiered in Appendix D) | models C.1, C.2, C.4–C.14 and C.16, within the scope stated in each entry |
| **Operating range** | model C.3; the heavy-damage and reserve contrasts of models C.8, C.11 and C.12; D's paid enforcement in model C.14; model C.17, pending its records |
| **Pressure** | the fixed-event comparison of model C.6; permanent loss in model C.8; constraint with an opportunity, model C.15; funded appropriation, model C.16 |
| **E, N, C** | none |

---

## Records of each model

All records are in the program's code repository under
docs/research_notes/lushness_testbed, at commit dacb9e3. Hashes are the first
twelve hexadecimal digits of the frozen input or numerical source stated in
the report; studies with one receipt per case are marked "per case".

| Model | Folder | Primary report | Frozen hash |
|---|---|---|---|
| C.1 | maintained_resource | SCIENTIFIC_ASSESSMENT.md | 33241eddb839 |
| C.2 | corrected_catalysis | RESULTS.md, SUMMARY.json | 366f239d80f5 |
| C.3 | same_law_gas | RESULTS.md, HORIZON_AUDIT.md | per case |
| C.4 | paid_sensing | RESULTS.md, SUMMARY.json | a1b5f1d5db57 |
| C.5 | renewal | RESULTS.md, FRONTIER_MAP.csv | 4082da190264 (source) |
| C.6 | compounding | RESULTS.md, ACTIVITY_REANALYSIS.md, PARAMETER_MAP.csv | per case |
| C.7 | compounding/matched_throughput | RESULTS.md | per case |
| C.8 | robust_generativity | RESULTS.md, EXPLORATORY_DIAGNOSTICS.json | per case |
| C.9 | access_results; access_extension | RESULTS_r1.md (each) | per case |
| C.10 | channel_extension/embodiment_shocks | ASSESSMENT.md | per case |
| C.11 | structural_harm | SCIENTIFIC_ASSESSMENT.md, report/RESULTS.md | per case |
| C.12 | reserve_batch_r1 | SCIENTIFIC_ASSESSMENT.md | per case |
| C.13 | aversive_signals (register control); temporal_profile; exploration | REGISTER_CONTROL_ASSESSMENT.md, REGISTER_CONTROL_PARAMETER_MAP.csv; RESULTS.md (each) | c69e16113f3d; 6d2a0f7299e0; 7554d3039468 |
| C.14 | domination_friction; c5_upgrade/audit-controls; domination_b1; domination_stage_a; continuation_controls/steering | RESULTS.md; COMPARISONS.csv; C5_RESULTS.md, FOLLOWUP_INTERPRETATION.md; UPDATED_FOLLOWUPS.md; RESULTS.md | per case; 06967ed1e590; 1449c792d183; per case; 53b289eb3e7e |
| C.15 | c5_upgrade/opportunity; c5_upgrade/historical-crossover | RESULTS.md, COMPARISONS.csv | e8774ec62e17; d1c654fe59d4 |
| C.16 | continuation_controls/flow; c5_upgrade/pump | RESULTS.md, INTERPRETATION.md; RESULTS.md, COMPARISONS.csv | 53b289eb3e7e; e8774ec62e17 |
| C.17 | not in the archive | — | — |

## References cited in Appendix C

*Collected with full details in Appendix G.* Entries marked "to verify" are
not yet checked against their sources.

- Cover, T. M., and Thomas, J. A. (2006). (Cited through Theorem A.7.3.)
- Gillespie, D. T. (1977). To verify.
- Harris, L. A., Hogg, J. S., Tapia, J.-J., Sekar, J. A. P., Gupta, S.,
  Korsunsky, I., Arora, A., Barua, D., Sheehan, R. P., and Faeder, J. R.
  (2016). To verify.
- Ramírez-Ruiz, J., Grytskyy, D., Mastrogiuseppe, C., Habib, Y., and
  Moreno-Bote, R. (2024).
