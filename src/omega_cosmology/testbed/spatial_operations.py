"""Shared finite actuator with externally prescribed spatial assembly couplings."""

from .physics import Condition as C
from .physics import Coordinate, EnergyTerm, LocalModel, Rule


def preparation_model(base, instruction="idle", *, source_on=True):
    """Instruction changes barriers; its exterior selector is not modeled.

    Stroke: bank-2, bond+1, displaced+1. A stroke and thermal relaxation export
    1.5 heat, retaining .5 bond energy. Both inverses remain native.
    """
    if instruction not in ("idle", "aa", "ab") or "actuator" in base.indices:
        raise ValueError("Known instruction and fresh actuator required")
    geometry = next(r for r in base.relations if r["id"] == "geometry")
    edges = geometry["edges"]
    rules = [r for r in base.rules if source_on or r.boundary == "native"]
    rules.append(
        Rule(
            "actuator.thermal",
            (C("actuator", "eq", 0),),
            (("actuator", 1),),
            0.02,
            roles=("operation.thermal",),
        )
    )
    patterns = (
        ()
        if instruction == "idle"
        else ((1, 1),)
        if instruction == "aa"
        else ((1, 2), (2, 1))
    )
    for i, j in edges:
        bond = f"bond.{i}.{j}"
        for a, b in patterns:
            rules.append(
                Rule(
                    f"stroke.{i}.{j}.{a}.{b}",
                    (
                        C(f"site.{i}", "eq", a),
                        C(f"site.{j}", "eq", b),
                        C(bond, "eq", 0),
                        C("bank", "ge", 2),
                        C("actuator", "eq", 0),
                    ),
                    ((bond, 1), ("bank", -2), ("actuator", 1)),
                    0.1,
                    roles=("operation.stroke", "construction.operation"),
                    child=bond,
                )
            )
    return LocalModel(
        base.id + ".actuator-v1",
        list(base.coordinates) + [Coordinate("actuator", (0, 1), "physical_actuator")],
        rules,
        list(base.energy_terms) + [EnergyTerm(".25", "actuator")],
        beta=base.beta,
        forbidden=base.forbidden,
        degeneracy=base.degeneracy_terms,
        material=list(base.material)
        + [{"id": "actuator_molecule", "inventory": [{"coefficient": "1"}]}],
        relations=list(base.relations)
        + [{"id": "actuator", "scope": "exterior_command_finite_paid_stroke"}],
        symmetry=[tuple(p) + (len(base.coordinates),) for p in base.symmetry],
    )


def preparation_root(model):
    """Same unbound full modeled present for idle, aa and ab instructions."""
    values = {"site.0": 1, "site.3": 1, "site.1": 2, "site.4": 2, "bank": 2}
    root = tuple(values.get(c.name, 0) for c in model.coordinates)
    model.validate(root)
    return root
