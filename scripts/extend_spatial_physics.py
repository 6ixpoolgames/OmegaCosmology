"""Unchanged-law physical occupation, charge and mixing diagnostics only."""

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.history import distributions_and_occupation
from omega_cosmology.testbed.spatial import ladder_edges, spatial_root, spatial_world
from omega_cosmology.testbed.thermodynamics import audit_equilibrium
from omega_cosmology.testbed.workflow import capped


def write(path, obj):
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def worker(out):
    model = spatial_world()
    old = json.loads(
        Path(
            "research/platform/engineering/v42c-spatial-2026-11-01/benchmark-r3/COMPILATION.json"
        ).read_text()
    )
    if model.fingerprint() != old["model_hash"]:
        raise ValueError("Physical law changed")
    compiled = enumerate_model(model, [spatial_root(model)], max_states=4000)
    compiled.require_complete()
    n = len(compiled.states)
    write(out / "MODEL.json", model.record())
    print(f"Compiled {n} unchanged states", flush=True)
    edges = ladder_edges(3)
    rules = {r.id: r for r in model.rules}
    masks = {
        k: np.zeros(n) for k in ("A", "B", "both", "contact", "bonds", "bank", "charge")
    }
    energy = np.array([float(model.energy(s)) for s in compiled.states])
    for i, s in enumerate(compiled.states):
        a, b = [], []
        for u, v in edges:
            if s[model.indices[f"bond.{u}.{v}"]]:
                masks["bonds"][i] += 1
                species = [s[model.indices[f"site.{x}"]] for x in (u, v)]
                if species == [1, 1]:
                    a = [u, v]
                if species == [2, 2]:
                    b = [u, v]
        masks["A"][i], masks["B"][i] = bool(a), bool(b)
        masks["both"][i] = bool(a and b)
        masks["contact"][i] = bool(
            a and b and any(tuple(sorted((u, v))) in edges for u in a for v in b)
        )
        masks["bank"][i] = s[model.indices["bank"]]
    masks["charge"] = masks["bank"] + masks["bonds"]
    rewards = {
        k: np.zeros(n)
        for k in (
            "work",
            "heat",
            "events",
            "accepted_work",
            "returned_work",
            "capture_net",
        )
    }
    for i, j, e in compiled.ledger:
        roles = rules[e.rule_id].roles
        is_capture = any(x in roles for x in ("capture.basal", "capture.enabled"))
        charge_change = masks["charge"][j] - masks["charge"][i]
        if charge_change != (e.direction if is_capture else 0):
            raise ArithmeticError("Pathwise charge identity")
        rewards["capture_net"][i] += e.rate * charge_change
        for key, val in (("work", e.work), ("heat", e.heat), ("events", 1)):
            rewards[key][i] += e.rate * val
        if e.boundary != "native":
            rewards["accepted_work" if e.work >= 0 else "returned_work"][i] += (
                e.rate * abs(e.work)
            )
        for role in roles:
            key = role + (".forward" if e.direction == 1 else ".reverse")
            rewards.setdefault(key, np.zeros(n))[i] += e.rate
    charge_residual = float(
        np.max(abs(compiled.q @ masks["charge"] - rewards["capture_net"]))
    )
    if charge_residual > 1e-10:
        raise ArithmeticError("Charge generator identity")
    matrix = compiled.q.T.tolil()
    matrix[0, :] = np.ones(n)
    rhs = np.zeros(n)
    rhs[0] = 1
    pi = spsolve(matrix.tocsc(), rhs)
    stationary_residual = float(np.max(abs(compiled.q.T @ pi)))
    if pi.min() < -1e-12 or abs(pi.sum() - 1) > 1e-10 or stationary_residual > 1e-10:
        raise ArithmeticError("Stationary distribution")
    write(
        out / "STATIONARY.json",
        {
            "states": n,
            "stationary_residual": stationary_residual,
            "charge_generator_residual": charge_residual,
            "equilibrium": audit_equilibrium(compiled),
            "observables": {k: float(pi @ v) for k, v in masks.items()},
            "physical_flows_per_time": {k: float(pi @ v) for k, v in rewards.items()},
            "entropy_scored": False,
        },
    )
    roots = {f"unbound.bank{v}": spatial_root(model, bank=v) for v in (2, 0)}
    for label, bsites in (("contact", (1, 4)), ("separated", (2, 5))):
        values = {
            "site.0": 1,
            "site.3": 1,
            "bond.0.3": 1,
            f"site.{bsites[0]}": 2,
            f"site.{bsites[1]}": 2,
            f"bond.{bsites[0]}.{bsites[1]}": 1,
        }
        roots[label] = tuple(values.get(c.name, 0) for c in model.coordinates)
    if model.energy(roots["contact"]) != model.energy(roots["separated"]):
        raise ValueError("Geometry diagnostic energy mismatch")
    horizons = (1, 4, 16, 64, 256, 1024, 4096)
    endpoints = {}
    for label, root in roots.items():
        mu = np.zeros(n)
        mu[compiled.index[root]] = 1
        initial = mu.copy()
        total_occ = np.zeros(n)
        rows, previous = [], 0
        endpoints[label] = {}
        for horizon in horizons:
            end, occ = distributions_and_occupation(compiled, mu, horizon - previous)
            total_occ += occ
            first_law = float(
                (end - initial) @ energy
                - total_occ @ rewards["work"]
                + total_occ @ rewards["heat"]
            )
            charge_balance = float(
                (end - initial) @ masks["charge"] - total_occ @ rewards["capture_net"]
            )
            if max(abs(first_law), abs(charge_balance)) > 1e-8:
                raise ArithmeticError("Finite balance")
            if abs(end.sum() - 1) > 1e-10 or end.min() < -1e-12:
                raise ArithmeticError("Propagation distribution")
            rows.append(
                {
                    "horizon": horizon,
                    "interval_start": previous,
                    "endpoint": {k: float(end @ v) for k, v in masks.items()},
                    "occupation": {k: float(total_occ @ v) for k, v in masks.items()},
                    "cumulative_flows": {
                        k: float(total_occ @ v) for k, v in rewards.items()
                    },
                    "interval_flows": {k: float(occ @ v) for k, v in rewards.items()},
                    "stationary_total_variation": float(abs(end - pi).sum() / 2),
                    "first_law_residual": first_law,
                    "charge_balance_residual": charge_balance,
                }
            )
            endpoints[label][horizon] = end
            mu, previous = end, horizon
        write(
            out / f"{label}.json",
            {"root": root, "root_energy": str(model.energy(root)), "rows": rows},
        )
        print(f"Completed physical window {label}", flush=True)
    write(
        out / "MIXING.json",
        {
            "interpretation": "Matched preparations, not enacted options",
            "initial_total_variation": 1,
            "rows": [
                {
                    "horizon": t,
                    "total_variation": float(
                        abs(endpoints["contact"][t] - endpoints["separated"][t]).sum()
                        / 2
                    ),
                }
                for t in horizons
            ],
        },
    )
    write(
        out / "RESULT.json",
        {
            "status": "completed",
            "history_entropy_scored": False,
            "model_hash": compiled.model_hash,
            "generator_hash": compiled.generator_hash,
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
        repo / "research/platform/specs/V42C_PHYSICAL_EXTENSION_r1.md",
    ]
    files += sorted((repo / "src/omega_cosmology/testbed").glob("*.py"))
    manifest = {}
    with zipfile.ZipFile(out / "SNAPSHOT.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for p in files:
            data = p.read_bytes()
            name = p.relative_to(repo).as_posix()
            manifest[name] = hashlib.sha256(data).hexdigest()
            archive.writestr(name, data)
    write(out / "INPUTS.json", manifest)
    receipt = capped(
        [sys.executable, str(Path(__file__).resolve()), str(out), "--worker"],
        out,
        seconds=600,
        memory=2 * 1024**3,
        output_cap=64 * 1024**2,
        cwd=repo,
    )
    write(out / "RECEIPT.json", receipt)
    print(json.dumps(receipt))
    if receipt["exit_code"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
