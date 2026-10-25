"""Frozen R1 exact worker. The parent assigns resource caps before GO."""

import sys

if __name__ == "__main__" and sys.stdin.readline().strip() != "GO":
    raise SystemExit("Runner GO gate required")


def main():
    import argparse
    import json
    import platform
    from hashlib import sha256
    from pathlib import Path
    from time import perf_counter

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--law", required=True)
    parser.add_argument("--cadence", required=True, type=float)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "src"))
    started = perf_counter()
    manifest_path = root / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for row in manifest["files"]:
        if sha256((root / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            raise RuntimeError("Changed frozen input: " + row["path"])
    protocol = json.loads(
        (root / "research/studies/R1-constructed-access/PROTOCOL.json").read_text(
            encoding="utf-8"
        )
    )
    if args.cadence not in protocol["cadences"]:
        raise ValueError("Undeclared cadence")
    law_record = next(v for v in protocol["laws"] if v["id"] == args.law)
    import numpy as np
    import scipy
    from scipy.linalg import expm
    from scipy.sparse.linalg import expm_multiply

    from omega_cosmology.testbed.backends import enumerate_model
    from omega_cosmology.testbed.history import (
        distributions_and_occupation,
        evaluate_history,
        history_profile,
        irreducible_asymptotics,
        sampled_kernel,
        sampled_support,
    )
    from omega_cosmology.testbed.physics import LocalModel
    from omega_cosmology.testbed.readouts import (
        activity_coefficients,
        coordinate_entropy_rewards,
        cumulative_sampled_rewards,
        two_event_monitor,
    )
    from omega_cosmology.testbed.semantics import (
        ComparisonSpec,
        LawSpec,
        ObservationSpec,
        PresentSpec,
        QuantitySpec,
    )
    from omega_cosmology.testbed.thermodynamics import (
        audit_equilibrium,
        balance,
        equilibrium,
        free_energy,
    )

    model = LocalModel.from_record(law_record["model"])
    roots = [tuple(s) for prep in protocol["preparations"] for s, _ in prep["roots"]]
    for state in roots:
        model.validate(state)
        if str(model.energy(state)) != protocol["energy_per_root"]:
            raise ValueError("Unmatched initial energy")
    t = perf_counter()
    compiled = enumerate_model(model, roots, max_states=1000)
    compiled.require_complete()
    eq_audit = audit_equilibrium(compiled)
    support = sampled_support(compiled)
    n = len(compiled.states)
    names = tuple(c.name for c in model.coordinates)
    if list(names) != protocol["coordinate_order"]:
        raise ValueError("Unmatched coordinate order")
    p = sampled_kernel(compiled, args.cadence)
    independent_kernel = expm_multiply(compiled.q * args.cadence, np.eye(n))
    kernel_residual = float(np.max(abs(p - independent_kernel)))
    if kernel_residual > protocol["numerical"]["kernel_agreement_tolerance"]:
        raise ArithmeticError("Independent sampled-kernel check failed")
    parts = coordinate_entropy_rewards(p, compiled.states, tuple(range(len(names))))
    bond = np.array([s[model.indices["bond"]] for s in compiled.states], dtype=float)
    active = np.array(
        [
            s[model.indices["a.active"]] + s[model.indices["b.active"]]
            for s in compiled.states
        ],
        dtype=float,
    )
    bank = np.array([0.5 * s[model.indices["bank"]] for s in compiled.states])
    usable = np.array(
        [s[model.indices["carrier"]] == 2 for s in compiled.states], dtype=float
    )
    inactive = (active == 0).astype(float)
    functional = bond > 0
    closed = int(np.sum(~support[:, functional].any(axis=1)))
    pi, energies, log_g = equilibrium(compiled)
    f_eq, _ = free_energy(pi, energies, log_g, model.beta)
    # Independent dense operators, used to audit sparse propagation and average
    # conditional-root free energy without inserting the entropy of drawing a root.
    block = np.zeros((2 * n, 2 * n))
    block[:n, :n] = compiled.q.toarray()
    block[:n, n:] = np.eye(n)
    operators = {T: expm(block * T) for T in protocol["horizons"]}
    setup_seconds = perf_counter() - t
    rows = []
    maxsteps = round(max(protocol["horizons"]) / args.cadence)
    for prep in protocol["preparations"]:
        present = PresentSpec(
            "R1." + prep["id"],
            tuple((tuple(s), w) for s, w in prep["roots"]),
            conditioning=prep["conditioning"],
            sufficiency="Full fixed-slot state with all rule/energy/boundary dependencies",
        )
        law = LawSpec(
            args.law,
            model.fingerprint(),
            {
                "beta": model.beta,
                "source_enabled": law_record["driven"],
                "unresolved": "Bath/source histories; no cancellation claimed",
            },
            conserved=("fixed constituent slots", "one carrier"),
        )
        obs = ObservationSpec("R1.whole", names, conditioning=present.conditioning)
        qty = QuantitySpec(
            "history.full_given_present",
            "Full sampled history, averaged over known roots when specified",
            "bits",
            present.conditioning,
        )
        mu = np.zeros(n)
        for state, w in present.roots:
            mu[compiled.index[state]] += w
        t = perf_counter()
        profile = history_profile(p, mu, maxsteps)
        share_profile = cumulative_sampled_rewards(p, mu, parts, maxsteps)
        # Binary powering gives a separate finite-history accumulation check.
        lifted = np.zeros((n + 1, n + 1))
        lifted[:n, :n] = p
        lifted[:n, n] = parts.sum(axis=1)
        lifted[n, n] = 1
        asymptotic = irreducible_asymptotics(compiled, args.cadence, mu)
        history_seconds = perf_counter() - t
        for T in protocol["horizons"]:
            t = perf_counter()
            steps = round(T / args.cadence)
            cmp = ComparisonSpec(
                "R1.query",
                "single_query",
                T,
                args.cadence,
                {"law": args.law, "preparation": prep["id"]},
            )
            query = evaluate_history(compiled, present, law, obs, cmp, qty)
            independent_ell = float(mu @ np.linalg.matrix_power(lifted, steps)[:n, n])
            accumulation_residual = abs(query["ell_bits"] - independent_ell)
            share_residual = abs(float(share_profile[steps].sum()) - query["ell_bits"])
            if (
                max(
                    accumulation_residual,
                    share_residual,
                    abs(query["ell_bits"] - profile[steps]),
                )
                > protocol["numerical"]["independent_history_tolerance"]
            ):
                raise ArithmeticError(
                    "Independent history/coordinate-share accumulation check failed"
                )
            endpoint, occupation = distributions_and_occupation(compiled, mu, T)
            dense = operators[T]
            propagation_residual = max(
                float(np.max(abs(endpoint - mu @ dense[:n, :n]))),
                float(np.max(abs(occupation - mu @ dense[:n, n:]))),
            )
            if propagation_residual > 1e-8:
                raise ArithmeticError("Independent continuous propagation check failed")
            physical = balance(compiled, mu, endpoint, occupation)
            conditional_f0 = conditional_ft = 0.0
            for state, w in present.roots:
                i = compiled.index[state]
                point = np.zeros(n)
                point[i] = 1.0
                conditional_f0 += w * (
                    free_energy(point, energies, log_g, model.beta)[0] - f_eq
                )
                conditional_ft += w * (
                    free_energy(dense[i, :n], energies, log_g, model.beta)[0] - f_eq
                )
            physical["ensemble_availability_scope"] = (
                "Distribution-level free energy, including preparation uncertainty"
            )
            physical["known_root_average_availability_initial"] = conditional_f0
            physical["known_root_average_availability_final"] = conditional_ft
            # Signed ledger entries distinguish accepted work from returned work.
            accepted = np.zeros(n)
            returned = np.zeros(n)
            for i, _, event in compiled.ledger:
                accepted[i] += event.rate * max(event.work, 0)
                returned[i] += event.rate * max(-event.work, 0)
            physical["work_accepted_gross"] = float(occupation @ accepted)
            physical["work_returned_gross"] = float(occupation @ returned)
            witness = two_event_monitor(
                compiled,
                mu,
                T,
                protocol["monitor"]["first"],
                protocol["monitor"]["second"],
            )
            monitor_residual = float(
                np.max(abs(witness.pop("physical_marginal") - endpoint))
            )
            if monitor_residual > 1e-9:
                raise ArithmeticError("Monitor changed the physical marginal")
            activity = activity_coefficients(
                compiled, occupation, protocol["reference_time"]
            )
            activity["finite_cadence_remainder_bits"] = query["ell_bits"] - (
                activity["expected_jumps"]
                * np.log2(protocol["reference_time"] / args.cadence)
                + activity["finite_coefficient_bits"]
            )
            row = {
                "law": args.law,
                "preparation": prep["id"],
                "horizon": T,
                "cadence": args.cadence,
                "history": query,
                "asymptotic": asymptotic,
                "coordinate_shares_bits": dict(
                    zip(names, map(float, share_profile[steps]))
                ),
                "activity": activity,
                "physical": physical,
                "function": {
                    "bound_probability": float(endpoint @ bond),
                    "active_units": float(endpoint @ active),
                    "no_active_units_probability": float(endpoint @ inactive),
                    "stored_energy": float(endpoint @ bank),
                    "usable_carrier_probability": float(endpoint @ usable),
                    "integrated_bound_time": float(occupation @ bond),
                    "integrated_active_unit_time": float(occupation @ active),
                    "permanently_closed_states": closed,
                    "dissolution_then_rebinding": witness,
                },
                "validation": {
                    "history_accumulation_residual": accumulation_residual,
                    "share_sum_residual": share_residual,
                    "continuous_propagation_residual": propagation_residual,
                    "monitor_marginal_residual": monitor_residual,
                },
                "measurement_seconds": perf_counter() - t,
                "history_profile_seconds": history_seconds,
            }
            rows.append(row)
    result = {
        "schema": "omega.r1-case/1",
        "status": "passed",
        "law": args.law,
        "cadence": args.cadence,
        "states": n,
        "model_hash": model.fingerprint(),
        "state_order_hash": compiled.state_order_hash,
        "generator_hash": compiled.generator_hash,
        "manifest_sha256": sha256(manifest_path.read_bytes()).hexdigest(),
        "equilibrium_audit": eq_audit,
        "kernel_residual": kernel_residual,
        "full_positive_sampled_support": bool(support.all()),
        "setup_seconds": setup_seconds,
        "worker_seconds": perf_counter() - started,
        "dependencies": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "rows": rows,
        "scope": protocol["scope"],
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "RESULT.json").write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "law": args.law,
                "cadence": args.cadence,
                "states": n,
                "rows": len(rows),
                "worker_seconds": result["worker_seconds"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
