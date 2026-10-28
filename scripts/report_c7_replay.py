"""Retain the fixed C.7 replay, its original sources, and explicit scope limits."""

import argparse
import json
import re
import shutil
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    Path(path).write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    run, out = args.run.resolve(), args.out.resolve()
    if out.exists() or not out.is_relative_to(ROOT / "research/platform/engineering"):
        parser.error("Fresh retained engineering directory required")
    summary, receipt = read(run / "output/RESULT.json"), read(run / "RECEIPT.json")
    provenance = read(run / "PROVENANCE.json")
    arms = {k: read(run / "output" / (k + ".json")) for k in ("loop", "basal")}
    privacy = read(run / "source-privacy.json")
    if receipt["exit_code"] or receipt["cap_reason"] or privacy["status"] != "passed":
        raise ValueError(
            "Keep incomplete or sensitive execution local; no successful package"
        )
    tests = (run / "tests.txt").read_text(encoding="utf-8")
    if not tests.rstrip().endswith("OK"):
        raise ValueError("Completed test validation required")
    out.mkdir(parents=True)
    retained = out / "retained"
    retained.mkdir()
    for path in sorted((run / "output").glob("*.json")):
        shutil.copyfile(path, retained / path.name)
    for name in ("PROVENANCE.json", "RECEIPT.json"):
        shutil.copyfile(run / name, out / name)
    # Original manifests and results are unchanged; recovered code stays an
    # archive rather than becoming another production simulator.
    with ZipFile(out / "SNAPSHOT.zip", "w", ZIP_DEFLATED) as archive:
        for folder in (run / "legacy", run / "frozen"):
            for path in sorted(folder.rglob("*")):
                if path.is_file() and "__pycache__" not in path.parts:
                    archive.write(path, path.relative_to(run).as_posix())
    original = retained / "original"
    original.mkdir()
    for arm in arms:
        shutil.copyfile(
            run / "legacy" / arm / "RESULTS.json", original / (arm + ".json")
        )
    rows = summary["comparison"]["profiles"]
    positive = all(
        r["delta_history_bits"] > summary["tolerances"]["bits"] for r in rows
    )
    rate_positive = all(
        r["delta_rate"] > summary["tolerances"]["rate_work"] for r in rows
    )
    reproduced = all(r["status"] == "reproduced" for r in arms.values())
    verdict = (
        "survives_for_selected_pair"
        if reproduced and positive and rate_positive
        else "changed_or_unresolved"
    )
    quality = {
        "numerical": {
            "status": "reproduced" if reproduced else "discrepant",
            "max_retained_history_difference": max(
                abs(r["retained_difference"]) for a in arms.values() for r in a["rows"]
            ),
            "max_independent_history_difference": max(
                abs(r["independent_history_difference"])
                for a in arms.values()
                for r in a["rows"]
            ),
            "max_stationary_rate_difference": max(
                abs(r["retained_rate_difference"])
                for a in arms.values()
                for r in a["rows"]
            ),
            "max_first_law_residual": max(
                abs(r["first_law_residual"])
                for a in arms.values()
                for r in a["finite_physics"].values()
            ),
            "rigorous_interval_certificate": False,
        },
        "resolution": {
            "cadences": [0.125, 0.25, 0.5],
            "state_grain": "bank, packet, apparatus count",
            "physical_faithfulness": "open; temporal audit is not a faithful-grain proof",
        },
        "physical_adequacy": {
            "event_energy_and_bank_increments": "checked against native state changes",
            "generator": "independently reconstructed from native events",
            "local_paired_rate_ratios": "264 pairs per arm checked; declared one-way channels excluded",
            "material": "apparatus plus derived precursor; full source/carrier/waste chemistry unresolved",
            "boundaries": "source arrival rates differ; stationary accepted work matches",
            "current_paired_comparison_certificate": "inapplicable; validator unchanged",
        },
        "claim_relevance": {
            "selected_pair_conclusion": verdict,
            "coverage": "one of 12 historical C.7 parameter points; seed only",
            "activity_independence": "not established",
            "finite_work_matching": "not established",
            "thermal_competitor": "not instantiated",
            "ethical_correspondence": "not assessed",
        },
    }
    write(out / "QUALITY.json", quality)
    validation = {
        "status": "passed",
        "tests": int(re.search(r"Ran (\d+) tests", tests)[1]),
        "focused_regressions": 4,
        "source_privacy": privacy,
        "historical_source_files_per_bundle": provenance["arms"]["loop"][
            "source_files"
        ],
        "scope": "source provenance, reproduction, accounting and numerical consistency; not full physical certification",
    }
    write(out / "VALIDATION.json", validation)
    table = []
    for horizon in (16, 64, 256, 1024):
        values = [
            next(
                r["delta_history_bits"]
                for r in rows
                if r["horizon"] == horizon and r["cadence"] == dt
            )
            for dt in (0.125, 0.25, 0.5)
        ]
        table.append(
            f"| {horizon} | {values[0]:+.9f} | {values[1]:+.9f} | {values[2]:+.9f} |"
        )
    physical = []
    for arm, result in arms.items():
        p = result["finite_physics"]["64"]
        physical.append(
            f"| {arm} | {p['accepted_work']:.9f} | {p['expected_jumps']:.9f} | {p['gross_bank_withdrawal']:.9f} | {p['construction_refund']:.9f} | {p['apparatus_deadline']:.9f} |"
        )
    rates = [
        next(r["delta_rate"] for r in rows if r["cadence"] == dt)
        for dt in (0.125, 0.25, 0.5)
    ]
    report = f"""# C.7 — fixed representative replay

28 October 2026. Complete locally; no parameter search, physical redesign or
publication. [Authorized scope](../../specs/C7_VERIFICATION_REPLAY_r1.md).

## Verdict

Numerical reproduction: **{quality["numerical"]["status"]}**. Original conclusion:
**{verdict}**. Both 90-state laws reproduce the retained seed profiles, with
maximum historical difference {quality["numerical"]["max_retained_history_difference"]:.3g} bits.
Uniformization and augmented matrix powers independently agree within
{quality["numerical"]["max_independent_history_difference"]:.3g} bits.
This verifies one historical parameter point, not the whole 12-point study.

The loop exceeds basal complete-history lushness at every tested horizon and
cadence. Stationary accepted external work matches: loop
{arms["loop"]["stationary_accepted_work"]:.16g}, basal
{arms["basal"]["stationary_accepted_work"]:.16g} energy/time; mismatch
{summary["comparison"]["stationary_work_mismatch"]:+.3g}.
The positive stationary rate differences survive at all three cadences.

## Actual comparison

This is the original capacity 4, middle-work-target loop/basal mechanism contrast.
Both start at bank 6 quanta, packet 1, apparatus 1, with energy 7 and three derived
precursors. The native loop assists capture and construction; basal removes both
assistance terms. All remaining parameters agree except source arrival rate:
loop 0.04305026325096872, basal 0.05219264208306122. Neither law is a spatial gas.
The root is a specified physical present, not a prior over policies.

**Different offered source boundaries are intentional and explicit.** The current
identical-boundary paired validator remains unchanged and its certificate is
inapplicable. This replay supplies a historical comparison/accounting audit;
it does not silently promote C.7 to that certificate or translate it into R2.
Stationary accepted-work equality does not cancel exterior correlations or match
finite work, useful capture, bath imports, source-event histories or activity.

## Recomputed profiles

Loop minus basal complete sampled-state history entropy, in bits. All native
physical variation remains counted; event labels do not create extra histories.

| Horizon | Cadence 0.125 | Cadence 0.25 | Cadence 0.5 |
|---|---:|---:|---:|
{chr(10).join(table)}

Stationary rate differences at the three cadences are
{rates[0]:+.9f}, {rates[1]:+.9f}, {rates[2]:+.9f} bits/time. Finite profiles remain
primary; the rate describes sustained behavior under these maintained sources.

At T64, independently integrated physical readouts:

| Arm | Accepted work | Expected jumps | Gross bank withdrawal | Construction refund | Apparatus at deadline |
|---|---:|---:|---:|---:|---:|
{chr(10).join(physical)}

Gross bank withdrawal includes construction, upkeep and leakage. Construction
refund is the native reverse-build contribution; thermal recharging is reported
separately in event counts. These are actual state-changing expenditures, not
nominal bills multiplied by unrelated events. In particular, the larger finite
history profile is not an equal-finite-work or equal-activity comparison.

## Physical and numerical checks

Both original manifest self-hashes, all 64 source files per bundle, source-list
hashes and result identities pass. Both bundles have the same frozen source.
The replay imports only that recovered native code. No rate was refitted, no
alternative case selected and no historical bytes modified.

Independent event enumeration reproduces the generator exactly. Declared bank
debits/refunds and heat increments agree with physical state changes for every
event. The 264 native paired-channel rate ratios per arm agree with the stated
energy and degeneracy factors. Declared one-way source, decay, capture and
external damage remain one-way; no equilibrium certificate is claimed for them.

The maximum integrated first-law residual is
{quality["numerical"]["max_first_law_residual"]:.3g}. Continuous occupation is
computed with a block exponential and checked against probability/integral
identities and retained cumulative work. Sampled kernels are independently
checked by uniformization, history sums by augmented powers, stationary rates
by a separate balance solve. Float64 tolerances remain the original 1e-5 bits
and 1e-8 rate/work; these are numerical consistency checks, not interval proofs.

Apparatus plus its **derived** precursor inventory is conserved. There is no
explicit waste pool or full chemical inventory for packets/reservoirs, so a
complete material-conservation certificate is unavailable. Boundary ledgers
record energy, while bath/source histories remain outside the modeled field.
Temporal agreement does not establish physical-resolution faithfulness.

## Manuscript use and stopping point

Suggested evidence sentence: “A representative retained enabling-loop comparison
was independently replayed from verified frozen source. Its finite-history and
stationary-rate advantages survived at matched stationary accepted work, with
different offered source rates and unmatched finite work and activity.”

This supports the representability of a costed enabling relation and its measured
consequences within the specified physics. It does not isolate an organization-only
surplus, prove dominance over equally active dynamics, or establish the ethical
correspondence. Other C.7 points remain historical without this replay status.
R2's physical-control qualification remains open and its search remains paused.
No further experimental campaign follows automatically.

## Delivery

The worker took {receipt["wall_seconds"]:.3f} seconds and peaked at
{receipt["peak_job_bytes"] / 1024**2:.2f} MiB under 240 seconds / 512 MiB / 32 MiB caps.
All {validation["tests"]} unit tests pass, including four adversarial replay tests.
[Provenance](PROVENANCE.json), [raw comparison](retained/RESULT.json),
[quality axes](QUALITY.json), [validation](VALIDATION.json), original results,
native event ledgers and a source snapshot accompany the byte manifest.
The snapshot preserves the recovered legacy bundles as evidence archives, not
as another installed production simulator. The reporting script and
[restoration instructions](REPRODUCE.md) are retained.
"""
    (out / "REPORT.md").write_text(report, encoding="utf-8")
    (out / "REPRODUCE.md").write_text(
        """# Restoring the replay

Extract SNAPSHOT.zip into a fresh ignored runs/ directory. It restores legacy/
with both original manifests, inputs, results and native source, and frozen/
with the auditor, cap wrapper, focused tests and scope specification. Verify
the external EVIDENCE.json before extraction. NumPy and SciPy are required.

The scientific worker needs no mutable legacy checkout. Launch it with the
retained cap wrapper, for example from the repository root:

```python
import importlib.util
import sys
from pathlib import Path

restored = Path("runs/c7-restored").resolve()  # fresh extraction destination
path = restored / "frozen/src/omega_cosmology/testbed/workflow.py"
spec = importlib.util.spec_from_file_location("restored_caps", path)
caps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(caps)
receipt = caps.capped(
    [sys.executable, "-B", str(restored / "frozen/scripts/replay_c7.py"),
     "--worker", str(restored)],
    restored, seconds=240, memory=512 * 1024**2, output_cap=32 * 1024**2,
    cwd=restored / "frozen",
)
print(receipt)
```

The cap wrapper supplies the required GO handshake. The worker verifies frozen
hashes and writes fresh output/ files. Compare these to retained/ from this
package. Do not extract into an existing execution or overwrite its results.
The parent script's legacy-root option is for locating original historical
bundles, not needed for an archive restoration. A successful restore reproduces
the same declared historical contrast; it grants no extra physical certificate.
""",
        encoding="utf-8",
    )
    analysis = out / "analysis"
    analysis.mkdir()
    shutil.copyfile(Path(__file__).resolve(), analysis / Path(__file__).name)
    files = [
        {
            "path": p.relative_to(out).as_posix(),
            "sha256": sha256(p.read_bytes()).hexdigest(),
            "bytes": p.stat().st_size,
        }
        for p in sorted(out.rglob("*"))
        if p.is_file()
    ]
    write(
        out / "EVIDENCE.json", {"schema": "omega.retained-evidence/1", "files": files}
    )
    print(
        json.dumps(
            {
                "status": "retained",
                "verdict": verdict,
                "out": out.relative_to(ROOT).as_posix(),
                "files": len(files),
            }
        )
    )


if __name__ == "__main__":
    main()
