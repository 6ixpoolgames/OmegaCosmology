"""Finite externally scheduled CTMCs, with histories retained across boundaries.

Schedules prescribe barrier changes; no random command prior or clock coordinate
is scored. All phases must have the same Hamiltonian and physical state grammar.
"""

from collections import deque

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import expm_multiply

from .backends import enumerate_model
from .history import distributions_and_occupation, entropy, validate_distribution
from .physics import LocalModel
from .query_validation import invariant_values, require_marked_identity
from .readouts import activity_coefficients
from .thermodynamics import balance


def compile_phases(models, roots, *, max_states=2000):
    """Common closed state order, including states unreachable in some phases.

    The union is used ONLY to enumerate support, never as a scored generator.
    No phase change can silently alter energy, inventory, symmetry or validity.
    """
    models = tuple(models)
    if not models:
        raise ValueError("At least one phase required")
    record = models[0].record()
    invariant = tuple(k for k in record if k not in ("id", "rules"))
    if any(any(m.record()[k] != record[k] for k in invariant) for m in models[1:]):
        raise ValueError(
            "Phase switch changes physical grammar/energy; explicit adapter required"
        )
    union = LocalModel.from_record(
        {
            **record,
            "id": "phase-support-union-not-a-scored-law",
            "material": [
                {
                    **item,
                    "exchange_by_rule": {
                        f"phase{p}." + key: amount
                        for p in range(len(models))
                        for key, amount in item["exchange_by_rule"].items()
                    },
                }
                if "exchange_by_rule" in item
                else item
                for item in record["material"]
            ],
            "rules": [
                {**row, "id": f"phase{p}." + row["id"]}
                for p, model in enumerate(models)
                for row in model.record()["rules"]
            ],
        }
    )
    support = enumerate_model(union, roots, max_states=max_states)
    support.require_complete()
    compiled = tuple(
        enumerate_model(m, support.states, max_states=max_states) for m in models
    )
    for c in compiled:
        c.require_complete()
        if c.states != support.states:
            raise ArithmeticError("Phase enumeration changed the common order")
    return compiled


def validate_native_schedule(runs, cadence, horizon):
    """No implicit truncation, changed Hamiltonian or mismatched state order."""
    if (
        not np.isfinite(cadence)
        or cadence <= 0
        or not np.isfinite(horizon)
        or horizon < 0
    ):
        raise ValueError("Positive cadence and nonnegative finite horizon required")
    if not runs or any(type(k) is not int or k <= 0 for _, k in runs):
        raise ValueError("Positive integer phase lengths required")
    if horizon > sum(k for _, k in runs) * cadence + 1e-12:
        raise ValueError("Horizon exceeds schedule")
    reference = runs[0][0]
    record = reference.model.record()
    invariant = tuple(k for k in record if k not in ("id", "rules"))
    for compiled, _ in runs:
        compiled.require_complete()
        if compiled.states != reference.states or any(
            compiled.model.record()[k] != record[k] for k in invariant
        ):
            raise ValueError(
                "Aligned state order and unchanged physical grammar required"
            )


def validate_runs(runs):
    runs = tuple(runs)
    if not runs or any(type(k) is not int or k < 1 for _, k in runs):
        raise ValueError("Positive integer phase lengths required")
    n = len(runs[0][0])
    for p, _ in runs:
        if (
            p.shape != (n, n)
            or not np.all(np.isfinite(p))
            or p.min() < 0
            or np.max(abs(p.sum(axis=1) - 1)) > 1e-10
        ):
            raise ValueError("Matched finite stochastic kernels required")
    return runs


def sampled_schedule_profiles(runs, initial, checkpoints, *, rewards=None):
    """Chain-rule history, not entropy of a composed endpoint kernel.

    Optional row-rewards per phase allow one fixed coordinate chain-rule order.
    A phase boundary is an ordinary observation, never an extra counted sample.
    """
    runs = validate_runs(runs)
    mu = validate_distribution(initial, len(runs[0][0])).copy()
    checkpoints = set(checkpoints)
    if not checkpoints or any(
        type(k) is not int or not 0 <= k <= sum(v for _, v in runs) for k in checkpoints
    ):
        raise ValueError("Query checkpoints must lie in the sampled schedule")
    h = [entropy(p, axis=1) for p, _ in runs]
    rewards = [v[:, None] for v in h] if rewards is None else rewards
    if len(rewards) != len(runs) or any(
        np.asarray(v).ndim != 2 or len(v) != len(mu) for v in rewards
    ):
        raise ValueError("Matched reward columns required for each phase")
    if len({np.asarray(v).shape[1] for v in rewards}) != 1:
        raise ValueError("Reward columns change across phases")
    total = 0.0
    accumulated = np.zeros(np.asarray(rewards[0]).shape[1])
    output, k = {}, 0

    def capture():
        output[k] = {
            "ell_bits": total,
            "endpoint": mu.copy(),
            "rewards": accumulated.copy(),
        }

    if 0 in checkpoints:
        capture()
    for phase, (p, length) in enumerate(runs):
        for _ in range(length):
            total += float(mu @ h[phase])
            accumulated += mu @ rewards[phase]
            mu = mu @ p
            k += 1
            if k in checkpoints:
                capture()
    return output


def projected_schedule_profiles(
    runs,
    initial,
    labels,
    checkpoints,
    *,
    memory=1,
    max_workspace_bytes=32 * 1024**2,
    max_words=100000,
):
    """Nonhomogeneous HMM bounds, retaining words that straddle a phase switch.

    Lower conditions on the hidden boundary preceding the observed-memory word;
    upper drops older observations. Only one known full root is supported here.
    """
    runs = validate_runs(runs)
    n = len(runs[0][0])
    mu = validate_distribution(initial, n).copy()
    total_steps = sum(k for _, k in runs)
    checkpoints = set(checkpoints)
    if (
        len(labels) != n
        or np.count_nonzero(mu) != 1
        or type(memory) is not int
        or memory < 0
        or not checkpoints
        or any(type(k) is not int or k < 0 or k > total_steps for k in checkpoints)
        or type(max_words) is not int
        or max_words < 1
        or not np.isfinite(max_workspace_bytes)
        or max_workspace_bytes <= 0
    ):
        raise ValueError(
            "Known full root, matched labels, valid memory/checkpoints/caps required"
        )
    values = tuple(dict.fromkeys(labels))
    count = len(values)
    used = min(memory, max(0, max(checkpoints) - 1))
    words = count ** (used + 1)
    # Bound one window operator plus work arrays, distribution queue and masks.
    required = 8 * n * (4 * words + count + used + 2)
    if words > max_words or required > max_workspace_bytes:
        raise MemoryError(
            "Scheduled projection exceeds word/workspace cap; no fallback"
        )
    masks = np.array([[v == w for w in values] for v in labels], dtype=float)
    queue = deque([mu], maxlen=used + 1)
    window = deque(maxlen=used + 1)
    # Only the last window is cached: avoids retained exponential word growth
    # with number of phases. Homogeneous interior steps reuse their operator.
    last_key, operator, lower_reward = None, None, None
    lower = upper = full = 0.0
    output, step = {}, 0
    if 0 in checkpoints:
        output[0] = {"lower_bits": 0.0, "upper_bits": 0.0, "width_bits": 0.0}
    for phase, (p, length) in enumerate(runs):
        full_reward = entropy(p, axis=1)
        for _ in range(length):
            step += 1
            window.append(phase)
            key = tuple(window)
            if key != last_key:
                operator = np.ones((n, 1))
                for index in reversed(key):
                    masked = (masks[:, :, None] * operator[:, None, :]).reshape(n, -1)
                    operator = runs[index][0] @ masked
                prefix = operator.reshape(n, -1, count).sum(axis=2)
                lower_reward = entropy(operator, axis=1) - entropy(prefix, axis=1)
                last_key = key
            lower += float(queue[0] @ lower_reward)
            joint = queue[0] @ operator
            conditional = float(
                entropy(joint) - entropy(joint.reshape(-1, count).sum(axis=1))
            )
            if conditional < -1e-10:
                raise ArithmeticError("Negative scheduled projected entropy")
            upper += max(0.0, conditional)
            full += float(mu @ full_reward)
            if step in checkpoints:
                hi = min(upper, full)
                if lower > hi + 1e-8:
                    raise ArithmeticError("Scheduled projected bounds crossed")
                output[step] = {
                    "lower_bits": lower,
                    "upper_bits": hi,
                    "width_bits": max(0.0, hi - lower),
                    "memory": used,
                    "workspace_bound_bytes": required,
                    "method": "scheduled_hidden_boundary_lower_observed_memory_upper",
                    "conditioning": "full_present",
                    "limits": "Analytic inequalities evaluated in float64; not numerical intervals or physical-resolution certification",
                }
            mu = mu @ p
            queue.append(mu)
    return output


def continuous_schedule(runs, initial, cadence, horizon):
    """Occupation, energy and event ledgers through an aligned scheduled window."""
    validate_native_schedule(runs, cadence, horizon)
    mu = validate_distribution(initial, len(runs[0][0].states)).copy()
    first = mu.copy()
    occupation = np.zeros_like(mu)
    totals = {
        k: 0.0
        for k in (
            "work_net",
            "work_accepted_gross",
            "work_returned_gross",
            "heat_export",
            "expected_jumps",
            "finite_coefficient_bits",
            "entropy_production",
        )
    }
    channels, channel_physical, segments, remaining = {}, {}, [], horizon
    reference = runs[0][0]
    reference.require_complete()
    for compiled, steps in runs:
        compiled.require_complete()
        if compiled.states != reference.states:
            raise ValueError("Aligned state order required")
        duration = min(remaining, steps * cadence)
        if duration <= 1e-14:
            break
        endpoint, occ = distributions_and_occupation(compiled, mu, duration)
        # Krylov propagation may produce round-off negative entries only.
        if endpoint.min() < -1e-11 or occ.min() < -1e-11:
            raise ArithmeticError("Negative scheduled probability/occupation")
        endpoint = np.maximum(endpoint, 0)
        ledger = balance(compiled, mu, endpoint, occ)
        activity = activity_coefficients(compiled, occ)
        gross_in = gross_out = 0.0
        for i, _, event in compiled.ledger:
            gross_in += occ[i] * event.rate * max(event.work, 0)
            gross_out += occ[i] * event.rate * max(-event.work, 0)
            key = event.rule_id + (".forward" if event.direction == 1 else ".reverse")
            amounts = channel_physical.setdefault(
                key, {"work": 0.0, "heat": 0.0, "delta_energy": 0.0}
            )
            for name, value in (
                ("work", event.work),
                ("heat", event.heat),
                ("delta_energy", event.delta_energy),
            ):
                amounts[name] += float(occ[i] * event.rate * value)
        for k in ("work_net", "heat_export", "entropy_production"):
            totals[k] += ledger[k]
        totals["work_accepted_gross"] += gross_in
        totals["work_returned_gross"] += gross_out
        totals["expected_jumps"] += activity["expected_jumps"]
        totals["finite_coefficient_bits"] += activity["finite_coefficient_bits"]
        for name, value in ledger["integrated_channels"].items():
            channels[name] = channels.get(name, 0.0) + value
        occupation += occ
        segments.append(
            {
                "model_hash": compiled.model_hash,
                "duration": duration,
                "energy_residual": ledger["energy_residual"],
                "entropy_production": ledger["entropy_production"],
            }
        )
        mu = endpoint
        remaining -= duration
    energies = np.array([float(reference.model.energy(s)) for s in reference.states])
    totals["delta_energy"] = float((mu - first) @ energies)
    totals["energy_residual"] = (
        totals["delta_energy"] - totals["work_net"] + totals["heat_export"]
    )
    if (
        abs(totals["energy_residual"]) > 1e-8
        or abs(
            totals["work_net"]
            - totals["work_accepted_gross"]
            + totals["work_returned_gross"]
        )
        > 1e-8
    ):
        raise ArithmeticError("Scheduled energy/work ledger failed")
    return {
        "endpoint": mu,
        "occupation": occupation,
        "physical": totals,
        "channels": channels,
        "channel_physical": channel_physical,
        "segments": segments,
    }


def event_then_return(
    runs,
    initial,
    cadence,
    horizon,
    event_prefix,
    functional,
    *,
    max_query_states=5000,
    event_rules=None,
):
    """Passive native-event monitor: no event / event / later functional return.

    Never added to physical history. Its marginal must agree with native paths.
    """
    validate_native_schedule(runs, cadence, horizon)
    for compiled, _ in runs:
        if event_rules is None or event_rules:
            require_marked_identity(compiled)
        invariant_values(compiled, functional, description="return predicate")
    if event_rules is not None:
        event_rules = frozenset(event_rules)
        known = {r.id for c, _ in runs for r in c.model.rules}
        if not event_rules <= known:
            raise ValueError("Operation selector references unknown rules")
    elif not event_prefix:
        raise ValueError("Explicit operation rules or a legacy event prefix required")
    n = len(runs[0][0].states)
    if 3 * n > max_query_states:
        raise MemoryError("Scheduled event monitor exceeds query-state cap")
    mu = validate_distribution(initial, n)
    monitored = np.r_[mu, np.zeros(2 * n)]
    remaining = horizon
    for compiled, steps in runs:
        duration = min(remaining, steps * cadence)
        if duration <= 1e-14:
            break
        entries = []
        for stage in range(3):
            for i, j, event in compiled.ledger:
                next_stage = stage
                if (
                    stage == 0
                    and event.direction == 1
                    and (
                        event.rule_id in event_rules
                        if event_rules is not None
                        else event.rule_id.startswith(event_prefix)
                    )
                ):
                    next_stage = 1
                elif stage == 1 and functional(compiled.states[j]):
                    next_stage = 2
                entries.extend(
                    (
                        (stage * n + i, next_stage * n + j, event.rate),
                        (stage * n + i, stage * n + i, -event.rate),
                    )
                )
        q = coo_matrix(
            (
                [x[2] for x in entries],
                ([x[0] for x in entries], [x[1] for x in entries]),
            ),
            shape=(3 * n, 3 * n),
        ).tocsr()
        monitored = expm_multiply(q.T * duration, monitored)
        remaining -= duration
    parts = monitored.reshape(3, n)
    if monitored.min() < -1e-11 or abs(monitored.sum() - 1) > 1e-9:
        raise ArithmeticError("Scheduled event monitor normalization failed")
    return {
        "any_forward_operation_probability": float(parts[1:].sum()),
        "no_forward_operation_probability": float(parts[0].sum()),
        "operation_then_functional_return_probability": float(parts[2].sum()),
        "physical_marginal": parts.sum(axis=0),
        "scope": "Unconditional probabilities; event followed by return, not permanent restoration",
    }
