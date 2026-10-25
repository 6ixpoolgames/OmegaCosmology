# Occupied assistance: S2 engineering design

25 October 2026. Implementation authorized by the author's "Proceed. Push on
completion" following the [programme scope](ECOLOGY_PROGRAMME_SCOPE_r1.md).
This sprint ends at engineering smoke, alongside S0 packaging and S1 feasibility.

## State, material and interfaces

Extend the existing fixed-slot ecology with one binary contact coordinate per
assistance edge H->P. Contact=1 requires H constructed and P precursor. A
constituent has one physical interface: it can participate in at most one
contact, whether as helper or substrate. Occupancy is derived from contacts;
there is no independent busy flag. A contact is a bond, not additional matter.

Group banks and the shared carrier retain their existing semantics. Formation
energy .5, bank quantum .5, capacity2 ticks and bill2 ticks are independent inputs.
Binding energy is -.25; beta=1. The contact's energetic contribution is counted
exactly once. Components are distinct material slots, not exchangeable molecules.

## Native reaction families

1. H+P <-> HP, conductance .04, no work. Forward delta H=-.25.
2. HP+recipient bank <-> H+C, conductance .06, bill .5. Forward delta H=.25
   (.5 construction-.5 bank+.25 unbinding), heat=-.25. This particular low
   engineering bill permits bath heat absorption; it is not free work. At bill1
   the conversion dissipates .25 instead. Both directions obey the full energy.
3. Basal and unassisted paid construction/breakdown persist for free components.
   While bound, additional reversible routes permit substrate construction with
   contact dissolution, and helper breakdown with contact dissolution. Their
   conductance is the corresponding native construction conductance. Their
   reverse is thermal restoration plus binding. Thus a full bank cannot make a
   bound helper immortal; paid reverse routes remain capacity-limited as usual.
4. Assisted capture requires the capture member's interface free. Basal capture,
   source, native carrier fluctuations and all paired reverses persist.

Original instantaneous assisted-construction rules are replaced by 1–2 in this
new adapter only. Occupancy consumes opportunity, not a separate helper fuel
bill. Simultaneous port use is physically excluded. Native release can happen
at every bank level; the occupancy model does not manufacture a motor or agent.

Rule guards and forbidden states enforce the same constraints in exact and
sampled backends. Local detailed balance includes bond energy. Source-off Gibbs
is checked on the entire reachable model. A nonconverting binding control can
later omit family2; it must retain binding, native fluctuations and release.

## Queries and baseline

Construction ancestry uses the actual contact-mediated conversion's helper and
child. Parent remains constructed; every child loss ends its instance. Passive
labels do not affect physical entropy. Basal rebuilding resets depth to zero.
No resource-packet or ambiguous multi-parent genealogy is claimed.

Compare roots with all contacts initially free. Helper material and energy
remain the same between unoccupied and occupied kinetic models, but they are
different physical representations/laws; smoke does not rank them as matched
preparations. S3 must state any observation mapping used for a comparison.
Local group projections contain member states and bank. Contact records span
groups and are omitted from that projection; its full observed history remains
non-Markov. Whole histories include contacts and their random activity.

Measure total occupied interfaces, functional groups, paid conversion and
release/breakdown flux, full history and small local-history bounds. Preserve
accepted work and native state-changing event counts. No desired sign is an
acceptance condition.

## Size and smoke

The unbound paired base has432 states. For a fixed contact matching, every
occupied edge fixes two member states. The exact combinatorial upper bound is
`3*(bank_capacity+1)^groups * sum_matchings 2^(members-2*edges)`.
Two reciprocal edges between the same slots cannot both be occupied. Four
local cycle edges give972 legal states; adding two cross edges gives1215.
These counts are checked against reachable enumeration; they are not entropy
multipliers. Single-group local cycle:54 states. A two-edge shared-helper case
inside one three-member group has108 states.

Smoke: six cases (largest reciprocal pair first; single local cycle;
shared-helper competitors; paired local cycles; one-way cross-assistance;
source-off reciprocal pair). Cadence.25, T4/16, one full root each. Largest
case gates the remainder. Cap5min/4GiB/32MiB per case,30min/192MiB aggregate,
one worker. Query caps and actual resource receipts are explicit. Connected
ancestry is checked on the small local and competing-port cases; larger
ancestry products may report unsupported rather than silently truncate.

Conformance tests cover competition at the event level, release at both bank
extremes, bound failure, energy/paired rates, source-off equilibrium, contact
legality, serialization and passive ancestry marginal. Untouched old model
fingerprints and retained evidence are checked by regression and hash checks.
