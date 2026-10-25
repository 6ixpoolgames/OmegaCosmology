# Executable reference map — first engineering slice

Sources: available Appendix A r19, read with foundations r4. This map records
finite examples and numerical checks, not machine proofs or r20 conformance.
The [source check](../../research/platform/specs/FORMAL_SOURCE_CHECK_r1.md)
governs the corrections to reviewer-supplied result IDs.

| Result / issue | Executable check | Status and limit |
|---|---|---|
| A.2.1 chain rule | conformance `chain_rule`; worker direct word sum | Full finite word sum agrees numerically |
| A.5.2 mixture versus average | `mixture_vs_root_average`; typed query test | Root draw is not added twice |
| A.7.1 own/full conditioning | `own_vs_full_present`; compatible-root validation | Explicit root law, pointwise distinction |
| A.7.3 projected memory | `projection_memory` | Strong-lumpability test; no assumed observed Markov law |
| A.1.2 / A.6.2 identity | labelled/quotient history test, mid-history swap test | Declared finite group only |
| A.6.5 / A.6.6 refinement | `named_refinement` | Certificate inequality separate from physical faithfulness |
| A.9.3 / A.9.4 foreclosure | `contraction_foreclosure`, `full_support_no_foreclosure`; word/DP comparison | History supports, not endpoints |
| Positive-cadence CTMC support | graph closure plus underflow test | Structural support survives numeric underflow |
| A.7.11 correlated exterior | `correlated_exterior` | Finite example with unchanged margins; no infinite-field proof |
| A.1 deterministic conditioning | `nontrivial_determinism` | Discrete cyclic map has ell=0 despite state change |
| Scalar compression / different response | `equal_entropy_different_response` | Constant row-entropy construction; coupled profiles can still tie |
| A.8.2 nonacting register | `nonacting_register` | Algebraic reference; not an embodied cost claim |
| A.7.6 self/whole gap | `self_whole_correlation` | Correlation changes joint breadth while the part ties |
| A.3.5 / A.11.1 / A.11.2 preparation | same-law stationary/Poisson test | Irreducible finite case; bounded offset numerically checked |
| Degeneracy | unresolved-state and orbit-Gibbs tests | Rates/reference weights change; no unresolved history bonus |
| Boundary and event accounting | source-off balance, paired-rate, parallel-ledger and trajectory tests | One bath, fixed material slots, unresolved exterior |
| A.2.1 coordinate chain rule | correlated-coordinate readout test | Current-coordinate shares conditioned on the full past; fixed order |
| Fine-cadence coordinates | symmetric-switch analytic Nbar/F and refinement test | Expected Poisson count and asymptotic remainder; no physical cutoff theorem |
| Passive ordered path witness | Poisson-tail and marginalized-propagation test | Query monitor adds no scored physical histories |

The [R1 readout tests](../../tests/test_testbed_readouts.py) add these checks and
verify that experimental variants remove only their declared paired channels,
while preserving the matched material/energy preparations.

The [shared-assay tests](../../tests/test_finite_study.py) check a four-event
monitor against a Poisson tail, absorbing aborts, genuinely capacity-dependent
captures, a costed sham, retained R1 numerical reproduction and unmarked-query
identity guards. Marked-path queries on nontrivial symmetry quotients require
an equivariance audit and are currently rejected; invariant whole-history and
count readouts remain supported. These guards do not add physical labels.

The twelve `run_reference_cases` records are in the calibration summary. Further
checks are in [kernel tests](../../tests/test_testbed_kernel.py) and
[query tests](../../tests/test_testbed_queries.py). Statistical sampler agreement
is distinct from deterministic numerical identities.

The 25 October [structural-analysis checks](../../tests/test_structural_analysis.py)
separate horizon/cadence changes, detect R2's refund lock and basal bypasses,
verify functional survival/loss/return against a symmetric-switch analytic law,
reject initially absent paths as recovered survivors, and preserve metric-specific
interaction disagreements. The [assistance-ancestry checks](../../tests/test_assistance_ancestry.py)
distinguish connected depth from unrelated births, reset unassisted replacements,
retain historical achievement after loss, and verify unchanged physical marginals
and scores. This is native-marked ancestry on distinct binary slots, not general
genealogy, catalytic necessity, resource attribution or a new formal theorem.

The [projected-history bounds contract](../contracts/projected-history-bounds-r1.md)
supplies finite observed-memory upper/lower inequalities without assuming the
observation is Markov. [Projection tests](../../tests/test_projection_bounds.py)
check them against exhaustive word laws and the shared assay. They are float64
evaluations of analytic inequalities, not rigorous numerical certificates.
[Coupled-physics tests](../../tests/test_coupled_physics.py) check spill at every
load, direct damage, paid repair bills, resource competition, recipient-bank
cross-assistance and source-off equilibrium. These do not validate the toy rates
against real chemistry or establish favorable scientific rankings.

E1 adds explicit law/cadence plan validation, backward-compatible physical
defaults, cost isolation from storage capacity/yield, and a shared multi-window
projection traversal checked against individual finite-history queries. Signed
interval sums preserve unresolved subject comparisons, including factorial
contrasts. The [E1 validation](../../research/studies/E1-coupled-autocatalysis/VALIDATION.md)
does not establish physical-grain faithfulness or ethical correspondence.

Pending: general reducible-class/absorption asymptotics; rigorous projected
entropy intervals at large horizons; implemented controller-policy comparisons
(A.2.5); all-horizon symbolic equality certificates beyond the explicit constant
row-entropy construction; infinite-field limiting proof; arbitrary present
sections; physical grain selection; quantum/incompatible record families; r20
delta verification. These do not become passed cases by metadata declaration.
