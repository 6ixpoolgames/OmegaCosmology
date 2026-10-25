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
