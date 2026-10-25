"""Source-frozen paired history-filter estimates on retained finite-study laws."""

import argparse
import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def worker(plan, case):
    import numpy as np

    from omega_cosmology.testbed.backends import enumerate_model
    from omega_cosmology.testbed.filtering import paired_projected_history_estimate
    from omega_cosmology.testbed.history import history_profile, sampled_kernel
    from omega_cosmology.testbed.physics import LocalModel
    from omega_cosmology.testbed.projections import projected_history_profiles

    protocol = json.loads((ROOT / plan["protocol"]).read_text(encoding="utf-8"))
    prep = next(p for p in protocol["preparations"] if p["id"] == case["preparation"])
    if prep["conditioning"] != "full_present" or len(prep["roots"]) != 1:
        raise ValueError("Known full present required")
    root = tuple(prep["roots"][0][0])
    all_roots = [
        tuple(s) for prep in protocol["preparations"] for s, _ in prep["roots"]
    ]
    labels, baselines, laws, checks = [], [], [], []
    steps = [round(T / plan["cadence"]) for T in case["horizons"]]
    if any(
        abs(k * plan["cadence"] - T) > 1e-10 for k, T in zip(steps, case["horizons"])
    ):
        raise ValueError("Horizons must fall on declared cadence")
    for name in (plan["reference_law"], plan["candidate_law"]):
        law = next(l for l in protocol["laws"] if l["id"] == name)
        model = LocalModel.from_record(law["model"])
        compiled = enumerate_model(model, all_roots)
        p = sampled_kernel(compiled, plan["cadence"])
        mu = np.zeros(len(p))
        mu[compiled.index[root]] = 1
        fields = plan["projections"][case["projection"]]
        values = [tuple(s[model.indices[k]] for k in fields) for s in compiled.states]
        laws.append((p, mu, values))
        retained = json.loads(
            (ROOT / plan["retained_cases"][name]).read_text(encoding="utf-8")
        )
        if model.fingerprint() != retained["model_hash"]:
            raise ArithmeticError("Physical model changed from retained E1")
        profile = history_profile(p, mu, max(steps))
        residuals = []
        for T, k in zip(case["horizons"], steps):
            old = next(
                (
                    r
                    for r in retained["rows"]
                    if r["preparation"] == case["preparation"] and r["horizon"] == T
                ),
                None,
            )
            if old:
                residuals.append(abs(profile[k] - old["history"]["ell_bits"]))
        if max(residuals, default=0) > 1e-6:
            raise ArithmeticError("Unchanged whole-history calculation differs from E1")
        checks.append(
            {
                "law": name,
                "model_hash": model.fingerprint(),
                "max_retained_whole_history_residual_bits": max(residuals, default=0),
            }
        )
        if case.get("exact_memory") is not None:
            baselines.append(
                projected_history_profiles(
                    p,
                    mu,
                    values,
                    steps,
                    memory=case["exact_memory"],
                    max_workspace_bytes=256 * 1024**2,
                )
            )
        labels.append(values)
    estimates = paired_projected_history_estimate(
        *laws,
        steps,
        samples=case["samples"],
        seed=case["seed"],
        batch_size=case["batch_size"],
        confidence=0.95,
        max_workspace_bytes=128 * 1024**2,
        max_sample_steps=case["samples"] * max(steps),
        control_variate=case.get("control_variate", "none"),
        confidence_family_size=plan.get("confidence_family_size"),
    )
    rows = []
    for T, k in zip(case["horizons"], steps):
        row = {"horizon": T, **estimates[k]}
        if baselines:
            ref, candidate = [b[k] for b in baselines]
            row["analytic_difference_interval_bits"] = [
                candidate["lower_bits"] - ref["upper_bits"],
                candidate["upper_bits"] - ref["lower_bits"],
            ]
            if any(b[k]["width_bits"] > 1e-8 for b in baselines):
                raise ArithmeticError("Calibration requires exact full observed prefix")
        rows.append(row)
    return {"status": "passed", "case": case, "physical_checks": checks, "rows": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--worker-case")
    args = parser.parse_args()
    plan_path = args.plan.resolve()
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    out = args.out_dir.resolve()
    if args.worker_case:
        if sys.stdin.readline().strip() != "GO":
            raise RuntimeError("Capped supervisor GO required")
        manifest_path = ROOT / "MANIFEST.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if any(digest(ROOT / r["path"]) != r["sha256"] for r in manifest["files"]):
            raise RuntimeError("Frozen source changed")
        case = next(c for c in plan["cases"] if c["id"] == args.worker_case)
        started = perf_counter()
        result = worker(plan, case)
        result["manifest_sha256"] = digest(manifest_path)
        result["worker_seconds"] = perf_counter() - started
        (out / "RESULT.json").write_text(
            json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8"
        )
        print(
            json.dumps(
                {
                    "case": case["id"],
                    "status": "passed",
                    "seconds": result["worker_seconds"],
                }
            ),
            flush=True,
        )
        return
    if (
        out.exists()
        or not out.is_relative_to(ROOT / "runs")
        or not plan_path.is_relative_to(ROOT / "research")
    ):
        parser.error("Use a fresh output inside runs/ and a plan inside research/")
    if plan["schema"] != "omega.projection-filter-plan/1":
        raise ValueError("Unsupported plan schema")
    ids = [c["id"] for c in plan["cases"]]
    if len(set(ids)) != len(ids) or any(not key.isidentifier() for key in ids):
        raise ValueError("Unique simple case identifiers required")
    out.mkdir(parents=True)
    frozen = out / "frozen"
    files = sorted((ROOT / "src/omega_cosmology/testbed").glob("*.py"))
    files += [
        ROOT / "src/omega_cosmology/__init__.py",
        Path(__file__).resolve(),
        plan_path,
        ROOT / plan["protocol"],
        *(ROOT / p for p in plan["retained_cases"].values()),
        *(ROOT / p for p in plan["source_inputs"]),
    ]
    manifest = {"schema": "omega.projection-filter-snapshot/1", "files": []}
    for path in dict.fromkeys(files):
        relative = path.relative_to(ROOT)
        target = frozen / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        manifest["files"].append({"path": relative.as_posix(), "sha256": digest(path)})
    manifest_path = frozen / "MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    from omega_cosmology.testbed.workflow import capped

    receipts = []
    started = perf_counter()
    for case in plan["cases"]:
        folder = out / case["id"]
        folder.mkdir()
        receipt = capped(
            [
                sys.executable,
                str(frozen / "scripts/run_projection_filter.py"),
                "--plan",
                str(plan_path.relative_to(ROOT)),
                "--out-dir",
                str(folder),
                "--worker-case",
                case["id"],
            ],
            folder,
            seconds=plan["caps"]["case_seconds"],
            memory=plan["caps"]["job_memory_bytes"],
            output_cap=plan["caps"]["case_output_bytes"],
            cwd=frozen,
        )
        file = folder / "RESULT.json"
        valid = (
            receipt["exit_code"] == 0
            and receipt["cap_reason"] is None
            and file.is_file()
        )
        if valid:
            result = json.loads(file.read_text(encoding="utf-8"))
            valid = result["status"] == "passed" and result[
                "manifest_sha256"
            ] == digest(manifest_path)
        receipts.append(
            {
                "id": case["id"],
                "passed": valid,
                "receipt": receipt,
                "result_sha256": digest(file) if file.is_file() else None,
            }
        )
        print(json.dumps(receipts[-1]), flush=True)
        if not valid:
            break
    final = {
        "status": "passed"
        if len(receipts) == len(plan["cases"]) and all(r["passed"] for r in receipts)
        else "failed",
        "wall_seconds": perf_counter() - started,
        "cases": receipts,
        "manifest_sha256": digest(manifest_path),
        "frozen_inputs_verified_after_run": all(
            digest(frozen / r["path"]) == r["sha256"] for r in manifest["files"]
        ),
    }
    (out / "BATCH_RECEIPT.json").write_text(
        json.dumps(final, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": final["status"], "seconds": final["wall_seconds"]}))
    raise SystemExit(0 if final["status"] == "passed" else 1)


if __name__ == "__main__":
    main()
