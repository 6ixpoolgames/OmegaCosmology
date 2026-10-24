#!/usr/bin/env python3
"""Reproduce the unchanged finite quantum baseline in a fresh directory."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    source = root / "sources" / "quantum_continuation"
    script = source / "10_FINITE_QUANTUM_CONTINUATION_VERIFY.py"
    expected_file = source / "10_FINITE_QUANTUM_CONTINUATION_RESULTS.json"
    out = args.out_dir.resolve()
    if out.exists():
        parser.error("Output directory already exists. Choose a fresh directory.")
    if out.is_relative_to(source.resolve()):
        parser.error("Output must not be inside the source snapshot.")
    if args.timeout_seconds <= 0:
        parser.error("Timeout must be positive.")
    if not out.is_relative_to(root / "runs"):
        parser.error("Output must be inside this repository's runs directory.")
    out.mkdir(parents=True)
    try:
        subprocess.run(
            [sys.executable, str(script), "--out-dir", str(out)],
            check=True,
            timeout=args.timeout_seconds,
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"},
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}))
        return 1
    actual_file = out / expected_file.name
    expected = json.loads(expected_file.read_text(encoding="utf-8"))
    actual = json.loads(actual_file.read_text(encoding="utf-8"))
    digest = hashlib.sha256(script.read_bytes()).hexdigest()
    match = actual == expected
    passed = (
        match
        and actual.get("status") == "passed"
        and actual.get("checks_passed") == 233
        and actual.get("verification_script_sha256") == digest
    )
    report = {
        "status": "passed" if passed else "failed",
        "checks_passed": actual.get("checks_passed"),
        "matches_archived_json": match,
        "verification_script_sha256": digest,
        "python_version": platform.python_version(),
        "scope": "reproduces the finite worked instances; no new lushness result",
    }
    (out / "BASELINE_REPRODUCTION.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
