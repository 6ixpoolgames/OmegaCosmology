"""Paid registers and physical responses on a small repairable access world.

All channels use LocalModel's paired thermodynamic law. No event label is
counted as an outcome, and no state is assigned valence or ethical weight.
"""

from .physics import Condition as C
from .physics import Coordinate, LocalModel, Rule
from .physics import EnergyTerm as E


def _extend(model, *, coordinates=(), rules=(), energy=(), relations=()):
    return LocalModel(
        model.id,
        (*model.coordinates, *coordinates),
        (*model.rules, *rules),
        (*model.energy_terms, *energy),
        beta=model.beta,
        forbidden=model.forbidden,
        degeneracy=model.degeneracy_terms,
        symmetry=model.symmetry if not coordinates else (),
        relations=(*model.relations, *relations),
        material=model.material,
    )


def hazard_access_world(*, barrier_conductance=0.02, beta=2.0):
    """Repairable apparatus, four half-unit bank levels and one source carrier.

    Location 0 is exposed; 1 is sheltered with faster capture. Barrier 0 blocks
    transit, 1 allows it. None means a fixed barrier, with the root selecting
    its conserved sector; a positive conductance supplies reversible openings.
    """
    if barrier_conductance is not None and barrier_conductance <= 0:
        raise ValueError("Use None for a fixed barrier, or positive conductance")
    coords = [
        Coordinate("body.working", (0, 1), "constructed_component", "body"),
        Coordinate("body.bank", tuple(range(4)), "energy", "body"),
        Coordinate("body.location", (0, 1), "location", "body"),
        Coordinate("hazard", (0, 1), "environment"),
        Coordinate("barrier", (0, 1), "physical_barrier"),
        Coordinate("carrier", (0, 1), "source_carrier"),
    ]
    rules = [
        Rule(
            "source",
            (C("carrier", "eq", 0),),
            (("carrier", 1),),
            0.08,
            work="3",
            boundary="work_source",
            mechanism="maintained reversible charging; source histories unresolved",
        ),
        Rule("hazard_toggle", (C("hazard", "eq", 0),), (("hazard", 1),), 0.03),
        Rule(
            "basal_restore",
            (C("body.working", "eq", 0),),
            (("body.working", 1),),
            0.003,
        ),
        Rule(
            "paid_restore",
            (C("body.working", "eq", 0), C("body.bank", "ge", 2)),
            (("body.working", 1), ("body.bank", -2)),
            0.04,
            mechanism="bank pays one unit to restore apparatus; reverse retained",
        ),
        Rule(
            "hazard_damage",
            (
                C("hazard", "eq", 1),
                C("body.location", "eq", 0),
                C("body.working", "eq", 1),
            ),
            (("body.working", -1),),
            0.08,
            mechanism="exposure catalyses breakdown AND its thermal reverse",
        ),
        Rule("metabolism", (C("body.bank", "ge", 1),), (("body.bank", -1),), 0.02),
    ]
    if barrier_conductance is not None:
        rules.append(
            Rule(
                "barrier_toggle",
                (C("barrier", "eq", 0),),
                (("barrier", 1),),
                barrier_conductance,
            )
        )
    for loc, conductance in [(0, 0.008), (1, 0.08)]:
        rules.append(
            Rule(
                f"capture_{loc}",
                (
                    C("carrier", "eq", 1),
                    C("body.bank", "le", 2),
                    C("body.working", "eq", 1),
                    C("body.location", "eq", loc),
                ),
                (("carrier", -1), ("body.bank", 1)),
                conductance,
                mechanism="working apparatus captures source energy; sheltered access is faster",
            )
        )
    for loc in (0, 1):
        rules.append(
            Rule(
                f"native_move_{loc}",
                (
                    C("body.location", "eq", loc),
                    C("barrier", "eq", 1),
                    C("body.bank", "ge", 1),
                    C("body.working", "eq", 1),
                ),
                (("body.location", 1 if loc == 0 else -1), ("body.bank", -1)),
                0.004,
                mechanism="unassisted paid movement; paired thermal reverse retained",
            )
        )
    return LocalModel(
        "paid-warning-access-v1",
        coords,
        rules,
        [E("1", "body.working"), E(".5", "body.bank"), E("1.5", "carrier")],
        beta=beta,
        material=[
            {"id": "body_slot", "states": "working/damaged retained material"},
            {"id": "carrier_slot", "states": "charged/spent retained carrier"},
        ],
    )


def with_paid_register(
    model,
    *,
    tracking=True,
    on_conductance=0.008,
    off_conductance=0.025,
    upkeep_conductance=0.01,
):
    """One energetic bit: bank-paid writing, native relaxation and paid upkeep.

    Tracking changes the paired write conductance by 15x in exposed hazard.
    It does not copy an uncosted observation into the state. The independent
    control uses the same write bill, bit energy and upkeep rule.
    """
    rules = []
    for loc in (0, 1):
        for hazard in (0, 1):
            high = tracking and loc == 0 and hazard == 1
            rules.append(
                Rule(
                    f"signal_write_{loc}_{hazard}",
                    (
                        C("body.location", "eq", loc),
                        C("hazard", "eq", hazard),
                        C("body.signal", "eq", 0),
                        C("body.bank", "ge", 2),
                    ),
                    (("body.signal", 1), ("body.bank", -2)),
                    on_conductance * (15 if high else 1),
                    mechanism="energetically paid sensor coupling; paired reverse is a refund",
                )
            )
    rules += [
        Rule(
            "signal_relax",
            (C("body.signal", "eq", 1),),
            (("body.signal", -1),),
            off_conductance,
            mechanism="energetic register relaxes to heat; thermal excitation retained",
        ),
        Rule(
            "signal_upkeep",
            (C("body.signal", "eq", 1), C("body.bank", "ge", 1)),
            (("body.bank", -1),),
            upkeep_conductance,
            mechanism="positive upkeep while register is on; paired reverse retained",
        ),
    ]
    return _extend(
        model,
        coordinates=[Coordinate("body.signal", (0, 1), "physical_register", "body")],
        energy=[E("1", "body.signal")],
        rules=rules,
    )


def with_escape_response(model, *, enabled=True, conductance=0.08):
    """Signal-dependent actuation spends reserve, including at a blocked barrier.

    A blocked attempt is a physical bank decrement, not a distinguishable
    self-event label. Parallel bank-loss channels aggregate in the generator.
    The no-response arm retains the entire register and all native routes.
    """
    if not enabled:
        return model
    guard = (
        C("body.signal", "eq", 1),
        C("body.location", "eq", 0),
        C("body.working", "eq", 1),
        C("body.bank", "ge", 1),
    )
    rules = [
        Rule(
            "escape",
            guard + (C("barrier", "eq", 1),),
            (("body.location", 1), ("body.bank", -1)),
            conductance,
            mechanism="signal-powered escape; reverse returns location and reserve",
        ),
        Rule(
            "blocked_effort",
            guard + (C("barrier", "eq", 0),),
            (("body.bank", -1),),
            conductance,
            mechanism="blocked effort dissipates reserve without opening the route",
        ),
    ]
    return _extend(model, rules=rules)


def with_paid_push_pull_register(
    model, *, tracking=True, on_conductance=0.008, off_conductance=0.008
):
    """Bank-driven write AND reset paths, not merely kinetic equilibration.

    Writing dissipates .5 and stores .5 energy. Active reset spends another
    .5 from the bank. Exposed hazard catalyses writing; its absence catalyses
    resetting. Both retain native reverse paths. Independent controls have
    identical bit energy and bills; only rate dependence differs.
    """
    rules = []
    for loc in (0, 1):
        for hazard in (0, 1):
            exposed = loc == 0 and hazard == 1
            shared = (C("body.location", "eq", loc), C("hazard", "eq", hazard))
            rules.extend(
                [
                    Rule(
                        f"signal_write_{loc}_{hazard}",
                        shared + (C("body.signal", "eq", 0), C("body.bank", "ge", 2)),
                        (("body.signal", 1), ("body.bank", -2)),
                        on_conductance * (15 if tracking and exposed else 1),
                        mechanism="paid writing dissipates .5 and stores .5; reverse retained",
                    ),
                    Rule(
                        f"signal_reset_{loc}_{hazard}",
                        shared + (C("body.signal", "eq", 1), C("body.bank", "ge", 1)),
                        (("body.signal", -1), ("body.bank", -1)),
                        off_conductance * (15 if tracking and not exposed else 1),
                        mechanism="paid reset dissipates bank .5 plus register .5; reverse retained",
                    ),
                ]
            )
    rules.extend(
        [
            Rule(
                "signal_relax",
                (C("body.signal", "eq", 1),),
                (("body.signal", -1),),
                0.025,
                mechanism="passive relaxation and thermal excitation remain",
            ),
            Rule(
                "signal_upkeep",
                (C("body.signal", "eq", 1), C("body.bank", "ge", 1)),
                (("body.bank", -1),),
                0.01,
                mechanism="positive on-state upkeep, native reverse retained",
            ),
        ]
    )
    return _extend(
        model,
        coordinates=[Coordinate("body.signal", (0, 1), "physical_register", "body")],
        energy=[E(".5", "body.signal")],
        rules=rules,
    )


def warning_world(
    *,
    tracking=True,
    response=True,
    barrier_conductance=0.02,
    on_conductance=0.008,
    off_conductance=None,
    sensor="kinetic",
):
    if sensor not in ("kinetic", "push_pull"):
        raise ValueError("Declare kinetic or push_pull sensor")
    if off_conductance is None:
        off_conductance = 0.025 if sensor == "kinetic" else 0.008
    register = (
        with_paid_register if sensor == "kinetic" else with_paid_push_pull_register
    )
    return with_escape_response(
        register(
            hazard_access_world(barrier_conductance=barrier_conductance),
            tracking=tracking,
            on_conductance=on_conductance,
            off_conductance=off_conductance,
        ),
        enabled=response,
    )


def warning_root(*, open_barrier=False):
    return (1, 3, 0, 1, int(open_barrier), 0, 0)
