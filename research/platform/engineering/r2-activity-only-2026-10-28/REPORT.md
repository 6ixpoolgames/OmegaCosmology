# R2 â€” Equal-barrier activity-only control

Completed locally 28 October 2026 from the 27 October execution snapshot. Bounded
engineering check only; no broader campaign, commit or push.
[Specification](../../specs/R2_ACTIVITY_ONLY_CONTROL_r1.md); [previous check](../r2-paid-cycle-2026-10-27/REPORT.md).

## Physical check

Restrict the same B-gated paid rotor to equal charge/reset barriers and fit event count alone. The native thermal pair stays at conductance 0.003. Each forward
charge/reset withdraws 0.5 bank energy, and its exact reverse refunds 0.5. A forward
closed rotor cycle spends 1 energy unit; actual net spending must still be measured.
The A/B/C construction, material inventories and two stochastic carriers remain.
Comparisons are same-root mechanism contrasts, not optimized choices under one law.
Whole modeled field excludes unresolved external boundary histories.

Calibration precedes history scoring and uses only continuous T64 occupation
moments. Matching status: **primary_moment_matched_only**. Selected parameters:
`{"rate": 0.04834939335656788}`.

| Moment | Target | Selected control | Control minus target | Allowed absolute error |
|---|---:|---:|---:|---:|
| expected_jumps | 16.1264636078 | 16.1264636078 | +1.91313632e-11 | 0.0161264736 |
| work_accepted_gross | 11.0997748861 | 11.1814314986 | +0.0816566125 | 0.0110997849 |

Tolerance for each moment is 1e-8 + 0.001 times its target. Equal event count
does not certify equal work, and matching both moments does not certify a
net-consuming load. No histories were conditioned on their realized counts.
The [physical map](PHYSICAL_MAP.json) retains all distinct evaluated parameter
points. The selected point was independently replayed. No global impossibility
or unique organization-only contribution follows from this bounded search.

Among 11 distinct evaluated points, 0 match both moments,
1 qualify as net-paying majority-paid loads, and
0 satisfy both requirements.

At T64 the selected rotor has 0.46437652993 paid-channel
events and 0.174408528435 thermal events
(72.696837% paid-channel activity).
Gross bank withdrawal=0.114969064395;
gross refund=0.11721920057;
**net payment=-0.00225013617503**. A negative net payment
means the rotor returns energy to the bank. Its channel name and predominance
of paid-channel events do not make it a net-consuming load.
Net-paying, majority-paid qualification: **False**.

## History accounting and interpretation

Three 324-state laws, cadences 0.25/0.5, horizons 4/16/64: 18 finite profiles.
Productive minus comparator in complete-history bits; every represented event
counts. Rate differences are separate stationary diagnostics, not observed
later-horizon wins. T64 count matching does not match stationary event rates.

| Comparator | Horizon | Cadence | History difference (bits) | Rate difference (bits/time) |
|---|---:|---:|---:|---:|
| no_secondary_access | 4 | 0.25 | +0.026133897 | +0.100814438 |
| no_secondary_access | 16 | 0.25 | +0.233061375 | +0.100814438 |
| no_secondary_access | 64 | 0.25 | +2.259620839 | +0.100814438 |
| no_secondary_access | 4 | 0.5 | +0.021891129 | +0.083399488 |
| no_secondary_access | 16 | 0.5 | +0.194058836 | +0.083399488 |
| no_secondary_access | 64 | 0.5 | +1.872633270 | +0.083399488 |
| activity_only_candidate | 4 | 0.25 | +0.012189782 | +0.005142009 |
| activity_only_candidate | 16 | 0.25 | +0.020865741 | +0.005142009 |
| activity_only_candidate | 64 | 0.25 | -0.311511117 | +0.005142009 |
| activity_only_candidate | 4 | 0.5 | +0.009997881 | +0.001376304 |
| activity_only_candidate | 16 | 0.5 | +0.013019681 | +0.001376304 |
| activity_only_candidate | 64 | 0.5 | -0.315763530 | +0.001376304 |

The count-only candidate exceeds productive finite lushness at T64 while accepting
more gross external work and returning net bank energy through the rotor.
It is an activity-matched comparison, not a jointly work-matched or net-consuming
nonproductive comparator. These limitations do not invalidate its native history
scores. They restrict what can be attributed to organization. The signs at two
cadences do not establish physical-resolution faithfulness.


The chain's distinct physical functions remain demonstrated by the prior
construction/transduction readouts. This control check leaves the clean
productive-versus-net-consuming comparison open. It is a comparator boundary,
not a failure of the generativity principle. All preceding scores, calibrations
and source snapshots remain intact, including the joint B-gated control's
negative net payment of about 0.025513 energy and the older thermally dominated
rotor. No result is removed because its ranking is inconvenient.

## Verification and provenance

The workspace check passes 165 tests, source/archive/evidence
checks and exact baseline/P001 reproduction. Native energy/material audits
and the fixed thermal rule are executable contracts. Receipt elapsed time:
63.324s; peak
147.39MiB under 900 s / 1 GiB / 64 MiB caps.
[Retained results](retained/RESULT.json), [calibration](retained/CALIBRATION.json),
[quality axes](QUALITY.json), [validation](VALIDATION.json), source snapshot and
byte manifest accompany this report. Numerical success does not certify physical
adequacy or the ethical thesis. Further comparator design requires review;
there is no automatic continuation of the search.
