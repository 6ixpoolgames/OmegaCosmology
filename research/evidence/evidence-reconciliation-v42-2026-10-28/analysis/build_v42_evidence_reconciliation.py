"""Build source-anchored editorial proposals; never edit manuscripts or run models."""

import argparse
import json
import re
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = "research/platform/engineering/c7-replay-2026-10-28"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def paragraph(text, needle):
    if text.count(needle) != 1:
        raise ValueError("Unique source needle required: " + needle)
    i = text.index(needle)
    start = text.rfind("\n\n", 0, i) + 2
    stop = text.find("\n\n", i)
    return text[start : stop if stop >= 0 else len(text)].strip("\n")


def between(text, start, stop):
    return text[text.index(start) : text.index(stop, text.index(start))].rstrip("\n")


def bullet(text, needle):
    if text.count(needle) != 1:
        raise ValueError("Unique bullet required: " + needle)
    start = text.rfind("\n", 0, text.index(needle)) + 1
    stop = start
    for line in text[start:].splitlines(keepends=True):
        if stop != start and not line.startswith(("  ", "\t")):
            break
        stop += len(line)
    return text[start:stop].rstrip("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    sources, out = args.sources.resolve(), args.out.resolve()
    if out.exists() or not out.is_relative_to(ROOT / "research/evidence"):
        parser.error("Fresh local evidence-reconciliation folder required")
    discovery = read(sources / "DISCOVERY_PRIVATE.json")["root"]
    active = [r for r in discovery if r["title"].endswith(".md")]
    if len(active) != 32:
        raise ValueError("Reassess coverage if the discovered working set changes")
    inventories, texts = [], {}
    for row in active:
        path = sources / row["title"]
        if path.stat().st_size != int(row["size"]):
            raise ValueError("Incomplete or normalized source text: " + row["title"])
        texts[row["title"]] = path.read_text(encoding="utf-8")
        inventories.append(
            {
                "id": "v42-" + sha256(row["title"].encode()).hexdigest()[:12],
                "file": row["title"],
                "bytes": path.stat().st_size,
                "sha256": digest(path),
                "modified_time": row["modified_time"],
                "role": "active_working_folder",
                "metadata_byte_size_agrees": True,
            }
        )
    for name in (
        "V42_OUTLINE_r2.md",
        "V42_MIGRATION_LOG.md",
        "V42_STYLE_SHEET_r5.md",
        "V42_STYLE_SHEET_HISTORY.md",
    ):
        path = sources / name
        texts[name] = path.read_text(encoding="utf-8")
        inventories.append(
            {
                "id": "v42-" + sha256(name.encode()).hexdigest()[:12],
                "file": name,
                "bytes": path.stat().st_size,
                "sha256": digest(path),
                "role": "context_note",
                "authority": "working context, not an independent approval",
            }
        )
    before_hashes = {name: digest(sources / name) for name in texts}
    c7 = read(ROOT / EVIDENCE / "retained/RESULT.json")
    quality = read(ROOT / EVIDENCE / "QUALITY.json")
    if c7["arms"] != {"loop": "reproduced", "basal": "reproduced"}:
        raise ValueError("Reassess proposals if the retained replay verdict differs")
    r2_path = (
        ROOT
        / "research/platform/engineering/r2-transduction-2026-10-27/retained/COMPARISON_CONTRACTS.json"
    )
    r2 = read(r2_path)
    links = [
        r
        for r in r2
        if r["second"] in ("no_construction_assistance", "no_secondary_access")
    ]
    if not links or any(
        r["contract"]["status"] != "validated_paired_comparison" for r in links
    ):
        raise ValueError("Do not assert unverified R2 paired checks")
    evidence_paths = [
        EVIDENCE + "/REPORT.md",
        EVIDENCE + "/PROVENANCE.json",
        EVIDENCE + "/QUALITY.json",
        EVIDENCE + "/retained/RESULT.json",
        EVIDENCE + "/retained/loop.json",
        EVIDENCE + "/retained/basal.json",
        "research/platform/engineering/r2-transduction-2026-10-27/REPORT.md",
        r2_path.relative_to(ROOT).as_posix(),
        "research/platform/engineering/r2-bank-load-2026-10-28/QUALITY.json",
        "research/platform/engineering/r2-bank-load-2026-10-28/retained/RESULT.json",
        "src/omega_cosmology/testbed/semantics.py",
    ]
    changes = []

    def add(file, original, replacement, reason, refs=None, action="replace"):
        text = texts[file]
        if text.count(original) != 1:
            raise ValueError(
                "Replacement must identify exactly one passage: "
                + file
                + " / "
                + original[:80]
            )
        index = text.index(original)
        heading = [v for v in text[:index].splitlines() if v.startswith("#")]
        section = (
            original.splitlines()[0]
            if original.startswith("#")
            else (heading[-1] if heading else "opening drafting note")
        )
        changes.append(
            {
                "id": f"ER{len(changes) + 1:02}",
                "file": file,
                "section": section,
                "line": text[:index].count("\n") + 1,
                "source_sha256": before_hashes[file],
                "action": action,
                "original": original,
                "replacement": replacement,
                "reason": reason,
                "evidence": refs
                or [EVIDENCE + "/REPORT.md", EVIDENCE + "/QUALITY.json"],
            }
        )

    ch = "19_WHAT_THE_EVIDENCE_ESTABLISHES_r4.md"
    original = next(
        l
        for l in texts[ch].splitlines()
        if l.startswith("| | At matched accepted work,")
    )
    add(
        ch,
        original,
        "| | The historical twelve-point study reports a higher enabling-loop rate at matched stationary accepted work; one selected point has now been numerically reproduced | M1, historical resolution label; faithfulness open | [C.7](#c-matched-work) |",
        "Separate original study coverage, stationary matching and the one-point replay.",
    )
    add(
        ch,
        paragraph(texts[ch], "**Results recorded before the current checks.**"),
        """**Historical results and later checks.** The original studies retain their
historical scope. A representative C.7 point—capacity 4, the middle work target,
from the retained seed—has now been replayed from verified frozen source.
All 24 arm profiles, comprising 12 paired horizon-and-cadence comparisons,
reproduce; independent calculations and the stated energy-accounting checks
agree. This is numerical reproduction of that point, not of all twelve points.

C.7 deliberately uses different source arrival rates. It matches stationary
accepted work, while offered boundaries, finite work, activity and unresolved
external histories are unmatched. The current identical-boundary paired
certificate is inapplicable to this construction. Full chemical material
accounting and physical faithfulness also remain open. Appendix D records
numerical reproduction, paired checks and physical limits separately.

Separately, the newer construction/transduction engineering smoke on the current
platform passes executable paired checks for its stated same-boundary mechanism
contrasts. Those are different laws from C.7 and do not recertify the historical
study. Passing those checks establishes finite-model comparison consistency;
it does not prove physical faithfulness or the ethical thesis.""",
        "Replace the blanket replay/recertification account and preserve the separate R2 evidence.",
        [*evidence_paths[:6], *evidence_paths[6:8]],
    )
    original = bullet(texts[ch], "- **The scope of the construction.**")
    add(
        ch,
        original,
        """- **The scope of the construction.** What the whole-field measure applies
  to where quantum records are incompatible, and comparison-specific checks of
  historical model results. C.7's selected numerical replay is complete; its
  unequal source boundaries leave the identical-boundary paired certificate
  inapplicable. Other studies need the checks appropriate to their own claims.""",
        "Do not prescribe one validator for every type of historical contrast.",
    )
    original = next(l for l in texts[ch].splitlines() if l.startswith("| **Open** |"))
    add(
        ch,
        original,
        "| **Open** | the physical scope of the construction and comparison-specific validation of historical results (19.3); C.7's selected numerical replay is complete, with paired certification inapplicable; the program ahead (19.5) |",
        "Keep the summary status consistent with the completed replay.",
    )
    original = paragraph(texts[ch], "- **Busy noise at matched activity**")
    # The source groups the four bullets into one block; retain the other three.
    replacement = original.replace(
        "- **Busy noise at matched activity** (section 18.9).",
        "- **Busy noise at matched activity** (section 18.9). A qualified comparison\n  remains open: engineering controls have been built, but matching the moments\n  did not yield the intended net-consuming control.",
    )
    add(
        ch,
        original,
        replacement,
        "Distinguish an unfinished scientific comparison from engineering work already attempted.",
        [evidence_paths[8], evidence_paths[9]],
    )

    c = "C_TEST_BED_MODELS_r1.md"
    original = between(texts[c], "#### Model C.7. Matched work", "#### Model C.8.")
    replacement = original.replace(
        "**Question.** Does the enabling relation add futures that a non-enabling\nprocess taking in the same external work does not?",
        "**Question.** Can an enabling-loop law have a higher history-breadth\nrate than its basal comparator at matched stationary accepted external work?",
    )
    replacement = replacement.replace(
        "**Key figures.**",
        "**Historical twelve-point study.** The following figures are retained from\nthe original study; they have not all received the representative replay.",
    )
    replacement = replacement.replace(
        "**How far it holds.** No sign changes. Tier M1.",
        "**Resolution coverage.** No reported sign changes at the three cadences.\nThe historical M1 label is retained as a provisional coverage descriptor, not\na physical-faithfulness or paired-comparison certificate.",
    )
    replacement = replacement.replace(
        "**Scope.** Work is matched, activity is not ([Appendix D, section\nD.5.1](#appendix-d)). This model does not answer the activity-matched test.",
        """**Representative replay, 28 October 2026.** The capacity-4 middle-target
loop/basal pair, from seed [6,1,1], was recovered from both original frozen
bundles. The common source manifest and all 64 source files per bundle pass
their hashes. All 24 arm profiles reproduce exactly, at horizons 16, 64, 256
and 1024 and cadences 0.125, 0.25 and 0.5. Independent history calculations
agree within 5.61 × 10⁻¹⁰ bits. Loop minus basal is positive at every tested
window; at T64 and cadence 0.25 it is +39.425660 bits. The corresponding rate
differences are +0.110125, +0.095049 and +0.080271 bits/time at the three
cadences. Only this one of the twelve historical parameter points was replayed.

**Matching and limits.** Stationary accepted work is about 0.07814421443
energy/time in both arms, differing by 1.4 × 10⁻¹⁷. Source arrival rates are
0.04305026325 for the loop and 0.05219264208 for basal. At T64 their accepted
work is 6.659681 and 4.252185, and their expected event counts are 13.025696
and 5.551628. The same mean stationary accepted work does not imply equal
offered boundaries, finite work, activity, useful capture or reservoir histories.

Native event energy/bank accounts and the declared paired-rate ratios pass
their stated checks. Material accounting covers apparatus plus a derived
precursor; full packet/waste chemistry is unresolved. No spatial thermal
competitor is represented. The current identical-boundary paired certificate
is inapplicable, without changing the validator. This is a numerical
reproduction and limited physical-accounting audit, not an organization-only,
activity-independent or ethical result (Appendix D, section D.5.1).""",
    )
    add(
        c,
        original,
        replacement,
        "Keep the historical study and the selected replay in one clearly scoped model record.",
    )
    original = paragraph(texts[c], "> **Drafting note (v4.2 r1, 28 October).**")
    add(
        c,
        original,
        original
        + "\n\n> **Evidence update proposed, 28 October 2026.** The drafting note above\n> describes the catalogue before the C.7 replay. One selected C.7 point has\n> since been numerically reproduced; the original twelve-point records remain\n> historical, and the identical-boundary paired certificate is inapplicable\n> to that unequal-source construction. See the updated C.7 entry and Appendix D.",
        "Preserve the historical drafting note and append a dated correction.",
        action="append_dated_note",
    )
    original = paragraph(texts[c], "**Status of this entry.** New in v4.2")
    add(
        c,
        original,
        """**Status of this entry.** New in v4.2, compiled from the reports summarized
in chapters 9 and 11. R1 is the first model on the current platform. Its own
historical profiles were not replayed by the selected C.7 verification. Their
record and comparison-check status must be identified specifically rather than
inferred from a blanket statement about every model. Later R2 engineering
checks use different laws and do not certify this R1 record.""",
        "Do not let C.7 or modern R2 checks silently promote the older R1 record.",
        [EVIDENCE + "/REPORT.md", evidence_paths[6], evidence_paths[7]],
    )
    original = paragraph(
        texts[c], "All records are in the program's code repository under"
    )
    add(
        c,
        original,
        """The original C.1–C.16 records below are retained in the historical
test-bed archive under docs/research_notes/lushness_testbed, with the cited
historical commit and per-case input/source hashes. Their primary records
remain unchanged. The selected C.7 replay is a separate later record on the
current platform, identified below; it does not replace the historical study.
The R1 record still needs its own explicit source identification.""",
        "The later replay is not located in the old study folder or commit.",
    )
    original = paragraph(
        texts[c], "Every record predates the test bed's paired-comparison checks"
    )
    add(
        c,
        original,
        """The original historical records predate the current paired checks.
The later selected C.7 replay verifies numerical reproduction and stated
accounting consistency; its different source boundaries make the current
paired certificate inapplicable. Appendix D records these statuses separately.""",
        "Replace an obsolete blanket statement without rewriting historical records.",
    )
    original = next(
        l for l in texts[c].splitlines() if l.startswith("| C.7 | compounding/")
    )
    add(
        c,
        original,
        original
        + "\n| C.7 selected replay | research/platform/engineering/c7-replay-2026-10-28 | REPORT.md, PROVENANCE.json, QUALITY.json | loop 41a5ce655b87; basal a82acef24f1d; independent replay source in SNAPSHOT.zip |",
        "Add a second source record, not a second model or an extra historical case.",
    )

    d = "D_EVIDENCE_MAP_r1.md"
    original = paragraph(texts[d], "**Verification is a separate field.**")
    add(
        d,
        original,
        """**Verification has separate axes.** A tier describes the resolution
coverage reported, not numerical reproduction, paired certification or physical
faithfulness. Numerical reproduction records which exact source, parameters,
starts and queries have been recomputed. Paired-comparison certification
records whether an applicable executable validator has passed. Physical
accounting and model adequacy retain their own scope statements. None of these
fields stands in for the others.

For C.7, one selected parameter point is numerically reproduced; the original
twelve-point study remains historical. Its different source arrival rates make
the current identical-boundary paired certificate inapplicable. An inapplicable
validator is not a failed calculation or a general verdict against mechanism
comparisons. For preparation contrasts one native law is required; supported
mechanism contrasts can have different generators with matched grammar,
endowment and boundaries. The current checks do not prove a process is enacted
under an encompassing law or that external histories cancel.

Pending fields on other rows remain study-specific. Do not convert an earlier
“awaiting replay” label into an invented pass, failure or universal validation
requirement. The two verification fields in D.3.3 make the C.7 distinction
explicit; other rows are not independently re-audited by this reconciliation.""",
        "Separate numerical and paired statuses and correct the one-law generalization.",
        [*evidence_paths[:6], evidence_paths[-1]],
    )
    original = paragraph(texts[d], "Of the 25 tiered model claims,")
    add(
        d,
        original,
        """The historical tier counts remain 25 model claims: 19 at M1, 3 at M2,
none at M3 and 3 without an archived record (†). These are not counts of
independent replays or paired certificates. The selected C.7 point has now
been numerically reproduced; its paired certificate is inapplicable. This
does not promote all twelve points or alter the tier counts. The two R1 rows
remain unassigned pending their own evidence review.""",
        "Do not count a replay as a new claim or promote historical tiers.",
    )
    table_start = texts[d].index(
        "| Claim | Model | Evidence | Tier | Scope and pending | Verified |",
        texts[d].index("### D.3.3"),
    )
    table_end = texts[d].index("\n\n", table_start)
    original = texts[d][table_start:table_end]
    lines = original.splitlines()
    updated = [
        "| Claim | Model | Evidence | Tier | Scope and pending | Numerical reproduction | Paired-comparison certificate |",
        "|---|---|---|---|---|---|---|",
    ]
    for line in lines[2:]:
        fields = [v.strip() for v in line.strip("|").split("|")]
        if "[C.7," in fields[1]:
            fields[0] = (
                "An enabling-loop law has a higher history-breadth rate than its basal comparator at matched stationary accepted work"
            )
            fields[2] = (
                "Historical study: positive rate contrasts at 12 points and three cadences. Selected capacity-4 middle-target seed pair: all 24 arm profiles reproduce, with +39.425660 bits at T64/cadence 0.25. The original funding range remains historical."
            )
            fields[4] = (
                "Different offered source rates; finite work, activity and external histories unmatched. Only derived apparatus/precursor material accounting; physical faithfulness open."
            )
            fields[5] = (
                "Passed for the selected point only; remaining 11 points not replayed in this pass"
            )
            fields.append("Inapplicable: unequal source boundary prescriptions")
        else:
            fields[5] = "Not reviewed by this reconciliation; historical replay pending"
            fields.append("Not assessed by this reconciliation")
        updated.append("| " + " | ".join(fields) + " |")
    add(
        d,
        original,
        "\n".join(updated),
        "Supply two distinct status columns without inventing verification of neighboring rows.",
    )
    original = paragraph(texts[d], "A claim that something can happen is not refuted")
    add(
        d,
        original,
        """A claim that something can happen is not refuted by one case where it does
not. A claim that something always happens within a domain is refuted by one
sound counterexample inside that domain. The numerical checks and the physical
comparison must support the claim being tested. The executable paired validator
certifies only comparisons within its supported contract; another kind of
contrast requires its own explicit warrants. C.7's numerical replay does not
establish physical faithfulness or an ethical counterexample. Record these
questions separately and apply the same evidential requirements to favorable
and contrary results.""",
        "A specific validator must not become an automatic gate that exempts unsupported contrast types from scrutiny.",
        [EVIDENCE + "/QUALITY.json", evidence_paths[-1]],
    )
    original = bullet(texts[d], "- **Replays under the paired validator.**")
    add(
        d,
        original,
        """- **A single combined verification verdict.** The selected C.7 point has
  a completed numerical replay and an inapplicable identical-boundary paired
  certificate. Separately, later R2 construction/transduction engineering
  contrasts pass executable paired checks within their limited scope. Those
  are not replays of the historical models catalogued here. Neither result
  establishes physical faithfulness or certifies the ethical thesis.""",
        "Remove the global no-reported-checks claim while preserving the distinct R2 evidence.",
        [EVIDENCE + "/QUALITY.json", evidence_paths[6], evidence_paths[7]],
    )
    original = paragraph(texts[d], "> - **Verification field**")
    add(
        d,
        original,
        original
        + "\n\n> **Evidence update proposed, 28 October 2026.** The original migration note\n> above records the earlier one-field design. D.1 and the C.7 record now\n> separate numerical reproduction, paired certification and physical limits.\n> One selected C.7 point reproduces; its unequal-boundary certificate is\n> inapplicable. Historical tier counts are unchanged.",
        "Keep the drafting history visible rather than rewriting its earlier rule.",
        action="append_dated_note",
    )

    b = "B_METHOD_r1.md"
    original = between(
        texts[b],
        "A comparison between two options is only as good",
        "- **Conservation.**",
    )
    add(
        b,
        original,
        """The executable checks depend on the kind of comparison. A preparation
contrast uses one native law and explicitly different starts. A supported
mechanism contrast can use different generators, while keeping the actual
present, physical grammar, endowment, observation and boundaries matched.
A process contrast additionally needs its action to be physically enacted
within an encompassing law; passing the validator does not prove that enactment.
- **Actual arms and presents.** Each arm must execute its declared compiled
  law. The validator checks actual roots, conditioning, energy/material
  endowments, observation and comparison windows. It checks a common present
  for process/mechanism contrasts and one law for preparation contrasts.
  Its current matched-boundary contract does not cover C.7's intentionally
  different source arrival rates; matching stationary work is a separate audit.""",
        "The implementation accepts distinct native generators for mechanism contrasts; it does not require identical starts for preparations.",
        [evidence_paths[-1], evidence_paths[7], EVIDENCE + "/PROVENANCE.json"],
    )
    original = bullet(texts[b], "- **They do not re-certify earlier results.**")
    add(
        b,
        original,
        """- **They do not automatically re-certify earlier results.** The selected
  C.7 point has a separate numerical replay and accounting audit; its unequal
  source boundaries leave the current paired certificate inapplicable.
  Other historical results retain their own pending checks. Newer R2
  engineering contrasts pass executable paired checks for their stated
  grammar and boundaries, without recertifying historical studies or proving
  physical faithfulness. Appendix D records the different questions separately.""",
        "Distinguish completed reproduction from applicable current checks.",
        [EVIDENCE + "/QUALITY.json", evidence_paths[7]],
    )

    overview = "00_OMEGA_COSMOLOGY_r3.md"
    original = between(
        texts[overview],
        "> - **Model evidence:**",
        "### Deciding without the whole view",
    )
    add(
        overview,
        original,
        """> - **Model evidence:** historical studies retain their limits. One
>   selected matched-stationary-work comparison (C.7) has been numerically
>   reproduced from verified frozen source. Its unequal source boundaries
>   leave the current paired certificate inapplicable. Separate newer
>   engineering contrasts pass executable paired checks within their stated
>   scope. Appendix D separates reproduction, pairing and physical adequacy.
>   These findings support continuing the program; they do not decide the thesis.""",
        "Replace the global pre-checks claim without inflating the replay's scope.",
        [EVIDENCE + "/QUALITY.json", evidence_paths[7]],
    )
    original = paragraph(texts[overview], "Evidence comes in three kinds,")
    add(
        overview,
        original,
        """Evidence comes in three kinds, which are distinct and not a ladder: that a
relation can be represented in Omega's terms; that the measure distinguishes
the relevant alternatives; and that a specified physical model exhibits a
particular effect. None establishes the others, and the text says which kind
each claim is. Numerical reproduction, executable pairing checks and physical
adequacy are recorded separately in Appendix D. The completed replay of one
C.7 point does not recertify the original twelve-point study.""",
        "The blanket statement is obsolete once the later replay is included.",
    )
    original = next(
        l
        for l in texts[overview].splitlines()
        if l.startswith("| **M** | the model results of section 0.6")
    )
    add(
        overview,
        original,
        "| **M** | the model results of section 0.6, each within its scope; numerical reproduction, paired certification and physical limits recorded separately in Appendix D |",
        "Update the status summary with no new tier or claim count.",
    )

    eleven = "11_PERSISTENCE_AND_COMPOUNDING_r3.md"
    original = between(
        texts[eleven], "- **Matched accepted work**", "- **Three links**"
    )
    add(
        eleven,
        original,
        """- **Matched stationary accepted work** ([model C.7](#c-matched-work)).
  The historical twelve-point study reports a higher enabling-loop rate at
  every tested cadence after calibrating stationary accepted work. One
  capacity-4 middle-target point has now been numerically reproduced from
  frozen source. Source arrival rates differ; finite work and activity are
  unmatched. This supports a mechanism demonstration within those laws,
  not an organization-only surplus or an activity-matched result.""",
        "Retain the historical finding and identify the independently reproduced subset.",
    )
    original = next(
        l
        for l in texts[eleven].splitlines()
        if l.startswith("| **M** |") and "[model C.7]" in l
    )
    add(
        eleven,
        original,
        original.replace(
            "[model C.7](#c-matched-work): higher rate at matched accepted work (11.7)",
            "[model C.7](#c-matched-work): historical higher-rate contrasts at matched stationary accepted work; one selected point numerically reproduced (11.7)",
        ),
        "Keep the chapter's status summary aligned with its qualified evidence paragraph.",
    )

    eighteen = "18_THE_HARDEST_TESTS_r4.md"
    original = between(
        texts[eighteen],
        "- **Organization raises the rate, at every level tested (M1).**",
        "- **Activity was not matched.**",
    )
    add(
        eighteen,
        original,
        """- **Historical enabling-loop rate contrasts are positive at the levels
  tested.** C.7 reports positive contrasts at twelve work targets/capacities,
  matching stationary accepted work rather than finite work or source rates.
  One selected point has now been numerically reproduced. Its historical
  M1 label describes provisional resolution coverage, not a paired or
  physical-faithfulness certificate.""",
        "Avoid treating the twelve-point historical grid as independently replayed.",
    )
    original = "- **The activity-matched comparison is not built (M4).**"
    add(
        eighteen,
        original,
        """- **A qualified activity/work-matched comparison remains open.**
  Engineering candidates have been constructed, but the selected jointly
  matched load returned net bank energy and was stopped before history
  scoring. It did not instantiate the intended net-consuming control.
  The requested scientific comparison is still unestablished.""",
        "An attempted control is not a completed scientific result; preserve its actual qualification boundary.",
        [evidence_paths[8], evidence_paths[9]],
    )

    h = "H_PROVENANCE_r1.md"
    original = paragraph(texts[h], "**All recorded model results come from")
    add(
        h,
        original,
        """**Historical model records and later verification records have separate
provenance.** The historical studies predate the current checks. One selected
C.7 point has a later numerical replay; its original source and results remain
unchanged. Newer engineering records do not silently recertify older models.""",
        "Preserve original provenance and add the later evidence layer.",
    )
    original = between(texts[h], "- **The paired validator.**", "- **The numbers.**")
    add(
        h,
        original,
        """- **The later verification records.** The selected C.7 replay checks
  original source provenance, numerical reproduction and stated physical
  accounts. Its unequal source boundaries make the current paired
  certificate inapplicable. Separate R2 construction/transduction engineering
  contrasts pass the executable matched-boundary checks for their own
  grammar and endowment. They do not constitute historical C.7 or R1 replays.
  Appendix D records numerical reproduction, pairing and physical limits
  separately; none is a certificate of the ethical thesis.""",
        "Correct the one-law/no-later-results generalization.",
        [EVIDENCE + "/PROVENANCE.json", evidence_paths[7]],
    )

    objections = "E_OBJECTIONS_r1.md"
    original = next(
        l
        for l in texts[objections].splitlines()
        if l.startswith("| The model results were not validated.")
    )
    add(
        objections,
        original,
        "| The model results were not validated. | The evidence has distinct checks. One selected C.7 point is numerically reproduced from verified source, with stated accounting checks; its unequal source boundaries leave the paired certificate inapplicable. Other historical studies retain their own pending checks. Separate R2 engineering contrasts pass executable paired checks without certifying physical faithfulness. | 19.3; [Appendix B, section B.10](#appendix-b); Appendix D | Qualified by the evidence record |",
        "Replace a blanket concession with the actual separate statuses.",
        [EVIDENCE + "/QUALITY.json", evidence_paths[7]],
    )

    migration = "V42_MIGRATION_LOG.md"
    original = paragraph(texts[migration], "- **Codex repairs.**")
    add(
        migration,
        original,
        original
        + "\n\n**Proposed evidence reconciliation, 28 October 2026.** The instruction above\nrecords the earlier one-field policy; keep it as history. Supersede its active\nuse with separate numerical-reproduction, paired-certificate and physical-scope\nfields. One selected C.7 point now reproduces; its unequal-source paired\ncertificate is inapplicable. Later R2 engineering checks are separate evidence.\nNo other historical model is promoted by this reconciliation.",
        "Append a dated supersession; do not rewrite migration history.",
        action="append_dated_note",
    )
    original = paragraph(
        texts[d],
        "The results drawn from models here await replay under the paired validator,",
    )
    add(
        d,
        original,
        """The historical model results in this section were not replayed by the
selected C.7 verification. Their numerical and physical-comparison checks
remain study-specific and pending as described in D.1; no global certificate
or new verdict is inferred here.""",
        "Keep other pressure results pending without prescribing an inapplicable validator to every comparison kind.",
    )

    # Dry application only in ignored working storage. Canonical files remain
    # untouched; nonunique, overlapping or stale anchors stop the build.
    dry = sources / "proposed"
    if dry.exists():
        raise FileExistsError("Fresh proposal dry-run directory required")
    dry.mkdir()
    dry_status = []
    for name in sorted({c["file"] for c in changes}):
        proposal = texts[name]
        edits = [c for c in changes if c["file"] == name]
        for change in edits:
            if proposal.count(change["original"]) != 1:
                raise ValueError("Overlapping or stale proposal: " + change["id"])
            proposal = proposal.replace(change["original"], change["replacement"], 1)
        (dry / name).write_text(proposal, encoding="utf-8")
        dry_status.append(
            {
                "file": name,
                "unique_anchors": len(edits),
                "proposed_sha256": sha256(proposal.encode()).hexdigest(),
            }
        )
    if any(digest(sources / name) != before_hashes[name] for name in texts):
        raise ValueError("Source preservation failed")

    patterns = {
        "c7_or_stationary_work": r"C\.7\b|c-matched-work|matched accepted work|matched stationary|matched[- ]work|stationary accepted",
        "replay_pairing_status": r"paired[- ]comparison|paired validator|re-certif|await.{0,20}replay|replayed under|None has.{0,30}replay",
    }
    review = []
    for name, text in texts.items():
        lines, section = text.splitlines(), "opening"
        for number, line in enumerate(lines, 1):
            if line.startswith("#"):
                section = line
            hits = [k for k, v in patterns.items() if re.search(v, line, re.IGNORECASE)]
            if not hits:
                continue
            related = [
                c["id"]
                for c in changes
                if c["file"] == name
                and c["line"] <= number <= c["line"] + c["original"].count("\n")
            ]
            review.append(
                {
                    "file": name,
                    "line": number,
                    "section": section,
                    "text": line,
                    "patterns": hits,
                    "proposed_edits": related,
                    "disposition": "proposed_update"
                    if related
                    else "reviewed_no_direct_change",
                    "reason": "Covered by exact replacement"
                    if related
                    else "Historical figure, unrelated formal result, pending other-model status or context note; no new verification inferred",
                }
            )
    out.mkdir(parents=True)
    write(
        out / "SOURCE_INVENTORY.json",
        {
            "active_working_files": 32,
            "context_notes": 4,
            "sources": sorted(inventories, key=lambda x: x["file"]),
            "coverage": "Active v4.2 working-folder Markdown and four context notes; not deprecated revisions or the duplicate ZIP",
            "authority": "Observed working versions, not blanket author approval or a repository canonical-reference migration",
            "private_locator_policy": "Raw source IDs, URLs and original fetched texts stay in ignored working storage",
        },
    )
    write(
        out / "PROPOSED_REPLACEMENTS.json",
        {"schema": "omega.editorial-reconciliation/1", "changes": changes},
    )
    write(
        out / "PASSAGE_REVIEW.json",
        {
            "patterns": patterns,
            "passages": review,
            "scope": "Every literal search hit in all 36 inspected texts reviewed; theoretical claims are not re-audited by this source search",
        },
    )
    facts = {
        "C7": {
            "original_parameter_points": 12,
            "replayed_parameter_points": 1,
            "replayed_arm_profiles": 24,
            "paired_window_comparisons": 12,
            "numerical_reproduction": "passed_selected_point",
            "paired_certificate": "inapplicable_unequal_boundaries",
            "physical_scope": quality["physical_adequacy"],
            "resolution": quality["resolution"],
        },
        "R2_construction_transduction": {
            "paired_certificate": "passed_for_stated_engineering_mechanism_contrasts",
            "enabling_link_paired_contracts": len(links),
            "historical_replication": False,
            "physical_faithfulness": "open",
            "matched_net_consuming_control": "not_established",
        },
    }
    write(out / "VERIFICATION_AXES.json", facts)
    write(
        out / "VALIDATION.json",
        {
            "status": "passed",
            "new_experiments": 0,
            "substrate_changes": 0,
            "canonical_manuscript_changes": 0,
            "inspected_sources_unchanged": True,
            "active_metadata_byte_sizes_agree": True,
            "unique_replacement_anchors": len(changes),
            "dry_application": dry_status,
            "evidence": [
                {"path": p, "sha256": digest(ROOT / p)} for p in evidence_paths
            ],
        },
    )
    note = f"""# v4.2 evidence reconciliation — proposed replacements r1

28 October 2026. Local editorial handoff. No experiments, substrate changes,
canonical manuscript edits, commit, push or upload. The source files and retained
scientific evidence are unchanged. This note proposes {len(changes)} exact edits;
it does not apply them.

## Finding and coverage

The active v4.2 working folder was read directly: all 32 Markdown files, including
Chapter 19 r4 and Appendices C/D r1, plus outline r2, migration log, style sheet r5
and its history. Retrieved active texts agree with all listed byte sizes.
The outline calls this a working baseline; no higher revision number is treated
as independent author approval. The older repository v4.1 files are not silently
substituted for these working texts. Deprecated revisions and the duplicate
working ZIP were excluded. The source search is complete for this inspected
working set, not for inaccessible drafts or later revisions, and it is not a
formal-core proof audit.

The historical claim of twelve positive C.7 parameter points is retained. No
active sentence explicitly says that all twelve have been independently
replayed. The corrections address shorthand matching claims, blanket
pre-validator/pending-replay statements and the conflation of reproduction with
paired certification. Exact old wording and proposed replacements follow.

## Evidence to carry forward

| Quantity or status | Original C.7 study | Representative replay |
|---|---|---|
| Parameter points | 12 historical points | 1: capacity 4, middle target, seed [6,1,1] |
| Queries | Original study remains on record | 24 arm profiles, 12 paired windows; T16/64/256/1024 and cadence 0.125/0.25/0.5 |
| Numerical reproduction | Not globally rechecked here | Exact agreement with retained profiles; independent discrepancy ≤5.61e-10 bits |
| Stationary accepted work | Matched in the original protocol | About 0.07814421443 in each arm; mismatch1.4e-17 |
| Current identical-boundary paired certificate | Not inherited | Inapplicable: different source arrival rates |
| Material/physical qualification | Must retain original limits | Event energy/bank accounts and native paired-rate ratios checked; only apparatus plus derived precursor inventory; full chemistry and physical faithfulness open |

At T64/cadence 0.25, loop minus basal is +39.425660 bits. The excess stationary
rates are +0.110125/+0.095049/+0.080271 at the three cadences. These are a
demonstration within specified laws, not a universal ranking or an ethical test.

Separate R2 construction/transduction evidence already contains {len(links)}
passing paired records for the enabling-link mechanism contrasts. Its actual
grammar, common present and endowment are checked. It is not a C.7 replay,
and its control candidates are not thereby qualified. Do not erase those checks
with a statement that no current-platform pair has been validated.

## Why stationary matching is limited

Equal stationary accepted work matches one long-run mean. It does not match
when energy arrives, how long it is stored, the probability of an empty bank,
rejection/decay, useful capture, work accumulated before a deadline or the
reservoirs' histories. The offered source rates themselves differ. At T64,
accepted work is 6.659681 versus 4.252185 and expected event count 13.025696
versus 5.551628. Initial endowments agree, while the boundary prescriptions and
finite resource availability differ. Those relationships remain part of the
comparison; they cannot be cancelled by matching a stationary average.

The latest R2 bank-load fit matches both finite moments but returns net bank
energy (payment −0.0483251), so it stops before history scoring. Some previous
candidate scores exist with work mismatches; they remain evidence of their own
laws. No qualified net-consuming work/activity comparator was established.

## Exact proposed replacements

Apply only after editorial review, to the source hash named in each record.
Every anchor was found uniquely and dry-applied to ignored copies. No original
manuscript was overwritten. Historical drafting notes and the migration log
receive dated additions rather than retrospective rewrites. Table counts and
unrelated model results are not promoted. Internal book anchors in the quoted
prose belong to the manuscript, not to this standalone handoff.
"""
    for c in changes:
        note += f"\n### {c['id']} — {c['file']}\n\nLocation: {c['section']}, line {c['line']}.\n\nReason: {c['reason']}\n\n**Current passage**\n\n```markdown\n{c['original']}\n```\n\n**Proposed replacement**\n\n```markdown\n{c['replacement']}\n```\n"
    note += """
## What stays unchanged or unresolved

- The original twelve-point results and their raw records stay historical.
- The replay neither adds a model claim to the tier counts nor derives a
  faithful physical resolution. Historical M1 labels are not new certificates.
- Other old models, the R1 entry and its pending source identification are not
  recertified. This package does not repair every older appendix omission.
- The D.3.3 proposal supplies separate status columns. Other historical table
  rows need study-specific migration if the two-column layout is propagated;
  a generic “awaiting replay” cell must never be converted into a fabricated
  pass or failure. Retain their old source status until then.
- No universal proof of conservation, complete thermal baseline, ethical
  correspondence or enactment of an intervention follows from these checks.

The manuscript may cite the selected replay once its local evidence package is
available to readers. It has not been pushed by this reconciliation. Use the
primary report and its source/quality records; do not invent a publication link
or imply external independent replication by another research group.

## Deferred experiments — none launched

1. A physically qualified paid work/activity comparator, after energy-flow
   review; no further search for a favorable sign is implied.
2. Equal-lushness compression pairs, with structural/analytic support beyond
   a finite numerical tie.
3. Stasis–chaos operating ranges and broader autocatalytic catalogues.
4. Populations, spatial ecology and confinement comparisons.
5. Paid information, uncertain agents and other expanded controller studies.

These remain research questions, not new prerequisites imposed here on v4.2.
Book One's central philosophical claim is not certified by this reconciliation.

## Machine-readable handoff

[Source inventory](SOURCE_INVENTORY.json), [replacement records](PROPOSED_REPLACEMENTS.json),
[complete literal-hit review](PASSAGE_REVIEW.json), [separate verification axes](VERIFICATION_AXES.json)
and [validation](VALIDATION.json) accompany this note. Source IDs, links and raw
manuscript copies stay in ignored working storage; public records contain file
names, hashes and evidence paths only. No canonical draft has been edited.
"""
    (out / "EVIDENCE_RECONCILIATION_V42_r1.md").write_text(note, encoding="utf-8")
    analysis = out / "analysis"
    analysis.mkdir()
    target = analysis / Path(__file__).name
    target.write_bytes(Path(__file__).read_bytes())
    files = [
        {
            "path": p.relative_to(out).as_posix(),
            "sha256": digest(p),
            "bytes": p.stat().st_size,
        }
        for p in sorted(out.rglob("*"))
        if p.is_file()
    ]
    write(
        out / "EVIDENCE.json", {"schema": "omega.retained-evidence/1", "files": files}
    )
    print(
        json.dumps(
            {
                "status": "proposals_built",
                "active_sources": 32,
                "context_notes": 4,
                "proposed_edits": len(changes),
                "affected_files": len(dry_status),
                "reviewed_literal_hits": len(review),
                "new_experiments": 0,
            }
        )
    )


if __name__ == "__main__":
    main()
