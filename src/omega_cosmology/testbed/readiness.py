"""Consequential reserve expenditure and paid physical response memory.

Compose a new version over S4b without changing any retained warning world.
All physical memory, noisy cues and reverse/refund reactions stay in the law.
"""

from dataclasses import replace
from math import isfinite, log, sqrt

from .physics import Condition as C
from .physics import Coordinate, LocalModel, Rule, rational
from .physics import EnergyTerm as E
from .signals import warning_world

POLICIES = ("always", "conserve", "stop", "reengage")


def _ticks(value, quantum, *, positive=True):
    result = rational(value) / quantum
    if result.denominator != 1 or result < (1 if positive else 0):
        raise ValueError("Bill/threshold must be an exact nonnegative bank quantum")
    return int(result)


def readiness_world(
    policy,
    *,
    bank_quantum=".5",
    effort_bill=".5",
    memory_bill=".5",
    failure_limit=2,
    source_conductance=0.04,
    repair_conductance=0.01,
    opening_rate=0.02,
    closing_rate=0.25,
    low_reserve_damage=0.02,
    low_reserve_threshold=".5",
    effort_damage_weight=0.1,
    memory_relaxation=0.0001,
):
    if policy not in POLICIES:
        raise ValueError("Declare a supported physical response mechanism")
    if type(failure_limit) is not int or not 1 <= failure_limit <= 4:
        raise ValueError("The exact reference uses one to four failure marks")
    q = rational(bank_quantum)
    if q <= 0 or rational(".5") / q < 1:
        raise ValueError("Positive bank quantum must resolve the old half-unit bills")
    scale = _ticks(".5", q)
    capacity = _ticks("1.5", q)
    effort, memory = _ticks(effort_bill, q), _ticks(memory_bill, q)
    if effort + memory > capacity:
        raise ValueError("Effort plus failure-memory bill must fit full reserve")
    if not 0 <= effort_damage_weight < 1 or not isfinite(effort_damage_weight):
        raise ValueError("Damage-channel conductance weight must lie in [0,1)")
    if low_reserve_damage < 0 or not isfinite(low_reserve_damage):
        raise ValueError("Nonnegative finite low-reserve damage conductance")
    threshold = _ticks(low_reserve_threshold, q, positive=False)
    if threshold > capacity:
        raise ValueError("Reserve threshold must fit the bank")
    base = warning_world(sensor="push_pull", response=False, barrier_conductance=None)
    coords = [
        replace(c, domain=tuple(range(capacity + 1))) if c.name == "body.bank" else c
        for c in base.coordinates
    ]
    energy = [
        replace(t, coefficient=str(q)) if t.coordinate == "body.bank" else t
        for t in base.energy_terms
    ]
    rules = []
    for r in base.rules:
        guards = tuple(
            replace(c, value=c.value * scale) if c.coordinate == "body.bank" else c
            for c in r.guards
        )
        changes = tuple((k, d * scale if k == "body.bank" else d) for k, d in r.changes)
        conductance = {
            "source": source_conductance,
            "paid_restore": repair_conductance,
        }.get(r.id, r.conductance)
        rules.append(
            replace(r, guards=guards, changes=changes, conductance=conductance)
        )
    if opening_rate is not None:
        if not all(isfinite(v) and v > 0 for v in (opening_rate, closing_rate)):
            raise ValueError("Positive finite opening/closing rates required")
        energy.append(E(str(log(closing_rate / opening_rate) / base.beta), "barrier"))
        rules.append(
            Rule(
                "barrier_toggle",
                (C("barrier", "eq", 0),),
                (("barrier", 1),),
                sqrt(opening_rate * closing_rate),
                mechanism="native opportunity opening/closing with barrier energy accounted",
            )
        )
    if low_reserve_damage:
        rules.append(
            Rule(
                "low_reserve_damage",
                (C("body.working", "eq", 1), C("body.bank", "le", threshold)),
                (("body.working", -1),),
                low_reserve_damage,
                mechanism="reserve-dependent breakdown and thermal reverse, not irreversible death",
            )
        )
    coords += [
        Coordinate(
            "body.failures", tuple(range(failure_limit + 1)), "physical_memory", "body"
        ),
        Coordinate("body.cue", (0, 1), "physical_register", "body"),
    ]
    energy += [E(".125", "body.failures"), E(".25", "body.cue")]
    for count in range(1, failure_limit + 1):
        rules.append(
            Rule(
                f"failure_relax_{count}",
                (C("body.failures", "eq", count),),
                (("body.failures", -1),),
                memory_relaxation,
                mechanism="slow physical forgetting plus reverse thermal mark errors",
            )
        )
    for opened in (0, 1):
        common = (C("barrier", "eq", opened),)
        rules += [
            Rule(
                f"cue_write_{opened}",
                common + (C("body.cue", "eq", 0), C("body.bank", "ge", scale)),
                (("body.cue", 1), ("body.bank", -scale)),
                0.02 * (16 if opened else 1),
                mechanism="bank-paid observation, faster at an open barrier; reverse retained",
                roles=("register.cue",),
            ),
            Rule(
                f"cue_reset_{opened}",
                common + (C("body.cue", "eq", 1), C("body.bank", "ge", scale)),
                (("body.cue", -1), ("body.bank", -scale)),
                0.02 * (1 if opened else 16),
                mechanism="bank-paid cue reset; stale and false cues remain possible",
                roles=("register.cue",),
            ),
        ]
    rules += [
        Rule(
            "cue_relax",
            (C("body.cue", "eq", 1),),
            (("body.cue", -1),),
            0.0001,
            roles=("register.cue",),
        ),
        Rule(
            "cue_upkeep",
            (C("body.cue", "eq", 1), C("body.bank", "ge", scale)),
            (("body.bank", -scale),),
            0.002,
            roles=("register.cue",),
        ),
    ]
    response_guard = (
        C("body.signal", "eq", 1),
        C("body.location", "eq", 0),
        C("body.working", "eq", 1),
    )
    active = range(failure_limit + 1) if policy == "always" else range(failure_limit)
    if policy != "conserve":
        for count in active:
            limit = (C("body.failures", "eq", count),)
            rules.append(
                Rule(
                    f"escape_{count}",
                    response_guard
                    + limit
                    + (C("barrier", "eq", 1), C("body.bank", "ge", effort)),
                    (("body.location", 1), ("body.bank", -effort)),
                    0.08,
                    mechanism="funded warning response below declared physical memory threshold",
                    roles=("response.attempt",),
                )
            )
            writing = count < failure_limit
            bill = effort + (memory if writing else 0)
            changes = (("body.bank", -bill),) + (
                (("body.failures", 1),) if writing else ()
            )
            guard = (
                response_guard
                + limit
                + (C("barrier", "eq", 0), C("body.bank", "ge", bill))
            )
            rules.append(
                Rule(
                    f"blocked_effort_{count}",
                    guard,
                    changes,
                    0.08 * (1 - effort_damage_weight),
                    mechanism="failed attempt pays effort and unsaturated physical memory; reverse can undo both",
                    roles=("response.attempt",),
                )
            )
            if effort_damage_weight:
                rules.append(
                    Rule(
                        f"effort_damage_{count}",
                        guard,
                        changes + (("body.working", -1),),
                        0.08 * effort_damage_weight,
                        mechanism="distinct paid effort outcome damages repairable apparatus; native reverse retained",
                        roles=("response.attempt",),
                    )
                )
    if policy == "reengage":
        for count in range(1, failure_limit + 1):
            rules.append(
                Rule(
                    f"cue_clear_{count}",
                    (
                        C("body.failures", "eq", count),
                        C("body.cue", "eq", 1),
                        C("body.bank", "ge", scale),
                        C("body.working", "eq", 1),
                    ),
                    (("body.failures", -1), ("body.bank", -scale)),
                    0.12,
                    mechanism="cue-dependent mark clearing pays reserve, not an oracle reset",
                    roles=("register.cue",),
                )
            )
    return LocalModel(
        "paid-readiness-v1",
        coords,
        rules,
        energy,
        beta=base.beta,
        material=base.material,
        relations=[
            {
                "id": "failure_register",
                "meaning": "noisy physical mark count, not exact historical count",
            },
            {
                "id": "opening_cue",
                "meaning": "paid finite-rate observation, not direct barrier knowledge",
            },
        ],
    )


def readiness_root(model):
    values = {
        "body.working": 1,
        "body.bank": max(model.domains[model.indices["body.bank"]]),
        "hazard": 1,
    }
    return tuple(values.get(c.name, 0) for c in model.coordinates)
