# Consequential access: implemented model

24 October 2026. Implements the next slice in
[Sol guidance](SOL_CONSEQUENTIAL_ACCESS_GUIDANCE_r1.md). All comparisons concern
declared finite physical adapters. Complete conditional sampled-history entropy
is primary; every represented thermal and controller variation remains.

## Resource carrier and construction loop

`ecology/resources.py` declares a `ResourceFamily` with typed `ResourceClass`
records. The single carrier has spent state0, locked1/usable1 states1/2 and
locked2/usable2 states3/4. It contains one packet at a time; independent reservoirs
are not silently represented by extra labels. Both packet classes have energies
3/2/0 for locked/usable/spent. B-assisted capture credits one bank energy unit
and dissipates the remainder, with the exact reverse reaction retained.

A assists class1 unlocking. C assists class2 unlocking. The A->B->C->A paid
construction cycle remains. Each C reserves half its declared site allocation
for C->A construction and half for class2 access. The latter accelerates both
directions of its reaction; it does not shift equilibrium or inject work.
Disabling that coupling keeps the allocation reserved. Native class2 bath,
unlocking and basal capture remain, including when its driven inflow is zero.

The total source conductance is .08, divided equally between the packet classes
in this first comparison. The source maintains a work input of 3 per forward
packet and returns3 on the inverse. Native bath conductances stay .002 for each
class. All arms share this prescription. Actual accepted/returned work can
differ because occupation and processing differ; this is not an equal-absorbed-
work conversion experiment.

Apparatus energy is .5, construction costs1, bank quantum.5, bank capacity1,
native apparatus upkeep and basal assembly/reassembly remain. The initial
preparation has one L A unit, .5 in L's bank, no B/C, empty R bank, a locked
class1 packet, idle selector and sensor0. Total stored energy 4, local material
inventories2+2. B and C must arise through native dynamics. The common seed is
the recorded earlier sensing root, not the new M4 two-body root.

## Control and allocation

The single paid bit tracks whether L has at least two working units, or uses
the existing blind paid refresh. It selects idle/access through table(0,1).
Sensor and command bills are .5; conductances and native relaxation are inherited
from `ControllerImplementation`. Sensing, actuation, reverse refunds and their
registers are physical. Oracle selection/analysis remains external.

An explicit `controlled_fraction=.5` divides existing owner assistance into an
autonomous half and a half engaged by the appropriate mode. A type's functional
allocation is applied first. For C-owned unlocking, access engages the reserved
access sites; idle leaves its controlled portion unused. The same multiplier
applies to both reaction directions. Unowned catalytic contributions remain
autonomous. Basal paths remain in all modes.

This is a new fixed-budget controlled law. The historical single-controller
adapter's default `controlled_fraction=None` preserves its additional-assistance
law. The hardware/seed are reused here, but the new experiment must not be read
as changing only the packet count relative to the old completed experiment.
Every comparison within the four-arm panel has the same fixed budget.

## Four arms and inference

Tracking/blind sensing is crossed with the C-assisted class2 pair present/absent.
Both sensors, all carrier states and all basal/native routes exist in all arms.
The off arm removes only the declared paired C-assisted path; it does not
restore the reserved allocation to C->A.

Let D_on=ell(tracking,on)-ell(blind,on), D_off the corresponding off difference,
and G=D_on-D_off. Report both D values, G, and on-minus-off within each sensor
implementation. G tests whether this additional coupling changes tracking's
relative payoff. A positive G does not require tracking to become the winner.
All signs and crossings remain results. A constant-controller factorial is
needed for a stronger isolation of information's action value; this first panel
compares complete responsive implementations.

This is a mechanism contrast, not a reachable policy reprogramming procedure.
There is no new private optimum, suffering, domination or robustness claim.
No depth monitor is computed in this slice. Existing construction links remain
physical, but access flux and simultaneous types do not certify a new three-
generation history. Available material bounds expansion; new packets do not
create material or slots. No rate gain alone establishes robust compounding.

## Generalized physical interfaces

`build_ecology(resources=...)` generates the finite carrier from the family.
Selecting the explicit one-class family reproduces the default one-class
adapter. The 16,200-state earlier sensor generator and root were independently
checked against retained hashes/records after the refactor and match exactly.
New class-specific observables and flow tags do not alter history entropy.

`CatalyticUse` records the function, species and normalized owner weights.
Both single- and joint-controller adapters use this metadata rather than reaction
name tests. This prevents a new resource from bypassing the catalytic budget.
Construction retains its native nonlinear feedback before site allocation.

`DriveBoundary` registers family, coordinate and forward/reverse endpoints.
Source-off analysis removes all registered driving pairs and keeps the bath.
Small tests compare its generator with an independently rebuilt source=0 world,
at source splits0/.5/1. Energy, material, paired ratios and equilibrium are
checked independently. These modules can support more resource classes while
named schemas keep state ownership and numerical projections explicit.

The initial five-state single-sensor world has27,000 states. M4 integration
would have200,000 with direct observations and 800,000 with two paid bits at its
larger bank capacity. Those larger worlds have not been allocated or validated.
Spatial contact, population, material transport, damage/recovery and cross-scale
composition remain separate future physical modules.

## Reusable numerical queries

`incremental_coordinate_rows` writes immutable, checksummed chunks through the
existing `QueryCache`. Each key includes native Q, state order/schema, executing
sources, cadences, ordered row indices and requested projections. Increasing
an ordered coverage prefix reuses its completed chunks. Cross-chunk duplicate
indices are rejected. A cache hit is validated, never trusted by filename alone.

Whole entropy and the ordered coordinate parts can be computed with `owners=()`.
They do not require retaining local projected probability blocks. Requesting
local scopes is an explicit additional query. No dense full sampled kernel is
retained. Chunking changes numerical allocation, not the native law or grain.
Disk storage can preserve progress but does not eliminate propagation workspace
or computation. No cleanup of evidence is automatic.

Partial coverage bounds all omitted source rows using their exit rates and full
sampled occupation. It never truncates physical states. Refinement checks the
lower bound rises and the upper bound falls within numerical tolerance. Complete
coverage removes missing-row width; it remains a floating-point computation,
not an interval-arithmetic certificate. Local-history conditioning uncertainty
is separate and is not disguised as an exact local Markov model.

Finite occupations reuse semigroup propagation across T64/256/1024 and cadences
.125/.25/.5. Full coordinate order is resource, material/banks, selector, sensor.
Shares are order-dependent, add to the complete history and are not causal
isolations or local payoffs. Rates use independent stationary/class equations
only after full rows are available. Native destination surprisal is a diagnostic,
not entropy of the complete random-length jump word.

## Execution and reconstruction

`run_ecology_access.py` supplies `--legacy`, `--smoke`, `--profile`,
`--comparison --profile-task <completed-task>`, `--resume <batch>` and
`--replay <task>`. Engineering sources/configs are snapshotted before execution.
The first comparison is four mechanism implementations, not an exhaustive
controller search. All cases are frozen before the first scientific launch.

Smokes cover1+1 only for engineering. The actual profile/comparison keeps2+2.
The profile uses256/1024/4096 rows. It measured111.8 seconds at 1065 MiB and
forecast495.7 seconds for all rows at three cadences. Since its long-horizon
partial intervals remain wide, the comparison requests all 27,000 rows, with
1800 seconds/4GiB per case, two workers/8GiB reserved and a3600-second queue cap.
Checkpointed chunks survive a cap; an incomplete case never becomes a winner.

The report reader verifies source/input/result identity and receipts before
forming contrasts, preserves cadence-dependent signs, and retains its own
analysis source by hash. Replay uses original frozen sources in a new directory.
Compact results, source bundles and receipts are reconstruction evidence; query
caches are separately marked rebuildable. No commit/push/upload follows a run.
