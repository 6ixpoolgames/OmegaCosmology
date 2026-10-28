"""Shared symmetry and identity contracts for every evaluator."""

import math


def invariant_values(compiled, evaluate, *, description="observable"):
    compiled.require_complete()
    result = []
    for state in compiled.states:
        values = [evaluate(s) for s in compiled.model.orbit(state)]
        if any(not math.isfinite(v) for v in values):
            raise ValueError(f"Nonfinite {description}")
        if max(values) - min(values) > 1e-12:
            raise ValueError(f"{description} distinguishes unmarked representatives")
        result.append(evaluate(state))
    return result


def require_marked_identity(compiled):
    compiled.require_complete()
    if len(compiled.model.symmetry) > 1:
        raise ValueError(
            "Marked event queries require a labelled law or an equivariance proof"
        )
