"""Source-frozen capped engineering cases; largest coupled case gates the rest."""

import argparse
import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
DEFAULT_PLAN = "research/platform/models/coupled-autocatalysis/ENGINEERING_PLAN.json"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--plan", type=Path, default=Path(DEFAULT_PLAN))
    parser.add_argument("--worker-case")
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    if args.worker_case:
        if sys.stdin.readline().strip() != "GO":
            raise RuntimeError("Capped supervisor GO required")
        manifest = json.loads(args.manifest.read_text())
        for row in manifest["files"]:
            if digest(ROOT / row["path"]) != row["sha256"]:
                raise RuntimeError("Frozen source changed")
        plan = json.loads((ROOT / args.plan).read_text())
        case = next(c for c in plan["cases"] if c["id"] == args.worker_case)
        from omega_cosmology.testbed.finite_study import evaluate_case

        result = evaluate_case(case["protocol"], case["law"], 0.25)
        for row in result["rows"]:
            for spec in case["protocol"]["projected_histories"]:
                name = spec["id"]
                bounds = row["projected_histories"][name]
                if (
                    bounds["lower_bits"] > bounds["upper_bits"] + 1e-8
                    or bounds["upper_bits"] > row["history"]["ell_bits"] + 1e-8
                ):
                    raise ArithmeticError(
                        "Projected bounds conflict with whole history"
                    )
                if name.endswith(".m2"):
                    previous = row["projected_histories"][name[:-1] + "1"]
                    if bounds["upper_bits"] > previous["upper_bits"] + 1e-8:
                        raise ArithmeticError(
                            "Longer observed memory loosened the upper bound"
                        )
                    if bounds["lower_bits"] < previous["lower_bits"] - 1e-8:
                        raise ArithmeticError(
                            "Longer observed memory loosened the lower bound"
                        )
        result["source_manifest_sha256"] = digest(args.manifest)
        result["engineering_only"] = True
        (args.out_dir / "RESULT.json").write_text(
            json.dumps(result, indent=2, allow_nan=False) + "\n"
        )
        print(
            json.dumps(
                {
                    "status": result["status"],
                    "states": result["states"],
                    "profiles": len(result["rows"]),
                }
            )
        )
        return
    out = args.out_dir.resolve()
    plan_path = args.plan.resolve()
    if (
        out.exists()
        or not out.is_relative_to(ROOT / "runs")
        or not plan_path.is_relative_to(ROOT / "research/platform/models")
    ):
        parser.error(
            "Use a fresh run directory and a plan under research/platform/models/"
        )
    plan = json.loads(plan_path.read_text())
    if plan["schema"] != "omega.coupled-engineering-plan/1":
        raise ValueError("Unsupported engineering plan")
    if len({c["id"] for c in plan["cases"]}) != len(plan["cases"]) or any(
        not c["id"].isidentifier() for c in plan["cases"]
    ):
        raise ValueError("Unique simple case IDs required")
    out.mkdir(parents=True)
    files = sorted((ROOT / "src/omega_cosmology/testbed").glob("*.py"))
    files += [
        ROOT / "src/omega_cosmology/__init__.py",
        ROOT / "pyproject.toml",
        Path(__file__).resolve(),
        ROOT / "scripts/write_coupled_smoke_plan.py",
        plan_path,
        ROOT / plan["spec"],
        ROOT / "tests/test_coupled_physics.py",
        ROOT / "tests/test_projection_bounds.py",
    ]
    for name in plan.get("snapshot_files", ()):
        extra = (ROOT / name).resolve()
        if not extra.is_relative_to(ROOT) or not extra.is_file():
            raise ValueError("Snapshot input must be a repository file")
        files.append(extra)
    frozen = out / "frozen"
    manifest = {
        "schema": "omega.coupled-engineering-snapshot/1",
        "date": plan.get("date", "2026-10-25"),
        "plan": plan_path.relative_to(ROOT).as_posix(),
        "caps": plan["caps"],
        "files": [],
    }
    for path in dict.fromkeys(files):
        relative = path.relative_to(ROOT)
        target = frozen / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        manifest["files"].append(
            {
                "path": relative.as_posix(),
                "sha256": digest(target),
                "bytes": target.stat().st_size,
            }
        )
    manifest_path = frozen / "MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    from omega_cosmology.testbed.workflow import capped, tree_bytes

    started = perf_counter()
    cases = []
    for case in plan["cases"]:
        remaining = plan["caps"]["batch_seconds"] - (perf_counter() - started)
        if remaining <= 0:
            break
        folder = out / case["id"]
        folder.mkdir()
        try:
            receipt = capped(
                [
                    sys.executable,
                    str(frozen / "scripts/run_coupled_smoke.py"),
                    "--out-dir",
                    str(folder),
                    "--plan",
                    manifest["plan"],
                    "--worker-case",
                    case["id"],
                    "--manifest",
                    str(manifest_path),
                ],
                folder,
                seconds=min(remaining, plan["caps"]["case_seconds"]),
                memory=plan["caps"]["job_memory_bytes"],
                output_cap=plan["caps"]["case_output_bytes"],
                cwd=ROOT,
            )
        except MemoryError as error:
            # A host-memory refusal happens before the child exists. Preserve
            # a capped-batch receipt instead of leaving only a partial snapshot.
            receipt = {
                "exit_code": None,
                "cap_reason": "host_memory_preflight",
                "error": str(error),
                "worker_started": False,
                "job_memory_cap_bytes": plan["caps"]["job_memory_bytes"],
                "peak_job_bytes": None,
                "wall_seconds": 0.0,
            }
        result_path = folder / "RESULT.json"
        passed = (
            receipt["exit_code"] == 0
            and receipt["cap_reason"] is None
            and result_path.is_file()
        )
        if passed:
            result = json.loads(result_path.read_text())
            passed = result["status"] == "passed" and result[
                "source_manifest_sha256"
            ] == digest(manifest_path)
        cases.append(
            {
                "id": case["id"],
                "passed": passed,
                "receipt": receipt,
                "result_sha256": digest(result_path) if result_path.is_file() else None,
            }
        )
        if not passed or tree_bytes(out) > plan["caps"]["batch_output_bytes"]:
            break
    receipt = {
        "schema": "omega.coupled-engineering-receipt/1",
        "status": "passed"
        if len(cases) == len(plan["cases"]) and all(c["passed"] for c in cases)
        else "failed",
        "engineering_only": True,
        "plan_sha256": digest(plan_path),
        "source_manifest_sha256": digest(manifest_path),
        "cases": cases,
        "wall_seconds": perf_counter() - started,
        "output_bytes": tree_bytes(out),
    }
    if receipt["output_bytes"] > plan["caps"]["batch_output_bytes"]:
        receipt["status"] = "failed"
    (out / "BATCH_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    if receipt["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
