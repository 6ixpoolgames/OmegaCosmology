# First kernel: engineering decisions

24 October 2026. Implements the reviewed M0–M2 handoff on the current branch.
This is a finite classical engineering release, not the full research programme.

1. **State and relations.** An ordered tuple of finite integer coordinates
   records all declared dependencies. A relation is a physical coordinate with
   guarded formation and dissolution rules. The worked worlds use one local
   contact and a memoryless well-mixed resource. They contain no hidden transit
   completions, geometry inferred from names or arbitrary distance charge.
   Population counts can use the vocabulary, but population ecology is absent.

2. **Matching and multiplicity.** Rules contain local predicates and additive
   coordinate changes. Each valid pair is generated once per rule and source.
   Separate physical mechanisms add their rates in Q and retain separate
   thermodynamic ledgers. Repeated action labels add no history distinctions.
   Actual dependency support is derived from changes, guards, energetic terms
   and validity constraints; an annotation cannot hide those dependencies.
   This is not general subgraph matching or a mass-action multiplicity engine.

3. **Identity.** An explicitly supplied complete finite permutation group
   determines the physical quotient. Symmetry is checked against energy,
   intrinsic degeneracy and aggregate event intensities. Quotient degeneracy
   includes orbit multiplicity. Unmarked permutations vanish throughout a
   history; they are not events with an entropy bonus. A projection that singles
   out an unmarked representative is rejected. Dissipative self-events hidden
   by the quotient are unsupported and rejected rather than silently discarded.

4. **Thermodynamics.** Energies and bills use exact decimal/fractional rational
   values. Coordinate granularity is independent of the energy quantum. For a
   pair i→j, `log(k+/k-) = log(g_j/g_i) + beta*(W-DeltaE)`; positive conductance
   supplies both directions symmetrically. Heat exported is `W-DeltaE`.
   Removing the source removes its paired work-exchange channels. Intrinsic
   log degeneracy affects rates/reference weights, not unresolved history count.
   Only a single source-off communicating reference sector is accepted by the
   availability helper. Multiple sectors need an explicit extension, not an
   arbitrary mixture. Fixed material slots retain their constituents in all
   conformations; a general stoichiometric conservation type system is pending.

5. **Semantics.** Six versioned records preserve the distinctions in the source
   check. Validation checks declared compatibility; it cannot certify physical
   sufficiency or faithfulness empirically. Own-present queries require a
   compatible conditional root law with provenance. Average known-root histories
   and an unknown-root mixture are different quantities. Process metadata
   requires a common present and an implementation description; those declarations
   alone do not prove an implemented intervention. R0–R2 have no policy search.

6. **Identity of evidence.** Physical-model, state-order and generator hashes
   bind an executed query. Mutable compiled data are checked before querying;
   a changed model or matrix requires recompilation. A model hash is a content
   identity, not a theorem of equivalence under all representations. The snapshot
   manifest includes source, configurations and tests; output/source hashes are
   retained. Numerical dependencies and versions are recorded separately.

7. **Backends and budgets.** Sparse complete root-reachable enumeration and
   Gillespie sampling consume the same physical event law. Enumeration over a
   budget returns an unscored incomplete frontier; it never truncates physics
   into a convenient finite generator. The small dense exponential has a
   conservative workspace gate, not a universal LAPACK memory guarantee. The
   supervisor also applies an OS job-memory cap and a wall deadline. Projected
   word queries have an explicit word budget. None of these caps edits the law.

8. **Measurement.** Full sampled-history entropy is computed by the chain rule.
   Projected histories use finite HMM word propagation, with no assumed Markov
   closure. These computations use float64, not exact real arithmetic or certified
   intervals. Structural CTMC reachability establishes sampled support even if
   tiny numeric probabilities underflow. Foreclosure uses history support rather
   than endpoints or an arbitrary probability threshold. The stationary/Poisson
   helper accepts irreducible chains only; a finite profile is never replaced
   by its rate. No randomness is subtracted and Rule A is not a scoring filter.

9. **Resource profile and expansion.** R0 nominally has 30 configurations but
   reaches 18 from its even-bank root. R1 reaches 75 and R2 reaches 180.
   R2's four-work-array dense estimate is about 0.99 MiB, while library/Python
   overhead and word enumeration dominate actual memory. This is a calibration,
   not a scaling promise. Future graph matching, delayed transport, conservation
   sectors and larger entropy solvers must pass the same contracts. R2 constructs
   a larger store; it is not a three-generation compounding experiment.

The future controller, observation and analysis layers should consume this
kernel rather than install independent physics or alternative entropy scores.
No ML/controller abstraction has been inserted before a physical need exists.
