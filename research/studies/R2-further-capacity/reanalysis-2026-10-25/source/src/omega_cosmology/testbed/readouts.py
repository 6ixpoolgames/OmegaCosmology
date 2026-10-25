"""Passive path readouts; none changes the law or contributes extra entropy."""

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import expm_multiply

from .history import entropy, validate_distribution


def coordinate_entropy_rewards(p, states, order):
    """H(next coordinates | full past state), in one declared chain-rule order."""
    states = tuple(states)
    if sorted(order) != list(range(len(states[0]))) or len(states) != len(p):
        raise ValueError(
            "Supply every coordinate exactly once and a matched state order"
        )
    result = np.zeros((len(p), len(order)))
    previous = np.zeros(len(p))
    for column in range(len(order)):
        labels = [tuple(s[k] for k in order[: column + 1]) for s in states]
        blocks = tuple(dict.fromkeys(labels))
        grouped = np.array(
            [
                p[:, np.array([v == label for v in labels])].sum(axis=1)
                for label in blocks
            ]
        ).T
        current = entropy(grouped, axis=1)
        result[:, column] = current - previous
        previous = current
    if np.max(abs(result.sum(axis=1) - entropy(p, axis=1))) > 1e-10:
        raise ArithmeticError("Coordinate chain rule failed")
    return result


def cumulative_sampled_rewards(p, mu, rewards, steps):
    """Expected sum over sampled pre-step states; initial uncertainty is excluded."""
    mu = validate_distribution(mu, len(p)).copy()
    rewards = np.asarray(rewards, dtype=float)
    if (
        rewards.ndim != 2
        or rewards.shape[0] != len(p)
        or type(steps) is not int
        or steps < 0
    ):
        raise ValueError(
            "Matched reward columns and a nonnegative integer horizon required"
        )
    result = np.zeros((steps + 1, rewards.shape[1]))
    for i in range(steps):
        result[i + 1] = result[i] + mu @ rewards
        mu = mu @ p
    return result


def activity_coefficients(compiled, occupation, reference_time=1.0):
    """Unmarked-state CTMC fine-cadence coordinates Nbar,F (not a new score).

    Parallel mechanisms with the same represented outcome are aggregated in Q.
    ell(dt) ~ Nbar log2(reference_time/dt) + F as dt approaches zero.
    """
    compiled.require_complete()
    if not np.isfinite(reference_time) or reference_time <= 0:
        raise ValueError(
            "Positive reference time required for dimensionless logarithms"
        )
    q = compiled.q
    exits = -q.diagonal()
    finite_reward = exits * np.log2(np.e)
    for i in range(q.shape[0]):
        for k in range(q.indptr[i], q.indptr[i + 1]):
            j, rate = q.indices[k], q.data[k]
            if i != j and rate > 0:
                finite_reward[i] -= rate * np.log2(rate * reference_time)
    return {
        "expected_jumps": float(occupation @ exits),
        "finite_coefficient_bits": float(occupation @ finite_reward),
        "reference_time": reference_time,
        "scope": "Asymptotic fine-cadence diagnostic, not an exact finite-cadence decomposition",
    }


def two_event_monitor(compiled, initial, horizon, first, second):
    """Probability of an ordered two-event witness on the SAME physical paths.

    The three monitor phases exist only in the query calculation. They are
    marginalized for a propagation check and never supplied to history entropy.
    Selectors are (rule_id, direction); no reset/restart is performed.
    """
    compiled.require_complete()
    n = len(compiled.states)
    initial = validate_distribution(initial, n)
    entries = {}

    def add(i, j, rate):
        entries[i, j] = entries.get((i, j), 0.0) + rate

    for phase in range(3):
        for i, j, event in compiled.ledger:
            mark = (event.rule_id, event.direction)
            next_phase = 1 if phase == 0 and mark == tuple(first) else phase
            if phase == 1 and mark == tuple(second):
                next_phase = 2
            add(phase * n + i, next_phase * n + j, event.rate)
            add(phase * n + i, phase * n + i, -event.rate)
    keys = list(entries)
    q = coo_matrix(
        ([entries[k] for k in keys], ([k[0] for k in keys], [k[1] for k in keys])),
        shape=(3 * n, 3 * n),
    ).tocsr()
    propagated = expm_multiply(q.T * horizon, np.r_[initial, np.zeros(2 * n)]).reshape(
        3, n
    )
    if (
        not np.all(np.isfinite(propagated))
        or propagated.min() < -1e-11
        or abs(propagated.sum() - 1) > 1e-9
    ):
        raise ArithmeticError("Passive monitor propagation failed")
    return {
        "completed_probability": float(propagated[2].sum()),
        "first_without_second_probability": float(propagated[1].sum()),
        "physical_marginal": propagated.sum(axis=0),
    }
