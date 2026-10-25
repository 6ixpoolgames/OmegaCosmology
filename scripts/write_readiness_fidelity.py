"""Freeze a bounded readiness fidelity/resource pilot, without changing physics."""

import json

from write_coupled_smoke_plan import cond
from write_readiness_smoke import ROOT, protocol

from omega_cosmology.testbed.readiness import readiness_world


def pilot_protocol(model, *, policy, quantum, effort):
    p = protocol(model, policy=policy, quantum=quantum, effort=effort)
    p["id"] = "readiness-fidelity." + policy + "." + quantum
    p["horizons"] = [64, 256]
    p["max_states"] = 3000
    p["max_dense_bytes"] = 256 * 1024**2
    p["max_occupation_dense_bytes"] = 2 * 1024**3
    p["structural_analysis"]["max_functional_query_states"] = 12000
    for spec in p["projected_histories"]:
        spec["max_workspace_bytes"] = 256 * 1024**2
    p["scope"] = (
        "Engineering fidelity/resource pilot; no policy optimization, clinical "
        "learning claim or physical-faithfulness certificate"
    )
    for cue in (0, 1):
        for opened in (0, 1):
            p["observables"].append(
                {
                    "id": f"cue_joint_{cue}_{opened}",
                    "constant": 1,
                    "conditions": [
                        cond("body.cue", "eq", cue),
                        cond("barrier", "eq", opened),
                    ],
                }
            )
    for marked in (0, 1):
        p["observables"].append(
            {
                "id": f"marked_{marked}",
                "constant": 1,
                "conditions": [cond("body.failures", "ge" if marked else "eq", marked)],
            }
        )
    # Count only reactions that really change the mark. Saturated attempts do not.
    failed_writes = [
        r.id
        for r in model.rules
        if r.id.startswith(("blocked_effort_", "effort_damage_"))
        and dict(r.changes).get("body.failures", 0) == 1
    ]
    relax = [r.id for r in model.rules if r.id.startswith("failure_relax_")]
    clears = [r.id for r in model.rules if r.id.startswith("cue_clear_")]
    for name, rules, direction in [
        ("marks_failed_attempt", failed_writes, 1),
        ("marks_undo_attempt", failed_writes, -1),
        ("marks_reverse_clear", clears, -1),
        ("marks_thermal", relax, -1),
        ("marks_cleared", clears, 1),
        ("marks_relaxed", relax, 1),
    ]:
        p["event_readouts"].append(
            {
                "id": name,
                "selectors": [{"rules": rules, "direction": direction}]
                if rules
                else [],
            }
        )
    return p


def main():
    cases = []
    # Largest representation first. No shrinking on failure.
    settings = [("reengage", ".25", ".25")] + [
        (policy, ".5", ".5") for policy in ("reengage", "always", "conserve", "stop")
    ]
    for policy, quantum, effort in settings:
        model = readiness_world(policy, bank_quantum=quantum, effort_bill=effort)
        cases.append(
            {
                "id": ("quarter_" if quantum == ".25" else "half_") + policy,
                "law": {"id": policy, "model": model.record()},
                "protocol": pilot_protocol(
                    model, policy=policy, quantum=quantum, effort=effort
                ),
            }
        )
    plan = {
        "schema": "omega.coupled-engineering-plan/1",
        "date": "2026-10-26",
        "cases": cases,
        "spec": "research/platform/specs/READINESS_FIDELITY_PILOT_r1.md",
        "snapshot_files": [
            "scripts/write_readiness_fidelity.py",
            "scripts/report_readiness_fidelity.py",
            "scripts/write_readiness_smoke.py",
            "tests/test_readiness_fidelity.py",
        ],
        "caps": {
            "case_seconds": 600,
            "job_memory_bytes": 2816 * 1024**2,
            "case_output_bytes": 16 * 1024**2,
            "batch_seconds": 1800,
            "batch_output_bytes": 64 * 1024**2,
        },
    }
    out = ROOT / "research/platform/models/struggle-readiness/FIDELITY_PLAN.json"
    out.write_text(json.dumps(plan, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "written",
                "cases": len(cases),
                "path": out.relative_to(ROOT).as_posix(),
            }
        )
    )


if __name__ == "__main__":
    main()
