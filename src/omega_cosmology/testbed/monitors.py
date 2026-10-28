"""Declarative, passive finite-state queries on native marked paths."""

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import expm_multiply

from .history import validate_distribution
from .physics import Condition


def conditions_hold(model, state, conditions):
    return all(Condition(**c).test(state, model.indices) for c in conditions)


def event_matches(model, source, event, selector):
    return (
        (not selector.get("rules") or event.rule_id in selector["rules"])
        and ("direction" not in selector or event.direction == selector["direction"])
        and conditions_hold(model, source, selector.get("source", ()))
        and conditions_hold(model, event.target, selector.get("target", ()))
    )


def validate_selectors(model, selectors, *, absent_rules=()):
    """An intentionally ablated channel is different from an unknown name."""
    known = {r.id for r in model.rules}
    absent = set(absent_rules)
    if absent & known:
        raise ValueError("Declared absent query rules exist in this law")
    for selector in selectors:
        rules = selector.get("rules")
        if rules is not None and (not rules or len(set(rules)) != len(rules)):
            raise ValueError(
                "Explicit rule selectors need distinct nonempty references"
            )
        if rules is not None and set(rules) - known - absent:
            raise ValueError(
                "Unknown query rule; declare intended ablations explicitly"
            )
        if selector.get("direction", 1) not in (-1, 1):
            raise ValueError("Event direction must be forward or reverse")
        for side in ("source", "target"):
            model._validate_conditions(
                tuple(Condition(**c) for c in selector.get(side, ()))
            )


def state_value(model, state, expression):
    """A numerical observable, never an added objective or physical rule."""
    if not conditions_hold(model, state, expression.get("conditions", ())):
        return 0.0
    value = float(expression.get("constant", 0))
    for coordinate, coefficient in expression.get("terms", ()):
        value += float(coefficient) * state[model.indices[coordinate]]
    if "min" in expression:
        value = max(value, float(expression["min"]))
    if "max" in expression:
        value = min(value, float(expression["max"]))
    if not np.isfinite(value):
        raise ValueError("Nonfinite observable")
    return value


def compile_monitor(compiled, spec, *, max_query_states=5000, absent_rules=()):
    """Stages advance on matching events; abort is absorbing, never restarted.

    Advancement takes priority over abort for that event. This allows an event
    consuming high stored energy to finish a stage before its target is low.
    Absent rule IDs must be explicitly declared for shared ablation queries.
    """
    compiled.require_complete()
    if spec.get("evidence_kind", "ordered_event_sequence") != "ordered_event_sequence":
        raise ValueError(
            "This monitor cannot certify causal ancestry or generative depth"
        )
    if len(compiled.model.symmetry) > 1:
        raise ValueError(
            "Marked path queries on a symmetry quotient need equivariant selectors; unsupported in this release"
        )
    stages = spec["stages"]
    if not stages:
        raise ValueError("A path witness needs at least one stage")
    validate_selectors(
        compiled.model,
        [
            selector
            for stage in stages
            for kind in ("advance", "abort")
            for selector in stage.get(kind, ())
        ],
        absent_rules=absent_rules,
    )
    n = len(compiled.states)
    phase_count = len(stages) + 2
    if n * phase_count > max_query_states:
        raise MemoryError("Passive monitor exceeds declared query-state budget")
    success, failed = len(stages), len(stages) + 1
    entries = {}
    for phase in range(phase_count):
        for i, j, event in compiled.ledger:
            next_phase = phase
            if phase < len(stages):
                stage = stages[phase]
                if any(
                    event_matches(compiled.model, compiled.states[i], event, s)
                    for s in stage["advance"]
                ):
                    next_phase += 1
                elif any(
                    event_matches(compiled.model, compiled.states[i], event, s)
                    for s in stage.get("abort", ())
                ):
                    next_phase = failed
            a, b = phase * n + i, next_phase * n + j
            entries[a, b] = entries.get((a, b), 0.0) + event.rate
            entries[a, a] = entries.get((a, a), 0.0) - event.rate
    keys = list(entries)
    q = coo_matrix(
        ([entries[k] for k in keys], ([k[0] for k in keys], [k[1] for k in keys])),
        shape=(phase_count * n, phase_count * n),
    ).tocsr()
    return {
        "q": q,
        "n": n,
        "phases": phase_count,
        "success": success,
        "failed": failed,
        "id": spec["id"],
        "stage_names": [s["name"] for s in stages],
        "evidence_kind": "ordered_event_sequence",
    }


def evaluate_monitor(monitor, initial, horizon):
    n = monitor["n"]
    initial = validate_distribution(initial, n)
    if not np.isfinite(horizon) or horizon < 0:
        raise ValueError("Nonnegative finite monitor horizon required")
    augmented = np.zeros(n * monitor["phases"])
    augmented[:n] = initial
    p = expm_multiply(monitor["q"].T * horizon, augmented).reshape(monitor["phases"], n)
    if not np.all(np.isfinite(p)) or p.min() < -1e-11 or abs(p.sum() - 1) > 1e-9:
        raise ArithmeticError("Passive monitor propagation failed")
    return {
        "id": monitor["id"],
        "evidence_kind": monitor["evidence_kind"],
        "ancestry_status": "not_established_by_event_order",
        "completed_probability": float(p[monitor["success"]].sum()),
        "failed_probability": float(p[monitor["failed"]].sum()),
        "waiting_probabilities": dict(
            zip(monitor["stage_names"], map(float, p[: monitor["success"]].sum(axis=1)))
        ),
        "physical_marginal": p.sum(axis=0),
    }


def event_rewards(compiled, descriptors, *, absent_rules=()):
    compiled.require_complete()
    validate_selectors(
        compiled.model,
        [s for d in descriptors for s in d["selectors"]],
        absent_rules=absent_rules,
    )
    if descriptors and len(compiled.model.symmetry) > 1:
        raise ValueError(
            "Marked event readouts on a symmetry quotient require an equivariance audit"
        )
    result = {d["id"]: np.zeros(len(compiled.states)) for d in descriptors}
    if len(result) != len(descriptors):
        raise ValueError("Distinct event readout IDs required")
    for i, _, event in compiled.ledger:
        source = compiled.states[i]
        for d in descriptors:
            if any(
                event_matches(compiled.model, source, event, s) for s in d["selectors"]
            ):
                amount = state_value(
                    compiled.model, source, d.get("amount", {"constant": 1})
                )
                result[d["id"]][i] += event.rate * amount
    return result
