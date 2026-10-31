# J boundary: physical diagnosis and next comparator

31 October 2026. The user's “Ok go” authorizes the review recommended after
the [physical pilot](../../engineering/joint-resource-load-2026-10-31/REPORT.md).
Completed using retained inputs, results and sensitivities only. No new
model enumeration, stationary solve, parameter fit, history score or simulation.
Earlier evidence and private manuscripts remain unchanged. No commit or push.

## Finding

**The selected fit meets a physical parameter boundary, not a memory limit
or a scoring problem.** The local linear correction to the two target
moments requires a negative locked-load conductance. That is forbidden.
The two direct drains also differ structurally from useful unlocking and
capture: they discharge a resource in one step, whereas the useful pathway
routes part of its energy into the bank through a two-step sequence.

This explains the observed local search behavior. It does **not** prove that
every parameter point in the family is infeasible. The one-start fit and
the local derivative must not be turned into a global impossibility claim.
The original no-match outcome and all evaluated points stay retained.

## What the existing numbers show

Stationary quantities at the common source-.08 boundary:

| Arm | Physical jumps/time | Net work/time | Gross accepted work/time | Returned work/time |
|---|---:|---:|---:|---:|
| Productive | .182404771 | .023797683 | .080718929 | .056921246 |
| Plain ablation | .155662809 | .022168066 | .089477367 | .067309301 |
| Selected two-load control | .160438538 | .024553467 | .094341145 | .069787678 |

Relative to the plain ablation, the useful pathway adds .026741961
jumps/time for .001629617 additional net work/time. The selected control
adds .004775729 jumps/time for .002385401 additional net work/time.
These are differences of stationary means between laws, **not** a causal
assignment of a particular stream of events to a particular energy supply.

Total activity divided by net source work is 7.664812 for the useful arm,
7.021939 for the ablation and 6.534252 for the selected control. This ratio
is descriptive only. Thermal and reverse events are included; some events
consume no external work directly. It is not a microscopic cost per event,
not an efficiency definition and not a proposed normalization of lushness.
It becomes unsuitable as net work approaches zero.

The selected control does not simply fail to obtain enough input. It accepts
more gross work and returns more of it than the useful arm. Its event flux,
resource occupancy and productive use differ. Changing a load cannot be
assumed to turn net work into events at a fixed conversion factor.

## Why the fit reaches its boundary

At the selected point, the stored physical sensitivity is

```text
                         k_L            k_U
event-rate derivative   .774787802    1.093066206
net-work derivative    1.372485004     .540759827
```

The required change from that point to the target is
`(+.021966233 events/time, -.000755784 energy/time)`.
Inverting this stored 2x2 Jacobian gives the linearized step

```text
delta k_L = -.011749976
delta k_U = +.028424601
```

The selected k_L is already approximately zero. The predicted k_L would be
negative; increasing both conductances cannot fix the target in this
linearization. The Jacobian is nonsingular, so this is not merely two
identical knobs masquerading as two degrees of freedom.

A useful local separation check makes the constraint clear. With k_L at
zero and delta k_L nonnegative, decreasing net work requires decreasing k_U.
Substitution into the event-rate derivative gives the coefficient
`a - b*c/d = -1.999488135` on delta k_L. Thus a local decrease in work cannot
also raise events along these feasible linearized directions. The current
point is the observed numerical near-boundary, so this is a limiting tangent
argument, not a finite-neighborhood exclusion theorem.

The algebra reconstructs the desired linearized changes to 6.94e-18 in
the stored units. That checks arithmetic, not the physical accuracy of a
large extrapolation. A curved moment surface or another basin elsewhere
is not excluded. The target's presence in the convex hull of sampled
moments only says mixtures of observations can span it; it does not supply
one static control law. A physical switching selector would be a different,
costed mechanism, with its own events and state.

## What the pathway energies explain

The retained Hamiltonian and native rule changes give these forward
sequence accounts (all reverses remain physical):

| Route | Heat released | Bank increment | Physical transitions |
|---|---:|---:|---:|
| locked3 -> usable2 | 1 | 0 | 1 |
| usable2 -> spent0 plus capture | 1 | 1 | 1 |
| Combined useful sequence | 2 | 1 | 2 |
| Direct locked load -> spent | 3 | 0 | 1 |
| Direct usable load -> spent | 2 | 0 | 1 |

The labels locked3/usable2/spent0 here denote **energies**, not the model's
carrier integer codes (which are 1/2/0). The bank's two-tick increment is
one energy unit. Bank energy can subsequently pay for activation or relax;
it does not disappear from the ledger. The complete long-run energy
account still balances.

The two current load parameters choose how fast to discharge different
carrier states in one step. They do not supply a separate multistep
dissipation pathway. In addition, these drains change the availability of
usable fuel and therefore the bank and assembly occupancy. In the retained
stationary data, the useful arm has usable-carrier probability .426499,
bank energy 1.353734 and bond probability .464409; the selected control has
.316130, 1.193865 and .429033 respectively.

This is a structural explanation consistent with the observed map, not a
proof that one-step disposal alone makes joint matching impossible. Basal
unlocking and capture still operate in the control; futile or thermal
activity still counts. Energy destinations explain the intervention;
they do not determine a history-entropy ranking without a history law.

## Recommendation

Do not widen the numerical search merely because a second parameter was
expected to be enough. First change the question from “which rates give
the answer?” to “which explicit physical pathway supplies the missing
activity/work relation?”

The most useful next candidate is a **two-step discharge through a physically
resolved intermediate conformation of the same carrier**, while keeping
that conformation and its thermal dynamics in both arms. It would release
energy to heat without adding a direct bank-capture step. This addresses
the path-length difference more directly than adding another one-step drain.

The [prospective design](NEXT_CONTROL_DESIGN.md) specifies the shared
background, energy destinations and qualification gates. It is a new
version of the substrate, not another fit of old J and not a proof of a
successful future match. Both targets must be recomputed. The intermediate
must be an actual represented physical state with a residence time and
energy, not an event label, hidden clock or bookkeeping counter.

This is the recommended next engineering candidate, **not an experiment
executed in this review**. If a physically justified intermediate cannot be
specified, leave the joint comparison open rather than manufacture one.
The existing separate activity/work comparisons remain evidence with
their stated limitations; this failed comparator search does not change them.

## Evidence and checks

[ANALYSIS.json](ANALYSIS.json) retains the source hashes, exact figures,
stored-Jacobian calculation, source-current identities and independently
derived energy differences. The review imports no test-bed backend and
calculates no new physical process. Its [script](analysis/review_boundary.py)
can be rerun into a fresh ignored directory with `--out-dir`; it verifies
its inputs against J's existing evidence manifest.

[VALIDATION.json](VALIDATION.json) separates these algebra/source checks
from the preceding 203-test implementation validation. No test suite or
physical qualification is claimed for the unimplemented next design.
