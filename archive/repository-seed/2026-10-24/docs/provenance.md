# Provenance and migration

The origin is the supplied [Omega Cosmology Drive folder](https://drive.google.com/drive/folders/1IPgWdTOB2AECVuDBYzTPXm-r-VPjAimZ),
its [v2 directory](https://drive.google.com/drive/folders/1M6KiTcC8hKy-FFNj4nbcG1zSGuA7eZY3),
and the [15 September local research handoff](https://drive.google.com/drive/folders/1yzEd04tIFJXKFisRqQi6VrXEYPzKCqry).

The full local handoff passed its 66-file inventory check. This repository
imports 25 selected source files unchanged, inventoried in
`sources/manifest.json`. The complete handoff remains locally under `.local/`
and is not needed for the standalone technical checks.

The working manuscript starts as ten copies of the original v2 chapters.
The [current position](current-position.md) carries the later corrections.
Neither those copies nor the inherited combined packet is being relabeled as
a completed new edition.

The local P001 result was migrated from the initial `omega-lushness` seed.
Its mathematical core and fixture are unchanged. The Python package was renamed
to reflect the whole cosmology, and the fixture, specification and report were
grouped under one probe directory. Imports, links and reproduction instructions
were adapted to those locations.

P001's retained complete object is byte-for-byte unchanged. Its expected
scientific summary omits the old location-dependent hash keys and interpreter
version. New runs record current input hashes and must reproduce the retained
objects and the remaining summary exactly. Original output and core hashes
are recorded in [P001 provenance](../research/probes/P001/evidence/PROVENANCE.json).

The earlier local projects remain intact. The selected legacy reports describe
prior results; their entire code and proof dependencies were not migrated or
rerun. For detailed source attribution see the unchanged
[handoff source map](../sources/handoff/06_PROVENANCE_AND_SOURCE_MAP.md) and
[v2 bibliography](../sources/v2_packet/09_REFERENCES_AND_PROVENANCE.md).

Relative links inside frozen historical reports may target material outside
this selected snapshot. Their source context is preserved, rather than
rewritten to imply that the missing dependency trees are present.
