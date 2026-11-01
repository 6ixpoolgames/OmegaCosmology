# Version C spatial prototype: engineering result

1 November 2026. Physical-only benchmark; no lushness scores or rankings.

## Outcome

The preferred 2x3 world fits exact enumeration and one exact sampled kernel.
All 3672 structural/chemical states are reachable from the unbonded
root under the implemented law, with 26248 marked transitions.
The final benchmark took 43.13 seconds and peaked at
946.41 MiB under a 600-second / 2-GiB Job Object cap.
No cap was hit. One .25-cadence kernel took 8.90 seconds;
row-sum error 4.44e-16. No entropy was calculated.

Source-off equilibrium has one connected sector, edge-flow residual
3.39e-20. The largest finite first-law
residual across both roots and horizons is
2.8e-14.
Material inventories are executable. This checks the declared chemistry,
not physical faithfulness to microscopic chemistry or a thermal gas.

## What the physical loop currently does

At T64 from two stored charges, A-assisted B assembly contributes
0.229642 expected forward events,
versus 0.123367 basal B births.
Enabled capture has 0.237526 forward and
0.157407 reverse events: net charge delivery
0.080119.
Both enabling links are actually used; the assisted fraction of B births is
65.05%.

This does not establish sustained self-funding. Final bank charge is
1.521261, down from2. Initial charge remains substantial.
From zero initial charge, assisted B births are only
0.000201, and final bank charge is
0.096322. Starting charges change the endowment: these roots are
preparation diagnostics, never presented as common-present options.

First B construction occurs by T64 with probability
0.210073 from the charged root. Expected A and B
occupation times are 4.385288 and
5.923503; simultaneous occupation
1.831737, and contact occupation
1.623168. The contact fraction of simultaneous
occupation is 88.61%.
Thus the small geometry brings coexisting dimers into contact most of the time.
It supplies native motion but may be too cramped for a durable separated-versus-
connected arrangement comparison. Finite contact exits and occupation are
reported unconditionally; their ratio is not an uncensored episode lifetime.

## Physical and interpretive scope

A and B are mobile dimers assembled from the same four conserved constituents;
aa/bb/ab compete. A locally catalyzes reversible B assembly; B catalyzes
reversible capture into one shared three-conformation storage molecule carrying
0/1/2 charges. One carrier has spent/locked/usable conformations. The chemical
medium is rapidly mixed. Fuel transport, bath/source histories and controller
hardware are not resolved. The stage implements no preparation pulse or enacted
option comparison. Bond dissociation refunds charge in this stipulated chemistry;
it is not irreversible damage or paid repair of irreversible loss.

Positive assisted event counts establish use of a catalytic channel. They do not
prove causal ancestry, capture-financed descendants, long-run repayment, robust
compounding or an ethical correspondence. No A-ablated law was substituted for
the intended same-law alternatives. No coefficients were searched on lushness.

## Execution history and retention

All three completed physical benchmarks are retained. r1 used the ambiguous
inventory description of two storage molecules. That description did not account
for the statistical multiplicities of independent charge-bearing molecules.
r2 corrected the definition to one three-conformation storage molecule, preserved
the energetic transition law, and added simultaneous-occupation output. r3 adds
separate basal A/B/ab birth and dissolution counters; it changes no physical
rates from r2. Snapshots bind each result to its executed code. Earlier r1 is
retained as a superseded physical description, not separate confirmatory evidence.
No failed cap or unfavourable physical result was removed. A launcher import
issue was fixed before any worker started by reusing the existing Job Object
wrapper rather than introducing an unavailable monitoring dependency.

## Readiness

Numerical implementation and the first enabling links are ready for further
physical qualification. Scientific C1-C3 option runs are not yet implemented.
Before those runs, define paid preparation operations with their exterior
command scope; assess a longer physical window to determine whether capture
actually maintains the loop; and decide whether the crowded geometry can answer
C2. These are physical questions, without a promised lushness sign. No arbitrary
rate difference or irreversible partition should be introduced to secure one.

## Reproduction

Run scripts/benchmark_spatial.py with a fresh output directory using the repository
Python environment and PYTHONPATH=src. It snapshots source before launching one
capped worker. INPUTS.json records source hashes; each SNAPSHOT.zip preserves the
executed testbed and runner. Compare benchmark-r3/MODEL.json for exact rates and
coordinates, PHYSICAL.json for raw results and RECEIPT.json for actual caps.
The specification is research/platform/specs/V42C_SPATIAL_PROTOTYPE_r1.md.

Validation: all216 repository tests pass on the final source (112.76seconds);
the five spatial tests cover the tiny alphabet/equilibrium, paid local
assistance and reverse, intact dimer movement, capture and spatial reflection.
Focused lint checks pass. All executed source snapshots verify against their
INPUTS.json hashes. No publication was performed.
