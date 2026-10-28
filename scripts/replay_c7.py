"""One fixed historical C.7 pair, with independent accounting and numerics."""

import argparse
import json
import math
import shutil
import sys
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "docs/research_notes/lushness_testbed/compounding/matched_throughput"
ARMS = ("loop", "basal")
HORIZONS = (16, 64, 256, 1024)
CADENCES = (0.125, 0.25, 0.5)
SEED = (6, 1, 1)
TOLERANCES = {
    "bits": 1e-5,
    "rate_work": 1e-8,
    "residual": 1e-8,
    "uniformization_tail": 1e-15,
}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    Path(path).write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def fingerprint(value):
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode()
    ).hexdigest()


def verify_original_bundle(root, expected_input=None):
    root = Path(root).resolve()
    m = read(root / "manifest.json")
    unsigned = {k: v for k, v in m.items() if k != "input_hash"}
    if (
        m["schema_version"] != "omega-frozen-bundle/1"
        or fingerprint(unsigned) != m["input_hash"]
        or fingerprint(m["sources"]) != m["source_hash"]
        or expected_input is not None
        and expected_input != m["input_hash"]
    ):
        raise ValueError("Historical manifest identity failed")
    seen = set()
    source = (root / "source").resolve()
    for r in m["sources"]:
        path = (source / r["path"]).resolve()
        if r["path"] in seen or not path.is_relative_to(source) or not path.is_file():
            raise ValueError("Invalid historical source path")
        seen.add(r["path"])
        raw = path.read_bytes()
        if len(raw) != r["bytes"] or sha256(raw).hexdigest() != r["sha256"]:
            raise ValueError("Historical source bytes failed: " + r["path"])
    return m


def check_pair(left, right):
    """A declared unequal-source contrast, not an identical-boundary certificate."""
    if left["mechanism"] != "loop" or right["mechanism"] != "basal":
        raise ValueError("Fixed loop/basal mechanisms required")
    lp, rp = left["parameters"], right["parameters"]
    if (
        lp["capacity"] != 4
        or left["target_number"] != 2
        or right["target_number"] != 2
        or left["target"] != right["target"]
    ):
        raise ValueError("Fixed capacity-4 midpoint required")
    if {k: v for k, v in lp.items() if k != "supply_rate"} != {
        k: v for k, v in rp.items() if k != "supply_rate"
    }:
        raise ValueError("Unexpected physical parameter difference")
    return {
        "kind": "historical_stationary_throughput_matched_mechanism",
        "common_seed": list(SEED),
        "same_initial_endowment": True,
        "source_arrival_rates": {"loop": lp["supply_rate"], "basal": rp["supply_rate"]},
        "identical_boundaries": lp["supply_rate"] == rp["supply_rate"],
        "current_identical_boundary_certificate": "inapplicable",
        "unmatched": [
            "offered work",
            "finite cumulative accepted work",
            "event activity",
            "bath imports",
        ],
        "horizons": list(HORIZONS),
        "cadences": list(CADENCES),
    }


def declared_heat(increments):
    outward = (
        "unused_packet_energy",
        "conversion_loss",
        "overflow_energy",
        "construction_dissipation",
        "thermal_hardware_release",
        "damage_release",
        "starvation_release",
        "upkeep_bank_debit",
        "leak_bank_debit",
    )
    inward = (
        "reverse_bath_import",
        "thermal_hardware_import",
        "starvation_bath_import",
        "upkeep_bath_import",
        "leak_bath_import",
    )
    return sum(increments.get(k, 0) for k in outward) - sum(
        increments.get(k, 0) for k in inward
    )


def event_bank_change(increments):
    return sum(
        increments.get(k, 0)
        for k in (
            "captured_energy",
            "reverse_bank_return",
            "upkeep_bath_import",
            "leak_bath_import",
        )
    ) - sum(
        increments.get(k, 0)
        for k in ("construction_bank_debit", "upkeep_bank_debit", "leak_bank_debit")
    )


def audit_events(compiled, parameters):
    import numpy as np

    states, world = compiled["states"], compiled["world"]
    n = len(states)
    q, heat, work, withdrawal, refund = (
        np.zeros((n, n)),
        np.zeros(n),
        np.zeros(n),
        np.zeros(n),
        np.zeros(n),
    )
    families, records, max_heat, max_bank = {}, [], 0.0, 0.0
    channels = {}
    for i, state in enumerate(states):
        for module in sorted(world.modules, key=lambda m: m.id):
            for e in module.events(state):
                j = compiled["index"][e.target]
                if i == j or e.rate <= 0 or not math.isfinite(e.rate):
                    raise ValueError("Invalid physical event")
                if (
                    state[2] + parameters.capacity - state[2] != parameters.capacity
                    or not 0 <= e.target[2] <= parameters.capacity
                ):
                    raise ValueError("Apparatus/derived precursor inventory failed")
                delta = world.energy(e.target) - world.energy(state)
                actual_bank = parameters.quantum * (e.target[0] - state[0])
                h = declared_heat(e.increments)
                max_heat = max(max_heat, abs(e.work - delta - h))
                max_bank = max(
                    max_bank, abs(actual_bank - event_bank_change(e.increments))
                )
                q[i, j] += e.rate
                q[i, i] -= e.rate
                heat[i] += e.rate * h
                work[i] += e.rate * e.work
                withdrawal[i] += e.rate * max(-actual_bank, 0)
                refund[i] += e.rate * (e.increments.get("reverse_bank_return", 0))
                families.setdefault(e.family, np.zeros(n))[i] += e.rate
                channels[i, j, e.family] = e.rate
                records.append(
                    {
                        "source": i,
                        "target": j,
                        "family": e.family,
                        "rate": e.rate,
                        "work": e.work,
                        "declared_heat": h,
                        "delta_energy": delta,
                        "bank_change": actual_bank,
                        "increments": dict(e.increments),
                    }
                )
    rate_ratio_residual = 0.0
    pairs_checked = 0
    for (i, j, family), rate in channels.items():
        if family not in (
            "paid_build",
            "thermal_build",
            "bank_leak",
            "hardware_upkeep",
            "starvation_reconstruction",
        ):
            continue
        reverse = {
            "paid_build": "reverse_build",
            "thermal_build": "thermal_break",
            "bank_leak": "leak_reverse",
            "hardware_upkeep": "upkeep_reverse",
            "starvation_reconstruction": "starvation_damage",
        }[family]
        if (j, i, reverse) not in channels:
            raise ValueError("Missing native reverse for declared paired channel")
        factor = (
            (parameters.capacity - states[i][2]) / states[j][2]
            if family in ("paid_build", "thermal_build", "starvation_reconstruction")
            else 1.0
        )
        expected_log = math.log(factor) - parameters.beta * (
            world.energy(states[j]) - world.energy(states[i])
        )
        actual_log = math.log(rate / channels[j, i, reverse])
        rate_ratio_residual = max(rate_ratio_residual, abs(actual_log - expected_log))
        pairs_checked += 1
    residuals = {
        "generator_reconstruction": float(np.max(abs(q - compiled["Q"].toarray()))),
        "event_declared_heat": max_heat,
        "event_declared_bank": max_bank,
        "compiled_heat_flow": float(np.max(abs(heat - compiled["flows"]["bath_heat"]))),
        "compiled_work_flow": float(
            np.max(abs(work - compiled["flows"]["resource_work"]))
        ),
        "paired_local_rate_ratio_log": rate_ratio_residual,
    }
    if max(residuals.values()) > TOLERANCES["residual"]:
        raise ArithmeticError(
            "Physical event accounting failed: " + json.dumps(residuals)
        )
    return {
        "residuals": residuals,
        "native_pairs_checked": pairs_checked,
        "material_scope": "Apparatus plus derived precursor only; full carrier/waste chemistry unresolved",
        "unpaired_boundary_channels": [
            "packet_inflow",
            "packet_decay",
            "basal_capture",
            "assisted_capture",
            "external_damage",
        ],
    }, {
        "q": q,
        "heat": heat,
        "work": work,
        "withdrawal": withdrawal,
        "construction_refund": refund,
        "families": families,
        "records": records,
    }


def uniformized_kernel(q, dt):
    import numpy as np
    from scipy.stats import poisson

    rate = float(max(-q.diagonal()))
    n = len(q)
    transition = np.eye(n) + q / rate
    mean = rate * dt
    term = np.eye(n)
    result = math.exp(-mean) * term
    count = 0
    weight = math.exp(-mean)
    while poisson.sf(count, mean) > TOLERANCES["uniformization_tail"]:
        count += 1
        term = term @ transition
        weight *= mean / count
        result += weight * term
        if count > 10000:
            raise ArithmeticError("Uniformization series cap reached")
    return result, float(poisson.sf(count, mean))


def worker(out):
    if sys.stdin.readline().strip() != "GO":
        raise SystemExit("Capped worker handshake required")
    for row in read(out / "frozen/MANIFEST.json")["files"]:
        if sha256((out / "frozen" / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            raise ValueError("Replay audit source hash failed")
    import numpy as np
    from scipy.linalg import expm, solve
    from scipy.special import xlogy

    verify_original_bundle(out / "legacy/loop")
    verify_original_bundle(out / "legacy/basal")
    sys.path.insert(0, str(out / "legacy/loop/source"))
    from omega_v2.testbed.analysis.finite_classes import analyze
    from omega_v2.testbed.analysis.renewal_profile import SampledHorizons
    from omega_v2.testbed.compiler import compile_world
    from omega_v2.testbed.compounding import CompoundingParameters, build_world

    results = {}
    (out / "output").mkdir()
    for arm in ARMS:
        manifest = read(out / "legacy" / arm / "manifest.json")
        original = read(out / "legacy" / arm / "RESULTS.json")
        law = manifest["config"]["law"]
        params = CompoundingParameters(**law["parameters"])
        compiled = compile_world(build_world(params, arm))
        audit, native = audit_events(compiled, params)
        write(out / "output" / (arm + "-events.json"), native["records"])
        q = native["q"]
        n = len(q)
        initial = np.zeros(n)
        initial[compiled["index"][SEED]] = 1
        constraint = q.T.copy()
        constraint[-1] = 1
        rhs = np.zeros(n)
        rhs[-1] = 1
        pi = solve(constraint, rhs)
        if min(pi) < -1e-12:
            raise ArithmeticError("Invalid stationary distribution")
        audit["residuals"]["stationarity"] = float(np.max(abs(pi @ q)))
        finite_physics = {}
        # Continuous physical integrals are independent of the sampled cadence.
        augmented = np.block([[q, np.eye(n)], [np.zeros((n, n)), np.zeros((n, n))]])
        for horizon in HORIZONS:
            evolution = expm(augmented * horizon)
            final = initial @ evolution[:n, :n]
            occupation = initial @ evolution[:n, n:]
            check = max(
                float(np.max(abs(occupation @ q - final + initial))),
                abs(float(occupation.sum()) - horizon),
                abs(float(final.sum()) - 1),
            )
            if check > TOLERANCES["residual"]:
                raise ArithmeticError("Continuous propagation identity failed")
            physical = {
                "expected_jumps": float(occupation @ -q.diagonal()),
                "accepted_work": float(occupation @ native["work"]),
                "heat_out": float(occupation @ native["heat"]),
                "energy_change": float((final - initial) @ compiled["energy"]),
                "gross_bank_withdrawal": float(occupation @ native["withdrawal"]),
                "construction_refund": float(
                    occupation @ native["construction_refund"]
                ),
                "apparatus_deadline": float(
                    final @ compiled["observables"]["apparatus"]
                ),
                "integral_residual": check,
                "event_counts": {
                    k: float(occupation @ v) for k, v in native["families"].items()
                },
            }
            previous = original["physical"][arm + ":seed"][str(horizon)]
            physical["retained_work_difference"] = (
                physical["accepted_work"] - previous["resource_work"]
            )
            physical["first_law_residual"] = (
                physical["accepted_work"]
                - physical["heat_out"]
                - physical["energy_change"]
            )
            finite_physics[str(horizon)] = physical
        rows = []
        max_bits_difference = max_independent = max_rate_difference = 0.0
        for dt in CADENCES:
            legacy = analyze(compiled["Q"], dt)
            kernel, tail = uniformized_kernel(q, dt)
            kernel_residual = float(np.max(abs(kernel - legacy["P"])))
            g = -np.sum(xlogy(kernel, kernel), axis=1) / math.log(2)
            cache = SampledHorizons(legacy["P"], round(max(HORIZONS) / dt))
            rate = float(pi @ g / dt)
            retained = next(
                r
                for r in original["rows"]
                if r["root"] == "seed" and r["cadence"] == dt
            )
            max_rate_difference = max(max_rate_difference, abs(rate - retained["rate"]))
            matrix = np.block(
                [[kernel, g[:, None]], [np.zeros((1, n)), np.ones((1, 1))]]
            )
            for horizon in HORIZONS:
                count = round(horizon / dt)
                independent_bits = float(
                    initial @ np.linalg.matrix_power(matrix, count)[:n, n]
                )
                weights, _ = cache.occupation(compiled["index"][SEED], count)
                bits = float(weights @ legacy["row_entropy"])
                old_bits = retained["scores"][str(horizon)]["bits"]
                delta = bits - old_bits
                check = independent_bits - bits
                max_bits_difference = max(max_bits_difference, abs(delta))
                max_independent = max(max_independent, abs(check))
                rows.append(
                    {
                        "cadence": dt,
                        "horizon": horizon,
                        "history_bits": bits,
                        "retained_history_bits": old_bits,
                        "retained_difference": delta,
                        "independent_history_difference": check,
                        "stationary_rate": rate,
                        "retained_rate_difference": rate - retained["rate"],
                        "kernel_residual": kernel_residual,
                        "uniformization_tail": tail,
                    }
                )
        work_rate = float(pi @ native["work"])
        checks = {
            "history_reproduction": max_bits_difference <= TOLERANCES["bits"],
            "independent_history": max_independent <= TOLERANCES["bits"],
            "stationary_rate_reproduction": max_rate_difference
            <= TOLERANCES["rate_work"],
            "stationary_work_target": abs(work_rate - law["target"])
            <= TOLERANCES["rate_work"],
            "finite_work_reproduction": max(
                abs(v["retained_work_difference"]) for v in finite_physics.values()
            )
            <= TOLERANCES["residual"],
            "first_law": max(
                abs(v["first_law_residual"]) for v in finite_physics.values()
            )
            <= TOLERANCES["residual"],
            "sampled_kernel": max(r["kernel_residual"] for r in rows)
            <= TOLERANCES["residual"],
        }
        result = {
            "status": "reproduced" if all(checks.values()) else "discrepant",
            "checks": checks,
            "states": n,
            "seed_energy": compiled["world"].energy(SEED),
            "parameters": law["parameters"],
            "physical_audit": audit,
            "stationary_accepted_work": work_rate,
            "target": law["target"],
            "finite_physics": finite_physics,
            "rows": rows,
        }
        write(out / "output" / (arm + ".json"), result)
        results[arm] = result
        print(
            json.dumps({"arm": arm, "status": result["status"], "checks": checks}),
            flush=True,
        )
    loaded = {
        name: str(
            Path(module.__file__).resolve().relative_to(out / "legacy/loop/source")
        )
        for name, module in sys.modules.items()
        if name.startswith("omega_v2") and getattr(module, "__file__", None)
    }
    comparison = check_pair(
        read(out / "legacy/loop/manifest.json")["config"]["law"],
        read(out / "legacy/basal/manifest.json")["config"]["law"],
    )
    comparison["profiles"] = [
        {
            "horizon": l["horizon"],
            "cadence": l["cadence"],
            "delta_history_bits": l["history_bits"] - r["history_bits"],
            "delta_rate": l["stationary_rate"] - r["stationary_rate"],
        }
        for l, r in zip(results["loop"]["rows"], results["basal"]["rows"], strict=True)
    ]
    comparison["stationary_work_mismatch"] = (
        results["loop"]["stationary_accepted_work"]
        - results["basal"]["stationary_accepted_work"]
    )
    write(
        out / "output/RESULT.json",
        {
            "status": "completed",
            "arms": {k: v["status"] for k, v in results.items()},
            "comparison": comparison,
            "frozen_legacy_imports": loaded,
            "tolerances": TOLERANCES,
        },
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legacy-root", type=Path, default=ROOT.parent / "Omega")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--worker", type=Path)
    args = parser.parse_args()
    if args.worker:
        worker(args.worker.resolve())
        return
    if args.out is None:
        parser.error("Fresh --out required")
    out = args.out.resolve()
    if out.exists() or not out.is_relative_to(ROOT / "runs"):
        parser.error("Fresh ignored runs/ directory required")
    legacy_root = args.legacy_root.resolve()
    doc = legacy_root / BASE
    status = read(doc / "SCIENCE_STATUS.json")
    out.mkdir(parents=True)
    verified = {}
    laws = {}
    for arm in ARMS:
        entry = status["laws"]["M4-target2-" + arm]
        original = Path(entry["run"]).resolve()
        if not original.is_relative_to(legacy_root):
            raise ValueError("Historical source run outside declared legacy root")
        m = verify_original_bundle(original, entry["input_hash"])
        old_result = read(original / "RESULTS.json")
        if (
            old_result != read(doc / "laws" / ("M4-target2-" + arm + ".json"))
            or old_result["input_hash"] != m["input_hash"]
            or old_result["source_hash"] != m["source_hash"]
        ):
            raise ValueError("Historical result provenance failed")
        protocol = m["config"]["protocol"]
        if (
            tuple(sorted(protocol["cadences"])) != CADENCES
            or tuple(protocol["horizons"]) != HORIZONS
            or tuple(protocol["roots"]["seed"]) != SEED
        ):
            raise ValueError("Historical query mismatch")
        target = out / "legacy" / arm
        target.mkdir(parents=True)
        shutil.copytree(original / "source", target / "source")
        shutil.copyfile(original / "manifest.json", target / "manifest.json")
        shutil.copyfile(original / "RESULTS.json", target / "RESULTS.json")
        laws[arm] = m["config"]["law"]
        verified[arm] = {
            "input_hash": m["input_hash"],
            "source_hash": m["source_hash"],
            "source_files": len(m["sources"]),
            "sources_verified": True,
            "result_sha256": sha256(
                (original / "RESULTS.json").read_bytes()
            ).hexdigest(),
        }
    if verified["loop"]["source_hash"] != verified["basal"]["source_hash"]:
        raise ValueError("Historical arms use different frozen source")
    comparison = check_pair(laws["loop"], laws["basal"])
    write(
        out / "PROVENANCE.json",
        {
            "status": "verified",
            "arms": verified,
            "comparison": comparison,
            "tolerances": TOLERANCES,
        },
    )
    frozen = out / "frozen"
    for relative in (
        "scripts/replay_c7.py",
        "src/omega_cosmology/testbed/workflow.py",
        "research/platform/specs/C7_VERIFICATION_REPLAY_r1.md",
        "tests/test_c7_replay.py",
    ):
        target = frozen / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    write(
        frozen / "MANIFEST.json",
        {
            "files": [
                {
                    "path": p.relative_to(frozen).as_posix(),
                    "sha256": sha256(p.read_bytes()).hexdigest(),
                }
                for p in sorted(frozen.rglob("*"))
                if p.is_file()
            ]
        },
    )
    sys.path.insert(0, str(ROOT / "src"))
    from omega_cosmology.testbed.workflow import capped

    receipt = capped(
        [
            sys.executable,
            "-B",
            str(frozen / "scripts/replay_c7.py"),
            "--worker",
            str(out),
        ],
        out,
        seconds=240,
        memory=512 * 1024**2,
        output_cap=32 * 1024**2,
        cwd=frozen,
    )
    write(out / "RECEIPT.json", receipt)
    print(json.dumps(receipt))
    if receipt["exit_code"] or receipt["cap_reason"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
