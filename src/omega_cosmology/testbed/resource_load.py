"""Apparatus-gated resource relaxation, with its native energy-return channel.

The factory does not certify a paid load. Actual net source/resource flows must
be measured; reverses, equilibrium activity and initial stores are not ignored.
"""

from dataclasses import asdict

import numpy as np

from .physics import Condition, LocalModel, Rule

LOAD_ROLE = "load.resource_relaxation"


def attach_resource_load(
    model,
    *,
    resource,
    charged,
    spent,
    helper_conditions,
    conductance,
    rule_id="resource_load",
):
    helpers = tuple(helper_conditions)
    if not helpers or any(
        not isinstance(c, Condition) or c.coordinate == resource for c in helpers
    ):
        raise ValueError(
            "Existing apparatus conditions, distinct from resource, required"
        )
    if (
        resource not in model.indices
        or type(charged) is not int
        or type(spent) is not int
        or charged == spent
    ):
        raise ValueError("Two distinct states of an existing resource required")
    if model.coordinates[model.indices[resource]].role not in (
        "resource",
        "shared_resource",
        "source_carrier",
    ):
        raise ValueError("A bank or register cannot be relabelled as the resource")
    domain = model.coordinates[model.indices[resource]].domain
    if (
        charged not in domain
        or spent not in domain
        or any(c.coordinate not in model.indices for c in helpers)
    ):
        raise ValueError("Resource/helper outside declared physical grammar")
    if rule_id in {r.id for r in model.rules}:
        raise ValueError("Load rule already exists")
    rule = Rule(
        rule_id,
        (Condition(resource, "eq", charged), *helpers),
        ((resource, spent - charged),),
        conductance,
        roles=(LOAD_ROLE,),
        mechanism="Apparatus-catalysed relaxation to heat; actual net payment requires physical qualification",
    )
    record = model.record()
    record = {
        **record,
        "id": model.id + ".resource-load-v1",
        "rules": [*record["rules"], asdict(rule)],
    }
    return LocalModel.from_record(record)


def load_rewards(compiled, *, role=LOAD_ROLE, rule_ids=None):
    """Continuous physical flow vectors. They never enter entropy scoring."""
    compiled.require_complete()
    ids = {r.id for r in compiled.model.rules if role in r.roles}
    if rule_ids is not None:
        requested = set(rule_ids)
        if not requested or not requested <= ids:
            raise ValueError("Select nonempty existing load-rule identifiers")
        ids = requested
    if not ids:
        raise ValueError("Declared load channel is absent")
    names = (
        "forward_events",
        "reverse_events",
        "gross_heat_release",
        "gross_heat_return",
        "net_heat",
        "net_work",
    )
    rewards = {name: np.zeros(len(compiled.states)) for name in names}
    forward_deltas = []
    for i, _, event in compiled.ledger:
        if event.rule_id not in ids:
            continue
        rewards["forward_events" if event.direction == 1 else "reverse_events"][i] += (
            event.rate
        )
        rewards["gross_heat_release"][i] += event.rate * max(event.heat, 0)
        rewards["gross_heat_return"][i] += event.rate * max(-event.heat, 0)
        rewards["net_heat"][i] += event.rate * event.heat
        rewards["net_work"][i] += event.rate * event.work
        if event.direction == 1:
            forward_deltas.append(event.delta_energy)
    if not forward_deltas:
        raise ValueError("Declared load has no reachable forward event")
    return rewards, {
        "rule_ids": sorted(ids),
        "forward_energy_delta_min": min(forward_deltas),
        "forward_energy_delta_max": max(forward_deltas),
        "no_forward_energy_gain": max(forward_deltas) < 0,
        "scope": "Gross and net marked energy flows; not distinct outcome labels or a qualified-paid-load certificate",
    }
