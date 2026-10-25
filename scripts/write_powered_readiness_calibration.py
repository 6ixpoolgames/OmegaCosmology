"""Materialize a bounded fuel-powered register calibration, not a policy map."""

import json

from write_coupled_smoke_plan import cond
from write_readiness_fidelity import pilot_protocol
from write_readiness_smoke import ROOT

from omega_cosmology.testbed.readiness import readiness_root
from omega_cosmology.testbed.readiness_v2 import powered_readiness_world


def calibration_case(
    name, policy="reengage", *, held=None, memory_control=False, source=True
):
    physical = {} if held is None else {"opening_rate": None}
    model = powered_readiness_world(
        policy, source_enabled=source, attempts_enabled=not memory_control, **physical
    )
    p = pilot_protocol(model, policy=policy, quantum=".5", effort=".5")
    p["id"] = "powered-readiness." + name
    p["max_states"] = 2000
    p["max_dense_bytes"] = 128 * 1024**2
    p["max_occupation_dense_bytes"] = 1024**3
    p["structural_analysis"]["max_functional_query_states"] = 8000
    for projection in p["projected_histories"]:
        projection["max_workspace_bytes"] = 128 * 1024**2
    p["scope"] = (
        "Physical circuit calibration; preparations may differ in energy; no policy optimum or clinical claim"
    )
    p["horizons"] = (
        [16, 64, 256]
        if held is None
        else ([4, 16, 64] if memory_control else [1, 4, 16, 64])
    )
    p["observables"].append({"id": "carrier_charged", "terms": [["carrier", 1]]})
    fuel_rules = [
        r.id
        for r in model.rules
        if r.id.startswith(("cue_write_", "cue_reset_", "cue_clear_"))
        and dict(r.changes).get("carrier") == -1
    ]
    for direction in (1, -1):
        p["event_readouts"].append(
            {
                "id": "register_fuel_" + ("forward" if direction == 1 else "reverse"),
                "selectors": [{"rules": fuel_rules, "direction": direction}],
            }
        )
    if held is not None:
        p["preparations"] = []
        settings = (
            [("unmarked", 3, 0, int(held)), ("marked", 3, 2, int(held))]
            if memory_control
            else [
                (
                    f"{'full' if bank else 'empty'}_{'correct' if cue == held else 'wrong'}",
                    bank,
                    0,
                    cue,
                )
                for bank in (3, 0)
                for cue in (0, 1)
            ]
        )
        for prep_id, bank, marks, cue in settings:
            state = list(readiness_root(model))
            for key, value in {
                "barrier": int(held),
                "body.bank": bank,
                "body.failures": marks,
                "body.cue": cue,
            }.items():
                state[model.indices[key]] = value
            state = tuple(state)
            model.validate(state)
            p["preparations"].append(
                {
                    "id": prep_id,
                    "roots": [[list(state), 1.0]],
                    "conditioning": "full_present",
                    "energy_per_root": str(model.energy(state)),
                }
            )
        p["structural_analysis"]["organizations"].append(
            {
                "id": "correct_cue",
                "definition": "Cue equals the fixed barrier sector; first correctness is not persistent correctness",
                "coordinates": ["body.cue"],
                "functional_any_of": [[cond("body.cue", "eq", int(held))]],
            }
        )
    return {
        "id": name,
        "law": {"id": name, "model": model.record()},
        "protocol": p,
        "held_open": held,
        "memory_control": memory_control,
        "source_enabled": source,
    }


def main():
    plan = {
        "schema": "omega.coupled-engineering-plan/1",
        "date": "2026-10-26",
        "cases": [
            calibration_case("native_reengage"),
            calibration_case("native_stop", "stop"),
            calibration_case("native_source_off", source=False),
            calibration_case("held_closed", held=False),
            calibration_case("held_open", held=True),
            calibration_case("memory_closed", held=False, memory_control=True),
            calibration_case("memory_open", held=True, memory_control=True),
        ],
        "spec": "research/platform/specs/POWERED_READINESS_CALIBRATION_r1.md",
        "snapshot_files": [
            "scripts/write_powered_readiness_calibration.py",
            "scripts/report_powered_readiness.py",
            "scripts/write_readiness_fidelity.py",
            "scripts/write_readiness_smoke.py",
            "scripts/report_readiness_fidelity.py",
            "tests/test_powered_readiness.py",
        ],
        "caps": {
            "case_seconds": 600,
            "job_memory_bytes": 1536 * 1024**2,
            "case_output_bytes": 16 * 1024**2,
            "batch_seconds": 1800,
            "batch_output_bytes": 64 * 1024**2,
        },
    }
    out = (
        ROOT
        / "research/platform/models/struggle-readiness/POWERED_CALIBRATION_PLAN.json"
    )
    out.write_text(json.dumps(plan, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "written", "cases": len(plan["cases"])}))


if __name__ == "__main__":
    main()
