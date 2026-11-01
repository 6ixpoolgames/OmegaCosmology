"""Capped physical-only spatial prototype. No history entropy is evaluated."""

import argparse
import hashlib
import json
import sys
import time
import zipfile
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import expm_multiply

from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.history import distributions_and_occupation, sampled_kernel
from omega_cosmology.testbed.spatial import ladder_edges, spatial_root, spatial_world
from omega_cosmology.testbed.thermodynamics import audit_equilibrium, flow_rewards
from omega_cosmology.testbed.workflow import capped


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def worker(out):
    start = time.perf_counter()
    model = spatial_world()
    write(out / "MODEL.json", model.record())
    compiled = enumerate_model(model, [spatial_root(model)], max_states=4000)
    compiled.require_complete()
    write(
        out / "COMPILATION.json",
        {
            "states": len(compiled.states),
            "marked_events": len(compiled.ledger),
            "seconds": compiled.seconds,
            "model_hash": compiled.model_hash,
            "generator_hash": compiled.generator_hash,
            "equilibrium": audit_equilibrium(compiled),
        },
    )
    print(f"Compiled {len(compiled.states)} states", flush=True)
    edges = ladder_edges(3)
    states = compiled.states

    def dimers(s, species):
        return [
            {i, j}
            for i, j in edges
            if s[model.indices[f"bond.{i}.{j}"]] == 1
            and s[model.indices[f"site.{i}"]] == species
            and s[model.indices[f"site.{j}"]] == species
        ]

    aa = [dimers(s, 1) for s in states]
    bb = [dimers(s, 2) for s in states]
    contact = np.array(
        [
            bool(
                a
                and b
                and any(tuple(sorted((i, j))) in edges for i in a[0] for j in b[0])
            )
            for a, b in zip(aa, bb)
        ],
        dtype=float,
    )
    masks = {
        "A": np.array(list(map(bool, aa)), float),
        "B": np.array(list(map(bool, bb)), float),
        "contact": contact,
    }
    masks["both"] = masks["A"] * masks["B"]
    wr, heat, activity, _ = flow_rewards(compiled)
    rewards = {
        "source_gross": np.zeros(len(states)),
        "source_returned": np.zeros(len(states)),
        "contact_exit": np.zeros(len(states)),
    }
    rules = {r.id: r for r in model.rules}
    for i, j, e in compiled.ledger:
        for role in rules[e.rule_id].roles:
            key = role + (".forward" if e.direction == 1 else ".reverse")
            rewards.setdefault(key, np.zeros(len(states)))[i] += e.rate
        rule = rules[e.rule_id]
        if "construction.basal" in rule.roles:
            species = sorted(
                c.value
                for c in rule.guards
                if model.coordinates[model.indices[c.coordinate]].role
                == "site_occupancy"
                and c.operator == "eq"
            )
            kind = "A" if species == [1, 1] else "B" if species == [2, 2] else "AB"
            key = f"construction.basal.{kind}." + (
                "forward" if e.direction == 1 else "reverse"
            )
            rewards.setdefault(key, np.zeros(len(states)))[i] += e.rate
        if e.boundary == "work_source":
            rewards["source_gross" if e.work >= 0 else "source_returned"][i] += (
                e.rate * abs(e.work)
            )
        if contact[i] and not contact[j]:
            rewards["contact_exit"][i] += e.rate
    energies = np.array([float(model.energy(s)) for s in states])
    rows = []
    for charge in (2, 0):
        mu = np.zeros(len(states))
        mu[compiled.index[spatial_root(model, bank=charge)]] = 1
        for horizon in (16, 64):
            end, occupation = distributions_and_occupation(compiled, mu, horizon)
            work = float(occupation @ wr)
            q = float(occupation @ heat)
            delta = float((end - mu) @ energies)
            residual = delta - work + q
            if abs(residual) > 1e-8:
                raise ArithmeticError("Finite first-law residual")
            rows.append(
                {
                    "initial_bank": charge,
                    "horizon": horizon,
                    "net_source_work": work,
                    "heat": q,
                    "delta_energy": delta,
                    "first_law_residual": residual,
                    "events": float(occupation @ activity),
                    "bank_endpoint": float(
                        end @ np.array([s[model.indices["bank"]] for s in states])
                    ),
                    "occupations": {k: float(occupation @ v) for k, v in masks.items()},
                    "endpoints": {k: float(end @ v) for k, v in masks.items()},
                    "flows": {k: float(occupation @ v) for k, v in rewards.items()},
                }
            )
        print(f"Physical propagation complete bank={charge}", flush=True)
    no_b = np.flatnonzero(masks["B"] == 0)
    qsub = compiled.q[no_b][:, no_b]
    root = compiled.index[spatial_root(model)]
    initial = np.zeros(len(no_b))
    initial[np.flatnonzero(no_b == root)[0]] = 1
    survival = expm_multiply(qsub.T * 64, initial)
    write(
        out / "PHYSICAL.json",
        {
            "rows": rows,
            "probability_first_B_by_T64": float(1 - survival.sum()),
            "note": "Unconditional flows do not certify pathwise financing or lineage.",
        },
    )
    kernel_start = time.perf_counter()
    p = sampled_kernel(compiled, 0.25, max_dense_bytes=1024**3)
    kernel = {
        "cadence": 0.25,
        "seconds": time.perf_counter() - kernel_start,
        "minimum_probability": float(p.min()),
        "max_row_sum_error": float(np.max(abs(p.sum(axis=1) - 1))),
        "matrix_bytes": p.nbytes,
        "entropy_scored": False,
    }
    write(
        out / "RESULT.json",
        {
            "status": "completed",
            "kernel": kernel,
            "worker_seconds": time.perf_counter() - start,
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
    paths = [
        Path(__file__),
        repo / "research/platform/specs/V42C_SPATIAL_PROTOTYPE_r1.md",
    ]
    paths += sorted((repo / "src/omega_cosmology/testbed").glob("*.py"))
    manifest = {}
    with zipfile.ZipFile(out / "SNAPSHOT.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            name = path.relative_to(repo).as_posix()
            content = path.read_bytes()
            manifest[name] = hashlib.sha256(content).hexdigest()
            archive.writestr(name, content)
    write(out / "INPUTS.json", manifest)
    write(
        out / "PLAN.json",
        {
            "wall_seconds": 600,
            "rss_bytes": 2 * 1024**3,
            "state_cap": 4000,
            "history_scoring": False,
        },
    )
    receipt = capped(
        [sys.executable, str(Path(__file__).resolve()), str(out), "--worker"],
        out,
        seconds=600,
        memory=2 * 1024**3,
        output_cap=64 * 1024**2,
        cwd=repo,
    )
    receipt["status"] = (
        "completed" if receipt["exit_code"] == 0 else "worker_incomplete"
    )
    write(out / "RECEIPT.json", receipt)
    print(json.dumps(receipt))
    if receipt["status"] != "completed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
