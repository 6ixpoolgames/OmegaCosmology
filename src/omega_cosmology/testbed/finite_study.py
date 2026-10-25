"""Shared small exact assay, driven by model/query/readout data, not study names."""

from time import perf_counter

import numpy as np
from scipy.linalg import expm
from scipy.sparse.linalg import expm_multiply

from .ancestry import compile_ancestry_query, evaluate_ancestry_query
from .backends import enumerate_model
from .ecology import compile_functional_query, evaluate_functional_query
from .history import (
    distributions_and_occupation,
    evaluate_history,
    history_profile,
    irreducible_asymptotics,
    sampled_kernel,
    sampled_support,
)
from .monitors import compile_monitor, evaluate_monitor, event_rewards, state_value
from .physics import LocalModel
from .projections import projected_history_profiles
from .readouts import (
    activity_coefficients,
    coordinate_entropy_rewards,
    cumulative_sampled_rewards,
)
from .semantics import (
    ComparisonSpec,
    LawSpec,
    ObservationSpec,
    PresentSpec,
    QuantitySpec,
)
from .structure import paired_state_probe, transition_audit
from .thermodynamics import audit_equilibrium, balance, equilibrium, free_energy


def evaluate_case(protocol, law_record, cadence):
    started = perf_counter()
    model = LocalModel.from_record(law_record["model"])
    roots = [tuple(s) for prep in protocol["preparations"] for s, _ in prep["roots"]]
    for s in roots:
        model.validate(s)
        if str(model.energy(s)) != protocol["energy_per_root"]:
            raise ValueError("Preparation energy mismatch")
    compiled = enumerate_model(
        model, roots, max_states=protocol.get("max_states", 1000)
    )
    compiled.require_complete()
    analysis_spec = law_record.get(
        "structural_analysis", protocol.get("structural_analysis", {})
    )
    functional_queries = [
        compile_functional_query(compiled, spec)
        for spec in analysis_spec.get("organizations", ())
    ]
    if len({q["id"] for q in functional_queries}) != len(functional_queries):
        raise ValueError("Distinct organization query IDs required")
    structure_audit = {
        "transition_audits": [
            transition_audit(compiled, spec)
            for spec in analysis_spec.get("transition_audits", ())
        ],
        "paired_state_probes": [
            paired_state_probe(compiled, spec)
            for spec in analysis_spec.get("paired_state_probes", ())
        ],
        "scope": "Structural opportunity diagnostics; no causal ancestry inferred",
    }
    n = len(compiled.states)
    names = tuple(c.name for c in model.coordinates)
    if list(names) != protocol["coordinate_order"]:
        raise ValueError("Declared coordinate order mismatch")
    eq_audit = audit_equilibrium(compiled)
    support = sampled_support(compiled)
    dense_cap = protocol.get("max_dense_bytes", 32 * 1024**2)
    p = sampled_kernel(compiled, cadence, max_dense_bytes=dense_cap)
    projection_specs = protocol.get("projected_histories", ())
    if len({s["id"] for s in projection_specs}) != len(projection_specs):
        raise ValueError("Distinct projected-history query IDs required")
    for spec in projection_specs:
        fields = spec["coordinates"]
        if (
            not fields
            or len(set(fields)) != len(fields)
            or any(field not in model.indices for field in fields)
        ):
            raise ValueError("Projection must name distinct physical coordinates")
        if spec.get("conditioning", "full_present") != "full_present":
            raise ValueError(
                "This assay projection path currently requires a known full present"
            )
        if len(model.symmetry) > 1:
            for state in compiled.states:
                labels = {
                    tuple(s[model.indices[k]] for k in fields)
                    for s in model.orbit(state)
                }
                if len(labels) > 1:
                    raise ValueError(
                        "Projection distinguishes unmarked representatives"
                    )
    kernel_residual = float(
        np.max(abs(p - expm_multiply(compiled.q * cadence, np.eye(n))))
    )
    if kernel_residual > protocol["numerical"]["kernel_agreement_tolerance"]:
        raise ArithmeticError("Independent sampled kernel mismatch")
    shares = coordinate_entropy_rewards(p, compiled.states, tuple(range(len(names))))
    observables = {
        d["id"]: np.array([state_value(model, s, d) for s in compiled.states])
        for d in protocol["observables"]
    }
    for descriptor in protocol["observables"]:
        for state in compiled.states:
            values = [state_value(model, s, descriptor) for s in model.orbit(state)]
            if max(values) - min(values) > 1e-12:
                raise ValueError(
                    "A passive observable distinguishes unmarked representatives"
                )
    rewards = event_rewards(compiled, protocol["event_readouts"])
    monitors = [
        compile_monitor(compiled, spec) for spec in protocol.get("monitors", ())
    ]
    pi_eq, energies, log_g = equilibrium(compiled)
    feq, _ = free_energy(pi_eq, energies, log_g, model.beta)
    # Stationary physical readouts are computed from Q, independently of the
    # sampled Poisson-equation rate helper. This helper assumes irreducibility.
    system = compiled.q.T.toarray()
    system[-1] = 1.0
    rhs = np.zeros(n)
    rhs[-1] = 1.0
    stationary = np.linalg.solve(system, rhs)
    stationary_residual = float(np.max(abs(compiled.q.T @ stationary)))
    if stationary.min() < -1e-12 or stationary_residual > 1e-10:
        raise ArithmeticError("Stationary physical readout failed")
    # Include retained operators plus conservative exponential workspace.
    occupation_cap = protocol.get("max_occupation_dense_bytes", 512 * 1024**2)
    if 8 * (2 * n) ** 2 * (4 + len(protocol["horizons"])) > occupation_cap:
        raise MemoryError(
            "Continuous occupation reference exceeds declared dense workspace"
        )
    block = np.zeros((2 * n, 2 * n))
    block[:n, :n] = compiled.q.toarray()
    block[:n, n:] = np.eye(n)
    operators = {T: expm(block * T) for T in protocol["horizons"]}
    setup_seconds = perf_counter() - started
    rows = []
    for prep in protocol["preparations"]:
        t0 = perf_counter()
        present = PresentSpec(
            protocol["id"] + "." + prep["id"],
            tuple((tuple(s), w) for s, w in prep["roots"]),
            conditioning=prep["conditioning"],
            sufficiency=protocol["sufficiency"],
        )
        if projection_specs and present.conditioning != "full_present":
            raise ValueError(
                "Known-root averaging and own-present projection require separate typed queries"
            )
        law = LawSpec(
            law_record["id"],
            model.fingerprint(),
            protocol["boundary_scope"],
            conserved=tuple(protocol["conserved"]),
        )
        obs = ObservationSpec("whole.modeled", names, conditioning=present.conditioning)
        qty = QuantitySpec(
            "history.full_given_present",
            "Full sampled history conditioned on the declared known root(s)",
            "bits",
            present.conditioning,
        )
        mu = np.zeros(n)
        for state, w in present.roots:
            mu[compiled.index[model.canonical(state)]] += w
        ancestry_queries = [
            compile_ancestry_query(
                compiled,
                spec,
                mu,
                max_query_states=analysis_spec.get("max_ancestry_query_states", 5000),
            )
            for spec in analysis_spec.get("ancestry", ())
        ]
        if len({q["id"] for q in ancestry_queries}) != len(ancestry_queries):
            raise ValueError("Distinct ancestry query IDs required")
        maxsteps = round(max(protocol["horizons"]) / cadence)
        local_profiles = {
            spec["id"]: projected_history_profiles(
                p,
                mu,
                [
                    tuple(state[model.indices[k]] for k in spec["coordinates"])
                    for state in compiled.states
                ],
                [round(T / cadence) for T in protocol["horizons"]],
                memory=spec.get("memory", 1),
                max_workspace_bytes=spec.get("max_workspace_bytes", 32 * 1024**2),
                max_words=spec.get("max_words", 100000),
            )
            for spec in projection_specs
        }
        profile = history_profile(p, mu, maxsteps)
        share_profile = cumulative_sampled_rewards(p, mu, shares, maxsteps)
        lifted = np.zeros((n + 1, n + 1))
        lifted[:n, :n] = p
        lifted[:n, n] = shares.sum(axis=1)
        lifted[n, n] = 1
        asymptotic = irreducible_asymptotics(
            compiled, cadence, mu, max_dense_bytes=dense_cap
        )
        history_seconds = perf_counter() - t0
        for T in protocol["horizons"]:
            t0 = perf_counter()
            steps = round(T / cadence)
            comparison = ComparisonSpec(
                protocol["id"] + ".query",
                "single_query",
                T,
                cadence,
                {"law": law_record["id"], "preparation": prep["id"]},
            )
            query = evaluate_history(
                compiled, present, law, obs, comparison, qty, max_dense_bytes=dense_cap
            )
            accumulation_residual = abs(
                query["ell_bits"]
                - float(mu @ np.linalg.matrix_power(lifted, steps)[:n, n])
            )
            share_residual = abs(share_profile[steps].sum() - query["ell_bits"])
            if (
                max(
                    accumulation_residual,
                    share_residual,
                    abs(query["ell_bits"] - profile[steps]),
                )
                > protocol["numerical"]["independent_history_tolerance"]
            ):
                raise ArithmeticError("Independent history accumulation failed")
            endpoint, occupation = distributions_and_occupation(compiled, mu, T)
            dense = operators[T]
            propagation_residual = max(
                float(np.max(abs(endpoint - mu @ dense[:n, :n]))),
                float(np.max(abs(occupation - mu @ dense[:n, n:]))),
            )
            if propagation_residual > 1e-8:
                raise ArithmeticError("Independent continuous propagation failed")
            physical = balance(compiled, mu, endpoint, occupation)
            physical["known_root_average_availability_initial"] = sum(
                w
                * (
                    free_energy(
                        np.eye(n)[compiled.index[model.canonical(s)]],
                        energies,
                        log_g,
                        model.beta,
                    )[0]
                    - feq
                )
                for s, w in present.roots
            )
            physical["known_root_average_availability_final"] = sum(
                w
                * (
                    free_energy(
                        dense[compiled.index[model.canonical(s)], :n],
                        energies,
                        log_g,
                        model.beta,
                    )[0]
                    - feq
                )
                for s, w in present.roots
            )
            accepted = np.zeros(n)
            returned = np.zeros(n)
            for i, _, event in compiled.ledger:
                accepted[i] += event.rate * max(event.work, 0)
                returned[i] += event.rate * max(-event.work, 0)
            physical["work_accepted_gross"] = float(occupation @ accepted)
            physical["work_returned_gross"] = float(occupation @ returned)
            witnesses = {}
            monitor_residual = 0.0
            for monitor in monitors:
                result = evaluate_monitor(monitor, mu, T)
                monitor_residual = max(
                    monitor_residual,
                    float(np.max(abs(result.pop("physical_marginal") - endpoint))),
                )
                witnesses[monitor["id"]] = result
            if monitor_residual > 1e-9:
                raise ArithmeticError("Monitor changed the physical marginal")
            activity = activity_coefficients(
                compiled, occupation, protocol.get("reference_time", 1.0)
            )
            rows.append(
                {
                    "law": law_record["id"],
                    "preparation": prep["id"],
                    "horizon": T,
                    "cadence": cadence,
                    "history": query,
                    "projected_histories": {
                        spec["id"]: {
                            **local_profiles[spec["id"]][steps],
                            "quantity": "history.projected_given_full_present",
                            "conditioning": "full_present",
                            "scope": list(spec["coordinates"]),
                            "cadence": cadence,
                            "horizon": T,
                            "model_hash": compiled.model_hash,
                            "generator_hash": compiled.generator_hash,
                        }
                        for spec in projection_specs
                    },
                    "asymptotic": asymptotic,
                    "horizon_diagnostics": {
                        "endpoint_total_variation_to_stationary": float(
                            np.sum(abs(endpoint - stationary)) / 2
                        ),
                        "rate_offset_profile_residual_bits": float(
                            query["ell_bits"]
                            - T * asymptotic["rate_bits_per_time"]
                            - asymptotic["offset_bits"]
                        ),
                    },
                    "physical": physical,
                    "activity": activity,
                    "coordinate_shares_bits": dict(
                        zip(names, map(float, share_profile[steps]))
                    ),
                    "observables": {
                        key: {
                            "endpoint": float(endpoint @ v),
                            "integrated": float(occupation @ v),
                            "stationary": float(stationary @ v),
                        }
                        for key, v in observables.items()
                    },
                    "event_readouts": {
                        key: float(occupation @ v) for key, v in rewards.items()
                    },
                    "witnesses": witnesses,
                    "functional_profiles": {
                        q["id"]: evaluate_functional_query(
                            q, mu, T, endpoint, occupation
                        )
                        for q in functional_queries
                    },
                    "assistance_ancestry": {
                        q["id"]: evaluate_ancestry_query(q, T, endpoint)
                        for q in ancestry_queries
                    },
                    "validation": {
                        "history_accumulation_residual": float(accumulation_residual),
                        "coordinate_share_residual": float(share_residual),
                        "continuous_propagation_residual": propagation_residual,
                        "monitor_marginal_residual": monitor_residual,
                    },
                    "measurement_seconds": perf_counter() - t0,
                    "history_profile_seconds": history_seconds,
                }
            )
    return {
        "schema": "omega.finite-study-case/1",
        "status": "passed",
        "law": law_record["id"],
        "cadence": cadence,
        "states": n,
        "model_hash": model.fingerprint(),
        "state_order_hash": compiled.state_order_hash,
        "generator_hash": compiled.generator_hash,
        "equilibrium_audit": eq_audit,
        "kernel_residual": kernel_residual,
        "stationary_residual": stationary_residual,
        "full_positive_sampled_support": bool(support.all()),
        "setup_seconds": setup_seconds,
        "worker_seconds": perf_counter() - started,
        "rows": rows,
        "structural_analysis": structure_audit,
        "scope": protocol["scope"],
    }
