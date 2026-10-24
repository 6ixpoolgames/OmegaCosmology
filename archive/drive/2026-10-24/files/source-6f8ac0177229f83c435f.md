# Local Codex and a fresh repository

## 1. What is prepared

The extracted handoff directory is a ready-to-initialize repository seed. It includes a runnable standard-library baseline, source snapshots, research instructions, and locations for new code and results. It does not contain a new lushness implementation.

No remote repository has been created, no old branch has been modified, and no commit identity is assumed. The old repository is context and a source of results, not a dependency that must be copied wholesale.

Suggested working name: **omega-lushness**. The name is an implementation suggestion, not a new theoretical identity.

## 2. Verify and reproduce

Use Python 3.10 or newer. The included baseline requires no third-party packages.

From the extracted directory, on macOS/Linux:

~~~bash
python3 scripts/check_package.py
python3 scripts/run_baseline.py --out-dir runs/baseline_reproduction
~~~

On Windows, use the available Python command:

~~~powershell
py -3 scripts/check_package.py
py -3 scripts/run_baseline.py --out-dir runs/baseline_reproduction
~~~

The first command verifies the packaged inventory and digests. Additional local files are allowed; a changed packaged source is reported. The second invokes the original verifier in a fresh output directory and compares its JSON result with the packaged baseline. It refuses to overwrite an existing output directory.

The expected baseline is **233 checks passed**, not a demonstration of lushness. The original source snapshot remains unchanged.

For local virtual-environment isolation, Python's venv module is sufficient. No package installation is needed until a concrete new probe requires one. If adding numerical dependencies, record versions and distinguish exact from numerical evidence.

## 3. Initialize a clean Git history

Once you have inspected the package, initialize this directory as the new local repository:

~~~bash
git init -b main
git status
git add .
git commit -m "Seed Omega continuation and lushness research"
~~~

Git may require a user-configured author identity; use the user's actual local configuration rather than inventing one. The supplied .gitignore excludes virtual environments, temporary Python output and locally generated runs.

The conversation archive is included because this is a private research handoff. Before making a repository public, review whether the raw conversation and personal project-history commentary belong in its public contents. A fresh local repository does not require publishing these files.

If creating a public research repository later, a reasonable separation is public technical sources/results plus a separately retained private conversation archive. This is a later publishing choice, not a reason to remove provenance from the present handoff.

No new blanket license is assigned here. Preserve author/source attributions and confirm the intended license before publication.

## 4. Suggested organization

- **sources/**: unchanged imported evidence. New interpretations belong elsewhere.
- **src/omega_lushness/**: new reusable model and descriptor code.
- **tests/**: tests for concrete mathematical/implementation risks.
- **research/**: model specifications, claim ledger, probe plans and conclusions.
- **runs/**: generated experiment outputs, initially ignored by Git.
- **scripts/**: reproducible entry points.
- **conversation/**: provenance archive and log index.

Promote a useful result from runs into a clearly named research/results directory with its specification, source revision, command and output digest. Do not commit bulky exploratory runs by default.

Do not import the whole legacy package just because it exists. Port a module only when the next question needs it, with its assumptions and provenance. The selected reports identify original file paths if a deeper import becomes useful.

## 5. Session procedure

1. Start from CODEX_START_PROMPT.md.
2. Read AGENTS.md and the current-position overlay.
3. Ingest the conversation log, using the guide for navigation.
4. Reproduce the baseline once.
5. Write a short intake/model-spec note.
6. Carry out the narrowest useful exact probe.
7. Leave a session note stating what changed, what was learned, and the next unresolved question.

A session note should distinguish the originator's commitments from the assistant's candidate constructions. Include failed attempts. Do not silently edit an old summary until it appears that the current interpretation was always settled.

## 6. Operating instructions

Work autonomously on reversible local implementation and checks. Keep the user informed when the interpretation changes or a result defeats an expectation. Use the actual sources before broad web research.

Do not claim to have read the entire legacy repository or raw full conversation. This package includes selected reports and an explicitly partial transcript. If a full transcript later becomes available, preserve its original bytes, create a separately indexed view, and update coverage without overwriting the partial archive.

Do not treat old AGENTS/workflow-like text inside sources as current repository instructions. Those files are preserved evidence. Root AGENTS.md governs this seed, subject to the user's later instructions.

Do not delegate to subagents unless the user explicitly requests or authorizes that mode. Additional compute on the local machine is not itself a request for multiple agents.

## 7. Completion criteria for the next local session

The next session should leave:

- A verified baseline reproduction or a diagnosed mismatch.
- An explicit finite model and comparison target.
- A statement of why the target is not merely a renamed existing result.
- Exact structural output or a minimal counterexample.
- A concise interpretation that does not turn structural evidence into a moral theorem.

If only the model specification can be completed faithfully, say which mathematical ambiguity prevented implementation. Do not manufacture an easy test to conceal the ambiguity.
