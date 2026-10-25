"""Fuel-powered readiness registers; retained readiness-v1 remains unchanged."""

from dataclasses import replace
from math import isfinite

from .physics import Condition as C
from .physics import LocalModel, Rule, rational
from .readiness import readiness_world
from .registers import RegisterPayment, paid_register_rule

FUEL_ONLY = RegisterPayment("0", True)
FUEL_AND_BANK = RegisterPayment(".5", True)


def powered_readiness_world(
    policy,
    *,
    bank_quantum=".5",
    effort_bill=".5",
    memory_write_bill=".5",
    cue_write=FUEL_ONLY,
    cue_reset=FUEL_ONLY,
    memory_clear=FUEL_AND_BANK,
    cue_energy=".25",
    mark_energy=".125",
    cue_conductance=0.02,
    cue_selectivity=16.0,
    cue_relaxation=0.0001,
    cue_upkeep_conductance=0.002,
    cue_upkeep_bill=".5",
    clear_conductance=0.12,
    response_conductance=0.08,
    attempts_enabled=True,
    source_enabled=True,
    **physical,
):
    if type(attempts_enabled) is not bool or type(source_enabled) is not bool:
        raise ValueError("Declare boolean pathway/source controls")
    for value in (
        cue_conductance,
        cue_selectivity,
        clear_conductance,
        response_conductance,
    ):
        if not isfinite(value) or value <= 0:
            raise ValueError(
                "Positive finite circuit conductances/selectivity required"
            )
    for value in (cue_relaxation, cue_upkeep_conductance):
        if not isfinite(value) or value < 0:
            raise ValueError("Nonnegative finite passive/upkeep conductance required")
    if rational(cue_energy) <= 0 or rational(mark_energy) <= 0:
        raise ValueError("Positive stored register energies required")
    base = readiness_world(
        policy,
        bank_quantum=bank_quantum,
        effort_bill=effort_bill,
        memory_bill=memory_write_bill,
        **physical,
    )
    for payment in (
        cue_write,
        cue_reset,
        memory_clear,
        RegisterPayment(cue_upkeep_bill),
    ):
        if not isinstance(payment, RegisterPayment):
            raise TypeError("Typed register payments required")
        payment.terms(base, bank_quantum)
    rules = []
    for rule in base.rules:
        if rule.id.startswith(
            ("cue_write_", "cue_reset_", "cue_clear_")
        ) or rule.id in ("cue_relax", "cue_upkeep"):
            continue
        if not source_enabled and rule.boundary != "native":
            continue
        if rule.id.startswith(("escape_", "blocked_effort_", "effort_damage_")):
            if not attempts_enabled:
                continue
            rule = replace(
                rule, conductance=rule.conductance * response_conductance / 0.08
            )
        rules.append(rule)
    for opened in (0, 1):
        for write in (True, False):
            template = Rule(
                f"cue_{'write' if write else 'reset'}_{opened}",
                (C("barrier", "eq", opened), C("body.cue", "eq", 0 if write else 1)),
                (("body.cue", 1 if write else -1),),
                cue_conductance * (cue_selectivity if bool(opened) == write else 1),
                mechanism="paid physical cue cycle; reverse consumes heat and refunds its declared inputs",
            )
            rules.append(
                paid_register_rule(
                    template,
                    base,
                    cue_write if write else cue_reset,
                    bank_quantum,
                    variable_changes=template.changes,
                )
            )
    if cue_relaxation:
        rules.append(
            Rule(
                "cue_relax",
                (C("body.cue", "eq", 1),),
                (("body.cue", -1),),
                cue_relaxation,
            )
        )
    if cue_upkeep_conductance:
        template = Rule(
            "cue_upkeep",
            (C("body.cue", "eq", 1),),
            (("body.bank", -1),),
            cue_upkeep_conductance,
        )
        rules.append(
            paid_register_rule(
                template,
                base,
                RegisterPayment(cue_upkeep_bill),
                bank_quantum,
                variable_changes=(),
            )
        )
    if policy == "reengage":
        limit = max(base.domains[base.indices["body.failures"]])
        for count in range(1, limit + 1):
            template = Rule(
                f"cue_clear_{count}",
                (
                    C("body.failures", "eq", count),
                    C("body.cue", "eq", 1),
                    C("body.working", "eq", 1),
                ),
                (("body.failures", -1),),
                clear_conductance,
                mechanism="fuel-powered cue clearing; no oracle reset and native reverse retained",
            )
            rules.append(
                paid_register_rule(
                    template,
                    base,
                    memory_clear,
                    bank_quantum,
                    variable_changes=template.changes,
                )
            )
    energy = [
        replace(
            term,
            coefficient=str(cue_energy)
            if term.coordinate == "body.cue"
            else str(mark_energy),
        )
        if term.coordinate in ("body.cue", "body.failures")
        else term
        for term in base.energy_terms
    ]
    return LocalModel(
        "paid-readiness-v2",
        base.coordinates,
        rules,
        energy,
        beta=base.beta,
        forbidden=base.forbidden,
        degeneracy=base.degeneracy_terms,
        symmetry=base.symmetry,
        material=base.material,
        relations=(
            *base.relations,
            {
                "id": "physical_register_power",
                "meaning": "Cue and reset inputs drawn from existing bank/carrier; no new work source or observer",
                "attempts_enabled": attempts_enabled,
                "source_enabled": source_enabled,
            },
        ),
    )
