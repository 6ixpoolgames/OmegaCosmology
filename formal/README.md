# Formal arm

The available formal starting source is [Appendix A r19](../sources/v4.1/A_FORMAL_CORE_r19.md),
read with [foundations r4](../sources/v4.1/FOUNDATIONS_r4.md) and current user
clarifications. The supplied Opus review referred to r20; that version was not
found in the Drive intake. No r20 conformance is claimed.

Use contracts/ for explicit semantic definitions and verification/ for the map
between stable proposition IDs, proof status, examples and executable tests.
Chapter numbering is metadata; it is not a semantic identifier.

The [source check](../research/platform/specs/FORMAL_SOURCE_CHECK_r1.md) verifies
targeted r19 definitions, corrects reviewer mappings and separates certification
against a named refinement from physical faithfulness. Foreclosure concerns
history support, not merely endpoint reachability.

Current classical targets include complete conditional history entropy, whole
and projected histories, two present-conditioning modes, resolution relations,
comparison admissibility and reference cases. The quantum/infinite-field scope
is stated in each source; a CTMC test does not validate incompatible quantum
record families or a joint space-time limit.

No new proof assistant package or formal conformance implementation is introduced
by this repository preparation. Historical proofs and finite checks retain
their exact evidence type.
