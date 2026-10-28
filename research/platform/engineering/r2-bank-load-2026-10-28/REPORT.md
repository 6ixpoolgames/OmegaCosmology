# R2 â€” Bank-load physical qualification boundary

Completed locally 28 October 2026 from the 27 October execution snapshot. Bounded
engineering check only; no broader campaign, commit or push.
[Specification](../../specs/R2_BANK_LOAD_CONTROL_r1.md); [previous check](../r2-activity-only-2026-10-28/REPORT.md).

## Physical check

Remove B gating from the rotor equally in all arms; retain the fixed thermal pair and native refunds. The native thermal pair stays at conductance 0.003. Each forward
charge/reset withdraws 0.5 bank energy, and its exact reverse refunds 0.5. A forward
closed rotor cycle spends 1 energy unit; actual net spending must still be measured.
The A/B/C construction, material inventories and two stochastic carriers remain.
Comparisons are same-root mechanism contrasts, not optimized choices under one law.
Whole modeled field excludes unresolved external boundary histories.

Calibration precedes history scoring and uses only continuous T64 occupation
moments. Matching status: **matched**. Selected parameters:
`{"charge": 0.0024477337346205654, "reset": 0.02268810430294934}`.

| Moment | Target | Selected control | Control minus target | Allowed absolute error |
|---|---:|---:|---:|---:|
| expected_jumps | 16.5235733668 | 16.5235733668 | +3.09547943e-11 | 0.0165235834 |
| work_accepted_gross | 11.1965202794 | 11.1965202794 | +4.08668654e-11 | 0.0111965303 |

Tolerance for each moment is 1e-8 + 0.001 times its target. Equal event count
does not certify equal work, and matching both moments does not certify a
net-consuming load. No histories were conditioned on their realized counts.
The [physical map](PHYSICAL_MAP.json) retains all distinct evaluated parameter
points. The selected point was independently replayed. No global impossibility
or unique organization-only contribution follows from this bounded search.

Among 33 distinct evaluated points, 12 match both moments,
10 qualify as net-paying majority-paid loads, and
0 satisfy both requirements.

At T64 the selected rotor has 0.868961097726 paid-channel
events and 0.178784033501 thermal events
(82.936305% paid-channel activity).
Gross bank withdrawal=0.193077740019;
gross refund=0.241402808844;
**net payment=-0.0483250688256**. A negative net payment
means the rotor returns energy to the bank. Its channel name and predominance
of paid-channel events do not make it a net-consuming load.
Net-paying, majority-paid qualification: **False**.

## History accounting and interpretation

No sampled-history entropy or stationary entropy rate was calculated for this
bank-load family. The selected control fails the net-payment prerequisite, so
the worker stopped before the history stage. An execution status of `passed`
means the prescribed bounded check completed, not that this comparator qualified.
No further family adjustment or history search follows from this checkpoint.


The chain's distinct physical functions remain demonstrated by the prior
construction/transduction readouts. This control check leaves the clean
productive-versus-net-consuming comparison open. It is a comparator boundary,
not a failure of the generativity principle. All preceding scores, calibrations
and source snapshots remain intact, including the joint B-gated control's
negative net payment of about 0.025513 energy and the older thermally dominated
rotor. No result is removed because its ranking is inconvenient.

## Verification and provenance

The workspace check passes 166 tests, source/archive/evidence
checks and exact baseline/P001 reproduction. Native energy/material audits
and the fixed thermal rule are executable contracts. Receipt elapsed time:
85.342s; peak
100.06MiB under 900 s / 1 GiB / 64 MiB caps.
[Retained results](retained/RESULT.json), [calibration](retained/CALIBRATION.json),
[quality axes](QUALITY.json), [validation](VALIDATION.json), source snapshot and
byte manifest accompany this report. Numerical success does not certify physical
adequacy or the ethical thesis. Further comparator design requires review;
there is no automatic continuation of the search.
