"""Shared physical intermediate; qualify first, then hash-gated histories."""

import argparse
import json
import shutil
import sys
from hashlib import sha256
from itertools import pairwise
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
SOURCE = Path("research/platform/engineering/joint-resource-load-2026-10-31")


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def write(p, v):
    Path(p).write_text(
        json.dumps(v, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def digest(p):
    return sha256(Path(p).read_bytes()).hexdigest()


def make_control(inputs, source_on, k_entry, k_exit):
    from resource_load_control import model_for

    from omega_cosmology.testbed.physics import Condition
    from omega_cosmology.testbed.resource_load import attach_resource_load

    m = model_for(inputs, "ablation", source_on)
    for a, b, k, n in [(1, 3, k_entry, "load_entry"), (3, 0, k_exit, "load_exit")]:
        if not 0 <= k <= 2:
            raise ValueError("Outside physical box")
        if k:
            m = attach_resource_load(
                m,
                resource="carrier",
                charged=a,
                spent=b,
                helper_conditions=(Condition("bond", "eq", 1),),
                conductance=k,
                rule_id=n,
            )
    return m


def prepare(out):
    from omega_cosmology.testbed.physics import LocalModel
    from omega_cosmology.testbed.resource_conformation import add_resource_conformation

    if out.exists() or not out.is_relative_to(ROOT / "runs"):
        raise ValueError("Fresh ignored run required")
    src = ROOT / SOURCE
    entries = {r["path"]: r for r in read(src / "EVIDENCE.json")["files"]}
    if digest(src / "SNAPSHOT.zip") != entries["SNAPSHOT.zip"]["sha256"]:
        raise ValueError("Original source changed")
    with ZipFile(src / "SNAPSHOT.zip") as z:
        old = json.loads(z.read("INPUTS.json"))
    inputs = {k: old[k] for k in ["root", "all_roots"]}
    for arm in ["productive", "ablation"]:
        m = LocalModel.from_record(old[arm])
        expanded = add_resource_conformation(
            m,
            resource="carrier",
            value=3,
            energy="1.5",
            links=(1, 0),
            conductance=0.002,
        )
        for s, _ in inputs["root"]["roots"]:
            if (
                m.energy(tuple(s)) != expanded.energy(tuple(s))
                or float(expanded.energy(tuple(s))) != 4.5
            ):
                raise ValueError("Expanded root changed endowment")
        inputs[arm] = expanded.record()
    inputs["source_evidence"] = {
        "path": SOURCE.as_posix(),
        "manifest_sha256": digest(src / "EVIDENCE.json"),
    }
    plan = {
        "schema": "omega.J2-discharge/1",
        "date": "2026-10-31",
        "grid": [0, 1e-5, 0.001, 0.01, 0.1, 2],
        "parameter_names": ["k_entry", "k_exit"],
        "intermediate_code": 3,
        "load_energy_releases": {"load_entry": 1.5, "load_exit": 1.5},
        "source_conductance": 0.08,
        "fit_initializations": 2,
        "per_start_evaluations": 24,
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
        "caps": {
            "seconds": 300,
            "memory_bytes": 1024**3,
            "output_bytes": 64 * 1024**2,
            "max_states": 200,
        },
        "history_caps": {
            "seconds": 600,
            "memory_bytes": 1024**3,
            "output_bytes": 64 * 1024**2,
        },
        "cadences": [0.125, 0.25, 0.5],
        "horizons": [16, 64, 256, 1024],
        "prefix_steps": 65536,
        "geometric_mean_physical_durations": [10, 100, 1000, 10000],
        "sign_deadband_bits": 1e-7,
        "history_gate": "qualified joint match, unchanged physical calibration hash and independent physical residual check",
        "conditional_history_authorized": True,
        "scope": "One source anchor/new common grammar; no required winner; retain failures then publish",
    }
    out.mkdir(parents=True)
    frozen = out / "frozen"
    frozen.mkdir()
    write(out / "PLAN.json", plan)
    write(frozen / "INPUTS.json", inputs)
    files = sorted((ROOT / "src/omega_cosmology/testbed").glob("*.py")) + [
        ROOT / "src/omega_cosmology/__init__.py",
        Path(__file__).resolve(),
        ROOT / "scripts/joint_resource_load_pilot.py",
        ROOT / "scripts/resource_load_control.py",
        ROOT / "scripts/restore_research_snapshot.py",
        ROOT / "tests/test_resource_conformation.py",
        ROOT / "tests/test_resource_load.py",
        ROOT / "research/platform/specs/J2_SHARED_INTERMEDIATE_r1.md",
    ]
    for p in files:
        q = frozen / p.relative_to(ROOT)
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, q)
    write(
        frozen / "MANIFEST.json",
        {
            "schema": "omega.J2-snapshot/1",
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


def history(out, calibration_sha):
    import numpy as np
    from resource_load_control import compile_for, model_for, stationary

    from omega_cosmology.testbed.history import (
        distributions_and_occupation,
        history_profile,
        sampled_kernel,
        sampled_support,
    )
    from omega_cosmology.testbed.profile_analysis import (
        geometric_total,
        kernel_profile,
        uniform_total,
    )
    from omega_cosmology.testbed.resource_load import load_rewards
    from omega_cosmology.testbed.semantics import (
        ComparisonSpec,
        LawSpec,
        ObservationSpec,
        PresentSpec,
        QuantitySpec,
        validate_comparison,
    )
    from omega_cosmology.testbed.thermodynamics import balance, flow_rewards

    if digest(out / "physical/CALIBRATION.json") != calibration_sha:
        raise ValueError("Physical calibration changed")
    cal = read(out / "physical/CALIBRATION.json")
    plan = read(out / "PLAN.json")
    inputs = read(out / "frozen/INPUTS.json")
    if (
        cal["status"] != "qualified_joint_match"
        or not cal["best"]["qualified_source_fed_load"]
        or not cal["history_permission"]
    ):
        raise ValueError("Unqualified control cannot be scored")
    k = list(cal["best"]["parameters"].values())
    # Verify both physical arms before scoring even the productive reference.
    precompiled = {}
    for name in ["productive", "control"]:
        model = (
            make_control(inputs, True, *k)
            if name == "control"
            else model_for(inputs, name, True)
        )
        c, mu = compile_for(inputs, model)
        expected = cal["best"] if name == "control" else cal["target"]
        if c.model_hash != expected["model_hash"]:
            raise ValueError("Preflight law differs from calibrated law")
        pi, _ = stationary(c)
        w, _h, jumps, _ = flow_rewards(c)
        for quantity, actual in [
            ("event_rate", float(pi @ jumps)),
            ("net_work_rate", float(pi @ w)),
        ]:
            if abs(actual - expected["stationary"][quantity]) > 1e-10:
                raise ValueError("Physical preflight differs from calibration")
            if (
                name == "control"
                and abs(actual - cal["target"]["stationary"][quantity])
                > cal["allowances"][quantity]
            ):
                raise ValueError("Joint physical preflight failed before any scoring")
        if name == "control":
            reward, audit = load_rewards(c)
            endpoint, occupation = distributions_and_occupation(c, mu, 64)
            if (
                float(pi @ w) <= plan["payment_epsilon"]
                or float(occupation @ reward["net_heat"]) <= plan["payment_epsilon"]
            ):
                raise ValueError("Net physical payment preflight failed")
            for rule in audit["rule_ids"]:
                individual, _ = load_rewards(c, rule_ids=(rule,))
                if float(pi @ individual["net_heat"]) <= plan["payment_epsilon"]:
                    raise ValueError("Per-route physical payment preflight failed")
        precompiled[name] = c, mu
    rows = []
    profiles = []
    comparisons = []
    certificates = []
    validation = []
    for source_on in [True, False]:
        compiled = {}
        fulls = {}
        coordinates = {}
        endings = {}
        for name in ["productive", "ablation", "control"]:
            model = (
                make_control(inputs, source_on, *k)
                if name == "control"
                else model_for(inputs, name, source_on)
            )
            c, mu = (
                precompiled[name]
                if source_on and name in precompiled
                else compile_for(inputs, model)
            )
            compiled[name] = (c, mu)
            if source_on:
                physical = (
                    cal["best"]
                    if name == "control"
                    else (cal["target"] if name == "productive" else None)
                )
                if physical and c.model_hash != physical["model_hash"]:
                    raise ValueError("History law differs from qualified law")
                if physical:
                    pi, _ = stationary(c)
                    w, _h, j, _ = flow_rewards(c)
                    for q, value in [
                        ("event_rate", float(pi @ j)),
                        ("net_work_rate", float(pi @ w)),
                    ]:
                        if abs(value - physical["stationary"][q]) > 1e-10:
                            raise ArithmeticError(
                                "Physical moments changed before history"
                            )
                        if (
                            name == "control"
                            and abs(value - cal["target"]["stationary"][q])
                            > cal["allowances"][q]
                        ):
                            raise ValueError(
                                "Joint match failed independent history gate"
                            )
            for dt in plan["cadences"]:
                p = sampled_kernel(c, dt)
                profile = kernel_profile(p, structural_support=sampled_support(c))
                full = history_profile(p, mu, plan["prefix_steps"])
                fulls[name, dt] = full
                coordinates[name, dt] = profile.coordinates(mu, cadence=dt)
                ending = {
                    "geometric": [
                        {
                            "mean_physical_duration": mean,
                            **geometric_total(profile, mu, mean / dt),
                        }
                        for mean in plan["geometric_mean_physical_durations"]
                    ],
                    "uniform": uniform_total(profile, mu, plan["prefix_steps"]),
                }
                endings[name, dt] = ending
                grid = sorted(
                    set(
                        [0, plan["prefix_steps"]]
                        + [round(t / dt) for t in plan["horizons"]]
                        + list(map(int, np.geomspace(1, plan["prefix_steps"], 80)))
                    )
                )
                profiles.append(
                    {
                        "arm": name,
                        "source_on": source_on,
                        "cadence": dt,
                        "coordinates": coordinates[name, dt],
                        "endings": ending,
                        "profile": [
                            {
                                "steps": n,
                                "physical_duration": n * dt,
                                "ell_bits": float(full[n]),
                            }
                            for n in grid
                        ],
                    }
                )
                reward, _ = load_rewards(c) if name == "control" else (None, None)
                for t in plan["horizons"]:
                    n = round(t / dt)
                    endpoint, occupation = distributions_and_occupation(c, mu, t)
                    phys = balance(c, mu, endpoint, occupation)
                    g = np.zeros(len(mu))
                    ret = np.zeros(len(mu))
                    for i, _, e in c.ledger:
                        g[i] += e.rate * max(e.work, 0)
                        ret[i] += e.rate * max(-e.work, 0)
                    phys.update(
                        {
                            "gross_accepted_work": float(occupation @ g),
                            "gross_returned_work": float(occupation @ ret),
                        }
                    )
                    function = {}
                    for label, vec in [
                        (
                            "bond",
                            np.array([s[model.indices["bond"]] for s in c.states]),
                        ),
                        (
                            "bank_energy",
                            np.array(
                                [0.5 * s[model.indices["bank"]] for s in c.states]
                            ),
                        ),
                        (
                            "intermediate",
                            np.array(
                                [s[model.indices["carrier"]] == 3 for s in c.states],
                                dtype=float,
                            ),
                        ),
                    ]:
                        function[label] = {
                            "endpoint": float(endpoint @ vec),
                            "integrated": float(occupation @ vec),
                        }
                    discrepancy = abs(float(full[n]) - profile.at(mu, n)["ell_bits"])
                    if discrepancy > 1e-6:
                        raise ArithmeticError(
                            "Direct history and independent Poisson identity disagree"
                        )
                    validation.append(discrepancy)
                    rows.append(
                        {
                            "arm": name,
                            "source_on": source_on,
                            "cadence": dt,
                            "horizon": t,
                            "steps": n,
                            "ell_bits": float(full[n]),
                            "physical": phys,
                            "function": function,
                            "load": {
                                q: float(occupation @ v) for q, v in reward.items()
                            }
                            if reward is not None
                            else None,
                        }
                    )
                print(
                    json.dumps(
                        {
                            "history_case": name,
                            "source_on": source_on,
                            "cadence": dt,
                            "states": len(c.states),
                        }
                    ),
                    flush=True,
                )
        for control in ["ablation", "control"]:
            left, mu = compiled["productive"]
            right, _ = compiled[control]
            present = PresentSpec(
                "J2.built",
                tuple((tuple(s), w) for s, w in inputs["root"]["roots"]),
                conditioning=inputs["root"]["conditioning"],
                sufficiency="Full expanded physical carrier and fixed-slot state",
            )

            def arm(c, comp, _present=present):
                boundary = {
                    "beta": c.model.beta,
                    "external_rules": [
                        r
                        for r in c.model.record()["rules"]
                        if r["boundary"] != "native"
                    ],
                    "unresolved": "bath/source histories",
                }
                return {
                    "compiled": c,
                    "present": _present,
                    "comparison": comp,
                    "law": LawSpec(c.model.id, c.model_hash, boundary),
                    "observation": ObservationSpec(
                        "whole", tuple(x.name for x in c.model.coordinates)
                    ),
                    "quantity": QuantitySpec(
                        "full.history",
                        "Complete native sampled history",
                        "bits",
                        "full_present",
                    ),
                }

            for dt in plan["cadences"]:
                delta = fulls["productive", dt] - fulls[control, dt]
                nz = np.flatnonzero(abs(delta) > plan["sign_deadband_bits"])
                cross = [
                    [int(a), int(b)]
                    for a, b in pairwise(nz)
                    if np.sign(delta[a]) != np.sign(delta[b])
                ]
                rate = (
                    coordinates["productive", dt]["rate_bits_per_step"]
                    - coordinates[control, dt]["rate_bits_per_step"]
                )
                bias = (
                    coordinates["productive", dt]["bias_offset_bits"]
                    - coordinates[control, dt]["bias_offset_bits"]
                )
                for t in plan["horizons"]:
                    comp = ComparisonSpec(
                        "J2.contrast",
                        "mechanism",
                        t,
                        dt,
                        {
                            "root": "same",
                            "material": "same retained units",
                            "boundaries": "same prescription",
                            "physical_match": "joint stationary only for calibrated source-on control",
                        },
                    )
                    cert = validate_comparison(
                        comp, arm(left, comp), arm(right, comp), require_material=True
                    )
                    certificates.append(
                        {
                            "control": control,
                            "source_on": source_on,
                            "cadence": dt,
                            "horizon": t,
                            "certificate": cert,
                        }
                    )
                    comparisons.append(
                        {
                            "control": control,
                            "source_on": source_on,
                            "cadence": dt,
                            "horizon": t,
                            "delta_bits": float(delta[round(t / dt)]),
                            "delta_rate_bits_per_time": rate / dt,
                            "delta_bias_bits": bias,
                            "line_crossing_step_estimate": -bias / rate
                            if rate
                            else None,
                            "remainder_bound_bits": coordinates["productive", dt][
                                "bias_sup_norm_bits"
                            ]
                            + coordinates[control, dt]["bias_sup_norm_bits"],
                            "crossing_step_brackets": cross,
                            "crossing_physical_brackets": [
                                [a * dt, b * dt] for a, b in cross
                            ],
                            "verdict": "observed_crossings"
                            if cross
                            else "no_crossing_observed_on_evaluated_prefix",
                            "scope": "Float64 prefix/rate diagnostics, not verified all-horizon dominance",
                        }
                    )
    write(
        out / "history/RESULT.json",
        {
            "status": "passed",
            "calibration_sha256": calibration_sha,
            "rows": rows,
            "profiles": profiles,
            "comparisons": comparisons,
            "paired_contracts": certificates,
            "max_independent_identity_difference_bits": max(validation),
            "scope": "New shared-intermediate grammar; no physical-faithfulness or ethics certification",
        },
    )


def run(out):
    from omega_cosmology.testbed.workflow import capped

    if (out / "RECEIPT.json").exists():
        raise ValueError("Completed run cannot be overwritten")
    plan = read(out / "PLAN.json")
    receipts = {}
    if digest(out / "PLAN.json") != read(out / "frozen/MANIFEST.json")["plan_sha256"]:
        raise ValueError("Plan changed")
    for mode in ["physical", "history"]:
        if (
            mode == "history"
            and read(out / "physical/CALIBRATION.json")["status"]
            != "qualified_joint_match"
        ):
            receipts[mode] = {"status": "not_run_no_qualified_joint_match"}
            break
        folder = out / mode
        folder.mkdir()
        caps = plan["caps"] if mode == "physical" else plan["history_caps"]
        command = [
            sys.executable,
            str(out / "frozen/scripts/run_j2_discharge.py"),
            mode,
            "--out-dir",
            str(out),
        ]
        if mode == "history":
            command += ["--calibration-sha", digest(out / "physical/CALIBRATION.json")]
        receipt = capped(
            command,
            folder,
            seconds=caps["seconds"],
            memory=caps["memory_bytes"],
            output_cap=caps["output_bytes"],
            cwd=out / "frozen",
        )
        receipts[mode] = receipt
        print(
            json.dumps(
                {
                    "stage": mode,
                    "exit_code": receipt["exit_code"],
                    "cap_reason": receipt["cap_reason"],
                    "wall_seconds": receipt["wall_seconds"],
                }
            ),
            flush=True,
        )
        if receipt["exit_code"] or receipt["cap_reason"]:
            break
    complete = (
        receipts.get("physical", {}).get("exit_code") == 0
        and not receipts["physical"]["cap_reason"]
        and (
            receipts.get("history", {}).get("exit_code") == 0
            and not receipts["history"]["cap_reason"]
            or receipts.get("history", {}).get("status")
            == "not_run_no_qualified_joint_match"
        )
    )
    write(
        out / "RECEIPT.json",
        {
            "status": "completed" if complete else "incomplete",
            "plan_sha256": digest(out / "PLAN.json"),
            "stages": receipts,
        },
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode", choices=["prepare", "run", "physical", "history"])
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--calibration-sha")
    a = p.parse_args()
    out = a.out_dir.resolve()
    if a.mode in ["physical", "history"]:
        if sys.stdin.readline().strip() != "GO":
            raise ValueError("Capped worker required")
        m = read(out / "frozen/MANIFEST.json")
        if digest(out / "PLAN.json") != m["plan_sha256"] or any(
            digest(out / "frozen" / r["path"]) != r["sha256"] for r in m["files"]
        ):
            raise ValueError("Frozen inputs/source changed")
        if a.mode == "physical":
            from joint_resource_load_pilot import worker

            worker(out, control_builder=make_control)
        else:
            history(out, a.calibration_sha)
    else:
        if not out.is_relative_to(ROOT / "runs"):
            raise ValueError("Ignored output required")
        prepare(out) if a.mode == "prepare" else run(out)


if __name__ == "__main__":
    main()
