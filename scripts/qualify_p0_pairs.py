"""Frozen, capped retained-slot qualification of the selected P0 inputs."""

import argparse
import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path
from time import perf_counter
from zipfile import ZipFile

from restore_research_snapshot import write_archive

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
P0 = Path("research/platform/engineering/p0-t-verification-2026-10-30")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    Path(path).write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def witness_records(study):
    def slot(coordinate, labels):
        return {
            "coordinate": coordinate,
            "states": [[i, label] for i, label in enumerate(labels)],
        }

    def inventory(id, slots):
        return {
            "inventory_id": id,
            "slots": slots,
            "justification": "The original declaration retains each named physical unit through all listed internal states; this witness interprets fixed units, not chemical atoms or unmodeled matter.",
        }

    active = ("precursor", "working")
    if study in ("R1", "R2"):
        result = [
            inventory(
                "constituent_slots",
                [slot("a.active", active), slot("b.active", active)],
            )
        ]
        if study == "R2":
            result.append(
                inventory(
                    "latent_storage_slot", [slot("store.built", ("precursor", "built"))]
                )
            )
        return result
    if study in ("E1", "S3"):
        return [
            inventory(
                group + ".slots",
                [slot(group + ".x", active), slot(group + ".y", active)],
            )
            for group in ("A", "B")
        ] + [
            inventory(
                "shared_carrier", [slot("carrier", ("spent", "locked", "usable"))]
            )
        ]
    if study in ("S4", "S4b"):
        return [
            inventory("body_slot", [slot("body.working", ("damaged", "working"))]),
            inventory("carrier_slot", [slot("carrier", ("spent", "charged"))]),
        ]
    raise ValueError("Unregistered study")


def prepare(out):
    if out.exists() or not out.is_relative_to(ROOT / "runs"):
        raise ValueError("Fresh run directory required")
    evidence = ROOT / P0
    records = {r["path"]: r for r in read(evidence / "EVIDENCE.json")["files"]}

    def verified(relative):
        path = evidence / relative
        if digest(path) != records[relative]["sha256"]:
            raise ValueError("P0 input evidence changed")
        return path

    source_archive = verified("ORIGINAL_SOURCES.zip")
    plan = read(verified("PLAN.json"))
    registered = {
        "schema": "omega.paired-qualification/1",
        "date": "2026-10-30",
        "cadence": 0.25,
        "horizons": [16, 64],
        "studies": [],
        "caps": {
            "case_seconds": 240,
            "job_memory_bytes": 2 * 1024**3,
            "case_output_bytes": 32 * 1024**2,
            "batch_seconds": 1200,
            "batch_output_bytes": 128 * 1024**2,
        },
        "source_evidence": {
            "path": P0.as_posix(),
            "manifest_sha256": digest(evidence / "EVIDENCE.json"),
            "source_archive_sha256": digest(source_archive),
        },
        "r2_constraint_change": {
            "removed": [],
            "added": [[{"coordinate": "bank", "operator": "ge", "value": 5}]],
        },
    }
    blobs = {}
    with ZipFile(source_archive) as z:
        for study in plan["studies"]:
            protocol = json.loads(z.read(study["id"] + "/" + study["protocol"]))
            prep = next(
                p for p in protocol["preparations"] if p["id"] == study["preparation"]
            )
            laws = []
            for law_id in study["laws"]:
                law = next(l for l in protocol["laws"] if l["id"] == law_id)
                prefix = "retained/" + study["id"] + "__" + law_id + "__0.25/"
                result = read(verified(prefix + "ORIGINAL_RESULT.json"))
                native = verified(prefix + "LAW.npz")
                relative = "inputs/" + study["id"] + "/" + law_id + ".npz"
                blobs[relative] = native.read_bytes()
                expected = [
                    r
                    for r in result["rows"]
                    if r["preparation"] == prep["id"]
                    and r["horizon"] in registered["horizons"]
                ]
                if len(expected) != len(registered["horizons"]):
                    raise ValueError("Original selected windows missing")
                laws.append(
                    {
                        "law": law,
                        "native_export": relative,
                        "expected_rows": expected,
                        "original_result_sha256": digest(
                            verified(prefix + "ORIGINAL_RESULT.json")
                        ),
                    }
                )
            payload = {
                "study": study["id"],
                "preparation": prep,
                "all_roots": [
                    s for p in protocol["preparations"] for s, _ in p["roots"]
                ],
                "laws": laws,
                "witnesses": witness_records(study["id"]),
                "coefficients": study["coefficients"],
                "pairs": study.get("pair_indices", [[0, 1]]),
            }
            name = "inputs/" + study["id"] + ".json"
            blobs[name] = (json.dumps(payload, indent=2) + "\n").encode()
            registered["studies"].append({"id": study["id"], "input": name})
    # Everything above is source/protocol inspection; no fresh profile scored.
    out.mkdir(parents=True)
    current = out / "frozen"
    for name, raw in blobs.items():
        path = current / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    write(out / "PLAN.json", registered)
    files = sorted((ROOT / "src/omega_cosmology/testbed").glob("*.py")) + [
        ROOT / "src/omega_cosmology/__init__.py",
        Path(__file__).resolve(),
        ROOT / "scripts/restore_research_snapshot.py",
        ROOT / "tests/test_paired_qualification.py",
        ROOT / "research/platform/specs/PAIRED_QUALIFICATION_r1.md",
    ]
    manifest = {
        "schema": "omega.paired-qualification-snapshot/1",
        "plan_sha256": digest(out / "PLAN.json"),
        "files": [],
    }
    for p in files:
        relative = p.relative_to(ROOT)
        path = current / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, path)
    for p in sorted(current.rglob("*")):
        if p.is_file():
            manifest["files"].append(
                {
                    "path": p.relative_to(current).as_posix(),
                    "bytes": p.stat().st_size,
                    "sha256": digest(p),
                }
            )
    write(current / "MANIFEST.json", manifest)
    print(
        json.dumps(
            {
                "status": "prepared",
                "studies": len(registered["studies"]),
                "plan_sha256": manifest["plan_sha256"],
            }
        )
    )


def worker(out, id):
    if sys.stdin.readline().strip() != "GO":
        raise SystemExit("Capped worker gate required")
    import numpy as np

    manifest = read(out / "frozen/MANIFEST.json")
    if digest(out / "PLAN.json") != manifest["plan_sha256"]:
        raise ValueError("Qualification plan changed")
    for row in manifest["files"]:
        if digest(out / "frozen" / row["path"]) != row["sha256"]:
            raise ValueError("Frozen qualification source changed")
    sys.path.insert(0, str(out / "frozen/src"))
    from omega_cosmology.testbed.backends import enumerate_model
    from omega_cosmology.testbed.history import (
        distributions_and_occupation,
        entropy,
        history_profile,
        sampled_kernel,
    )
    from omega_cosmology.testbed.inventory_witness import (
        InventoryWitness,
        RetainedSlot,
        interpret_retained_slots,
    )
    from omega_cosmology.testbed.physics import LocalModel
    from omega_cosmology.testbed.semantics import (
        ComparisonSpec,
        LawSpec,
        ObservationSpec,
        PresentSpec,
        QuantitySpec,
        validate_comparison,
    )
    from omega_cosmology.testbed.state_mapping import (
        ConstraintStateMapping,
        constraint_identity,
    )
    from omega_cosmology.testbed.thermodynamics import balance

    plan = read(out / "PLAN.json")
    data = read(out / "frozen/inputs" / (id + ".json"))
    witnesses = [
        InventoryWitness(
            w["inventory_id"],
            tuple(
                RetainedSlot(s["coordinate"], tuple(tuple(v) for v in s["states"]))
                for s in w["slots"]
            ),
            w["justification"],
        )
        for w in data["witnesses"]
    ]
    prep = data["preparation"]
    present = PresentSpec(
        "qualified.present",
        tuple((tuple(s), weight) for s, weight in prep["roots"]),
        conditioning=prep["conditioning"],
        sufficiency="The complete original rule-dependent state, under an explicit fixed-retained-unit interpretation",
    )
    results, compilations, arms = [], [], []
    for item in data["laws"]:
        source = LocalModel.from_record(item["law"]["model"])
        model, interpretation = interpret_retained_slots(source, witnesses)
        roots = [tuple(s) for s in data["all_roots"]]
        original = enumerate_model(source, roots, max_states=1500)
        compiled = enumerate_model(model, roots, max_states=1500)
        original.require_complete()
        compiled.require_complete()
        native = np.load(out / "frozen" / item["native_export"], allow_pickle=False)
        if (
            not np.array_equal(np.array(compiled.states), native["states"])
            or compiled.states != original.states
        ):
            raise ArithmeticError("Inventory interpretation changed states")
        qdiff = float(np.max(abs(compiled.q.toarray() - native["q"])))
        if (
            qdiff != 0
            or (original.q != compiled.q).nnz
            or compiled.ledger != original.ledger
        ):
            raise ArithmeticError(
                "Inventory interpretation changed native dynamics or event marks"
            )
        if any(model.energy(s) != source.energy(s) for s in compiled.states):
            raise ArithmeticError("Inventory interpretation changed energy")
        counts = [len(w.slots) for w in witnesses]
        expected_inventory = {
            w.inventory_id: str(count) for w, count in zip(witnesses, counts)
        }
        if any(model.inventory(s) != expected_inventory for s in compiled.states):
            raise ArithmeticError("Retained-unit witness failed on compiled state")
        mu = np.zeros(len(compiled.states))
        for state, weight in present.roots:
            mu[compiled.index[model.canonical(state)]] += weight
        p = sampled_kernel(compiled, plan["cadence"], max_dense_bytes=128 * 1024**2)
        profile = history_profile(p, mu, round(max(plan["horizons"]) / plan["cadence"]))
        rows = []
        for T in plan["horizons"]:
            old = next(r for r in item["expected_rows"] if r["horizon"] == T)
            value = float(profile[round(T / plan["cadence"])])
            diff = value - old["history"]["ell_bits"]
            if abs(diff) > 1e-7:
                raise ArithmeticError("Qualification changed historical history value")
            endpoint, occupation = distributions_and_occupation(compiled, mu, T)
            physical = balance(compiled, mu, endpoint, occupation)
            if (
                max(
                    abs(physical[k] - old["physical"][k])
                    for k in (
                        "work_net",
                        "heat_export",
                        "delta_energy",
                        "expected_jumps",
                    )
                )
                > 1e-8
            ):
                raise ArithmeticError("Qualification changed physical accounting")
            rows.append(
                {
                    "horizon": T,
                    "ell_bits": value,
                    "difference_from_P0_bits": diff,
                    "physical": physical,
                }
            )
        boundary = {
            "beta": model.beta,
            "external_channels": [
                r
                for r in item["law"]["model"]["rules"]
                if r.get("boundary", "native") != "native"
            ],
            "unresolved": "external bath/source histories",
        }
        base = {
            "compiled": compiled,
            "present": present,
            "law": LawSpec(item["law"]["id"], model.fingerprint(), boundary),
            "observation": ObservationSpec(
                "qualified.whole", tuple(c.name for c in model.coordinates)
            ),
            "quantity": QuantitySpec(
                "full.history",
                "Full sampled native history under explicit retained-unit interpretation",
                "bits",
                "full_present",
            ),
        }
        arms.append(base)
        compilations.append(compiled)
        results.append(
            {
                "original_law": item["law"]["id"],
                "interpretation": interpretation,
                "interpreted_model": model.record(),
                "native_generator_difference": qdiff,
                "state_count": len(compiled.states),
                "marked_event_count": len(compiled.ledger),
                "native_ledger_unchanged": True,
                "state_hash": compiled.state_order_hash,
                "native_generator_entries_sha256": sha256(
                    compiled.q.toarray().tobytes()
                ).hexdigest(),
                "inventory_on_every_reachable_state": expected_inventory,
                "rows": rows,
            }
        )
    pairs = []
    for left, right in data["pairs"]:
        mapping = None
        if id == "R2":
            a, b = compilations[left], compilations[right]
            changes = plan["r2_constraint_change"]
            mapping = ConstraintStateMapping(
                a.model_hash,
                b.model_hash,
                a.state_order_hash,
                b.state_order_hash,
                tuple(constraint_identity(p) for p in changes["removed"]),
                tuple(constraint_identity(p) for p in changes["added"]),
            )
        for T in plan["horizons"]:
            comparison = ComparisonSpec(
                "qualified.pair",
                "mechanism",
                T,
                plan["cadence"],
                {
                    "energy": "same actual physical root",
                    "material": "same explicitly witnessed retained units",
                    "resolution": "same full physical coordinate alphabet; R2 has declared constraint mapping",
                },
            )
            la, ra = (
                dict(arms[left], comparison=comparison),
                dict(arms[right], comparison=comparison),
            )
            certificate = validate_comparison(
                comparison, la, ra, state_mapping=mapping, require_material=True
            )
            map_check = None
            if mapping is not None:
                residuals = []
                for which, c in (
                    ("left", compilations[left]),
                    ("right", compilations[right]),
                ):
                    mu = np.zeros(len(c.states))
                    for state, w in present.roots:
                        mu[c.index[c.model.canonical(state)]] += w
                    p = sampled_kernel(c, plan["cadence"])
                    endpoint = mu @ p
                    embedded = mapping.embed_distribution(
                        compilations[left], compilations[right], which, endpoint
                    )
                    residuals.append(abs(float(entropy(endpoint) - entropy(embedded))))
                map_check = {
                    "one_step_entropy_relabelling_residual_bits": max(residuals),
                    "all_finite_histories": "injective symbol mapping preserves word probabilities; no probability assigned to absent symbols",
                    "padding_physical_process": False,
                }
                if max(residuals) > 1e-12:
                    raise ArithmeticError("Ambient observation mapping changed entropy")
            pairs.append(
                {
                    "left": results[left]["original_law"],
                    "right": results[right]["original_law"],
                    "horizon": T,
                    "certificate": certificate,
                    "mapping_check": map_check,
                }
            )
    contrasts = [
        {
            "horizon": T,
            "delta_bits": sum(
                c * next(r for r in arm["rows"] if r["horizon"] == T)["ell_bits"]
                for c, arm in zip(data["coefficients"], results)
            ),
        }
        for T in plan["horizons"]
    ]
    write(
        out / "jobs" / id / "RESULT.json",
        {
            "status": "passed",
            "study": id,
            "cadence": plan["cadence"],
            "arms": results,
            "paired_checks": pairs,
            "contrasts": contrasts,
            "limits": "Interpreted retained-unit inventories only; not full chemistry, historical-certificate replacement, physical faithfulness, exterior cancellation or an ethical certificate",
        },
    )
    print(json.dumps({"status": "passed", "study": id, "paired_checks": len(pairs)}))


def run(out):
    from omega_cosmology.testbed.workflow import capped, tree_bytes

    if (out / "BATCH_RECEIPT.json").exists():
        raise ValueError("Do not overwrite completed qualification")
    plan = read(out / "PLAN.json")
    started, receipts, status = perf_counter(), [], "passed"
    for study in plan["studies"]:
        folder = out / "jobs" / study["id"]
        folder.mkdir(parents=True)
        remaining = plan["caps"]["batch_seconds"] - (perf_counter() - started)
        if remaining <= 0:
            status = "incomplete"
            break
        receipt = capped(
            [
                sys.executable,
                str(out / "frozen/scripts/qualify_p0_pairs.py"),
                "worker",
                "--out-dir",
                str(out),
                "--study",
                study["id"],
            ],
            folder,
            seconds=min(remaining, plan["caps"]["case_seconds"]),
            memory=plan["caps"]["job_memory_bytes"],
            output_cap=plan["caps"]["case_output_bytes"],
            cwd=out / "frozen",
        )
        write(folder / "RECEIPT.json", receipt)
        ok = (
            receipt["exit_code"] == 0
            and receipt["cap_reason"] is None
            and (folder / "RESULT.json").exists()
        )
        receipts.append({"study": study["id"], "passed": ok, "receipt": receipt})
        print(
            json.dumps(
                {"study": study["id"], "passed": ok, "seconds": receipt["wall_seconds"]}
            ),
            flush=True,
        )
        if not ok:
            status = "incomplete"
        if tree_bytes(out / "jobs") > plan["caps"]["batch_output_bytes"]:
            status = "incomplete"
            break
    write(
        out / "BATCH_RECEIPT.json",
        {
            "status": status,
            "plan_sha256": digest(out / "PLAN.json"),
            "manifest_sha256": digest(out / "frozen/MANIFEST.json"),
            "wall_seconds": perf_counter() - started,
            "jobs": receipts,
        },
    )
    return status


def retain(out, evidence):
    if evidence.exists() or not evidence.is_relative_to(
        ROOT / "research/platform/engineering"
    ):
        raise ValueError("Fresh engineering evidence output required")
    evidence.mkdir(parents=True)
    for name in ("PLAN.json", "BATCH_RECEIPT.json"):
        shutil.copyfile(out / name, evidence / name)
    manifest = read(out / "frozen/MANIFEST.json")
    files = {
        r["path"]: (out / "frozen" / r["path"]).read_bytes() for r in manifest["files"]
    }
    if any(
        sha256(files[r["path"]]).hexdigest() != r["sha256"] for r in manifest["files"]
    ):
        raise ValueError("Frozen source changed before retention")
    files["MANIFEST.json"] = (out / "frozen/MANIFEST.json").read_bytes()
    write_archive(evidence / "SNAPSHOT.zip", files)
    for path in (out / "jobs").rglob("*"):
        if path.is_file():
            target = evidence / "retained" / path.relative_to(out / "jobs")
            target.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix == ".log":
                text = (
                    path.read_text(encoding="utf-8")
                    .replace(str(ROOT), "<repo>")
                    .replace(ROOT.as_posix(), "<repo>")
                )
                target.write_text(text, encoding="utf-8")
            else:
                shutil.copyfile(path, target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run", "worker", "retain"))
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--study")
    parser.add_argument("--evidence-dir", type=Path)
    a = parser.parse_args()
    out = a.out_dir.resolve()
    if a.mode != "worker" and not out.is_relative_to(ROOT / "runs"):
        parser.error("Local run directory required")
    if a.mode == "prepare":
        prepare(out)
    elif a.mode == "worker":
        worker(out, a.study)
    elif a.mode == "run":
        return run(out) != "passed"
    else:
        retain(out, a.evidence_dir.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
