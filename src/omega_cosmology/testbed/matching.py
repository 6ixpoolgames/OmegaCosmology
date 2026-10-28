"""Bounded physical moment matching, with no access to the history score."""

from dataclasses import asdict, dataclass
from itertools import product

import numpy as np
from scipy.optimize import brentq, least_squares


@dataclass(frozen=True)
class MomentSpec:
    quantity: str
    units: str
    horizon: float | None
    convention: str
    absolute_tolerance: float = 1e-12
    relative_tolerance: float = 0.001

    def __post_init__(self):
        if (
            not self.quantity
            or not self.units
            or self.convention
            not in ("continuous_integral", "sampled_count", "stationary_rate")
        ):
            raise ValueError(
                "Named quantity, units and explicit moment convention required"
            )
        if self.convention == "stationary_rate":
            if self.horizon is not None:
                raise ValueError("Stationary rate has no finite matching horizon")
        elif self.horizon is None or not np.isfinite(self.horizon) or self.horizon <= 0:
            raise ValueError("Finite positive matching horizon required")
        if (
            any(
                not np.isfinite(v) or v < 0
                for v in (self.absolute_tolerance, self.relative_tolerance)
            )
            or self.absolute_tolerance + self.relative_tolerance <= 0
        ):
            raise ValueError("Explicit finite nonnegative moment tolerances required")


def match_one_physical_moment(
    evaluate, target, bounds, *, primary, moment_specs, max_evaluations=24
):
    """Bracket one physical moment; never label other unmatched moments matched.

    One positive parameter, one declared bracket. Other physical quantities stay
    in the output and acceptance tests. No uniqueness/global-feasibility claim.
    """
    if (
        len(bounds) != 1
        or primary not in target
        or set(moment_specs) != set(target)
        or any(
            not isinstance(s, MomentSpec) or s.quantity != k
            for k, s in moment_specs.items()
        )
        or type(max_evaluations) is not int
        or max_evaluations < 3
        or any(not np.isfinite(v) for v in target.values())
    ):
        raise ValueError(
            "One parameter, typed moments and primary physical quantity required"
        )
    name, (lo, hi) = next(iter(bounds.items()))
    if not 0 < lo < hi or not np.isfinite(hi):
        raise ValueError("Positive finite parameter bracket required")
    allowances = {
        k: moment_specs[k].absolute_tolerance
        + moment_specs[k].relative_tolerance * abs(v)
        for k, v in target.items()
    }
    if any(not np.isfinite(v) or v <= 0 for v in allowances.values()):
        raise ValueError("Positive finite matching allowances required")
    rows, cache = [], {}

    class BudgetReached(Exception):
        pass

    def objective(log_parameter):
        parameter = float(np.exp(log_parameter))
        if parameter not in cache:
            if len(rows) >= max_evaluations:
                raise BudgetReached
            values = evaluate({name: parameter})
            if set(values) != set(target) or any(
                not np.isfinite(v) for v in values.values()
            ):
                raise ValueError(
                    "Moment evaluator returned different/nonfinite quantities"
                )
            row = {
                "parameters": {name: parameter},
                "moments": values,
                "absolute_residuals": {k: values[k] - v for k, v in target.items()},
                "scaled_residuals": {
                    k: (values[k] - v) / allowances[k] for k, v in target.items()
                },
            }
            rows.append(row)
            cache[parameter] = row
        return cache[parameter]["scaled_residuals"][primary]

    left, right = objective(np.log(lo)), objective(np.log(hi))
    reason = "no_sign_bracket"
    if left * right <= 0:
        try:
            brentq(objective, np.log(lo), np.log(hi), xtol=1e-10, rtol=1e-10)
            reason = "bracketed_root_completed"
        except BudgetReached:
            reason = "literal_evaluation_budget_reached"
    best = min(rows, key=lambda r: abs(r["scaled_residuals"][primary]))
    all_ok = max(abs(v) for v in best["scaled_residuals"].values()) <= 1
    primary_ok = abs(best["scaled_residuals"][primary]) <= 1
    return {
        "status": "matched"
        if all_ok
        else (
            "primary_moment_matched_only"
            if primary_ok
            else "not_matched_in_bounded_search"
        ),
        "primary": primary,
        "target": target,
        "bounds": bounds,
        "best": best,
        "evaluations": rows,
        "absolute_allowances": allowances,
        "moment_specs": {k: asdict(v) for k, v in moment_specs.items()},
        "termination": reason,
        "scope": "One physical-moment bracket; other moment residuals retained; no path match or global certificate",
    }


def match_physical_moments(
    evaluate, target, bounds, *, max_evaluations=24, tolerance=None, moment_specs=None
):
    """Probe then fit in a positive parameter box; report a failed match honestly.

    evaluate receives only parameters and returns the named physical moments.
    Bounds constrain the physical family, not a post-hoc score correction.
    Every evaluated point is retained. No inference of global infeasibility.
    """
    names = tuple(bounds)
    moments = tuple(target)
    if (
        not names
        or len(names) > 3
        or not moments
        or type(max_evaluations) is not int
        or max_evaluations < 1
        or (tolerance is not None and (not np.isfinite(tolerance) or tolerance <= 0))
        or any(not np.isfinite(v) for v in target.values())
        or any(
            len(b) != 2 or not 0 < b[0] < b[1] or not np.isfinite(b[1])
            for b in bounds.values()
        )
    ):
        raise ValueError(
            "Finite targets, positive bounded parameters and search budget required"
        )
    lo = np.log([bounds[k][0] for k in names])
    hi = np.log([bounds[k][1] for k in names])
    if moment_specs is not None:
        if (
            tolerance is not None
            or set(moment_specs) != set(moments)
            or any(
                not isinstance(s, MomentSpec) or s.quantity != k
                for k, s in moment_specs.items()
            )
        ):
            raise ValueError(
                "One typed spec per target; do not mix legacy scaled tolerance"
            )
        allowances = np.array(
            [
                moment_specs[k].absolute_tolerance
                + moment_specs[k].relative_tolerance * abs(target[k])
                for k in moments
            ]
        )
        mode = "typed_absolute_plus_relative"
    elif tolerance is not None:
        # Explicit compatibility only. Retained snapshots keep their original rule.
        allowances = tolerance * np.maximum(1.0, np.abs([target[k] for k in moments]))
        mode = "explicit_legacy_scaled_tolerance"
    else:
        allowances = 1e-12 + 0.001 * np.abs([target[k] for k in moments])
        mode = "absolute_plus_relative_no_physical_context"
    if np.any(allowances <= 0) or not np.isfinite(allowances).all():
        raise ValueError("Positive finite absolute matching allowances required")
    scales = allowances
    rows, cache = [], {}

    def evaluate_at(log_values):
        parameters = {k: float(np.exp(x)) for k, x in zip(names, log_values)}
        key = tuple(parameters.values())
        if key not in cache:
            values = evaluate(parameters)
            if set(values) != set(moments) or any(
                not np.isfinite(v) for v in values.values()
            ):
                raise ValueError(
                    "Moment evaluator returned different/nonfinite quantities"
                )
            residual = (np.array([values[k] - target[k] for k in moments])) / scales
            entry = {
                "parameters": parameters,
                "moments": values,
                "scaled_residuals": dict(zip(moments, residual.tolist())),
                "absolute_residuals": {k: values[k] - target[k] for k in moments},
            }
            rows.append(entry)
            cache[key] = residual
        return cache[key]

    for point in product((0.0, 0.5, 1.0), repeat=len(names)):
        evaluate_at(lo + np.array(point) * (hi - lo))
    best = min(rows, key=lambda r: sum(v * v for v in r["scaled_residuals"].values()))
    # SciPy's max_nfev excludes finite-difference calls. Also enforce a literal
    # moment-evaluator budget for the fitted search, including those calls.
    probe_count = len(rows)

    class BudgetReached(Exception):
        pass

    def objective(x):
        key = tuple(float(np.exp(v)) for v in x)
        if key not in cache and len(rows) - probe_count >= max_evaluations:
            raise BudgetReached
        return evaluate_at(x)

    reason = "optimizer_completed"
    try:
        least_squares(
            objective,
            np.log([best["parameters"][k] for k in names]),
            bounds=(lo, hi),
            max_nfev=max_evaluations,
            xtol=1e-9,
            ftol=1e-9,
            gtol=1e-9,
        )
    except BudgetReached:
        reason = "literal_evaluation_budget_reached"
    # A lower least-squares norm can still violate one moment's limit while
    # another evaluated point satisfies every limit. Feasibility takes priority.
    best = min(
        rows,
        key=lambda r: (
            max(abs(v) for v in r["scaled_residuals"].values()) > 1.0,
            sum(v * v for v in r["scaled_residuals"].values()),
        ),
    )
    matched = max(abs(v) for v in best["scaled_residuals"].values()) <= 1.0
    return {
        "status": "matched" if matched else "not_matched_in_bounded_search",
        "target": target,
        "bounds": bounds,
        "scale": dict(zip(moments, scales.tolist())),
        "tolerance": 1.0,
        "matching_contract": mode,
        "legacy_scaled_tolerance": tolerance,
        "moment_specs": {k: asdict(v) for k, v in (moment_specs or {}).items()},
        "absolute_allowances": dict(zip(moments, allowances.tolist())),
        "best": best,
        "evaluations": rows,
        "probe_evaluations": probe_count,
        "fit_evaluation_budget": max_evaluations,
        "termination": reason,
        "scope": "Physical moment search only; no lushness objective, no all-path match or global infeasibility certificate",
    }
