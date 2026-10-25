"""Define the paid further-capacity experiment without evaluating outcomes."""

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def condition(name, op, value):
    return {"coordinate": name, "operator": op, "value": value}


def selector(rules=(), direction=None, source=(), target=()):
    result = {"rules": list(rules), "source": list(source), "target": list(target)}
    if direction is not None:
        result["direction"] = direction
    return result


def main():
    from omega_cosmology.testbed.physics import LocalModel

    fixture = json.loads(
        (ROOT / "research/platform/models/R2.json").read_text(encoding="utf-8")
    )
    model = LocalModel.from_record(fixture["model"])
    preparations = [
        {"id": name, "roots": [[state, 1.0]], "conditioning": "full_present"}
        for name, state in [
            ("assembly_seed", (1, 1, 1, 1, 2, 0)),
            ("unassembled", (0, 0, 0, 1, 3, 0)),
            ("store_seed", (1, 1, 1, 1, 1, 1)),
        ]
    ]
    for prep in preparations:
        state = tuple(prep["roots"][0][0])
        model.validate(state)
        if str(model.energy(state)) != "9/2":
            raise ValueError("Unmatched material/energy preparation")
    laws = []
    for driven in (True, False):
        for mode in ("assisted", "basal", "sham"):
            name = ("driven" if driven else "source_off") + "__" + mode
            record = copy.deepcopy(fixture["model"])
            record["id"] = "R2." + name
            record["rules"] = [
                r
                for r in record["rules"]
                if (mode != "basal" or r["id"] != "build_store_assisted")
                and (driven or r["boundary"] == "native")
            ]
            if mode == "sham":
                record["forbidden"].append([condition("bank", "ge", 5)])
            laws.append({"id": name, "driven": driven, "mode": mode, "model": record})
    store_lost = [selector(target=[condition("store.built", "eq", 0)])]
    high = condition("bank", "ge", 5)
    restored = [condition("a.active", "eq", 1), condition("b.active", "eq", 1)]
    construction = selector(["build_store", "build_store_assisted"], 1)
    extra_capture = selector(
        ["capture"],
        1,
        [
            condition("bank", "ge", 3),
            condition("bank", "le", 4),
            condition("store.built", "eq", 1),
        ],
    )
    repair = selector(["paid_activate_a.active", "paid_activate_b.active"], 1, [high])
    complete_repair = selector(repair["rules"], 1, [high], restored)
    monitor = {
        "id": "capacity_to_reconstruction",
        "meaning": "First new store construction episode only; no restarts. Ordered witness is not a generation count.",
        "stages": [
            {"name": "await_first_store_construction", "advance": [construction]},
            {
                "name": "await_expanded_only_capture",
                "advance": [extra_capture],
                "abort": store_lost,
            },
            {
                "name": "await_high_bank_paid_repair",
                "advance": [complete_repair],
                "abort": store_lost + [selector(target=[condition("bank", "le", 4)])],
            },
            {
                "name": "await_rebinding",
                "advance": [selector(["binding"], 1)],
                "abort": store_lost
                + [
                    selector(target=[condition("a.active", "eq", 0)]),
                    selector(target=[condition("b.active", "eq", 0)]),
                ],
            },
        ],
    }
    obs = [
        {"id": "bound", "terms": [["bond", 1]]},
        {"id": "active", "terms": [["a.active", 1], ["b.active", 1]]},
        {"id": "store_built", "terms": [["store.built", 1]]},
        {"id": "bank_energy", "terms": [["bank", 0.5]]},
        {"id": "high_bank", "constant": 1, "conditions": [high]},
        {
            "id": "excess_stored_energy",
            "terms": [["bank", 0.5]],
            "constant": -2,
            "conditions": [high],
        },
    ]
    events = [
        {"id": "expanded_capture_forward", "selectors": [extra_capture]},
        {
            "id": "expanded_capture_reverse",
            "selectors": [selector(["capture"], -1, [high])],
        },
        {"id": "high_bank_paid_activation", "selectors": [repair]},
        {
            "id": "high_bank_repair_energy_above_old_cap",
            "selectors": [repair],
            "amount": {"terms": [["bank", 0.5]], "constant": -2, "min": 0, "max": 1},
        },
    ]
    contrasts = []
    for law in laws:
        for a, b in [("assembly_seed", "unassembled"), ("store_seed", "assembly_seed")]:
            contrasts.append(
                {
                    "id": law["id"] + ":" + a + "-minus-" + b,
                    "kind": "preparation",
                    "first": [law["id"], a],
                    "second": [law["id"], b],
                }
            )
    for prefix in ("driven", "source_off"):
        for prep in preparations:
            for comparator, kind in [
                ("basal", "construction_assistance"),
                ("sham", "functional_capacity"),
            ]:
                contrasts.append(
                    {
                        "id": prefix
                        + ":assisted-minus-"
                        + comparator
                        + ":"
                        + prep["id"],
                        "kind": kind,
                        "first": [prefix + "__assisted", prep["id"]],
                        "second": [prefix + "__" + comparator, prep["id"]],
                    }
                )
    for mode in ("assisted", "basal", "sham"):
        for prep in preparations:
            contrasts.append(
                {
                    "id": mode + ":driven-minus-source_off:" + prep["id"],
                    "kind": "boundary",
                    "first": ["driven__" + mode, prep["id"]],
                    "second": ["source_off__" + mode, prep["id"]],
                }
            )
    protocol = {
        "schema": "omega.finite-study-protocol/1",
        "id": "R2-further-capacity-r1",
        "question": "Does an access interface assist paid construction of useful capacity, and does its stored energy feed actual reconstruction?",
        "energy_per_root": "9/2",
        "preparations": preparations,
        "laws": laws,
        "coordinate_order": [c.name for c in model.coordinates],
        "horizons": [16, 64, 256, 1024],
        "cadences": [0.125, 0.25, 0.5],
        "primary_cadence": 0.25,
        "reference_time": 1.0,
        "sufficiency": "All fixed material slots, local interface/capacity constraints, energy, rate and Markov boundary dependencies retained",
        "boundary_scope": {
            "bath_beta": 1.0,
            "source": "Same reversible work-exchange prescription when driven; source-off is a boundary-law contrast",
            "unresolved": "Bath/source histories; no exterior cancellation asserted",
        },
        "conserved": [
            "two apparatus constituent slots",
            "one latent store constituent slot",
            "one carrier",
        ],
        "observables": obs,
        "event_readouts": events,
        "monitors": [monitor],
        "comparisons": contrasts,
        "bank_account": {
            "coordinate": "bank",
            "quantum": 0.5,
            "capture_rules": ["capture"],
            "spend_rules": {
                "paid_activate_a.active": 1.0,
                "paid_activate_b.active": 1.0,
                "upkeep": 0.5,
                "build_store": 1.0,
                "build_store_assisted": 1.0,
            },
        },
        "numerical": {
            "sign_deadband_bits": 1e-7,
            "independent_history_tolerance": 1e-7,
            "kernel_agreement_tolerance": 1e-12,
            "basis": "Conservative float64 validation allowance for up to8192 accumulated steps; not a rigorous interval certificate",
        },
        "caps": {
            "case_wall_seconds": 120,
            "job_memory_bytes": 2 * 1024**3,
            "case_output_bytes": 32 * 1024**2,
            "batch_wall_seconds": 600,
            "batch_output_bytes": 128 * 1024**2,
        },
        "source_inputs": [
            "research/platform/models/R2.json",
            "scripts/write_r2_protocol.py",
            "tests/test_finite_study.py",
        ],
        "scope": "Bounded further-enabling and first-episode feedback witness; no three-generation compounding, microscopic gas, optimizer or ethical verdict. All represented randomness counts.",
        "controls": "Basal construction remains in all laws. Sham builds the same costed component with the same conductances but no high-bank capacity. Realized flux/work are not forced equal.",
    }
    out = ROOT / "research/studies/R2-further-capacity"
    out.mkdir(parents=True, exist_ok=True)
    (out / "PROTOCOL.json").write_text(
        json.dumps(protocol, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "laws": len(laws),
                "preparations": len(preparations),
                "cases": len(laws) * 3,
                "profile_rows": len(laws) * 3 * 3 * 4,
            }
        )
    )


if __name__ == "__main__":
    main()
