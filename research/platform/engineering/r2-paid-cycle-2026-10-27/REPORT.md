# R2 construction and physical control smoke

27 October 2026. Complete locally; smoke checkpoint only. No wider map or push.
Read the [existing-R2 audit](../../models/r2-integrated/AUDIT.md) and
[specification](../../specs/R2_PAID_CYCLE_CONTROL_r1.md) with these results.

## Engineering result

3 laws, two cadences and three horizons:18 finite profiles,324 states per law.
Every paired comparison validates the actual common root, energy, inventories,
boundary prescription, observation and window. Native source-off balance and
complete-history identities pass. Maximum first-law residual 9.33e-15;
maximum query/propagation residual 1.35e-12. The whole-workspace check
passes 163 tests and exact baseline evidence reproduction.

Run time 109.903s; capped-worker peak
146.18MiB, below900s/1GiB/64MiB.
Explicit module ports bind resource carriers, bank, construction, capture,
secondary access and rotor. Bindings do not create physical events.

## Physical chain and competing use

A is constructed using the common bank and assists B/C construction. B and C
compete for the same conserved precursor. B transduces secondary energy: locked3 becomes usable2 plus.5 stored in the bank and.5 heat. A instead unlocks its carrier with1 heat and no bank return. Their functions and stoichiometries differ.
C accelerates primary capture. Both carriers keep their native
stochastic paths in every arm. Thermal breakdown and paid/native rebuilding
remain, so payment is not assumed logically necessary for persistence.

T64 physical readouts at cadence.25:

| Law | Nbar | Gross accepted work | B uptime | Assisted B builds | B release events | Continuity witness probability |
|---|---:|---:|---:|---:|---:|---:|
| productive | 16.126464 | 11.099775 | 8.137078 | 0.073142 | 0.236450 | 0.00099426227 |
| no_secondary_access | 15.768398 | 11.181598 | 8.000903 | 0.074707 | 0.000000 | 0 |
| paid_cycle_candidate | 16.130310 | 11.169743 | 8.100991 | 0.073426 | 0.000000 | 0 |

The productive law's A uptime is
29.229541; C uptime is
8.183715. Raw forward/reverse
construction, capture and rotor counts travel with each full profile. Presence,
event counts and the witness are distinct quantities.

The conservative witness requires a paid A build, A-assisted B build, B-assisted
release and secondary capture, aborting if the necessary current A/B instance
or released carrier disappears. This supplies an instance-continuity check for
that sequence, not depth-three ancestry, causal necessity or energy-packet lineage.
The physical chain can occur on paths the conservative witness does not count.

## Lushness profiles

Productive minus comparator in complete-history bits; all physical events count.

| Comparator | Horizon | cadence.25 | cadence.5 |
|---|---:|---:|---:|
| no_secondary_access | 4 | +0.02613390 | +0.02189113 |
| no_secondary_access | 16 | +0.23306137 | +0.19405884 |
| no_secondary_access | 64 | +2.25962084 | +1.87263327 |
| paid_cycle_candidate | 4 | +0.01342983 | +0.01119264 |
| paid_cycle_candidate | 16 | +0.03230151 | +0.02737335 |
| paid_cycle_candidate | 64 | +0.01528832 | +0.02763421 |

Rates and offsets remain diagnostics in retained profiles. These same-root
between-law contrasts can have different stationary rates; they are not choices
of an embodied optimizer under one law. No thermal spatial baseline is claimed.

## Work/activity control

Calibration status: **not_matched_in_bounded_search**. It was saved before history evaluation.
Target Nbar=16.126463608, accepted work=
11.099774886. Selected parameters:
charge=0.000161510239, reset=0.0796483945. Residual(control-target): Nbar=
+0.00384590137, accepted work=
+0.0699676759.

Each moment must pass absolute1e-8+relative0.001 tolerance. The control is
retained whether it matches or not. No tolerance widening or path conditioning
occurred. A near event-count match with a work mismatch cannot demonstrate an
advantage independent of both work and activity. The bounded search also does
not prove that a matching physical control is impossible. The rotor changes
reserve occupancy and reverse flows; even an exact two-moment match would not
identify a unique organization-only contribution.

AtT64 the rotor candidate has
0.447436271 paid stroke/reverse events versus 0.174247054 thermal
forward/reverse events; paid fraction=0.719717. Most fitted rotor events use the paid cycle; this alone does not establish work/activity matching.
The ID `paid_cycle_candidate` is a requested role, not a matching certificate. The
finite score remains a physical result of this law; the rotor gain cannot
automatically be attributed to energy-consuming nonproductive work.

Both rotor stroke and reset are bank-paid; a forward closed cycle draws1 energy
unit. The native thermal pair remains at conductance.003 in every arm/candidate.
AtT64 the candidate withdraws 0.0991026588 bank energy gross, refunds
0.124615476, and pays -0.0255128177 net. The conservative first-charge
then-paid-reset witness probability is 0.000215759958. This is a passive
query on the rotor, not an additional entropy coordinate or an all-cycle count.


The productive-minus-rotor limiting rate is
+0.0431887781 and +0.0375216932bits/time at the two cadences. The
finite profile and long-horizon diagnostic are reported separately in this window.
No later horizon was run; a predicted repayment crossover is not an observed
crossover. T64 moment matching also says nothing about equality of stationary
work or event rates.

## What this checkpoint establishes and leaves open

The substrate can represent and measure a paid construction link, a distinct
downstream resource function, competition for a construction precursor, and a
paid non-enabling control under common resource prescriptions. Physical readouts
and complete histories are reported together. This is a bounded mechanism
fixture; its observed signs neither establish a universal ranking nor a theory
failure. Paid work, event activity and temporal resolution remain explicit.

The next decision should use the measured chain incidence and matching residuals:
improve the physical control family if needed, or size a limited cost/yield map.
No such expansion has been run. Spatial disorder, growing populations, third
generation, lineage of captured energy, paid sensing and ethical correspondence
remain separate extensions.

## Provenance and initial attempt

[Retained inputs/results](retained/RESULT.json), [comparison contracts](retained/COMPARISON_CONTRACTS.json),
[calibration](retained/CALIBRATION.json), [validation](VALIDATION.json) and
[quality axes](QUALITY.json) accompany the source snapshot and byte manifest.
The [preceding integration](../r2-transduction-2026-10-27/REPORT.md) remains intact with all profiles. This revision adds a paid rotor reset in every arm and fixes the thermal baseline; only paid charge/reset barriers are calibrated. The old transduction fixture's default fingerprint is unchanged.
