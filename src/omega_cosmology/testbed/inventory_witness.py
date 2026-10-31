"""Explicit interpretations of legacy retained-slot material declarations.

A slot partition establishes retained-unit counts, not chemical stoichiometry.
It adds no states, rules or physical capacity and never replaces an existing
executable inventory. Historical records are not mutated.
"""

from copy import deepcopy
from dataclasses import dataclass

from .physics import LocalModel


@dataclass(frozen=True)
class RetainedSlot:
    coordinate: str
    states: tuple[tuple[int, str], ...]

    def __post_init__(self):
        object.__setattr__(self, "states", tuple(tuple(v) for v in self.states))
        if (
            not self.coordinate
            or not self.states
            or any(
                type(value) is not int or not isinstance(label, str) or not label
                for value, label in self.states
            )
        ):
            raise ValueError("Named slot and explicit physical state meanings required")
        if len({v for v, _ in self.states}) != len(self.states):
            raise ValueError("Slot state partition repeats a value")


@dataclass(frozen=True)
class InventoryWitness:
    inventory_id: str
    slots: tuple[RetainedSlot, ...]
    justification: str

    def __post_init__(self):
        object.__setattr__(self, "slots", tuple(self.slots))
        if not self.inventory_id or not self.slots or not self.justification:
            raise ValueError(
                "Inventory identity, named slots and justification required"
            )


def interpret_retained_slots(model, witnesses):
    """Return a newly fingerprinted interpretation and a provenance receipt.

    The source assumption is explicit: each named slot retains its unit in all
    listed states. A complete disjoint domain partition verifies its inventory
    function for every legal state, including currently unreachable ones.
    """
    witnesses = tuple(witnesses)
    original = model.record()
    declared = {m["id"]: m for m in model.material}
    ids = [w.inventory_id for w in witnesses]
    if not declared or len(set(ids)) != len(ids) or set(ids) != set(declared):
        raise ValueError(
            "Witnesses must cover every original material declaration exactly"
        )
    if any("inventory" in item for item in model.material):
        raise ValueError("Do not replace or weaken an existing executable inventory")
    allowed_roles = {
        "material_state",
        "constructed_component",
        "resource",
        "shared_resource",
        "source_carrier",
    }
    used = set()
    record = deepcopy(original)
    receipts = []
    for witness in witnesses:
        declaration = next(
            m for m in record["material"] if m["id"] == witness.inventory_id
        )
        quantity = declaration.get("quantity")
        if quantity is not None and (
            type(quantity) is not int or quantity != len(witness.slots)
        ):
            raise ValueError("Slot witness disagrees with original declared quantity")
        terms, slots = [], []
        for slot in witness.slots:
            if slot.coordinate in used or slot.coordinate not in model.indices:
                raise ValueError("Duplicate material slot or unknown coordinate")
            coordinate = model.coordinates[model.indices[slot.coordinate]]
            if coordinate.role not in allowed_roles:
                raise ValueError(
                    "Energy, relation or register is not an independently declared retained material unit"
                )
            if {v for v, _ in slot.states} != set(coordinate.domain):
                raise ValueError("Slot partition must cover its entire physical domain")
            used.add(slot.coordinate)
            for value, _ in slot.states:
                terms.append(
                    {
                        "coefficient": "1",
                        "conditions": [
                            {
                                "coordinate": slot.coordinate,
                                "operator": "eq",
                                "value": value,
                            }
                        ],
                    }
                )
            slots.append(
                {
                    "coordinate": slot.coordinate,
                    "states": [list(v) for v in slot.states],
                }
            )
        declaration["inventory"] = terms
        declaration["inventory_scope"] = (
            "declared_retained_units_only_not_chemical_closure"
        )
        receipts.append(
            {
                "id": witness.inventory_id,
                "retained_units": len(witness.slots),
                "slots": slots,
                "source_declaration": deepcopy(declared[witness.inventory_id]),
                "interpretation_justification": witness.justification,
            }
        )
    record["id"] += ".retained-slot-interpretation-v1"
    interpreted = LocalModel.from_record(record)
    for field, value in original.items():
        if field not in ("id", "material") and interpreted.record()[field] != value:
            raise ArithmeticError("Inventory interpretation changed physical law")
    return interpreted, {
        "source_model_hash": model.fingerprint(),
        "interpreted_model_hash": interpreted.fingerprint(),
        "changed_fields": ["id", "material"],
        "inventories": receipts,
        "scope": "Fixed retained-unit interpretation; no atom/waste/bath-material or full chemical closure certificate",
        "law_equivalence": "requires native compilation/event-ledger comparison; metadata is not sufficient",
    }
