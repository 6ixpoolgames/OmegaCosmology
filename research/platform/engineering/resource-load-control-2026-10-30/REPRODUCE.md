# Restore the source-fed load comparison

Use the repository NumPy/SciPy Python environment on Windows. Restore into
a fresh ignored directory; no historical private run cache is required:

```powershell
python scripts/restore_research_snapshot.py --archive research/platform/engineering/resource-load-control-2026-10-30/SNAPSHOT.zip --out-dir runs/resource-load-restored/frozen
Copy-Item -LiteralPath research/platform/engineering/resource-load-control-2026-10-30/PLAN.json -Destination runs/resource-load-restored/PLAN.json
```

Check the copied PLAN.json hash against frozen/MANIFEST.json's plan_sha256.
Check the repository scripts/resource_load_control.py hash against its frozen
source entry, then run that driver:

```powershell
python scripts/resource_load_control.py run --out-dir runs/resource-load-restored
```

Physical matching is recomputed and frozen before the conditional history
phase. Unqualified matches must remain unscored; never select using entropy.
The source-off laws reuse the source-on conductances and are not refitted.
All outcomes remain in the output. This is one anchor and two separate matches,
not a joint/finite-work match, a spatial gas baseline or an ethical certificate.
