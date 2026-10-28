"""One serial source-snapshot worker, with physical calibration before history."""

import argparse
import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
PLAN = "research/platform/models/enacted-damage/ENGINEERING_PLAN.json"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def worker(out, plan, manifest_hash):
    from write_enacted_damage_plan import protocol

    from omega_cosmology.testbed.matching import MomentSpec, match_physical_moments
    from omega_cosmology.testbed.operations import operation_world
    from omega_cosmology.testbed.phases import continuous_schedule
    from omega_cosmology.testbed.repair import repair_capacity_world
    from omega_cosmology.testbed.scheduled_study import (
        evaluate_scheduled_case,
        schedule_inputs,
    )

    started = perf_counter()
    cases = {c["id"]: c for c in plan["cases"]}
    calibration = plan["calibration"]
    moments = calibration["moments"]
    target_values = {}
    for name in calibration["targets"]:
        compiled, lengths, mu = schedule_inputs(cases[name])
        row = continuous_schedule(
            list(zip(compiled, lengths)),
            mu,
            cases[name]["cadence"],
            calibration["horizon"],
        )
        target_values[name] = {k: row["physical"][k] for k in moments}

    base = repair_capacity_world()
    recovery = operation_world(base)

    def sham_protocol(parameters, name="calibration_only"):
        return protocol(name, operation_world(base, **parameters), recovery)

    def evaluate_moments(parameters):
        spec = sham_protocol(parameters)
        compiled, lengths, mu = schedule_inputs(spec)
        result = continuous_schedule(
            list(zip(compiled, lengths)), mu, spec["cadence"], calibration["horizon"]
        )
        return {k: result["physical"][k] for k in moments}

    fits = {}
    for name, target in target_values.items():
        fits[name] = match_physical_moments(
            evaluate_moments,
            target,
            calibration["bounds"],
            max_evaluations=calibration["max_fit_evaluations"],
            # Preserve the retained plan's numerical allowances, but state each
            # quantity, unit, window and absolute acceptance tolerance explicitly.
            moment_specs={
                k: MomentSpec(
                    k,
                    "events" if k == "expected_jumps" else "model_energy",
                    calibration["horizon"],
                    "continuous_integral",
                    absolute_tolerance=calibration["scaled_tolerance"] * max(1, abs(v)),
                    relative_tolerance=0,
                )
                for k, v in target.items()
            },
        )
        parameters = fits[name]["best"]["parameters"]
        fits[name]["independent_replay"] = evaluate_moments(parameters)
        controls = sham_protocol(parameters, "sham_for_" + name)
        cases[controls["id"]] = controls
    write(
        out / "CALIBRATION.json",
        {
            "horizon": calibration["horizon"],
            "completed_before_any_history_evaluation": True,
            "fits": fits,
        },
    )
    write(out / "EXECUTION_CASES.json", list(cases.values()))

    results = []
    for name, spec in cases.items():
        result = evaluate_scheduled_case(spec)
        write(out / (name + ".json"), result)
        results.append(result)
        print(
            json.dumps(
                {
                    "case": name,
                    "states": result["states"],
                    "profiles": len(result["rows"]),
                    "seconds": result["wall_seconds"],
                }
            ),
            flush=True,
        )
    lookup = {r["id"]: r for r in results}
    comparisons = []
    for first, second in [(k, "idle") for k in cases if k != "idle"] + [
        (n, "sham_for_" + n) for n in calibration["targets"]
    ]:
        for a, b in zip(lookup[first]["rows"], lookup[second]["rows"]):
            comparisons.append(
                {
                    "first": first,
                    "second": second,
                    "horizon": a["horizon"],
                    "delta_history_bits": a["history"]["ell_bits"]
                    - b["history"]["ell_bits"],
                    "delta_expected_jumps": a["physical"]["expected_jumps"]
                    - b["physical"]["expected_jumps"],
                    "delta_accepted_work": a["physical"]["work_accepted_gross"]
                    - b["physical"]["work_accepted_gross"],
                    "delta_net_work": a["physical"]["work_net"]
                    - b["physical"]["work_net"],
                    "delta_body_bounds": {
                        "lower_bits": a["projected_histories"]["repair_body.m1"][
                            "lower_bits"
                        ]
                        - b["projected_histories"]["repair_body.m1"]["upper_bits"],
                        "upper_bits": a["projected_histories"]["repair_body.m1"][
                            "upper_bits"
                        ]
                        - b["projected_histories"]["repair_body.m1"]["lower_bits"],
                    },
                }
            )
    summary = {
        "status": "passed",
        "engineering_only": True,
        "source_manifest_sha256": manifest_hash,
        "cases": [
            {
                "id": r["id"],
                "states": r["states"],
                "profiles": len(r["rows"]),
                "result_sha256": digest(out / (r["id"] + ".json")),
            }
            for r in results
        ],
        "comparisons": comparisons,
        "wall_seconds": perf_counter() - started,
        "calibration_seconds_excluded_from_history_case_timings": True,
        "limits": "Moment matches are finite-horizon and only if returned residuals pass. No scientific sweep, no rate-first verdict, no physical-resolution certification.",
    }
    write(out / "RESULT.json", summary)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-dir", required=True, type=Path)
    p.add_argument("--worker", action="store_true")
    p.add_argument("--manifest", type=Path)
    a = p.parse_args()
    if a.worker:
        if sys.stdin.readline().strip() != "GO":
            raise RuntimeError("Capped supervisor GO required")
        manifest = json.loads(a.manifest.read_text(encoding="utf-8"))
        for row in manifest["files"]:
            if digest(ROOT / row["path"]) != row["sha256"]:
                raise ValueError("Frozen source changed")
        worker(
            a.out_dir,
            json.loads((ROOT / PLAN).read_text(encoding="utf-8")),
            digest(a.manifest),
        )
        return
    out = a.out_dir.resolve()
    if out.exists() or not out.is_relative_to(ROOT / "runs"):
        p.error("Fresh output under runs required")
    plan = json.loads((ROOT / PLAN).read_text(encoding="utf-8"))
    if plan["schema"] != "omega.enacted-damage-engineering/1":
        raise ValueError("Unsupported plan")
    out.mkdir(parents=True)
    files = list((ROOT / "src/omega_cosmology/testbed").glob("*.py")) + [
        ROOT / "src/omega_cosmology/__init__.py",
        ROOT / "pyproject.toml",
        ROOT / PLAN,
        Path(__file__).resolve(),
        ROOT / "scripts/write_enacted_damage_plan.py",
        ROOT / "tests/test_phases.py",
        ROOT / plan["spec"],
    ]
    manifest = {
        "schema": "omega.enacted-damage-snapshot/1",
        "plan": PLAN,
        "caps": plan["caps"],
        "files": [],
    }
    for path in files:
        rel = path.relative_to(ROOT)
        target = out / "frozen" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        manifest["files"].append(
            {
                "path": rel.as_posix(),
                "sha256": digest(target),
                "bytes": target.stat().st_size,
            }
        )
    manifest_path = out / "frozen/MANIFEST.json"
    write(manifest_path, manifest)
    from omega_cosmology.testbed.workflow import capped, tree_bytes

    folder = out / "smoke"
    folder.mkdir()
    try:
        receipt = capped(
            [
                sys.executable,
                str(out / "frozen/scripts/run_enacted_damage_smoke.py"),
                "--worker",
                "--manifest",
                str(manifest_path),
                "--out-dir",
                str(folder),
            ],
            folder,
            seconds=plan["caps"]["case_seconds"],
            memory=plan["caps"]["job_memory_bytes"],
            output_cap=plan["caps"]["case_output_bytes"],
            cwd=out / "frozen",
        )
    except MemoryError as error:
        receipt = {
            "exit_code": None,
            "cap_reason": "host_memory_preflight",
            "error": str(error),
            "worker_started": False,
            "wall_seconds": 0,
        }
    result_path = folder / "RESULT.json"
    passed = (
        receipt["exit_code"] == 0
        and receipt["cap_reason"] is None
        and result_path.exists()
    )
    if passed:
        result = json.loads(result_path.read_text(encoding="utf-8"))
        passed = result["status"] == "passed" and result[
            "source_manifest_sha256"
        ] == digest(manifest_path)
    record = {
        "status": "passed" if passed else "failed",
        "source_manifest_sha256": digest(manifest_path),
        "cases": [
            {
                "id": "smoke",
                "passed": passed,
                "receipt": receipt,
                "result_sha256": digest(result_path) if result_path.exists() else None,
            }
        ],
        "output_bytes": tree_bytes(out),
    }
    write(out / "BATCH_RECEIPT.json", record)
    print(json.dumps(record, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
