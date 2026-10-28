"""R0–R2 are data-level instances of one local rule vocabulary."""

from .physics import Condition as C
from .physics import Coordinate, LocalModel, Rule
from .physics import EnergyTerm as E


def resource_rules(bank_max):
    return [
        Rule(
            "source",
            (C("carrier", "eq", 0),),
            (("carrier", 1),),
            0.08,
            "3",
            "work_source",
            mechanism="maintained carrier drive",
        ),
        Rule("native_locked_bath", (C("carrier", "eq", 0),), (("carrier", 1),), 0.002),
        Rule("native_usable_bath", (C("carrier", "eq", 0),), (("carrier", 2),), 0.002),
        Rule("unlock_basal", (C("carrier", "eq", 1),), (("carrier", 1),), 0.02),
        Rule(
            "capture",
            (C("carrier", "eq", 2), C("bank", "le", bank_max - 2)),
            (("carrier", -2), ("bank", 2)),
            0.06,
            support=("carrier", "bank"),
            mechanism="capture stores 1 native energy unit",
        ),
    ]


def resource_energy():
    return [
        E("3", conditions=(C("carrier", "eq", 1),)),
        E("2", conditions=(C("carrier", "eq", 2),)),
        E(".5", "bank"),
    ]


def calibration_world():
    coords = [
        Coordinate("bond", (0, 1), "relation"),
        Coordinate("carrier", (0, 1, 2), "resource"),
        Coordinate("bank", tuple(range(5)), "energy"),
    ]
    rules = resource_rules(4) + [
        Rule(
            "binding",
            (C("bond", "eq", 0),),
            (("bond", 1),),
            0.04,
            mechanism="two component reversible binding",
        ),
        Rule(
            "unlock_motif",
            (C("bond", "eq", 1), C("carrier", "eq", 1)),
            (("carrier", 1),),
            0.12,
            support=("bond", "carrier"),
            mechanism="bonded local interface assists conversion",
        ),
    ]
    return LocalModel(
        "R0-binding-access",
        coords,
        rules,
        resource_energy() + [E("-.5", "bond")],
        relations=(
            {
                "id": "bond",
                "support": ["component_a", "component_b"],
                "geometry": "one local contact",
                "capacity": 1,
                "transit": "no resolved transport",
            },
        ),
        material=(
            {
                "id": "component_slots",
                "quantity": 2,
                "inventory": [{"coefficient": "2"}],
                "conservation": "fixed material constituents",
            },
        ),
    ), (0, 1, 0)


def enabling_world(*, expansion=False):
    """The same pattern/change primitives encode paid activation and new storage."""
    bank_max = 6 if expansion else 4
    coords = [
        Coordinate("a.active", (0, 1), "material_state", "a"),
        Coordinate("b.active", (0, 1), "material_state", "b"),
        Coordinate("bond", (0, 1), "relation"),
        Coordinate("carrier", (0, 1, 2), "resource"),
        Coordinate("bank", tuple(range(bank_max + 1)), "energy"),
    ]
    forbidden = [(C("bond", "eq", 1), C(k, "eq", 0)) for k in ("a.active", "b.active")]
    rules = resource_rules(bank_max)
    energies = resource_energy() + [
        E(".5", "a.active"),
        E(".5", "b.active"),
        E("-.5", "bond"),
    ]
    for unit in ("a.active", "b.active"):
        guards = (C(unit, "eq", 0), C("bond", "eq", 0))
        rules += [
            Rule("basal_activate_" + unit, guards, ((unit, 1),), 0.003),
            Rule(
                "paid_activate_" + unit,
                guards + (C("bank", "ge", 2),),
                ((unit, 1), ("bank", -2)),
                0.04,
                support=(unit, "bank"),
                mechanism="precursor conformation constructed using stored work",
            ),
        ]
    rules += [
        Rule(
            "binding",
            (C("a.active", "eq", 1), C("b.active", "eq", 1), C("bond", "eq", 0)),
            (("bond", 1),),
            0.04,
            support=("a.active", "b.active", "bond"),
        ),
        Rule(
            "unlock_motif",
            (C("bond", "eq", 1), C("carrier", "eq", 1)),
            (("carrier", 1),),
            0.12,
            support=("bond", "carrier"),
            mechanism="assembled interface assists resource conversion",
        ),
        Rule(
            "upkeep",
            (C("bond", "eq", 1), C("bank", "ge", 1)),
            (("bank", -1),),
            0.01,
            support=("bond", "bank"),
            mechanism="native paid relaxation and reverse fluctuation",
        ),
    ]
    relations = [
        {
            "id": "bond",
            "support": ["a.active", "b.active"],
            "geometry": "one local contact",
            "capacity": 1,
            "transit": "no resolved transport",
            "repair": "native unbind/reconstruct/rebind paths",
        }
    ]
    material = [
        {
            "id": "constituent_slots",
            "quantity": 2,
            "inventory": [{"coefficient": "2"}],
            "conservation": "each precursor/active state retains its material slot",
        }
    ]
    if expansion:
        coords.append(Coordinate("store.built", (0, 1), "material_state", "storage"))
        energies.append(E(".5", "store.built"))
        forbidden.append((C("store.built", "eq", 0), C("bank", "ge", 5)))
        rules += [
            Rule(
                "build_store",
                (C("store.built", "eq", 0), C("bank", "ge", 2)),
                (("store.built", 1), ("bank", -2)),
                0.003,
                support=("store.built", "bank"),
            ),
            Rule(
                "build_store_assisted",
                (C("store.built", "eq", 0), C("bank", "ge", 2), C("bond", "eq", 1)),
                (("store.built", 1), ("bank", -2)),
                0.04,
                support=("store.built", "bank", "bond"),
                mechanism="first assembly enables paid construction of second interface",
            ),
        ]
        relations.append(
            {
                "id": "storage_interface",
                "support": ["store.built", "bank"],
                "geometry": "adjacent bank contact",
                "capacity": "2 extra half-energy ticks when built",
                "transit": "effective memoryless local exchange",
                "repair": "same paid construction pair",
            }
        )
        material.append(
            {
                "id": "latent_storage_slot",
                "quantity": 1,
                "inventory": [{"coefficient": "1"}],
                "conservation": "precursor or built, never free new material",
            }
        )
    model = LocalModel(
        "R2-further-storage" if expansion else "R1-paid-reconstruction",
        coords,
        rules,
        energies,
        forbidden=forbidden,
        relations=relations,
        material=material,
    )
    root = (1, 0, 0, 1, 2, 0) if expansion else (1, 0, 0, 1, 2)
    return model, root


def two_copy_world(*, quotient):
    coords = [
        Coordinate("first", (0, 1), "unmarked_internal"),
        Coordinate("second", (0, 1), "unmarked_internal"),
    ]
    rules = [
        Rule("flip_" + c.name, (C(c.name, "eq", 0),), ((c.name, 1),), 0.1)
        for c in coords
    ]
    return LocalModel(
        "two-unmarked-copies",
        coords,
        rules,
        [],
        symmetry=((0, 1), (1, 0)) if quotient else (),
    ), (0, 0)
