"""Freeze and execute the small M0–M2 engineering calibration on Windows.

All generated files stay under runs/. No ecology/policy survey is launched.
"""

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    if out.exists() or not out.is_relative_to(ROOT / "runs"):
        parser.error("Choose a fresh directory inside runs/")
    out.mkdir(parents=True)
    frozen = out / "frozen"
    package = ROOT / "src/omega_cosmology/testbed"
    inputs = sorted(package.glob("*.py"))
    inputs += [
        ROOT / "src/omega_cosmology/__init__.py",
        ROOT / "scripts/testbed_calibration_worker.py",
        ROOT / "scripts/run_testbed_calibration.py",
        ROOT / "scripts/write_testbed_fixtures.py",
        ROOT / "pyproject.toml",
    ]
    inputs += sorted((ROOT / "research/platform/models").glob("*.json"))
    inputs += sorted((ROOT / "tests").glob("test_testbed*.py"))
    files = []
    for path in inputs:
        relative = path.relative_to(ROOT)
        target = frozen / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        files.append(
            {
                "path": relative.as_posix(),
                "sha256": digest(path),
                "bytes": path.stat().st_size,
            }
        )
    manifest = {
        "schema": "omega.engineering-snapshot/1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "files": files,
        "purpose": "M0–M2 engineering; no scientific ranking sweep",
        "caps": {
            "wall_seconds": 120,
            "job_memory_bytes": 2 * 1024**3,
            "output_bytes": 32 * 1024**2,
        },
    }
    manifest_path = frozen / "MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    from omega_cosmology.testbed.workflow import capped

    if not all(digest(ROOT / row["path"]) == row["sha256"] for row in files):
        raise RuntimeError(
            "Live inputs changed during snapshot creation; start a fresh run"
        )

    probes = {}
    for mode, seconds, memory in [
        ("wall", 0.5, 128 * 1024**2),
        ("memory", 10, 64 * 1024**2),
    ]:
        folder = out / ("cap-" + mode)
        folder.mkdir()
        probes[mode] = capped(
            [
                sys.executable,
                str(frozen / "scripts/testbed_calibration_worker.py"),
                "--cap-probe",
                mode,
            ],
            folder,
            seconds=seconds,
            memory=memory,
            output_cap=1024**2,
            cwd=frozen,
        )
    if (
        probes["wall"]["cap_reason"] != "wall_cap"
        or probes["memory"]["exit_code"] != 86
        or probes["memory"]["cap_reason"]
    ):
        raise RuntimeError("Hard cap probe failed; no calibration was launched")
    result_dir = out / "calibration"
    result_dir.mkdir()
    receipt = capped(
        [
            sys.executable,
            str(frozen / "scripts/testbed_calibration_worker.py"),
            "--out-dir",
            str(result_dir),
        ],
        out,
        cwd=frozen,
        seconds=manifest["caps"]["wall_seconds"],
        memory=manifest["caps"]["job_memory_bytes"],
        output_cap=manifest["caps"]["output_bytes"],
    )
    verified = all(digest(frozen / row["path"]) == row["sha256"] for row in files)
    summary_path = result_dir / "SUMMARY.json"
    summary = (
        json.loads(summary_path.read_text(encoding="utf-8"))
        if summary_path.exists()
        else {}
    )
    success = (
        receipt["exit_code"] == 0
        and receipt["cap_reason"] is None
        and verified
        and summary.get("status") == "passed"
    )
    evidence = {
        "status": "passed" if success else "failed",
        "manifest_sha256": digest(manifest_path),
        "frozen_inputs_verified_after_run": verified,
        "cap_probes": probes,
        "calibration": receipt,
        "summary_sha256": digest(summary_path) if summary_path.exists() else None,
        "source_scope": "Calibration worker executes from the frozen snapshot; launcher/cap-helper bytes matched before launch. Installed dependency versions recorded by worker",
    }
    (out / "RECEIPT.json").write_text(
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(evidence, indent=2))
    return not success


if __name__ == "__main__":
    sys.exit(main())
