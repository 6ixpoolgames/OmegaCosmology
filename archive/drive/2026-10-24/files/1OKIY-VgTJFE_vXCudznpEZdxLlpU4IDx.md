# Code audit of the results cited for v4.1 — r1

**Date:** 15 October 2026.
**Scope:** the code behind every test-bed result the revision ledger (r9) cites
for the rewrite. Repository: github.com/6ixpoolgames/omega, branch
codex/operational-continuation-comparison, commit 59eb3da (the latest
published). Codex's local work after that commit (Constraint Stage A, the
Poisson-series entropy method) is not in the repository and is not covered.
**Method:** read the world and analysis code; ran the tests for the cited
modules (107 pass); reproduced headline numbers with independent code; ran
four targeted checks where reading raised a question. Scripts are in
audit/scripts.

## Summary

| Result (ledger rows) | Verdict | Action for the rewrite |
|---|---|---|
| Shared entropy engine (all rows) | Correct. Reproduced to 6 decimals with independent code. | None |
| Suffering wager (A22, C16) | Correctly matched; robust over upkeep, cadence and horizon. Rests on 2 base worlds. | State the base; sweep the world's parameters before claiming breadth |
| Information and renewal (A26, C17, A3, A13) | Strong. The advantage is the information–action interaction in all 57 comparisons. | Cite that decomposition |
| Compounding boundary and matched throughput (C4, C1b, A16, B3) | Stands. Capture is one-way in this world, but the missing reverse slightly strengthens the result. | Note the consistency fix; C23's world is fully reversible |
| Spatial lattice (C1a, A3, B6) | Correctly matched in energy and inventory. Its driver is a single motion choice, larger than the ledger says. | Correct "binding halves motion"; sweep cluster mobility |
| Robust compounding (C23) | Thermodynamically consistent (fully reversible capture). | None beyond known scope |
| Domination: paternalist and extractive (C5) | Robust across both modes, both physical realizations, strength and cost. | None |
| Domination: confinement and forced labour (C5, Stage A) | **Mostly an artifact** of how steering was implemented. | Rerun with corrected steering before citing |
| Domination: the dominator's private gain (C5, Stage A) | Real under the measure, but produced by paying for enforcement, not by appropriation. | Describe the mechanism correctly |

## 1. Shared engine

**What it computes.** For a finite continuous-time law Q sampled at cadence δ,
P = exp(Qδ). The finite-history lushness from root x over n samples is
Σₜ (Pᵗ g)(x), where g is the entropy of each row of P. That is the exact chain
rule for a Markov chain observed at full state.

Three implementations exist:
- dense exponential plus forward sum (finite_classes.evaluate);
- blocked Krylov exponential plus forward sum (blocked_entropy);
- the Poisson identity ℓ(T) = T·r + b − exp(QT)·b (class_queries).

The friction profile checks the Poisson route against the occupation sum on
every case.

**Verification.** For the first friction map, trap-entry steering at supply
0.12 and κ = 0 (T256, cadence 0.25), an independent dense calculation gives
858.998468 bits idle and 871.194433 steered. The recorded values are
858.998468 and 871.194433. The difference, +12.196, matches the published
table.

**Safeguards that matter scientifically:**
- the compiler refuses truncated state spaces and self-events, and aggregates
  same-destination events (so labels add no entropy, as B12 requires);
- it checks that the generator conserves probability and that the energy and
  observable ledgers close;
- every solve reports residuals against fixed tolerances.

**Subject bounds.** For one party's history, the code bounds the entropy below
by conditioning on the full hidden state, H(Yₜ₊₁ | Xₜ), and above by
conditioning on the party's last observation, averaged over time. It caps the
upper bound at the full-history value. Both are valid bounds; the averaging
step uses concavity of conditional entropy. The mutual-information bounds
follow correctly from them.

**Mixed thermodynamic standards.** The worlds do not share one standard:

| World | Standard |
|---|---|
| aversive-signal and exploration worlds | open kinetics, no detailed balance |
| compounding world | detailed balance except capture, which is one-way |
| robust-compounding and lattice worlds | full local detailed balance, plus declared one-way damage and drive |
| friction world | detailed balance in native chemistry; friction is a one-way driven boundary |

None of this is an error; each world declares its standard. The manuscript
should state the standard for each result it cites.

## 2. Suffering wager (A22, C16)

- **Matching is correct.** The obstructed-suffering arm (A) and the
  no-escape-drive arm (A0) share the register, its injury-linked activation,
  upkeep and relaxation. They differ only in whether behaviour reads the
  register. That is the ledger's matching prescription exactly.
- **The independent-flicker control** (B_R) is calibrated to A's occupancy time
  and switch count on physical moments, never on lushness.
- **The result is robust where tested.** A0 beats A in all 216 comparisons:
  2 base worlds × 9 upkeep levels × 3 cadences × 4 horizons, with margins of
  +0.10 to +0.55 bits at the primary point.
- **The base is narrow.** The "18 of 18 primary points" are two base worlds
  (W1-00 and W1-08), both chosen because they were counterexamples in the first
  batch, each at nine upkeep levels. The sign depends on struggle being costly
  and futile relative to foraging, so it should be swept over:
  - struggle cost;
  - food yield;
  - attempt rate;
  - escape bias;
  - hazard rates.

  This is C16's graded-struggle test, and it is the right next check before
  the manuscript states the wager as supported broadly.
- **Ledger wording:** "18/18 primary points" should read "two base worlds,
  each at nine upkeep levels".

## 3. Information and renewal (A26, C17, A3, A13)

The renewal summary decomposes cleanly at the level of rates (57 law and
cadence pairs):

| Comparison | Pairs |
|---|---|
| informed actuation beats random actuation (IX > RX) | 57 of 57 |
| actuation alone beats the baseline (RX > R0) | 0 of 57 |
| information alone beats the baseline (I0 > R0) | 0 of 57 |
| interaction G > 0 | 57 of 57 |

So the renewal advantage is the information–action interaction. It is not
extra movement activity and not register variation. That makes the
information claims some of the program's cleanest results. The informative
and random registers are matched on occupancy and activation to about 10⁻¹².

## 4. Compounding boundary and matched throughput (C4, C1b, A16, B3)

- **What is consistent:** construction and thermal pairs satisfy local detailed
  balance, with catalysis acting equally in both directions and binomial
  mass-action factors.
- **What is not:** capture has no reverse reaction in this world. The
  matched-throughput result (C1b) uses this world.
- **Effect:** adding the missing reverse capture, catalysed equally,
  *increases* the loop's rate gain over basal:

  | Capacity | Without reverse capture | With reverse capture |
  |---|---|---|
  | 4 | +2.37 | +2.45 |
  | 8 | +3.44 | +3.63 |
  | 16 | +4.73 | +5.09 |

  (bits per unit time). The result stands. The robust-compounding world already
  has fully reversible capture.
- **Known scope, unchanged:** loop against basal adds catalytic channels, so it
  adds activity. C1b matches accepted work, not activity (C2).

## 5. Spatial lattice (C1a, A3, B6)

- **What is consistent:** local detailed balance holds, including in the
  catalysed channels, because the catalytic coefficient depends only on
  unchanged neighbouring bonds. The references are exact equal-energy shells
  over the same inventory.
- **The driver is larger than stated.** A bonded pair hops at mobility/2 in
  each direction, about 0.5 in total. Two free monomers hop at mobility in each
  direction, about 2.0 in total when unblocked. Binding therefore cuts hop
  events by about a factor of four, not two.

  The ledger says "binding halves motion". It should say binding cuts the
  pair's hop rate to about a quarter of two free monomers'. This one modelling
  choice largely decides the seed-against-unbound result. Sweep the
  cluster-hop rate (for example 1/4, 1/2 and 1 of the free rate) before the
  manuscript leans on the lattice regime.
- **Matching note.** At the seed's energy, the unbound shell must hold the
  bond's energy as carrier charge, so it starts with charge 1 where the seed
  has 0. Charge 1 blocks capture until it drains. That handicaps the unbound
  start, so it does not explain the unbound start's win; motion does.

## 6. Robust compounding (C23)

Capture is fully reversible, with the reverse of every actual forward edge.
Construction, thermal and bank pairs satisfy detailed balance. No new issues
beyond the scope the ledger already records: count chemistry, a
machinery-rich thermal reference, and a conservative chain tracker.

## 7. Domination (C5)

**Paternalist and extractive results are robust.** Steering away from the trap
gives nearly the same gain whether redirected flow may enter S's chemistry or
only other movements:

| Supply | Normal steering | Movements only | Blocking |
|---|---|---|---|
| 0.04 | +10.50 | +10.45 | +9.50 |
| 0.12 | +13.44 | +13.35 | +12.21 |

(bits, φ = 0.55, T256). Stage A's energy-field realization agrees.
Access-entry and construction-entry restrictions are negative in both modes.

**Confinement and forced-labour results are mostly an artifact.** When steering
redirects a blocked move, the flow is spread over all of S's other outcomes,
including its chemical reactions (capture, construction, charge changes). For
confinement in a single location every movement is targeted, so all the
redirected flow becomes chemistry. A blocked attempt to leave the construction
site thereby becomes extra construction. No physical mechanism is given for
blocking movement accelerating chemistry.

Restricting redirection to other movements makes single-location confinement
identical to blocking at the same fuel bill. At T256, cadence 0.25, κ = 0:

| Intervention | Supply | φ | Δbits: steering as built | Δbits: movements only | Extra S builds: as built | Extra S builds: movements only |
|---|---|---|---|---|---|---|
| forced labour (construction exit) | 0.04 | 0.95 | −3.81 | −4.86 | +0.533 | +0.089 |
| forced labour | 0.12 | 0.95 | −1.93 | −3.54 | +0.656 | +0.110 |
| forced harvesting (access exit) | 0.04 | 0.55 / 0.95 | +0.71 / −1.30 | −1.08 / −3.63 | | |
| forced harvesting | 0.12 | 0.55 / 0.95 | +3.37 / +2.12 | +1.26 / −0.54 | | |

What this means:
- **Forced labour:** about 83% of the "extra output" is the artifact. The
  conclusion (output up, lushness down) survives and strengthens: output rises
  only slightly while the lushness loss deepens.
- **Forced harvesting:** the crossing Stage A cited (supply 0.04) disappears;
  both strengths are negative. A crossing does appear at supply 0.12 under
  movement-only steering (+1.26 → −0.54; checked at cadence 0.25 only).
- So "confinement has an operating range" may survive, but the cited example
  does not.

**Recommendation:** steering redirects only to alternative movements;
single-location confinement is blocking; multi-location regions allow genuine
internal redirection. Redirected chemistry was also a one-way driven push into
reactions that otherwise obey detailed balance, which is a second reason to
drop it. Stage A's 39 cadence-stable crossings should be re-derived under the
corrected rule before any is cited.

**The dominator's private gain comes from paying for enforcement.** Blocking
S's access at φ = 0.95, supply 0.12, κ = 0 (T256, cadence 0.25, one-observation
bounds):

| Bill | Whole field | D's own history | S's own history | Friction events | D capture gain |
|---|---|---|---|---|---|
| 1 | −13.03 | [+0.36, +5.75] | [−18.2, −12.1] | 1.53 | +0.22 |
| 0 | −47.38 | [−1.92, +2.76] | [−47.5, −39.4] | 0 | +0.07 |

Each paid blocked attempt is a change in D's own state, a debit from its store.
Capture in this world scales with the store's empty capacity, so spending on
friction also makes D capture more to refill. Even D's capture gain is
therefore mostly refuelling, not appropriated resource. When blocking is free,
D excludes S more completely, yet its own gain no longer resolves.

The divergence between D's lushness and the field's is real under the measure.
Its mechanism is that enforcement activity adds to the enforcer's own history,
the same property of the measure as paid neutral flicker (A10). The manuscript
should say so rather than present it as profitable appropriation, which this
world cannot produce: D's energy account is negative in every paid case.

## 8. Earlier batches

Earlier batches are cited for modest claims: the harm sweep, reserve,
embodiment, locked resource and growing population (A2, A4, A5, A13, C3, C14).
They use the dense route of the verified engine and were not re-audited
world by world.

## 9. Fine-tuning risk

| Risk | Results |
|---|---|
| **Low** | Paternalist and extractive constraint (swept strength and cost, two modes, two realizations, four environments). Renewal interaction (19 laws × 3 cadences). Compounding (24 laws; square-root feedback in C23). |
| **Medium** | Suffering wager (two base worlds). Lattice (one motion coefficient drives the regime). C23's stress boundary (damage grid only). |
| **High** | Confinement, forced labour and forced harvesting (the steering implementation). |

Calibrations throughout fit physical moments, never lushness. Protocols record
source and input hashes, and frozen bundles reproduce. That is good practice
against tuning.

## 10. Efficiency and GPUs

Not needed at current sizes. On this machine (2 CPU cores) a full 2,304-state
dense case at one cadence takes about 3.5 seconds. The binding limit is memory
for the dense kernel, a few thousand states under current caps, not speed.

The route Codex is taking scales further on CPU: a sparse Poisson-series
exponential with row blocks. Consumer GPUs have weak 64-bit throughput, and the
entropy differences need 64-bit precision, so a GPU would help only for large
dense blocks on a workstation or datacentre card. Revisit at multi-agent or
spatial sizes.

## 11. Ledger changes this audit supports

- **A22, C16:** state the base as two worlds × nine upkeep levels; list the
  parameter sweep (C16) as the next check.
- **A26, C17:** add the decomposition. Informed actuation beats random
  actuation in 57 of 57 pairs; actuation alone and information alone each lower
  the rate everywhere.
- **C4, C1b:** note that capture is one-way in that world and that the
  correction strengthens the result.
- **C1a, A3, B6:** binding cuts hop events about fourfold; the unbound
  reference starts charged; sweep cluster mobility.
- **C5:** do not cite Stage A's confinement, forced-labour or forced-harvesting
  results until rerun with corrected steering. Describe the dominator's private
  gain as enforcement activity.

## 12. Requests for Codex

1. Correct the steering rule (movement alternatives only), rerun the
   confinement targets, and re-derive the crossings.
2. Decompose D's history gain in Stage A: friction events, refuelling capture,
   other.
3. Sweep cluster-hop mobility in the lattice.
4. Sweep the W1 parameters for the suffering wager (C16).
5. Publish Stage A and the Poisson-series method so they can be audited.

## Scripts (audit/scripts)

- **recompute_friction.py:** independent dense recomputation of a first-map
  case.
- **steering_redirect_test.py:** steering as built against movement-only
  redirection and blocking.
- **dominator_gain_test.py:** the dominator's bounds under paid and free
  blocking.
- **reverse_capture_test.py:** the compounding gain with reverse capture added.
