"""Algebra on retained J evidence only: no model compilation or new fit."""

import argparse
import json
import math
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / "research/platform/engineering/joint-resource-load-2026-10-31"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    if out.exists() or not out.is_relative_to(ROOT / "runs"):
        raise ValueError("Fresh ignored output required")
    manifest = json.loads((SOURCE / "EVIDENCE.json").read_text(encoding="utf-8"))
    entries = {r["path"]: r for r in manifest["files"]}
    sources = []
    for name in ["physical/CALIBRATION.json", "SNAPSHOT.zip"]:
        raw = (SOURCE / name).read_bytes()
        digest = sha256(raw).hexdigest()
        if digest != entries[name]["sha256"]:
            raise ValueError("Retained evidence changed")
        sources.append(
            {
                "path": (SOURCE / name).relative_to(ROOT).as_posix(),
                "sha256": digest,
                "bytes": len(raw),
            }
        )
    data = json.loads(
        (SOURCE / "physical/CALIBRATION.json").read_text(encoding="utf-8")
    )
    target, best = data["target"], data["best"]
    baseline = next(
        r
        for r in data["all_physical_rows"]
        if r["kind"] == "ablation" and r["source_on"]
    )
    names = ["event_rate", "net_work_rate"]
    desired = [target["stationary"][n] - best["stationary"][n] for n in names]
    a, b = data["sensitivity"]["moment_parameter_derivatives"][0]
    c, d = data["sensitivity"]["moment_parameter_derivatives"][1]
    determinant = a * d - b * c
    if abs(determinant) < 1e-12:
        raise ArithmeticError("Stored Jacobian does not support this inverse diagnosis")
    step = [
        (d * desired[0] - b * desired[1]) / determinant,
        (-c * desired[0] + a * desired[1]) / determinant,
    ]
    reconstructed = [a * step[0] + b * step[1], c * step[0] + d * step[1]]
    inverse_residual = max(abs(x - y) for x, y in zip(reconstructed, desired))
    result = {
        "status": "retained_evidence_review_complete",
        "source_manifest_sha256": sha256(
            (SOURCE / "EVIDENCE.json").read_bytes()
        ).hexdigest(),
        "sources": sources,
        "new_physical_evaluations": 0,
        "new_history_scores": 0,
        "new_fits": 0,
        "local_linear_diagnosis": {
            "moment_names": names,
            "parameter_names": ["k_L", "k_U"],
            "stored_jacobian": [[a, b], [c, d]],
            "determinant": determinant,
            "desired_moment_change": desired,
            "linearized_parameter_step": step,
            "linearized_parameter_values": [
                best["parameters"]["k_L"] + step[0],
                best["parameters"]["k_U"] + step[1],
            ],
            "inverse_identity_residual": inverse_residual,
            "event_per_work_derivative_ratios": {"k_L": a / c, "k_U": b / d},
            "tangent_separation_coefficient": a - b * c / d,
            "negative_locked_conductance_required_by_linearization": best["parameters"][
                "k_L"
            ]
            + step[0]
            < 0,
            "scope": "Stored local derivatives only; finite extrapolation and global infeasibility are not established",
        },
        "arms": {},
    }
    for label, row in [
        ("productive", target),
        ("selected_control", best),
        ("ablation", baseline),
    ]:
        s = row["stationary"]
        p0, p1, _p2 = row["function"]["stationary_carrier_probabilities"]
        source_current_identity = 3 * 0.08 * (p0 - p1)
        if abs(source_current_identity - s["net_work_rate"]) > 1e-12:
            raise ArithmeticError(
                "Source-current identity does not match retained ledger"
            )
        result["arms"][label] = {
            "row_index": row["index"],
            "stationary": s,
            "function": row["function"],
            "total_event_rate_per_net_source_work_rate": s["event_rate"]
            / s["net_work_rate"],
            "net_source_work_rate_per_total_event_rate": s["net_work_rate"]
            / s["event_rate"],
            "source_current_identity_residual": source_current_identity
            - s["net_work_rate"],
            "ratio_scope": "Descriptive stationary rates, including thermal/reverse events; not microscopic per-event cost, extractable efficiency or lushness",
        }
    for label, row in [("productive", target), ("selected_control", best)]:
        dn = row["stationary"][names[0]] - baseline["stationary"][names[0]]
        dw = row["stationary"][names[1]] - baseline["stationary"][names[1]]
        result["arms"][label]["relative_to_ablation"] = {
            "delta_event_rate": dn,
            "delta_net_work_rate": dw,
            "delta_event_rate_per_delta_work_rate": dn / dw,
            "scope": "Between-law diagnostic difference of means; not an attributed stream of events",
        }
    # Independently derive energy destinations from the retained rule grammar.
    with ZipFile(SOURCE / "SNAPSHOT.zip") as z:
        inputs = json.loads(z.read("INPUTS.json"))
    model = inputs["productive"]
    rules = {r["id"]: r for r in model["rules"]}

    def energy(state):
        total = Fraction(0)
        for term in model["energy_terms"]:
            if not all(
                state[g["coordinate"]] == g["value"] and g["operator"] == "eq"
                for g in term.get("conditions", [])
            ):
                continue
            total += Fraction(term["coefficient"]) * (
                state[term["coordinate"]] if term.get("coordinate") else 1
            )
        return total

    initial = {"a.active": 1, "b.active": 1, "bond": 1, "carrier": 1, "bank": 0}
    after_unlock = {**initial, "carrier": 2}
    after_capture = {**initial, "carrier": 0, "bank": 2}
    unlock_delta = energy(after_unlock) - energy(initial)
    capture_delta = energy(after_capture) - energy(after_unlock)
    if rules["unlock_motif"]["changes"] != [["carrier", 1]] or rules["capture"][
        "changes"
    ] != [["carrier", -2], ["bank", 2]]:
        raise ValueError("Reviewed productive pathway grammar changed")
    result["path_energy_account"] = {
        "beta": model["beta"],
        "unlock_heat": float(-unlock_delta),
        "capture_heat": float(-capture_delta),
        "capture_bank_increment": 1.0,
        "locked_direct_load_heat": 3.0,
        "usable_direct_load_heat": 2.0,
        "two_step_unlock_capture_heat": float(-unlock_delta - capture_delta),
        "locked_load_forward_reverse_rate_ratio": math.exp(3 * model["beta"]),
        "usable_load_forward_reverse_rate_ratio": math.exp(2 * model["beta"]),
        "scope": "One forward sequence energy account, not frequency, irreversible dynamics or a complete stochastic trajectory attribution",
    }
    assert inverse_residual < 1e-12
    assert unlock_delta == -1 and capture_delta == -1
    out.mkdir(parents=True)
    (out / "ANALYSIS.json").write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "linearized_step": step,
                "new_physical_evaluations": 0,
                "new_fits": 0,
                "new_history_scores": 0,
            }
        )
    )


if __name__ == "__main__":
    main()
