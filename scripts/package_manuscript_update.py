"""Verify and bundle the six-study documentary update; never run new science."""

import json
import re
import subprocess
from hashlib import sha256
from pathlib import Path

from restore_research_snapshot import write_archive

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/evidence/manuscript-handoff-2026-10-26"
COMMIT = "6ff53614c42cc13fad727ef453ff4d980a0717bb"
STUDIES = {
    "R1": ("R1-constructed-access", "INTERPRETATION_r1.md", 144, 240),
    "R2": ("R2-further-capacity", "INTERPRETATION_r2.md", 216, 396),
    "E1": ("E1-coupled-autocatalysis", "INTERPRETATION_r1.md", 650, 1935),
    "S3": ("S3-repair-and-interaction", "INTERPRETATION_r1.md", 168, 254),
    "S4": ("S4-warning-and-obstruction", "INTERPRETATION_r1.md", 192, 192),
    "S4b": ("S4b-paid-warning", "INTERPRETATION_r1.md", 192, 192),
}


def write(name, value):
    (OUT / name).write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def main():
    if (OUT / "MANUSCRIPT_MATERIALS.zip").exists():
        raise ValueError(
            "Use a new versioned packet; never overwrite an existing bundle"
        )
    git = ["git", "-c", "safe.directory=" + ROOT.as_posix()]
    sources, interpretations, rows = [], [], []

    def source(path, *, include_text=False):
        path = Path(path)
        raw = (ROOT / path).read_bytes()
        committed = subprocess.check_output(
            git + ["show", COMMIT + ":" + path.as_posix()], cwd=ROOT
        )
        if raw != committed:
            raise ValueError(
                "Source differs from the cited published commit: " + str(path)
            )
        sources.append(
            {
                "path": path.as_posix(),
                "sha256": sha256(raw).hexdigest(),
                "bytes": len(raw),
            }
        )
        if include_text:
            interpretations.append((path.as_posix(), raw))
        return raw

    old_validation = json.loads(
        source("research/evidence/manuscript-handoff-2026-10-25/VALIDATION.json")
    )
    for study, (
        folder,
        interpretation,
        expected_profiles,
        expected_comparisons,
    ) in STUDIES.items():
        base = Path("research/studies") / folder
        interpretation_path = base / interpretation
        source(interpretation_path, include_text=True)
        if study in ("R1", "R2", "E1"):
            numerical = next(c for c in old_validation["checks"] if c["study"] == study)
            count_profiles, count_comparisons = (
                numerical["profiles"],
                numerical["comparisons"],
            )
        else:
            analysis_path = base / "results-2026-10-26/ANALYSIS.json"
            analysis = json.loads(source(analysis_path))
            count_profiles, count_comparisons = (
                analysis["profile_rows"],
                len(analysis["comparisons"]),
            )
            if count_profiles != sum(
                v["profiles"] for v in analysis["summary"].values()
            ):
                raise ValueError(
                    "Profile row count disagrees with subgroup receipts: " + study
                )
            source(base / "results-2026-10-26/QUALITY.json")
        if (count_profiles, count_comparisons) != (
            expected_profiles,
            expected_comparisons,
        ):
            raise ValueError("Retained study count mismatch: " + study)
        card = OUT / (study + "_MODEL_CARD.md")
        text = card.read_text(encoding="utf-8")
        for axis in (
            "Numerical confidence",
            "Resolution coverage",
            "Physical adequacy",
            "Claim relevance",
        ):
            if axis not in text:
                raise ValueError("Missing evidence axis: " + study + ":" + axis)
        rows.append(
            {
                "study": study,
                "card": card.name,
                "interpretation": interpretation_path.as_posix(),
                "source_commit": COMMIT,
                "profiles": count_profiles,
                "comparisons": count_comparisons,
                "scope": "study-version card; separate numerical/resolution/physical/relevance axes",
            }
        )
    for path in (
        "research/studies/R2-further-capacity/INTERPRETATION_r1.md",
        "research/studies/R2-further-capacity/reanalysis-2026-10-25/REPORT.md",
        "research/studies/E1-coupled-autocatalysis/refinement-2026-10-25/INTERPRETATION.md",
        "research/studies/S4b-paid-warning/CHAPTER_18_EVIDENCE.md",
        "research/platform/engineering/powered-readiness-2026-10-26/REPORT.md",
    ):
        source(path, include_text=True)
    catalogue = source("sources/v4.1/C_TEST_BED_MODELS_r4.md").decode("utf-8")
    source("sources/v4.1/D_EVIDENCE_MAP_r5.md")
    titles = re.findall(r"^#### Model C\.(\d+)\. (.+)$", catalogue, re.MULTILINE)
    if [int(n) for n, _ in titles] != list(range(1, 18)):
        raise ValueError("Expected every legacy model C.1 through C.17")
    related = {
        1: ["R1"],
        2: ["R1"],
        3: [],
        4: ["S4", "S4b"],
        5: [],
        6: ["R2"],
        7: [],
        8: [],
        9: [],
        10: [],
        11: ["S3"],
        12: [],
        13: ["S4", "S4b"],
        14: [],
        15: [],
        16: [],
        17: [],
    }
    legacy = []
    for n, title in titles:
        number = int(n)
        legacy.append(
            {
                "model": "C." + n,
                "title": title,
                "replication_status": "not_yet_attempted",
                "replication_contract": "literal legacy native-law/protocol reproduction on the audited platform",
                "related_new_studies": related[number],
                "related_studies_are_literal_replication": False,
                "disposition": "recover_missing_primary_records_before_promotion"
                if number == 17
                else "historical_with_claim_specific_qualifications",
                "claim_checks": [
                    {
                        "claim": "removing futile drive widens continuation",
                        "status": "not_reproduced",
                        "comparison_contract": "new S4/S4b maintained physical proxies",
                        "limits": "Not a literal legacy-law rerun; formal T/phenomenal suffering not established",
                    }
                ]
                if number == 13
                else [],
            }
        )
    write(
        "CARD_INDEX.json",
        {
            "schema": "omega.manuscript-study-cards/1",
            "source_commit": COMMIT,
            "studies": rows,
        },
    )
    write(
        "CARRY_FORWARD.json",
        {
            "schema": "omega.legacy-carry-forward/1",
            "source_commit": COMMIT,
            "allowed_replication_statuses": [
                "reproduced",
                "not_reproduced",
                "not_yet_attempted",
            ],
            "limits": "Statuses require their named comparison contract; no automatic model/data withdrawal or claim of a fresh full legacy audit",
            "models": legacy,
        },
    )
    write("SOURCES.json", {"source_commit": COMMIT, "files": sources})
    write(
        "VALIDATION.json",
        {
            "status": "passed",
            "source_commit_bytes_verified": True,
            "cards": len(rows),
            "legacy_models": len(legacy),
            "all_profile_and_comparison_counts_checked": True,
            "source_files": len(sources),
            "new_scientific_runs": 0,
        },
    )
    package = {
        path.relative_to(ROOT).as_posix(): path.read_bytes()
        for path in OUT.iterdir()
        if path.is_file()
        and path.name not in ("EVIDENCE.json", "MANUSCRIPT_MATERIALS.zip")
    }
    package.update(dict(interpretations))
    manifest = {
        "schema": "omega.manuscript-bundle/1",
        "source_commit": COMMIT,
        "files": [
            {"path": path, "sha256": sha256(raw).hexdigest(), "bytes": len(raw)}
            for path, raw in sorted(package.items())
        ],
        "limits": "Full interpretations and narrative handoff; numerical maps remain at the linked published repository paths",
    }
    package["BUNDLE_MANIFEST.json"] = (json.dumps(manifest, indent=2) + "\n").encode(
        "utf-8"
    )
    write_archive(OUT / "MANUSCRIPT_MATERIALS.zip", package)
    write(
        "EVIDENCE.json",
        {
            "schema": "omega.retained-evidence/1",
            "files": [
                {
                    "path": path.name,
                    "sha256": sha256(path.read_bytes()).hexdigest(),
                    "bytes": path.stat().st_size,
                }
                for path in sorted(OUT.iterdir())
                if path.is_file() and path.name != "EVIDENCE.json"
            ],
        },
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "cards": len(rows),
                "legacy_rows": len(legacy),
                "bundle_files": len(package),
                "bundle_bytes": (OUT / "MANUSCRIPT_MATERIALS.zip").stat().st_size,
            }
        )
    )


if __name__ == "__main__":
    main()
