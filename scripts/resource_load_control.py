"""One source-fed load family: qualify/freeze physical matches before scoring."""

import argparse
import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile

from restore_research_snapshot import write_archive

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
SOURCE = Path("research/platform/engineering/paired-qualification-2026-10-30-r2")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    Path(path).write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def prepare(out):
    if out.exists() or not out.is_relative_to(ROOT / "runs"):
        raise ValueError("Fresh run inside runs required")
    source = ROOT / SOURCE
    records = {r["path"]: r for r in read(source / "EVIDENCE.json")["files"]}
    for name in ("SNAPSHOT.zip", "retained/R1/RESULT.json"):
        if digest(source / name) != records[name]["sha256"]:
            raise ValueError("Qualified R1 source evidence changed")
    prior = read(source / "retained/R1/RESULT.json")
    with ZipFile(source / "SNAPSHOT.zip") as z:
        original = json.loads(z.read("inputs/R1.json"))
    inputs = {
        "root": original["preparation"],
        "all_roots": original["all_roots"],
        "productive": prior["arms"][0]["interpreted_model"],
        "ablation": prior["arms"][1]["interpreted_model"],
        "prior_rows": {a["original_law"]: a["rows"] for a in prior["arms"]},
        "source_evidence": {
            "path": SOURCE.as_posix(),
            "manifest_sha256": digest(source / "EVIDENCE.json"),
        },
    }
    plan = {
        "schema": "omega.resource-load-control/1",
        "date": "2026-10-30",
        "physical_grid": [1e-5, 0.001, 0.01, 0.1, 1, 2],
        "conductance_bounds": [1e-5, 2],
        "max_fit_evaluations": 24,
        "absolute_tolerance": 1e-10,
        "relative_tolerance": 0.001,
        "payment_epsilon": 1e-8,
        "payment_horizon": 64,
        "horizons": [16, 64, 256, 1024],
        "cadences": [0.125, 0.25, 0.5],
        "source_off_reuses_on_conductance": True,
        "caps": {
            "physical_seconds": 180,
            "history_seconds": 240,
            "memory_bytes": 1024**3,
            "output_bytes": 32 * 1024**2,
        },
        "physical_only_before_freeze": True,
        "claim": "Compare one specified productive mechanism with individually activity/net-work-matched source-fed relaxation controls; no required entropy sign",
    }
    out.mkdir(parents=True)
    frozen = out / "frozen"
    frozen.mkdir()
    write(out / "PLAN.json", plan)
    write(frozen / "INPUTS.json", inputs)
    files = sorted((ROOT / "src/omega_cosmology/testbed").glob("*.py")) + [
        ROOT / "src/omega_cosmology/__init__.py",
        Path(__file__).resolve(),
        ROOT / "scripts/restore_research_snapshot.py",
        ROOT / "tests/test_resource_load.py",
        ROOT / "research/platform/specs/RESOURCE_LOAD_CONTROL_r1.md",
    ]
    for p in files:
        target = frozen / p.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
    write(
        frozen / "MANIFEST.json",
        {
            "schema": "omega.resource-load-snapshot/1",
            "plan_sha256": digest(out / "PLAN.json"),
            "files": [
                {
                    "path": p.relative_to(frozen).as_posix(),
                    "bytes": p.stat().st_size,
                    "sha256": digest(p),
                }
                for p in sorted(frozen.rglob("*"))
                if p.is_file()
            ],
        },
    )
    print(json.dumps({"status": "prepared", "plan_sha256": digest(out / "PLAN.json")}))


def model_for(inputs, kind, source_on, conductance=None):
    from omega_cosmology.testbed.physics import Condition, LocalModel
    from omega_cosmology.testbed.resource_load import attach_resource_load

    model = LocalModel.from_record(
        inputs["productive"] if kind == "productive" else inputs["ablation"]
    )
    if not source_on:
        r = model.record()
        r["id"] += ".source-off"
        r["rules"] = [
            rule for rule in r["rules"] if rule.get("boundary", "native") == "native"
        ]
        model = LocalModel.from_record(r)
    if kind == "load":
        model = attach_resource_load(
            model,
            resource="carrier",
            charged=1,
            spent=0,
            helper_conditions=(Condition("bond", "eq", 1),),
            conductance=conductance,
        )
    return model


def compile_for(inputs, model):
    import numpy as np

    from omega_cosmology.testbed.backends import enumerate_model

    c = enumerate_model(model, [tuple(s) for s in inputs["all_roots"]], max_states=200)
    c.require_complete()
    mu = np.zeros(len(c.states))
    for s, w in inputs["root"]["roots"]:
        mu[c.index[model.canonical(tuple(s))]] += w
    return c, mu


def stationary(c):
    import numpy as np
    from scipy.sparse.csgraph import connected_components

    if connected_components(c.q, directed=True, connection="strong")[0] != 1:
        raise ValueError(
            "This physical stationary calibration requires one communicating class"
        )
    q = c.q.toarray()
    a = q.T.copy()
    a[-1] = 1
    b = np.zeros(len(q))
    b[-1] = 1
    pi = np.linalg.solve(a, b)
    residual = float(max(abs(pi @ q)))
    if pi.min() < -1e-12 or residual > 1e-10:
        raise ArithmeticError("Physical stationary solve failed")
    return pi, residual


def physical_worker(out):
    import numpy as np

    from omega_cosmology.testbed.history import distributions_and_occupation
    from omega_cosmology.testbed.matching import MomentSpec, match_one_physical_moment
    from omega_cosmology.testbed.resource_load import load_rewards
    from omega_cosmology.testbed.thermodynamics import (
        audit_equilibrium,
        balance,
        flow_rewards,
    )

    inputs, plan = read(out / "frozen/INPUTS.json"), read(out / "PLAN.json")
    cache, physical_map = {}, []

    def evaluate(kind, source_on, k=None):
        key = (kind, source_on, k)
        if key in cache:
            return cache[key]
        model = model_for(inputs, kind, source_on, k)
        c, mu = compile_for(inputs, model)
        pi, residual = stationary(c)
        w, h, jumps, _ = flow_rewards(c)
        incoming, returned = np.zeros(len(pi)), np.zeros(len(pi))
        for i, _, e in c.ledger:
            incoming[i] += e.rate * max(e.work, 0)
            returned[i] += e.rate * max(-e.work, 0)
        end, occupation = distributions_and_occupation(c, mu, plan["payment_horizon"])
        finite = balance(c, mu, end, occupation)
        row = {
            "kind": kind,
            "source_on": source_on,
            "conductance": k,
            "model_hash": model.fingerprint(),
            "states": len(c.states),
            "stationary_residual": residual,
            "equilibrium_audit": audit_equilibrium(c),
            "stationary": {
                "event_rate": float(pi @ jumps),
                "net_work_rate": float(pi @ w),
                "gross_accepted_work_rate": float(pi @ incoming),
                "gross_returned_work_rate": float(pi @ returned),
                "heat_rate": float(pi @ h),
            },
            "finite_T64": finite,
            "load": None,
            "qualified_source_fed_load": False,
        }
        if abs(float(pi @ (w - h))) > 1e-9:
            raise ArithmeticError("Stationary first law failed")
        if kind == "load":
            reward, audit = load_rewards(c)
            if any(
                e.work != 0
                or any(
                    s != t
                    for i, (s, t) in enumerate(zip(c.states[a], c.states[b]))
                    if model.coordinates[i].name != "carrier"
                )
                for a, b, e in c.ledger
                if e.rule_id in audit["rule_ids"]
            ):
                raise ArithmeticError(
                    "Load changes bank/apparatus or accepts hidden work"
                )
            rate = {name: float(pi @ value) for name, value in reward.items()}
            cumulative = {
                name: float(occupation @ value) for name, value in reward.items()
            }
            row["load"] = {"audit": audit, "stationary": rate, "finite_T64": cumulative}
            eps = plan["payment_epsilon"]
            row["qualified_source_fed_load"] = bool(
                source_on
                and audit["no_forward_energy_gain"]
                and rate["net_heat"] > eps
                and row["stationary"]["net_work_rate"] > eps
                and cumulative["net_heat"] > eps
            )
            if (
                not source_on
                and max(abs(rate["net_heat"]), abs(row["stationary"]["net_work_rate"]))
                > eps
            ):
                raise ArithmeticError("Source-off load has sustained net payment")
        physical_map.append(row)
        cache[key] = row
        return row

    for source_on in (True, False):
        for kind in ("productive", "ablation"):
            evaluate(kind, source_on)
        for k in plan["physical_grid"]:
            evaluate("load", source_on, k)
    target = evaluate("productive", True)["stationary"]
    targets = {name: target[name] for name in ("event_rate", "net_work_rate")}
    specs = {
        name: MomentSpec(
            name,
            "events/time" if name == "event_rate" else "energy/time",
            None,
            "stationary_rate",
            plan["absolute_tolerance"],
            plan["relative_tolerance"],
        )
        for name in targets
    }
    selections = []
    for primary in targets:
        fit = match_one_physical_moment(
            lambda params: {
                name: evaluate("load", True, params["conductance"])["stationary"][name]
                for name in targets
            },
            targets,
            {"conductance": tuple(plan["conductance_bounds"])},
            primary=primary,
            moment_specs=specs,
            max_evaluations=plan["max_fit_evaluations"],
        )
        k = fit["best"]["parameters"]["conductance"]
        chosen = evaluate("load", True, k)
        off = evaluate("load", False, k)
        matched = abs(fit["best"]["scaled_residuals"][primary]) <= 1
        selections.append(
            {
                "name": "activity_matched"
                if primary == "event_rate"
                else "net_work_matched",
                "primary": primary,
                "fit": fit,
                "conductance": k,
                "primary_matched": matched,
                "qualified": chosen["qualified_source_fed_load"],
                "history_permitted": bool(
                    matched and chosen["qualified_source_fed_load"]
                ),
                "selected_physical": chosen,
                "source_off_physical": off,
            }
        )
    write(
        out / "physical/CALIBRATION.json",
        {
            "status": "completed_physical_qualification",
            "history_computed": False,
            "target": evaluate("productive", True),
            "ablation": evaluate("ablation", True),
            "selections": selections,
            "physical_map": physical_map,
            "matched_quantity_scope": "individual stationary event-rate and net-work-rate matches; not finite/gross/path matches",
            "entropy_was_not_a_selection_quantity": True,
        },
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "physical_points": len(physical_map),
                "qualified_matches": [
                    s["name"] for s in selections if s["history_permitted"]
                ],
            }
        )
    )


def history_worker(out, calibration_sha):
    from itertools import pairwise

    import numpy as np

    from omega_cosmology.testbed.history import (
        distributions_and_occupation,
        history_profile,
        sampled_kernel,
        sampled_support,
    )
    from omega_cosmology.testbed.profile_analysis import geometric_total, kernel_profile
    from omega_cosmology.testbed.resource_load import load_rewards
    from omega_cosmology.testbed.semantics import (
        ComparisonSpec,
        LawSpec,
        ObservationSpec,
        PresentSpec,
        QuantitySpec,
        validate_comparison,
    )
    from omega_cosmology.testbed.thermodynamics import balance

    if digest(out / "physical/CALIBRATION.json") != calibration_sha:
        raise ValueError("Physical calibration changed before scoring")
    calibration = read(out / "physical/CALIBRATION.json")
    selected = [s for s in calibration["selections"] if s["history_permitted"]]
    if not selected:
        raise ValueError(
            "No physically qualified matched comparison; scoring forbidden"
        )
    inputs, plan = read(out / "frozen/INPUTS.json"), read(out / "PLAN.json")
    configurations = [
        ("productive", "productive", None),
        ("ablation", "ablation", None),
    ] + [(s["name"], "load", s["conductance"]) for s in selected]
    rows, comparisons, contracts, profile_maps = [], [], [], []
    for source_on in (True, False):
        compiled, native_profiles, coordinates = {}, {}, {}
        for name, kind, k in configurations:
            model = model_for(inputs, kind, source_on, k)
            c, mu = compile_for(inputs, model)
            compiled[name] = (c, mu)
            for cadence in plan["cadences"]:
                p = sampled_kernel(c, cadence)
                d = kernel_profile(p, structural_support=sampled_support(c))
                full = history_profile(p, mu, round(max(plan["horizons"]) / cadence))
                native_profiles[name, cadence] = full
                coordinates[name, cadence] = d.coordinates(mu, cadence=cadence)
                grid = sorted(
                    set(
                        [0, len(full) - 1]
                        + [round(T / cadence) for T in plan["horizons"]]
                        + [int(v) for v in np.geomspace(1, len(full) - 1, 48)]
                    )
                )
                profile_maps.append(
                    {
                        "arm": name,
                        "source_on": source_on,
                        "cadence": cadence,
                        "coordinates": coordinates[name, cadence],
                        "profile": [
                            {
                                "steps": n,
                                "physical_duration": n * cadence,
                                "ell_bits": float(full[n]),
                            }
                            for n in grid
                        ],
                        "geometric_endings": [
                            {
                                "mean_physical_duration": mean,
                                **geometric_total(d, mu, mean / cadence),
                            }
                            for mean in (10, 100, 1000, 10000)
                        ],
                    }
                )
                for T in plan["horizons"]:
                    endpoint, occupation = distributions_and_occupation(c, mu, T)
                    physical = balance(c, mu, endpoint, occupation)
                    incoming, returned = np.zeros(len(mu)), np.zeros(len(mu))
                    for i, _, event in c.ledger:
                        incoming[i] += event.rate * max(event.work, 0)
                        returned[i] += event.rate * max(-event.work, 0)
                    physical.update(
                        {
                            "gross_accepted_work": float(occupation @ incoming),
                            "gross_returned_work": float(occupation @ returned),
                        }
                    )
                    observables = {}
                    for field, value in (
                        (
                            "bank_energy",
                            np.array(
                                [0.5 * s[model.indices["bank"]] for s in c.states]
                            ),
                        ),
                        (
                            "working_units",
                            np.array(
                                [
                                    s[model.indices["a.active"]]
                                    + s[model.indices["b.active"]]
                                    for s in c.states
                                ]
                            ),
                        ),
                        (
                            "assembled_motif",
                            np.array([s[model.indices["bond"]] for s in c.states]),
                        ),
                    ):
                        observables[field] = {
                            "endpoint": float(endpoint @ value),
                            "integrated": float(occupation @ value),
                        }
                    load = None
                    if kind == "load":
                        reward, _ = load_rewards(c)
                        load = {
                            field: float(occupation @ value)
                            for field, value in reward.items()
                        }
                    value = float(full[round(T / cadence)])
                    if (
                        source_on
                        and cadence == 0.25
                        and T in (16, 64)
                        and kind != "load"
                    ):
                        prior = inputs["prior_rows"][
                            "driven__intact"
                            if kind == "productive"
                            else "driven__ablated"
                        ]
                        expected = next(
                            r["ell_bits"] for r in prior if r["horizon"] == T
                        )
                        if abs(value - expected) > 1e-7:
                            raise ArithmeticError(
                                "Original productive/ablation anchor changed"
                            )
                    rows.append(
                        {
                            "arm": name,
                            "source_on": source_on,
                            "conductance": k,
                            "cadence": cadence,
                            "horizon": T,
                            "ell_bits": value,
                            "physical": physical,
                            "load": load,
                            "observables": observables,
                        }
                    )
        for name, _, _ in configurations[1:]:
            a, _ = compiled["productive"]
            b, _ = compiled[name]
            present = PresentSpec(
                "R1.built",
                tuple((tuple(s), w) for s, w in inputs["root"]["roots"]),
                conditioning=inputs["root"]["conditioning"],
                sufficiency="Original complete fixed-slot present and explicit retained-unit interpretation",
            )

            def arm(c, comparison, _present=present):
                boundary = {
                    "beta": c.model.beta,
                    "external_rules": [
                        r
                        for r in c.model.record()["rules"]
                        if r["boundary"] != "native"
                    ],
                    "unresolved": "source and bath histories",
                }
                return {
                    "compiled": c,
                    "present": _present,
                    "comparison": comparison,
                    "law": LawSpec(c.model.id, c.model_hash, boundary),
                    "observation": ObservationSpec(
                        "whole", tuple(c.name for c in c.model.coordinates)
                    ),
                    "quantity": QuantitySpec(
                        "full.history",
                        "Complete native sampled history",
                        "bits",
                        "full_present",
                    ),
                }

            for cadence in plan["cadences"]:
                delta = (
                    native_profiles["productive", cadence]
                    - native_profiles[name, cadence]
                )
                nonzero = np.flatnonzero(abs(delta) > 1e-7)
                crossings = [
                    [int(i), int(j)]
                    for i, j in pairwise(nonzero)
                    if np.sign(delta[i]) != np.sign(delta[j])
                ]
                for T in plan["horizons"]:
                    comparison = ComparisonSpec(
                        "load.contrast",
                        "mechanism",
                        T,
                        cadence,
                        {
                            "present": "same actual root",
                            "retained_units": "same",
                            "source": "same offered prescription",
                            "physical_moment": "stationary individual match only where calibrated",
                        },
                    )
                    certificate = validate_comparison(
                        comparison,
                        arm(a, comparison),
                        arm(b, comparison),
                        require_material=True,
                    )
                    contracts.append(
                        {
                            "control": name,
                            "source_on": source_on,
                            "cadence": cadence,
                            "horizon": T,
                            "certificate": certificate,
                        }
                    )
                    comparisons.append(
                        {
                            "control": name,
                            "source_on": source_on,
                            "cadence": cadence,
                            "horizon": T,
                            "productive_minus_control_bits": float(
                                delta[round(T / cadence)]
                            ),
                            "delta_rate_bits_per_time": coordinates[
                                "productive", cadence
                            ]["rate_bits_per_time"]
                            - coordinates[name, cadence]["rate_bits_per_time"],
                            "delta_bias_offset_bits": coordinates[
                                "productive", cadence
                            ]["bias_offset_bits"]
                            - coordinates[name, cadence]["bias_offset_bits"],
                            "observed_crossing_step_intervals": crossings,
                            "crossing_scope": "full evaluated discrete prefix; no unique/all-horizon claim",
                        }
                    )
    write(
        out / "history/RESULT.json",
        {
            "status": "passed",
            "calibration_sha256": calibration_sha,
            "rows": rows,
            "comparisons": comparisons,
            "paired_contracts": contracts,
            "profiles": profile_maps,
            "scope": "One fixed finite load family; source-off diagnostic not refitted; whole modeled field excludes boundary histories; no ethical or physical-faithfulness certificate",
        },
    )
    print(
        json.dumps(
            {"status": "passed", "rows": len(rows), "comparisons": len(comparisons)}
        )
    )


def run(out):
    from omega_cosmology.testbed.workflow import capped

    if (out / "RECEIPT.json").exists():
        raise ValueError("Do not overwrite a completed run")
    plan = read(out / "PLAN.json")
    if digest(out / "PLAN.json") != read(out / "frozen/MANIFEST.json")["plan_sha256"]:
        raise ValueError("Plan changed after freeze")
    receipts = {}
    for mode in ("physical", "history"):
        if mode == "history":
            calibration = read(out / "physical/CALIBRATION.json")
            if not any(s["history_permitted"] for s in calibration["selections"]):
                receipts["history"] = {"status": "not_run_no_qualified_match"}
                break
        folder = out / mode
        folder.mkdir()
        command = [
            sys.executable,
            str(out / "frozen/scripts/resource_load_control.py"),
            mode,
            "--out-dir",
            str(out),
        ]
        if mode == "history":
            command += ["--calibration-sha", digest(out / "physical/CALIBRATION.json")]
        receipt = capped(
            command,
            folder,
            seconds=plan["caps"][mode + "_seconds"],
            memory=plan["caps"]["memory_bytes"],
            output_cap=plan["caps"]["output_bytes"],
            cwd=out / "frozen",
        )
        receipts[mode] = receipt
        print(
            json.dumps(
                {
                    "mode": mode,
                    "exit_code": receipt["exit_code"],
                    "cap_reason": receipt["cap_reason"],
                    "seconds": receipt["wall_seconds"],
                }
            ),
            flush=True,
        )
        if receipt["exit_code"] != 0 or receipt["cap_reason"]:
            break
    status = (
        "passed"
        if receipts.get("physical", {}).get("exit_code") == 0
        and (
            receipts.get("history", {}).get("exit_code") == 0
            or receipts.get("history", {}).get("status") == "not_run_no_qualified_match"
        )
        else "incomplete"
    )
    write(
        out / "RECEIPT.json",
        {
            "status": status,
            "plan_sha256": digest(out / "PLAN.json"),
            "manifest_sha256": digest(out / "frozen/MANIFEST.json"),
            "phases": receipts,
        },
    )
    return status


def retain(out, evidence):
    if evidence.exists() or not evidence.is_relative_to(
        ROOT / "research/platform/engineering"
    ):
        raise ValueError("Fresh retained engineering folder required")
    evidence.mkdir(parents=True)
    for name in ("PLAN.json", "RECEIPT.json"):
        shutil.copyfile(out / name, evidence / name)
    m = read(out / "frozen/MANIFEST.json")
    data = {r["path"]: (out / "frozen" / r["path"]).read_bytes() for r in m["files"]}
    if any(sha256(data[r["path"]]).hexdigest() != r["sha256"] for r in m["files"]):
        raise ValueError("Source snapshot changed")
    write_archive(
        evidence / "SNAPSHOT.zip",
        data | {"MANIFEST.json": (out / "frozen/MANIFEST.json").read_bytes()},
    )
    for mode in ("physical", "history"):
        if (out / mode).is_dir():
            for path in (out / mode).iterdir():
                if path.is_file():
                    target = evidence / mode / path.name
                    target.parent.mkdir(exist_ok=True)
                    if path.suffix == ".log":
                        target.write_text(
                            path.read_text(encoding="utf-8")
                            .replace(str(ROOT), "<repo>")
                            .replace(ROOT.as_posix(), "<repo>"),
                            encoding="utf-8",
                        )
                    else:
                        shutil.copyfile(path, target)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode", choices=("prepare", "run", "physical", "history", "retain"))
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--evidence-dir", type=Path)
    p.add_argument("--calibration-sha")
    a = p.parse_args()
    out = a.out_dir.resolve()
    if a.mode in ("physical", "history"):
        if sys.stdin.readline().strip() != "GO":
            raise SystemExit("Capped worker gate required")
        m = read(out / "frozen/MANIFEST.json")
        if digest(out / "PLAN.json") != m["plan_sha256"] or any(
            digest(out / "frozen" / r["path"]) != r["sha256"] for r in m["files"]
        ):
            raise ValueError("Frozen source or plan changed")
        sys.path.insert(0, str(out / "frozen/src"))
        physical_worker(out) if a.mode == "physical" else history_worker(
            out, a.calibration_sha
        )
    else:
        if not out.is_relative_to(ROOT / "runs"):
            p.error("Run output must remain under runs")
        if a.mode == "prepare":
            prepare(out)
        elif a.mode == "run":
            return run(out) != "passed"
        else:
            retain(out, a.evidence_dir.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
