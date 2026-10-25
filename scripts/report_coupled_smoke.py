"""Verify and retain capped engineering evidence, without scientific rankings."""

import argparse
import json
import shutil
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    run, out = args.run_dir.resolve(), args.out_dir.resolve()
    if (
        not run.is_relative_to(ROOT / "runs")
        or not out.is_relative_to(ROOT / "research/platform/engineering")
        or out.exists()
    ):
        parser.error("Use a run under runs/ and a fresh engineering evidence directory")
    receipt = json.loads((run / "BATCH_RECEIPT.json").read_text())
    manifest_path = run / "frozen/MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())
    plan_path = run / "frozen" / manifest["plan"]
    plan = json.loads(plan_path.read_text())
    if (
        receipt["status"] != "passed"
        or not receipt["engineering_only"]
        or receipt["source_manifest_sha256"] != digest(manifest_path)
        or receipt["plan_sha256"] != digest(plan_path)
    ):
        raise RuntimeError("Complete source-frozen engineering evidence required")
    for row in manifest["files"]:
        if digest(run / "frozen" / row["path"]) != row["sha256"]:
            raise RuntimeError("Frozen input/source mismatch")
    results = {}
    for c in receipt["cases"]:
        path = run / c["id"] / "RESULT.json"
        result = json.loads(path.read_text())
        if (
            not c["passed"]
            or digest(path) != c["result_sha256"]
            or result["source_manifest_sha256"] != receipt["source_manifest_sha256"]
        ):
            raise RuntimeError("Case provenance mismatch")
        results[c["id"]] = result
    if set(results) != {c["id"] for c in plan["cases"]}:
        raise RuntimeError("Incomplete engineering plan")
    table = ["| Case | States | Seconds | Peak MiB |", "|---|---:|---:|---:|"]
    locals_table = ["| Case / scope | T16 m1 width | T16 m2 width |", "|---|---:|---:|"]
    depth_table = [
        "| Case / scope | P(ever depth >=3), T16 | Expected births depth >=3 | Query states |",
        "|---|---:|---:|---:|",
    ]
    errors = []
    for c in receipt["cases"]:
        result = results[c["id"]]
        table.append(
            f"| {c['id']} | {result['states']} | {c['receipt']['wall_seconds']:.3f} | {c['receipt']['peak_job_bytes'] / 1024**2:.2f} |"
        )
        row = max(result["rows"], key=lambda r: r["horizon"])
        for name, value in row["projected_histories"].items():
            if name.endswith(".m2"):
                one = row["projected_histories"][name[:-1] + "1"]
                locals_table.append(
                    f"| {c['id']} / {name[:-3]} | {one['width_bits']:.6g} | {value['width_bits']:.6g} |"
                )
        for name, value in row["assistance_ancestry"].items():
            depth_table.append(
                f"| {c['id']} / {name} | {value['ever_reached_depth_probability']:.8g} | {value['expected_assisted_births_by_depth']['3']:.8g} | {value['query_states']} |"
            )
        for r in result["rows"]:
            errors.append(abs(r["physical"]["energy_residual"]))
    report = f"""# Coupled autocatalytic engineering smoke

25 October 2026. Five cases and ten full-profile queries complete. This is a
physics/analysis/computational smoke, not a parameter survey or a scientific
ranking of ecological strategies. Original R2-v1 evidence is unchanged.
Specification: [engineering slice](../../specs/COUPLED_AUTOCATALYTIC_SLICE_SPEC_r1.md).

## What was exercised

{chr(10).join(table)}

Cadence .25; horizons 4 and 16. Total {receipt["wall_seconds"]:.3f} s, peak
{max(c["receipt"]["peak_job_bytes"] for c in receipt["cases"]) / 1024**2:.2f} MiB,
run output {receipt["output_bytes"]:,} bytes. Largest shared-pair case gated the
rest. Caps: 150 s/3 GiB/32 MiB per case; 600 s/128 MiB batch.

## Physical changes

R2-v2 adds store breakdown/spill at every load and bound-constituent damage
independent of bank. It removes the dissipative-only rule named upkeep. Paid
activation restores damaged constituents; native thermal substitutes remain.
Payment is not made logically necessary. Full-bank storage no longer has
protection through lack of refund space along every breakdown path.

The new blocks compose costed component cycles, distinct banks and one finite
shared carrier. Capturing it changes the other group's opportunity. Additional
cross-assistance uses recipient energy. Every channel has its paired reverse,
source-off Gibbs checks pass, and maximum first-law residual is {max(errors):.2e}.
No conditional moral reward, noise subtraction or activity normalization is used.

## Local histories are actually projected histories

Conditional history of each group's components and bank is bounded under the
known full present. The shared carrier stays in the whole model and is hidden
from these local observations. Finite-memory bounds retain hidden state and
do not assume the projection is Markov. Widths, in bits:

{chr(10).join(locals_table)}

The lower conditions on an older hidden boundary state plus observed memory;
the upper conditions on observed memory only. Increasing memory is checked to
tighten both. Tiny exhaustive hidden-Markov word laws independently validate
the inequalities. These are float64 evaluations of analytic bounds, not rigorous
interval arithmetic. Positive width is unresolved information, not a local score
estimate. No private/whole conflict or optimal policy is inferred from this smoke.

## Connected native assistance ancestry

{chr(10).join(depth_table)}

Initial instances have depth zero. Newly constructed children can become parents;
basal or unlisted reconstruction resets depth, and loss ends the instance.
Query-only labels preserve the physical marginal. This is actual connectivity
in declared native marked channels, not merely event order. The last count bin
means >=3 and counts assisted births, not independent chains. Small probabilities
at T16 are neither a theory failure nor evidence of long-horizon robustness.

Coupled-case monitors track within-group ancestry. Cross-group assistance
is conservatively treated as an unlisted birth for that local genealogy; the
query is not a complete cross-community pedigree. The one-group three-member
case follows the full local cycle. No material/energy packet ancestry is claimed.

## Boundaries and next assessment

Contacts, banks and slots are fixed; no general population or transport is
represented. Banks are existing local infrastructure, not free new storage.
Capture, construction and damage coefficients are stipulated. Native capture
and thermal repair remain, so these are assisted routes, not exclusive channels.
The reversible source can receive returned work during a transient; source-on
does not guarantee net accepted work at every short horizon. All histories of
source/bath variables outside the model remain unresolved.

The one-group and two-group cases have different inventories and are not
matched competitors. Pair cases share an initial endowment; adding helper
channels or removing source channels changes the law. Mutualism, parasitism,
competition outcomes, repayment windows and ethical correspondence are not
established here. Horizon 16 is a smoke window, not a claim of sufficient
scientific duration. Parameter/cost/source-lifetime maps and matched preparations
are next study design work, after assessing these physical assumptions.

No commit, push or upload performed. All exact input/result hashes are retained;
no dense kernels, generated paths or genealogy-state arrays are stored.
"""
    out.mkdir(parents=True)
    (out / "cases").mkdir()
    for c in receipt["cases"]:
        shutil.copyfile(
            run / c["id"] / "RESULT.json", out / "cases" / (c["id"] + ".json")
        )
    for name, path in [
        ("ENGINEERING_PLAN.json", plan_path),
        ("SOURCE_MANIFEST.json", manifest_path),
        ("BATCH_RECEIPT.json", run / "BATCH_RECEIPT.json"),
    ]:
        shutil.copyfile(path, out / name)
    (out / "REPORT.md").write_text(report, encoding="utf-8")
    evidence = {
        "schema": "omega.coupled-smoke-evidence/1",
        "report_generator_sha256": digest(Path(__file__)),
        "files": [
            {
                "path": p.relative_to(out).as_posix(),
                "sha256": digest(p),
                "bytes": p.stat().st_size,
            }
            for p in sorted(out.rglob("*"))
            if p.is_file()
        ],
    }
    (out / "EVIDENCE.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": "verified",
                "cases": len(results),
                "profiles": sum(len(r["rows"]) for r in results.values()),
            }
        )
    )


if __name__ == "__main__":
    main()
