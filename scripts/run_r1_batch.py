"""Snapshot R1 inputs, gate on the longest-horizon case, then run the small batch."""

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--feasibility-only", action="store_true")
    args = parser.parse_args()
    out = args.out_dir.resolve()
    if out.exists() or not out.is_relative_to(ROOT / "runs"):
        parser.error("Choose a fresh directory inside runs/")
    protocol_path = ROOT / "research/studies/R1-constructed-access/PROTOCOL.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    out.mkdir(parents=True)
    frozen = out / "frozen"
    files = sorted((ROOT / "src/omega_cosmology/testbed").glob("*.py"))
    files += [
        ROOT / "src/omega_cosmology/__init__.py",
        ROOT / "scripts/r1_worker.py",
        Path(__file__).resolve(),
        ROOT / "scripts/write_r1_protocol.py",
        ROOT / "tests/test_testbed_readouts.py",
        protocol_path,
        ROOT / "research/studies/R1-constructed-access-PROPOSAL.md",
        ROOT / "pyproject.toml",
    ]
    manifest = {
        "schema": "omega.r1-snapshot/1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "protocol_sha256": digest(protocol_path),
        "files": [],
        "caps": protocol["caps"],
    }
    for path in files:
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
        raise RuntimeError("Inputs changed while snapshotting")
    from omega_cosmology.testbed.workflow import capped, tree_bytes

    cases = [
        (law["id"], cadence)
        for law in protocol["laws"]
        for cadence in protocol["cadences"]
    ]
    if cases[0] != ("driven__intact", 0.125):
        raise ValueError("The longest fine-cadence intact case must gate the batch")
    if args.feasibility_only:
        cases = cases[:1]
    started = perf_counter()
    receipts = []
    complete = True
    for i, (law, cadence) in enumerate(cases):
        remaining = protocol["caps"]["batch_wall_seconds"] - (perf_counter() - started)
        if remaining <= 0:
            complete = False
            break
        case_id = f"{law}__dt{str(cadence).replace('.', 'p')}"
        folder = out / case_id
        folder.mkdir()
        receipt = capped(
            [
                sys.executable,
                str(frozen / "scripts/r1_worker.py"),
                "--law",
                law,
                "--cadence",
                str(cadence),
                "--out-dir",
                str(folder),
            ],
            folder,
            cwd=frozen,
            seconds=min(remaining, protocol["caps"]["case_wall_seconds"]),
            memory=protocol["caps"]["job_memory_bytes"],
            output_cap=protocol["caps"]["case_output_bytes"],
        )
        path = folder / "RESULT.json"
        valid = (
            receipt["exit_code"] == 0
            and receipt["cap_reason"] is None
            and path.exists()
        )
        if valid:
            result = json.loads(path.read_text(encoding="utf-8"))
            valid = (
                result["status"] == "passed"
                and result["manifest_sha256"] == digest(manifest_path)
                and len(result["rows"])
                == len(protocol["preparations"]) * len(protocol["horizons"])
            )
        receipts.append(
            {
                "case": case_id,
                "law": law,
                "cadence": cadence,
                "receipt": receipt,
                "result_sha256": digest(path) if path.exists() else None,
                "validated": valid,
            }
        )
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
        if not valid or tree_bytes(out) > protocol["caps"]["batch_output_bytes"]:
            complete = False
            break
    verified = all(digest(frozen / r["path"]) == r["sha256"] for r in manifest["files"])
    result = {
        "schema": "omega.r1-batch/1",
        "status": "passed" if complete and verified else "failed",
        "feasibility_only": args.feasibility_only,
        "manifest_sha256": digest(manifest_path),
        "protocol_sha256": manifest["protocol_sha256"],
        "frozen_inputs_verified_after_run": verified,
        "cases": receipts,
        "wall_seconds": perf_counter() - started,
        "output_bytes": tree_bytes(out),
        "scope": "Scientific finite modeled-world comparison; no policy search, microscopic gas or ethics verdict",
    }
    (out / "BATCH_RECEIPT.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "cases": len(receipts),
                "wall_seconds": result["wall_seconds"],
                "output_bytes": result["output_bytes"],
            }
        )
    )
    return result["status"] != "passed"


if __name__ == "__main__":
    sys.exit(main())
