"""Source-frozen, capped study runner; first full case gates the remaining cases."""

import argparse
import json
import shutil
import sys
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def study_cases(protocol):
    valid = {(l["id"], dt) for l in protocol["laws"] for dt in protocol["cadences"]}
    default = [(l["id"], dt) for l in protocol["laws"] for dt in protocol["cadences"]]
    cases = [tuple(c) for c in protocol.get("case_grid", default)]
    if not cases or len(set(cases)) != len(cases) or any(c not in valid for c in cases):
        raise ValueError("Case grid must contain unique declared law/cadence pairs")
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--feasibility-only", action="store_true")
    args = parser.parse_args()
    out = args.out_dir.resolve()
    source = args.protocol.resolve()
    if (
        out.exists()
        or not out.is_relative_to(ROOT / "runs")
        or not source.is_relative_to(ROOT / "research/studies")
    ):
        parser.error(
            "Choose a fresh output inside runs/ and a study protocol inside research/studies/"
        )
    protocol = json.loads(source.read_text(encoding="utf-8"))
    if protocol["schema"] != "omega.finite-study-protocol/1":
        raise ValueError("Unsupported protocol schema")
    out.mkdir(parents=True)
    frozen = out / "frozen"
    files = sorted((ROOT / "src/omega_cosmology/testbed").glob("*.py"))
    files += [
        ROOT / "src/omega_cosmology/__init__.py",
        ROOT / "scripts/finite_study_worker.py",
        Path(__file__).resolve(),
        ROOT / "pyproject.toml",
        source,
    ]
    for relative in protocol["source_inputs"]:
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError("External source input is unsupported")
        files.append(path)
    manifest = {
        "schema": "omega.finite-study-snapshot/1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "protocol": source.relative_to(ROOT).as_posix(),
        "protocol_sha256": digest(source),
        "caps": protocol["caps"],
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
                "sha256": digest(path),
                "bytes": path.stat().st_size,
            }
        )
    manifest_path = frozen / "MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    if not all(digest(ROOT / r["path"]) == r["sha256"] for r in manifest["files"]):
        raise RuntimeError("Live inputs changed during snapshot")
    from omega_cosmology.testbed.workflow import capped, tree_bytes

    cases = study_cases(protocol)
    if args.feasibility_only:
        cases = cases[:1]
    workers = protocol.get("execution", {}).get("max_workers", 1)
    if type(workers) is not int or not 1 <= workers <= 3:
        raise ValueError("This runner supports one to three capped workers")
    receipts = []
    started = perf_counter()
    complete = True

    def execute(i, law, dt):
        remaining = protocol["caps"]["batch_wall_seconds"] - (perf_counter() - started)
        if remaining <= 0:
            raise TimeoutError("Batch deadline reached before case dispatch")
        case_id = law + "__dt" + str(dt).replace(".", "p")
        folder = out / case_id
        folder.mkdir()
        receipt = capped(
            [
                sys.executable,
                str(frozen / "scripts/finite_study_worker.py"),
                "--protocol",
                manifest["protocol"],
                "--law",
                law,
                "--cadence",
                str(dt),
                "--out-dir",
                str(folder),
            ],
            folder,
            cwd=frozen,
            seconds=min(remaining, protocol["caps"]["case_wall_seconds"]),
            memory=protocol["caps"]["job_memory_bytes"],
            output_cap=protocol["caps"]["case_output_bytes"],
        )
        result_path = folder / "RESULT.json"
        valid = (
            receipt["exit_code"] == 0
            and receipt["cap_reason"] is None
            and result_path.exists()
        )
        if valid:
            result = json.loads(result_path.read_text(encoding="utf-8"))
            valid = (
                result["status"] == "passed"
                and result["manifest_sha256"] == digest(manifest_path)
                and len(result["rows"])
                == len(protocol["preparations"]) * len(protocol["horizons"])
            )
        item = {
            "case": case_id,
            "law": law,
            "cadence": dt,
            "validated": valid,
            "receipt": receipt,
            "result_sha256": digest(result_path) if result_path.exists() else None,
        }
        print(
            json.dumps(
                {
                    "case": i + 1,
                    "of": len(cases),
                    "id": case_id,
                    "validated": valid,
                    "seconds": receipt["wall_seconds"],
                }
            ),
            flush=True,
        )
        return item

    # The first complete case gates dispatch. Subsequent independent kernels
    # can run concurrently, each inside its own hard job/output caps.
    def safe_execute(i, law, dt):
        try:
            return execute(i, law, dt)
        except (OSError, ValueError, RuntimeError, ArithmeticError) as error:
            return {
                "case": law + "__dt" + str(dt).replace(".", "p"),
                "law": law,
                "cadence": dt,
                "validated": False,
                "receipt": {
                    "exit_code": None,
                    "cap_reason": "dispatch_error",
                    "error": f"{type(error).__name__}: {error}",
                },
                "result_sha256": None,
            }

    first = safe_execute(0, *cases[0])
    receipts.append(first)
    complete = first["validated"]
    if complete and len(cases) > 1:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            pending = {}
            next_index = 1
            while pending or (complete and next_index < len(cases)):
                while complete and len(pending) < workers and next_index < len(cases):
                    if (
                        perf_counter() - started
                        >= protocol["caps"]["batch_wall_seconds"]
                    ):
                        complete = False
                        break
                    law, dt = cases[next_index]
                    future = pool.submit(safe_execute, next_index, law, dt)
                    pending[future] = next_index
                    next_index += 1
                if not pending:
                    break
                finished, _ = wait(pending, timeout=1, return_when=FIRST_COMPLETED)
                for future in finished:
                    pending.pop(future)
                    item = future.result()
                    receipts.append(item)
                    if not item["validated"]:
                        complete = False
                if tree_bytes(out) > protocol["caps"]["batch_output_bytes"]:
                    complete = False
    complete = complete and len(receipts) == len(cases)
    order = {(law, dt): i for i, (law, dt) in enumerate(cases)}
    receipts.sort(key=lambda r: order[r["law"], r["cadence"]])
    verified = all(digest(frozen / r["path"]) == r["sha256"] for r in manifest["files"])
    evidence = {
        "schema": "omega.finite-study-batch/1",
        "status": "passed" if complete and verified else "failed",
        "feasibility_only": args.feasibility_only,
        "max_workers": workers,
        "manifest_sha256": digest(manifest_path),
        "protocol_sha256": manifest["protocol_sha256"],
        "frozen_inputs_verified_after_run": verified,
        "cases": receipts,
        "wall_seconds": perf_counter() - started,
        "output_bytes": tree_bytes(out),
        "scope": protocol["scope"],
    }
    (out / "BATCH_RECEIPT.json").write_text(
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": evidence["status"],
                "cases": len(receipts),
                "wall_seconds": evidence["wall_seconds"],
                "output_bytes": evidence["output_bytes"],
            }
        )
    )
    return evidence["status"] != "passed"


if __name__ == "__main__":
    sys.exit(main())
