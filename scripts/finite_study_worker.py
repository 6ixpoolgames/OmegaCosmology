"""Thin generic worker for a frozen finite-study protocol."""

import sys

if __name__ == "__main__" and sys.stdin.readline().strip() != "GO":
    raise SystemExit("Runner GO gate required")


def main():
    import argparse
    import json
    import platform
    from hashlib import sha256
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", required=True)
    parser.add_argument("--law", required=True)
    parser.add_argument("--cadence", required=True, type=float)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "src"))
    manifest_path = root / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for row in manifest["files"]:
        if sha256((root / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            raise RuntimeError("Frozen input changed")
    protocol = json.loads((root / args.protocol).read_text(encoding="utf-8"))
    if args.cadence not in protocol["cadences"]:
        raise ValueError("Undeclared cadence")
    if (
        "case_grid" in protocol
        and [args.law, args.cadence] not in protocol["case_grid"]
    ):
        raise ValueError("Undeclared law/cadence case")
    import numpy as np
    import scipy

    from omega_cosmology.testbed.finite_study import evaluate_case

    result = evaluate_case(
        protocol, next(l for l in protocol["laws"] if l["id"] == args.law), args.cadence
    )
    result["manifest_sha256"] = sha256(manifest_path.read_bytes()).hexdigest()
    result["dependencies"] = {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }
    (args.out_dir / "RESULT.json").write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "law": args.law,
                "states": result["states"],
                "rows": len(result["rows"]),
                "worker_seconds": result["worker_seconds"],
            }
        )
    )


if __name__ == "__main__":
    main()
