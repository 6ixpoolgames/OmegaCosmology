"""Passive functional profiles for organizations, collectives and niches.

The predicates identify configurations; they do not declare valuers, causal
ancestry, ecological relationships or rewards. Scope history is a separate query.
"""

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import expm_multiply

from .history import validate_distribution
from .monitors import conditions_hold


def structural_closure_mask(q, functional_mask):
    """States with no native directed path back to the functional target set."""
    mask = np.asarray(functional_mask, dtype=bool)
    if q.shape != (len(mask), len(mask)):
        raise ValueError("Generator and functional target must agree")
    reverse = q.tocsc()
    reachable = mask.copy()
    pending = list(np.flatnonzero(mask))
    while pending:
        target = pending.pop()
        for k in range(reverse.indptr[target], reverse.indptr[target + 1]):
            source = reverse.indices[k]
            if source != target and reverse.data[k] > 0 and not reachable[source]:
                reachable[source] = True
                pending.append(source)
    return ~reachable


def compile_functional_query(compiled, spec, *, max_query_states=5000):
    compiled.require_complete()
    model, n = compiled.model, len(compiled.states)
    if 4 * n > max_query_states:
        raise MemoryError("Functional return query exceeds declared state budget")
    if not spec.get("id") or not spec.get("definition"):
        raise ValueError("Name and physical functional definition required")
    coordinates = spec.get("coordinates", ())
    if not coordinates or len(set(coordinates)) != len(coordinates):
        raise ValueError("Distinct physical observation coordinates required")
    if any(c not in model.indices for c in coordinates):
        raise ValueError("Unknown functional observation coordinate")
    clauses = spec.get("functional_any_of", ())
    if not clauses or any(not clause for clause in clauses):
        raise ValueError("Explicit nonempty functional predicate clauses required")
    for clause in clauses:
        if any(c["coordinate"] not in coordinates for c in clause):
            raise ValueError(
                "Functional predicate has undeclared physical dependencies"
            )

    def functional(state):
        return any(conditions_hold(model, state, c) for c in clauses)

    mask = np.array([functional(s) for s in compiled.states], dtype=bool)
    for state in compiled.states:
        if len({functional(s) for s in model.orbit(state)}) != 1:
            raise ValueError("Function distinguishes unmarked representatives")
    # Cohort 0 starts functional and has never lost function. Cohort 1 has
    # lost it; 2 has returned at least once. Initially nonfunctional paths are
    # cohort 3 and cannot be silently credited as recovery of initial function.
    q = compiled.q.tocoo()
    entries = []
    for phase in range(4):
        for i, j, rate in zip(q.row, q.col, q.data):
            target_phase = phase
            if i != j:
                if phase == 0 and not mask[j]:
                    target_phase = 1
                elif phase == 1 and mask[j]:
                    target_phase = 2
            entries.append((phase * n + i, target_phase * n + j, rate))
    lifted = coo_matrix(
        ([x[2] for x in entries], ([x[0] for x in entries], [x[1] for x in entries])),
        shape=(4 * n, 4 * n),
    ).tocsr()
    entry_rate, exit_rate = np.zeros(n), np.zeros(n)
    for i, j, rate in zip(q.row, q.col, q.data):
        if i != j:
            if not mask[i] and mask[j]:
                entry_rate[i] += rate
            if mask[i] and not mask[j]:
                exit_rate[i] += rate
    return {
        "id": spec["id"],
        "definition": spec["definition"],
        "coordinates": list(coordinates),
        "model_hash": compiled.model_hash,
        "state_order_hash": compiled.state_order_hash,
        "generator_hash": compiled.generator_hash,
        "mask": mask,
        "closure_mask": structural_closure_mask(compiled.q, mask),
        "q": compiled.q,
        "lifted": lifted,
        "entry_rate": entry_rate,
        "exit_rate": exit_rate,
    }


def evaluate_functional_query(query, initial, horizon, endpoint, occupation):
    n = len(query["mask"])
    mu = validate_distribution(initial, n)
    endpoint = validate_distribution(endpoint, n)
    occupation = np.asarray(occupation, dtype=float)
    if (
        not np.isfinite(horizon)
        or horizon < 0
        or occupation.shape != (n,)
        or not np.all(np.isfinite(occupation))
        or occupation.min() < -1e-10
        or abs(occupation.sum() - horizon) > 1e-8 * max(1, horizon)
    ):
        raise ValueError("Finite horizon and compatible physical occupation required")
    mask = query["mask"]
    start = np.zeros((4, n))
    start[0] = mu * mask
    start[3] = mu * ~mask
    result = expm_multiply(query["lifted"].T * horizon, start.ravel()).reshape(4, n)
    marginal_residual = float(np.max(abs(result.sum(axis=0) - endpoint)))
    if result.min() < -1e-10 or marginal_residual > 1e-9:
        raise ArithmeticError("Functional query changed the physical marginal")
    absent = np.flatnonzero(~mask)
    never_functional = 0.0
    if len(absent):
        killed = query["q"][absent][:, absent]
        never_functional = float(expm_multiply(killed.T * horizon, mu[absent]).sum())
    initial_function = float(mu @ mask)
    survival = float(result[0].sum())
    returned = float(result[2].sum())
    return {
        "id": query["id"],
        "definition": query["definition"],
        "model_hash": query["model_hash"],
        "generator_hash": query["generator_hash"],
        "horizon": horizon,
        "initial_functional_probability": initial_function,
        "endpoint_functional_probability": float(endpoint @ mask),
        "integrated_functional_time": float(occupation @ mask),
        "ever_functional_probability": 1 - never_functional,
        "uninterrupted_initial_function_probability": survival,
        "initial_function_lost_probability": initial_function - survival,
        "initial_function_lost_then_returned_probability": returned,
        "returned_and_functional_at_deadline_probability": float(result[2] @ mask),
        "expected_entries": float(occupation @ query["entry_rate"]),
        "expected_exits": float(occupation @ query["exit_rate"]),
        "structural_closure_by_deadline_probability": float(
            endpoint @ query["closure_mask"]
        ),
        "structural_closure_state_count": int(query["closure_mask"].sum()),
        "closure_definition": "No native directed path to the declared functional set; closed set is forward invariant",
        "physical_marginal_residual": marginal_residual,
        "scope": "Unconditional functional profile; return is not causal reconstruction, ancestry or foreclosure",
    }
