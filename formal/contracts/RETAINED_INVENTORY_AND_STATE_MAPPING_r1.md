# Retained-unit inventory witnesses and constraint-state mappings

30 October 2026. Implemented finite-adapter contract. It does not establish
conformance to an unavailable newer Appendix A or repair physical omissions in
an old model.

## Retained units

A legacy declaration may stipulate that a named component remains the same
physical unit in precursor/constructed or charged/spent states. For a named
coordinate x with declared domain D, an explicit state-meaning witness gives
the partition:

    N_x(s) = sum_(v in D) 1[x(s)=v] = 1.

The inventory of a collection of distinct such slots is the sum of their
partitions. It is conserved in every legal state and therefore under every
native event; the interpreted model also executes its material checks on event
pairs. Missing values, duplicate slots, conflicting declared quantities and
replacing an existing executable inventory are rejected. Energy ticks and
relations cannot be counted as independent retained material units by this
adapter.

This is a proof about the model's explicitly assumed fixed units. It is not
evidence for chemical composition or conservation of unresolved atoms/waste,
and does not fill in omitted environmental/register hardware. The state meanings
are an explicit physical interpretation, not something a conservation equation
can discover. Adding the witness gives a new input fingerprint. A separate
equivalence check must verify that no states, rates, energies or event marks
changed; the legacy input remains descriptively unverified as originally stored.

## Common physical alphabet

Two mechanism laws can have identical coordinates, domains, Hamiltonian,
degeneracy, material assumptions and symmetry while forbidding different state
configurations. Let S_L and S_R be their complete reachable canonical state
sets. The first mapping adapter uses their identity-labelled union
A = S_L union S_R, with injections i_L and i_R.

A mapping binds both model hashes and both state-order hashes. Every differing
forbidden pattern must be declared. Every remaining grammar field except ID
and rule set must agree. Roots, source boundaries, conditioning, quantity,
resolution and actual endowment are checked separately by the paired validator.
Mapping does not waive those checks. It is not supported for an enacted-process
claim, a preparation under different laws or a hidden-state projection.

The distribution of any finite native word w is pushed to i(w) with the same
probability. Since each symbol map is injective, each induced word map is
injective. Hence its Shannon entropy is unchanged at every finite horizon.
Absent symbols have zero weight. The union does not create a generator: absent
states are not given physical self-loops, thermal transitions or new histories.

The selected R2 mechanism comparison has 180 useful-capacity states and
150 sham states. Shared coordinates still distinguish all native outcomes; an
explicit constraint map allows their word measures to be compared on a common
alphabet without conditioning on the 150-state intersection. It does not repair
the missing loaded-store spill/maintenance physics identified in that study.

## What a passing certificate says

The ordinary strict validator is unchanged when no mapping is supplied. The
material-required mode rejects absent inventories as well as prose-only ones.
A passing interpreted pair establishes declared finite grammar, actual initial
energy, scoped inventory totals, observation/window/boundary matching and the
specific mapping conditions. It does not establish all material closure,
exterior cancellation, physical-resolution faithfulness or ethical correspondence.

Implementation: [inventory witnesses](../../src/omega_cosmology/testbed/inventory_witness.py),
[state mappings](../../src/omega_cosmology/testbed/state_mapping.py),
[paired validator](../../src/omega_cosmology/testbed/semantics.py).
Adversarial tests: [paired qualification](../../tests/test_paired_qualification.py).
