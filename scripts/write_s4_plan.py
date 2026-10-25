"""Calibrate physical register moments under a cap, then materialize S4 inputs."""

import argparse
import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
FOLDER = "research/studies/S4-warning-and-obstruction"
SENSOR = "kinetic"
ENVIRONMENTS = {"blocked": None, "slow": 0.005, "fast": 0.05, "open": None}
ARMS = {
    "T0": (True, False),
    "TX": (True, True),
    "R0": (False, False),
    "RX": (False, True),
}


def write(path, value):
    path.write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def calibration_worker(out, manifest):
    if sys.stdin.readline().strip() != "GO":
        raise RuntimeError("Capped supervisor required")
    for r in json.loads(manifest.read_text())["files"]:
        if digest(ROOT / r["path"]) != r["sha256"]:
            raise RuntimeError("Calibration input changed")
    import numpy as np
    from scipy.optimize import least_squares

    from omega_cosmology.testbed.backends import enumerate_model
    from omega_cosmology.testbed.history import distributions_and_occupation
    from omega_cosmology.testbed.signals import warning_root, warning_world

    def moments(env, *, tracking, on=0.008, off=None, details=False):
        if off is None:
            off = 0.025 if SENSOR == "kinetic" else 0.008
        model = warning_world(
            tracking=tracking,
            response=False,
            barrier_conductance=ENVIRONMENTS[env],
            on_conductance=on,
            off_conductance=off,
            sensor=SENSOR,
        )
        root = warning_root(open_barrier=env == "open")
        c = enumerate_model(model, [root], max_states=300)
        c.require_complete()
        mu = np.zeros(len(c.states))
        mu[c.index[root]] = 1
        _, occ = distributions_and_occupation(c, mu, 64)
        active = np.array([s[-1] for s in c.states])
        switches = np.zeros(len(c.states))
        for i, j, e in c.ledger:
            if c.states[i][-1] != c.states[j][-1]:
                switches[i] += e.rate
        values = np.array([occ @ active, occ @ switches])
        if not details:
            return values
        system = c.q.T.toarray()
        system[-1] = 1
        rhs = np.zeros(len(c.states))
        rhs[-1] = 1
        stationary = np.linalg.solve(system, rhs)
        hazard = np.array([s[2] == 0 and s[3] == 1 for s in c.states])

        def joint_information(weights):
            joint = np.array(
                [
                    [weights[(active == s) & (hazard == h)].sum() for h in (0, 1)]
                    for s in (0, 1)
                ]
            )
            product = joint.sum(axis=1)[:, None] * joint.sum(axis=0)[None, :]
            keep = joint > 0
            return float(np.sum(joint[keep] * np.log2(joint[keep] / product[keep])))

        return {
            "moments": values.tolist(),
            "stationary_signal_exposure_mi_bits": joint_information(stationary),
            "T64_time_averaged_signal_exposure_mi_bits": joint_information(occ / 64),
            "scope": "Diagnostic signal/exposure dependence, not future-breadth T test",
        }

    results = {}
    for env in ENVIRONMENTS:
        target = moments(env, tracking=True)
        attempts = []

        def residual(log_rates, env=env, target=target, attempts=attempts):
            rates = np.exp(log_rates)
            measured = moments(env, tracking=False, on=rates[0], off=rates[1])
            relative = (measured - target) / target
            attempts.append(
                {
                    "rates": rates.tolist(),
                    "moments": measured.tolist(),
                    "relative_residuals": relative.tolist(),
                }
            )
            return relative

        fit = least_squares(
            residual,
            np.log([0.03, 0.025]),
            bounds=(np.log([1e-5, 1e-5]), np.log([2, 2])),
            xtol=1e-10,
            ftol=1e-10,
            gtol=1e-10,
            max_nfev=60,
        )
        error = float(np.max(abs(fit.fun)))
        if not fit.success or error > 1e-6:
            write(
                out / "CALIBRATION_FAILED.json",
                {
                    "environment": env,
                    "target": target.tolist(),
                    "attempts": attempts,
                    "message": fit.message,
                },
            )
            raise ArithmeticError("Physical moment calibration unresolved")
        rates = np.exp(fit.x)
        results[env] = {
            "on_conductance": float(rates[0]),
            "off_conductance": float(rates[1]),
            "target_occupancy_time": float(target[0]),
            "target_switches": float(target[1]),
            "max_relative_residual": error,
            "attempts": attempts,
            "tracking_diagnostics": moments(env, tracking=True, details=True),
            "independent_diagnostics": moments(
                env, tracking=False, on=rates[0], off=rates[1], details=True
            ),
        }
        print(env, "calibrated", error, flush=True)
    write(
        out / "CALIBRATION.json",
        {
            "schema": "omega.paid-register-calibration/1",
            "horizon": 64,
            "reference": "T0, same root; physical moments only",
            "signal_exposure_information_diagnostic_computed_after_fit": True,
            "history_entropy_computed": False,
            "sensor": SENSOR,
            "environments": results,
            "source_manifest_sha256": digest(manifest),
        },
    )


def cond(name, value):
    return {"coordinate": name, "operator": "eq", "value": value}


def protocol(calibration):
    from write_coupled_smoke_plan import case

    from omega_cosmology.testbed.signals import warning_root, warning_world

    laws = []
    for env, barrier in ENVIRONMENTS.items():
        rates = calibration["environments"][env]
        for arm, (tracking, response) in ARMS.items():
            model = warning_world(
                tracking=tracking,
                response=response,
                barrier_conductance=barrier,
                on_conductance=0.008 if tracking else rates["on_conductance"],
                off_conductance=(0.025 if SENSOR == "kinetic" else 0.008)
                if tracking
                else rates["off_conductance"],
                sensor=SENSOR,
            )
            laws.append(
                {
                    "id": env + "_" + arm,
                    "model": model.record(),
                    "environment": env,
                    "arm": arm,
                    "tracking_write": tracking,
                    "response": response,
                }
            )
    m = warning_world(sensor=SENSOR)
    root = warning_root()
    p = case("S4", m, root, [])["protocol"]
    p.update(
        {
            "schema": "omega.finite-study-protocol/1",
            "id": ("S4" if SENSOR == "kinetic" else "S4b") + ".warning-obstruction",
            "question": "When does a paid warning response widen or narrow continuation as escape changes?",
            "laws": laws,
            "horizons": [16, 64, 256, 1024],
            "cadences": [0.125, 0.25, 0.5],
            "max_states": 300,
            "max_dense_bytes": 32 * 1024**2,
            "max_occupation_dense_bytes": 256 * 1024**2,
            "sufficiency": "All modeled body, register, hazard, barrier and carrier dependencies retained",
            "scope": "Finite functional aversive-response proxy; no phenomenal valence, mortality, optimizer or ethical verdict",
            "conserved": ["body_slot", "carrier_slot"],
            "execution": {"max_workers": 1},
            "caps": {
                "case_wall_seconds": 300,
                "job_memory_bytes": 2 * 1024**3,
                "case_output_bytes": 8 * 1024**2,
                "batch_wall_seconds": 7200,
                "batch_output_bytes": 128 * 1024**2,
            },
            "source_inputs": [
                "scripts/write_s4_plan.py",
                "tests/test_signals.py",
                FOLDER + "/SPECIFICATION_r1.md",
                FOLDER + "/CALIBRATION.json",
                FOLDER + "/CALIBRATION_RECEIPT.json",
            ],
            "projected_histories": [
                {
                    "id": "body",
                    "coordinates": [
                        "body.working",
                        "body.bank",
                        "body.location",
                        "body.signal",
                    ],
                    "conditioning": "full_present",
                    "memory": 1,
                },
                {
                    "id": "body_signal_merged",
                    "coordinates": ["body.working", "body.bank", "body.location"],
                    "conditioning": "full_present",
                    "memory": 1,
                },
            ],
            "structural_analysis": {
                "ancestry": [],
                "organizations": [
                    {
                        "id": "body",
                        "definition": "Working apparatus, regardless of bank or location",
                        "coordinates": ["body.working"],
                        "functional_any_of": [[cond("body.working", 1)]],
                    },
                ],
            },
        }
    )
    p["numerical"]["sign_deadband_bits"] = 1e-6
    p["boundary_scope"]["bath_beta"] = 2.0
    # Law-specific roots accommodate the physically fixed open-barrier sector.
    # The shared assay consumes per-law protocols via separate open protocol.
    p["observables"] = [{"id": "bank_energy", "terms": [["body.bank", 0.5]]}]
    for name, conditions in {
        "signal_on": [cond("body.signal", 1)],
        "exposed_hazard": [cond("body.location", 0), cond("hazard", 1)],
        "signal_and_exposed_hazard": [
            cond("body.signal", 1),
            cond("body.location", 0),
            cond("hazard", 1),
        ],
        "sheltered": [cond("body.location", 1)],
        "barrier_open": [cond("barrier", 1)],
        "signal_blocked": [
            cond("body.signal", 1),
            cond("body.location", 0),
            cond("barrier", 0),
        ],
    }.items():
        p["observables"].append({"id": name, "constant": 1, "conditions": conditions})
    all_ids = {r.id for r in m.rules}
    groups = {
        "capture": ["capture_0", "capture_1"],
        "paid_repair": ["paid_restore"],
        "hazard_damage": ["hazard_damage"],
        "escape": ["escape"],
        "blocked_effort": ["blocked_effort"],
        "signal_write": sorted(i for i in all_ids if i.startswith("signal_write")),
        "signal_relax": ["signal_relax"],
        "signal_upkeep": ["signal_upkeep"],
    }
    resets = sorted(i for i in all_ids if i.startswith("signal_reset"))
    if resets:
        groups["signal_reset"] = resets
    p["event_readouts"] = [
        {
            "id": name + ("_forward" if direction == 1 else "_reverse"),
            "selectors": [{"rules": ids, "direction": direction}],
        }
        for name, ids in groups.items()
        for direction in (1, -1)
    ]
    return p


def materialize(calibration):
    import copy

    from omega_cosmology.testbed.signals import warning_root

    base = protocol(calibration)
    target = ROOT / FOLDER
    comparisons = {}
    for group in ("dynamic", "open"):
        p = copy.deepcopy(base)
        p["id"] += "." + group
        p["laws"] = [
            l for l in p["laws"] if (l["environment"] == "open") == (group == "open")
        ]
        root = list(warning_root(open_barrier=group == "open"))
        p["preparations"] = [
            {"id": "present", "roots": [[root, 1.0]], "conditioning": "full_present"}
        ]
        p["energy_per_root"] = "5/2"
        # Largest world first; first completed full case gates each batch.
        order = {"fast": 0, "slow": 1, "blocked": 2, "open": 3}
        p["laws"].sort(
            key=lambda l: (order[l["environment"]], list(ARMS).index(l["arm"]))
        )
        p["case_grid"] = [[l["id"], dt] for l in p["laws"] for dt in p["cadences"]]
        write(target / ("PROTOCOL_" + group.upper() + ".json"), p)
        comparisons[group] = [
            {
                "id": env + ":" + first + "-minus-" + second,
                "kind": "mechanism",
                "first": [env + "_" + first, "present"],
                "second": [env + "_" + second, "present"],
                "matching": "same root, material, energy and boundaries; declared sensor/response coupling differs",
            }
            for env in dict.fromkeys(l["environment"] for l in p["laws"])
            for first, second in [
                ("TX", "T0"),
                ("TX", "RX"),
                ("T0", "R0"),
                ("RX", "R0"),
            ]
        ]
    write(
        target / "ANALYSIS_PLAN.json",
        {
            "schema": "omega.signed-comparison-plan/1",
            "title": "Paid warning and obstruction results",
            "physical_scope_notes": [
                "All arms retain the same energetic register, bank and body; sensor or response coupling differs explicitly.",
                "Independent-register occupancy and switches are matched at T64 only; joint histories and actual costs are not matched.",
            ],
            "comparison_scope_notes": [
                "These are same-endowment mechanism contrasts, not enacted rewiring options or a phenomenal-suffering verdict.",
                "Physical randomness counts. Finite profiles are primary; rates and offsets remain diagnostics.",
                "No formal future-breadth T test, learned helplessness, anaesthesia or factory farming is modeled.",
            ],
            "engineering_note": "Four largest-world smoke cases and the entropy-free physical calibration are retained separately.",
            "tolerance_bits": 1e-6,
            "comparisons": comparisons,
            "projected_scopes": {
                k: {"body": "body", "body_signal_merged": "body_signal_merged"}
                for k in comparisons
            },
        },
    )
    # Engineering smoke exercises the same four mechanisms in the largest world.
    p = copy.deepcopy(base)
    p["horizons"] = [4, 16]
    cases = [
        {"id": l["id"], "law": l, "protocol": copy.deepcopy(p)}
        for l in base["laws"]
        if l["environment"] == "fast"
    ]
    plan = {
        "schema": "omega.coupled-engineering-plan/1",
        "date": "2026-10-26",
        "cases": cases,
        "spec": FOLDER + "/SPECIFICATION_r1.md",
        "snapshot_files": base["source_inputs"],
        "caps": {
            "case_seconds": 300,
            "job_memory_bytes": 2 * 1024**3,
            "case_output_bytes": 8 * 1024**2,
            "batch_seconds": 1200,
            "batch_output_bytes": 32 * 1024**2,
        },
    }
    smoke_name = "s4-warning" if SENSOR == "kinetic" else "s4b-warning"
    smoke = ROOT / ("research/platform/models/" + smoke_name + "/ENGINEERING_PLAN.json")
    smoke.parent.mkdir(parents=True, exist_ok=True)
    write(smoke, plan)


def main():
    global FOLDER, SENSOR
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--calibration-worker", action="store_true")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--sensor", choices=("kinetic", "push_pull"), default="kinetic")
    args = parser.parse_args()
    SENSOR = args.sensor
    if SENSOR == "push_pull":
        FOLDER = "research/studies/S4b-paid-warning"
    out = args.out_dir.resolve()
    if args.calibration_worker:
        calibration_worker(out, args.manifest)
        return
    if out.exists() or not out.is_relative_to(ROOT / "runs"):
        parser.error("Choose a fresh calibration folder under runs")
    out.mkdir(parents=True)
    files = sorted((ROOT / "src/omega_cosmology/testbed").glob("*.py")) + [
        Path(__file__),
        ROOT / FOLDER / "SPECIFICATION_r1.md",
        ROOT / "tests/test_signals.py",
    ]
    manifest = {"files": []}
    for path in files:
        relative = path.relative_to(ROOT)
        dest = out / "frozen" / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
        manifest["files"].append(
            {
                "path": relative.as_posix(),
                "sha256": digest(path),
                "bytes": path.stat().st_size,
            }
        )
    path = out / "frozen/MANIFEST.json"
    write(path, manifest)
    from omega_cosmology.testbed.workflow import capped

    receipt = capped(
        [
            sys.executable,
            str(out / "frozen/scripts/write_s4_plan.py"),
            "--out-dir",
            str(out),
            "--calibration-worker",
            "--manifest",
            str(path),
            "--sensor",
            SENSOR,
        ],
        out,
        seconds=600,
        memory=2 * 1024**3,
        output_cap=32 * 1024**2,
        cwd=out / "frozen",
    )
    write(out / "CALIBRATION_RECEIPT.json", receipt)
    if receipt["exit_code"] != 0 or receipt["cap_reason"]:
        raise RuntimeError("Calibration did not pass; no scientific protocol emitted")
    target = ROOT / FOLDER
    for name in ("CALIBRATION.json", "CALIBRATION_RECEIPT.json"):
        if (target / name).exists():
            raise FileExistsError("Calibration already retained; no silent overwrite")
        shutil.copyfile(out / name, target / name)
    materialize(json.loads((target / "CALIBRATION.json").read_text()))
    print(
        json.dumps(
            {
                "status": "passed",
                "calibration_receipt": receipt,
                "laws": 16,
                "cases": 48,
                "profiles": 192,
            }
        )
    )


if __name__ == "__main__":
    main()
