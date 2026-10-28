"""Build the bounded R2 integration smoke input without evaluating rankings."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from omega_cosmology.testbed.construction_chain import construction_chain


def condition(coordinate, value):
    return {"coordinate": coordinate, "operator": "eq", "value": value}


def protocol(model, root):
    absent = []
    rules = {r.id for r in model.rules}
    for name in (
        "products.assisted_B",
        "products.assisted_C",
        "secondary_access.transduce",
    ):
        if name not in rules:
            absent.append(name)
    event_rules = {
        "A_paid": "A.paid_build",
        "A_basal": "A.basal_build",
        "B_paid": "products.paid_B",
        "B_basal": "products.basal_B",
        "B_assisted": "products.assisted_B",
        "C_assisted": "products.assisted_C",
        "secondary_access": "secondary_access.transduce",
        "primary_access": "A.unlock",
        "primary_capture": "primary_capture.capture",
        "C_capture": "primary_capture.assisted_capture",
        "secondary_capture": "secondary_capture.capture",
        "rotor_stroke": "rotor.stroke",
        "rotor_relax": "rotor.relax",
    }
    observations = [
        {"id": k, "terms": [[k, 1]]}
        for k in ("A.active", "products.B", "products.C", "bank.ticks", "rotor.state")
    ]
    observations.append(
        {
            "id": "A_and_B",
            "constant": 1,
            "conditions": [condition("A.active", 1), condition("products.B", 1)],
        }
    )
    selector = lambda name: {"rules": [name], "direction": 1}
    monitor = {
        "id": "paid_connected_chain",
        "stages": [
            {"name": "build_A", "advance": [selector("A.paid_build")]},
            {
                "name": "A_builds_B",
                "advance": [selector("products.assisted_B")],
                "abort": [{"target": [condition("A.active", 0)]}],
            },
            {
                "name": "B_unlocks",
                "advance": [selector("secondary_access.transduce")],
                "abort": [{"target": [condition("products.B", 0)]}],
            },
            {
                "name": "capture_release",
                "advance": [selector("secondary_capture.capture")],
                "abort": [
                    {"target": [condition("products.B", 0)]},
                    {"target": [condition("secondary.state", 0)]},
                    {"target": [condition("secondary.state", 1)]},
                ],
            },
        ],
    }
    return {
        "id": "R2-integrated-smoke",
        "preparations": [
            {
                "id": "common_unbuilt",
                "roots": [[list(root), 1.0]],
                "conditioning": "full_present",
            }
        ],
        "energy_per_root": str(model.energy(root)),
        "coordinate_order": [c.name for c in model.coordinates],
        "horizons": [4, 16, 64],
        "cadences": [0.25, 0.5],
        "max_states": 400,
        "max_dense_bytes": 64 * 1024**2,
        "validation_mode": "sampled_endpoint_crosscheck",
        "sufficiency": "All distinct constituent, precursor, rotor, carrier and bank states; fixed native Markov law",
        "boundary_scope": {
            "bath_beta": 1,
            "sources": {
                "primary": {"work": "3", "conductance": 0.08},
                "secondary": {"work": "3", "conductance": 0.08},
            },
            "exterior": "bath and source histories unresolved",
        },
        "conserved": [
            "A material slot",
            "shared B/C precursor",
            "two carriers",
            "rotor material slot",
        ],
        "observables": observations,
        "event_readouts": [
            {
                "id": name + suffix,
                "selectors": [{"rules": [rule], "direction": direction}],
            }
            for name, rule in event_rules.items()
            for direction, suffix in ((1, ".forward"), (-1, ".reverse"))
        ],
        "monitors": [monitor],
        "structural_analysis": {
            "organizations": [
                {
                    "id": "both_interfaces",
                    "definition": "A and B physically present",
                    "coordinates": ["A.active", "products.B"],
                    "functional_any_of": [
                        [condition("A.active", 1), condition("products.B", 1)]
                    ],
                }
            ]
        },
        "numerical": {
            "kernel_agreement_tolerance": 1e-10,
            "independent_history_tolerance": 1e-8,
        },
        "scope": "Finite construction/access mechanisms; no thermal spatial baseline, packet provenance, optimal policy or ethical verdict",
    }, absent


def make_plan():
    cases = []
    for id, params in (
        ("productive", {}),
        ("no_construction_assistance", {"assist": False}),
        ("no_secondary_access", {"access": False}),
        ("neither_link", {"assist": False, "access": False}),
    ):
        model, root, bindings = construction_chain(**params)
        query, absent = protocol(model, root)
        cases.append(
            {
                "id": id,
                "parameters": params,
                "law": {
                    "id": id,
                    "model": model.record(),
                    "absent_query_rules": absent,
                },
                "protocol": query,
                "bindings": bindings,
            }
        )
    return {
        "schema": "omega.r2-integrated-smoke/1",
        "spec": "research/platform/specs/R2_INTEGRATED_SMOKE_r2.md",
        "cases": cases,
        "cadences": [0.25, 0.5],
        "calibration": {
            "horizon": 64,
            "target": "productive",
            "control": "no_secondary_access",
            "bounds": {"rotor_stroke": [1e-5, 0.5], "rotor_relax": [1e-5, 0.5]},
            "absolute_tolerance": 1e-8,
            "relative_tolerance": 0.001,
            "fit_evaluations": 24,
        },
        "caps": {"seconds": 900, "memory_bytes": 1024**3, "output_bytes": 64 * 1024**2},
    }


if __name__ == "__main__":
    path = ROOT / "research/platform/models/r2-integrated/ENGINEERING_PLAN.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(make_plan(), indent=2) + "\n", encoding="utf-8")
    print(path.relative_to(ROOT))
