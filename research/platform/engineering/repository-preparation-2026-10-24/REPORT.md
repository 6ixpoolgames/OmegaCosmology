# Repository preparation — 24 October 2026

Status: complete, local only. No commits, remote creation, publication or new
test-bed engine implementation. Current branch: codex/repository-preparation.

## Changes

Paolo selected v4.1 as the canonical starting reference and requested all old
versions/deprecated Drive files as repository context. Imported 377 files from
25 folders in the inventoried Omega Cosmology and Project OMEGA trees. The
archive contains 16,519,754 bytes (about15.75MiB). Stored files preserve original
bytes; 44 native Google Docs are DOCX exports. No Drive files were changed.

Twenty files form the immutable v4.1 reference snapshot, with 15 initial working
chapter/appendix copies. Source filenames and editorial status are retained.
Foundations r4 governs updated frame wording; available formal source is r19.
Discussed r20 was not found. Outline r25 says it remains proposed and r22 stays
canonical; selecting the v4.1 family does not silently approve that proposal.

Archived the prior local entry points, v2 working chapters and initial drafts
before updating the repository. Imported 12 reviewed design/evidence files from
the old Omega checkout, with original hashes. Three active specs adapt links and
the package home to src/omega_cosmology/testbed/. The original checkout is intact.

Current docs separate manuscript, formal contracts/verification, shared platform,
scientific studies, immutable references, history and generated outputs. Generated
data and signed transfer plans remain ignored. Archive/source bytes are exempt
from Git line-ending normalization.

## Verification

Command:

```text
python scripts/check_workspace.py --out-dir runs/repository-preparation-2026-10-24
```

All six stages passed: inherited source integrity, new archive/reference
integrity, active layout/links, unit tests, inherited finite quantum baseline
and P001 reproduction. P001 complete objects and scientific summary reproduce;
current input hashes verify. See the retained CHECKS.json and compact
verification outputs in this directory. Full generated execution output stays
in ignored runs/ and can be reconstructed.

Archive checks cover 377 Drive files, 12 imported legacy design/evidence files,
24 prior local seed files and 20 v4.1 reference files. Every downloaded file is
present with the expected hash; all native exports contain DOCX structures.
The active-document checker validates 49 local links. The archive index separately
links every payload and retains source IDs/paths for duplicate-title handling.

This is a snapshot of accessible, separately named files and revisions. It is
not a reconstruction of every native file's internal edit history. Completeness
claims refer to the inventoried trees at intake time. Historical source prose
can link outside its preserved context and is not rewritten to imply otherwise.

## Next work

Task002 is ready: M0–M2 contracts, shared rule kernel and formal reference queries.
Repository preparation did not start that sprint or any scientific survey.
Future source imports update references explicitly; future working manuscript
edits leave this starting snapshot unchanged.
