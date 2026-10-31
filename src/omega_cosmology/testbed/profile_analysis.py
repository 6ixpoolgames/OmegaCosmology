"""Finite full-state profile identities; no Markov approximation of projections.

All returned evaluations use float64, not verified rounding intervals. A
periodic kernel has an exact bias identity but need not have a limiting offset.
"""

from dataclasses import dataclass
from math import floor, isfinite

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

from .history import entropy, validate_distribution


def checked_kernel(p):
    p = np.asarray(p, dtype=float)
    if (
        p.ndim != 2
        or not len(p)
        or p.shape[0] != p.shape[1]
        or not np.all(np.isfinite(p))
        or p.min() < 0
        or np.max(abs(p.sum(axis=1) - 1)) > 1e-10
    ):
        raise ValueError("Finite square stochastic kernel required")
    return p


def checked_steps(n):
    if type(n) is not int or n < 0:
        raise ValueError("Nonnegative integer steps required")
    return n


@dataclass(frozen=True)
class KernelProfile:
    p: np.ndarray
    reward: np.ndarray
    rate: np.ndarray
    bias: np.ndarray
    projector: np.ndarray
    residual: float
    closed_classes: int

    def coordinates(self, mu, *, cadence=1.0):
        mu = validate_distribution(mu, len(self.p))
        if not isfinite(cadence) or cadence <= 0:
            raise ValueError("Positive finite cadence required")
        return {
            "rate_bits_per_step": float(mu @ self.rate),
            "rate_bits_per_time": float(mu @ self.rate) / cadence,
            "bias_offset_bits": float(mu @ self.bias),
            "bias_sup_norm_bits": float(np.max(abs(self.bias))),
            "poisson_projector_residual": self.residual,
            "closed_classes": self.closed_classes,
            "guarantee": "float64_equations_not_rounding_certificate",
            "offset_limit": "requires_convergence_of_mu_Pn_bias_to_zero",
        }

    def at(self, mu, n):
        checked_steps(n)
        mu = validate_distribution(mu, len(self.p))
        endpoint = mu @ np.linalg.matrix_power(self.p, n)
        remainder = float(endpoint @ self.bias)
        return {
            "steps": n,
            "ell_bits": float(n * (mu @ self.rate) + mu @ self.bias - remainder),
            "remainder_bits": remainder,
            "remainder_bound_bits": float(np.max(abs(self.bias))),
        }


def kernel_profile(p, *, structural_support=None, max_states=1500):
    """Ergodic-projector/Poisson identity, including finite reducible kernels.

    Structural support is optional for synthetic kernels whose zeros are exact.
    CTMC callers supply graph-derived sampled support rather than thresholding
    underflowed numerical probabilities. This function does not change the
    existing CTMC irreducible-asymptotics API or its rejection contracts.
    """
    p = checked_kernel(p)
    n = len(p)
    if n > max_states:
        raise MemoryError("Declared profile dense state cap exceeded")
    support = p > 0 if structural_support is None else np.asarray(structural_support)
    if support.dtype != bool or support.shape != p.shape:
        raise ValueError("Boolean full-state structural support required")
    if np.any((p > 0) & ~support) or np.any(~support.any(axis=1)):
        raise ValueError("Structural support contradicts numeric kernel")
    count, labels = connected_components(
        csr_matrix(support), directed=True, connection="strong"
    )
    classes = [np.flatnonzero(labels == k) for k in range(count)]
    closed = [
        c for c in classes if not support[np.ix_(c, labels != labels[c[0]])].any()
    ]
    stationary = np.zeros((len(closed), n))
    weights = np.zeros((n, len(closed)))
    recurrent = np.zeros(n, dtype=bool)
    for k, c in enumerate(closed):
        system = p[np.ix_(c, c)].T - np.eye(len(c))
        system[-1] = 1
        rhs = np.zeros(len(c))
        rhs[-1] = 1
        pi = np.linalg.solve(system, rhs)
        if pi.min() < -1e-10:
            raise ArithmeticError("Negative stationary mass")
        stationary[k, c] = pi
        weights[c, k] = 1
        recurrent[c] = True
    transient = np.flatnonzero(~recurrent)
    if len(transient):
        rhs = np.column_stack([p[np.ix_(transient, c)].sum(axis=1) for c in closed])
        weights[transient] = np.linalg.solve(
            np.eye(len(transient)) - p[np.ix_(transient, transient)], rhs
        )
    projector = weights @ stationary
    g = entropy(p, axis=1)
    rate = projector @ g
    bias = np.linalg.solve(np.eye(n) - p + projector, g - rate)
    residual = max(
        float(np.max(abs(p @ projector - projector))),
        float(np.max(abs(projector @ p - projector))),
        float(np.max(abs(projector @ bias))),
        float(np.max(abs((np.eye(n) - p) @ bias - (g - rate)))),
        float(np.max(abs(weights.sum(axis=1) - 1))),
    )
    if not np.isfinite(residual) or residual > 1e-8:
        raise ArithmeticError("Profile projector/Poisson equations failed")
    # Bind the decomposition to its evaluated kernel. A caller mutating the
    # original array must not silently invalidate its bias or future queries.
    p = p.copy()
    for value in (p, g, rate, bias, projector):
        value.setflags(write=False)
    return KernelProfile(p, g, rate, bias, projector, residual, len(closed))


def geometric_total(profile, mu, mean_steps):
    """E[ell_N], N on {0,1,...}, E[N]=mean_steps, independent of development."""
    if not isfinite(mean_steps) or mean_steps < 0:
        raise ValueError("Nonnegative finite mean steps required")
    mu = validate_distribution(mu, len(profile.p))
    rho = mean_steps / (mean_steps + 1)
    if rho >= 1:
        raise ValueError("Geometric stopping probability below float64 resolution")
    system = np.eye(len(profile.p)) - rho * profile.p
    rewards = np.linalg.solve(system, profile.reward)
    bias = np.linalg.solve(system, profile.bias)
    direct = float(rho * (mu @ rewards))
    remainder = float((1 - rho) * (mu @ bias))
    identity = float(mean_steps * (mu @ profile.rate) + mu @ profile.bias - remainder)
    return {
        "ell_expected_bits": direct,
        "identity_bits": identity,
        "identity_residual_bits": abs(direct - identity),
        "expected_steps": mean_steps,
        "remainder_bits": remainder,
        "ending": "independent_geometric_on_nonnegative_steps",
    }


def uniform_total(profile, mu, max_steps):
    checked_steps(max_steps)
    mu = validate_distribution(mu, len(profile.p))
    # Sum P^k without an O(max_steps) loop. Upper triangular block power.
    n = len(profile.p)
    augmented = np.zeros((2 * n, 2 * n))
    augmented[:n, :n] = profile.p
    augmented[:n, n:] = np.eye(n)
    augmented[n:, n:] = np.eye(n)
    sum_powers = np.linalg.matrix_power(augmented, max_steps + 1)[:n, n:]
    remainder = float(mu @ sum_powers @ profile.bias) / (max_steps + 1)
    value = float(max_steps / 2 * (mu @ profile.rate) + mu @ profile.bias - remainder)
    return {
        "ell_expected_bits": value,
        "remainder_bits": remainder,
        "ending": "independent_uniform_0_through_max",
        "max_steps": max_steps,
    }


def state_dependent_stop(p, mu, hazards):
    """Stop before each transition; termination is part of the stopped record.

    Distinguishes expected transition surprisal from the actual entropy of the
    variable-length record, which also counts physical stopping uncertainty.
    Neither is substituted for an independent-ending E[ell_N].
    """
    p = checked_kernel(p)
    mu = validate_distribution(mu, len(p))
    h = np.asarray(hazards, dtype=float)
    if h.shape != mu.shape or not np.all(np.isfinite(h)) or h.min() < 0 or h.max() > 1:
        raise ValueError("One valid stopping probability per state required")
    survival = 1 - h
    killed = survival[:, None] * p
    # Require eventual stopping from EVERY state; never silently solve a
    # singular system or accept a root-specific inaccessible non-stopping class.
    graph = killed > 0
    _, labels = connected_components(
        csr_matrix(graph), directed=True, connection="strong"
    )
    for label in set(labels):
        c = np.flatnonzero(labels == label)
        if np.all(h[c] == 0) and not graph[np.ix_(c, labels != label)].any():
            raise ValueError("Non-stopping closed class unsupported")
    matrix = np.eye(len(p)) - killed
    rewards = np.column_stack(
        (
            survival * entropy(p, axis=1),
            entropy(np.column_stack((h, survival)), axis=1),
            survival,
        )
    )
    values = np.linalg.solve(matrix, rewards)
    means = mu @ values
    return {
        "expected_transition_surprisal_bits": float(means[0]),
        "stopping_contribution_bits": float(means[1]),
        "stopped_record_entropy_bits": float(means[0] + means[1]),
        "expected_steps": float(means[2]),
        "independent_ending_formula_applicable": False,
    }


def contrast_tail(left, mu_left, right, mu_right, *, deadband=1e-8):
    """Conservative full-state line/remainder bound, not a unique-crossing claim."""
    if not isfinite(deadband) or deadband < 0:
        raise ValueError("Nonnegative finite deadband required")
    a, b = left.coordinates(mu_left), right.coordinates(mu_right)
    dr = a["rate_bits_per_step"] - b["rate_bits_per_step"]
    db = a["bias_offset_bits"] - b["bias_offset_bits"]
    bound = a["bias_sup_norm_bits"] + b["bias_sup_norm_bits"]
    threshold = None
    if abs(dr) > deadband:
        # Strict inequality; include numerical decision margin, but this does
        # not turn float64 into a verified error certificate.
        threshold = max(0, floor((bound + deadband - np.sign(dr) * db) / abs(dr)) + 1)
    return {
        "delta_rate_bits_per_step": dr,
        "delta_bias_offset_bits": db,
        "remainder_bound_bits": bound,
        "line_crossing_steps": -db / dr if abs(dr) > deadband else None,
        "eventual_sign_from_step": threshold,
        "eventual_sign": int(np.sign(dr)) if threshold is not None else None,
        "scope": "float64_bound_evaluation_not_rounding_certificate; no claim of unique crossing",
    }
