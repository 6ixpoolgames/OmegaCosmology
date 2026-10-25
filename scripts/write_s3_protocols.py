"""Materialize the small repair smoke; later map settings are explicit inputs."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from write_coupled_smoke_plan import case, cond

from omega_cosmology.testbed.repair import repair_capacity_world


def repair_protocol(model, *, horizons=(4, 16)):
    group = [
        {
            "id": "repair",
            "members": ["repair.R", "repair.Y"],
            "access_member": "repair.Y",
        }
    ]
    p = case("repair", model, (1, 1, 2, 1, 0, 0), group)["protocol"]
    p["horizons"] = list(horizons)
    roots = {
        "intact": (1, 1, 2, 1, 0, 0),
        "repair_fault": (0, 1, 2, 1, 0, 0),
        "access_fault": (1, 0, 2, 1, 0, 0),
    }
    p["preparations"] = [
        {
            "id": name,
            "roots": [[list(s), 1.0]],
            "conditioning": "full_present",
            "energy_per_root": str(model.energy(s)),
        }
        for name, s in roots.items()
    ]
    p["energy_per_root"] = str(model.energy(roots["repair_fault"]))
    p["matching"] = {
        "primary": "repair_fault versus access_fault: same immediate .5 energy loss, same material",
        "intact_reference": "different-energy diagnostic; no fault pulse enacted",
    }
    p["projected_histories"] = [
        {
            "id": f"{v}.m{memory}",
            "coordinates": ["repair." + v],
            "conditioning": "full_present",
            "memory": memory,
        }
        for v in ("R", "Y")
        for memory in (1, 2)
    ]
    p["structural_analysis"]["organizations"] += [
        {
            "id": v,
            "definition": f"{v} constructed and available irrespective of current contact occupancy",
            "coordinates": ["repair." + v],
            "functional_any_of": [[cond("repair." + v, "eq", 1)]],
        }
        for v in ("R", "Y")
    ]
    p["observables"] = [
        {"id": "bank_energy", "terms": [["repair.bank", 0.5]]},
        {
            "id": "occupied_contacts",
            "terms": [
                [c.name, 1] for c in model.coordinates if c.role == "catalytic_contact"
            ],
        },
    ]
    p["event_readouts"] = [
        {
            "id": "paid_repair_" + v,
            "selectors": [
                {
                    "rules": [
                        "assisted_construct_repair." + parent + "_to_repair." + v
                    ],
                    "direction": 1,
                }
            ],
        }
        for parent, v in [("R", "Y"), ("Y", "R")]
    ]
    p["foreclosure_queries"] = [
        {
            "id": f"{a}_relative_to_{b}.{scope}",
            "candidate": a,
            "reference": b,
            "coordinates": fields,
        }
        for a, b in [
            ("repair_fault", "access_fault"),
            ("repair_fault", "intact"),
            ("access_fault", "intact"),
        ]
        for scope, fields in [
            ("whole", p["coordinate_order"]),
            ("R", ["repair.R"]),
            ("Y", ["repair.Y"]),
        ]
    ]
    p["scope"] = (
        "Finite repair/access motif; reversible damage, no enacted faults, no optimizer or valuer identification"
    )
    return p


def main():
    cases = []
    for feedback in (True, False):
        m = repair_capacity_world(feedback=feedback)
        name = "repair_feedback" if feedback else "repair_no_feedback"
        cases.append(
            {
                "id": name,
                "law": {"id": name, "model": m.record()},
                "protocol": repair_protocol(m),
            }
        )
    plan = {
        "schema": "omega.coupled-engineering-plan/1",
        "date": "2026-10-25",
        "cases": cases,
        "spec": "research/platform/specs/S3_REPAIR_ENGINEERING_r1.md",
        "snapshot_files": [
            "scripts/write_s3_protocols.py",
            "tests/test_repair.py",
            "tests/test_foreclosure.py",
        ],
        "caps": {
            "case_seconds": 300,
            "job_memory_bytes": 2 * 1024**3,
            "case_output_bytes": 32 * 1024**2,
            "batch_seconds": 600,
            "batch_output_bytes": 64 * 1024**2,
        },
    }
    out = ROOT / "research/platform/models/s3-repair/ENGINEERING_PLAN.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print("Wrote two repair engineering cases")


if __name__ == "__main__":
    main()
