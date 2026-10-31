"""J's bounded physical-only qualification. There is no history-scoring stage."""

import argparse
import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
SOURCE = Path("research/platform/engineering/resource-load-control-2026-10-30")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    path = Path(path)
    temp = path.with_suffix(".tmp")
    temp.write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    temp.replace(path)


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def control_model(inputs, source_on, k_l, k_u):
    from resource_load_control import model_for

    from omega_cosmology.testbed.physics import Condition
    from omega_cosmology.testbed.resource_load import attach_resource_load

    model = model_for(inputs, "ablation", source_on)
    for charged, k, name in [(1, k_l, "load_locked"), (2, k_u, "load_usable")]:
        if not 0 <= k <= 2:
            raise ValueError("Load conductance outside frozen physical box")
        if k:
            model = attach_resource_load(
                model,
                resource="carrier",
                charged=charged,
                spent=0,
                helper_conditions=(Condition("bond", "eq", 1),),
                conductance=k,
                rule_id=name,
            )
    return model


def prepare(out):
    if out.exists() or not out.is_relative_to(ROOT / "runs"):
        raise ValueError("Fresh ignored run directory required")
    source = ROOT / SOURCE
    manifest = {r["path"]: r for r in read(source / "EVIDENCE.json")["files"]}
    for name in ["SNAPSHOT.zip", "physical/CALIBRATION.json"]:
        if digest(source / name) != manifest[name]["sha256"]:
            raise ValueError("Original source changed")
    with ZipFile(source / "SNAPSHOT.zip") as z:
        inputs = json.loads(z.read("INPUTS.json"))
    for model in [inputs["productive"], inputs["ablation"]]:
        if (
            next(r for r in model["rules"] if r["id"] == "source")["conductance"]
            != 0.08
        ):
            raise ValueError("Only the source .08 anchor is authorized")
    # Retain only inputs needed by physical evaluation, not historical scores.
    inputs = {k: inputs[k] for k in ["root", "all_roots", "productive", "ablation"]}
    inputs["reference_target"] = read(source / "physical/CALIBRATION.json")["target"][
        "stationary"
    ]
    inputs["source_evidence"] = {
        "path": SOURCE.as_posix(),
        "manifest_sha256": digest(source / "EVIDENCE.json"),
    }
    plan = {
        "schema": "omega.joint-resource-load-physical/1",
        "date": "2026-10-31",
        "grid": [0, 1e-5, 0.001, 0.01, 0.1, 2],
        "conductance_box": [0, 2],
        "source_conductance": 0.08,
        "fit_extra_evaluations": 48,
        "additional_off_evaluations": 8,
        "max_physical_evaluations": 132,
        "physical_horizon": 64,
        "absolute_tolerance": 1e-10,
        "relative_tolerance": 0.001,
        "payment_epsilon": 1e-8,
        "stationary_tolerance": 1e-10,
        "energy_tolerance": 1e-8,
        "parameter_transform_scale": 1e-4,
        "fit_objective": "sum squared allowance-scaled physical moment residuals; one start at best grid point",
        "per_route_stationary_consumption_required": True,
        "caps": {
            "seconds": 300,
            "memory_bytes": 1024**3,
            "output_bytes": 64 * 1024**2,
            "max_states": 200,
        },
        "history_stage": "absent_and_not_authorized",
        "stop": "physical report for review",
    }
    out.mkdir(parents=True)
    frozen = out / "frozen"
    frozen.mkdir()
    write(out / "PLAN.json", plan)
    write(frozen / "INPUTS.json", inputs)
    files = sorted((ROOT / "src/omega_cosmology/testbed").glob("*.py")) + [
        ROOT / "src/omega_cosmology/__init__.py",
        Path(__file__).resolve(),
        ROOT / "scripts/resource_load_control.py",
        ROOT / "scripts/restore_research_snapshot.py",
        ROOT / "tests/test_resource_load.py",
        ROOT / "research/platform/specs/JOINT_RESOURCE_LOAD_PILOT_r1.md",
    ]
    for path in files:
        target = frozen / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    write(
        frozen / "MANIFEST.json",
        {
            "schema": "omega.joint-load-snapshot/1",
            "plan_sha256": digest(out / "PLAN.json"),
            "files": [
                {
                    "path": p.relative_to(frozen).as_posix(),
                    "sha256": digest(p),
                    "bytes": p.stat().st_size,
                }
                for p in sorted(frozen.rglob("*"))
                if p.is_file()
            ],
        },
    )
    print(json.dumps({"status": "prepared", "plan_sha256": digest(out / "PLAN.json")}))


def worker(out, *, control_builder=control_model):
    import numpy as np
    from resource_load_control import compile_for, model_for, stationary
    from scipy.optimize import least_squares
    from scipy.spatial import Delaunay, QhullError

    from omega_cosmology.testbed.history import distributions_and_occupation
    from omega_cosmology.testbed.resource_load import LOAD_ROLE, load_rewards
    from omega_cosmology.testbed.thermodynamics import (
        audit_equilibrium,
        balance,
        flow_rewards,
    )

    inputs, plan = read(out / "frozen/INPUTS.json"), read(out / "PLAN.json")
    parameter_names = plan.get("parameter_names", ["k_L", "k_U"])
    heat_releases = plan.get(
        "load_energy_releases", {"load_locked": 3, "load_usable": 2}
    )
    rows, cache, objects = [], {}, {}
    folder = out / "physical"

    def evaluate(kind, source_on, k_l=0.0, k_u=0.0):
        key = (kind, source_on, float(k_l), float(k_u))
        if key in cache:
            return cache[key]
        if len(rows) >= plan["max_physical_evaluations"]:
            raise RuntimeError("Total physical evaluation cap reached")
        model = (
            control_builder(inputs, source_on, k_l, k_u)
            if kind == "control"
            else model_for(inputs, kind, source_on)
        )
        base = model_for(inputs, "ablation", source_on)
        if kind == "control":
            for name, value in base.record().items():
                if name not in ["id", "rules"] and model.record()[name] != value:
                    raise ArithmeticError("Control changed common physical grammar")
            if list(model.rules[: len(base.rules)]) != list(base.rules):
                raise ArithmeticError("Control changed a common native rule")
        c, mu = compile_for(inputs, model)
        if len(c.states) > plan["caps"]["max_states"]:
            raise RuntimeError("State cap exceeded")
        pi, residual = stationary(c)
        work, heat, jumps, _ = flow_rewards(c)
        q = c.q.toarray()
        if max(abs(jumps + q.diagonal())) > 1e-10:
            raise ArithmeticError("Marked jump total differs from physical state exits")
        initial, occupied = distributions_and_occupation(
            c, mu, plan["physical_horizon"]
        )
        finite = balance(c, mu, initial, occupied)
        equilibrium = audit_equilibrium(c)
        if equilibrium["status"] != "passed" or residual > plan["stationary_tolerance"]:
            raise ArithmeticError("Stationary or source-off equilibrium audit failed")
        if (
            max(abs(finite["energy_residual"]), abs(float(pi @ (work - heat))))
            > plan["energy_tolerance"]
        ):
            raise ArithmeticError("First law failed")
        gross, returned = np.zeros(len(pi)), np.zeros(len(pi))
        for i, _, e in c.ledger:
            gross[i] += e.rate * max(e.work, 0)
            returned[i] += e.rate * max(-e.work, 0)
        row = {
            "index": len(rows),
            "kind": kind,
            "source_on": source_on,
            "parameters": dict(zip(parameter_names, [float(k_l), float(k_u)])),
            "model_hash": model.fingerprint(),
            "state_order_hash": c.state_order_hash,
            "event_ledger_hash": c.ledger_hash,
            "states": len(c.states),
            "stationary_residual": residual,
            "stationary_system_condition": float(
                np.linalg.cond(np.vstack([q.T[:-1], np.ones(len(pi))]))
            ),
            "equilibrium_audit": equilibrium,
            "stationary": {
                "event_rate": float(pi @ jumps),
                "net_work_rate": float(pi @ work),
                "gross_accepted_work_rate": float(pi @ gross),
                "gross_returned_work_rate": float(pi @ returned),
                "heat_rate": float(pi @ heat),
                "first_law_residual": float(pi @ (work - heat)),
            },
            "finite_T64": finite,
            "loads": {},
            "load_total": None,
            "qualified_source_fed_load": False,
        }
        ids = {r.id for r in model.rules if LOAD_ROLE in r.roles}
        if ids:
            for a, b, e in c.ledger:
                if e.rule_id in ids:
                    if e.work or any(
                        s != t
                        for i, (s, t) in enumerate(zip(c.states[a], c.states[b]))
                        if model.coordinates[i].name != "carrier"
                    ):
                        raise ArithmeticError(
                            "Load contains hidden work/bank/other change"
                        )
                    expected = heat_releases[e.rule_id]
                    if (
                        e.heat != expected * e.direction
                        or e.delta_energy != -expected * e.direction
                    ):
                        raise ArithmeticError("Load energy destination mismatch")
            for label, selected in [(name, (name,)) for name in sorted(ids)] + [
                ("total", tuple(sorted(ids)))
            ]:
                reward, audit = load_rewards(c, rule_ids=selected)
                item = {
                    "audit": audit,
                    "stationary": {n: float(pi @ v) for n, v in reward.items()},
                    "finite_T64": {n: float(occupied @ v) for n, v in reward.items()},
                }
                if label == "total":
                    row["load_total"] = item
                else:
                    row["loads"][label] = item
            eps = plan["payment_epsilon"]
            total = row["load_total"]
            row["qualified_source_fed_load"] = bool(
                source_on
                and row["stationary"]["net_work_rate"] > eps
                and total["stationary"]["net_heat"] > eps
                and total["finite_T64"]["net_heat"] > eps
                and all(
                    v["stationary"]["net_heat"] > eps for v in row["loads"].values()
                )
            )
            if (
                not source_on
                and max(
                    [abs(v["stationary"]["net_heat"]) for v in row["loads"].values()]
                    + [abs(float(pi @ work))]
                )
                > eps
            ):
                raise ArithmeticError("Source-off sustained net flow")
        if not source_on and abs(float(pi @ work)) > plan["payment_epsilon"]:
            raise ArithmeticError("Source-off work present")
        ix = model.indices
        row["function"] = {
            "stationary_bond_probability": float(
                sum(pi[i] * s[ix["bond"]] for i, s in enumerate(c.states))
            ),
            "stationary_bank_energy": float(
                sum(pi[i] * s[ix["bank"]] * 0.5 for i, s in enumerate(c.states))
            ),
            "stationary_carrier_probabilities": [
                float(
                    sum(pi[i] for i, s in enumerate(c.states) if s[ix["carrier"]] == j)
                )
                for j in model.coordinates[ix["carrier"]].domain
            ],
        }
        row["function"]["carrier_domain"] = list(
            model.coordinates[ix["carrier"]].domain
        )
        if "intermediate_code" in plan:
            intermediate = plan["intermediate_code"]
            indicator = np.array(
                [s[ix["carrier"]] == intermediate for s in c.states], dtype=float
            )
            exit_reward = np.zeros(len(pi))
            for a, b, event in c.ledger:
                if (
                    c.states[a][ix["carrier"]] == intermediate
                    and c.states[b][ix["carrier"]] != intermediate
                ):
                    exit_reward[a] += event.rate
            occupied_probability = float(pi @ indicator)
            flux = float(pi @ exit_reward)
            row["function"]["intermediate"] = {
                "stationary_occupancy": occupied_probability,
                "stationary_exit_flux": flux,
                "stationary_mean_episode_duration": occupied_probability / flux
                if flux > 0
                else None,
                "finite_T64_occupancy_time": float(occupied @ indicator),
                "finite_T64_exit_count": float(occupied @ exit_reward),
                "scope": "Episodes end on carrier changes, not unrelated apparatus events",
            }
        rows.append(row)
        cache[key] = row
        objects[row["index"]] = (c, mu, pi, work, jumps)
        write(
            folder / "PHYSICAL_MAP.json",
            {"complete": False, "history_computed": False, "rows": rows},
        )
        if len(rows) % 20 == 0:
            print(json.dumps({"physical_evaluations": len(rows)}), flush=True)
        return row

    for on in [True, False]:
        for kind in ["productive", "ablation"]:
            evaluate(kind, on)
        for k_l in plan["grid"]:
            for k_u in plan["grid"]:
                evaluate("control", on, k_l, k_u)
    target = evaluate("productive", True)
    names = ["event_rate", "net_work_rate"]
    targets = np.array([target["stationary"][n] for n in names])
    if (
        "reference_target" in inputs
        and max(abs(targets - [inputs["reference_target"][n] for n in names])) > 1e-10
    ):
        raise ArithmeticError("Productive physical anchor changed from run A")
    allowances = plan["absolute_tolerance"] + plan["relative_tolerance"] * abs(targets)

    def residuals(row):
        return np.array([row["stationary"][n] for n in names]) - targets

    def score(row):
        return float(sum((residuals(row) / allowances) ** 2))

    grid = [r for r in rows if r["kind"] == "control" and r["source_on"]]
    start = min(grid, key=score)
    moment_image = (
        np.array([[r["stationary"][n] for n in names] for r in grid]) / targets
    )
    try:
        hull = bool(Delaunay(moment_image).find_simplex(np.ones(2)) >= 0)
    except QhullError:
        hull = None
    extra_start = len(rows)

    class FitBudget(Exception):
        pass

    scale = plan["parameter_transform_scale"]

    def objective(x):
        k_l, k_u = [float(np.clip(scale * np.expm1(v), 0, 2)) for v in x]
        if ("control", True, k_l, k_u) not in cache and len(rows) - extra_start >= plan[
            "fit_extra_evaluations"
        ]:
            raise FitBudget()
        return residuals(evaluate("control", True, k_l, k_u)) / allowances

    starts = [start]
    if plan.get("fit_initializations", 1) == 2:
        start_x = np.log1p(np.array(list(start["parameters"].values())) / scale)
        separated = [
            r
            for r in grid
            if np.linalg.norm(
                (np.log1p(np.array(list(r["parameters"].values())) / scale) - start_x)
                / np.log1p(2 / scale)
            )
            >= 0.5
        ]
        if separated:
            starts.append(min(separated, key=score))
    solver = {"termination": "completed", "starts": []}
    for seed in starts:
        seed_begin = len(rows)

        def limited_objective(x, _seed_begin=seed_begin):
            if len(rows) - _seed_begin >= plan.get(
                "per_start_evaluations", plan["fit_extra_evaluations"]
            ):
                raise FitBudget()
            return objective(x)

        try:
            result = least_squares(
                limited_objective,
                np.log1p(np.array(list(seed["parameters"].values())) / scale),
                bounds=(np.zeros(2), np.full(2, np.log1p(2 / scale))),
                max_nfev=48,
                xtol=1e-10,
                ftol=1e-10,
                gtol=1e-10,
            )
            solver["starts"].append(
                {
                    "seed_index": seed["index"],
                    "success": bool(result.success),
                    "message": result.message,
                    "extra_evaluations": len(rows) - seed_begin,
                }
            )
        except FitBudget:
            solver["starts"].append(
                {
                    "seed_index": seed["index"],
                    "termination": "literal_evaluation_cap",
                    "extra_evaluations": len(rows) - seed_begin,
                }
            )
            solver["termination"] = "one_or_more_literal_evaluation_caps"
        if len(rows) - extra_start >= plan["fit_extra_evaluations"]:
            break
    candidates = [r for r in rows if r["kind"] == "control" and r["source_on"]]

    def matched(row):
        return bool(max(abs(residuals(row) / allowances)) <= 1)

    best = min(
        candidates,
        key=lambda r: (
            not (matched(r) and r["qualified_source_fed_load"]),
            not matched(r),
            score(r),
        ),
    )
    off = evaluate("control", False, *best["parameters"].values())
    # Generator derivatives from the fixed physical grid; no extra models.
    c, _mu, pi, work, jumps = objects[best["index"]]

    def aligned_q(row):
        other = objects[row["index"]][0]
        if set(other.states) != set(c.states):
            raise ArithmeticError("Sensitivity models have different state alphabets")
        order = [other.index[s] for s in c.states]
        return other.q.toarray()[np.ix_(order, order)]

    base_q = aligned_q(evaluate("control", True, 0, 0))
    dqs = [
        (aligned_q(evaluate("control", True, 2, 0)) - base_q) / 2,
        (aligned_q(evaluate("control", True, 0, 2)) - base_q) / 2,
    ]
    q = c.q.toarray()
    affine_residual = float(
        np.max(
            abs(
                q
                - base_q
                - best["parameters"][parameter_names[0]] * dqs[0]
                - best["parameters"][parameter_names[1]] * dqs[1]
            )
        )
    )
    if affine_residual > 1e-10:
        raise ArithmeticError(
            "Aligned conductance derivatives fail affine generator identity"
        )
    system = q.T.copy()
    system[-1] = 1
    columns = []
    for dq in dqs:
        rhs = -(pi @ dq)
        rhs[-1] = 0
        dpi = np.linalg.solve(system, rhs)
        columns.append([float(dpi @ jumps + pi @ -dq.diagonal()), float(dpi @ work)])
    jac = np.array(columns).T
    dimensionless = (
        jac
        * (np.array(list(best["parameters"].values())) + scale)[None, :]
        / targets[:, None]
    )
    singular = np.linalg.svd(dimensionless, compute_uv=False)
    sensitivity = {
        "moment_parameter_derivatives": jac.tolist(),
        "aligned_affine_generator_residual": affine_residual,
        "dimensionless_log_parameter_derivatives": dimensionless.tolist(),
        "singular_values": singular.tolist(),
        "condition_number": float(singular[0] / singular[-1])
        if singular[-1] > 0
        else None,
        "scope": "Local stationary derivative, not a global feasibility test",
    }
    status = (
        "qualified_joint_match"
        if matched(best) and best["qualified_source_fed_load"]
        else (
            "joint_match_physical_qualification_failed"
            if matched(best)
            else "no_joint_match_in_bounded_search"
        )
    )
    write(
        folder / "CALIBRATION.json",
        {
            "status": status,
            "history_computed": False,
            "history_permission": bool(
                status == "qualified_joint_match"
                and plan.get("conditional_history_authorized", False)
            ),
            "target": target,
            "best": best,
            "source_off_at_best": off,
            "absolute_residuals": dict(zip(names, residuals(best).tolist())),
            "scaled_residuals": dict(
                zip(names, (residuals(best) / allowances).tolist())
            ),
            "allowances": dict(zip(names, allowances.tolist())),
            "physical_evaluations": len(rows),
            "extra_fit_evaluations": len(candidates) - len(grid),
            "solver": solver,
            "target_inside_sampled_moment_convex_hull": hull,
            "hull_scope": "Convex hull of samples is not the physical attainable image or a global certificate",
            "sensitivity": sensitivity,
            "all_physical_rows": rows,
            "scope": "Stationary two-moment physical qualification only; finite/path moments unmatched; no history score",
        },
    )
    write(
        folder / "PHYSICAL_MAP.json",
        {"complete": True, "history_computed": False, "rows": rows},
    )
    print(
        json.dumps(
            {
                "status": status,
                "physical_evaluations": len(rows),
                "history_computed": False,
            }
        ),
        flush=True,
    )


def run(out):
    from omega_cosmology.testbed.workflow import capped

    if (out / "RECEIPT.json").exists():
        raise ValueError("Run already completed")
    plan = read(out / "PLAN.json")
    if digest(out / "PLAN.json") != read(out / "frozen/MANIFEST.json")["plan_sha256"]:
        raise ValueError("Frozen plan changed")
    folder = out / "physical"
    folder.mkdir()
    receipt = capped(
        [
            sys.executable,
            str(out / "frozen/scripts/joint_resource_load_pilot.py"),
            "worker",
            "--out-dir",
            str(out),
        ],
        folder,
        seconds=plan["caps"]["seconds"],
        memory=plan["caps"]["memory_bytes"],
        output_cap=plan["caps"]["output_bytes"],
        cwd=out / "frozen",
    )
    write(
        out / "RECEIPT.json",
        {
            "status": "completed_physical_pilot"
            if receipt["exit_code"] == 0 and not receipt["cap_reason"]
            else "incomplete",
            "plan_sha256": digest(out / "PLAN.json"),
            "worker": receipt,
            "history_stage": "not_run_not_authorized",
        },
    )
    print(
        json.dumps(
            {
                "exit_code": receipt["exit_code"],
                "cap_reason": receipt["cap_reason"],
                "wall_seconds": receipt["wall_seconds"],
            }
        )
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["prepare", "run", "worker"])
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    if args.mode == "worker":
        if sys.stdin.readline().strip() != "GO":
            raise ValueError("Capped worker gate required")
        manifest = read(out / "frozen/MANIFEST.json")
        if digest(out / "PLAN.json") != manifest["plan_sha256"] or any(
            digest(out / "frozen" / r["path"]) != r["sha256"] for r in manifest["files"]
        ):
            raise ValueError("Frozen source or plan changed")
        worker(out)
    else:
        if not out.is_relative_to(ROOT / "runs"):
            raise ValueError("Output must remain in runs")
        prepare(out) if args.mode == "prepare" else run(out)


if __name__ == "__main__":
    main()
