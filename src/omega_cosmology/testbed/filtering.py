"""Predictive-entropy sampling for passive histories, with explicit uncertainty.

Each sample follows an exact finite hidden-Markov filter from a known full root.
Its sum of conditional predictive entropies has the desired history entropy as
its expectation. No projected-Markov assumption or truncation of history is used.
The paired t interval is approximate, never an analytic projection bound.
"""

from math import isfinite, log, log2, sqrt

import numpy as np
from scipy.stats import t

from .history import entropy, validate_distribution


def empirical_bernstein_radius(variance, samples, score_range, alpha):
    """Two-sided Maurer-Pontil Theorem4, union bound over its two tails.

    variance is the unbiased sample variance. score_range is a proven support
    width, never the observed sample range. Exact-arithmetic iid guarantee only.
    """
    if (
        type(samples) is not int
        or samples < 2
        or not 0 < alpha < 1
        or not isfinite(variance)
        or variance < 0
        or not isfinite(score_range)
        or score_range < 0
    ):
        raise ValueError(
            "Valid variance, fixed sample count and support width required"
        )
    term = log(4 / alpha)
    return sqrt(2 * variance * term / samples) + 7 * score_range * term / (
        3 * (samples - 1)
    )


class ProjectedFilter:
    """Finite deterministic observation, padded hidden blocks, and known root."""

    def __init__(self, p, initial, labels, values, *, max_workspace_bytes):
        p = np.asarray(p, dtype=float)
        n = len(p)
        mu = validate_distribution(initial, n)
        if np.count_nonzero(mu) != 1:
            raise ValueError("Known full-present root required; no hidden-root mixture")
        if (
            p.shape != (n, n)
            or len(labels) != n
            or not np.all(np.isfinite(p))
            or p.min() < 0
            or np.max(abs(p.sum(axis=1) - 1)) > 1e-10
        ):
            raise ValueError("Finite stochastic kernel and compatible labels required")
        values = tuple(values)
        if len(set(values)) != len(values) or set(labels) != set(values):
            raise ValueError("A common, complete observation alphabet is required")
        self.values = values
        groups = [np.array([i for i, y in enumerate(labels) if y == v]) for v in values]
        self.hidden_size = max(map(len, groups))
        c, h = len(values), self.hidden_size
        required = 8 * (c * c * h * h + c * h * c + n * n)
        if required > max_workspace_bytes:
            raise MemoryError("Padded filter blocks exceed declared workspace")
        self.workspace_bytes = required
        self.blocks = np.zeros((c, c, h, h))
        for a, left in enumerate(groups):
            for b, right in enumerate(groups):
                self.blocks[a, b, : len(left), : len(right)] = p[np.ix_(left, right)]
        self.observation_probs = self.blocks.sum(axis=3).transpose(0, 2, 1)
        root = int(np.flatnonzero(mu)[0])
        self.root_observation = values.index(labels[root])
        self.root_hidden = int(np.flatnonzero(groups[self.root_observation] == root)[0])

    def start(self, count):
        obs = np.full(count, self.root_observation, dtype=int)
        belief = np.zeros((count, self.hidden_size))
        belief[:, self.root_hidden] = 1.0
        return obs, belief

    def predict(self, observations, beliefs):
        probabilities = np.einsum(
            "bi,bij->bj", beliefs, self.observation_probs[observations], optimize=False
        )
        if probabilities.min() < 0 or np.max(abs(probabilities.sum(axis=1) - 1)) > 1e-9:
            raise ArithmeticError("Filter predictive law lost normalization")
        return probabilities

    def condition(self, observations, beliefs, next_observations, probabilities):
        selected = self.blocks[observations, next_observations]
        posterior = np.einsum("bi,bij->bj", beliefs, selected, optimize=False)
        likelihood = probabilities[np.arange(len(beliefs)), next_observations]
        if np.any(likelihood <= 0):
            raise ArithmeticError("An impossible observation was selected")
        posterior /= likelihood[:, None]
        if np.max(abs(posterior.sum(axis=1) - 1)) > 1e-9:
            raise ArithmeticError("Filter posterior lost normalization")
        return posterior


def memory1_entropy_control(p, initial, labels, values, steps):
    """g_k(y)=H(Y_(k+1)|Y_k=y,X0), with its exactly propagated mean sum.

    This is a control variate, never a replacement for the full-history filter.
    Its expectation is available without sampling or assuming Y is Markov.
    """
    p = np.asarray(p, dtype=float)
    mu = validate_distribution(initial, len(p)).copy()
    masks = np.array(
        [[label == value for value in values] for label in labels], dtype=float
    )
    emission = p @ masks
    rewards = np.zeros((steps, len(values)))
    means = np.zeros(steps + 1)
    for k in range(steps):
        joint = (masks.T * mu) @ emission
        mass = joint.sum(axis=1)
        probabilities = np.divide(
            joint, mass[:, None], out=np.zeros_like(joint), where=mass[:, None] > 0
        )
        rewards[k] = entropy(probabilities, axis=1)
        means[k + 1] = means[k] + float(mass @ rewards[k])
        mu = mu @ p
    return rewards, means


def paired_projected_history_estimate(
    reference,
    candidate,
    requested_steps,
    *,
    samples,
    seed,
    batch_size=128,
    confidence=0.95,
    max_workspace_bytes=128 * 1024**2,
    max_sample_steps=20_000_000,
    control_variate="none",
    confidence_family_size=None,
):
    """Paired iid trajectories of observation filters; candidate minus reference.

    Kernel tuples are (p, one-hot initial, labels). Common independent uniforms
    couple the two filters for precision; their marginals are unchanged. Steps
    within a path are NOT treated as independent observations for standard errors.
    No optional stopping or adaptive sample-count choice is performed.
    """
    requested_steps = tuple(requested_steps)
    if not requested_steps or any(type(k) is not int or k < 0 for k in requested_steps):
        raise ValueError("Nonempty nonnegative integer query steps required")
    if confidence_family_size is None:
        confidence_family_size = len(set(requested_steps))
    if (
        type(samples) is not int
        or samples < 2
        or type(batch_size) is not int
        or batch_size < 1
        or type(seed) is not int
        or seed < 0
        or not 0 < confidence < 1
        or max_workspace_bytes <= 0
        or not isfinite(max_workspace_bytes)
        or type(max_sample_steps) is not int
        or samples * max(requested_steps) > max_sample_steps
        or control_variate not in ("none", "memory1_exact_mean")
        or type(confidence_family_size) is not int
        or confidence_family_size < len(set(requested_steps))
    ):
        raise ValueError(
            "Valid fixed sampling plan and positive resource caps required"
        )
    checkpoints = sorted(set(requested_steps))
    maximum = max(checkpoints)
    values = tuple(dict.fromkeys(reference[2]))
    c = len(values)
    sizes = [
        (len(law[0]), max(sum(y == value for y in law[2]) for value in values))
        for law in (reference, candidate)
    ]
    h = max(h for _, h in sizes)
    # Persistent blocks plus selected blocks, predictions/posteriors, and outputs.
    workspace = sum(8 * (c * c * h * h + c * h * c + n * n) for n, h in sizes) + 8 * (
        2 * batch_size * (h * h + 5 * h + 4 * c + 2)
        + samples * len(checkpoints) * 4
        + (2 * maximum * (c + 1) if control_variate != "none" else 0)
    )
    if workspace > max_workspace_bytes:
        raise MemoryError("Filter sampling plan exceeds declared workspace")
    filters = [
        ProjectedFilter(*law, values, max_workspace_bytes=max_workspace_bytes)
        for law in (reference, candidate)
    ]
    rng = np.random.default_rng(seed)
    scores = np.zeros((2, len(checkpoints), samples))
    raw_scores = np.zeros_like(scores)
    positions = {step: i for i, step in enumerate(checkpoints)}
    controls = []
    if control_variate == "memory1_exact_mean":
        controls = [
            memory1_entropy_control(*law, values, maximum)
            for law in (reference, candidate)
        ]
    for start in range(0, samples, batch_size):
        count = min(batch_size, samples - start)
        states = [f.start(count) for f in filters]
        cumulative = np.zeros((2, count))
        sampled_controls = np.zeros_like(cumulative)
        for k in range(1, maximum + 1):
            uniforms = rng.random(count)
            for a, f in enumerate(filters):
                obs, belief = states[a]
                probabilities = f.predict(obs, belief)
                cumulative[a] += entropy(probabilities, axis=1)
                if controls:
                    sampled_controls[a] += controls[a][0][k - 1, obs]
                next_obs = (uniforms[:, None] >= np.cumsum(probabilities, axis=1)).sum(
                    axis=1
                )
                # Only guard cumulative floating point drift at the final bucket.
                next_obs = np.minimum(next_obs, c - 1)
                states[a] = (
                    next_obs,
                    f.condition(obs, belief, next_obs, probabilities),
                )
            if k in positions:
                raw_scores[:, positions[k], start : start + count] = cumulative
                adjusted = cumulative - sampled_controls
                if controls:
                    adjusted = adjusted + np.array([v[1][k] for v in controls])[:, None]
                scores[:, positions[k], start : start + count] = adjusted
    output = {}
    alpha = 1 - confidence
    critical = float(t.ppf(1 - alpha / 2, samples - 1))
    for i, k in enumerate(checkpoints):
        paired = scores[1, i] - scores[0, i]
        mean = float(paired.mean())
        se = float(paired.std(ddof=1) / sqrt(samples))
        halfwidth = critical * se
        # With controls each residual is in [-B,B]; the known mean is deterministic.
        range_factor = 4 if controls else 2
        radius = range_factor * k * log2(c) * sqrt(log(2 / alpha) / (2 * samples))
        eb_radius = empirical_bernstein_radius(
            float(paired.var(ddof=1)),
            samples,
            range_factor * k * log2(c),
            alpha / confidence_family_size,
        )
        output[k] = {
            "steps": k,
            "reference_estimate_bits": float(scores[0, i].mean()),
            "candidate_estimate_bits": float(scores[1, i].mean()),
            "difference_estimate_bits": mean,
            "paired_standard_error_bits": se,
            "uncontrolled_paired_standard_error_bits": float(
                (raw_scores[1, i] - raw_scores[0, i]).std(ddof=1) / sqrt(samples)
            ),
            "control_variate": control_variate,
            "approximate_t_interval_bits": [mean - halfwidth, mean + halfwidth],
            "distribution_free_hoeffding_interval_bits": [mean - radius, mean + radius],
            "empirical_bernstein_family_interval_bits": [
                mean - eb_radius,
                mean + eb_radius,
            ],
            "empirical_bernstein_family_size": confidence_family_size,
            "bounded_paired_score_support_width_bits": range_factor * k * log2(c),
            "finite_sample_guarantee": "Maurer-Pontil2009 Theorem4, two tails and Bonferroni family; ideal iid exact arithmetic",
            "confidence": confidence,
            "coverage_scope": "pointwise per requested horizon; no simultaneous guarantee",
            "samples": samples,
            "seed": seed,
            "batch_size": batch_size,
            "workspace_bound_bytes": workspace,
            "conditioning": "known_full_present_each_arm",
            "quantity": "history.projected_given_full_present.difference",
            "method": "paired_iid_predictive_entropy_filter_sampling",
            "guarantee": "statistical_estimate_not_analytic_projection_bound",
            "limits": (
                "Paired t coverage is approximate; Hoeffding is distribution-free for "
                "ideal iid samples and exact arithmetic. Float64/PRNG evaluation is "
                "not a rigorous numerical certificate. No physical-grain certification."
            ),
        }
    return output
