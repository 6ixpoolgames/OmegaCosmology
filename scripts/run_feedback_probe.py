"""Reproduce P001 into a fresh runs directory, leaving packaged sources unchanged."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from omega_cosmology.feedback_probe import Model, analyze


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    if out.exists() or not out.is_relative_to(ROOT / "runs"):
        parser.error("Choose a fresh output directory inside this repository's runs directory")
    fixture = ROOT / "research/probes/P001/fixture.json"
    objects, summary = analyze(Model.read(fixture))
    inputs = [fixture, ROOT / "src/omega_cosmology/feedback_probe.py", Path(__file__).resolve(),
              ROOT / "research/probes/P001/spec.md", ROOT / "tests/test_feedback_probe.py",
              ROOT / "sources/quantum_continuation/10_FINITE_QUANTUM_CONTINUATION_VERIFY.py"]
    summary["input_sha256"] = {str(p.relative_to(ROOT)).replace("\\", "/"): sha256(p.read_bytes()).hexdigest()
                               for p in inputs}
    summary["python_version"] = platform.python_version()
    out.mkdir(parents=True)
    for name, value in [("FULL_OBJECTS.json", objects), ("SUMMARY.json", summary)]:
        (out / name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(out), "policies_per_action": 64,
                      "residuals_per_action": 2,
                      "full_geometry_equal": summary["actions"][0]["descriptors"]["full"] == summary["actions"][1]["descriptors"]["full"],
                      "common_policy_witness": summary["common_policy_witness"]}, indent=2))


if __name__ == "__main__":
    main()
