"""Two bank-paid rotor strokes with a fixed native thermal baseline."""

from .construction_chain import construction_chain
from .modules import Module, Port
from .physics import Condition as C
from .physics import Coordinate, EnergyTerm, LocalModel, Rule

THERMAL_CONDUCTANCE = 0.003


def paid_rotor(*, charge=0.01, reset=0.01, gated=True):
    """A clockwise cycle draws one energy unit; each native reverse refunds.

    Bank-independent thermal switching remains fixed and is never optimized.
    Conductances change barriers symmetrically, not thermodynamic affinities.
    """
    helper = (C("helper", "eq", 1),) if gated else ()
    return Module(
        "paid_two_stroke_rotor",
        (Coordinate("state", (0, 1), "rotor"),),
        (Port("bank", "energy", (0, 1, 2), ".5"),)
        + ((Port("helper", "material_state", (0, 1)),) if gated else ()),
        (
            Rule(
                "stroke",
                (C("state", "eq", 0), C("bank", "ge", 1)) + helper,
                (("state", 1), ("bank", -1)),
                charge,
                roles=("churn.paid", "rotor.charge"),
            ),
            Rule(
                "reset",
                (C("state", "eq", 1), C("bank", "ge", 1)) + helper,
                (("state", -1), ("bank", -1)),
                reset,
                roles=("churn.paid", "rotor.reset"),
            ),
            Rule(
                "relax",
                (C("state", "eq", 0),),
                (("state", 1),),
                THERMAL_CONDUCTANCE,
                roles=("churn.thermal",),
            ),
        ),
        (EnergyTerm(".25", "state"),),
        material=({"id": "slot", "inventory": [{"coefficient": "1"}]},),
    )


def paid_cycle_chain(*, assist=True, access=True, charge=0.01, reset=0.01, gated=True):
    model, root, bindings = construction_chain(
        assist=assist,
        access=access,
        rotor_override=paid_rotor(charge=charge, reset=reset, gated=gated),
    )
    # Metadata version distinguishes this successor while preserving v2 defaults.
    model = LocalModel.from_record(
        {**model.record(), "id": "R2-fixed-thermal-paid-cycle-v1"}
    )
    return model, root, bindings
