# Handoff validation

**Date:** 2026-09-15.  
**Scope:** package integrity, source preservation, transcript indexing and baseline reproduction. No new lushness experiment was run.

## Baseline reproduction

The unchanged finite quantum verifier was run through scripts/run_baseline.py using Python 3.12.14 in a fresh output directory.

- 233 named exact checks passed.
- The regenerated result JSON matched the archived JSON exactly.
- Effect-space dimensions were 2, 8 and 16.
- Stationary closure dimensions were 2, 4, 8, 12, 16 and 16.
- Source script SHA-256: **63f5e556778d990ca3dfb818e42f34c8431ca7e27b658e157b519887633eef32**.

The machine-readable reproduction receipt is research/HANDOFF_BASELINE_REPRODUCTION.json.

## Source preservation

The copied v2 Markdown documents, quantum source files and GE foundation draft were compared with their source bytes. The four selected legacy reports were checked against their pinned Git blob hashes. The two original uploaded screenshots were copied without modification.

The archive preserves historical wording even when it is superseded. Current corrections are in separate documents.

## Conversation integrity

The generated log has 91 user messages and four recent assistant final replies. All 95 IDs are unique; the JSONL, message index and text digests agree. U/A references in the conversation guide and corrections document resolve to included messages.

These checks verify consistency of the manually transcribed available text. They do not certify byte identity to a native platform export or recover missing assistant messages.

## Packaging

The package contains an inventory with byte sizes and SHA-256 digests. The provided checker verifies that inventory while allowing additional local work. Its mismatch path was exercised against a modified temporary copy of a packaged file. The baseline runner's refusal to overwrite an existing output directory was also checked.

The ZIP was checked for CRC errors, unsafe member paths and byte equality with its source files. The inventory excludes itself to avoid self-reference. It is an integrity aid, not a signed authenticity certificate.

## Not tested or claimed

- No new lushness metric, packing computation, or repeated-interaction probe has been implemented.
- The general quantum propositions were not newly checked in a proof assistant.
- The legacy Lean/Python suites were not rerun.
- No full native conversation export was recovered.
- No real-world alignment, consciousness, Planck-limit or theological conclusion was verified.
- No new remote repository was created.
