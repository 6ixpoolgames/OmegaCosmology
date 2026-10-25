"""Small exact-reference queries; every exponential allocation has a size gate."""

import numpy as np
from scipy.linalg import expm
from scipy.sparse.linalg import expm_multiply


def entropy(p, axis=None):
    p = np.asarray(p, dtype=float)
    if not np.all(np.isfinite(p)) or np.min(p, initial=0.0) < -1e-12:
        raise ArithmeticError("Negative probability outside numerical tolerance")
    values = np.maximum(p, 0.0)
    logs = np.zeros_like(values)
    np.log2(values, out=logs, where=values > 0)
    return -np.sum(values * logs, axis=axis)


def validate_distribution(mu, n):
    mu = np.asarray(mu, dtype=float)
    if (
        mu.shape != (n,)
        or not np.all(np.isfinite(mu))
        or np.min(mu) < 0
        or abs(mu.sum() - 1) > 1e-10
    ):
        raise ValueError("Normalized finite distribution of correct dimension required")
    return mu


def sampled_kernel(compiled, cadence, *, max_dense_bytes=32 * 1024**2):
    compiled.require_complete()
    n = len(compiled.states)
    if not np.isfinite(cadence) or cadence <= 0:
        raise ValueError("Positive finite cadence required")
    if n * n * 8 * 4 > max_dense_bytes:
        raise MemoryError(
            "Small exact-reference dense allocation exceeds declared workspace"
        )
    p = expm(compiled.q.toarray() * cadence)
    if (
        not np.all(np.isfinite(p))
        or p.min() < -1e-12
        or np.max(abs(p.sum(axis=1) - 1)) > 1e-10
    ):
        raise ArithmeticError("Invalid sampled transition matrix")
    p[p < 0] = 0  # Round-off only, never a physical probability cutoff.
    return p


def history_profile(p, mu, steps):
    mu = validate_distribution(mu, len(p)).copy()
    if type(steps) is not int or steps < 0:
        raise ValueError("Nonnegative integer horizon required")
    h = entropy(p, axis=1)
    result = [0.0]
    for _ in range(steps):
        result.append(result[-1] + float(mu @ h))
        mu = mu @ p
    return np.array(result)


def distributions_and_occupation(compiled, mu, horizon):
    compiled.require_complete()
    from scipy.sparse import bmat, csr_matrix, eye

    n = len(compiled.states)
    mu = validate_distribution(mu, n)
    if not np.isfinite(horizon) or horizon < 0:
        raise ValueError("Finite nonnegative horizon required")
    z = csr_matrix((n, n))
    augmented = bmat([[compiled.q.T, z], [eye(n, format="csr"), z]], format="csr")
    result = expm_multiply(augmented * horizon, np.r_[mu, np.zeros(n)])
    endpoint, occupation = result[:n], result[n:]
    if np.max(abs(endpoint.sum() - 1)) > 1e-9 or abs(
        occupation.sum() - horizon
    ) > 1e-8 * max(1.0, horizon):
        raise ArithmeticError("Occupation propagation failed normalization")
    return endpoint, occupation


def sampled_support(compiled, *, max_bytes=32 * 1024**2):
    """Exact structural support at ANY positive cadence, without a cutoff.

    A finite CTMC can make any finite directed path in a positive interval;
    its sampled support is the reflexive transitive closure of its jump graph.
    The graph, rather than underflowed expm entries, decides possibility.
    """
    compiled.require_complete()
    n = len(compiled.states)
    if n * n > max_bytes:
        raise MemoryError("Sampled support exceeds declared Boolean workspace")
    result = np.eye(n, dtype=bool)
    q = compiled.q
    for i in range(n):
        pending = [i]
        while pending:
            source = pending.pop()
            for j in q.indices[q.indptr[source] : q.indptr[source + 1]]:
                if j != source and not result[i, j]:
                    result[i, j] = True
                    pending.append(j)
    return result


def irreducible_asymptotics(compiled, cadence, mu, *, max_dense_bytes=32 * 1024**2):
    """Numerical rate/offset of a small irreducible sampled CTMC only.

    The finite profile remains the query. Reducible chains are deliberately
    rejected here instead of substituting a convenient recurrent class.
    """
    from scipy.sparse.csgraph import connected_components

    compiled.require_complete()
    if connected_components(compiled.q, directed=True, connection="strong")[0] != 1:
        raise ValueError(
            "Reducible asymptotics require class/absorption accounting; unsupported here"
        )
    p = sampled_kernel(compiled, cadence, max_dense_bytes=max_dense_bytes)
    n = len(p)
    mu = validate_distribution(mu, n)
    system = p.T - np.eye(n)
    system[-1] = 1.0
    target = np.zeros(n)
    target[-1] = 1.0
    pi = np.linalg.solve(system, target)
    validate_distribution(pi, n)
    h = entropy(p, axis=1)
    step_rate = float(pi @ h)
    bias = np.linalg.solve(np.eye(n) - p + np.ones((n, 1)) * pi, h - step_rate)
    residual = max(
        float(np.max(abs(pi @ p - pi))),
        float(np.max(abs((np.eye(n) - p) @ bias - (h - step_rate)))),
    )
    if residual > 1e-10:
        raise ArithmeticError("Stationary/Poisson equations failed residual check")
    return {
        "rate_bits_per_time": step_rate / cadence,
        "offset_bits": float(mu @ bias),
        "residual": residual,
        "scope": "finite irreducible sampled CTMC; numerical, not a persistence claim",
    }


def observed_history_law(p, mu, labels, steps, *, max_words=100000):
    """Exact finite HMM word law; observation is passive and can have memory."""
    mu = validate_distribution(mu, len(p))
    if len(labels) != len(p) or type(steps) is not int or steps < 0:
        raise ValueError("Valid labels and integer horizon required")
    words = {(): mu.copy()}
    unique = tuple(dict.fromkeys(labels))
    masks = {label: np.array([x == label for x in labels]) for label in unique}
    for _ in range(steps):
        if len(words) * len(unique) > max_words:
            raise MemoryError("Observed history query exceeds exact word budget")
        next_words = {}
        for word, hidden in words.items():
            pred = hidden @ p
            for label, mask in masks.items():
                value = pred * mask
                if value.sum() > 0:
                    next_words[word + (label,)] = value
        words = next_words
    return {word: float(hidden.sum()) for word, hidden in words.items()}


def foreclosure(reference_law, candidate_law):
    """For exact finite word laws. Numerical expm probabilities are not support proofs."""
    removed = set(reference_law) - set(candidate_law)
    return {
        "histories": tuple(sorted(removed)),
        "reference_weight": float(sum(reference_law[k] for k in removed)),
    }


def full_state_foreclosure(p_reference, p_candidate, mu_reference, mu_candidate, steps):
    """DP with structural boolean support supplied separately from numeric kernels."""
    support = np.asarray(p_candidate)
    weights = np.asarray(p_reference, dtype=float)
    ref = validate_distribution(mu_reference, len(weights))
    candidate = np.asarray(mu_candidate)
    if support.dtype != bool or candidate.dtype != bool:
        raise ValueError(
            "Supply structural Boolean supports, not numerical probabilities"
        )
    if type(steps) is not int or steps < 0:
        raise ValueError("Nonnegative integer sampled horizon required")
    if support.shape != weights.shape or candidate.shape != ref.shape:
        raise ValueError("Matched full-state alphabets required")
    if steps < 1:
        return 0.0
    # Histories omit X0: a first observed state is allowed under any candidate root.
    allowed_first = (
        np.any(support[candidate], axis=0)
        if np.any(candidate)
        else np.zeros(len(ref), bool)
    )
    active = ref @ weights
    lost = float(active[~allowed_first].sum())
    active[~allowed_first] = 0
    for _ in range(steps - 1):
        transition_mass = active[:, None] * weights
        lost += float(transition_mass[~support].sum())
        active = (transition_mass * support).sum(axis=0)
    return lost


def strong_lumpability(p, labels, tolerance=1e-12):
    labels = tuple(labels)
    unique = tuple(dict.fromkeys(labels))
    transition = np.array(
        [
            [sum(p[i, j] for j in range(len(p)) if labels[j] == v) for v in unique]
            for i in range(len(p))
        ]
    )
    residual = 0.0
    for label in unique:
        group = [i for i, x in enumerate(labels) if x == label]
        residual = max(
            residual, float(np.max(abs(transition[group] - transition[group[0]])))
        )
    return {"lumpable": residual <= tolerance, "residual": residual}


def refinement_certificate(coarse_gap_lower, added_b_upper, *, refinement):
    if added_b_upper < 0:
        raise ValueError("Conditional entropy upper bound must be nonnegative")
    margin = coarse_gap_lower - added_b_upper
    return {
        "refinement": refinement,
        "bound": float(added_b_upper),
        "margin": float(margin),
        "method": "A.6.6 conditional-entropy difference bound",
        "certified": margin > 0,
        "faithfulness": "open",
        "governing_status": "provisional",
    }


def evaluate_history(
    compiled,
    present,
    law,
    observation,
    comparison,
    quantity,
    *,
    max_words=100000,
    max_dense_bytes=32 * 1024**2,
):
    from .semantics import validate_query

    validate_query(present, law, observation, comparison, quantity)
    compiled.require_complete()
    if law.physical_model_hash != compiled.model.fingerprint():
        raise ValueError("Query law identity does not match executing physics")
    names = tuple(c.name for c in compiled.model.coordinates)
    if any(k not in names for k in observation.coordinates):
        raise ValueError("Observation references an unknown physical coordinate")
    if observation.scope == "whole_modeled_field" and set(
        observation.coordinates
    ) != set(names):
        raise ValueError("Whole modeled field cannot omit a coordinate")
    roots = []
    for state, weight in present.roots:
        compiled.model.validate(state)
        canonical = compiled.model.canonical(state)
        if canonical not in compiled.index:
            raise ValueError("Present root was not covered by this compilation")
        roots.append((compiled.index[canonical], weight))
    fields = tuple(compiled.model.indices[k] for k in observation.coordinates)
    if observation.scope == "projected_history":
        for state in compiled.states:
            if (
                len({tuple(s[k] for k in fields) for s in compiled.model.orbit(state)})
                != 1
            ):
                raise ValueError(
                    "Projection distinguishes unmarked representatives of one physical orbit"
                )
    labels = [tuple(s[k] for k in fields) for s in compiled.states]
    if (
        present.conditioning == "own_present"
        and len({labels[i] for i, _ in roots}) != 1
    ):
        raise ValueError(
            "Own-present hidden roots disagree on the observed initial present"
        )
    steps = round(comparison.horizon / comparison.cadence)
    p = sampled_kernel(compiled, comparison.cadence, max_dense_bytes=max_dense_bytes)
    mu = np.zeros(len(compiled.states))
    for i, w in roots:
        mu[i] += w
    if observation.scope == "whole_modeled_field":
        ell = float(history_profile(p, mu, steps)[-1])
        if present.conditioning in ("unobserved_root_mixture", "own_present") and steps:
            ell += float(entropy(mu @ p) - mu @ entropy(p, axis=1))
    elif present.conditioning in ("full_present", "root_conditioned_average"):
        ell = 0.0
        for i, w in roots:
            point = np.zeros(len(p))
            point[i] = 1.0
            ell += w * float(
                entropy(
                    list(
                        observed_history_law(
                            p, point, labels, steps, max_words=max_words
                        ).values()
                    )
                )
            )
    else:
        ell = float(
            entropy(
                list(
                    observed_history_law(
                        p, mu, labels, steps, max_words=max_words
                    ).values()
                )
            )
        )
    return {
        "quantity": quantity.id,
        "ell_bits": ell,
        "scope": observation.scope,
        "conditioning": present.conditioning,
        "horizon": comparison.horizon,
        "cadence": comparison.cadence,
        "guarantee": "numerical_full_model",
        "model_hash": law.physical_model_hash,
        "state_order_hash": compiled.state_order_hash,
        "generator_hash": compiled.generator_hash,
        "resolution": observation.resolution,
        "boundary_history_limit": "External bath/source histories are unresolved",
    }
