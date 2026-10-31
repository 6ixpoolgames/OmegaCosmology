# Reproduce the bounded P0/T verification

Use the repository testbed Python environment (NumPy/SciPy) on Windows. No ignored historical run cache is required: both source archives and all selected original result bytes are retained here.

First restore into a fresh ignored directory, without execution:

```powershell
python scripts/restore_p0_t_verification.py --evidence-dir research/platform/engineering/p0-t-verification-2026-10-30 --out-dir runs/p0-t-restored
```

Restoration checks the registered plan, every original source and auditor file, and each retained original result. It rejects overwrites and unlisted archive inputs. Verify the repository driver matches its hash in the restored current/MANIFEST.json before executing it:

```powershell
python scripts/run_p0_t_verification.py execute --out-dir runs/p0-t-restored
```

The driver invokes only the frozen worker/native sources under the retained plan and caps. A cap/provenance failure stays incomplete; do not substitute a point or broaden the map. One study point is not its full parameter sweep. Latest Appendix A/B conformance and physical faithfulness are outside this reproduction.
