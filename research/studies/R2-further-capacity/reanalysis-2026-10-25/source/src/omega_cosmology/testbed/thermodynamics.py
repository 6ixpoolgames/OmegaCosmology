"""Degeneracy-aware one-bath stocks and channel-resolved reward accounting."""

import numpy as np
from scipy.special import logsumexp


def equilibrium(compiled):
    compiled.require_complete()
    model = compiled.model
    energies = np.array([float(model.energy(s)) for s in compiled.states])
    log_g = np.array([model.quotient_log_degeneracy(s) for s in compiled.states])
    logs = log_g - model.beta * energies
    pi = np.exp(logs - logsumexp(logs))
    return pi, energies, log_g


def source_off_matrix(compiled):
    q = compiled.q.copy().tolil()
    for i, j, e in compiled.ledger:
        if e.boundary != "native":
            q[i, j] -= e.rate
            q[i, i] += e.rate
    return q.tocsr()


def require_single_reference_sector(compiled):
    from scipy.sparse.csgraph import connected_components

    q = source_off_matrix(compiled)
    n, _ = connected_components(q, directed=True, connection="strong")
    if n != 1:
        raise ValueError(
            "Multiple source-off sectors require explicit sector weights; reference availability unsupported"
        )
    return q


def free_energy(p, energies, log_g, beta):
    p = np.asarray(p, dtype=float)
    if not np.all(np.isfinite(p)) or p.min() < -1e-11 or abs(p.sum() - 1) > 1e-9:
        raise ArithmeticError("Invalid distribution for thermodynamics")
    p = np.maximum(p, 0.0)
    positive = p > 0
    entropy = float(-np.sum(p[positive] * (np.log(p[positive]) - log_g[positive])))
    return float(p @ energies) - entropy / beta, entropy


def flow_rewards(compiled):
    n = len(compiled.states)
    work, heat, jumps = np.zeros(n), np.zeros(n), np.zeros(n)
    channels = {}
    for i, _, e in compiled.ledger:
        work[i] += e.rate * e.work
        heat[i] += e.rate * e.heat
        jumps[i] += e.rate
        key = e.rule_id + (".forward" if e.direction == 1 else ".reverse")
        channels.setdefault(key, np.zeros(n))[i] += e.rate
    return work, heat, jumps, channels


def audit_equilibrium(compiled):
    compiled.require_complete()
    pi, _, _ = equilibrium(compiled)
    # Same states, remove registered source channels only; do not rebuild roots.
    q = require_single_reference_sector(compiled)
    flux = q.multiply(pi[:, None])
    difference = flux - flux.T
    residual = float(max(abs(difference.data), default=0.0))
    stationary = float(max(abs(q.T @ pi), default=0.0))
    if max(residual, stationary) > 1e-10:
        raise ArithmeticError("Source-off equilibrium/detailed balance failed")
    return {
        "status": "passed",
        "edge_flux_residual": residual,
        "stationary_residual": stationary,
        "reference_scope": "Gibbs on the enumerated conserved/reachable sector; sector weights fixed",
    }


def balance(compiled, initial, endpoint, occupation):
    require_single_reference_sector(compiled)
    model = compiled.model
    pi, energies, log_g = equilibrium(compiled)
    f0, s0 = free_energy(initial, energies, log_g, model.beta)
    ft, st = free_energy(endpoint, energies, log_g, model.beta)
    feq, _ = free_energy(pi, energies, log_g, model.beta)
    wr, qr, nr, channels = flow_rewards(compiled)
    work, heat = float(occupation @ wr), float(occupation @ qr)
    delta_e = float((endpoint - initial) @ energies)
    sigma = st - s0 + model.beta * heat
    residual = delta_e - work + heat
    if abs(residual) > 1e-8 * max(1.0, abs(work) + abs(heat)) or sigma < -1e-8:
        raise ArithmeticError("First/second-law audit failed")
    positive = endpoint > 0
    kl = (
        float(
            np.sum(
                endpoint[positive] * (np.log(endpoint[positive]) - np.log(pi[positive]))
            )
        )
        / model.beta
    )
    return {
        "work_net": work,
        "heat_export": heat,
        "delta_energy": delta_e,
        "energy_residual": residual,
        "entropy_production": sigma,
        "free_energy_excess_initial": f0 - feq,
        "free_energy_excess_final": ft - feq,
        "kl_availability": kl,
        "availability_identity_residual": abs(kl - (ft - feq)),
        "expected_jumps": float(occupation @ nr),
        "integrated_channels": {k: float(occupation @ v) for k, v in channels.items()},
        "scope": "One declared bath; boundary histories unresolved; availability is a benchmark, not guaranteed extractable work",
    }
