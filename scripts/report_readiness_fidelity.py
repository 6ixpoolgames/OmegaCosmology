"""Read-only fidelity diagnostics and compact retention for the readiness pilot."""

import argparse
import json
from math import isfinite, log2
from pathlib import Path

from report_signed_studies import ROOT, retain_run, write


def divide(a, b):
    return a / b if b > 1e-15 else None


def cue_metrics(probabilities):
    """Rows=cue, columns=open barrier; no causal interpretation of association."""
    p = [list(row) for row in probabilities]
    if len(p) != 2 or any(len(row) != 2 for row in p):
        raise ValueError("Binary joint table required")
    if any(not isfinite(v) or v < -1e-10 for row in p for v in row):
        raise ValueError("Finite nonnegative joint table required")
    if abs(sum(map(sum, p)) - 1) > 1e-8:
        raise ValueError("Normalized joint table required")
    p = [[max(v, 0) for v in row] for row in p]
    rows = list(map(sum, p))
    cols = [p[0][j] + p[1][j] for j in range(2)]
    mi = sum(
        p[i][j] * log2(p[i][j] / (rows[i] * cols[j]))
        for i in range(2)
        for j in range(2)
        if p[i][j] > 0
    )
    return {
        "joint_cue_by_open": p,
        "mutual_information_bits": mi,
        "open_prevalence": cols[1],
        "cue_prevalence": rows[1],
        "sensitivity": divide(p[1][1], cols[1]),
        "specificity": divide(p[0][0], cols[0]),
        "positive_predictive_value": divide(p[1][1], rows[1]),
        "accuracy": p[0][0] + p[1][1],
        "always_closed_accuracy": cols[0],
        "balanced_accuracy": None
        if min(cols) <= 1e-15
        else (p[1][1] / cols[1] + p[0][0] / cols[0]) / 2,
    }


def profile_diagnostics(row):
    obs, events, T = row["observables"], row["event_readouts"], row["horizon"]
    cue = {}
    for mode in ("endpoint", "integrated", "stationary"):
        table = [
            [
                obs[f"cue_joint_{i}_{j}"][mode] / (T if mode == "integrated" else 1)
                for j in (0, 1)
            ]
            for i in (0, 1)
        ]
        cue[mode] = cue_metrics(table)
    birth_ids = ("marks_failed_attempt", "marks_reverse_clear", "marks_thermal")
    death_ids = ("marks_undo_attempt", "marks_cleared", "marks_relaxed")
    writes, erases = (
        sum(events[k] for k in birth_ids),
        sum(events[k] for k in death_ids),
    )
    residual = obs["failure_marks"]["endpoint"] - (writes - erases)
    if abs(residual) > 1e-7:
        raise ArithmeticError("Physical mark drift and native event ledger disagree")
    return {
        "horizon": T,
        "cue": cue,
        "marks": {
            "write_origins": {k: events[k] for k in birth_ids},
            "erase_origins": {k: events[k] for k in death_ids},
            "failed_attempt_share_of_writes": divide(
                events["marks_failed_attempt"], writes
            ),
            "non_attempt_share_of_writes": divide(
                events["marks_reverse_clear"] + events["marks_thermal"], writes
            ),
            "endpoint_expected_marks": obs["failure_marks"]["endpoint"],
            "endpoint_marked_probability": obs["marked_1"]["endpoint"],
            "saturation_probability": obs["memory_saturated"]["endpoint"],
            "drift_ledger_residual": residual,
            "limit": "Event origins, not lineage or accuracy of individual retained marks",
        },
        "opportunities": {
            k: events[k]
            for k in (
                "openings",
                "openings_ready",
                "closings_exposed",
                "closings_exposed_unfunded",
            )
        },
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
    summaries = []
    for c in receipt["cases"]:
        name = c.get("case", c.get("id"))
        path = out / "retained" / name / "RESULT.json"
        if not path.exists():
            summaries.append({"case": name, "passed": False, "receipt": c["receipt"]})
            continue
        record = json.loads(path.read_text(encoding="utf-8"))
        summaries.append(
            {
                "case": name,
                "passed": c["passed"],
                "states": record["states"],
                "receipt": c["receipt"],
                "profiles": [profile_diagnostics(row) for row in record["rows"]],
            }
        )
    write(
        out / "FIDELITY_SUMMARY.json",
        {
            "status": receipt["status"],
            "engineering_only": True,
            "wall_seconds": receipt["wall_seconds"],
            "cases": summaries,
            "snapshot_inputs": len(manifest["files"]),
            "limits": [
                "No physical changes",
                "Single cadence",
                "No optimized policy or private sign certificate",
            ],
        },
    )
    print(
        json.dumps(
            {"status": receipt["status"], "cases": len(summaries), "out": str(out)}
        )
    )


if __name__ == "__main__":
    main()
