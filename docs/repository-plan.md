# Repository layout and extension policy

Prepared 24 October 2026. v4.1 is the canonical starting reference family.

```text
omega-cosmology/
  README.md, AGENTS.md, NOTICE.md
  docs/                       current position, workflow and decisions
    decisions/                short records for consequential architecture choices
  manuscript/v4.1/
    chapters/                 editable imported drafts, original revision names
    appendices/               editable manuscript appendices
  formal/
    contracts/                executable semantic contract specifications
    verification/             proposition-to-proof/example/test mapping
  research/
    platform/specs/           active architecture and implementer handoff
    studies/                  future experiments grouped by research question
    probes/                   small retained investigations
    tasks/                    bounded implementation/scientific tasks
    claims.json               claim status and evidence pointers
  src/omega_cosmology/
    testbed/                  next-generation engine home; not implemented yet
  tests/                      conformance, physics, backend and workflow checks
  scripts/                    reproducible entry points and integrity tooling
  sources/v4.1/               immutable canonical-start reference snapshot
  archive/
    drive/2026-10-24/          full inventoried Drive collection and manifest
    legacy-testbed/           selected unchanged reviewed designs/evidence
    repository-seed/          prior local v2-era layout and drafts
  runs/                       generated outputs and caches; ignored
  .local/                     private intake/session state; ignored
```

## Placement rules

Definitions and proof obligations live in formal/; narrative explanation lives
in manuscript/; experiments carry their question, model, configuration, analysis
and compact evidence together under research/studies/<stable-id>/.
Use stable semantic/claim IDs so chapter renumbering does not break evidence links.

Reusable numerical/physical code belongs under src/, never inside a report.
The reviewed testbed subpackages are semantics, physics, backends, queries,
analysis and workflow. Create them as they become implemented, with capability
contracts; do not populate empty APIs that imply unsupported functionality.

Future population, transport, spatial contact, cross-scale composition and
controller work should extend physical rules/query capabilities in that package.
A new family of physics can use a separate adapter. It should not create an
independent entropy definition, report schema or artifact-lifecycle convention.

Large trajectories, sampled kernels and rebuildable dumps stay in runs/.
Promote only compact evidence with manifests, source/config hashes, uncertainty
and reconstruction instructions. Disk caching aids reuse, not memory complexity.
No scheduled cleanup is enabled. Eviction is manifest-scoped, logged and skips
pinned or referenced evidence.

## Current reference versus history

sources/v4.1 is a byte-preserving reference snapshot. manuscript/v4.1 contains
working copies which may later change explicitly. archive/drive preserves the
broader source history and native-document exports, organized by its index.
Do not auto-promote the highest revision number or reactivate old instructions.

The two old local repositories remain intact. Selected utility imports will
record original hashes and scope; old experiments can be reproduced exactly or
replicated in the new substrate, with the relationship labelled.

## Publication

Preparation is local only; no remote or commit is configured by this task.
The archive contains historical contextual documents as well as manuscripts.
Keep download references and private handoff ignored. A future publication,
visibility choice and licensing decision need their actual user authorization.
