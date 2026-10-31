"""Publishable local report for scoped inventory and alphabet qualification."""

import argparse
import json
import shutil
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def write(p, v):
    Path(p).write_text(
        json.dumps(v, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--evidence-dir", type=Path, required=True)
    a = p.parse_args()
    out = a.evidence_dir.resolve()
    if (
        not out.is_relative_to(ROOT / "research/platform/engineering")
        or (out / "REPORT.md").exists()
    ):
        p.error("Fresh retained engineering output required")
    receipt, plan = read(out / "BATCH_RECEIPT.json"), read(out / "PLAN.json")
    initial = out.parent / "paired-qualification-2026-10-30"
    if read(initial / "PLAN.json") != plan:
        raise ValueError("Engineering refresh changed registered physical inputs")
    cases = [
        read(out / "retained" / study["id"] / "RESULT.json")
        for study in plan["studies"]
    ]
    table, summary = [], []
    rows, checks, max_difference, max_energy = 0, 0, 0.0, 0.0
    for case in cases:
        original = read(initial / "retained" / case["study"] / "RESULT.json")
        if case["contrasts"] != original["contrasts"]:
            raise ArithmeticError("Guard refresh changed a scientific score")
        checks += len(case["paired_checks"])
        if any(
            pair["certificate"]["status"] != "validated_paired_comparison"
            for pair in case["paired_checks"]
        ):
            raise ValueError("Paired qualification incomplete")
        for arm in case["arms"]:
            for row in arm["rows"]:
                rows += 1
                max_difference = max(
                    max_difference, abs(row["difference_from_P0_bits"])
                )
                max_energy = max(max_energy, abs(row["physical"]["energy_residual"]))
        t16, t64 = [
            next(r["delta_bits"] for r in case["contrasts"] if r["horizon"] == T)
            for T in (16, 64)
        ]
        inventories = case["arms"][0]["inventory_on_every_reachable_state"]
        info = {
            "study": case["study"],
            "states": [a["state_count"] for a in case["arms"]],
            "declared_retained_counts": inventories,
            "paired_checks": len(case["paired_checks"]),
            "contrasts": case["contrasts"],
            "source_laws_and_event_ledgers_unchanged": all(
                a["native_generator_difference"] == 0 and a["native_ledger_unchanged"]
                for a in case["arms"]
            ),
        }
        summary.append(info)
        table.append(
            f"|{case['study']}|{', '.join(map(str, info['states']))}|{len(case['paired_checks'])}|{t16:+.9f}|{t64:+.9f}|"
        )
    peak = max(j["receipt"]["peak_job_bytes"] for j in receipt["jobs"])
    write(
        out / "SUMMARY.json",
        {
            "status": receipt["status"],
            "studies": summary,
            "native_arm_profile_rows": rows,
            "paired_checks": checks,
            "max_history_change_from_P0_bits": max_difference,
            "max_integrated_first_law_residual": max_energy,
            "peak_job_bytes": peak,
            "wall_seconds": receipt["wall_seconds"],
            "legacy_P0_status": "unchanged: literal historical material/mapping inputs remain inapplicable",
            "inventory_scope": "explicit retained-unit model interpretation, not chemical closure",
        },
    )
    write(
        out / "QUALITY.json",
        {
            "numerical": "Native state space/Q/event marks and checked histories unchanged; float64 physical residuals, not verified rounding bounds",
            "resolution": "cadence .25; T16/T64; same full count-state observations; physical faithfulness open",
            "physical_adequacy": "Explicit fixed-retained-unit interpretation of original declarations; chemical formulas, atomic/waste/bath closure and omitted hardware remain unresolved",
            "claim_relevance": "Typed paired comparability of interpreted versions; does not repair original physical limitations or establish ethical correspondence",
            "latest_Appendix_AB": "not asserted: current revisions not supplied",
        },
    )
    text = [
        "# Paired qualification after P0 — interpreted inputs",
        "",
        "30 October 2026. Bounded local engineering, not a new physical campaign. No manuscript edits, commit or push.",
        "",
        f"**All six studies pass {checks} scoped paired checks** at cadence .25 and T16/T64. All {rows} checked native arm-history values match P0 without change. Every interpreted law retains its original reachable states, transition rates, event marks and Hamiltonian.",
        "",
        "## What changed",
        "",
        "Original fixed-component assumptions are now explicit executable state partitions: a named unit remains present in every precursor/working or charged/spent state. The interpreter preserves every original material declaration, adds its finite inventory function, records the physical state meanings and gives the interpreted input a new fingerprint. It rejects partial partitions, repeated slots, wrong original quantities and replacing an existing executable inventory. An energy bank or bond cannot be recast as new matter to pass.",
        "",
        "This is NOT a chemical closure certificate. It checks the declared retained units only. Atomic composition, unmodeled waste or bath material, and omitted environment/register hardware are not inferred. The state meanings are an explicit interpretation of the old model assumptions; they are not discoveries made by counting. Counts are positive in these cases and checked on every enumerated state and event pair.",
        "",
        "R2 has 180 useful-capacity states and 150 sham states. The sham additionally forbids bank >=5. A hash-bound mapping puts their native states into a common observation alphabet, declaring precisely that constraint difference. It changes neither law. The missing 30 symbols have zero weight for the sham; they receive no physical transitions or self-loops. Injective relabelling preserves every finite native word probability and its entropy. A one-step numerical check and an independent tiny exhaustive three-step test exercise this identity.",
        "",
        "The ordinary validator remains strict without a mapping. Mapping cannot waive root, energy, material, source, observation, resolution or horizon checks, and applies only to full-state mechanism contrasts in this adapter. Material-required validation rejects absent inventories and empty term sets. Duplicate native symbols cannot silently merge under a mapping.",
        "",
        "## Signed results preserved",
        "",
        "Differences in complete-history bits; S4b is the four-arm interaction, not a simple two-law effect.",
        "",
        "|Study|Native states per arm|Paired checks|Delta T16|Delta T64|",
        "|---|---|---:|---:|---:|",
        *table,
        "",
        f"Maximum change from P0: {max_difference:.3g} bits. Maximum integrated first-law residual: {max_energy:.3g}. The negative early S4b interaction is retained; qualification does not depend on the ranking sign.",
        "",
        "## Relationship to earlier evidence",
        "",
        "The P0 literal-input rejection statuses and all original bytes remain unchanged. These are explicitly interpreted versions with their own fingerprints and certificates, not retroactive certificates attached to the old source. Native-generator and marked-event equivalence connects the new interpretation to the old numerical law. This does not promote a selected point to its whole parameter map or certify newer manuscript Appendix B conformance.",
        "",
        "R2's load spill/maintenance/ancestry limitations remain. E1/S3 are finite count worlds, not spatial or open-ended ecologies; S3's early donor/whole opposition and unresolved late private signs retain their earlier scope. S4's weak sensor is still weak. S4b's paid-response and turnover caveats remain. No cost, random variation, event or unfavorable result was removed.",
        "",
        "Matched: actual starting energy, scoped retained-unit counts, physical coordinate interpretation, declared source/bath prescriptions, observation and window. Unmatched: realized accepted work and event activity. Exterior bath/source histories remain unresolved. This does not qualify the separate activity/work comparator or establish any ethical ranking.",
        "",
        "## Engineering history, resources and reproduction",
        "",
        "An initial passing checkpoint is retained [separately](../paired-qualification-2026-10-30/REPORT.md). Two additional negative-case guards were added for empty inventory term sets and aliasing native labels. This refreshed run uses exactly the same registered input plan and no changed physical parameter, tolerance or selection; its signed results match the initial checkpoint. Both source versions and outcomes remain available.",
        "",
        f"Wall time {receipt['wall_seconds']:.2f} seconds; peak job memory {peak / 1024**2:.2f} MiB. Six sequential capped jobs. [PLAN.json](PLAN.json), [SUMMARY.json](SUMMARY.json), [QUALITY.json](QUALITY.json), receipts, native/ interpreted fingerprints and a complete frozen snapshot accompany this report.",
        "",
        "Restore SNAPSHOT.zip with scripts/restore_research_snapshot.py into a fresh runs/<name>/frozen directory. Copy the retained PLAN.json into runs/<name>/PLAN.json, verifying it against MANIFEST.json's plan hash. Use the driver version recorded in that snapshot to dispatch the frozen worker under the retained caps. Restoration itself runs no simulation. All expected P0 rows and native Q exports are embedded; no private historical cache is required.",
        "",
        "Further activity-control, irreversible-damage, spatial or social work remains separately scoped. No automatic publication, manuscript edit or broader certificate follows.",
        "",
    ]
    (out / "REPORT.md").write_text("\n".join(text), encoding="utf-8")
    analysis = out / "analysis"
    analysis.mkdir()
    shutil.copyfile(Path(__file__), analysis / Path(__file__).name)
    write(
        out / "EVIDENCE.json",
        {
            "schema": "omega.paired-qualification-evidence/1",
            "files": [
                {
                    "path": f.relative_to(out).as_posix(),
                    "bytes": f.stat().st_size,
                    "sha256": sha256(f.read_bytes()).hexdigest(),
                }
                for f in sorted(out.rglob("*"))
                if f.is_file() and f.name != "EVIDENCE.json"
            ],
        },
    )
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "paired_checks": checks,
                "history_rows": rows,
                "history_change": max_difference,
                "peak_MiB": peak / 1024**2,
            }
        )
    )


if __name__ == "__main__":
    main()
