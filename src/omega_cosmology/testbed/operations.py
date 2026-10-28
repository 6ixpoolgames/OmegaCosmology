"""Paid, reversible operations on existing constituents; no prepared fault roots."""

from itertools import product

from .physics import Condition as C
from .physics import Coordinate, EnergyTerm, LocalModel, Rule, rational


def operation_world(
    base,
    *,
    target=None,
    bank="repair.bank",
    bill_ticks=1,
    stroke_conductance=None,
    relaxation_conductance=0.02,
    actuator="operation.displaced",
    actuator_energy=".25",
):
    """Append identical hardware; optionally enable a damage or sham stroke.

    target=None with a stroke is a paid non-enabling sham. Without a stroke it
    is idle/common recovery. Changing conductance is an external barrier pulse,
    not free internal policy choice. Every rule has its physical native reverse.
    """
    if (
        bank not in base.indices
        or actuator in base.indices
        or type(bill_ticks) is not int
        or bill_ticks < 1
        or rational(actuator_energy) <= 0
    ):
        raise ValueError(
            "Existing bank, positive bill/energy and fresh actuator required"
        )
    if target is not None and (
        target not in base.indices
        or base.coordinates[base.indices[target]].role != "constructed_component"
    ):
        raise ValueError("Damage targets an existing constructed component")
    if target is not None and stroke_conductance is None:
        raise ValueError("A target requires an enabled physical stroke")
    contacts = sorted(
        r["id"]
        for r in base.relations
        if "interface_capacity" in r and target in (r["parent"], r["child"])
    )
    if len(contacts) > 8:
        raise ValueError(
            "Explicit contact-pattern operation limited to eight incident bonds"
        )
    rules = list(base.rules)
    rules.append(
        Rule(
            "operation.thermal",
            (C(actuator, "eq", 0),),
            ((actuator, 1),),
            relaxation_conductance,
            mechanism="finite actuator thermal displacement and relaxation",
        )
    )
    if stroke_conductance is not None:
        for bits in product((0, 1), repeat=len(contacts)):
            guards = (C(actuator, "eq", 0), C(bank, "ge", bill_ticks))
            changes = ((actuator, 1), (bank, -bill_ticks))
            if target is not None:
                guards += (C(target, "eq", 1),)
                changes += ((target, -1),)
            guards += tuple(C(c, "eq", b) for c, b in zip(contacts, bits))
            changes += tuple((c, -1) for c, b in zip(contacts, bits) if b)
            rules.append(
                Rule(
                    "operation.stroke."
                    + (target or "sham")
                    + "."
                    + "".join(map(str, bits)),
                    guards,
                    changes,
                    stroke_conductance,
                    mechanism="bank-paid actuator stroke; target/contact energy goes to heat; paired inverse",
                    roles=("operation.stroke",),
                )
            )
    return LocalModel(
        base.id + ".operation-v1",
        list(base.coordinates) + [Coordinate(actuator, (0, 1), "physical_actuator")],
        rules,
        list(base.energy_terms) + [EnergyTerm(str(actuator_energy), actuator)],
        beta=base.beta,
        forbidden=base.forbidden,
        degeneracy=base.degeneracy_terms,
        symmetry=[tuple(p) + (len(base.coordinates),) for p in base.symmetry],
        relations=list(base.relations)
        + [
            {
                "id": actuator,
                "physical_role": "finite paid stroke hardware; barrier externally prescribed",
            }
        ],
        material=list(base.material)
        + [
            {
                "id": actuator,
                "quantity": 1,
                "inventory": [{"coefficient": "1"}],
                "conservation": "one actuator, relaxed or displaced",
            }
        ],
    )
