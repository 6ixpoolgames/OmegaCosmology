"""Versioned physical fixtures composed from the existing reversible grammar.

No functions here alter retained R1/R2 models. All native channels keep their
reverse and energy accounting. These are stipulated finite chemistries.
"""

from .models import enabling_world, resource_energy
from .physics import Condition as C
from .physics import Coordinate, LocalModel, Rule, rational
from .physics import EnergyTerm as E


def repaired_capacity_world(*, spill_conductance=0.001, damage_conductance=0.004):
    """R2-v2 adds refund-independent breakdown and bound damage, removes fake upkeep.

    Every load-specific store breakdown releases its content to heat and ends
    at an empty unbuilt bank. Reverse thermal assembly/loading is retained.
    Paid activation restores damage; native substitutes remain. There is no
    free repair or immediate empty-bank shutdown imposed by the analysis.
    """
    old, root = enabling_world(expansion=True)
    rules = [r for r in old.rules if r.id != "upkeep"]
    for load in range(7):
        change = (("store.built", -1),) + ((("bank", -load),) if load else ())
        rules.append(
            Rule(
                f"store_spill_{load}",
                (C("store.built", "eq", 1), C("bank", "eq", load)),
                change,
                spill_conductance,
                mechanism="store breaks and dissipates stored contents; native reverse retained",
            )
        )
    for field in ("a.active", "b.active"):
        rules.append(
            Rule(
                "bound_damage_" + field,
                (C("bond", "eq", 1), C(field, "eq", 1)),
                ((field, -1), ("bond", -1)),
                damage_conductance,
                mechanism="damage breaks a working constituent and its contact, independent of bank",
            )
        )
    model = LocalModel(
        "R2-v2-spill-and-bound-damage",
        old.coordinates,
        rules,
        old.energy_terms,
        beta=old.beta,
        forbidden=old.forbidden,
        relations=old.relations,
        material=old.material,
    )
    return model, root


def autocatalytic_ecology(
    groups,
    *,
    extra_assistance=(),
    driven=True,
    bank_capacity=2,
    bank_quantum="1",
    construction_bill_ticks=1,
    formation_energy=".5",
    basal_conductance=0.003,
    repair_conductance=0.02,
    assistance_conductance=0.06,
    capture_conductance=0.004,
    assisted_capture_conductance=0.05,
    source_conductance=0.08,
):
    """Compose distinct local component cycles sharing a finite carrier.

    Group records provide ID, members and an access member. Each member assists
    paid construction of its cyclic successor using the recipient group's bank.
    Extra (parent, child) edges use the same paid chemistry. Contacts are fixed,
    well mixed and explicit; this is not spatial colonization or a population.
    """
    if not groups or type(bank_capacity) is not int or bank_capacity < 1:
        raise ValueError("Groups and positive integer bank capacity required")
    if (
        type(construction_bill_ticks) is not int
        or not 1 <= construction_bill_ticks <= bank_capacity
    ):
        raise ValueError(
            "Construction bill must fit the bank without changing capacity"
        )
    quantum = rational(bank_quantum)
    if (
        quantum <= 0
        or rational(formation_energy) <= 0
        or construction_bill_ticks * quantum < rational(formation_energy)
    ):
        raise ValueError("Positive quantum and bill at least formation energy required")
    ids, members = set(), {}
    coords, rules, energies, relations, material, edges = [], [], [], [], [], []
    for group in groups:
        name, fields = group["id"], tuple(group["members"])
        if (
            not name
            or name in ids
            or len(fields) < 2
            or len(set(fields)) != len(fields)
            or group["access_member"] not in fields
        ):
            raise ValueError(
                "Unique groups need at least two distinct components and an access member"
            )
        ids.add(name)
        bank = name + ".bank"
        for field in fields:
            if field in members or field == bank or field == "carrier":
                raise ValueError("Component names collide")
            members[field] = name
            coords.append(Coordinate(field, (0, 1), "constructed_component", name))
            energies.append(E(str(formation_energy), field))
        coords.append(Coordinate(bank, tuple(range(bank_capacity + 1)), "energy", name))
        energies.append(E(str(quantum), bank))
        for field in fields:
            absent = (C(field, "eq", 0),)
            rules += [
                Rule(
                    "basal_construct_" + field,
                    absent,
                    ((field, 1),),
                    basal_conductance,
                    mechanism="native construction and bank-independent thermal breakdown",
                ),
                Rule(
                    "paid_construct_" + field,
                    absent + (C(bank, "ge", construction_bill_ticks),),
                    ((field, 1), (bank, -construction_bill_ticks)),
                    repair_conductance,
                    mechanism="paid reconstruction with formation energy and heat accounted",
                ),
            ]
        for parent, child in zip(fields, fields[1:] + fields[:1]):
            edges.append((parent, child))
        rules += [
            Rule(
                "capture_" + name,
                (C("carrier", "eq", 2), C(bank, "le", bank_capacity - 1)),
                (("carrier", -2), (bank, 1)),
                capture_conductance,
                mechanism="basal capture competes for one shared carrier",
            ),
            Rule(
                "assisted_capture_" + name,
                (
                    C("carrier", "eq", 2),
                    C(bank, "le", bank_capacity - 1),
                    C(group["access_member"], "eq", 1),
                ),
                (("carrier", -2), (bank, 1)),
                assisted_capture_conductance,
                mechanism="constructed local interface assists access; native route stays",
            ),
        ]
        relations.append(
            {
                "id": name + ".contact",
                "support": list(fields) + [bank, "carrier"],
                "geometry": "fixed well-mixed contact to a shared finite carrier",
                "construction": "interfaces require the corresponding constructed members",
                "transport": "no resolved spatial displacement or migration",
            }
        )
        material.append(
            {
                "id": name + ".slots",
                "quantity": len(fields),
                "conservation": "fixed distinct material slots, precursor or constructed",
            }
        )
    all_names = [c.name for c in coords] + ["carrier"]
    if len(set(all_names)) != len(all_names):
        raise ValueError("Bank, member and carrier names must be distinct")
    edges.extend(tuple(pair) for pair in extra_assistance)
    if len(set(edges)) != len(edges):
        raise ValueError("Duplicate assistance edge")
    for parent, child in edges:
        if parent not in members or child not in members or parent == child:
            raise ValueError("Assistance needs two declared component slots")
        bank = members[child] + ".bank"
        rules.append(
            Rule(
                "assisted_construct_" + parent + "_to_" + child,
                (
                    C(parent, "eq", 1),
                    C(child, "eq", 0),
                    C(bank, "ge", construction_bill_ticks),
                ),
                ((child, 1), (bank, -construction_bill_ticks)),
                assistance_conductance,
                mechanism="native marked parent assists paid construction; paired reverse retained",
            )
        )
    coords.append(Coordinate("carrier", (0, 1, 2), "shared_resource"))
    energies += resource_energy()[:2]
    if driven:
        rules.append(
            Rule(
                "source",
                (C("carrier", "eq", 0),),
                (("carrier", 1),),
                source_conductance,
                "3",
                "work_source",
                mechanism="maintained reversible work supply",
            )
        )
    rules += [
        Rule("native_locked_bath", (C("carrier", "eq", 0),), (("carrier", 1),), 0.002),
        Rule("native_usable_bath", (C("carrier", "eq", 0),), (("carrier", 2),), 0.002),
        Rule("unlock_basal", (C("carrier", "eq", 1),), (("carrier", 1),), 0.02),
    ]
    return LocalModel(
        "autocatalytic-ecology-v1",
        coords,
        rules,
        energies,
        relations=relations,
        material=material
        + [
            {
                "id": "shared_carrier",
                "quantity": 1,
                "conservation": "one carrier switches state; no extra matter",
            }
        ],
    )


def assistance_spec(model, fields, *, depth_cap=3):
    """Select actual native assisted construction channels, not arbitrary births."""
    fields = list(fields)
    edges = []
    for rule in model.rules:
        if not rule.id.startswith("assisted_construct_"):
            continue
        children = [k for k, delta in rule.changes if k in fields and delta == 1]
        parents = [
            c.coordinate
            for c in rule.guards
            if c.coordinate in fields and c.operator == "eq" and c.value == 1
        ]
        if len(children) == len(parents) == 1:
            edges.append({"rule": rule.id, "parent": parents[0], "child": children[0]})
    return {
        "id": "construction_depth",
        "presence_coordinates": fields,
        "depth_cap": depth_cap,
        "identity_definition": "Distinct constituent slots; breakdown ends an instance; paid or basal rebuilding creates a new instance",
        "assistance_edges": edges,
    }
