# M4 delivery: independent control, transfers and coordinate diagnosis

24 October 2026. Local engineering and analysis delivery; no policy map or
publication. [Model](JOINT_CONTROL_MODEL.md),
[verified compact evidence](JOINT_RESULTS_SUMMARY.json).

## What is implemented

Two independently wired, embodied controllers can redirect their own catalytic
capacity, build, share bank energy or extract it from the other pool. Extraction
has positive per-event actor return after an upfront handling bill; sharing and
extraction are both affordable in the declared bank. Exact reverse channels,
refunds, passive exchange, apparatus dependence and complete energy ledgers
remain. The new fixed-budget law allocates existing catalytic capacity between
autonomous and controlled uses. It does not grant extra productive capacity to
the controller. Historical single-controller laws and results are unchanged.

The same candidate-pair record feeds whole-field choice and each controller's
best response while holding the other table fixed. Local scores are bounds on
true projected histories. They are not the ordered coordinate shares, and no
coarse Markov dynamics replace hidden-state dependence. Incomplete tables and
overlapping intervals cannot certify a global winner. Pure equilibria may be
unresolved or absent. This machinery is engineering-tested, not evidence of
different private and whole-field optima in the new world.

## What explains the previous reversal

The two earlier 16,200-state sensor worlds were reconstructed with their native
kernels and roots. All nine full-history scores per world reproduce the retained
results within 4.55e-13 bits. Every native state and represented random event
remains. This is a new explanation of existing results, not a new policy search.

The fixed decomposition order is **resource; material and banks; selectors;
sensors**, applied to each sampled transition conditional on the complete
previous state. The terms below are tracking minus blind control, in bits:

| Horizon, cadence .25 | Resource | Material/banks | Selector | Sensor | Complete history |
|---|---:|---:|---:|---:|---:|
| 64 | +0.506 | +0.970 | +0.294 | -0.774 | +0.996 |
| 256 | +2.388 | +2.859 | +0.356 | -2.856 | +2.746 |
| 1024 | +5.377 | +0.326 | -0.610 | -11.995 | -6.902 |

At T1024, tracking still contributes more in resource and material/bank
coordinates at the primary cadence. Blind control has more residual sensor
randomness, enough to outweigh those gains. This is consistent with tracking
having more capture, apparatus and expected jumps, yet less total lushness.
It corrects any interpretation that blind wins merely by having more events.

The complete T1024 difference is negative at all three measured cadences:
-4.744, -6.902 and -9.092 bits at .125, .25 and .5. The sensor term is negative
throughout. The material/bank term itself changes sign at .5. No inference about
arbitrarily fine cadence is made.

These shares depend on ordering. The sensor term is what remains unpredictable
after the preceding coordinates are supplied; it is not the sensor's marginal
history entropy, a unique causal attribution, or an amount to subtract. The
direct complete-history comparison is order-independent. Randomness continues
to count. This fixture demonstrates a physical trade between tracking's
downstream effects and the register's own variation; it does not establish a
general ranking of information versus noise.

## Measured engineering performance

| Task | States | Wall time | Peak process-tree memory |
|---|---:|---:|---:|
| Initial 1+1 joint smoke | 19,200 | 27.3 s | 176.9 MiB |
| Tracking decomposition, all rows/three cadences | 16,200 | 268.9 s | 687.1 MiB |
| Blind decomposition, all rows/three cadences | 16,200 | 269.0 s | 699.7 MiB |
| 2+2 joint profile | 120,000 | 237.9 s | 928.7 MiB |
| Current-source 1+1 smoke | 19,200 | 28.3 s | 177.5 MiB |
| Frozen-source smoke replay | 19,200 | 28.2 s | 177.4 MiB |

Every task finished inside its declared wall, memory and storage caps. The
four-slot generator has 3,050,600 nonzeros; its 2,118,820 canonical reaction
pairs are generated lazily. Compilation took 157.7 seconds. No dense sampled
kernel or full Cartesian event-object table is retained.

The four-slot native independent energy residual is 4.66e-15; source-off
pairwise flux residual is 1.28e-21 or less. The source-off check retains native
bath dynamics and tests the independent Gibbs distribution. A regression also
compares this shortcut with a separately constructed source=0 world with paid
transfer enabled. Pair audits check every positive channel's inverse.

The 2+2 profile has one L A unit and one R B unit initially, both banks full,
idle selectors and the locked resource. Its tables are L=(access,extract),
R=(access,share). This is one engineering pair with direct kinetic observation,
not an optimum or a paid-sensor experiment. At T64 both pools have expanded in
expected working stock (L=1.396, R=1.371). Net transfer into L is +.02859 bank
energy, counting both parties' transfer routes and the passive conduit. Both
banks are below their initial levels. Without another policy's result, none of
this establishes a comparative benefit from extraction.

## Precision and the next execution decision

The row probe retains the **entire** native generator and exact numerical
occupations, then computes 256 selected sampled rows. Every uncomputed row
receives an analytic entropy upper bound rather than being discarded. At the
primary cadence .25, the whole-history intervals are:

| Horizon | Lower bits | Upper bits | Width |
|---|---:|---:|---:|
| 4 | 9.567 | 9.901 | .335 |
| 16 | 32.229 | 46.979 | 14.750 |
| 64 | 62.037 | 301.704 | 239.667 |

Local bounds are wider still: at T64 L is [20.548,301.704] and R is
[22.699,301.704]. These are analytic missing-row/conditioning bounds around
floating-point propagation, not interval-arithmetic solver certificates. No
midpoint or lower-bound ranking is licensed.

**Go:** the physical module, capped execution, reconstruction and source
integrity. **Hold the exhaustive map:** these probe bounds cannot resolve its
intended questions. Extrapolating the measured 8.22-second row query gives
3,852 seconds (64 minutes) for all 120,000 rows at one cadence. That is a cost
forecast, not a measured full-row run. Nine policies would cost roughly ten
serial hours at the primary cadence before additional audits/queries. Three
cadences can reuse propagation but require a separate profile. Full rows remove
the missing-row width; intrinsic local-history conditioning width can remain.
The current512MiB query-workspace guard also prevents simply asking this combined
backend to retain all projected rows: their storage grows with coverage. A full
query needs an explicitly larger workspace budget or separate whole/local
artifacts. No oversized allocation was attempted.

The next query sprint should:

1. Reuse common state layout, grouping and reaction structure across wirings;
   cache each policy-specific sparse generator and audit under its own hash.
2. Refine occupation-weighted row coverage incrementally in the same four-slot
   world. Measure width versus rows and wall cost before choosing a grid budget.
   Reuse computed rows rather than restarting each refinement.
3. Separate complete-world row-entropy queries from optional projected-row
   storage. A whole-field score should not require retaining large local
   probability artifacts. Add targeted local-history depth/filter refinement
   only where the resulting intervals can answer a best-response question.
4. Profile a longer capped all-row query or a validated paired estimator on one
   representative pair if incremental bounds remain too wide. Statistical
   intervals and deterministic conditioning bounds must remain distinct.
5. Only then map the proposed 3x3 constant access/share/extract family on the
   same five-mode hardware, followed by responsive wirings. Keep unresolved
   private decisions explicit even if the whole-field winner separates.

No enlarged map, paid-bit four-slot world or further physical sweep launched.
The two-paid-bit forecast is 480,000 states and has not been built. The 1+1
world is an engineering control, not a substitute for four-slot composition.

## Standard report form and scope

**Mechanism:** independent physical control and costed reversible energy
transfer inside a shared productive ecology. **Ranking:** not assessed in the
new world; prior tracking/blind differences decomposed without changing them.
**Parameter relationship:** current work measures scaling/precision, not a
response surface. **Comparison:** new-world engineering; previous matched-cost
sensor mechanism contrast. **Horizon:** engineering T4/16/64 at .25; prior
decomposition T64/256/1024 at .125/.25/.5. **Challenged:** whether control can
be embodied without free productive machinery, and what carries the earlier
reversal. No new ethical bridge, domination verdict or robust-compounding claim.

No permanent structural loss, refusal/defence, spatial contact, lineage,
arbitrary population, cross-scale assembly or bounded/ML learning is yet
implemented in this adapter. Named schemas, owned controllers, pair modules,
query-side monitors and scope records leave those additions separate from the
objective. Offline oracle search remains external; its own compute is not
pretended to be an in-world deliberator.

## Verification and retention

55 focused tests passed across joint physics/game analysis, coordinate queries,
legacy ecology physics/control/scope and workflow. Ruff is clean. The final
current-source smoke reproduces the earlier engineering kernel and numerical
profiles, and exercises candidate recording. Frozen-source replay independently
matches profiles, kernel and audits. These comparisons exclude host/runtime.

Six completed tasks in five retained batches occupy about155 MiB, mostly
rebuildable query caches. Compact JSON is about197 KiB. Analysis code is retained
under its content hash in `analysis_source/`; each batch has verified source
snapshots, receipts and a reconstruction inventory. Only explicitly identified
query caches are marked evictable; no data was deleted. No commit, push, upload,
external task message or manuscript edit occurred.
