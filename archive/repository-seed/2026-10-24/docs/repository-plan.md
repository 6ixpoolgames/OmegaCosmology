# Repository organization and first milestone

**Working repository name:** `omega-cosmology`.  
**Prepared:** 16 September 2026.  
**Scope:** the cosmology, Gradient Ethics and supporting research. The current
continuation probes are one part of that program.

## Concrete layout

```text
omega-cosmology/
  README.md                    reading entry point and reproduction command
  AGENTS.md                    current research operating instructions
  NOTICE.md                    attribution and licensing status
  pyproject.toml               minimal Python package; no runtime dependencies
  manuscript/                  editable numbered cosmology chapters
  docs/
    current-position.md        later corrections and present claim boundaries
    provenance.md              where sources and results came from
    repository-plan.md         this organization and launch plan
  sources/
    manifest.json              inventory of immutable imported evidence
    v2_packet/                 untouched v2 originals
    quantum_continuation/      formal note, exact verifier and archived results
    gradient_ethics/           inherited foundation draft
    legacy_repo/               selected prior reports, not the old codebase
    handoff/                   selected conceptual/formal handoff documents
  research/
    ROADMAP.md
    claims.json                new local claims and evidence paths
    tasks/                     bounded, reviewable task specifications
    baseline/                  inherited reproduction evidence
    probes/P001/
      spec.md
      fixture.json
      report.md
      evidence/                retained exact objects, expectations and provenance
  src/omega_cosmology/          reusable code with model scope stated
  tests/                       meaningful checks for formal/implementation risks
  scripts/                     reproduction and integrity commands
  .github/                     automated checks and research contribution templates
  runs/                        ignored generated outputs
  .local/                      ignored complete handoff and private context
```

## Editing and evidence conventions

The current-position document controls how the inherited prose is read. The
numbered manuscript will be reconciled explicitly before a revised edition
is declared. The frozen sources allow that editorial work to be compared with
what was actually inherited.

Each probe keeps its assumptions, fixture, report, and retained evidence
together. Reusable code belongs in `src/`; a probe-specific result does not
automatically become a universal API. Generated runs remain outside Git until
an intentionally selected result is promoted into a probe's evidence directory.

Keep source snapshots unchanged. The source manifest records their original
paths and hashes. New executable results record the current code hashes.
The claim ledger distinguishes finite computation, ordinary proof,
counterexample, conjecture and unresolved questions.

The private handoff remains usable for local continuity, while the checked-in
current position and specifications are sufficient to interpret the technical
results. Raw conversational files are not part of the proposed Git contents.

## GitHub launch

The local preparation has a dedicated Git root and a `codex/` preparation
branch. The proposed default branch on GitHub is `main`; no remote or release
is assumed by this document. Choose repository name/visibility before creation.
Licensing remains a distinct decision for code, prose and imported material.

The first GitHub issue can use the already prepared
[task 001](../research/tasks/001-continuation-contract.md). Its proposed scope
is concrete enough to review before any further probe is launched.

The workflow runs the same standard-library checks used locally. Its action
syntax follows the official [checkout](https://github.com/actions/checkout)
and [setup-python](https://github.com/actions/setup-python) documentation checked
on 16 September 2026. GitHub-hosted execution remains unverified until a remote
exists and the workflow has run.
