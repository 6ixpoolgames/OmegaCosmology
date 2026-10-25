"""Comparison diagnostics. No scores are changed and no ecological label is inferred."""

from collections import defaultdict
from itertools import pairwise
from math import fsum, isfinite


def numerical_sign(value, tolerance):
    if not isfinite(value) or not isfinite(tolerance) or tolerance < 0:
        raise ValueError("Finite value and nonnegative numerical tolerance required")
    return 1 if value > tolerance else -1 if value < -tolerance else 0


def linear_interval(terms):
    """Conservative signed sum of intervals, with no independence assumption.

    Each term is (coefficient, lower, upper). Quantity/units/scope compatibility
    is the caller's typed-comparison responsibility. Overlap never becomes a
    midpoint verdict. Useful for ordinary and factorial physical comparisons.
    """
    if not terms:
        raise ValueError("At least one interval term required")
    lower, upper = [], []
    for coefficient, lo, hi in terms:
        if not all(isfinite(v) for v in (coefficient, lo, hi)) or lo > hi:
            raise ValueError(
                "Finite coefficients and ordered interval endpoints required"
            )
        a, b = coefficient * lo, coefficient * hi
        lower.append(min(a, b))
        upper.append(max(a, b))
    return {"lower": fsum(lower), "upper": fsum(upper)}


def comparison_profiles(comparisons, tolerance):
    """Separate cadence refinement from horizon extension on a retained grid.

    Sign changes are brackets between measured points, not roots or claims
    of no crossing between points. Zeros within tolerance are unresolved.
    Interval differences are average accumulation differences, not stationary rates.
    """
    seen, cadence_groups, horizon_groups = set(), defaultdict(list), defaultdict(list)
    for row in comparisons:
        key = (row["id"], row["cadence"], row["horizon"])
        if key in seen:
            raise ValueError("Duplicate comparison/cadence/horizon")
        seen.add(key)
        if any(not isfinite(x) or x <= 0 for x in key[1:]):
            raise ValueError("Positive finite cadence and horizon required")
        numerical_sign(row["delta_ell_bits"], tolerance)
        cadence_groups[row["id"], row["horizon"]].append(row)
        horizon_groups[row["id"], row["cadence"]].append(row)

    def summarize(groups, axis, fixed):
        output = []
        for (name, fixed_value), rows in sorted(groups.items()):
            points = [
                {
                    axis: r[axis],
                    "delta_ell_bits": r["delta_ell_bits"],
                    "sign": numerical_sign(r["delta_ell_bits"], tolerance),
                }
                for r in sorted(rows, key=lambda r: r[axis])
            ]
            resolved = [p for p in points if p["sign"]]
            brackets = [
                {
                    "lower": a[axis],
                    "upper": b[axis],
                    "from_sign": a["sign"],
                    "to_sign": b["sign"],
                }
                for a, b in pairwise(resolved)
                if a["sign"] != b["sign"]
            ]
            item = {
                "id": name,
                fixed: fixed_value,
                "points": points,
                "sign_change_brackets": brackets,
                "strict_sign_flip": bool(brackets),
            }
            if axis == "horizon":
                item["intervals"] = [
                    {
                        "start": a[axis],
                        "end": b[axis],
                        "delta_accumulated_bits": b["delta_ell_bits"]
                        - a["delta_ell_bits"],
                        "mean_delta_bits_per_time": (
                            b["delta_ell_bits"] - a["delta_ell_bits"]
                        )
                        / (b[axis] - a[axis]),
                    }
                    for a, b in pairwise(points)
                ]
            output.append(item)
        return output

    return {
        "schema": "omega.comparison-profiles/1",
        "tolerance_bits": tolerance,
        "cadence_audit": summarize(cadence_groups, "cadence", "horizon"),
        "horizon_audit": summarize(horizon_groups, "horizon", "cadence"),
        "scope": "Measured grid only; brackets are not exact crossover locations",
    }


def interaction_effects(effects):
    """Retain a directed, metric-specific contrast matrix without moral typing.

    Metric IDs and units cannot be mixed to label a pair mutualistic/parasitic.
    A source may be a collective, and targets may overlap. Whole-field values
    are computed separately rather than summed from parts.
    """
    required = (
        "contrast_id",
        "source",
        "target",
        "metric",
        "units",
        "comparison_kind",
        "scope",
        "conditioning",
        "evidence",
    )
    output, seen = [], set()
    for item in effects:
        if any(not item.get(k) for k in required):
            raise ValueError(
                "Interaction effects need complete metric and comparison provenance"
            )
        if item["comparison_kind"] not in ("preparation", "mechanism", "process"):
            raise ValueError("Interaction contrast kind is unsupported")
        if item["comparison_kind"] == "process" and (
            not item.get("common_present") or not item.get("implementation")
        ):
            raise ValueError(
                "Process effects require a physically implemented common-present comparison"
            )
        if not isfinite(item["horizon"]) or item["horizon"] <= 0:
            raise ValueError("A finite positive horizon is required")
        lo, hi, tol = item["lower"], item["upper"], item["tolerance"]
        numerical_sign(lo, tol)
        numerical_sign(hi, tol)
        if lo > hi:
            raise ValueError("Reversed effect interval")
        key = tuple(str(item[k]) for k in required[:-1]) + (
            item["horizon"],
            item.get("cadence"),
            item.get("resolution_id"),
        )
        if key in seen:
            raise ValueError("Duplicate interaction effect")
        seen.add(key)
        sign = "positive" if lo > tol else "negative" if hi < -tol else "unresolved"
        output.append({**item, "resolved_sign": sign})
    return {
        "schema": "omega.interaction-effects/1",
        "effects": output,
        "scope": "Effects on named metrics; no automatic ecological or ethical verdict",
    }
