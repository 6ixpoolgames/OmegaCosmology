"""Inject native full-state alphabets into an explicit common physical alphabet.

Only identical coordinate semantics/Hamiltonians and declared constraint changes
are supported. The union is an observation alphabet, never a padded generator.
"""

from dataclasses import dataclass

import numpy as np

from .semantics import fingerprint


def constraint_identity(pattern):
    return fingerprint(
        sorted(pattern, key=lambda c: (c["coordinate"], c["operator"], c["value"]))
    )


@dataclass(frozen=True)
class ConstraintStateMapping:
    left_model_hash: str
    right_model_hash: str
    left_state_hash: str
    right_state_hash: str
    removed_constraints: tuple[str, ...]
    added_constraints: tuple[str, ...]

    def __post_init__(self):
        object.__setattr__(self, "removed_constraints", tuple(self.removed_constraints))
        object.__setattr__(self, "added_constraints", tuple(self.added_constraints))
        if not all(
            (
                self.left_model_hash,
                self.right_model_hash,
                self.left_state_hash,
                self.right_state_hash,
            )
        ):
            raise ValueError(
                "Mapping must bind both physical models and state enumerations"
            )
        if len(set(self.removed_constraints)) != len(self.removed_constraints) or len(
            set(self.added_constraints)
        ) != len(self.added_constraints):
            raise ValueError("Repeated constraint difference")

    def verify(self, left, right):
        left.require_complete()
        right.require_complete()
        if (
            left.model_hash,
            right.model_hash,
            left.state_order_hash,
            right.state_order_hash,
        ) != (
            self.left_model_hash,
            self.right_model_hash,
            self.left_state_hash,
            self.right_state_hash,
        ):
            raise ValueError("Stale or wrong-law state mapping")
        a, b = left.model.record(), right.model.record()
        la = {constraint_identity(p) for p in a["forbidden"]}
        rb = {constraint_identity(p) for p in b["forbidden"]}
        if (
            set(self.removed_constraints) != la - rb
            or set(self.added_constraints) != rb - la
        ):
            raise ValueError("Mapping must declare every constraint difference exactly")
        for field in a:
            if field not in ("id", "rules", "forbidden") and a[field] != b[field]:
                raise ValueError(
                    "State mapping changes common physical grammar: " + field
                )
        # This first adapter uses already-canonical identical physical labels.
        # It does not rename, merge or quotient states.
        if len(left.states) != len(set(left.states)) or len(right.states) != len(
            set(right.states)
        ):
            raise ValueError("Noninjective ambient state labels")
        states = tuple(sorted(set(left.states) | set(right.states)))
        for state in states:
            if left.model.energy(state) != right.model.energy(
                state
            ) or left.model.log_degeneracy(state) != right.model.log_degeneracy(state):
                raise ValueError("Ambient Hamiltonian/degeneracy mismatch")
        return {
            "kind": "identity_coordinate_constraint_mapping",
            "left_model_hash": left.model_hash,
            "right_model_hash": right.model_hash,
            "ambient_state_hash": fingerprint(states),
            "ambient_states": len(states),
            "left_native_states": len(left.states),
            "right_native_states": len(right.states),
            "left_only_states": len(set(left.states) - set(right.states)),
            "right_only_states": len(set(right.states) - set(left.states)),
            "removed_constraint_hashes": list(self.removed_constraints),
            "added_constraint_hashes": list(self.added_constraints),
            "scoring": "native laws only; injective history labels; missing symbols have zero weight; no padded physical transitions",
        }

    def embed_distribution(self, left, right, which, weights):
        self.verify(left, right)
        if which not in ("left", "right"):
            raise ValueError("Choose native left/right alphabet")
        native = left if which == "left" else right
        weights = np.asarray(weights, dtype=float)
        if (
            weights.shape != (len(native.states),)
            or not np.all(np.isfinite(weights))
            or weights.min() < 0
            or abs(weights.sum() - 1) > 1e-10
        ):
            raise ValueError("Normalized native distribution required")
        alphabet = tuple(sorted(set(left.states) | set(right.states)))
        indices = {s: i for i, s in enumerate(alphabet)}
        result = np.zeros(len(alphabet))
        for state, weight in zip(native.states, weights):
            result[indices[state]] = weight
        return result
