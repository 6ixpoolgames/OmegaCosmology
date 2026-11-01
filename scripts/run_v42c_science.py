"""Fixed Version C batch: paid full-prefix histories and physical accounts."""

import argparse
import hashlib
import itertools
import json
import sys
import time
import zipfile
from pathlib import Path

import numpy as np

from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.history import distributions_and_occupation, sampled_kernel
from omega_cosmology.testbed.phases import validate_native_schedule
from omega_cosmology.testbed.semantics import (
    ComparisonSpec,
    LawSpec,
    ObservationSpec,
    PresentSpec,
    QuantitySpec,
    validate_comparison,
)
from omega_cosmology.testbed.spatial import spatial_world
from omega_cosmology.testbed.spatial_operations import (
    preparation_model,
    preparation_root,
)
from omega_cosmology.testbed.stream_schedule import stream_schedule
from omega_cosmology.testbed.thermodynamics import audit_equilibrium
from omega_cosmology.testbed.workflow import capped


def write(path, value):
    path.write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def paired(a, b, root, dt):
    p = PresentSpec(
        "common",
        ((root, 1.0),),
        sufficiency="All modeled coordinates retained; exterior commands prescribed",
    )
    c = ComparisonSpec(
        "pulse",
        "process",
        16.0,
        dt,
        {"energy": "literal", "material": "executable", "state": "literal"},
        implementation="Paid reversible stroke under prescribed exterior command",
        common_present=p.id,
        common_present_hash=p.content_fingerprint(),
    )

    def arm(compiled):
        return {
            "compiled": compiled,
            "present": p,
            "comparison": c,
            "law": LawSpec(
                "pulse", compiled.model_hash, {"source": "maintained", "bath_beta": 1}
            ),
            "observation": ObservationSpec(
                "all", tuple(x.name for x in compiled.model.coordinates)
            ),
            "quantity": QuantitySpec(
                "ell", "Complete sampled history entropy", "bits", "full_present"
            ),
        }

    return validate_comparison(c, arm(a), arm(b), require_material=True)


def physical(c, mu, horizon):
    end, occ = distributions_and_occupation(c, mu, horizon)
    n = len(mu)
    roles = {r.id: r.roles for r in c.model.rules}
    rr = {
        k: np.zeros(n)
        for k in (
            "work",
            "heat",
            "events",
            "capture_net",
            "stroke_net",
            "source_gross",
            "source_returned",
        )
    }
    bond_indices = [
        c.model.indices[x.name]
        for x in c.model.coordinates
        if x.role == "structural_bond"
    ]
    bank = c.model.indices["bank"]
    charge = np.array([s[bank] + sum(s[k] for k in bond_indices) for s in c.states])
    energy = np.array([float(c.model.energy(s)) for s in c.states])
    for i, j, e in c.ledger:
        role = roles[e.rule_id]
        cap = any(k in role for k in ("capture.enabled", "capture.basal"))
        stroke = "operation.stroke" in role
        if charge[j] - charge[i] != e.direction * (int(cap) - int(stroke)):
            raise ArithmeticError("Per-event charge imbalance")
        for key, val in (
            ("work", e.work),
            ("heat", e.heat),
            ("events", 1),
            ("capture_net", e.direction * int(cap)),
            ("stroke_net", e.direction * int(stroke)),
        ):
            rr[key][i] += e.rate * val
        if e.boundary != "native":
            rr["source_gross" if e.work >= 0 else "source_returned"][i] += e.rate * abs(
                e.work
            )
        for key in role:
            rr.setdefault(
                key + (".forward" if e.direction == 1 else ".reverse"), np.zeros(n)
            )[i] += e.rate
    flows = {key: float(occ @ v) for key, v in rr.items()}
    balance = float((end - mu) @ energy - flows["work"] + flows["heat"])
    cb = float((end - mu) @ charge - flows["capture_net"] + flows["stroke_net"])
    if max(abs(balance), abs(cb)) > 1e-8:
        raise ArithmeticError("Finite physical balance failed")
    obs = {"bank": [], "A": [], "B": [], "mixed": [], "contact": [], "both": []}
    edges = next(r["edges"] for r in c.model.relations if r["id"] == "geometry")
    for s in c.states:
        types = {"A": [], "B": [], "mixed": []}
        for i, j in edges:
            if s[c.model.indices[f"bond.{i}.{j}"]]:
                a, b = s[c.model.indices[f"site.{i}"]], s[c.model.indices[f"site.{j}"]]
                types["A" if a == b == 1 else "B" if a == b == 2 else "mixed"].append(
                    (i, j)
                )
        contact = any(
            sorted((x, y)) in edges
            for aa in types["A"]
            for bb in types["B"]
            for x in aa
            for y in bb
        )
        for key, value in types.items():
            obs[key].append(len(value))
        obs["bank"].append(s[bank])
        obs["both"].append(bool(types["A"] and types["B"]))
        obs["contact"].append(contact)
    return end, {
        "flows": flows,
        "first_law_residual": balance,
        "charge_residual": cb,
        "endpoint": {k: float(end @ v) for k, v in obs.items()},
        "integrated": {k: float(occ @ v) for k, v in obs.items()},
    }


def worker(out, option, source, dt, smoke):
    started = time.perf_counter()
    base = spatial_world()
    # All pulse arms are validated on their real compilations before scoring.
    compiled = {}
    for k in ("idle", "aa", "ab"):
        m = preparation_model(base, k)
        root = preparation_root(m)
        c = enumerate_model(
            m, [root] if not compiled else compiled["idle"].states, max_states=8000
        )
        c.require_complete()
        if compiled and c.states != compiled["idle"].states:
            raise ArithmeticError("Changed state order")
        compiled[k] = c
        print("compiled", k, len(c.states), flush=True)
    contracts = {
        k: paired(compiled["aa"], compiled[k], root, dt) for k in ("idle", "ab")
    }
    audits = {k: audit_equilibrium(c) for k, c in compiled.items()}
    prefix = compiled[option]
    recovery = compiled["idle"]
    del compiled
    if source == "short":
        m = preparation_model(base, source_on=False)
        recovery = enumerate_model(m, prefix.states, max_states=8000)
        recovery.require_complete()
        audits["off"] = audit_equilibrium(recovery)
    horizon = 64 if smoke else 4096
    phases = [(prefix, round(16 / dt)), (recovery, round((horizon - 16) / dt))]
    validate_native_schedule(phases, dt, horizon)
    for c, _ in phases:
        write(out / ("MODEL_" + c.model_hash + ".json"), c.model.record())
    write(out / "CONTRACTS.json", contracts)
    write(out / "AUDITS.json", audits)
    mu = np.zeros(len(prefix.states))
    mu[prefix.index[root]] = 1
    prefix_end, prefix_phys = physical(prefix, mu, 16)
    physical_rows = {"16": prefix_phys}
    exact_endpoints = {16: prefix_end}
    for t in (64, 256, 1024, 4096):
        if t > horizon:
            continue
        endpoint, row = physical(recovery, prefix_end, t - 16)
        row["flows"] = {
            k: prefix_phys["flows"].get(k, 0) + row["flows"].get(k, 0)
            for k in prefix_phys["flows"].keys() | row["flows"].keys()
        }
        row["integrated"] = {
            k: prefix_phys["integrated"][k] + v for k, v in row["integrated"].items()
        }
        physical_rows[str(t)] = row
        exact_endpoints[t] = endpoint
    write(out / "PHYSICAL.json", physical_rows)
    print("physical gates passed", flush=True)
    times = []

    def factory(c):
        def load():
            start = time.perf_counter()
            p = sampled_kernel(c, dt, max_dense_bytes=3 * 1024**3)
            times.append(
                {"model_hash": c.model_hash, "seconds": time.perf_counter() - start}
            )
            return p

        return load

    checkpoints = {0} | {round(t / dt) for t in exact_endpoints}
    result = stream_schedule(
        [(factory(c), length) for c, length in phases],
        mu,
        checkpoints,
        retain_profile=True,
    )
    errors = {
        str(t): float(
            np.max(
                abs(
                    exact_endpoints[t]
                    - result["checkpoints"][round(t / dt)]["endpoint"]
                )
            )
        )
        for t in exact_endpoints
    }
    if max(errors.values()) > 1e-10:
        raise ArithmeticError("Independent endpoint mismatch")
    profile = np.array(result["profile_bits"])
    np.savez_compressed(out / "PROFILE.npz", ell_bits=profile, cadence=dt)
    write(
        out / "RESULT.json",
        {
            "status": "completed",
            "option": option,
            "source": source,
            "cadence": dt,
            "horizon": horizon,
            "states": len(mu),
            "scientific_scoring": True,
            "qualification": smoke,
            "ell_bits": {
                str(t): float(profile[round(t / dt)]) for t in exact_endpoints
            },
            "endpoint_residuals": errors,
            "max_normalization_error": result["max_normalization_error"],
            "kernel_seconds": times,
            "propagation_seconds": result["propagation_seconds"],
            "seconds": time.perf_counter() - started,
            "law_hashes": [c.model_hash for c, _ in phases],
            "state_order_hash": prefix.state_order_hash,
        },
    )
    print("scoring completed", option, source, dt, flush=True)


def snapshot(repo, out):
    files = sorted((repo / "src/omega_cosmology/testbed").glob("*.py"))
    files += [
        Path(__file__),
        repo / "tests/test_spatial_operations.py",
        repo / "tests/test_v42c_executor.py",
        repo / "research/platform/specs/V42C_MINIMAL_SCIENCE_PLAN_r1.md",
        repo / "research/platform/specs/V42C_PAID_OPERATIONS_PROTOCOL_r1.md",
    ]
    manifest = {}
    with zipfile.ZipFile(out / "SNAPSHOT.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            data = p.read_bytes()
            name = p.relative_to(repo).as_posix()
            manifest[name] = hashlib.sha256(data).hexdigest()
            z.writestr(name, data)
    write(out / "INPUTS.json", manifest)
    return manifest


def main():
    p = argparse.ArgumentParser()
    p.add_argument("out", type=Path)
    p.add_argument("--worker", action="store_true")
    p.add_argument("--option", default="idle", choices=("idle", "aa", "ab"))
    p.add_argument("--source", default="maintained", choices=("maintained", "short"))
    p.add_argument("--dt", type=float, default=0.125, choices=(0.125, 0.25, 0.5))
    p.add_argument("--smoke", action="store_true")
    args = p.parse_args()
    out = args.out.resolve()
    if args.worker:
        if sys.stdin.readline().strip() != "GO":
            raise RuntimeError("Capped launch required")
        worker(out, args.option, args.source, args.dt, args.smoke)
        return
    out.mkdir(parents=True, exist_ok=False)
    repo = Path(__file__).resolve().parents[1]
    manifest = snapshot(repo, out)
    cases = [("idle", "maintained", 0.125, True)] + [
        (o, s, dt, False)
        for dt in (0.125, 0.25, 0.5)
        for s in ("maintained", "short")
        for o in ("idle", "aa", "ab")
    ]
    results = []
    for i, (o, s, dt, smoke) in enumerate(cases):
        if any(
            hashlib.sha256((repo / name).read_bytes()).hexdigest() != digest
            for name, digest in manifest.items()
        ):
            raise RuntimeError("Executed inputs changed after source snapshot")
        job = out / f"{i:02d}_{o}_{s}_{dt}"
        job.mkdir()
        cmd = [
            sys.executable,
            str(Path(__file__).resolve()),
            str(job),
            "--worker",
            "--option",
            o,
            "--source",
            s,
            "--dt",
            str(dt),
        ]
        if smoke:
            cmd += ["--smoke"]
        receipt = capped(
            cmd,
            job,
            seconds=3600,
            memory=4 * 1024**3,
            output_cap=64 * 1024**2,
            cwd=repo,
        )
        write(job / "RECEIPT.json", receipt)
        if receipt["exit_code"] or not (job / "RESULT.json").exists():
            write(
                out / "STATUS.json",
                {
                    "status": "stopped_at_failed_gate",
                    "job": job.name,
                    "receipt": receipt,
                },
            )
            raise SystemExit(1)
        results.append(json.loads((job / "RESULT.json").read_text()))
        write(
            out / "STATUS.json",
            {
                "status": "running",
                "completed": len(results),
                "total": len(cases),
                "latest": job.name,
            },
        )
        print("completed", job.name, receipt, flush=True)
    comparisons = []
    for dt in (0.125, 0.25, 0.5):
        for s in ("maintained", "short"):
            rows = {
                r["option"]: r
                for r in results
                if not r["qualification"] and r["cadence"] == dt and r["source"] == s
            }
            profiles = {}
            for i, (o, ss, dd, smoke) in enumerate(cases):
                if not smoke and ss == s and dd == dt:
                    profiles[o] = np.load(
                        out / f"{i:02d}_{o}_{ss}_{dd}" / "PROFILE.npz"
                    )["ell_bits"]
            for other in ("idle", "ab"):
                delta = profiles["aa"] - profiles[other]
                eps = 1e-7 + 1e-9 * np.arange(len(delta))
                sign = np.where(delta > eps, 1, np.where(delta < -eps, -1, 0))
                nz = np.flatnonzero(sign)
                crosses = []
                for a, b in itertools.pairwise(nz):
                    if sign[a] != sign[b]:
                        crosses.append([float(a * dt), float(b * dt)])
                comparisons.append(
                    {
                        "cadence": dt,
                        "source": s,
                        "left": "aa",
                        "right": other,
                        "headline_delta": {
                            t: rows["aa"]["ell_bits"][t] - rows[other]["ell_bits"][t]
                            for t in rows["aa"]["ell_bits"]
                        },
                        "crossing_brackets": crosses,
                    }
                )
    write(out / "COMPARISONS.json", comparisons)
    write(
        out / "STATUS.json",
        {"status": "completed", "completed": len(results), "total": len(cases)},
    )
    # Compact evidence stays local; publication is a separate author action.
    import shutil

    retained = repo / "research/studies/V42C-spatial-investment/results-2026-11-01"
    retained.mkdir(parents=True, exist_ok=False)
    for path in out.rglob("*"):
        if path.is_file() and path.suffix in (".json", ".npz", ".zip"):
            target = retained / path.relative_to(out)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
    write(
        retained / "EVIDENCE.json",
        {
            "files": [
                {
                    "path": p.relative_to(retained).as_posix(),
                    "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                    "bytes": p.stat().st_size,
                }
                for p in sorted(retained.rglob("*"))
                if p.is_file() and p.name != "EVIDENCE.json"
            ]
        },
    )


if __name__ == "__main__":
    main()
