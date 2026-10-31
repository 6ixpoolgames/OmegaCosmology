# J — joint activity/net-work comparator: physical design review

31 October 2026. Review completed locally under the user's “Proceed”.
**No new model was compiled, calibrated or history-scored.** This report
recommends one bounded physical pilot, not dispatch of the three-source study.
The results of run A and all earlier unsuccessful rotor attempts stay unchanged.

## Finding

The present R1 source-fed relaxation family has one conductance and two
matching targets. Its two selected points cannot be combined into one joint
control. A second explicitly modeled relaxation route can provide a physically
meaningful second parameter **without** a new clock, register, energy store,
source, material species or adjustment to the common basal thermal rates.

This makes J ready for a bounded qualification pilot after review. It does not
establish that the joint target lies in this family's attainable set. Two
parameters neither imply independent responses nor guarantee a solution.
Do not describe J as matched, feasible or scientifically run at this stage.

## Native world and fixed quantities

Use run A's interpreted R1 productive/ablated laws and its exact built root.
The retained model has five coordinates: two active constituents, their bond,
one three-state carrier, and a five-tick bank. There are 75 reachable states.
The carrier's spent, locked and usable states have energies 0, 3 and 2.
Each bank tick is .5 energy. Bond formation changes energy by −.5; the
existing paid/basal formation and dissolution channels remain untouched.

All arms retain the same Hamiltonian, temperature beta=1, material inventory,
allowed states, root, construction/capture/upkeep rules, and boundary source.
At the anchor the source conductance is .08 and source forward/reverse work
is ±3. A future source sweep is explicitly a family of boundary laws; within
each contrast the prescription is identical. It is not a chooser's free
option and does not establish cancellation of the unmodeled exterior.

The useful arm retains `unlock_motif` and has no added loads. The plain
ablation removes that paired motif-unlock reaction only. The proposed load
control is the ablation with the following **two additional, reversible,
bond-gated** catalytic relaxation routes:

| Parameter | Physical conversion while bond=1 | Forward bank increment | Forward heat to bath | Direct external work |
|---|---|---:|---:|---:|
| k_L | locked carrier 1 -> spent carrier 0 | 0 | 3 | 0 |
| k_U | usable carrier 2 -> spent carrier 0 | 0 | 2 | 0 |

Run A already implements the first. The existing generic
`attach_resource_load` factory can express the second with a distinct rule
identifier; `load_rewards` aggregates their physical ledgers. Channel-level
readouts must additionally retain their separate bills and refunds.

Both routes have distinct physical endpoints from one another. Their
reverse reactions absorb their respective heat from the bath. They are not
one-way disposals or distinct labels on identical outcomes. Each can be
parallel to an existing basal bath route: its rates must aggregate into Q
before sampled-state history entropy is computed. Extra labels add no entropy.

## Why this is costed, and its limits

For a conversion releasing d energy, the compiler's native rates, with no
degeneracy change, are

`q_forward = k exp(beta*d/2)`, `q_reverse = k exp(-beta*d/2)`.

Therefore their ratio is exp(beta*d), with heat ±d and no hidden work. The
same assembled catalyst gates both directions; no working bond means no
added catalytic event. Source-off Gibbs detailed balance is preserved
analytically for each pair on the unchanged allowed sector. A pilot must
still check the compiled ledger/material pairs and numerical equilibrium.

Construction of the original bond/apparatus has its existing physical costs.
This is **not** an upgraded model of obligatory maintenance: R1 still permits
basal reconstruction, reversible fluctuations and its original upkeep law.
No new manufacturing cost for choosing a catalytic chemistry is asserted.
The contrast changes an intrinsic coupling parameter between laws. Any
claim about implementing or changing that chemistry within one law needs
separate paid machinery.

These are direct dissipation routes, not direct bank charging or construction.
Nevertheless the usable-state reverse can replenish usable fuel; the
locked-state reverse can replenish locked fuel; both alter capture and
apparatus occupancies indirectly. The comparator must be called a **load
control**, with those consequences reported. It cannot be guaranteed to
open nothing, destroy all capability, or be purely useless. No after-the-fact
veto based on an inconvenient functional or lushness sign is permitted.

## Matching problem and physical gate

At the source-on anchor the useful arm's retained targets are:

- physical state-jump rate: .18240477065575628 events/time;
- **net** external work: .023797683097786553 energy/time.

Gross accepted and returned source work are .0807189288942378 and
.05692124579645124 energy/time. They are not the net-work target. Every
candidate must report all three quantities, total and channel-specific heat,
and finite T64 totals, even though the match is stationary.

Let `m(k_L,k_U) = (pi q_exit, pi w_source)` for the actual stationary pi of
the whole compiled model. For this source,
`pi w_source = 3*.08*(P(carrier=0)-P(carrier=1))` at the anchor.
Changing either load changes pi, so neither target is independently linear
in its conductance. Do not assume an interpolation between run A's two old
points attains both targets, or freeze the productive pi while changing Q.

Before fitting, inspect the physical attainable map. A numerical sensitivity
matrix can be obtained by differentiating stationarity,
`(d pi) Q = -pi (d Q)`, `(d pi) 1 = 0`, or checked finite differences.
Report dimensionless moment responses, singular values/conditioning and
whether the target lies inside the sampled image. A rank-deficient local
response is not a proof of global infeasibility; a coarse map is not a proof
of feasibility. The bounded pilot ends with an observed boundary or an
actually evaluated qualified fit, not a solver's success flag alone.

Suggested qualification gates, frozen before evaluation:

1. Unchanged common physical grammar, endowment and source; only the two
   declared load pairs differ from the ablation. Check both directions and
   all affected states, material and energy, not just rule prose.
2. Stationary residual <=1e-10; finite first-law and source-off equilibrium
   checks <=1e-8, with conditioning/scale reported. No clipping tiny reverses.
3. Source-on stationary net load heat, net source work and finite T64 net
   load heat each >1e-8 in their typed units. Record each route separately:
   if either is a net heat importer, do not conceal it inside a net-positive
   total or call both routes net consumers. The minimal two-consuming-load
   interpretation requires positive stationary net heat for both nonzero routes.
4. Source-off stationary source work and each load's net heat within 1e-8
   of zero. Initial-store finite discharge is not sustained payment.
5. **Both residuals** in the *same* evaluated model satisfy
   `abs(error) <= 1e-10 + .001*abs(target)` for the appropriate physical
   quantity, as in run A. Also report achieved residuals, not only pass/fail.
6. Preserve all tested points, failed fits, initializations and maps. No
   entropy, rate, bias or desired ranking is available to the calibrator.

The nonzero-load/current condition narrows the qualifying family; if it
prevents a joint fit, that boundary is the result. A thermal importer is
not silently reclassified as net resource consumption. Changing this
interpretation later would require an explicitly different comparator.

## Proposed pilot and budget, not executed

At source .08 only: k_L,k_U in [0,2], with zero represented by omitting that
extra rule rather than compiling a zero-conductance reaction. Start with
the fixed grid {0,1e-5,.001,.01,.1,2} squared. Evaluate source-on and source-off
physics for its 36 points each. Reserve at most 48 additional source-on fit
probes and up to eight source-off/finiteness checks, plus four fixed
productive/ablation references: at most 132 compiled physical evaluations.
No automatic change of bounds or alternative family if these fail.

One worker; 300 seconds, 1 GiB process memory, 64 MiB output; preserve the
host RAM reserve. The existing single-load physical stage used 40 evaluations
in 9.68 seconds and the complete prior stage peaked near 122 MiB. The new
model adds no coordinates or supported state edges beyond existing bath
routes, so 75 states are expected, **subject to checking**, with a hard
200-state ceiling. A dense 75x75 float64 matrix is 45,000 bytes. These are
engineering estimates, not a measured new benchmark. No dense matrices or
sample trajectories need be retained.

The expected computational footprint is comfortably local. The primary
uncertainty is physical attainability and qualification, not RAM or disk.
State-count growth, changed native semantics, provenance failure, failed
energy gates or a time/memory cap stops the pilot and retains its output.

If it qualifies, stop at its physical report, with frozen selected inputs
and calibration hash. A later authorized history stage can evaluate the
three cadences and T16/64/256/1024, full crossing profiles, rate/bias, and
independent endings. It must retain finite work/activity mismatches. The
additional source strengths .04 and .16 are sensible prospective companion
points, but their targets must be recalculated under their own common
boundary laws and separately qualified; no result at .08 licenses them.

## What J could establish

A qualified joint match would compare a useful pathway and a specified load
family with equal mean stationary jumps and mean net source work to the
declared tolerances. It would not match gross work, finite totals, occupancy,
event timing, event destinations, path probabilities or exterior histories.
Those remaining differences are physical consequences, not errors to remove
from lushness. Either sign or multiple crossings are legitimate observations.

It would be a stronger nuisance-control comparison than run A, not a unique
organization-only causal decomposition, a gas baseline, proof of deep
compounding, an ethical result or a universal ranking. If the proposed family
cannot meet the joint target, report that bounded physical limitation and
score no unqualified comparison. Do not search histories for a replacement.

## Implementation recommendation

**Proceed next with the anchor's capped physical qualification pilot, if the
author chooses to continue.** Reuse the existing load factory and native
thermodynamics; add an explicit two-load builder and per-route accounting
checks rather than clone an old success-oriented report generator. A fresh,
outcome-neutral report must handle no fit, importer, cap, unresolved and
qualified outcomes. Do not retune common basal noise, erase reverse channels,
rescale the clock, change the score or launch the spatial pilot automatically.
