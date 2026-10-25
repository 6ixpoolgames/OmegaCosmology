"""Exact reachable enumeration and event sampling share LocalModel.events."""

import math
from collections import defaultdict
from dataclasses import dataclass
from hashlib import sha256
from time import perf_counter

import numpy as np
from scipy.sparse import coo_matrix

from .semantics import fingerprint


@dataclass
class Compilation:
    model: object
    states: tuple
    index: dict
    q: object
    ledger: tuple
    frontier: tuple
    complete: bool
    seconds: float

    def __post_init__(self):
        self.model_hash = self.model.fingerprint()
        self.state_order_hash = fingerprint(self.states)
        self.generator_hash = self._generator_hash()

    def _generator_hash(self):
        if self.q is None:
            return None
        value = sha256()
        value.update(self.model_hash.encode())
        value.update(self.state_order_hash.encode())
        for array in (self.q.indptr, self.q.indices, self.q.data):
            value.update(str(array.dtype).encode())
            value.update(array.tobytes())
        return value.hexdigest()

    def require_complete(self):
        if not self.complete:
            raise ValueError(
                "Incomplete native enumeration cannot supply a scored generator"
            )
        if (
            self.model.fingerprint() != self.model_hash
            or fingerprint(self.states) != self.state_order_hash
            or self._generator_hash() != self.generator_hash
            or self.index != {s: i for i, s in enumerate(self.states)}
        ):
            raise ValueError(
                "Compiled law/state order changed; recompile before querying"
            )


def physical_events(model, state, include_drive=True):
    model.audit_symmetry(state)
    events = []
    for event in model.events(state, include_drive=include_drive):
        if model.canonical(event.target) == state:
            if event.work or event.heat:
                raise ValueError(
                    "Hidden dissipative self-event needs an explicit adapter"
                )
            continue
        events.append(event)
    return events


def enumerate_model(model, roots, *, max_states=2000, include_drive=True):
    started = perf_counter()
    if type(max_states) is not int or max_states < 1:
        raise ValueError("Positive state cap required")
    states, index = [], {}
    for root in roots:
        root = tuple(root)
        model.validate(root)
        s = model.canonical(root)
        if s not in index:
            index[s] = len(states)
            states.append(s)
    if not states:
        raise ValueError("At least one physical root is required")
    if len(states) > max_states:
        return Compilation(
            model,
            tuple(states),
            index,
            None,
            (),
            tuple(states[max_states:]),
            False,
            perf_counter() - started,
        )
    entries, ledger = defaultdict(float), []
    cursor = 0
    while cursor < len(states):
        state = states[cursor]
        for event in physical_events(model, state, include_drive):
            target = model.canonical(event.target)
            if target == state:
                if event.work or event.heat:
                    raise ValueError(
                        "Hidden dissipative self-event requires an explicit physical/accounting adapter"
                    )
                continue  # Pure unmarked permutation, no physical history distinction.
            if target not in index:
                if len(states) >= max_states:
                    return Compilation(
                        model,
                        tuple(states),
                        index,
                        None,
                        (),
                        (target,),
                        False,
                        perf_counter() - started,
                    )
                index[target] = len(states)
                states.append(target)
            j = index[target]
            entries[cursor, j] += event.rate
            ledger.append((cursor, j, event))
        cursor += 1
    n = len(states)
    exits = np.zeros(n)
    for (i, _), v in entries.items():
        exits[i] += v
    for i, value in enumerate(exits):
        entries[i, i] = -value
    keys = tuple(entries)
    q = coo_matrix(
        ([entries[k] for k in keys], ([k[0] for k in keys], [k[1] for k in keys])),
        shape=(n, n),
    ).tocsr()
    if not np.all(np.isfinite(q.data)):
        raise ArithmeticError(
            "Aggregated native generator overflowed; no rate clipping permitted"
        )
    return Compilation(
        model,
        tuple(states),
        index,
        q,
        tuple(ledger),
        (),
        True,
        perf_counter() - started,
    )


def trajectory(model, root, horizon, rng, *, max_events=100000, include_drive=True):
    if not math.isfinite(horizon) or horizon < 0:
        raise ValueError("Nonnegative finite horizon required")
    state, t = model.canonical(tuple(root)), 0.0
    model.validate(state)
    times, states, marks = [0.0], [state], []
    work = heat = 0.0
    while t < horizon:
        events = physical_events(model, state, include_drive)
        total = sum(e.rate for e in events)
        if not total:
            break
        t += float(rng.exponential(1 / total))
        if t > horizon:
            break
        if len(marks) >= max_events:
            return {
                "complete": False,
                "reason": "event_cap",
                "times": times,
                "states": states,
                "marks": marks,
            }
        event = events[
            int(rng.choice(len(events), p=np.array([e.rate for e in events]) / total))
        ]
        state = model.canonical(event.target)
        times.append(t)
        states.append(state)
        marks.append((event.rule_id, event.direction))
        work += event.work
        heat += event.heat
    return {
        "complete": True,
        "times": times,
        "states": states,
        "marks": marks,
        "endpoint": state,
        "work": work,
        "heat": heat,
        "jumps": len(marks),
    }
