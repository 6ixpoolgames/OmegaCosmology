# Readiness pilot: compute fits, physical fidelity needs repair

26 October 2026. All five exact cases pass at T64/T256, cadence .25, in
421.438 seconds. The quarter-energy intermittent world has 2688 states and
peaks at 2.422 GiB. The four half-energy cases have 1536 states each, peak
below .879 GiB and take about 50–53 seconds each. No smaller world, coarser
observation, shorter horizon or shallower projection was substituted.

The initial 4 GiB budget was refused by host preflight before a simulation
started. The completed batch used a 2.75 GiB hard cap and kept the existing
4 GiB host reserve. The user's later authorization to use 4 GiB was not needed
for completion. Both the initial refusal and successful run are preserved.
The supervisor now saves a failed receipt for future preflight refusals.

## What the pilot establishes

The [plan](../../models/struggle-readiness/FIDELITY_PLAN.json) and
[specification](../../specs/READINESS_FIDELITY_PILOT_r1.md) extend only the
observation horizon and diagnostics. The native readiness module is unchanged.
The four half-energy mechanisms retain their original smoke fingerprints.
The quarter case combines finer bank representation and a lower effort bill;
it is a resource check, not an isolated cost effect. A subsequent cost map
must use one common quantum in every compared arm.

Numerical maxima: kernel agreement residual 6.7e-16; stationary residual
7.9e-16; energy balance residual 2.6e-14; independent history accumulation
residual 3.6e-10. The physical mark ledger agrees with endpoint expected marks
to 9.5e-16. Source-off equilibrium, chain rule, continuous propagation and
passive functional-query marginal checks pass. These are float64 checks,
not interval-arithmetic or physical-faithfulness certificates.

Workspace validation passes123 tests,233 inherited finite checks, exact P001,
source/archive/evidence and repository checks. New tests cover cue base rates,
the complete native mark drift identity and recorded preflight refusal. See
[quality record](QUALITY.json) and [validation](validation/CHECKS.json).

## The memory and cue do not yet justify the intended interpretation

At T256, the half-energy re-engage circuit has .244530 expected attempt-written
marks, .624231 marks written by reverse clearing, and .021426 thermal mark
writes. Thus **72.53% of increments are not failed attempts**. The quarter case
gives 72.77%. These are event-origin fractions, not estimates of the ancestry
or truth of individual marks still stored at the deadline.

This is specifically a re-engagement problem, not a claim that every failure
register is equally unfaithful. In always/stop, about 8.8% of writes are thermal;
there is no cue-clear pathway. Conserve has no failed-attempt writes, yet thermal
marks appear, as expected. No counter value should be called an exact count
of past failures.

The half-energy re-engage cue is on with probability .36918 at T256. Yet the
barrier is open with probability .07407, and an on cue raises that probability
only to .07563. Its balanced accuracy is .50418, and cue/barrier mutual
information is 1.48e-5 bits. The other circuits likewise have weak association.
The quarter re-engage result is .50445 balanced accuracy and 1.68e-5 bits.
Positive information is retained; no threshold is used to replace it with zero.

Time-pooled and stationary metrics are reported separately in
[FIDELITY_SUMMARY.json](FIDELITY_SUMMARY.json). Pooling transients can generate
association, so pooled information alone does not demonstrate sensing.
Ordinary accuracy is also misleading with rare openings: an always-closed
prediction is correct about 92.6% of the time at the deadline.

The event ledger identifies a plausible mechanism for the weak cue. The fast
closed-barrier reset has a reverse that creates a cue and refunds bank energy.
It occurs about 21.67 times by T256 in half-energy re-engage. Reverse cue
clearing similarly writes marks and refunds energy. Forward paid corrections
can be unavailable when the bank is depleted. Multiplying a reversible
conductance would accelerate these reverse routes as well. These are physical
model consequences, not an entropy-calculation error.

## Keep the raw continuation results

All physical randomness remains in the total. The following are the half-energy
T256 results, under the common root and boundary prescription. They compare
fixed physical mechanism laws; there is no learner or free policy choice.

| Circuit | Whole history, bits | Working time | Ever sheltered probability |
|---|---:|---:|---:|
| Always |715.247051|35.421882|.041023|
| Conserve |714.329714|35.735347|.012493|
| Stop |715.161967|35.423165|.040713|
| Re-engage |724.968805|35.683485|.040546|

Re-engage's larger history value is a valid result for this noisy physical
circuit. It is not evidence that recognizing openings or learning to restart
is the mechanism of that gain. No term is subtracted to make another circuit
win. The quarter case is not added to this cost-comparison table.

## Horizons, scope and next step

T256 includes about 4.75 openings on average. The physical endpoint is still
.444–.696 in total variation from its limiting distribution across the cases.
Memory is slow, and rate/offset is not a good substitute for these finite
profiles. Full-body projected-history bounds remain roughly 174–175 bits wide
at T256; no private ranking is inferred. The body-core quantity omits memory
and cue and cannot substitute for the full-body history.

This modeled field has recoverable damage and thermal return paths, no permanent
death or material foreclosure, and unresolved source/bath histories. It does
not instantiate neurological learned helplessness or phenomenal suffering.
No biological or ethical verdict follows from the engineering pass.

**Next: calibrate the physical sensing/reset circuit before the broad map.**
The [repair guidance](../../specs/READINESS_FIDELITY_REPAIR_GUIDANCE_r1.md)
separates energetic bias, conductance and passive errors, and proposes funded/
depleted and held-open/closed controls before native brief openings. Any
successor must pay its sensing/reset bills, keep reverses and retain the old
results. Calibration must not target a lushness winner.

Source inputs, native outputs and cap receipts are retained compactly. No dense
operators or paths are required to reconstruct them. The original smoke,
S3/S4/S4b models and results remain unchanged. Nothing was committed or pushed.
