"""Inputs for fixed-thermal paid-cycle control, without history scoring."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from write_r2_integrated_plan import protocol as base_protocol

from omega_cosmology.testbed.paid_cycle import paid_cycle_chain


def protocol(model, root):
    p, absent = base_protocol(model, root)
    p["id"] = "R2-fixed-thermal-paid-cycle"
    p["event_readouts"].extend(
        {
            "id": "rotor_reset." + suffix,
            "selectors": [{"rules": ["rotor.reset"], "direction": direction}],
        }
        for direction, suffix in ((1, "forward"), (-1, "reverse"))
    )
    p["monitors"].append(
        {
            "id": "first_paid_cycle",
            "stages": [
                {
                    "name": "charge",
                    "advance": [{"rules": ["rotor.stroke"], "direction": 1}],
                },
                {
                    "name": "reset",
                    "advance": [{"rules": ["rotor.reset"], "direction": 1}],
                    "abort": [
                        {
                            "target": [
                                {
                                    "coordinate": "rotor.state",
                                    "operator": "eq",
                                    "value": 0,
                                }
                            ]
                        }
                    ],
                },
            ],
        }
    )
    return p, absent


def make_plan(*, activity_only=False, ungated=False):
    cases = []
    for id, params in (("productive", {}), ("no_secondary_access", {"access": False})):
        params = {**params, **({"gated": False} if ungated else {})}
        m, root, bindings = paid_cycle_chain(**params)
        p, absent = protocol(m, root)
        cases.append(
            {
                "id": id,
                "parameters": params,
                "law": {"id": id, "model": m.record(), "absent_query_rules": absent},
                "protocol": p,
                "bindings": bindings,
            }
        )
    plan = {
        "schema": "omega.r2-paid-cycle-control/1",
        "spec": "research/platform/specs/R2_PAID_CYCLE_CONTROL_r1.md",
        "support_scripts": ["scripts/write_r2_paid_cycle_plan.py"],
        "test_files": ["tests/test_paid_cycle.py"],
        "snapshot_inputs": [
            "research/platform/engineering/r2-transduction-2026-10-27/retained/EXECUTION_CASES.json"
        ],
        "control_id": "paid_cycle_candidate",
        "cases": cases,
        "cadences": [0.25, 0.5],
        "physical_diagnostics": {
            "bank_coordinate": "bank.ticks",
            "paid_role": "churn.paid",
            "thermal_role": "churn.thermal",
        },
        "calibration": {
            "horizon": 64,
            "target": "productive",
            "control": "no_secondary_access",
            "bounds": {"charge": [1e-5, 0.5], "reset": [1e-5, 0.5]},
            "absolute_tolerance": 1e-8,
            "relative_tolerance": 0.001,
            "fit_evaluations": 24,
        },
        "caps": {"seconds": 900, "memory_bytes": 1024**3, "output_bytes": 64 * 1024**2},
    }
    if activity_only:
        plan["spec"] = "research/platform/specs/R2_ACTIVITY_ONLY_CONTROL_r1.md"
        plan["control_id"] = "activity_only_candidate"
        plan["calibration"].update(
            method="activity_diagonal", bounds={"rate": [1e-5, 0.5]}
        )
    if ungated:
        plan["spec"] = "research/platform/specs/R2_BANK_LOAD_CONTROL_r1.md"
        plan["control_id"] = "bank_load_candidate"
        plan["control_parameters"] = {"gated": False}
        plan["require_net_paying_control_before_history"] = True
    return plan


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--activity-only", action="store_true")
    parser.add_argument("--ungated", action="store_true")
    args = parser.parse_args()
    folder = (
        "r2-bank-load"
        if args.ungated
        else ("r2-activity-only" if args.activity_only else "r2-paid-cycle")
    )
    path = ROOT / "research/platform/models" / folder / "ENGINEERING_PLAN.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            make_plan(activity_only=args.activity_only, ungated=args.ungated), indent=2
        )
        + "\n",
        encoding="utf-8",
    )
    print(path.relative_to(ROOT))
