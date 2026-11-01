"""Verify and summarize the fixed completed Version C batch; no new scoring."""

import hashlib
import json
import zipfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research/studies/V42C-spatial-investment/results-2026-11-01"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def main():
    status = read(DATA / "STATUS.json")
    assert status == {"status": "completed", "completed": 19, "total": 19}
    manifest = read(DATA / "EVIDENCE.json")
    if "files" not in manifest:
        for name, digest in manifest.items():
            assert hashlib.sha256((DATA / name).read_bytes()).hexdigest() == digest, (
                name
            )
        # Preserve the executed formatter's original output before schema repair.
        (DATA / "EVIDENCE_EXECUTED.json").write_bytes(
            (DATA / "EVIDENCE.json").read_bytes()
        )
    else:
        for row in manifest["files"]:
            assert (
                hashlib.sha256((DATA / row["path"]).read_bytes()).hexdigest()
                == row["sha256"]
            )
    inputs = read(DATA / "INPUTS.json")
    with zipfile.ZipFile(DATA / "SNAPSHOT.zip") as z:
        for name, digest in inputs.items():
            assert hashlib.sha256(z.read(name)).hexdigest() == digest
    runs = {}
    totals = []
    endpoint = []
    norm = []
    balances = []
    charge = []
    paired = 0
    audits = 0
    for job in sorted(DATA.iterdir()):
        if not job.is_dir():
            continue
        r = read(job / "RESULT.json")
        receipt = read(job / "RECEIPT.json")
        assert (
            r["status"] == "completed"
            and receipt["exit_code"] == 0
            and receipt["cap_reason"] is None
        )
        assert (
            receipt["peak_job_bytes"] <= receipt["job_memory_cap_bytes"] == 4 * 1024**3
        )
        assert (
            receipt["wall_seconds"] <= 3600 and receipt["output_bytes"] <= 64 * 1024**2
        )
        assert r["states"] == 7344
        for c in read(job / "CONTRACTS.json").values():
            assert c["status"] == "validated_paired_comparison"
            paired += 1
        for a in read(job / "AUDITS.json").values():
            assert a["status"] == "passed" and a["reference_sectors"] == 1
            audits += 1
        endpoint.extend(r["endpoint_residuals"].values())
        norm.append(r["max_normalization_error"])
        profile = np.load(job / "PROFILE.npz")["ell_bits"]
        assert len(profile) == round(r["horizon"] / r["cadence"]) + 1
        assert (
            np.isfinite(profile).all()
            and profile[0] == 0
            and np.all(np.diff(profile) >= -1e-10)
        )
        for t, ell in r["ell_bits"].items():
            assert abs(profile[round(float(t) / r["cadence"])] - ell) < 1e-10
        phys = read(job / "PHYSICAL.json")
        prefix_error = abs(phys["16"]["first_law_residual"])
        for t, x in phys.items():
            balances.append(
                abs(x["first_law_residual"]) + (prefix_error if t != "16" else 0)
            )
            e = x["endpoint"]
            f = x["flows"]
            charge.append(
                abs(
                    e["bank"]
                    + e["A"]
                    + e["B"]
                    + e["mixed"]
                    - 2
                    - f["capture_net"]
                    + f["stroke_net"]
                )
            )
        assert all(x < 1e-8 for x in (max(balances), max(charge)))
        totals.append(receipt)
        if not r["qualification"]:
            key = (r["option"], r["source"], r["cadence"])
            assert key not in runs
            runs[key] = {"result": r, "physical": phys, "profile": profile}
    assert len(totals) == 19 and len(runs) == 18
    assert max(endpoint) < 1e-10 and max(norm) < 1e-10
    comparisons = read(DATA / "COMPARISONS.json")
    assert len(comparisons) == 12
    positive = 0
    for c in comparisons:
        left = runs[("aa", c["source"], c["cadence"])]
        right = runs[(c["right"], c["source"], c["cadence"])]
        delta = left["profile"] - right["profile"]
        eps = 1e-7 + 1e-9 * np.arange(len(delta))
        for t, value in c["headline_delta"].items():
            assert abs(value - delta[round(float(t) / c["cadence"])]) < 1e-10
        positive += int(delta[-1] > eps[-1])
    assert positive == 12
    # Schedules have identical physics across observational cadence.
    max_physical = 0.0
    for o in ("idle", "aa", "ab"):
        for s in ("maintained", "short"):
            ref = runs[(o, s, 0.25)]["physical"]
            for dt in (0.125, 0.5):
                other = runs[(o, s, dt)]["physical"]
                for t in ref:
                    for group in ("flows", "endpoint", "integrated"):
                        for k, v in ref[t][group].items():
                            max_physical = max(
                                max_physical, abs(v - other[t][group][k])
                            )
            for dt in (0.125, 0.25, 0.5):
                a = runs[(o, "maintained", dt)]["profile"]
                b = runs[(o, "short", dt)]["profile"]
                assert (
                    np.max(abs(a[: round(16 / dt) + 1] - b[: round(16 / dt) + 1]))
                    < 1e-10
                )
    assert max_physical < 1e-10
    physical_deltas = []
    for s in ("maintained", "short"):
        for other in ("idle", "ab"):
            for t in ("16", "64", "256", "1024", "4096"):
                a = runs[("aa", s, 0.25)]["physical"][t]
                b = runs[(other, s, 0.25)]["physical"][t]
                physical_deltas.append(
                    {
                        "source": s,
                        "right": other,
                        "horizon": int(t),
                        **{
                            group: {
                                k: a[group].get(k, 0) - b[group].get(k, 0)
                                for k in a[group].keys() | b[group].keys()
                            }
                            for group in ("flows", "endpoint", "integrated")
                        },
                    }
                )
    summary = {
        "status": "verified_completed_batch",
        "jobs": 19,
        "scientific_profiles": 18,
        "paired_contract_checks": paired,
        "source_off_audits": audits,
        "frozen_inputs_verified": len(inputs),
        "wall_hours": sum(r["wall_seconds"] for r in totals) / 3600,
        "peak_GiB": max(r["peak_job_bytes"] for r in totals) / 1024**3,
        "max_endpoint_error": max(endpoint),
        "max_normalization_error": max(norm),
        "max_schedule_first_law_residual_bound": max(balances),
        "max_reconstructed_charge_residual": max(charge),
        "max_cadence_physical_discrepancy": max_physical,
        "positive_comparisons_at_T4096": positive,
        "numerical_scope": "float64 numerical validation; not a rigorous rounding certificate",
        "new_simulations_performed": False,
    }
    write(DATA / "VALIDATION.json", summary)
    write(DATA / "PHYSICAL_DELTAS.json", physical_deltas)
    files = []
    for p in sorted(DATA.rglob("*")):
        if p.is_file() and p.name != "EVIDENCE.json":
            raw = p.read_bytes()
            files.append(
                {
                    "path": p.relative_to(DATA).as_posix(),
                    "sha256": hashlib.sha256(raw).hexdigest(),
                    "bytes": len(raw),
                }
            )
    write(DATA / "EVIDENCE.json", {"files": files})
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
