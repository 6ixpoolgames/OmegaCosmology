# Consequential access: scientific assessment

24 October 2026. [Full report](ACCESS_RESULTS.md),
[compact evidence](ACCESS_RESULTS_SUMMARY.json), [figure](ACCESS_COMPARISON.png),
[implemented physical model](ACCESS_MODEL.md).

The added C-assisted resource route has a sustained positive continuation
effect in both sensor implementations. At cadence .25 it adds 68.9915 bits to
tracking and 69.3017 bits to blind control by T1024. Gains are positive at every
tested horizon and cadence. It also increases maintained apparatus, C presence
and net captured bank energy in both arms. The mechanism is physically useful
under the stipulated supply and costs.

It does not remove the later tracking/blind reversal. The additional opportunity
favours tracking slightly more at T64/T256, and blind control slightly more at
T1024. All these interaction signs agree across the three cadences.

| Horizon, cadence .25 | Added route: tracking gain | Added route: blind gain | Difference in gains |
|---|---:|---:|---:|
| 64 | +.379287 | +.371266 | +.008020 |
| 256 | +7.251934 | +7.206791 | +.045143 |
| 1024 | +68.991503 | +69.301740 | -.310237 |

Tracking beats blind control with the route present by .346589 bits at T64 and
.900033 at T256, then trails by 9.117475 at T1024. Without the added route, the
corresponding differences are+.338568,+.854890 and -8.807237. These comparisons
are within the new fixed-budget law; they are not replacements for the earlier
completed additional-assistance experiment's numbers.

## What physically changed

At T1024, adding the route raises net captured bank energy from 3.1361 to 4.2361
in tracking, and from 3.2141 to 4.3731 in blind control. Endpoint apparatus rises
from 2.6781 to 2.7168 and from 2.6715 to 2.7078 respectively. Net accepted-minus-
returned source work also rises. The available work prescription is matched;
realized work is endogenous and differs.

Class2's net captured energy increases strongly while class1's decreases:

| Implementation | Class1 off -> on | Class2 off -> on |
|---|---:|---:|
| Tracking | 2.8395 -> 2.6238 | .2965 -> 1.6124 |
| Blind | 2.9004 -> 2.7012 | .3136 -> 1.6718 |

The two classes compete for one shared carrier. Access to the second channel
therefore changes the first channel too. This is part of the intended coupled
physics, and it explains why a new channel cannot simply be assigned an isolated
additive productivity bonus.

Under the declared resource/material-bank/selector/sensor chain-rule order,
the coupling gain in tracking comprises57.076 resource bits,10.798 material/bank,
.838 selector and .280 sensor bits. Blind has a similar breakdown. The additional
benefit is carried chiefly by the resource and material processes in this
decomposition. These shares depend on order; they are explanatory, not unique
causal contributions or quantities to subtract.

The remaining tracking/blind difference has the familiar structure. With the
new route, tracking has+1.415 resource and +1.368 material/bank bits relative to
blind, -.531 selector and -11.369 sensor, totaling-9.117 bits at T1024/.25. Tracking
has slightly more endpoint apparatus, but blind has more net captured energy
in this new regime. Neither stock nor capture alone replaces the whole score.

## What the result answers

An added physical use of organization increases complete-history lushness here.
It continues paying in the stationary diagnostic: the on-minus-off rate gain
is +.092874 bits/time for tracking and +.093341 for blind at cadence .25, positive
at all three cadences. Finite scores are the primary result; the rate diagnoses
the persistent effect under this maintained source.

More available productive access does not automatically favour this tracking
mechanism over this blind one. Both can assemble C and use its catalytic route.
The bit observes local reserve, not resource identity, and the access mode
engages the relevant available access reactions rather than choosing between
the packet classes. The new opportunity does not itself introduce a new
information-dependent resource-routing decision.

The late interaction of -.310 bits is small compared with the roughly 69 bit gain
shared by both arms. It is a measured relationship at this setting, not a failed
generativity principle. The route is functional even where it helps blind
control slightly more. Conversely, its positive continuation effect does not
establish the complete ethical identification.

## Best next scientific step

Map source composition and the alternative use of C sites to determine which
dependency governs the observed relationship. If the question is specifically
information's value, the next control extension should let a paid observation
distinguish opportunities requiring different physical actions, with the same
sensor/actuator hardware in its blind control. Keep regimes with little or no
decision-relevant information as controls. No information bonus is needed.

Adding slots alone would not answer that question. Expansion, independent
controllers, harm/recovery and robustness remain valuable separate additions,
with their actual costs and dependencies. This first panel has one source
composition, four responsive implementations and no newly computed depth
witness or population-growth mechanism. It is not an exhaustive policy search.

## Engineering outcome

All four scientific cases completed with every native state and every sampled
row. Actual runtimes were 644.7-678.8 seconds per case, peak 1134.0 MiB, inside
1800 seconds/4GiB per case. The two-worker queue completed. Native energy
residuals are below 3e-15; source-off equilibrium and independent stationary
diagnostics pass.74focused tests pass and Ruff is clean.

Legacy one-resource generator/root reproduction, frozen-source smoke replay and
current-source common-query replication are retained. The first legacy check
had a tuple/list validation mismatch; its original incomplete bundle is kept,
and the normalized check reproduces the original native hash/root exactly.
No scientific prediction is scored from that engineering bookkeeping issue.

The seven retained batches occupy about 37 MiB, including rebuildable caches.
Sources, manifests, receipts, result hashes, report code and reconstruction
inventories are preserved. No data was purged. No commit, push, upload, external
task message or manuscript edit occurred.
