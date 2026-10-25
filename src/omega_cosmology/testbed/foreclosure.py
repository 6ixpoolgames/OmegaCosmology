"""History-support foreclosure and separate finite-law suppression diagnostics.

Candidate possibility uses a structural Boolean support, never a numerical
probability cutoff. Reference weights retain the reference hidden-state law.
"""

import numpy as np

from .history import validate_distribution


def projected_foreclosure_profiles(
    p_reference,
    reference_support,
    initial_reference,
    candidate_support,
    candidate_roots,
    labels_reference,
    labels_candidate,
    requested_steps,
    *,
    max_subsets=10000,
    max_workspace_bytes=32 * 1024**2,
):
    """Reference probability of words impossible under the candidate.

    Words omit the conditioned initial observation. A candidate reachable-state
    subset is the exact memory needed for support; reference mass is a vector
    over its hidden states. Histories with equal subsets can be merged linearly.
    """
    p = np.asarray(p_reference, dtype=float)
    rs, cs = np.asarray(reference_support), np.asarray(candidate_support)
    roots = np.asarray(candidate_roots)
    nr, nc = len(p), len(cs)
    mu = validate_distribution(initial_reference, nr)
    lr, lc = tuple(labels_reference), tuple(labels_candidate)
    steps = sorted(set(requested_steps))
    if (
        not steps
        or any(type(k) is not int or k < 0 for k in steps)
        or rs.dtype != bool
        or cs.dtype != bool
        or roots.dtype != bool
        or rs.shape != (nr, nr)
        or cs.shape != (nc, nc)
        or roots.shape != (nc,)
        or len(lr) != nr
        or len(lc) != nc
        or not roots.any()
        or p.shape != rs.shape
        or not np.isfinite(p).all()
        or p.min() < 0
        or np.max(abs(p.sum(axis=1) - 1)) > 1e-10
        or np.any(p[~rs] > 0)
        or type(max_subsets) is not int
        or max_subsets < 1
        or max_workspace_bytes <= 0
    ):
        raise ValueError(
            "Compatible finite kernels, structural supports, roots and positive caps required"
        )
    base_workspace = p.nbytes + rs.nbytes + cs.nbytes + 8 * nr
    if base_workspace > max_workspace_bytes:
        raise MemoryError("Foreclosure base workspace exceeds declared cap")
    alphabet = tuple(dict.fromkeys(lr))
    candidate_alphabet = set(lc)

    def record(k, mass, method, subsets, zero=False):
        return {
            "steps": k,
            "reference_weight": float(mass),
            "structurally_certified_zero": zero,
            "quantity": "history.foreclosure_reference_weight",
            "history_convention": "Y1..Yn; initial observation conditioned out",
            "method": method,
            "candidate_subset_count": subsets,
            "support_guarantee": "exact Boolean native support; no numerical zero test",
            "weight_guarantee": "exact structural zero"
            if zero
            else "float64 reference propagation; no interval enclosure",
        }

    # Full candidate state support implies full word support on its alphabet.
    # This is a structural theorem, not a shortcut based on numerical expm.
    if cs.all() and set(alphabet) <= candidate_alphabet:
        return {k: record(k, 0, "full_candidate_word_support", 1, True) for k in steps}
    masks = {v: np.array([x == v for x in lr]) for v in alphabet}
    cmasks = {v: np.array([x == v for x in lc]) for v in alphabet}
    active = {tuple(np.flatnonzero(roots)): mu.copy()}
    lost = 0.0
    out = {0: record(0, 0, "empty_word", 1, True)} if 0 in steps else {}
    transition_cache = {}
    for k in range(1, max(steps) + 1):
        following = {}
        for subset, mass in active.items():
            predicted = mass @ p
            possible = np.any(cs[list(subset)], axis=0)
            for label in alphabet:
                key = (subset, label)
                if key not in transition_cache:
                    transition_cache[key] = tuple(
                        np.flatnonzero(possible & cmasks[label])
                    )
                target = transition_cache[key]
                weighted = predicted * masks[label]
                if not target:
                    lost += float(weighted.sum())
                else:
                    if target not in following:
                        if len(following) >= max_subsets:
                            raise MemoryError(
                                "Projected support subset cap exceeded; no truncation"
                            )
                        required = (
                            base_workspace
                            + 8 * nr * (len(active) + len(following) + 3)
                            + nc * nc
                        )
                        required += sum(
                            (len(s) + len(t)) * 32 + 128
                            for (s, _), t in transition_cache.items()
                        )
                        if required > max_workspace_bytes:
                            raise MemoryError(
                                "Projected support workspace cap exceeded before allocation"
                            )
                        following[target] = np.zeros(nr)
                    following[target] += weighted
        # Include both frontiers, dense candidate row selection and cache keys.
        workspace = base_workspace + 8 * nr * (len(active) + len(following) + 2)
        workspace += nc * nc + sum(
            (len(s) + len(t)) * 32 + 128 for (s, _), t in transition_cache.items()
        )
        if workspace > max_workspace_bytes:
            raise MemoryError("Projected support workspace cap exceeded; no truncation")
        active = following
        total = lost + sum(float(v.sum()) for v in active.values())
        if abs(total - 1) > 1e-8 or not -1e-10 <= lost <= 1 + 1e-8:
            raise ArithmeticError("Foreclosure mass propagation lost normalization")
        if k in steps:
            out[k] = record(
                k, lost, "candidate_subset_reference_hidden_vector", len(active)
            )
    return out


def suppression_profile(reference, candidate, budgets):
    """Finite common-word LP; a diagnostic, never a modification of lushness.

    Fractional likelihood-ratio tests maximize reference mass at a fixed
    candidate-mass budget. This is not an efficient long-history algorithm.
    """
    budgets = tuple(budgets)
    words = set(reference) | set(candidate)
    if (
        not words
        or any(
            not np.isfinite(v) or v < 0
            for d in (reference, candidate)
            for v in d.values()
        )
        or any(abs(sum(d.values()) - 1) > 1e-10 for d in (reference, candidate))
        or any(not np.isfinite(e) or not 0 <= e <= 1 for e in budgets)
    ):
        raise ValueError("Normalized finite laws and budgets in [0,1] required")
    free = sum(reference.get(w, 0) for w in words if candidate.get(w, 0) == 0)
    paid = sorted(
        (
            (reference.get(w, 0) / candidate[w], candidate[w], reference.get(w, 0))
            for w in words
            if candidate.get(w, 0) > 0
        ),
        reverse=True,
    )
    output = []
    for epsilon in budgets:
        remaining, value = float(epsilon), float(free)
        for _, cost, benefit in paid:
            fraction = min(1.0, remaining / cost)
            value += fraction * benefit
            remaining -= fraction * cost
            if remaining <= 0:
                break
        output.append(
            {
                "candidate_mass_budget": float(epsilon),
                "max_reference_mass": float(value),
                "quantity": "history.probability_suppression",
                "method": "finite_word_fractional_test_LP",
                "guarantee": "float64 evaluation; no numerical interval certificate",
            }
        )
    return output
