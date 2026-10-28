"""Capped finite scheduled assay; fixed-law study behavior is left unchanged."""

from time import perf_counter

import numpy as np

from .ecology import structural_closure_mask
from .history import sampled_kernel, sampled_support
from .monitors import conditions_hold, state_value
from .phases import (
    compile_phases,
    continuous_schedule,
    event_then_return,
    projected_schedule_profiles,
    sampled_schedule_profiles,
)
from .physics import LocalModel
from .query_validation import invariant_values
from .readouts import coordinate_entropy_rewards
from .semantics import (
    ComparisonSpec,
    LawSpec,
    ObservationSpec,
    PresentSpec,
    QuantitySpec,
    fingerprint,
    validate_query,
)
from .thermodynamics import audit_equilibrium


def schedule_inputs(protocol):
    """Strict boundary alignment and known common-root input contract."""
    cadence = protocol["cadence"]
    if not np.isfinite(cadence) or cadence <= 0:
        raise ValueError("Positive finite cadence required")
    models = [LocalModel.from_record(p["model"]) for p in protocol["phases"]]
    lengths = []
    for phase in protocol["phases"]:
        v = phase["duration"] / cadence
        if not np.isfinite(v) or v <= 0 or abs(v - round(v)) > 1e-9:
            raise ValueError("Every phase boundary must align with cadence")
        lengths.append(round(v))
    horizons = protocol["horizons"]
    if not horizons or len(set(horizons)) != len(horizons):
        raise ValueError("Distinct nonempty horizon list required")
    for T in horizons:
        if (
            not np.isfinite(T)
            or T <= 0
            or T > sum(lengths) * cadence
            or abs(T / cadence - round(T / cadence)) > 1e-9
        ):
            raise ValueError("Horizons must align and lie within schedule")
    root = tuple(protocol["root"])
    if any(str(m.energy(root)) != protocol["energy_per_root"] for m in models):
        raise ValueError("Common root energy mismatch")
    compiled = compile_phases(models, [root], max_states=protocol["max_states"])
    mu = np.zeros(len(compiled[0].states))
    mu[compiled[0].index[compiled[0].model.canonical(root)]] = 1
    return compiled, lengths, mu


def evaluate_scheduled_case(protocol):
    started = perf_counter()
    compiled, lengths, mu = schedule_inputs(protocol)
    native_runs = list(zip(compiled, lengths))
    cadence = protocol["cadence"]
    model = compiled[0].model
    names = [c.name for c in model.coordinates]
    if names != protocol["coordinate_order"]:
        raise ValueError("Fixed coordinate chain-rule order required")
    cap = protocol["max_dense_bytes"]
    # Each phase kernel plus coordinate rewards remains live. Refuse this
    # aggregate workspace before making exponential allocations.
    n = len(mu)
    if 8 * n * n * (4 + len(compiled)) > cap:
        raise MemoryError("Scheduled kernels exceed aggregate dense workspace cap")
    kernels = [sampled_kernel(c, cadence, max_dense_bytes=cap) for c in compiled]
    kernel_runs = list(zip(kernels, lengths))
    checkpoints = [round(T / cadence) for T in protocol["horizons"]]
    boundaries = list(map(int, np.cumsum(lengths)))
    shares = [
        coordinate_entropy_rewards(p, compiled[0].states, list(range(len(names))))
        for p in kernels
    ]
    profiles = sampled_schedule_profiles(
        kernel_runs, mu, set(checkpoints + boundaries), rewards=shares
    )
    if len({p["id"] for p in protocol["projected_histories"]}) != len(
        protocol["projected_histories"]
    ):
        raise ValueError("Distinct projection IDs required")
    projections = {}
    for projection in protocol["projected_histories"]:
        fields = projection["coordinates"]
        if (
            not fields
            or len(set(fields)) != len(fields)
            or any(k not in model.indices for k in fields)
        ):
            raise ValueError("Distinct valid projection coordinates required")
        if len(model.symmetry) > 1:
            for s in compiled[0].states:
                if (
                    len(
                        {
                            tuple(t[model.indices[k]] for k in fields)
                            for t in model.orbit(s)
                        }
                    )
                    > 1
                ):
                    raise ValueError(
                        "Projection distinguishes unmarked representatives"
                    )
        labels = [
            tuple(s[model.indices[k]] for k in fields) for s in compiled[0].states
        ]
        projections[projection["id"]] = projected_schedule_profiles(
            kernel_runs,
            mu,
            labels,
            checkpoints,
            memory=projection["memory"],
            max_workspace_bytes=protocol["max_projection_bytes"],
        )
    present = PresentSpec(
        protocol["present_id"],
        ((tuple(protocol["root"]), 1.0),),
        sufficiency=protocol["sufficiency"],
    )
    law = LawSpec(
        protocol["id"],
        fingerprint([(c.model_hash, k) for c, k in native_runs]),
        protocol["boundary_scope"],
    )
    observation = ObservationSpec("whole.modeled", tuple(names))
    quantity = QuantitySpec(
        "history.full_given_present",
        "Complete sampled history under declared native phase schedule",
        "bits",
        "full_present",
    )
    eq = [audit_equilibrium(c) for c in compiled]
    operation_rules = protocol.get("operation_rules")
    if operation_rules is None:
        operation_rules = sorted(
            {
                r.id
                for c in compiled
                for r in c.model.rules
                if "operation.stroke" in r.roles
            }
        )
        if not operation_rules and any(
            r.id.startswith("operation.stroke") for c in compiled for r in c.model.rules
        ):
            raise ValueError(
                "Legacy operation protocol needs explicit operation_rules migration"
            )
    values = {
        s["id"]: np.array(
            invariant_values(
                compiled[0], lambda state, s=s: state_value(model, state, s)
            )
        )
        for s in protocol["observables"]
    }
    functional = lambda s: conditions_hold(model, s, protocol["functional_conditions"])
    mask = np.array(
        invariant_values(compiled[0], functional, description="functional predicate"),
        dtype=bool,
    )
    closure = structural_closure_mask(compiled[-1].q, mask)
    support = [sampled_support(c, max_bytes=cap) for c in compiled]
    rows = []
    for T, k in zip(protocol["horizons"], checkpoints):
        comparison = ComparisonSpec(
            protocol["id"],
            "process",
            T,
            cadence,
            protocol["matched"],
            protocol["implementation"],
            present.id,
            common_present_hash=present.content_fingerprint(),
        )
        contract = validate_query(present, law, observation, comparison, quantity)
        physical = continuous_schedule(native_runs, mu, cadence, T)
        sampled = profiles[k]
        endpoint_residual = float(
            np.max(abs(physical["endpoint"] - sampled["endpoint"]))
        )
        if (
            endpoint_residual > 1e-9
            or abs(sum(sampled["rewards"]) - sampled["ell_bits"]) > 1e-8
        ):
            raise ArithmeticError(
                "Sampled/continuous propagation or chain rule disagrees"
            )
        monitor = event_then_return(
            native_runs, mu, cadence, T, None, functional, event_rules=operation_rules
        )
        marginal_residual = float(
            np.max(abs(monitor.pop("physical_marginal") - physical["endpoint"]))
        )
        if marginal_residual > 1e-9:
            raise ArithmeticError("Passive monitor changed physical paths")
        prefix_steps = min(lengths[0], k)
        prefix_entropy = (
            profiles[prefix_steps]["ell_bits"]
            if prefix_steps in profiles
            else sampled["ell_bits"]
        )
        row = {
            "horizon": T,
            "cadence": cadence,
            "contract": contract,
            "history": {
                "ell_bits": sampled["ell_bits"],
                "operation_prefix_bits": prefix_entropy,
                "recovery_bits": sampled["ell_bits"] - prefix_entropy,
            },
            "coordinate_entropy_shares": dict(zip(names, sampled["rewards"].tolist()))
            if len(model.symmetry) == 1
            else None,
            "coordinate_share_status": "declared_order"
            if len(model.symmetry) == 1
            else "unsupported_unmarked_coordinate_attribution",
            "physical": physical["physical"],
            "channels": physical["channels"],
            "channel_physical": physical["channel_physical"],
            "segments": physical["segments"],
            "operation_monitor": monitor,
            "observables": {
                name: {
                    "endpoint": float(physical["endpoint"] @ v),
                    "integrated": float(physical["occupation"] @ v),
                }
                for name, v in values.items()
            },
            "projected_histories": {name: p[k] for name, p in projections.items()},
            "support": {
                "closure_probability_under_common_recovery": float(
                    physical["endpoint"] @ closure
                ),
                "all_phase_sampled_kernels_full_support": bool(
                    all(np.all(v) for v in support)
                ),
                "scope": "Exact graph support at positive cadence, not low-probability cutoff or weighted access",
            },
            "validation": {
                "continuous_sampled_endpoint_residual": endpoint_residual,
                "event_monitor_marginal_residual": marginal_residual,
            },
        }
        rows.append(row)
    return {
        "schema": "omega.scheduled-study-result/1",
        "status": "passed",
        "id": protocol["id"],
        "states": n,
        "state_order_hash": compiled[0].state_order_hash,
        "phase_model_hashes": [c.model_hash for c in compiled],
        "phase_ledger_hashes": [c.ledger_hash for c in compiled],
        "material_conservation": [c.model.material_status for c in compiled],
        "equilibrium_audits": eq,
        "present": present.record(),
        "law": law.record(),
        "observation": observation.record(),
        "quantity": quantity.record(),
        "rows": rows,
        "wall_seconds": perf_counter() - started,
        "scope": "Finite externally scheduled classical whole modeled field. Thermal/external apparatus histories unresolved. No stationary rate assigned to finite pulse, no ethical verdict.",
    }
