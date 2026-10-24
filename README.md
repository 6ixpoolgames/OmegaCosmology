# Omega Cosmology

Omega studies physical continuation: how organization, access, composition and
control change what can follow from a present. Gradient Ethics investigates the
proposed correspondence between the continuation substrate and prospective value.

**Canonical starting reference: v4.1**, selected by Paolo on 24 October 2026.
The rewrite is incomplete. Imported chapters retain their original revision
names and editorial status; this repository does not silently approve proposals
or declare the manuscript finished.

## Start here

1. [Current position](docs/current-position.md): governing definitions and scope.
2. [v4.1 source reference](sources/v4.1/README.md) and [working manuscript](manuscript/README.md).
3. [Platform design](research/platform/README.md): architecture and the M0–M2 handoff.
4. [Formal work](formal/README.md): definitions, source mapping and verification status.
5. [Historical archive](archive/README.md): all inventoried Drive versions/deprecated files.

## Repository structure

| Directory | Purpose |
|---|---|
| `docs/` | Current guidance, architecture decisions and contributor workflow |
| `manuscript/v4.1/` | Editable v4.1 working chapters and appendices |
| `formal/` | Semantic contracts, proposition mappings and verification work |
| `research/platform/` | Shared instrument specifications and engineering evidence |
| `research/studies/` | Future physical studies, with question/configuration/analysis/evidence together |
| `research/probes/` | Retained small investigations, including historical P001 |
| `src/omega_cosmology/` | Reusable implementation; next platform belongs in `testbed/` |
| `tests/` | Formal conformance and implementation tests |
| `scripts/` | Reproduction, integrity, intake and maintenance commands |
| `sources/v4.1/` | Immutable canonical-start reference files and source manifest |
| `sources/` | Other immutable imported reference evidence |
| `archive/` | Indexed historical sources and deprecated designs |
| `runs/` | Ignored generated results and reconstructible caches |
| `.local/` | Ignored private handoff, intake plans and machine-specific context |

See the [forward-looking layout](docs/repository-plan.md) for extension rules.

## Current implementation status

The repository has inherited finite reference tooling and a **reviewed design**
for the new test bed. The new compositional engine is not implemented. The next
engineering task is [M0–M2](research/tasks/002-next-generation-platform.md).
Preparation does not launch that task or a scientific survey.
The [repository preparation report](research/platform/engineering/repository-preparation-2026-10-24/REPORT.md)
records the import scope and completed integrity/reproduction checks.

The previous P001 probe and 233-check finite quantum baseline remain reproducible
historical evidence. They do not validate the new platform or ethical thesis.

## Check the workspace

Use Python 3.10+; preparation checks use the standard library:

```text
python scripts/check_workspace.py --out-dir runs/workspace-check-001
```

Use a fresh output directory. The command checks source/archive bytes, reference
links/layout, focused tests and the inherited exact reproductions. No automatic
publication is implied by a scientific run. The authorized publication destination
is [OmegaCosmology](https://github.com/6ixpoolgames/OmegaCosmology). Its existing
MIT [LICENSE](LICENSE) is retained; imported materials retain their notices.
See [NOTICE](NOTICE.md).
