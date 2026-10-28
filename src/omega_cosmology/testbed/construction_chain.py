"""Bounded two-function construction chain built with explicit module ports."""

from .modules import Binding, Module, Port, compose
from .physics import Condition as C
from .physics import Coordinate as Coord
from .physics import EnergyTerm as E
from .physics import Rule


def slot_inventory(id, *fields):
    return {
        "id": id,
        "inventory": [{"coefficient": "1", "coordinate": f} for f in fields],
    }


def resource_module(source=0.08):
    return Module(
        "metastable_carrier",
        (Coord("state", (0, 1, 2), "resource"),),
        rules=(
            Rule(
                "source",
                (C("state", "eq", 0),),
                (("state", 1),),
                source,
                "3",
                "work_source",
            ),
            Rule("locked_bath", (C("state", "eq", 0),), (("state", 1),), 0.002),
            Rule("usable_bath", (C("state", "eq", 0),), (("state", 2),), 0.002),
            Rule("unlock", (C("state", "eq", 1),), (("state", 1),), 0.02),
        ),
        energy=(
            E("3", conditions=(C("state", "eq", 1),)),
            E("2", conditions=(C("state", "eq", 2),)),
        ),
        material=({"id": "carrier", "inventory": [{"coefficient": "1"}]},),
    )


def construction_chain(
    *,
    assist=True,
    access=True,
    rotor_stroke=0.01,
    rotor_relax=0.003,
    rotor_override=None,
):
    """All arms have identical matter, energy functions, source and native routes.

    A assists conversion of the same precursor into either B or C. B unlocks
    the second carrier; C accelerates capture of the first. B/C compete for one
    precursor. B additionally stores part of the unlocking energy: its function
    is transduction, unlike A's heat-only unlocking. A and rotor each retain an
    existing material slot in both states.
    """
    bank = Port("bank", "energy", (0, 1, 2), ".5")
    binary = lambda name: Port(name, "material_state", (0, 1))
    fuel = Port("fuel", "resource", (0, 1, 2))
    reserve = Module(
        "energy_bank",
        (Coord("ticks", (0, 1, 2), "energy"),),
        energy=(E(".5", "ticks"),),
    )
    a = Module(
        "first_interface",
        (Coord("active", (0, 1), "material_state"),),
        (bank, fuel),
        (
            Rule(
                "basal_build",
                (C("active", "eq", 0),),
                (("active", 1),),
                0.003,
                roles=("construction.basal",),
                child="active",
            ),
            Rule(
                "paid_build",
                (C("active", "eq", 0), C("bank", "ge", 2)),
                (("active", 1), ("bank", -2)),
                0.04,
                roles=("construction.paid",),
                child="active",
            ),
            Rule(
                "unlock",
                (C("active", "eq", 1), C("fuel", "eq", 1)),
                (("fuel", 1),),
                0.12,
                roles=("access.assisted",),
            ),
        ),
        (E(".5", "active"),),
        material=({"id": "slot", "inventory": [{"coefficient": "1"}]},),
    )
    rules = []
    for child in ("B", "C"):
        change = (("precursor", -1), (child, 1))
        guards = (C("precursor", "eq", 1), C(child, "eq", 0))
        rules.extend(
            (
                Rule(
                    "basal_" + child,
                    guards,
                    change,
                    0.003,
                    roles=("construction.basal",),
                    child=child,
                ),
                Rule(
                    "paid_" + child,
                    guards + (C("bank", "ge", 2),),
                    change + (("bank", -2),),
                    0.004,
                    roles=("construction.paid",),
                    child=child,
                ),
            )
        )
        if assist:
            rules.append(
                Rule(
                    "assisted_" + child,
                    guards + (C("bank", "ge", 2), C("helper", "eq", 1)),
                    change + (("bank", -2),),
                    0.04,
                    roles=("construction.assisted",),
                    parent="helper",
                    child=child,
                )
            )
    products = Module(
        "competing_products",
        (
            Coord("precursor", (0, 1), "material_state"),
            Coord("B", (0, 1), "material_state"),
            Coord("C", (0, 1), "material_state"),
        ),
        (bank, binary("helper")),
        tuple(rules),
        (E(".5", "B"), E(".5", "C")),
        forbidden=(
            (C("B", "eq", 1), C("C", "eq", 1)),
            (C("precursor", "eq", 1), C("B", "eq", 1)),
            (C("precursor", "eq", 1), C("C", "eq", 1)),
            (C("precursor", "eq", 0), C("B", "eq", 0), C("C", "eq", 0)),
        ),
        material=(slot_inventory("shared_precursor", "precursor", "B", "C"),),
    )

    def capture_module(assisted):
        rules = [
            Rule(
                "capture",
                (C("fuel", "eq", 2), C("bank", "le", 1)),
                (("fuel", -2), ("bank", 1)),
                0.01,
            )
        ]
        if assisted:
            rules.append(
                Rule(
                    "assisted_capture",
                    (C("fuel", "eq", 2), C("bank", "le", 1), C("helper", "eq", 1)),
                    (("fuel", -2), ("bank", 1)),
                    0.06,
                    roles=("capture.assisted",),
                )
            )
        return Module(
            "capture",
            ports=(bank, fuel) + ((binary("helper"),) if assisted else ()),
            rules=tuple(rules),
        )

    second_access = Module(
        "second_access",
        ports=(fuel, binary("helper"), bank),
        rules=(
            Rule(
                "transduce",
                (C("fuel", "eq", 1), C("helper", "eq", 1), C("bank", "le", 1)),
                (("fuel", 1), ("bank", 1)),
                0.12,
                roles=("access.transduction",),
            ),
        )
        if access
        else (),
    )
    rotor = Module(
        "paid_non_enabling_rotor",
        (Coord("state", (0, 1), "rotor"),),
        (bank, binary("helper")),
        (
            Rule(
                "stroke",
                (C("state", "eq", 0), C("bank", "ge", 1), C("helper", "eq", 1)),
                (("state", 1), ("bank", -1)),
                rotor_stroke,
                roles=("churn.paid",),
            ),
            Rule(
                "relax",
                (C("state", "eq", 0),),
                (("state", 1),),
                rotor_relax,
                roles=("churn.thermal",),
            ),
        ),
        (E(".25", "state"),),
        material=({"id": "slot", "inventory": [{"coefficient": "1"}]},),
    )
    if rotor_override is not None:
        if (
            not isinstance(rotor_override, Module)
            or rotor_stroke != 0.01
            or rotor_relax != 0.003
        ):
            raise ValueError(
                "An explicit rotor module cannot also use legacy rotor parameters"
            )
        rotor = rotor_override
    bindings = [
        Binding(reserve, "bank", {}),
        Binding(resource_module(), "primary", {}),
        Binding(resource_module(), "secondary", {}),
        Binding(a, "A", {"bank": "bank.ticks", "fuel": "primary.state"}),
        Binding(products, "products", {"bank": "bank.ticks", "helper": "A.active"}),
        Binding(
            capture_module(True),
            "primary_capture",
            {"bank": "bank.ticks", "fuel": "primary.state", "helper": "products.C"},
        ),
        Binding(
            capture_module(False),
            "secondary_capture",
            {"bank": "bank.ticks", "fuel": "secondary.state"},
        ),
        Binding(
            second_access,
            "secondary_access",
            {"fuel": "secondary.state", "helper": "products.B", "bank": "bank.ticks"},
        ),
        Binding(
            rotor,
            "rotor",
            {
                p.name: {"bank": "bank.ticks", "helper": "products.B"}[p.name]
                for p in rotor.ports
            },
        ),
    ]
    model = compose("R2-integrated-construction-chain-v2", bindings)
    root = {c.name: 0 for c in model.coordinates}
    root.update(
        {
            "bank.ticks": 2,
            "primary.state": 1,
            "secondary.state": 1,
            "products.precursor": 1,
        }
    )
    return (
        model,
        tuple(root[c.name] for c in model.coordinates),
        [
            {"module": b.module.id, "namespace": b.namespace, "ports": b.ports}
            for b in bindings
        ],
    )
