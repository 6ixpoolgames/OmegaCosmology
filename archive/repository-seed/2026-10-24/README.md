# Omega Cosmology

Omega investigates reality as completed structure encountered through situated
perspectives, and the conditions under which value-capable continuation can
arise within that structure. Gradient Ethics is its investigation of agency,
consequence, and the proposed substrate of value.

This is the working repository for the updated program. It brings together
the v2 manuscript, its later corrections, finite formal work, and reproducible
research probes. Lushness remains an open hypothesis. A successful finite
calculation does not establish the cosmology or an ethical ordering.

## Start reading

1. [Current position](docs/current-position.md): what is committed, established,
   conjectural, or superseded.
2. [Manuscript guide](manuscript/README.md): the ten v2 chapters and where they
   still need reconciliation with later corrections.
3. [Research roadmap](research/ROADMAP.md): what the evidence supports next.
4. [First proposed task](research/tasks/001-continuation-contract.md): make the
   existing finite continuation object a shared contract for further probes.

## Repository map

| Location | Role |
| --- | --- |
| `manuscript/` | Editable exposition, beginning from the v2 chapters |
| `docs/` | Current interpretation, reading route, provenance and project organization |
| `sources/` | Selected unchanged source snapshots with a checksum inventory |
| `research/` | Claim ledger, task specifications, probes and retained evidence |
| `src/omega_cosmology/` | Reusable implementations, with their modeled scope stated |
| `tests/` | Checks for concrete mathematical and implementation risks |
| `scripts/` | Source verification and reproducible experiment entry points |
| `runs/` | Generated local outputs, excluded from version control |
| `.local/` | Local handoff and private conversational context, excluded from version control |

The detailed [repository plan](docs/repository-plan.md) explains the boundaries.

## Reproduce the starting evidence

Use Python 3.10 or newer. The checks require only the standard library; installing
the package is optional.

```text
python scripts/check_workspace.py --out-dir runs/first-check
```

Choose a new output directory for each run. This verifies the imported source
bytes, runs the focused tests, reproduces the inherited 233-check quantum
baseline, and compares P001's complete objects and scientific summary with
retained evidence. Detailed output and current input hashes stay in the run.

P001 establishes a limited counterexample: the weighted distance geometry of
one boundary family can hide different later feedback responses. Later-stage
support sizes differ in that example. See its [report](research/probes/P001/report.md)
before using it to motivate a broader claim.

## Status and provenance

The manuscript begins as v2, dated 15 September 2026. Later corrections are
explicit in the current-position document; a revised manuscript edition has
not yet been declared. The tooling version is independent of manuscript editions.

S. Poole originated the research program. AI systems contributed drafting,
formal translation, and implementation under that direction. Borrowed
mathematics and prior results retain their attribution. See
[provenance](docs/provenance.md) and [notices](NOTICE.md).
