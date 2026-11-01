"""Sequential exact kernel schedule, preserving distributions and history totals.

Factories are called only after releasing the preceding kernel. The caller
certifies physical state alignment; this numerical primitive validates arrays.
"""

import time

import numpy as np

from .history import entropy, validate_distribution


def stream_schedule(
    phases,
    initial,
    checkpoints,
    *,
    score_history=True,
    retain_profile=False,
    endpoint_tolerance=1e-10,
):
    """phases=(zero-argument kernel factory, positive step count).

    No reset at phase boundaries. Only requested endpoints are retained. The
    no-scoring mode supports physical/performance qualification before science.
    """
    phases = tuple(phases)
    checkpoints = set(checkpoints)
    if not phases or any(type(n) is not int or n <= 0 for _, n in phases):
        raise ValueError("Positive phase lengths required")
    total = sum(n for _, n in phases)
    if not checkpoints or any(
        type(n) is not int or not 0 <= n <= total for n in checkpoints
    ):
        raise ValueError("Checkpoints outside schedule")
    mu = validate_distribution(initial, len(initial)).copy()
    ell, step = 0.0, 0
    result = {}
    profile = [0.0] if retain_profile and score_history else None
    max_normalization_error = 0.0

    def capture():
        result[step] = {
            "endpoint": mu.copy(),
            "ell_bits": ell if score_history else None,
        }

    if 0 in checkpoints:
        capture()
    timings = []
    for factory, length in phases:
        kernel = factory()
        if (
            kernel.shape != (len(mu), len(mu))
            or not np.all(np.isfinite(kernel))
            or kernel.min() < 0
            or np.max(abs(kernel.sum(axis=1) - 1)) > 1e-10
        ):
            raise ValueError("Invalid aligned stochastic kernel")
        # Bound entropy workspace independently of the full dense kernel.
        h = (
            np.concatenate(
                [entropy(kernel[i : i + 128], axis=1) for i in range(0, len(mu), 128)]
            )
            if score_history
            else None
        )
        start = time.perf_counter()
        for _ in range(length):
            if score_history:
                ell += float(mu @ h)
            mu = mu @ kernel
            error = abs(float(mu.sum()) - 1)
            max_normalization_error = max(max_normalization_error, error)
            if (
                not np.all(np.isfinite(mu))
                or mu.min() < 0
                or error > endpoint_tolerance
            ):
                raise ArithmeticError("Schedule probability drift exceeds allowance")
            step += 1
            if profile is not None:
                profile.append(ell)
            if step in checkpoints:
                capture()
        timings.append(time.perf_counter() - start)
        del kernel, h
    return {
        "checkpoints": result,
        "propagation_seconds": timings,
        "scored": score_history,
        "profile_bits": profile,
        "max_normalization_error": max_normalization_error,
    }
