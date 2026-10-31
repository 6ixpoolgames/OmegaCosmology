# Reproducing the review

The ten manuscript drafts are private author-supplied inputs, not repository
dependencies distributed with this report. To repeat the numerical portion,
use request packet `V42B_CODEX_REQUEST_r7.zip` with the SHA256 recorded in
SOURCE_INPUTS.json. Do not substitute another manuscript revision silently.

From the repository root and its Python environment:

```text
python research/platform/reviews/r7-k-j-review-2026-10-31/analysis/audit_retained.py --packet <local-r7-packet> --out runs/r7-audit-fresh
```

The output must report 124 checks, zero mismatches, 17 verified retained JSON
sources, ten private draft members, and no simulation. Compare the generated
SOURCE_INPUTS.json, NUMERICAL_CHECKS.json and PROFILE_SCOPE.json semantically
or byte-for-byte with this folder. Existing output directories are rejected.
The source filenames, hashes and relative retained-evidence selectors are
preserved; manuscript text is never emitted by the audit script.

The script's explicit figure registry checks the numerical groups cited in
K_REPORT.md. It does not automatically infer a manuscript claim, validate its
meaning, prove physical faithfulness or guarantee every possible textual
paraphrase. Those are the manual inspection component, with covered passages
and correction locations recorded separately. J is a source/thermodynamics
design review; it has no run to reproduce yet. Its cited physics-source bytes
are fingerprinted in J_SOURCE_INPUTS.json.

No package restore, random sampling, matrix solve, new model enumeration or
history-scoring process is part of this audit.
