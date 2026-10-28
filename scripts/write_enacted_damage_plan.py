"""Write the small enacted-operation smoke inputs; no scientific ranking."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from omega_cosmology.testbed.operations import operation_world
from omega_cosmology.testbed.repair import repair_capacity_world


def protocol(name, pulse, recovery):
    condition = lambda k, v: {"coordinate": k, "operator": "eq", "value": v}
    body = [
        "repair.R",
        "repair.Y",
        "repair.bank",
        "contact.repair.R_to_repair.Y",
        "contact.repair.Y_to_repair.R",
    ]
    observables = [
        {"id": k, "terms": [[k, 1]]}
        for k in ("repair.R", "repair.Y", "repair.bank", "operation.displaced")
    ]
    observables += [
        {
            "id": "both_working",
            "constant": 1,
            "conditions": [condition(k, 1) for k in ("repair.R", "repair.Y")],
        },
        {
            "id": "empty_bank",
            "constant": 1,
            "conditions": [condition("repair.bank", 0)],
        },
        {
            "id": "usable_capture_interface",
            "constant": 1,
            "conditions": [condition("repair.Y", 1)]
            + [condition(k, 0) for k in body[3:]],
        },
    ]
    return {
        "id": name,
        "present_id": "enacted-damage.intact-common-present",
        "root": [1, 1, 2, 1, 0, 0, 0],
        "energy_per_root": "5",
        "coordinate_order": [c.name for c in pulse.coordinates],
        "cadence": 0.25,
        "horizons": [1, 4, 16],
        "phases": [
            {"id": "operation_pulse", "duration": 1, "model": pulse.record()},
            {"id": "common_recovery", "duration": 15, "model": recovery.record()},
        ],
        "sufficiency": "Full finite component, contact, bank, carrier and actuator state; externally fixed phase schedule determines native Markov law",
        "implementation": "Bank-paid paired stroke under a declared barrier pulse, all outcomes retained, common recovery without a reset",
        "boundary_scope": {
            "bath": "beta1; heat ledger, unresolved histories",
            "source": "same reversible maintained carrier work source in every arm",
            "pulse": "barrier schedule; unresolved external setting apparatus; unchanged Hamiltonian",
        },
        "matched": {
            "root": "identical intact full present",
            "endowment": "same slots, carrier, bank and actuator Hamiltonian",
            "offered_boundary": "same source; actual accepted work may differ",
            "resolution": "same physical coordinates and cadence; faithfulness open",
        },
        "observables": observables,
        "functional_conditions": [condition(k, 1) for k in ("repair.R", "repair.Y")],
        "projected_histories": [
            {"id": f"repair_body.m{m}", "coordinates": body, "memory": m}
            for m in (0, 1)
        ],
        "max_states": 200,
        "max_dense_bytes": 128 * 1024**2,
        "max_projection_bytes": 32 * 1024**2,
    }


def main():
    out = ROOT / "research/platform/models/enacted-damage/ENGINEERING_PLAN.json"
    if out.exists():
        raise ValueError("Plan already exists; preserve prior inputs")
    base = repair_capacity_world()
    recovery = operation_world(base)
    cases = [
        protocol("idle", recovery, recovery),
        protocol("sham", operation_world(base, stroke_conductance=0.2), recovery),
        protocol(
            "damage_R",
            operation_world(base, target="repair.R", stroke_conductance=0.2),
            recovery,
        ),
        protocol(
            "damage_Y",
            operation_world(base, target="repair.Y", stroke_conductance=0.2),
            recovery,
        ),
    ]
    plan = {
        "schema": "omega.enacted-damage-engineering/1",
        "date": "2026-10-26",
        "spec": "research/platform/specs/ENACTED_DAMAGE_SPRINT_r1.md",
        "cases": cases,
        "calibration": {
            "targets": ["damage_R", "damage_Y"],
            "horizon": 16,
            "moments": ["expected_jumps", "work_accepted_gross"],
            "bounds": {
                "stroke_conductance": [0.0001, 2.0],
                "relaxation_conductance": [0.0001, 2.0],
            },
            "max_fit_evaluations": 24,
            "scaled_tolerance": 0.001,
        },
        "caps": {
            "case_seconds": 300,
            "job_memory_bytes": 1024**3,
            "case_output_bytes": 32 * 1024**2,
        },
        "scope": "Engineering calibration/smoke only; no expected score sign and no automatic scientific map",
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(out.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
