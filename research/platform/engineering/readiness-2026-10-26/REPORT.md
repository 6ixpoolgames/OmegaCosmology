# Paid readiness: engineering smoke and feasibility

26 October2026. The specification and first implementation are complete.
All five source-frozen smoke cases passed atT4/16, cadence.25. This is an
engineering result, not a scientific ranking of struggle/conservation and
not an explanation of the development of learned helplessness.

| Case | Physical states | Profiles | Wall seconds | Peak MiB |
|---|---:|---:|---:|---:|
| Re-engage, brief openings |1536|2|41.521|898.37|
| Always respond, brief openings |1536|2|41.426|897.22|
| Conserve, brief openings |1536|2|39.300|896.04|
| Stop, brief openings |1536|2|41.326|897.78|
| Quarter-energy effort, blocked |672|2|6.658|270.85|

Total170.310s; one worker,2GiB/job and enforced memory reserve,300s/case,
1200s batch, no cap failure. Frozen output including source copies is under
1MiB. The compressed retained packet stores no dense operators or paths.

## What is implemented

The [specification](../../specs/STRUGGLE_READINESS_SPEC_r1.md) and
`testbed/readiness.py` add exact rational bills, constrained reserve, separate
source/recovery kinetics, low-reserve and effort-associated damage, brief
native opening opportunities, a paid failure-mark register and an energetic
opening cue. All four mechanisms carry the same hardware and energy function.
Writing a mark costs reserve; clearing through the cue also costs reserve.
Memory has no separate hold bill in this slice: its physical state has stored
energy, slow relaxation and thermal errors. Cue and warning upkeep are paid.
The hardware is stipulated present, not constructed by the body in this slice.

The counter is a noisy physical register. Native reverse reactions can undo
an effort and its mark, or create a mark through reverse clearing. An opening
cue is paid, delayed and potentially false/stale; it is not a free read of
barrier state. A stopped body can return through forgetting/reversal. All
those changes remain in the generator and history score. No death/stock reward,
learned objective, action-label entropy or persistence filter is added.

The full-body projection includes both new registers. Its engineering
memory0 bounds are distinct from the body-core memory1 bounds. The shared
assay now accepts an explicit lifted functional-query cap while retaining
the old5000-state default. Invalid or exceeded budgets reject rather than
falling back to another grain. The smoke supervisor uses the plan's date.

## Verification

Full workspace validation passes120 tests,233 inherited finite checks, exact
P001 reproduction, source/archive checks, links and retained evidence hashes.
Ruff and Windows-aware whitespace checks pass. Eight new tests cover paid
marks, thermal reverses, cue-gated paid restart, quarter-unit bills without
rounding, exhaustion, opportunity rates, common endowment and query caps.

All smoke cases pass source-off detailed balance and event energy accounting,
independent kernels and history accumulation, coordinate chain rule, continuous
occupation propagation and passive-query marginals. Maximum kernel residual
6.7e-16, energy residual2.7e-15, history residual7.2e-13. These are float64
checks, not rigorous rounding enclosures or physical-faithfulness certificates.

See [machine summary](ENGINEERING_SUMMARY.json),
[raw cap receipt](retained/BATCH_RECEIPT.json),
[source snapshot](retained/SNAPSHOT.zip) and
[workspace validation](validation/CHECKS.json). All five native models rebuild
from the live code with the same physical fingerprint. A subsequent live-only
positive-integer input check for the cap does not change the frozen physics.
The previous S3/S4/S4b results and laws remain unchanged and unpublished locally.

## Feasibility limits before a scientific map

1. **The tested exact size fits.** Four1536-state short-horizon cases need
   about40s and.9GiB each. Long-horizon physical/query costs must be measured;
   do not multiply this into a promised runtime for an untested full grid.
2. **T16 is early for this environment.** Mean time to an opening is50 units;
   mean open duration4. The smoke verifies available transitions and queries,
   not a useful balance across many opportunities. A long-horizon feasibility
   case should precede the large map.
3. **Private scores are not resolved.** Full-body bounds are about14.9bits
   wide atT16 (11.0 in the fractional blocked case). Full-body history cannot
   be replaced with body core or coordinate shares to obtain a private sign.
4. **Memory accuracy must be measured.** In the re-engage smoke atT16, forward
   cue-clear events average.014459 and reverse cue-clear events.045785.
   These reverse reactions can write marks without a failed attempt. Therefore
   endpoint mark count is not a count of actual failures, and a larger count
   cannot be interpreted as more learning or more experienced helplessness.
   This is a physical calibration issue independent of the lushness ranking.
5. **Fractional bills need a common representation for comparisons.** The
   quarter-unit closed case works exactly; it is not compared scientifically
   with the half-unit cases. A cost sweep must fix a common bank quantum.
   The fully open/intermittent quarter-quantum product space has2688 candidate
   states, beyond this plan's2000-state enumeration cap. It needs an explicit
   larger-world feasibility/budget check; no automatic coarsening is allowed.

The next engineering assessment should measure cue/memory fidelity and cost
over horizons that include openings, then freeze a bounded cost–supply–opening
map with these physical limitations disclosed. Damage and memory effects are
separate factors, not a demand that conservation must win. Activity-matched
controls and irreversible-loss variants remain subsequent comparisons.

No full parameter map, manuscript edit, commit or push was performed here.
