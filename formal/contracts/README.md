# Semantic contracts

The active platform specification defines six public records: PresentSpec,
LawSpec, ObservationSpec, ComparisonSpec, QuantitySpec and EvidenceSpec.
Nested scope, conditioning and resolution fields retain distinct meanings.

Contract implementations are in
[semantics.py](../../src/omega_cosmology/testbed/semantics.py), with
[serializable examples](../../research/platform/models/SEMANTIC_EXAMPLES.json).
They preserve sufficient-state declarations, native-law probabilities,
physical options versus conditioning, history projections and support limits.
Sufficiency/faithfulness remain physical claims; compatible metadata does not
prove them. The initial version uses dataclass records, not a general schema DSL.

Projected-history readouts have separate contracts:

- [Analytic finite-memory inequalities](projected-history-bounds-r1.md).
- [Predictive-filter statistical estimator](projected-filter-estimator-r1.md),
  including exact-mean controls and approximate versus distribution-free intervals.

An estimated interval must not be passed off as an analytic projection bound.
The [S1 confidence design](../../research/platform/specs/PROJECTED_CONFIDENCE_FEASIBILITY_r1.md)
specifies finite-sample family coverage separately from numerical error, using
the proven path-score support width and a fixed sampling plan.
