# R2 integrated construction and paid-control smoke

27 October 2026. Complete locally; smoke checkpoint only. No wider map or push.
Read the [existing-R2 audit](../../models/r2-integrated/AUDIT.md) and
[specification](../../specs/R2_INTEGRATED_SMOKE_r1.md) with these results.

## Engineering result

Five laws, two cadences and three horizons:30 finite profiles,324 states per law.
Every paired comparison validates the actual common root, energy, inventories,
boundary prescription, observation and window. Native source-off balance and
complete-history identities pass. Maximum first-law residual 1.24e-14;
maximum query/propagation residual 1.72e-12. The whole-workspace check
passes 159 tests and exact baseline evidence reproduction.

Run time 128.159s; capped-worker peak
148.98MiB, below900s/1GiB/64MiB.
Explicit module ports bind resource carriers, bank, construction, capture,
secondary access and rotor. Bindings do not create physical events.

## Physical chain and competing use

A is constructed using the common bank and assists B/C construction. B and C
compete for the same conserved precursor. B accelerates secondary resource
unlocking; C accelerates primary capture. Both carriers keep their native
stochastic paths in every arm. Thermal breakdown and paid/native rebuilding
remain, so payment is not assumed logically necessary for persistence.

T64 physical readouts at cadence.25:

| Law | Nbar | Gross accepted work | B uptime | Assisted B builds | B release events | Continuity witness probability |
|---|---:|---:|---:|---:|---:|---:|
| productive | 16.219891 | 11.077911 | 7.984446 | 0.075046 | 0.349205 | 0.0013528883 |
| no_construction_assistance | 15.919747 | 11.039689 | 7.605890 | 0.000000 | 0.331700 | 0 |
| no_secondary_access | 15.717150 | 11.186640 | 7.957172 | 0.075317 | 0.000000 | 0 |
| neither_link | 15.434009 | 11.139923 | 7.592163 | 0.000000 | 0.000000 | 0 |
| matched_rotor | 16.219892 | 11.180950 | 7.950604 | 0.075632 | 0.000000 | 0 |

The productive law's A uptime is
28.947482; C uptime is
8.228024. Raw forward/reverse
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
| no_construction_assistance | 4 | +0.01351389 | +0.01134906 |
| no_construction_assistance | 16 | +0.18794760 | +0.16013560 |
| no_construction_assistance | 64 | +2.17986932 | +1.86684447 |
| no_secondary_access | 4 | +0.03503778 | +0.02775324 |
| no_secondary_access | 16 | +0.28373210 | +0.22300863 |
| no_secondary_access | 64 | +2.68737861 | +2.12041866 |
| neither_link | 4 | +0.04794969 | +0.03862007 |
| neither_link | 16 | +0.46285434 | +0.37622758 |
| neither_link | 64 | +4.78653376 | +3.92507291 |
| matched_rotor | 4 | -0.25184908 | -0.22742692 |
| matched_rotor | 16 | -0.87006104 | -0.80279328 |
| matched_rotor | 64 | -1.90250693 | -1.95184589 |

Rates and offsets remain diagnostics in retained profiles. These same-root
between-law contrasts can have different stationary rates; they are not choices
of an embodied optimizer under one law. No thermal spatial baseline is claimed.

## Work/activity control

Calibration status: **not_matched_in_bounded_search**. It was saved before history evaluation.
Target Nbar=16.219891275, accepted work=
11.077910741. Selected rotor stroke=
1.00006022e-05, relaxation=
0.0117133309. Residual(control-target): Nbar=
+8.67655707e-07, accepted work=
+0.103039414.

Each moment must pass absolute1e-8+relative0.001 tolerance. The control is
retained whether it matches or not. No tolerance widening or path conditioning
occurred. A near event-count match with a work mismatch cannot demonstrate an
advantage independent of both work and activity. The bounded search also does
not prove that a matching physical control is impossible. The rotor changes
reserve occupancy and reverse flows; even an exact two-moment match would not
identify a unique organization-only contribution.

The rotor candidate is almost entirely thermal: atT64 it has
0.0000402183 paid stroke/reverse events versus0.701405269 thermal forward/reverse
events. The fitted stroke conductance is near its lower bound. This does not
supply the intended comparator whose extra activity is sustained mainly by paid
cycling. The ID `matched_rotor` is a requested role, not a matching certificate.
Its higher finite score remains a physical result of this law; it cannot be
attributed specifically to energy-consuming nonproductive work.

The productive-minus-rotor limiting rate is nevertheless positive:
+0.062575965 and+0.043752725bits/time at the two cadences. The finite profile
and long-horizon diagnostic therefore differ in this window. No later horizon
was run; a predicted repayment crossover is not an observed crossover. T64
moment matching says nothing about equality of stationary work or event rates.

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
An initial attempt calibrated and scored the first case, then stopped on a
runner timing-field typo. Its source, fit, first profiles and receipt are retained
under initial-attempt/. Correcting worker_seconds changed no physical law,
parameter bounds, tolerance or score. The same smoke then ran from a fresh snapshot.
