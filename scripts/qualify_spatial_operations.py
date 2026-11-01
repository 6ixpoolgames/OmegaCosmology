"""Paid-operation physical qualification; scientific entropy scoring disabled."""

import argparse
import hashlib
import json
import sys
import time
import zipfile
from pathlib import Path

import numpy as np

from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.history import distributions_and_occupation, sampled_kernel
from omega_cosmology.testbed.spatial import spatial_world
from omega_cosmology.testbed.spatial_operations import (
    preparation_model,
    preparation_root,
)
from omega_cosmology.testbed.stream_schedule import stream_schedule
from omega_cosmology.testbed.thermodynamics import audit_equilibrium
from omega_cosmology.testbed.workflow import capped


def write(path, obj):
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def worker(out):
    base = spatial_world()
    models = {k: preparation_model(base, k) for k in ("idle", "aa", "ab")}
    models["off"] = preparation_model(base, source_on=False)
    root = preparation_root(models["idle"])
    compiled = {}
    audits = {}
    for key, model in models.items():
        assert preparation_root(model) == root
        roots = [root] if not compiled else compiled["idle"].states
        c = enumerate_model(model, roots, max_states=8000)
        c.require_complete()
        if compiled and c.states != compiled["idle"].states:
            raise ArithmeticError("Phase alphabet changed")
        audits[key] = {
            "model_hash": c.model_hash,
            "states": len(c.states),
            "seconds": c.seconds,
            "equilibrium": audit_equilibrium(c),
        }
        compiled[key] = c
        write(out / f"MODEL_{key}.json", model.record())
        print(f"Compiled {key}: {len(c.states)} states", flush=True)
    write(out / "AUDITS.json", audits)
    reference = models["idle"].record()
    for model in models.values():
        record = model.record()
        assert all(
            record[k] == reference[k] for k in reference if k not in ("id", "rules")
        )
    n = len(compiled["idle"].states)
    energy = np.array(
        [float(models["idle"].energy(s)) for s in compiled["idle"].states]
    )
    charge = np.array(
        [
            s[base.indices["bank"]]
            + sum(
                s[base.indices[x.name]]
                for x in base.coordinates
                if x.role == "structural_bond"
            )
            for s in compiled["idle"].states
        ],
        dtype=float,
    )
    observables = {
        "bank": np.array([s[base.indices["bank"]] for s in compiled["idle"].states]),
        "bonds": charge
        - np.array([s[base.indices["bank"]] for s in compiled["idle"].states]),
        "displaced": np.array([s[-1] for s in compiled["idle"].states]),
    }
    rewards = {}
    for key, c in compiled.items():
        roles = {r.id: r.roles for r in c.model.rules}
        rr = {
            name: np.zeros(n)
            for name in (
                "work",
                "heat",
                "capture_net",
                "stroke_net",
                "events",
                "source_gross",
                "source_returned",
            )
        }
        for i, j, e in c.ledger:
            capture = any(
                v in roles[e.rule_id] for v in ("capture.basal", "capture.enabled")
            )
            stroke = "operation.stroke" in roles[e.rule_id]
            if charge[j] - charge[i] != e.direction * (int(capture) - int(stroke)):
                raise ArithmeticError("Chemical charge identity")
            for name, value in (
                ("work", e.work),
                ("heat", e.heat),
                ("events", 1),
                ("capture_net", e.direction * int(capture)),
                ("stroke_net", e.direction * int(stroke)),
            ):
                rr[name][i] += e.rate * value
            if e.boundary != "native":
                rr["source_gross" if e.work >= 0 else "source_returned"][i] += (
                    e.rate * abs(e.work)
                )
            for role in roles[e.rule_id]:
                name = role + (".forward" if e.direction == 1 else ".reverse")
                rr.setdefault(name, np.zeros(n))[i] += e.rate
        rewards[key] = rr
    mu = np.zeros(n)
    mu[compiled["idle"].index[root]] = 1
    rows = []
    for option in ("idle", "aa", "ab"):
        prefix, occ = distributions_and_occupation(compiled[option], mu, 16)
        for recovery in ("idle", "off"):
            end, recovery_occ = distributions_and_occupation(
                compiled[recovery], prefix, 48
            )
            flows = {
                k: float(
                    occ @ rewards[option].get(k, np.zeros(n))
                    + recovery_occ @ rewards[recovery].get(k, np.zeros(n))
                )
                for k in set(rewards[option]) | set(rewards[recovery])
            }
            balance = float((end - mu) @ energy - flows["work"] + flows["heat"])
            charge_balance = float(
                (end - mu) @ charge - flows["capture_net"] + flows["stroke_net"]
            )
            if max(abs(balance), abs(charge_balance)) > 1e-8:
                raise ArithmeticError("Finite operation balances")
            rows.append(
                {
                    "option": option,
                    "source_recovery": recovery,
                    "horizon": 64,
                    "first_law_residual": balance,
                    "charge_residual": charge_balance,
                    "prefix_flows": {
                        k: float(occ @ v) for k, v in rewards[option].items()
                    },
                    "total_flows": flows,
                    "prefix_endpoint": {
                        k: float(prefix @ v) for k, v in observables.items()
                    },
                    "endpoint": {k: float(end @ v) for k, v in observables.items()},
                }
            )
        print(f"Physical schedule qualified: {option}", flush=True)
    write(out / "PHYSICAL.json", rows)
    # Release unused phase ledgers before expensive matrix exponentiation.
    del compiled["ab"], compiled["off"]
    timings = []

    def factory(key):
        def load():
            start = time.perf_counter()
            p = sampled_kernel(compiled[key], 0.25, max_dense_bytes=3 * 1024**3)
            timings.append(
                {
                    "phase": key,
                    "seconds": time.perf_counter() - start,
                    "matrix_bytes": p.nbytes,
                }
            )
            return p

        return load

    streamed = stream_schedule(
        [(factory("aa"), 64), (factory("idle"), 64)], mu, {64, 128}, score_history=False
    )
    prefix, _ = distributions_and_occupation(compiled["aa"], mu, 16)
    end, _ = distributions_and_occupation(compiled["idle"], prefix, 16)
    residual = float(np.max(abs(end - streamed["checkpoints"][128]["endpoint"])))
    if residual > 1e-10:
        raise ArithmeticError("Streamed schedule reset or propagation mismatch")
    write(
        out / "RESULT.json",
        {
            "status": "completed",
            "kernel_builds": timings,
            "propagation_seconds": streamed["propagation_seconds"],
            "endpoint_residual": residual,
            "scientific_entropy_scored": False,
        },
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("out", type=Path)
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args()
    out = args.out.resolve()
    if args.worker:
        if sys.stdin.readline().strip() != "GO":
            raise RuntimeError("Capped launch required")
        worker(out)
        return
    out.mkdir(parents=True, exist_ok=False)
    repo = Path(__file__).resolve().parents[1]
    files = [
        Path(__file__),
        repo / "research/platform/specs/V42C_OPERATIONS_ENGINEERING_r1.md",
        repo / "research/platform/specs/V42C_PAID_OPERATIONS_PROTOCOL_r1.md",
    ]
    files += sorted((repo / "src/omega_cosmology/testbed").glob("*.py"))
    files += [repo / "tests/test_spatial_operations.py"]
    manifest = {}
    with zipfile.ZipFile(out / "SNAPSHOT.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            data = p.read_bytes()
            name = p.relative_to(repo).as_posix()
            manifest[name] = hashlib.sha256(data).hexdigest()
            z.writestr(name, data)
    write(out / "INPUTS.json", manifest)
    receipt = capped(
        [sys.executable, str(Path(__file__).resolve()), str(out), "--worker"],
        out,
        seconds=900,
        memory=4 * 1024**3,
        output_cap=64 * 1024**2,
        cwd=repo,
    )
    write(out / "RECEIPT.json", receipt)
    print(json.dumps(receipt))
    if receipt["exit_code"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
