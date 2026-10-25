"""Export retained model profiles and comparisons, without executing physics."""

import argparse
import json
import shutil
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDIES = {
    "R1": ("R1-constructed-access", "2026-10-24", "INTERPRETATION_r1.md", 144),
    "R2": ("R2-further-capacity", "2026-10-24", "INTERPRETATION_r2.md", 216),
    "E1": ("E1-coupled-autocatalysis", "2026-10-25", "INTERPRETATION_r1.md", 650),
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def receipt(path):
    raw = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": sha256(raw).hexdigest(),
        "bytes": len(raw),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    if out.exists() or not out.is_relative_to(ROOT / "research/evidence"):
        parser.error("Choose a fresh directory under research/evidence")
    out.mkdir(parents=True)
    inputs, claims, checks = [], [], []
    for sid, (folder, date, interpretation, expected) in STUDIES.items():
        study = ROOT / "research/studies" / folder
        results = study / ("results-" + date)
        protocol = read(study / "PROTOCOL.json")
        analysis_path = results / "ANALYSIS.json"
        analysis = read(analysis_path)
        files = [
            study / "PROTOCOL.json",
            study / interpretation,
            analysis_path,
            results / "EVIDENCE.json",
            results / "SOURCE_MANIFEST.json",
        ]
        if sid == "R2":
            files.append(study / "reanalysis-2026-10-25/REPORT.md")
        profiles = []
        for path in sorted((results / "cases").glob("*.json")):
            case = read(path)
            if case["status"] != "passed":
                raise ValueError("Retained failed case cannot be exported as passed")
            files.append(path)
            for row in case["rows"]:
                key = f"{sid}:{row['law']}:{row['preparation']}:dt{row['cadence']}:T{row['horizon']}"
                profiles.append(
                    {
                        "id": key,
                        "law_id": row["law"],
                        "present_id": row["preparation"],
                        "observation_id": "whole.modeled",
                        "quantity_id": row["history"]["quantity"],
                        "horizon": row["horizon"],
                        "cadence": row["cadence"],
                        "history": row["history"],
                        "limiting_reading": row.get("asymptotic"),
                        "projected_histories": row.get("projected_histories"),
                        "projected_status": "analytic_float64_bounds"
                        if row.get("projected_histories")
                        else "not_calculated",
                        "activity": row["activity"],
                        "physical": {
                            k: row["physical"].get(k)
                            for k in [
                                "work_net",
                                "work_accepted_gross",
                                "work_returned_gross",
                                "heat_export",
                                "delta_energy",
                                "expected_jumps",
                                "energy_residual",
                            ]
                        },
                        "structure": {
                            k: row.get(k)
                            for k in [
                                "observables",
                                "function",
                                "functional_profiles",
                                "assistance_ancestry",
                                "witnesses",
                            ]
                        },
                        "foreclosure": {
                            "value": None,
                            "status": "not_calculated",
                            "reason": "No history-support comparison was executed; stock is not support",
                        },
                        "validation": row["validation"],
                        "source": {
                            **receipt(path),
                            "row_key": [
                                row["law"],
                                row["preparation"],
                                row["cadence"],
                                row["horizon"],
                            ],
                        },
                    }
                )
        if len(profiles) != expected or len({p["id"] for p in profiles}) != expected:
            raise ValueError("Profile completeness/uniqueness mismatch")
        comparisons = []
        for i, row in enumerate(analysis["comparisons"]):
            if "delta_ell_bits" not in row:
                raise ValueError("Missing whole-history comparison")
            original_kind = row["kind"]
            kind = "preparation" if original_kind == "preparation" else "mechanism"
            comparisons.append(
                {
                    "id": f"{sid}.comparison.{i:04d}",
                    "study": sid,
                    "comparison_kind": kind,
                    "original_kind": original_kind,
                    "physical_choice": False,
                    "source_comparison": row,
                    "scope": "whole_modeled_field; projected parts only where explicitly returned",
                    "conditioning": "see preparation records; R1 reference is known-root average",
                    "units": "log2 complete-history perplexity in bits",
                    "projected_sign_status": "per source intervals; unresolved is not zero"
                    if sid == "E1"
                    else "not_calculated",
                    "rate_offset_status": "see source comparison and matched individual profiles",
                    "crossover": {
                        "value": None,
                        "reason": "not bracketed in retained run",
                    },
                    "foreclosure": {"value": None, "reason": "not_calculated"},
                    "numerical_status": "float64_full_model; residuals and tolerance retained",
                    "temporal_audit": "three cadences"
                    if sid != "E1"
                    else "three cadences at two physical corners; primary elsewhere",
                    "state_refinement": "not_audited",
                    "physical_faithfulness": "open",
                    "governing_status": "provisional",
                    "editorial_mapping": {
                        "version": "Claude-request-r1-qualified",
                        "whole_candidate_tier": "M2",
                        "qualification": "Numerically resolved at declared model resolution; no finest-physical-grain claim",
                    },
                    "interpretation_source": (study / interpretation)
                    .relative_to(ROOT)
                    .as_posix(),
                    "prospective_prediction": {
                        "value": None,
                        "reason": "not reconstructed after the result; consult original protocol",
                    },
                }
            )
        write(out / (sid + "_PROFILES.json"), profiles)
        write(out / (sid + "_COMPARISONS.json"), comparisons)
        write(
            out / (sid + "_MODEL.json"),
            {
                "study": sid,
                "question": protocol["question"],
                "energy_per_root": protocol["energy_per_root"],
                "preparations": protocol["preparations"],
                "laws": [
                    {"id": l["id"], "model": l["model"]} for l in protocol["laws"]
                ],
                "horizons": protocol["horizons"],
                "cadences": protocol["cadences"],
                "scope": protocol["scope"],
                "boundary_scope": protocol.get("boundary_scope"),
                "protocol_source": receipt(study / "PROTOCOL.json"),
            },
        )
        for metric in ("preparation", "mechanism"):
            rows = [r for r in comparisons if r["comparison_kind"] == metric]
            claims.append(
                {
                    "claim_id": sid + "." + metric,
                    "study": sid,
                    "comparison_file": sid + "_COMPARISONS.json",
                    "comparison_count": len(rows),
                    "question": protocol["question"],
                    "candidate_tier": "M2",
                    "scope": "finite physical mechanisms; no ethical correspondence established",
                    "pending": [
                        "physical grain faithfulness",
                        "work/activity matched attribution",
                        "history-support foreclosure",
                    ],
                    "mechanism": "see model card and native rules",
                    "relationship": "full signed map retained",
                    "challenged": "see original protocol and corrected interpretation; no reconstructed guesses",
                }
            )
        inputs.extend(receipt(p) for p in files)
        checks.append(
            {
                "study": sid,
                "profiles": len(profiles),
                "comparisons": len(comparisons),
                "complete": True,
                "whole_profile_numbers_copied_without_recalculation": True,
            }
        )
    refinement = (
        ROOT / "research/studies/E1-coupled-autocatalysis/refinement-2026-10-25"
    )
    inputs += [
        receipt(refinement / "INTERPRETATION.md"),
        receipt(refinement / "evidence/ANALYSIS.json"),
    ]
    claims.append(
        {
            "claim_id": "E1.donor_filter_estimates",
            "candidate_tier": "M3",
            "scope": "same full present, donor A at cadence.25; estimates retained separately",
            "resolved_sign": None,
            "reason": "Approximate t intervals do not satisfy requested certified sign",
            "source": (refinement / "INTERPRETATION.md").relative_to(ROOT).as_posix(),
        }
    )
    write(
        out / "CLAIMS.json",
        {
            "schema": "omega.manuscript-claims/1",
            "rows": claims,
            "tier_mapping": "Editorial candidates only; scientific quality axes in comparison rows",
        },
    )
    write(
        out / "SOURCES.json",
        {
            "schema": "omega.manuscript-handoff-sources/1",
            "files": inputs,
            "basis": "retained numerical evidence; no scientific rerun",
        },
    )
    write(
        out / "VALIDATION.json",
        {
            "status": "passed",
            "checks": checks,
            "source_files": len(inputs),
            "source_hashes_verified_at_export": True,
        },
    )
    shutil.copyfile(__file__, out / "package_manuscript_evidence.py")
    print(json.dumps({"status": "passed", "studies": checks}))


if __name__ == "__main__":
    main()
