"""Trusted worker: wait for Job Object assignment before heavy imports."""

import sys

if __name__ == "__main__" and sys.stdin.readline().strip() != "GO":
    raise SystemExit("Runner GO gate required")


def main():
    import argparse
    import json
    import platform
    from hashlib import sha256
    from pathlib import Path
    from time import perf_counter, sleep

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cap-probe", choices=("wall", "memory"))
    parser.add_argument("--out-dir", type=Path)
    args = parser.parse_args()
    if args.cap_probe == "wall":
        sleep(30)
        return 1
    if args.cap_probe == "memory":
        chunks = []
        try:
            for _ in range(16):
                chunks.append(bytearray(8 * 1024**2))
        except MemoryError:
            print(
                json.dumps(
                    {
                        "probe": "memory_refusal",
                        "payload_bytes_retained": len(chunks) * 8 * 1024**2,
                        "note": "Windows peak job counter can include a refused allocation attempt; not RSS",
                    }
                )
            )
            return 86
        return 1
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "src"))
    started = perf_counter()
    manifest_path = root / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for row in manifest["files"]:
        if sha256((root / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            raise RuntimeError("Frozen input changed: " + row["path"])
    import numpy as np
    import scipy
    from scipy.linalg import expm

    from omega_cosmology.testbed.backends import enumerate_model, trajectory
    from omega_cosmology.testbed.conformance import run_reference_cases
    from omega_cosmology.testbed.history import (
        distributions_and_occupation,
        entropy,
        evaluate_history,
        history_profile,
        irreducible_asymptotics,
        observed_history_law,
        sampled_kernel,
        sampled_support,
    )
    from omega_cosmology.testbed.physics import LocalModel
    from omega_cosmology.testbed.semantics import (
        ComparisonSpec,
        EvidenceSpec,
        LawSpec,
        ObservationSpec,
        PresentSpec,
        QuantitySpec,
    )
    from omega_cosmology.testbed.thermodynamics import (
        audit_equilibrium,
        balance,
        flow_rewards,
    )

    imports_seconds = perf_counter() - started
    results = []
    for fixture in sorted((root / "research/platform/models").glob("R[012].json")):
        case = json.loads(fixture.read_text(encoding="utf-8"))
        model = LocalModel.from_record(case["model"])
        present = PresentSpec(**case["present"])
        law = LawSpec(**case["law"])
        observation = ObservationSpec(**case["observation"])
        comparison = ComparisonSpec(**case["comparison"])
        quantity = QuantitySpec(**case["quantity"])
        EvidenceSpec(**case["evidence"])
        times = {}
        t = perf_counter()
        for state, _ in present.roots:
            for _ in range(50):
                list(model.events(state))
        times["rule_matching_50_root_calls"] = perf_counter() - t
        t = perf_counter()
        for state, _ in present.roots:
            for _ in range(50):
                model.canonical(state)
        times["canonicalization_50_root_calls"] = perf_counter() - t
        t = perf_counter()
        compiled = enumerate_model(
            model, [s for s, _ in present.roots], max_states=1000
        )
        compiled.require_complete()
        times["enumeration_including_symmetry_checks"] = perf_counter() - t
        t = perf_counter()
        equilibrium = audit_equilibrium(compiled)
        times["source_off_audit"] = perf_counter() - t
        t = perf_counter()
        p = sampled_kernel(compiled, comparison.cadence)
        support = sampled_support(compiled)
        times["sampled_kernel_and_support"] = perf_counter() - t
        mu = np.zeros(len(compiled.states))
        for state, weight in present.roots:
            mu[compiled.index[model.canonical(state)]] += weight
        t = perf_counter()
        endpoint, occupation = distributions_and_occupation(
            compiled, mu, comparison.horizon
        )
        times["continuous_propagation_and_occupation"] = perf_counter() - t
        t = perf_counter()
        profile = history_profile(p, mu, round(comparison.horizon / comparison.cadence))
        query = evaluate_history(
            compiled, present, law, observation, comparison, quantity
        )
        # Independent direct word sum for two sampled steps, with no Markov projection assumption.
        word_law = observed_history_law(p, mu, list(range(len(p))), 2, max_words=100000)
        chain_residual = float(abs(entropy(list(word_law.values())) - profile[2]))
        if chain_residual > 1e-10 or abs(query["ell_bits"] - profile[-1]) > 1e-10:
            raise ArithmeticError("History-query audit failed")
        times["history_queries_and_direct_word_audit"] = perf_counter() - t
        t = perf_counter()
        physical = balance(compiled, mu, endpoint, occupation)
        n = len(p)
        # Independent dense block exponential for occupation and endpoint.
        augmented = np.zeros((n + 1, n + 1))
        augmented[:n, :n] = compiled.q.toarray()
        augmented[n, :n] = mu
        independent = expm(augmented * comparison.horizon)
        occupation_residual = float(np.max(abs(independent[n, :n] - occupation)))
        endpoint_residual = float(np.max(abs(mu @ independent[:n, :n] - endpoint)))
        if max(occupation_residual, endpoint_residual) > 1e-9:
            raise ArithmeticError("Independent propagation audit failed")
        asymptotic = irreducible_asymptotics(compiled, comparison.cadence, mu)
        times["physics_and_asymptotic_audits"] = perf_counter() - t
        t = perf_counter()
        rng = np.random.default_rng(1704)
        sample_count, sample_horizon = 1000, 2.0
        counts = np.zeros(n)
        jump_counts = []
        for _ in range(sample_count):
            path = trajectory(model, present.roots[0][0], sample_horizon, rng)
            if not path["complete"]:
                raise ArithmeticError("Calibration sampler event cap")
            counts[compiled.index[path["endpoint"]]] += 1
            jump_counts.append(path["jumps"])
            delta = float(
                model.energy(path["endpoint"]) - model.energy(present.roots[0][0])
            )
            if abs(delta - path["work"] + path["heat"]) > 1e-10:
                raise ArithmeticError("Sample trajectory energy balance failed")
        exact_endpoint, short_occupation = distributions_and_occupation(
            compiled, mu, sample_horizon
        )
        envelope = (
            6 * np.sqrt(exact_endpoint * (1 - exact_endpoint) / sample_count)
            + 6 / sample_count
        )
        endpoint_ratio = float(
            np.max(abs(counts / sample_count - exact_endpoint) / envelope)
        )
        exact_jumps = float(short_occupation @ flow_rewards(compiled)[2])
        jump_mean = float(np.mean(jump_counts))
        jump_envelope = (
            6 * float(np.std(jump_counts, ddof=1)) / np.sqrt(sample_count)
            + 6 / sample_count
        )
        if endpoint_ratio > 1 or abs(jump_mean - exact_jumps) > jump_envelope:
            raise ArithmeticError("Sample/exact agreement failed calibration envelope")
        times["sampler_1000_paths"] = perf_counter() - t
        results.append(
            {
                "id": case["id"],
                "model_hash": model.fingerprint(),
                "states": n,
                "directed_mechanism_events": len(compiled.ledger),
                "nonzero_generator_entries": compiled.q.nnz,
                "enumeration_complete": True,
                "full_positive_sampled_support": bool(support.all()),
                "query": query,
                "equilibrium": equilibrium,
                "thermodynamics": physical,
                "asymptotic_diagnostic": asymptotic,
                "chain_rule_residual": chain_residual,
                "independent_occupation_residual": occupation_residual,
                "independent_endpoint_residual": endpoint_residual,
                "sampler": {
                    "paths": sample_count,
                    "horizon": sample_horizon,
                    "seed": 1704,
                    "endpoint_six_sigma_envelope_max_fraction": endpoint_ratio,
                    "exact_expected_jumps": exact_jumps,
                    "sample_mean_jumps": jump_mean,
                    "jump_mean_envelope": jump_envelope,
                    "guarantee": "statistical calibration only; no sampled entropy estimate",
                },
                "timings_seconds": times,
            }
        )
    if len(results) != 3:
        raise RuntimeError("Expected the three frozen engineering models")
    conformance = run_reference_cases()
    summary = {
        "status": "passed",
        "schema": "omega.engineering-calibration/1",
        "manifest_sha256": sha256(manifest_path.read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "imports_seconds": imports_seconds,
        "worker_seconds": perf_counter() - started,
        "models": results,
        "reference_cases": conformance,
        "scope": "M0–M2 engineering only; finite classical physics, not an ethical or generativity result",
        "limitations": [
            "Boundary histories unresolved",
            "Physical faithfulness open",
            "Finite fixed material slots",
            "Projected word queries have an explicit exponential word cap",
            "Reducible-chain asymptotic rates not implemented",
            "No r20 conformance claimed",
        ],
    }
    (args.out_dir / "SUMMARY.json").write_text(
        json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": summary["status"],
                "worker_seconds": summary["worker_seconds"],
                "models": [{"id": x["id"], "states": x["states"]} for x in results],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
