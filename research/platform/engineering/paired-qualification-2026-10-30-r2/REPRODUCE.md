# Restore and replay the scoped qualification

No original local run cache is required. From the repository root, use the
Python environment with NumPy and SciPy on Windows.

```powershell
python scripts/restore_research_snapshot.py --archive research/platform/engineering/paired-qualification-2026-10-30-r2/SNAPSHOT.zip --out-dir runs/paired-qualified-restored/frozen
Copy-Item -LiteralPath research/platform/engineering/paired-qualification-2026-10-30-r2/PLAN.json -Destination runs/paired-qualified-restored/PLAN.json
```

Verify PLAN.json against frozen/MANIFEST.json's plan_sha256. Verify the
repository scripts/qualify_p0_pairs.py hash against its frozen source entry
before dispatching it. The completed validation did both checks. Then:

```powershell
python scripts/qualify_p0_pairs.py run --out-dir runs/paired-qualified-restored
```

Use a fresh output; preserve all results and receipts. The driver executes
only the retained worker/input plan under the recorded caps. Restoration
alone does not run a simulation. Interpretation adds no physical state or
transition, and the common alphabet is not a new generator. A passing
retained-unit contract does not certify chemical closure or ethical claims.
