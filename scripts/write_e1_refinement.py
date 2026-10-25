"""Derive readout-only E1 memory refinements; every physical law stays unchanged."""

import json
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "research/studies/E1-coupled-autocatalysis"


def main():
    source = STUDY / "PROTOCOL.json"
    original = json.loads(source.read_text(encoding="utf-8"))
    folder = STUDY / "refinement-2026-10-25"
    folder.mkdir(exist_ok=True)
    for memory in (2, 3):
        protocol = deepcopy(original)
        protocol["id"] = f"E1-projected-memory-{memory}-r1"
        protocol["question"] = (
            "Readout refinement of the retained low-supply/low-bill/slow-turnover "
            "AtoB versus local contrast, including its unresolved donor history."
        )
        selected = {"S0p02_C1_D0p001__local", "S0p02_C1_D0p001__AtoB"}
        protocol["laws"] = [l for l in protocol["laws"] if l["id"] in selected]
        protocol["cadences"] = [0.25]
        protocol["case_grid"] = [[l["id"], 0.25] for l in protocol["laws"]]
        for spec in protocol["projected_histories"]:
            spec["memory"] = memory
            spec["max_workspace_bytes"] = 256 * 1024**2
            spec["max_words"] = 100000
        protocol["caps"].update(
            case_wall_seconds=240,
            batch_wall_seconds=600,
            job_memory_bytes=2 * 1024**3,
            case_output_bytes=16 * 1024**2,
            batch_output_bytes=64 * 1024**2,
        )
        protocol["execution"] = {"max_workers": 2}
        protocol["source_inputs"] = list(
            dict.fromkeys(
                protocol["source_inputs"]
                + [
                    "scripts/write_e1_refinement.py",
                    "research/studies/E1-coupled-autocatalysis/refinement-2026-10-25/PLAN.md",
                ]
            )
        )
        protocol["refines"] = {
            "protocol_sha256": sha256(source.read_bytes()).hexdigest(),
            "kind": "analysis_only_observation_memory",
            "physical_changes": [],
            "reason_for_selection": (
                "The documented E1 donor/recipient example; selected to benchmark "
                "precision, without selecting a desired sign. Both preparations retained."
            ),
        }
        path = folder / f"PROTOCOL_m{memory}.json"
        if path.exists():
            raise FileExistsError(
                "Use a new revision rather than overwrite a run input"
            )
        path.write_text(json.dumps(protocol, indent=2) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
