"""Exact query-side assistance ancestry for distinct binary component slots.

Ancestry belongs to the declared native marked construction channels. This is
not resource-packet provenance, necessity of the catalyst, or a biological
identity claim. No query labels enter the physical history entropy.
"""

from collections import defaultdict, deque

import numpy as np
from scipy.sparse import bmat, coo_matrix, csr_matrix
from scipy.sparse.linalg import expm_multiply

from .history import validate_distribution
from .semantics import fingerprint


def compile_ancestry_query(compiled, spec, initial, *, max_query_states=5000):
    compiled.require_complete()
    model, n = compiled.model, len(compiled.states)
    initial = validate_distribution(initial, n)
    if len(model.symmetry) > 1:
        raise ValueError(
            "Assistance ancestry currently requires physically distinct slots"
        )
    depth = spec["depth_cap"]
    if type(depth) is not int or depth < 1 or not spec.get("identity_definition"):
        raise ValueError("Positive depth cap and physical identity convention required")
    fields = spec["presence_coordinates"]
    if not fields or len(set(fields)) != len(fields):
        raise ValueError("Distinct binary presence coordinates required")
    if any(
        k not in model.indices or model.domains[model.indices[k]] != {0, 1}
        for k in fields
    ):
        raise ValueError("Ancestry adapter requires 0/1 presence coordinates")
    positions = [model.indices[k] for k in fields]
    rules = {r.id: r for r in model.rules}
    edges = {}
    for edge in spec["assistance_edges"]:
        rule_id, parent, child = edge["rule"], edge["parent"], edge["child"]
        if (
            rule_id not in rules
            or parent not in fields
            or child not in fields
            or parent == child
        ):
            raise ValueError(
                "Each assistance edge needs a native rule and distinct represented parent/child"
            )
        if rule_id in edges:
            raise ValueError(
                "Ambiguous/multiple-parent marks require an explicit physical attribution model"
            )
        rule = rules[rule_id]
        guards = {(c.coordinate, c.operator, c.value) for c in rule.guards}
        changes = dict(rule.changes)
        if (
            (parent, "eq", 1) not in guards
            or (child, "eq", 0) not in guards
            or changes.get(child) != 1
            or any(k in changes for k in fields if k != child)
        ):
            raise ValueError(
                "Assistance must preserve an explicitly present parent and construct one absent child"
            )
        edges[rule_id] = (fields.index(parent), fields.index(child))
    if not edges:
        raise ValueError("At least one declared native assistance channel is required")
    # Other births get depth zero. This can miss omitted mechanisms but cannot
    # credit them with an arbitrary ancestry. Loss sets absence, never a new seed.
    outgoing = defaultdict(list)
    for i, j, event in compiled.ledger:
        outgoing[i].append((j, event))
    starts = {}
    for i in np.flatnonzero(initial):
        labels = tuple(0 if compiled.states[i][p] else -1 for p in positions)
        starts[(int(i), labels, False)] = float(initial[i])
    if len(starts) > max_query_states:
        raise MemoryError("Initial ancestry roots exceed the query-state budget")
    index = {key: i for i, key in enumerate(starts)}
    pending = deque(starts)
    entries, rewards = defaultdict(float), defaultdict(float)
    while pending:
        key = pending.popleft()
        i, labels, ever = key
        a = index[key]
        source = compiled.states[i]
        for j, event in outgoing[i]:
            target = compiled.states[j]
            new = list(labels)
            for k, pos in enumerate(positions):
                if not target[pos]:
                    new[k] = -1
                elif not source[pos]:
                    new[k] = 0
            child_depth = 0
            if event.direction == 1 and event.rule_id in edges:
                parent, child = edges[event.rule_id]
                if labels[parent] < 0:
                    raise ArithmeticError(
                        "Assistance event has no represented live parent"
                    )
                child_depth = min(depth, labels[parent] + 1)
                new[child] = child_depth
            next_key = (j, tuple(new), ever or child_depth == depth)
            if next_key not in index:
                if len(index) >= max_query_states:
                    raise MemoryError(
                        "Assistance ancestry query exceeds declared state budget; no truncation allowed"
                    )
                index[next_key] = len(index)
                pending.append(next_key)
            b = index[next_key]
            entries[a, b] += event.rate
            entries[a, a] -= event.rate
            if child_depth:
                rewards[a, child_depth - 1] += event.rate
    size = len(index)
    keys = list(entries)
    q = coo_matrix(
        ([entries[k] for k in keys], ([k[0] for k in keys], [k[1] for k in keys])),
        shape=(size, size),
    ).tocsr()
    reward = np.zeros((size, depth))
    for (i, d), rate in rewards.items():
        reward[i, d] = rate
    mu = np.zeros(size)
    for key, weight in starts.items():
        mu[index[key]] = weight
    return {
        "id": spec["id"],
        "spec_hash": fingerprint(spec),
        "depth_cap": depth,
        "model_hash": compiled.model_hash,
        "generator_hash": compiled.generator_hash,
        "physical_states": n,
        "states": tuple(index),
        "q": q,
        "initial": mu,
        "rewards": reward,
        "identity_definition": spec["identity_definition"],
    }


def evaluate_ancestry_query(query, horizon, physical_endpoint):
    if not np.isfinite(horizon) or horizon < 0:
        raise ValueError("Nonnegative finite ancestry horizon required")
    n, depth = len(query["states"]), query["depth_cap"]
    physical_endpoint = validate_distribution(
        physical_endpoint, query["physical_states"]
    )
    lifted = bmat(
        [
            [query["q"].T, csr_matrix((n, depth))],
            [csr_matrix(query["rewards"].T), csr_matrix((depth, depth))],
        ],
        format="csr",
    )
    propagated = expm_multiply(
        lifted * horizon, np.r_[query["initial"], np.zeros(depth)]
    )
    distribution, counts = propagated[:n], propagated[n:]
    marginal = np.zeros(query["physical_states"])
    ever = live = 0.0
    for mass, (physical, labels, completed) in zip(distribution, query["states"]):
        marginal[physical] += mass
        if completed:
            ever += mass
        if max(labels) == depth:
            live += mass
    residual = float(np.max(abs(marginal - physical_endpoint)))
    if residual > 1e-9 or distribution.min() < -1e-10 or counts.min() < -1e-10:
        raise ArithmeticError("Ancestry query changed the physical marginal")
    return {
        "id": query["id"],
        "spec_hash": query["spec_hash"],
        "model_hash": query["model_hash"],
        "generator_hash": query["generator_hash"],
        "evidence_kind": "native_marked_assistance_ancestry",
        "horizon": horizon,
        "query_states": n,
        "depth_cap": depth,
        "ever_reached_depth_probability": float(ever),
        "live_descendant_at_depth_probability": float(live),
        "expected_assisted_births_by_depth": {
            str(i + 1): float(v) for i, v in enumerate(counts)
        },
        "identity_definition": query["identity_definition"],
        "physical_marginal_residual": residual,
        "scope": "Initial depth zero; last depth bin means >=cap; one count per assisted birth, not independent chain count. Unlisted births reset to zero. No resource-packet ancestry or catalytic necessity inferred",
    }
