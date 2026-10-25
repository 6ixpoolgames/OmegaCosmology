"""Materialize authorized S1 feasibility and S2 engineering inputs, without running."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from run_coupled_smoke import DEFAULT_PLAN  # Existing runner remains the supervisor.
from write_coupled_smoke_plan import case

from omega_cosmology.testbed.occupancy import contact_state_bound, occupied_ecology


def write(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def main():
    pair = [
        {"id": g, "members": [g + ".x", g + ".y"], "access_member": g + ".x"}
        for g in ("A", "B")
    ]
    single = pair[:1]
    triple = [{"id": "A", "members": ["A.x", "A.y", "A.z"], "access_member": "A.x"}]
    cross = [("A.x", "B.y"), ("B.x", "A.y")]
    settings = {
        "bank_quantum": ".5",
        "formation_energy": ".5",
        "construction_bill_ticks": 2,
    }
    specifications = [
        ("reciprocal_pair", pair, {"extra_assistance": cross}),
        ("single_cycle", single, {}),
        (
            "competing_port",
            triple,
            {
                "extra_assistance": [("A.x", "A.z")],
                "assistance_edges": [("A.x", "A.y"), ("A.x", "A.z")],
            },
        ),
        ("local_pair", pair, {}),
        ("one_way_pair", pair, {"extra_assistance": cross[:1]}),
        ("source_off_pair", pair, {"extra_assistance": cross, "driven": False}),
    ]
    cases = []
    for name, groups, options in specifications:
        m = occupied_ecology(groups, **settings, **options)
        root = tuple(
            1
            if (c.role == "constructed_component" and c.name.endswith(".x"))
            or c.role == "energy"
            or c.name == "carrier"
            else 0
            for c in m.coordinates
        )
        m.validate(root)
        item = case(name, m, root, groups)
        p = item["protocol"]
        p["max_states"] = 2000
        p["max_dense_bytes"] = 128 * 1024**2
        p["max_occupation_dense_bytes"] = 512 * 1024**2
        p["legal_state_count_reference"] = contact_state_bound(m)
        p["projected_histories"] = [
            s for s in p["projected_histories"] if s["memory"] == 1
        ]
        if len(groups) > 1:
            p["structural_analysis"]["ancestry"] = []
        p["observables"].append(
            {
                "id": "occupied_contacts",
                "terms": [
                    [c.name, 1] for c in m.coordinates if c.role == "catalytic_contact"
                ],
            }
        )
        p["event_readouts"] = [
            {
                "id": "paid_contact_conversions",
                "selectors": [
                    {
                        "rules": [
                            r.id
                            for r in m.rules
                            if r.id.startswith("assisted_construct_")
                        ],
                        "direction": 1,
                    }
                ],
            },
        ]
        # The generic marked-event readout syntax is validated by the smoke.
        p["scope"] = (
            "S2 engineering smoke: occupied finite catalysis, no policy search or ecological verdict"
        )
        cases.append(item)
        print(name, p["legal_state_count_reference"], "legal states")
    write(
        "research/platform/models/occupied-assistance/ENGINEERING_PLAN.json",
        {
            "schema": "omega.coupled-engineering-plan/1",
            "date": "2026-10-25",
            "cases": cases,
            "spec": "research/platform/specs/OCCUPIED_ASSISTANCE_DESIGN_r1.md",
            "caps": {
                "case_seconds": 300,
                "job_memory_bytes": 4 * 1024**3,
                "case_output_bytes": 32 * 1024**2,
                "batch_seconds": 1800,
                "batch_output_bytes": 192 * 1024**2,
            },
            "snapshot_files": [
                "scripts/write_ecology_sprint_plans.py",
                "tests/test_occupancy.py",
                "research/platform/specs/ECOLOGY_PROGRAMME_SCOPE_r1.md",
            ],
            "supervisor_reference": DEFAULT_PLAN,
        },
    )
    old_path = (
        ROOT
        / "research/studies/E1-coupled-autocatalysis/refinement-2026-10-25/FILTER_LONG_PLAN.json"
    )
    for cadence in (0.25, 0.5):
        plan = json.loads(old_path.read_text(encoding="utf-8"))
        plan["cadence"] = cadence
        plan["confidence_family_size"] = 6
        suffix = str(cadence).replace(".", "p")
        plan["retained_cases"] = {
            k: v.replace("dt0p25", "dt" + suffix)
            for k, v in plan["retained_cases"].items()
        }
        plan["source_inputs"] += [
            "tests/test_filter_confidence.py",
            "research/platform/specs/PROJECTED_CONFIDENCE_FEASIBILITY_r1.md",
        ]
        plan["caps"] = {
            "case_seconds": 600,
            "job_memory_bytes": 4 * 1024**3,
            "case_output_bytes": 64 * 1024**2,
        }
        plan["cases"] = [
            {
                "id": "donor_unassembled",
                "preparation": "unassembled",
                "projection": "A",
                "horizons": [16, 64, 256],
                "samples": 8192,
                "seed": 2026102504 if cadence == 0.25 else 2026102505,
                "batch_size": 256,
                "control_variate": "memory1_exact_mean",
            }
        ]
        write(
            "research/platform/models/projected-confidence/PLAN_dt" + suffix + ".json",
            plan,
        )


if __name__ == "__main__":
    main()
