# Occupied-assistance sprint: S0, S1 feasibility and S2 smoke

25 October 2026. Completed on the author's instruction to proceed and push on
completion. [Numerical report](REPORT.md), [machine-readable evidence](ANALYSIS.json)
and [hash manifest](EVIDENCE.json). This is the implementation sprint specified
by the [programme scope](../../specs/ECOLOGY_PROGRAMME_SCOPE_r1.md).

## Delivered

- [Manuscript evidence packet](../../../evidence/manuscript-handoff-2026-10-25/README.md):
  three reviewed model cards,1010 retained profiles,2571 comparison rows, claim
  mappings, R2 corrections and input receipts. No scientific rerun or manuscript edit.
- Reversible occupied contacts with single-port exclusion, recipient-paid
  conversion, helper opportunity cost and native release/bound failure. An
  occupied helper cannot also use its capture port or assist another substrate.
- Six capped engineering worlds,54–1215 states,12 whole/local profiles at T4/16.
  All pass,85.691s total,611.32MiB peak/job, under1MiB run output including its
  source snapshot. Larger compound ancestry products were deliberately not
  requested; the two small cases verify physical-marginal preservation.
- A finite-sample empirical-Bernstein family interval added to the existing
  projected-history estimator. Six E1 donor contrasts use8192 fixed paths
  apiece across two cadence runs, taking52.215s and27.523s, about160.3MiB peak.

## What became known

Occupied assistance fits the current native grammar. Competition is present
in the event set rather than inserted as a negative score. Energies include the
binding bond. The recipient pays conversion; the helper's cost is lost use of
its finite interface. Source-off detailed balance and source-on energy balances
pass. Fractional bills remain independent of bank capacity and capture yield.

The donor's early history differences remain estimated negative at both.25 and
.5. Approximate pointwise intervals exclude zero in all six requested cases.
The more conservative finite-sample family intervals all include zero. Float64
filter/kernel error also lacks a rigorous enclosure. Therefore the requested
certified donor sign is still unresolved. This is an instrument limitation,
not a reversal of the estimated effect or a judgment of cooperation.

At.25, merely making this particular bound's support-width term smaller than
the current point estimates would require roughly7.18million paths at T16,
1.37million at T64 and2.10million at T256. These are conditional planning
calculations, not sample guarantees: the mean and variance can change with more
data, and numerical error remains. Blindly extending the present run is a poor
next step. Tighter proven score ranges, conditional/tree bounds and numerical
enclosures need a targeted algorithmic investigation if certification is essential.

## Interpretation and next scientific question

This is engineering readiness for a small interaction map. It does not show
that occupied help improves or worsens lushness. The smoke's brief horizons and
single initial roots do not establish repayment, persistence, robust compounding,
symbiosis or domination. Contacts contribute real physical history entropy;
they must remain in the whole quantity. Local projections omit cross contacts
and preserve hidden-state memory in their bounds.

Next, S3 should map source supply and helper residence/competing use in this
same substrate, with local/one-way/reciprocal and nonconverting controls. Precise
donor inference can proceed independently; unresolved private signs cannot be
used to support a private/whole ethical claim. Work/activity matching still
needs a feasible physical comparator. Moving niches and population await S4.

## Reproduction and failures retained

The [engineering plan](../../models/occupied-assistance/ENGINEERING_PLAN.json)
and two [confidence](../../models/projected-confidence/PLAN_dt0p25.json)
[plans](../../models/projected-confidence/PLAN_dt0p5.json) fix the inputs.
Run the named supervisor with `--plan <plan> --out-dir runs/<fresh-name>`.
The report builder's retained command line follows its `--help` interface.

For exact historical reconstruction, restore the retained runtime tree from
each run's `SNAPSHOT.zip`; its MANIFEST.json preserves input bytes. The first
two smoke attempts failed before any profile: root naming setup, then the old
32MiB kernel gate. Both receipts/logs/source versions remain in this packet.
The successful plan explicitly allows128MiB kernel and512MiB occupation
workspace under a4GiB job cap; the world was not shrunk. Current source adds a
root validity preflight; that does not change the successful native law.

Preflight observed31.92GiB total RAM,8.10GiB free and about1612GiB disk free.
Jobs ran serially with4GiB memory caps and a4GiB reserve. No dense kernels or
sampled paths are retained. Logs redact the local checkout prefix and record
their original hashes; numerical result bytes and native inputs are unchanged.

Snapshot archives avoid Windows Git path-length limits. Every archive was
byte-compared against the original files and restored with manifest verification;
[PACKAGING.json](PACKAGING.json) records this. For example:

```text
python scripts/restore_research_snapshot.py --archive research/platform/engineering/occupied-sprint-2026-10-25/occupied-smoke-20261025-r3/SNAPSHOT.zip --out-dir runs/s2-restore
```

Then execute the restored supervisor from runs/s2-restore with its original
plan and a fresh run output. This restores historical inputs without importing
the current package accidentally. It does not launch a run automatically.
