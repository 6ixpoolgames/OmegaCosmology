"""Report physical register calibration without selecting a lushness winner."""

import argparse
import json
from pathlib import Path
from zipfile import ZipFile

from report_readiness_fidelity import cue_metrics, divide
from report_signed_studies import ROOT, retain_run, write


def calibration_diagnostics(row, initial_marks):
    obs, ev, T = row["observables"], row["event_readouts"], row["horizon"]
    cue = {
        mode: cue_metrics(
            [
                [
                    obs[f"cue_joint_{i}_{j}"][mode] / (T if mode == "integrated" else 1)
                    for j in (0, 1)
                ]
                for i in (0, 1)
            ]
        )
        for mode in ("endpoint", "integrated", "stationary")
    }
    births = {
        k: ev[k]
        for k in ("marks_failed_attempt", "marks_reverse_clear", "marks_thermal")
    }
    deaths = {
        k: ev[k] for k in ("marks_undo_attempt", "marks_cleared", "marks_relaxed")
    }
    delta = obs["failure_marks"]["endpoint"] - initial_marks
    residual = delta - sum(births.values()) + sum(deaths.values())
    if abs(residual) > 1e-7:
        raise ArithmeticError("Mark drift mismatch relative to actual initial marks")
    correct = row["functional_profiles"].get("correct_cue")
    return {
        "preparation": row["preparation"],
        "horizon": T,
        "cue": cue,
        "first_correct_probability": correct["ever_functional_probability"]
        if correct
        else None,
        "current_correct_probability": correct["endpoint_functional_probability"]
        if correct
        else None,
        "marks": {
            "initial_expected": initial_marks,
            "endpoint_expected": obs["failure_marks"]["endpoint"],
            "write_origins": births,
            "erase_origins": deaths,
            "non_attempt_share_of_writes": divide(
                ev["marks_reverse_clear"] + ev["marks_thermal"], sum(births.values())
            ),
            "saturated_probability": obs["memory_saturated"]["endpoint"],
            "drift_ledger_residual": residual,
        },
        "register_fuel": {
            "charged_carriers_spent_gross": ev["register_fuel_forward"],
            "charged_carriers_refunded_gross": ev["register_fuel_reverse"],
            "carrier_energy_spent_gross": 1.5 * ev["register_fuel_forward"],
            "carrier_energy_refunded_gross": 1.5 * ev["register_fuel_reverse"],
            "scope": "Internal carrier energy flow, not additional external work or heat",
        },
        "external_work_accepted_gross": row["physical"]["work_accepted_gross"],
        "bank_empty_fraction": obs["empty_bank"]["integrated"] / T,
        "whole_history_bits": row["history"]["ell_bits"],
        "full_body_bound_width_bits": row["projected_histories"]["body_full.m0"][
            "width_bits"
        ],
        "convergence": row["horizon_diagnostics"],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    args = p.parse_args()
    out = args.out_dir.resolve()
    if out.exists() or not out.is_relative_to(ROOT / "research/platform/engineering"):
        p.error("Use a fresh engineering evidence directory")
    receipt, _records, manifest = retain_run(args.run, out / "retained", complete=False)
    with ZipFile(out / "retained/SNAPSHOT.zip") as archive:
        plan = json.loads(archive.read(manifest["plan"]))
    cases = {c["id"]: c for c in plan["cases"]}
    summaries = []
    for item in receipt["cases"]:
        name = item["id"]
        path = out / "retained" / name / "RESULT.json"
        entry = {"case": name, "passed": item["passed"], "receipt": item["receipt"]}
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            spec = cases[name]
            ix = spec["protocol"]["coordinate_order"].index("body.failures")
            initial_marks = {
                prep["id"]: sum(state[ix] * w for state, w in prep["roots"])
                for prep in spec["protocol"]["preparations"]
            }
            entry.update(
                {
                    "states": data["states"],
                    "held_open": spec["held_open"],
                    "memory_control": spec["memory_control"],
                    "source_enabled": spec["source_enabled"],
                    "profiles": [
                        calibration_diagnostics(row, initial_marks[row["preparation"]])
                        for row in data["rows"]
                    ],
                }
            )
        summaries.append(entry)
    write(
        out / "CALIBRATION_SUMMARY.json",
        {
            "status": receipt["status"],
            "engineering_only": True,
            "wall_seconds": receipt["wall_seconds"],
            "snapshot_inputs": len(manifest["files"]),
            "cases": summaries,
            "limits": [
                "Single physical successor, not a parameter frontier",
                "Single cadence, physical faithfulness open",
                "No clinical learning or policy optimization claim",
            ],
        },
    )
    print(json.dumps({"status": receipt["status"], "cases": len(summaries)}))


if __name__ == "__main__":
    main()
