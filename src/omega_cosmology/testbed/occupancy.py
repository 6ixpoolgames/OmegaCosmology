"""Finite reversible catalytic contacts over distinct physical component slots.

Contact occupancy is physical. Diagnostic genealogy is not. This adapter leaves
the old instantaneous-assistance worlds and their fingerprints unchanged.
"""

from dataclasses import replace
from itertools import combinations

from .physical_modules import autocatalytic_ecology
from .physics import Condition as C
from .physics import Coordinate, EnergyTerm, LocalModel, Rule, rational


def occupied_ecology(
    groups,
    *,
    binding_energy="-.25",
    binding_conductance=0.04,
    assistance_edges=None,
    converting_edges=None,
    **kwargs,
):
    """Replace instantaneous assisted construction by binding then conversion.

    Each distinct constituent has one port, shared by substrate binding and its
    helper/capture uses. Recipient pays conversion. Native bound failure and
    unassisted substrate construction dissolve the contact, with paired reverses.
    """
    base = autocatalytic_ecology(groups, **kwargs)
    originals = [r for r in base.rules if r.id.startswith("assisted_construct_")]
    available = {}
    for rule in originals:
        parent = next(
            c.coordinate for c in rule.guards if c.operator == "eq" and c.value == 1
        )
        child = next(k for k, d in rule.changes if d == 1)
        available[parent, child] = rule
    chosen = (
        list(available)
        if assistance_edges is None
        else list(map(tuple, assistance_edges))
    )
    if len(set(chosen)) != len(chosen) or any(e not in available for e in chosen):
        raise ValueError("Distinct declared assistance edges required")
    conversions = (
        chosen if converting_edges is None else list(map(tuple, converting_edges))
    )
    if len(set(conversions)) != len(conversions) or any(
        e not in chosen for e in conversions
    ):
        raise ValueError("Conversion edges must be distinct bound assistance edges")
    rational(binding_energy)
    contacts = {
        edge: "contact." + available[edge].id.removeprefix("assisted_construct_")
        for edge in chosen
    }
    incident = {
        c.name: [] for c in base.coordinates if c.role == "constructed_component"
    }
    for (parent, child), contact in contacts.items():
        incident[parent].append(contact)
        incident[child].append(contact)
    coords = list(base.coordinates)
    energies = list(base.energy_terms)
    forbidden = list(base.forbidden)
    for (parent, child), contact in contacts.items():
        coords.append(Coordinate(contact, (0, 1), "catalytic_contact"))
        energies.append(EnergyTerm(str(binding_energy), contact))
        forbidden.extend(
            [
                (C(contact, "eq", 1), C(parent, "eq", 0)),
                (C(contact, "eq", 1), C(child, "eq", 1)),
            ]
        )
    for names in incident.values():
        forbidden.extend(
            (C(a, "eq", 1), C(b, "eq", 1)) for a, b in combinations(names, 2)
        )

    def free(fields):
        return tuple(
            C(k, "eq", 0) for k in sorted({x for f in fields for x in incident[f]})
        )

    rules = []
    for rule in base.rules:
        if rule in originals:
            continue
        # A component-changing event or capture catalysis needs its own port.
        fields = {k for k, _ in rule.changes if k in incident}
        if rule.id.startswith("assisted_capture_"):
            fields.update(c.coordinate for c in rule.guards if c.coordinate in incident)
        rules.append(replace(rule, guards=rule.guards + free(fields)))
        if not (
            rule.id.startswith("basal_construct_")
            or rule.id.startswith("paid_construct_")
        ):
            continue
        field = next(k for k, d in rule.changes if k in incident and d == 1)
        for (parent, child), contact in contacts.items():
            if field not in (parent, child):
                continue
            # Parent failure: forward rebuilds helper+contact, reverse breaks both.
            # Substrate birth: forward builds product and releases helper.
            delta = 1 if field == parent else -1
            guards = rule.guards + (C(contact, "eq", 0 if delta == 1 else 1),)
            rules.append(
                replace(
                    rule,
                    id=rule.id + ".bound." + contact,
                    guards=guards,
                    changes=rule.changes + ((contact, delta),),
                    mechanism="native construction/failure dissolves or restores contact; paired reverse",
                )
            )
    for (parent, child), contact in contacts.items():
        original = available[parent, child]
        rules.append(
            Rule(
                "bind." + contact,
                (C(parent, "eq", 1), C(child, "eq", 0)) + free((parent, child)),
                ((contact, 1),),
                binding_conductance,
                mechanism="reversible binding sequesters a finite helper and substrate port",
            )
        )
        if (parent, child) in conversions:
            rules.append(
                replace(
                    original,
                    guards=original.guards + (C(contact, "eq", 1),),
                    changes=original.changes + ((contact, -1),),
                    mechanism="occupied native helper assists recipient-paid construction then releases",
                )
            )
    model = LocalModel(
        "autocatalytic-ecology-occupied-v1",
        coords,
        rules,
        energies,
        beta=base.beta,
        forbidden=forbidden,
        relations=list(base.relations)
        + [
            {
                "id": name,
                "parent": p,
                "child": c,
                "interface_capacity": 1,
                "construction": "reversible physical bond",
                "helper_cost": "occupied port; recipient pays conversion",
            }
            for (p, c), name in contacts.items()
        ],
        material=base.material,
    )
    return model


def contact_state_bound(model):
    """Exact legal product-space count for this adapter, without enumerating states.

    Matchings can grow exponentially; this helper is for small reference models.
    """
    contacts = [r for r in model.relations if "interface_capacity" in r]
    if len(contacts) > 20:
        raise ValueError("Combinatorial reference limited to twenty contacts")
    members = sum(c.role == "constructed_component" for c in model.coordinates)
    other = 1
    for c in model.coordinates:
        if c.role not in ("constructed_component", "catalytic_contact"):
            other *= len(c.domain)
    count = 0
    for size in range(len(contacts) + 1):
        for chosen in combinations(contacts, size):
            fields = [v[k] for v in chosen for k in ("parent", "child")]
            if len(set(fields)) == len(fields):
                count += 2 ** (members - len(fields))
    return other * count
