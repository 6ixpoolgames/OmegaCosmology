"""P001: exact finite response geometry, with records and policy indices intact.

This is a diagonal classical subcase, not a general quantum simulator.
All state updates are specified reversible controlled-X gates. See MODEL_SPEC.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path

ROLE_ORDER = ("source", "mode", "actuator", "r0", "r1", "r2")
POLICIES = tuple(product((0, 1), repeat=6))
# p[0:2] specifies b1(r); p[2:6] specifies b2(r,a1), in lexicographic order.


def total_variation(p, q):
    return sum((abs(p.get(k, 0) - q.get(k, 0)) for k in p.keys() | q.keys()),
               Fraction(0)) / 2


def packing_size(matrix, epsilon):
    """Maximum size with strict pairwise d > epsilon; exhaustive, small n only."""
    n = len(matrix)
    for size in range(n, 0, -1):
        for subset in combinations(range(n), size):
            if all(matrix[i][j] > epsilon for i, j in combinations(subset, 2)):
                return size, list(subset)
    return 0, []


class Model:
    def __init__(self, fixture):
        self.fixture = deepcopy(fixture)
        self.components = tuple(fixture["components"])
        self.roles = fixture["roles"]
        if len(self.components) != 6 or len(set(self.components)) != 6:
            raise ValueError("P001 requires six distinct components")
        if set(self.roles) != set(ROLE_ORDER) or set(self.roles.values()) != set(self.components):
            raise ValueError("roles must bijectively cover the components")
        self.index = {name: i for i, name in enumerate(self.components)}
        self.initial = [(tuple(row["state"]), Fraction(row["weight"]))
                        for row in fixture["initial"]]
        if any(len(s) != 6 or any(x not in (0, 1) for x in s) or w <= 0
               for s, w in self.initial):
            raise ValueError("invalid physical initial state")
        if sum(w for _, w in self.initial) != 1:
            raise ValueError("initial probabilities do not normalize")
        expected = [( (r, 0, 0, 0, 0, 0), Fraction(1, 2)) for r in (0, 1)]
        if sorted((self.canonical(s), w) for s, w in self.initial) != expected:
            raise ValueError("fixture is not the declared P001 initial state")
        for gate in fixture["gates"].values():
            if gate is not None:
                controls = gate["controls"]
                if (len(set(controls)) != len(controls)
                        or gate["target"] in controls
                        or not set(controls + [gate["target"]]) <= set(self.components)):
                    raise ValueError("invalid controlled-X gate")

    @classmethod
    def read(cls, path):
        return cls(json.loads(Path(path).read_text(encoding="utf-8")))

    def value(self, state, role):
        return state[self.index[self.roles[role]]]

    def canonical(self, state):
        return tuple(self.value(state, role) for role in ROLE_ORDER)

    def gate(self, name, state):
        gate = self.fixture["gates"][name]
        if gate is None:
            return state
        result = list(state)
        if all(state[self.index[c]] for c in gate["controls"]):
            result[self.index[gate["target"]]] ^= 1
        return tuple(result)

    def branch(self, mode, r, policy):
        if mode not in (0, 1) or r not in (0, 1) or policy not in POLICIES:
            raise ValueError("invalid action, record, or causal policy")
        state, weight = next((s, w) for s, w in self.initial
                             if self.value(s, "source") == r)
        initial = state
        state = self.gate("record_initial", state)
        recorded = state
        state = self.gate(f"mode_{mode}", state)
        boundary = state
        b1 = policy[r]
        state = self.gate(f"source_{b1}", state)
        state = self.gate("feedback", state)
        state = self.gate("record_1", state)
        a1 = self.value(state, "r1")
        first = state
        b2 = policy[2 + 2*r + a1]
        state = self.gate(f"source_{b2}", state)
        state = self.gate("feedback", state)
        state = self.gate("record_2", state)
        a2 = self.value(state, "r2")
        return {
            "mode": mode, "r": r, "weight": weight,
            "controls": (b1, b2), "actuator_records": (a1, a2),
            "history": (r, b1, a1, b2, a2),
            "states": (initial, recorded, boundary, first, state),
        }

    def readout(self, state, scope):
        if scope == "full":
            return self.canonical(state)
        if scope == "actuator":
            return (self.value(state, "r1"), self.value(state, "r2"))
        raise ValueError("unknown scope")

    def law(self, mode, policy, scope, r=None):
        law = {}
        for record in ((0, 1) if r is None else (r,)):
            branch = self.branch(mode, record, policy)
            key = self.readout(branch["states"][-1], scope)
            weight = branch["weight"] if r is None else Fraction(1)
            law[key] = law.get(key, Fraction(0)) + weight
        return law

    def metric(self, mode, scope, policies=POLICIES):
        best, witness = Fraction(-1), None
        for policy in policies:
            d = total_variation(self.law(mode, policy, scope, 0),
                                self.law(mode, policy, scope, 1))
            if d > best:
                best, witness = d, policy
        return [[Fraction(0), best], [best, Fraction(0)]], witness

    def transition_tables(self):
        states = list(product((0, 1), repeat=6))
        return {name: [{"from": list(s), "to": list(self.gate(name, s))} for s in states]
                for name in self.fixture["gates"]}

    def transported(self):
        """One explicit presentation change: rename and reverse all coordinates."""
        rename = {c: f"coordinate_{i}" for i, c in enumerate(self.components)}
        fixture = deepcopy(self.fixture)
        fixture["components"] = [rename[c] for c in reversed(self.components)]
        fixture["roles"] = {role: rename[c] for role, c in self.roles.items()}
        fixture["initial"] = [{"state": list(reversed(s)), "weight": str(w)}
                              for s, w in self.initial]
        for gate in fixture["gates"].values():
            if gate is not None:
                gate["controls"] = [rename[c] for c in gate["controls"]]
                gate["target"] = rename[gate["target"]]
        return Model(fixture)


def serial_law(law):
    return [{"outcome": list(key), "probability": str(value)}
            for key, value in sorted(law.items())]


def analyze(model):
    objects = {"fixture": model.fixture,
               "transition_tables": model.transition_tables(),
               "policy_semantics": "alternative causal programs; no policy prior",
               "occurrence_semantics": "occurrences within each policy; repeated rows across policies are counterfactual alternatives, not extra physical copies",
               "actions": []}
    summary = {"id": "P001", "arithmetic": "exact integers and rational probabilities",
               "scope": "declared six-bit, two-slot, diagonal model", "actions": []}
    for mode in (0, 1):
        action = {"mode": mode, "policies": []}
        reachable = {r: set() for r in (0, 1)}
        stage_supports = [set() for _ in range(5)]
        for policy in POLICIES:
            branches = [model.branch(mode, r, policy) for r in (0, 1)]
            rows = []
            for branch in branches:
                reachable[branch["r"]].add(branch["actuator_records"])
                for support, state in zip(stage_supports, branch["states"]):
                    support.add(state)
                rows.append({
                    "record": branch["r"], "weight": str(branch["weight"]),
                    "controls": list(branch["controls"]),
                    "history": list(branch["history"]),
                    "states": [list(s) for s in branch["states"]],
                    "subnormalized_boundary": [{"state": list(branch["states"][2]),
                                                 "weight": str(branch["weight"])}],
                    "subnormalized_terminal": [{"state": list(branch["states"][-1]),
                                                 "weight": str(branch["weight"])}],
                })
            action["policies"].append({"policy": list(policy), "occurrences": rows,
                "full_law": serial_law(model.law(mode, policy, "full")),
                "actuator_law": serial_law(model.law(mode, policy, "actuator"))})
        objects["actions"].append(action)
        descriptors = {}
        for scope in ("full", "actuator"):
            matrix, witness = model.metric(mode, scope)
            descriptors[scope] = {
                "distance_matrix": [[str(x) for x in row] for row in matrix],
                "maximizing_policy": list(witness),
                "packing_at_zero": packing_size(matrix, Fraction(0))[0],
                "packing_at_one": packing_size(matrix, Fraction(1))[0],
                "profile": ([{"epsilon": "[0,1)", "N": 2}, {"epsilon": "[1,infinity)", "N": 1}]
                            if matrix[0][1] == 1 else [{"epsilon": "[0,infinity)", "N": 1}]),
            }
        summary["actions"].append({
            "mode": mode, "residual_weights": ["1/2", "1/2"],
            "full_state_support_by_stage": dict(zip(
                ("initial", "recorded", "comparison_boundary", "after_slot_1", "after_slot_2"),
                (len(support) for support in stage_supports))),
            "descriptors": descriptors,
            "reachable_actuator_records_by_r": {str(r): [list(p) for p in sorted(v)]
                                                 for r, v in reachable.items()},
        })
    # b1 = 1-r, b2 = 1, using only already acquired information.
    witness_policy = (1, 0, 1, 1, 1, 1)
    summary["common_policy_witness"] = {
        "policy": list(witness_policy),
        "mode_0": serial_law(model.law(0, witness_policy, "actuator")),
        "mode_1": serial_law(model.law(1, witness_policy, "actuator")),
    }
    summary["rejected_claim"] = "weighted within-family distance geometry determines the complete tester-indexed feedback response object"
    summary["not_established"] = ["a lushness measure", "a value ranking", "valuerhood",
                                  "a general quantum result", "emergent generativity"]
    return objects, summary
