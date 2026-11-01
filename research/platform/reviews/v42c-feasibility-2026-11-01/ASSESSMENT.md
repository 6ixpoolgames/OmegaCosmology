# Version C: Sol feasibility handoff

1 November 2026. Assessment against V42C_SCIENTIFIC_CORE_r1.

## Verdict

A small spatial enabling model is plausible with the present numerical engine.
Recommend a six-site 2x3 ladder, four mobile constituents of two species, and
nearest-neighbor reversible bonding. Preserve resolved site positions. Implement
one adapter and a minimal operation interface rather than replace the engine.

This assessment includes a reproducible combinatorial count, not a compiled
physical model, reachability test, speed benchmark, or scientific score. Exact
enumeration and kernel timing remain the next engineering milestone. The
strong common-present option claim requires a comparison-semantics decision;
existing exterior schedules do not automatically establish it.

## 1. Preferred grammar

Use two indistinguishable particles of species a and two of species b on six
fixed sites arranged as a rectangular ladder, with one occupant per site and
two vacancies. Site positions are resolved physical coordinates. Keep spatial
translations and rearrangements in histories; do not quotient them away merely
to reduce matrix size. Species identity is physical; individual serial labels
are not. The eventual validation reference may label particles temporarily to
check that lumping identical unmarked particles preserves the physical law.

Allow nearest-neighbor bonds of types aa, bb and ab, with at most one bond per
particle. The homotypic dimers are A=aa and B=bb. Heterotypic ab association is
a competing use of the same matter, with its own native consequences. It may
become productive if the specified chemistry permits it; do not disable that.

Candidate enabling loop, subject to an explicit energetic design:

1. Assembly of A consumes available chemical resource and changes a real bond.
2. A increases both directions of an eligible B assembly reaction when an A
   dimer is locally in contact with the prospective b pair. Basal B assembly
   remains available. The catalyst changes kinetics, not equilibrium affinity.
3. B catalyzes resource capture into a shared finite chemical store. That store
   funds construction and reconstruction, including A. Capture and construction
   retain their reverse channels and explicit material/energy exchanges.

This provides distinct structural and energetic functions, with a candidate
resource-return loop. It does not yet prove that these functions run fast enough,
repay their costs, or yield a positive lushness contrast.

For the smallest candidate, represent a three-state carrier pool and a bank
with levels 0,1,2. They are explicitly well mixed chemical coordinates, not
spatially transported fuel. Positions apply to structural constituents; chemical
transport is not resolved. This scope restriction must travel with every result.
A later localization of fuel is a new model, not an invisible refinement.

Unbound particles hop into vacant neighboring sites. Bonded dimers need declared
rigid translations and, where geometrically possible, rotations, all reversible
and with physically motivated conductances. Bond breaking also restores free
motion. Do not immobilize all bound structures simply to make movement rules
easy. Neither mobility ratios nor catalytic strengths are chosen on lushness.

Why a ladder: an exclusion ring can conserve cyclic particle order, making
apparently simple arrangement changes inaccessible. A ladder supplies routes
around vacancies, but the actual compiled graph must still verify reachability.
Its finite width, dense occupancy and artificial geometry remain limitations.

## 2. Structural counts and numerical implications

The accompanying count script enumerates site occupancies and all allowed
nearest-neighbor matching bonds. It imposes the two-per-species inventory and
single-bond rule. It then multiplies by nine chemical states. It does not impose
energetic reachability, construct rules or assert that all states are reached.

| Grid | Occupancy/bond states | With carrier and bank | One dense matrix | Four-array kernel guard |
|---|---:|---:|---:|---:|
| 2x2 | 42 | 378 | 1.09 MiB | 4.36 MiB |
| 2x3 | 408 | 3,672 | 102.87 MiB | 411.49 MiB |
| 2x4 | 1,494 | 13,446 | 1,379.36 MiB | 5,517.42 MiB |

Counts are exact for the stated alphabet, before any selector, actuator,
source-lifetime variable, or localized chemical coordinates. They are upper
bounds on reachable-state counts for a law using precisely this alphabet.

The kernel's default workspace guard is 32 MiB and allows at most 1,024 states:
it checks four dense arrays, not one. Thus the preferred candidate needs an
explicit larger budget; the default would reject it. Its four-array figure is
an admission estimate, not a measured peak-memory guarantee for scipy.linalg.expm.
Ledger objects, auditing, coordinate rewards and temporary arrays add overhead.

A three-state selector could raise the alphabet to 11,016 states and the same
guard to about 3.62 GiB, before other overhead. A two-state actuator alone
quadruples dense storage relative to the unaugmented alphabet. Controller design
is therefore a major feasibility choice, not a cosmetic addition.

The 2x2 case has no vacancies and cannot represent the proposed free hopping
comparison. Use it only as a tiny conformance reference, not a scientific
fallback. The 2x4 case is an expansion target; it is already beyond a 4 GiB
budget under the current four-array guard before any control machinery.

No runtime estimate has been measured. Dense exponentiation and repeated
matrix-vector profile propagation may dominate even when memory fits. Benchmark
one qualified kernel and one bounded profile before promising batch throughput.
Keep one cadence/case resident at a time. Do not cache all cases or independent
option kernels simultaneously without aggregate accounting.

## 3. Common-present operations: what the machinery can currently say

Existing operations.py appends a paid finite stroke apparatus but varies its
stroke conductance through an externally prescribed barrier pulse. The module
explicitly disclaims a free internal policy choice. scheduled_study.py propagates
the common initial distribution through all phases without resetting it; the
scheduled-continuation contract conditions on the prescribed exterior schedule.

That is a useful controlled/interventional comparison. It is not an autonomous
selector modeled together with everything that selects its initial command.
Adding different initial selector codes produces matched preparations. Adding
a random selector gives one joint distribution; selecting only its successful
outcomes is not a substitute for executing separate options.

Recommended practical first operation design: common paid assembly apparatus,
with externally specified finite preparation instructions that alter barriers
while retaining the same Hamiltonian, inventories and available reactions.
Compare invest-in-A, leave-available, and alternate assembly instructions. Charge
the physical assembly events; retain native dynamics during preparation and
include the entire prefix in every profile. After preparation, all options use
the identical autonomous recovery/production law. No successful-assembly filter.

This is a proposal for a controlled comparison, with exterior command selection
explicit. A constant Hamiltonian avoids quench energy but does not prove that
operating the barrier controller has no cost. Its physical strokes and energy
must be modeled or the omitted operation cost stated. The existing finite
damage-stroke builder is not a general spatial assembly apparatus; extend it
through an explicit reusable interface, not by calling damage assembly.

If version C requires a completely autonomous same-full-present interpretation,
the option/intervention semantics need a formal decision before implementation.
One full autonomous state and law determine one native distribution. Software
cannot settle what external alternative selection means by changing a label.
The physical feasibility work can proceed without claiming that stronger result.

After any finite pulse, a common finite irreducible final law implies a common
asymptotic entropy rate. This design therefore targets the full finite-window
advantage and offset. Persistent distinct rate claims need a different, explicit
maintained-operation contract; do not promise them for this pulse design.

## 4. Reuse and extensions

Keep:

- LocalModel rational energies, reversible marked event rules and executable
  inventories; Compilation integrity checks and event-ledger aggregation.
- Exact sparse reachable enumeration and Gillespie events from the same law.
- sampled_kernel, history profiles, continuous occupation and physical rewards.
- Paired input validation, full-profile/asymptotic analysis where applicable,
  scheduled propagation, and retained-source evidence packaging.

Add:

- A spatial adapter generating local motion, bond and contact rules with legal
  state constraints, explicit competing binding and structural energy terms.
- Bond-carrying motion that preserves bonds and occupancy, including its native
  reverses; no exchange of species through occupied sites by numerical shortcut.
- Physical local motif selectors for A-assisted B assembly and B-enabled capture,
  with declared reaction roles rather than discovery from rule-name strings.
- A paid preparation interface with an explicit external-command scope until
  an autonomous operation contract is actually implemented.
- A state-alphabet and aggregate-workspace preflight that accounts for all
  apparatus states, kernel copies and requested coordinate decompositions.

The current finite coordinate grammar can express this small graph through
generated guards and changes. It does not supply generic spatial matching or
transport semantics already. General graph canonicalization, learned agents,
population scaling and a new entropy estimator are unnecessary for this step.

## 5. Qualification and physical-only outputs

Before scoring, demonstrate legal occupancy/bonds, conserved a and b inventory,
consistent carrier/store accounting, and per-route first-law/local-balance
checks. Source-off equilibrium must be tested on the actual spatial law.
Boundaries and any chemostatted species require explicit exchanges; closing
energy does not by itself establish chemical closure.

Verify from native rules that A changes eligible B rates, that B affects capture,
that basal routes survive, and that changing association does not add free
capability. Audit assistance in both directions and the competing ab route.

Return physical-only root reachability, interface contact occupancy, A/B
assembly and loss counts, first passage to B, use of B's capture path, energy
store occupancy, gross/returned/net work, heat, and event activity. No score
should determine which parameter choice becomes the purported untouched design.
Mechanism operation and functional repayment remain distinct requirements.

Structural state counting is sufficient for this report only. The next prototype
must construct the actual event graph and measure resource use. If that graph
is incomplete under the cap it cannot be scored as a complete smaller world.

## 6. Recommended next handoff

Proceed to an implementation protocol for a 2x3 physical grammar and bounded
enumeration benchmark. First resolve whether the controlled-pulse interpretation
is adequate for this batch's claim or whether autonomous choice is required.
Do not add selector states until that decision establishes what they would do.

Then implement and qualify one anchor chemistry, with no lushness-driven
selection. Return actual reachability, peak memory, compilation and kernel
timings, accounting checks and a list of unsupported comparisons. Only then
set the small scientific case set and execution budgets.

No further world search, scientific ranking, source revision, commit or push
was performed in this assessment. Both the scientific core and this engineering
return remain review documents.

Reproduce the count with the repository Python environment by running
count_structures.py in this folder. STRUCTURAL_COUNTS.json records its output.
Source inspection covered physics.py, backends.py, history.py, operations.py,
scheduled_study.py and the scheduled-continuation contract. Existing tests were
not rerun because production code was unchanged; the count is independently
inspectable combinatorial enumeration, not a physical validation certificate.
