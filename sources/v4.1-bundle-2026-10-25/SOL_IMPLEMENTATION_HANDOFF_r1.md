# Sol implementation handoff: start with M0–M2

24 October 2026. Companion to
[architecture r2](ARCHITECTURE_VISION_SPEC_r2.md) and its
[formal source check](FORMAL_SOURCE_CHECK_r1.md).

This is an engineering work order proposal, not a record of implemented code.
No runs, commits or uploads have been started. On implementation authorization,
complete the stages below without turning every routine coding choice into a
new approval request. Preserve the active branch and unrelated local work.

## Aim of the first sprint

Deliver a small compositional physical kernel whose exact and sampled dynamics
agree, with explicit query semantics and a complete calibration report. The
first deliverable is not a broad ecology sweep or an asserted ethical result.
R1 access/self-maintenance follows once this kernel is validated.

## Decisions settled for engineering

| Topic | Initial implementation |
|---|---|
| Package | Separate `omega_v2/testbed_next/`; old adapters/evidence preserved |
| Public metadata | Six records from architecture r2, with distinct nested semantics |
| Physical state | Finite count coordinates plus a small number of relational slots |
| Identity | Explicit finite symmetries and a tiny labelled reference |
| Dynamics | Locally generated reversible CTMC event pairs and explicit driven boundaries |
| Energetics | Exact rational bill representation, floating numerical rates, energy/degeneracy ledgers |
| Exact backend | Root-reachable sparse enumeration, with explicit incomplete frontier status |
| Sampler | Same native event law; small conformance harness initially |
| Measurements | Full sampled-history entropy first; honest support/precision declarations for projections |
| Large plugin systems | Defer graph canonicalization libraries and generic estimator dispatch until needed |
| Formal baseline | Verified foundations r4 plus checked r19 definitions; r20 conformance pending |

Do not hardcode two pools or three species into any public core API. A small
fixed calibration world may have a fixed inventory; the engine must receive
that inventory and its symmetry as data.

## M0: contracts and one complete worked world

Create serializable examples of the six records and validation errors for
incompatible combinations. The examples must cover full-present and own-present
conditioning, a mechanism contrast, a matched-preparation contrast and a
physically implemented control process. A single-world query uses the same
continuation fields without a dummy comparison arm.

Write the R0 world as data plus reviewed rate functions before building a general
configuration language. Use two components with a reversible bond, a spent/
locked/usable carrier, and a finite energy store. A local motif enables one
paired resource-conversion pathway. Native fluctuations and an uncatalysed path
remain. A boundary drives the carrier with declared work. This is calibration
chemistry, not a microscopic biological model.

List every reaction and reverse, material inventory, bond-energy change,
resource bill, degeneracy factor and local dependence. Explain how the same
rule applies when the motif forms away from the initial seed. R0 does not need
autocatalytic reproduction or a controller yet.

Resolve these engineering choices in a short decision record:

1. State encoding and exact finite symmetry action.
2. Local match enumeration and multiplicity conventions.
3. Pair-conductance representation ensuring the declared rate ratio.
4. Content hashing and separation of law, query and reporting identities.
5. Estimated reachable states and maximum working memory for R0.

Acceptance: all physical quantities and all query inputs are explicit; R1's
later paid construction and R2's additional interface have a clear extension
path without rewriting the event model.

## M1: physical engine and backend agreement

Implement rule matching, reversible events, source-off validation, exact
enumeration, sampler and compact physical ledgers. Canonicalize only the
declared finite symmetry; avoid a general graph-isomorphism subsystem.

Required tests:

- rates and material/energy balances match independent hand calculations;
- parallel mechanisms aggregate for Q but remain separate in work/heat ledgers;
- relabelling at the root and mid-history changes no physical history;
- distinct arrangements retain their distinct enabled interactions;
- a degenerate unresolved state with no transitions adds zero history entropy;
- source-off equilibrium agrees with energy and degeneracy;
- source-on work and heat close the first law;
- the sampler agrees with exact small-world state probabilities and event
  expectations within independently justified statistical tolerances;
- a computational cap returns the frontier rather than removing reactions.

No test asserts that assembled matter must have greater lushness.

## M2: measurement and conformance spine

Reuse suitable old pure numerical routines through a narrow adapter. Verify
them against independent tiny dense calculations before depending on streamed
queries. Query metadata identifies the state order and generator fingerprint.

Implement early conformance cases:

1. Chain rule and average-root versus unobserved-root mixture.
2. Full versus own-present conditioning with an explicit hidden-root law.
3. Non-Markov observation and a validated lumpable observation.
4. Named-refinement certificate, its scope, and faithful versus unverified
   reversal status; these are separate metadata dimensions.
5. History-support foreclosure and contraction, including zero foreclosure
   for two irreducible CTMCs sharing a finite sampled state alphabet.
6. Correlated exterior with unchanged marginal and a nonzero whole comparison
   correction. This is a finite reference example, not an infinite-field proof.

Record later reference cases as pending rather than marking the whole formal
suite complete. The r20 source gap prevents a claim of r20 conformance, not
implementation of the already explicit verified semantics.

## Validation and report

Start with the architecture's small capped tests and profile before any larger
world. Report separately rule matching, canonicalization, enumeration, physics
audits, propagation and entropy costs. A good total runtime does not identify
which stage will limit later composition.

Deliver:

- implemented kernel/contracts with focused tests;
- `ENGINEERING_DECISIONS.md` and a fully specified R0 model;
- source-frozen calibration receipts and compact results;
- `ENGINEERING_REPORT.md` with measured resource use and unsupported queries;
- an R1 construction/self-maintenance configuration proposal using the same
  engine, including its material endowment and resource dependence;
- an updated formal-source mapping with source versions actually inspected.

Scientific interpretation remains separate from numerical predicates. A passed
conformance suite says the instrument implements its contracts, not that the
ethical correspondence has been established.

The next scope after this sprint is R1, then R2's further enabling and R3's
interdependence. Expensive policy surveys, generalized graph machinery and ML
remain downstream of a working instrument and measured need.
