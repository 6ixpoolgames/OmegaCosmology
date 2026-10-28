"""Frozen, capped R2 integration with moment-only physical calibration first."""

import argparse
import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
PLAN = "research/platform/models/r2-integrated/ENGINEERING_PLAN.json"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def compile_case(case):
    import numpy as np

    from omega_cosmology.testbed.backends import enumerate_model
    from omega_cosmology.testbed.physics import LocalModel

    model = LocalModel.from_record(case["law"]["model"])
    root = tuple(case["protocol"]["preparations"][0]["roots"][0][0])
    compiled = enumerate_model(model, [root], max_states=400)
    compiled.require_complete()
    mu = np.zeros(len(compiled.states))
    mu[compiled.index[root]] = 1
    return compiled, mu


def physical_moments(compiled, mu, horizon, *, diagnostics=None):
    import numpy as np

    from omega_cosmology.testbed.history import distributions_and_occupation

    _, occupation = distributions_and_occupation(compiled, mu, horizon)
    accepted = np.zeros(len(mu))
    for i, _, event in compiled.ledger:
        accepted[i] += event.rate * max(event.work, 0)
    moments = {
        "expected_jumps": float(occupation @ -compiled.q.diagonal()),
        "work_accepted_gross": float(occupation @ accepted),
    }
    if diagnostics is None:
        return moments
    bank = compiled.model.indices[diagnostics["bank_coordinate"]]
    bank_name = diagnostics["bank_coordinate"]
    from omega_cosmology.testbed.physics import rational

    if any(
        t.conditions
        and (
            t.coordinate == bank_name
            or any(c.coordinate == bank_name for c in t.conditions)
        )
        for t in compiled.model.energy_terms
    ):
        raise ValueError("Payment diagnostic requires additive bank energy")
    tick = float(
        sum(
            (
                rational(t.coefficient)
                for t in compiled.model.energy_terms
                if t.coordinate == bank_name
            ),
            rational(0),
        )
    )
    if tick <= 0:
        raise ValueError("Payment diagnostic needs a positive bank energy tick")
    rules = {r.id: r for r in compiled.model.rules}
    paid = thermal = withdrawal = refund = 0.0
    channels = {}
    # Derive the actual bank tick from the same physical Hamiltonian.
    for i, _, event in compiled.ledger:
        count = float(occupation[i] * event.rate)
        roles = rules[event.rule_id].roles
        if diagnostics["paid_role"] in roles:
            paid += count
            delta = tick * (event.target[bank] - compiled.states[i][bank])
            withdrawal += count * max(-delta, 0)
            refund += count * max(delta, 0)
            key = event.rule_id + (".forward" if event.direction == 1 else ".reverse")
            channels[key] = channels.get(key, 0.0) + count
        if diagnostics["thermal_role"] in roles:
            thermal += count
    return moments, {
        "paid_channel_events": paid,
        "thermal_channel_events": thermal,
        "paid_channel_fraction": paid / (paid + thermal) if paid + thermal else 0,
        "gross_bank_withdrawal": withdrawal,
        "gross_bank_refund": refund,
        "net_bank_payment": withdrawal - refund,
        "paid_channel_counts": channels,
        "scope": "All native directions counted; paid-channel activity alone is not net payment",
    }


def pair_contract(a, b, cadence, horizon, *, compiled_cases=None):
    from omega_cosmology.testbed.semantics import (
        ComparisonSpec,
        LawSpec,
        ObservationSpec,
        PresentSpec,
        QuantitySpec,
        validate_comparison,
    )

    comparison = ComparisonSpec(
        "paired_mechanism",
        "mechanism",
        horizon,
        cadence,
        {
            "endowment": "Actual roots, energy and executable inventories checked",
            "boundary": "Same drive and native source barriers",
        },
    )

    def arm(case):
        c = (
            compiled_cases[case["id"]]
            if compiled_cases is not None
            else compile_case(case)[0]
        )
        root = tuple(case["protocol"]["preparations"][0]["roots"][0][0])
        return {
            "compiled": c,
            "present": PresentSpec(
                "common", ((root, 1),), sufficiency=case["protocol"]["sufficiency"]
            ),
            "law": LawSpec(
                case["id"], c.model_hash, case["protocol"]["boundary_scope"]
            ),
            "comparison": comparison,
            "observation": ObservationSpec(
                "whole", tuple(x.name for x in c.model.coordinates)
            ),
            "quantity": QuantitySpec(
                "H", "Complete sampled history", "bits", "full_present"
            ),
        }

    return validate_comparison(comparison, arm(a), arm(b))


def worker(out, manifest, *, plan_path=PLAN):
    from omega_cosmology.testbed.finite_study import evaluate_case
    from omega_cosmology.testbed.matching import (
        MomentSpec,
        match_one_physical_moment,
        match_physical_moments,
    )
    from omega_cosmology.testbed.thermodynamics import audit_equilibrium

    start = perf_counter()
    plan = json.loads((ROOT / plan_path).read_text())
    if plan["schema"] == "omega.r2-paid-cycle-control/1":
        from write_r2_paid_cycle_plan import protocol

        from omega_cosmology.testbed.paid_cycle import paid_cycle_chain as build_model
    elif plan["schema"] == "omega.r2-integrated-smoke/1":
        from write_r2_integrated_plan import protocol

        from omega_cosmology.testbed.construction_chain import (
            construction_chain as build_model,
        )
    else:
        raise ValueError("Unsupported physical control plan")
    cases = {c["id"]: c for c in plan["cases"]}
    calibration = plan["calibration"]
    target_compiled, mu = compile_case(cases["productive"])
    diagnostics = plan.get("physical_diagnostics")
    evaluated = []
    result = physical_moments(
        target_compiled, mu, calibration["horizon"], diagnostics=diagnostics
    )
    target, target_payment = result if diagnostics else (result, None)
    physical_audit = {"productive": audit_equilibrium(target_compiled)}

    def control_case(params):
        physical_params = (
            {"charge": params["rate"], "reset": params["rate"]}
            if calibration.get("method") == "activity_diagonal"
            else params
        )
        physical_params = {**plan.get("control_parameters", {}), **physical_params}
        model, root, bindings = build_model(access=False, **physical_params)
        p, absent = protocol(model, root)
        return {
            "id": plan.get("control_id", "matched_rotor"),
            "parameters": {"access": False, **physical_params},
            "law": {
                "id": plan.get("control_id", "matched_rotor"),
                "model": model.record(),
                "absent_query_rules": absent,
            },
            "protocol": p,
            "bindings": bindings,
        }

    def evaluate(params):
        c, initial = compile_case(control_case(params))
        if diagnostics:
            target_rules = {r.id: r for r in target_compiled.model.rules}
            actual_rules = {r.id: r for r in c.model.rules}
            expected_ids = {
                k
                for k, r in target_rules.items()
                if "access.transduction" not in r.roles
            }
            if set(actual_rules) != expected_ids:
                raise ValueError("Paid control changes undeclared native channels")
            for key, rule in actual_rules.items():
                if (
                    diagnostics["paid_role"] not in rule.roles
                    and rule != target_rules[key]
                ):
                    raise ValueError(
                        "Non-paid control physics changed during calibration"
                    )
        audit_equilibrium(c)
        result = physical_moments(
            c, initial, calibration["horizon"], diagnostics=diagnostics
        )
        moments, payment = result if diagnostics else (result, None)
        evaluated.append({"parameters": params, "moments": moments, "payment": payment})
        return moments

    match = (
        match_one_physical_moment
        if calibration.get("method") == "activity_diagonal"
        else match_physical_moments
    )
    extra = (
        {"primary": "expected_jumps"}
        if calibration.get("method") == "activity_diagonal"
        else {}
    )
    fit = match(
        evaluate,
        target,
        calibration["bounds"],
        max_evaluations=calibration["fit_evaluations"],
        **extra,
        moment_specs={
            k: MomentSpec(
                k,
                "events" if k == "expected_jumps" else "model_energy",
                calibration["horizon"],
                "continuous_integral",
                calibration["absolute_tolerance"],
                calibration["relative_tolerance"],
            )
            for k in target
        },
    )
    fit["independent_replay"] = evaluate(fit["best"]["parameters"])
    selected_payment = evaluated[-1]["payment"]
    qualified = (
        selected_payment is not None
        and selected_payment["net_bank_payment"] > 1e-8
        and selected_payment["paid_channel_fraction"] > 0.5
    )
    write(
        out / "CALIBRATION.json",
        {
            "completed_before_history_scoring": True,
            "calibration": calibration,
            "fit": fit,
            "physical_evaluations": evaluated,
            "target_payment": target_payment,
            "selected_payment": selected_payment,
            "net_paying_majority_paid_control": qualified,
            "seconds": perf_counter() - start,
        },
    )
    cases[plan.get("control_id", "matched_rotor")] = control_case(
        fit["best"]["parameters"]
    )
    write(out / "EXECUTION_CASES.json", list(cases.values()))
    if plan.get("require_net_paying_control_before_history") and not qualified:
        write(
            out / "RESULT.json",
            {
                "status": "passed",
                "engineering_only": True,
                "source_manifest_sha256": digest(manifest),
                "history_evaluated": False,
                "boundary": "No net-paying majority-paid selected control; stop before history scoring",
                "calibration_status": fit["status"],
                "cases": [],
                "comparisons": [],
                "wall_seconds": perf_counter() - start,
            },
        )
        return
    print(
        json.dumps(
            {
                "calibration": fit["status"],
                "parameters": fit["best"]["parameters"],
                "seconds": perf_counter() - start,
            }
        ),
        flush=True,
    )
    contracts = []
    compiled_cases = {name: compile_case(case)[0] for name, case in cases.items()}
    # Validate actual executable paired inputs before any score is computed.
    for name, case in cases.items():
        if name != "productive":
            for cadence in plan["cadences"]:
                for horizon in case["protocol"]["horizons"]:
                    contracts.append(
                        {
                            "first": "productive",
                            "second": name,
                            "cadence": cadence,
                            "horizon": horizon,
                            "contract": pair_contract(
                                cases["productive"],
                                case,
                                cadence,
                                horizon,
                                compiled_cases=compiled_cases,
                            ),
                        }
                    )
    write(out / "COMPARISON_CONTRACTS.json", contracts)
    results = {}
    for name, case in cases.items():
        for cadence in plan["cadences"]:
            result = evaluate_case(case["protocol"], case["law"], cadence)
            key = name + "__dt" + str(cadence)
            write(out / (key + ".json"), result)
            results[name, cadence] = result
            print(
                json.dumps(
                    {
                        "case": name,
                        "cadence": cadence,
                        "states": result["states"],
                        "profiles": len(result["rows"]),
                        "seconds": result["worker_seconds"],
                    }
                ),
                flush=True,
            )
    differences = []
    for name in cases:
        if name == "productive":
            continue
        for cadence in plan["cadences"]:
            for a, b in zip(
                results["productive", cadence]["rows"], results[name, cadence]["rows"]
            ):
                differences.append(
                    {
                        "first": "productive",
                        "second": name,
                        "cadence": cadence,
                        "horizon": a["horizon"],
                        "delta_history_bits": a["history"]["ell_bits"]
                        - b["history"]["ell_bits"],
                        "delta_expected_jumps": a["physical"]["expected_jumps"]
                        - b["physical"]["expected_jumps"],
                        "delta_accepted_work": a["physical"]["work_accepted_gross"]
                        - b["physical"]["work_accepted_gross"],
                        "delta_Nbar": a["activity"]["expected_jumps"]
                        - b["activity"]["expected_jumps"],
                        "delta_F_bits": a["activity"]["finite_coefficient_bits"]
                        - b["activity"]["finite_coefficient_bits"],
                        "delta_rate_bits_per_time": a["asymptotic"][
                            "rate_bits_per_time"
                        ]
                        - b["asymptotic"]["rate_bits_per_time"],
                        "delta_B_integrated": a["observables"]["products.B"][
                            "integrated"
                        ]
                        - b["observables"]["products.B"]["integrated"],
                    }
                )
    summary = {
        "status": "passed",
        "engineering_only": True,
        "source_manifest_sha256": digest(manifest),
        "calibration_status": fit["status"],
        "physical_pre_audit": physical_audit,
        "cases": [
            {
                "id": name,
                "cadence": cadence,
                "states": result["states"],
                "profiles": len(result["rows"]),
                "sha256": digest(out / (name + "__dt" + str(cadence) + ".json")),
            }
            for (name, cadence), result in results.items()
        ],
        "comparisons": differences,
        "wall_seconds": perf_counter() - start,
        "limits": "Finite capped smoke; T64 moments only if fit passes. No spatial thermal baseline, unmatched-rate work equivalence, unbounded compounding or ethical verdict.",
    }
    write(out / "RESULT.json", summary)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--worker", action="store_true")
    p.add_argument("--manifest", type=Path)
    p.add_argument("--plan", type=Path, default=Path(PLAN))
    args = p.parse_args()
    if args.worker:
        if sys.stdin.readline().strip() != "GO":
            raise RuntimeError("Capped supervisor required")
        manifest = json.loads(args.manifest.read_text())
        for row in manifest["files"]:
            if digest(ROOT / row["path"]) != row["sha256"]:
                raise ValueError("Frozen source changed")
        worker(args.out_dir, args.manifest, plan_path=manifest.get("plan", PLAN))
        return
    out = args.out_dir.resolve()
    if out.exists() or not out.is_relative_to(ROOT / "runs"):
        p.error("Choose fresh output inside runs")
    plan_path = (ROOT / args.plan).resolve()
    if not plan_path.is_relative_to(ROOT):
        p.error("Plan must be inside this repository")
    relative_plan = plan_path.relative_to(ROOT).as_posix()
    plan = json.loads(plan_path.read_text())
    out.mkdir(parents=True)
    files = list((ROOT / "src/omega_cosmology/testbed").glob("*.py")) + [
        ROOT / "src/omega_cosmology/__init__.py",
        ROOT / "pyproject.toml",
        plan_path,
        Path(__file__).resolve(),
        ROOT / "scripts/write_r2_integrated_plan.py",
        ROOT / "tests/test_module_bindings.py",
        ROOT / plan["spec"],
    ]
    files.extend(ROOT / name for name in plan.get("support_scripts", ()))
    files.extend(ROOT / name for name in plan.get("test_files", ()))
    files.extend(ROOT / name for name in plan.get("snapshot_inputs", ()))
    if any(not file.resolve().is_relative_to(ROOT) for file in files):
        raise ValueError("Snapshot inputs must be repository files")
    manifest = {
        "schema": "omega.r2-integrated-snapshot/1",
        "plan": relative_plan,
        "caps": plan["caps"],
        "files": [],
    }
    for file in files:
        rel = file.relative_to(ROOT)
        target = out / "frozen" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(file, target)
        manifest["files"].append(
            {
                "path": rel.as_posix(),
                "sha256": digest(target),
                "bytes": target.stat().st_size,
            }
        )
    path = out / "frozen/MANIFEST.json"
    write(path, manifest)
    from omega_cosmology.testbed.workflow import capped, tree_bytes

    folder = out / "smoke"
    folder.mkdir()
    receipt = capped(
        [
            sys.executable,
            str(out / "frozen/scripts/run_r2_integrated_smoke.py"),
            "--worker",
            "--manifest",
            str(path),
            "--out-dir",
            str(folder),
        ],
        folder,
        seconds=plan["caps"]["seconds"],
        memory=plan["caps"]["memory_bytes"],
        output_cap=plan["caps"]["output_bytes"],
        cwd=out / "frozen",
    )
    result = folder / "RESULT.json"
    passed = (
        receipt["exit_code"] == 0 and receipt["cap_reason"] is None and result.exists()
    )
    if passed:
        parsed = json.loads(result.read_text())
        passed = parsed["status"] == "passed" and parsed[
            "source_manifest_sha256"
        ] == digest(path)
    record = {
        "status": "passed" if passed else "failed",
        "receipt": receipt,
        "source_manifest_sha256": digest(path),
        "output_bytes": tree_bytes(out),
        "result_sha256": digest(result) if result.exists() else None,
    }
    write(out / "BATCH_RECEIPT.json", record)
    print(json.dumps(record, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
