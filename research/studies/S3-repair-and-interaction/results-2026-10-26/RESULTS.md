# S3 repair and occupied-interaction results

All signed comparisons are retained; no outcome was an acceptance criterion.

| Study | Cases | Profiles | Wall s | Peak MiB |
|---|---:|---:|---:|---:|
| repair | 8 | 120 | 80.093 | 120.12 |
| interaction | 12 | 48 | 559.724 | 702.86 |

## Last registered horizon at the primary cadence

| Study/contrast | T | Whole delta bits | Projected intervals |
|---|---:|---:|---|
| repair/S0p02_feedback:repair_fault-minus-access_fault | 4096 | 0.459174 | R[-72.1409,83.2857]; Y[-83.9125,71.7255] |
| repair/S0p02_feedback:repair_fault-minus-intact | 4096 | 20.455694 | R[-70.0087,84.7546]; Y[-76.2107,78.9067] |
| repair/S0p02_feedback:access_fault-minus-intact | 4096 | 19.996520 | R[-75.6359,79.2370]; Y[-70.0517,84.9347] |
| repair/S0p02_no_feedback:repair_fault-minus-access_fault | 4096 | -2.326080 | R[-28.9649,38.3810]; Y[-87.4863,70.8852] |
| repair/S0p02_no_feedback:repair_fault-minus-intact | 4096 | 16.992979 | R[-28.8449,38.0279]; Y[-78.4276,79.3699] |
| repair/S0p02_no_feedback:access_fault-minus-intact | 4096 | 19.319059 | R[-33.6375,33.4044]; Y[-70.0798,87.6233] |
| repair/S0p12_feedback:repair_fault-minus-access_fault | 4096 | 0.351315 | R[-73.8368,84.6591]; Y[-85.9415,73.5724] |
| repair/S0p12_feedback:repair_fault-minus-intact | 4096 | 26.488814 | R[-70.9786,86.7862]; Y[-77.6366,81.2966] |
| repair/S0p12_feedback:access_fault-minus-intact | 4096 | 26.137499 | R[-76.4316,81.4170]; Y[-71.3879,87.4169] |
| repair/S0p12_no_feedback:repair_fault-minus-access_fault | 4096 | -3.717296 | R[-28.5614,37.5837]; Y[-89.3710,72.2946] |
| repair/S0p12_no_feedback:repair_fault-minus-intact | 4096 | 22.192582 | R[-28.0573,37.6021]; Y[-79.6586,81.3674] |
| repair/S0p12_no_feedback:access_fault-minus-intact | 4096 | 25.909879 | R[-32.6470,33.1696]; Y[-71.0805,89.8657] |
| repair/S0p02:feedback-minus-no-feedback:intact | 4096 | 155.268713 | R[110.8755,221.2647]; Y[-69.1504,86.6471] |
| repair/S0p02:feedback-minus-no-feedback:repair_fault | 4096 | 158.731428 | R[113.2280,224.4750]; Y[-68.9335,88.1839] |
| repair/S0p02:feedback-minus-no-feedback:access_fault | 4096 | 155.946174 | R[112.2244,223.7500]; Y[-71.0279,85.8642] |
| repair/S0p12:feedback-minus-no-feedback:intact | 4096 | 176.954901 | R[119.7117,230.9360]; Y[-67.5125,91.7529] |
| repair/S0p12:feedback-minus-no-feedback:repair_fault | 4096 | 181.251133 | R[122.3552,234.5553]; Y[-67.2511,93.4427] |
| repair/S0p12:feedback-minus-no-feedback:access_fault | 4096 | 177.182521 | R[121.3348,233.7758]; Y[-69.5007,90.9849] |
| repair/supply:feedback:intact | 4096 | 1670.327719 | R[-58.9392,96.7243]; Y[-66.8637,89.4812] |
| repair/supply:feedback:repair_fault | 4096 | 1676.360839 | R[-59.0089,97.8556]; Y[-67.0620,90.6435] |
| repair/supply:feedback:access_fault | 4096 | 1676.468698 | R[-58.9443,98.1136]; Y[-66.8413,90.6049] |
| repair/supply:no_feedback:intact | 4096 | 1648.641531 | R[-23.3362,42.6137]; Y[-71.4220,87.2959] |
| repair/supply:no_feedback:repair_fault | 4096 | 1653.841135 | R[-23.4716,43.1109]; Y[-71.7327,88.3730] |
| repair/supply:no_feedback:access_fault | 4096 | 1655.232351 | R[-23.4377,43.4709]; Y[-71.4078,88.5235] |
| interaction/local-minus-none | 1024 | 149.136474 | A[52.8311,94.1839]; B[52.8311,94.1839] |
| interaction/one_way-minus-local | 1024 | 29.821984 | A[-22.5315,22.7441]; B[4.7332,51.0798] |
| interaction/reciprocal-minus-local | 1024 | 59.904794 | A[4.9536,51.2731]; B[4.9536,51.2731] |
| interaction/reciprocal-minus-one_way | 1024 | 30.082811 | A[4.8543,51.1599]; B[-23.4815,23.8951] |
| interaction/one_way_low_supply-minus-one_way | 1024 | -314.317808 | A[-26.2954,18.2075]; B[-28.6339,18.0242] |
| interaction/one_way_high_supply-minus-one_way | 1024 | 154.502994 | A[-22.1230,23.0980]; B[-22.9604,24.4018] |
| interaction/one_way_slow_contact-minus-one_way | 1024 | -331.781215 | A[-24.1468,21.2061]; B[-25.3904,22.1522] |
| interaction/one_way_fast_contact-minus-one_way | 1024 | 926.866388 | A[-19.5465,24.6640]; B[-20.4944,25.6549] |
| interaction/one_way_low_local-minus-one_way | 1024 | -105.969205 | A[-74.0458,-32.2277]; B[-74.0287,-28.7076] |
| interaction/one_way_high_local-minus-one_way | 1024 | 302.688763 | A[127.2426,192.1502]; B[124.4855,188.9949] |

## Guarantees and scope

Integrated foreclosure rows: 360; structural-zero counts: {True: 360}.
Structural zeros follow from native Boolean support; nonzero reference weights would be float64 numerical values.
Constituent recovery, graph closure and history entropy are separate outputs. No tiny reverse route was removed.
The intact repair root has0.5 more formation energy; only repair-fault versus access-fault is the equal-energy fault contrast.
All interaction arms retain the same six contacts; only paired conversions or declared physical conductances change.
Analytic local inequalities are evaluated in float64; unresolved intervals are not ties or midpoint verdicts.
Bath/source histories are unresolved. Work and activity differ, so these are not matched-throughput/activity attribution tests.
Same-law preparation rates agree; offsets can remain. Rate does not replace a finite-horizon comparison.
No permanent destruction, interacting valuers, optimizer, gas, population expansion or ethical correspondence is claimed.

## Reconstruction

Each study/run folder contains raw case results, capped receipts and a byte-exact SNAPSHOT.zip.
Restore with scripts/restore_research_snapshot.py into a fresh ignored directory and execute the retained supervisor/plan there.
Engineering repetitions and the incomplete ancestry-query configuration attempt are retained separately; no physical parameter changed in that repair.
No dense matrices or sampled paths are retained. All physical randomness remains in the total.
