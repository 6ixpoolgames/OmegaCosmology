"""Native-law opportunity audits; legal state probes are not interventions."""

from math import isfinite

from .monitors import conditions_hold, event_matches


def validate_selector(model, selector):
    if not selector.get("rules"):
        raise ValueError("Audit selectors must list their physical rules explicitly")
    missing = set(selector["rules"]) - {r.id for r in model.rules}
    if missing:
        raise ValueError(f"Unknown audit rules: {sorted(missing)}")
    if selector.get("direction") not in (-1, 1):
        raise ValueError("Audit direction must be explicit")
    for side in ("source", "target"):
        for c in selector.get(side, ()):
            if c["coordinate"] not in model.indices:
                raise ValueError("Unknown audit coordinate")


def selected_rate(model, state, selector):
    return sum(
        e.rate for e in model.events(state) if event_matches(model, state, e, selector)
    )


def transition_audit(compiled, spec):
    """Report where a specified event route is absent, including capacity locks.

    Structural counts are not occupation probabilities. Missing alternatives
    outside the selected routes must not be inferred from their absence here.
    """
    compiled.require_complete()
    model = compiled.model
    validate_selector(model, spec["selector"])
    if len(model.symmetry) > 1:
        raise ValueError("Marked structural audits require an equivariance audit")
    rows = []
    for state in compiled.states:
        if conditions_hold(model, state, spec.get("when", ())):
            rows.append((state, selected_rate(model, state, spec["selector"])))
    blocked = [s for s, rate in rows if rate == 0]
    return {
        "id": spec["id"],
        "model_hash": compiled.model_hash,
        "state_order_hash": compiled.state_order_hash,
        "eligible_states": len(rows),
        "route_absent_states": len(blocked),
        "minimum_rate": min((r for _, r in rows), default=None),
        "maximum_rate": max((r for _, r in rows), default=None),
        "absent_examples": [list(s) for s in blocked[:5]],
        "scope": "Selected native routes on enumerated states; no physical necessity claim",
    }


def paired_state_probe(compiled, spec):
    """Compare native event rates at legal states differing only in declared fields.

    Unreachable/invalid counterparts are counted as unmatched, never zero-rate.
    This does not perform a physical removal, preserve energy by fiat, or
    establish path ancestry. Resource/energy differences remain explicit.
    """
    compiled.require_complete()
    model = compiled.model
    if len(model.symmetry) > 1:
        raise ValueError("Paired state probes require a verified labelled reference")
    validate_selector(model, spec["selector"])
    substitutions = spec["replace"]
    if not substitutions or any(k not in model.indices for k in substitutions):
        raise ValueError("A probe needs named state replacements")
    tolerance = spec.get("rate_tolerance", 1e-12)
    if not isfinite(tolerance) or tolerance < 0:
        raise ValueError("Invalid rate tolerance")
    counts = {
        key: 0
        for key in (
            "eligible",
            "paired",
            "invalid_counterpart",
            "outside_enumeration",
            "enabled_only_in_original",
            "disabled_in_original",
            "faster_in_original",
            "slower_in_original",
            "equal",
        )
    }
    pairs = []
    for state in compiled.states:
        if not conditions_hold(model, state, spec.get("when", ())):
            continue
        counts["eligible"] += 1
        other = list(state)
        for field, value in substitutions.items():
            other[model.indices[field]] = value
        other = tuple(other)
        if other == state:
            raise ValueError("Probe replacement must change each eligible state")
        if not model.valid(other):
            counts["invalid_counterpart"] += 1
            continue
        if other not in compiled.index:
            counts["outside_enumeration"] += 1
            continue
        counts["paired"] += 1
        a, b = [selected_rate(model, s, spec["selector"]) for s in (state, other)]
        if a > 0 and b == 0:
            counts["enabled_only_in_original"] += 1
        if a == 0 and b > 0:
            counts["disabled_in_original"] += 1
        key = (
            "faster_in_original"
            if a - b > tolerance
            else ("slower_in_original" if b - a > tolerance else "equal")
        )
        counts[key] += 1
        pairs.append(
            {
                "original": list(state),
                "counterpart": list(other),
                "original_rate": a,
                "counterpart_rate": b,
                "delta_energy": float(model.energy(state) - model.energy(other)),
            }
        )
    return {
        "id": spec["id"],
        "model_hash": compiled.model_hash,
        "state_order_hash": compiled.state_order_hash,
        "counts": counts,
        "examples": pairs[:5],
        "scope": "Legal-state local rate comparison, not a paid intervention or ancestry proof",
    }
