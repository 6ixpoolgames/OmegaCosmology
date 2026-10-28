# Machinery audit before the further-enabling package

27 October 2026. Assessment, not an implementation specification or authorization
for a scientific run. Audited the current working tree, including the uncommitted
enacted-damage/matching slice, on top of published revision 3cc7925.

## Verdict

Keep the physical event kernel, entropy mathematics and independent reference
tests. Harden the contracts and reorganize evaluation around reusable compiled
objects before adding the integrated R2 successor. Another wholesale rewrite is
not justified by this audit. Several present abstractions are still fixture
builders rather than safe, general composition interfaces.

No retained scientific result was shown incorrect by this review. Six tiny probes
demonstrate enforcement or abstraction gaps; they do not demonstrate that a
retained run exercised those gaps. Existing kernel, projection, ancestry and
phase suites passed: 31 tests. No scientific sweep or physical-law edit was made.
This is a targeted source audit, not an exhaustive proof of numerical correctness.

## What should be preserved

- Exact enumeration and Gillespie sampling both consume LocalModel.events.
- Rates are paired with native reverses and local detailed balance. Energies use
  rational arithmetic before numerical rate evaluation; fractional costs exist.
- An incomplete state enumeration cannot be scored as a smaller complete world.
- Parallel channels aggregate in Q for state-history entropy while their physical
  work/heat marks remain available for ledgers. Labels do not add entropy.
- Hidden-state projection methods retain memory rather than pretending the
  observed process is Markov. Bound widths and statistical estimates are distinct.
- Passive sequence, function and ancestry queries do not enter the physical score.
  Marginal agreement is checked. Ancestry is explicitly narrower than causation.
- Scheduled histories include the operation prefix and memory across boundaries.
- Structural possibility is calculated from the graph, not a floating-point
  probability cutoff. Numerical precision and physical faithfulness stay separate.
- Frozen execution inputs, retained results and hard process caps already exist.

## Verified gaps

### A1. Material conservation is descriptive, not executable

Location: physics.py, LocalModel.material and record/from_record; semantics.py,
LawSpec.conserved. Material entries are serialized but do not supply conserved
quantities checked on events. The ordinary assay independently checks declared
root energy, not a general material inventory.

Probe: a count coordinate n with a declaration that n is conserved, and a
reversible 0-to-1 rule, compiles and passes the equilibrium audit. The count
changes. This shows that the declaration is not an enforced invariant, not that
existing fixed slots manufacture matter.

Existing precursor/constructed slots often conserve material by construction.
That protection will not carry automatically into competing construction uses,
transport, populations or shared precursor pools.

Required direction: explicit inventory vectors or state functions, plus declared
boundary exchanges; check every event against them. A module should declare
consumed, produced and retained constituents. Keep heat/work checks as well.
First-law closure alone cannot discover a missing construction bill when heat
is calculated as work minus the stipulated energy change.

### A2. A common present is compared by name, not physical content

Location: semantics.py, ComparisonSpec and validate_query; finite_study.py.
The process check compares common_present with present.id. The matched object
only needs to be nonempty. It does not validate two arms together. Most fixed-law
study measurements are typed as single_query; later comparison scripts carry
much of the scientific comparison responsibility.

Probe: two PresentSpec objects with the same ID but physical energies 0 and 1
both pass a process contract declaring equal endowment.

Required direction: a comparison validator referencing both actual inputs,
present-content identity, coordinate/observation mappings, inventories, boundary
prescriptions, horizons and conditioning. A common process root should require
content equality under the declared mapping. Preparation and mechanism contrasts
should require their appropriate explicit matching checks. Equal energy alone
is not equal endowment. An exterior-cancellation claim remains separate.

### A3. Compiled event accounting is not covered by the integrity guard

Location: backends.py, Compilation.require_complete.
Model, state order, index and Q hashes are checked. The ledger is not included.

Probe: replace a freshly compiled ledger with an empty tuple. require_complete
still passes, Q and its hash are unchanged, and flow_rewards reports zero event
activity instead of 0.2 summed exit reward in the tiny example.

This is a mutation-guard defect, not evidence of a changed historical ledger.
Required direction: immutable compiled artifacts, a marked-event ledger digest,
and validation that aggregating the ledger reproduces Q and its work/heat reward
vectors. Bind query/cache identities to the appropriate artifact. A state-only
kernel identity and a physical marked-channel identity are different objects.

### A4. Symmetry safeguards differ between evaluators

Location: scheduled_study.py, observable and functional-condition evaluation;
compare finite_study.py's observable orbit checks and monitors.py's refusal of
unsupported quotient event selectors.

Probe: the scheduled assay accepts an observable selecting `first` from two
interchangeable unmarked copies. Its reported endpoint is 0.00821463497 at T1.
The orbit contains both (0,1) and (1,0), on which the expression differs. The
ordinary assay rejects that class of observable. The resulting number describes
the chosen representative convention, not an admissible named constituent.

Required direction: shared validation for observables, functional predicates,
event selectors, projections and lineage across static and scheduled execution.
Either prove invariance/equivariance or explicitly require a labelled reference.
Current enacted-damage studies use distinct slots; this probe does not show an
error in their outputs.

### A5. Scientific roles depend on string naming conventions

Locations: physical_modules.assistance_spec; occupancy.occupied_ecology;
readiness_v2; scheduled_study's literal `operation.stroke` prefix.

Probe: rename every rule while keeping all guards, changes and rates. The
aggregated numerical Q is unchanged, but assistance_spec discovers zero ancestry
edges instead of two. The downstream ancestry compiler then rejects an empty
edge specification. Renaming can thus break analysis despite unchanged physics.

Some builders also identify the parent by guard position. Several upgrade
functions rewrite an old fixture's rules by prefix. Generic monitor selectors
allow absent IDs for ablations, so a typo and an intended absence are not always
distinguished.

Required direction: explicit module ports and typed construction/catalysis/payment
roles, with rule IDs serving as references. Validate declared parents/children and
payments against actual transitions. For ablations, distinguish required channels,
explicitly absent channels and unknown names. Typed role labels are validated
descriptions, never extra physical states or entropy contributions.

### A6. Matching uses one implicit unit-dependent tolerance

Location: matching.match_physical_moments. Residual scales are max(1, abs(target))
and one tolerance applies to all moments.

Probe: activity target 1e-8 and control 1e-4 receive `matched` under the default
0.001 tolerance. This follows the implemented absolute allowance; it is not an
optimizer arithmetic error. It would be misleading if read as a relative match.

Required direction: typed moment definitions, units, horizon, cadence-independent
or sampled-event convention, and separate absolute/relative tolerances for each
quantity. Record target/control/residual and calibration objective. Distinguish
finite-horizon matching from stationary matching. Preserve all bounded search
attempts and unmatched outcomes. Matching these moments never matches complete
path laws or uniquely identifies an organization-specific entropy contribution.

## Architectural limitations relevant to the next model

### B1. Finite evaluation is coupled to stationary and reference requirements

finite_study.evaluate_case unconditionally audits a single source-off sector,
solves for a stationary distribution and invokes irreducible_asymptotics.
thermodynamics.balance also requires a single reference sector before returning
even first-law results. Finite history itself has no such irreducibility
requirement. A valid finite experiment with disconnected sectors can be refused
because an optional asymptotic or availability query is unsupported.

Split the query plan into requested capabilities: finite history, physical
flows, source-off reference, asymptotics, projections and monitors. A missing
optional capability should have a typed unsupported result, not invalidate the
other well-defined quantities. Do not silently select a recurrent class.

All LocalModel rules currently have positive reverse rates. Each reachable
component of a static native law is therefore communicating; this grammar cannot
directly express one-way absorbing material loss. Retain its honest scope. A
future loss adapter needs explicit waste/destination accounting and physical
assumptions, not merely a reverse-rate deletion to obtain a desired ranking.

### B2. Repeated dense references consume the expansion budget

The fixed-law assay constructs P once, reconstructs it in the asymptotic helper
for each preparation, and reconstructs it again in evaluate_history for every
preparation/horizon. It also retains a dense 2n-by-2n occupation exponential for
every horizon, alongside sparse-action occupation calculations. Stationary/Poisson
systems repeat across roots. These are useful independent checks in small reference
worlds, but unnecessarily expensive as the default production execution plan.

Use a compiled-law evaluation context with cached validated P and row entropies
per cadence, shared stationary/bias vectors, and sparse-action occupation/reward
propagation. Stream larger reference comparisons or restrict exhaustive dual
methods to calibrated reference sizes. Keep validation available and report the
selected execution/validation mode. Joint memory budgets must account for all
live arrays, not only each helper's allocation estimate.

The projected-history methods additionally grow exponentially with observation
alphabet and memory depth; filtering still needs a full sampled kernel here.
These are separate limits from RAM management. Raising memory alone will not
make general population or spatial histories tractable.

### B3. Composition is still assembly of prearranged slots

The low-level grammar can express local guards, energetic interactions and
changes. Most high-level interfaces, however, are tied to names such as bank,
carrier, store.built and existing model constructors. relations is largely
descriptive; actual constraints are separately encoded in rules and forbidden
patterns. There is no general validated module-binding layer for resources,
ports, capacities and local geometry.

For the next R2 package, a small explicit module interface is enough: bind named
resource ports, constituents, stores and dependencies, compile to the existing
grammar, and validate collisions/conservation/exclusivity. Do not build a general
graph-rewriting engine before a physical fixture needs it. Preserve a route to
population/symmetry and niche/transport adapters without claiming they exist now.

### B4. Causal attribution has several valid but different objects

Ordered monitors, connected native-marked assistance ancestry, coordinate
chain-rule shares and physical mechanism ablations answer different questions.
The code recognizes many of these limits, but reporting remains partly custom.
Ancestry is currently for distinct binary slots, one named parent per assisted
birth, and capped depth. It is not a general pedigree, joint multi-parent enabling,
resource ancestry or a causal effect estimator.

The integrated R2 report should pair connected assistance and actual downstream
use with explicit mechanism comparisons. Native substitutes remain visible.
Energy fungibility does not justify inventing a unique parent for each spent
energy unit. Add resource-route attribution only when it has a physical or
explicitly analytical definition that the claim needs.

### B5. Evidence identity is strong; report contracts are uneven

Execution snapshots and worker dependency versions are retained, and source
checks are useful. Evidence quality is also described carefully in prose. Yet
result dictionaries and study exporters do not all use one enforced set of
quantity, comparison, resolution and guarantee fields. Protocol strings can
promise more than the executed query checks. The working guidance additionally
contains many successive historical permission/status paragraphs, which make
the active scope hard to identify.

Use one report schema tied to actual executable query identities, retaining the
four independent quality axes. Keep current scope concise and move completed
workflow history to a ledger. Record dependency/BLAS environment sufficiently for
numerical reproduction; exact-byte reproduction and tolerance-based numerical
reproduction must remain distinct. This does not require rewriting old evidence.

## Recommended order

1. Close the verified guard gaps: compiled ledger integrity, common-present and
   paired-comparison validation, shared symmetry checks, explicit rule roles and
   per-moment matching tolerances. Add adversarial regression cases from these
   probes, in addition to the existing successful-world references.
2. Add the minimal executable material/resource and interface contracts needed
   for competing construction uses in R2. Keep old versioned adapters unchanged.
3. Separate query planning and cache reusable numerical artifacts; finite results
   must not depend on optional asymptotic/reference queries. Benchmark against the
   old evaluator on unchanged small laws, then measure the larger slice.
4. Build the integrated R2 successor from those modules, with connected enabling,
   actual use, meaningful alternative resource use and paid moment controls.

These are foundations of the next sprint, not a request to implement every future
physical capability first. General graphs, expanding populations, spatial thermal
baselines, quantum backends and autonomous/ML controllers remain separate stages.

## Audit evidence

See probes.py for the six minimal diagnostic constructions and PROBES.json for
their output. All operate on temporary in-memory model objects. The existing
test suites run were test_testbed_kernel (12), test_projection_bounds (6),
test_assistance_ancestry (5), and test_phases (8): all passed. No production source,
retained study, scientific ranking, commit or remote was changed.
