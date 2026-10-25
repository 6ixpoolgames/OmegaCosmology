# Worked engineering worlds

These are serializable instances of one rule grammar. Rebuild their JSON with
`python scripts/write_testbed_fixtures.py`. The files contain all six semantic
records as well as coordinates, energies, local rules, relations and material
slot declarations. No comparative scientific ranking follows from their scores.

## R0: binding and accessible fuel

Two fixed constituents can bind. `bond` is 0/1; `carrier` is spent=0, locked=1,
usable=2; `bank` is an integer number of half-energy ticks from 0 to 4.
The state contains everything the memoryless transition law depends on.
One local contact is assumed; there is no represented transport delay.

The energy is `-.5*bond + .5*bank + E(carrier)`, with carrier energies 0,3,2.
Beta is 1 and intrinsic degeneracy is 1. Every row below is a reversible pair.
The displayed k is symmetric conductance, not the actual directional rate.

| Forward pair | Guard | Changes | k | Forward external work |
|---|---|---|---:|---:|
| source | spent carrier | spent→locked | .08 | 3 |
| locked native bath | spent carrier | spent→locked | .002 | 0 |
| usable native bath | spent carrier | spent→usable | .002 | 0 |
| basal unlock | locked carrier | locked→usable | .02 | 0 |
| capture | usable, bank≤2 | usable→spent, bank+2 | .06 | 0 |
| binding | bond=0 | bond+1 | .04 | 0 |
| motif unlock | bond=1, locked | locked→usable | .12 | 0 |

For every pair the reverse is generated from the same guards on its forward
source, with opposite changes/work/heat. Rates follow the ratio documented in
the engineering decisions. Catalysis adds a paired path and preserves its
equilibrium ratio. The native fluctuations and basal unlock remain available
whether bound or unbound. The motif applies at every eligible bank value.

The root `(0,1,0)` has energy 3. There are 30 Cartesian configurations, but
capture changes bank by two ticks and the root has even parity, yielding 18
reachable states. The Gibbs reference is restricted to that sector. The source
is bidirectional work exchange; starting with charged fuel can give negative
net accepted work over a short calibration. That is retained in the ledger.

## R1: paid reconstruction

[R1.json](R1.json) adds inactive/active conformations of each of the two fixed
constituents. Each active conformation costs .5 energy. Both active units are
required to bind; an inactive unit cannot remain bonded. Each unbound unit can
activate basally at k=.003, or use two bank ticks at k=.04. The paid forward
construction consumes energy 1, raises conformation energy .5, and exports heat
.5. The exact reverse reconstructs the source and refunds the stored balance.
Bonding still releases .5 energy and forms the interface enabling unlock.

A bonded interface also permits bank relaxation by one tick at k=.01, with its
thermal reverse. This is a coarse reversible upkeep channel, not a detailed
failure/repair network. Repair currently goes through unbinding, activation
and rebinding; there is no invisible repair of a damaged bound constituent.
The root `(1,0,0,1,2)` has energy 4.5. All 75 admissible states are reachable.

## R2: constructing another interface

[R2.json](R2.json) adds a third, always-present material slot in an unbuilt/built
storage conformation. Building it consumes two ticks, stores .5 energy and
exports .5 heat. The basal pair has k=.003; the existing bonded interface
assists the same pair at k=.04 in both directions. A built store permits bank
ticks 5 and 6; unbuilt configurations with those contents are inadmissible.
Reverse dissolution is unavailable while the returned bank energy would violate
capacity, exactly as forward filling is unavailable beyond capacity.

The root `(1,0,0,1,2,0)` has energy 4.5. The 180 reachable states cover five
unbuilt-bank values and seven built-bank values, five admissible constituent/
bond conformations and three carrier states. This demonstrates that paid
construction can expose new capacity through the same grammar. It does not
demonstrate unbounded growth, three-link genealogy or robust compounding.

## Limits and metadata examples

[SEMANTIC_EXAMPLES.json](SEMANTIC_EXAMPLES.json) gives full/own-present,
mechanism/preparation and implemented-process metadata examples. Its process
entry is a validation example; an actuator world is still required before a
process comparison is executed. R0–R2 contain no oracle-selected policy,
uninformative sensor comparator or embodied-agent search.

Bath/source histories remain unresolved in every world. Report scope as the
whole **modeled** field. Boundary matching is not a cancellation proof.
