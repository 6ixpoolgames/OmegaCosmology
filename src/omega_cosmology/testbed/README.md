# Finite classical test bed

The first engineering slice of the reviewed design is implemented here.

| Module | Responsibility |
|---|---|
| semantics | Six serializable records, conditioning, scope and comparison checks |
| physics | Rational energies, finite local rules, reversible event pairs and declared symmetries |
| models | R0 calibration and concrete R1/R2 grammar examples |
| backends | Complete reachable enumeration and shared-law Gillespie trajectories |
| history | Full histories, small projected word laws, support, refinement and irreducible asymptotics |
| thermodynamics | Source-off reference, work/heat ledgers and availability benchmark |
| conformance | Transparent finite mathematical reference cases |
| readouts | Passive coordinate shares, activity coordinates and ordered-event witnesses |
| monitors | Declarative path witnesses with explicit absorbing aborts |
| finite_study | Shared protocol-driven exact assay; R1 reproduction and R2 evaluation |
| analysis | Separate horizon/cadence profiles and directed metric-specific effects |
| structure | Native-route audits and legal-state rate probes with explicit limits |
| ecology | Functional persistence, loss/return and occupancy queries; no ancestry inferred |
| ancestry | Native marked assistance genealogy for distinct binary component slots |
| physical_modules | Versioned storage/damage repair and generic costed cycles sharing a resource |
| projections | Known-root projected-history bounds retaining hidden-state memory |
| workflow | Windows process-tree caps used by the snapshot runner |

Install the testbed extra, then use scripts/run_testbed_calibration.py. The
engineering report and worked models are under research/platform/. This package
does not yet implement population ecology, generic graph matching, spatial
transport or an optimizer. A sampler path is not an entropy estimator. No
physical-faithfulness or ethical-correspondence claim follows from these tests.

See the [ecology analysis contract](../../../research/platform/specs/ECOLOGY_ANALYSIS_SPEC_r1.md).
Organization predicates and monitor labels are query-only. Ordered monitors
cannot certify connected ancestry; local coordinate entropy shares cannot stand
in for a subject's projected history entropy.
The separate ancestry adapter tracks constructed parents and children, resets
basal replacements to depth zero, preserves historical achievement after loss,
and rejects unsupported exchangeable or multiple-parent attributions.
The [coupled slice](../../../research/platform/specs/COUPLED_AUTOCATALYTIC_SLICE_SPEC_r1.md)
uses these modules; it does not change retained R1/R2-v1 laws. The projection
bound adapter reports interval width and rejects over-budget words and unsupported
conditioning. Its analytic inequalities are evaluated numerically, not with
rigorous interval arithmetic.
