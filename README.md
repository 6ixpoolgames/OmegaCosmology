# Omega Cosmology

Official attribution: **S. Poole**. See [privacy and source sanitization](docs/privacy.md).

Omega studies physical continuation: how organization, access, composition and
control change what can follow from a present. Gradient Ethics investigates the
proposed correspondence between the continuation substrate and prospective value.

**Canonical starting reference: v4.1**, selected by the author on 24 October 2026.
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

The first finite classical [M0–M2 engineering slice](research/tasks/002-next-generation-platform.md)
is implemented locally: one rule kernel, two numerical backends, explicit
continuation queries and physical/formal reference checks. The
[engineering report](research/platform/engineering/m0-m2-2026-10-24/ENGINEERING_REPORT.md)
records the capped calibration and limits. The
[first R1 batch](research/studies/R1-constructed-access/README.md) now evaluates
costed access and reconstruction with matched preparations and explicit
mechanism/source controls. The
[R2 batch](research/studies/R2-further-capacity/README.md) tests useful further
capacity against costed construction churn, including actual repair/rebinding
readouts. No broad ecology survey or ethical result is claimed.
The [analysis repair for interacting ecologies](research/platform/specs/ECOLOGY_ANALYSIS_SPEC_r1.md)
adds functional persistence/return, native-route audits and bounded assistance
ancestry. R2's [corrected interpretation](research/studies/R2-further-capacity/INTERPRETATION_r2.md)
records the physical limitations without changing its original scores.
The [coupled engineering slice](research/platform/engineering/coupled-slice-2026-10-25/REPORT.md)
exercises repaired storage/damage, costed construction ancestry, shared-resource
cycles and local projected-history bounds. All five capped smoke cases passed.
The first [E1 coupled-autocatalysis map](research/studies/E1-coupled-autocatalysis/README.md)
has completed locally:650 profiles, matched preparations and
cost/source/turnover factors, with separate local and whole-model readouts.
The [repository preparation report](research/platform/engineering/repository-preparation-2026-10-24/REPORT.md)
records the import scope and completed integrity/reproduction checks.

The previous P001 probe and 233-check finite quantum baseline remain reproducible
historical evidence. They do not validate the new platform or ethical thesis.

## Check the workspace

Use Python 3.10+ and install the small numerical extra for the complete checks:

```text
python -m pip install -e ".[testbed]"
python scripts/check_workspace.py --out-dir runs/workspace-check-001
```

For the source-frozen Windows capped engineering calibration:

```text
python scripts/run_testbed_calibration.py --out-dir runs/calibration-001
```

Use a fresh output directory. Workspace checks cover source/archive bytes, reference
links/layout, focused tests and the inherited exact reproductions. No automatic
publication is implied by a scientific run. The authorized publication destination
is [OmegaCosmology](repository://OmegaCosmology). Its existing
MIT [LICENSE](LICENSE) is retained; imported materials retain their notices.
See [NOTICE](NOTICE.md).
