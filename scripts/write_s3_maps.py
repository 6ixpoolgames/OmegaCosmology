"""Write compact S3 maps after repair and occupied-contact feasibility checks."""

import json
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from write_coupled_smoke_plan import case
from write_s3_protocols import repair_protocol

from omega_cosmology.testbed.occupancy import occupied_ecology
from omega_cosmology.testbed.physics import LocalModel
from omega_cosmology.testbed.repair import repair_capacity_world

FOLDER = "research/studies/S3-repair-and-interaction"


def finish(p, name):
    p["schema"] = "omega.finite-study-protocol/1"
    p["id"] = "S3." + name
    p["numerical"]["sign_deadband_bits"] = 1e-6
    p["source_inputs"] = [
        "scripts/write_s3_maps.py",
        "scripts/write_s3_protocols.py",
        "scripts/write_coupled_smoke_plan.py",
        "tests/test_repair.py",
        "tests/test_foreclosure.py",
        FOLDER + "/SPECIFICATION_r1.md",
    ]
    p["execution"] = {"max_workers": 1}
    p["caps"] = {
        "case_wall_seconds": 300 if name == "repair" else 600,
        "job_memory_bytes": 2 * 1024**3,
        "case_output_bytes": 16 * 1024**2,
        "batch_wall_seconds": 1200 if name == "repair" else 7200,
        "batch_output_bytes": 32 * 1024**2 if name == "repair" else 128 * 1024**2,
    }
    target = ROOT / FOLDER / ("PROTOCOL_" + name.upper() + ".json")
    target.write_text(json.dumps(p, indent=2) + "\n", encoding="utf-8")
    print(name, len(p["case_grid"]), "cases")


def main():
    repair_laws = []
    for supply in (0.02, 0.12):
        for feedback in (True, False):
            name = (
                "S"
                + str(supply).replace(".", "p")
                + ("_feedback" if feedback else "_no_feedback")
            )
            m = repair_capacity_world(source_conductance=supply, feedback=feedback)
            repair_laws.append(
                {
                    "id": name,
                    "model": m.record(),
                    "supply": supply,
                    "feedback": feedback,
                    "structural_analysis": repair_protocol(m)["structural_analysis"],
                }
            )
    p = repair_protocol(repair_capacity_world(), horizons=(16, 64, 256, 1024, 4096))
    p["question"] = (
        "How do matched repair/access faults depend on supply, reconstruction feedback and horizon?"
    )
    p["laws"] = repair_laws
    p["cadences"] = [0.125, 0.25, 0.5]
    p["case_grid"] = [[l["id"], 0.25] for l in repair_laws] + [
        [l["id"], dt] for l in repair_laws if l["feedback"] for dt in (0.125, 0.5)
    ]
    finish(p, "repair")
    groups = [
        {"id": g, "members": [g + ".x", g + ".y"], "access_member": g + ".x"}
        for g in ("A", "B")
    ]
    local = [
        (g + "." + a, g + "." + b)
        for g in ("A", "B")
        for a, b in [("x", "y"), ("y", "x")]
    ]
    cross = [("A.x", "B.y"), ("B.x", "A.y")]
    settings = [
        ("one_way", local + cross[:1], 0.08, 0.04, 1),
        ("none", [], 0.08, 0.04, 1),
        ("local", local, 0.08, 0.04, 1),
        ("reciprocal", local + cross, 0.08, 0.04, 1),
        ("one_way_low_supply", local + cross[:1], 0.02, 0.04, 1),
        ("one_way_high_supply", local + cross[:1], 0.12, 0.04, 1),
        ("one_way_slow_contact", local + cross[:1], 0.08, 0.01, 1),
        ("one_way_fast_contact", local + cross[:1], 0.08, 0.16, 1),
        ("one_way_low_local", local + cross[:1], 0.08, 0.04, 0.25),
        ("one_way_high_local", local + cross[:1], 0.08, 0.04, 4),
    ]
    laws = []
    for name, conversions, supply, binding, factor in settings:
        m = occupied_ecology(
            groups,
            extra_assistance=cross,
            converting_edges=conversions,
            bank_quantum=".5",
            construction_bill_ticks=2,
            source_conductance=supply,
            binding_conductance=binding,
        )
        if factor != 1:
            selected = {"assisted_construct_" + a + "_to_" + b for a, b in local}
            m = LocalModel(
                m.id,
                m.coordinates,
                [
                    replace(r, conductance=r.conductance * factor)
                    if r.id in selected
                    else r
                    for r in m.rules
                ],
                m.energy_terms,
                beta=m.beta,
                forbidden=m.forbidden,
                relations=m.relations,
                material=m.material,
            )
        laws.append(
            {
                "id": name,
                "model": m.record(),
                "settings": {
                    "supply": supply,
                    "binding": binding,
                    "local_factor": factor,
                },
            }
        )
    root = tuple(1 if c.role == "constructed_component" else 0 for c in m.coordinates)
    p = case("S3interaction", m, root, groups)["protocol"]
    p["question"] = (
        "What do occupied productive contacts buy each part and the whole under competing uses?"
    )
    p["laws"] = laws
    p["horizons"] = [16, 64, 256, 1024]
    p["cadences"] = [0.25, 0.5]
    p["case_grid"] = [[l["id"], 0.25] for l in laws] + [
        ["local", 0.5],
        ["one_way", 0.5],
    ]
    p["max_states"] = 2000
    p["max_dense_bytes"] = 128 * 1024**2
    p["max_occupation_dense_bytes"] = 512 * 1024**2
    p["structural_analysis"]["ancestry"] = []
    p["projected_histories"] = [
        {
            "id": g["id"],
            "coordinates": g["members"] + [g["id"] + ".bank"],
            "conditioning": "full_present",
            "memory": 1,
        }
        for g in groups
    ]
    contacts = [c.name for c in m.coordinates if c.role == "catalytic_contact"]
    p["observables"] += [
        {"id": "occupied_contacts", "terms": [[c, 1] for c in contacts]}
    ]
    for g in groups:
        access = g["access_member"]
        incident = [
            r["id"]
            for r in m.relations
            if "interface_capacity" in r and access in (r["parent"], r["child"])
        ]
        p["observables"] += [
            {"id": g["id"] + ".active", "terms": [[f, 1] for f in g["members"]]},
            {
                "id": g["id"] + ".free_access",
                "constant": 1,
                "conditions": [{"coordinate": access, "operator": "eq", "value": 1}]
                + [{"coordinate": c, "operator": "eq", "value": 0} for c in incident],
            },
        ]
    p["event_readouts"] = [
        {
            "id": "conversion_" + a + "_to_" + b,
            "selectors": [
                {"rules": ["assisted_construct_" + a + "_to_" + b], "direction": 1}
            ],
        }
        for a, b in local + cross
    ]
    p["scope"] = (
        "Finite occupied interactions; fixed contact geometry and initial endowment; no controllers or ethical verdict"
    )
    finish(p, "interaction")


if __name__ == "__main__":
    main()
