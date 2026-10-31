"""Capped worker for literal native replay and separately frozen current audit."""

import argparse
import importlib.util
import json
import sys
from hashlib import sha256
from itertools import pairwise
from pathlib import Path


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def write(p, value):
    Path(p).write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def verify(root):
    manifest = read(root / "MANIFEST.json")
    for row in manifest["files"]:
        path = (root / row["path"]).resolve()
        if (
            not path.is_relative_to(root.resolve())
            or sha256(path.read_bytes()).hexdigest() != row["sha256"]
        ):
            raise ValueError("Frozen input integrity failed: " + row["path"])
    return manifest


def native(a, study):
    import numpy as np

    original = a.run / "original" / study["id"]
    manifest = verify(original)
    protocol = read(original / study["protocol"])
    if (
        sha256((original / study["protocol"]).read_bytes()).hexdigest()
        != manifest["protocol_sha256"]
    ):
        raise ValueError("Original protocol identity failed")
    sys.path.insert(0, str(original / "src"))
    law = next(v for v in protocol["laws"] if v["id"] == a.law)
    if study["id"] == "R1":
        path = original / "scripts/r1_worker.py"
        spec = importlib.util.spec_from_file_location("original_r1_worker", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.argv = [
            str(path),
            "--law",
            a.law,
            "--cadence",
            str(a.cadence),
            "--out-dir",
            str(a.out),
        ]
        module.main()
        result = read(a.out / "RESULT.json")
    else:
        from omega_cosmology.testbed.finite_study import evaluate_case

        result = evaluate_case(protocol, law, a.cadence)
        write(a.out / "RESULT.json", result)
    # Export independently reconstructible native law, not a changed protocol.
    from omega_cosmology.testbed.backends import enumerate_model
    from omega_cosmology.testbed.physics import LocalModel

    model = LocalModel.from_record(law["model"])
    roots = [tuple(s) for prep in protocol["preparations"] for s, _ in prep["roots"]]
    c = enumerate_model(model, roots, max_states=protocol.get("max_states", 1000))
    c.require_complete()
    np.savez_compressed(a.out / "LAW.npz", states=np.array(c.states), q=c.q.toarray())
    print(
        json.dumps(
            {
                "status": result["status"],
                "states": len(c.states),
                "rows": len(result["rows"]),
            }
        )
    )


def paired_contract(protocol, laws, compiled, prep, cadence, horizon):
    from omega_cosmology.testbed.semantics import (
        ComparisonSpec,
        LawSpec,
        ObservationSpec,
        PresentSpec,
        QuantitySpec,
        validate_comparison,
    )

    present = PresentSpec(
        "P0.present",
        tuple((tuple(s), w) for s, w in prep["roots"]),
        conditioning=prep["conditioning"],
        sufficiency="All finite rule dependencies retained from original sufficient state",
    )
    comparison = ComparisonSpec(
        "P0.mechanism",
        "mechanism",
        horizon,
        cadence,
        {"endowment": "original root, physical grammar and boundaries"},
    )
    arms = []
    for law, c in zip(laws, compiled):
        # Boundary identity is read from the physical input, not chosen from a
        # name like 'cooperation' or a desired matching verdict.
        boundary = {
            "beta": c.model.beta,
            "external_channels": [
                r
                for r in law["model"]["rules"]
                if r.get("boundary", "native") != "native"
            ],
            "unresolved": "external bath/source histories",
        }
        arms.append(
            {
                "compiled": c,
                "present": present,
                "law": LawSpec(law["id"], c.model.fingerprint(), boundary),
                "observation": ObservationSpec(
                    "P0.whole", tuple(k.name for k in c.model.coordinates)
                ),
                "comparison": comparison,
                "quantity": QuantitySpec(
                    "history.full",
                    "Complete sampled history conditional on full present",
                    "bits",
                    "full_present",
                ),
            }
        )
    try:
        return validate_comparison(comparison, *arms)
    except ValueError as exc:
        return {
            "status": "inapplicable_to_literal_historical_inputs",
            "reason": str(exc),
            "material_status": [c.model.material_status for c in compiled],
            "physics_changed": False,
        }


def audit(a, study):
    import math

    import numpy as np
    from scipy.linalg import expm
    from scipy.sparse.linalg import expm_multiply

    current = a.run / "current"
    sys.path.insert(0, str(current / "src"))
    from omega_cosmology.testbed.backends import enumerate_model
    from omega_cosmology.testbed.history import (
        distributions_and_occupation,
        history_profile,
        sampled_kernel,
        sampled_support,
    )
    from omega_cosmology.testbed.physics import LocalModel
    from omega_cosmology.testbed.profile_analysis import geometric_total, kernel_profile
    from omega_cosmology.testbed.thermodynamics import audit_equilibrium, balance

    plan = read(a.run / "PLAN.json")
    protocol = read(a.run / "original" / study["id"] / study["protocol"])
    prep = next(v for v in protocol["preparations"] if v["id"] == study["preparation"])
    roots = [tuple(s) for pr in protocol["preparations"] for s, _ in pr["roots"]]
    models, laws, decompositions, initials, results, native_results = (
        [],
        [],
        [],
        [],
        {},
        {},
    )
    for name in study["laws"]:
        law = next(l for l in protocol["laws"] if l["id"] == name)
        case = a.run / "jobs" / (study["id"] + "__" + name + "__" + str(a.cadence))
        original_result = read(case / "ORIGINAL_RESULT.json")
        replay = read(case / "RESULT.json")
        key = lambda r: (r["preparation"], r["horizon"])
        old_rows = {key(r): r for r in original_result["rows"]}
        if set(old_rows) != {key(r) for r in replay["rows"]}:
            raise ValueError("Native replay row identity changed")
        native_error, projected_error = 0.0, 0.0
        for row in replay["rows"]:
            old = old_rows[key(row)]
            error = abs(row["history"]["ell_bits"] - old["history"]["ell_bits"])
            native_error = max(native_error, error)
            if error > 1e-7 + 1e-10 * abs(old["history"]["ell_bits"]):
                raise ArithmeticError("Native finite history failed reproduction")
            for scope, interval in row.get("projected_histories", {}).items():
                for field in ("lower_bits", "upper_bits"):
                    error = abs(
                        interval[field] - old["projected_histories"][scope][field]
                    )
                    projected_error = max(projected_error, error)
                    if error > 1e-7 + 1e-10 * abs(interval[field]):
                        raise ArithmeticError(
                            "Native projected bound failed reproduction"
                        )
        model = LocalModel.from_record(law["model"])
        c = enumerate_model(model, roots, max_states=protocol.get("max_states", 1500))
        c.require_complete()
        native_law = np.load(case / "LAW.npz", allow_pickle=False)
        if not np.array_equal(native_law["states"], np.array(c.states)):
            raise ValueError("Current enumeration changed native state order")
        qerror = float(np.max(abs(native_law["q"] - c.q.toarray())))
        if qerror > 1e-10:
            raise ArithmeticError("Current grammar changed native generator")
        mu = np.zeros(len(c.states))
        for state, w in prep["roots"]:
            mu[c.index[model.canonical(tuple(state))]] += w
        p = sampled_kernel(c, a.cadence, max_dense_bytes=128 * 1024**2)
        independent = expm_multiply(c.q * a.cadence, np.eye(len(c.states)))
        kerror = float(np.max(abs(p - independent)))
        if kerror > 1e-10:
            raise ArithmeticError("Independent kernel action disagrees")
        decomposition = kernel_profile(p, structural_support=sampled_support(c))
        coords = decomposition.coordinates(mu, cadence=a.cadence)
        physics, old_selected = [], {}
        for row in replay["rows"]:
            if row["preparation"] != prep["id"]:
                continue
            T = row["horizon"]
            endpoint, occupation = distributions_and_occupation(c, mu, T)
            physical = balance(c, mu, endpoint, occupation)
            work_in, work_out = np.zeros(len(mu)), np.zeros(len(mu))
            for i, _, event in c.ledger:
                work_in[i] += event.rate * max(event.work, 0)
                work_out[i] += event.rate * max(-event.work, 0)
            physical.update(
                {
                    "horizon": T,
                    "work_accepted_gross": float(occupation @ work_in),
                    "work_returned_gross": float(occupation @ work_out),
                    "expected_jumps": float(occupation @ -c.q.diagonal()),
                }
            )
            for field in (
                "work_net",
                "heat_export",
                "delta_energy",
                "work_accepted_gross",
                "work_returned_gross",
                "expected_jumps",
            ):
                residual = abs(physical[field] - row["physical"][field])
                if residual > 1e-8 + 1e-10 * abs(row["physical"][field]):
                    raise ArithmeticError(
                        "Independent physical accounting failed: " + field
                    )
            if abs(physical["energy_residual"]) > 1e-8:
                raise ArithmeticError("Integrated first law failed")
            physics.append(physical)
            old_selected[T] = row
            asym = row["asymptotic"]
            for field, fresh in (
                ("rate_bits_per_time", coords["rate_bits_per_time"]),
                ("offset_bits", coords["bias_offset_bits"]),
            ):
                if field in asym and abs(asym[field] - fresh) > 1e-8 + 1e-9 * abs(
                    asym[field]
                ):
                    raise ArithmeticError("Kernel rate/bias failed native agreement")
        # Independent dense continuous endpoint only at the original longest T.
        final_T = max(protocol["horizons"])
        endpoint, _ = distributions_and_occupation(c, mu, final_T)
        continuous_error = float(
            np.max(abs(endpoint - mu @ expm(c.q.toarray() * final_T)))
        )
        if continuous_error > 1e-8:
            raise ArithmeticError("Independent continuous propagation failed")
        results[name] = {
            "states": len(c.states),
            "native_reproduction_max_bits": native_error,
            "native_projection_reproduction_max_bits": projected_error,
            "current_generator_difference": qerror,
            "independent_kernel_difference": kerror,
            "continuous_endpoint_difference": continuous_error,
            "native_rows_replayed": len(replay["rows"]),
            "profile_coordinates": coords,
            "physical": physics,
            "equilibrium_audit": audit_equilibrium(c),
            "projected_histories": [
                {"horizon": T, "bounds": row.get("projected_histories", {})}
                for T, row in old_selected.items()
            ],
            "projected_asymptotics": "unsupported; no quotient Markov approximation",
        }
        models.append(c)
        laws.append(law)
        decompositions.append(decomposition)
        initials.append(mu)
        native_results[name] = old_selected
    coefficients = study["coefficients"]
    delta_rate = sum(
        k * float(mu @ d.rate)
        for k, mu, d in zip(coefficients, initials, decompositions)
    )
    delta_offset = sum(
        k * float(mu @ d.bias)
        for k, mu, d in zip(coefficients, initials, decompositions)
    )
    bound = sum(
        abs(k) * float(np.max(abs(d.bias)))
        for k, d in zip(coefficients, decompositions)
    )
    threshold = None
    if abs(delta_rate) > 1e-8:
        threshold = max(
            0,
            math.floor(
                (bound + 1e-8 - np.sign(delta_rate) * delta_offset) / abs(delta_rate)
            )
            + 1,
        )
    original_steps = max(round(T / a.cadence) for T in protocol["horizons"])
    desired = max(original_steps, 3 * threshold if threshold is not None else 0)
    steps = min(plan["max_profile_steps"], desired)
    grid = sorted(
        set(
            [0, steps]
            + [round(T / a.cadence) for T in protocol["horizons"]]
            + [int(v) for v in np.geomspace(1, steps, 48)]
        )
    )
    contrast = np.zeros(steps + 1)
    original_contrast, max_identity = {}, 0.0
    for name, k, d, mu in zip(study["laws"], coefficients, decompositions, initials):
        full = history_profile(d.p, mu, steps)
        contrast += k * full
        evolution, maxerr, remainder_profile = mu.copy(), 0.0, []
        # Walk independently to check the bias identity at the reporting grid.
        previous = 0
        for n in grid:
            for _ in range(n - previous):
                evolution = evolution @ d.p
            previous = n
            rem = float(evolution @ d.bias)
            identity = float(n * (mu @ d.rate) + mu @ d.bias - rem)
            maxerr = max(maxerr, abs(full[n] - identity))
            remainder_profile.append(
                {
                    "steps": n,
                    "physical_duration": n * a.cadence,
                    "ell_bits": float(full[n]),
                    "remainder_bits": rem,
                }
            )
        if maxerr > 1e-7 + 1e-10 * max(abs(full)):
            raise ArithmeticError("Direct profile and Poisson identity disagree")
        max_identity = max(max_identity, maxerr)
        selected_error = 0.0
        for T, row in native_results[name].items():
            e = abs(full[round(T / a.cadence)] - row["history"]["ell_bits"])
            selected_error = max(selected_error, e)
            if e > 1e-7 + 1e-10 * abs(row["history"]["ell_bits"]):
                raise ArithmeticError("Independent current profile failed reproduction")
            original_contrast[T] = (
                original_contrast.get(T, 0.0) + k * row["history"]["ell_bits"]
            )
        results[name]["independent_profile_reproduction_max_bits"] = selected_error
        results[name]["profile"] = remainder_profile
        results[name]["geometric_endings"] = [
            {"mean_physical_duration": mean, **geometric_total(d, mu, mean / a.cadence)}
            for mean in (10, 100, 1000, 10000)
        ]
        results[name]["uniform_ending"] = {
            "ending": "independent_uniform_steps_0_through_evaluated_window",
            "max_steps": steps,
            "max_physical_duration": steps * a.cadence,
            "ell_expected_bits": float(np.mean(full)),
        }
    nonzero = np.flatnonzero(abs(contrast) > 1e-7)
    changes = [
        {
            "last_opposite_step": int(x),
            "first_new_step": int(y),
            "physical_interval": [float(x * a.cadence), float(y * a.cadence)],
        }
        for x, y in pairwise(nonzero)
        if np.sign(contrast[x]) != np.sign(contrast[y])
    ]
    pairs = study.get("pair_indices", [[0, 1]])
    certificates = [
        paired_contract(
            protocol,
            [laws[i], laws[j]],
            [models[i], models[j]],
            prep,
            a.cadence,
            max(protocol["horizons"]),
        )
        for i, j in pairs
    ]
    write(
        a.out / "AUDIT.json",
        {
            "status": "passed",
            "study": study["id"],
            "cadence": a.cadence,
            "arms": results,
            "paired_contracts": certificates,
            "contrast": {
                "coefficients": dict(zip(study["laws"], coefficients)),
                "delta_rate_bits_per_step": delta_rate,
                "delta_rate_bits_per_time": delta_rate / a.cadence,
                "delta_bias_offset_bits": delta_offset,
                "remainder_bound_bits": bound,
                "line_crossing_steps": -delta_offset / delta_rate
                if abs(delta_rate) > 1e-8
                else None,
                "eventual_sign_bound_from_step": threshold,
                "tail_threshold_reached": threshold is not None and steps >= threshold,
                "desired_steps": desired,
                "evaluated_steps": steps,
                "cap_limited": steps < desired,
                "observed_crossings": changes,
                "classification": "observed_crossing"
                if changes
                else "no_crossing_observed_on_evaluated_window",
                "original_horizons": [
                    {"horizon": T, "delta_bits": v}
                    for T, v in sorted(original_contrast.items())
                ],
                "profile": [
                    {
                        "steps": n,
                        "physical_duration": n * a.cadence,
                        "delta_bits": float(contrast[n]),
                    }
                    for n in grid
                ],
            },
            "max_profile_identity_residual_bits": max_identity,
            "limits": "Float64 checks; no rounding, physical-faithfulness, exterior-cancellation or ethical certificate. Tail inequalities are numerical evaluations, not interval proofs.",
        },
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "study": study["id"],
                "cadence": a.cadence,
                "steps": steps,
                "crossings": len(changes),
            }
        )
    )


def references(a):
    import numpy as np

    sys.path.insert(0, str(a.run / "current/src"))
    from omega_cosmology.testbed.history import history_profile
    from omega_cosmology.testbed.profile_analysis import (
        contrast_tail,
        geometric_total,
        kernel_profile,
        state_dependent_stop,
        uniform_total,
    )

    def delayed(delay):
        p = np.zeros((delay + 3, delay + 3))
        for k in range(delay):
            p[k, k + 1] = 1
        p[delay, -2:] = 0.5
        p[-2, -2] = p[-1, -1] = 1
        return p

    p = delayed(2)
    early, late = np.eye(5)[2], np.eye(5)[0]
    d = kernel_profile(p)
    ep, lp = history_profile(p, early, 128), history_profile(p, late, 128)
    if not (np.all(ep >= lp) and ep[3] == lp[3]):
        raise ArithmeticError("Early/late reference construction invalid")
    cases = {
        "early_late": {
            "early_profile": ep.tolist(),
            "late_profile": lp.tolist(),
            "equal_at_T3": True,
            "geometric": [],
            "uniform": [],
        }
    }
    residuals = []
    for mean in (10, 100, 1000, 10000):
        e, l = geometric_total(d, early, mean), geometric_total(d, late, mean)
        rho = mean / (mean + 1)
        residuals += [
            abs(e["ell_expected_bits"] - rho),
            abs(l["ell_expected_bits"] - rho**3),
            e["identity_residual_bits"],
            l["identity_residual_bits"],
        ]
        cases["early_late"]["geometric"].append(
            {"mean_steps": mean, "early": e, "late": l}
        )
    for n in (0, 3, 16, 128):
        e, l = uniform_total(d, early, n), uniform_total(d, late, n)
        residuals += [
            abs(e["ell_expected_bits"] - ep[: n + 1].mean()),
            abs(l["ell_expected_bits"] - lp[: n + 1].mean()),
        ]
        cases["early_late"]["uniform"].append({"max_steps": n, "early": e, "late": l})
    cases["equal_rate_equal_offset_distinct_transient"] = {
        "early": d.coordinates(early),
        "late": d.coordinates(late),
    }
    zero = np.eye(5)[3]
    cases["equal_rate_distinct_offset"] = {
        "unresolved_bit": d.coordinates(early),
        "already_fixed_bit": d.coordinates(zero),
        "limiting_difference": 1.0,
    }
    coin = np.array([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0.5, 0.5], [0, 0, 0.5, 0.5]])
    c, cmu = kernel_profile(coin), np.array([1, 0, 0, 0])
    cases["crossing"] = {
        "tail": contrast_tail(c, cmu, d, early),
        "difference": (history_profile(coin, cmu, 128) - ep).tolist(),
    }
    if not (
        cases["crossing"]["difference"][1] < 0
        and cases["crossing"]["difference"][4] > 0
    ):
        raise ArithmeticError("Crossing reference did not cross")
    pa = np.zeros((12, 12))
    pa[0, 1:3] = 0.5
    for i in range(1, 9):
        pa[i, i + 2] = 1
    pa[9:, 10:] = 0.5
    pb = np.zeros((8, 8))
    pb[0, 1] = 1
    pb[1, 2:4] = 0.5
    pb[2:4, 4:8] = 0.25
    for i in range(4, 8):
        pb[i, i] = 1
    amu, bmu = np.eye(12)[0], np.eye(8)[0]
    ap, bp = kernel_profile(pa), kernel_profile(pb)
    double = history_profile(pa, amu, 128) - history_profile(pb, bmu, 128)
    signs = np.sign(double[abs(double) > 1e-8])
    if np.count_nonzero(signs[1:] != signs[:-1]) != 2:
        raise ArithmeticError("Multiple-crossing reference invalid")
    cases["multiple_crossings"] = {
        "difference": double.tolist(),
        "tail": contrast_tail(ap, amu, bp, bmu),
    }
    periodic = np.array([[0, 0.5, 0.5], [1, 0, 0], [1, 0, 0]])
    pd, pmu = kernel_profile(periodic), np.array([1, 0, 0])
    direct = history_profile(periodic, pmu, 128)
    residuals += [abs(pd.at(pmu, n)["ell_bits"] - direct[n]) for n in range(129)]
    cases["periodic"] = {
        "coordinates": pd.coordinates(pmu),
        "bias_remainders": [pd.at(pmu, n) for n in range(16)],
    }
    # Termination record has probabilities .5, .25, .25 exactly.
    stop = state_dependent_stop(delayed(0), [1, 0, 0], [0.5, 1, 1])
    residuals.append(abs(stop["stopped_record_entropy_bits"] - 1.5))
    cases["state_dependent_stop"] = stop
    if max(residuals) > 1e-8:
        raise ArithmeticError("Ending/profile reference identity failed")
    write(
        a.out / "REFERENCES.json",
        {
            "status": "passed",
            "max_identity_residual_bits": max(residuals),
            "cases": cases,
            "limits": "Synthetic finite-kernel mathematical verification, not physically paid chemistry or latest-Appendix conformance",
        },
    )
    print(
        json.dumps({"status": "passed", "max_identity_residual_bits": max(residuals)})
    )


def main():
    if sys.stdin.readline().strip() != "GO":
        raise SystemExit("Capped worker handshake required")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("native", "audit", "references"))
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--study")
    parser.add_argument("--law")
    parser.add_argument("--cadence", type=float)
    parser.add_argument("--out", type=Path, required=True)
    a = parser.parse_args()
    verify(a.run / "current")
    study = next(
        (s for s in read(a.run / "PLAN.json")["studies"] if s["id"] == a.study), None
    )
    if a.mode == "references":
        references(a)
    elif a.mode == "native":
        native(a, study)
    else:
        audit(a, study)


if __name__ == "__main__":
    main()
