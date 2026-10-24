# Available work, access bottlenecks and consequential expansion

Implementation specification for Sol 6.1 — 24 October 2026, revision 1.

Status: specification only. The user requested this handoff; this document does
not launch implementation, runs, commits, pushes, uploads or external messages.
When implementation is authorized, follow the staged scope below. Preserve the
current branch and unrelated pending work. No manuscript definition changes.

## 1. Research question and intended outcome

How much thermodynamic opportunity remains in the current ecology, what
prevents its use, and which additional physical enabling relation could turn
that opportunity into further sustained or compounding continuation breadth?

The framework's open hypothesis is that there are regimes in which successive
costed enabling structures unlock resources that maintain or expand further
enabling structures, producing greater lushness than a matched baseline.
The task is to locate and explain such regimes and their boundaries. It does
not require organization, information or additional layers to win universally.

Deliver an audit of the existing four arms, a small causal bottleneck map, and
an evidence-based recommendation for one next physical module. Do not interpret
unspent energy as proof that another generative layer must win. Do not expand
everything until a preferred ranking appears.

Separate four questions throughout:

1. Is excess free energy stored, or work continuously supplied?
2. Which existing physical paths can use it, and what limits their flux?
3. Does a specific costed addition improve access and continuation breadth?
4. Does that addition participate in recursive construction and persistence?

The first two diagnose opportunity; the latter two test its consequences.

## 2. Starting evidence and comparator discipline

Use the completed four-arm batch
`results/local_runs/lushness_testbed/ecology_access/20261023T233013Z-51c8dc34`:

| Arm | Sensor | C-assisted class-2 access |
|---|---|---|
| I+ | Tracking local reserve | Present |
| I− | Tracking local reserve | Absent |
| R+ | Blind paid refresh | Present |
| R− | Blind paid refresh | Absent |

Each has 27,000 states, inventories 2+2, one five-state shared carrier,
source split .5, C site allocation .5 to access/.5 to construction, fixed
controlled fraction .5, paid sensor and selector, and the same H=4 seed.
All native randomness remains in all arms. Read exact settings and receipts
from the frozen manifests, not this prose.

At T1024/cadence .25 the added route yields +68.9915 bits for tracking and
+69.3017 for blind; both gains persist in the stationary diagnostic and across
the three measured cadences. Tracking minus blind is −9.1175 bits with the route.
Both arms already contain generative machinery. Blind control is not gas or a
non-generative baseline. Distinguish:

- access mechanism versus its paired ablation;
- informed versus blind control of comparable machinery;
- organized versus disordered preparations under one law;
- additional enabling depth versus a matched shallower mechanism.

Only the first two are instantiated by the current panel. Same-law finite
irreducible preparations normally share a limiting rate; finite profiles and
offsets remain valid evidence. A new capability need not produce a rate contrast
between roots to count as consequential.

## 3. Thermodynamic contract

### 3.1 Reference and units

Use the existing state energy E_i, log degeneracy log g_i, and beta. Construct
the normalized equilibrium reference of the source-off native law:

    pi_i = g_i exp(−beta E_i) / Z.

Verify detailed balance and stationarity independently using the registered
drive-boundary removal. Do not use the driven stationary distribution in place
of this equilibrium reference. Keep all bath, reverse and controller reactions.
The current reaction contract includes degeneracy explicitly; omitting g_i
would silently change the physical entropy and free energy.

For a distribution p over count states, in units with k_B=1:

    S_phys[p] = −sum_i p_i log(p_i/g_i)
    F[p]      = sum_i p_i E_i − S_phys[p]/beta
    A[p]      = F[p] − F[pi] = D_KL(p || pi)/beta.

All logarithms here are natural. A is in native energy units, unlike log
lushness in bits. Report units explicitly. This is the coarse model's
nonequilibrium free-energy excess relative to its specified bath/reference;
it is not a universal measure of organization, value or lushness.

Call A an available-work benchmark. Actual extraction depends on permitted
controls, barriers, time and costs. Do not claim every unit is recoverable by
the present apparatus. A delta preparation at the count grain does not assert
knowledge of one resolved microstate within its degeneracy class.

For disconnected source-off components, identify conserved sectors. Use the
equilibrium distribution with the same sector weights for operational
relaxation availability. If reporting a global Gibbs KL as well, label the
sector-weight contribution separately: inaccessible changes in conserved
sector weights are not extractable work. Declare support failures explicitly.

### 3.2 Time-dependent stocks and flows

Compute p(t) from the unmodified native driven Q at
T={0,4,16,64,256,1024}. Add intermediate times only for a stated diagnostic.
Report mean stored energy, S_phys, F, A and source-off reference identity.
The maintained source is not a finite remaining fuel stock. Separate:

- stored free energy at a section;
- gross external work accepted and returned over a window;
- net external work;
- heat exported to the bath, with sign;
- changes in internal stored energy and free energy;
- irreversible entropy production.

Use continuous occupations for integrated physical flows. Sampled occupations
are for sampled-history entropy and must not be substituted into energy bills.

For the present single-bath, fixed-energy, fixed-degeneracy model, verify:

    Delta<E> = W_net − Q_out
    Sigma    = Delta S_phys + beta Q_out
             = beta (W_net − Delta F) >= 0.

Count all external work channels. Internal bank transfers, capture and refunds
must not be counted again as external work. If future modules introduce
chemical reservoirs, multiple baths or changing energies, extend the contract
explicitly before applying this identity.

Compute cumulative Sigma robustly from endpoint/flow identities. Independently
validate it on small worlds using channel-resolved pair currents:

    sigma(t) = sum_pairs (p_i k_ij − p_j k_ji)
                        log[(p_i k_ij)/(p_j k_ji)].

Sum each reversible physical pair once, retaining parallel mechanisms with
different work/affinity. Aggregating them into Q_ij before computing production
can hide dissipation. At a point-mass start, instantaneous sigma can diverge;
the integrated value can remain finite. Do not insert arbitrary probability
floors. Use endpoint identities or convergence-checked integration at t>0.

Entropy production is not history entropy, and heat export is not synonymous
with avoidable waste. Necessary maintenance also dissipates. A stationary stock
of A can coexist with continuous work consumption and useful sustained access.

### 3.3 Physical and accounting scope

Existing ReactionPair.work and declared_heat_export are the primary ledger.
Audit consistency with state-energy differences, degeneracy and rate ratios.
Use a stable pair registry for thermodynamics; do not infer heat from labels.
Keep full-system A primary. Free energies of subsystem marginals cannot be
summed blindly because correlations contribute; subsystem decomposition is
optional and must include its interaction/correlation remainder.

Do not define lushness/A as an objective or universal efficiency score.
Do not interpret an equilibrium thermal process's continuing history entropy
as thermodynamic production of available work.

## 4. Access and bottleneck observables

Add query-only observables. They must not change Q, the state schema, root,
entropy grain, source prescription or controller wiring.

For every resource class and relevant pool/type, report:

| Process | Required readouts |
|---|---|
| Supply | Forward acceptance, reverse return, net work, carrier occupancy |
| Unlocking | Locked/usable occupation; basal and assisted forward/reverse flux |
| Capture | Gross credits, reverse debits, net credits by class and pool |
| Construction | Gross builds/disassemblies, paid bank change, substrate availability |
| Maintenance | Upkeep/damage/recovery flows actually present; no invented damage |
| Control | Sensor/selector spending/refunds, mode occupation, catalytic engagement |
| Storage | Empty/full bank fractions and joint occupancy with usable resource |
| Allocation | Existing sites allocated/engaged per function and alternative uses |

Record T-window integrals, endpoint values and time-normalized values. Do not
turn an internal flow ratio into a conservation claim. Retain gross and net
values; do not hide large reversals behind net capture.

### 4.1 Availability predicates

Each predicate must have an explicit state-based definition and list of
required coordinates, applicable reaction families and interpretation:

- locked resource with no matching catalytic unit;
- matching catalyst present but its controlled sites disengaged;
- usable resource with a capture partner but insufficient bank headroom;
- material eligible for construction but bank below the bill;
- sufficient material/bank but absent assisted route;
- carrier occupied by the other class;
- organization present but no currently enabled downstream use in the adapter.

Predicates may overlap. Publish joint masks or intersections for major pairs;
do not add marginal percentages into a fictitious partition. Distinguish
missing assistance from absence of all access when basal reactions remain.

Time occupancy is not lost work. The current source has no explicit arriving
packets while the carrier is occupied, so there is no observed rejected-arrival
count. Label any offered-arrival benchmark as a counterfactual source model;
do not invent it by subtracting accepted work from conductance times horizon.

### 4.2 Fate and delay

For each carrier class, estimate the next outcome after entering its locked
state: capture into a bank, return to source, native loss/return to bath, or
unresolved by deadline. Specify the absorbing event families and competing
risks exactly, including apparatus/control evolution during the episode.

Use actual entry-event-weighted state distributions, not uniform states or
ordinary time occupancy. Report the number of entries/normalizer and undefined
cases when it is zero. Terminal capture is a first-entry credit, not permanent
retention; report subsequent reverse flux separately. If repeated source
cycling starts a new episode, state this convention and do not claim unique
physical particle lineage in the count adapter.

Use killed generators/event-marked queries as analysis objects. They must not
replace the physical generator used for lushness. Begin with eventual fate
and unconditional truncated episode time; deadline-specific queries can follow
if their state-space/time dependence is affordable. Report survival mass for
episodes with no absorbing outcome.

## 5. Minimal causal probe map

First complete the unchanged four-arm audit. Correlations/occupancies nominate
bottlenecks but cannot establish them alone. Then select at most two candidate
bottlenecks, with a written physical reason, for a small diagnostic map.

Recommended first candidates supported by current architecture:

1. Reallocate C sites: c_access={.25,.5,.75}, retaining total allocation and
   the same source, thermal law, bills and inventories.
2. Change source composition: phi={.25,.5,.75}, retaining total source
   conductance and affinity. Composition is a boundary contrast, not a policy.

Run these as separate one-axis maps around the existing .5/.5 point, not their
Cartesian product. Across all four arms this is at most 16 new physical cases;
the four center cases are reused. Audit occupations/flows first. At zero
assistance some allocations may alias: detect identical Q and reuse queries.

An alternative second probe can vary a symmetric paired kinetic conductance
around its current value to diagnose a capture/transport bottleneck. This is
a changed-law kinetic sensitivity, not free hardware that a physical agent
possesses. Preserve local detailed balance, document the intervention, and do
not classify faster traffic alone as added generative depth.

Initially evaluate cheap physical diagnostics for the complete nominated map.
Full history scoring defaults to no more than four new cases, selected to
bracket the identified bottleneck or trade-off before inspecting their new
lushness scores. State that selection is mechanistic/exploratory and report the
full cheap map. Expand scoring if results and compute justify it; preserve every
evaluated point. No confirmation ceremony or guessed-sign pass/fail is needed.

Carry the existing contrasts:

    U_I = ell(I+)−ell(I−), U_R = ell(R+)−ell(R−)
    D_on = ell(I+)−ell(R+), D_off = ell(I−)−ell(R−)
    G = D_on−D_off.

Also report finite differences of physical throughput and A against each probe.
These estimate local sensitivity, not a global optimum or recoverable-work
ceiling. No ratio of entropy gain to a vanishing denominator is a headline.

## 6. Decision rule for the next physical expansion

The audit must end with a mechanism table, including evidence against each
candidate explanation, and a recommendation for ONE next module:

| Diagnosed limitation | Candidate physical addition | Required cost/matching |
|---|---|---|
| Shared carrier congestion | Additional carrier or transport machinery | Material, construction, upkeep; matched supply/endowment |
| Bank headroom | Constructible storage | Capacity material, energy, leakage/upkeep and preparation cost |
| Missing route to useful resource | New catalytic dependency | Basal thermal route retained; paired reverses and site budget |
| Reserve information cannot guide resource choice | Paid opportunity-specific sensing and distinct actions | Blind hardware comparator; no free observation or action |
| Apparatus has no further productive use | Costed downstream construction/access layer | Explicit prerequisites and resource budget; no arbitrary bonus |
| Energy availability too low | Supply/window regime map | Declared boundary contrast; do not claim same supply |

More stored A alone does not select a module. Require a concrete dependency
and a probe consistent with relieving it, or state that the diagnosis remains
unresolved. A negative result is also useful: current paths may already exploit
the useful opportunity, or further access may be too costly in this regime.

Future layering studies should index physical designs by enabling architecture
and compare their full profiles under matched endowment/boundaries. New hardware
must come from paid latent material, not an unexplained extra initial stock.
The baseline retains native thermal activity and any self-assembly allowed by
its declared comparison. A reaction ablation is a mechanism contrast explicitly.

Track separately: causal enabling depth, maintained function, expansion,
recovery, lushness and stationary diagnostics. Reuse the existing conservative
lineage/witness machinery only where its assumptions hold; do not equate three
species, three reactions or three births with three genealogical generations.
Analysis witnesses add no physical entropy and never silently restart.

No finite ladder proves unlimited compounding. A crossed frontier demonstrates
a regime of the modeled mechanism; no crossing bounds the inspected range.
Robustness and opportunity-window dependence remain explicit separate axes.

## 7. Architecture and interfaces

Extend reusable analysis interfaces, not one experiment's reporting script.
Suggested new modules (names may follow repository conventions):

- `analysis/ecology_thermodynamics.py`: equilibrium reference, degeneracy-aware
  F/A, endpoint/flow balances, sector handling, pair-resolved validation.
- `analysis/access_bottlenecks.py`: typed predicates, joint occupations,
  continuous rewards, pathway fates, interventions and sensitivity summaries.
- `scripts/ecology_opportunity_worker.py`, `run_ecology_opportunity.py`,
  `report_ecology_opportunity.py`: frozen tasks, capped queue and report.

Reuse `ReactionPair`, `ResourceFamily`, `CatalyticUse`, `DriveBoundary`,
`source_off_generator`, occupation propagation, incremental history queries,
and reconstruction receipts. Reconstruct the original four arms from their
frozen sources/inputs, then verify kernel, state-order, root and metadata
identities against the analysis adapter before reusing evidence.

Public data contracts must separate:

- `ThermodynamicReference`: energy/degeneracy/beta, sectors, normalized log pi,
  source-off fingerprint, reference assumptions and units;
- `MechanismLedger`: stable pair identity, module/owner, endpoints, two rates,
  work, heat, stoichiometry and catalytic dependencies;
- `BottleneckQuery`: definition/version, coordinates, masks/event families,
  normalization, deadlines and interpretation;
- `OpportunityAudit`: context hashes, numerical residuals, reference, endpoint
  profiles, integrated flows, fates, probes and explicit unavailable fields.

Use iterable/chunked reaction ledgers rather than retaining duplicate millions
of Python objects. Preserve parallel channels. Query labels/lineage annotations
are not additional states in the scored physics. Future population, spatial,
multi-agent and cross-scale modules should register their own coordinates,
mechanisms and boundaries through these contracts, without hardcoded A/B/C or
five-state-carrier assumptions. Different physical schema versions cannot share
cached query artifacts simply because their dimensions match.

Future multiple reservoirs/baths require a richer reservoir ledger, not a
misleading application of the single-bath formulas. Reserve extension fields
now; unsupported cases return explicit status rather than fabricated zeros.

## 8. Numerics, validation and resource limits

The audit needs sparse propagation and reward queries, not a new dense sampled
kernel. Reuse existing finite lushness results and compatible cached rows.
Endpoint free energy is nonlinear in p: an integrated occupation alone is not
sufficient to reconstruct it. If endpoint arrays were not retained, recompute
them cheaply from the verified generator. Do not approximate F from mean energy
and an entropy of a mean state.

Validation required before scientific interpretation:

1. Source-off pi passes stationarity/detailed balance, including degeneracy.
2. F−F_eq agrees with KL/beta on independent small examples; A(pi)=0;
   source-off A relaxes monotonically within numerical tolerance.
3. Integrated first and second laws close; pair-current integration agrees
   with endpoint balances on a small driven example with parallel pathways.
4. Zero-probability terms, point roots, sector mixtures and zero-entry fates
   produce correct finite/undefined statuses, never arbitrary floors.
5. Fate probabilities plus unresolved mass sum to one; small independent
   absorbing-chain solutions reproduce episode metrics.
6. Query additions preserve original four Q/root hashes and history scores.
7. Fixed site allocations and paired rates are respected by interventions;
   resource coupling-off retains all native thermal paths.

Initial tolerances: probability normalization 1e-10; energy/balance comparisons
1e-8 times max(1, sum of absolute ledger terms); reject meaningful negative A
or Sigma outside the corresponding error budget. For nonlinear pair-current
integration require numerical refinement with an error estimate rather than
using that balance tolerance as a quadrature guarantee. Calibrate changes from
small solver convergence tests and record them, not from desired scientific
signs. Preserve raw residuals. Refinement failure marks a query unresolved.

Engineering stages: 1+1 smoke under 120s/2GiB; one original 27k-state audit
profile under 600s/4GiB. These are engineering probes, not smaller substitute
science. Initial four-arm audit: two workers, 4GiB each, 8GiB aggregate,
900s per case. If profiles justify larger limits, record the estimate and use
available local capacity; never reduce physical state space silently.

Full history cases retain the existing 1800s/4GiB cap initially; last measured
27k cases took 645–679s and about1.11GiB. No new broad full-history grid until
the audit identifies its purpose and the exact query forecast fits.

Use JSON manifests/summaries, compressed arrays only where needed, and existing
query caches. Default additional storage budget 1GiB, with a dry-run size
forecast before enlargement. Preserve code/config/source hashes, compact
results, receipts and enough provenance to reconstruct. No automatic deletion
of historical evidence; cache eviction must follow existing manifest/pinning
rules and record what was reconstructible. No user-path glob purges.

## 9. Deliverables and staged completion

Stage A: implement reusable queries and independent small validation; run the
unchanged four-arm audit once feasibility is established.

Stage B: produce the small physical sensitivity map, and at most four initially
selected new full-history cases if computationally feasible. Distinguish audit
results from exploratory new-law comparisons.

Stage C: write the next-module recommendation and its concrete physical design.
Do not implement that next physical expansion under this audit's scope.

Files:

- `OPPORTUNITY_AUDIT_MODEL.md`: definitions, reference and query contracts;
- `OPPORTUNITY_AUDIT_RESULTS.md` and compact verified JSON;
- `OPPORTUNITY_AUDIT_ASSESSMENT.md`: bottleneck evidence and recommendation;
- figures: free-energy stock alongside net work/production; resource fates;
  bottleneck intersections; physical probe response; existing/new lushness
  profiles with scope labels;
- tests, frozen runner/source receipts and reconstruction instructions.

Every report fills the manuscript's standard six fields: mechanism, what
lushness ranked, parameter relationship, comparison kind, horizon, and what was
challenged. Add a seventh practical field: which physical expansion this evidence
supports, or why none is yet selected.

Conclusions must distinguish stored opportunity, maintained opportunity flow,
demonstrated access, demonstrated recursion, and demonstrated breadth payoff.
Any putative transition toward recognizable valuers is exploratory: look for
self-maintenance, consequential paid sensing/action, reconstruction and further
enabling. Neither high A, high dissipation nor a lushness crossing establishes
consciousness, normative status or a phase transition by itself.

## 10. References and existing implementation anchors

- [Current physical model](ACCESS_MODEL.md), [assessment](ACCESS_ASSESSMENT.md),
  [verified results](ACCESS_RESULTS_SUMMARY.json).
- `omega_v2/testbed/ecology/pairs.py`: work/heat, degeneracy and reversible rates.
- `omega_v2/testbed/analysis/joint_physics.py`: independent source-off audit.
- `scripts/ecology_access_worker.py`: current occupations, flows and history queries.
- [Qian: relative entropy and free energy](https://arxiv.org/abs/math-ph/0007010).
- [Seifert: stochastic thermodynamics](https://arxiv.org/abs/1205.4176).

The physical audit informs where to search for compounding. It neither changes
lushness nor adds an available-work factor to it.
