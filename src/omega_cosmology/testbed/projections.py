"""Finite-history bounds for passive non-Markov projections of a Markov law.

Lower: sum H(Y_k | last m Y's, X_{k-m-1}); upper omits that hidden boundary state.
The known initial state supplies the shorter early prefixes. The Markov property
makes the lower valid despite dropping older observations after fixing the hidden
boundary. Word operators retain hidden state; no observed Markov assumption is made.
These are analytic bounds evaluated in float64, not interval-arithmetic certificates.
"""

from collections import deque
from math import isfinite

import numpy as np

from .history import entropy, history_profile, validate_distribution


def projected_history_profiles(
    p,
    initial,
    labels,
    requested_steps,
    *,
    memory=1,
    max_workspace_bytes=32 * 1024**2,
    max_words=100000,
):
    requested_steps = tuple(requested_steps)
    if not requested_steps or any(type(k) is not int or k < 0 for k in requested_steps):
        raise ValueError("Nonempty nonnegative integer query steps required")
    checkpoints = set(requested_steps)
    steps = max(checkpoints)
    p = np.asarray(p, dtype=float)
    n = len(p)
    mu = validate_distribution(initial, n).copy()
    if np.count_nonzero(mu) != 1:
        raise ValueError(
            "This projection adapter requires one known full-present root; mixtures need separate conditioning"
        )
    if (
        p.shape != (n, n)
        or not np.all(np.isfinite(p))
        or p.min() < 0
        or np.max(abs(p.sum(axis=1) - 1)) > 1e-10
    ):
        raise ValueError("A finite stochastic transition kernel is required")
    if (
        len(labels) != n
        or type(steps) is not int
        or steps < 0
        or type(memory) is not int
        or memory < 0
    ):
        raise ValueError(
            "Compatible labels and nonnegative integer steps/memory required"
        )
    if (
        not isfinite(max_workspace_bytes)
        or max_workspace_bytes <= 0
        or type(max_words) is not int
        or max_words < 1
    ):
        raise ValueError("Positive query workspace and word caps required")
    unique = tuple(dict.fromkeys(labels))
    count = len(unique)
    used_memory = min(memory, max(0, steps - 1))
    if steps == 0:
        return {
            0: {
                "lower_bits": 0.0,
                "upper_bits": 0.0,
                "width_bits": 0.0,
                "steps": 0,
                "memory": 0,
                "method": "empty_history",
                "guarantee": "numerical_full_model",
            }
        }
    if count == n:
        profile = history_profile(p, mu, steps)
        return {
            k: {
                "lower_bits": float(profile[k]),
                "upper_bits": float(profile[k]),
                "width_bits": 0.0,
                "method": "injective_projection_full_history",
                "steps": k,
                "memory": min(memory, max(0, k - 1)),
                "guarantee": "numerical_full_model",
            }
            for k in sorted(checkpoints)
        }
    words = count ** (used_memory + 1)
    operator_words = sum(count**i for i in range(1, used_memory + 2))
    # Operators, temporary masked columns, output, and the hidden-distribution queue.
    required_bytes = 8 * n * (operator_words + 2 * words + count + used_memory + 2)
    if words > max_words or required_bytes > max_workspace_bytes:
        raise MemoryError(
            "Projected-history word workspace exceeds cap; no automatic grain/memory change"
        )
    masks = np.array(
        [[label == value for value in unique] for label in labels], dtype=float
    )
    operators = {}
    previous = np.ones((n, 1))
    for length in range(1, used_memory + 2):
        masked = (masks[:, :, None] * previous[:, None, :]).reshape(n, -1)
        previous = p @ masked
        operators[length] = previous
    lower_rewards = {}
    for length, operator in operators.items():
        prefixes = operator.reshape(n, -1, count).sum(axis=2)
        lower_rewards[length] = entropy(operator, axis=1) - entropy(prefixes, axis=1)
    full_step_entropy = entropy(p, axis=1)
    queue = deque([mu], maxlen=used_memory + 1)
    lower = upper = full_upper = 0.0
    output = {}
    if 0 in checkpoints:
        output[0] = {
            "lower_bits": 0.0,
            "upper_bits": 0.0,
            "width_bits": 0.0,
            "steps": 0,
            "memory": 0,
            "method": "empty_history",
            "guarantee": "numerical_full_model",
        }
    for k in range(1, steps + 1):
        full_upper += float(mu @ full_step_entropy)
        history_length = min(used_memory, k - 1)
        lower += float(queue[0] @ lower_rewards[history_length + 1])
        joint = queue[0] @ operators[history_length + 1]
        prefixes = joint.reshape(-1, count).sum(axis=1)
        conditional = float(entropy(joint) - entropy(prefixes))
        if conditional < -1e-10:
            raise ArithmeticError("Negative projected conditional entropy")
        upper += max(0.0, conditional)
        if k in checkpoints:
            upper_at = min(upper, full_upper)
            if lower > upper_at + 1e-8:
                raise ArithmeticError("Projected-history bounds crossed numerically")
            output[k] = {
                "lower_bits": float(lower),
                "upper_bits": float(upper_at),
                "width_bits": float(max(0.0, upper_at - lower)),
                "steps": k,
                "memory": min(memory, max(0, k - 1)),
                "observation_values": count,
                "workspace_bound_bytes": required_bytes,
                "method": "observed_memory_with_hidden_boundary_lower_and_observed_memory_upper",
                "guarantee": "numerical_full_model",
                "limits": "Analytic entropy inequalities, float64 evaluation; not rigorous numerical intervals or physical-grain certification",
            }
        mu = mu @ p
        queue.append(mu)
    return output


def projected_history_bounds(p, initial, labels, steps, **kwargs):
    """One horizon; use projected_history_profiles to share a multi-window traversal."""
    return projected_history_profiles(p, initial, labels, [steps], **kwargs)[steps]
