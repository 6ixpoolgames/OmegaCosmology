# R2 integrated construction and paid-control smoke

27 October 2026. Complete locally; smoke checkpoint only. No wider map or push.
Read the [existing-R2 audit](../../models/r2-integrated/AUDIT.md) and
[specification](../../specs/R2_INTEGRATED_SMOKE_r2.md) with these results.

## Engineering result

Five laws, two cadences and three horizons:30 finite profiles,324 states per law.
Every paired comparison validates the actual common root, energy, inventories,
boundary prescription, observation and window. Native source-off balance and
complete-history identities pass. Maximum first-law residual 7.99e-15;
maximum query/propagation residual 1.79e-12. The whole-workspace check
passes 159 tests and exact baseline evidence reproduction.

Run time 128.322s; capped-worker peak
148.55MiB, below900s/1GiB/64MiB.
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
| productive | 16.068975 | 11.103608 | 8.113952 | 0.073384 | 0.236463 | 0.0010333026 |
| no_construction_assistance | 15.778547 | 11.062270 | 7.662068 | 0.000000 | 0.222156 | 0 |
| no_secondary_access | 15.717150 | 11.186640 | 7.957172 | 0.075317 | 0.000000 | 0 |
| neither_link | 15.434009 | 11.139923 | 7.592163 | 0.000000 | 0.000000 | 0 |
| matched_rotor | 16.068977 | 11.180951 | 7.950602 | 0.075632 | 0.000000 | 0 |

The productive law's A uptime is
29.152952; C uptime is
8.188981. Raw forward/reverse
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
| no_construction_assistance | 4 | +0.01338490 | +0.01126520 |
| no_construction_assistance | 16 | +0.18248320 | +0.15586743 |
| no_construction_assistance | 64 | +2.13213669 | +1.82997457 |
| no_secondary_access | 4 | +0.02612163 | +0.02188862 |
| no_secondary_access | 16 | +0.23158669 | +0.19298036 |
| no_secondary_access | 64 | +2.22801505 | +1.84865171 |
| neither_link | 4 | +0.03903355 | +0.03275545 |
| neither_link | 16 | +0.41070893 | +0.34619931 |
| neither_link | 64 | +4.32717021 | +3.65330596 |
| matched_rotor | 4 | -0.18487677 | -0.16646130 |
| matched_rotor | 16 | -0.61176469 | -0.55949666 |
| matched_rotor | 64 | -1.06072418 | -1.07873139 |

Rates and offsets remain diagnostics in retained profiles. These same-root
between-law contrasts can have different stationary rates; they are not choices
of an embodied optimizer under one law. No thermal spatial baseline is claimed.

## Work/activity control

Calibration status: **not_matched_in_bounded_search**. It was saved before history evaluation.
Target Nbar=16.068975493, accepted work=
11.103607853. Selected rotor stroke=
1.00058791e-05, relaxation=
0.00926663581. Residual(control-target): Nbar=
+1.62541759e-06, accepted work=
+0.0773428342.

Each moment must pass absolute1e-8+relative0.001 tolerance. The control is
retained whether it matches or not. No tolerance widening or path conditioning
occurred. A near event-count match with a work mismatch cannot demonstrate an
advantage independent of both work and activity. The bounded search also does
not prove that a matching physical control is impossible. The rotor changes
reserve occupancy and reverse flows; even an exact two-moment match would not
identify a unique organization-only contribution.

AtT64 the rotor candidate has
3.95679613e-05 paid stroke/reverse events versus 0.550491207 thermal
forward/reverse events; paid fraction=7.18724e-05. Most fitted rotor events are thermal; this does not supply a predominantly paid-cycling comparator.
The ID `matched_rotor` is a requested role, not a matching certificate. The
finite score remains a physical result of this law; the rotor gain cannot
automatically be attributed to energy-consuming nonproductive work.

The productive-minus-rotor limiting rate is
+0.0697279248 and +0.0558917295bits/time at the two cadences. The
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
The [preceding integration](../r2-integrated-2026-10-27/REPORT.md) remains intact with all profiles and its first reporting-error attempt. This revision changes B's stoichiometry to energy transduction, with a bank-space guard. It tests a distinct second function; it does not discard or relabel the earlier result.
