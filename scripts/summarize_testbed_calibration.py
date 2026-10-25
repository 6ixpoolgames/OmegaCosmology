"""Promote compact verified engineering evidence; retain no dense arrays."""

import argparse
import json
import re
import shutil
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument(
        "--workspace-check",
        type=Path,
        help="Optional passed check_workspace run; retained commands omit local paths",
    )
    args = parser.parse_args()
    run, out = args.run_dir.resolve(), args.out_dir.resolve()
    if not run.is_relative_to(ROOT / "runs") or not out.is_relative_to(
        ROOT / "research/platform/engineering"
    ):
        parser.error(
            "Use a run under runs/ and output under research/platform/engineering/"
        )
    sources = {
        "SOURCE_MANIFEST.json": run / "frozen/MANIFEST.json",
        "RECEIPT.json": run / "RECEIPT.json",
        "SUMMARY.json": run / "calibration/SUMMARY.json",
    }
    receipt = json.loads(sources["RECEIPT.json"].read_text(encoding="utf-8"))
    summary = json.loads(sources["SUMMARY.json"].read_text(encoding="utf-8"))
    manifest = json.loads(sources["SOURCE_MANIFEST.json"].read_text(encoding="utf-8"))
    if (
        receipt["status"] != "passed"
        or summary["status"] != "passed"
        or receipt["summary_sha256"] != digest(sources["SUMMARY.json"])
        or receipt["manifest_sha256"] != digest(sources["SOURCE_MANIFEST.json"])
        or summary["manifest_sha256"] != receipt["manifest_sha256"]
    ):
        raise RuntimeError("Calibration receipts do not verify")
    for row in manifest["files"]:
        path = run / "frozen" / row["path"]
        if digest(path) != row["sha256"] or path.stat().st_size != row["bytes"]:
            raise RuntimeError("Snapshot mismatch: " + row["path"])
    out.mkdir(parents=True, exist_ok=True)
    extra_files = []
    workspace_note = "Full workspace reproduction is recorded separately when supplied to the report generator."
    if args.workspace_check:
        check_dir = args.workspace_check.resolve()
        if not check_dir.is_relative_to(ROOT / "runs"):
            parser.error("Workspace check must be under runs/")
        check_source = check_dir / "CHECKS.json"
        check = json.loads(check_source.read_text(encoding="utf-8"))
        if check["status"] != "passed":
            raise RuntimeError("Workspace check did not pass")
        for item in check["checks"]:
            item["command"][0] = "<PYTHON>"
            item["command"] = [s.replace(str(ROOT), "<REPO>") for s in item["command"]]
        check["representation"] = {
            "type": "redacted_derivative",
            "source_sha256": digest(check_source),
            "changes": "Interpreter and repository absolute paths replaced by placeholders; results unchanged",
        }
        (out / "WORKSPACE_CHECK.json").write_text(
            json.dumps(check, indent=2) + "\n", encoding="utf-8"
        )
        tests = (check_dir / "tests.txt").read_text(encoding="utf-8")
        (out / "TESTS.txt").write_text(tests, encoding="utf-8")
        count = re.search(r"Ran (\d+) tests", tests)
        workspace_note = (
            f"Full workspace check passed: {count[1] if count else 'see log'} unit tests, "
            "archive/source/link integrity, retained finite baseline and exact P001 reproduction. "
            "See [WORKSPACE_CHECK.json](WORKSPACE_CHECK.json) and [TESTS.txt](TESTS.txt). "
            "Local interpreter/repository paths are redacted, with the original receipt hash retained."
        )
        extra_files = ["WORKSPACE_CHECK.json", "TESTS.txt"]
    for name, source in sources.items():
        shutil.copyfile(source, out / name)
    memory_probe = json.loads(
        (run / "cap-memory/worker.log").read_text(encoding="utf-8")
    )
    (out / "MEMORY_PROBE.json").write_text(
        json.dumps(memory_probe, indent=2) + "\n", encoding="utf-8"
    )
    live_match = all(
        (ROOT / r["path"]).is_file() and digest(ROOT / r["path"]) == r["sha256"]
        for r in manifest["files"]
    )
    cases = summary["models"]
    rows = "\n".join(
        f"| {c['id']} | {c['states']} | {c['directed_mechanism_events']} | "
        f"{c['query']['ell_bits']:.9f} | {c['thermodynamics']['energy_residual']:.2e} |"
        for c in cases
    )
    timings = "\n".join(
        f"| {c['id']} | {c['timings_seconds']['enumeration_including_symmetry_checks']:.4f} | "
        f"{c['timings_seconds']['sampled_kernel_and_support']:.4f} | "
        f"{c['timings_seconds']['continuous_propagation_and_occupation']:.4f} | "
        f"{c['timings_seconds']['history_queries_and_direct_word_audit']:.4f} | "
        f"{c['timings_seconds']['sampler_1000_paths']:.4f} |"
        for c in cases
    )
    cap = receipt["calibration"]
    max_chain = max(c["chain_rule_residual"] for c in cases)
    max_prop = max(c["independent_occupation_residual"] for c in cases)
    report = f"""# M0–M2 first engineering report

24 October 2026. **PASS for the implemented finite classical engineering slice.**
No new scientific survey, ethical conclusion or r20 conformance is claimed.
The preparation archive was already pushed at e2da4f1; this implementation and
its evidence are local and uncommitted.

## Scope delivered

Six serializable semantic records, one local reversible physical kernel,
explicit finite symmetries, complete reachable enumeration, shared-law event
sampling, channel-resolved work/heat, full sampled-history queries, finite
projected word propagation, structural support, named-refinement diagnostics
and small irreducible rate/offset calculations. R1 and R2 are concrete same-
grammar construction examples, not scientific demonstrations of compounding.

## Capped source-frozen execution

- Worker wall time: {summary["worker_seconds"]:.3f} seconds; supervised wall time: {cap["wall_seconds"]:.3f} seconds.
- Reported peak job commitment: {cap["peak_job_bytes"] / 1024**2:.2f} MiB under a {cap["job_memory_cap_bytes"] / 1024**3:.0f}-GiB limit.
- Wall budget: {cap["wall_cap_seconds"]} seconds. Output budget: 32 MiB; measured output including snapshot: {cap["output_bytes"]:,} bytes.
- Timeout probe terminated the process tree. The 64-MiB memory probe refused
  further allocation after retaining {memory_probe["payload_bytes_retained"] / 1024**2:.0f} MiB of payload.
  Windows peak commitment counters can include refused allocation attempts;
  they are not resident-set measurements.
- {len(manifest["files"])} frozen inputs verified before/after execution; current input bytes match: **{live_match}**.
- Python {summary["python"]}, NumPy {summary["numpy"]}, SciPy {summary["scipy"]}.

The launcher/cap helper matched the snapshot before launch; the calibration
worker imported its implementation from that snapshot. Signed transfer plans,
machine credentials and home paths are not included in the retained evidence.

## Numerical and physical checks

| World | Reachable states | Directed mechanism events | ell at T16, dt=.25 (bits) | First-law residual |
|---|---:|---:|---:|---:|
{rows}

R0 has 30 nominal configurations but 18 in the root's conserved bank-parity
sector. R1/R2 contain 75/180 admissible reachable states. These rows have
different laws and material inventories; they are **not** an organized-versus-
disordered or capability ranking.

All source-off Gibbs/detailed-balance checks pass. Independent dense block
exponentials agree with sparse endpoint/occupation propagation; maximum
occupation residual is {max_prop:.2e}. Direct short-word entropy agrees with the
chain rule, maximum residual {max_chain:.2e}. All sampled supports are positive
on their enumerated sectors. Unresolved degeneracy creates no extra histories.

Each world has 1,000 seeded trajectories checked against exact endpoint and
expected-jump predictions, with the declared six-sigma calibration envelopes;
every sampled path closes its energy account. This is statistical sampler
validation, not a sampled history-entropy estimator or proof of exactness.

The calibration also records {len(summary["reference_cases"])} finite reference cases. Focused tests add
same-law rate/offset checks, mid-history identity invariance, support under
exponential underflow, mutable-compilation rejection and invalid-projection
rejection. See the [formal map](../../../../formal/verification/reference-suite-r1.md)
for inspected source versions, guarantees and pending cases.

## Profile

| World | Enumeration + symmetry (s) | Sampled kernel + support (s) | Continuous propagation (s) | Entropy + word audit (s) | 1,000 paths (s) |
|---|---:|---:|---:|---:|---:|
{timings}

The summary additionally separates root rule-matching and canonicalization
microbenchmarks, equilibrium and other physical audits. Enumeration includes
its matching/symmetry work; these columns are not a disjoint call-graph profile.
At this size repeated event matching in the sampler dominates. For larger
worlds dense sampled kernels scale quadratically in storage, and projected
word enumeration can grow exponentially in horizon. Faster hardware does not
remove either limitation. No large-state scaling claim follows from this run.

## What remains outside this slice

{workspace_note}

Sufficiency and physical faithfulness are declared assumptions, not empirical
certificates. Baths/sources have accounting but unresolved histories, so the
scope is the whole modeled field with no exterior cancellation claim. Numerical
results are float64 with checked residuals, not rigorous interval certificates.

Not yet implemented: general stoichiometric conservation sectors, spatial or
delayed transport, generic graph matching, dynamic population ecology,
three-generation path witnesses, optimizer/controller physics, large projected
entropy bounds, reducible-class asymptotics, quantum record families and
arbitrary present sections. Process-comparison metadata is an example contract,
not an implemented policy search. These remain explicit expansion points.

## Next step and reconstruction

The [R1 proposal](../../../studies/R1-constructed-access-PROPOSAL.md) compares
costed access and reconstruction against explicitly declared baselines. It has
not been launched. The [engineering decisions](ENGINEERING_DECISIONS.md) and
[worked models](../../models/README.md) justify the foundation.

From the repository root, install `.[testbed]`, rebuild model JSON with
`python scripts/write_testbed_fixtures.py`, and run
`python scripts/run_testbed_calibration.py --out-dir runs/calibration-fresh`.
Promote a verified run with `scripts/summarize_testbed_calibration.py`.
Exact bytes/hashes of this run are in [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json),
[RECEIPT.json](RECEIPT.json) and [SUMMARY.json](SUMMARY.json). Numerical results
should agree within declared tolerances across supported libraries; timing and
allocation counters need not match. Full ignored snapshot: `{run.relative_to(ROOT).as_posix()}/frozen`.

No commit, push, broad science run or external upload follows automatically.
"""
    (out / "ENGINEERING_REPORT.md").write_text(report, encoding="utf-8")
    retained = [*sources, "MEMORY_PROBE.json", "ENGINEERING_REPORT.md", *extra_files]
    evidence = {
        "schema": "omega.engineering-evidence/1",
        "status": "verified",
        "run": run.relative_to(ROOT).as_posix(),
        "report_generator_sha256": digest(Path(__file__)),
        "current_inputs_match_snapshot": live_match,
        "files": [
            {
                "path": name,
                "sha256": digest(out / name),
                "bytes": (out / name).stat().st_size,
            }
            for name in retained
        ],
    }
    (out / "EVIDENCE.json").write_text(
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": "verified",
                "models": len(cases),
                "source_inputs": len(manifest["files"]),
                "current_inputs_match_snapshot": live_match,
                "retained_bytes": sum(r["bytes"] for r in evidence["files"]),
            }
        )
    )


if __name__ == "__main__":
    main()
