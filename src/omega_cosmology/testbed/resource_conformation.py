"""Explicit categorical carrier conformations with common native bath routes."""

from dataclasses import asdict
from fractions import Fraction

from .physics import Condition, EnergyTerm, LocalModel, Rule


def add_resource_conformation(model, *, resource, value, energy, links, conductance):
    """Extend a categorical resource, not a clock, bank or independent register.

    Existing rules/energy terms are retained. Callers must verify that existing
    guards and inventory declarations do not accidentally reinterpret new codes.
    This operation changes the physical law and is not a relabelling refinement.
    """
    if resource not in model.indices or type(value) is not int:
        raise ValueError("Existing resource and integer conformation code required")
    index = model.indices[resource]
    coordinate = model.coordinates[index]
    if coordinate.role not in ("resource", "shared_resource", "source_carrier"):
        raise ValueError("Only a categorical resource can acquire a conformation")
    if value in coordinate.domain or not links or len(set(links)) != len(links):
        raise ValueError("New code and distinct existing native neighbours required")
    if any(v not in coordinate.domain for v in links):
        raise ValueError("Native links must reference existing resource states")
    if any(t.coordinate == resource for t in model.energy_terms):
        raise ValueError("Resource energy must be categorical, not integer-code energy")
    amount = str(Fraction(energy))
    record = model.record()
    record["id"] += ".resource-conformation-v1"
    record["coordinates"][index]["domain"] = sorted((*coordinate.domain, value))
    record["energy_terms"].append(
        asdict(EnergyTerm(amount, conditions=(Condition(resource, "eq", value),)))
    )
    for neighbour in links:
        name = f"native_{resource}_{neighbour}_to_{value}"
        if name in {r.id for r in model.rules}:
            raise ValueError("Native conformation rule already exists")
        record["rules"].append(
            asdict(
                Rule(
                    name,
                    (Condition(resource, "eq", neighbour),),
                    ((resource, value - neighbour),),
                    conductance,
                    roles=("resource.native_conformation",),
                    mechanism="Native reversible thermal conformation of the same carrier",
                )
            )
        )
    return LocalModel.from_record(record)
